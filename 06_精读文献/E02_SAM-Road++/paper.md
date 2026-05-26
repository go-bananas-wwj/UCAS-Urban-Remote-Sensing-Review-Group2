# SAM-Road++ 精读文档

## 论文基本信息

| 项目 | 内容 |
|------|------|
| **标题** | Towards Satellite Image Road Graph Extraction: A Global-Scale Dataset and A Novel Method |
| **作者** | Pan Yin, Kaiyu Li, Xiangyong Cao, Jing Yao, Lei Liu, Xueru Bai, Feng Zhou, Deyu Meng |
| **单位** | 西安交通大学, 中国科学院空天信息创新研究院, 西安电子科技大学 |
| **会议/期刊** | CVPR 2025 / arXiv:2411.16733 |
| **代码** | https://github.com/earth-insights/samroadplus |
| **类型** | Methods + Dataset / Foundation Model Adaptation |

---

## 摘要 (Abstract)

**Source:** p.1 | S001

**Original:**
Recently, road graph extraction has garnered increasing attention due to its crucial role in autonomous driving, navigation, etc. However, accurately and efficiently extracting road graphs remains a persistent challenge, primarily due to the severe scarcity of labeled data. To address this limitation, we collect a global-scale satellite road graph extraction dataset, i.e. Global-Scale dataset. Specifically, the Global-Scale dataset is ~20× larger than the largest existing public road extraction dataset and spans over 13,800 km² globally. Additionally, we develop a novel road graph extraction model, i.e. SAM-Road++, which adopts a node-guided resampling method to alleviate the mismatch issue between training and inference in global-based methods, while mitigating the occlusion challenges inherent in road graph extraction tasks. Extensive experiments demonstrate that Global-Scale serves as a more comprehensive and challenging benchmark. In addition, SAM-Road++ achieves superior performance on both existing public datasets and Global-Scale, without incurring significant inference costs.

**中文:**
近年来，由于道路图提取在自动驾驶、导航等领域的关键作用，它受到了越来越多的关注。然而，准确高效地提取道路图仍然是一个持续的挑战，主要原因是标注数据的严重稀缺。为了解决这一限制，我们收集了一个全球尺度的卫星道路图提取数据集，即Global-Scale数据集。具体而言，Global-Scale数据集比现有最大的公开道路提取数据集大约20倍，全球覆盖面积超过13,800平方公里。此外，我们开发了一种新颖的道路图提取模型SAM-Road++，采用节点引导重采样方法来缓解全局方法中训练与推理之间的不匹配问题，同时减轻道路图提取任务中固有的遮挡挑战。大量实验表明，Global-Scale作为一个更全面、更具挑战性的基准数据集。此外，SAM-Road++在现有公开数据集和Global-Scale上均取得了优越性能，且没有产生显著的推理成本。

---

## 1. 引言 (Introduction)

**Source:** p.1-2 | S002-S005

### 1.1 研究背景

**Original:**
In recent years, daily travel has increasingly relied on navigation systems, particularly with the advent of autonomous driving technology, which has greatly enhanced convenience in everyday life. These advancements demand higher accuracy and real-time performance in extracting road graphs from satellite images.

**中文:**
近年来，日常出行越来越依赖导航系统，特别是随着自动驾驶技术的出现，极大地提升了日常生活的便利性。这些进步要求从卫星图像中提取道路图具有更高的准确性和实时性。

### 1.2 现有方法的局限性

**Original:**
Existing approaches to end-to-end road graph extraction can be categorized into two main types: iterative methods and global-based methods. Iterative methods suffer from error accumulation during sequential inference. Global-based methods predict all vertices and edges simultaneously, avoiding error accumulation. However, global-based methods face a critical mismatch issue between training and inference: during training, they sample nodes from ground truth, while during inference, they must rely on predicted masks to obtain nodes via Non-Maximum Suppression (NMS). This inconsistency significantly degrades performance.

