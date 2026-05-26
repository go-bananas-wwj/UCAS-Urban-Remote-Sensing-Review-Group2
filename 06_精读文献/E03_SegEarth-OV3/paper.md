# SegEarth-OV3: Exploring SAM 3 for Open-Vocabulary Semantic Segmentation in Remote Sensing Images

**Authors:** Kaiyu Li, Shengqi Zhang, Yujie Wang, et al. (Xi'an Jiaotong University)  
**Venue:** arXiv 2025 (v2 Apr 2026)  
**Code:** https://github.com/earth-insights/SegEarth-OV-3

---

## 一、研究背景与动机

### 1.1 现有问题
- **CLIP-based OVSS的局限**：现有训练无关开放词汇语义分割方法主要基于CLIP，但存在两个核心问题：(1) 粗粒度定位，边界模糊；(2) 复杂多阶段pipeline，需要特征对齐和模块组合。
- **遥感场景的特殊挑战**：遥感图像中存在大量密集小目标和广阔无定形背景，传统CLIP-based方法难以处理。
- **SAM 3的潜力**：SAM 3 (Carion et al., 2025) 是一个统一的分割与识别模型，支持promptable概念分割，但其零样本能力在遥感领域的适配尚未充分探索。

### 1.2 核心贡献
1. **双头掩码融合策略 (Dual-Head Mask Fusion)**：利用SAM 3的语义分割头处理"stuff"类（道路、裸地等无定形区域），利用Transformer decoder（实例头）处理"things"类（建筑物、车辆等可数目标），实现优势互补。
2. **存在性引导过滤 (Presence-Guided Filtering)**：利用SAM 3的presence head预测概念在图像中的存在概率，抑制无关类别，消除大词汇表vs局部patch导致的假阳性。
3. **扩展至开放词汇变化检测 (OVCD)**：提出联合实例级和像素级验证策略，解决双时相图像的配准误差和VLM识别不一致问题。

---

## 二、方法详解

### 2.1 SAM 3架构回顾
SAM 3包含三个解耦头：
- **Presence Head**：输出标量分数 $S_{pres} \in [0,1]$，表示概念在图像中的全局存在概率
- **Semantic Segmentation Head**：FCN风格的密集预测，输出语义概率图 $P_{sem} \in [0,1]^{H \times W}$
- **Transformer Decoder (Instance Head)**：基于query的模块，输出N个实例预测 $\{(P_{inst}^{(k)}, s_{conf}^{(k)})\}_{k=1}^N$

### 2.2 SegEarth-OV3 Pipeline

#### (1) 实例聚合 (Instance Aggregation)
将Transformer decoder输出的稀疏实例预测聚合成单一类别级地图：
$$P_{inst\_agg}(h,w) = \max_{k=1}^N \left( P_{inst}^{(k)}(h,w) \cdot s_{conf}^{(k)} \right)$$
有效解决了密集小目标簇的边界粘连问题。

#### (2) 双头掩码融合 (Dual-Head Mask Fusion)
采用max-fusion策略融合实例头和语义头：
$$P_{fused}(h,w) = \max\left( P_{sem}(h,w), P_{inst\_agg}(h,w) \right)$$
- 实例头擅长可数目标的精细边界
- 语义头保持无定形区域的全局连续性

#### (3) 存在性引导过滤 (Presence-Guided Filtering)
利用全局presence score进行软门控：
$$P_{final}^{(c)} = P_{fused}^{(c)} \cdot S_{pres}^{(c)}$$
有效抑制了词汇表中大量不存在类别的幻觉预测。

### 2.3 开放词汇变化检测扩展
- **Pixel-level Comparison**：利用SAM 3视觉编码器的密集特征计算余弦相似度，构建特征变化图 $F_{change}$
- **Instance-level Comparison**：将连续概率图转换为离散实例预测，通过形态学膨胀容忍配准漂移
- **联合验证**：仅当像素级和实例级同时确认变化时才判定为有效变化

---

## 三、实验结果

### 3.1 数据集
- **2D语义分割**：20个数据集（OpenEarthMap, LoveDA, iSAID, Potsdam, Vaihingen, WHU Building, Inria, DeepGlobe, Massachusetts, SpaceNet等）
- **变化检测**：LEVIR-CD, WHU-CD, S2Looking
- **3D分割**：STPLS3D

### 3.2 关键结果
- **遥感语义分割**（Table 1）：SegEarth-OV3平均mIoU达**53.4%**，超越最佳训练无关方法CorrCLIP (40.7%) **+12.7%**
- **建筑物提取IoU**（Table 2）：WHU Aerial 86.9%, WHU Sat.II 44.2%, Inria 72.4%, xBD 64.3%
- **道路提取IoU**（Table 2）：CHN6-CUG 49.6%, DeepGlobe 39.3%, Massachusetts 27.7%, SpaceNet 35.6%
- **高分数据集**（Table 3）：GF-7 Building 58.7%, Low-Grade Road 60.2%

### 3.3 消融实验（Table 4）
- Instance Only: LoveDA 32.2, Uavid 50.4
- Semantic Only: LoveDA 35.4, Uavid 47.1
- **SegEarth-OV3 (融合)**: LoveDA **47.4**, Uavid **54.7** → 双头融合显著优于任一单头

---

## 四、精读收获

### 4.1 综述写作价值
1. **SAM3在遥感中的标杆应用**：SegEarth-OV3是SAM 3在遥感领域的首个系统性探索，展示了foundation model在开放词汇遥感分割中的强大潜力。
2. **"Stuff-Things"二分策略**：遥感中的道路（无定形）和建筑物（可数）恰好对应SAM 3的双头设计，可作为综述中讨论SAM适配策略的经典案例。
3. **无需训练的零样本能力**：相比需要领域微调的CLIP-based方法，SegEarth-OV3完全无需训练即可达到SOTA，体现了大模型的范式转变。

### 4.2 关键引用点
- SAM 3的统一架构：presence head + semantic head + instance head 解耦设计
- 在Massachusetts道路数据集上IoU 27.7%（零样本无训练），虽低于监督学习方法但展示了通用性
- 建筑物提取表现更优（WHU Aerial 86.9%），说明SAM 3对"things"类更友好

### 4.3 局限与展望
- 道路提取IoU相对监督方法仍有差距，尤其是在Massachusetts等道路数据集上
- 需要针对遥感数据进一步微调以提升专用场景性能
- 未来可探索结合轻量级domain adapter进一步提升遥感道路/建筑物提取精度
