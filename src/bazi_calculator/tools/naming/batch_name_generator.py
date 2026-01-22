"""批量取名工具

批量生成20-30个名字，支持基于用户选择或自动组合
"""

import random
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

from bazi_calculator.data.pingze_patterns import PingzePatterns
from bazi_calculator.data.kangxi_strokes import KangxiStrokes


@tool
def generate_batch_names(
    suitable_chars: Dict[str, Any],
    bazi_analysis: Dict[str, Any],
    user_selected_chars: Optional[List[str]] = None,
    count: int = 30
) -> Dict[str, Any]:
    """批量生成名字建议

    生成20-30个名字，包含简要分析

    Args:
        suitable_chars: 适合字字典
        bazi_analysis: 八字分析结果
        user_selected_chars: 用户选择的心仪字（可选）
        count: 生成数量（默认30个）

    Returns:
        批量名字建议
    """
    if user_selected_chars:
        mode = "基于用户选择"
        names = _generate_from_selected(
            user_selected_chars,
            suitable_chars,
            bazi_analysis,
            count
        )
    else:
        mode = "自动组合"
        names = _generate_auto(
            suitable_chars,
            bazi_analysis,
            count
        )

    return {
        "names": names,
        "count": len(names),
        "mode": mode,
        "bazi_analysis": bazi_analysis,
        "summary": f"已生成{len(names)}个名字（{mode}）"
    }


def _generate_from_selected(
    user_selected_chars: List[str],
    suitable_chars: Dict[str, Any],
    bazi_analysis: Dict[str, Any],
    count: int
) -> List[Dict[str, Any]]:
    """基于用户选择生成名字

    Args:
        user_selected_chars: 用户选择的字
        suitable_chars: 适合字字典
        bazi_analysis: 八字分析结果
        count: 生成数量

    Returns:
        名字列表
    """
    names = []
    suitable_chars_dict = suitable_chars.get("suitable_chars", {})

    # 从适合字中获取候选字
    all_candidates = []
    for wuxing, chars in suitable_chars_dict.items():
        all_candidates.extend(chars)

    # 为每个用户选择的字生成组合
    for selected_char in user_selected_chars:
        for candidate in all_candidates:
            if len(names) >= count:
                break

            char = candidate.get("char", "")

            # 组合成双字名
            name = selected_char + char

            # 确保不重复
            if any(n["name"] == name for n in names):
                continue

            name_info = _create_name_info(name, bazi_analysis, suitable_chars)
            names.append(name_info)

    # 补充名字直到达到目标数量
    while len(names) < count:
        # 随机组合用户选择的字
        name = "".join(random.sample(user_selected_chars, min(2, len(user_selected_chars))))

        if len(name) < 2:
            candidate = random.choice(all_candidates)
            name += candidate.get("char", "")

        # 确保不重复
        if any(n["name"] == name for n in names):
            continue

        name_info = _create_name_info(name, bazi_analysis, suitable_chars)
        names.append(name_info)

    return names[:count]


def _generate_auto(
    suitable_chars: Dict[str, Any],
    bazi_analysis: Dict[str, Any],
    count: int
) -> List[Dict[str, Any]]:
    """自动组合生成名字

    Args:
        suitable_chars: 适合字字典
        bazi_analysis: 八字分析结果
        count: 生成数量

    Returns:
        名字列表
    """
    names = []
    suitable_chars_dict = suitable_chars.get("suitable_chars", {})

    # 按优先级获取适合字
    yong_shen = bazi_analysis.get("yong_shen", "")
    xi_shen = bazi_analysis.get("xi_shen", "")

    # 获取用神和喜神的字
    priority_chars = []

    if yong_shen and yong_shen in suitable_chars_dict:
        priority_chars.extend(suitable_chars_dict[yong_shen][:10])

    if xi_shen and xi_shen in suitable_chars_dict:
        priority_chars.extend(suitable_chars_dict[xi_shen][:10])

    # 获取其他五行的字
    for wuxing in ["木", "火", "土", "金", "水"]:
        if wuxing not in [yong_shen, xi_shen] and wuxing in suitable_chars_dict:
            priority_chars.extend(suitable_chars_dict[wuxing][:5])

    # 生成双字名
    for i, char1 in enumerate(priority_chars):
        for j, char2 in enumerate(priority_chars):
            if len(names) >= count:
                break

            if i >= j:
                continue

            name = char1["char"] + char2["char"]

            # 检查平仄和谐
            pingze1 = char1.get("pingze", "")
            pingze2 = char2.get("pingze", "")

            if pingze1 and pingze2:
                if pingze1 == pingze2:
                    continue

            # 确保不重复
            if any(n["name"] == name for n in names):
                continue

            name_info = _create_name_info(name, bazi_analysis, suitable_chars)
            names.append(name_info)

    # 补充单字名
    while len(names) < count:
        char = random.choice(priority_chars)
        name = char["char"]

        # 确保不重复
        if any(n["name"] == name for n in names):
            continue

        name_info = _create_name_info(name, bazi_analysis, suitable_chars)
        names.append(name_info)

    return names[:count]


