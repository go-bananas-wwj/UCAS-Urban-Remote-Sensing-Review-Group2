#!/usr/bin/env python3
"""
图5: SAM系列架构演进
修复v3: SAM(2023)分叉箭头从框边中心精确引出/汇入
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

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(8, 9.6, '图5 SAM系列架构演进：从视觉提示分割到概念提示分割',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#2C3E50')

C_ENC = '#9B59B6'
C_PROMPT = '#3498DB'
C_MASK = '#E67E22'
C_OUT = '#27AE60'
C_TRACK = '#E74C3C'
C_DET = '#2980B9'

def draw_box(ax, cx, cy, w, h, label, color, text_color='white', fontsize=10):
    box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                         boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor=color, edgecolor='white', linewidth=2, alpha=0.92, zorder=3)
    ax.add_patch(box)
    ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', zorder=4)
    return (cx, cy, w, h)

def draw_arrow(ax, x1, y1, x2, y2, color='#555', lw=2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                               connectionstyle="arc3,rad=0"))

# ========== Column 1: SAM ==========
cx = 3.0
ax.text(cx, 8.8, 'SAM (2023)', ha='center', va='center', fontsize=14, fontweight='bold', color='#8E44AD')
ax.text(cx, 8.3, 'Promptable Visual Segmentation', ha='center', va='center', fontsize=9, color='#7F8C8D')

b1 = draw_box(ax, cx, 7.2, 3.0, 0.8, 'Image Encoder\n(ViT-based)', C_ENC, fontsize=10)
b2 = draw_box(ax, cx - 0.8, 5.8, 1.4, 0.8, 'Prompt Encoder\n(点/框/掩码)', C_PROMPT, fontsize=9)
b3 = draw_box(ax, cx + 0.8, 5.8, 1.4, 0.8, 'Mask Decoder\n(轻量Transformer)', C_MASK, fontsize=9)
b4 = draw_box(ax, cx, 4.3, 3.0, 0.8, '输出：单目标分割掩码\n(O-H-M三选一)', C_OUT, fontsize=10)

# Image Encoder底边中心 → 分叉到Prompt/Mask顶边中心
enc_bottom_y = b1[1] - b1[3]/2
prompt_top_y = b2[1] + b2[3]/2
mask_top_y = b3[1] + b3[3]/2
mid_y = (enc_bottom_y + prompt_top_y) / 2

# 先垂直向下到中间点，再分叉
ax.plot([cx, cx], [enc_bottom_y, mid_y], color=C_ENC, linewidth=1.8, zorder=3)
ax.plot([cx, b2[0]], [mid_y, prompt_top_y], color=C_ENC, linewidth=1.8, zorder=3)
ax.plot([cx, b3[0]], [mid_y, mask_top_y], color=C_ENC, linewidth=1.8, zorder=3)
ax.annotate('', xy=(b2[0], prompt_top_y), xytext=(cx, mid_y),
            arrowprops=dict(arrowstyle='->', color=C_ENC, lw=1.5))
ax.annotate('', xy=(b3[0], mask_top_y), xytext=(cx, mid_y),
            arrowprops=dict(arrowstyle='->', color=C_ENC, lw=1.5))

# Prompt/Mask底边中心 → 汇聚到输出顶边中心
prompt_bottom_y = b2[1] - b2[3]/2
mask_bottom_y = b3[1] - b3[3]/2
out_top_y = b4[1] + b4[3]/2
mid_y2 = (prompt_bottom_y + out_top_y) / 2

ax.plot([b2[0], b2[0]], [prompt_bottom_y, mid_y2], color=C_PROMPT, linewidth=1.8, zorder=3)
ax.plot([b3[0], b3[0]], [mask_bottom_y, mid_y2], color=C_MASK, linewidth=1.8, zorder=3)
ax.plot([b2[0], b4[0]], [mid_y2, out_top_y], color='#555', linewidth=1.8, zorder=3)
ax.plot([b3[0], b4[0]], [mid_y2, out_top_y], color='#555', linewidth=1.8, zorder=3)
ax.annotate('', xy=(b4[0], out_top_y), xytext=(b2[0], mid_y2),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
ax.annotate('', xy=(b4[0], out_top_y), xytext=(b3[0], mid_y2),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))

ax.text(cx, 2.5, '局限：仅支持视觉提示\n每次仅分割单个目标',
        ha='center', va='center', fontsize=9.5, color='#C0392B',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.5, alpha=0.9))

# ========== Column 2: SAM-Road++ ==========
cx = 8.0
ax.text(cx, 8.8, 'SAM-Road++ (2024)', ha='center', va='center', fontsize=14, fontweight='bold', color='#E67E22')
ax.text(cx, 8.3, 'Geometry + Topology Two-Stage', ha='center', va='center', fontsize=9, color='#7F8C8D')

b5 = draw_box(ax, cx, 7.2, 3.2, 0.8, 'Stage 1: SAM几何提取\n分割候选道路 + 节点检测', C_ENC, fontsize=10)
b6 = draw_box(ax, cx, 5.8, 3.2, 0.8, 'Stage 2: Graph Network拓扑恢复\n节点引导重采样 + Extended-Line', C_PROMPT, fontsize=9.5)
b7 = draw_box(ax, cx, 4.3, 3.2, 0.8, '输出：道路网络矢量图\n(拓扑连通的道路图)', C_OUT, fontsize=10)

draw_arrow(ax, cx, 7.2 - 0.4, cx, 5.8 + 0.4, C_ENC)
draw_arrow(ax, cx, 5.8 - 0.4, cx, 4.3 + 0.4, C_PROMPT)

ax.text(cx, 2.5, '创新：SAM零样本分割 + 专用拓扑恢复\n兼顾效率与连通性',
        ha='center', va='center', fontsize=9.5, color='#D35400',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FDEBD0', edgecolor='#E67E22', linewidth=1.5, alpha=0.9))

# ========== Column 3: SAM 3 ==========
cx = 13.0
ax.text(cx, 8.8, 'SAM 3 (2025)', ha='center', va='center', fontsize=14, fontweight='bold', color='#27AE60')
ax.text(cx, 8.3, 'Promptable Concept Segmentation', ha='center', va='center', fontsize=9, color='#7F8C8D')

b8 = draw_box(ax, cx, 7.2, 3.0, 0.8, 'Perception Encoder\n(共享视觉主干)', C_ENC, fontsize=10)
b9 = draw_box(ax, cx - 0.85, 5.8, 1.4, 0.8, 'Detector\n(DETR-based)', C_DET, fontsize=9)
b10 = draw_box(ax, cx + 0.85, 5.8, 1.4, 0.8, 'Tracker\n(SAM 2-based)', C_TRACK, fontsize=9)
b11 = draw_box(ax, cx, 4.5, 3.0, 0.7, '统一输出：实例掩码 + 语义分割 + 时序追踪', C_OUT, fontsize=9.5)
b12 = draw_box(ax, cx, 3.3, 3.0, 0.7, 'Presence Head (核心创新)\n解耦识别与定位', '#E74C3C', fontsize=10)

# Perception Encoder底边中心 → 分叉到Detector/Tracker顶边中心
enc3_bottom_y = b8[1] - b8[3]/2
det_top_y = b9[1] + b9[3]/2
track_top_y = b10[1] + b10[3]/2
mid_y3 = (enc3_bottom_y + det_top_y) / 2

ax.plot([cx, cx], [enc3_bottom_y, mid_y3], color=C_ENC, linewidth=1.8, zorder=3)
ax.plot([cx, b9[0]], [mid_y3, det_top_y], color=C_ENC, linewidth=1.8, zorder=3)
ax.plot([cx, b10[0]], [mid_y3, track_top_y], color=C_ENC, linewidth=1.8, zorder=3)
ax.annotate('', xy=(b9[0], det_top_y), xytext=(cx, mid_y3),
            arrowprops=dict(arrowstyle='->', color=C_ENC, lw=1.5))
ax.annotate('', xy=(b10[0], track_top_y), xytext=(cx, mid_y3),
            arrowprops=dict(arrowstyle='->', color=C_ENC, lw=1.5))

# Detector/Tracker底边中心 → 汇聚到统一输出顶边中心
det_bottom_y = b9[1] - b9[3]/2
track_bottom_y = b10[1] - b10[3]/2
unified_top_y = b11[1] + b11[3]/2
mid_y4 = (det_bottom_y + unified_top_y) / 2

ax.plot([b9[0], b9[0]], [det_bottom_y, mid_y4], color=C_DET, linewidth=1.8, zorder=3)
ax.plot([b10[0], b10[0]], [track_bottom_y, mid_y4], color=C_TRACK, linewidth=1.8, zorder=3)
ax.plot([b9[0], b11[0]], [mid_y4, unified_top_y], color='#555', linewidth=1.8, zorder=3)
ax.plot([b10[0], b11[0]], [mid_y4, unified_top_y], color='#555', linewidth=1.8, zorder=3)
ax.annotate('', xy=(b11[0], unified_top_y), xytext=(b9[0], mid_y4),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
ax.annotate('', xy=(b11[0], unified_top_y), xytext=(b10[0], mid_y4),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))

draw_arrow(ax, cx, 4.5 - 0.35, cx, 3.3 + 0.35, C_OUT)

ax.text(cx, 2.0, '突破：文本/图像概念提示\n检测+分割+追踪统一架构',
        ha='center', va='center', fontsize=9.5, color='#27AE60',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#D5F5E3', edgecolor='#27AE60', linewidth=1.5, alpha=0.9))

# ========== 演进箭头 ==========
for i in range(2):
    x1 = [3.0, 8.0][i] + 1.8
    x2 = [8.0, 13.0][i] - 1.8
    y = 6.2
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=3,
                               connectionstyle="arc3,rad=0"))
    mid = (x1 + x2) / 2
    ax.text(mid, y + 0.35, '演进', ha='center', va='bottom', fontsize=10, color='#7F8C8D', fontweight='bold')

plt.tight_layout()
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图5_SAM系列架构演进.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图5_SAM系列架构演进.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("图5 v3 保存完成")
