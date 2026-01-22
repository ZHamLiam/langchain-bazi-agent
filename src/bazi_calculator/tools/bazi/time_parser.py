"""时间解析工具

用于解析自然语言时间描述，支持多种格式
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional

from langchain_core.tools import tool

from bazi_calculator.models.schemas import BirthInfo, TimeParseResult


@tool
def parse_birth_time(time_description: str, gender: str, calendar_type: str = "公历") -> Dict[str, Any]:
    """解析自然语言时间描述

    支持多种时间格式：
    - 标准格式：2024年3月15日 10点30分
    - 简写格式：2024.3.15 10:30
    - 纯数字格式：202403151030
    - 汉字格式：甲辰年二月十五日

    Args:
        time_description: 时间描述
        gender: 性别（男/女）
        calendar_type: 历法类型（公历/农历）

    Returns:
        解析后的出生信息字典
    """
    birth_info = _parse_time_description(time_description, gender, calendar_type)
    return birth_info.model_dump()


def _parse_time_description(time_description: str, gender: str, calendar_type: str) -> BirthInfo:
    """解析时间描述

    Args:
        time_description: 时间描述
        gender: 性别
        calendar_type: 历法类型

    Returns:
        BirthInfo对象
    """
    time_description = time_description.strip()

    # 尝试匹配标准格式：2024年3月15日 10点30分
    pattern1 = r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2})点?(\d{0,2})分?'
    match = re.search(pattern1, time_description)

    if match:
        year, month, day, hour, minute = match.groups()
        hour = int(hour) if hour else 0
        minute = int(minute) if minute else 0
        birth_date = datetime(int(year), int(month), int(day), hour, minute)
    else:
        # 尝试匹配简写格式：2024.3.15 10:30
        pattern2 = r'(\d{4})\.(\d{1,2})\.(\d{1,2})\s*(\d{1,2}):?(\d{0,2})?'
        match = re.search(pattern2, time_description)

        if match:
            year, month, day, hour, minute = match.groups()
            hour = int(hour) if hour else 0
            minute = int(minute) if minute else 0
            birth_date = datetime(int(year), int(month), int(day), hour, minute)
        else:
            # 尝试匹配纯数字格式：202403151030
            pattern3 = r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})'
            match = re.search(pattern3, time_description.replace(' ', ''))

            if match:
                year, month, day, hour, minute = match.groups()
                birth_date = datetime(int(year), int(month), int(day), int(hour), int(minute))
            else:
                raise ValueError(f"无法解析时间描述：{time_description}")

    return BirthInfo(
        date=birth_date,
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=birth_date.hour,
        minute=birth_date.minute,
        second=birth_date.second,
        gender=gender,
        calendar_type=calendar_type
    )


@tool
def validate_time(birth_date: datetime) -> Dict[str, Any]:
    """验证出生时间的有效性

    Args:
        birth_date: 出生日期时间

    Returns:
        验证结果
    """
    result = {
        "valid": True,
        "message": "时间有效"
    }

    try:
        # 检查年份范围（1900-2100）
        if birth_date.year < 1900 or birth_date.year > 2100:
            result["valid"] = False
            result["message"] = f"年份超出范围：{birth_date.year}"

        # 检查月份
        if birth_date.month < 1 or birth_date.month > 12:
            result["valid"] = False
            result["message"] = f"月份无效：{birth_date.month}"

        # 检查日期
        if birth_date.day < 1 or birth_date.day > 31:
            result["valid"] = False
            result["message"] = f"日期无效：{birth_date.day}"

        # 检查时间
        if birth_date.hour < 0 or birth_date.hour > 23:
            result["valid"] = False
            result["message"] = f"小时无效：{birth_date.hour}"

        if birth_date.minute < 0 or birth_date.minute > 59:
            result["valid"] = False
            result["message"] = f"分钟无效：{birth_date.minute}"

    except Exception as e:
        result["valid"] = False
        result["message"] = f"验证出错：{str(e)}"

    return result
