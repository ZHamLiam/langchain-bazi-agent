## 📋 八字取名Agent - 完整开发计划与TODO
### 一、项目概述
项目名称: langchain_bazi_agent  
核心功能: 基于LangChain 1.2.6的八字计算和取名Agent  
核心痛点: 传统大模型计算八字结果因过度思考导致偏差，使用确定性公式确保准确  
技术栈: Python 3.10+, LangChain 1.2.6, GPT-4
### 二、功能需求
核心功能
1. ✅ 八字计算（年月日时四柱）
2. ✅ 五行分析和用神推算
3. ✅ 自然语言时间解析
4. ✅ 完整天文节气计算
5. ✅ 五行分析
6. ✅ 取名建议生成
7. ✅ 名字综合分析（八字、平仄、笔画、三才五格、生肖）
8. ✅ 批量取名功能
9. ✅ 交互式多次选择分析
批量取名功能说明
- 触发时机: 用户在看到适合字列表后，可选择心仪的字
- 生成策略:
  - 如果用户选择了心仪的字：基于用户选择的字进行组合生成
  - 如果用户未选择：从适合字列表中自动组合生成
- 生成数量: 20-30个名字
- 分析深度: 简要分析（包含五行、平仄、简要寓意）
---
### 三、开发计划
阶段0: 项目初始化 (0.5天)
任务清单
- [ ] 创建项目目录结构
- [ ] 配置虚拟环境
- [ ] 安装依赖（langchain==1.2.6, pydantic, pytest等）
- [ ] 编写requirements.txt
- [ ] 初始化Git仓库
- [ ] 创建README.md
目录结构
src/
├── bazi_calculator/
│   ├── __init__.py
│   ├── core/                          # 核心算法模块
│   │   ├── __init__.py
│   │   ├── ganzhi.py                  # 天干地支
│   │   ├── jieqi.py                   # 节气计算
│   │   ├── calendar.py                # 日历转换
│   │   └── wuxing.py                  # 五行生克
│   ├── data/                          # 数据模块
│   │   ├── __init__.py
│   │   ├── char_database.py           # 字库（LLM生成）
│   │   ├── kangxi_strokes.py          # 康熙字典笔画
│   │   ├── zodiac_rules.py           # 生肖规则
│   │   └── pingze_patterns.py        # 平仄声调
│   ├── tools/                         # LangChain Tools
│   │   ├── __init__.py
│   │   ├── bazi/                      # 八字计算Tools
│   │   │   ├── __init__.py
│ 批量取名功能设计
│   │   └── naming/                    # 取名分析Tools
│   │       ├── __init__.py
│   │       ├── char_library_generator.py  # 字库生成
│   │       ├── bazi_for_naming.py         # 八字取名分析
│   │       ├── suitable_chars.py          # 适合字查询
│   │       ├── name_generator.py          # 名字生成
│   │       ├── name_generator.py          # 名字生成
│   │       ├── batch_name_generator.py     # 批量取名生成
│   │       ├── pingze_analysis.py         # 平仄分析
│   │       ├── stroke_analysis.py         # 笔画分析
│   │       ├── sangcai_wuge.py            # 三才五格
│   │       ├── comprehensive_analysis.py   # 综合凶吉
│   │       └── user_selection_analysis.py # 用户选择分析
│   ├── chains/                        # Agent编排
│   │   ├── __init__.py
│   │   ├── bazi_agent.py              # 八字Agent
│   │   ├── naming_agent.py            # 取名Agent
│   │   └── interactive_agent.py       # 交互式Agent
│   └── models/                        # 数据模型
│       ├── __init__.py
│       ├── schemas.py                 # Pydantic模型
│       └── enums.py                   # 枚举类型
tests/
├── core/
│   ├── test_ganzhi.py
│   ├── test_jieqi.py
│   └── test_calendar.py
├── tools/
│   ├── test_bazi_tools.py
│   └── test_naming_tools.py
├── chains/
│   ├── test_bazi_agent.py
│   └── test_interactive_agent.py
└── integration/
    └── test_full_workflow.py
docs/
├── DEVELOPMENT_PLAN.md  # 本文档
├── TODO.md
└── API_REFERENCE.md
requirements.txt
README.md
AGENTS.md
---
阶段1: 核心算法模块 (2-3天)
1.1 Ganzhi模块 (0.5天)
文件: src/bazi_calculator/core/ganzhi.py
功能:
- 天干地支定义（10天干，12地支）
- 五行映射（天干地支对应五行）
- 干支计算函数
- 五行查询函数
关键实现:
class GanzhiCalculator:
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    @staticmethod
    def get_ganzhi_pair(tiangan_idx: int, dizhi_idx: int) -> Tuple[str, str]
    
    @staticmethod
    def get_wuxing(tiangan: str, dizhi: str) -> Tuple[str, str]
