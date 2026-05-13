# yt-dlp Subtitle Extraction Reference

Quick reference for extracting subtitles using yt-dlp.

## Common Commands

### List Available Subtitles

```bash
yt-dlp --list-subs "<video_url>"
```

### Download Specific Subtitle Language

```bash
yt-dlp --write-subs --sub-lang "zh-Hans,en" --convert-subs srt --skip-download "<video_url>"
```

### Download All Subtitles

```bash
yt-dlp --write-subs --write-auto-subs --convert-subs srt --skip-download "<video_url>"
```

### With Browser Cookies (for Premium Content)

```bash
yt-dlp --cookies-from-browser chrome --write-subs --sub-lang "ai-zh" --convert-subs srt --skip-download "<video_url>"
```

### Specify Output Filename

```bash
yt-dlp --write-subs --sub-lang "zh-Hans" --convert-subs srt --skip-download -o "subtitles/%(id)s.%(ext)s" "<video_url>"
```

## Platform-Specific Notes

### Bilibili

- Language codes: `ai-zh` (AI Chinese), `ai-en` (AI English), `zh-Hans` (Simplified Chinese)
- AI-generated subtitles are usually available
- May need browser cookies for some videos

### YouTube

- Auto-generated language codes: `en`, `zh-Hans`, `zh-Hant`
- Manual subtitles: varies by video
- `--write-auto-subs` for auto-generated

### Other Platforms

Check available subtitles first with `--list-subs`.

## Subtitle Language Codes

Common codes:
- `zh-Hans`: Simplified Chinese
- `zh-Hant`: Traditional Chinese
- `en`: English
- `ai-zh`: Bilibili AI Chinese
- `ai-en`: Bilibili AI English
