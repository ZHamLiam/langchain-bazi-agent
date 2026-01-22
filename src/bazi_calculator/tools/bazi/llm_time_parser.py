"""基于LLM的智能八字输入解析工具

使用大语言模型解析用户的自然语言输入，输出结构化的八字计算所需信息
"""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from bazi_calculator.models.schemas import BirthInfo


class ParsedBirthInfo(BaseModel):
    """解析后的出生信息"""
    year: int = Field(description="年份，如2024")
    month: int = Field(description="月份，1-12")
    day: int = Field(description="日期，1-31")
    hour: int = Field(default=0, description="小时，0-23")
    minute: int = Field(default=0, description="分钟，0-59")
    gender: str = Field(description="性别，'男'或'女'")
    calendar_type: str = Field(default="公历", description="历法类型，'公历'或'农历'")
    original_input: str = Field(description="用户的原始输入")

    def to_birth_info(self):
        """转换为BirthInfo对象"""
        from datetime import datetime
        return BirthInfo(
            date=datetime(self.year, self.month, self.day, self.hour, self.minute),
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=0,
            gender=self.gender,
            calendar_type=self.calendar_type
        )


class LLMTimeParser:
    """基于LLM的时间解析器"""

    def __init__(self, llm):
        """
        初始化LLM时间解析器

        Args:
            llm: LangChain LLM实例
        """
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ParsedBirthInfo)
        self.prompt = self._create_prompt()

    def _create_prompt(self) -> ChatPromptTemplate:
        """创建解析提示词"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的八字时间信息提取专家。你的任务是从用户的自然语言输入中提取出生时间、性别和历法信息。

提取规则：
1. 时间提取：
   - 支持多种格式：2024年3月15日、2024.3.15、2024/03/15、二零二四年三月十五日等
   - 时间部分：上午10点、10:30、十点三十分、23:30、下午3点等
   - 如果只提到日期没有具体时间，默认设为0:0
   - 将"上午/早上/清晨"等转换为对应的小时数（如上午10点 -> 10:00）
   - 将"下午/中午/晚上"等转换为对应的小时数（如下午3点 -> 15:00）
   - 将"凌晨/半夜"等转换为对应的小时数（如凌晨2点 -> 2:00）

2. 性别提取：
   - 识别：男、女、先生、女士、男孩、女孩等
   - 必须输出'男'或'女'

3. 历法类型：
   - 默认为'公历'
   - 如果明确提到农历、阴历、旧历等，设为'农历'

4. 输出要求：
   - 年份必须为4位数字
   - 月份和日期必须为数字
   - 小时范围：0-23
   - 分钟范围：0-59
   - 所有字段都必须提供值，不能为空

示例：
用户输入："我出生于1999年10月17日凌晨3点，男性"
输出：year=1999, month=10, day=17, hour=3, minute=0, gender='男', calendar_type='公历'

用户输入："2025年12月30日下午6点，女的"
输出：year=2025, month=12, day=30, hour=18, minute=0, gender='女', calendar_type='公历'"""),
            ("user", "{input}\n\n请按照要求提取时间信息：{format_instructions}")
        ])

        return prompt

    def parse(self, user_input: str) -> ParsedBirthInfo:
        """
        解析用户输入

        Args:
            user_input: 用户的自然语言输入

        Returns:
            ParsedBirthInfo对象
        """
        chain = self.prompt | self.llm | self.parser
        result = chain.invoke({
            "input": user_input,
            "format_instructions": self.parser.get_format_instructions()
        })
        result.original_input = user_input
        return result

    def parse_with_fallback(self, user_input: str, max_retries: int = 3) -> ParsedBirthInfo:
        """
        带重试机制的解析

        Args:
            user_input: 用户的自然语言输入
            max_retries: 最大重试次数

        Returns:
            ParsedBirthInfo对象
        """
        for attempt in range(max_retries):
            try:
                return self.parse(user_input)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise ValueError(f"解析失败，已重试{max_retries}次: {str(e)}")
                continue