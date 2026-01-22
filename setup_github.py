#!/usr/bin/env python3
"""GitHub仓库设置助手"""

import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("GitHub仓库设置助手")
print("=" * 60)

print("""
当前状态：
✓ Git仓库已初始化
✓ .gitignore文件已创建
✓ 所有文件已添加到Git
✓ 初始提交已创建

【需要您手动完成的步骤】

步骤1：创建GitHub仓库

1. 访问 https://github.com
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息：
   Repository name: langchain-bazi-agent
   Description: 基于 LangChain 1.2.6 的智能八字计算和取名 Agent
   Public: [√] (建议勾选，公开仓库)
   Add a README file: [ ] (不勾选，我们已有README.md)
5. 点击 "Create repository"

步骤2：获取仓库地址

创建后，GitHub会显示仓库地址，格式为：
https://github.com/你的用户名/langchain-bazi-agent.git

或者使用SSH地址：
git@github.com:你的用户名/langchain-bazi-agent.git

步骤3：添加远程仓库

使用以下命令之一（替换 YOUR_USERNAME）：

【方法1：HTTPS】
git remote add origin https://github.com/YOUR_USERNAME/langchain-bazi-agent.git

【方法2：SSH】
git remote add origin git@github.com:YOUR_USERNAME/langchain-bazi-agent.git

步骤4：推送到GitHub

git branch -M main
git push -u origin main

如果需要认证：
- HTTPS方式：会提示输入GitHub用户名和密码
- 推荐使用Personal Access Token（不要使用密码）
- SSH方式：需要配置SSH密钥

【获取Personal Access Token】

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 填写token信息：
   Note: langchain-bazi-agent-push
   Expiration: No expiration 或选择有效期
   Select scopes: 勾选 [√] repo 和 [√] workflow
4. 点击 "Generate token"
5. 复制token（只显示一次！）

【验证推送成功】

推送成功后，你会看到类似输出：
Enumerating objects: 71, done.
Counting objects: 100% (71/71), done.
Delta compression using up to 8 threads
Compressing objects: 100% (71/71), done.
Writing objects: 100% (71/71), done.
Total 71 (delta 0), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (71/71), done.
To https://github.com/YOUR_USERNAME/langchain-bazi-agent.git
   * [new branch]      main -> main

【验证仓库内容】

1. 访问你的GitHub仓库页面
2. 检查文件列表是否正确
3. 检查README.md是否正确显示
4. 检查commit历史

【后续工作】

推送成功后，你可以：
1. 在GitHub上查看和编辑文件
2. 创建Issue和Pull Requests
3. 设置分支保护（Branch protection）
4. 添加Topics和Description
5. 管理Releases版本

【分支策略建议】

main分支: 稳定版本
  - 用于生产环境
  - 需要代码审查
  - 通过PR合并

develop分支: 开发版本
  - 用于日常开发
  - 可直接推送
  - 定期合并到main

feature分支: 功能开发
  - 从develop创建
  - 开发完成后合并回develop

【常见问题】

Q: 推送失败，提示认证错误？
A:
  1. 检查用户名是否正确
  2. 检查token是否有效
  3. 确认token权限包含repo
  4. 尝试使用SSH方式

Q: 推送很慢？
A:
  1. 首次推送可能较慢
  2. 检查网络连接
  3. 考虑使用压缩传输

Q: 文件太多，推送失败？
A:
  1. 检查.gitignore是否正确
  2. 考虑分批提交
  3. 使用Git LFS（如果需要）

【快速命令参考】

# 查看当前状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 查看分支
git branch -a

# 拉取最新更改
git pull origin main

# 推送新更改
git add .
git commit -m "Update: xxx"
git push origin main

【项目信息】

项目名称: langchain-bazi-agent
项目类型: Python项目
主语言: Python
许可证: MIT
标签: langchain, bazi, chinese-astrology, llm

【文档】

- README.md - 项目总览
- AGENTS.md - 开发指南
- PLAN.md - 开发计划
- BAZI_ALGORITHM_FIX.md - 算法修复详解
- DEVELOPMENT_HISTORY.md - 开发历程
- DOCS_GUIDE.md - 文档说明
- GITHUB_SETUP.md - GitHub仓库创建指南（本文件）

【技术支持】

GitHub文档: https://docs.github.com/
Git文档: https://git-scm.com/docs

【下一步】

1. 在GitHub创建新仓库
2. 添加远程仓库地址
3. 推送代码到GitHub
4. 验证仓库内容
5. 开始后续开发工作

""")

print("=" * 60)
print("准备就绪！")
print("=" * 60)
print("\n请按照上述步骤操作，创建GitHub仓库并推送代码。")
print("如有问题，请查看GitHub文档或寻求帮助。")