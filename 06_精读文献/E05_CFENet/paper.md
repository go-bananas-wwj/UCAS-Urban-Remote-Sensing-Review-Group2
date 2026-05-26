# CFENet 精读文档

## 论文基本信息

| 项目 | 内容 |
|------|------|
| **标题** | A Context Feature Enhancement Network for Building Extraction from High-Resolution Remote Sensing Imagery |
| **作者** | Jinzhi Chen, Dejun Zhang*, Yiqi Wu, Yilin Chen, Xiaohu Yan |
| **单位** | 中国地质大学(武汉)、武汉工程大学、深圳职业技术学院 |
| **期刊** | Remote Sensing (MDPI), 2022, 14(9), 2276 |
| **DOI** | https://doi.org/10.3390/rs14092276 |
| **类型** | Methods / Algorithm Paper |
| **代码** | https://github.com/djzgroup/CFENet |

---

## 摘要 (Abstract)

**Source:** p.1 | S001

**Original:**
The complexity and diversity of buildings make it challenging to extract low-level and high-level features with strong feature representation by using deep neural networks in building extraction tasks. Meanwhile, deep neural network-based methods have many network parameters, which take up a lot of memory and time in training and testing. We propose a novel fully convolutional neural network called the Context Feature Enhancement Network (CFENet) to address these issues. CFENet comprises three modules: the spatial fusion module, the focus enhancement module, and the feature decoder module. First, the spatial fusion module aggregates the spatial information of low-level features to obtain buildings' outline and edge information. Secondly, the focus enhancement module fully aggregates the semantic information of high-level features to filter the information of building-related attribute categories. Finally, the feature decoder module decodes the output of the above two modules to segment the buildings more accurately. In a series of experiments on the WHU Building Dataset and the Massachusetts Building Dataset, our CFENet balances efficiency and accuracy compared to the other four methods we compared, and achieves optimality on all five evaluation metrics: PA, PC, F1, IoU, and FWIoU. This indicates that CFENet can effectively enhance and fuse buildings' low-level and high-level features, improving building extraction accuracy.

**中文:**
建筑物的复杂性和多样性使得在建筑物提取任务中，利用深度神经网络提取具有强特征表征能力的低层特征和高层特征变得具有挑战性。同时，基于深度神经网络的方法具有大量的网络参数，在训练和测试过程中占用大量内存和时间。本文提出了一种新颖的全卷积神经网络——上下文特征增强网络（CFENet）来解决这些问题。CFENet包含三个模块：空间融合模块（SFM）、焦点增强模块（FEM）和特征解码模块（FDM）。首先，空间融合模块聚合低层特征的空间信息，以获取建筑物的轮廓和边缘信息。其次，焦点增强模块充分聚合高层特征的语义信息，以筛选与建筑物相关的属性类别信息。最后，特征解码模块对上述两个模块的输出进行解码，以更准确地对建筑物进行分割。在WHU建筑物数据集和Massachusetts建筑物数据集上的一系列实验中，与其他四种方法相比，CFENet在效率和精度之间取得了平衡，并在PA、PC、F1、IoU和FWIoU五项评估指标上均达到了最优。这表明CFENet能够有效增强和融合建筑物的低层和高层特征，提高建筑物提取精度。

**关键词:** CFENet; fully convolutional neural network; remote sensing images; building extraction

---

## 1. 引言 (Introduction)

**Source:** p.2-3 | S002-S005

### 1.1 研究背景

**Original:**
With the advancement of earth observation technology, the quality and quantity of high-resolution remote sensing data are constantly improving. The generation of high-resolution remote sensing images has made more convenient and detailed data sources available for its applications. Building extraction from high-resolution remote sensing images is a conversion process from data to information. In urban remote sensing, building extraction can be applied to urban and rural planning. In surveying and mapping engineering, building extraction is widely used as a means of acquiring data.

**中文:**
随着地球观测技术的进步，高分辨率遥感数据的质量和数量不断提高。高分辨率遥感影像的生成为其应用提供了更便捷、更详细的数据源。从高分辨率遥感影像中提取建筑物是一个从数据到信息的转换过程。在城市遥感中，建筑物提取可应用于城乡规划。在测绘工程中，建筑物提取被广泛用作数据获取的手段。

