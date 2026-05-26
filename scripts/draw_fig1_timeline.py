#!/usr/bin/env python3
"""
图1: 城市路网与建筑物提取方法技术演进时间线
修复v3: 箭头精确连接框底/顶边中心
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(18, 9))
ax.set_xlim(0, 18)
ax.set_ylim(0, 9)
ax.axis('off')

COLORS = {
    'era_trad': '#E8D5C4', 'era_cnn': '#B8D4E3', 'era_multi': '#D4E6B5',
    'era_attn': '#E8D0E8', 'era_trans': '#F5D0A9', 'era_fm': '#F5B7B1',
    'road': '#E74C3C', 'building': '#3498DB', 'text': '#2C3E50',
    'subtext': '#7F8C8D', 'timeline': '#95A5A6',
}

ax.text(9, 8.6, '城市路网与建筑物提取方法技术演进时间线',
        ha='center', va='center', fontsize=17, fontweight='bold', color=COLORS['text'])
ax.text(9, 8.15, 'Technical Evolution Timeline of Urban Road & Building Extraction Methods',
        ha='center', va='center', fontsize=10, color=COLORS['subtext'], style='italic')

eras = [
    (0.3, 2.7, '传统方法\nTraditional', COLORS['era_trad']),
    (3.1, 2.8, 'CNN/FCN时代\nCNN/FCN Era', COLORS['era_cnn']),
    (6.0, 2.8, '多尺度与注意力\nMulti-scale & Attention', COLORS['era_multi']),
    (8.9, 2.8, 'Transformer时代\nTransformer Era', COLORS['era_trans']),
    (11.8, 2.8, '基础模型/FM时代\nFoundation Model', COLORS['era_fm']),
    (14.7, 2.7, '未来趋势\nFuture', '#F0F0F0'),
]
for x, w, label, color in eras:
    rect = FancyBboxPatch((x, 1.2), w, 5.6, boxstyle="round,pad=0.05,rounding_size=0.15",
                          facecolor=color, edgecolor='none', alpha=0.5, zorder=0)
    ax.add_patch(rect)
    ax.text(x + w/2, 1.5, label, ha='center', va='center', fontsize=8,
            color=COLORS['subtext'], fontweight='medium')

ax.plot([1.0, 17.0], [4.5, 4.5], color=COLORS['timeline'], linewidth=3, zorder=1, solid_capstyle='round')

year_ticks = [2010, 2015, 2018, 2020, 2022, 2024, 2025]
x_map = lambda y: 1.0 + (y - 2010) / (2025 - 2010) * 16.0
for year in year_ticks:
    x = x_map(year)
    ax.plot([x, x], [4.35, 4.65], color=COLORS['timeline'], linewidth=2, zorder=2)
    ax.text(x, 4.12, str(year), ha='center', va='top', fontsize=9, color=COLORS['subtext'], fontweight='bold')

# 绘制带精确中心连线的框
def draw_timeline_box(ax, x, y_target, label, color, marker_shape, box_w=1.7, box_h=0.7):
    bw = box_w if len(label) > 15 else 1.4
    bh = box_h if '\n' in label else 0.45
    
    # 框底边/顶边中心精确坐标
    box_bottom = y_target - bh/2
    box_top = y_target + bh/2
    
    # 时间轴到框的连线 — 精确连接到框边中心
    if y_target > 4.5:  # 上方（路网）
        ax.plot([x, x], [4.62, box_bottom], color=color, linewidth=1.5, zorder=3)
    else:  # 下方（建筑物）
        ax.plot([x, x], [4.38, box_top], color=color, linewidth=1.5, zorder=3)
    
    ax.plot(x, 4.5, marker_shape, color=color, markersize=8 if marker_shape=='o' else 7,
            zorder=4, markeredgecolor='white', markeredgewidth=1.2)
    
    box = FancyBboxPatch((x - bw/2, y_target - bh/2), bw, bh,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor='#FADBD8' if color==COLORS['road'] else '#D4E6F1',
                         edgecolor=color, linewidth=1.8, alpha=0.95, zorder=5)
    ax.add_patch(box)
    ax.text(x, y_target, label, ha='center', va='center', fontsize=8,
            color=COLORS['text'], fontweight='medium', zorder=6)

road_color = COLORS['road']
road_key = [
    (2010, 6.4, '形态学/边缘检测\n边缘检测与形态学滤波'),
    (2012, 7.7, '面向对象分类\n(OBIA)'),
    (2015, 6.4, 'FCN / U-Net\n端到端语义分割奠基'),
    (2018, 7.7, 'DeepLabV3+ / D-LinkNet\n多尺度与空洞卷积'),
    (2020, 6.4, 'RNGDet++ / Sat2Graph\n图网络拓扑恢复'),
    (2022, 7.7, 'CFENet / TopoRF-Net\n级联特征与拓扑保持'),
    (2024, 6.4, 'SAM-Road / SAM-Road++\nSAM适配与拓扑增强'),
    (2025, 7.7, 'SAM 3 / SegEarth-OV3\n概念提示与零样本'),
]
for year, y_off, label in road_key:
    draw_timeline_box(ax, x_map(year), y_off, label, road_color, 'o')

building_color = COLORS['building']
build_key = [
    (2010, 2.6, '手工特征/规则分类\nSVM + 形态学特征'),
    (2015, 1.3, 'U-Net迁移遥感\nEncoder-Decoder架构'),
    (2018, 2.6, 'DeepLabV3+ 建筑物\nASPP多尺度上下文'),
    (2021, 1.3, 'SegFormer / ViT Building\nTransformer全局建模'),
    (2023, 2.6, 'HTC Building / DeH4R\n高分辨率与层次特征'),
    (2024, 1.3, 'RSAM-Seg / Guo et al.\nSAM遥感适配与联合提取'),
    (2025, 2.6, 'SegEarth-OV3\n20数据集零样本SOTA'),
]
for year, y_off, label in build_key:
    draw_timeline_box(ax, x_map(year), y_off, label, building_color, 's')

ax.text(0.35, 6.5, '路网提取', ha='center', va='center', fontsize=12,
        color=road_color, fontweight='bold', rotation=90)
ax.text(0.35, 2.5, '建筑物提取', ha='center', va='center', fontsize=12,
        color=building_color, fontweight='bold', rotation=90)

legend_y = 0.5
legend_items = [
    (1.2, '传统方法', COLORS['era_trad']),
    (3.8, 'CNN/FCN', COLORS['era_cnn']),
    (6.4, '多尺度/注意力', COLORS['era_multi']),
    (9.2, 'Transformer', COLORS['era_trans']),
    (12.0, '基础模型 FM', COLORS['era_fm']),
]
for lx, llabel, lcolor in legend_items:
    rect = mpatches.Rectangle((lx, legend_y - 0.08), 0.3, 0.16, facecolor=lcolor,
                               edgecolor='#999', linewidth=0.8, alpha=0.8)
    ax.add_patch(rect)
    ax.text(lx + 0.45, legend_y, llabel, ha='left', va='center', fontsize=8, color=COLORS['subtext'])

ax.plot(15.5, legend_y, 'o', color=road_color, markersize=7)
ax.text(15.7, legend_y, '路网', ha='left', va='center', fontsize=8, color=road_color)
ax.plot(16.3, legend_y, 's', color=building_color, markersize=6)
ax.text(16.5, legend_y, '建筑物', ha='left', va='center', fontsize=8, color=building_color)

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图1_技术演进时间线.png',
            dpi=300, bbox_inches='tight', pad_inches=0.25, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图1_技术演进时间线.pdf',
            bbox_inches='tight', pad_inches=0.25, facecolor='white')
print("图1 v3 保存完成")
