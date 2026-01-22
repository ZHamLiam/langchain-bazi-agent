"""交互式八字取名Agent

 整合所有功能，提供完整的交互式八字取名服务
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from langchain_openai import ChatOpenAI

from bazi_calculator.chains.bazi_agent import BaziAgent
from bazi_calculator.tools.naming import (
    analyze_bazi_for_naming,
    get_suitable_chars,
    generate_name_suggestions,
    generate_batch_names,
    comprehensive_name_analysis,
    format_comprehensive_analysis,
)
from bazi_calculator.tools.naming.char_library_generator import generate_character_library
from bazi_calculator.data.char_database import CharacterDatabase


class InteractiveBaziNamingAgent:
    """交互式八字取名Agent

    提供完整的八字计算和取名服务
    """

    def __init__(self, llm: Optional[ChatOpenAI] = None, char_library_path: Optional[str] = None):
        """初始化交互式Agent

        Args:
            llm: 语言模型实例
            char_library_path: 字库文件路径
        """
        self.llm = llm or ChatOpenAI(
            model=os.getenv('QWEN_MODEL', 'qwen-flash'),
            api_key=os.getenv('QWEN_API_KEY'),
            base_url=os.getenv('QWEN_BASE_URL'),
            temperature=0.7
        )
        self.bazi_agent = BaziAgent(llm)
        self.char_library_path = char_library_path
        self.char_library = {}

        # 加载或生成字库
        self._load_or_generate_char_library()

        # 初始化数据库
        self.db = CharacterDatabase(char_library_path)
        if self.char_library:
            self.db.set_char_library(self.char_library)

    def _load_or_generate_char_library(self):
        """加载或生成字库"""
        if self.char_library_path and Path(self.char_library_path).exists():
            try:
                with open(self.char_library_path, 'r', encoding='utf-8') as f:
                    self.char_library = json.load(f)
                print(f"已加载字库：{self.char_library_path}")
            except Exception as e:
                print(f"加载字库失败，将生成新字库：{e}")
                self._generate_char_library()
        else:
            print("字库不存在，正在生成...")
            self._generate_char_library()

    def _generate_char_library(self):
        """生成字库"""
        try:
            result = generate_character_library.invoke({
                "wuxing_categories": ["木", "火", "土", "金", "水"],
                "count_per_category": 50
            })

            self.char_library = result

            if self.char_library_path:
                from bazi_calculator.tools.naming.char_library_generator import save_character_library
                save_character_library.invoke({
                    "char_library": self.char_library,
                    "filepath": self.char_library_path
                })

            print("字库生成完成")
        except Exception as e:
            print(f"生成字库失败：{e}")
            self.char_library = {}

    def calculate_bazi(
        self,
        time_description: str,
        gender: str,
        calendar_type: str = "公历"
    ) -> Dict[str, Any]:
        """计算八字

        Args:
            time_description: 时间描述
            gender: 性别
            calendar_type: 历法类型

        Returns:
            八字计算结果
        """
        return self.bazi_agent.calculate_bazi(time_description, gender, calendar_type)

    def display_bazi_result(self, bazi_result: Dict[str, Any]):
        """显示八字计算结果

        Args:
            bazi_result: 八字计算结果
        """
        formatted = self.bazi_agent.format_bazi_result(bazi_result)
        print(formatted)

    def ask_need_naming(self) -> bool:
        """询问是否需要取名

        Returns:
            是否需要取名
        """
        while True:
            response = input("\n是否需要取名建议？（y/n）: ").strip().lower()
            if response in ['y', 'yes', '是']:
                return True
            elif response in ['n', 'no', '否']:
                return False
            else:
                print("请输入 y/n 或 是/否")

    def generate_suitable_chars(
        self,
        bazi_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成适合字列表

        Args:
            bazi_result: 八字计算结果

        Returns:
            适合字列表
        """
        # 八字分析
        bazi_analysis = analyze_bazi_for_naming.invoke(bazi_result["bazi"])

        # 获取适合字
        suitable = get_suitable_chars.invoke({
            "bazi_analysis": bazi_analysis,
            "char_library": self.char_library,
            "count_per_wuxing": 25
        })

        return suitable

    def display_suitable_chars(self, suitable_chars: Dict[str, Any]):
        """显示适合字列表

        Args:
            suitable_chars: 适合字字典
        """
        from bazi_calculator.tools.naming.suitable_chars import format_suitable_chars
        formatted = format_suitable_chars.invoke(suitable_chars)
        print(formatted)

    def ask_batch_naming(self) -> bool:
        """询问是否批量取名

        Returns:
            是否批量取名
        """
        while True:
            response = input("\n是否需要批量生成名字（20-30个）？（y/n）: ").strip().lower()
            if response in ['y', 'yes', '是']:
                return True
            elif response in ['n', 'no', '否']:
                return False
            else:
                print("请输入 y/n 或 是/否")

    def ask_user_selection(self, suitable_chars: Dict[str, Any]) -> List[str]:
        """询问用户选择心仪字

        Args:
            suitable_chars: 适合字字典

        Returns:
            用户选择的字列表
        """
        print("\n请从适合字列表中选择您心仪的字（可以输入多个字，用空格分隔）")
        print("如果不选择，将自动组合生成名字")

        selected = input("请输入您心仪的字（留空则不选择）: ").strip()

        if selected:
            return selected.split()
        else:
            return []

    def generate_name_suggestions(
        self,
        bazi_result: Dict[str, Any],
        count: int = 10
    ) -> Dict[str, Any]:
        """生成名字建议（精选版）

        Args:
            bazi_result: 八字计算结果
            count: 生成数量，默认10个

        Returns:
            名字建议
        """
        bazi_analysis = analyze_bazi_for_naming.invoke(bazi_result["bazi"])

        result = generate_name_suggestions.invoke({
            "bazi_analysis": bazi_analysis,
            "count": count
        })

        return result

    def generate_batch_names(
        self,
        bazi_result: Dict[str, Any],
        suitable_chars: Dict[str, Any],
        user_selected_chars: Optional[List[str]] = None,
        count: int = 30
    ) -> Dict[str, Any]:
        """批量生成名字

        Args:
            bazi_result: 八字计算结果
            suitable_chars: 适合字字典
            user_selected_chars: 用户选择的字（可选）
            count: 生成数量，默认30个

        Returns:
            批量名字建议
        """
        bazi_analysis = analyze_bazi_for_naming.invoke(bazi_result["bazi"])

        result = generate_batch_names.invoke({
            "suitable_chars": suitable_chars,
            "bazi_analysis": bazi_analysis,
            "user_selected_chars": user_selected_chars,
            "count": count
        })

        return result

    def display_name_suggestions(self, name_result: Dict[str, Any]):
        """显示名字建议

        Args:
            name_result: 名字建议结果
        """
        from bazi_calculator.tools.naming.name_generator import format_name_suggestions
        formatted = format_name_suggestions.invoke(name_result["names"])
        print(formatted)

    def display_batch_names(self, batch_result: Dict[str, Any]):
        """显示批量名字建议

        Args:
            batch_result: 批量名字结果
        """
        from bazi_calculator.tools.naming.batch_name_generator import format_batch_names
        formatted = format_batch_names.invoke(batch_result["names"])
        print(formatted)

    def user_select_name(self, name_list: List[str]) -> Optional[str]:
        """用户选择心仪名字

        Args:
            name_list: 名字列表

        Returns:
            用户选择的名字，如果选择"退出"则返回None
        """
        print('\n请输入您想详细了解的名字编号，或输入"退出"结束')
        response = input("请输入: ").strip()

        if response.lower() in ['exit', '退出', 'quit']:
            return None

        try:
            index = int(response) - 1
            if 0 <= index < len(name_list):
                return name_list[index]
            else:
                print("编号无效，请重新选择")
                return None
        except ValueError:
            print("请输入有效的编号")
            return None

    def analyze_selected_name(
        self,
        name: str,
        bazi_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """详细分析选中的名字

        Args:
            name: 名字
            bazi_result: 八字计算结果

        Returns:
            详细分析结果
        """
        bazi_analysis = analyze_bazi_for_naming.invoke(bazi_result["bazi"])

        result = comprehensive_name_analysis.invoke({
            "name": name,
            "bazi_analysis": bazi_analysis,
            "char_library": self.char_library,
            "surname": "李"
        })

        return result

    def display_name_analysis(self, analysis: Dict[str, Any]):
        """显示名字详细分析

        Args:
            analysis: 分析结果
        """
        formatted = format_comprehensive_analysis.invoke(analysis)
        print(formatted)

    def ask_continue_analysis(self) -> bool:
        """询问是否继续分析其他名字

        Returns:
            是否继续
        """
        while True:
            response = input("\n是否继续分析其他名字？（y/n）: ").strip().lower()
            if response in ['y', 'yes', '是']:
                return True
            elif response in ['n', 'no', '否']:
                return False
            else:
                print("请输入 y/n 或 是/否")

    def run_interactive_session(
        self,
        time_description: str,
        gender: str,
        calendar_type: str = "公历"
    ):
        """运行完整的交互式取名会话

        Args:
            time_description: 时间描述
            gender: 性别
            calendar_type: 历法类型
        """
        print("=" * 60)
        print("八字取名交互系统")
        print("=" * 60)

        # 1. 计算八字
        print("\n正在计算八字...")
        bazi_result = self.calculate_bazi(time_description, gender, calendar_type)
        self.display_bazi_result(bazi_result)

        # 2. 询问是否需要取名
        if not self.ask_need_naming():
            print("\n感谢使用八字取名系统！")
            return

        # 3. 生成适合字列表
        print("\n正在生成适合字列表...")
        suitable_chars = self.generate_suitable_chars(bazi_result)
        self.display_suitable_chars(suitable_chars)

        # 4. 询问是否批量取名
        if self.ask_batch_naming():
            # 批量取名流程
            user_selected = self.ask_user_selection(suitable_chars)

            print("\n正在批量生成名字...")
            batch_result = self.generate_batch_names(
                bazi_result,
                suitable_chars,
                user_selected,
                count=30
            )

            self.display_batch_names(batch_result)

            # 从批量结果中选择分析
            name_list = [name_info["name"] for name_info in batch_result["names"]]

            while True:
                selected_name = self.user_select_name(name_list)

                if selected_name is None:
                    break

                print(f"\n正在分析名字：{selected_name}")
                analysis = self.analyze_selected_name(selected_name, bazi_result)
                self.display_name_analysis(analysis)

                if not self.ask_continue_analysis():
                    break
        else:
            # 精选名字流程
            print("\n正在生成精选名字建议...")
            name_result = self.generate_name_suggestions(bazi_result, count=10)
            self.display_name_suggestions(name_result)

            name_list = [name_info["name"] for name_info in name_result["names"]]

            while True:
                selected_name = self.user_select_name(name_list)

                if selected_name is None:
                    break

                print(f"\n正在分析名字：{selected_name}")
                analysis = self.analyze_selected_name(selected_name, bazi_result)
                self.display_name_analysis(analysis)

                if not self.ask_continue_analysis():
                    break

        print("\n" + "=" * 60)
        print("感谢使用八字取名系统！")
        print("=" * 60)


def main():
    """主函数 - 命令行入口"""
    print("\n欢迎使用八字取名系统")
    print("=" * 60)

    # 获取用户输入
    time_description = input("请输入出生时间（如：2024年3月15日10点30分）: ").strip()
    gender = input("请输入性别（男/女）: ").strip()

    calendar_types = ["公历", "农历"]
    calendar_type = input(f"请选择历法类型（{'/'.join(calendar_types)}，默认公历）: ").strip()

    if not calendar_type or calendar_type not in calendar_types:
        calendar_type = "公历"

    # 创建并运行交互式Agent
    agent = InteractiveBaziNamingAgent(
        char_library_path="char_library.json"
    )

    agent.run_interactive_session(time_description, gender, calendar_type)


if __name__ == "__main__":
    main()
