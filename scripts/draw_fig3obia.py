#!/usr/bin/env python3
"""
图3: OBIA多尺度分割概念示意图
修复: 精确居中、增大间距、统一风格
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 3, figsize=(14, 5.5))
fig.suptitle('OBIA多尺度分割中不同尺度参数对建筑物对象生成的影响', fontsize=15, fontweight='bold', y=0.97)

# 三个panel的配置
panels = [
    {
        'title': '(a) 尺度参数较小',
        'subtitle': '分割过细，产生大量破碎对象',
        'boxes': [
            {'x': 0.15, 'y': 0.55, 'w': 0.18, 'h': 0.22, 'label': 'B1', 'color': '#FADBD8'},
            {'x': 0.55, 'y': 0.55, 'w': 0.18, 'h': 0.22, 'label': 'B2', 'color': '#D4E6F1'},
            {'x': 0.15, 'y': 0.18, 'w': 0.18, 'h': 0.22, 'label': 'B3', 'color': '#D5F5E3'},
            {'x': 0.55, 'y': 0.18, 'w': 0.18, 'h': 0.22, 'label': 'B4', 'color': '#FCF3CF'},
        ]
    },
    {
        'title': '(b) 尺度参数适中',
        'subtitle': '对象边界与建筑物轮廓一致',
        'boxes': [
            {'x': 0.12, 'y': 0.52, 'w': 0.35, 'h': 0.30, 'label': 'B1+B2', 'color': '#FADBD8'},
            {'x': 0.55, 'y': 0.52, 'w': 0.35, 'h': 0.30, 'label': 'B5', 'color': '#D4E6F1'},
            {'x': 0.12, 'y': 0.12, 'w': 0.35, 'h': 0.30, 'label': 'B3+B4', 'color': '#D5F5E3'},
            {'x': 0.55, 'y': 0.12, 'w': 0.35, 'h': 0.30, 'label': 'B6', 'color': '#FCF3CF'},
        ]
    },
    {
        'title': '(c) 尺度参数较大',
        'subtitle': '对象过合并，丢失个体信息',
        'boxes': [
            {'x': 0.08, 'y': 0.10, 'w': 0.84, 'h': 0.78, 'label': '建筑群\n(过合并)', 'color': '#F5B7B1'},
        ]
    },
]

for ax, panel in zip(axes, panels):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # 背景
    bg = Rectangle((0, 0), 1, 1, facecolor='#F8F9FA', edgecolor='#DEE2E6', linewidth=1.5)
    ax.add_patch(bg)
    
    # 道路示意（十字交叉）
    ax.plot([0.5, 0.5], [0.05, 0.95], color='#6C757D', linewidth=4, zorder=1)
    ax.plot([0.05, 0.95], [0.5, 0.5], color='#6C757D', linewidth=4, zorder=1)
    
    # 标题
    ax.text(0.5, 0.96, panel['title'], ha='center', va='top', fontsize=13, fontweight='bold', color='#2C3E50')
    
    # 建筑物框
    for b in panel['boxes']:
        box = FancyBboxPatch((b['x'], b['y']), b['w'], b['h'],
                             boxstyle="round,pad=0.01,rounding_size=0.02",
                             facecolor=b['color'], edgecolor='#2C3E50', linewidth=2, zorder=3)
        ax.add_patch(box)
        ax.text(b['x'] + b['w']/2, b['y'] + b['h']/2, b['label'],
                ha='center', va='center', fontsize=12, fontweight='bold', color='#2C3E50', zorder=4)
    
    # 底部说明
    ax.text(0.5, 0.02, panel['subtitle'], ha='center', va='bottom', fontsize=10, color='#6C757D')

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图3_OBIA多尺度分割.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图3_OBIA多尺度分割.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("图3 保存完成")
