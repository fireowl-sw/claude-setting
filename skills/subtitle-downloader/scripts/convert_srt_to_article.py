#!/usr/bin/env python3
"""
Convert SRT subtitle file to readable article format.
Removes timestamps and merges text into paragraphs.
"""
import re
import sys
from pathlib import Path


def parse_srt(srt_path):
    """Parse SRT file and return list of (start_time, end_time, text) tuples"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    subtitles = []
    for start, end, text in matches:
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = text.replace('\n', ' ')  # Merge lines
        text = ' '.join(text.split())  # Normalize whitespace
        subtitles.append((start, end, text))

    return subtitles


def merge_to_paragraphs(subtitles, sentences_per_paragraph=5):
    """Merge subtitles into paragraphs"""
    paragraphs = []
    current_para = []

    for i, (start, end, text) in enumerate(subtitles):
        current_para.append(text)

        # Split into paragraphs
        if len(current_para) >= sentences_per_paragraph:
            paragraphs.append(' '.join(current_para))
            current_para = []

    # Add remaining
    if current_para:
        paragraphs.append(' '.join(current_para))

    return paragraphs


def generate_article(srt_path, output_path):
    """Generate readable article from SRT"""
    subtitles = parse_srt(srt_path)
    paragraphs = merge_to_paragraphs(subtitles)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 视频字幕文章\n\n")
        f.write(f"**来源字幕**: {srt_path.name}\n\n")
        f.write("---\n\n")

        for i, para in enumerate(paragraphs, 1):
            f.write(f"{para}\n\n")

    print(f"✅ Article generated: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert_srt_to_article.py <input.srt> <output.md>")
        sys.exit(1)

    srt_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not srt_path.exists():
        print(f"❌ SRT file not found: {srt_path}")
        sys.exit(1)

    generate_article(srt_path, output_path)


if __name__ == '__main__':
    main()
