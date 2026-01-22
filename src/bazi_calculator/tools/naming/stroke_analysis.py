"""笔画分析工具

分析名字的康熙字典笔画和吉凶判断
"""

from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

from bazi_calculator.data.kangxi_strokes import KangxiStrokes


class StrokeLuckData:
    """81数理吉凶数据"""

    @staticmethod
    def get_stroke_luck_info(stroke_num: int) -> Dict[str, Any]:
        """获取指定笔画数的81数理吉凶信息

        Args:
            stroke_num: 笔画数（1-81）

        Returns:
            81数理吉凶信息字典
        """
        NUMERology_DATA = {
            1: {"luck": "吉", "score": 100, "description": "太极之数，万物开泰", "detail": "首领运，大吉之数，万象更新，神气饱满"},
            2: {"luck": "凶", "score": 40, "description": "一身孤节，分离破灭", "detail": "分离之数，一身孤节，难觅伴侣，困苦之象"},
            3: {"luck": "吉", "score": 100, "description": "身伴明月，福禄绵绵", "detail": "大吉之数，智勇双全，繁荣富贵，志大望重"},
            4: {"luck": "凶", "score": 30, "description": "破体败亡，灾害无穷", "detail": "破败之数，身受其害，万事挫折，困苦病弱"},
            5: {"luck": "吉", "score": 95, "description": "阴阳和合，精神安逸", "detail": "种竹成林，福禄长聚，大吉之数，六爻福至"},
            6: {"luck": "吉", "score": 95, "description": "安稳吉庆，百事如意", "detail": "六爻之数，发展变化，天赋美德，吉顺吉祥"},
            7: {"luck": "吉", "score": 90, "description": "刚毅果断，勇往直前", "detail": "七政之数，刚毅果断，勇往直前，贵人相助"},
            8: {"luck": "吉", "score": 100, "description": "意志刚健，勤勉发展", "detail": "八卦之数，意志刚健，勤勉发展，富于进取"},
            9: {"luck": "凶", "score": 50, "description": "浮华不定，多成多败", "detail": "凶数之极，浮华不定，多成多败，需防意外"},
            10: {"luck": "凶", "score": 50, "description": "万事终局，黯淡无光", "detail": "终局之数，万事终结，黯淡无光，守已成业"},
            11: {"luck": "吉", "score": 95, "description": "草木逢春，雨过天晴", "detail": "早苗逢雨，枯木逢春，恢复生机，大吉之数"},
            12: {"luck": "凶", "score": 40, "description": "掘井无泉，空无精神", "detail": "掘井无泉，空无精神，困苦病弱，需防意外"},
            13: {"luck": "吉", "score": 95, "description": "才艺多能，智谋奇略", "detail": "春日牡丹，才艺多能，智谋奇略，大吉之数"},
            14: {"luck": "凶", "score": 40, "description": "沦落天涯，失意烦闷", "detail": "沦落天涯，失意烦闷，家庭缘薄，多事多难"},
            15: {"luck": "吉", "score": 100, "description": "福寿双全，德望高大", "detail": "福寿双全，德望高大，大吉之数，富贵繁荣"},
            16: {"luck": "吉", "score": 100, "description": "厚重显贵，贵人得助", "detail": "厚重显贵，贵人得助，大吉之数，繁荣昌盛"},
            17: {"luck": "吉", "score": 95, "description": "突破万难，刚柔兼备", "detail": "突破万难，刚柔兼备，智达勇锐，大吉之数"},
            18: {"luck": "吉", "score": 100, "description": "功成名就，有志竟成", "detail": "镜花水月，功成名就，有志竟成，大吉之数"},
            19: {"luck": "凶", "score": 40, "description": "多难多愁，祸患缠身", "detail": "多难多愁，祸患缠身，破财之数，需防失败"},
            20: {"luck": "凶", "score": 30, "description": "灾难重重，一生劳苦", "detail": "破舟进海，灾难重重，一生劳苦，需防失败"},
            21: {"luck": "吉", "score": 95, "description": "光风霁月，万物成形", "detail": "光风霁月，万物成形，智达勇锐，大吉之数"},
            22: {"luck": "凶", "score": 50, "description": "秋草逢霜，怀才不遇", "detail": "秋草逢霜，怀才不遇，困苦病弱，需防意外"},
            23: {"luck": "吉", "score": 95, "description": "旭日东升，壮丽壮观", "detail": "旭日东升，壮丽壮观，大吉之数，富贵繁荣"},
            24: {"luck": "吉", "score": 90, "description": "家门余庆，金钱丰盈", "detail": "家门余庆，金钱丰盈，大吉之数，繁荣昌盛"},
            25: {"luck": "吉", "score": 100, "description": "资性英敏，有奇特才", "detail": "资性英敏，有奇特才，大吉之数，富贵繁荣"},
            26: {"luck": "吉", "score": 80, "description": "变怪奇异，艰难辛苦", "detail": "变怪奇异，艰难辛苦，波澜重叠，有勇无谋"},
            27: {"luck": "凶", "score": 50, "description": "增长诽谤，身受其害", "detail": "增长诽谤，身受其害，毁誉不明，易招诽谤"},
            28: {"luck": "吉", "score": 80, "description": "遭难之数，豪杰气概", "detail": "遭难之数，豪杰气概，有勇无谋，需防意外"},
            29: {"luck": "吉", "score": 80, "description": "智谋优秀，财力归集", "detail": "智谋优秀，财力归集，大吉之数，富贵繁荣"},
            30: {"luck": "吉", "score": 80, "description": "一成一败，一盛一衰", "detail": "一成一败，一盛一衰，吉凶难分，需防意外"},
            31: {"luck": "吉", "score": 100, "description": "智勇得志，心想事成", "detail": "智勇得志，心想事成，大吉之数，富贵繁荣"},
            32: {"luck": "吉", "score": 100, "description": "宝马金鞍，侥幸多望", "detail": "宝马金鞍，侥幸多望，大吉之数，繁荣昌盛"},
            33: {"luck": "吉", "score": 95, "description": "旭日升天，名闻天下", "detail": "旭日升天，名闻天下，大吉之数，富贵繁荣"},
            34: {"luck": "凶", "score": 50, "description": "破家之数，见识短小", "detail": "破家之数，见识短小，困难重重，需防失败"},
            35: {"luck": "吉", "score": 95, "description": "温和平静，优雅发展", "detail": "温和平静，优雅发展，大吉之数，富贵繁荣"},
            36: {"luck": "吉", "score": 95, "description": "波澜重叠，英雄贵人", "detail": "波澜重叠，英雄贵人，大吉之数，富贵繁荣"},
            37: {"luck": "吉", "score": 95, "description": "权威显达，吉人天相", "detail": "权威显达，吉人天相，大吉之数，富贵繁荣"},
            38: {"luck": "吉", "score": 95, "description": "磨铁成针，意志薄弱", "detail": "磨铁成针，意志薄弱，大吉之数，富贵繁荣"},
            39: {"luck": "凶", "score": 50, "description": "富贵荣华，变化无穷", "detail": "富贵荣华，变化无穷，吉凶难分，需防意外"},
            40: {"luck": "凶", "score": 50, "description": "退安保吉，谨慎从事", "detail": "退安保吉，谨慎从事，困难重重，需防失败"},
            41: {"luck": "吉", "score": 95, "description": "德望高大，忠孝俱全", "detail": "德望高大，忠孝俱全，大吉之数，富贵繁荣"},
            42: {"luck": "凶", "score": 50, "description": "博艺多才，虽吉还凶", "detail": "博艺多才，虽吉还凶，吉凶难分，需防意外"},
            43: {"luck": "凶", "score": 30, "description": "散财破产，外祥内苦", "detail": "散财破产，外祥内苦，困难重重，需防失败"},
            44: {"luck": "凶", "score": 30, "description": "须眉难展，力量有限", "detail": "须眉难展，力量有限，困难重重，需防失败"},
            45: {"luck": "吉", "score": 95, "description": "新生泰和，顺风扬帆", "detail": "新生泰和，顺风扬帆，大吉之数，富贵繁荣"},
            46: {"luck": "凶", "score": 50, "description": "载宝沉舟，浪里淘金", "detail": "载宝沉舟，浪里淘金，困难重重，需防失败"},
            47: {"luck": "吉", "score": 90, "description": "开花之象，祯祥吉庆", "detail": "开花之象，祯祥吉庆，大吉之数，富贵繁荣"},
            48: {"luck": "吉", "score": 90, "description": "青松立鹤，智谋兼备", "detail": "青松立鹤，智谋兼备，大吉之数，富贵繁荣"},
            49: {"luck": "凶", "score": 40, "description": "吉凶难分，多争多愁", "detail": "吉凶难分，多争多愁，困难重重，需防失败"},
            50: {"luck": "凶", "score": 30, "description": "小舟入海，成败难定", "detail": "小舟入海，成败难定，困难重重，需防失败"},
            51: {"luck": "吉", "score": 95, "description": "沉浮不定，盛衰无常", "detail": "沉浮不定，盛衰无常，吉凶难分，需防意外"},
            52: {"luck": "吉", "score": 95, "description": "草木逢春，雨过天晴", "detail": "草木逢春，雨过天晴，大吉之数，富贵繁荣"},
            53: {"luck": "吉", "score": 90, "description": "外表掩饰，内含忧愁", "detail": "外表掩饰，内含忧愁，吉凶难分，需防意外"},
            54: {"luck": "凶", "score": 40, "description": "石上载花，费力徒劳", "detail": "石上载花，费力徒劳，困难重重，需防失败"},
            55: {"luck": "吉", "score": 80, "description": "外美内苦，吉中藏凶", "detail": "外美内苦，吉中藏凶，吉凶难分，需防意外"},
            56: {"luck": "凶", "score": 50, "description": "浪里行舟，历尽艰辛", "detail": "浪里行舟，历尽艰辛，困难重重，需防失败"},
            57: {"luck": "吉", "score": 80, "description": "日照春松，壮志凌云", "detail": "日照春松，壮志凌云，大吉之数，富贵繁荣"},
            58: {"luck": "凶", "score": 50, "description": "晚苦早荣，先甘后苦", "detail": "晚苦早荣，先甘后苦，吉凶难分，需防意外"},
            59: {"luck": "凶", "score": 40, "description": "寒蝉悲风，意志衰退", "detail": "寒蝉悲风，意志衰退，困难重重，需防失败"},
            60: {"luck": "吉", "score": 80, "description": "无谋争斗，谋事难成", "detail": "无谋争斗，谋事难成，吉凶难分，需防意外"},
            61: {"luck": "吉", "score": 95, "description": "牡丹芙蓉，名利双收", "detail": "牡丹芙蓉，名利双收，大吉之数，富贵繁荣"},
            62: {"luck": "凶", "score": 60, "description": "败坏运气，空虚沉沦", "detail": "败坏运气，空虚沉沦，困难重重，需防失败"},
            63: {"luck": "吉", "score": 90, "description": "富贵荣华，变化无穷", "detail": "富贵荣华，变化无穷，大吉之数，富贵繁荣"},
            64: {"luck": "凶", "score": 60, "description": "骨肉分离，孤独悲愁", "detail": "骨肉分离，孤独悲愁，困难重重，需防失败"},
            65: {"luck": "吉", "score": 80, "description": "巨流归海，富贵荣华", "detail": "巨流归海，富贵荣华，大吉之数，富贵繁荣"},
            66: {"luck": "凶", "score": 50, "description": "岩头步马，灾害重生", "detail": "岩头步马，灾害重生，困难重重，需防失败"},
            67: {"luck": "吉", "score": 90, "description": "通达顺遂，贵人相助", "detail": "通达顺遂，贵人相助，大吉之数，富贵繁荣"},
            68: {"luck": "凶", "score": 60, "description": "思虑周全，计划如意", "detail": "思虑周全，计划如意，吉凶难分，需防意外"},
            69: {"luck": "凶", "score": 60, "description": "非业非力，精神不定", "detail": "非业非力，精神不定，困难重重，需防失败"},
            70: {"luck": "凶", "score": 60, "description": "残菊逢霜，沉沦病弱", "detail": "残菊逢霜，沉沦病弱，困难重重，需防失败"},
            71: {"luck": "吉", "score": 80, "description": "石上金花，半凶半吉", "detail": "石上金花，半凶半吉，吉凶难分，需防意外"},
            72: {"luck": "凶", "score": 60, "description": "劳苦愁闷，内心郁结", "detail": "劳苦愁闷，内心郁结，困难重重，需防失败"},
            73: {"luck": "吉", "score": 90, "description": "志高力微，努力奋斗", "detail": "志高力微，努力奋斗，大吉之数，富贵繁荣"},
            74: {"luck": "凶", "score": 50, "description": "困苦奔波，沉沦疾病", "detail": "困苦奔波，沉沦疾病，困难重重，需防失败"},
            75: {"luck": "吉", "score": 80, "description": "退守保吉，虽有作为", "detail": "退守保吉，虽有作为，吉凶难分，需防意外"},
            76: {"luck": "凶", "score": 60, "description": "倾覆离散，劳而无功", "detail": "倾覆离散，劳而无功，困难重重，需防失败"},
            77: {"luck": "吉", "score": 80, "description": "家庭有悦，半凶半吉", "detail": "家庭有悦，半凶半吉，吉凶难分，需防意外"},
            78: {"luck": "凶", "score": 60, "description": "晚景凄凉，光芒消失", "detail": "晚景凄凉，光芒消失，困难重重，需防失败"},
            79: {"luck": "凶", "score": 50, "description": "云头望月，身疲力尽", "detail": "云头望月，身疲力尽，困难重重，需防失败"},
            80: {"luck": "凶", "score": 60, "description": "凶星入度，灾难重重", "detail": "凶星入度，灾难重重，困难重重，需防失败"},
            81: {"luck": "吉", "score": 100, "description": "万物回春，名利双收", "detail": "万物回春，名利双收，大吉之数，富贵繁荣"}
        }

        return NUMERology_DATA.get(stroke_num, {
            "luck": "平",
            "score": 70,
            "description": "笔画数超出81数理范围，无法判断",
            "detail": "笔画数超出81数理范围"
        })


