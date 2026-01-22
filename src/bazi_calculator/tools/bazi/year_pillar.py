"""年柱计算工具"""

from datetime import datetime

from langchain_core.tools import tool

from bazi_calculator.core.calendar import BaziCalendar


@tool
def calculate_year_pillar(birth_date: datetime) -> dict:
    """计算年柱（年干和年支）

    年柱以立春为界：立春之前为上一年，立春之后为新的一年

    Args:
        birth_date: 出生日期

    Returns:
        年柱信息字典
    """
    year_gan, year_zhi, year_gan_wuxing, year_zhi_wuxing = BaziCalendar.get_year_pillar(birth_date)

    return {
        "gan": year_gan,
        "zhi": year_zhi,
        "gan_wuxing": year_gan_wuxing,
        "zhi_wuxing": year_zhi_wuxing,
        "full": year_gan + year_zhi
    }
