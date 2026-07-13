#!/usr/bin/env python3
"""抖音视频一键提取：链接 → 文字稿 → AI 总结"""

import argparse, json, os, subprocess, sys, time, yaml
from pathlib import Path

def load_cookies(path):
    """从 YAML 配置文件加载 cookies"""
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    return cfg.get('cookies', {}) or {}

def get_video_url(douyin_url, cookies_dict):
    """Playwright 获取视频源地址"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        for name, value in cookies_dict.items():
            if value and name:
                ctx.add_cookies([{
                    'name': name, 'value': str(value),
                    'domain': '.douyin.com', 'path': '/'
                }])
        page = ctx.new_page()
        page.goto(douyin_url, timeout=30000)
        page.wait_for_timeout(5000)
        src = page.evaluate("""() => {
            const v = document.querySelector('video source') || document.querySelector('video');
            return v ? (v.src || '') : '';
        }""")
        title = page.title()
        browser.close()
    
    if not src:
        raise RuntimeError(f"无法获取视频地址: {title}")
    return src, title

def extract_audio(video_url, output_path, ffmpeg_path='ffmpeg'):
    """ffmpeg 提取音频流（不下载视频）"""
    cmd = [
        ffmpeg_path,
        '-headers', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36',
        '-headers', 'Referer: https://www.douyin.com/',
        '-i', video_url,
        '-vn',                     # 不处理视频
        '-acodec', 'libmp3lame',
        '-ab', '128k',
        '-y',                      # 覆盖
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 失败: {result.stderr[:200]}")
    return os.path.getsize(output_path)

def transcribe(audio_path, use_gpu=True):
    """faster-whisper 转写"""
    from faster_whisper import WhisperModel
    
    if use_gpu:
        try:
            model = WhisperModel('tiny', device='cuda', compute_type='float16')
        except Exception:
            model = WhisperModel('tiny', device='cpu', compute_type='int8')
            print("GPU 不可用，回退到 CPU int8")
    else:
        model = WhisperModel('tiny', device='cpu', compute_type='int8')
    
    segments, info = model.transcribe(audio_path, language='zh', beam_size=1)
    return [s.text.strip() for s in segments if s.text.strip()]

def main():
    parser = argparse.ArgumentParser(description='抖音视频提取文字稿')
    parser.add_argument('url', help='抖音分享链接')
    parser.add_argument('--cookies', '-c', default='config.yml',
                       help='cookies 配置文件路径 (默认: config.yml)')
    parser.add_argument('--output', '-o', default=None,
                       help='输出文件路径 (默认: 桌面 dy_transcript.txt)')
    parser.add_argument('--no-gpu', action='store_true',
                       help='强制使用 CPU')
    parser.add_argument('--ffmpeg', default='ffmpeg',
                       help='ffmpeg 路径')
    args = parser.parse_args()
    
    # 加载 cookies
    cookies = load_cookies(args.cookies)
    if not cookies:
        print("错误: 未找到 cookies，请先运行 cookie_fetcher 扫码登录")
        sys.exit(1)
    
    # 获取视频地址
    print(f"正在解析: {args.url}")
    video_url, title = get_video_url(args.url, cookies)
    print(f"标题: {title[:80]}")
    
    # 提取音频
    tmp_audio = os.path.join(os.environ.get('TMP', '/tmp'), 'dy_audio.mp3')
    print("正在提取音频...")
    size = extract_audio(video_url, tmp_audio, args.ffmpeg)
    print(f"音频: {size/1024:.0f}KB")
    
    # 转写
    print("正在转写（faster-whisper tiny）...")
    start = time.time()
    segments = transcribe(tmp_audio, use_gpu=not args.no_gpu)
    elapsed = time.time() - start
    print(f"转写完成: {len(segments)} 段, 耗时 {elapsed:.0f}s")
    
    # 保存文字稿
    desktop = os.path.join(Path.home(), 'Desktop')
    output = args.output or os.path.join(desktop, 'dy_transcript.txt')
    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(segments))
    print(f"文字稿: {output}")
    
    # 清理
    os.remove(tmp_audio)
    print("临时音频已删除")

if __name__ == '__main__':
    main()
