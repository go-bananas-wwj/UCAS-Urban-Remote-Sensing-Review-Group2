# SAM 3: Segment Anything with Concepts

**Authors:** Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, et al. (Meta Superintelligence Labs)  
**Venue:** arXiv 2025 (v2 Mar 2026)  
**Code:** https://github.com/facebookresearch/sam3  
**Demo:** https://segment-anything.com

---

## 一、研究背景与动机

### 1.1 SAM系列的演进
- **SAM 1 (2023)**：引入promptable视觉分割（PVS），支持点、框、掩码提示分割单个目标
- **SAM 2 (2024)**：扩展至视频分割，引入记忆机制实现时空一致性追踪
- **SAM 3 (2025)**：突破性引入**Promptable Concept Segmentation (PCS)**，支持文本短语、图像示例或其组合作为提示，分割所有匹配的实例

### 1.2 核心问题
现有SAM系列只能处理视觉提示（点/框/掩码），无法直接响应文本概念（如"所有黄色的校车"）。PCS任务要求模型能：
- 接收文本名词短语（NP）或图像示例
- 检测、分割并追踪所有匹配概念的对象实例
- 在视频中保持实例身份一致性

---

## 二、方法详解

### 2.1 整体架构
SAM 3采用**双编码器-解码器Transformer**架构：
- **Detector（图像级检测器）**：基于DETR范式，处理文本和图像提示
- **Tracker（视频追踪器）**：继承SAM 2的transformer encoder-decoder，支持视频分割和交互式细化
- **共享Backbone**：Perception Encoder (PE) 提供对齐的视觉-语言特征

### 2.2 Detector架构
1. **编码阶段**：图像和文本提示由PE编码，图像示例由示例编码器编码
2. **融合编码器 (Fusion Encoder)**：图像嵌入通过cross-attention与提示token条件化
3. **DETR-like Decoder**：学习目标query与条件化图像嵌入的cross-attention
4. **预测头**：
   - 分类logit（二分类：是否匹配提示）
   - 边界框回归（逐层delta预测）
   - Mask head（改编自MaskFormer）
   - **Semantic Segmentation Head**：像素级二分类（是否属于提示概念）

### 2.3 Presence Token（核心创新）
**问题**：每个proposal query同时负责识别（what）和定位（where）存在冲突——识别需要全局上下文，而定位本质上是局部的。

**解决方案**：引入一个可学习的全局**presence token**，专门预测目标概念在输入中是否存在的概率：
$$p(\text{NP is present in input})$$
每个proposal query只需解决条件定位问题：
$$p(q_i \text{ is a match} | \text{NP is present in input})$$
最终分数 = presence score × query自身分数

**效果**：在训练时加入困难负样本短语（hard negatives），presence head能有效区分相似概念，显著提升开放词汇检测精度。

### 2.4 Tracker与视频架构
- 每帧检测新对象 $O_t$，追踪器传播前一帧的masklet $M_{t-1}$ 到当前帧 $\hat{M}_t$
- **传播**：基于SAM 2风格的单帧传播
- **匹配与更新**：IoU-based matching function关联传播的masklet和当前帧检测
- **重提示策略**：定期用高置信度检测mask重新初始化追踪器，避免漂移
- **时间消歧**：masklet detection score衡量时间窗口内的一致性

### 2.5 交互式细化
支持正负图像示例和点击来细化单个masklet，视频中的mask会传播到整个序列。

---

## 三、数据引擎（Data Engine）

SAM 3的数据引擎采用人机协同、AI辅助的迭代标注流程：

**四个阶段**：
1. **Phase 1 - 人工验证**：SAM 2生成初始mask，人工验证质量（4.3M image-NP pairs）
2. **Phase 2 - 人机+AI验证**：用Phase 1数据微调Llama 3.2作为AI verifier，自动执行Mask Verification和Exhaustivity Verification，人工专注于困难案例（+122M pairs）
3. **Phase 3 - 规模扩展**：扩展到15个数据集，引入22.4M节点的SA-Co ontology（基于Wikidata），挖掘长尾细粒度概念（+19.5M pairs）
4. **Phase 4 - 视频扩展**：将数据引擎扩展至视频

**数据集规模**：
- SA-Co/HQ：4M唯一短语，52M masks
- 合成数据集：38M短语，1.4B masks
- SA-Co benchmark：207K唯一概念，120K图像，1.7K视频（>50×现有benchmark概念数）

---

## 四、实验结果

### 4.1 性能指标
- **零样本LVIS mask AP**：**48.8** vs 当前最佳38.5
- **SA-Co benchmark**：超越baseline至少**2×**
- **推理速度**：H200 GPU上单图30ms（100+检测对象），视频近实时（~5并发对象）

### 4.2 训练阶段
四阶段渐进训练：
1. Perception Encoder预训练
2. Detector预训练
3. Detector微调
4. 冻结backbone训练Tracker

---

## 五、精读收获

### 5.1 对综述的核心价值
1. **Foundation Model时代的里程碑**：SAM 3代表了从"视觉提示分割"到"概念提示分割"的范式跃迁，是综述第6章"Transformer与基础模型时代"的核心节点。
2. **Presence Head的设计思想**：解耦识别与定位的策略对遥感中的道路/建筑物提取有启发——可借鉴此思想设计domain-specific的存在性判断模块。
3. **统一架构的优势**：SAM 3将检测、分割、追踪统一在一个框架中，相比传统"检测→分割→矢量化"的多阶段pipeline大幅简化。

### 5.2 与其他文献的关联
- **SegEarth-OV3 (Li et al., 2025)**：直接基于SAM 3构建，验证了其在遥感零样本分割中的有效性
- **SAM-Road/SAM-Road++**：SAM 1/2时代的道路提取方法，SAM 3的出现可能进一步简化道路提取pipeline
- **Road-SAM**：基于SAM 1的adapter微调方法，SAM 3的开放词汇能力可能减少对领域微调的依赖

### 5.3 综述中可引用的要点
- SAM 3在LVIS上AP 48.8，远超现有方法
- 4M唯一概念、52M mask的高质量训练数据
- Presence token的解耦设计是开放词汇识别的关键
- 30ms单图推理速度，具备实际应用潜力
- 与MLLM结合可处理更复杂的语言提示
