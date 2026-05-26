# TopoRF-Net: Topology-Aware Road Segmentation in Multi-Resolution Remote Sensing via Multi-Receptive Field Adaptation

**Authors:** Junjie Fu, Chenliang Wang, Hongchen Lv, Hao Lu, Wenjiao Shi, Xuefeng Liao  
**Affiliations:** SuperMap Software Co., Wenzhou University of Technology, CAS  
**Venue:** Sensors 2025, 25, 7428  
**DOI:** https://doi.org/10.3390/s25247428

---

## 一、研究背景与动机

### 1.1 核心问题
道路在遥感影像中具有**稀疏分布、细长结构、复杂拓扑**的形态学特征。现有方法主要存在两大缺陷：
1. **像素级精度vs拓扑完整性矛盾**：现有方法聚焦像素级分类精度，忽视道路网络的拓扑完整性，导致预测结果频繁出现断裂和遗漏
2. **多分辨率感受野失配**：不同分辨率影像中道路尺度差异巨大，固定感受野难以同时捕捉主干道路和细小分支

### 1.2 关键观察
- 大尺度粗粒度结构决定全局布局，小尺度细粒度分支支撑局部连续性
- 忽略这种层次性会导致碎片化或不一致的预测
- 脆弱路段（狭窄弯道、遮挡区域）易被遗漏，进一步损害网络连通性

---

## 二、方法详解

### 2.1 整体架构
基于MiT (Mix Transformer) backbone，包含三大核心组件：

#### (1) Multi-Receptive Field Enhancement (MRFE) Module
插入每个Transformer block后的轻量级多感受野模块：
- **结构**：多头注意力 + 深度可分离卷积组（3×3, 5×5, 7×7并行分支）+ 残差路径
- **功能**：以极少的参数量和计算开销，实现多尺度上下文建模
- **优势**：增强编码器对细长道路特征的敏感性

#### (2) Connectivity-Inherent Decoder (CI-Decoder)
- **动态蛇形卷积模块 (DSConv)**：三个方向性模块
  - DSConv-X：感知水平方向道路曲线
  - DSConv-Y：感知垂直方向道路曲线
  - Conv-XY：感知交叉路口特征
- **局部连接的特征感知卷积** + **全局特征聚合**
- **功能**：显式感知道路曲线和交叉路口的几何特征，保持道路结构连续性

#### (3) Connectivity-Constrained Training Strategy
- **拓扑一致性损失 (Topology Loss)**：与Dice Loss和Cross-Entropy Loss联合优化
- **功能**：显式引导模型在训练过程中优先恢复道路主干结构
- **设计思想**：通过形态学操作和连通性约束，惩罚导致网络断裂的预测

### 2.2 创新点总结
| 组件 | 解决的问题 | 技术方案 |
|------|-----------|---------|
| MRFE | 多尺度道路特征 | 并行多尺寸深度可分离卷积 |
| CI-Decoder | 拓扑断裂 | 方向性蛇形卷积 + 全局聚合 |
| Topology Loss | 结构不连续 | 连通性约束 + 形态学先验 |

---

## 三、实验结果

### 3.1 数据集
- **DeepGlobe-Road**：6226张1024×1024 VHR图像
- **Massachusetts Roads**：1108张1500×1500航拍图像

### 3.2 定量结果

**DeepGlobe-Road：**
- OA: **98.57%**
- IoU: **69.76%**
- F1-score: **82.18%**
- Precision: **85.50%**
- Recall: **79.12%**

**Massachusetts Roads：**
- OA: **96.65%**
- IoU: **59.68%**
- F1-score: **74.75%**
- Precision: **77.98%**
- Recall: **71.77%**

### 3.3 对比方法
与UNet, DeepLabV3+, D-LinkNet, HRNet, Swin-UNet等SOTA方法对比，TopoRF-Net在精度和连通性指标上均显著优于现有方法，同时保持了较好的参数效率和推理性能。

---

## 四、精读收获

### 4.1 综述写作价值
1. **拓扑保持的典型案例**：TopoRF-Net是CNN/Transformer混合架构中显式引入拓扑约束的代表性工作，适合放在"深度学习I: CNN时代"到"深度学习II: Transformer时代"的过渡章节。
2. **多分辨率问题的系统解决方案**：MRFE + CI-Decoder + Topology Loss的三层设计提供了一个完整的技术框架，可用于综述中讨论"多尺度特征融合与拓扑保持"子主题。
3. **对比SAM系列方法**：TopoRF-Net是专用监督方法，在DeepGlobe上IoU 69.76%，可作为与SAM-Road (专用两阶段方法) 和SegEarth-OV3 (零样本SAM3方法) 对比的基准。

### 4.2 关键引用点
- MiT backbone + 多感受野增强：轻量级Transformer在遥感道路提取中的有效应用
- 方向性蛇形卷积：针对道路曲线几何特征的结构化解码器设计
- Topology Loss：将连通性约束从后处理（如CRF）前移到训练阶段
- 在DeepGlobe和Massachusetts上的SOTA性能验证了方法的有效性

### 4.3 与其他文献关联
- **SAM-Road++**：同样关注道路拓扑，但采用SAM-based两阶段策略（几何提取+图网络拓扑恢复）
- **TopoRF-Net**：在单阶段分割框架内引入拓扑约束，更轻量高效
- **Zao & Shi (Richer U-Net)**：引用的相关工作，也关注道路边界细节
- **DeH4R (2025)**：解耦混合架构，可与TopoRF-Net的多感受野策略形成对比

### 4.4 方法局限
- 仅在两个道路数据集上验证，缺乏建筑物提取任务的验证
- Topology Loss的具体实现细节（形态学操作类型、连通性度量）描述不够详细
- 与最新的SAM-based方法（如SAM-Road++）缺乏直接对比
