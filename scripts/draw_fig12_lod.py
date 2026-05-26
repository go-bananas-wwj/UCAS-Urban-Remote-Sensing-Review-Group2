#!/usr/bin/env python3
"""
图12: CityGML标准中建筑物LOD层级定义示意图
修复v2: 箭头置顶避免遮挡、标签分散避免重叠
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
import numpy as np
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(7, 7.5, '图12 CityGML标准中建筑物LOD层级定义示意图',
        ha='center', va='center', fontsize=16, fontweight='bold', color='#2C3E50')

ax.plot([1.0, 13.0], [1.2, 1.2], color='#5D6D7E', linewidth=2, zorder=1)

lods = [
    {'name': 'LOD0', 'desc': '二维轮廓\n(2D footprint)', 'x': 1.5, 'w': 1.8, 'h': 0.05, 'color': '#3498DB', 'light': '#D4E6F1', 'y_text': 1.6, 'x_text': 1.5},
    {'name': 'LOD1', 'desc': '块体模型\n(Prismatic block)', 'x': 4.0, 'w': 1.8, 'h': 2.0, 'color': '#27AE60', 'light': '#D5F5E3', 'y_text': 3.6, 'x_text': 4.9},
    {'name': 'LOD2', 'desc': '简单屋顶\n(Simple roof)', 'x': 6.5, 'w': 1.8, 'h': 3.0, 'color': '#E67E22', 'light': '#FDEBD0', 'y_text': 5.2, 'x_text': 5.6},
    {'name': 'LOD3', 'desc': '详细立面\n(Detailed facade)', 'x': 9.0, 'w': 1.8, 'h': 4.0, 'color': '#9B59B6', 'light': '#E8DAEF', 'y_text': 5.8, 'x_text': 9.9},
    {'name': 'LOD4', 'desc': '室内结构\n(Interior structure)', 'x': 11.5, 'w': 1.8, 'h': 4.5, 'color': '#E74C3C', 'light': '#FADBD8', 'y_text': 6.6, 'x_text': 11.5},
]

for lod in lods:
    x, w, h = lod['x'], lod['w'], lod['h']
    base_y = 1.2
    
    if lod['name'] == 'LOD0':
        rect = Rectangle((x, base_y - 0.05), w, 0.1, facecolor=lod['light'],
                         edgecolor=lod['color'], linewidth=2.5, zorder=3)
        ax.add_patch(rect)
    else:
        rect = Rectangle((x, base_y), w, h, facecolor=lod['light'],
                         edgecolor=lod['color'], linewidth=2.5, zorder=3)
        ax.add_patch(rect)
        
        if lod['name'] in ['LOD2', 'LOD3', 'LOD4']:
            roof_h = 0.5 if lod['name'] == 'LOD2' else 0.6
            roof = Polygon([(x, base_y + h), (x + w/2, base_y + h + roof_h), (x + w, base_y + h)],
                           facecolor=lod['light'], edgecolor=lod['color'], linewidth=2, zorder=3)
            ax.add_patch(roof)
            h += roof_h
        
        if lod['name'] in ['LOD3', 'LOD4']:
            for wy in np.arange(base_y + 0.6, base_y + h - 0.3, 0.7):
                for wx in [x + 0.3, x + w - 0.5]:
                    win = Rectangle((wx, wy), 0.25, 0.4, facecolor='white',
                                    edgecolor=lod['color'], linewidth=1, zorder=4)
                    ax.add_patch(win)
            door = Rectangle((x + w/2 - 0.2, base_y), 0.4, 0.6, facecolor='white',
                            edgecolor=lod['color'], linewidth=1.5, zorder=4)
            ax.add_patch(door)
        
        if lod['name'] == 'LOD4':
            for fy in np.arange(base_y + 1.5, base_y + h - 0.3, 1.2):
                ax.plot([x + 0.1, x + w - 0.1], [fy, fy], '--', color=lod['color'],
                        linewidth=1, alpha=0.5, zorder=4)
                ax.text(x + w/2, fy + 0.15, '楼层', ha='center', va='bottom',
                        fontsize=7, color=lod['color'], alpha=0.7)
    
    # 标签框位置
    lx = lod['x_text']
    ly = lod['y_text']
    
    # 引线从建筑物顶部到标签
    top_y = base_y + h if lod['name'] != 'LOD0' else base_y
    ax.plot([x + w/2, lx], [top_y + 0.05, ly - 0.35], color=lod['color'],
            linewidth=1.5, zorder=5, alpha=0.7)
    
    ax.text(lx, ly, f"{lod['name']}\n{lod['desc']}",
            ha='center', va='center', fontsize=10, fontweight='bold', color=lod['color'],
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=lod['color'],
                     linewidth=1.5, alpha=0.95), zorder=6)

# 精度递增箭头（放在建筑物上方，不遮挡）
ax.annotate('', xy=(12.5, 6.9), xytext=(2.0, 6.9),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2.5,
                           connectionstyle="arc3,rad=0"))
ax.text(7.25, 7.15, '几何细节与语义丰富度递增 →', ha='center', va='bottom',
        fontsize=11, color='#E74C3C', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(7, 0.35, 'CityGML LOD0–LOD4 定义了从二维轮廓到室内结构的多级细节层次，\nLOD越高，几何复杂度与语义信息越丰富，适用于不同应用场景。',
        ha='center', va='center', fontsize=10, color='#5D6D7E',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#F8F9FA', edgecolor='#D5D8DC'))

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图12_CityGML_LOD层级.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图12_CityGML_LOD层级.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("图12 v2 保存完成")
