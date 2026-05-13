#!/usr/bin/env python3
"""
基于问题驱动的方式组织SRT字幕
合并相同问题的段落，使用清晰的排版格式
"""
import re
from typing import List, Dict, Tuple

def parse_time(time_str: str) -> int:
    """将SRT时间戳转换为秒数"""
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        if ',' in s:
            s = s.split(',')[0]
        return int(h) * 3600 + int(m) * 60 + int(s)
    elif len(parts) == 2:
        m, s = parts
        if ',' in s:
            s = s.split(',')[0]
        return int(m) * 60 + int(s)
    return int(time_str)

def format_time(seconds: int) -> str:
    """将秒数转换为 MM:SS 或 HH:MM:SS 格式"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h > 0:
        return f"{h}:{m}:{s:02d}"
    else:
        return f"{m}:{s:02d}"

def parse_srt(file_path: str) -> List[Dict]:
    """解析SRT文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            timestamp = lines[1]
            text = '\n'.join(lines[2:])

            match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', timestamp)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)

                subtitles.append({
                    'start': start_time,
                    'end': end_time,
                    'start_sec': parse_time(start_time.split(',')[0]),
                    'end_sec': parse_time(end_time.split(',')[0]),
                    'text': text.strip()
                })

    return subtitles

def detect_topic_change(text1: str, text2: str) -> bool:
    """检测两句话是否话题转换"""
    transition_markers = ['但是', '然而', '不过', '另外', '接下来', '然后', '现在', '接下来我们', '好的，所以']

    for marker in transition_markers:
        if marker in text2:
            return True

    return False

def segment_by_topic(subtitles: List[Dict]) -> List[Dict]:
    """基于话题边界分段"""
    segments = []
    current_segment = []

    for i, subtitle in enumerate(subtitles):
        text = subtitle['text']

        should_start_new = False

        if not current_segment:
            should_start_new = False
        else:
            last_sub = current_segment[-1]
            time_gap = subtitle['start_sec'] - last_sub['end_sec']

            last_text = current_segment[-1]['text']
            topic_changed = detect_topic_change(last_text, text)

            too_long_gap = time_gap > 60
            too_long_segment = len(current_segment) >= 30

            if topic_changed or too_long_gap or too_long_segment:
                should_start_new = True

        if should_start_new:
            if current_segment:
                segments.append(current_segment.copy())
            current_segment = [subtitle]
        else:
            current_segment.append(subtitle)

    if current_segment:
        segments.append(current_segment)

    return segments

