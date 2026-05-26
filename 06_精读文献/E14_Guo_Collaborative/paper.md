# Building-Road Collaborative Extraction From Remote Sensing Images via Cross-Task and Cross-Scale Interaction

**Authors:** Haonan Guo, Xin Su, Chen Wu, Bo Du, Liangpei Zhang  
**Affiliations:** Wuhan University (LIESMARS, School of RS & Info Eng., School of CS)  
**Venue:** IEEE TGRS, Vol. 62, 2024  
**DOI:** 10.1109/TGRS.2024.3383057

---

## 一、研究背景与动机

### 1.1 核心问题
1. **孤立提取的局限**：现有方法通常用独立模型分别提取建筑物和道路，忽略了两者的强空间相关性
2. **简单多任务学习的"跷跷板现象" (Seesaw Phenomenon)**：直接为多任务附加多个分类器会导致一个任务的特征主导，牺牲另一任务的性能
3. **感受野需求差异**：建筑物和道路对模型感受野的需求不同，统一感受野无法同时优化两个任务

### 1.2 关键发现
通过可视化U-Net在建筑物提取和道路提取任务上学到的特征：
- **建筑物模型自动学习了道路区域信息**（无道路标签监督）
- **道路模型自动学习了建筑物区域信息**（无建筑标签监督）
- **结论**：两个任务在特征空间中存在互补关系，高质量建筑特征能提升道路提取性能，反之亦然

---

## 二、方法详解

### 2.1 CRIN整体架构
**C**ross-task and c**R**oss-scale **IN**teraction Network：
- **共享编码器**：权重共享的backbone提取层次特征
- **MFI模块 (Multitask Feature Interaction)**：在decoder阶段实现任务内和跨任务特征交互
- **CSI模块 (Cross-Scale Interaction)**：自适应选择最优感受野

### 2.2 MTI模块 (Multitask Interaction)

#### 阶段1：特征融合 (Feature Fusion Stage)
- 将输入特征分成两组，交替拼接
- 组卷积（group size=2）分别生成building features和road features
- **优势**：不同任务专注于各自任务的空间细节

#### 阶段2：特征交互 (Feature Interaction Stage)
将特征投影到三类特征空间：
- **Building-specific feature space**：建筑物专用特征
- **Road-specific feature space**：道路专用特征
- **Task-shared feature space**：任务共享特征（跨任务交互）

**效果**：
- 共享空间中两个任务的信息可以交互互补
- 专用空间中保留各自任务的独特性
- 相比传统decoder节省1/3计算成本

### 2.3 CSI模块 (Cross-Scale Interaction)

**问题**：不同任务的最优感受野不同，手动选择kernel size可能不利于多任务精度

**解决方案**：
- 多分支大卷积核（7×7, 11×11, 21×21）+ 残差分支
- **降参技巧**：用1×n + n×1的逐行/逐列卷积替代n×n卷积
- **尺度注意力模块**：全局平均池化 → MLP → Softmax生成各尺度贡献权重
- 各尺度特征按注意力加权求和

**计算效率**：
- 深度可分离卷积降低参数量
- 行列分解使计算量降至原版的1/600

### 2.4 损失函数
$$L_{building} = (Dice(\hat{y}_b, y_b) + CE(\hat{y}_b, y_b)) / 2$$
$$L_{road} = (Dice(\hat{y}_r, y_r) + CE(\hat{y}_r, y_r)) / 2$$
$$L_{aux} = \sum_{i=1}^n CE(Conv_{1×1}([f_b^i, f_s^i]), y_b) + CE(Conv_{1×1}([f_r^i, f_s^i]), y_r)$$

---

## 三、实验结果

### 3.1 数据集
- 城市和农村场景的VHR遥感图像（具体数据集名称在后续页面中，提取文本未完全展示）

### 3.2 关键对比
| 架构类型 | 代表 | 问题 |
|---------|------|------|
| Separate Models | Zhang & Wang, Ayala et al. | 分别训练，计算量翻倍，未利用空间相关性 |
| Simple Multitask | Ding et al. (NFSNet) | 跷跷板现象，一个任务主导 |
| **CRIN (Ours)** | **Guo et al.** | **同时利用互补关系，避免跷跷板** |

### 3.3 性能优势
- 单模型同时提取建筑物和道路，**推理时间减半**
- 在城市和农村场景均达到最高精度
- 有效缓解多任务学习中的跷跷板现象

---

## 四、精读收获

### 4.1 综述写作价值
1. **多任务联合提取的代表性工作**：Guo et al. (2024) 是综述第7章"多源融合方法"或独立"联合提取"子主题的核心文献，展示了建筑物-道路协同提取的优势。
2. **特征空间分析的创新视角**：通过可视化证明两个任务在特征空间的互补性，为设计协同机制提供了理论依据。
3. **感受野自适应选择**：CSI模块的尺度注意力机制为综述讨论"不同地物对感受野的需求差异"提供了具体技术案例。

### 4.2 关键引用点
- 建筑物和道路在特征空间的互补性可视化（Fig. 1）
- MTI模块将decoder计算成本降低1/3
- CSI模块通过行列分解将计算量降至1/600
- 单模型推理时间减半，同时提升两个任务精度

### 4.3 与其他文献的关联
- **SAM-Road++**：虽主要关注道路，但其节点引导策略可与Guo的协同思想结合
- **TopoRF-Net**：专注道路拓扑，可与Guo的多任务框架结合实现建筑-道路联合拓扑保持
- **CFENet**：Chen et al. (2022) 的级联特征增强方法可作为Guo方法的单任务baseline
- **SegEarth-OV3**：SAM 3的开放词汇能力可能同时提取建筑物和道路，无需专用多任务设计

### 4.4 局限与展望
- 仅在光学VHR图像验证，未融合LiDAR等多源数据
- 未引入拓扑保持机制，道路连通性可能不如专用方法（如TopoRF-Net, SAM-Road++）
- 未来可探索将协同提取与foundation model结合，利用SAM 3的开放词汇能力同时识别并提取相关地物
