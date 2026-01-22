"""平仄声调数据模块

提供汉字平仄声调查询和名字平仄和谐分析功能
"""

from typing import Dict, List, Optional, Tuple


class PingzePatterns:
    """平仄声调查询器"""

    # 声调到平仄的映射（一声、二声为平，三声、四声为仄）
    TONE_TO_PINGZE = {
        1: "平",
        2: "平",
        3: "仄",
        4: "仄"
    }

    # 常用汉字平仄数据（示例）
    PINGZE_DATA: Dict[str, int] = {
        # 一声（平）
        "一": 1, "伊": 1, "衣": 1, "医": 1, "依": 1, "伊": 1,
        "云": 2, "文": 2, "闻": 2, "雯": 2, "君": 1, "军": 1,
        "天": 1, "田": 2, "仙": 1, "山": 1, "心": 1, "星": 1,
        "东": 1, "冬": 1, "中": 1, "风": 1, "飞": 1, "芳": 1,
        # 二声（平）
        "华": 2, "宏": 2, "昊": 4, "浩": 4, "海": 3, "恒": 2,
        "明": 2, "名": 2, "鸣": 2, "梦": 4, "敏": 3, "美": 3,
        "阳": 2, "洋": 2, "扬": 2, "易": 4, "逸": 4, "义": 4,
        "泽": 2, "哲": 2, "臻": 1, "振": 4, "正": 4, "智": 4,
        # 三声（仄）
        "伟": 3, "伟": 3, "伟": 3, "文": 2, "武": 3, "雅": 3,
        "思": 1, "思": 1, "思": 1, "思": 1, "四": 4, "思": 1,
        "宇": 3, "宇": 3, "宇": 3, "宇": 3, "雨": 3, "玉": 4,
        "宁": 2, "宁": 2, "宁": 2, "宁": 2, "妮": 1, "妮": 1,
        # 四声（仄）
        "大": 4, "达": 2, "大": 4, "达": 2, "大": 4, "达": 2,
        "小": 3, "晓": 3, "小": 3, "晓": 3, "小": 3, "晓": 3,
        "嘉": 1, "佳": 1, "家": 1, "加": 1, "嘉": 1, "佳": 1,
        "志": 4, "智": 4, "志": 4, "智": 4, "志": 4, "智": 4,
        # 更多字可以后续添加
    }

    # 优选的平仄组合模式
    FAVORABLE_PATTERNS = [
        ["平", "平"],  # 平平
        ["仄", "仄"],  # 仄仄
        ["平", "仄"],  # 平仄
        ["仄", "平"],  # 仄平
        ["平", "平", "平"],  # 平平平
        ["仄", "仄", "仄"],  # 仄仄仄
        ["平", "仄", "平"],  # 平仄平
        ["仄", "平", "仄"],  # 仄平仄
    ]

    @staticmethod
    def get_tone(char: str) -> Optional[int]:
        """获取汉字的声调

        Args:
            char: 汉字

        Returns:
            声调（1-4），如果找不到则返回None
        """
        return PingzePatterns.PINGZE_DATA.get(char)

    @staticmethod
    def get_pingze(char: str) -> Optional[str]:
        """获取汉字的平仄

        Args:
            char: 汉字

        Returns:
            平/仄，如果找不到则返回None
        """
        tone = PingzePatterns.get_tone(char)
        if tone is not None:
            return PingzePatterns.TONE_TO_PINGZE[tone]
        return None

    @staticmethod
    def analyze_name_pingze(name: str) -> Dict[str, any]:
        """分析名字的平仄

        Args:
            name: 名字字符串

        Returns:
            平仄分析字典
        """
        tones = []
        pingzes = []

        for char in name:
            tone = PingzePatterns.get_tone(char)
            pingze = PingzePatterns.get_pingze(char)
            tones.append(tone if tone is not None else 0)
            pingzes.append(pingze if pingze is not None else "平")

        return {
            "name": name,
            "tones": tones,
            "pingzes": pingzes,
            "pattern": "".join(pingzes)
        }

    @staticmethod
    def check_harmony(name: str) -> Dict[str, any]:
        """检查名字的平仄和谐度

        Args:
            name: 名字字符串

        Returns:
            和谐度分析字典
        """
        analysis = PingzePatterns.analyze_name_pingze(name)
        pattern = analysis["pattern"]

        # 检查是否在优选模式中
        is_favorable = pattern in PingzePatterns.FAVORABLE_PATTERNS

        # 计算得分
        score = PingzePatterns._calculate_score(pattern)

        return {
            "name": name,
            "pattern": pattern,
            "is_favorable": is_favorable,
            "score": score,
            "description": PingzePatterns._get_description(pattern, score)
        }

    @staticmethod
    def _calculate_score(pattern: str) -> int:
        """计算平仄模式的得分

        Args:
            pattern: 平仄模式字符串

        Returns:
            得分（0-100）
        """
        if len(pattern) == 2:
            # 双字名
            if pattern in ["平平", "仄仄", "平仄", "仄平"]:
                return 90
            else:
                return 70
        elif len(pattern) == 3:
            # 三字名
            if pattern in ["平平平", "仄仄仄", "平仄平", "仄平仄"]:
                return 90
            elif pattern in ["平平仄", "仄仄平", "平仄仄", "仄平平"]:
                return 80
            else:
                return 70
        else:
            return 60

    @staticmethod
    def _get_description(pattern: str, score: int) -> str:
        """获取平仄模式的描述

        Args:
            pattern: 平仄模式字符串
            score: 得分

        Returns:
            描述文本
        """
        if score >= 90:
            return "平仄搭配极佳，读起来朗朗上口"
        elif score >= 80:
            return "平仄搭配较好，读起来比较顺口"
        elif score >= 70:
            return "平仄搭配一般，读起来尚可"
        else:
            return "平仄搭配有待改进"

    @staticmethod
    def get_suggestions(
        chars_list: List[List[str]],
        preferred_pattern: Optional[List[str]] = None
    ) -> List[Tuple[str, Dict[str, any]]]:
        """根据平仄模式生成名字建议

        Args:
            chars_list: 字符列表的列表，每个列表代表一个位置的可选字
            preferred_pattern: 首选的平仄模式

        Returns:
            名字建议列表，每个元素是(名字, 分析字典)的元组
        """
        import itertools

        suggestions = []

        # 生成所有可能的组合
        for chars in chars_list:
            for name_tuple in itertools.product(*chars):
                name = "".join(name_tuple)
                harmony = PingzePatterns.check_harmony(name)
                suggestions.append((name, harmony))

        # 按分数排序
        suggestions.sort(key=lambda x: x[1]["score"], reverse=True)

        # 如果有首选模式，优先返回符合该模式的
        if preferred_pattern:
            pattern_str = "".join(preferred_pattern)
            preferred = [s for s in suggestions if s[1]["pattern"] == pattern_str]
            others = [s for s in suggestions if s[1]["pattern"] != pattern_str]
            suggestions = preferred + others

        return suggestions

    @staticmethod
    def add_char(char: str, tone: int):
        """添加字符到平仄数据库

        Args:
            char: 汉字
            tone: 声调（1-4）
        """
        PingzePatterns.PINGZE_DATA[char] = tone

    @staticmethod
    def batch_add_chars(chars_dict: Dict[str, int]):
        """批量添加字符到平仄数据库

        Args:
            chars_dict: 字符到声调的映射字典
        """
        PingzePatterns.PINGZE_DATA.update(chars_dict)
