<p align="center">
  <img src="https://img.shields.io/badge/Codex-ready-1f425f?logo=visualstudiocode" alt="Codex">
  <img src="https://img.shields.io/badge/Claude%20Code-ready-1f425f?logo=anthropic" alt="Claude Code">
  <img src="https://img.shields.io/badge/OpenCode-ready-1f425f" alt="OpenCode">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="Python">
</p>

<h1 align="center">🎬 Douyin Video Analyzer</h1>
<p align="center">
  <strong>抖音/TikTok 视频一键提取文字稿 + AI 结构化总结</strong><br>
  支持 <b>Codex · Claude Code · OpenCode</b> 三大 AI 编程平台<br>
  🚫 无需第三方付费 API  |  ⚡ GPU 加速  |  🔒 完全离线
</p>

---

## 📋 目录

- [概述](#-概述)
- [效果展示](#-效果展示)
- [原理](#-原理)
- [环境要求](#-环境要求)
- [安装教程](#-安装教程)
- [获取抖音 Cookies](#-获取抖音-cookies)
- [使用教程](#-使用教程)
- [多平台配置](#-多平台配置)
- [性能参考](#-性能参考)
- [项目结构](#-项目结构)
- [常见问题](#-常见问题)
- [与同类方案对比](#-与同类方案对比)
- [许可证](#-许可证)

---

## 🎯 概述

**Douyin Video Analyzer** 是一个 AI 编程助手 Skill，能够：

1. 接收一条抖音/TikTok 分享链接
2. **自动提取**视频中的完整语音文字稿
3. **生成 AI 结构化摘要**（核心观点 + 要点提炼）

整个过程**不需要注册任何第三方 API**，不依赖 AI Douyin、TikHub 等付费服务。只需要你的抖音账号扫码登录一次即可。

### 适用人群

- 🎥 内容创作者 — 批量分析对标视频的文案和结构
- 📊 运营人员 — 快速理解竞品视频的核心卖点
- 🤖 AI 开发者 — 搭建自己的视频数据处理管道
- 🧑‍🎓 普通用户 — 长视频不想看完整，直接看摘要

---

## ✨ 效果展示

### 输入

```
https://v.douyin.com/xxxxx/
```

### 输出

```markdown
## 视频分析结果

### 视频信息
| 项目 | 内容 |
|------|------|
| 原标题 | 刚装上codex，一定要做好两件事，让ai越用越聪明 |
| 来源 | 抖音 |
| 时长 | 约 2 分钟 |
| 话题 | #codex #ai #人工智能 |

### AI摘要

视频教刚装上 Codex 的用户如何通过两个关键步骤让 AI 越用越聪明。
第一步是让 Codex 扫描整台电脑，列出 10 个可以提效的工作场景；
第二步是创建专用的工作目录，并在其中建立复盘日志和架构规范文档。

### 核心要点

1. 建立专属工作目录，所有项目集中管理
2. 全局复盘踩坑日志，让 AI 自己记录和改进
3. 架构规范文档，约束 AI 的输出行为
4. 项目隔离，避免上下文混乱
```

---

## 🔬 原理

```
┌──────────────┐    ┌────────────────┐    ┌────────────┐    ┌───────────────┐
│  抖音分享链接   │ → │ Playwright 浏览器  │ → │  ffmpeg     │ → │ faster-whisper  │
│              │    │ 注入 cookies    │    │  拉音频流    │    │  GPU 转写      │
│  v.douyin.com │    │ 提取视频源地址   │    │  不下载视频   │    │  20-40 秒/40分  │
└──────────────┘    └────────────────┘    └────────────┘    └───────┬───────┘
                                                                    │
                                                                    ▼
┌──────────────┐    ┌────────────────┐    ┌──────────────────────────┐
│  AI 结构化总结 │ ← │  完整文字稿      │ ← │  临时音频自动删除          │
│  标题+摘要+要点 │    │  dy_transcript.txt │    │  仅保留文字稿 ✅            │
└──────────────┘    └────────────────┘    └──────────────────────────┘
```

### 为什么不需要第三方 API？

大多数类似工具依赖 **AI Douyin** 或 **TikHub** 等付费解析服务来获取视频下载地址。
本工具使用 **Playwright**（浏览器自动化框架）直接加载抖音页面，利用你已登录的 cookies，
从页面中提取视频源文件地址。整个过程不调用任何第三方 API，完全免费。

---

## 💻 环境要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.9+ | 运行环境 |
| 操作系统 | Windows / macOS / Linux | 全平台支持 |
| 内存 | 4GB+（推荐 8GB） | CPU 模式 2GB+ 可运行 |
| 磁盘 | 2GB 可用空间 | 存放 whisper 模型文件 |
| NVIDIA GPU | GTX 1060+（可选） | 开启 GPU 加速，速度快 8-10 倍 |

---

## 📦 安装教程

> ⏱ 预计耗时：15-30 分钟（主要取决于网络速度）

### 第一步：克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/douyin-video-analyzer.git
cd douyin-video-analyzer
```

### 第二步：安装 Python 依赖

```bash
pip install faster-whisper playwright pyyaml
```

<details>
<summary><b>🐍 什么是 pip？点我展开</b></summary>

`pip` 是 Python 的包管理器。如果提示 `pip 不是内部或外部命令`，
说明你没有安装 Python。请前往 https://www.python.org/downloads/ 下载安装，
安装时勾选 "Add Python to PATH"。
</details>

### 第三步：安装 Playwright 浏览器

```bash
python -m playwright install chromium
```

这步会下载约 300MB 的 Chromium 浏览器，用于自动化加载抖音页面。

### 第四步：安装 ffmpeg

<details>
<summary><b>点击展开各系统的 ffmpeg 安装方法</b></summary>

**Windows：**
1. 打开 https://ffmpeg.org/download.html
2. 点击 "Windows" → "Windows builds from gyan.dev"
3. 下载 `ffmpeg-release-essentials.zip`
4. 解压，将 `bin` 文件夹加入系统 PATH

**macOS：**
```bash
brew install ffmpeg
```

**Ubuntu/Debian：**
```bash
sudo apt update && sudo apt install ffmpeg
```
</details>

验证安装：
```bash
ffmpeg -version
```

### 第五步：GPU 加速（可选但强烈推荐）

如果你有 NVIDIA 显卡，安装 CUDA 加速库，速度提升 8-10 倍：

```bash
pip install nvidia-cublas-cu12
```

> 💡 没有独立显卡也不用担心，工具会自动切换 CPU 模式，只是速度慢一些。

---

## 🔑 获取抖音 Cookies

本工具需要你的抖音登录信息来获取视频源地址。

### 方法一：使用 douyin-downloader（推荐）

```bash
# 克隆 douyin-downloader
git clone https://github.com/jiji262/douyin-downloader.git
cd douyin-downloader
pip install -r requirements.txt
cp config.example.yml config.yml

# 运行 cookie 获取工具
python -m tools.cookie_fetcher --config config.yml
```

执行后会弹出一个浏览器窗口，用手机抖音扫码登录，登录成功后按回车。
cookies 会自动写入 `config.yml` 文件。

### 方法二：手动从浏览器导出

<details>
<summary><b>📖 点击查看详细步骤</b></summary>

1. 在 Chrome 浏览器中打开 `https://www.douyin.com/` 并登录你的账号
2. 按键盘上的 **F12** 键打开开发者工具
3. 切换到 **Application** → **Cookies** → **www.douyin.com**
4. 找到以下字段，复制它们的值：

| 字段 | 说明 | 有效期 |
|------|------|--------|
| `sessionid` | 登录会话 ID | 约 60 天 |
| `ttwid` | 设备标识 | 长期 |
| `msToken` | 反爬 Token | 较短 |

5. 在项目根目录创建 `config.yml` 文件：

```yaml
cookies:
  sessionid: "粘贴你的sessionid"
  ttwid: "粘贴你的ttwid"
  msToken: "粘贴你的msToken"
```

> ⚠️ 不要将 `config.yml` 提交到 Git 仓库！`.gitignore` 已自动排除。
</details>

---

## 🚀 使用教程

### 方式一：AI 对话中使用（推荐）

在 Codex / Claude Code / OpenCode 的对话中，直接发送抖音链接：

```
https://v.douyin.com/xxxxx/
```

AI 会自动检测到链接并按照本文档的流程处理。

### 方式二：命令行直接运行

```bash
python scripts/extract_douyin.py "https://v.douyin.com/xxxx/" --cookies config.yml
```

参数说明：

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | （必填） | - | 抖音分享链接 |
| `--cookies` | `-c` | `config.yml` | cookies 配置文件路径 |
| `--output` | `-o` | `桌面/dy_transcript.txt` | 输出文件路径 |
| `--no-gpu` | - | 自动检测 | 强制使用 CPU |
| `--ffmpeg` | - | `ffmpeg` | ffmpeg 可执行文件路径 |

### 输出文件

处理完成后，桌面会自动生成 `dy_transcript.txt` 文件，包含视频的完整文字稿。

---

## 🔧 多平台配置

### Codex

```bash
mkdir -p ~/.codex/skills
cp -r douyin-video-analyzer ~/.codex/skills/douyin-video-analyzer
```

之后在 Codex 对话中发送抖音链接即可自动处理。

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -r douyin-video-analyzer ~/.claude/skills/douyin-video-analyzer
```

### OpenCode

```bash
cp -r douyin-video-analyzer <你的项目>/.agents/skills/douyin-video-analyzer
```

---

## ⚡ 性能参考

测试环境：GTX 1650 4GB / Intel i5 / Windows 11

| 视频长度 | GPU 模式 | CPU int8 模式 | 场景示例 |
|---------|----------|--------------|---------|
| 2 分钟 | ~1 秒 | ~6 秒 | 短视频/搞笑段子 |
| 8 分钟 | ~4 秒 | ~108 秒 | 短剧/综艺片段 |
| 22 分钟 | ~11 秒 | ~143 秒 | 教程/课程 |
| 40 分钟 | ~20 秒 | ~183 秒 | 电影解说/深度分析 |

---

## 📁 项目结构

```
douyin-video-analyzer/
│
├── SKILL.md                   ← 技能主文件（三平台通用）
├── README.md                  ← 本文件
├── LICENSE                    ← MIT 开源协议
├── .gitignore
│
├── scripts/
│   └── extract_douyin.py      ← 核心处理脚本（平台无关）
│
├── tests/
│   └── test_extract.py        ← 单元测试
│
└── docs/
    └── cookie-guide.md        ← 获取 Cookies 详细指南
```

---

## ❓ 常见问题

<details>
<summary><b>为什么需要 cookies？不登录不行吗？</b></summary>

抖音对视频源地址做了反爬保护，未登录状态下无法获取。cookies 只是用来证明"你是真实用户"，不会上传到任何第三方服务器。
</details>

<details>
<summary><b>sessionid 过期了怎么办？</b></summary>

`sessionid` 有效期约 60 天。过期后重新运行 cookie_fetcher 扫码登录一次即可。
</details>

<details>
<summary><b>提示 "GPU 不可用" 怎么办？</b></summary>

工具会自动回退到 CPU 模式。如果想用 GPU，请确认：
1. 你有 NVIDIA 显卡（GTX 1060+）
2. 安装了 CUDA 驱动：`nvidia-smi` 能正常输出
3. 安装了 CUDA 库：`pip install nvidia-cublas-cu12`
</details>

<details>
<summary><b>支持 B 站/小红书吗？</b></summary>

目前仅支持抖音/TikTok。B 站和小红书的适配需要在 Playwright 中添加对应的 cookies 和页面解析逻辑，未来计划支持。
</details>

<details>
<summary><b>和 imlewc/video-to-subtitle-summary 有什么区别？</b></summary>

最大的区别是**费用**。imlewc 的方案需要注册 AI Douyin 或 TikHub 并充值（按次计费），本方案通过浏览器自动化完全免费。详见下方对比表。
</details>

---

## 📊 与同类方案对比

| 特性 | **本方案** ✅ | imlewc 方案 | wendy7756 方案 |
|------|-------------|-------------|---------------|
| **视频获取** | Playwright 浏览器自动化 | AI Douyin API（付费）| yt-dlp |
| **费用** | **完全免费** 🆓 | 按次计费 | 免费 |
| **GPU 加速** | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| **适配平台** | Codex + Claude + OpenCode | Codex + Claude | Web UI |
| **离线使用** | ✅ 完全离线 | ⚠️ 需要 API Key | ✅ 完全离线 |
| **抖音支持** | ✅ 已适配 | ✅ 已适配 | ❌ 仅本地文件 |
| **安装复杂度** | ⭐⭐ 中等 | ⭐ 简单 | ⭐⭐ 中等 |

---

## 📄 许可证

[MIT License](LICENSE)

---

<p align="center">
  <sub>如果你觉得这个项目有帮助，欢迎 ⭐ Star 支持！</sub>
</p>