**中文:**
现有的端到端道路图提取方法可分为两类：迭代方法和全局方法。迭代方法在顺序推理过程中存在误差累积问题。全局方法同时预测所有顶点和边，避免了误差累积。然而，全局方法面临训练与推理之间的关键不匹配问题：在训练期间，它们从真值中采样节点；而在推理期间，它们必须依赖预测的掩膜通过非极大值抑制(NMS)获取节点。这种不一致性显著降低了性能。

### 1.3 本文贡献

**Original:**
To address these challenges, we first collect a large-scale satellite image road graph extraction dataset named Global-Scale. ... Additionally, we develop a novel road graph extraction model named SAM-Road++. Specifically, SAM-Road++ adopts a node-guided resampling method to bridge the gap between training and inference in global-based methods. Furthermore, SAM-Road++ proposes an "extended-line" strategy to mitigate occlusion challenges in road graph extraction.

**中文:**
为了应对这些挑战，我们首先收集了一个名为Global-Scale的大规模卫星图像道路图提取数据集。... 此外，我们开发了一种名为SAM-Road++的新颖道路图提取模型。具体而言，SAM-Road++采用节点引导重采样方法来弥合全局方法中训练与推理之间的差距。此外，SAM-Road++提出了一种"延伸线"策略来缓解道路图提取中的遮挡挑战。

---

## 2. Global-Scale数据集

**Source:** p.3-4 | S006-S008

### 2.1 数据集规模与覆盖

| 特性 | 数值 |
|------|------|
| 覆盖面积 | >13,800 km² |
| 覆盖范围 | 六大洲 |
| 图像尺寸 | 512×512 (patch) |
| 场景类型 | 城市、乡村、山区 |
| 相对规模 | ~20× 现有最大公开数据集 |

### 2.2 数据集意义

**Original:**
Global-Scale serves as a more comprehensive and challenging benchmark for evaluating the generalization ability of road graph extraction models in complex scenarios.

**中文:**
Global-Scale作为一个更全面、更具挑战性的基准数据集，用于评估道路图提取模型在复杂场景下的泛化能力。

---

## 3. 方法详解 (Methodology)

**Source:** p.4-6 | S009-S015

### 3.1 与SAM-Road的关系

**Original:**
SAM-Road is the first global-based end-to-end road graph extraction method and the first to bring the foundation model into the field of road graph extraction. ... SAM-Road++ is built upon SAM-Road but addresses two critical limitations.

**中文:**
SAM-Road是第一个基于全局的端到端道路图提取方法，也是第一个将基础模型引入道路图提取领域的方法。... SAM-Road++建立在SAM-Road之上，但解决了两个关键局限性。

### 3.2 问题一：训练-推理不匹配 (Training-Inference Mismatch)

**Original:**
During training, SAM-Road randomly samples nodes from the ground truth. During inference, ground truth is not available, therefore SAM-Road selects road nodes from the predicted masks via NMS. This creates a mismatch: the nodes used to train the connectivity classifier differ from those encountered during inference.

**中文:**
在训练期间，SAM-Road从真值中随机采样节点。在推理期间，真值不可用，因此SAM-Road通过NMS从预测掩膜中选择道路节点。这造成了一种不匹配：用于训练连通性分类器的节点与推理期间遇到的节点不同。

### 3.3 解决方案一：Node-Guided Resampling

**Original:**
SAM-Road++ proposes a node-guided resampling strategy. For each source node sampled from ground truth, we identify target nodes within a distance R. Then, for each target node, we find the maximum probability point of the predicted road mask around the target node and save it as the new target node. This ensures that the re-sampled nodes not only retain the connectivity information from ground truth, but the position information of the new target nodes also matches the node selection strategy in inference.

**中文:**
SAM-Road++提出了一种节点引导重采样策略。对于从真值中采样的每个源节点，我们在距离R内识别目标节点。然后，对于每个目标节点，我们在预测道路掩膜中目标节点周围找到最大概率点，并将其保存为新的目标节点。这确保了重采样节点不仅保留了来自真值的连通性信息，而且新目标节点的位置信息也与推理中的节点选择策略相匹配。

```
Node-Guided Resampling流程:
1. 从真值采样源节点(source nodes)
2. 对每个源节点，找到距离R内的目标节点(target nodes)
3. 对每个目标节点，在预测掩膜周围找最大概率点 → 新目标节点
4. 保留真值的源节点和连通性，但用预测掩膜的位置
```

