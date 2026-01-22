"""时柱计算工具"""

from datetime import datetime

from langchain_core.tools import tool

from bazi_calculator.core.calendar import BaziCalendar


@tool
def calculate_hour_pillar(birth_time: datetime, day_gan: str) -> dict:
    """计算时柱（时干和时支）

    使用五鼠遁法计算时干，根据出生时间确定时支

    Args:
        birth_time: 出生时间
        day_gan: 日干

    Returns:
        时柱信息字典
    """
    hour_gan, hour_zhi, hour_gan_wuxing, hour_zhi_wuxing = BaziCalendar.get_hour_pillar(
        birth_time, day_gan
    )

    return {
        "gan": hour_gan,
        "zhi": hour_zhi,
        "gan_wuxing": hour_gan_wuxing,
        "zhi_wuxing": hour_zhi_wuxing,
        "full": hour_gan + hour_zhi
    }
