"""八字取名分析工具

分析八字为取名提供指导，包括用神确定、生肖分析等
"""

from typing import Dict, Any, List
from langchain_core.tools import tool

from bazi_calculator.core.wuxing import WuxingAnalyzer
from bazi_calculator.data.zodiac_rules import ZodiacRules


@tool
def analyze_bazi_for_naming(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """分析八字为取名提供指导

    包括：
    - 用神、喜神、忌神分析
    - 生肖信息
    - 五行缺失和过多分析
    - 取名建议

    Args:
        bazi: 八字信息字典，包含四柱信息

    Returns:
        八字取名分析结果
    """
    # 获取年份（用于生肖）
    year = bazi.get("birth_info", {}).get("year", 0)

    # 获取生肖
    zodiac = ZodiacRules.get_zodiac_by_year(year)

    # 五行分析
    wuxing_analysis = WuxingAnalyzer.analyze_comprehensive(bazi)

    # 获取用神信息
    yong_shen_info = wuxing_analysis["yong_shen_info"]

    # 获取缺失和过多的五行
    missing_wuxing = wuxing_analysis.get("missing_wuxing", [])
    excessive_wuxing = wuxing_analysis.get("excessive_wuxing", [])

    # 生肖宜忌
    zodiac_favor_radicals = ZodiacRules.get_favor_radicals(zodiac)
    zodiac_avoid_radicals = ZodiacRules.get_avoid_radicals(zodiac)

    # 生成取名建议
    naming_suggestions = _generate_naming_suggestions(
        yong_shen_info,
        zodiac,
        missing_wuxing,
        excessive_wuxing
    )

    return {
        "zodiac": zodiac,
        "day_master": wuxing_analysis["summary"]["day_master"],
        "day_master_wuxing": wuxing_analysis["summary"]["day_master_wuxing"],
        "strength": wuxing_analysis["strength"],
        "yong_shen": yong_shen_info["yong_shen"],
        "xi_shen": yong_shen_info["xi_shen"],
        "ji_shen": yong_shen_info["ji_shen"],
        "missing_wuxing": missing_wuxing,
        "excessive_wuxing": excessive_wuxing,
        "zodiac_favor_radicals": zodiac_favor_radicals,
        "zodiac_avoid_radicals": zodiac_avoid_radicals,
        "naming_suggestions": naming_suggestions,
    }


@tool
def get_naming_priorities(
    bazi_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """获取取名优先级

    根据八字分析确定取名的优先级顺序

    Args:
        bazi_analysis: 八字分析结果

    Returns:
        取名优先级列表
    """
    yong_shen = bazi_analysis.get("yong_shen", "")
    xi_shen = bazi_analysis.get("xi_shen", "")
    missing_wuxing = bazi_analysis.get("missing_wuxing", [])
    excessive_wuxing = bazi_analysis.get("excessive_wuxing", [])

    # 确定优先级
    priorities = []

    # 1. 用神（最高优先级）
    if yong_shen:
        priorities.append({
            "priority": 1,
            "type": "用神",
            "wuxing": yong_shen,
            "reason": "用神为八字核心，取名首选"
        })

    # 2. 喜神（第二优先级）
    if xi_shen:
        priorities.append({
            "priority": 2,
            "type": "喜神",
            "wuxing": xi_shen,
            "reason": "喜神辅助用神，为次优选择"
        })

    # 3. 缺失的五行（第三优先级）
    for wuxing in missing_wuxing:
        priorities.append({
            "priority": 3,
            "type": "缺失五行",
            "wuxing": wuxing,
            "reason": f"{wuxing}五行缺失，可适当补充"
        })

    # 4. 其他五行（最低优先级）
    other_wuxing = ["木", "火", "土", "金", "水"]
    for wuxing in other_wuxing:
        if wuxing not in [yong_shen, xi_shen] and wuxing not in missing_wuxing and wuxing not in excessive_wuxing:
            priorities.append({
                "priority": 4,
                "type": "其他五行",
                "wuxing": wuxing,
                "reason": "可用，但优先级较低"
            })

    return {
        "priorities": priorities,
        "summary": f"取名顺序：用神({yong_shen}) > 喜神({xi_shen}) > 缺失五行({', '.join(missing_wuxing)})"
    }


@tool
def check_name_wuxing_balance(
    name: str,
    char_library: Dict[str, Any],
    bazi_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """检查名字的五行平衡

    Args:
        name: 名字
        char_library: 字库
        bazi_analysis: 八字分析结果

    Returns:
        五行平衡分析结果
    """
    from bazi_calculator.data.char_database import CharacterDatabase

    db = CharacterDatabase()
    db.set_char_library(char_library)

    yong_shen = bazi_analysis.get("yong_shen", "")
    xi_shen = bazi_analysis.get("xi_shen", "")
    ji_shen = bazi_analysis.get("ji_shen", [])

    # 获取名字中每个字的五行
    name_wuxing = []
    for char in name:
        char_info = db.get_char_info(char)
        if char_info:
            name_wuxing.append(char_info.get("wuxing", ""))
        else:
            name_wuxing.append("")

    # 检查是否包含用神
    has_yong_shen = yong_shen in name_wuxing

    # 检查是否包含喜神
    has_xi_shen = xi_shen in name_wuxing

    # 检查是否包含忌神
    has_ji_shen = any(js in name_wuxing for js in ji_shen)

    # 计算得分
    score = 0
    if has_yong_shen:
        score += 40
    if has_xi_shen:
        score += 30
    if not has_ji_shen:
        score += 30

    return {
        "name": name,
        "name_wuxing": name_wuxing,
        "has_yong_shen": has_yong_shen,
        "has_xi_shen": has_xi_shen,
        "has_ji_shen": has_ji_shen,
        "score": score,
        "evaluation": _get_wuxing_balance_evaluation(score)
    }


def _generate_naming_suggestions(
    yong_shen_info: Dict[str, Any],
    zodiac: str,
    missing_wuxing: List[str],
    excessive_wuxing: List[str]
) -> List[str]:
    """生成取名建议

    Args:
        yong_shen_info: 用神信息
        zodiac: 生肖
        missing_wuxing: 缺失的五行
        excessive_wuxing: 过多的五行

    Returns:
        建议列表
    """
    suggestions = []

    yong_shen = yong_shen_info["yong_shen"]
    xi_shen = yong_shen_info["xi_shen"]

    suggestions.append(f"用神为【{yong_shen}】，取名应优先选择{yong_shen}属性的汉字")

    if xi_shen:
        suggestions.append(f"喜神为【{xi_shen}】，次优选择{xi_shen}属性的汉字")

    if missing_wuxing:
        suggestions.append(f"八字缺失{', '.join(missing_wuxing)}，可适当补充")

    if excessive_wuxing:
        suggestions.append(f"八字{', '.join(excessive_wuxing)}过多，应避免使用")

    suggestions.append(f"生肖为{zodiac}，应选择符合生肖宜忌的字根")

    return suggestions


def _get_wuxing_balance_evaluation(score: int) -> str:
    """获取五行平衡评价

    Args:
        score: 得分

    Returns:
        评价文本
    """
    if score >= 80:
        return "五行搭配极佳，符合用神喜神"
    elif score >= 60:
        return "五行搭配较好"
    elif score >= 40:
        return "五行搭配一般"
    else:
        return "五行搭配有待改进"
