#!/usr/bin/env python3
"""
图11: 三维建筑物提取技术路线
修复v3: 汇聚箭头精确连接框边缘中心
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(8, 8.5, '图11 三维建筑物提取技术路线', ha='center', va='center',
        fontsize=16, fontweight='bold', color='#2C3E50')

C_STEREO = '#3498DB'
C_LIDAR = '#27AE60'
C_NERF = '#E67E22'
C_2D3D = '#9B59B6'
C_ROAD = '#E74C3C'
C_CENTER = '#C0392B'

def draw_box(ax, cx, cy, w, h, label, color, text_color='white', fontsize=10, linewidth=2):
    box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                         boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor=color, edgecolor='white', linewidth=linewidth, alpha=0.9, zorder=3)
    ax.add_patch(box)
    ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', zorder=4)
    return (cx, cy, w, h)

def draw_arrow(ax, x1, y1, x2, y2, color='#555', lw=2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                               connectionstyle="arc3,rad=0"))

# 列标题
col_titles = ['立体影像重建', 'LiDAR点云处理', '神经辐射场(NeRF)', '2D转3D融合']
col_x = [2.5, 6.0, 9.5, 13.0]
for x, title in zip(col_x, col_titles):
    ax.text(x, 7.8, title, ha='center', va='center', fontsize=11,
            fontweight='bold', color='#2C3E50',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ECF0F1', edgecolor='#BDC3C7', linewidth=1.5))

# ========== Column 1: 立体影像 ==========
cx = col_x[0]
r1 = draw_box(ax, cx, 6.8, 2.0, 0.65, '立体影像/多视角影像', C_STEREO, fontsize=9.5)
r2 = draw_box(ax, cx, 5.7, 2.0, 0.65, '立体匹配(SGM/MVS)', C_STEREO, fontsize=9.5)
r3 = draw_box(ax, cx, 4.6, 2.0, 0.65, 'DSM/DTM生成', '#85C1E9', fontsize=10)
draw_arrow(ax, cx, 6.8 - 0.32, cx, 5.7 + 0.32, C_STEREO)
draw_arrow(ax, cx, 5.7 - 0.32, cx, 4.6 + 0.32, C_STEREO)

# ========== Column 2: LiDAR ==========
cx = col_x[1]
r4 = draw_box(ax, cx, 6.8, 2.0, 0.65, 'LiDAR点云数据', C_LIDAR, fontsize=10)
r5 = draw_box(ax, cx, 5.7, 2.0, 0.65, '点云分割(PointNet++)', C_LIDAR, fontsize=9)
r6 = draw_box(ax, cx, 4.6, 2.0, 0.65, '点云实例分割', '#58D68D', fontsize=10)
r7 = draw_box(ax, cx, 3.5, 2.0, 0.65, '三维实例标签', '#58D68D', fontsize=10)
draw_arrow(ax, cx, 6.8 - 0.32, cx, 5.7 + 0.32, C_LIDAR)
draw_arrow(ax, cx, 5.7 - 0.32, cx, 4.6 + 0.32, C_LIDAR)
draw_arrow(ax, cx, 4.6 - 0.32, cx, 3.5 + 0.32, C_LIDAR)

# ========== Column 3: NeRF ==========
cx = col_x[2]
r8 = draw_box(ax, cx, 6.8, 2.0, 0.65, '多视角影像序列', C_NERF, fontsize=10)
r9 = draw_box(ax, cx, 5.7, 2.0, 0.65, 'NeRF / 3D GS\n神经辐射场', C_NERF, fontsize=9.5)
r10 = draw_box(ax, cx, 4.6, 2.0, 0.65, '隐式三维场景表示', '#F8C471', fontsize=10)
r11 = draw_box(ax, cx, 3.5, 2.0, 0.65, '三维几何网格提取', '#F8C471', fontsize=10)
draw_arrow(ax, cx, 6.8 - 0.32, cx, 5.7 + 0.32, C_NERF)
draw_arrow(ax, cx, 5.7 - 0.32, cx, 4.6 + 0.32, C_NERF)
draw_arrow(ax, cx, 4.6 - 0.32, cx, 3.5 + 0.32, C_NERF)

# ========== Column 4: 2D转3D ==========
cx = col_x[3]
r12 = draw_box(ax, cx, 6.8, 2.0, 0.65, '二维道路中心线', C_2D3D, fontsize=10)
r13 = draw_box(ax, cx, 5.7, 2.0, 0.65, 'DSM高程叠加', '#AF7AC5', fontsize=10)
r14 = draw_box(ax, cx, 4.6, 2.0, 0.65, '坡度/曲率属性计算', '#AF7AC5', fontsize=10)
r15 = draw_box(ax, cx, 3.5, 2.0, 0.65, '三维道路网络图', C_ROAD, fontsize=10)
draw_arrow(ax, cx, 6.8 - 0.32, cx, 5.7 + 0.32, C_2D3D)
draw_arrow(ax, cx, 5.7 - 0.32, cx, 4.6 + 0.32, C_2D3D)
draw_arrow(ax, cx, 4.6 - 0.32, cx, 3.5 + 0.32, C_2D3D)

# ========== 中心: 三维建筑物矢量模型 ==========
center = draw_box(ax, 8.0, 2.3, 3.0, 0.8, '三维建筑物\n矢量模型', C_CENTER, fontsize=12, linewidth=3)
cx_c, cy_c, cw_c, ch_c = center

# 从各列到中心的精确箭头（连接到中心框的对应边缘中心）
# 立体影像→中心 (从DSM/DTM的底边中心出发，到中心框顶边偏左)
source = r3  # DSM/DTM
src_x = source[0]
src_y = source[1] - source[3]/2  # 底边中心
dst_x = cx_c - cw_c/4
dst_y = cy_c + ch_c/2  # 顶边
ax.annotate('', xy=(dst_x, dst_y), xytext=(src_x, src_y),
            arrowprops=dict(arrowstyle='->', color=C_STEREO, lw=2, connectionstyle="arc3,rad=-0.1"))
ax.text(4.8, 3.3, '高度信息', ha='center', va='center', fontsize=9, color=C_STEREO, fontweight='bold')

# LiDAR→中心 (从三维实例标签的底边中心)
source = r7
src_x = source[0]
src_y = source[1] - source[3]/2
dst_x = cx_c - cw_c/8
dst_y = cy_c + ch_c/2
ax.annotate('', xy=(dst_x, dst_y), xytext=(src_x, src_y),
            arrowprops=dict(arrowstyle='->', color=C_LIDAR, lw=2, connectionstyle="arc3,rad=-0.05"))
ax.text(6.8, 2.85, '几何约束', ha='center', va='center', fontsize=9, color=C_LIDAR, fontweight='bold')

# NeRF→中心 (从三维几何网格的底边中心)
source = r11
src_x = source[0]
src_y = source[1] - source[3]/2
dst_x = cx_c + cw_c/8
dst_y = cy_c + ch_c/2
ax.annotate('', xy=(dst_x, dst_y), xytext=(src_x, src_y),
            arrowprops=dict(arrowstyle='->', color=C_NERF, lw=2, connectionstyle="arc3,rad=0.05"))
ax.text(9.2, 2.85, '表面重建', ha='center', va='center', fontsize=9, color=C_NERF, fontweight='bold')

# 2D转3D→中心 (从三维道路的底边中心)
source = r15
src_x = source[0]
src_y = source[1] - source[3]/2
dst_x = cx_c + cw_c/4
dst_y = cy_c + ch_c/2
ax.annotate('', xy=(dst_x, dst_y), xytext=(src_x, src_y),
            arrowprops=dict(arrowstyle='->', color=C_2D3D, lw=2, connectionstyle="arc3,rad=0.1"))
ax.text(11.2, 3.3, '矢量融合', ha='center', va='center', fontsize=9, color=C_2D3D, fontweight='bold')

# 底部: 二维分割+高度融合
draw_box(ax, 4.5, 1.1, 2.2, 0.6, '二维分割\n+高度融合', '#AF7AC5', fontsize=9.5)
ax.annotate('', xy=(cx_c - 0.8, cy_c - ch_c/2), xytext=(4.5 + 1.1, 1.1 + 0.3),
            arrowprops=dict(arrowstyle='<->', color='#7F8C8D', lw=1.8, connectionstyle="arc3,rad=0.1"))
ax.text(6.0, 1.55, '双向融合', ha='center', va='bottom', fontsize=9, color='#7F8C8D', fontweight='bold')

# 底部注释
ax.text(8.0, 0.35, '四条技术路线最终汇聚为统一的三维城市模型，分别侧重几何精度、点云密度、视觉真实感与语义一致性。',
        ha='center', va='center', fontsize=10, color='#5D6D7E',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F9FA', edgecolor='#D5D8DC'))

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图11_三维建筑物提取技术路线.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图11_三维建筑物提取技术路线.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("图11 v3 保存完成")
