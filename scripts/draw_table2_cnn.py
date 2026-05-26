#!/usr/bin/env python3
"""
表2: CNN时代代表性道路与建筑物提取方法对比
修复: 画布加宽、字体加大、行高增加、列宽优化
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(18, 5.5))
ax.set_xlim(0, 18)
ax.set_ylim(0, 5.5)
ax.axis('off')

ax.text(9, 5.2, '表2 CNN时代代表性道路与建筑物提取方法对比', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#2C3E50')

# 表头
headers = ['方法', '年份', '主干网络', '核心创新', '适用任务', 'Massachusetts', 'DeepGlobe', '主要特点']
col_widths = [1.6, 1.3, 2.2, 3.0, 2.0, 2.4, 2.4, 3.1]
ncol = len(headers)

# 计算x位置
x_pos = [0.5]
for w in col_widths[:-1]:
    x_pos.append(x_pos[-1] + w)

# 行数据
rows = [
    ['FCN', '2015', 'VGG16', '全卷积+反卷积上采样', '通用分割', '道路IoU ~52', '道路IoU ~45', '端到端语义分割奠基'],
    ['U-Net', '2015', 'Encoder-Decoder', '跳跃连接融合多尺度特征', '医学/遥感', '道路IoU ~58', '道路IoU ~52', '遥感分割基石架构'],
    ['SegNet', '2015', 'VGG16', '池化索引指导上采样', '通用分割', '-', '-', '轻量高效，参数量小'],
    ['DeepLabV3+', '2018', 'ResNet/Xception', 'ASPP+可分离空洞卷积', '通用分割', '-', '道路IoU ~66', '多尺度上下文建模'],
    ['D-LinkNet', '2018', 'ResNet34', '空洞卷积分支+LinkNet', '道路提取', '-', 'IoU 66.2 / F1 79.6', '道路提取经典基准'],
    ['CFENet', '2022', 'ResNet', 'SFM+FEM+FDM三级增强', '建筑物', '建筑IoU 73.8', '-', '级联特征增强专用网络'],
    ['TopoRF-Net', '2025', 'MiT', 'MRFE+CI-Decoder+Topology', '道路提取', 'IoU 59.7 / F1 74.8', 'IoU 69.8 / F1 82.2', '拓扑保持与多感受野'],
]

nrow = len(rows)
row_height = 0.55
table_top = 4.6
header_height = 0.65

# 绘制表头
for j, (h, x, w) in enumerate(zip(headers, x_pos, col_widths)):
    rect = plt.Rectangle((x, table_top), w, header_height, facecolor='#2C3E50', edgecolor='white', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, table_top + header_height/2, h, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

# 绘制数据行
for i, row in enumerate(rows):
    y = table_top - (i + 1) * row_height
    bg_color = '#F8F9FA' if i % 2 == 0 else 'white'
    for j, (cell, x, w) in enumerate(zip(row, x_pos, col_widths)):
        rect = plt.Rectangle((x, y), w, row_height, facecolor=bg_color, edgecolor='#DEE2E6', linewidth=1)
        ax.add_patch(rect)
        fontsize = 9.5 if len(cell) < 12 else 8.5
        ax.text(x + w/2, y + row_height/2, cell, ha='center', va='center',
                fontsize=fontsize, color='#2C3E50')

# 表格外边框
ax.plot([0.5, 0.5], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5 + sum(col_widths), 0.5 + sum(col_widths)], [table_top - nrow * row_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + sum(col_widths)], [table_top + header_height, table_top + header_height], color='#2C3E50', linewidth=2)
ax.plot([0.5, 0.5 + sum(col_widths)], [table_top - nrow * row_height, table_top - nrow * row_height], color='#2C3E50', linewidth=2)

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表2_CNN时代方法对比.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/表2_CNN时代方法对比.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("表2 保存完成")
