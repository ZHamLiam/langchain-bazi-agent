# 交互式八字取名系统 - 完整指南

本系统提供完整的八字计算、五行分析、命格分析和取名建议功能。

## 快速开始

### 运行交互式程序

```bash
python interactive_bazi_with_naming.py
```

### 使用流程

1. **输入出生信息** - 支持多种格式
2. **查看分析结果** - 八字、五行、命格
3. **选择是否需要取名** - 可跳过
4. **选择性别** - 男孩/女孩
5. **查看取名建议** - 10个名字及详细分析

## 功能概述

### 1. 八字计算

使用LLM智能解析多种格式的出生信息，准确计算：
- 年柱（天干地支、五行）
- 月柱（天干地支、五行、节气）
- 日柱（天干地支、五行、日主）
- 时柱（天干地支、五行）

**输入格式示例：**
- `1990年3月15日上午10点30分，男`
- `1985年8月22日下午3点，女`
- `2000年12月25日晚上8点15分，男`
- `我是1998年出生的，生日是9月18日下午2点，女`

### 2. 五行分析

- **五行统计**：金、木、水、火、土的数量
- **日主强弱**：判断日主强弱程度（强/中和/弱）
- **用神推算**：确定用神、喜神、忌神

**输出示例：**
```
五行统计：
  木：2个 ██
  火：2个 ██
  土：1个 █
  金：1个 █
  水：2个 ██

日主强弱：弱

用神推算：
  用神：金
  喜神：土
  忌神：木, 火
```

### 3. 命格分析

#### 格局分析

判断命局属于哪种格局：
- **正格**：建禄格、财格、官格
- **从格**：从财格、从官格、从儿格
- **化气格**：甲己化土、乙庚化金等

#### 性格分析

根据日主分析性格特征：
- 甲木：刚强、正直、有领导力
- 乙木：温柔、善良、灵活
- 丙火：热情、开朗、阳光
- 丁火：细腻、敏感、有洞察力
- 戊土：稳重、可靠、有担当
- 己土：温和、包容、善解人意
- 庚金：刚毅、果断、有魄力
- 辛金：精致、优雅、有品味
- 壬水：聪明、灵活、适应力强
- 癸水：温柔、智慧、深沉

#### 事业财运分析

根据用神、喜神分析适合的事业和财运：

**五行对应事业：**
- 金：金融、银行、珠宝、汽车、机械、IT技术、法律
- 木：教育、文化、艺术、出版、林业、家具、服装
- 水：贸易、物流、旅游、水产、航运、饮料、清洁
- 火：电子、IT互联网、能源、餐饮、娱乐、广告、媒体
- 土：房地产、建筑、农业、矿产、陶瓷、古玩、仓储

#### 健康分析

根据五行分析健康状况和保健建议：

**五行与健康对应：**
- 金：肺、呼吸系统、皮肤、大肠
- 木：肝、胆、眼睛、筋骨
- 水：肾、膀胱、耳朵、生殖系统
- 火：心、小肠、舌头、血液
- 土：脾、胃、肌肉、消化系统

### 4. 取名建议

#### 取名流程

1. 根据八字分析查询适合字（用神、喜神优先）
2. 结合生肖过滤不适合的字
3. 使用LLM生成10个名字建议
4. 每个名字都有详细分析

#### 名字分析内容

每个名字包含：
- **名字**：含拼音
- **类型**：单字/双字
- **五行属性**：每个字的五行
- **平仄搭配**：每个字的平仄
- **笔画数**：每个字的康熙笔画
- **寓意解释**：字义说明
- **出处**：出自经典文献
- **八字匹配度**：与八字的匹配说明
- **评分**：满分100分

#### 取名评分标准

- 符合用神：+30分
- 符合喜神：+20分
- 寓意优美：+20分
- 平仄和谐：+15分
- 出自经典：+15分

## 技术架构

### 文件结构

