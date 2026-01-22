"""八字日历计算模块

此模块提供年、月、日、时四柱的计算功能。
"""

from datetime import datetime, timedelta
from typing import Tuple
from bazi_calculator.core.ganzhi import GanzhiCalculator
from bazi_calculator.core.jieqi import JieqiCalculator


class BaziCalendar:
    """八字日历计算器
    
    提供年、月、日、时四柱的计算功能。
    """
    
    # 基准日期：1949年10月1日（中华人民共和国成立日）
    # 这一天是甲子日（干支日）
    BASE_DATE = datetime(1949, 10, 1)
    
    # 五虎遁月干计算表（年份天干到月份天干的映射）
    # 年干: 甲(0), 乙(1), 丙(2), 丁(3), 戊(4), 己(5), 庚(6), 辛(7), 壬(8), 癸(9)
    # 月干从寅月（立春）开始计算
    WUHU_DUN_TABLE = [
        ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],  # 甲年起
        ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],  # 乙年起
        ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],  # 丙年起
        ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],  # 丁年起
        ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],  # 戊年起
        ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],  # 己年起
        ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],  # 庚年起
        ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],  # 辛年起
        ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],  # 壬年起
        ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],  # 癸年起
    ]
    
    # 五鼠遁时干计算表（日干到时干的映射）
    # 日干: 甲(0), 乙(1), 丙(2), 丁(3), 戊(4), 己(5), 庚(6), 辛(7), 壬(8), 癸(9)
    # 时干从子时开始计算
    WUSHU_DUN_TABLE = [
        ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],  # 甲日
        ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],  # 乙日
        ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],  # 丙日
        ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],  # 丁日
        ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],  # 戊日
        ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],  # 己日
        ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],  # 庚日
        ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],  # 辛日
        ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],  # 壬日
        ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],  # 癸日
    ]
    
    @staticmethod
    def get_year_pillar(birth_date: datetime) -> Tuple[str, str, str, str]:
        """计算年柱（年干和年支）
        
        年柱以立春为界：立春之前为上一年，立春之后为新的一年
        
        Args:
            birth_date: 出生日期
            
        Returns:
            (年干, 年支, 年干五行, 年支五行) 元组
        """
        # 判断是否在立春之前
        if JieqiCalculator.is_before_lichun(birth_date):
            year = birth_date.year - 1
        else:
            year = birth_date.year
        
        # 计算年干（从公元4年甲子年起算）
        year_gan_index = (year - 4) % 10
        year_gan = GanzhiCalculator.get_tiangan_by_index(year_gan_index)
        
        # 计算年支（从公元4年甲子年起算）
        year_zhi_index = (year - 4) % 12
        year_zhi = GanzhiCalculator.get_dizhi_by_index(year_zhi_index)
        
        # 获取五行
        year_gan_wuxing = GanzhiCalculator.get_tiangan_wuxing(year_gan)
        year_zhi_wuxing = GanzhiCalculator.get_dizhi_wuxing(year_zhi)
        
        return year_gan, year_zhi, year_gan_wuxing, year_zhi_wuxing
    
    @staticmethod
    def get_month_pillar(birth_date: datetime, year_gan: str) -> Tuple[str, str, str, str, str]:
        """计算月柱（月干和月支）
        
        月柱以节气为界，使用五虎遁法计算月干
        
        Args:
            birth_date: 出生日期
            year_gan: 年干
            
        Returns:
            (月干, 月支, 月干五行, 月支五行, 节气名称) 元组
        """
        year = birth_date.year
        
        # 找到当前节气
        current_jieqi, jieqi_time, _ = JieqiCalculator.get_current_jieqi(birth_date)
        
        # 节气名称到月份的映射（从寅月开始）
        jieqi_to_month = {
            "立春": ("寅", "一月"),
            "雨水": ("寅", "一月"),
            "惊蛰": ("卯", "二月"),
            "春分": ("卯", "二月"),
            "清明": ("辰", "三月"),
            "谷雨": ("辰", "三月"),
            "立夏": ("巳", "四月"),
            "小满": ("巳", "四月"),
            "芒种": ("午", "五月"),
            "夏至": ("午", "五月"),
            "小暑": ("未", "六月"),
            "大暑": ("未", "六月"),
            "立秋": ("申", "七月"),
            "处暑": ("申", "七月"),
            "白露": ("酉", "八月"),
            "秋分": ("酉", "八月"),
            "寒露": ("戌", "九月"),
            "霜降": ("戌", "九月"),
            "立冬": ("亥", "十月"),
            "小雪": ("亥", "十月"),
            "大雪": ("子", "十一月"),
            "冬至": ("子", "十一月"),
            "小寒": ("丑", "十二月"),
            "大寒": ("丑", "十二月"),
        }
        
        month_zhi, month_name = jieqi_to_month.get(current_jieqi, ("寅", "正月"))
        
        # 使用五虎遁法计算月干
        year_gan_index = GanzhiCalculator.TIANGAN.index(year_gan)
        month_index = GanzhiCalculator.DIZHI.index(month_zhi)
        
        # 五虎遁法月份顺序（从寅月开始）：寅、卯、辰、巳、午、未、申、酉、戌、亥、子、丑
        month_order = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        month_index_in_order = month_order.index(month_zhi)
        
        # 五虎遁表：年干对应行，月份对应列（从寅月开始）
        # 寅月是第0列
        month_gan_index_in_year = month_index_in_order % 10
        month_gan = BaziCalendar.WUHU_DUN_TABLE[year_gan_index][month_gan_index_in_year]
        
        # 获取五行
        month_gan_wuxing = GanzhiCalculator.get_tiangan_wuxing(month_gan)
        month_zhi_wuxing = GanzhiCalculator.get_dizhi_wuxing(month_zhi)
        
        return month_gan, month_zhi, month_gan_wuxing, month_zhi_wuxing, current_jieqi
    
    @staticmethod
    def get_day_pillar(birth_date: datetime) -> Tuple[str, str, str, str]:
        """计算日柱（日干和日支）
        
        以1949年10月1日（甲子日）为基准推算
        
        Args:
            birth_date: 出生日期
            
        Returns:
            (日干, 日支, 日干五行, 日支五行) 元组
        """
        # 计算与基准日期的天数差
        delta = birth_date.date() - BaziCalendar.BASE_DATE.date()
        days_diff = delta.days
        
        # 计算日干索引
        day_gan_index = days_diff % 10
        day_gan = GanzhiCalculator.get_tiangan_by_index(day_gan_index)
        
        # 计算日支索引
        day_zhi_index = days_diff % 12
        day_zhi = GanzhiCalculator.get_dizhi_by_index(day_zhi_index)
        
        # 获取五行
        day_gan_wuxing = GanzhiCalculator.get_tiangan_wuxing(day_gan)
        day_zhi_wuxing = GanzhiCalculator.get_dizhi_wuxing(day_zhi)
        
        return day_gan, day_zhi, day_gan_wuxing, day_zhi_wuxing
    
    @staticmethod
    def get_hour_pillar(birth_time: datetime, day_gan: str) -> Tuple[str, str, str, str]:
        """计算时柱（时干和时支）
        
        使用五鼠遁法计算时干，根据出生时间确定时支
        
        Args:
            birth_time: 出生时间
            day_gan: 日干
            
        Returns:
            (时干, 时支, 时干五行, 时支五行) 元组
        """
        # 根据出生时间确定时支
        hour = birth_time.hour
        
        # 时辰划分（按照八字标准）
        # 亥时：21:00-23:00
        # 子时：23:00-01:00（跨日）
        if hour >= 21 and hour < 23:
            hour_zhi = "亥"
        elif hour >= 23 or hour < 1:
            hour_zhi = "子"
        elif hour >= 1 and hour < 3:
            hour_zhi = "丑"
        elif hour >= 3 and hour < 5:
            hour_zhi = "寅"
        elif hour >= 5 and hour < 7:
            hour_zhi = "卯"
        elif hour >= 7 and hour < 9:
            hour_zhi = "辰"
        elif hour >= 9 and hour < 11:
            hour_zhi = "巳"
        elif hour >= 11 and hour < 13:
            hour_zhi = "午"
        elif hour >= 13 and hour < 15:
            hour_zhi = "未"
        elif hour >= 15 and hour < 17:
            hour_zhi = "申"
        elif hour >= 17 and hour < 19:
            hour_zhi = "酉"
        elif hour >= 19 and hour < 21:
            hour_zhi = "戌"
        else:
            hour_zhi = "亥"
        
        # 使用五鼠遁法计算时干
        day_gan_index = GanzhiCalculator.TIANGAN.index(day_gan)
        hour_zhi_index = GanzhiCalculator.DIZHI.index(hour_zhi)
        
        # 五鼠遁表：日干对应行，时支对应列
        hour_gan = BaziCalendar.WUSHU_DUN_TABLE[day_gan_index][hour_zhi_index]
        
        # 获取五行
        hour_gan_wuxing = GanzhiCalculator.get_tiangan_wuxing(hour_gan)
        hour_zhi_wuxing = GanzhiCalculator.get_dizhi_wuxing(hour_zhi)
        
        return hour_gan, hour_zhi, hour_gan_wuxing, hour_zhi_wuxing
    
    @staticmethod
    def get_all_pillars(birth_date: datetime) -> dict:
        """计算完整的八字四柱
        
        Args:
            birth_date: 出生日期时间
            
        Returns:
            包含四柱完整信息的字典
        """
        # 计算年柱
        year_gan, year_zhi, year_gan_wuxing, year_zhi_wuxing = BaziCalendar.get_year_pillar(birth_date)
        
        # 计算月柱
        month_gan, month_zhi, month_gan_wuxing, month_zhi_wuxing, jieqi = BaziCalendar.get_month_pillar(birth_date, year_gan)
        
        # 计算日柱
        day_gan, day_zhi, day_gan_wuxing, day_zhi_wuxing = BaziCalendar.get_day_pillar(birth_date)
        
        # 计算时柱
        hour_gan, hour_zhi, hour_gan_wuxing, hour_zhi_wuxing = BaziCalendar.get_hour_pillar(birth_date, day_gan)
        
        return {
            "year": {
                "gan": year_gan,
                "zhi": year_zhi,
                "gan_wuxing": year_gan_wuxing,
                "zhi_wuxing": year_zhi_wuxing,
                "full": year_gan + year_zhi
            },
            "month": {
                "gan": month_gan,
                "zhi": month_zhi,
                "gan_wuxing": month_gan_wuxing,
                "zhi_wuxing": month_zhi_wuxing,
                "full": month_gan + month_zhi,
                "jieqi": jieqi
            },
            "day": {
                "gan": day_gan,
                "zhi": day_zhi,
                "gan_wuxing": day_gan_wuxing,
                "zhi_wuxing": day_zhi_wuxing,
                "full": day_gan + day_zhi,
                "day_master": day_gan  # 日主
            },
            "hour": {
                "gan": hour_gan,
                "zhi": hour_zhi,
                "gan_wuxing": hour_gan_wuxing,
                "zhi_wuxing": hour_zhi_wuxing,
                "full": hour_gan + hour_zhi
            },
            "birth_info": {
                "date": birth_date,
                "year": birth_date.year,
                "month": birth_date.month,
                "day": birth_date.day,
                "hour": birth_date.hour,
                "minute": birth_date.minute,
                "second": birth_date.second
            }
        }