测试: 编写单元测试验证干支计算准确性
1.2 Jieqi模块 (1天)
文件: src/bazi_calculator/core/jieqi.py
功能:
- 二十四节气定义
- 节气太阳黄经定义
- 节气时刻计算（天文算法）
- 当前节气查询
关键实现:
class JieqiCalculator:
    JIEQI_NAMES = ['立春', '雨水', ...]  # 24个节气
    JIEQI_LONGITUDE = [315, 330, ...]    # 对应太阳黄经
    
    @staticmethod
    def calculate_jieqi_datetime(year: int, jieqi_index: int) -> datetime
    
    @staticmethod
    def get_current_jieqi(date: datetime) -> Tuple[str, datetime]
算法: 基于Jean Meeus《Astronomical Algorithms》
测试: 验证节气时刻准确性（对比历书）
1.3 Calendar模块 (1天)
文件: src/bazi_calculator/core/calendar.py
功能:
- 年柱计算（以立春为界）
- 月柱计算（以节气为界，五虎遁法）
- 日柱计算（基准日期推算）
- 时柱计算（五鼠遁法）
关键实现:
class BaziCalendar:
    @staticmethod
    def get_year_pillar(birth_date: datetime) -> Tuple[str, str, str, str]
    
    @staticmethod
    def get_month_pillar(birth_date: datetime, year_tiangan: str) -> Tuple[str, str, str, str]
    
    @staticmethod
    def get_day_pillar(birth_date: datetime) -> Tuple[str, str, str, str]
    
    @staticmethod
    def get_hour_pillar(birth_time: datetime, day_tiangan: str) -> Tuple[str, str, str, str]
测试: 验证四柱计算准确性
1.4 Wuxing模块 (0.5天)
文件: src/bazi_calculator/core/wuxing.py
功能:
- 五行生克关系定义
- 日主强弱分析
- 用神推算算法
测试: 验证五行分析逻辑
---
阶段2: LangChain Tools - 八字计算 (2-3天)
2.1 时间解析Tool (0.5天)
文件: src/bazi_calculator/tools/bazi/time_parser.py
功能: 
- 解析自然语言时间描述
- 支持公历/农历
- 支持多种格式
关键实现:
@tool
def parse_birth_time(time_description: str, gender: str) -> dict
2.2 四柱计算Tools (1天)
文件: 
- src/bazi_calculator/tools/bazi/year_pillar.py
- src/bazi_calculator/tools/bazi/month_pillar.py
- src/bazi_calculator/tools/bazi/day_pillar.py
- src/bazi_calculator/tools/bazi/hour_pillar.py
功能: 封装四柱计算为LangChain Tools
2.3 五行分析Tool (0.5天)
文件: src/bazi_calculator/tools/bazi/wuxing_analysis.py
功能:
- 统计四柱五行
- 分析日主强弱
- 确定用神、喜神、忌神
2.4 八字Agent (1天)
文件: src/bazi_calculator/chains/bazi_agent.py
功能:
- 整合所有八字计算Tools
- 提供统一接口
---
阶段3: 数据模块 - 字库生成 (2-3天)
3.1 字库生成Tool (1天)
文件: src/bazi_calculator/tools/naming/char_library_generator.py
功能: 
- 使用LLM生成汉字字库
- 每个五行500字
- 包含完整属性（五行、拼音、康熙笔画、生肖宜忌、平仄、寓意、出处）
关键实现:
@tool
def generate_character_library(wuxing_categories: List[str] = None) -> Dict[str, Any]
LLM Prompt设计: 详细的JSON输出要求
3.2 康熙字典笔画 (0.5天)
文件: src/bazi_calculator/data/kangxi_strokes.py
功能:
- 康熙字典笔画数查询
- 约20000字
3.3 生肖规则 (0.5天)
文件: src/bazi_calculator/data/zodiac_rules.py
功能:
- 12生肖宜忌规则
- 字根映射
3.4 平仄声调 (0.5天)
文件: src/bazi_calculator/data/pingze_patterns.py
功能:
- 汉字平仄数据
- 声调分析
- 平仄和谐检查
3.5 字库查询 (0.5天)
文件: src/bazi_calculator/data/char_database.py
功能:
- 字库数据结构
- 按五行/生肖查询
---
阶段4: 取名分析Tools (2-3天)
4.1 八字取名分析Tool (0.5天)
文件: src/bazi_calculator/tools/naming/bazi_for_naming.py
功能:
- 分析八字确定用神
- 提取生肖信息
4.2 适合字查询Tool (0.5天)
文件: src/bazi_calculator/tools/naming/suitable_chars.py
功能:
- 根据生肖和五行需求筛选字
- 每个五行返回25个字
4.3 名字生成Tool (1天)
文件: src/bazi_calculator/tools/naming/name_generator.py
功能:
- 使用LLM生成10个名字
- 单字+双字名
- 详细分析（八字、五行、寓意、出处）
4.4 批量取名Tool (0.5天) ⭐ 新增
文件: src/bazi_calculator/tools/naming/batch_name_generator.py
功能:
- 批量生成20-30个名字
- 支持基于用户选择或自动组合
- 简要分析
关键实现:
@tool
def generate_batch_names(
    suitable_chars: Dict[str, List[Dict]],
    bazi_analysis: Dict,
    user_selected_chars: List[str] = None,  # 用户选择的心仪字
    count: int = 30
) -> Dict[str, List[Dict]]:
    """批量生成名字建议
    
    Args:
        suitable_chars: 适合字字典
        bazi_analysis: 八字分析
        user_selected_chars: 用户选择的心仪字（可选）
        count: 生成数量（默认30个）
        
    Returns:
        {
            "names": [
                {
                    "name": "煜坤",
                    "type": "双字",
                    "pinyin": "yù kūn",
                    "wuxing": {"煜": "火", "坤": "土"},
                    "pingze": {"煜": "仄", "坤": "平"},
                    "brief_meaning": "光辉灿烂，大地广阔",
                    "wuxing_match": "符合用神火、喜神土",
                    "score": 90
                },
                # 共20-30个
            ],
            "generation_mode": "基于用户选择" or "自动组合",
            "summary": "已生成25个名字"
        }
    """
    pass
