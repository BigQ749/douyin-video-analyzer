---
name: douyin-video-analyzer
description: "抖音视频解析与AI总结 — 自动提取文字稿并生成结构化摘要。覆盖完整工作流：从需求分析、工具开发、到开源发布。支持 Codex / Claude Code / OpenCode。"
args: "<douyin_url | local_video_path> - 抖音分享链接或本地视频/音频文件路径"
---

# 抖音视频解析与 AI 总结

## 总览

本项目是 **端到端开源项目实战** 的完整案例，覆盖：

| 阶段 | 内容 | 对应文档 |
|------|------|---------|
| **需求分析** | 用户需要什么、同类方案调研 | 本 Skill |
| **工具开发** | Playwright + ffmpeg + faster-whisper 流程实现 | `scripts/extract_douyin.py` |
| **文档编写** | README / LICENSE / .gitignore / FAQ | `README.md` |
| **开源发布** | 清理敏感信息 → Git 提交 → 推送到 GitHub | `workflows/publish-to-github.md` |

---

## 第一部分：抖音视频解析工具

### 概述

自动解析抖音/TikTok 视频，提取完整文字稿并生成 AI 摘要。无需第三方付费 API。

### 前置依赖

```bash
pip install faster-whisper playwright pyyaml
python -m playwright install chromium
# ffmpeg: macOS brew install ffmpeg / Windows 从 ffmpeg.org 下载
# GPU(可选): pip install nvidia-cublas-cu12
pip install nvidia-cublas-cu12
```

### 获取 cookies

```bash
# 使用 douyin-downloader 的 cookie_fetcher
python -m tools.cookie_fetcher --config config.yml
# 浏览器扫码登录 → 回车 → cookies 自动保存
```

### 核心流程

```
抖音链接 → Playwright 注入cookies → 提取视频地址 → ffmpeg 拉音频(不下载视频)
  → faster-whisper GPU转写 → AI结构化摘要 → 自动删除临时文件
```

### 命令行使用

```bash
python scripts/extract_douyin.py "https://v.douyin.com/xxxx/" --cookies config.yml
```

### 性能

| 视频时长 | GPU (GTX 1650) | CPU |
|---------|----------------|-----|
| 2 分钟 | ~1秒 | ~6秒 |
| 40 分钟 | ~20秒 | ~3分钟 |

---

## 第二部分：开源发布工作流

> 完整文档见 `workflows/publish-to-github.md`

### 核心理念

**不要直接把工作目录上传 GitHub。** 应该拆出干净的开源目录，只放需要公开的代码和文档。

### 七步流程

```
① 建干净目录 → ② 复制必要源码 → ③ 写 README/.gitignore/LICENSE
  → ④ 扫描敏感信息 → ⑤ git init → ⑥ 创建 GitHub 仓库 → ⑦ 推送
```

### 关键原则

#### 1. 只复制必要文件

```
✅ 源码 (.py/.js/.ts 等)
✅ 配置文件模板 (.env.example)
✅ 文档 (README, LICENSE)
✅ 构建脚本 (Dockerfile, requirements.txt)
❌ 日志 (*.log)
❌ 历史数据 (*.json, *.csv, *.db)
❌ 凭据 (auth.json, .env, token)
❌ 临时文件 (*.tmp, *.lnk)
```

#### 2. 敏感信息扫描（提交前必须执行）

```bash
# 扫描关键词
rg -n --hidden -i "access_token|refresh_token|bearer|password|secret|auth\.json|\.env" .

# 检查目录是否有不该提交的文件
ls -la
```

#### 3. README 必须包含隐私说明

尤其是涉及账号读取的工具，必须写清楚：

- 读取什么数据
- **不上传**什么数据
- 会不会消耗 API 额度
- 是不是官方工具

示例：

```markdown
## 隐私说明

- 不会将 token 写入仓库
- 不会上传你的个人数据
- 不会调用模型
- 不是抖音官方工具
```

#### 4. 许可证选择

小工具默认 **MIT License**：允许免费使用、修改、分发，保留版权声明。

#### 5. Git 提交

```bash
git init
git config user.name "你的用户名"
git config user.email "你的用户名@users.noreply.github.com"
git add .
git commit -m "init: 项目简短描述"

git branch -M main
git remote add origin https://github.com/用户名/仓库名.git
git push -u origin main
```

#### 6. 首次推送冲突处理

如果 GitHub 仓库已存在文件（比如自动生成的 README），需要用 `--force`：

```bash
git push -u origin main --force
```

#### 7. 推送后检查

- README 正常显示中文
- 没有上传日志/凭据/个人数据
- 文件列表干净
- 默认分支是 main

---

## 本次实战记录

| 项目 | 地址 |
|------|------|
| 抖音视频解析工具 | https://github.com/BigQ749/douyin-video-analyzer |

### 遇到的典型问题

1. **`gh` CLI 认证超时** → 改用 Personal Access Token 推送
2. **仓库名已存在** → 直接推送到已创建的仓库（`--force`）
3. **Windows PATH 刷新问题** → 新装 `gh` 后用全路径调用
4. **CRLF 换行符警告** → Git 自动处理，不影响功能

---

## 给 AI 的直接提示词

### 场景一：处理抖音视频

```
请帮我总结这个抖音视频：https://v.douyin.com/xxxx/
```

### 场景二：将本地项目开源

```
请把当前目录下的小工具整理成开源 GitHub 仓库。

要求：
1. 新建干净目录，只复制必要源码
2. 写 README.md（含隐私说明）、.gitignore、MIT LICENSE
3. 提交前扫描 token、auth.json、.env、日志
4. 初始化 Git，本地提交
5. 等我给你仓库地址后推送到 main
```