def generate_question_title(segment: List[Dict]) -> str:
    """为段落生成问题标题"""
    all_text = ' '.join([s['text'] for s in segment])
    text_lower = all_text.lower()

    # 1. 课程目标和介绍相关
    if any(kw in text_lower for kw in ['课程', '这门课', '目标', '学习', '收获']):
        if any(kw in text_lower for kw in ['为什么', '原因']):
            return "为什么要开设这门从零构建语言模型的课程？"
        if any(kw in text_lower for kw in ['构建', '从头', '零开始', '内容']):
            return "这门课会学到什么内容？"
        if any(kw in text_lower for kw in ['团队', '教师', '讲师', '助教']):
            return "教师团队有哪些人？"
        if any(kw in text_lower for kw in ['调整', '改变', 'youtube', '公开']):
            return "课程有什么新的安排？"

    # 2. 技术背景和动机
    if any(kw in text_lower for kw in ['危机', '脱离', '抽象', '底层', '堆栈', '理解技术']):
        return "为什么研究人员需要理解底层技术？"

    if any(kw in text_lower for kw in ['gpt-4', '参数', '规模', '成本', 'h100', '训练', '万亿']):
        if any(kw in text_lower for kw in ['公开', '披露', '细节', '不']):
            return "前沿模型的构建细节为什么没有公开？"
        if any(kw in text_lower for kw in ['万亿', 'billion', '成本', '投入']):
            return "GPT-4的规模和训练成本是多少？"

    # 3. 小模型vs大模型
    if any(kw in text_lower for kw in ['小型', '小规模', '小型模型', '涌现', '代表性']):
        if any(kw in text_lower for kw in ['涌现', '突然', '出现', '行为']):
            return "什么是涌现行为？"
        if any(kw in text_lower for kw in ['注意力', 'mlp', '浮点运算', '差异']):
            return "小模型和大模型的架构有什么差异？"
        return "小模型能够代表大模型的特性吗？"

    # 4. 知识类型
    if any(kw in text_lower for kw in ['知识', '类型', '传授', '思维', '方式', '三种']):
        return "这门课会传授哪些类型的知识？"

    # 5. 数据和分词
    if any(kw in text_lower for kw in ['数据', '分词', 'token', 'bpe', '词表', '字节', '编码']):
        if any(kw in text_lower for kw in ['bpe', 'bp算法', '合并', '词汇表']):
            return "什么是BPE分词算法？"
        if any(kw in text_lower for kw in ['字节', '0-256', '词汇量']):
            return "字节编码的词汇量有多大？"
        if any(kw in text_lower for kw in ['质量', '过滤', '清洗', '去重']):
            return "如何保证数据质量？"
        return "数据部分包含哪些内容？"

    # 6. 架构和模型
    if any(kw in text_lower for kw in ['架构', 'transformer', '模型', '层']):
        if any(kw in text_lower for kw in ['激活', '归一化', 'mlp', '注意力', '改进']):
            return "Transformer架构有哪些改进？"
        if any(kw in text_lower for kw in ['替代', 'ssm', 'hyena', '状态空间', '混合']):
            return "有哪些Transformer的替代方案？"
        return "课程会讲解哪些模型架构？"

    # 7. 训练相关
    if any(kw in text_lower for kw in ['优化器', 'adam', '学习率', '超参数', '调优', '正则化']):
        return "训练模型时有哪些重要的超参数和设计决策？"

    # 8. 作业和项目
    if any(kw in text_lower for kw in ['作业', '实现', 'bp', '排行榜', '困惑度', '90分钟']):
        if any(kw in text_lower for kw in ['一', 'bp分词器', 'transformer', '实现']):
            return "作业1需要实现什么？"
        if any(kw in text_lower for kw in ['排行榜', '困惑度', '评分', 'h100']):
            return "作业1如何评分？"

    # 9. 系统和硬件
    if any(kw in text_lower for kw in ['系统', '硬件', 'gpu', '内核', '并行', '推理']):
        if any(kw in text_lower for kw in ['gpu', '内存', '缓存', '结构', '芯片']):
            return "GPU的结构是怎样的？"
        if any(kw in text_lower for kw in ['内核', 'triton', '融合', '算子']):
            return "如何优化GPU内核？"
        if any(kw in text_lower for kw in ['并行', '分布式', '多gpu']):
            return "如何进行模型并行训练？"
        if any(kw in text_lower for kw in ['推理', '部署', 'kv', '量化']):
            return "如何优化推理性能？"
        return "系统部分会学习什么内容？"

    # 10. 苦涩的教训
    if any(kw in text_lower for kw in ['苦涩', '教训', '规模', '效率', '算法']):
        return "什么是\"苦涩的教训\"？"

    # 11. 评估
    if any(kw in text_lower for kw in ['评估', '基准', '测试', '性能', '准确率']):
        return "如何评估语言模型的性能？"

    # 默认：提取关键信息
    first_sentences = ' '.join([s['text'] for s in segment[:3]])
    if len(all_text) < 100:
        preview = all_text[:50]
    else:
        preview = all_text[:100]

    return f"关于：{preview}..."

