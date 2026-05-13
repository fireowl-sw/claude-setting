#!/usr/bin/env python3
"""
Generate Media Extended compatible format from SRT subtitles.
Creates clickable timestamp links that work with Media Extended plugin.
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple


def parse_srt(srt_path: Path) -> List[Tuple[str, str, str]]:
    """Parse SRT file and return list of (start_time, end_time, text) tuples"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match SRT entries
    pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\n\d+\n|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    subtitles = []
    for start, end, text in matches:
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = text.replace('\n', ' ')  # Merge lines
        text = ' '.join(text.split())  # Normalize whitespace
        subtitles.append((start, end, text))

    return subtitles


def time_to_seconds(time_str: str) -> int:
    """Convert SRT timestamp to seconds"""
    h, m, s = time_str.split(':')
    s, ms = s.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s)


def format_timestamp(seconds: int) -> str:
    """Format seconds to MM:SS or H:MM:SS"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def generate_media_extended_link(video_url: str, seconds: int, display_time: str) -> str:
    """Generate Media Extended clickable link"""
    return f"[{display_time}]({video_url}?t={seconds}#t={display_time})"


def detect_topic_change(text1: str, text2: str) -> bool:
    """Detect if topic changes between two subtitle entries"""
    # Simple heuristic: if both are very short, might be same topic
    # This is a placeholder - more sophisticated NLP could be used
    keywords_change = ['首先', '然后', '接下来', '另外', '此外', '但是', '不过']
    return any(kw in text2 for kw in keywords_change)


def merge_subtitles_by_topic(subtitles: List[Tuple[str, str, str]], min_sentences: int = 3) -> List[dict]:
    """Merge subtitles into topic-based segments"""
    segments = []
    current_segment = []

    for start, end, text in subtitles:
        current_segment.append((start, end, text))

        # Check if we should split
        if len(current_segment) >= min_sentences:
            # Check for topic change indicators
            if len(current_segment) > min_sentences * 2:
                segments.append(list(current_segment))
                current_segment = []
            elif detect_topic_change('', text):
                segments.append(list(current_segment))
                current_segment = []

    # Add remaining
    if current_segment:
        segments.append(current_segment)

    return segments


def generate_media_extended_markdown(srt_path: Path, output_path: Path, video_url: str):
    """Generate Media Extended format markdown"""
    subtitles = parse_srt(srt_path)
    segments = merge_subtitles_by_topic(subtitles)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 视频字幕 - Media Extended 格式\n\n")
        f.write(f"**视频链接**: [{video_url}]({video_url})\n\n")
        f.write(f"**来源字幕**: `{srt_path.name}`\n\n")
        f.write("---\n\n")

        for i, segment in enumerate(segments, 1):
            if not segment:
                continue

            # Get time range
            start_time = segment[0][0]
            end_time = segment[-1][1]

            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)

            start_display = format_timestamp(start_seconds)
            end_display = format_timestamp(end_seconds)

            # Generate clickable timestamp links
            start_link = generate_media_extended_link(video_url, start_seconds, start_display)
            end_link = generate_media_extended_link(video_url, end_seconds, end_display)

            # Merge text content
            content = ' '.join([text for _, _, text in segment])

            # Write segment
            f.write(f"## {i}. 段落\n\n")
            f.write(f"**⏱️ 时间**: {start_link} - {end_link}\n\n")
            f.write(f"**📝 内容**:\n\n{content}\n\n")
            f.write("---\n\n")

    print(f"✅ Media Extended format generated: {output_path}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 generate_media_extended.py <input.srt> <output.md> <video_url>")
        print("\nExample:")
        print('  python3 generate_media_extended.py subtitle.srt output.md "https://www.bilibili.com/video/BV1xxx"')
        sys.exit(1)

    srt_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    video_url = sys.argv[3]

    if not srt_path.exists():
        print(f"❌ SRT file not found: {srt_path}")
        sys.exit(1)

    generate_media_extended_markdown(srt_path, output_path, video_url)


if __name__ == '__main__':
    main()
