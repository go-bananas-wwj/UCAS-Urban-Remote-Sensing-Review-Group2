#!/usr/bin/env python3
"""
Rebuild 综述正文_for_docx.md from 综述正文.md:
1. Convert figure/table blockquotes to markdown image syntax
2. Insert new figures for Deep Learning II section
3. Renumber all figures sequentially
"""

import re

md_path = '/workspace/other/yaogan/02_综述报告/综述正文.md'
output_path = '/workspace/other/yaogan/02_综述报告/综述正文_for_docx.md'

with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Figure mapping: figure name/number in 综述正文.md -> actual image path (PNG)
# Also track the new sequential numbering
fig_paths = {
    '图1': '05_图表素材/技术演进时间线.png',
    '图2': '05_图表素材/pdf_extracted_images/E06_Qian_ISPRS_p3_img1.png',
    '图3': '05_图表素材/图3_OBIA多尺度分割.png',
    '图4': '05_图表素材/图4_编码器解码器架构简图.png',
    '图5': '05_图表素材/图5_SAM系列架构演进.png',
    '图6': '05_图表素材/pdf_extracted_images/C10_p6_img1.png',
    '图7': '05_图表素材/pdf_extracted_images/E08_p2_img1_whitebg.png',
    '图8': '05_图表素材/pdf_extracted_images/E05_p11_img2.png',
    '图9': '05_图表素材/pdf_extracted_images/E01_p8_img1.png',
    '图10': '05_图表素材/pdf_extracted_images/E12_p2_img1.png',
    '图11': '05_图表素材/图11_三维建筑物提取技术路线.png',
    '图12': '05_图表素材/图12_CityGML_LOD层级.png',
}

table_paths = {
    '表2': '05_图表素材/表2_CNN时代方法对比.png',
    '表3': '05_图表素材/表3_SAM系列方法对比.png',
    '表4': '05_图表素材/表4_多源融合方法对比.png',
}

# New figures to insert
new_figs = {
    'segformer': {
        'caption': '图8 SegFormer编码器-解码器架构示意图：层次化Mix Transformer编码器与轻量All-MLP解码器',
        'path': '05_图表素材/图X_SegFormer架构.png',
        'note': '（引自SegFormer Xie et al., NeurIPS 2021：MiT编码器通过逐层递减的patch嵌入提取多尺度特征，All-MLP解码器直接融合多级特征并输出分割结果）',
        'insert_before': '### 6.3 SAM系列：从视觉提示到概念提示',
    },
    'sam3': {
        'caption': '图11 SAM 3概念提示分割范式：从视觉提示（点/框）到概念提示（文本名词短语）的跃迁',
        'path': '05_图表素材/图X_SAM3概念提示分割.png',
        'note': '（引自SAM 3 Carion et al., Meta 2025：左列为SAM 1/2的视觉提示分割（单目标），右列为SAM 3的概念提示分割（文本驱动全实例分割））',
        'insert_before': '### 6.4 开放词汇与多模态大模型趋势',
    },
    'segearth': {
        'caption': '图12 SegEarth-OV3在遥感影像上的零样本开放词汇分割效果',
        'path': '05_图表素材/图X_SegEarth_OV3零样本分割.png',
        'note': '（引自SegEarth-OV3 Li et al., 2025：(a)原始遥感影像，(b)SAM 3零样本分割结果，道路与建筑物在无训练条件下被正确识别）',
        'insert_before': '### 6.5 小结',
    },
}

# Renumbering mapping for existing figures
# Reading order: 图1, 图2, 图3, 图6, 图4, 图7, 图8, 图10, 图9, 图5, 图11, 图12
# New order:     图1, 图2, 图3, 图4, 图5, 图6, 图7, 图8(new), 图9, 图10, 图11(new), 图12(new), 图13, 图14, 图15
fig_renumber = {
    '图1': '图1',
    '图2': '图2',
    '图3': '图3',
    '图4': '图5',   # encoder-decoder
    '图5': '图13',  # SAM evolution
    '图6': '图4',   # SVM→U-Net+CRF
    '图7': '图6',   # TopoRF-Net
    '图8': '图7',   # CFENet
    '图9': '图10',  # SAM-Road
    '图10': '图9',  # Road-SAM
    '图11': '图14', # 3D buildings
    '图12': '图15', # LOD
}

# Step 1: Convert blockquotes to image markdown and renumber
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Check if this is a figure blockquote
    fig_match = re.match(r'^> \*\*(图\d+)\s+(.+?)\*\*$', stripped)
    if fig_match:
        fig_old = fig_match.group(1)
        fig_caption = fig_match.group(2)
        fig_new = fig_renumber.get(fig_old, fig_old)
        img_path = fig_paths.get(fig_old, '')
        
        # Read the next line for the note/source
        note = ''
        if i + 1 < len(lines) and lines[i+1].strip().startswith('> '):
            note_line = lines[i+1].strip()
            # Extract note text, removing the leading '> '
            note = note_line[2:].strip()
            i += 1
        
        # Convert to markdown image
        output_lines.append(f'![{fig_new} {fig_caption}]({img_path})\n')
        if note and not note.startswith('（插入') and not note.startswith('（建议'):
            output_lines.append(f'> {note}\n')
        
        i += 1
        continue
    
    # Check if this is a table blockquote
    table_match = re.match(r'^> \*\*(表\d+)\s+(.+?)\*\*$', stripped)
    if table_match:
        table_old = table_match.group(1)
        table_caption = table_match.group(2)
        img_path = table_paths.get(table_old, '')
        
        # Read the next line for the note
        note = ''
        if i + 1 < len(lines) and lines[i+1].strip().startswith('> '):
            note_line = lines[i+1].strip()
            note = note_line[2:].strip()
            i += 1
        
        output_lines.append(f'![{table_old} {table_caption}]({img_path})\n')
        if note and not note.startswith('（`'):
            output_lines.append(f'> {note}\n')
        
        i += 1
        continue
    
    # Check if this is a plain note blockquote (not a figure/table caption)
    if stripped.startswith('> '):
        output_lines.append(line)
        i += 1
        continue
    
    # Regular line
    output_lines.append(line)
    i += 1

content = ''.join(output_lines)

# Step 2: Fix inline text references
# Map: old -> new for text references
ref_map = {
    '图1': '图1', '图2': '图2', '图3': '图3',
    '图4': '图5', '图5': '图13', '图6': '图4',
    '图7': '图6', '图8': '图7', '图9': '图10',
    '图10': '图9', '图11': '图14', '图12': '图15',
}

def replace_ref(match):
    prefix = match.group(1)
    fig = match.group(2)
    new_fig = ref_map.get(fig, fig)
    return f'{prefix}{new_fig}'

# Replace text references (not in image markdown)
lines = content.split('\n')
new_lines = []
for line in lines:
    if line.strip().startswith('!['):
        new_lines.append(line)
        continue
    # Replace figure references
    line = re.sub(r'([如（，、；：\s]*)(图\d+)(?![0-9])', replace_ref, line)
    new_lines.append(line)
content = '\n'.join(new_lines)

# Step 3: Insert new figures
for key, fig_info in new_figs.items():
    insert_markdown = f"![{fig_info['caption']}]({fig_info['path']})\n> {fig_info['note']}\n\n"
    content = content.replace(fig_info['insert_before'], insert_markdown + fig_info['insert_before'])

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Saved to {output_path}")

# Verify
print("\nFigure order in new markdown:")
for i, line in enumerate(content.split('\n'), 1):
    if line.strip().startswith('![图'):
        print(f"{i}: {line.strip()[:80]}")
