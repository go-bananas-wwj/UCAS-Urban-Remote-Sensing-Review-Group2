#!/usr/bin/env python3
"""
表4: 多源融合与多任务联合提取代表性方法对比
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(17, 4.2))
ax.set_xlim(0, 17)
ax.set_ylim(0, 4.2)
ax.axis('off')

ax.text(8.5, 3.9, '表4 多源融合与多任务联合提取代表性方法对比',
        ha='center', va='center', fontsize=14, fontweight='bold', color='#2C3E50')

headers = ['方法', '年份', '融合/任务策略', '数据源', '目标地物', '核心创新', '关键效果']
col_widths = [2.2, 1.3, 2.8, 2.4, 2.0, 3.0, 3.3]
ncol = len(headers)

x_pos = [0.5]
for w in col_widths[:-1]:
    x_pos.append(x_pos[-1] + w)

rows = [
    ['Guo CRIN', '2024', '多任务联合提取', '光学VHR影像', '建筑+道路', 'MTI模块+CSI自适应感受野', '推理时间减半，双任务精度提升'],
    ['Chen HTC', '2023', '多源高度约束', '光学+LiDAR/DSM', '建筑物', '高度约束Transformer', '三维建筑边界精化'],
    ['TopoRF-Net', '2025', '拓扑保持单任务', '光学VHR影像', '道路', 'MRFE+CI-Decoder+Topology Loss', 'DeepGlobe IoU 69.76%，拓扑连通'],
    ['NFSNet', '2020', '多任务联合', '光学VHR影像', '建筑+道路', '非局部特征搜索', '缓解多任务特征竞争'],
    ['D-LinkNet+DSM', '2018', '多源融合', '光学+DSM', '道路', '高度辅助道路筛选', '减少道路与停车场混淆'],
]

nrow = len(rows)
row_height = 0.55
table_top = 3.4
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
        fontsize = 9.5 if len(cell) < 14 else 8.5
        ax.text(x + w/2, y + row_height/2, cell, ha='center', va='center',
                fontsize=fontsize, color='#2C3E50')

total_w = sum(col_widths)
ax.plot([0.5, 0.5], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5 + total_w, 0.5 + total_w], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + total_w], [table_top + header_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + total_w], [table_top - nrow * row_height, table_top - nrow * row_height], color='#2C3E50', linewidth=2)

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表4_多源融合方法对比.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表4_多源融合方法对比.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("表4 保存完成")
