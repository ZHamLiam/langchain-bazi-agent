# GitHub仓库创建指南

## 准备工作

✅ Git仓库已初始化
✅ .gitignore文件已创建
✅ 所有文件已添加到Git
✅ 初始提交已创建

## 创建GitHub仓库步骤

### 1. 登录GitHub

访问 [GitHub](https://github.com) 并登录

### 2. 创建新仓库

1. 点击右上角的 "+" 按钮
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `langchain-bazi-agent`
   - **Description**: 基于 LangChain 1.2.6 的智能八字计算和取名 Agent
   - **Public/Private**: 选择 Public 或 Private
4. 建议勾选：
   - ✓ Add a README file
   - ✓ Add .gitignore

### 3. 不初始化README

由于我们已经有README.md文件，建议：
- **不要** 勾选 "Add a README file" 选项
- 或者创建后删除自动生成的README.md

## 推送到GitHub

### 方法1：使用HTTPS（推荐）

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/langchain-bazi-agent.git

# 推送代码
git branch -M main
git push -u origin main
```

### 方法2：使用SSH

如果已配置SSH密钥：

```bash
# 添加远程仓库
git remote add origin git@github.com:YOUR_USERNAME/langchain-bazi-agent.git

# 推送代码
git branch -M main
git push -u origin main
```

## 首次推送认证

执行推送命令后，GitHub会要求认证：
1. 输入GitHub用户名
2. 输入Personal Access Token（或密码）

如果还没有Personal Access Token：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 勾选权限：
   - ✓ repo
   - ✓ workflow
4. 生成token并复制
5. 使用token作为密码

## 推送后的验证

### 查看提交历史
```bash
git log --oneline
```

### 查看远程仓库
```bash
git remote -v
```

### 查看分支
```bash
git branch
```

## 仓库内容

### 主要文件
- `README.md` - 项目总览
- `test_bazi_agent.py` - 主测试程序
- `src/` - 源代码
- `tests/` - 测试文件

### 文档文件
- `AGENTS.md` - 开发指南
- `PLAN.md` - 开发计划
- `BAZI_ALGORITHM_FIX.md` - 算法修复详解
- `DEVELOPMENT_HISTORY.md` - 开发历程
- `DOCS_GUIDE.md` - 文档说明

## 提交信息

当前提交：
```
Initial commit: 八字智能计算系统

- 实现准确的八字四柱计算（年月日时）
- 修复月柱计算错误（节气映射和五虎遁法）
- 修复时柱计算错误（五鼠遁表数据）
- 集成LLM智能输入解析
- 提供交互式八字计算界面
- 完善文档体系和测试
```

## 分支策略

### 推荐策略
- **main分支**：稳定版本
- **develop分支**：开发版本
- **feature/xxx分支**：功能开发
- **fix/xxx分支**：bug修复

### 首次推送
```bash
# 当前在main分支
git branch -M main
git push -u origin main
```

## 后续开发

### 创建开发分支
```bash
# 创建并切换到develop分支
git checkout -b develop

# 推送到远程
git push -u origin develop
```

### 开发新功能
```bash
# 从develop创建功能分支
git checkout -b feature/new-feature

# 开发完成后
git checkout develop
git merge feature/new-feature
git push
```

### 修复bug
```bash
# 从main或develop创建修复分支
git checkout -b fix/bug-name

# 修复完成后
git checkout main
git merge fix/bug-name
git push
```

## GitHub仓库设置

### 推荐设置
1. **Branch protection**
   - 保护main分支
   - 要求PR review
   - 要求状态检查通过

2. **Topics**
   - langchain
   - bazi
   - chinese-astrology
   - llm

3. **Description模板**
   ```
   基于 LangChain 1.2.6 的智能八字计算和取名 Agent
   
   ## 功能特性
   - 准确的八字四柱计算
   - LLM智能输入解析
   - 五行分析和用神推算
   - 智能取名建议
   
   ## 技术栈
   - LangChain 1.2.6
   - Python 3.12+
   - OpenAI API / 通义千问
   ```

4. **License**
   - 选择 MIT License

5. **Visibility**
   - Public：开源项目
   - Private：私有项目

## 常见问题

### Q: 推送失败，提示认证错误？
A: 
1. 检查GitHub用户名是否正确
2. 确认Personal Access Token有效
3. 确认token权限包含repo和workflow

### Q: 推送很慢？
A: 
1. 首次推送可能较慢
2. 检查网络连接
3. 使用压缩传输：`git config --global compression 9`

### Q: 文件太大，推送失败？
A:
1. .gitignore已排除虚拟环境
2. 如果仍然太大，可以使用Git LFS
3. 检查是否意外提交了大文件

### Q: 如何删除远程仓库？
A:
1. 登录GitHub
2. 进入仓库Settings
3. 滚到最底部
4. 点击"Delete this repository"

## 仓库维护

### 定期更新
```bash
# 拉取最新更改
git pull origin main

# 推送新提交
git add .
git commit -m "Update: xxx"
git push
```

### 版本标签
```bash
# 创建标签
git tag -a v1.0.0 -m "Initial release"

# 推送标签
git push origin v1.0.0
```

### Releases管理
1. 登录GitHub仓库
2. 点击"Releases"
3. 点击"Draft a new release"
4. 选择标签，填写发布信息
5. 上传附件（如果需要）

## 总结

### 已完成的步骤
1. ✅ 初始化Git仓库
2. ✅ 创建.gitignore文件
3. ✅ 添加所有文件到Git
4. ✅ 创建初始提交

### 需要手动完成的步骤
1. 在GitHub创建新仓库
2. 添加远程仓库地址
3. 推送代码到GitHub

### 快速命令
```bash
# 1. 创建GitHub仓库后
git remote add origin https://github.com/YOUR_USERNAME/langchain-bazi-agent.git

# 2. 推送代码
git branch -M main
git push -u origin main
```

## 下一步

1. 在GitHub创建新仓库
2. 使用上面命令推送到GitHub
3. 验证仓库内容正确
4. 开始后续开发工作

需要帮助？查看GitHub文档：https://docs.github.com/