### 1.2 现有方法的局限性

**Original:**
At present, building extraction methods can be broadly divided into two categories: the traditional building extraction method and the learning-based building extraction method. The traditional building extraction method mainly relies on manual design features such as color, texture, and shape. These methods are deficient in robustness and accuracy. ... The learning-based building extraction method cannot effectively enhance and fuse low-level and high-level features from neural networks and often contain a large number of network structure parameters.

**中文:**
目前，建筑物提取方法大致可分为两类：传统建筑物提取方法和基于学习的建筑物提取方法。传统建筑物提取方法主要依赖于人工设计的特征，如颜色、纹理和形状。这些方法在鲁棒性和准确性方面存在不足。... 基于学习的建筑物提取方法无法有效增强和融合神经网络中的低层和高层特征，且通常包含大量的网络结构参数。

### 1.3 本文贡献

**Original:**
To better address the above issues, we design a Context Feature Enhancement Network (CFENet) that can learn more contextual information to achieve accurate localization segmentation of buildings. The contributions of this paper can be summarized as follows:
- An end-to-end context feature enhancement network, namely CFENet, is proposed to address the challenges of complexity and diversity of buildings encountered in building extraction from remote sensing images.
- CFENet achieves more accurate building extraction results on the WHU Building Dataset and the Massachusetts Building Dataset by explicitly establishing rich contextual relationships on low-level and high-level features.
- CFENet balances efficiency and accuracy by employing dilated convolution in the spatial fusion module and asymmetric convolution in the focus enhancement module.

**中文:**
为了更好地解决上述问题，我们设计了一种上下文特征增强网络（CFENet），该网络能够学习更多的上下文信息，以实现对建筑物的精确定位分割。本文的贡献可总结如下：
- 提出了一种端到端的上下文特征增强网络CFENet，以应对遥感图像建筑物提取中遇到的建筑物复杂性和多样性挑战。
- CFENet通过在低层和高层特征上显式建立丰富的上下文关系，在WHU建筑物数据集和Massachusetts建筑物数据集上获得了更准确的建筑物提取结果。
- CFENet通过在空间融合模块中采用空洞卷积、在焦点增强模块中采用非对称卷积，在效率和精度之间取得了平衡。

---

## 2. 方法概述 (Method Overview)

**Source:** p.4-8 | S006-S015

### 2.1 整体架构

**Original:**
CFENet adopts ResNet-101 as the backbone, and the input image size is 512 × 512 pixels. After performing feature extraction through ResNet-101, four different size feature maps are obtained, denoted as Feature 1, Feature 2, Feature 3, and Feature 4. Feature 1 and Feature 2 are low-level features, while Feature 3 and Feature 4 are high-level features. The low-level features contain larger spatial resolution and more detailed information (color, outline, texture, etc.) by employing fewer convolution layers and downsampling operations. However, the low-level features are not rich in semantic information and contain much noisy information. On the contrary, the high-level features have more abstract and rich semantic information (attributes, categories, etc.) by employing more convolution layers and downsampling operations. However, the spatial resolution of the high-level features is small, and spatial information loss is serious.

**中文:**
CFENet采用ResNet-101作为骨干网络，输入图像尺寸为512×512像素。通过ResNet-101进行特征提取后，获得四种不同尺寸的特征图，分别记为Feature 1、Feature 2、Feature 3和Feature 4。Feature 1和Feature 2是低层特征，Feature 3和Feature 4是高层特征。低层特征由于采用了较少的卷积层和下采样操作，包含更大的空间分辨率和更多的细节信息（颜色、轮廓、纹理等）。然而，低层特征的语义信息不丰富，且包含大量噪声信息。相反，高层特征由于采用了更多的卷积层和下采样操作，具有更抽象和丰富的语义信息（属性、类别等）。然而，高层特征的空间分辨率较小，空间信息损失严重。

### 2.2 空间融合模块 (Spatial Fusion Module, SFM)

**Source:** p.4-5 | S007-S009