def merge_segments_by_question(segments: List[List[Dict]]) -> List[Tuple[str, List[List[Dict]]]]:
    """
    合并相同问题的段落
    返回: [(问题, [段落列表]), ...]
    """
    question_groups = {}

    for segment in segments:
        question = generate_question_title(segment)

        if question not in question_groups:
            question_groups[question] = []

        question_groups[question].append(segment)

    # 转换为列表并按问题排序
    result = []
    for question, seg_list in question_groups.items():
        result.append((question, seg_list))

    # 按第一个段落的时间排序
    result.sort(key=lambda x: x[1][0][0]['start_sec'])

    return result

def format_content_paragraph(text: str) -> str:
    """格式化内容段落，添加适当的换行和标点"""
    # 去除语气词
    text = re.sub(r'^(嗯|呃|啊|嘿|哈)\s*', '', text)
    text = re.sub(r'\s+(嗯|呃|啊|嘿|哈)\s+', ' ', text)

    # 在句子之间添加换行（基于句号、感叹号、问号）
    text = re.sub(r'([。！？])\s*', r'\1\n\n', text)

    # 在逗号后适当换行（长句拆分）
    text = re.sub(r'，\s*', r'，\n', text)

    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def generate_markdown(question_groups: List[Tuple[str, List[List[Dict]]]], video_url: str) -> str:
    """生成Markdown，合并相同问题"""
    output = []
    output.append(f"# 斯坦福 CS336 P01：从零开始构建语言模型\n\n")
    output.append(f"**视频链接**: {video_url}\n\n")
    output.append(f"**总问题数**: {len(question_groups)}\n\n")
    output.append("---\n\n")

    for question, segments in question_groups:
        output.append(f"## {question}\n\n")

        # 为每个时间段的段落添加子标题
        for i, segment in enumerate(segments, 1):
            start_sec = segment[0]['start_sec']
            end_sec = segment[-1]['end_sec']

            start_time_str = format_time(start_sec)
            end_time_str = format_time(end_sec)

            # 合并文本内容
            content_parts = []
            for sub in segment:
                text = sub['text']
                text = re.sub(r'^(嗯|呃|啊|嘿|哈)\s*', '', text)
                if text:
                    content_parts.append(text)

            content = ' '.join(content_parts)

            # 格式化内容
            formatted_content = format_content_paragraph(content)

            # 如果是同一问题的多个时间段，添加子标题
            if len(segments) > 1:
                output.append(f"### 讨论时间 {i}\n\n")

            output.append(f"**⏱️ 时间**: [{start_time_str}]({video_url}?t={start_sec}#t={start_time_str}) - [{end_time_str}]({video_url}?t={end_sec}#t={end_time_str})\n\n")
            output.append(f"**📝 内容**:\n\n{formatted_content}\n\n")

            if len(segments) > 1:
                output.append("---\n\n")

        output.append("---\n\n")

    return ''.join(output)

def main():
    import sys

    if len(sys.argv) < 4:
        print("Usage: python3 generate_question_outline.py <input.srt> <output.md> <video_url>")
        sys.exit(1)

    srt_file = sys.argv[1]
    output_file = sys.argv[2]
    video_url = sys.argv[3]

    print("📖 读取SRT文件...")
    subtitles = parse_srt(srt_file)
    print(f"✅ 共读取 {len(subtitles)} 条字幕")

    print("🧠 基于话题边界分段...")
    segments = segment_by_topic(subtitles)
    print(f"✅ 共生成 {len(segments)} 个段落")

    print("🔄 合并相同问题的段落...")
    question_groups = merge_segments_by_question(segments)
    print(f"✅ 合并后共 {len(question_groups)} 个问题")

    # 统计信息
    single_count = sum(1 for _, segs in question_groups if len(segs) == 1)
    multi_count = sum(1 for _, segs in question_groups if len(segs) > 1)

    print(f"\n📊 统计信息:")
    print(f"  - 单次讨论的问题: {single_count}个")
    print(f"  - 多次讨论的问题: {multi_count}个")

    print("\n📝 生成清晰的排版格式...")
    markdown = generate_markdown(question_groups, video_url)

    print(f"💾 保存到文件: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print("✅ 完成！")

if __name__ == "__main__":
    main()