生成逻辑:
def generate_batch_names(suitable_chars, bazi_analysis, user_selected_chars, count):
    if user_selected_chars:
        # 模式1: 基于用户选择
        # 将用户选择的字与适合字组合
        names = _generate_from_selected(user_selected_chars, suitable_chars, bazi_analysis, count)
    else:
        # 模式2: 自动组合
        # 从适合字列表中智能组合
        names = _generate_auto(suitable_chars, bazi_analysis, count)
    
    # 为每个名字添加简要分析
    for name in names:
        name["brief_analysis"] = _generate_brief_analysis(name, bazi_analysis)
    
    return names
4.5 平仄分析Tool (0.5天)
文件: src/bazi_calculator/tools/naming/pingze_analysis.py
4.6 笔画分析Tool (0.5天)
文件: src/bazi_calculator/tools/naming/stroke_analysis.py
4.7 三才五格Tool (0.5天)
文件: src/bazi_calculator/tools/naming/sangcai_wuge.py
4.8 综合凶吉分析Tool (1天)
文件: src/bazi_calculator/tools/naming/comprehensive_analysis.py
---
阶段5: 交互式Agent (2-3天)
5.1 交互式Agent (2天)
文件: src/bazi_calculator/chains/interactive_agent.py
功能:
- 完整交互流程
- 支持批量取名 ⭐ 新增
- 支持多次选择分析
工作流程:
1. 计算八字
2. 显示八字结果
3. 询问是否需要取名
4. 生成适合字列表（每个五行25个）
5. 询问是否批量取名 ⭐ **新增**
   - 如果是：
     a. 询问用户是否选择心仪字
     b. 批量生成20-30个名字
     c. 显示简要分析
   - 如果否：
     a. 生成10个精选名字
     b. 显示详细分析
6. 用户选择心仪名字
7. 详细分析选中的名字
8. 询问是否继续分析其他名字（循环）
关键方法:
class InteractiveBaziNamingAgent:
    def calculate_bazi(self, time_description: str, gender: str) -> Dict
    
    def ask_batch_naming(self) -> bool  # ⭐ 新增
    
    def ask_user_selection(self) -> List[str]  # ⭐ 新增：询问用户选择心仪字
    
    def generate_batch_names(
        self, 
        user_selected_chars: List[str] = None,
        count: int = 30
    ) -> Dict  # ⭐ 新增
    
    def generate_name_suggestions(self, count: int = 10) -> Dict
    
    def display_batch_names(self, names: List[Dict]) -> None  # ⭐ 新增
    
    def display_name_suggestions(self) -> None
    
    def user_select_name(self) -> Optional[str]
    
    def analyze_selected_name(self, name: str) -> Dict
    
    def display_analysis(self, analysis: Dict) -> None
    
    def ask_continue_analysis(self) -> bool
    
    def run_interactive_session(self) -> None
