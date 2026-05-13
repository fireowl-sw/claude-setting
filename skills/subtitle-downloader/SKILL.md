---
name: subtitle-downloader
description: Download and process video subtitles from multiple platforms (Bilibili, YouTube, etc.) without downloading the video itself. Use when user wants to extract subtitles from a video URL, convert subtitles to readable article format, create Media Extended compatible timestamp links, or organize subtitles by content topics with question-based outlines. Supports SRT extraction, markdown conversion, and Obsidian-friendly output formats.
---

# Subtitle Downloader

## Overview

Extract video subtitles from popular platforms (Bilibili, YouTube, and 1000+ supported sites) without downloading the video itself. Convert subtitles into multiple Obsidian-friendly formats: readable articles, Media Extended timestamp links, and question-based outlines organized by content topics.

**Core capabilities**:
- Download subtitles using yt-dlp (preserves timestamps, supports auto/manual subtitles)
- Convert SRT to readable markdown article
- Generate Media Extended format with clickable timestamp links
- Create question-based outlines organized by semantic content

**When to use this skill**:
- User provides a video URL and wants the transcript/subtitles
- User wants to create video notes with timestamp navigation
- User wants to convert video content into readable markdown
- User mentions "subtitle", "caption", "transcript", "timestamp", or "Media Extended"

## Workflow

### Step 1: Check Dependencies

Verify yt-dlp is installed:

```bash
python3 -m yt_dlp --version
```

If not found, install with:

```bash
pip install yt-dlp
```

**Optional** - Install from browser for premium content (Bilibili, YouTube):
```bash
# For Chrome
pip install browser-cookie3
```

### Step 2: List Available Subtitles

Before downloading, check what subtitle languages are available:

```bash
python3 ~/.claude/skills/subtitle-downloader/scripts/download_subtitle.py "<video_url>" --list
```

Or use yt-dlp directly:

```bash
python3 -m yt_dlp --list-subs --cookies-from-browser chrome "<video_url>"
```

**Common language codes**:
- Bilibili: `ai-zh` (AI Chinese), `ai-en` (AI English), `zh-Hans` (Simplified Chinese)
- YouTube: `en`, `zh-Hans`, `zh-Hant` (auto/manual varies)

### Step 3: Download Subtitle

Use the download script:

```bash
python3 ~/.claude/skills/subtitle-downloader/scripts/download_subtitle.py \
  "<video_url>" \
  "<output_directory>" \
  "<language_code>"
```

**Example**:

```bash
# Download Bilibili AI Chinese subtitle
python3 ~/.claude/skills/subtitle-downloader/scripts/download_subtitle.py \
  "https://www.bilibili.com/video/BV1T21PBqErg" \
  "./subs" \
  "ai-zh"
```

The script will:
1. Check dependencies
2. List available subtitles
3. Download the specified language as SRT file
4. Save to output directory

**Output**: `subs/<video_id>.<lang>.srt`

### Step 4: Convert to Desired Format

Choose from three output formats based on user needs:

#### Option A: Readable Article Format

Convert SRT to continuous text without timestamps:

```bash
python3 ~/.claude/skills/subtitle-downloader/scripts/convert_srt_to_article.py \
  "<input.srt>" \
  "<output.md>"
```

**Output**: Clean markdown article suitable for reading

**Use case**: User wants a readable transcript, not concerned about timestamps

#### Option B: Media Extended Format (Recommended)

Generate clickable timestamp links compatible with Media Extended plugin:

```bash
python3 ~/.claude/skills/subtitle-downloader/scripts/generate_media_extended.py \
  "<input.srt>" \
  "<output.md>" \
  "<video_url>"
```

**Output**: Markdown with clickable timestamps like `[1:30](video_url?t=90#t=1:30)`

**Use case**: User wants to watch video while reading transcript, jump to specific times

**Example output**:

```markdown
## 5. Topic Name

**⏱️ Time**: [1:30](video?t=90#t=1:30) - [2:45](video?t=165#t=2:45)

**📝 Content**:

Full paragraph content merged from multiple subtitle entries...
```

#### Option C: Question-Based Outline (Advanced)

Organize subtitles by semantic topics, merge same questions across the video:

```bash
python3 ~/.claude/skills/subtitle-downloader/scripts/generate_question_outline.py \
  "<input.srt>" \
  "<output.md>" \
  "<video_url>"
```

**Output**: Question-driven outline where each topic becomes a question

**Use case**: User wants organized notes, video study guide, or searchable content

**Example output**:

```markdown
## 为什么要学习语言模型？

### Discussion 1
**⏱️ Time**: [2:29](video?t=149#t=2:29) - [2:51](video?t=171#t=2:51)

**📝 Content**:

Researchers are becoming disconnected from the underlying technology...

### Discussion 2
**⏱️ Time**: [15:30](video?t=930#t=15:30) - [16:45](video?t=1005#t=16:45)

**📝 Content**:

Eight years ago, researchers would implement their own models...
```

