"""节气计算模块测试"""

import pytest
from datetime import datetime
from bazi_calculator.core.jieqi import JieqiCalculator


class TestJieqiCalculator:
    """测试节气计算器"""
    
    def test_jieqi_names(self):
        """测试节气名称列表"""
        names = JieqiCalculator.get_all_jieqi_names()
        assert len(names) == 24
        assert "立春" in names
        assert "冬至" in names
        assert "大寒" in names
        assert names[0] == "立春"
        assert names[23] == "大寒"
    
    def test_jieqi_names_order(self):
        """测试节气名称顺序"""
        names = JieqiCalculator.JIEQI_NAMES
        assert names[0] == "立春"
        assert names[1] == "雨水"
        assert names[2] == "惊蛰"
        assert names[3] == "春分"
        assert names[12] == "立秋"
        assert names[24 - 12] == "立秋"
        assert names[24 - 1] == "大寒"
    
    def test_jieqi_longitude(self):
        """测试节气对应的太阳黄经"""
        longitudes = JieqiCalculator.JIEQI_LONGITUDE
        assert len(longitudes) == 24
        assert longitudes[0] == 315  # 立春
        assert longitudes[3] == 0     # 春分
        assert longitudes[9] == 90    # 夏至
        assert longitudes[15] == 180   # 秋分
        assert longitudes[21] == 270   # 冬至
    
    def test_get_jieqi_name_by_index_valid(self):
        """测试获取有效的节气名称"""
        assert JieqiCalculator.get_jieqi_name_by_index(0) == "立春"
        assert JieqiCalculator.get_jieqi_name_by_index(3) == "春分"
        assert JieqiCalculator.get_jieqi_name_by_index(9) == "夏至"
        assert JieqiCalculator.get_jieqi_name_by_index(15) == "秋分"
        assert JieqiCalculator.get_jieqi_name_by_index(21) == "冬至"
        assert JieqiCalculator.get_jieqi_name_by_index(23) == "大寒"
    
    def test_get_jieqi_name_by_index_invalid(self):
        """测试获取无效的节气索引"""
        with pytest.raises(IndexError):
            JieqiCalculator.get_jieqi_name_by_index(-1)
        with pytest.raises(IndexError):
            JieqiCalculator.get_jieqi_name_by_index(24)
    
    def test_get_jieqi_index_by_name_valid(self):
        """测试获取有效的节气索引"""
        assert JieqiCalculator.get_jieqi_index_by_name("立春") == 0
        assert JieqiCalculator.get_jieqi_index_by_name("春分") == 3
        assert JieqiCalculator.get_jieqi_index_by_name("夏至") == 9
        assert JieqiCalculator.get_jieqi_index_by_name("秋分") == 15
        assert JieqiCalculator.get_jieqi_index_by_name("冬至") == 21
        assert JieqiCalculator.get_jieqi_index_by_name("大寒") == 23
    
    def test_get_jieqi_index_by_name_invalid(self):
        """测试获取无效的节气名称"""
        with pytest.raises(ValueError):
            JieqiCalculator.get_jieqi_index_by_name("无效节气")
        with pytest.raises(ValueError):
            JieqiCalculator.get_jieqi_index_by_name("Spring")
    
    def test_calculate_jieqi_datetime_valid(self):
        """测试计算节气的精确时间"""
        # 测试立春（索引0）
        lichun = JieqiCalculator.calculate_jieqi_datetime(2024, 0)
        assert isinstance(lichun, datetime)
        assert lichun.year == 2024
        assert lichun.month == 2
        
        # 测试春分（索引3）
        chunfen = JieqiCalculator.calculate_jieqi_datetime(2024, 3)
        assert isinstance(chunfen, datetime)
        assert chunfen.year == 2024
        assert chunfen.month == 3
        
        # 测试夏至（索引9）
        xiazhi = JieqiCalculator.calculate_jieqi_datetime(2024, 9)
        assert isinstance(xiazhi, datetime)
        assert xiazhi.year == 2024
        assert xiazhi.month == 6
    
    def test_calculate_jieqi_datetime_invalid(self):
        """测试计算无效的节气索引"""
        with pytest.raises(IndexError):
            JieqiCalculator.calculate_jieqi_datetime(2024, -1)
        with pytest.raises(IndexError):
            JieqiCalculator.calculate_jieqi_datetime(2024, 24)
    
    def test_get_current_jieqi(self):
        """测试获取当前节气"""
        # 测试2024年1月的某个日期（应该在小寒和大寒之间）
        date1 = datetime(2024, 1, 10, 0, 0, 0)
        current_jieqi, current_time, next_time = JieqiCalculator.get_current_jieqi(date1)
        assert current_jieqi == "小寒"
        assert current_time < date1 < next_time
        
        # 测试2024年2月5日（应该在立春之后）
        date2 = datetime(2024, 2, 5, 12, 0, 0)
        current_jieqi, current_time, next_time = JieqiCalculator.get_current_jieqi(date2)
        assert current_jieqi == "立春"
        
        # 测试2024年6月（夏至附近）
        date3 = datetime(2024, 6, 21, 12, 0, 0)
        current_jieqi, current_time, next_time = JieqiCalculator.get_current_jieqi(date3)
        assert current_jieqi == "夏至"
    
    def test_is_before_lichun(self):
        """测试判断是否在立春之前"""
        # 立春之前的日期
        date_before = datetime(2024, 2, 3, 0, 0, 0)
        assert JieqiCalculator.is_before_lichun(date_before) is True
        
        # 立春之后的日期
        date_after = datetime(2024, 2, 5, 12, 0, 0)
        assert JieqiCalculator.is_before_lichun(date_after) is False
        
        # 立春当天
        lichun_time = JieqiCalculator.calculate_jieqi_datetime(2024, 0)
        assert JieqiCalculator.is_before_lichun(lichun_time) is False
        assert JieqiCalculator.is_before_lichun(lichun_time.replace(hour=lichun_time.hour - 1)) is True
    
    def test_jieqi_count(self):
        """测试节气数量"""
        assert len(JieqiCalculator.JIEQI_NAMES) == 24
        assert len(JieqiCalculator.JIEQI_LONGITUDE) == 24
        assert len(JieqiCalculator.JIEQI_INDEX) == 24
    
    def test_jieqi_index_mapping(self):
        """测试节气索引映射"""
        assert JieqiCalculator.JIEQI_INDEX["立春"] == 0
        assert JieqiCalculator.JIEQI_INDEX["雨水"] == 1
        assert JieqiCalculator.JIEQI_INDEX["大寒"] == 23
    
    def test_jieqi_consistency(self):
        """测试节气数据的一致性"""
        for i in range(24):
            name = JieqiCalculator.get_jieqi_name_by_index(i)
            idx = JieqiCalculator.get_jieqi_index_by_name(name)
            assert idx == i


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
