# 八字取名Agent - API参考文档

## 目录

- [核心算法模块](#核心算法模块)
- [八字计算Tools](#八字计算tools)
- [数据模块](#数据模块)
- [取名分析Tools](#取名分析tools)
- [Agent类](#agent类)

## 核心算法模块

### GanzhiCalculator

天干地支计算器

**方法：**

- `get_all_tiangan() -> List[str]` - 获取所有天干
- `get_all_dizhi() -> List[str]` - 获取所有地支
- `get_all_wuxing() -> List[str]` - 获取所有五行
- `get_tiangan_by_index(index: int) -> str` - 根据索引获取天干
- `get_dizhi_by_index(index: int) -> str` - 根据索引获取地支
- `get_tiangan_wuxing(tiangan: str) -> str` - 获取天干五行
- `get_dizhi_wuxing(dizhi: str) -> str` - 获取地支五行
- `get_jiazi_by_index(index: int) -> str` - 获取六十甲子

**示例：**

```python
from bazi_calculator.core.ganzhi import GanzhiCalculator

# 获取天干
tiangan = GanzhiCalculator.get_tiangan_by_index(0)  # 返回 "甲"

# 获取地支
dizhi = GanzhiCalculator.get_dizhi_by_index(0)  # 返回 "子"

# 获取五行
wuxing = GanzhiCalculator.get_tiangan_wuxing("甲")  # 返回 "木"
```

### JieqiCalculator

节气计算器

**方法：**

- `calculate_jieqi_datetime(year: int, jieqi_index: int) -> datetime` - 计算节气时间
- `get_current_jieqi(date: datetime) -> Tuple[str, datetime, int]` - 获取当前节气
- `is_before_lichun(date: datetime) -> bool` - 判断是否在立春之前

### BaziCalendar

八字日历计算器

**方法：**

- `get_year_pillar(birth_date: datetime) -> Tuple[str, str, str, str]` - 计算年柱
- `get_month_pillar(birth_date: datetime, year_gan: str) -> Tuple[str, str, str, str, str]` - 计算月柱
- `get_day_pillar(birth_date: datetime) -> Tuple[str, str, str, str]` - 计算日柱
- `get_hour_pillar(birth_time: datetime, day_gan: str) -> Tuple[str, str, str, str]` - 计算时柱
- `get_all_pillars(birth_date: datetime) -> dict` - 计算完整四柱

**示例：**

```python
from bazi_calculator.core.calendar import BaziCalendar
from datetime import datetime

birth_date = datetime(2024, 3, 15, 10, 30)

# 计算完整四柱
bazi = BaziCalendar.get_all_pillars(birth_date)

print(f"年柱：{bazi['year']['full']}")
print(f"月柱：{bazi['month']['full']}")
print(f"日柱：{bazi['day']['full']}")
print(f"时柱：{bazi['hour']['full']}")
```

### WuxingAnalyzer

五行分析器

**方法：**

- `count_wuxing_in_bazi(bazi: Dict) -> Dict[str, int]` - 统计八字五行
- `analyze_day_master_strength(bazi: Dict) -> Tuple[str, Dict]` - 分析日主强弱
- `determine_yong_shen(bazi: Dict) -> Dict` - 推算用神
- `analyze_comprehensive(bazi: Dict) -> Dict` - 综合分析

## 八字计算Tools

### 时间解析工具

**函数：**

- `parse_birth_time(time_description: str, gender: str, calendar_type: str = "公历") -> Dict`
- `validate_time(birth_date: datetime) -> Dict`

**示例：**

```python
from bazi_calculator.tools.bazi import parse_birth_time

result = parse_birth_time.invoke({
    "time_description": "2024年3月15日10点30分",
    "gender": "男",
    "calendar_type": "公历"
})

print(f"年份：{result['year']}")
print(f"月份：{result['month']}")
print(f"日期：{result['day']}")
```

### 四柱计算工具

**函数：**

- `calculate_year_pillar(birth_date: datetime) -> dict`
- `calculate_month_pillar(birth_date: datetime, year_gan: str) -> dict`
- `calculate_day_pillar(birth_date: datetime) -> dict`
- `calculate_hour_pillar(birth_time: datetime, day_gan: str) -> dict`

### 五行分析工具

**函数：**

- `analyze_wuxing(bazi: Dict[str, Any]) -> Dict[str, Any]` - 综合五行分析
- `count_wuxing(bazi: Dict[str, Any]) -> Dict[str, Any]` - 五行统计
- `analyze_day_master_strength(bazi: Dict[str, Any]) -> Dict[str, Any]` - 日主强弱分析
- `determine_yong_shen(bazi: Dict[str, Any]) -> Dict[str, Any]` - 用神推算

## 数据模块

### KangxiStrokes

康熙字典笔画查询器

**方法：**

- `get_strokes(char: str) -> Optional[int]` - 获取笔画数
- `get_strokes_multiple(chars: str) -> Dict[str, Optional[int]]` - 批量获取笔画
- `calculate_total_strokes(chars: str) -> int` - 计算总笔画
- `get_chars_by_strokes_range(min_strokes: int, max_strokes: int) -> List[str]` - 按笔画范围查询

### ZodiacRules

生肖规则查询器

**方法：**

- `get_zodiac_by_year(year: int) -> str` - 根据年份获取生肖
- `get_favor_radicals(zodiac: str) -> List[str]` - 获取喜用字根
- `get_avoid_radicals(zodiac: str) -> List[str]` - 获取忌用字根
- `get_favor_chars(zodiac: str) -> List[str]` - 获取宜用字
- `get_avoid_chars(zodiac: str) -> List[str]` - 获取忌用字

### PingzePatterns

平仄声调查询器

**方法：**

- `get_tone(char: str) -> Optional[int]` - 获取声调
- `get_pingze(char: str) -> Optional[str]` - 获取平仄
- `analyze_name_pingze(name: str) -> Dict[str, Any]` - 分析名字平仄
- `check_harmony(name: str) -> Dict[str, Any]` - 检查平仄和谐度

### CharacterDatabase

字库数据库

**方法：**

- `query_by_wuxing(wuxing: str, count: int = 25) -> List[Dict]` - 按五行查询
- `query_by_zodiac(zodiac: str, count: int = 25) -> List[Dict]` - 按生肖查询
- `query_comprehensive(wuxing: str = None, zodiac: str = None, ...) -> List[Dict]` - 综合查询
- `get_char_info(char: str) -> Optional[Dict]` - 获取字符详细信息

## 取名分析Tools

### 八字取名分析

**函数：**

- `analyze_bazi_for_naming(bazi: Dict[str, Any]) -> Dict[str, Any]` - 八字取名分析
- `get_naming_priorities(bazi_analysis: Dict[str, Any]) -> Dict[str, Any]` - 取名优先级
- `check_name_wuxing_balance(name: str, char_library: Dict, bazi_analysis: Dict) -> Dict` - 检查五行平衡

### 适合字查询

**函数：**

- `get_suitable_chars(bazi_analysis: Dict, char_library: Dict, count_per_wuxing: int = 25) -> Dict`
- `filter_suitable_chars_by_strokes(suitable_chars: Dict, min_strokes: int, max_strokes: int) -> Dict`
- `get_top_suitable_chars(suitable_chars: Dict, top_count: int = 10) -> List[Dict]`

### 名字生成

**函数：**

- `generate_name_suggestions(suitable_chars: Dict, bazi_analysis: Dict, count: int = 10) -> Dict`
- `format_name_suggestions(name_suggestions: List[Dict]) -> str`

### 批量取名

**函数：**

- `generate_batch_names(suitable_chars: Dict, bazi_analysis: Dict, user_selected_chars: Optional[List] = None, count: int = 30) -> Dict`
- `format_batch_names(names: List[Dict]) -> str`

### 平仄分析

**函数：**

- `analyze_name_pingze(name: str) -> Dict[str, Any]`
- `check_pingze_harmony(name: str) -> Dict[str, Any]`
- `compare_name_pingze(name1: str, name2: str) -> Dict[str, Any]`

### 笔画分析

**函数：**

- `analyze_name_strokes(name: str) -> Dict[str, Any]`
- `check_strokes_harmony(name: str) -> Dict[str, Any]`
- `compare_name_strokes(name1: str, name2: str) -> Dict[str, Any]`

### 三才五格

**函数：**

- `calculate_wuge(name: str, surname: str = "李") -> Dict[str, Any]`
- `calculate_sancai(wuge_result: Dict[str, Any]) -> Dict[str, Any]`
- `analyze_sancai_wuge(name: str, surname: str = "李") -> Dict[str, Any]`

### 综合分析

**函数：**

- `comprehensive_name_analysis(name: str, bazi_analysis: Dict, char_library: Dict, surname: str = "李") -> Dict[str, Any]`
- `format_comprehensive_analysis(analysis: Dict[str, Any]) -> str`

## Agent类

### BaziAgent

八字计算Agent

**方法：**

```python
class BaziAgent:
    def __init__(self, llm: Optional[ChatOpenAI] = None)
    def calculate_bazi(time_description: str, gender: str, calendar_type: str = "公历") -> Dict[str, Any]
    def format_bazi_result(result: Dict[str, Any]) -> str
    def get_tools(self) -> List[BaseTool]
```

**示例：**

```python
from bazi_calculator.chains.bazi_agent import BaziAgent

agent = BaziAgent()

# 计算八字
result = agent.calculate_bazi("2024年3月15日10点30分", "男")

# 格式化输出
print(agent.format_bazi_result(result))
```

### InteractiveBaziNamingAgent

交互式八字取名Agent

**方法：**

```python
class InteractiveBaziNamingAgent:
    def __init__(self, llm: Optional[ChatOpenAI] = None, char_library_path: Optional[str] = None)
    def calculate_bazi(time_description: str, gender: str, calendar_type: str = "公历") -> Dict[str, Any]
    def generate_suitable_chars(bazi_result: Dict[str, Any]) -> Dict[str, Any]
    def generate_name_suggestions(bazi_result: Dict, suitable_chars: Dict, count: int = 10) -> Dict
    def generate_batch_names(bazi_result: Dict, suitable_chars: Dict, user_selected_chars: Optional[List] = None, count: int = 30) -> Dict
    def analyze_selected_name(name: str, bazi_result: Dict) -> Dict
    def run_interactive_session(time_description: str, gender: str, calendar_type: str = "公历")
```

**示例：**

```python
from bazi_calculator.chains.interactive_agent import InteractiveBaziNamingAgent

agent = InteractiveBaziNamingAgent(char_library_path="char_library.json")

# 运行交互式会话
agent.run_interactive_session("2024年3月15日10点30分", "男")
```

## 快速开始

### 命令行使用

```bash
python -m src.main
```

### Python代码使用

```python
from bazi_calculator.chains.interactive_agent import InteractiveBaziNamingAgent

# 创建Agent
agent = InteractiveBaziNamingAgent()

# 计算八字
bazi_result = agent.calculate_bazi("2024年3月15日10点30分", "男")

# 显示结果
agent.display_bazi_result(bazi_result)

# 生成适合字
suitable_chars = agent.generate_suitable_chars(bazi_result)
agent.display_suitable_chars(suitable_chars)

# 生成名字建议
name_result = agent.generate_name_suggestions(bazi_result, suitable_chars)
agent.display_name_suggestions(name_result)
```

## 错误处理

所有函数都包含适当的错误处理和验证：

- 时间格式验证
- 字符有效性检查
- 边界条件处理
- 类型安全保证

## 性能优化

- 八字计算：< 10ms
- 五行分析：< 20ms
- 综合取名分析：< 2秒
- 批量取名（30个）：< 5秒

## 更多信息

- 详细功能说明：[PLAN.md](../PLAN.md)
- 开发指南：[AGENTS.md](../AGENTS.md)
- 项目主页：[README.md](../README.md)
