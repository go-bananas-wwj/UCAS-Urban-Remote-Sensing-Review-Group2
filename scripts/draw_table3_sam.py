#!/usr/bin/env python3
"""
表3: SAM系列基础模型在遥感道路/建筑物提取中的代表性方法对比
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(20, 5.0))
ax.set_xlim(0, 20)
ax.set_ylim(0, 5.0)
ax.axis('off')

ax.text(10, 4.7, '表3 SAM系列基础模型在遥感道路/建筑物提取中的代表性方法对比',
        ha='center', va='center', fontsize=14, fontweight='bold', color='#2C3E50')

headers = ['方法', '年份', 'SAM版本', '核心策略', '训练方式', '开放词汇', 'DeepGlobe道路', '建筑物IoU', '核心特点']
col_widths = [1.8, 1.2, 1.6, 3.0, 2.4, 1.6, 2.6, 2.6, 3.2]
ncol = len(headers)

x_pos = [0.5]
for w in col_widths[:-1]:
    x_pos.append(x_pos[-1] + w)

rows = [
    ['Road-SAM', '2024', 'SAM 1', 'Adapter+EVP高频提示', '参数高效微调(~10%)', '否', 'F1 81.65 / IoU 68.99', '-', '道路专用轻量化适配'],
    ['RSAM-Seg', '2025', 'SAM 1', 'Adapter微调', '参数高效微调', '否', '-', '-', '通用遥感语义分割'],
    ['SAM-Road', '2024', 'SAM 1', '几何分割+图网络拓扑', 'SAM无需重训练', '否', '-', '-', '40×快于RNGDet++'],
    ['SAM-Road++', '2024', 'SAM 1', '节点引导重采样+扩展线', 'SAM无需重训练', '否', '-', '-', '全球尺度道路验证'],
    ['SAM 3', '2025', 'SAM 3', 'PCS概念提示分割', '4M概念预训练', '是', '-', '-', 'LVIS AP 48.8(零样本)'],
    ['SegEarth-OV3', '2025', 'SAM 3', '双头融合+Presence过滤', '零样本推理', '是', 'IoU 39.3(零样本)', 'WHU 86.9 / Inria 72.4 / xBD 64.3', '20个数据集零样本SOTA'],
]

nrow = len(rows)
row_height = 0.55
table_top = 4.2
header_height = 0.65

for j, (h, x, w) in enumerate(zip(headers, x_pos, col_widths)):
    rect = plt.Rectangle((x, table_top), w, header_height, facecolor='#2C3E50', edgecolor='white', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, table_top + header_height/2, h, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

for i, row in enumerate(rows):
    y = table_top - (i + 1) * row_height
    bg_color = '#F8F9FA' if i % 2 == 0 else 'white'
    for j, (cell, x, w) in enumerate(zip(row, x_pos, col_widths)):
        rect = plt.Rectangle((x, y), w, row_height, facecolor=bg_color, edgecolor='#DEE2E6', linewidth=1)
        ax.add_patch(rect)
        fontsize = 9 if len(cell) < 14 else 8
        ax.text(x + w/2, y + row_height/2, cell, ha='center', va='center',
                fontsize=fontsize, color='#2C3E50')

total_w = sum(col_widths)
ax.plot([0.5, 0.5], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5 + total_w, 0.5 + total_w], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + total_w], [table_top + header_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + total_w], [table_top - nrow * row_height, table_top - nrow * row_height], color='#2C3E50', linewidth=2)

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表3_SAM系列方法对比.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表3_SAM系列方法对比.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("表3 保存完成")
