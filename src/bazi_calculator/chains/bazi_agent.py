"""八字Agent
 
 整合所有八字计算工具，提供统一接口
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI

from bazi_calculator.core.calendar import BaziCalendar
from bazi_calculator.core.wuxing import WuxingAnalyzer
from bazi_calculator.tools.bazi.time_parser import parse_birth_time
from bazi_calculator.tools.bazi.year_pillar import calculate_year_pillar
from bazi_calculator.tools.bazi.month_pillar import calculate_month_pillar
from bazi_calculator.tools.bazi.day_pillar import calculate_day_pillar
from bazi_calculator.tools.bazi.hour_pillar import calculate_hour_pillar
from bazi_calculator.tools.bazi.wuxing_analysis import analyze_wuxing


class BaziAgent:
    """八字计算Agent

    整合所有八字计算工具，提供完整的八字计算和五行分析功能
    """

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """初始化八字Agent

        Args:
            llm: 语言模型实例，如果为None则使用默认Qwen
        """
        self.llm = llm or ChatOpenAI(
            model=os.getenv('QWEN_MODEL', 'qwen-flash'),
            api_key=os.getenv('QWEN_API_KEY'),
            base_url=os.getenv('QWEN_BASE_URL'),
            temperature=0.3
        )

    def calculate_bazi(
        self,
        time_description: str,
        gender: str,
        calendar_type: str = "公历"
    ) -> Dict[str, Any]:
        """计算完整的八字

        Args:
            time_description: 时间描述
            gender: 性别
            calendar_type: 历法类型

        Returns:
            完整的八字结果
        """
        # 解析时间
        birth_info = parse_birth_time.invoke(
            {"time_description": time_description, "gender": gender, "calendar_type": calendar_type}
        )

        birth_date = datetime(
            birth_info["year"],
            birth_info["month"],
            birth_info["day"],
            birth_info["hour"],
            birth_info["minute"],
        )

        # 计算四柱（直接调用核心函数，避免Tool装饰器的验证问题）
        year_pillar = BaziCalendar.get_year_pillar(birth_date)
        month_pillar = BaziCalendar.get_month_pillar(
            birth_date,
            year_pillar[0]  # gan
        )
        day_pillar = BaziCalendar.get_day_pillar(birth_date)
        hour_pillar = BaziCalendar.get_hour_pillar(
            birth_date,
            day_pillar[0],  # gan
        )

        # 组装八字
        bazi = {
            "year": {
                "gan": year_pillar[0],
                "zhi": year_pillar[1],
                "gan_wuxing": year_pillar[2],
                "zhi_wuxing": year_pillar[3],
                "full": year_pillar[0] + year_pillar[1]
            },
            "month": {
                "gan": month_pillar[0],
                "zhi": month_pillar[1],
                "gan_wuxing": month_pillar[2],
                "zhi_wuxing": month_pillar[3],
                "full": month_pillar[0] + month_pillar[1],
                "jieqi": month_pillar[4]
            },
            "day": {
                "gan": day_pillar[0],
                "zhi": day_pillar[1],
                "gan_wuxing": day_pillar[2],
                "zhi_wuxing": day_pillar[3],
                "full": day_pillar[0] + day_pillar[1],
                "day_master": day_pillar[0]
            },
            "hour": {
                "gan": hour_pillar[0],
                "zhi": hour_pillar[1],
                "gan_wuxing": hour_pillar[2],
                "zhi_wuxing": hour_pillar[3],
                "full": hour_pillar[0] + hour_pillar[1]
            },
        }

        # 五行分析
        wuxing_analysis = WuxingAnalyzer.analyze_comprehensive(bazi)

        return {
            "birth_info": birth_info,
            "bazi": bazi,
            "wuxing_analysis": wuxing_analysis,
        }

    def format_bazi_result(self, result: Dict[str, Any]) -> str:
        """格式化八字结果为文本

        Args:
            result: 八字计算结果

        Returns:
            格式化后的文本
        """
        birth_info = result["birth_info"]
        bazi = result["bazi"]
        wuxing = result["wuxing_analysis"]

        output = []
        output.append("=" * 50)
        output.append("八字计算结果")
        output.append("=" * 50)

        # 出生信息
        output.append("\n【出生信息】")
        output.append(f"出生时间：{birth_info['year']}年{birth_info['month']}月{birth_info['day']}日 "
                    f"{birth_info['hour']:02d}时{birth_info['minute']:02d}分")
        output.append(f"性别：{birth_info['gender']}")
        output.append(f"历法：{birth_info.get('calendar_type', '公历')}")

        # 八字四柱
        output.append("\n【八字四柱】")
        output.append(f"年柱：{bazi['year']['full']}（{bazi['year']['gan_wuxing']} {bazi['year']['zhi_wuxing']}）")
        output.append(f"月柱：{bazi['month']['full']}（{bazi['month']['gan_wuxing']} {bazi['month']['zhi_wuxing']}）节气：{bazi['month']['jieqi']}")
        output.append(f"日柱：{bazi['day']['full']}（{bazi['day']['gan_wuxing']} {bazi['day']['zhi_wuxing']}）日主：{bazi['day']['gan']}")
        output.append(f"时柱：{bazi['hour']['full']}（{bazi['hour']['gan_wuxing']} {bazi['hour']['zhi_wuxing']}）")

        # 五行分析
        output.append("\n【五行统计】")
        wuxing_count = wuxing["wuxing_count"]
        output.append(f"木：{wuxing_count.get('木', 0)}个")
        output.append(f"火：{wuxing_count.get('火', 0)}个")
        output.append(f"土：{wuxing_count.get('土', 0)}个")
        output.append(f"金：{wuxing_count.get('金', 0)}个")
        output.append(f"水：{wuxing_count.get('水', 0)}个")

        # 日主强弱
        output.append("\n【日主分析】")
        output.append(f"日主：{wuxing['summary']['day_master']}（{wuxing['summary']['day_master_wuxing']}）")
        output.append(f"强弱：{wuxing['strength']}")

        # 用神
        output.append("\n【用神分析】")
        yong_shen_info = wuxing.get("yong_shen_info", {})
        output.append(f"用神：{yong_shen_info.get('yong_shen', '')}")
        output.append(f"喜神：{yong_shen_info.get('xi_shen', '')}")
        output.append(f"忌神：{', '.join(yong_shen_info.get('ji_shen', []))}")

        output.append("\n" + "=" * 50)

        return "\n".join(output)

    def get_tools(self) -> list:
        """获取所有可用的工具

        Returns:
            工具列表
        """
        return [
            parse_birth_time,
            calculate_year_pillar,
            calculate_month_pillar,
            calculate_day_pillar,
            calculate_hour_pillar,
            analyze_wuxing,
        ]
