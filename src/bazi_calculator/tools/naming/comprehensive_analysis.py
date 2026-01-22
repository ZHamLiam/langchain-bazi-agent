"""综合凶吉分析工具

整合八字、平仄、笔画、三才五格等分析，给出综合评分
"""

from typing import Dict, Any, List
from langchain_core.tools import tool

from bazi_calculator.tools.naming.bazi_for_naming import check_name_wuxing_balance
from bazi_calculator.tools.naming.pingze_analysis import check_pingze_harmony
from bazi_calculator.tools.naming.stroke_analysis import check_strokes_harmony
from bazi_calculator.tools.naming.sangcai_wuge import analyze_sancai_wuge


@tool
def comprehensive_name_analysis(
    name: str,
    bazi_analysis: Dict[str, Any],
    char_library: Dict[str, Any],
    surname: str = "李"
) -> Dict[str, Any]:
    """综合分析名字的凶吉

    整合以下分析：
    - 八字五行匹配度
    - 平仄和谐度
    - 笔画和谐度
    - 三才五格吉凶

    Args:
        name: 名字
        bazi_analysis: 八字分析结果
        char_library: 字库
        surname: 姓氏

    Returns:
        综合分析结果
    """
    # 八字五行分析
    wuxing_result = check_name_wuxing_balance(name, char_library, bazi_analysis)

    # 平仄分析
    pingze_result = check_pingze_harmony(name)

    # 笔画分析
    stroke_result = check_strokes_harmony(name)

    # 三才五格分析
    sangcai_wuge_result = analyze_sancai_wuge(name, surname)

    # 计算综合得分
    overall_score = _calculate_overall_score(
        wuxing_result,
        pingze_result,
        stroke_result,
        sangcai_wuge_result
    )

    # 生成综合评价
    evaluation = _get_comprehensive_evaluation(overall_score)

    # 生成建议
    suggestions = _generate_comprehensive_suggestions(
        wuxing_result,
        pingze_result,
        stroke_result,
        sangcai_wuge_result
    )

    return {
        "name": name,
        "surname": surname,
        "bazi_analysis": bazi_analysis,
        "wuxing_analysis": wuxing_result,
        "pingze_analysis": pingze_result,
        "stroke_analysis": stroke_result,
        "sangcai_wuge_analysis": sangcai_wuge_result,
        "overall_score": overall_score,
        "evaluation": evaluation,
        "suggestions": suggestions
    }


@tool
def compare_names_comprehensive(
    names: List[str],
    bazi_analysis: Dict[str, Any],
    char_library: Dict[str, Any],
    surname: str = "李"
) -> Dict[str, Any]:
    """批量比较多个名字的综合凶吉

    Args:
        names: 名字列表
        bazi_analysis: 八字分析结果
        char_library: 字库
        surname: 姓氏

    Returns:
        批量比较结果
    """
    results = []

    for name in names:
        result = comprehensive_name_analysis(name, bazi_analysis, char_library, surname)
        results.append({
            "name": name,
            "overall_score": result["overall_score"],
            "evaluation": result["evaluation"],
            "wuxing_score": result["wuxing_analysis"]["score"],
            "pingze_score": result["pingze_analysis"]["score"],
            "stroke_score": result["stroke_analysis"]["score"],
            "sangcai_wuge_score": result["sangcai_wuge_analysis"]["overall_score"]
        })

    # 按综合得分排序
    results.sort(key=lambda x: x["overall_score"], reverse=True)

    return {
        "results": results,
        "best": results[0] if results else None,
        "worst": results[-1] if results else None,
        "average": sum(r["overall_score"] for r in results) / len(results) if results else 0
    }


@tool
def get_best_names(
    names: List[str],
    bazi_analysis: Dict[str, Any],
    char_library: Dict[str, Any],
    surname: str = "李",
    top_count: int = 5
) -> Dict[str, Any]:
    """获取最佳名字

    Args:
        names: 名字列表
        bazi_analysis: 八字分析结果
        char_library: 字库
        surname: 姓氏
        top_count: 返回的顶级名字数

    Returns:
        最佳名字列表
    """
    comparison = compare_names_comprehensive(names, bazi_analysis, char_library, surname)

    return {
        "best_names": comparison["results"][:top_count],
        "top_count": top_count
    }


