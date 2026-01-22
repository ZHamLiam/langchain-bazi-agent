"""测试八字计算和五行分析完整流程

输入：出生年月日时性别
输出：八字以及其分析（五行统计、日主强弱、用神推算）
"""

import pytest
from datetime import datetime
from bazi_calculator.chains.bazi_agent import BaziAgent


class TestBaziWithWuxingAnalysis:
    """测试八字计算和五行分析完整流程"""

    @pytest.fixture
    def agent(self):
        """创建八字Agent实例"""
        return BaziAgent()

    def test_full_workflow_with_time_description(self, agent):
        """测试完整工作流程：时间描述 -> 八字 -> 五行分析"""

        time_description = "1990年3月15日上午10点30分"
        gender = "男"
        calendar_type = "公历"

        result = agent.calculate_bazi(
            time_description=time_description,
            gender=gender,
            calendar_type=calendar_type
        )

        assert "birth_info" in result
        assert "bazi" in result
        assert "wuxing_analysis" in result

        birth_info = result["birth_info"]
        bazi = result["bazi"]
        wuxing_analysis = result["wuxing_analysis"]

        assert birth_info["year"] == 1990
        assert birth_info["month"] == 3
        assert birth_info["day"] == 15
        assert birth_info["hour"] == 10
        assert birth_info["minute"] == 30
        assert birth_info["gender"] == gender

        assert "year" in bazi
        assert "month" in bazi
        assert "day" in bazi
        assert "hour" in bazi

        assert "gan" in bazi["year"]
        assert "zhi" in bazi["year"]
        assert "gan_wuxing" in bazi["year"]
        assert "zhi_wuxing" in bazi["year"]
        assert "full" in bazi["year"]

        assert "wuxing_count" in wuxing_analysis
        assert "strength" in wuxing_analysis
        assert "yong_shen_info" in wuxing_analysis

        assert wuxing_analysis["strength"] in ["强", "中和", "弱"]
        assert "yong_shen" in wuxing_analysis["yong_shen_info"]

        print("\n" + "=" * 60)
        print("测试用例1：时间描述输入")
        print("=" * 60)
        print(f"输入：{time_description}，{gender}，{calendar_type}")
        print(agent.format_bazi_result(result))

    def test_bazi_structure_validation(self, agent):
        """验证八字数据结构完整性"""

        result = agent.calculate_bazi(
            time_description="1985年8月22日下午3点",
            gender="女",
            calendar_type="公历"
        )

        bazi = result["bazi"]

        for pillar_name in ["year", "month", "day", "hour"]:
            pillar = bazi[pillar_name]

            assert "gan" in pillar, f"{pillar_name} 缺少 gan"
            assert "zhi" in pillar, f"{pillar_name} 缺少 zhi"
            assert "gan_wuxing" in pillar, f"{pillar_name} 缺少 gan_wuxing"
            assert "zhi_wuxing" in pillar, f"{pillar_name} 缺少 zhi_wuxing"
            assert "full" in pillar, f"{pillar_name} 缺少 full"

            assert pillar["full"] == pillar["gan"] + pillar["zhi"], f"{pillar_name} full 格式错误"

    def test_wuxing_analysis_completeness(self, agent):
        """测试五行分析完整性"""

        result = agent.calculate_bazi(
            time_description="2000年12月25日晚上8点15分",
            gender="男",
            calendar_type="公历"
        )

        wuxing_analysis = result["wuxing_analysis"]

        assert "wuxing_count" in wuxing_analysis
        wuxing_count = wuxing_analysis["wuxing_count"]
        for wuxing in ["金", "木", "水", "火", "土"]:
            assert wuxing in wuxing_count
            assert isinstance(wuxing_count[wuxing], int)

        assert "strength" in wuxing_analysis
        assert wuxing_analysis["strength"] in ["强", "中和", "弱"]

        assert "yong_shen_info" in wuxing_analysis
        yong_shen_info = wuxing_analysis["yong_shen_info"]
        assert "yong_shen" in yong_shen_info
        assert "xi_shen" in yong_shen_info
        assert "ji_shen" in yong_shen_info
        assert "strength" in yong_shen_info

        assert "summary" in wuxing_analysis
        summary = wuxing_analysis["summary"]
        assert "day_master" in summary
        assert "day_master_wuxing" in summary
        assert "yong_shen" in summary
        assert "xi_shen" in summary
        assert "ji_shen" in summary

    def test_multiple_birth_dates(self, agent):
        """测试多个出生日期的计算"""

        test_cases = [
            ("1990年1月1日早上6点", "男"),
            ("1995年5月20日中午12点", "女"),
            ("2005年10月10日下午4点30分", "男"),
            ("2010年7月15日上午9点", "女"),
        ]

        for time_desc, gender in test_cases:
            result = agent.calculate_bazi(
                time_description=time_desc,
                gender=gender,
                calendar_type="公历"
            )

            assert "bazi" in result
            assert "wuxing_analysis" in result

            bazi = result["bazi"]
            wuxing_analysis = result["wuxing_analysis"]

            day_master = bazi["day"]["gan"]
            day_master_wuxing = bazi["day"]["gan_wuxing"]

            assert len(day_master) == 1
            assert day_master_wuxing in ["金", "木", "水", "火", "土"]

            assert wuxing_analysis["strength"] in ["强", "中和", "弱"]
            assert wuxing_analysis["yong_shen_info"]["yong_shen"] in ["金", "木", "水", "火", "土"]

    def test_format_bazi_result(self, agent):
        """测试八字结果格式化输出"""

        result = agent.calculate_bazi(
            time_description="1988年4月12日上午10点",
            gender="男",
            calendar_type="公历"
        )

        formatted_text = agent.format_bazi_result(result)

        assert "八字计算结果" in formatted_text
        assert "出生信息" in formatted_text
        assert "八字四柱" in formatted_text
        assert "五行统计" in formatted_text
        assert "日主分析" in formatted_text
        assert "用神分析" in formatted_text

        assert "年柱：" in formatted_text
        assert "月柱：" in formatted_text
        assert "日柱：" in formatted_text
        assert "时柱：" in formatted_text

        print("\n" + formatted_text)

    def test_day_master_strength_logic(self, agent):
        """测试日主强弱分析逻辑"""

        result = agent.calculate_bazi(
            time_description="1992年2月28日晚上11点",
            gender="女",
            calendar_type="公历"
        )

        wuxing_analysis = result["wuxing_analysis"]
        strength = wuxing_analysis["strength"]
        scores = wuxing_analysis["scores"]

        assert "day_master" in scores
        assert "yin" in scores
        assert "bijie" in scores
        assert "shishang" in scores
        assert "cai" in scores
        assert "guansha" in scores

        input_energy = scores["day_master"] + scores["yin"] + scores["bijie"]
        output_energy = scores["shishang"] + scores["cai"] + scores["guansha"]

        assert isinstance(input_energy, (int, float))
        assert isinstance(output_energy, (int, float))
        assert input_energy >= 0
        assert output_energy >= 0

    def test_yong_shen_determination(self, agent):
        """测试用神推算逻辑"""

        result = agent.calculate_bazi(
            time_description="1998年9月18日下午2点",
            gender="男",
            calendar_type="公历"
        )

        wuxing_analysis = result["wuxing_analysis"]
        yong_shen_info = wuxing_analysis["yong_shen_info"]

        yong_shen = yong_shen_info["yong_shen"]
        xi_shen = yong_shen_info["xi_shen"]
        ji_shen = yong_shen_info["ji_shen"]

        assert yong_shen in ["金", "木", "水", "火", "土"]
        assert xi_shen in ["金", "木", "水", "火", "土", ""]
        assert isinstance(ji_shen, list)

    def test_wuxing_count_accuracy(self, agent):
        """测试五行计数准确性"""

        result = agent.calculate_bazi(
            time_description="1986年11月3日上午8点",
            gender="女",
            calendar_type="公历"
        )

        wuxing_analysis = result["wuxing_analysis"]
        wuxing_count = wuxing_analysis["wuxing_count"]

        total_count = sum(wuxing_count.values())
        assert total_count == 8, f"五行总数应为8，实际为{total_count}"

    def test_edge_case_midnight(self, agent):
        """测试午夜时间"""

        result = agent.calculate_bazi(
            time_description="2000年1月1日凌晨0点5分",
            gender="男",
            calendar_type="公历"
        )

        assert "bazi" in result
        assert "wuxing_analysis" in result
        assert result["birth_info"]["hour"] == 0
        assert result["birth_info"]["minute"] == 5

    def test_edge_case_year_boundary(self, agent):
        """测试年份边界"""

        result = agent.calculate_bazi(
            time_description="1999年12月31日晚上11点59分",
            gender="女",
            calendar_type="公历"
        )

        assert result["birth_info"]["year"] == 1999
        assert result["birth_info"]["month"] == 12
        assert result["birth_info"]["day"] == 31
        assert result["birth_info"]["hour"] == 23
        assert result["birth_info"]["minute"] == 59

        print("\n" + agent.format_bazi_result(result))
