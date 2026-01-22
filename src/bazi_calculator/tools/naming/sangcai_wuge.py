"""三才五格分析工具

分析名字的三才五格吉凶
"""

from typing import Dict, Any, List
from langchain_core.tools import tool

from bazi_calculator.data.kangxi_strokes import KangxiStrokes


class SangcaiWuge:
    """三才五格分析器"""

    # 五格数理吉凶评分（1-81）
    WUGE_SCORES = {
        1: 100, 2: 50, 3: 100, 4: 40, 5: 100, 6: 100, 7: 100, 8: 100, 9: 50,
        10: 50, 11: 100, 12: 40, 13: 100, 14: 40, 15: 100, 16: 100, 17: 100, 18: 100, 19: 40,
        20: 40, 21: 100, 22: 40, 23: 100, 24: 80, 25: 100, 26: 60, 27: 50, 28: 60, 29: 60,
        30: 60, 31: 100, 32: 100, 33: 100, 34: 50, 35: 100, 36: 100, 37: 100, 38: 100, 39: 50,
        40: 50, 41: 100, 42: 50, 43: 40, 44: 40, 45: 100, 46: 50, 47: 80, 48: 80, 49: 40,
        50: 40, 51: 100, 52: 100, 53: 80, 54: 40, 55: 80, 56: 60, 57: 60, 58: 100, 59: 40,
        60: 60, 61: 100, 62: 60, 63: 80, 64: 60, 65: 80, 66: 50, 67: 80, 68: 60, 69: 60,
        70: 60, 71: 80, 72: 60, 73: 80, 74: 50, 75: 80, 76: 60, 77: 80, 78: 60, 79: 50,
        80: 50, 81: 100
    }

    # 三才配置吉凶评分
    SANCAI_SCORES = {
        "木木木": 90, "木木火": 90, "木木土": 70, "木木金": 50, "木木水": 80,
        "木火木": 80, "木火火": 80, "木火土": 60, "木火金": 40, "木火水": 70,
        "木土木": 60, "木土火": 50, "木土土": 60, "木土金": 40, "木土水": 50,
        "木金木": 50, "木金火": 40, "木金土": 40, "木金金": 40, "木金水": 50,
        "木水木": 70, "木水火": 60, "木水土": 50, "木水金": 50, "木水水": 70,
        "火木木": 80, "火木火": 80, "火木土": 60, "火木金": 40, "火木水": 70,
        "火火木": 80, "火火火": 80, "火火土": 70, "火火金": 50, "火火水": 80,
        "火土木": 60, "火土火": 60, "火土土": 60, "火土金": 40, "火土水": 50,
        "火金木": 40, "火金火": 50, "火金土": 40, "火金金": 40, "火金水": 50,
        "火水木": 70, "火水火": 80, "火水土": 50, "火水金": 50, "火水水": 70,
        "土木木": 70, "土木火": 60, "土木土": 80, "土木金": 50, "土木水": 60,
        "土火木": 60, "土火火": 70, "土火土": 80, "土火金": 60, "土火水": 60,
        "土土木": 80, "土土火": 80, "土土土": 90, "土土金": 70, "土土水": 80,
        "土金木": 50, "土金火": 60, "土金土": 70, "土金金": 70, "土金水": 70,
        "土水木": 60, "土水火": 60, "土水土": 80, "土水金": 70, "土水水": 80,
        "金木木": 50, "金木火": 40, "金木土": 50, "金木金": 70, "金木水": 60,
        "金火木": 40, "金火火": 50, "金火土": 60, "金火金": 70, "金火水": 60,
        "金土木": 50, "金土火": 60, "金土土": 70, "金土金": 70, "金土水": 70,
        "金金木": 70, "金金火": 60, "金金土": 70, "金金金": 70, "金金水": 70,
        "金水木": 60, "金水火": 60, "金水土": 70, "金水金": 70, "金水水": 70,
        "水木木": 80, "水木火": 70, "水木土": 60, "水木金": 60, "水木水": 90,
        "水火木": 70, "水火火": 80, "水火土": 50, "水火金": 60, "水火水": 80,
        "水土木": 60, "水土火": 50, "水土土": 80, "水土金": 70, "水土水": 80,
        "水金木": 60, "水金火": 60, "水金土": 70, "水金金": 70, "水金水": 70,
        "水水木": 90, "水水火": 80, "水水土": 80, "水水金": 70, "水水水": 90
    }

    @staticmethod
    def _get_number_wuxing(num: int) -> str:
        """获取数字对应的五行

        1, 2: 木
        3, 4: 火
        5, 6: 土
        7, 8: 金
        9, 0: 水

        Args:
            num: 数字

        Returns:
            五行
        """
        last_digit = num % 10
        if last_digit in [1, 2]:
            return "木"
        elif last_digit in [3, 4]:
            return "火"
        elif last_digit in [5, 6]:
            return "土"
        elif last_digit in [7, 8]:
            return "金"
        else:
            return "水"


