# Git 学习笔记：面向 AI 工程项目管理

> 来源：`Git讲义.pdf`。本笔记不是逐页抄写讲义，而是按照你当前的学习路线整理成“能直接放进项目仓库使用”的版本。

---

## 0. 我为什么要学 Git？

Git 的核心作用不是“上传代码”，而是：

1. **备份代码**：防止本地文件误删或电脑故障。
2. **版本回退**：代码写坏了可以回到之前的状态。
3. **协同开发**：多人可以同时开发，最后合并代码。
4. **追踪责任**：知道每一行代码是谁在什么时候修改的。

一句话：

> Git = 代码项目的时间机器 + 协作系统。

---

## 1. Git 的基本概念

### 1.1 版本控制

版本控制就是记录文件的变化历史。

常见版本控制工具：

- SVN / CVS：集中式版本控制。
- Git：分布式版本控制。

### 1.2 集中式 vs 分布式

| 类型 | 特点 | 代表 |
|---|---|---|
| 集中式 | 中央服务器保存完整版本库，本地依赖服务器 | SVN |
| 分布式 | 每个人本地都有完整版本库，可离线提交 | Git |

Git 虽然经常配合 GitHub 使用，但 GitHub 不是 Git 的核心。  
GitHub 只是远程代码托管平台，方便多人共享代码。

---

## 2. Git 的三个区域

Git 最重要的三个区域：

```text
工作区 workspace
    ↓ git add
暂存区 index / staging area
    ↓ git commit
本地仓库 repository
    ↓ git push
远程仓库 remote repository
```

### 2.1 工作区

你正在编辑的项目文件夹。

例如：

```text
ai-engineering-practice/
  README.md
  00_python_basic/
  04_rag_project/
```

### 2.2 暂存区

你通过 `git add` 暂时放入待提交队列的修改。

### 2.3 本地仓库

你通过 `git commit` 保存到本地历史记录的版本。

### 2.4 远程仓库

GitHub / Gitee / GitLab 上的仓库。

---

## 3. Git 工作流

日常最常用流程：

```bash
git status
git add .
git commit -m "说明本次修改"
git push
```

完整理解：

```text
修改文件
  ↓
git status 查看状态
  ↓
git add . 加入暂存区
  ↓
git commit -m "message" 提交到本地仓库
  ↓
git push 推送到 GitHub
```

从远程更新代码：

```bash
git pull
```

---

## 4. 初始化和配置

### 4.1 配置用户名和邮箱

```bash
git config --global user.name "your_name"
git config --global user.email "your_email@example.com"
```

查看配置：

```bash
git config --global user.name
git config --global user.email
```

### 4.2 初始化本地仓库

在项目目录下：

```bash
git init
```

初始化后，项目目录中会生成隐藏目录：

```text
.git/
```

这个目录就是 Git 版本库的核心，不要随便删除。

---

## 5. 常用命令

### 5.1 查看状态

```bash
git status
```

用途：

- 查看哪些文件被修改；
- 查看哪些文件已经暂存；
- 查看哪些文件还没有被 Git 跟踪。

---

### 5.2 添加到暂存区

添加全部修改：

```bash
git add .
```

添加单个文件：

```bash
git add README.md
```

---

### 5.3 提交到本地仓库

```bash
git commit -m "add project structure"
```

提交信息建议写清楚：

```bash
git commit -m "add file organizer project"
git commit -m "fix csv export bug"
git commit -m "update git learning notes"
```

不要写：

```bash
git commit -m "111"
git commit -m "update"
git commit -m "test"
```

---

### 5.4 查看提交日志

普通日志：

```bash
git log
```

简洁日志：

```bash
git log --pretty=oneline --all --graph --abbrev-commit
```

可以配置别名：

```bash
alias git-log='git log --pretty=oneline --all --graph --abbrev-commit'
```

---

### 5.5 查看远程仓库

```bash
git remote -v
```

你当前仓库应该看到类似：

```text
origin  git@github.com:runliujiawei-create/ai-engineering-practice.git (fetch)
origin  git@github.com:runliujiawei-create/ai-engineering-practice.git (push)
```

---

### 5.6 推送到远程仓库

第一次推送：

```bash
git push -u origin main
```

之后推送：

```bash
git push
```

---

### 5.7 拉取远程更新

```bash
git pull
```

如果多人协作，建议每天开始写代码前先：

```bash
git pull
```

---

## 6. .gitignore

`.gitignore` 用来告诉 Git：哪些文件不要上传。

AI 项目中尤其重要，因为不能上传：

- 虚拟环境；
- API Key；
- 数据集；
- 模型权重；
- 训练输出；
- 日志文件。

推荐 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environments
.venv/
venv/
env/
.conda/

# Secrets
.env
.env.*
*.key

# Logs
*.log
logs/

# Data and outputs
data/
datasets/
outputs/
runs/
checkpoints/
models/
weights/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 7. 分支 branch

### 7.1 分支是什么？

分支就是从主线代码中拉出一条独立开发线。

用途：

