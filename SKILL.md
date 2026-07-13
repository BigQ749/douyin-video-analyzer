---
name: douyin-video-analyzer
description: "抖音视频解析与AI总结。自动提取抖音/TikTok视频文字稿并生成结构化摘要。基于 Playwright 浏览器自动化 + faster-whisper 语音转写，无需第三方付费 API。支持 Codex / Claude Code / OpenCode。"
args: "<douyin_url | local_video_path> - 抖音分享链接或本地视频文件路径"
---

# 抖音视频解析与 AI 总结

## 概述

自动解析抖音/TikTok 视频，提取完整文字稿并生成 AI 摘要。无需第三方付费解析 API，通过 Playwright 浏览器自动化获取视频源地址，ffmpeg 提取音频，faster-whisper 转写。

## 前置依赖

```bash
pip install faster-whisper playwright pyyaml
python -m playwright install chromium
# ffmpeg: macOS brew install ffmpeg / Ubuntu sudo apt install ffmpeg / Windows 手动下载
# GPU 加速(可选): pip install nvidia-cublas-cu12
```

## 获取 cookies

```bash
# 推荐: 使用 douyin-downloader 的 cookie_fetcher
python -m tools.cookie_fetcher --config config.yml
# 扫码登录后 cookies 自动保存
```

## 执行流程

### Step 1 - 获取视频地址
Playwright 加载页面提取 `<video>` 源地址：
```bash
python scripts/extract_douyin.py "https://v.douyin.com/xxxx/" --cookies config.yml
```

### Step 2 - 提取音频
ffmpeg 拉取音频流，不下载视频：
```bash
ffmpeg -headers "Referer: https://www.douyin.com/" -i <VIDEO_URL> -vn -ab 128k -y audio.mp3
```

### Step 3 - 转写
```python
from faster_whisper import WhisperModel
model = WhisperModel('tiny', device='cuda', compute_type='float16')  # GPU
segments, _ = model.transcribe('audio.mp3', language='zh')
text = '\n'.join(s.text.strip() for s in segments if s.text.strip())
```

### Step 4 - AI 总结
读取文字稿后生成结构化摘要（标题 + 摘要 + 要点）。

### Step 5 - 清理
删除临时音频，仅保留文字稿。

## 性能参考

| 视频时长 | GPU (GTX 1650) | CPU int8 |
|---------|----------------|----------|
| 2 分钟 | ~1 秒 | ~6 秒 |
| 10 分钟 | ~5 秒 | ~50 秒 |
| 40 分钟 | ~20 秒 | ~3 分钟 |

## 多平台安装

```bash
# Codex
mkdir -p ~/.codex/skills && cp -r douyin-video-analyzer ~/.codex/skills/

# Claude Code
mkdir -p ~/.claude/skills && cp -r douyin-video-analyzer ~/.claude/skills/

# OpenCode
cp -r douyin-video-analyzer <project>/.agents/skills/
```

## 与类似方案对比

| 特性 | 本方案 | imlewc 方案 |
|------|--------|------------|
| 视频获取 | Playwright 自动化（免费） | AI Douyin API（付费）|
| GPU | ✅ 支持 | ✅ 支持 |
| 平台 | Codex + Claude + OpenCode | Codex + Claude |
| 离线 | ✅ 完全离线 | ⚠️ 需 API |
