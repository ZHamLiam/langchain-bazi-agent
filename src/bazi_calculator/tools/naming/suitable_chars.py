"""适合字查询工具

根据八字和生肖查询适合取名的字
"""

from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

from bazi_calculator.data.char_database import CharacterDatabase
from bazi_calculator.data.zodiac_rules import ZodiacRules


@tool
def get_suitable_chars(
    bazi_analysis: Dict[str, Any],
    char_library: Dict[str, Any],
    count_per_wuxing: int = 25
) -> Dict[str, Any]:
    """根据八字分析查询适合的字

    返回每个五行25个适合的字，已经过生肖过滤

    Args:
        bazi_analysis: 八字分析结果
        char_library: 字库字典
        count_per_wuxing: 每个五行返回的字数，默认25个

    Returns:
        适合字的字典，按五行分类
    """
    db = CharacterDatabase()
    db.set_char_library(char_library)

    zodiac = bazi_analysis.get("zodiac", "")
    yong_shen = bazi_analysis.get("yong_shen", "")
    xi_shen = bazi_analysis.get("xi_shen", "")

    # 获取所有五行的适合字
    suitable = {}

    for wuxing in ["木", "火", "土", "金", "水"]:
        # 综合查询：五行 + 生肖
        chars = db.query_comprehensive(
            wuxing=wuxing,
            zodiac=zodiac,
            count=count_per_wuxing
        )

        # 为每个字添加评分
        scored_chars = []
        for char_info in chars:
            char = char_info.get("char", "")
            score = _calculate_char_score(char_info, wuxing, yong_shen, xi_shen)
            char_info["score"] = score
            scored_chars.append(char_info)

        # 按分数排序
        scored_chars.sort(key=lambda x: x["score"], reverse=True)

        suitable[wuxing] = scored_chars[:count_per_wuxing]

    # 按优先级排序五行
    priority_order = _get_wuxing_priority(yong_shen, xi_shen)

    return {
        "suitable_chars": suitable,
        "priority_order": priority_order,
        "zodiac": zodiac,
        "yong_shen": yong_shen,
        "xi_shen": xi_shen,
        "summary": f"已为{zodiac}年生肖，用神{yong_shen}，喜神{xi_shen}生成适合字列表"
    }


@tool
def filter_suitable_chars_by_strokes(
    suitable_chars: Dict[str, Any],
    min_strokes: int,
    max_strokes: int
) -> Dict[str, Any]:
    """按笔画范围过滤适合字

    Args:
        suitable_chars: 适合字字典
        min_strokes: 最小笔画数
        max_strokes: 最大笔画数

    Returns:
        过滤后的适合字字典
    """
    from bazi_calculator.data.kangxi_strokes import KangxiStrokes

    filtered = {}

    for wuxing, chars in suitable_chars.items():
        if wuxing == "suitable_chars":
            continue

        filtered_chars = []
        for char_info in chars:
            char = char_info.get("char", "")
            strokes = KangxiStrokes.get_strokes(char)

            if strokes is not None and min_strokes <= strokes <= max_strokes:
                filtered_chars.append(char_info)

        filtered[wuxing] = filtered_chars

    return filtered


@tool
def get_top_suitable_chars(
    suitable_chars: Dict[str, Any],
    top_count: int = 10
) -> List[Dict[str, Any]]:
    """获取最适合的Top N字

    Args:
        suitable_chars: 适合字字典
        top_count: 返回的顶级字数，默认10个

    Returns:
        Top适合字列表
    """
    all_chars = []

    for wuxing, chars in suitable_chars.items():
        if wuxing == "suitable_chars":
            continue

        for char_info in chars:
            char_info["wuxing_type"] = wuxing
            all_chars.append(char_info)

    # 按分数排序
    all_chars.sort(key=lambda x: x.get("score", 0), reverse=True)

    return all_chars[:top_count]


@tool
def get_suitable_chars_by_wuxing(
    suitable_chars: Dict[str, Any],
    wuxing: str,
    count: int = 25
) -> List[Dict[str, Any]]:
    """获取指定五行的适合字

    Args:
        suitable_chars: 适合字字典
        wuxing: 五行属性
        count: 返回的字数，默认25个

    Returns:
        适合字列表
    """
    return suitable_chars.get(wuxing, [])[:count]


@tool
def format_suitable_chars(suitable_chars: Dict[str, Any]) -> str:
    """格式化适合字列表为文本

    Args:
        suitable_chars: 适合字字典

    Returns:
        格式化后的文本
    """
    output = []
    output.append("=" * 50)
    output.append("适合字列表")
    output.append("=" * 50)

    zodiac = suitable_chars.get("zodiac", "")
    yong_shen = suitable_chars.get("yong_shen", "")
    xi_shen = suitable_chars.get("xi_shen", "")

    output.append(f"\n生肖：{zodiac}")
    output.append(f"用神：{yong_shen}")
    output.append(f"喜神：{xi_shen}\n")

    priority_order = suitable_chars.get("priority_order", [])

    for i, wuxing in enumerate(priority_order, 1):
        chars = suitable_chars.get("suitable_chars", {}).get(wuxing, [])

        if not chars:
            continue

        output.append(f"{i}. 【{wuxing}】属性（共{len(chars)}个）")
        output.append("-" * 50)

        for char_info in chars:
            char = char_info.get("char", "")
            pinyin = char_info.get("pinyin", "")
            meaning = char_info.get("meaning", "")
            strokes = char_info.get("kangxi_strokes", 0)
            pingze = char_info.get("pingze", "")
            score = char_info.get("score", 0)

            output.append(f"  {char}（{pinyin}）- 笔画{strokes}，{pingze}，得分{score}")
            output.append(f"    {meaning}")

        output.append("")

    output.append("=" * 50)

    return "\n".join(output)


def _calculate_char_score(
    char_info: Dict[str, Any],
    wuxing: str,
    yong_shen: str,
    xi_shen: str
) -> int:
    """计算字符的适用分数

    Args:
        char_info: 字符信息
        wuxing: 五行属性
        yong_shen: 用神
        xi_shen: 喜神

    Returns:
        分数（0-100）
    """
    score = 50

    # 如果是用神，加分最多
    if wuxing == yong_shen:
        score += 30
    # 如果是喜神，加分
    elif wuxing == xi_shen:
        score += 20

    # 笔画分（适中笔画加分）
    strokes = char_info.get("kangxi_strokes", 0)
    if 5 <= strokes <= 15:
        score += 10
    elif 16 <= strokes <= 20:
        score += 5

    # 平仄分（平声加分）
    pingze = char_info.get("pingze", "")
    if pingze == "平":
        score += 5

    # 寓意长度适中加分
    meaning = char_info.get("meaning", "")
    if 4 <= len(meaning) <= 15:
        score += 5

    return min(score, 100)


def _get_wuxing_priority(yong_shen: str, xi_shen: str) -> List[str]:
    """获取五行优先级顺序

    Args:
        yong_shen: 用神
        xi_shen: 喜神

    Returns:
        五行优先级列表
    """
    all_wuxing = ["木", "火", "土", "金", "水"]

    # 用神第一，喜神第二
    priority = []

    if yong_shen and yong_shen in all_wuxing:
        priority.append(yong_shen)

    if xi_shen and xi_shen not in priority and xi_shen in all_wuxing:
        priority.append(xi_shen)

    # 其他五行按顺序
    for wuxing in all_wuxing:
        if wuxing not in priority:
            priority.append(wuxing)

    return priority