```
langchain_bazi_agent/
├── interactive_bazi_with_naming.py  # 交互式主程序
├── .env                           # 环境变量配置
├── requirements.txt                # 依赖项
└── src/
    └── bazi_calculator/
        ├── core/
        │   ├── calendar.py          # 八字日历计算
        │   ├── ganzhi.py            # 干支计算
        │   ├── wuxing.py            # 五行分析
        │   ├── jieqi.py             # 节气计算
        │   └── mingge.py            # 命格分析（新增）
        ├── tools/
        │   ├── bazi/
        │   │   ├── intelligent_parser.py  # 智能解析器
        │   │   ├── time_parser.py        # 时间解析
        │   │   ├── llm_time_parser.py    # LLM时间解析
        │   │   └── wuxing_analysis.py    # 五行分析工具
        │   └── naming/
        │       ├── name_generator.py     # 名字生成
        │       └── suitable_chars.py     # 适合字查询
        └── chains/
            └── bazi_agent.py            # 八字Agent
```

### 核心模块

#### 1. IntelligentBaziCalculator

智能八字计算器，使用LLM解析用户输入：

```python
from bazi_calculator.tools.bazi.intelligent_parser import IntelligentBaziCalculator

calculator = IntelligentBaziCalculator(llm)
result = calculator.calculate_from_natural_language("1990年3月15日上午10点30分，男")
```

#### 2. WuxingAnalyzer

五行分析器，提供五行统计、日主强弱分析和用神推算：

```python
from bazi_calculator.core.wuxing import WuxingAnalyzer

# 统计五行
wuxing_count = WuxingAnalyzer.count_wuxing_in_bazi(bazi)

# 分析日主强弱
strength, scores = WuxingAnalyzer.analyze_day_master_strength(bazi)

# 推算用神
yong_shen_info = WuxingAnalyzer.determine_yong_shen(bazi)

# 综合分析
wuxing_analysis = WuxingAnalyzer.analyze_comprehensive(bazi)
```

#### 3. MingGeAnalyzer

命格分析器，提供格局、性格、事业财运、健康分析：

```python
from bazi_calculator.core.mingge import MingGeAnalyzer

# 格局分析
pattern = MingGeAnalyzer.determine_pattern(bazi)

# 性格分析
personality = MingGeAnalyzer.analyze_personality(bazi)

# 事业财运分析
career_wealth = MingGeAnalyzer.analyze_career_wealth(bazi, wuxing_analysis)

# 健康分析
health = MingGeAnalyzer.analyze_health(bazi)

# 综合分析
mingge_analysis = MingGeAnalyzer.analyze_comprehensive(bazi, wuxing_analysis)
```

## 环境配置

### .env 文件配置

```
# Qwen API配置
QWEN_API_KEY="sk-0ab370f572574ba38227876f3a687d67"
QWEN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL="qwen-flash"
```

### 依赖项

确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

主要依赖：
- langchain
- langchain-openai
- pydantic
- python-dotenv
- 其他依赖见 requirements.txt

## 注意事项

### 1. 八字分析仅供参考

八字分析基于传统理论，仅供参考，不应过度依赖。

### 2. 取名建议需结合实际

取名建议需要结合家庭实际情况，最终选择建议与家人商量。

### 3. 网络和API配置

- 需要稳定的网络连接
- 确保 API Key 有效
- 确保 API 配额充足

### 4. LSP 类型检查警告

可能会看到类型检查警告，这是静态类型检查器的误报，不影响运行。

## 故障排除

### 问题：连接失败

**检查：**
1. `.env` 文件是否存在
2. `QWEN_API_KEY` 是否配置正确
3. 网络连接是否正常
4. API Key 是否有效

### 问题：取名建议生成失败

**解决：**
- 可能是网络或API问题，可以稍后重试
- 检查 API 配额是否充足

### 问题：八字计算失败

**检查：**
1. 输入格式是否正确
2. 日期是否有效
3. 时间解析是否成功

## 测试

### 运行单元测试

```bash
pytest tests/
```

### 测试八字计算

```bash
pytest tests/integration/test_bazi_with_wuxing_analysis.py -v -s
```

## 开发指南

详细的开发指南请参考：
- `AGENTS.md` - 开发者指南
- `README.md` - 项目总览
- `PLAN.md` - 项目规划

## 项目历史

详细的历史记录请参考 `DEVELOPMENT_HISTORY.md`。

## 许可证

本项目仅供学习和研究使用。
