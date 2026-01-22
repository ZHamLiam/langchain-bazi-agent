"""节气计算模块

此模块提供二十四节气的定义和计算功能。
基于Jean Meeus《Astronomical Algorithms》中的算法。
"""

from datetime import datetime, timedelta
from typing import Tuple
from math import radians, sin, cos, tan, atan, asin, acos, degrees, floor, pi


class JieqiCalculator:
    """节气计算器
    
    提供二十四节气的定义和时刻计算功能。
    """
    
    # 二十四节气名称
    JIEQI_NAMES = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]
    
    # 二十四节气对应的太阳黄经（角度）
    JIEQI_LONGITUDE = [
        315, 330, 345, 0, 15, 30,
        45, 60, 75, 90, 105, 120,
        135, 150, 165, 180, 195, 210,
        225, 240, 255, 270, 285, 300
    ]
    
    # 节气名称到索引的映射
    JIEQI_INDEX = {name: idx for idx, name in enumerate(JIEQI_NAMES)}
    
    @staticmethod
    def _get_julian_day(date: datetime) -> float:
        """获取儒略日
        
        Args:
            date: 日期时间
            
        Returns:
            儒略日
        """
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second
        
        if month <= 2:
            year -= 1
            month += 12
        
        A = int(year / 100)
        B = 2 - A + int(A / 4)
        
        jd_day = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
        jd_time = (hour + minute / 60.0 + second / 3600.0) / 24.0
        
        return jd_day + jd_time
    
    @staticmethod
    def _get_solar_longitude(jd: float) -> float:
        """计算太阳黄经
        
        Args:
            jd: 儒略日
            
        Returns:
            太阳黄经（角度）
        """
        # 从2000年1月1日12时UT起算的儒略世纪数
        T = (jd - 2451545.0) / 36525.0
        
        # 太阳平黄经
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
        L0 = L0 % 360
        
        # 太阳平近点角
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T
        M = radians(M % 360)
        
        # 地球轨道偏心率
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
        
        # 太阳中心差
        C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * sin(M) \
            + (0.019993 - 0.000101 * T) * sin(2 * M) \
            + 0.000289 * sin(3 * M)
        
        # 太阳真黄经
        L_true = L0 + C
        
        # 章动修正（简化版）
        omega = 125.04 - 1934.136 * T
        omega = radians(omega)
        nutation = -0.00478 * sin(omega)
        
        L_true += nutation
        
        return L_true % 360
    
    @staticmethod
    def _find_jieqi_time(year: int, longitude: float) -> datetime:
        """查找指定年份太阳到达指定黄经的时间
        
        Args:
            year: 年份
            longitude: 目标黄经（度）
            
        Returns:
            节气时间
        """
        # 初始估计：从年初开始，每隔15天左右有一个节气
        jd_start = JieqiCalculator._get_julian_day(datetime(year, 1, 1))
        
        # 简化的节气时间估计
        # 根据黄经确定大致的月份
        idx = JieqiCalculator.JIEQI_LONGITUDE.index(int(longitude))
        days_per_jieqi = 365.25 / 24.0
        estimated_jd = jd_start + idx * days_per_jieqi - 10
        
        # 使用牛顿迭代法精确定位
        for _ in range(10):
            current_longitude = JieqiCalculator._get_solar_longitude(estimated_jd)
            
            # 处理黄经过0度的情况
            if abs(current_longitude - longitude) > 180:
                if current_longitude < longitude:
                    current_longitude += 360
                else:
                    longitude += 360
            
            diff = current_longitude - longitude
            
            if abs(diff) < 0.0001:  # 精度足够
                break
            
            # 太阳黄经变化率（简化为每天约1度）
            jd_correction = diff / 0.9856
            estimated_jd -= jd_correction
        
        # 将儒略日转换回datetime
        jd = estimated_jd
        jd = jd + 0.5
        
        Z = int(jd)
        F = jd - Z
        
        if Z < 2299161:
            A = Z
        else:
            alpha = int((Z - 1867216.25) / 36524.25)
            A = Z + 1 + alpha - int(alpha / 4)
        
        B = A + 1524
        C = int((B - 122.1) / 365.25)
        D = int(365.25 * C)
        E = int((B - D) / 30.6001)
        
        day = B - D - int(30.6001 * E)
        month = E - 1 if E < 14 else E - 13
        year_calc = C - 4716 if month > 2 else C - 4715
        
        hour = int(F * 24)
        minute = int((F * 24 - hour) * 60)
        second = int(((F * 24 - hour) * 60 - minute) * 60)
        
        return datetime(year_calc, month, day, hour, minute, second)
    
    @staticmethod
    def calculate_jieqi_datetime(year: int, jieqi_index: int) -> datetime:
        """计算指定年份指定节气的精确时间
        
        Args:
            year: 年份
            jieqi_index: 节气索引（0-23）
            
        Returns:
            节气时间
            
        Raises:
            IndexError: 节气索引超出范围
        """
        if not 0 <= jieqi_index < 24:
            raise IndexError(f"节气索引超出范围: {jieqi_index}")
        
        longitude = JieqiCalculator.JIEQI_LONGITUDE[jieqi_index]
        return JieqiCalculator._find_jieqi_time(year, longitude)
    
    @staticmethod
    def get_current_jieqi(date: datetime) -> Tuple[str, datetime, datetime]:
        """获取指定日期当前所在的节气
        
        Args:
            date: 日期
            
        Returns:
            (节气名称, 节气开始时间, 下一个节气开始时间) 元组
        """
        year = date.year
        jd_date = JieqiCalculator._get_julian_day(date)
        
        # 计算该年所有节气
        jieqi_times = []
        for i in range(24):
            jieqi_time = JieqiCalculator.calculate_jieqi_datetime(year, i)
            jieqi_times.append((i, jieqi_time))
        
        # 检查是否在年份的前几个节气（可能是前一年的大寒和小寒）
        if date < jieqi_times[0][1]:
            # 在第一个节气之前，需要查看前一年的后几个节气
            prev_year_jieqi_times = []
            for i in range(22, 24):  # 小寒和大寒
                jieqi_time = JieqiCalculator.calculate_jieqi_datetime(year - 1, i)
                prev_year_jieqi_times.append((i, jieqi_time))
            
            # 找到当前节气
            for i in range(len(prev_year_jieqi_times)):
                idx, jieqi_time = prev_year_jieqi_times[i]
                if jd_date >= JieqiCalculator._get_julian_day(jieqi_time):
                    current_jieqi_index = idx
                    current_jieqi_time = jieqi_time
                    next_jieqi_time = jieqi_times[0][1]
                    current_jieqi_name = JieqiCalculator.JIEQI_NAMES[current_jieqi_index]
                    return current_jieqi_name, current_jieqi_time, next_jieqi_time
        
        # 找到当前日期所在的节气
        current_jieqi_index = 0
        current_jieqi_time = jieqi_times[0][1]
        next_jieqi_time = jieqi_times[1][1]
        
        for i in range(len(jieqi_times)):
            idx = int(i)
            _, jieqi_time = jieqi_times[idx]
            if jd_date >= JieqiCalculator._get_julian_day(jieqi_time):
                current_jieqi_index = idx
                current_jieqi_time = jieqi_time
                if idx < 23:
                    next_jieqi_time = jieqi_times[idx + 1][1]
                else:
                    # 最后一个节气，下一个是下一年的小寒
                    next_jieqi_time = JieqiCalculator.calculate_jieqi_datetime(year + 1, 22)
            else:
                break
        
        current_jieqi_name = JieqiCalculator.JIEQI_NAMES[current_jieqi_index]
        
        return current_jieqi_name, current_jieqi_time, next_jieqi_time
    
    @staticmethod
    def get_jieqi_name_by_index(idx: int) -> str:
        """根据索引获取节气名称
        
        Args:
            idx: 节气索引（0-23）
            
        Returns:
            节气名称
            
        Raises:
            IndexError: 索引超出范围
        """
        if not 0 <= idx < len(JieqiCalculator.JIEQI_NAMES):
            raise IndexError(f"节气索引超出范围: {idx}")
        return JieqiCalculator.JIEQI_NAMES[idx]
    
    @staticmethod
    def get_jieqi_index_by_name(name: str) -> int:
        """根据名称获取节气索引
        
        Args:
            name: 节气名称
            
        Returns:
            节气索引
            
        Raises:
            ValueError: 无效的节气名称
        """
        if name not in JieqiCalculator.JIEQI_INDEX:
            raise ValueError(f"无效的节气名称: {name}")
        return JieqiCalculator.JIEQI_INDEX[name]
    
    @staticmethod
    def get_all_jieqi_names() -> list[str]:
        """获取所有节气名称"""
        return JieqiCalculator.JIEQI_NAMES.copy()
    
    @staticmethod
    def is_before_lichun(date: datetime) -> bool:
        """判断日期是否在立春之前
        
        Args:
            date: 日期
            
        Returns:
            是否在立春之前
        """
        lichun_time = JieqiCalculator.calculate_jieqi_datetime(date.year, 0)
        return date < lichun_time
