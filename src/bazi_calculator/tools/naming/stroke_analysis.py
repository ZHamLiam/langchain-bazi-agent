"""笔画分析工具

分析名字的康熙字典笔画
"""

from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

from bazi_calculator.data.kangxi_strokes import KangxiStrokes


@tool
def analyze_name_strokes(name: str) -> Dict[str, Any]:
    """分析名字的康熙字典笔画

    Args:
        name: 名字

    Returns:
        笔画分析结果
    """
    strokes_dict = {}
    strokes_list = []

    for char in name:
        strokes = KangxiStrokes.get_strokes(char)
        strokes_dict[char] = strokes
        if strokes is not None:
            strokes_list.append(strokes)

    total_strokes = sum(strokes_list) if strokes_list else 0
    average_strokes = total_strokes / len(strokes_list) if strokes_list else 0

    return {
        "name": name,
        "strokes_dict": strokes_dict,
        "strokes_list": strokes_list,
        "total_strokes": total_strokes,
        "average_strokes": round(average_strokes, 1),
        "char_count": len(name)
    }


@tool
def check_strokes_harmony(name: str) -> Dict[str, Any]:
    """检查名字的笔画和谐度

    Args:
        name: 名字

    Returns:
        和谐度分析结果
    """
    analysis = analyze_name_strokes(name)
    total_strokes = analysis["total_strokes"]
    average_strokes = analysis["average_strokes"]
    strokes_list = analysis["strokes_list"]

    # 评价标准
    score = 0
    evaluations = []

    # 总笔画适中（10-25画）
    if 10 <= total_strokes <= 25:
        score += 40
        evaluations.append("总笔画适中")
    elif 5 <= total_strokes <= 30:
        score += 30
        evaluations.append("总笔画尚可")
    else:
        score += 10
        evaluations.append("总笔画不理想")

    # 平均笔画适中（5-15画）
    if 5 <= average_strokes <= 15:
        score += 30
        evaluations.append("平均笔画适中")
    elif 3 <= average_strokes <= 18:
        score += 20
        evaluations.append("平均笔画尚可")
    else:
        score += 10
        evaluations.append("平均笔画不理想")

    # 笔画分布均匀
    if strokes_list:
        stroke_range = max(strokes_list) - min(strokes_list)
        if stroke_range <= 5:
            score += 20
            evaluations.append("笔画分布均匀")
        elif stroke_range <= 10:
            score += 15
            evaluations.append("笔画分布较为均匀")
        else:
            score += 10
            evaluations.append("笔画分布不均匀")

    # 无过多笔画字
    if all(s <= 20 for s in strokes_list):
        score += 10
        evaluations.append("无过多笔画字")

    return {
        "name": name,
        "total_strokes": total_strokes,
        "average_strokes": round(average_strokes, 1),
        "score": min(score, 100),
        "evaluations": evaluations,
        "description": _get_strokes_description(score)
    }


@tool
def compare_name_strokes(name1: str, name2: str) -> Dict[str, Any]:
    """比较两个名字的笔画

    Args:
        name1: 名字1
        name2: 名字2

    Returns:
        比较结果
    """
    harmony1 = check_strokes_harmony(name1)
    harmony2 = check_strokes_harmony(name2)

    return {
        "name1": {
            "name": name1,
            "total_strokes": harmony1["total_strokes"],
            "average_strokes": harmony1["average_strokes"],
            "score": harmony1["score"],
            "description": harmony1["description"]
        },
        "name2": {
            "name": name2,
            "total_strokes": harmony2["total_strokes"],
            "average_strokes": harmony2["average_strokes"],
            "score": harmony2["score"],
            "description": harmony2["description"]
        },
        "better": name1 if harmony1["score"] >= harmony2["score"] else name2,
        "difference": abs(harmony1["score"] - harmony2["score"])
    }


