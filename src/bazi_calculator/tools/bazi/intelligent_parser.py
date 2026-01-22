"""智能八字解析和计算工具

集成LLM输入解析和八字计算功能
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime

from langchain_core.tools import tool

from bazi_calculator.tools.bazi.llm_time_parser import LLMTimeParser, ParsedBirthInfo
from bazi_calculator.core.calendar import BaziCalendar


class IntelligentBaziCalculator:
    """智能八字计算器

    使用LLM解析用户输入，然后进行八字计算
    """

    def __init__(self, llm):
        """
        初始化智能八字计算器

        Args:
            llm: LangChain LLM实例
        """
        self.llm = llm
        self.parser = LLMTimeParser(llm)

    def calculate_from_natural_language(self, user_input: str) -> Dict[str, Any]:
        """
        从自然语言输入计算八字

        Args:
            user_input: 用户的自然语言输入，如"我出生于1999年10月17日凌晨3点，男性"

        Returns:
            包含解析结果和八字计算结果的字典
        """
        # 1. 使用LLM解析用户输入
        parsed_info = self.parser.parse_with_fallback(user_input)

        # 2. 转换为BirthInfo
        birth_info = parsed_info.to_birth_info()

        # 3. 计算八字
        bazi_result = BaziCalendar.get_all_pillars(birth_info.date)

        # 4. 组装返回结果
        result = {
            "original_input": user_input,
            "parsed_info": {
                "year": parsed_info.year,
                "month": parsed_info.month,
                "day": parsed_info.day,
                "hour": parsed_info.hour,
                "minute": parsed_info.minute,
                "gender": parsed_info.gender,
                "calendar_type": parsed_info.calendar_type,
                "formatted_time": f"{parsed_info.year}年{parsed_info.month}月{parsed_info.day}日 {parsed_info.hour:02d}时{parsed_info.minute:02d}分"
            },
            "bazi": {
                "year": {
                    "gan": bazi_result["year"]["gan"],
                    "zhi": bazi_result["year"]["zhi"],
                    "full": bazi_result["year"]["full"],
                    "gan_wuxing": bazi_result["year"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["year"]["zhi_wuxing"]
                },
                "month": {
                    "gan": bazi_result["month"]["gan"],
                    "zhi": bazi_result["month"]["zhi"],
                    "full": bazi_result["month"]["full"],
                    "gan_wuxing": bazi_result["month"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["month"]["zhi_wuxing"],
                    "jieqi": bazi_result["month"]["jieqi"]
                },
                "day": {
                    "gan": bazi_result["day"]["gan"],
                    "zhi": bazi_result["day"]["zhi"],
                    "full": bazi_result["day"]["full"],
                    "gan_wuxing": bazi_result["day"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["day"]["zhi_wuxing"],
                    "day_master": bazi_result["day"]["gan"]
                },
                "hour": {
                    "gan": bazi_result["hour"]["gan"],
                    "zhi": bazi_result["hour"]["zhi"],
                    "full": bazi_result["hour"]["full"],
                    "gan_wuxing": bazi_result["hour"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["hour"]["zhi_wuxing"]
                }
            },
            "bazi_result": {
                "year": {
                    "full": bazi_result["year"]["full"],
                    "gan_wuxing": bazi_result["year"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["year"]["zhi_wuxing"]
                },
                "month": {
                    "full": bazi_result["month"]["full"],
                    "gan_wuxing": bazi_result["month"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["month"]["zhi_wuxing"],
                    "jieqi": bazi_result["month"]["jieqi"]
                },
                "day": {
                    "full": bazi_result["day"]["full"],
                    "gan_wuxing": bazi_result["day"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["day"]["zhi_wuxing"],
                    "day_master": bazi_result["day"]["day_master"]
                },
                "hour": {
                    "full": bazi_result["hour"]["full"],
                    "gan_wuxing": bazi_result["hour"]["gan_wuxing"],
                    "zhi_wuxing": bazi_result["hour"]["zhi_wuxing"]
                }
            },
            "success": True
        }

        return result

    def format_result(self, result: Dict[str, Any]) -> str:
        """
        格式化输出结果

        Args:
            result: calculate_from_natural_language的返回结果

        Returns:
            格式化的字符串
        """
        output_lines = [
            f"原始输入：{result['original_input']}",
            f"",
            f"解析信息：",
            f"出生时间：{result['parsed_info']['formatted_time']}",
            f"性别：{result['parsed_info']['gender']}",
            f"历法：{result['parsed_info']['calendar_type']}",
            f"",
            f"【八字四柱】"
        ]

        bazi = result['bazi_result']
        output_lines.extend([
            f"年柱：{bazi['year']['full']}（{bazi['year']['gan_wuxing']} {bazi['year']['zhi_wuxing']}）",
            f"月柱：{bazi['month']['full']}（{bazi['month']['gan_wuxing']} {bazi['month']['zhi_wuxing']}）节气：{bazi['month']['jieqi']}",
            f"日柱：{bazi['day']['full']}（{bazi['day']['gan_wuxing']} {bazi['day']['zhi_wuxing']}）日主：{bazi['day']['day_master']}",
            f"时柱：{bazi['hour']['full']}（{bazi['hour']['gan_wuxing']} {bazi['hour']['zhi_wuxing']}）"
        ])

        return '\n'.join(output_lines)


@tool
def parse_and_calculate_bazi(user_input: str, llm=None) -> Dict[str, Any]:
    """解析自然语言输入并计算八字

    支持多种输入格式：
    - "我出生于1999年10月17日凌晨3点，男性"
    - "2025年12月30日下午6点，女的，公历"
    - "男孩，出生在甲辰年二月十五日上午10点"

    Args:
        user_input: 用户的自然语言输入
        llm: LangChain LLM实例（可选，用于后续集成）

    Returns:
        包含解析结果和八字计算结果的字典
    """
    # 这里为了演示，暂时不使用LLM，实际使用时需要传入llm参数
    # 在完整集成时，可以通过Agent的上下文获取llm实例
    if llm is None:
        # 创建临时LLM实例（实际使用时应该从环境配置）
        try:
            from langchain_openai import ChatOpenAI
            import os
            import dotenv
            dotenv.load_dotenv()

            # 获取API配置
            api_key = os.getenv("QWEN_API_KEY") or os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("QWEN_BASE_URL") or os.getenv("OPENAI_BASE_URL")
            model = os.getenv("QWEN_MODEL", "qwen-flash")

            if not api_key:
                raise ValueError("未找到API密钥，请配置QWEN_API_KEY或OPENAI_API_KEY")

            # 直接传递API密钥，而不是依赖环境变量
            llm_kwargs = {
                "model": model,
                "api_key": api_key,
                "temperature": 0
            }

            if base_url:
                llm_kwargs["base_url"] = base_url

            llm = ChatOpenAI(**llm_kwargs)
        except Exception as e:
            raise ValueError(f"LLM初始化失败: {str(e)}")

    calculator = IntelligentBaziCalculator(llm)
    result = calculator.calculate_from_natural_language(user_input)
    return result