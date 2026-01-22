"""字库查询模块

提供字库数据结构和查询功能
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from bazi_calculator.data.kangxi_strokes import KangxiStrokes
from bazi_calculator.data.zodiac_rules import ZodiacRules
from bazi_calculator.data.pingze_patterns import PingzePatterns


class CharacterDatabase:
    """字库数据库"""

    def __init__(self, data_path: Optional[str] = None):
        """初始化字库数据库

        Args:
            data_path: 字库数据文件路径，如果为None则使用内存数据库
        """
        self.data_path = data_path
        self.char_library = {}

        if data_path and Path(data_path).exists():
            self.load_from_file(data_path)

    def load_from_file(self, filepath: str) -> bool:
        """从文件加载字库

        Args:
            filepath: 文件路径

        Returns:
            是否加载成功
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.char_library = json.load(f)
            return True
        except Exception as e:
            print(f"加载字库失败：{e}")
            return False

    def save_to_file(self, filepath: str) -> bool:
        """保存字库到文件

        Args:
            filepath: 文件路径

        Returns:
            是否保存成功
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.char_library, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存字库失败：{e}")
            return False

    def set_char_library(self, char_library: Dict[str, Any]):
        """设置字库数据

        Args:
            char_library: 字库字典
        """
        self.char_library = char_library

    def query_by_wuxing(
        self,
        wuxing: str,
        count: int = 25,
        include_details: bool = True
    ) -> List[Dict[str, Any]]:
        """按五行查询适合的字

        Args:
            wuxing: 五行属性
            count: 返回的字数，默认25个
            include_details: 是否包含详细信息，默认True

        Returns:
            字符列表
        """
        if wuxing not in self.char_library:
            return []

        chars = self.char_library[wuxing][:count]

        if include_details:
            return chars
        else:
            return [{"char": char_info["char"], "pinyin": char_info.get("pinyin", "")} for char_info in chars]

    def query_by_zodiac(
        self,
        zodiac: str,
        count: int = 25,
        favor_only: bool = True
    ) -> List[Dict[str, Any]]:
        """按生肖查询适合的字

        Args:
            zodiac: 生肖
            count: 返回的字数，默认25个
            favor_only: 是否只显示宜用的字，默认True

        Returns:
            字符列表
        """
        all_chars = []
        for wuxing_chars in self.char_library.values():
            all_chars.extend(wuxing_chars)

        filtered = []
        for char_info in all_chars:
            char = char_info.get("char", "")
            if favor_only:
                if ZodiacRules.is_char_favorable(zodiac, char):
                    filtered.append(char_info)
            else:
                if char not in ZodiacRules.get_avoid_chars(zodiac):
                    filtered.append(char_info)

            if len(filtered) >= count:
                break

        return filtered[:count]

    def query_by_strokes(
        self,
        min_strokes: int,
        max_strokes: int,
        count: int = 25
    ) -> List[Dict[str, Any]]:
        """按笔画范围查询适合的字

        Args:
            min_strokes: 最小笔画数
            max_strokes: 最大笔画数
            count: 返回的字数，默认25个

        Returns:
            字符列表
        """
        all_chars = []
        for wuxing_chars in self.char_library.values():
            for char_info in wuxing_chars:
                char = char_info.get("char", "")
                strokes = KangxiStrokes.get_strokes(char)
                if strokes is not None and min_strokes <= strokes <= max_strokes:
                    all_chars.append(char_info)

                if len(all_chars) >= count:
                    break

            if len(all_chars) >= count:
                break

        return all_chars[:count]

    def query_comprehensive(
        self,
        wuxing: Optional[str] = None,
        zodiac: Optional[str] = None,
        min_strokes: Optional[int] = None,
        max_strokes: Optional[int] = None,
        count: int = 25
    ) -> List[Dict[str, Any]]:
        """综合查询适合的字

        Args:
            wuxing: 五行属性（可选）
            zodiac: 生肖（可选）
            min_strokes: 最小笔画数（可选）
            max_strokes: 最大笔画数（可选）
            count: 返回的字数，默认25个

        Returns:
            字符列表
        """
        # 获取基础字库
        if wuxing:
            candidates = self.query_by_wuxing(wuxing, count=100)
        else:
            candidates = []
            for wuxing_chars in self.char_library.values():
                candidates.extend(wuxing_chars)

        # 按生肖过滤
        if zodiac:
            candidates = [
                char_info for char_info in candidates
                if ZodiacRules.is_char_favorable(zodiac, char_info.get("char", ""))
            ]

        # 按笔画过滤
        if min_strokes is not None or max_strokes is not None:
            candidates = [
                char_info for char_info in candidates
                if self._check_strokes_range(char_info.get("char", ""), min_strokes, max_strokes)
            ]

        return candidates[:count]

    def _check_strokes_range(
        self,
        char: str,
        min_strokes: Optional[int],
        max_strokes: Optional[int]
    ) -> bool:
        """检查字符笔画是否在范围内

        Args:
            char: 汉字
            min_strokes: 最小笔画数
            max_strokes: 最大笔画数

        Returns:
            是否在范围内
        """
        strokes = KangxiStrokes.get_strokes(char)
        if strokes is None:
            return False

        if min_strokes is not None and strokes < min_strokes:
            return False

        if max_strokes is not None and strokes > max_strokes:
            return False

        return True

    def get_char_info(self, char: str) -> Optional[Dict[str, Any]]:
        """获取单个字符的详细信息

        Args:
            char: 汉字

        Returns:
            字符信息字典，如果找不到则返回None
        """
        for wuxing_chars in self.char_library.values():
            for char_info in wuxing_chars:
                if char_info.get("char") == char:
                    return char_info
        return None

    def get_char_pingze(self, char: str) -> Optional[str]:
        """获取字符的平仄

        Args:
            char: 汉字

        Returns:
            平/仄，如果找不到则返回None
        """
        return PingzePatterns.get_pingze(char)

    def get_statistics(self) -> Dict[str, Any]:
        """获取字库统计信息

        Returns:
            统计信息字典
        """
        stats = {
            "total_chars": 0,
            "by_wuxing": {},
            "by_strokes": {}
        }

        for wuxing, chars in self.char_library.items():
            stats["by_wuxing"][wuxing] = len(chars)
            stats["total_chars"] += len(chars)

            for char_info in chars:
                char = char_info.get("char", "")
                strokes = KangxiStrokes.get_strokes(char)
                if strokes is not None:
                    stats["by_strokes"][str(strokes)] = stats["by_strokes"].get(str(strokes), 0) + 1

        return stats