@tool
def get_strokes_suggestions(
    chars_list: List[List[str]],
    min_total_strokes: int = 10,
    max_total_strokes: int = 25
) -> List[Dict[str, Any]]:
    """根据笔画数生成名字建议

    Args:
        chars_list: 字符列表的列表
        min_total_strokes: 最小总笔画数，默认10
        max_total_strokes: 最大总笔画数，默认25

    Returns:
        名字建议列表
    """
    import itertools

    suggestions = []

    for chars in chars_list:
        for name_tuple in itertools.product(*chars):
            name = "".join(name_tuple)
            analysis = check_strokes_harmony(name)

            if min_total_strokes <= analysis["total_strokes"] <= max_total_strokes:
                suggestions.append({
                    "name": name,
                    "total_strokes": analysis["total_strokes"],
                    "score": analysis["score"],
                    "description": analysis["description"]
                })

    # 按分数排序
    suggestions.sort(key=lambda x: x["score"], reverse=True)

    return suggestions[:20]


@tool
def format_strokes_analysis(analysis: Dict[str, Any]) -> str:
    """格式化笔画分析为文本

    Args:
        analysis: 笔画分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    strokes_dict = analysis.get("strokes_dict", {})
    total_strokes = analysis.get("total_strokes", 0)
    average_strokes = analysis.get("average_strokes", 0)
    score = analysis.get("score", 0)
    evaluations = analysis.get("evaluations", [])
    description = analysis.get("description", "")

    output = []
    output.append("=" * 50)
    output.append("笔画分析")
    output.append("=" * 50)
    output.append(f"\n名字：{name}")

    for char, strokes in strokes_dict.items():
        if strokes is not None:
            output.append(f"{char}：{strokes}画")
        else:
            output.append(f"{char}：未知")

    output.append(f"\n总笔画：{total_strokes}画")
    output.append(f"平均笔画：{average_strokes}画")
    output.append(f"得分：{score}/100")
    output.append(f"\n评价：")
    for evaluation in evaluations:
        output.append(f"  - {evaluation}")
    output.append(f"\n总结：{description}")
    output.append("\n" + "=" * 50)

    return "\n".join(output)


@tool
def check_multiple_names_strokes(names: List[str]) -> Dict[str, Any]:
    """批量检查多个名字的笔画

    Args:
        names: 名字列表

    Returns:
        批量分析结果
    """
    results = []

    for name in names:
        harmony = check_strokes_harmony(name)
        results.append({
            "name": name,
            "total_strokes": harmony["total_strokes"],
            "average_strokes": harmony["average_strokes"],
            "score": harmony["score"],
            "description": harmony["description"]
        })

    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "results": results,
        "best": results[0] if results else None,
        "worst": results[-1] if results else None,
        "average": sum(r["score"] for r in results) / len(results) if results else 0
    }


@tool
def get_strokes_by_range(
    name: str,
    min_strokes: int,
    max_strokes: int
) -> Dict[str, Any]:
    """获取名字中指定笔画范围的字

    Args:
        name: 名字
        min_strokes: 最小笔画数
        max_strokes: 最大笔画数

    Returns:
        符合条件的字列表
    """
    matching_chars = []

    for char in name:
        strokes = KangxiStrokes.get_strokes(char)
        if strokes is not None and min_strokes <= strokes <= max_strokes:
            matching_chars.append({
                "char": char,
                "strokes": strokes
            })

    return {
        "name": name,
        "min_strokes": min_strokes,
        "max_strokes": max_strokes,
        "matching_chars": matching_chars,
        "count": len(matching_chars)
    }


def _get_strokes_description(score: int) -> str:
    """获取笔画描述

    Args:
        score: 得分

    Returns:
        描述文本
    """
    if score >= 80:
        return "笔画搭配极佳，书写流畅美观"
    elif score >= 60:
        return "笔画搭配较好"
    elif score >= 40:
        return "笔画搭配一般"
    else:
        return "笔画搭配有待改进"
