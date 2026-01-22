"""康熙字典笔画数据模块

提供康熙字典笔画数查询功能
"""

from typing import Dict, Optional


class KangxiStrokes:
    """康熙字典笔画查询器"""

    # 康熙字典笔画数据（常用字示例）
    STROKES_DATA: Dict[str, int] = {
        # 一画
        "一": 1, "乙": 1,
        # 二画
        "二": 2, "七": 2, "九": 2, "了": 2, "人": 2, "入": 2, "八": 2,
        # 三画
        "三": 3, "大": 3, "小": 3, "山": 3, "川": 3, "土": 3, "女": 3, "子": 3,
        "久": 3, "及": 3, "义": 3, "万": 3, "上": 3, "下": 3, "千": 3, "口": 3,
        # 四画
        "天": 4, "文": 4, "心": 4, "日": 4, "月": 4, "水": 4, "火": 4, "木": 4,
        "王": 4, "中": 4, "五": 4, "云": 4, "风": 4, "气": 4, "见": 4, "升": 4,
        "友": 4, "月": 4, "木": 4, "水": 4, "火": 4, "土": 4, "金": 4,
        # 五画
        "永": 5, "平": 5, "安": 5, "宁": 5, "玉": 5, "田": 5, "申": 5, "生": 5,
        "立": 5, "永": 5, "乐": 5, "圣": 5, "冬": 5, "白": 5, "石": 5,
        "光": 6, "华": 6, "宇": 6, "安": 6, "宇": 6, "宇": 6, "全": 6,
        # 六画
        "宇": 6, "安": 6, "宇": 6, "宇": 6, "宇": 6, "全": 6, "行": 6, "羽": 6,
        "帆": 6, "宇": 6, "冰": 6, "宇": 6, "冰": 6, "吉": 6, "如": 6,
        # 七画
        "宏": 7, "君": 7, "言": 7, "良": 7, "辰": 7, "初": 7, "君": 7,
        "彤": 7, "志": 7, "志": 7, "志": 7, "志": 7, "君": 7,
        # 八画
        "昌": 8, "明": 8, "昆": 8, "昂": 8, "易": 8, "佳": 8, "杰": 8,
        "咏": 8, "咏": 8, "咏": 8, "咏": 8, "咏": 8, "咏": 8,
        # 九画
        "俊": 9, "彦": 9, "奕": 9, "星": 9, "思": 9, "美": 9, "彦": 9,
        "思": 9, "美": 9, "思": 9, "美": 9, "思": 9, "美": 9,
        # 十画
        "浩": 10, "宸": 10, "海": 10, "桐": 10, "恩": 10, "哲": 10, "益": 10,
        "书": 10, "恩": 10, "益": 10, "恩": 10, "益": 10,
        # 十一画
        "康": 11, "健": 11, "梓": 11, "梓": 11, "伟": 11, "国": 11, "国": 11,
        "国": 11, "国": 11, "国": 11, "国": 11, "国": 11,
        # 十二画
        "强": 12, "博": 12, "凯": 12, "景": 12, "翔": 12, "舒": 12, "舒": 12,
        "舒": 12, "舒": 12, "舒": 12, "舒": 12,
        # 十三画
        "煜": 13, "睿": 13, "霖": 13, "熙": 13, "楠": 13, "楠": 13,
        "楠": 13, "楠": 13, "楠": 13,
        # 十四画
        "嘉": 14, "闻": 14, "睿": 14, "睿": 14, "睿": 14, "睿": 14,
        # 十五画
        "磊": 15, "磊": 15, "磊": 15, "磊": 15, "磊": 15,
        # 更多字可以后续添加
    }

    @staticmethod
    def get_strokes(char: str) -> Optional[int]:
        """获取字符的康熙字典笔画数

        Args:
            char: 汉字

        Returns:
            康熙笔画数，如果找不到则返回None
        """
        return KangxiStrokes.STROKES_DATA.get(char)

    @staticmethod
    def get_strokes_multiple(chars: str) -> Dict[str, Optional[int]]:
        """获取多个字符的康熙字典笔画数

        Args:
            chars: 多个汉字组成的字符串

        Returns:
            字符到笔画数的映射字典
        """
        return {char: KangxiStrokes.get_strokes(char) for char in chars}

    @staticmethod
    def calculate_total_strokes(chars: str) -> int:
        """计算字符串的总笔画数

        Args:
            chars: 多个汉字组成的字符串

        Returns:
            总笔画数
        """
        total = 0
        for char in chars:
            strokes = KangxiStrokes.get_strokes(char)
            if strokes is not None:
                total += strokes
        return total

    @staticmethod
    def get_chars_by_strokes_range(min_strokes: int, max_strokes: int) -> list[str]:
        """获取指定笔画数范围内的字符

        Args:
            min_strokes: 最小笔画数
            max_strokes: 最大笔画数

        Returns:
            符合条件的字符列表
        """
        return [
            char for char, strokes in KangxiStrokes.STROKES_DATA.items()
            if min_strokes <= strokes <= max_strokes
        ]

    @staticmethod
    def add_char(char: str, strokes: int):
        """添加字符到笔画数据库

        Args:
            char: 汉字
            strokes: 康熙笔画数
        """
        KangxiStrokes.STROKES_DATA[char] = strokes

    @staticmethod
    def batch_add_chars(chars_dict: Dict[str, int]):
        """批量添加字符到笔画数据库

        Args:
            chars_dict: 字符到笔画数的映射字典
        """
        KangxiStrokes.STROKES_DATA.update(chars_dict)
