"""生肖规则数据模块

提供12生肖的宜忌规则和字根映射
"""

from typing import Dict, List, Tuple


class ZodiacRules:
    """生肖规则查询器"""

    # 12生肖列表
    ZODIACS = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

    # 生肖宜忌规则
    ZODIAC_RULES: Dict[str, Dict[str, List[str]]] = {
        "鼠": {
            "favor": ["宀", "米", "豆", "鱼", "水", "木", "月", "王", "大", "人", "一"],
            "avoid": ["火", "日", "羊", "牛", "马", "刀", "血", "车"],
            "favor_chars": ["宁", "宝", "家", "福", "嘉", "颖", "静", "雯", "雅", "婷"],
            "avoid_chars": ["照", "烈", "炎", "辉", "阳", "旭", "胜", "猛", "冲", "仁"]
        },
        "牛": {
            "favor": ["草", "禾", "豆", "米", "氵", "辶", "宀", "田", "金"],
            "avoid": ["月", "日", "马", "羊", "人", "彡", "巾", "衣", "采", "车"],
            "favor_chars": ["秀", "科", "福", "嘉", "怡", "恩", "惠", "慧", "敏", "智"],
            "avoid_chars": ["胜", "猛", "俊", "伟", "腾", "冲", "仁", "仲", "任", "佳"]
        },
        "虎": {
            "favor": ["山", "林", "木", "王", "君", "长", "马", "衣", "彡", "巾", "采"],
            "avoid": ["申", "口", "日", "月", "田", "辰", "龙", "虎", "彧", "彡"],
            "favor_chars": ["岚", "峰", "杰", "伟", "凯", "明", "峰", "智", "敏", "慧"],
            "avoid_chars": ["申", "连", "瑞", "辉", "胜", "猛", "腾", "冲", "旭", "俊"]
        },
        "兔": {
            "favor": ["草", "禾", "豆", "米", "口", "木", "宀", "月", "彡", "巾", "采"],
            "avoid": ["日", "龙", "鸡", "人", "一", "心", "彡", "衣", "采", "车"],
            "favor_chars": ["秀", "科", "芳", "菲", "萍", "莹", "雅", "婷", "慧", "敏"],
            "avoid_chars": ["胜", "猛", "腾", "冲", "旭", "俊", "伟", "仁", "任", "佳"]
        },
        "龙": {
            "favor": ["水", "雨", "云", "王", "君", "大", "日", "月", "星", "马", "山"],
            "avoid": ["戌", "犬", "狗", "山", "土", "田", "车", "刀", "弓", "辶"],
            "favor_chars": ["云", "雨", "霖", "瑞", "嘉", "宇", "明", "星", "泽", "海"],
            "avoid_chars": ["成", "威", "猛", "强", "腾", "冲", "旭", "胜", "杰", "辉"]
        },
        "蛇": {
            "favor": ["木", "草", "宀", "口", "彡", "巾", "采", "衣", "日", "月", "星"],
            "avoid": ["日", "猪", "虎", "人", "一", "心", "刀", "血", "弓", "辶"],
            "favor_chars": ["秀", "芳", "菲", "萍", "莹", "雅", "婷", "慧", "敏", "智"],
            "avoid_chars": ["胜", "猛", "腾", "冲", "旭", "俊", "伟", "仁", "任", "佳"]
        },
        "马": {
            "favor": ["草", "禾", "豆", "米", "龙", "辰", "宀", "木", "王", "人", "一"],
            "avoid": ["子", "水", "田", "车", "牛", "马", "羊", "刀", "血", "车"],
            "favor_chars": ["秀", "科", "腾", "骏", "祥", "福", "嘉", "明", "辉", "杰"],
            "avoid_chars": ["子", "连", "福", "祥", "伟", "胜", "猛", "冲", "旭", "俊"]
        },
        "羊": {
            "favor": ["草", "禾", "豆", "米", "月", "宀", "口", "彡", "巾", "采", "衣"],
            "avoid": ["子", "鼠", "水", "牛", "人", "一", "心", "刀", "血", "车"],
            "favor_chars": ["秀", "芳", "菲", "萍", "莹", "雅", "婷", "慧", "敏", "智"],
            "avoid_chars": ["子", "连", "胜", "猛", "冲", "旭", "俊", "伟", "仁", "任"]
        },
        "猴": {
            "favor": ["木", "山", "草", "禾", "豆", "米", "宀", "人", "一", "口", "彡"],
            "avoid": ["火", "金", "刀", "血", "车", "辶", "龙", "辰", "虎", "彧"],
            "favor_chars": ["岚", "峰", "杰", "伟", "凯", "明", "智", "敏", "慧", "婷"],
            "avoid_chars": ["烈", "炎", "辉", "胜", "猛", "腾", "冲", "旭", "俊", "成"]
        },
        "鸡": {
            "favor": ["米", "豆", "麦", "禾", "山", "宀", "月", "彡", "巾", "采", "衣"],
            "avoid": ["金", "心", "彡", "人", "一", "刀", "血", "车", "辶", "兔"],
            "favor_chars": ["科", "翔", "飞", "智", "敏", "慧", "婷", "雅", "莹", "秀"],
            "avoid_chars": ["胜", "猛", "腾", "冲", "旭", "俊", "伟", "仁", "任", "佳"]
        },
        "狗": {
            "favor": ["人", "一", "宀", "口", "彡", "巾", "采", "衣", "鱼", "豆", "米"],
            "avoid": ["辰", "龙", "月", "日", "羊", "人", "一", "心", "刀", "血", "车"],
            "favor_chars": ["宁", "宝", "家", "福", "嘉", "颖", "静", "雯", "雅", "婷"],
            "avoid_chars": ["胜", "猛", "腾", "冲", "旭", "俊", "伟", "仁", "任", "佳"]
        },
        "猪": {
            "favor": ["草", "豆", "米", "鱼", "宀", "王", "金", "月", "彡", "巾", "采"],
            "avoid": ["蛇", "猴", "虎", "山", "刀", "血", "车", "辶", "人", "一", "心"],
            "favor_chars": ["秀", "科", "芳", "菲", "萍", "莹", "雅", "婷", "慧", "敏"],
            "avoid_chars": ["胜", "猛", "腾", "冲", "旭", "俊", "伟", "仁", "任", "佳"]
        }
    }

    @staticmethod
    def get_zodiac_by_year(year: int) -> str:
        """根据年份获取生肖

        Args:
            year: 公历年份

        Returns:
            生肖名称
        """
        offset = (year - 1900) % 12
        if offset < 0:
            offset += 12
        return ZodiacRules.ZODIACS[offset]

    @staticmethod
    def get_favor_radicals(zodiac: str) -> List[str]:
        """获取生肖喜用的字根

        Args:
            zodiac: 生肖

        Returns:
            喜用字根列表
        """
        return ZodiacRules.ZODIAC_RULES.get(zodiac, {}).get("favor", [])

    @staticmethod
    def get_avoid_radicals(zodiac: str) -> List[str]:
        """获取生肖忌用的字根

        Args:
            zodiac: 生肖

        Returns:
            忌用字根列表
        """
        return ZodiacRules.ZODIAC_RULES.get(zodiac, {}).get("avoid", [])

    @staticmethod
    def get_favor_chars(zodiac: str) -> List[str]:
        """获取生肖宜用的字

        Args:
            zodiac: 生肖

        Returns:
            宜用字列表
        """
        return ZodiacRules.ZODIAC_RULES.get(zodiac, {}).get("favor_chars", [])

    @staticmethod
    def get_avoid_chars(zodiac: str) -> List[str]:
        """获取生肖忌用的字

        Args:
            zodiac: 生肖

        Returns:
            忌用字列表
        """
        return ZodiacRules.ZODIAC_RULES.get(zodiac, {}).get("avoid_chars", [])

    @staticmethod
    def is_char_favorable(zodiac: str, char: str) -> bool:
        """判断字符是否宜用

        Args:
            zodiac: 生肖
            char: 汉字

        Returns:
            是否宜用
        """
        favor_chars = ZodiacRules.get_favor_chars(zodiac)
        avoid_chars = ZodiacRules.get_avoid_chars(zodiac)
        return char in favor_chars and char not in avoid_chars

    @staticmethod
    def get_all_rules(zodiac: str) -> Dict[str, List[str]]:
        """获取生肖的所有宜忌规则

        Args:
            zodiac: 生肖

        Returns:
            规则字典
        """
        return ZodiacRules.ZODIAC_RULES.get(zodiac, {})
