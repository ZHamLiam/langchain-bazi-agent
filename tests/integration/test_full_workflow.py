"""测试完整工作流程"""

import pytest
from datetime import datetime

from bazi_calculator.chains.bazi_agent import BaziAgent
from bazi_calculator.tools.bazi import parse_birth_time
from bazi_calculator.tools.naming import (
    analyze_bazi_for_naming,
    get_suitable_chars,
    comprehensive_name_analysis,
)
from bazi_calculator.data import KangxiStrokes, ZodiacRules, PingzePatterns


class TestFullWorkflow:
    """测试完整工作流程"""

    def setup_method(self):
        """设置测试环境"""
        self.test_time = "2024年3月15日10点30分"
        self.test_gender = "男"

    def test_complete_bazi_workflow(self):
        """测试完整八字计算流程"""
        # 1. 解析时间
        birth_info = parse_birth_time.invoke({
            "time_description": self.test_time,
            "gender": self.test_gender,
            "calendar_type": "公历"
        })

        assert birth_info["year"] == 2024
        assert birth_info["month"] == 3
        assert birth_info["day"] == 15

        # 2. 创建Agent并计算八字
        agent = BaziAgent()
        result = agent.calculate_bazi(self.test_time, self.test_gender)

        assert "birth_info" in result
        assert "bazi" in result
        assert "wuxing_analysis" in result

        # 3. 验证八字四柱
        bazi = result["bazi"]
        assert "year" in bazi
        assert "month" in bazi
        assert "day" in bazi
        assert "hour" in bazi

        assert len(bazi["year"]["full"]) == 2
        assert len(bazi["month"]["full"]) == 2
        assert len(bazi["day"]["full"]) == 2
        assert len(bazi["hour"]["full"]) == 2

    def test_bazi_to_naming_workflow(self):
        """测试八字到取名的流程"""
        # 1. 计算八字
        agent = BaziAgent()
        bazi_result = agent.calculate_bazi(self.test_time, self.test_gender)

        # 2. 八字分析
        bazi_analysis = analyze_bazi_for_naming.invoke(bazi_result["bazi"])

        assert "zodiac" in bazi_analysis
        assert "yong_shen" in bazi_analysis
        assert "xi_shen" in bazi_analysis

        # 3. 验证生肖
        assert bazi_analysis["zodiac"] in ZodiacRules.ZODIACS

        # 4. 验证用神
        valid_wuxing = ["木", "火", "土", "金", "水"]
        assert bazi_analysis["yong_shen"] in valid_wuxing or bazi_analysis["yong_shen"] == ""

    def test_data_modules_consistency(self):
        """测试数据模块一致性"""
        # 测试康熙笔画数据
        strokes = KangxiStrokes.get_strokes("张")
        assert strokes is not None
        assert strokes > 0

        # 测试生肖规则
        zodiac = ZodiacRules.get_zodiac_by_year(2024)
        assert zodiac == "龙"
        favor_radicals = ZodiacRules.get_favor_radicals(zodiac)
        assert isinstance(favor_radicals, list)

        # 测试平仄数据
        pingze = PingzePatterns.get_pingze("张")
        assert pingze in ["平", "仄", None]


class TestDataValidation:
    """数据验证测试"""

    def test_kangxi_strokes_database(self):
        """测试康熙字典笔画数据库"""
        test_chars = ["张", "三", "李", "王", "木"]

        for char in test_chars:
            strokes = KangxiStrokes.get_strokes(char)
            assert strokes is not None
            assert strokes > 0
            assert strokes < 50

    def test_zodiac_rules_completeness(self):
        """测试生肖规则完整性"""
        all_zodiacs = ZodiacRules.ZODIACS

        for zodiac in all_zodiacs:
            rules = ZodiacRules.get_all_rules(zodiac)

            assert "favor" in rules
            assert "avoid" in rules
            assert "favor_chars" in rules
            assert "avoid_chars" in rules

            assert isinstance(rules["favor"], list)
            assert isinstance(rules["avoid"], list)

    def test_pingze_patterns_completeness(self):
        """测试平仄数据完整性"""
        pingze_data = PingzePatterns.PINGZE_DATA

        if len(pingze_data) > 0:
            for char, tone in pingze_data.items():
                assert isinstance(char, str)
                assert tone in [1, 2, 3, 4]


class TestNamingAnalysisWorkflow:
    """取名分析工作流程测试"""

    def setup_method(self):
        """设置测试环境"""
        self.test_name = "张三"
        self.surname = "张"

    def test_complete_naming_analysis(self):
        """测试完整取名分析流程"""
        # 模拟字库
        mock_char_library = {
            "木": [
                {
                    "char": "木",
                    "pinyin": "mù",
                    "wuxing": "木",
                    "kangxi_strokes": 4,
                    "zodiac_favor": [],
                    "zodiac_avoid": [],
                    "pingze": "仄",
                    "meaning": "树木",
                    "score": 50
                }
            ],
            "火": [
                {
                    "char": "火",
                    "pinyin": "huǒ",
                    "wuxing": "火",
                    "kangxi_strokes": 4,
                    "zodiac_favor": [],
                    "zodiac_avoid": [],
                    "pingze": "仄",
                    "meaning": "火焰",
                    "score": 50
                }
            ],
            "土": [],
            "金": [],
            "水": []
        }

        mock_bazi_analysis = {
            "zodiac": "龙",
            "day_master": "甲",
            "day_master_wuxing": "木",
            "yong_shen": "火",
            "xi_shen": "土",
            "ji_shen": ["水"]
        }

        # 综合分析
        result = comprehensive_name_analysis.invoke({
            "name": "三",
            "bazi_analysis": mock_bazi_analysis,
            "char_library": mock_char_library,
            "surname": "张"
        })

        assert "name" in result
        assert "bazi_analysis" in result
        assert "wuxing_analysis" in result
        assert "pingze_analysis" in result
        assert "stroke_analysis" in result
        assert "sangcai_wuge_analysis" in result
        assert "overall_score" in result
        assert "evaluation" in result


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_name(self):
        """测试空名字"""
        from bazi_calculator.tools.naming.pingze_analysis import analyze_name_pingze

        result = analyze_name_pingze.invoke({"name": ""})

        assert "name" in result
        assert result["name"] == ""

    def test_very_long_name(self):
        """测试超长名字"""
        long_name = "张" * 10

        from bazi_calculator.tools.naming.stroke_analysis import analyze_name_strokes

        result = analyze_name_strokes.invoke({"name": long_name})

        assert "name" in result
        assert len(result["strokes_dict"]) == len(long_name)

    def test_unknown_character(self):
        """测试未知字符"""
        unknown_char = "𠀀"

        strokes = KangxiStrokes.get_strokes(unknown_char)
        pingze = PingzePatterns.get_pingze(unknown_char)

        assert strokes is None or strokes >= 0
        assert pingze in ["平", "仄", None]
