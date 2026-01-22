"""八字计算工具的数据模型定义"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class BirthInfo(BaseModel):
    """出生信息"""

    date: datetime = Field(description="出生日期时间")
    year: int = Field(description="公历年份")
    month: int = Field(description="公历月份")
    day: int = Field(description="公历日")
    hour: int = Field(description="出生时")
    minute: int = Field(description="出生分")
    second: int = Field(description="出生秒")
    gender: str = Field(description="性别，男/女")
    calendar_type: str = Field(default="公历", description="历法类型，公历/农历")


class Pillar(BaseModel):
    """柱（年/月/日/时柱）"""

    gan: str = Field(description="天干")
    zhi: str = Field(description="地支")
    gan_wuxing: str = Field(description="天干五行")
    zhi_wuxing: str = Field(description="地支五行")
    full: str = Field(description="完整干支")


class YearPillar(Pillar):
    """年柱"""

    pass


class MonthPillar(Pillar):
    """月柱"""

    jieqi: str = Field(description="当前节气")
    month_name: Optional[str] = Field(default=None, description="农历月份名称")


class DayPillar(Pillar):
    """日柱"""

    day_master: str = Field(description="日主（日干）")


class HourPillar(Pillar):
    """时柱"""

    pass


class BaziResult(BaseModel):
    """八字计算结果"""

    year: YearPillar = Field(description="年柱")
    month: MonthPillar = Field(description="月柱")
    day: DayPillar = Field(description="日柱")
    hour: HourPillar = Field(description="时柱")
    birth_info: BirthInfo = Field(description="出生信息")
    jieqi_info: Optional[Dict[str, Any]] = Field(default=None, description="节气信息")


class WuxingCount(BaseModel):
    """五行统计"""

    wood: int = Field(description="木的数量")
    fire: int = Field(description="火的数量")
    earth: int = Field(description="土的数量")
    metal: int = Field(description="金的数量")
    water: int = Field(description="水的数量")


class DayMasterStrength(BaseModel):
    """日主强弱"""

    strength: str = Field(description="强弱程度：强/中/弱")
    score: int = Field(description="强度分数，0-100")
    description: str = Field(description="强弱分析描述")


class WuxingAnalysisResult(BaseModel):
    """五行分析结果"""

    day_master: str = Field(description="日主")
    wuxing_count: WuxingCount = Field(description="五行统计")
    day_master_strength: DayMasterStrength = Field(description="日主强弱")
    favorable_elements: List[str] = Field(description="用神/喜神")
    unfavorable_elements: List[str] = Field(description="忌神/闲神")
    analysis: str = Field(description="详细分析")


class TimeParseInput(BaseModel):
    """时间解析输入"""

    time_description: str = Field(description="时间描述，如'2024年3月15日上午10点'")
    gender: str = Field(description="性别，男/女")
    calendar_type: str = Field(default="公历", description="历法类型，公历/农历")


class TimeParseResult(BaseModel):
    """时间解析结果"""

    birth_info: BirthInfo = Field(description="出生信息")
    bazi: BaziResult = Field(description="八字结果")
    wuxing_analysis: Optional[WuxingAnalysisResult] = Field(default=None, description="五行分析")