**Original:**
The spatial fusion module aggregates the spatial information of low-level features to obtain buildings' outline and edge information. The design of the spatial fusion module is based on multi-branch dilated convolution. The input of this module is Feature 1 (number of channels: 256, feature map size: 128 × 128) and Feature 2 (number of channels: 512, feature map size: 64 × 64). First, by using a 3 × 3 convolution layer with a step size of 2 to keep Feature 1 the same size as Feature 2, and then through a parallel branch, which has four branches. A 1 × 1 convolution layer is used in each branch to reduce the number of channels in the feature map. When k > 1, a 3 × 3 dilated convolution layer is added after the 1 × 1 convolution layer in each branch, and the dilation ratio is set to 2k. Subsequently, the output features of the four branches are aggregated through a concatenation operation, and then the dimensionality is reduced by a 1 × 1 convolution layer. Finally, the dimensionality reduction features are added element-by-element with the features before entering the branch.

**中文:**
空间融合模块聚合低层特征的空间信息，以获取建筑物的轮廓和边缘信息。空间融合模块的设计基于多分支空洞卷积。该模块的输入为Feature 1（通道数：256，特征图尺寸：128×128）和Feature 2（通道数：512，特征图尺寸：64×64）。首先，使用步长为2的3×3卷积层使Feature 1与Feature 2尺寸相同，然后通过一个具有四个分支的并行分支。每个分支中使用1×1卷积层来减少特征图的通道数。当k>1时，在每个分支的1×1卷积层之后添加一个3×3空洞卷积层，空洞率设置为2k。随后，通过拼接操作聚合四个分支的输出特征，然后通过1×1卷积层进行降维。最后，将降维后的特征与进入分支前的特征进行逐元素相加。

**核心思想:**
- 使用**多分支空洞卷积**模拟不同感受野
- 对Feature 1和Feature 2分别增强后拼接
- 通过Location Block进一步提炼空间关系

### 2.3 焦点增强模块 (Focus Enhancement Module, FEM)

**Source:** p.6-7 | S010-S013

**Original:**
The focus enhancement module fully aggregates the semantic information of high-level features to filter the information of building-related attribute categories. After completing the above steps, we design two parallel branches to capture rich long-range contextual relationships in spatial and channel dimensions, in order to further enhance the feature representations. ... We only enhance Feature 3 and do not expand the receptive field for Feature 4. Meanwhile, we design multi-branch convolution layers with different kernels to simulate multi-scale receptive fields.

**中文:**
焦点增强模块充分聚合高层特征的语义信息，以筛选与建筑物相关的属性类别信息。在完成上述步骤后，我们设计了两个并行分支来捕获空间和通道维度中丰富的长距离上下文关系，以进一步增强特征表征。... 我们只对Feature 3进行增强，而不扩展Feature 4的感受野。同时，我们设计了具有不同核的多分支卷积层来模拟多尺度感受野。

**核心思想:**
- 对高层特征（Feature 3）进行**空间和通道双维度**的上下文建模
- 使用**自注意力机制**（Location Block）捕获长距离依赖
- 通过**非对称卷积**减少参数量，提升效率

### 2.4 特征解码模块 (Feature Decoder Module, FDM)

**Source:** p.7-8 | S014-S015

**Original:**
The feature decoder module decodes the output of the above two modules to segment the buildings more accurately. The feature decoder module further fuses and enhances the features generated by the spatial fusion module and the focus enhancement module to obtain the final probability map.

**中文:**
特征解码模块对上述两个模块的输出进行解码，以更准确地对建筑物进行分割。特征解码模块进一步融合和增强空间融合模块和焦点增强模块生成的特征，以获得最终的概率图。

---

## 3. 实验结果 (Experimental Results)

**Source:** p.9-14 | S016-S025

### 3.1 数据集

| 数据集 | 来源 | 图像尺寸 | 训练/验证/测试 | 特点 |
|--------|------|----------|----------------|------|
| WHU Building | 新西兰基督城航空影像 | 512×512 | 4736/1036/2416 | 纹理、形状、颜色多样 |
| Massachusetts | 波士顿城区/郊区航空影像 | 256×256 (切分后) | 137/4/10 | 地面分辨率1m，难度更高 |