def _analyze_name_strokes_internal(name: str) -> Dict[str, Any]:
    """分析名字的康熙字典笔画（内部函数，不带装饰器）

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
def analyze_name_strokes(name: str) -> Dict[str, Any]:
    """分析名字的康熙字典笔画

    Args:
        name: 名字

    Returns:
        笔画分析结果
    """
    return _analyze_name_strokes_internal(name)


@tool
def check_strokes_luck(name: str) -> Dict[str, Any]:
    """检查名字的笔画吉凶

    Args:
        name: 名字

    Returns:
        笔画吉凶分析结果
    """
    analysis = _analyze_name_strokes_internal(name)
    total_strokes = analysis["total_strokes"]

    # 获取总笔画的吉凶信息
    total_luck_info = StrokeLuckData.get_stroke_luck_info(total_strokes)

    # 获取单字的吉凶信息
    char_luck_info = {}
    for char in name:
        strokes = analysis["strokes_dict"].get(char)
        if strokes:
            char_luck_info[char] = StrokeLuckData.get_stroke_luck_info(strokes)

    # 计算综合吉凶评分
    luck_score = 0
    luck_evaluations = []

    # 总笔画吉凶（权重40%）
    if total_luck_info["luck"] == "吉":
        luck_score += 40
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（吉）")
    elif total_luck_info["luck"] == "凶":
        luck_score += 10
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（凶）")
    else:
        luck_score += 25
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（平）")

    # 单字吉凶（权重60%，平均分配）
    if char_luck_info:
        char_scores = []
        for char, luck_info in char_luck_info.items():
            if luck_info["luck"] == "吉":
                char_score = 60 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（吉）")
            elif luck_info["luck"] == "凶":
                char_score = 15 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（凶）")
            else:
                char_score = 37.5 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（平）")
            char_scores.append(char_score)
        luck_score += sum(char_scores)

    return {
        "name": name,
        "total_strokes": total_strokes,
        "total_luck": total_luck_info,
        "char_luck": char_luck_info,
        "luck_score": min(luck_score, 100),
        "luck_evaluations": luck_evaluations,
        "overall_luck": "吉" if luck_score >= 70 else "凶" if luck_score <= 40 else "平",
        "luck_description": _get_luck_description(luck_score)
    }


@tool
def check_strokes_harmony(name: str) -> Dict[str, Any]:
    """检查名字的笔画和谐度

    Args:
        name: 名字

    Returns:
        和谐度分析结果
    """
    analysis = _analyze_name_strokes_internal(name)
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
def check_strokes_comprehensive(name: str) -> Dict[str, Any]:
    """综合检查名字的笔画（包含和谐度和吉凶）

    Args:
        name: 名字

    Returns:
        综合笔画分析结果
    """
    # 获取和谐度分析（使用内部函数）
    harmony_score = _get_harmony_score_internal(name)

    # 获取吉凶分析（使用内部函数）
    luck_score, luck_evaluations, overall_luck, luck_description = _get_luck_score_internal(name)

    # 综合评分（和谐度50% + 吉凶50%）
    comprehensive_score = (harmony_score + luck_score) / 2

    # 获取分析结果
    analysis = _analyze_name_strokes_internal(name)

    # 获取和谐度评价
    harmony_evaluations, harmony_description = _get_harmony_evaluations_internal(name, analysis)

    # 综合评价
    evaluations = harmony_evaluations + luck_evaluations

    return {
        "name": name,
        "harmony": {
            "score": harmony_score,
            "evaluations": harmony_evaluations,
            "description": harmony_description,
            "total_strokes": analysis["total_strokes"],
            "average_strokes": analysis["average_strokes"]
        },
        "luck": {
            "luck_score": luck_score,
            "luck_evaluations": luck_evaluations,
            "overall_luck": overall_luck,
            "luck_description": luck_description,
            "total_strokes": analysis["total_strokes"]
        },
        "comprehensive_score": round(comprehensive_score, 1),
        "evaluations": evaluations,
        "overall_description": _get_comprehensive_description(comprehensive_score)
    }


def _get_harmony_score_internal(name: str) -> int:
    """获取和谐度分数（内部函数）"""
    analysis = _analyze_name_strokes_internal(name)
    total_strokes = analysis["total_strokes"]
    average_strokes = analysis["average_strokes"]
    strokes_list = analysis["strokes_list"]

    score = 0

    if 10 <= total_strokes <= 25:
        score += 40
    elif 5 <= total_strokes <= 30:
        score += 30
    else:
        score += 10

    if 5 <= average_strokes <= 15:
        score += 30
    elif 3 <= average_strokes <= 18:
        score += 20
    else:
        score += 10

    if strokes_list:
        stroke_range = max(strokes_list) - min(strokes_list)
        if stroke_range <= 5:
            score += 20
        elif stroke_range <= 10:
            score += 15
        else:
            score += 10

    if all(s <= 20 for s in strokes_list):
        score += 10

    return min(score, 100)


def _get_harmony_evaluations_internal(name: str, analysis: Dict[str, Any]) -> tuple:
    """获取和谐度评价（内部函数）"""
    total_strokes = analysis["total_strokes"]
    average_strokes = analysis["average_strokes"]
    strokes_list = analysis["strokes_list"]

    evaluations = []

    if 10 <= total_strokes <= 25:
        evaluations.append("总笔画适中")
    elif 5 <= total_strokes <= 30:
        evaluations.append("总笔画尚可")
    else:
        evaluations.append("总笔画不理想")

    if 5 <= average_strokes <= 15:
        evaluations.append("平均笔画适中")
    elif 3 <= average_strokes <= 18:
        evaluations.append("平均笔画尚可")
    else:
        evaluations.append("平均笔画不理想")

    if strokes_list:
        stroke_range = max(strokes_list) - min(strokes_list)
        if stroke_range <= 5:
            evaluations.append("笔画分布均匀")
        elif stroke_range <= 10:
            evaluations.append("笔画分布较为均匀")
        else:
            evaluations.append("笔画分布不均匀")

    if all(s <= 20 for s in strokes_list):
        evaluations.append("无过多笔画字")

    score = _get_harmony_score_internal(name)
    description = _get_strokes_description(score)

    return evaluations, description


def _get_luck_score_internal(name: str) -> tuple:
    """获取吉凶分数（内部函数）"""
    analysis = _analyze_name_strokes_internal(name)
    total_strokes = analysis["total_strokes"]

    total_luck_info = StrokeLuckData.get_stroke_luck_info(total_strokes)

    char_luck_info = {}
    for char in name:
        strokes = analysis["strokes_dict"].get(char)
        if strokes:
            char_luck_info[char] = StrokeLuckData.get_stroke_luck_info(strokes)

    luck_score = 0
    luck_evaluations = []

    if total_luck_info["luck"] == "吉":
        luck_score += 40
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（吉）")
    elif total_luck_info["luck"] == "凶":
        luck_score += 10
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（凶）")
    else:
        luck_score += 25
        luck_evaluations.append(f"总笔画{total_strokes}画：{total_luck_info['description']}（平）")

    if char_luck_info:
        char_scores = []
        for char, luck_info in char_luck_info.items():
            if luck_info["luck"] == "吉":
                char_score = 60 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（吉）")
            elif luck_info["luck"] == "凶":
                char_score = 15 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（凶）")
            else:
                char_score = 37.5 / len(char_luck_info)
                luck_evaluations.append(f"{char}字{analysis['strokes_dict'][char]}画：{luck_info['description']}（平）")
            char_scores.append(char_score)
        luck_score += sum(char_scores)

    overall_luck = "吉" if luck_score >= 70 else "凶" if luck_score <= 40 else "平"
    luck_description = _get_luck_description(luck_score)

    return min(luck_score, 100), luck_evaluations, overall_luck, luck_description


@tool
def compare_name_strokes(name1: str, name2: str) -> Dict[str, Any]:
    """比较两个名字的笔画

    Args:
        name1: 名字1
        name2: 名字2

    Returns:
        比较结果
    """
    analysis1 = _analyze_name_strokes_internal(name1)
    analysis2 = _analyze_name_strokes_internal(name2)

    harmony_evaluations1, harmony_description1 = _get_harmony_evaluations_internal(name1, analysis1)
    harmony_evaluations2, harmony_description2 = _get_harmony_evaluations_internal(name2, analysis2)

    harmony_score1 = _get_harmony_score_internal(name1)
    harmony_score2 = _get_harmony_score_internal(name2)

    return {
        "name1": {
            "name": name1,
            "total_strokes": analysis1["total_strokes"],
            "average_strokes": analysis1["average_strokes"],
            "score": harmony_score1,
            "description": harmony_description1
        },
        "name2": {
            "name": name2,
            "total_strokes": analysis2["total_strokes"],
            "average_strokes": analysis2["average_strokes"],
            "score": harmony_score2,
            "description": harmony_description2
        },
        "better": name1 if harmony_score1 >= harmony_score2 else name2,
        "difference": abs(harmony_score1 - harmony_score2)
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
            analysis = _analyze_name_strokes_internal(name)
            harmony_score = _get_harmony_score_internal(name)
            _, harmony_description = _get_harmony_evaluations_internal(name, analysis)

            if min_total_strokes <= analysis["total_strokes"] <= max_total_strokes:
                suggestions.append({
                    "name": name,
                    "total_strokes": analysis["total_strokes"],
                    "score": harmony_score,
                    "description": harmony_description
                })

    # 按分数排序
    suggestions.sort(key=lambda x: x["score"], reverse=True)

    return suggestions[:20]


@tool
def format_strokes_luck_analysis(analysis: Dict[str, Any]) -> str:
    """格式化81数理吉凶分析为文本

    Args:
        analysis: 笔画吉凶分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    total_strokes = analysis.get("total_strokes", 0)
    total_luck = analysis.get("total_luck", {})
    char_luck = analysis.get("char_luck", {})
    luck_score = analysis.get("luck_score", 0)
    luck_evaluations = analysis.get("luck_evaluations", [])
    overall_luck = analysis.get("overall_luck", "")
    luck_description = analysis.get("luck_description", "")
    strokes_dict = analysis.get("strokes_dict", {})

    output = []
    output.append("=" * 50)
    output.append("81数理吉凶分析")
    output.append("=" * 50)
    output.append(f"\n姓名：{name}")

    # 总笔画81数理吉凶
    output.append(f"\n【总笔画81数理】")
    output.append(f"总笔画：{total_strokes}画")
    output.append(f"81数理：{total_strokes}数")
    output.append(f"吉凶：{total_luck.get('luck', '')}")
    output.append(f"评分：{total_luck.get('score', 0)}/100")
    output.append(f"含义：{total_luck.get('description', '')}")
    output.append(f"详细说明：{total_luck.get('detail', '')}")

    # 单字81数理吉凶
    if char_luck:
        output.append(f"\n【单字81数理】")
        for char, luck_info in char_luck.items():
            char_strokes = strokes_dict.get(char, '')
            output.append(f"  {char}字{char_strokes}画：")
            output.append(f"    81数理：{luck_info.get('luck', '')}")
            output.append(f"    含义：{luck_info.get('description', '')}")

    # 评价
    output.append(f"\n【综合评分】")
    output.append(f"81数理综合得分：{luck_score}/100")
    output.append(f"整体吉凶：{overall_luck}")
    output.append(f"综合评价：{luck_description}")
    output.append(f"\n【详细评价】")
    for evaluation in luck_evaluations:
        output.append(f"  - {evaluation}")

    output.append(f"\n总结：{luck_description}")
    output.append("\n" + "=" * 50)

    return "\n".join(output)


