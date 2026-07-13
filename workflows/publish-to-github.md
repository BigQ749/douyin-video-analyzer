# 开源发布工作流：将本地工具发布到 GitHub

> 本文档是 `douyin-video-analyzer` 的开源发布工作流，也适用于任何本地小工具。

---

## 📋 目录

- [核心理念](#-核心理念)
- [完整流程（七步）](#-完整流程七步)
- [敏感信息检查清单](#-敏感信息检查清单)
- [README 内容规范](#-readme-内容规范)
- [常见问题](#-常见问题)
- [实战记录：抖音视频解析工具](#-实战记录抖音视频解析工具)

---

## 🎯 核心理念

### 不要直接上传工作目录

原始工作目录里经常混有：

```
❌ 临时脚本         ❌ 日志文件          ❌ 个人数据
❌ 调试文件         ❌ 大模型文件         ❌ 凭据配置
❌ 其他项目文件      ❌ 截图缓存           ❌ 环境变量
```

**正确做法**：拆出干净的开源目录，只放真正需要公开的文件。

### 开源不是"把文件夹丢上去"

一个好的开源仓库应该让陌生人能在 30 秒内理解：

| 问题 | 答案应该在… |
|------|-----------|
| 这是什么？ | README 第一段 |
| 能解决什么问题？ | README 概述 |
| 怎么安装？ | README 安装步骤 |
| 怎么用？ | README 使用教程 |
| 有没有隐私风险？ | README 隐私说明 |
| 用的是什么协议？ | LICENSE 文件 |
| 哪些文件是无关的？ | .gitignore |

---

## 📦 完整流程（七步）

### 第一步：建干净目录

```bash
mkdir <project-name>
```

### 第二步：复制必要源码

```bash
# ✅ 复制这些
Copy-Item src/ <project-name>/src/ -Recurse
Copy-Item requirements.txt <project-name>/
Copy-Item Dockerfile <project-name>/

# ❌ 不要复制这些
# auth.json, .env, *.log, *.csv, *.db, config.yml（含私人信息）
```

### 第三步：写三个核心文件

#### 3.1 README.md

结构模板见下方 [README 内容规范](#-readme-内容规范)。

#### 3.2 .gitignore

```gitignore
# 凭据
.env
auth.json
config.yml
*.token

# 日志
*.log
*.csv
*.db

# 运行时生成
__pycache__/
node_modules/
.venv/
venv/

# 临时文件
*.tmp
*.lnk
Thumbs.db
.DS_Store
```

#### 3.3 LICENSE

小工具默认 **MIT License**：

```text
MIT License

Copyright (c) 2026 <你的名字>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

### 第四步：扫描敏感信息（提交前必须做）

```bash
# 1. 关键词扫描
rg -n --hidden -i "access_token|refresh_token|bearer|password|secret|auth\.json|\.env|api_key" .

# 2. 检查文件列表
Get-ChildItem -Recurse -Force | Select-Object FullName
```

确认没有：

```
❌ .env 文件
❌ auth.json 或任何含真实 token 的文件
❌ 日志文件（*.log）
❌ 历史数据（*.csv, *.json-db 等）
❌ 配置文件（含真实密码/密钥的）
❌ 个人截图
❌ 临时文件
```

### 第五步：初始化 Git

```bash
cd <project-name>
git init
git config user.name "你的 GitHub 用户名"
git config user.email "你的用户名@users.noreply.github.com"
git add .
git commit -m "init: 项目简短说明"
```

提交信息写法建议：

```
init: 抖音视频解析与AI总结

- 支持 Codex / Claude Code / OpenCode 三平台
- Playwright 浏览器自动化获取视频源地址
- faster-whisper GPU/CPU 转写
- 无需第三方付费 API

Constraint: No tokens, logs, or config committed.
```

### 第六步：创建 GitHub 仓库

在 GitHub 网站上：

1. 点右上角 `+` → `New repository`
2. 仓库名填项目名（与本地目录同名）
3. 选 `Public`
4. **不要勾** "Add a README"（本地已有）
5. **不要勾** ".gitignore"（本地已有）
6. **不要勾** "License"（本地已有）

### 第七步：推送

```bash
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

如果遇到冲突（仓库已有文件）：

```bash
git push -u origin main --force
```

如果遇到认证问题：

```bash
# 方案 A：使用 GitHub CLI
gh auth login

# 方案 B：使用 Personal Access Token
# 1. 去 https://github.com/settings/tokens 生成 token
# 2. 勾选 repo 权限
git remote set-url origin https://YOUR_TOKEN@github.com/用户名/仓库名.git
git push -u origin main
```

---

## 🔍 敏感信息检查清单

提交前逐项确认：

- [ ] `.env` 已排除
- [ ] `auth.json` 已排除
- [ ] 无 `api_key` / `password` / `secret` 等关键词在代码中硬编码
- [ ] 日志文件已排除
- [ ] 数据库文件已排除
- [ ] 配置文件模板用 `.example` 后缀（如 `config.example.yml`）
- [ ] `.gitignore` 已覆盖所有不需要的文件类型

---

## 📝 README 内容规范

### 必需内容

| 章节 | 说明 |
|------|------|
| 项目名称 + 一句话简介 | 第一屏就要让人看懂 |
| 效果展示 | 输入/输出示例，让人知道能干什么 |
| 原理 | 一张图或几句话讲清楚是怎么工作的 |
| 环境要求 | 操作系统、Python 版本、内存等 |
| 安装步骤 | 分步，每一步都要能复制粘贴执行 |
| 使用教程 | 命令示例 + 参数说明 |
| FAQ | 常见问题（折叠式，不占空间） |
| 隐私说明 | **涉及账号的工具必须写** |
| 许可证 | MIT / Apache 2.0 等 |

### 隐私说明写法

```markdown
## 隐私说明

- 本工具需要你的抖音登录 cookies 来获取视频源地址
- cookies 仅用于向抖音发送请求，**不会上传到任何第三方服务器**
- 所有处理在本地完成，**不会调用任何外部 API**
- 临时音频文件在处理完成后**自动删除**
- 本工具**不是抖音官方产品**
```

---

## ❓ 常见问题

### Q：推送时提示 "remote contains work that you do not have locally"

**原因**：GitHub 仓库已经有了文件（如自动生成的 README）。

**解决**：
```bash
git push -u origin main --force
```

### Q：`gh auth login` 超时或连不上

**原因**：网络环境问题。

**解决**：改用 Personal Access Token（在 GitHub 设置页面生成）。

### Q：Windows 上 `gh` 命令找不到

**原因**：安装后未重启终端，PATH 未刷新。

**解决**：
```bash
# 用全路径
& "C:\Program Files\GitHub CLI\gh.exe" repo create xxx

# 或者重启终端
```

### Q：CRLF 换行符警告

**原因**：Windows 和 Linux 换行符差异。

**解决**：不影响功能，可忽略。或设置：
```bash
git config core.autocrlf true
```

### Q：README 中文显示乱码

**原因**：GitHub 使用 UTF-8 编码，文件需保存为 UTF-8。

**解决**：确认文件编码为 UTF-8（不带 BOM）。

---

## 📊 实战记录：抖音视频解析工具

### 项目信息

| 项目 | 内容 |
|------|------|
| 名称 | douyin-video-analyzer |
| 地址 | https://github.com/BigQ749/douyin-video-analyzer |
| 许可证 | MIT |
| 技术栈 | Python + Playwright + ffmpeg + faster-whisper |

### 发布过程

| 步骤 | 操作 | 遇到的问题 |
|------|------|-----------|
| ① 建目录 | `mkdir douyin-video-analyzer` | - |
| ② 复制源码 | 复制 extract_douyin.py 等 | - |
| ③ 写文档 | README / .gitignore / LICENSE | - |
| ④ 扫描 | rg 扫描关键词 | 无敏感信息 |
| ⑤ git init | `git init && git add && git commit` | 需要先设置 user.name/email |
| ⑥ 创建仓库 | GitHub 网页创建 | - |
| ⑦ 推送 | `git push -u origin main` | 仓库已存在文件 → 改用 `--force` |

### 关键经验

1. **先建 GitHub 空仓库，再本地初始化**，可以避免首次推送冲突
2. **Personal Access Token 比 `gh auth login` 更稳定**，适合自动化场景
3. **README 一定要有隐私说明**，尤其是涉及用户数据的工具
4. **`.gitignore` 在第一次 commit 之前就要写好**，避免把敏感文件提交上去再删除（会留在 git 历史里）

---

## 💣 实战坑记录（来自真实翻车经历）

以下是我在发布 `douyin-video-analyzer` 时实际踩过的坑，理论流程里不会告诉你这些。

### 坑 1：`gh` CLI 装完找不到

```
gh : 无法将"gh"识别为 cmdlet
```

**原因**：`winget install GitHub.cli` 安装后，新开终端才刷新 PATH。当前会话找不到。

**对比理论流程**：理论只说"安装 gh"，没说安装完后怎么调用。

**实战解法**：

```powershell
# 方案 A：用全路径（推荐，不依赖 PATH）
& "C:\Program Files\GitHub CLI\gh.exe" repo create xxx

# 方案 B：临时加到 PATH
$env:PATH = "C:\Program Files\GitHub CLI;$env:PATH"
gh repo create xxx
```

### 坑 2：`gh auth login --web` 超时死锁

```
failed to authenticate via web browser: Post "https://github.com/login/device/code": EOF
```

**原因**：`gh auth login --web` 需要打开浏览器让用户确认 + 输入的设备码。

当在非交互式终端（如 OpenCode 的后台）运行时，命令卡住等待输入 → 超时被 kill。

**理论流程没覆盖的点**：

- gh 认证需要**用户主动参与**（打开链接 + 输入验证码）
- AI agent 无法代劳，必须引导用户操作
- 超时后认证状态不保存，下次还得重来

**实战解法**：

```powershell
# 改用 Personal Access Token（不需要交互）
$env:GH_TOKEN = "ghp_xxxxxxxxxxxx"
```

Token 生成步骤：https://github.com/settings/tokens → Generate new token → 勾选 `repo`

### 坑 3：Token 推送到远程仓库 URL 中的安全隐患

```powershell
git remote add origin https://oauth2:$GH_TOKEN@github.com/用户名/仓库名.git
```

**问题**：Token 直接暴露在 `git remote -v` 和 shell 历史里。

**理论流程没覆盖的点**：Token 和密码一样，暴露后别人可以操控你的 GitHub。

**实战解法**：推送成功后立即清除历史：

```powershell
# 1. 推送后改回不带 token 的 URL
git remote set-url origin https://github.com/用户名/仓库名.git

# 2. 清除 PowerShell 历史
Clear-History

# 3. 注销环境变量
Remove-Item Env:GH_TOKEN
```

### 坑 4：仓库已存在导致的首次推送失败

```
HTTP 422: Repository creation failed.
name already exists on this account
```

**原因**：用户提前在网页上创建了同名仓库（带了 README），`gh repo create` 冲突了。

**理论流程**：假设仓库不存在，可以自由创建。但实际可能是用户先建好了。

**实战解法**：

```powershell
# 不创建了，直接推送到已有仓库
git remote add origin https://github.com/用户名/仓库名.git
git push -u origin main --force
```

`--force` 会用本地文件覆盖远程已有内容。**前提是确认远程仓库里没有你想保留的修改。**

### 坑 5：Windows Git 换行符警告

```
warning: in the working copy of 'README.md', LF will be replaced by CRLF
```

**原因**：Windows 用 CRLF（`\r\n`），Linux/macOS 用 LF（`\n`）。Git 自作聪明帮你转换。

**影响**：不影响功能。但新手看到满屏 warning 会慌。

**实战解法**：

```powershell
# 让 Git 自动转换（推荐 Windows 用户）
git config core.autocrlf true

# 或者关掉警告（不转换，保持原样）
git config core.autocrlf false
```

### 坑 6：`git commit` 前必须设置身份

```
Author identity unknown
*** Please tell me who you are.
```

**原因**：Git 需要知道谁提交的。新环境首次使用必须配置。

**理论流程**：只写了 `git commit`，没写前置条件。

**实战解法**：

```powershell
git config user.email "你的用户名@users.noreply.github.com"
git config user.name "你的 GitHub 用户名"
```

推荐用 `users.noreply.github.com` 邮箱，避免暴露真实邮箱。

### 坑汇总对比

| 序号 | 理论流程 | 实战实际发生的 | 谁对 |
|------|---------|---------------|------|
| 1 | `gh repo create` | 仓库已存在，报 422 | 实战 |
| 2 | `gh auth login` | 非交互环境超时死锁 | 实战 |
| 3 | 安装 gh CLI | 装完后命令找不到 | 实战 |
| 4 | `git commit -m "xxx"` | 必须先设 user.name/email | 实战 |
| 5 | 正常推送 | 远程已有文件，被拒绝 | 实战 |
| 6 | Token 正常使用 | Token 留存在远程 URL 中 | 实战 |
| 7 | - | CRLF 换行符警告 | 理论没提 |
| 8 | - | `--force` 推送覆盖风险 | 理论没提 |
