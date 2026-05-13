#!/usr/bin/env python3
"""
Download video subtitles from Bilibili, YouTube, and other platforms using yt-dlp.
Does NOT download the video itself, only the subtitles.
"""
import sys
import subprocess
import json
import re
from pathlib import Path


def check_dependencies():
    """Check if yt-dlp is installed"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ yt-dlp version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass

    # Try python3 -m yt_dlp
    try:
        result = subprocess.run(
            ['python3', '-m', 'yt_dlp', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ yt-dlp (via python3) version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass

    print("❌ yt-dlp not found. Install with: pip install yt-dlp")
    return False


def list_subtitles(video_url, use_cookies=True):
    """List available subtitle languages for the video"""
    cmd = ['python3', '-m', 'yt_dlp', '--list-subs']

    if use_cookies:
        cmd.extend(['--cookies-from-browser', 'chrome'])

    cmd.append(video_url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print(result.stdout)
    return result.stdout


def download_subtitle(video_url, output_dir, lang='ai-zh', use_cookies=True):
    """
    Download subtitle from video URL

    Args:
        video_url: URL of the video
        output_dir: Directory to save subtitle
        lang: Subtitle language code (default: ai-zh for AI Chinese)
        use_cookies: Whether to use browser cookies for authentication

    Returns:
        Path to downloaded SRT file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        'python3', '-m', 'yt_dlp',
        '--write-subs',
        '--sub-lang', lang,
        '--convert-subs', 'srt',
        '--skip-download',
        '-o', str(output_dir / '%(id)s.%(ext)s')
    ]

    if use_cookies:
        cmd.extend(['--cookies-from-browser', 'chrome'])

    cmd.append(video_url)

    print(f"Downloading subtitle with language: {lang}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"❌ Error downloading subtitle: {result.stderr}")
        return None

    # Find the downloaded SRT file
    srt_files = list(output_dir.glob('*.srt'))
    if srt_files:
        print(f"✅ Subtitle downloaded: {srt_files[0]}")
        return srt_files[0]

    print("❌ No SRT file found")
    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 download_subtitle.py <video_url> <output_dir> [lang]")
        print("\nExample:")
        print('  python3 download_subtitle.py "https://www.bilibili.com/video/BV1xxx" ./subs ai-zh')
        sys.exit(1)

    video_url = sys.argv[1]
    output_dir = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else 'ai-zh'

    if not check_dependencies():
        sys.exit(1)

    print(f"\n📥 Video URL: {video_url}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🌐 Language: {lang}\n")

    # First, list available subtitles
    print("Available subtitles:")
    list_subtitles(video_url)

    print("\n" + "="*60)
    srt_path = download_subtitle(video_url, output_dir, lang)

    if srt_path:
        print(f"\n✅ Success! Subtitle saved to: {srt_path}")
    else:
        print(f"\n❌ Failed to download subtitle")
        sys.exit(1)


if __name__ == '__main__':
    main()
