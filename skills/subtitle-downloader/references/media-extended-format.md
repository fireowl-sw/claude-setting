# Media Extended Timestamp Format Reference

Quick reference for creating clickable timestamp links compatible with Obsidian Media Extended plugin.

## Link Format

### Basic Syntax

```markdown
[timestamp](video_url?t=seconds#t=display_time)
```

### Components

- `timestamp`: Display text (e.g., `1:30`, `45:20`)
- `video_url`: Full video URL
- `seconds`: Time in seconds (integer)
- `display_time`: Formatted time for display

### Examples

#### YouTube

```markdown
[1:30](https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=90#t=1:30)
```

#### Bilibili

```markdown
[17:00](https://www.bilibili.com/video/BV1T21PBqErg/?t=1020#t=17:00)
```

#### Local Video

```markdown
[5:30](./videos/lecture.mp4#t=330)
```

## Time Conversion

### Seconds to Timestamp Format

```python
def format_timestamp(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"  # H:MM:SS
    return f"{m}:{s:02d}"  # MM:SS
```

### Timestamp to Seconds

```python
def parse_timestamp(timestamp: str) -> int:
    parts = timestamp.split(':')
    if len(parts) == 3:  # H:MM:SS
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + int(s)
    elif len(parts) == 2:  # MM:SS
        m, s = parts
        return int(m) * 60 + int(s)
    return 0
```

## Usage in Markdown

### Single Timestamp

```markdown
Jump to [1:30](https://example.com/video?t=90#t=1:30) for the explanation.
```

### Time Range

```markdown
**Time**: [1:30](url?t=90#t=1:30) - [2:45](url?t=165#t=2:45)
```

### Timestamp List

```markdown
## Topics Covered

- Introduction: [0:00](video?t=0#t=0:00)
- Main concept: [1:30](video?t=90#t=1:30)
- Examples: [5:45](video?t=345#t=5:45)
- Summary: [10:20](video?t=620#t=10:20)
```

## Integration with Obsidian

### Prerequisites

1. Install [Media Extended](https://github.com/aidenlx/media-extended) plugin
2. Enable timestamp links in plugin settings

### Best Practices

1. Use consistent timestamp format
2. Include both start and end times for segments
3. Keep display time human-readable
4. Test links after generation

### Example Segment

```markdown
## 5. Tokenization Explained

**⏱️ Time**: [5:30](https://www.bilibili.com/video/BV1xxx?t=330#t=5:30) - [7:15](https://www.bilibili.com/video/BV1xxx?t=435#t=7:15)

**📝 Content**:

Tokenization breaks text into smaller units called tokens. These tokens are the basic building blocks that language models process...

---
```
