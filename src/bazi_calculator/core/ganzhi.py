"""天干地支计算模块

此模块提供天干地支的基础定义和计算功能。
"""

from typing import Dict, Tuple, List


def _generate_jiazi_list() -> List[str]:
    """生成完整的六十甲子列表"""
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    jiazi = []
    for i in range(60):
        t = tiangan[i % 10]
        d = dizhi[i % 12]
        jiazi.append(t + d)
    
    return jiazi


# 预生成六十甲子列表
_JIAZI_FULL = _generate_jiazi_list()


class GanzhiCalculator:
    """干支计算器
    
    提供天干、地支、干支的计算和五行查询功能。
    """
    
    # 十天干
    TIANGAN = [
        "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"
    ]
    
    # 十二地支
    DIZHI = [
        "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
    ]
    
    # 天干对应的五行
    TIANGAN_WUXING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    # 地支对应的五行
    DIZHI_WUXING = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    # 五行生克关系
    WUXING_SHENG = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木"
    }
    
    WUXING_KE = {
        "木": "土",
        "土": "水",
        "水": "火",
        "火": "金",
        "金": "木"
    }
    
    # 六十甲子（干支纪年表）
    # 以甲子年开始的60年干支表
    JIAZI = _JIAZI_FULL
    
    @staticmethod
    def get_tiangan_by_index(idx: int) -> str:
        """根据索引获取天干
        
        Args:
            idx: 索引（0-9）
            
        Returns:
            天干字符
            
        Raises:
            IndexError: 索引超出范围
        """
        if not 0 <= idx < len(GanzhiCalculator.TIANGAN):
            raise IndexError(f"天干索引超出范围: {idx}")
        return GanzhiCalculator.TIANGAN[idx]
    
    @staticmethod
    def get_dizhi_by_index(idx: int) -> str:
        """根据索引获取地支
        
        Args:
            idx: 索引（0-11）
            
        Returns:
            地支字符
            
        Raises:
            IndexError: 索引超出范围
        """
        if not 0 <= idx < len(GanzhiCalculator.DIZHI):
            raise IndexError(f"地支索引超出范围: {idx}")
        return GanzhiCalculator.DIZHI[idx]
    
    @staticmethod
    def get_ganzhi_pair(tiangan_idx: int, dizhi_idx: int) -> Tuple[str, str]:
        """获取干支对
        
        Args:
            tiangan_idx: 天干索引（0-9）
            dizhi_idx: 地支索引（0-11）
            
        Returns:
            (天干, 地支) 元组
        """
        tiangan = GanzhiCalculator.get_tiangan_by_index(tiangan_idx)
        dizhi = GanzhiCalculator.get_dizhi_by_index(dizhi_idx)
        return tiangan, dizhi
    
    @staticmethod
    def get_ganzhi_str(tiangan_idx: int, dizhi_idx: int) -> str:
        """获取干支字符串
        
        Args:
            tiangan_idx: 天干索引（0-9）
            dizhi_idx: 地支索引（0-11）
            
        Returns:
            干支字符串（如"甲子"）
        """
        tiangan, dizhi = GanzhiCalculator.get_ganzhi_pair(tiangan_idx, dizhi_idx)
        return tiangan + dizhi
    
    @staticmethod
    def get_tiangan_wuxing(tiangan: str) -> str:
        """获取天干的五行属性
        
        Args:
            tiangan: 天干字符
            
        Returns:
            五行属性（"金"、"木"、"水"、"火"、"土"）
            
        Raises:
            ValueError: 无效的天干
        """
        if tiangan not in GanzhiCalculator.TIANGAN_WUXING:
            raise ValueError(f"无效的天干: {tiangan}")
        return GanzhiCalculator.TIANGAN_WUXING[tiangan]
    
    @staticmethod
    def get_dizhi_wuxing(dizhi: str) -> str:
        """获取地支的五行属性
        
        Args:
            dizhi: 地支字符
            
        Returns:
            五行属性（"金"、"木"、"水"、"火"、"土"）
            
        Raises:
            ValueError: 无效的地支
        """
        if dizhi not in GanzhiCalculator.DIZHI_WUXING:
            raise ValueError(f"无效的地支: {dizhi}")
        return GanzhiCalculator.DIZHI_WUXING[dizhi]
    
    @staticmethod
    def get_wuxing(tiangan: str, dizhi: str) -> Tuple[str, str]:
        """获取干支的五行属性
        
        Args:
            tiangan: 天干字符
            dizhi: 地支字符
            
        Returns:
            (天干五行, 地支五行) 元组
        """
        tiangan_wuxing = GanzhiCalculator.get_tiangan_wuxing(tiangan)
        dizhi_wuxing = GanzhiCalculator.get_dizhi_wuxing(dizhi)
        return tiangan_wuxing, dizhi_wuxing
    
    @staticmethod
    def get_jiazi_by_index(idx: int) -> str:
        """根据索引获取六十甲子
        
        Args:
            idx: 索引（0-59）
            
        Returns:
            干支字符串（如"甲子"）
            
        Raises:
            IndexError: 索引超出范围
        """
        if not 0 <= idx < len(GanzhiCalculator.JIAZI):
            raise IndexError(f"六十甲子索引超出范围: {idx}")
        return GanzhiCalculator.JIAZI[idx]
    
    @staticmethod
    def is_sheng_relation(wuxing1: str, wuxing2: str) -> bool:
        """判断两个五行是否为相生关系
        
        Args:
            wuxing1: 第一个五行
            wuxing2: 第二个五行
            
        Returns:
            是否相生
        """
        return GanzhiCalculator.WUXING_SHENG.get(wuxing1) == wuxing2
    
    @staticmethod
    def is_ke_relation(wuxing1: str, wuxing2: str) -> bool:
        """判断两个五行是否为相克关系
        
        Args:
            wuxing1: 第一个五行
            wuxing2: 第二个五行
            
        Returns:
            是否相克
        """
        return GanzhiCalculator.WUXING_KE.get(wuxing1) == wuxing2
    
    @staticmethod
    def get_all_tiangan() -> list[str]:
        """获取所有天干"""
        return GanzhiCalculator.TIANGAN.copy()
    
    @staticmethod
    def get_all_dizhi() -> list[str]:
        """获取所有地支"""
        return GanzhiCalculator.DIZHI.copy()
    
    @staticmethod
    def get_all_wuxing() -> list[str]:
        """获取所有五行"""
        return ["金", "木", "水", "火", "土"]
