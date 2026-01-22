"""准确性和性能测试"""

import pytest
import time
from datetime import datetime

from bazi_calculator.core.ganzhi import GanzhiCalculator
from bazi_calculator.core.jieqi import JieqiCalculator
from bazi_calculator.core.calendar import BaziCalendar
from bazi_calculator.chains.bazi_agent import BaziAgent


class TestAccuracy:
    """准确性验证测试"""

    def test_known_bazi_accuracy(self):
        """测试已知八字计算的准确性"""
        test_cases = [
            {
                "date": datetime(2024, 3, 15, 10, 30),
                "expected_year_gan": "甲",
                "expected_year_zhi": "辰",
            },
            {
                "date": datetime(1990, 8, 8, 14, 0),
                "expected_year_gan": "庚",
                "expected_year_zhi": "午",
            },
        ]

        for test_case in test_cases:
            result = BaziCalendar.get_year_pillar(test_case["date"])
            year_gan = result[0]
            year_zhi = result[1]

            if test_case["expected_year_gan"]:
                assert year_gan == test_case["expected_year_gan"], \
                    f"年干计算错误：期望{test_case['expected_year_gan']}，实际{year_gan}"

            if test_case["expected_year_zhi"]:
                assert year_zhi == test_case["expected_year_zhi"], \
                    f"年支计算错误：期望{test_case['expected_year_zhi']}，实际{year_zhi}"

    def test_wuxing_mapping_accuracy(self):
        """测试五行映射准确性"""
        test_mappings = [
            ("甲", "木"),
            ("乙", "木"),
            ("丙", "火"),
            ("丁", "火"),
            ("戊", "土"),
            ("己", "土"),
            ("庚", "金"),
            ("辛", "金"),
            ("壬", "水"),
            ("癸", "水"),
            ("子", "水"),
            ("寅", "木"),
            ("巳", "火"),
            ("申", "金"),
            ("亥", "水"),
        ]

        for char, expected_wuxing in test_mappings:
            if char in GanzhiCalculator.TIANGAN:
                wuxing = GanzhiCalculator.get_tiangan_wuxing(char)
            else:
                wuxing = GanzhiCalculator.get_dizhi_wuxing(char)

            assert wuxing == expected_wuxing, \
                f"五行映射错误：{char} 应为 {expected_wuxing}，实际为 {wuxing}"

    def test_jiazi_cycle_accuracy(self):
        """测试六十甲子循环准确性"""
        for i in range(60):
            jiazi = GanzhiCalculator.get_jiazi_by_index(i)
            assert len(jiazi) == 2, f"第{i}个甲子长度错误"

            # 验证干支有效性
            assert jiazi[0] in GanzhiCalculator.TIANGAN
            assert jiazi[1] in GanzhiCalculator.DIZHI

    def test_zodiac_cycle_accuracy(self):
        """测试生肖循环准确性"""
        test_years = [
            (2020, "鼠"),
            (2021, "牛"),
            (2022, "虎"),
            (2023, "兔"),
            (2024, "龙"),
        ]

        from bazi_calculator.data.zodiac_rules import ZodiacRules

        for year, expected_zodiac in test_years:
            zodiac = ZodiacRules.get_zodiac_by_year(year)
            assert zodiac == expected_zodiac, \
                f"生肖计算错误：{year}年应为{expected_zodiac}，实际为{zodiac}"

    def test_bazi_complete_calculation(self):
        """测试八字完整计算"""
        test_date = datetime(2024, 3, 15, 10, 30)

        result = BaziCalendar.get_all_pillars(test_date)

        assert "year" in result
        assert "month" in result
        assert "day" in result
        assert "hour" in result

        # 验证每个柱都有完整信息
        for pillar_name in ["year", "month", "day", "hour"]:
            pillar = result[pillar_name]
            assert "gan" in pillar
            assert "zhi" in pillar
            assert "gan_wuxing" in pillar
            assert "zhi_wuxing" in pillar
            assert "full" in pillar


