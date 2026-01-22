"""月柱计算工具"""

from datetime import datetime

from langchain_core.tools import tool

from bazi_calculator.core.calendar import BaziCalendar


@tool
def calculate_month_pillar(birth_date: datetime, year_gan: str) -> dict:
    """计算月柱（月干和月支）

    月柱以节气为界，使用五虎遁法计算月干

    Args:
        birth_date: 出生日期
        year_gan: 年干

    Returns:
        月柱信息字典
    """
    month_gan, month_zhi, month_gan_wuxing, month_zhi_wuxing, jieqi = BaziCalendar.get_month_pillar(
        birth_date, year_gan
    )

    return {
        "gan": month_gan,
        "zhi": month_zhi,
        "gan_wuxing": month_gan_wuxing,
        "zhi_wuxing": month_zhi_wuxing,
        "full": month_gan + month_zhi,
        "jieqi": jieqi
    }
