"""测试取名分析工具"""

import pytest

from bazi_calculator.tools.naming.pingze_analysis import (
    analyze_name_pingze,
    check_pingze_harmony,
    get_pingze_pattern_statistics,
)
from bazi_calculator.tools.naming.stroke_analysis import (
    analyze_name_strokes,
    check_strokes_harmony,
    get_strokes_by_range,
)
from bazi_calculator.tools.naming.sangcai_wuge import (
    calculate_wuge,
    calculate_sancai,
    analyze_sancai_wuge,
)


class TestPingzeAnalysis:
    """测试平仄分析工具"""

    def test_analyze_name_pingze(self):
        """测试名字平仄分析"""
        result = analyze_name_pingze.invoke({"name": "张三"})

        assert "name" in result
        assert "tones" in result
        assert "pingzes" in result
        assert "pattern" in result

    def test_check_pingze_harmony(self):
        """测试平仄和谐检查"""
        result = check_pingze_harmony.invoke({"name": "张三"})

        assert "name" in result
        assert "pattern" in result
        assert "is_favorable" in result
        assert "score" in result

    def test_get_pingze_pattern_statistics(self):
        """测试平仄模式统计"""
        result = get_pingze_pattern_statistics.invoke({"name": "张三"})

        assert "name" in result
        assert "total_chars" in result
        assert "ping_count" in result
        assert "ze_count" in result


class TestStrokeAnalysis:
    """测试笔画分析工具"""

    def test_analyze_name_strokes(self):
        """测试名字笔画分析"""
        result = analyze_name_strokes.invoke({"name": "张三"})

        assert "name" in result
        assert "strokes_dict" in result
        assert "total_strokes" in result
        assert "average_strokes" in result

    def test_check_strokes_harmony(self):
        """测试笔画和谐检查"""
        result = check_strokes_harmony.invoke({"name": "张三"})

        assert "name" in result
        assert "total_strokes" in result
        assert "score" in result
        assert "evaluations" in result

    def test_get_strokes_by_range(self):
        """测试笔画范围查询"""
        result = get_strokes_by_range.invoke({
            "name": "张三",
            "min_strokes": 5,
            "max_strokes": 15
        })

        assert "name" in result
        assert "min_strokes" in result
        assert "max_strokes" in result
        assert "matching_chars" in result


class TestSangcaiWuge:
    """测试三才五格工具"""

    def test_calculate_wuge(self):
        """测试五格计算"""
        result = calculate_wuge.invoke({
            "name": "三",
            "surname": "张"
        })

        assert "name" in result
        assert "surname" in result
        assert "tian_ge" in result
        assert "ren_ge" in result
        assert "di_ge" in result
        assert "wai_ge" in result
        assert "zong_ge" in result

    def test_calculate_sancai(self):
        """测试三才计算"""
        wuge = calculate_wuge.invoke({"name": "三", "surname": "张"})
        result = calculate_sancai.invoke(wuge)

        assert "tian_wuxing" in result
        assert "ren_wuxing" in result
        assert "di_wuxing" in result
        assert "sancai_pattern" in result

    def test_analyze_sancai_wuge(self):
        """测试三才五格综合分析"""
        result = analyze_sancai_wuge.invoke({
            "name": "三",
            "surname": "张"
        })

        assert "name" in result
        assert "wuge" in result
        assert "sancai" in result
        assert "overall_score" in result
        assert "evaluation" in result


class TestNamingToolsIntegration:
    """取名工具集成测试"""

    def test_pingze_and_strokes_combined(self):
        """测试平仄和笔画分析结合"""
        name = "张三"

        pingze_result = check_pingze_harmony.invoke({"name": name})
        stroke_result = check_strokes_harmony.invoke({"name": name})

        assert pingze_result["score"] >= 0
        assert stroke_result["score"] >= 0

        combined_score = (pingze_result["score"] + stroke_result["score"]) / 2
        assert 0 <= combined_score <= 100

    def test_sancai_wuge_consistency(self):
        """测试三才五格一致性"""
        result = analyze_sancai_wuge.invoke({"name": "三", "surname": "张"})

        wuge = result["wuge"]
        sancai = result["sancai"]

        assert wuge["tian_ge"] > 0
        assert wuge["ren_ge"] > 0
        assert wuge["di_ge"] > 0
        assert sancai["tian_wuxing"] in ["木", "火", "土", "金", "水"]
        assert sancai["ren_wuxing"] in ["木", "火", "土", "金", "水"]
        assert sancai["di_wuxing"] in ["木", "火", "土", "金", "水"]