def _create_name_info(
    name: str,
    bazi_analysis: Dict[str, Any],
    suitable_chars: Dict[str, Any]
) -> Dict[str, Any]:
    """创建名字信息

    Args:
        name: 名字
        bazi_analysis: 八字分析结果
        suitable_chars: 适合字字典

    Returns:
        名字信息字典
    """
    from bazi_calculator.data.char_database import CharacterDatabase

    db = CharacterDatabase()
    db.set_char_library(suitable_chars.get("suitable_chars", {}))

    # 获取拼音
    pinyin_parts = []
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            pinyin_parts.append(char_info.get("pinyin", ""))
        else:
            pinyin_parts.append("")

    pinyin = " ".join(pinyin_parts)

    # 获取五行
    wuxing_dict = {}
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            wuxing_dict[char] = char_info.get("wuxing", "")

    # 获取平仄
    pingze_dict = {}
    for char in name:
        pingze = PingzePatterns.get_pingze(char)
        if pingze:
            pingze_dict[char] = pingze

    # 获取笔画
    strokes_dict = {}
    for char in name:
        strokes = KangxiStrokes.get_strokes(char)
        if strokes:
            strokes_dict[char] = strokes

    # 获取寓意
    meanings = []
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            meaning = char_info.get("meaning", "")
            if meaning:
                meanings.append(meaning)

    brief_meaning = "，".join(meanings)

    # 计算得分
    score = _calculate_name_score(name, bazi_analysis, suitable_chars)

    # 判断类型
    name_type = "单字" if len(name) == 1 else "双字"

    return {
        "name": name,
        "type": name_type,
        "pinyin": pinyin,
        "wuxing": wuxing_dict,
        "pingze": pingze_dict,
        "strokes": strokes_dict,
        "brief_meaning": brief_meaning,
        "score": score
    }


def _calculate_name_score(
    name: str,
    bazi_analysis: Dict[str, Any],
    suitable_chars: Dict[str, Any]
) -> int:
    """计算名字得分

    Args:
        name: 名字
        bazi_analysis: 八字分析结果
        suitable_chars: 适合字字典

    Returns:
        得分（0-100）
    """
    from bazi_calculator.data.char_database import CharacterDatabase

    db = CharacterDatabase()
    db.set_char_library(suitable_chars.get("suitable_chars", {}))

    yong_shen = bazi_analysis.get("yong_shen", "")
    xi_shen = bazi_analysis.get("xi_shen", "")

    score = 0

    # 检查是否包含用神
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            char_wuxing = char_info.get("wuxing", "")
            if char_wuxing == yong_shen:
                score += 30
            elif char_wuxing == xi_shen:
                score += 20

    # 平仄和谐检查
    pingzes = [PingzePatterns.get_pingze(char) for char in name]
    if all(pingzes):
        if len(set(pingzes)) > 1:
            score += 15

    # 笔画适中检查
    strokes = [KangxiStrokes.get_strokes(char) for char in name]
    if all(5 <= s <= 15 for s in strokes if s):
        score += 10

    # 总笔画适中
    total_strokes = sum(s for s in strokes if s)
    if 10 <= total_strokes <= 25:
        score += 10

    # 寓意优美（简单检查）
    meanings = []
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            meaning = char_info.get("meaning", "")
            if meaning:
                meanings.append(meaning)

    if meanings and len("".join(meanings)) > 5:
        score += 15

    return min(score, 100)


@tool
def format_batch_names(names: List[Dict[str, Any]]) -> str:
    """格式化批量名字为文本

    Args:
        names: 名字列表

    Returns:
        格式化后的文本
    """
    output = []
    output.append("=" * 60)
    output.append(f"批量名字建议（共{len(names)}个）")
    output.append("=" * 60)

    for i, name_info in enumerate(names, 1):
        name = name_info.get("name", "")
        name_type = name_info.get("type", "")
        pinyin = name_info.get("pinyin", "")
        brief_meaning = name_info.get("brief_meaning", "")
        score = name_info.get("score", 0)

        # 五行
        wuxing_dict = name_info.get("wuxing", {})
        wuxing_str = "，".join([f"{k}: {v}" for k, v in wuxing_dict.items()])

        # 平仄
        pingze_dict = name_info.get("pingze", {})
        pingze_str = "，".join([f"{k}: {v}" for k, v in pingze_dict.items()])

        output.append(f"\n{i}. {name}（{pinyin}）- {name_type}，评分{score}")
        output.append(f"   五行：{wuxing_str}")
        output.append(f"   平仄：{pingze_str}")
        output.append(f"   寓意：{brief_meaning}")

    output.append("\n" + "=" * 60)

    return "\n".join(output)


@tool
def filter_batch_names_by_score(
    names: List[Dict[str, Any]],
    min_score: int = 70
) -> List[Dict[str, Any]]:
    """按分数过滤批量名字

    Args:
        names: 名字列表
        min_score: 最低分数，默认70

    Returns:
        过滤后的名字列表
    """
    return [name for name in names if name.get("score", 0) >= min_score]