### 3.2 WHU数据集结果

**Source:** p.10-11 | S018-S019

**Original:**
Our method outperforms other methods on all five evaluation metrics. In particular, our method improves 0.0158 on PA, 0.1004 on PC, 0.0827 on F1, 0.0266 on FWIoU and even more on IoU by 0.1303 over U-Net.

**中文:**
我们的方法在全部五项评估指标上均优于其他方法。特别是，与U-Net相比，我们的方法在PA上提升了0.0158，在PC上提升了0.1004，在F1上提升了0.0827，在FWIoU上提升了0.0266，在IoU上更是提升了0.1303。

**关键精度对比 (WHU数据集):**

| 方法 | PA | PC | F1 | IoU | FWIoU |
|------|-----|-----|-----|------|--------|
| U-Net | 0.9713 | 0.8366 | 0.8435 | 0.7419 | 0.9485 |
| Deeplabv3+ | 0.9701 | 0.8158 | 0.8304 | 0.7239 | 0.9452 |
| PSPNet | 0.9609 | 0.7784 | 0.7894 | 0.6769 | 0.9324 |
| HRNet | 0.9812 | 0.9109 | 0.9045 | 0.8456 | 0.9705 |
| **CFENet** | **0.9871** | **0.9370** | **0.9262** | **0.8722** | **0.9751** |

### 3.3 Massachusetts数据集结果

**Source:** p.12-13 | S020-S021

**关键精度对比 (Massachusetts数据集):**

| 方法 | PA | PC | F1 | IoU | FWIoU |
|------|-----|-----|-----|------|--------|
| U-Net | 0.9517 | 0.8635 | 0.7701 | 0.6626 | 0.9099 |
| Deeplabv3+ | 0.9163 | 0.7153 | 0.6506 | 0.5266 | 0.8559 |
| PSPNet | 0.9116 | 0.7375 | 0.6084 | 0.4704 | 0.8455 |
| HRNet | 0.9581 | 0.8292 | 0.7910 | 0.6968 | 0.9225 |
| **CFENet** | **0.9626** | **0.8277** | **0.8304** | **0.7486** | **0.9317** |

### 3.4 消融实验 (Ablation Study)

**Source:** p.13-14 | S022-S023

**Original:**
Compared with the baseline FCN (ResNet-101), we improve PA/PC/F1/IoU/FWIoU by 0.0168/0.1376/0.05/0.0839/0.0275 by using only the spatial fusion module. The effect of using both the spatial fusion module and the focus enhance module improved over baseline on all five evaluation metrics. When three modules are integrated together, the PA/PC/F1/IoU/FWIoU of CFENet is further improved to 0.9871/0.9370/0.9262/0.8722/0.9751.

**中文:**
与基线FCN（ResNet-101）相比，仅使用空间融合模块就使PA/PC/F1/IoU/FWIoU提升了0.0168/0.1376/0.05/0.0839/0.0275。同时使用空间融合模块和焦点增强模块后，在全部五项评估指标上均超越了基线。当三个模块集成在一起时，CFENet的PA/PC/F1/IoU/FWIoU进一步提升至0.9871/0.9370/0.9262/0.8722/0.9751。

**消融实验结果 (WHU数据集):**

| 配置 | PA | PC | F1 | IoU | FWIoU |
|------|-----|-----|-----|------|--------|
| Baseline (ResNet-101) | 0.9703 | 0.7994 | 0.8762 | 0.7883 | 0.9476 |
| + SFM | 0.9871 | 0.9370 | 0.9262 | 0.8722 | 0.9751 |
| + SFM + FEM | - | - | - | - | - |
| + SFM + FEM + FDM (CFENet) | **0.9871** | **0.9370** | **0.9262** | **0.8722** | **0.9751** |

### 3.5 效率对比

**Source:** p.15-16 | S024-S025

| 方法 | 模型大小(MB) | 参数量(M) | 训练时间(min/epoch) | 推理时间(ms/image) |
|------|-------------|-----------|---------------------|-------------------|
| U-Net | 108.9 | 28.58 | 4.183 | 52.47 |
| Deeplabv3+ | 158.1 | 41.43 | 5.250 | 84.43 |
| PSPNet | 189.8 | 49.75 | 20.383 | 60.97 |
| HRNet | 120.9 | 31.70 | 6.050 | 74.17 |
| **CFENet** | **118.6** | **31.10** | **5.783** | **66.20** |