批量取名交互流程 ⭐ 新增:
def run_interactive_session(self):
    # ... 前面的八字计算和适合字生成 ...
    
    # 询问是否批量取名
    if self.ask_batch_naming():
        # 询问用户是否选择心仪字
        user_chars = self.ask_user_selection()
        
        # 批量生成
        batch_result = self.generate_batch_names(user_chars, count=30)
        
        # 显示批量结果
        self.display_batch_names(batch_result["names"])
        
        # 用户可以从批量结果中选择名字进行详细分析
        # ...
    else:
        # 标准流程：生成10个精选名字
        # ...
5.2 命令行入口 (1天)
文件: src/main.py
---
阶段6: 测试和优化 (2-3天)
测试文件结构
tests/
├── core/
│   ├── test_ganzhi.py
│   ├── test_jieqi.py
│   ├── test_calendar.py
│   └── test_wuxing.py
├── tools/
│   ├── test_bazi_tools.py
│   ├── test_naming_tools.py
│   └── test_batch_naming.py  # ⭐ 新增
├── chains/
│   ├── test_bazi_agent.py
│   └── test_interactive_agent.py
└── integration/
    ├── test_full_workflow.py
    ├── test_batch_workflow.py  # ⭐ 新增
    └── test_user_scenarios.py
测试策略
1. 单元测试：每个核心函数
2. 集成测试：模块协同
3. 准确性测试：对比权威软件
4. 性能测试：< 2秒响应
5. 边界测试：节气、子时等
---
阶段7: 部署和文档 (1天)
任务
- [ ] 编写README.md
- [ ] 编写API参考文档
- [ ] 编写用户指南
- [ ] 代码格式化（black, isort）
- [ ] 类型检查（mypy）
- [ ] Lint检查（ruff）
---
四、TODO清单
Phase 1: 核心功能开发 (当前)
- [ ] 阶段0: 项目初始化 (0.5天)
  - [ ] 创建目录结构
  - [ ] 配置依赖
  - [ ] 初始化Git
  - [ ] 编写AGENTS.md (已完成)
- [ ] 阶段1: 核心算法模块 (2-3天)
  - [ ] Ganzhi模块
  - [ ] Jieqi模块
  - [ ] Calendar模块
  - [ ] Wuxing模块
  - [ ] 核心模块单元测试
- [ ] 阶段2: 八字计算Tools (2-3天)
  - [ ] 时间解析Tool
  - [ ] 四柱计算Tools
  - [ ] 五行分析Tool
  - [ ] 八字Agent
  - [ ] 八字模块测试
- [ ] 阶段3: 字库数据生成 (2-3天)
  - [ ] 字库生成Tool
  - [ ] 康熙字典笔画
  - [ ] 生肖规则
  - [ ] 平仄声调
  - [ ] 字库查询
- [ ] 阶段4: 取名分析Tools (2-3天)
  - [ ] 八字取名分析Tool
  - [ ] 适合字查询Tool
  - [ ] 名字生成Tool
  - [ ] 批量取名Tool ⭐
  - [ ] 平仄分析Tool
  - [ ] 笔画分析Tool
  - [ ] 三才五格Tool
  - [ ] 综合凶吉分析Tool
- [ ] 阶段5: 交互式Agent (2-3天)
  - [ ] 交互式Agent主体
  - [ ] 批量取名功能 ⭐
  - [ ] 多次选择分析功能
  - [ ] 命令行入口
- [ ] 阶段6: 测试和优化 (2-3天)
  - [ ] 单元测试
  - [ ] 集成测试
  - [ ] 准确性验证
  - [ ] 性能优化
- [ ] 阶段7: 部署和文档 (1天)
  - [ ] README.md
  - [ ] API文档
  - [ ] 用户指南
  - [ ] 代码规范检查
---
Phase 2: Web应用开发 (后续)
- [ ] 后端: FastAPI实现
  - [ ] 设计RESTful API
  - [ ] API接口:
    - POST /api/bazi/calculate - 计算八字
    - POST /api/naming/generate - 生成名字建议
    - POST /api/naming/batch - 批量取名 ⭐
    - POST /api/naming/analyze - 详细分析名字
    - GET /api/library/chars - 获取适合字列表
    - POST /api/library/suitable - 查询适合字
  - [ ] 请求/响应模型定义
  - [ ] 错误处理
  - [ ] API文档（Swagger）
  - [ ] CORS配置
  - [ ] 速率限制
  - [ ] 日志记录
  - [ ] 部署配置
