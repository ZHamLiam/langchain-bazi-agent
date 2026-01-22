"""五行分析工具"""

from typing import Dict, Any

from langchain_core.tools import tool

from bazi_calculator.core.wuxing import WuxingAnalyzer


@tool
def analyze_wuxing(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """分析八字五行

    包括：
    - 统计四柱五行数量
    - 分析日主强弱
    - 确定用神、喜神、忌神
    - 识别缺失和过多的五行

    Args:
        bazi: 八字信息字典，包含四柱信息

    Returns:
        五行分析结果字典
    """
    return WuxingAnalyzer.analyze_comprehensive(bazi)


@tool
def count_wuxing(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """统计八字中的五行数量

    Args:
        bazi: 八字信息字典

    Returns:
        五行计数字典
    """
    return WuxingAnalyzer.count_wuxing_in_bazi(bazi)


@tool
def analyze_day_master_strength(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """分析日主强弱

    Args:
        bazi: 八字信息字典

    Returns:
        日主强弱分析结果
    """
    strength, scores = WuxingAnalyzer.analyze_day_master_strength(bazi)

    return {
        "strength": strength,
        "scores": scores,
        "description": _get_strength_description(strength)
    }


@tool
def determine_yong_shen(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """推算用神、喜神、忌神

    Args:
        bazi: 八字信息字典

    Returns:
        用神信息字典
    """
    return WuxingAnalyzer.determine_yong_shen(bazi)


def _get_strength_description(strength: str) -> str:
    """获取强弱描述

    Args:
        strength: 强弱程度

    Returns:
        描述文本
    """
    descriptions = {
        "强": "日主较强，得令、得势，喜克泄耗，忌生扶",
        "中和": "日主中和，平衡协调，可用月支或季节定用神",
        "弱": "日主较弱，失令、失势，喜生扶，忌克泄耗"
    }
    return descriptions.get(strength, "未知")