### 3.4 问题二：遮挡挑战 (Occlusion Challenge)

**Original:**
The determination of connectivity between road nodes is susceptible to occlusion, such as tree shadows and building shadows covering parts of the road.

**中文:**
道路节点之间连通性的判断容易受到遮挡的影响，例如树木阴影和建筑物阴影覆盖道路部分。

### 3.5 解决方案二："Extended-Line" Strategy

**Original:**
For a pair of re-sampled nodes required for connectivity discrimination, we use their coordinates to extract node-centered patches in the feature map. Considering the extensibility of the road and the influence of factors such as tree shadows on road judgment, we believe that the information between the two nodes and the information on their extensions can also effectively assist the model in predicting the existence of the road. We uniformly sample the mask values at both ends of the respective extensions n times using the road masks previously generated by the model.

**中文:**
对于需要进行连通性判别的一对重采样节点，我们使用它们的坐标在特征图中提取以节点为中心的块。考虑到道路的可延伸性以及树木阴影等因素对道路判断的影响，我们认为两个节点之间的信息以及它们延伸方向上的信息也能有效辅助模型预测道路的存在性。我们使用模型先前生成的道路掩膜，在各自延伸线的两端均匀采样n次掩膜值。

```
Extended-Line Strategy核心思想:
- 道路具有可延伸性(extensibility)
- 遮挡处（如树影）虽然看不到道路，但道路两侧是连续的
- 在节点对的连线和延伸方向上采样，利用道路的几何连续性辅助判断
```

---

## 4. 实验结果 (Experimental Results)

**Source:** p.6-8 | S016-S022

### 4.1 现有公开数据集对比

**Source:** p.6 | Table 2

**City-Scale数据集:**

| 方法 | F1 | Precision | Recall | APLS |
|------|-----|-----------|--------|------|
| RNGDet | 68.35 | 79.44 | 60.03 | 47.34 |
| RNGDet++ | 85.49 | 90.38 | 81.10 | 68.71 |
| Sat2Graph | 74.05 | 83.95 | 66.10 | 59.53 |
| SAM-Road | 85.04 | 90.47 | 80.30 | 72.44 |
| **SAM-Road++** | **87.18** | **89.21** | **85.25** | **74.06** |
| SAM-Road++* | **89.53** | **90.47** | **88.63** | **77.24** |

**SpaceNet数据集:**

| 方法 | F1 | Precision | Recall | APLS |
|------|-----|-----------|--------|------|
| RNGDet++ | 87.08 | 92.63 | 82.10 | 68.68 |
| Sat2Graph | 74.69 | 82.88 | 68.00 | 56.85 |
| SAM-Road | 87.44 | 93.03 | 82.40 | 72.32 |
| **SAM-Road++** | **88.56** | **91.32** | **86.00** | **74.14** |
| SAM-Road++* | **90.12** | **91.85** | **88.45** | **76.83** |

**关键发现:**
- SAM-Road++在F1和APLS上全面超越SAM-Road和RNGDet++
- 使用Global-Scale预训练(*)后，性能进一步提升约2-3个点
- 在City-Scale上F1达到87.18%（无预训练）/ 89.53%（有预训练）

### 4.2 Global-Scale数据集基准测试

**Source:** p.7-8 | Table 3

**In-Domain测试:**

| 方法 | F1 | Precision | Recall | APLS |
|------|-----|-----------|--------|------|
| RNGDet++ | 62.30 | 85.63 | 49.03 | 33.71 |
| Sat2Graph | 35.53 | 90.15 | 22.13 | 21.64 |
| SAM-Road | 65.44 | 90.03 | 51.40 | 35.84 |
| **SAM-Road++** | **68.28** | 87.62 | **56.04** | **39.72** |

**Out-of-Domain测试:**

