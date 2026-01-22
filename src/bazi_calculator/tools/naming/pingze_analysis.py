"""平仄分析工具

分析名字的平仄和谐度
"""

from typing import Dict, Any, List
from langchain_core.tools import tool

from bazi_calculator.data.pingze_patterns import PingzePatterns


@tool
def analyze_name_pingze(name: str) -> Dict[str, Any]:
    """分析名字的平仄

    Args:
        name: 名字

    Returns:
        平仄分析结果
    """
    tones = []
    pingzes = []

    for char in name:
        tone = PingzePatterns.get_tone(char)
        pingze = PingzePatterns.get_pingze(char)
        tones.append(tone if tone is not None else 0)
        pingzes.append(pingze if pingze is not None else "平")

    pattern = "".join(pingzes)

    return {
        "name": name,
        "tones": tones,
        "pingzes": pingzes,
        "pattern": pattern,
        "length": len(name)
    }


@tool
def check_pingze_harmony(name: str) -> Dict[str, Any]:
    """检查名字的平仄和谐度

    Args:
        name: 名字

    Returns:
        和谐度分析结果
    """
    analysis = PingzePatterns.check_harmony(name)

    return {
        "name": name,
        "pattern": analysis["pattern"],
        "is_favorable": analysis["is_favorable"],
        "score": analysis["score"],
        "description": analysis["description"]
    }


@tool
def compare_name_pingze(name1: str, name2: str) -> Dict[str, Any]:
    """比较两个名字的平仄

    Args:
        name1: 名字1
        name2: 名字2

    Returns:
        比较结果
    """
    harmony1 = PingzePatterns.check_harmony(name1)
    harmony2 = PingzePatterns.check_harmony(name2)

    return {
        "name1": {
            "name": name1,
            "pattern": harmony1["pattern"],
            "score": harmony1["score"],
            "description": harmony1["description"]
        },
        "name2": {
            "name": name2,
            "pattern": harmony2["pattern"],
            "score": harmony2["score"],
            "description": harmony2["description"]
        },
        "better": name1 if harmony1["score"] >= harmony2["score"] else name2,
        "difference": abs(harmony1["score"] - harmony2["score"])
    }


@tool
def get_pingze_suggestions(
    chars_list: List[List[str]],
    preferred_pattern: str = None
) -> List[Dict[str, Any]]:
    """根据平仄模式生成名字建议

    Args:
        chars_list: 字符列表的列表
        preferred_pattern: 首选的平仄模式（可选）

    Returns:
        名字建议列表
    """
    suggestions = PingzePatterns.get_suggestions(chars_list, preferred_pattern)

    return [
        {
            "name": name,
            "pattern": harmony["pattern"],
            "score": harmony["score"],
            "description": harmony["description"]
        }
        for name, harmony in suggestions[:20]
    ]


@tool
def format_pingze_analysis(analysis: Dict[str, Any]) -> str:
    """格式化平仄分析为文本

    Args:
        analysis: 平仄分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    pattern = analysis.get("pattern", "")
    is_favorable = analysis.get("is_favorable", False)
    score = analysis.get("score", 0)
    description = analysis.get("description", "")

    output = []
    output.append("=" * 50)
    output.append("平仄分析")
    output.append("=" * 50)
    output.append(f"\n名字：{name}")
    output.append(f"平仄模式：{pattern}")

    if is_favorable:
        output.append("✅ 平仄模式优选")
    else:
        output.append("⚠️  平仄模式一般")

    output.append(f"得分：{score}/100")
    output.append(f"评价：{description}")
    output.append("\n" + "=" * 50)

    return "\n".join(output)


@tool
def check_multiple_names_pingze(names: List[str]) -> Dict[str, Any]:
    """批量检查多个名字的平仄

    Args:
        names: 名字列表

    Returns:
        批量分析结果
    """
    results = []

    for name in names:
        harmony = PingzePatterns.check_harmony(name)
        results.append({
            "name": name,
            "pattern": harmony["pattern"],
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
def get_pingze_pattern_statistics(name: str) -> Dict[str, Any]:
    """获取名字平仄模式的统计信息

    Args:
        name: 名字

    Returns:
        统计信息
    """
    pingzes = []

    for char in name:
        pingze = PingzePatterns.get_pingze(char)
        if pingze:
            pingzes.append(pingze)

    if not pingzes:
        return {
            "name": name,
            "total_chars": len(name),
            "ping_count": 0,
            "ze_count": 0,
            "ping_ratio": 0,
            "ze_ratio": 0
        }

    ping_count = pingzes.count("平")
    ze_count = pingzes.count("仄")
    total = len(pingzes)

    return {
        "name": name,
        "total_chars": total,
        "ping_count": ping_count,
        "ze_count": ze_count,
        "ping_ratio": ping_count / total,
        "ze_ratio": ze_count / total,
        "pattern": "".join(pingzes)
    }