- 开发新功能；
- 修复 bug；
- 做实验；
- 避免直接污染主分支。

### 7.2 查看分支

```bash
git branch
```

### 7.3 创建分支

```bash
git branch dev
```

### 7.4 切换分支

```bash
git checkout dev
```

或者：

```bash
git switch dev
```

### 7.5 创建并切换分支

```bash
git checkout -b feature/file-organizer
```

或者：

```bash
git switch -c feature/file-organizer
```

### 7.6 合并分支

先切回主分支：

```bash
git checkout main
```

合并：

```bash
git merge feature/file-organizer
```

### 7.7 删除分支

```bash
git branch -d feature/file-organizer
```

强制删除：

```bash
git branch -D feature/file-organizer
```

---

## 8. 常见分支命名

| 分支 | 用途 |
|---|---|
| `main` | 主分支，保存稳定代码 |
| `develop` | 开发分支 |
| `feature/xxx` | 新功能分支 |
| `hotfix/xxx` | 紧急修复分支 |
| `test` | 测试分支 |

你当前个人学习项目可以简单使用：

```text
main
feature/python-file-organizer
feature/rag-project
feature/agent-project
```

---

## 9. 冲突 conflict

### 9.1 冲突什么时候发生？

当两个人或两个分支修改了同一个文件的同一行，合并时可能产生冲突。

### 9.2 冲突文件长什么样？

```text
<<<<<<< HEAD
这是当前分支的内容
=======
这是要合并进来的分支内容
>>>>>>> feature/xxx
```

### 9.3 解决冲突流程

1. 打开冲突文件；
2. 手动保留正确内容；
3. 删除 `<<<<<<<`、`=======`、`>>>>>>>` 标记；
4. 重新添加并提交：

```bash
git add .
git commit -m "resolve merge conflict"
git push
```

---

## 10. SSH 远程仓库

你已经配置了 SSH。  
你的远程仓库地址是：

```text
git@github.com:runliujiawei-create/ai-engineering-practice.git
```

### 10.1 添加远程仓库

```bash
git remote add origin git@github.com:runliujiawei-create/ai-engineering-practice.git
```

### 10.2 修改远程仓库地址

如果 origin 已经存在：

```bash
git remote set-url origin git@github.com:runliujiawei-create/ai-engineering-practice.git
```

### 10.3 检查 SSH 是否成功

```bash
ssh -T git@github.com
```

成功时会看到类似：

```text
Hi runliujiawei-create! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 11. 你当前项目的推荐工作方式

你的项目目录：

```text
ai-engineering-practice/
  00_python_basic/
  01_algorithm_practice/
  02_git_linux_notes/
  03_ai_chat_backend/
  04_rag_project/
  05_agent_project/
  notes/
  README.md
  .gitignore
```

### 每天开始学习前

```bash
cd ~/Desktop/ai-engineering-practice
git pull
git status
```

### 写完代码或笔记后

```bash
git status
git add .
git commit -m "update git notes"
git push
```

### 新开一个项目功能时

```bash
git checkout -b feature/file-organizer
```

做完后：

```bash
git add .
git commit -m "add file organizer"
git checkout main
git merge feature/file-organizer
git push
```

---

## 12. Git 学习中的几条铁令

1. **切换分支前先提交本地修改。**
2. **每天写代码都要 commit。**
3. **不要把 API Key、模型权重、数据集上传到 GitHub。**
4. **遇到冲突不要删整个项目目录。**
5. **不确定之前先执行 `git status`。**
6. **仓库里不要放虚拟环境。**
7. **每个项目都要写 README。**

---

## 13. 最小日常命令表

| 场景 | 命令 |
|---|---|
| 查看状态 | `git status` |
| 添加全部修改 | `git add .` |
| 提交 | `git commit -m "message"` |
| 推送 | `git push` |
| 拉取 | `git pull` |
| 查看日志 | `git log --oneline --graph --all` |
| 查看远程仓库 | `git remote -v` |
| 查看分支 | `git branch` |
| 创建并切换分支 | `git checkout -b feature/name` |
| 合并分支 | `git merge feature/name` |

---

## 14. 你下一步要做什么？

1. 把本笔记保存到：

```text
02_git_linux_notes/git_notes.md
```

2. 提交到 GitHub：

```bash
git add .
git commit -m "add git learning notes"
git push
```

3. 后续你每学一个 Git 知识点，就更新这个笔记。

---

## 15. 当前你必须掌握的 Git 能力

短期找实习前，你只需要先掌握：

```text
git init
git status
git add
git commit
git log
git remote
git push
git pull
git branch
git checkout / switch
git merge
.gitignore
README
```

暂时不用深挖：

```text
rebase
cherry-pick
submodule
Git internals
复杂多人协作流
```

---

## 16. 你现在的标准工作流

最终你每天就按这个走：

```bash
cd ~/Desktop/ai-engineering-practice

git pull

# 写代码 / 写笔记

git status
git add .
git commit -m "describe what you changed"
git push
```

这就是你当前阶段最重要的 Git 实战能力。
