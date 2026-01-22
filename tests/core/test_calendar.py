"""八字日历计算模块测试"""

import pytest
from datetime import datetime
from bazi_calculator.core.calendar import BaziCalendar


class TestBaziCalendar:
    """测试八字日历计算器"""
    
    def test_get_year_pillar(self):
        """测试年柱计算"""
        # 测试2024年2月5日（立春之后）
        date1 = datetime(2024, 2, 5, 12, 0, 0)
        year_gan, year_zhi, year_gan_wuxing, year_zhi_wuxing = BaziCalendar.get_year_pillar(date1)
        assert isinstance(year_gan, str)
        assert isinstance(year_zhi, str)
        assert year_gan in BaziCalendar.WUHU_DUN_TABLE[0]  # 年干应该在表中
        assert year_zhi in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        assert year_gan_wuxing in ["金", "木", "水", "火", "土"]
        assert year_zhi_wuxing in ["金", "木", "水", "火", "土"]
    
    def test_get_year_pillar_before_lichun(self):
        """测试立春前的年柱计算"""
        # 2024年2月3日（立春之前）
        date1 = datetime(2024, 2, 3, 12, 0, 0)
        year_gan, year_zhi, _, _ = BaziCalendar.get_year_pillar(date1)
        # 应该算作2023年
        
        # 2024年2月5日（立春之后）
        date2 = datetime(2024, 2, 5, 12, 0, 0)
        year_gan2, year_zhi2, _, _ = BaziCalendar.get_year_pillar(date2)
        
        assert (year_gan, year_zhi) != (year_gan2, year_zhi2)
    
    def test_get_month_pillar(self):
        """测试月柱计算"""
        date = datetime(2024, 3, 21, 12, 0, 0)
        year_gan, _, _, _ = BaziCalendar.get_year_pillar(date)
        month_gan, month_zhi, month_gan_wuxing, month_zhi_wuxing, jieqi = BaziCalendar.get_month_pillar(date, year_gan)
        
        assert isinstance(month_gan, str)
        assert isinstance(month_zhi, str)
        assert month_zhi in ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        assert jieqi in ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
    
    def test_get_day_pillar(self):
        """测试日柱计算"""
        date = datetime(2024, 3, 21, 12, 0, 0)
        day_gan, day_zhi, day_gan_wuxing, day_zhi_wuxing = BaziCalendar.get_day_pillar(date)
        
        assert isinstance(day_gan, str)
        assert isinstance(day_zhi, str)
        assert day_gan in ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        assert day_zhi in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        assert day_gan_wuxing in ["金", "木", "水", "火", "土"]
        assert day_zhi_wuxing in ["金", "木", "水", "火", "土"]
    
    def test_get_hour_pillar(self):
        """测试时柱计算"""
        date = datetime(2024, 3, 21, 12, 30, 0)
        day_gan, _, _, _ = BaziCalendar.get_day_pillar(date)
        hour_gan, hour_zhi, hour_gan_wuxing, hour_zhi_wuxing = BaziCalendar.get_hour_pillar(date, day_gan)
        
        assert isinstance(hour_gan, str)
        assert isinstance(hour_zhi, str)
        assert hour_zhi in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        assert hour_gan_wuxing in ["金", "木", "水", "火", "土"]
        assert hour_zhi_wuxing in ["金", "木", "水", "火", "土"]
    
    def test_get_hour_pillar_different_hours(self):
        """测试不同时辰的时柱计算"""
        day_gan = "甲"
        
        # 子时
        date1 = datetime(2024, 3, 21, 0, 30, 0)
        hour_gan1, hour_zhi1, _, _ = BaziCalendar.get_hour_pillar(date1, day_gan)
        assert hour_zhi1 == "子"
        
        # 午时
        date2 = datetime(2024, 3, 21, 12, 30, 0)
        hour_gan2, hour_zhi2, _, _ = BaziCalendar.get_hour_pillar(date2, day_gan)
        assert hour_zhi2 == "午"
        
        # 亥时
        date3 = datetime(2024, 3, 21, 22, 30, 0)
        hour_gan3, hour_zhi3, _, _ = BaziCalendar.get_hour_pillar(date3, day_gan)
        assert hour_zhi3 == "亥"
    
    def test_get_all_pillars(self):
        """测试完整四柱计算"""
        date = datetime(2024, 3, 21, 12, 30, 0)
        bazi = BaziCalendar.get_all_pillars(date)
        
        assert "year" in bazi
        assert "month" in bazi
        assert "day" in bazi
        assert "hour" in bazi
        assert "birth_info" in bazi
        
        # 检查年柱结构
        assert "gan" in bazi["year"]
        assert "zhi" in bazi["year"]
        assert "full" in bazi["year"]
        
        # 检查月柱结构
        assert "gan" in bazi["month"]
        assert "zhi" in bazi["month"]
        assert "full" in bazi["month"]
        assert "jieqi" in bazi["month"]
        
        # 检查日柱结构
        assert "gan" in bazi["day"]
        assert "zhi" in bazi["day"]
        assert "full" in bazi["day"]
        assert "day_master" in bazi["day"]
        
        # 检查时柱结构
        assert "gan" in bazi["hour"]
        assert "zhi" in bazi["hour"]
        assert "full" in bazi["hour"]
        
        # 检查出生信息
        assert "date" in bazi["birth_info"]
        assert bazi["birth_info"]["year"] == 2024
        assert bazi["birth_info"]["month"] == 3
        assert bazi["birth_info"]["day"] == 21
        assert bazi["birth_info"]["hour"] == 12
    
    def test_wuhu_dun_table(self):
        """测试五虎遁表"""
        assert len(BaziCalendar.WUHU_DUN_TABLE) == 10
        assert len(BaziCalendar.WUHU_DUN_TABLE[0]) == 10
        assert BaziCalendar.WUHU_DUN_TABLE[0][0] == "丙"
        assert BaziCalendar.WUHU_DUN_TABLE[9][9] == "癸"
    
    def test_wushu_dun_table(self):
        """测试五鼠遁表"""
        assert len(BaziCalendar.WUSHU_DUN_TABLE) == 10
        assert len(BaziCalendar.WUSHU_DUN_TABLE[0]) == 12
        assert BaziCalendar.WUSHU_DUN_TABLE[0][0] == "甲"
        assert BaziCalendar.WUSHU_DUN_TABLE[9][11] == "乙"
    
    def test_base_date(self):
        """测试基准日期"""
        assert BaziCalendar.BASE_DATE == datetime(1949, 10, 1)
    
    def test_pillar_consistency(self):
        """测试四柱一致性"""
        date = datetime(2024, 3, 21, 12, 30, 0)
        bazi = BaziCalendar.get_all_pillars(date)
        
        # 验证年柱和月柱的关系
        # 月支应该在寅到亥之间
        assert bazi["month"]["zhi"] in ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        
        # 验证日主
        assert bazi["day"]["gan"] == bazi["day"]["day_master"]
        
        # 验证时支
        assert bazi["hour"]["zhi"] in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    def test_wuxing_consistency(self):
        """测试五行一致性"""
        date = datetime(2024, 3, 21, 12, 30, 0)
        bazi = BaziCalendar.get_all_pillars(date)
        
        # 检查所有五行属性
        for pillar in ["year", "month", "day", "hour"]:
            assert bazi[pillar]["gan_wuxing"] in ["金", "木", "水", "火", "土"]
            assert bazi[pillar]["zhi_wuxing"] in ["金", "木", "水", "火", "土"]
    
    def test_get_month_pillar_jieqi(self):
        """测试月柱节气计算"""
        # 测试春分附近（应该在卯月）
        date1 = datetime(2024, 3, 21, 12, 0, 0)
        year_gan1, _, _, _ = BaziCalendar.get_year_pillar(date1)
        month_gan1, month_zhi1, _, _, jieqi1 = BaziCalendar.get_month_pillar(date1, year_gan1)
        assert month_zhi1 in ["卯", "辰"]  # 春分可能在卯或辰月
        assert jieqi1 in ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
        
        # 测试夏至附近（应该在巳月或午月）
        date2 = datetime(2024, 6, 21, 12, 0, 0)
        year_gan2, _, _, _ = BaziCalendar.get_year_pillar(date2)
        month_gan2, month_zhi2, _, _, jieqi2 = BaziCalendar.get_month_pillar(date2, year_gan2)
        assert month_zhi2 in ["巳", "午"]  # 夏至可能在巳或午月
        assert jieqi2 in ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
