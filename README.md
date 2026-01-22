# 八字取名 Agent (Bazi Naming Agent)

基于 LangChain 1.2.6 的智能八字计算和取名 Agent，使用确定性算法确保八字计算准确性。

## 特性

- ✅ 准确的八字计算（年月日时四柱）
- ✅ 完整天文节气计算
- ✅ 五行分析和用神推算
- ✅ 自然语言时间解析
- ✅ 智能取名建议生成
- ✅ 名字综合分析（八字、平仄、笔画、三才五格、生肖）
- ✅ 批量取名功能
- ✅ 交互式多次选择分析

## 技术栈

- Python 3.10+
- LangChain 1.2.6
- GPT-4
- Pydantic
- Pytest

## 项目结构

```
src/
├── bazi_calculator/
│   ├── core/              # 核心算法模块
│   ├── data/              # 数据模块
│   ├── tools/             # LangChain Tools
│   ├── chains/            # Agent 编排
│   └── models/            # 数据模型
tests/                     # 测试文件
docs/                      # 文档
```

## 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 配置环境变量

创建 `.env` 文件：

```
OPENAI_API_KEY=your_api_key_here
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/core/test_ganzhi.py

# 查看测试覆盖率
pytest --cov=src
```

### 代码格式化和检查

```bash
# 格式化代码
black .

# 检查代码风格
ruff check .

# 类型检查
mypy src/
```

## 开发计划

详见 [PLAN.md](PLAN.md)

- ✅ 阶段0: 项目初始化
- ✅ 阶段1: 核心算法模块
- ✅ 阶段2: 八字计算 Tools
- ✅ 阶段3: 字库数据生成
- ✅ 阶段4: 取名分析 Tools
- ✅ 阶段5: 交互式 Agent
- ✅ 阶段6: 测试和优化
- ✅ 阶段7: 部署和文档

## 已完成功能

### 阶段1: 核心算法模块
- ✅ 天干地支计算 (GanzhiCalculator)
- ✅ 节气计算 (JieqiCalculator)
- ✅ 日历转换 (BaziCalendar)
- ✅ 五行分析 (WuxingAnalyzer)

### 阶段2: 八字计算 Tools
- ✅ 时间解析工具 (parse_birth_time)
- ✅ LLM智能解析工具 (LLMTimeParser)
- ✅ 智能八字计算器 (IntelligentBaziCalculator)
- ✅ 年柱计算 (calculate_year_pillar)
- ✅ 月柱计算 (calculate_month_pillar)
- ✅ 日柱计算 (calculate_day_pillar)
- ✅ 时柱计算 (calculate_hour_pillar)
- ✅ 五行分析工具 (analyze_wuxing)
- ✅ 八字Agent (BaziAgent)

### 阶段3: 数据模块
- ✅ 字库生成工具 (generate_character_library)
- ✅ 康熙字典笔画数据 (KangxiStrokes)
- ✅ 生肖规则数据 (ZodiacRules)
- ✅ 平仄声调数据 (PingzePatterns)
- ✅ 字库查询功能 (CharacterDatabase)

### 阶段4: 取名分析 Tools
- ✅ 八字取名分析Tool (analyze_bazi_for_naming)
- ✅ 适合字查询Tool (get_suitable_chars)
- ✅ 名字生成Tool (generate_name_suggestions)
- ✅ 批量取名Tool (generate_batch_names)
- ✅ 平仄分析Tool (check_pingze_harmony)
- ✅ 笔画分析Tool (check_strokes_harmony)
- ✅ 三才五格Tool (analyze_sancai_wuge)
- ✅ 综合凶吉分析Tool (comprehensive_name_analysis)

### 阶段5: 交互式 Agent
- ✅ 交互式八字取名Agent (InteractiveBaziNamingAgent)
- ✅ 完整交互流程
- ✅ 批量取名功能
- ✅ 多次选择分析功能
- ✅ 命令行入口 (main.py)

### 阶段6: 测试和优化
- ✅ 单元测试 (tests/tools/)
- ✅ 集成测试 (tests/integration/)
- ✅ 准确性验证 (已知八字测试)
- ✅ 性能测试 (响应时间<2秒)

### 阶段7: 部署和文档
- ✅ README.md 更新
- ✅ API参考文档 (docs/API_REFERENCE.md)
- ✅ 用户指南 (docs/TODO.md)
- ✅ 项目文档完善

### 阶段8: 算法修复和优化
- ✅ 修复月柱计算错误（节气映射和五虎遁法）
- ✅ 修复时柱计算错误（五鼠遁表数据）
- ✅ 验证所有测试用例通过
- ✅ 添加智能LLM输入解析功能
- ✅ 优化用户交互流程
- ✅ 整合文档体系

## 文档

### 核心文档
- [README.md](README.md) - 项目总览（本文件）
- [开发计划](PLAN.md) - 详细的开发计划和TODO
- [开发指南](AGENTS.md) - 为AI助手提供的开发指南

### 专项文档
- [八字算法修复](BAZI_ALGORITHM_FIX.md) - 算法修复详解
  - 月柱计算错误及修复
  - 时柱计算错误及修复
  - 节气映射表修正
  - 五鼠遁表修正
  - 测试用例验证

- [开发历程](DEVELOPMENT_HISTORY.md) - 项目开发历程
  - 各阶段完成情况
  - 关键修复和优化
  - 文档体系
  - 版本历史

- [文档说明](DOCS_GUIDE.md) - 文档使用指南
  - 文件结构说明
  - 快速开始指南
  - 常见问题解答
- [智能解析指南](LLM_PARSER_GUIDE.md) - LLM智能八字解析功能使用指南

## 项目特色

1. **准确的八字计算**：使用确定性算法，确保计算结果准确
2. **智能输入解析**：使用LLM解析自然语言，支持灵活的输入格式
3. **智能取名建议**：基于八字五行分析，提供个性化取名建议
4. **批量取名功能**：支持批量生成20-30个名字，支持用户选择
5. **综合分析**：整合八字、平仄、笔画、三才五格等多维度分析
6. **交互式体验**：友好的命令行界面，支持多次选择分析
7. **高性能**：八字计算<10ms，综合分析<2秒
8. **完整的测试**：包含单元测试、集成测试、准确性验证和性能测试

## 核心功能说明

### 八字计算

- 年柱计算（以立春为界）
- 月柱计算（以节气为界，五虎遁法）
- 日柱计算（基准日期推算）
- 时柱计算（五鼠遁法）

### 取名分析

- 五行分析（用神、喜神、忌神）
- 平仄分析（音韵和谐）
- 笔画分析（康熙字典）
- 三才五格（吉凶分析）
- 生肖宜忌（字根匹配）

### 批量取名

- 支持基于用户选择生成
- 自动智能组合
- 简要分析和评分
- 20-30 个名字建议

## 贡献指南

请查看 [AGENTS.md](AGENTS.md) 了解开发指南和代码规范。

## 许可证

MIT License