def _calculate_wuge_internal(
    name: str,
    surname: str = "李"
) -> Dict[str, Any]:
    """计算五格（内部函数，不带装饰器）

    五格包括：天格、人格、地格、外格、总格

    Args:
        name: 名字
        surname: 姓氏，默认"李"

    Returns:
        五格计算结果
    """
    strokes_list = []

    # 姓氏笔画
    surname_strokes = KangxiStrokes.get_strokes(surname)
    if surname_strokes is None:
        surname_strokes = 0
    strokes_list.append(surname_strokes)

    # 名字笔画
    for char in name:
        strokes = KangxiStrokes.get_strokes(char)
        if strokes is None:
            strokes = 0
        strokes_list.append(strokes)

    # 计算五格
    if len(name) == 1:
        # 单字名
        tian_ge = surname_strokes + 1
        ren_ge = surname_strokes + strokes_list[1]
        di_ge = strokes_list[1] + 1
        wai_ge = 2
        zong_ge = surname_strokes + strokes_list[1] + 1
    else:
        # 双字名
        tian_ge = surname_strokes + 1
        ren_ge = surname_strokes + strokes_list[1]
        di_ge = strokes_list[1] + strokes_list[2]
        wai_ge = strokes_list[0] + strokes_list[2]
        zong_ge = surname_strokes + strokes_list[1] + strokes_list[2]

    # 获取五格评分
    tian_ge_score = SangcaiWuge.WUGE_SCORES.get(tian_ge, 60)
    ren_ge_score = SangcaiWuge.WUGE_SCORES.get(ren_ge, 60)
    di_ge_score = SangcaiWuge.WUGE_SCORES.get(di_ge, 60)
    wai_ge_score = SangcaiWuge.WUGE_SCORES.get(wai_ge, 60)
    zong_ge_score = SangcaiWuge.WUGE_SCORES.get(zong_ge, 60)

    return {
        "name": name,
        "surname": surname,
        "tian_ge": tian_ge,
        "ren_ge": ren_ge,
        "di_ge": di_ge,
        "wai_ge": wai_ge,
        "zong_ge": zong_ge,
        "tian_ge_score": tian_ge_score,
        "ren_ge_score": ren_ge_score,
        "di_ge_score": di_ge_score,
        "wai_ge_score": wai_ge_score,
        "zong_ge_score": zong_ge_score,
        "average_score": (tian_ge_score + ren_ge_score + di_ge_score + wai_ge_score + zong_ge_score) / 5
    }


@tool
def calculate_wuge(
    name: str,
    surname: str = "李"
) -> Dict[str, Any]:
    """计算五格

    五格包括：天格、人格、地格、外格、总格

    Args:
        name: 名字
        surname: 姓氏，默认"李"

    Returns:
        五格计算结果
    """
    return _calculate_wuge_internal(name, surname)


def _calculate_sancai_internal(wuge_result: Dict[str, Any]) -> Dict[str, Any]:
    """计算三才（内部函数，不带装饰器）

    三才由天格、人格、地格的五行组成

    Args:
        wuge_result: 五格计算结果

    Returns:
        三才计算结果
    """
    tian_ge = wuge_result.get("tian_ge", 0)
    ren_ge = wuge_result.get("ren_ge", 0)
    di_ge = wuge_result.get("di_ge", 0)

    # 获取五行
    tian_wuxing = SangcaiWuge._get_number_wuxing(tian_ge)
    ren_wuxing = SangcaiWuge._get_number_wuxing(ren_ge)
    di_wuxing = SangcaiWuge._get_number_wuxing(di_ge)

    sancai_pattern = tian_wuxing + ren_wuxing + di_wuxing

    # 获取评分
    sancai_score = SangcaiWuge.SANCAI_SCORES.get(sancai_pattern, 60)

    return {
        "tian_wuxing": tian_wuxing,
        "ren_wuxing": ren_wuxing,
        "di_wuxing": di_wuxing,
        "sancai_pattern": sancai_pattern,
        "sancai_score": sancai_score
    }


@tool
def calculate_sancai(wuge_result: Dict[str, Any]) -> Dict[str, Any]:
    """计算三才

    三才由天格、人格、地格的五行组成

    Args:
        wuge_result: 五格计算结果

    Returns:
        三才计算结果
    """
    return _calculate_sancai_internal(wuge_result)


