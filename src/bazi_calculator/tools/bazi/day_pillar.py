"""日柱计算工具"""

from datetime import datetime

from langchain_core.tools import tool

from bazi_calculator.core.calendar import BaziCalendar


@tool
def calculate_day_pillar(birth_date: datetime) -> dict:
    """计算日柱（日干和日支）

    以1949年10月1日（甲子日）为基准推算

    Args:
        birth_date: 出生日期

    Returns:
        日柱信息字典
    """
    day_gan, day_zhi, day_gan_wuxing, day_zhi_wuxing = BaziCalendar.get_day_pillar(birth_date)

    return {
        "gan": day_gan,
        "zhi": day_zhi,
        "gan_wuxing": day_gan_wuxing,
        "zhi_wuxing": day_zhi_wuxing,
        "full": day_gan + day_zhi,
        "day_master": day_gan
    }