class TestPerformance:
    """性能测试"""

    def test_bazi_calculation_performance(self):
        """测试八字计算性能"""
        test_date = datetime(2024, 3, 15, 10, 30)

        iterations = 100
        start_time = time.time()

        for _ in range(iterations):
            BaziCalendar.get_all_pillars(test_date)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / iterations

        assert avg_time < 0.01, \
            f"八字计算性能不达标：平均耗时{avg_time}秒，应小于0.01秒"

    def test_wuxing_analysis_performance(self):
        """测试五行分析性能"""
        from bazi_calculator.core.wuxing import WuxingAnalyzer

        bazi = {
            "year": {"gan": "甲", "zhi": "子", "gan_wuxing": "木", "zhi_wuxing": "水"},
            "month": {"gan": "丁", "zhi": "卯", "gan_wuxing": "火", "zhi_wuxing": "木"},
            "day": {"gan": "戊", "zhi": "辰", "gan_wuxing": "土", "zhi_wuxing": "土"},
            "hour": {"gan": "庚", "zhi": "巳", "gan_wuxing": "金", "zhi_wuxing": "火"},
        }

        iterations = 100
        start_time = time.time()

        for _ in range(iterations):
            WuxingAnalyzer.analyze_comprehensive(bazi)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / iterations

        assert avg_time < 0.02, \
            f"五行分析性能不达标：平均耗时{avg_time}秒，应小于0.02秒"

    def test_database_query_performance(self):
        """测试数据库查询性能"""
        from bazi_calculator.data import KangxiStrokes, ZodiacRules, PingzePatterns

        test_chars = ["张", "三", "李", "王", "木", "火", "土", "金", "水"]
        test_zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

        iterations = 100
        start_time = time.time()

        for _ in range(iterations):
            for char in test_chars:
                KangxiStrokes.get_strokes(char)
                PingzePatterns.get_pingze(char)

            for zodiac in test_zodiacs:
                ZodiacRules.get_favor_radicals(zodiac)
                ZodiacRules.get_avoid_radicals(zodiac)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / iterations

        assert avg_time < 0.05, \
            f"数据库查询性能不达标：平均耗时{avg_time}秒，应小于0.05秒"

    def test_agent_workflow_performance(self):
        """测试Agent工作流程性能"""
        agent = BaziAgent()

        start_time = time.time()

        result = agent.calculate_bazi("2024年3月15日10点30分", "男")

        end_time = time.time()
        total_time = end_time - start_time

        assert total_time < 2.0, \
            f"Agent工作流程性能不达标：总耗时{total_time}秒，应小于2秒"

        assert "birth_info" in result
        assert "bazi" in result
        assert "wuxing_analysis" in result


class TestMemoryEfficiency:
    """内存效率测试"""

    def test_database_memory_usage(self):
        """测试数据库内存使用"""
        from bazi_calculator.data import KangxiStrokes, ZodiacRules, PingzePatterns

        # 测试数据库大小
        kangxi_size = len(KangxiStrokes.STROKES_DATA)
        pingze_size = len(PingzePatterns.PINGZE_DATA)
        zodiac_rules_count = len(ZodiacRules.ZODIAC_RULES)

        assert kangxi_size > 0, "康熙字典数据库为空"
        assert pingze_size > 0, "平仄数据库为空"
        assert zodiac_rules_count == 12, f"生肖规则数量错误：{zodiac_rules_count}"

    def test_object_creation_efficiency(self):
        """测试对象创建效率"""
        from bazi_calculator.core.ganzhi import GanzhiCalculator

        iterations = 1000
        start_time = time.time()

        for i in range(iterations):
            ganzhi = GanzhiCalculator.get_jiazi_by_index(i % 60)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / iterations

        assert avg_time < 0.001, \
            f"对象创建效率不达标：平均耗时{avg_time}秒，应小于0.001秒"


class TestIntegrationAccuracy:
    """集成准确性测试"""

    def test_end_to_end_accuracy(self):
        """测试端到端准确性"""
        # 已知日期的八字结果
        test_case = {
            "date": datetime(1984, 8, 8, 8, 30),
            "expected": {
                "year": ("甲", "子"),
                "month": ("壬", "申"),
                "day": ("甲", "戌"),
                "hour": ("戊", "辰"),
            }
        }

        result = BaziCalendar.get_all_pillars(test_case["date"])
        expected = test_case["expected"]

        for pillar_name, (expected_gan, expected_zhi) in expected.items():
            actual_gan = result[pillar_name]["gan"]
            actual_zhi = result[pillar_name]["zhi"]

            assert actual_gan == expected_gan, \
                f"{pillar_name}干错误：期望{expected_gan}，实际{actual_gan}"
            assert actual_zhi == expected_zhi, \
                f"{pillar_name}支错误：期望{expected_zhi}，实际{actual_zhi}"