@tool
def format_comprehensive_analysis(analysis: Dict[str, Any]) -> str:
    """格式化综合分析为文本

    Args:
        analysis: 综合分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    surname = analysis.get("surname", "")
    overall_score = analysis.get("overall_score", 0)
    evaluation = analysis.get("evaluation", "")

    wuxing_analysis = analysis.get("wuxing_analysis", {})
    pingze_analysis = analysis.get("pingze_analysis", {})
    stroke_analysis = analysis.get("stroke_analysis", {})
    sangcai_wuge_analysis = analysis.get("sangcai_wuge_analysis", {})

    suggestions = analysis.get("suggestions", [])

    output = []
    output.append("=" * 70)
    output.append(f"{surname}{name} - 综合凶吉分析")
    output.append("=" * 70)

    output.append(f"\n【综合评分】")
    output.append(f"综合得分：{overall_score}/100")
    output.append(f"综合评价：{evaluation}")

    output.append(f"\n【分项评分】")
    output.append(f"八字五行：{wuxing_analysis.get('score', 0)}/100")
    output.append(f"平仄和谐：{pingze_analysis.get('score', 0)}/100")
    output.append(f"笔画和谐：{stroke_analysis.get('score', 0)}/100")
    output.append(f"三才五格：{sangcai_wuge_analysis.get('overall_score', 0)}/100")

    output.append(f"\n【详细分析】")

    output.append(f"\n1. 八字五行分析")
    output.append(f"   得分：{wuxing_analysis.get('score', 0)}/100")
    output.append(f"   {wuxing_analysis.get('evaluation', '')}")
    if wuxing_analysis.get('has_yong_shen'):
        output.append(f"   ✅ 包含用神")
    else:
        output.append(f"   ❌ 不含用神")

    output.append(f"\n2. 平仄分析")
    output.append(f"   得分：{pingze_analysis.get('score', 0)}/100")
    output.append(f"   模式：{pingze_analysis.get('pattern', '')}")
    output.append(f"   {pingze_analysis.get('description', '')}")
    if pingze_analysis.get('is_favorable'):
        output.append(f"   ✅ 平仄模式优选")
    else:
        output.append(f"   ⚠️  平仄模式一般")

    output.append(f"\n3. 笔画分析")
    output.append(f"   得分：{stroke_analysis.get('score', 0)}/100")
    output.append(f"   总笔画：{stroke_analysis.get('total_strokes', 0)}画")
    output.append(f"   平均笔画：{stroke_analysis.get('average_strokes', 0)}画")
    output.append(f"   {stroke_analysis.get('description', '')}")

    output.append(f"\n4. 三才五格分析")
    output.append(f"   得分：{sangcai_wuge_analysis.get('overall_score', 0)}/100")
    output.append(f"   三才配置：{sangcai_wuge_analysis.get('sancai', {}).get('sancai_pattern', '')}")
    output.append(f"   {sangcai_wuge_analysis.get('evaluation', '')}")

    output.append(f"\n【改进建议】")
    for i, suggestion in enumerate(suggestions, 1):
        output.append(f"{i}. {suggestion}")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def _calculate_overall_score(
    wuxing_result: Dict[str, Any],
    pingze_result: Dict[str, Any],
    stroke_result: Dict[str, Any],
    sangcai_wuge_result: Dict[str, Any]
) -> float:
    """计算综合得分

    权重分配：
    - 八字五行：35%
    - 平仄和谐：25%
    - 笔画和谐：20%
    - 三才五格：20%

    Args:
        wuxing_result: 八字五行分析结果
        pingze_result: 平仄分析结果
        stroke_result: 笔画分析结果
        sangcai_wuge_result: 三才五格分析结果

    Returns:
        综合得分（0-100）
    """
    wuxing_score = wuxing_result.get("score", 0)
    pingze_score = pingze_result.get("score", 0)
    stroke_score = stroke_result.get("score", 0)
    sangcai_wuge_score = sangcai_wuge_result.get("overall_score", 0)

    overall_score = (
        wuxing_score * 0.35 +
        pingze_score * 0.25 +
        stroke_score * 0.20 +
        sangcai_wuge_score * 0.20
    )

    return round(overall_score, 1)


def _get_comprehensive_evaluation(score: float) -> str:
    """获取综合评价

    Args:
        score: 综合得分

    Returns:
        评价文本
    """
    if score >= 90:
        return "极佳，强烈推荐"
    elif score >= 80:
        return "很好，推荐使用"
    elif score >= 70:
        return "较好，可以考虑"
    elif score >= 60:
        return "一般，需要斟酌"
    else:
        return "不理想，不建议使用"


def _generate_comprehensive_suggestions(
    wuxing_result: Dict[str, Any],
    pingze_result: Dict[str, Any],
    stroke_result: Dict[str, Any],
    sangcai_wuge_result: Dict[str, Any]
) -> List[str]:
    """生成综合建议

    Args:
        wuxing_result: 八字五行分析结果
        pingze_result: 平仄分析结果
        stroke_result: 笔画分析结果
        sangcai_wuge_result: 三才五格分析结果

    Returns:
        建议列表
    """
    suggestions = []

    # 八字五行建议
    wuxing_score = wuxing_result.get("score", 0)
    if wuxing_score < 70:
        if not wuxing_result.get("has_yong_shen"):
            suggestions.append("名字不包含用神，建议选择用神属性的字")
        else:
            suggestions.append("八字五行匹配度一般，可以考虑增强用神属性的字")

    # 平仄建议
    pingze_score = pingze_result.get("score", 0)
    if pingze_score < 70:
        suggestions.append("平仄搭配不够和谐，建议调整平仄搭配")
    elif not pingze_result.get("is_favorable"):
        suggestions.append("平仄模式不是最优组合，可以考虑优化")

    # 笔画建议
    stroke_score = stroke_result.get("score", 0)
    if stroke_score < 70:
        total_strokes = stroke_result.get("total_strokes", 0)
        if total_strokes < 10:
            suggestions.append("总笔画偏少，建议增加笔画")
        elif total_strokes > 25:
            suggestions.append("总笔画偏多，建议减少笔画")
        else:
            suggestions.append("笔画搭配有待改进")

    # 三才五格建议
    sangcai_wuge_score = sangcai_wuge_result.get("overall_score", 0)
    if sangcai_wuge_score < 70:
        suggestions.append("三才五格不够吉利，可以考虑调整")

    # 如果各项都很好
    if all(score >= 80 for score in [
        wuxing_score, pingze_score, stroke_score, sangcai_wuge_score
    ]):
        suggestions.append("各项分析都很好，这是一个优秀的名字")

    return suggestions
