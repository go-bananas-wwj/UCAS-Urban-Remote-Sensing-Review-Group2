#!/usr/bin/env python3
"""
图4: U-Net与DeepLabV3+编码器-解码器架构简图
修复v3: Backbone到Low-Level Features箭头精确连接框边中心
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
fig.suptitle('(a) U-Net 编码器-解码器架构                    (b) DeepLabV3+ 架构',
             fontsize=14, fontweight='bold', y=0.98)

C_INPUT = '#85929E'
C_CONV = ['#E74C3C', '#E67E22', '#F39C12', '#F1C40F', '#27AE60']
C_SKIP = '#8E44AD'
C_ASPP = '#3498DB'
C_DECODER = '#E67E22'
C_OUTPUT = '#27AE60'
C_LOWLEVEL = '#1ABC9C'
C_BACKBONE = '#9B59B6'

def draw_box(ax, x, y, w, h, label, color, text_color='white', fontsize=10, zorder=3):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9, zorder=zorder)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', zorder=zorder+1)
    return (x, y, w, h)

def draw_arrow(ax, x1, y1, x2, y2, color='#555', style='->', lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                               connectionstyle="arc3,rad=0"))

# ========== (a) U-Net ==========
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 12)
ax1.axis('off')

enc_x, dec_x = 2.5, 7.5
box_w, box_h = 2.2, 0.9
y_positions = [10.5, 9.0, 7.5, 6.0, 4.5]
enc_labels = ['Input\n影像输入', 'Conv Block 1\n64通道', 'Conv Block 2\n128通道', 
              'Conv Block 3\n256通道', 'Conv Block 4\n512通道']
dec_labels = ['Output\n分割结果', 'Up-Conv 1\n64通道', 'Up-Conv 2\n128通道',
              'Up-Conv 3\n256通道', 'Up-Conv 4\n512通道']

for i, y in enumerate(y_positions):
    c = C_INPUT if i == 0 else C_CONV[i-1]
    draw_box(ax1, enc_x, y, box_w, box_h, enc_labels[i], c, fontsize=9 if i==0 else 9.5)
    c = C_OUTPUT if i == 0 else C_CONV[i-1]
    draw_box(ax1, dec_x, y, box_w, box_h, dec_labels[i], c, fontsize=9 if i==0 else 9.5)

bot_y = 3.0
draw_box(ax1, enc_x, bot_y, box_w, box_h, 'Bottleneck\n1024通道', C_CONV[4], fontsize=9.5)

for i in range(len(y_positions)):
    y1 = y_positions[i] - box_h/2
    if i < len(y_positions) - 1:
        y2 = y_positions[i+1] + box_h/2
    else:
        y2 = bot_y + box_h/2
    draw_arrow(ax1, enc_x, y1, enc_x, y2)

draw_arrow(ax1, enc_x, y_positions[-1] - box_h/2, enc_x, bot_y + box_h/2)

# Bottleneck到解码器
mid_y = (bot_y + y_positions[-1]) / 2
ax1.annotate('', xy=(dec_x, y_positions[-1] + box_h/2), xytext=(enc_x, bot_y - box_h/2),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.8, connectionstyle="arc3,rad=0"))

for i in range(len(y_positions)-1, 0, -1):
    y1 = y_positions[i] - box_h/2
    y2 = y_positions[i-1] + box_h/2
    draw_arrow(ax1, dec_x, y1, dec_x, y2)

for i in range(1, len(y_positions)):
    y = y_positions[i]
    x1 = enc_x + box_w/2
    x2 = dec_x - box_w/2
    ax1.annotate('', xy=(x2 - 0.02, y), xytext=(x1 + 0.02, y),
                arrowprops=dict(arrowstyle='->', color=C_SKIP, lw=1.5, linestyle='--'))

ax1.text(5.0, 2.0, '上采样 + 特征融合\n(Skip Connection)', ha='center', va='center',
         fontsize=10, color=C_SKIP, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=C_SKIP, alpha=0.9))

# ========== (b) DeepLabV3+ ==========
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 12)
ax2.axis('off')

modules = [
    (5.0, 10.5, 'Backbone\n(ResNet / Xception)', C_BACKBONE, 3.5),
    (5.0, 9.0, 'ASPP 模块\n(1×1Conv + 3×3 Atrous Conv ×3 + Image Pooling)', C_ASPP, 4.5),
    (5.0, 7.5, 'Decoder\n(1×1Conv + 3×3 Conv)', C_DECODER, 3.0),
    (5.0, 6.0, '4× Upsampling\n双线性插值', '#F39C12', 3.0),
    (5.0, 4.5, 'Output\n语义分割图', C_OUTPUT, 3.0),
]

mod_rects = []
for x, y, label, color, w in modules:
    mod_rects.append(draw_box(ax2, x, y, w, 0.85, label, color, fontsize=9))

for i in range(len(modules) - 1):
    y1 = modules[i][1] - 0.85/2
    y2 = modules[i+1][1] + 0.85/2
    draw_arrow(ax2, modules[i][0], y1, modules[i+1][0], y2)

# Low-Level Features (左侧，精确箭头连接)
ll_x, ll_y, ll_w, ll_h = 1.8, 7.5, 2.4, 0.85
draw_box(ax2, ll_x, ll_y, ll_w, ll_h, 'Low-Level Features\n(浅层细节)', C_LOWLEVEL, fontsize=9)

# Backbone底边中心 → 到Low-Level Features顶边中心（精确）
backbone_rect = mod_rects[0]  # (x, y, w, h)
backbone_bottom_x = backbone_rect[0]
backbone_bottom_y = backbone_rect[1] - backbone_rect[3]/2

# 从Backbone底边中心引到Low-Level Features顶边中心
ax2.annotate('', xy=(ll_x, ll_y + ll_h/2), xytext=(backbone_bottom_x, backbone_bottom_y),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5,
                           connectionstyle="arc3,rad=0.15"))

# Low-Level Features右边中心 → Decoder左边中心
ll_right_x = ll_x + ll_w/2
ll_right_y = ll_y
decoder_rect = mod_rects[2]
dec_left_x = decoder_rect[0] - decoder_rect[2]/2
dec_left_y = decoder_rect[1]
ax2.annotate('', xy=(dec_left_x, dec_left_y), xytext=(ll_right_x, ll_right_y),
            arrowprops=dict(arrowstyle='->', color=C_LOWLEVEL, lw=1.8, linestyle='--'))
ax2.text((ll_right_x + dec_left_x)/2, 7.95, '跳跃连接', ha='center', va='bottom',
         fontsize=8, color=C_LOWLEVEL, fontweight='bold')

ax2.text(5.0, 1.5, '注：ASPP通过多个不同采样率的空洞卷积\n并行捕获多尺度上下文，Decoder融合浅层细节改善边界。',
         ha='center', va='center', fontsize=9, color='#5D6D7E',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F9FA', edgecolor='#D5D8DC'))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图4_编码器解码器架构简图.png',
            dpi=300, bbox_inches='tight', pad_inches=0.15, facecolor='white')
plt.savefig('/workspace/other/yaogan/05_图表素材/v2/图4_编码器解码器架构简图.pdf',
            bbox_inches='tight', pad_inches=0.15, facecolor='white')
print("图4 v3 保存完成")