| 方法 | F1 | Precision | Recall | APLS |
|------|-----|-----------|--------|------|
| RNGDet++ | 48.28 | 75.83 | 35.46 | 22.18 |
| Sat2Graph | 28.46 | 82.45 | 17.20 | 14.83 |
| SAM-Road | 51.14 | 78.12 | 37.99 | 24.18 |
| **SAM-Road++** | **55.12** | 75.18 | **43.51** | **27.84** |

**关键发现:**
- Global-Scale比City-Scale/SpaceNet更具挑战性（所有方法性能下降）
- SAM-Road++在Out-of-Domain上优势更明显（F1领先SAM-Road 4个点）
- 证明SAM-Road++具有更强的泛化能力和鲁棒性

---

## 5. 结论与启示 (Conclusions & Implications)

**Source:** p.8 | S023

**Original:**
In this paper, we present a large-scale dataset, Global-Scale, and a novel method, SAM-Road++, for road graph extraction. The Global-Scale encompasses six continents and has been meticulously curated to include a diverse array of scenes, such as urban, rural, and mountainous areas. SAM-Road++ effectively addresses the mismatch between training and inference in global-based methods while mitigating the occlusion challenges inherent in road graph extraction tasks. Extensive experiments demonstrate that Global-Scale serves as a more comprehensive and challenging benchmark. In addition, SAM-Road++ achieves superior performance on both existing public datasets and Global-Scale, without incurring significant inference costs.

**中文:**
本文提出了一个大规模数据集Global-Scale和一种新颖的方法SAM-Road++用于道路图提取。Global-Scale涵盖六大洲，经过精心策划，包含城市、乡村和山区等多种场景。SAM-Road++有效解决了全局方法中训练与推理之间的不匹配问题，同时减轻了道路图提取任务中固有的遮挡挑战。大量实验表明，Global-Scale作为一个更全面、更具挑战性的基准数据集。此外，SAM-Road++在现有公开数据集和Global-Scale上均取得了优越性能，且没有产生显著的推理成本。

---

## 6. 综述引用要点 (Key Points for Citation in Review)

### 6.1 技术定位
- **时期**: 大模型时代深化（2025年）
- **核心创新**:
  1. **Node-Guided Resampling**: 解决全局方法训练-推理不一致问题
  2. **Extended-Line Strategy**: 利用道路几何连续性解决遮挡问题
  3. **Global-Scale数据集**: 迄今最大、最全面的道路图提取数据集
- **与SAM-Road的关系**: 继承两阶段框架，在算法层面解决关键瓶颈

### 6.2 与前人工作的关系
- **vs SAM-Road**: 解决训练-推理不匹配 + 遮挡问题，精度提升2-3个点
- **vs RNGDet++**: F1和APLS全面领先，且推理速度保持高效
- **vs 迭代方法**: 避免误差累积，同时保持全局方法的速度优势

### 6.3 对综述的价值
- **SAM系列演进**: SAM-Road (2024) → SAM-Road++ (2025) 的技术深化路径
- **数据集贡献**: Global-Scale为领域提供了新的benchmark
- **方法学启示**: 训练-推理一致性是全局方法的关键设计要素
- **可引用数据**: City-Scale F1=87.18%, SpaceNet F1=88.56%, Global-Scale F1=68.28%

---

## 7. 术语表 (Terminology)

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Node-Guided Resampling | 节点引导重采样 | 核心创新，对齐训练与推理的节点分布 |
| Extended-Line Strategy | 延伸线策略 | 利用道路连续性解决遮挡问题 |
| Training-Inference Mismatch | 训练-推理不匹配 | 全局方法的核心瓶颈 |
| Global-Scale Dataset | Global-Scale数据集 | 全球尺度道路图提取数据集 |
| In-Domain / Out-of-Domain | 域内/域外 | 训练数据分布内/外的测试 |
| Occlusion Challenge | 遮挡挑战 | 树木/建筑物阴影覆盖道路 |
| Road Extensibility | 道路可延伸性 | 道路几何连续性假设 |
| NMS (Non-Maximum Suppression) | 非极大值抑制 | 从概率图提取峰值点 |
| Connectivity Classifier | 连通性分类器 | 判断两点之间是否存在道路边 |
| Pre-training | 预训练 | 在Global-Scale上预训练后再微调 |