- [ ] 前端: Vite + TypeScript实现
  - [ ] 项目初始化（Vite + React + TypeScript）
  - [ ] UI框架选择
  - [ ] 页面设计:
    - 八字计算页面
    - 取名建议页面
    - 名字分析页面
    - 批量取名页面 ⭐
    - 字库浏览页面
  - [ ] 组件开发:
    - 时间输入组件
    - 八字结果展示组件
    - 名字卡片组件
    - 适合字选择组件
    - 分析报告组件
    - 批量结果展示组件 ⭐
  - [ ] 状态管理
  - [ ] API调用封装
  - [ ] 响应式设计
  - [ ] 用户体验优化
  - [ ] Loading状态
  - [ ] 错误处理
  - [ ] 打包和部署
- [ ] 部署和运维
  - [ ] 容器化（Docker）
  - [ ] CI/CD配置
  - [ ] 服务器部署
  - [ ] 监控和日志
  - [ ] 备份策略
---
Phase 3: 性能优化和持久化 (后续)
- [ ] 数据库集成
  - [ ] 数据库选型
  - [ ] 数据库设计:
    - 字库表（chars）
    - 康熙笔画表（strokes）
    - 生肖规则表（zodiac_rules）
    - 平仄数据表（pingze_data）
    - 历史记录表（history）- 可选
  - [ ] ORM集成（SQLAlchemy）
  - [ ] 数据迁移脚本
  - [ ] 从JSON/文件迁移到数据库
  - [ ] 数据库查询优化
  - [ ] 缓存策略
- [ ] LLM资源优化
  - [ ] 字库缓存（避免重复调用LLM）
  - [ ] 名字生成结果缓存
  - [ ] 批量查询优化
  - [ ] 异步调用
  - [ ] Prompt优化（减少Token消耗）
  - [ ] 模型版本管理
- [ ] 性能优化
  - [ ] 数据库索引优化
  - [ ] API响应时间优化
  - [ ] 前端加载优化
  - [ ] CDN部署
  - [ ] 负载均衡
---
Phase 4: 功能扩展 (后续)
- [ ] 增强功能
  - [ ] 多语言支持（繁体、英文）
  - [ ] 多时区支持
  - [ ] 批量导入用户数据
  - [ ] 导出报告（PDF）
  - [ ] 分享功能
  - [ ] 收藏夹
  - [ ] 历史记录
  - [ ] 用户账户系统
- [ ] 高级分析
  - [ ] 大运流年推算
  - [ ] 十神分析
  - [ ] 神煞分析
  - [ ] 格局分析
  - [ ] 用神变格分析
- [ ] 社交功能
  - [ ] 用户社区
  - [ ] 名字评分排行
  - [ ] 专家点评
  - [ ] 取名日记
---
五、技术细节
5.1 批量取名功能详细设计 ⭐ 新增
功能流程
1. 用户看到适合字列表完美！我将为您创建一个完整的开发计划文档，包含批量取名功能设计和To-Do事项。让我先检查当前目录结构，然后规划文档内容。
# 检查当前目录结构
$ ls -la
total 16
drwxr-xr-x 1 MiniHan 197121    0 Jan 22 03:59 .
drwxr-xr-x 1 MiniHan 197121    0 Jan 22 03:57 ..
drwxr-xr-x 1 MiniHan 197121    0 Jan 22 03:57 .venv
-rw-r--r-- 1 MiniHan 197121 5412 Jan 22 04:02 AGENTS.md
Thinking: 好的，目录中只有AGENTS.md和.venv。现在我需要规划创建一个完整的开发计划和TODO文档。
基于用户的需求：
1. 批量取名：如果用户选择心仪的字，基于用户选择；如果没有选择，则生成可能的组合
2. 批量数量：20-30个
3. 批量分析：简要分析
4. To-Do：单独创建一个文档，包含开发计划和TODO
我需要创建一个文档文件，包含：
- 完整的开发计划
- 批量取名功能的详细设计
- To-Do事项（包括后续的Web前端、数据库等）
让我规划文档结构。
→ Read AGENTS.md 
Thinking: 好的，我已经了解了AGENTS.md的内容。现在我需要创建一个完整的开发计划和TODO文档。
根据用户的需求，文档应该包含：
1. 完整的开发计划（包括批量取名功能）
2. To-Do事项（包括后续的Web前端、数据库等）
让我创建一个名为 DEVELOPMENT_PLAN.md 的文档。