### Step 5: Verify Output

Check generated files:

```bash
ls -lh <output_directory>
```

For Media Extended format, verify links work in Obsidian:
1. Open the markdown file in Obsidian
2. Ensure Media Extended plugin is installed
3. Click a timestamp link
4. Should jump to that position in the video

## Platform-Specific Notes

### Bilibili

- **Subtitle sources**: AI-generated (recommended), manual user uploads
- **Language codes**:
  - `ai-zh`: AI Chinese (most reliable)
  - `ai-en`: AI English
  - `zh-Hans`: Manual simplified Chinese
- **Authentication**: May need `--cookies-from-browser chrome` for some videos
- **URL formats supported**:
  - `https://www.bilibili.com/video/BV1xxx`
  - `https://b23.tv/xxx` (short links)

### YouTube

- **Subtitle sources**: Auto-generated (available for most videos), manual uploads
- **Language codes**: Use `--list-subs` to see available options
- **Quality**: Auto-generated English is generally good; other languages vary
- **Authentication**: Generally not required for public videos

### Other Platforms

yt-dlp supports 1000+ sites. Check compatibility:

```bash
python3 -m yt_dlp --list-subs "<video_url>"
```

## Troubleshooting

### No Subtitles Found

**Problem**: `--list-subs` shows no subtitles

**Solutions**:
1. Try with browser cookies: `--cookies-from-browser chrome`
2. Check if video actually has subtitles (watch the video with CC enabled)
3. Try different language code
4. Some platforms don't expose subtitles via API

### Download Fails

**Problem**: Download script returns error

**Solutions**:
1. Check yt-dlp version: `python3 -m yt_dlp --version` (update if old)
2. Verify internet connection
3. Try without cookies first, then with cookies
4. Check if video is private/restricted

### Encoding Issues

**Problem**: SRT file shows garbled characters

**Solution**: Ensure file is saved as UTF-8. Scripts handle this automatically, but if manual editing:
```bash
file -I <subtitle.srt>  # Should show charset=utf-8
```

### Media Extended Links Not Working

**Problem**: Clicking timestamps doesn't jump in video

**Solutions**:
1. Ensure Media Extended plugin is installed and enabled
2. Check plugin settings: Enable "Timestamp" and "Embed" features
3. Verify video URL format is correct
4. Try local video path if online URL has issues

## Advanced Usage

### Batch Processing Multiple Videos

Process entire playlist or course:

```bash
# Download all subtitles from playlist
python3 -m yt_dlp --write-subs --sub-lang "ai-zh" --convert-subs srt \
  --skip-download --cookies-from-browser chrome \
  -o "subs/%(playlist_index)s-%(title)s.%(ext)s" \
  "<playlist_url>"

# Convert all SRT files in directory
for srt in subs/*.srt; do
  python3 ~/.claude/skills/subtitle-downloader/scripts/generate_question_outline.py \
    "$srt" "${srt%.srt}_outline.md" \
    "https://www.bilibili.com/video/BV1xxx"
done
```

### Custom Output Formatting

Modify scripts to customize:
- Paragraph merging threshold (sentences per segment)
- Topic detection keywords
- Timestamp display format
- Markdown styling

See individual scripts for configuration variables.

### Integration with Obsidian Workflows

1. **Video notes template**: Create daily note with video URL and subtitle file
2. **Knowledge extraction**: Use question-based outline as basis for Anki cards
3. **Searchable transcript**: Combine with Obsidian search for video content
4. **Timestamped notes**: Take notes while watching, use Media Extended links

## Resources

### scripts/

- `download_subtitle.py` - Download subtitles from video URL (no video download)
- `convert_srt_to_article.py` - Convert SRT to readable markdown article
- `generate_media_extended.py` - Generate Media Extended format with clickable timestamps
- `generate_question_outline.py` - Create question-based outline organized by topics

### references/

- `yt-dlp-guide.md` - Quick reference for yt-dlp subtitle extraction commands
- `media-extended-format.md` - Media Extended timestamp format documentation

## Quick Start Example

Complete workflow for Bilibili video:

```bash
# 1. Download Chinese subtitle
python3 ~/.claude/skills/subtitle-downloader/scripts/download_subtitle.py \
  "https://www.bilibili.com/video/BV1T21PBqErg" \
  "./output" \
  "ai-zh"

# 2. Convert to question-based outline with timestamps
python3 ~/.claude/skills/subtitle-downloader/scripts/generate_question_outline.py \
  "./output/BV1T21PBqErg.ai-zh.srt" \
  "./output/CS336_P01_Notes.md" \
  "https://www.bilibili.com/video/BV1T21PBqErg"

# 3. Open in Obsidian
# File: output/CS336_P01_Notes.md
# Click any timestamp to jump to that position in video
```

**Result**: Organized video notes with 30-50 topic questions, each with clickable timestamps and full content.