@tool
def analyze_sancai_wuge(
    name: str,
    surname: str = "李"
) -> Dict[str, Any]:
    """综合分析三才五格

    Args:
        name: 名字
        surname: 姓氏

    Returns:
        综合分析结果
    """
    # 计算五格（使用内部函数）
    wuge = _calculate_wuge_internal(name, surname)

    # 计算三才（使用内部函数）
    sancai = _calculate_sancai_internal(wuge)

    # 综合评分
    wuge_scores = [
        wuge["tian_ge_score"],
        wuge["ren_ge_score"],
        wuge["di_ge_score"],
        wuge["wai_ge_score"],
        wuge["zong_ge_score"]
    ]

    sancai_score = sancai["sancai_score"]

    # 综合得分（五格占70%，三才占30%）
    overall_score = (sum(wuge_scores) / 5) * 0.7 + sancai_score * 0.3

    return {
        "name": name,
        "surname": surname,
        "wuge": wuge,
        "sancai": sancai,
        "overall_score": round(overall_score, 1),
        "evaluation": _get_sancai_wuge_evaluation(overall_score)
    }


@tool
def format_sancai_wuge_analysis(analysis: Dict[str, Any]) -> str:
    """格式化三才五格分析为文本

    Args:
        analysis: 分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    surname = analysis.get("surname", "")
    wuge = analysis.get("wuge", {})
    sancai = analysis.get("sancai", {})
    overall_score = analysis.get("overall_score", 0)
    evaluation = analysis.get("evaluation", "")

    output = []
    output.append("=" * 60)
    output.append("三才五格分析")
    output.append("=" * 60)
    output.append(f"\n姓氏：{surname}")
    output.append(f"名字：{name}")

    output.append("\n【五格】")
    output.append(f"天格：{wuge['tian_ge']}（得分{wuge['tian_ge_score']}）")
    output.append(f"人格：{wuge['ren_ge']}（得分{wuge['ren_ge_score']}）")
    output.append(f"地格：{wuge['di_ge']}（得分{wuge['di_ge_score']}）")
    output.append(f"外格：{wuge['wai_ge']}（得分{wuge['wai_ge_score']}）")
    output.append(f"总格：{wuge['zong_ge']}（得分{wuge['zong_ge_score']}）")

    output.append("\n【三才】")
    output.append(f"天格五行：{sancai['tian_wuxing']}")
    output.append(f"人格五行：{sancai['ren_wuxing']}")
    output.append(f"地格五行：{sancai['di_wuxing']}")
    output.append(f"三才配置：{sancai['sancai_pattern']}（得分{sancai['sancai_score']}）")

    output.append(f"\n【综合评价】")
    output.append(f"综合得分：{overall_score}/100")
    output.append(f"评价：{evaluation}")
    output.append("\n" + "=" * 60)

    return "\n".join(output)


@tool
def compare_sancai_wuge(name1: str, name2: str, surname: str = "李") -> Dict[str, Any]:
    """比较两个名字的三才五格

    Args:
        name1: 名字1
        name2: 名字2
        surname: 姓氏

    Returns:
        比较结果
    """
    # 使用内部函数计算
    wuge1 = _calculate_wuge_internal(name1, surname)
    sancai1 = _calculate_sancai_internal(wuge1)
    overall_score1 = (sum([
        wuge1["tian_ge_score"],
        wuge1["ren_ge_score"],
        wuge1["di_ge_score"],
        wuge1["wai_ge_score"],
        wuge1["zong_ge_score"]
    ]) / 5) * 0.7 + sancai1["sancai_score"] * 0.3

    wuge2 = _calculate_wuge_internal(name2, surname)
    sancai2 = _calculate_sancai_internal(wuge2)
    overall_score2 = (sum([
        wuge2["tian_ge_score"],
        wuge2["ren_ge_score"],
        wuge2["di_ge_score"],
        wuge2["wai_ge_score"],
        wuge2["zong_ge_score"]
    ]) / 5) * 0.7 + sancai2["sancai_score"] * 0.3

    return {
        "name1": {
            "name": name1,
            "overall_score": round(overall_score1, 1),
            "evaluation": _get_sancai_wuge_evaluation(overall_score1)
        },
        "name2": {
            "name": name2,
            "overall_score": round(overall_score2, 1),
            "evaluation": _get_sancai_wuge_evaluation(overall_score2)
        },
        "better": name1 if overall_score1 >= overall_score2 else name2,
        "difference": abs(overall_score1 - overall_score2)
    }


def _get_sancai_wuge_evaluation(score: float) -> str:
    """获取三才五格评价

    Args:
        score: 得分

    Returns:
        评价文本
    """
    if score >= 85:
        return "三才五格极佳，大吉大利"
    elif score >= 75:
        return "三才五格很好，较为吉利"
    elif score >= 65:
        return "三才五格尚可，一般吉利"
    elif score >= 55:
        return "三才五格一般，有待改进"
    else:
        return "三才五格不理想"
