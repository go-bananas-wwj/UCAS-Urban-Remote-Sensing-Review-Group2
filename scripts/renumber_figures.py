#!/usr/bin/env python3
"""
Renumber all figures sequentially in the markdown file.
Also insert new figures into the Deep Learning II section.
Uses token-based replacement to avoid cascading issues.
"""

import re

md_path = '/workspace/other/yaogan/02_综述报告/综述正文_for_docx.md'
output_path = '/workspace/other/yaogan/02_综述报告/综述正文_for_docx.md'

with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mapping: old figure number -> new figure number
fig_map = {
    1: 1,   # 技术演进时间线
    2: 2,   # 传统道路提取范式
    3: 3,   # OBIA多尺度分割
    4: 5,   # 编码器解码器架构
    5: 13,  # SAM系列架构演进
    6: 4,   # SVM→U-Net+CRF
    7: 6,   # TopoRF-Net
    8: 7,   # CFENet
    9: 10,  # SAM-Road
    10: 9,  # Road-SAM
    11: 14, # 三维建筑物提取
    12: 15, # LOD层级
}

# Step 1: Replace all image alt text
# Pattern: ![图X ...](...)
def replace_img_alt(match):
    prefix = match.group(1)
    num = int(match.group(2))
    suffix = match.group(3)
    new_num = fig_map.get(num, num)
    return f'{prefix}{new_num}{suffix}'

content = re.sub(r'(!\[图)(\d+)(\s[^\]]*\]\([^\)]*\))', replace_img_alt, content)

# Step 2: Replace inline text references
# Use a function that matches "图X" where X is in the mapping
# Avoid matching inside image alt text (already changed) and table markdown
def replace_text_ref(match):
    prefix = match.group(1)
    num = int(match.group(2))
    new_num = fig_map.get(num, num)
    return f'{prefix}{new_num}'

# Match "图X" not preceded by '[' or '!' and not followed by another digit
# Allow common Chinese punctuation before 图
content = re.sub(r'(?<![\[!])((?:如|如图|见|见 图|（|，|、|；|：|\s)图)(\d+)(?![0-9])', replace_text_ref, content)

# Also handle bare "图X" at start of sentence or after punctuation
content = re.sub(r'(?<![\[!\]])(?<![0-9])(图)(\d+)(?![0-9])', replace_text_ref, content)

# Step 3: Insert new figures

# New figure 8: SegFormer architecture - insert before "### 6.3 SAM系列"
segformer_insert = '''![图8 SegFormer编码器-解码器架构示意图：层次化Mix Transformer编码器与轻量All-MLP解码器](05_图表素材/图X_SegFormer架构.png)
> （引自SegFormer Xie et al., NeurIPS 2021：MiT编码器通过逐层递减的patch嵌入提取多尺度特征，All-MLP解码器直接融合多级特征并输出分割结果）

'''
content = content.replace(
    '### 6.3 SAM系列：从视觉提示到概念提示',
    segformer_insert + '### 6.3 SAM系列：从视觉提示到概念提示'
)

# New figure 11: SAM 3 concept illustration - insert before "### 6.4 开放词汇与多模态大模型趋势"
sam3_insert = '''![图11 SAM 3概念提示分割范式：从视觉提示（点/框）到概念提示（文本名词短语）的跃迁](05_图表素材/图X_SAM3概念提示分割.png)
> （引自SAM 3 Carion et al., Meta 2025：左列为SAM 1/2的视觉提示分割（单目标），右列为SAM 3的概念提示分割（文本驱动全实例分割））

'''
content = content.replace(
    '### 6.4 开放词汇与多模态大模型趋势',
    sam3_insert + '### 6.4 开放词汇与多模态大模型趋势'
)

# New figure 12: SegEarth-OV3 zero-shot results - insert before "### 6.5 小结"
segearth_insert = '''![图12 SegEarth-OV3在遥感影像上的零样本开放词汇分割效果](05_图表素材/图X_SegEarth_OV3零样本分割.png)
> （引自SegEarth-OV3 Li et al., 2025：(a)原始遥感影像，(b)SAM 3零样本分割结果，道路与建筑物在无训练条件下被正确识别）

'''
content = content.replace(
    '### 6.5 小结',
    segearth_insert + '### 6.5 小结'
)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Updated markdown saved.")

# Verify figure order
result = __import__('subprocess').run(['grep', '-n', '^!\[图', md_path], capture_output=True, text=True)
print("\nNew figure order:")
for line in result.stdout.strip().split('\n'):
    print(line)