@tool
def format_strokes_comprehensive_analysis(analysis: Dict[str, Any]) -> str:
    """格式化笔画综合分析为文本

    Args:
        analysis: 笔画综合分析结果

    Returns:
        格式化后的文本
    """
    name = analysis.get("name", "")
    harmony = analysis.get("harmony", {})
    luck = analysis.get("luck", {})
    comprehensive_score = analysis.get("comprehensive_score", 0)
    evaluations = analysis.get("evaluations", [])
    overall_description = analysis.get("overall_description", "")

    output = []
    output.append("=" * 50)
    output.append("笔画综合分析")
    output.append("=" * 50)
    output.append(f"\n名字：{name}")

    # 和谐度
    output.append(f"\n【和谐度】")
    output.append(f"总笔画：{harmony.get('total_strokes', 0)}画")
    output.append(f"平均笔画：{harmony.get('average_strokes', 0)}画")
    output.append(f"和谐得分：{harmony.get('score', 0)}/100")
    output.append(f"和谐评价：{harmony.get('description', '')}")

    # 吉凶
    output.append(f"\n【吉凶】")
    output.append(f"总笔画吉凶：{luck.get('total_luck', {}).get('luck', '')}")
    output.append(f"吉凶得分：{luck.get('luck_score', 0)}/100")
    output.append(f"整体吉凶：{luck.get('overall_luck', '')}")
    output.append(f"吉凶评价：{luck.get('luck_description', '')}")

    # 综合评价
    output.append(f"\n【综合评价】")
    output.append(f"综合得分：{comprehensive_score}/100")
    output.append(f"\n详细评价：")
    for evaluation in evaluations:
        output.append(f"  - {evaluation}")

    output.append(f"\n总结：{overall_description}")
    output.append("\n" + "=" * 50)

    return "\n".join(output)


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
        analysis = _analyze_name_strokes_internal(name)
        harmony_evaluations, harmony_description = _get_harmony_evaluations_internal(name, analysis)
        harmony_score = _get_harmony_score_internal(name)
        results.append({
            "name": name,
            "total_strokes": analysis["total_strokes"],
            "average_strokes": analysis["average_strokes"],
            "score": harmony_score,
            "description": harmony_description
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


def _get_luck_description(score: int) -> str:
    """获取吉凶描述

    Args:
        score: 得分

    Returns:
        描述文本
    """
    if score >= 80:
        return "笔画数理大吉，万事如意"
    elif score >= 60:
        return "笔画数理较好，吉多凶少"
    elif score >= 40:
        return "笔画数理一般，吉凶参半"
    else:
        return "笔画数理不理想，凶多吉少"


def _get_comprehensive_description(score: float) -> str:
    """获取综合描述

    Args:
        score: 得分

    Returns:
        描述文本
    """
    if score >= 85:
        return "笔画综合评价极佳，吉凶和谐，搭配完美"
    elif score >= 75:
        return "笔画综合评价很好，较为吉利"
    elif score >= 65:
        return "笔画综合评价尚可，一般吉利"
    elif score >= 55:
        return "笔画综合评价一般，有待改进"
    else:
        return "笔画综合评价不理想，需要调整"