**关键发现:**
- CFENet模型大小和参数量接近HRNet，远小于Deeplabv3+和PSPNet
- 推理速度（66.20 ms/图像）在精度最优的方法中最快
- 在精度和效率之间取得了良好平衡

---

## 4. 结论与启示 (Conclusions & Implications)

**Source:** p.17 | S026

**Original:**
This paper proposes an end-to-end neural network (CFENet) that can effectively enhance low-level and high-level features and fuse them to obtain strong feature representations for building extraction tasks. Specifically, we introduce the spatial fusion and focus enhancement modules to efficiently enhance the low-level features and high-level features extracted by ResNet-101, respectively. Then the feature decoder module further fuses and enhances the features generated by the spatial fusion module and the focus enhancement module to obtain the final probability map. CFENet achieves superior performance over other methods we have compared on the WHU Building Dataset and the Massachusetts Building Dataset, and significantly improves the extraction accuracy while controlling the computational cost. Moreover, ablation experiments show that our proposed three modules can improve the accuracy of building extraction from remote sensing images.

**中文:**
本文提出了一种端到端的神经网络（CFENet），能够有效增强和融合低层和高层特征，以获得用于建筑物提取任务的强特征表征。具体而言，我们引入了空间融合模块和焦点增强模块，分别高效增强ResNet-101提取的低层特征和高层特征。然后，特征解码模块进一步融合和增强空间融合模块和焦点增强模块生成的特征，以获得最终的概率图。CFENet在WHU建筑物数据集和Massachusetts建筑物数据集上均取得了优于所对比方法的性能，在控制计算成本的同时显著提高了提取精度。此外，消融实验表明，我们提出的三个模块均能提高遥感图像建筑物提取的精度。

---

## 5. 综述引用要点 (Key Points for Citation in Review)

### 5.1 技术定位
- **时期**: CNN时代（2022年，Transformer尚未大规模进入遥感分割）
- **核心创新**: 上下文特征增强——分别对低层特征（空间信息）和高层特征（语义信息）进行增强后再融合
- **三模块架构**: SFM → FEM → FDM

### 5.2 与前人工作的关系
- 继承了FCN + ResNet-101的编码器-解码器范式
- 区别于U-Net的简单跳连、Deeplabv3+的空洞空间金字塔、PSPNet的金字塔池化
- 核心差异：**显式分离低层/高层特征的增强策略**，而非统一的特征融合

### 5.3 局限性（作者自述）
- 各模块的泛化能力有待进一步提升
- 损失函数结构可改进以提升困难样本判别能力
- 遥感图像预处理可进一步优化以提升性能

### 5.4 对综述的价值
- 可作为"CNN/注意力时代（2018-2021）建筑物提取"的代表性方法
- 消融实验数据可用于支撑"多模块协同设计提升精度"的论点
- 效率对比数据可用于讨论"精度-效率权衡"
- **CF系列核心文献**，需在综述中详细展开

---

## 6. 术语表 (Terminology)

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Context Feature Enhancement | 上下文特征增强 | 核心概念 |
| Spatial Fusion Module (SFM) | 空间融合模块 | 低层特征增强 |
| Focus Enhancement Module (FEM) | 焦点增强模块 | 高层特征增强 |
| Feature Decoder Module (FDM) | 特征解码模块 | 特征融合解码 |
| Dilated Convolution | 空洞卷积 | 扩展感受野不损失分辨率 |
| Asymmetric Convolution | 非对称卷积 | 减少参数量 |
| Location Block | 位置块 | 自注意力机制模块 |
| PA (Pixel Accuracy) | 像素精度 | 评估指标 |
| PC (Precision) | 精确率 | 评估指标 |
| F1 Score | F1分数 | 精确率和召回率的调和平均 |
| IoU (Intersection over Union) | 交并比 | 评估指标 |
| FWIoU | 频权交并比 | 评估指标 |
