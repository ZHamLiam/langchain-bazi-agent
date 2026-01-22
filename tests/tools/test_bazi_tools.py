"""测试八字计算工具"""

import pytest
from datetime import datetime

from bazi_calculator.tools.bazi.time_parser import parse_birth_time, validate_time
from bazi_calculator.tools.bazi.year_pillar import calculate_year_pillar
from bazi_calculator.tools.bazi.month_pillar import calculate_month_pillar
from bazi_calculator.tools.bazi.day_pillar import calculate_day_pillar
from bazi_calculator.tools.bazi.hour_pillar import calculate_hour_pillar
from bazi_calculator.tools.bazi.wuxing_analysis import (
    analyze_wuxing,
    count_wuxing,
    analyze_day_master_strength,
    determine_yong_shen,
)


class TestBaziTimeParser:
    """测试时间解析工具"""

    def test_parse_birth_time_standard_format(self):
        """测试标准时间格式解析"""
        result = parse_birth_time.invoke({
            "time_description": "2024年3月15日10点30分",
            "gender": "男",
            "calendar_type": "公历"
        })

        assert result["year"] == 2024
        assert result["month"] == 3
        assert result["day"] == 15
        assert result["hour"] == 10
        assert result["minute"] == 30
        assert result["gender"] == "男"

    def test_parse_birth_time_short_format(self):
        """测试简写时间格式解析"""
        result = parse_birth_time.invoke({
            "time_description": "2024.3.15 10:30",
            "gender": "女",
            "calendar_type": "公历"
        })

        assert result["year"] == 2024
        assert result["month"] == 3
        assert result["day"] == 15

    def test_validate_time_valid(self):
        """测试验证有效时间"""
        result = validate_time.invoke(datetime(2024, 3, 15, 10, 30))

        assert result["valid"] is True


class TestBaziPillars:
    """测试四柱计算"""

    def test_calculate_year_pillar(self):
        """测试年柱计算"""
        result = calculate_year_pillar.invoke({"birth_date": datetime(2024, 3, 15, 10, 30)})

        assert "gan" in result
        assert "zhi" in result
        assert "full" in result
        assert len(result["full"]) == 2

    def test_calculate_month_pillar(self):
        """测试月柱计算"""
        year_pillar = calculate_year_pillar.invoke({"birth_date": datetime(2024, 3, 15, 10, 30)})
        result = calculate_month_pillar.invoke({
            "birth_date": datetime(2024, 3, 15, 10, 30),
            "year_gan": year_pillar["gan"]
        })

        assert "gan" in result
        assert "zhi" in result
        assert "jieqi" in result

    def test_calculate_day_pillar(self):
        """测试日柱计算"""
        result = calculate_day_pillar.invoke({"birth_date": datetime(2024, 3, 15, 10, 30)})

        assert "gan" in result
        assert "zhi" in result
        assert "day_master" in result

    def test_calculate_hour_pillar(self):
        """测试时柱计算"""
        day_pillar = calculate_day_pillar.invoke({"birth_date": datetime(2024, 3, 15, 10, 30)})
        result = calculate_hour_pillar.invoke({
            "birth_time": datetime(2024, 3, 15, 10, 30),
            "day_gan": day_pillar["gan"]
        })

        assert "gan" in result
        assert "zhi" in result


class TestBaziWuxingAnalysis:
    """测试五行分析工具"""

    def setup_method(self):
        """设置测试数据"""
        self.bazi = {
            "year": {"gan": "甲", "zhi": "子", "gan_wuxing": "木", "zhi_wuxing": "水"},
            "month": {"gan": "丁", "zhi": "卯", "gan_wuxing": "火", "zhi_wuxing": "木"},
            "day": {"gan": "戊", "zhi": "辰", "gan_wuxing": "土", "zhi_wuxing": "土"},
            "hour": {"gan": "庚", "zhi": "巳", "gan_wuxing": "金", "zhi_wuxing": "火"},
        }

    def test_analyze_wuxing(self):
        """测试五行分析"""
        result = analyze_wuxing.invoke(self.bazi)

        assert "wuxing_count" in result
        assert "strength" in result
        assert "yong_shen_info" in result

    def test_count_wuxing(self):
        """测试五行统计"""
        result = count_wuxing.invoke(self.bazi)

        assert "木" in result
        assert "火" in result
        assert "土" in result
        assert "金" in result
        assert "水" in result

    def test_analyze_day_master_strength(self):
        """测试日主强弱分析"""
        result = analyze_day_master_strength.invoke(self.bazi)

        assert "strength" in result
        assert result["strength"] in ["强", "弱", "中和"]
        assert "scores" in result

    def test_determine_yong_shen(self):
        """测试用神推算"""
        result = determine_yong_shen.invoke(self.bazi)

        assert "yong_shen" in result
        assert "xi_shen" in result
        assert "ji_shen" in result
        assert "strength" in result
