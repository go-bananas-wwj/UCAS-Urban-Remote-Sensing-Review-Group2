# Road-SAM: Adapting the Segment Anything Model to Road Extraction From Large Very-High-Resolution Optical Remote Sensing Images

**Authors:** Wenqing Feng, Fangli Guan, Chenhao Sun, Wei Xu  
**Affiliations:** Hangzhou Dianzi University, Changsha Univ. of Sci. & Tech., NUDT  
**Venue:** IEEE Geoscience and Remote Sensing Letters, Vol. 21, 2024  
**DOI:** 10.1109/LGRS.2024.3430900

---

## 一、研究背景与动机

### 1.1 核心问题
1. **现有深度学习方法的分块处理局限**：FCN类方法将大图像切分为小块处理，限制了建模大范围道路网络空间一致性和拓扑连贯性的能力
2. **专用模型泛化性差**：现有模型主要在特定小规模道路数据集上训练，难以跨数据集、跨环境泛化
3. **SAM在遥感领域的不足**：
   - SAM在自然图像上预训练，缺乏VHR遥感图像训练数据
   - 道路纹理和宽度变化大，SAM直接应用精度不足
   - 不同尺度和分辨率的VHR遥感图像适应性差

### 1.2 核心思路
- **无需全参数微调**：冻结SAM大部分参数，仅引入少量可训练参数（~10%）
- **Adapter机制**：在ViT block中插入轻量级adapter，将SAM从自然图像域迁移到遥感道路提取域
- **显式视觉提示 (EVP)**：利用高频分量(HFC)信息作为任务特定提示，增强道路边缘和纹理感知

---

## 二、方法详解

### 2.1 Road-SAM整体架构
继承SAM原始架构（ViT image encoder + prompt encoder + mask decoder），修改集中在image encoder和输入模块。

### 2.2 三种Adapter变体
在ViT block中灵活插入adapter：

| 变体 | 结构 | 插入位置 |
|------|------|---------|
| **Series Adapter** | 两个adapter顺序插入在MHA和FFN之间 | 串联 |
| **Parallel Adapter** | 两个adapter与MHA和FFN并行 | 并联 |
| **Mixed Adapter** | MHA层用串联，FFN层用并联 | 混合 |

Adapter公式：
$$Adapter(f_{input}) = Up(ReLU(Down(f_{input})))$$
即：下投影 → ReLU激活 → 上投影

### 2.3 任务特定输入模块：EVP (Explicit Visual Prompting)

#### (1) 高频分量提取 (HFC Extraction)
- 对输入图像进行FFT变换得到频域表示 $z = FFT(I)$
- 生成二值掩码 $M_{hfc}$，保留高频系数（边缘、纹理信息）
- 逆变换得到HFC：$I_{hfc} = IFFT(z \times M_{hfc}(\tau))$
- **原理**：道路在遥感图像中呈细长线性结构，边界和纹理特征在HFC中更突出

#### (2) 频率Adapter (Frequency Adapter)
将patch embedding特征 $F_{pe}$ 和HFC特征 $F_{hfc}$ 融合生成提示：
$$P_i = MLP_{up}(GELU(MLP_{tune}^i(F_{pe} + F_{hfc})))$$
- $MLP_{tune}^i$：每层独立的线性层生成不同提示
- $MLP_{up}$：跨层共享的上投影层匹配transformer特征维度
- 输出提示 $P_i$ 附加到每个transformer block

### 2.4 Mask Decoder微调
- 不输入原始prompt到SAM mask decoder
- Decoder权重用SAM预训练权重初始化，训练时微调
- 结合任务特定知识和大模型通用知识

---

## 三、实验结果

### 3.1 数据集
- **URUR**：3008张5120×5120 VHR图像，8类（建筑、农田、温室、林地、裸地、水体、道路、其他）
- **DeepGlobe Road**：6226张1024×1024图像

### 3.2 URUR数据集结果
| 方法 | F1 Score | IoU |
|------|----------|-----|
| LinkNet34 | - | - |
| D-LinkNet | - | - |
| RFE-LinkNet | - | - |
| ResUNet | - | - |
| DeepLab v3+ | - | - |
| Road-SAM (Series) | ~72 | ~56 |
| Road-SAM (Parallel) | ~72.5 | ~57 |
| **Road-SAM (Mixed)** | **73.29** | **57.84** |

### 3.3 DeepGlobe Road结果
| 方法 | F1 Score | IoU |
|------|----------|-----|
| **Road-SAM (Mixed)** | **81.65** | **68.99** |

### 3.4 消融实验
- **仅Mixed Adapter**（URUR）：F1 +36.35%, IoU +32.14%
- **仅EVP输入模块**（URUR）：F1 +16.22%, IoU +12.43%
- **两者结合**：最佳性能
- **仅10%参数可训练**：计算资源高效

---

## 四、精读收获

### 4.1 综述写作价值
1. **SAM适配遥感的典范**：Road-SAM是SAM在遥感道路提取中adapter-based微调的代表性工作，位于"SAM系列适配遥感"章节的核心位置。
2. **参数高效微调 (PEFT)** 的案例：仅10%参数可训练即可显著提升性能，为综述讨论"大模型轻量化适配策略"提供有力证据。
3. **频域特征增强**：EVP + HFC的设计展示了将领域先验（道路边缘在频域突出）融入大模型适配的创新思路。

### 4.2 SAM系列演进中的定位
| 方法 | SAM版本 | 策略 | 特点 |
|------|---------|------|------|
| Road-SAM | SAM 1 | Adapter + EVP微调 | 参数高效，道路专用 |
| RSAM-Seg | SAM 1 | Adapter微调 | 通用遥感分割 |
| SAM-Road | SAM 1 | 两阶段：分割+拓扑 | 无需微调SAM backbone |
| SAM-Road++ | SAM 1 | 节点引导重采样 | 扩展至全球尺度 |
| SegEarth-OV3 | SAM 3 | 零样本推理 | 无需训练，开放词汇 |

### 4.3 关键引用点
- 三种adapter结构（series/parallel/mixed）的对比实验表明mixed最佳
- HFC提取道路边缘和纹理的有效性
- 仅10%参数更新即可超越全监督SOTA方法
- 在URUR（5120×5120）和DeepGlobe（1024×1024）上的跨尺度泛化能力

### 4.4 局限
- 基于SAM 1，尚未利用SAM 2的视频追踪和SAM 3的开放词汇能力
- 仅在道路提取任务验证，未扩展至建筑物提取
- 缺乏与TopoRF-Net等最新拓扑保持方法的直接对比
