# 遥感影像路网与建筑物提取方法综述

中国科学院大学 · 城市环境遥感 · 第二组综述论文

## 论文信息

- **题目**：遥感影像路网与建筑物提取方法综述
- **课程**：城市环境遥感
- **单位**：中国科学院大学
- **小组**：第二组

## 仓库结构

```
.
├── 01_文献材料/          # 参考文献（中文+英文PDF）
├── 02_综述报告/          # 论文正文（Markdown + DOCX）
│   ├── 遥感影像路网与建筑物提取方法综述.docx      # 最终版（格式标准化）
│   ├── 综述正文.md
│   └── 综述正文_for_docx.md
├── 05_图表素材/          # 论文图表（自绘+论文原图）
│   ├── 图1_技术演进时间线.png
│   ├── 图3_OBIA多尺度分割.png
│   ├── 图4_编码器解码器架构简图.png
│   ├── 图5_SAM系列架构演进.png
│   ├── 图11_三维建筑物提取技术路线.png
│   ├── 图12_CityGML_LOD层级.png
│   ├── 表2_CNN时代方法对比.png
│   ├── 表3_SAM系列方法对比.png
│   ├── 表4_多源融合方法对比.png
│   └── ...
└── scripts/              # 图表绘制与文档处理脚本
    ├── draw_fig*.py      # 自绘图表脚本（Matplotlib）
    ├── draw_table*.py    # 表格绘制脚本
    ├── generate_docx.py  # DOCX生成脚本
    ├── renumber_figures.py  # 图号重排脚本
    └── standardize_format.py # 格式标准化脚本
```

## 论文内容概要

本文系统综述了遥感影像中路网提取与建筑物提取两大任务的技术演进，涵盖：

1. **传统图像处理方法**（阈值分割、边缘检测、形态学操作）
2. **面向对象影像分析（OBIA）**
3. **机器学习时代**（SVM、随机森林、CRFs）
4. **深度学习时代**
   - CNN 编码器-解码器架构（U-Net、SegNet、DeepLab 等）
   - Vision Transformer（SegFormer、Swin Transformer 等）
5. **基础模型时代**
   - SAM 系列在遥感领域的适配（SAM-Road、Road-SAM Adapter、SegEarth-OV 等）
   - 从视觉提示到概念提示的演进
6. **三维建筑物提取**（多视角立体、LiDAR、倾斜摄影）

## 图表清单

| 编号 | 内容 | 来源 |
|------|------|------|
| 图1 | 技术演进时间线 | 自绘 |
| 图2 | 传统图像处理方法示例 | 论文原图 (E06) |
| 图3 | OBIA多尺度分割 | 自绘 |
| 图4 | 编码器-解码器架构 | 自绘 |
| 图5 | SVM→U-Net+CRFs演进 | 论文原图 (C10) |
| 图6 | TopoRF-Net多尺度全局对比 | 论文原图 (E08) |
| 图7 | CFENet细节 | 论文原图 (E05) |
| 图8 | SegFormer架构 | 论文原图 (E10) |
| 图9 | Road-SAM Adapter | 论文原图 (E12) |
| 图10 | SAM-Road效果 | 论文原图 (E01) |
| 图11 | SAM 3概念提示 | 论文原图 (E04) |
| 图12 | SegEarth-OV3零样本分割 | 论文原图 (E03) |
| 图13 | SAM系列架构演进 | 自绘 |
| 图14 | 三维建筑物提取路线 | 自绘 |
| 图15 | CityGML LOD层级 | 自绘 |
| 表2 | CNN时代方法对比 | 自绘 |
| 表3 | SAM系列方法对比 | 自绘 |
| 表4 | 多源融合方法对比 | 自绘 |

## 技术栈

- **图表绘制**：Python + Matplotlib（字体：Noto Sans CJK JP）
- **文档生成**：Python + python-docx
- **格式标准化**：自定义 DOCX 格式脚本

## 使用说明

```bash
# 生成/更新自绘图表
python scripts/draw_fig1_timeline.py
python scripts/draw_fig3obia.py
# ... etc

# 生成 DOCX
python scripts/generate_docx.py

# 格式标准化
python scripts/standardize_format.py
```
