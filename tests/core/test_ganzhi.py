"""天干地支计算模块测试"""

import pytest
from bazi_calculator.core.ganzhi import GanzhiCalculator


class TestGanzhiCalculator:
    """测试干支计算器"""
    
    def test_tiangan_list(self):
        """测试天干列表"""
        tiangan = GanzhiCalculator.get_all_tiangan()
        assert len(tiangan) == 10
        assert "甲" in tiangan
        assert "癸" in tiangan
        assert tiangan[0] == "甲"
    
    def test_dizhi_list(self):
        """测试地支列表"""
        dizhi = GanzhiCalculator.get_all_dizhi()
        assert len(dizhi) == 12
        assert "子" in dizhi
        assert "亥" in dizhi
        assert dizhi[0] == "子"
    
    def test_wuxing_list(self):
        """测试五行列表"""
        wuxing = GanzhiCalculator.get_all_wuxing()
        assert len(wuxing) == 5
        assert set(wuxing) == {"金", "木", "水", "火", "土"}
    
    def test_get_tiangan_by_index_valid(self):
        """测试获取有效的天干"""
        assert GanzhiCalculator.get_tiangan_by_index(0) == "甲"
        assert GanzhiCalculator.get_tiangan_by_index(5) == "己"
        assert GanzhiCalculator.get_tiangan_by_index(9) == "癸"
    
    def test_get_tiangan_by_index_invalid(self):
        """测试获取无效的天干索引"""
        with pytest.raises(IndexError):
            GanzhiCalculator.get_tiangan_by_index(-1)
        with pytest.raises(IndexError):
            GanzhiCalculator.get_tiangan_by_index(10)
    
    def test_get_dizhi_by_index_valid(self):
        """测试获取有效的地支"""
        assert GanzhiCalculator.get_dizhi_by_index(0) == "子"
        assert GanzhiCalculator.get_dizhi_by_index(6) == "午"
        assert GanzhiCalculator.get_dizhi_by_index(11) == "亥"
    
    def test_get_dizhi_by_index_invalid(self):
        """测试获取无效的地支索引"""
        with pytest.raises(IndexError):
            GanzhiCalculator.get_dizhi_by_index(-1)
        with pytest.raises(IndexError):
            GanzhiCalculator.get_dizhi_by_index(12)
    
    def test_get_ganzhi_pair(self):
        """测试获取干支对"""
        tiangan, dizhi = GanzhiCalculator.get_ganzhi_pair(0, 0)
        assert tiangan == "甲"
        assert dizhi == "子"
        
        tiangan, dizhi = GanzhiCalculator.get_ganzhi_pair(3, 6)
        assert tiangan == "丁"
        assert dizhi == "午"
    
    def test_get_ganzhi_str(self):
        """测试获取干支字符串"""
        assert GanzhiCalculator.get_ganzhi_str(0, 0) == "甲子"
        assert GanzhiCalculator.get_ganzhi_str(3, 6) == "丁午"
        assert GanzhiCalculator.get_ganzhi_str(9, 11) == "癸亥"
    
    def test_tiangan_wuxing(self):
        """测试天干五行映射"""
        assert GanzhiCalculator.get_tiangan_wuxing("甲") == "木"
        assert GanzhiCalculator.get_tiangan_wuxing("乙") == "木"
        assert GanzhiCalculator.get_tiangan_wuxing("丙") == "火"
        assert GanzhiCalculator.get_tiangan_wuxing("丁") == "火"
        assert GanzhiCalculator.get_tiangan_wuxing("戊") == "土"
        assert GanzhiCalculator.get_tiangan_wuxing("己") == "土"
        assert GanzhiCalculator.get_tiangan_wuxing("庚") == "金"
        assert GanzhiCalculator.get_tiangan_wuxing("辛") == "金"
        assert GanzhiCalculator.get_tiangan_wuxing("壬") == "水"
        assert GanzhiCalculator.get_tiangan_wuxing("癸") == "水"
    
    def test_tiangan_wuxing_invalid(self):
        """测试无效天干的五行查询"""
        with pytest.raises(ValueError):
            GanzhiCalculator.get_tiangan_wuxing("A")
    
    def test_dizhi_wuxing(self):
        """测试地支五行映射"""
        assert GanzhiCalculator.get_dizhi_wuxing("子") == "水"
        assert GanzhiCalculator.get_dizhi_wuxing("寅") == "木"
        assert GanzhiCalculator.get_dizhi_wuxing("卯") == "木"
        assert GanzhiCalculator.get_dizhi_wuxing("巳") == "火"
        assert GanzhiCalculator.get_dizhi_wuxing("午") == "火"
        assert GanzhiCalculator.get_dizhi_wuxing("辰") == "土"
        assert GanzhiCalculator.get_dizhi_wuxing("未") == "土"
        assert GanzhiCalculator.get_dizhi_wuxing("戌") == "土"
        assert GanzhiCalculator.get_dizhi_wuxing("丑") == "土"
        assert GanzhiCalculator.get_dizhi_wuxing("申") == "金"
        assert GanzhiCalculator.get_dizhi_wuxing("酉") == "金"
        assert GanzhiCalculator.get_dizhi_wuxing("亥") == "水"
    
    def test_dizhi_wuxing_invalid(self):
        """测试无效地支的五行查询"""
        with pytest.raises(ValueError):
            GanzhiCalculator.get_dizhi_wuxing("A")
    
    def test_get_wuxing(self):
        """测试获取干支五行"""
        tiangan_wuxing, dizhi_wuxing = GanzhiCalculator.get_wuxing("甲", "子")
        assert tiangan_wuxing == "木"
        assert dizhi_wuxing == "水"
        
        tiangan_wuxing, dizhi_wuxing = GanzhiCalculator.get_wuxing("丙", "午")
        assert tiangan_wuxing == "火"
        assert dizhi_wuxing == "火"
    
    def test_jiazi_by_index(self):
        """测试六十甲子"""
        assert GanzhiCalculator.get_jiazi_by_index(0) == "甲子"
        assert GanzhiCalculator.get_jiazi_by_index(59) == "癸亥"
        assert GanzhiCalculator.get_jiazi_by_index(12) == "丙子"
    
    def test_jiazi_by_index_invalid(self):
        """测试无效的六十甲子索引"""
        with pytest.raises(IndexError):
            GanzhiCalculator.get_jiazi_by_index(-1)
        with pytest.raises(IndexError):
            GanzhiCalculator.get_jiazi_by_index(60)
    
    def test_is_sheng_relation(self):
        """测试五行相生关系"""
        assert GanzhiCalculator.is_sheng_relation("木", "火") is True
        assert GanzhiCalculator.is_sheng_relation("火", "土") is True
        assert GanzhiCalculator.is_sheng_relation("土", "金") is True
        assert GanzhiCalculator.is_sheng_relation("金", "水") is True
        assert GanzhiCalculator.is_sheng_relation("水", "木") is True
        
        assert GanzhiCalculator.is_sheng_relation("木", "土") is False
        assert GanzhiCalculator.is_sheng_relation("火", "金") is False
    
    def test_is_ke_relation(self):
        """测试五行相克关系"""
        assert GanzhiCalculator.is_ke_relation("木", "土") is True
        assert GanzhiCalculator.is_ke_relation("土", "水") is True
        assert GanzhiCalculator.is_ke_relation("水", "火") is True
        assert GanzhiCalculator.is_ke_relation("火", "金") is True
        assert GanzhiCalculator.is_ke_relation("金", "木") is True
        
        assert GanzhiCalculator.is_ke_relation("木", "火") is False
        assert GanzhiCalculator.is_ke_relation("火", "土") is False
    
    def test_jiazi_list_length(self):
        """测试六十甲子列表长度"""
        assert len(GanzhiCalculator.JIAZI) == 60
    
    def test_jiazi_sequence(self):
        """测试六十甲子序列正确性"""
        assert GanzhiCalculator.JIAZI[0] == "甲子"
        assert GanzhiCalculator.JIAZI[1] == "乙丑"
        assert GanzhiCalculator.JIAZI[12] == "丙子"
        assert GanzhiCalculator.JIAZI[60 - 1] == "癸亥"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
