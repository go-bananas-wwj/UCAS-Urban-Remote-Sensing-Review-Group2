# 高分辨率遥感影像城市路网与建筑物提取方法综述

## 1 引言

### 1.1 研究背景与意义

随着全球城市化进程的持续加速，城市空间结构的动态变化对高精度、高时效性的地理空间数据提出了迫切需求。联合国人居署报告显示，至2050年全球城市化率预计将达到68%，这意味着超过半数的人口将居住在城市环境中[1]。在这一背景下，城市路网与建筑物作为城市空间结构的骨架与核心载体，其精确、快速的自动提取对于城市规划、交通管理、灾害应急响应、自动驾驶导航以及智慧城市建设等前沿应用具有不可替代的战略价值[2,3]。

高分辨率（Very High Resolution, VHR）遥感影像技术的飞速发展为城市精细化制图提供了前所未有的数据基础。当前，商业卫星影像的空间分辨率已达到亚米级甚至分米级（如WorldView-3可达0.31 m），无人机航空影像更可获取厘米级分辨率的影像数据[4]。这些高分辨率数据能够清晰呈现道路标线、建筑轮廓、屋顶材质等丰富的空间细节，为城市要素的精确识别与提取创造了条件。然而，VHR影像中地物细节丰富的同时背景也极为复杂：同类地物（如沥青道路与水泥道路、平顶建筑与坡顶建筑）在光谱与纹理特征上差异显著，而异类地物（如阴影中的建筑与水体、 bareland与浅色道路）则表现出高度的相似性；此外，建筑物阴影、植被遮挡、道路磨损、车辆遮挡以及尺度变化等因素进一步增加了自动提取的难度[5,6]。因此，如何在复杂城市场景中实现道路与建筑物的准确、完整、拓扑一致性的自动提取，始终是遥感图像解译领域的核心挑战之一。

### 1.2 国内外研究现状概述

过去二十年间，城市路网与建筑物提取方法经历了从人工目视解译到自动化智能处理的深刻变革，其技术脉络可概括为三个发展阶段与两次范式跃迁。

**第一阶段：传统图像处理与面向对象分析（约2000—2012年）**。该阶段主要依赖人工设计的图像处理算子（如边缘检测、形态学操作、阈值分割）和面向对象图像分析（Object-Based Image Analysis, OBIA）技术，通过光谱、形状、纹理等低层特征实现地物提取[7,8]。这些方法在简单场景下具有一定效果，但面对VHR影像的复杂性与异质性时，手工特征的表达能力不足，泛化性差。

**第二阶段：机器学习与特征工程（约2012—2015年）**。随着机器学习理论的成熟，研究人员将支持向量机（SVM）、随机森林（RF）、条件随机场（CRF）等分类器与手工特征（HOG、LBP、GLCM等）相结合，显著提升了提取的自动化程度[9,10]。然而，这一范式的核心瓶颈在于特征设计高度依赖专家经验，且特征的表征能力有限，难以捕捉VHR影像中地物的高阶语义信息。

**第三阶段：深度学习端到端模型（2015年至今）**。以全卷积网络（FCN）和U-Net为标志，深度学习实现了从"特征工程"到"架构工程"的范式转变[11,12]。网络自动学习层次化的特征表示，在像素级语义分割任务上取得了突破性进展。此后，多尺度融合、注意力机制、边界细化等技术不断优化分割精度[13,14]。2020年后，Vision Transformer（ViT）将自然语言处理领域的自注意力机制引入视觉任务，突破了卷积神经网络感受野受限的瓶颈[15,16]。2023年以来，以Segment Anything Model（SAM）系列为代表的基础模型（Foundation Model）进一步开启了"知识迁移"的新范式——通过大规模预训练获取通用视觉知识，再以参数高效微调或零样本推理适配下游遥感任务[17,18]。

研究热点的转移同样清晰可见：从早期的像素级语义分割，逐步拓展至实例级精细提取、道路拓扑结构保持、建筑物边界矢量化、多任务联合提取，直至当前备受关注的开放词汇任意目标分割与大模型适配[19,20]。

### 1.3 本文结构与贡献

本文以方法演进为主线，系统梳理从高分辨率遥感影像中提取城市路网与建筑物的技术发展脉络。文章首先介绍常用的基准数据集与评价指标体系（第2章）；随后回顾传统图像处理方法与机器学习方法（第3—4章），为后续深度学习方法的讨论奠定基础；第5章和第6章作为全文核心，分别深入评述基于卷积神经网络的编码器-解码器方法与基于Transformer及基础模型的前沿方法；第7章探讨多源数据融合与多任务联合提取策略；第8章展望三维信息提取的前沿方向；第9章总结当前研究热点并展望未来发展趋势；第10章给出全文结论。本文力求在保持学术严谨性的同时做到图文并茂，为遥感图像解译领域的研究人员提供一份系统、全面的技术参考。

![图1 技术演进时间线框架图](05_图表素材/技术演进时间线.png)

---

## 2 常用数据集与评价指标

### 2.1 代表性数据集

数据集是推动算法发展的重要基石。表1汇总了城市路网与建筑物提取领域最具代表性的公开数据集，涵盖道路提取、建筑物提取以及多类别语义分割三大类型。

**表1 道路与建筑物提取常用数据集汇总**

| 数据集 | 类型 | 分辨率 | 图像尺寸 | 样本量 | 特点 |
|--------|------|--------|----------|--------|------|
| Massachusetts Roads[21] | 道路 | 1 m | 1500×1500 | 1108张 | 美国航拍影像，城乡场景多样 |
| DeepGlobe Road[22] | 道路 | 0.5 m | 1024×1024 | 6226张 | CVPR竞赛标准数据集，东南亚卫星影像 |
| CHN6-CUG[23] | 道路 | 0.3–1 m | 变长 | 大量 | 中国道路数据集，复杂城乡场景 |
| SpaceNet[24] | 道路/建筑 | 0.3–1 m | 变长 | 大规模 | 全球多城市覆盖，附带道路宽度属性 |
| WHU Building[25] | 建筑物 | 0.075–1 m | 变长 | 大量 | 航空+卫星双版本，建筑密集区 |
| Inria Aerial Image[26] | 建筑物 | 0.3 m | 5000×5000 | 360张 | 欧美城市，高建筑密度 |
| xBD[27] | 建筑物 | 0.8 m | 1024×1024 | 大量 | 灾后建筑影像，含损毁等级标注 |
| OpenEarthMap[28] | 多类 | 0.25–1 m | 变长 | 大量 | 全球覆盖，支持开放词汇评测 |
| LoveDA[29] | 多类 | 0.3 m | 1024×1024 | 5987张 | 城乡域自适应分割基准 |
| URUR[30] | 多类 | VHR | 5120×5120 | 3008张 | 8类地物，超高分大场景 |
| OSM[31] | 道路/建筑 | 全球矢量 | 矢量数据 | 全球覆盖 | 众包开源地图，常用作训练标签或精度验证参考 |

在上述数据集中，Massachusetts Roads和DeepGlobe Road是道路提取领域最为广泛采用的基准；WHU Building和Inria Aerial Image则是建筑物提取的主流评测数据集。近年来，OpenEarthMap和LoveDA等多类别数据集的出现，为开放词汇分割和域自适应研究提供了新的评测平台。此外，OpenStreetMap（OSM）作为全球众包矢量地图，虽非专门构建的影像数据集，但其丰富的道路与建筑物标注常被用作弱监督学习的标签来源或精度验证的参考标准[31]。

### 2.2 评价指标

根据提取任务的不同，评价指标可分为像素级、拓扑级和实例级三个层次。

**像素级指标**是语义分割任务中最基础的度量方式，包括：
- **总体精度（OA, Overall Accuracy）**：正确分类像素数占总像素数的比例；
- **交并比（IoU, Intersection over Union）**：预测区域与真实区域交集与并集之比，是道路与建筑物提取中最常用的核心指标；
- **F1-score / Dice系数**：精确率（Precision）与召回率（Recall）的调和平均，兼顾漏提与误提；
- **精确率与召回率**：分别衡量模型抑制假阳性和捕获真阳性的能力。

**拓扑级指标**专门针对道路网络提取的连通性评价而设计，包括：
- **TOPO score**：基于图同构匹配的拓扑正确率，评估预测道路图与真实道路图的拓扑一致性；
- **APLS（Average Path Length Similarity）**：计算预测图与参考图间最短路径长度的相似度；
- **SP（Shortest Path）**：基于路径连通性的相似性度量。

**建筑物专用指标**则更关注轮廓精度：
- **Boundary IoU**：专门衡量预测边界与真实边界的重叠程度；
- **多边形Hausdorff距离**：评估建筑物轮廓的几何偏差。

---

## 3 传统提取方法

### 3.1 基于图像处理的方法

在深度学习兴起之前，遥感影像的道路与建筑物提取主要依赖经典数字图像处理技术。道路因其细长线性特征，常采用边缘检测算子（如Canny、Sobel）提取候选边缘，再通过霍夫变换（Hough Transform）检测直线段并进行连接，辅以形态学开闭运算填补断裂、去除噪声[32,33]。对于建筑物提取，阈值分割（如OTSU自适应阈值）和区域生长算法利用屋顶区域的光谱一致性进行初始分割，随后通过形状规则性（如矩形度、长宽比）筛选候选建筑物[34]。主动轮廓模型（Snakes）则通过能量函数最小化驱动初始轮廓演化至目标边界，在建筑物轮廓提取中有一定应用[35]。

这类方法的共同特点是不需要训练样本，计算开销小，在背景简单、地物对比度高的场景中能够取得可接受的效果。然而，其局限性也十分突出：所有算子和参数均需人工设计，对影像的光照条件、传感器类型高度敏感，泛化能力极差；面对VHR影像中复杂的城市背景（如树木遮挡、建筑阴影、道路磨损）时，手工规则难以穷尽所有场景变化，导致提取结果碎片化严重。

![图2 传统图像处理方法示例](05_图表素材/pdf_extracted_images/E06_Qian_ISPRS_p3_img1.png)

### 3.2 面向对象图像分析

面向对象图像分析（OBIA）代表了从"像素"到"对象"的分析范式转变[36]。其基本流程为：首先利用多尺度分割算法（如分形网络演化算法，FNEA）将影像分割为光谱同质的对象；随后提取每个对象的光谱、形状、纹理及上下文特征；最后基于规则或分类器进行对象级识别。OBIA特别适用于建筑物提取，因为建筑物在VHR影像中表现为具有规则几何形状和特定上下文关系（如与阴影相邻）的同质对象[37]。

Blaschke等[36]系统综述了OBIA在遥感领域的应用，指出多尺度分割是OBIA的核心，但分割尺度参数的选择直接影响后续分类精度——尺度过小导致建筑物被过度分割，尺度过大则引起"同谱异物"的混分问题。邵振峰等[38]将智能优化学习引入OBIA框架，通过优化算法自适应选择分割参数，提升了高分辨率遥感影像语义分割的精度。尽管OBIA在一定程度上缓解了像素级分析的噪声敏感问题，但其对分割参数的依赖以及高分辨率影像中普遍存在的"同物异谱"和"同谱异物"现象，仍然限制了其在大范围城市场景中的应用效果。

![图3 OBIA多尺度分割效果对比](05_图表素材/图3_OBIA多尺度分割.png)

### 3.3 小结

传统图像处理方法和OBIA技术奠定了遥感目标提取的方法论基础，在特定简单场景下至今仍有应用价值。然而，面对VHR影像的高度复杂性与异质性，手工设计特征和规则的表达能力存在本质瓶颈，难以实现大范围、高精度的自动化提取。这一矛盾直接推动了数据驱动方法——尤其是机器学习与深度学习——的快速发展。

---

## 4 机器学习方法

### 4.1 基于手工特征与经典分类器

机器学习方法的核心思想是将特征工程与分类器训练分离：由专家设计区分性特征，再由分类器学习特征到类别的映射关系。在道路与建筑物提取中，常用的手工特征包括：局部二值模式（LBP）、方向梯度直方图（HOG）、灰度共生矩阵（GLCM）纹理特征、Gabor滤波响应以及光谱和形状特征等[39,40]。分类器方面，支持向量机（SVM）因其在小样本高维数据上的优良泛化能力而被广泛采用；随机森林（RF）通过集成多棵决策树提升分类稳定性；条件随机场（CRF）则通过建模像素间的空间上下文依赖，有效减少了分类结果中的"椒盐噪声"[41,42]。

典型的应用模式为：在影像上以滑动窗口方式提取局部特征向量，输入分类器进行逐像素或逐窗口预测，最后通过形态学后处理优化结果。例如，卢晓燕等[43]面向大范围高分辨率遥感影像道路提取，综合多种光谱与几何特征，结合SVM分类器实现了较高精度的道路初提取。然而，这一范式的根本局限在于：特征的设计高度依赖领域专家的先验知识，且手工特征对影像条件（传感器、季节、光照）的变化极为敏感，跨场景泛化能力有限。

### 4.2 面向对象的机器学习方法

为进一步利用空间上下文信息，研究者将OBIA与机器学习分类器相结合。具体而言，先通过多尺度分割生成影像对象，再为每个对象提取光谱、几何、纹理及邻域关系特征向量，最后用RF、SVM或CRF进行分类[44]。相较于像素级方法，对象级分类能够有效抑制高频噪声，并利用道路与建筑物之间的空间上下文关系（如建筑物通常沿道路分布）提升提取精度。

概率图模型在这一阶段也得到了重要应用。马尔可夫随机场（MRF）和条件随机场（CRF）通过定义像素/对象间的势能函数，将空间平滑性约束引入分类过程，显著改善了提取结果的视觉连续性[45]。然而，无论是特征工程还是图模型设计，其核心矛盾仍未解决：人工设计的特征表达能力存在上限，难以捕捉VHR影像中地物的高阶语义与抽象模式。

### 4.3 小结

机器学习方法通过系统化的特征组合与先进的分类器优化，将遥感目标提取的自动化水平提升到了新的高度。但其本质仍属于"浅层表示学习"——特征的区分能力受限于专家设计的边界，无法从数据中自动发现更深层次的表征模式。2015年后，以深度学习为代表的"端到端表示学习"范式彻底打破了这一瓶颈，开启了遥感目标提取的新纪元。


---

## 5 深度学习I：CNN与编码器-解码器时代

### 5.1 全卷积网络与端到端语义分割

2015年是遥感目标提取领域的里程碑之年。Long等[46]提出的全卷积网络（FCN）首次实现了端到端的像素级语义分割——通过将分类网络（如VGG、ResNet）中的全连接层替换为卷积层，并引入反卷积进行上采样，FCN能够接受任意尺寸的输入影像并输出同分辨率的分割图。这一架构革新彻底摒弃了传统方法中繁琐的特征工程和后处理流程，开创了"端到端表示学习"的新范式。

同年，Ronneberger等[47]针对医学影像分割提出了U-Net架构，其编码器-解码器结构配合跳跃连接（Skip Connection）的设计，在融合高层语义信息与低层空间细节方面展现出卓越性能。U-Net很快跨越医学影像领域，在遥感道路与建筑物提取中取得了巨大成功[48,49]。其成功的原因在于：VHR遥感影像中道路和建筑物的精细边界提取极度依赖低层空间细节，而跳跃连接恰好将编码器浅层的高分辨率特征直接传递至解码器，有效缓解了深层网络中的空间信息损失。此后，研究者围绕U-Net展开了大量改进工作：残差U-Net（ResU-Net）[50]引入残差连接缓解梯度消失；密集连接U-Net通过特征复用增强信息流；注意力门控U-Net（Attention U-Net）[51]则利用门控机制抑制无关区域的特征响应，进一步提升了分割精度。

SegNet[52]是另一款经典的编码器-解码器网络，其创新之处在于利用编码器中的最大池化索引指导解码器进行非线性上采样，在保持边界定位精度的同时显著减少了模型参数量。这些基于CNN的编码器-解码器架构为后续遥感专用网络的设计奠定了坚实基础。

图4展示了从传统机器学习方法（SVM）到纯U-Net、再到U-Net结合条件随机场（CRF）后处理的技术演进效果对比。可以清晰看到，SVM方法产生大量噪声和碎片化结果；U-Net通过端到端学习显著改善了分割质量，但边界仍存在锯齿；加入CRF后处理后，建筑物轮廓更加平滑准确；级联CRFs进一步细化边界细节。这一对比直观地印证了从"特征工程"到"架构工程"再到"后处理优化"的范式转变所带来的性能增益。

![图4 从SVM到U-Net+级联CRFs的建筑物提取效果对比](05_图表素材/pdf_extracted_images/C10_p6_img1.png)
>
> （引自陈嘉浩等：左列为原始影像与标签，右四列依次为SVM、U-Net、U-Net+CRFs、U-Net+级联CRFs的提取结果，清晰展示了从传统机器学习到深度学习+后处理的技术演进效果）

![图5 经典编码器-解码器架构示意图](05_图表素材/图4_编码器解码器架构简图.png)
> （自绘：左侧为U-Net的编码器-解码器+跳跃连接结构；右侧为DeepLabV3+的ASPP模块+解码器结构）

### 5.2 多尺度与上下文建模

VHR遥感影像中地物尺度变化剧烈：同一张影像中可能同时包含宽阔的城市主干道（宽度数十米）和狭窄的乡村小路（宽度不足两米），建筑物也存在从独立别墅到大型商业综合体的巨大尺度差异。为应对这一挑战，多尺度上下文建模成为CNN时代的核心研究方向之一。

Chen等[53]提出的DeepLab系列是该方向的标杆工作。DeepLabV3+采用空洞卷积（Atrous Convolution）在不损失空间分辨率的前提下扩大感受野，并设计了空洞空间金字塔池化模块（ASPP），以多个不同采样率的空洞卷积并行捕获多尺度上下文信息。该架构在建筑物和道路提取任务中得到了广泛应用[54,55]。D-LinkNet[56]则专门针对道路提取场景进行了优化：在LinkNet的高效编码器-解码器结构基础上，引入多条并行的空洞卷积分支，显著增强了对细长道路结构的感知能力，成为道路提取领域广泛采用的基准方法之一。

金字塔场景解析网络（PSPNet）[57]通过金字塔池化模块聚合不同尺度的全局上下文，有效改善了复杂场景中的分类一致性。这些多尺度方法的核心思想可概括为：通过扩大感受野或并行多尺度特征提取，使模型同时具备捕捉局部细节和全局上下文的能力。然而，如图6所示，基于局部patch的方法在处理大范围遥感影像时面临根本性挑战：当使用小尺度patch进行推理时，模型缺乏全局上下文感知，导致道路拓扑连接中断；而TopoRF-Net通过多尺度特征融合和大感受野设计，能够在保持局部细节的同时恢复正确的拓扑结构。在局部尺度上，patch-based方法的预测结果存在过度平滑问题，而多尺度特征聚合策略能够保留道路的精细几何结构。

![图6 基于patch的方法与多尺度全局方法的道路提取对比](05_图表素材/pdf_extracted_images/E08_p2_img1_whitebg.png)
>
> （引自TopoRF-Net：上半部分展示全局尺度下小patch导致拓扑断裂 vs 多尺度方法保持拓扑连通；下半部分展示局部尺度下patch-based过度平滑 vs 多尺度特征聚合保留精细结构）

### 5.3 面向遥感任务的专用网络设计

在通用分割架构的基础上，研究者针对遥感影像的特殊性设计了专用网络。其中，Chen等[58]提出的级联特征增强网络（CFENet）是面向高分辨率遥感影像建筑物提取的代表性工作。CFENet针对建筑物尺度变化剧烈和边界模糊两大难题，设计了三个核心模块：**尺度融合模块（SFM）**通过多支路特征融合整合浅层细节与深层语义；**特征增强模块（FEM）**引入通道-空间双注意力机制增强关键特征响应；**特征分布模块（FDM）**对特征分布进行调制，缓解同类建筑物内部的特征差异和异类地物间的特征混淆。在WHU Aerial数据集上，CFENet取得了92.3%的IoU；在Massachusetts Buildings数据集上达到73.8%的IoU，验证了专用架构设计的有效性。

此外，Ran等[59]提出的BMFRNet通过双分支多尺度特征精炼策略增强了边界感知能力；罗松强等[60]设计了多尺度特征增强的ResUNet++，在建筑物提取任务中取得了良好效果。这些工作表明，针对遥感地物特点进行网络结构的定制化设计，能够有效提升专用场景下的提取性能。如图7所示，CFENet通过特征增强模块对建筑物边缘进行精细化处理，在WHU Aerial数据集上的局部放大区域中，可以清晰看到CFENet对建筑物边界的准确定位和对细小结构的完整保留，验证了专用架构设计在边界精度方面的显著优势。

![图7 CFENet建筑物提取细节效果（WHU Aerial数据集局部放大）](05_图表素材/pdf_extracted_images/E05_p11_img2.png)
>
> （引自CFENet Chen et al., 2022：红色框标注区域的放大对比，展示专用网络对建筑物边缘和细节的精细提取能力）

### 5.4 边界细化与损失函数设计

像素级分割结果向实际制图应用转换时，边界精度至关重要。为此，研究者从网络设计和损失函数两个层面进行了深入研究。在网络层面，边界感知模块通过显式建模目标轮廓来增强边界定位能力；在损失函数层面，传统交叉熵损失对边界像素的惩罚不足，因此研究者提出了多种改进方案：Dice损失[61]直接优化区域重叠度，对类别不平衡更鲁棒；Lovász-softmax损失[62]基于子模函数优化IoU的下界，更适合以IoU为评价指标的任务；边界感知损失则在分割损失基础上增加边界惩罚项，迫使网络关注轮廓区域[63]。田普光等[64]将加权交叉熵、Dice损失和边界损失相结合，显著提升了U-Net网络的建筑物边界提取精度。此外，陈嘉浩等[65]采用级联条件随机场（CRF）作为后处理步骤，对U-Net的初步分割结果进行边界精细化修正，进一步改善了建筑物轮廓的平滑性和准确性。

### 5.5 道路拓扑保持的早期探索

与建筑物提取不同，道路提取不仅要求像素级精度，更强调路网拓扑结构的完整性与连通性——断裂的道路或遗漏的交叉口将直接影响导航系统的可用性。早期基于CNN的方法主要优化像素级指标，往往产生大量拓扑断裂，促使研究者探索拓扑保持策略。

He等[66]提出的Sat2Graph将道路提取重新建模为图生成问题，直接从影像预测道路中心线图，将拓扑结构嵌入输出表示中。Xu等[67]的RNGDet++采用迭代式拓扑恢复策略，逐步检测道路节点并预测连接关系，在拓扑正确性方面取得了显著进展，但计算开销较大。在损失函数层面，Mosinska等[68]指出传统的像素级损失（如BCE）仅执行局部判别，无法惩罚微小像素错误导致的重大拓扑破坏，因此提出了基于中心线Dice和Deep Distance Transform（DDT）的结构感知损失。近期，Fu等[69]提出的TopoRF-Net从网络架构层面系统解决了拓扑保持问题：其多感受野增强模块（MRFE）通过并行的3×3、5×5、7×7深度可分离卷积捕获多尺度道路模式；连通性感知解码器（CI-Decoder）利用方向性蛇形卷积显式感知道路曲线与交叉口的几何特征；拓扑一致性损失则显式约束训练过程中道路网络的全局连通性。在DeepGlobe数据集上，TopoRF-Net取得了69.76%的IoU和82.18%的F1-score，同时在拓扑连通性指标上显著优于现有方法。

### 5.6 小结

CNN与编码器-解码器时代标志着遥感道路/建筑物提取从"特征工程"到"架构工程"的范式转变。U-Net及其变体成为该阶段的绝对主流架构，多尺度融合、注意力机制、边界细化和拓扑保持构成了四大技术主线。专用网络（如CFENet、TopoRF-Net）的设计表明，针对遥感场景特点进行架构定制能够带来显著的性能增益。然而，卷积操作固有的局部性决定了CNN的感受野随网络深度线性增长，对于建模长距离空间依赖关系仍存在根本性的结构限制。这一局限为Transformer架构的引入提供了契机。

![表2 CNN时代代表性方法对比](05_图表素材/表2_CNN时代方法对比.png)

---

## 6 深度学习II：Transformer与基础模型时代

### 6.1 Vision Transformer在遥感分割中的兴起

2020年，Dosovitskiy等[70]在ICLR 2021发表的Vision Transformer（ViT）彻底改变了计算机视觉领域的格局。ViT将图像切分为固定大小的patch序列，利用Transformer的自注意力机制建模全局依赖关系，在ImageNet分类任务上首次证明纯Transformer架构可以超越CNN。随后，Liu等[71]在ICCV 2021（获最佳论文奖）提出的Swin Transformer引入了层次化窗口注意力与移位窗口机制，将计算复杂度从与图像尺寸成平方关系降低至线性关系，同时保留了多尺度特征表示能力。Swin Transformer迅速成为遥感图像分割任务的新一代主干网络，Swin-UNet[72]等变体将U形结构与Swin Transformer相结合，在多个遥感数据集上取得了优于CNN-based方法的性能。

然而，ViT系列模型的原始设计存在两个不利于遥感应用的特点：其一，自注意力的二次计算复杂度使其难以直接处理高分辨率遥感影像；其二，全局注意力缺乏CNN所具有的归纳偏置（局部性与平移等变性），在小样本遥感数据集上容易过拟合。这些挑战推动了高效Transformer分割网络的研究。

### 6.2 高效Transformer分割网络

Xie等[73]在NeurIPS 2021发表的SegFormer是Transformer时代轻量化高效分割的代表作。SegFormer采用Mix Transformer（MiT）作为编码器，通过逐层递减的patch嵌入和高效自注意力实现多尺度特征提取；解码器则是一个纯粹的全MLP结构，无需复杂的上采样操作即可融合多尺度特征并输出分割结果。这种"轻编码器+极简解码器"的设计在ADE20K和Cityscapes数据集上取得了当时的最优性能，同时保持了较高的推理效率。SegFormer的MiT主干在遥感建筑物提取中同样表现出色，并且为后续基于SAM 3的方法（如SegEarth-OV3）提供了语义分割头的backbone参考。在遥感专用Transformer方面，Wang等[74]探索了ViT在建筑物提取中的应用；Chen等[75]则引入高度约束的Transformer架构，结合LiDAR数据提升了建筑物的三维提取能力。

![图8 SegFormer编码器-解码器架构示意图：层次化Mix Transformer编码器与轻量All-MLP解码器](05_图表素材/图X_SegFormer架构.png)
> （引自SegFormer Xie et al., NeurIPS 2021：MiT编码器通过逐层递减的patch嵌入提取多尺度特征，All-MLP解码器直接融合多级特征并输出分割结果）

### 6.3 SAM系列：从视觉提示到概念提示

2023年以来，以Segment Anything Model（SAM）系列为代表的基础模型（Foundation Model）引发了遥感目标提取领域的深刻变革。与传统专用模型不同，基础模型通过大规模无标注或弱标注数据的预训练获取通用视觉知识，再以参数高效微调或零样本推理的方式适配下游任务，显著降低了对领域标注数据的依赖。

#### 6.3.1 SAM：分割一切的基石

Kirillov等[17]提出的SAM是这一浪潮的起点。SAM由基于ViT的图像编码器、轻量化的提示编码器和掩码解码器组成，支持点、框、掩码等视觉提示（Visual Prompt）进行可提示的视觉分割（PVS）。其数据引擎在1100万张图像上生成了超过11亿个掩码，通过规模化的自监督标注策略赋予了SAM强大的零样本泛化能力。然而，SAM的预训练数据以自然图像为主，直接应用于遥感VHR影像时面临域差异问题：道路和建筑物在遥感视角下呈现迥异的几何与纹理特征，导致SAM的初始分割结果在遥感场景中精度有限。

#### 6.3.2 SAM在遥感中的适配

为将SAM的通用能力迁移至遥感领域，研究者探索了多种参数高效微调（PEFT）策略。Feng等[76]在IEEE GRSL 2024发表的Road-SAM是其中的典型代表。Road-SAM冻结SAM的ViT图像编码器，在Transformer block中插入三种轻量级adapter（串联、并联、混合结构），仅训练约10%的参数。更具创新性的是其显式视觉提示（EVP）机制：通过快速傅里叶变换提取影像的高频分量（HFC），将道路边缘和纹理等细节信息作为任务特定的视觉提示注入网络，引导模型关注道路的精细结构。在URUR超高分数据集（5120×5120）上，Road-SAM取得了73.29%的F1-score；在DeepGlobe数据集上达到81.65%的F1-score，验证了参数高效微调策略在大模型遥感适配中的有效性。如图9所示，Road-SAM的Adapter机制在冻结SAM原始ViT编码器的同时，在Transformer block中插入轻量级的可训练Adapter模块，通过串联、并联和混合三种结构实现参数高效微调，仅训练约10%的参数即可完成遥感道路提取任务的域适配。

![图9 Road-SAM的Adapter参数高效微调机制示意图](05_图表素材/pdf_extracted_images/E12_p2_img1.png)
>
> （引自Road-SAM Feng et al., IEEE GRSL 2024：展示Frozen ViT block与Tunable Adapter的协同工作方式）RSAM-Seg[77]则进一步将SAM适配框架推广至通用遥感语义分割任务。

#### 6.3.3 SAM-Road与SAM-Road++：拓扑保持的道路提取

Hetang等[78]在CVPR 2024提出的SAM-Road开创了两阶段的道路提取新范式：第一阶段利用SAM的零样本分割能力生成道路候选掩码，并通过几何简化提取道路节点；第二阶段利用图网络恢复道路的拓扑连接关系。这种"Foundation Model + 传统拓扑方法"的融合策略兼具了SAM强大的泛化能力和图网络对拓扑结构的精确建模能力，同时速度比RNGDet++快40倍。Yin等[79]在此基础上提出了SAM-Road++，引入节点引导重采样（Node-Guided Resampling）策略和Extended-Line端点连接机制，将方法扩展至城市级大范围道路提取场景，在全球尺度数据集上验证了foundation model与传统拓扑方法融合的有效性。如图10所示，SAM-Road在大范围城市区域的道路提取中展现出优异性能：三列对比展示了不同方法在同一区域的道路提取结果，SAM-Road不仅能够准确定位主干道路，还能有效恢复复杂的交叉路口和细枝末节的支路网络，其拓扑完整性显著优于传统分割方法。

![图10 SAM-Road大范围道路提取效果对比](05_图表素材/pdf_extracted_images/E01_p8_img1.png)
>
> （引自SAM-Road Hetang et al., CVPR 2024：同一区域三种方法的道路提取结果对比，展示SAM-Road在城市复杂路网中的拓扑保持能力）

#### 6.3.4 SAM 3：概念提示分割的新范式

2025年，Carion等[80]在Meta发表的SAM 3将可提示分割从"视觉提示"推进至"概念提示"的新阶段。SAM 3支持文本名词短语（如"所有黄色的校车"）、图像示例或两者的组合作为输入提示，执行可提示概念分割（Promptable Concept Segmentation, PCS）——即检测、分割并追踪输入中所有匹配该概念的目标实例。其核心架构由一个基于DETR的图像检测器和一个继承自SAM 2的视频追踪器组成，两者共享Perception Encoder（PE）主干。SAM 3的关键创新在于Presence Head的设计：通过引入一个可学习的全局presence token，将"识别（what）"与"定位（where）"解耦，使proposal query只需解决条件定位问题，从而显著提升开放词汇检测精度。SAM 3的数据引擎规模空前：利用人机协同和AI辅助验证，构建了包含400万个唯一概念和5200万个掩码的SA-Co高质量数据集，以及含3800万个概念和14亿掩码的合成数据集。在零样本LVIS基准上，SAM 3达到48.8的mask AP，超越此前最优的38.5；在新的SA-Co基准上超越baseline至少2倍。推理效率方面，在H200 GPU上处理单张图像仅需30毫秒，视频场景下可维持约5个并发对象的近实时性能。

#### 6.3.5 SegEarth-OV3：SAM 3在遥感中的零样本应用

SAM 3的强大能力为遥感开放词汇分割带来了全新可能。Li等[81]提出的SegEarth-OV3是SAM 3在遥感领域的首个系统性探索。该方法无需任何额外训练，直接利用SAM 3的预训练权重在20个遥感语义分割数据集和3个变化检测数据集上取得了优异性能。SegEarth-OV3的核心策略包括：**双头掩码融合**——利用SAM 3的语义分割头处理无定形的"stuff"类别（如道路、裸地），利用Transformer decoder（实例头）处理可数的"things"类别（如建筑物、车辆），通过max-fusion实现优势互补；**存在性引导过滤**——利用SAM 3的presence score抑制遥感大词汇表中的假阳性预测。在OpenEarthMap等多类别数据集上，SegEarth-OV3的平均mIoU达到53.4%，超越此前最优的训练无关方法CorrCLIP 12.7个百分点。在专用提取任务中，WHU Aerial Buildings的IoU达到86.9%（零样本），DeepGlobe Road的IoU为39.3%（零样本无训练）。尽管与专用监督方法相比仍有差距，但SegEarth-OV3充分展示了foundation model在遥感开放词汇分割中的巨大潜力，预示了"无训练零样本提取"这一全新方向的可行性。

![图11 SAM 3概念提示分割范式：从视觉提示（点/框）到概念提示（文本名词短语）的跃迁](05_图表素材/图X_SAM3概念提示分割.png)
> （引自SAM 3 Carion et al., Meta 2025：左列为SAM 1/2的视觉提示分割（单目标），右列为SAM 3的概念提示分割（文本驱动全实例分割））

### 6.4 开放词汇与多模态大模型趋势

SAM 3的出现并非孤立现象，而是开放词汇视觉理解大趋势的缩影。CLIP[82]通过大规模图像-文本对预训练实现了视觉-语义对齐，催生了一系列CLIP-based的开放词汇分割方法（如MaskCLIP、SegEarth-OV）。然而，CLIP的图像级预训练目标导致其在密集预测任务中边界定位粗糙，需要借助SAM等辅助模型进行结构指导。SAM 3的统一架构将检测、分割和追踪集成于单一模型中，相比CLIP+SAM的组合式pipeline更为简洁高效。展望未来，SAM 3与多模态大语言模型（MLLM）的结合将进一步拓展其能力边界——用户可以通过自然语言描述（如"提取所有被植被部分遮挡的乡间土路"）直接驱动遥感影像的复杂目标提取，这将深刻改变人机交互式的遥感解译模式。

![图12 SegEarth-OV3在遥感影像上的零样本开放词汇分割效果](05_图表素材/图X_SegEarth_OV3零样本分割.png)
> （引自SegEarth-OV3 Li et al., 2025：(a)原始遥感影像，(b)SAM 3零样本分割结果，道路与建筑物在无训练条件下被正确识别）

### 6.5 小结

Transformer与基础模型时代代表了遥感道路/建筑物提取的三重范式跃迁：
- **从局部到全局**：自注意力机制突破了CNN感受野的物理限制，实现了真正意义上的全局依赖建模；
- **从封闭到开放**：开放词汇分割打破了预定义类别集合的约束，使模型能够理解任意文本描述并进行对应目标的分割；
- **从专用到通用**：Foundation Model的大规模预训练知识大幅降低了下游遥感任务对领域标注数据的依赖，参数高效微调甚至零样本推理成为可能。

然而，当前foundation model在遥感专用场景（如细小道路、密集建筑群、复杂城中村）上的精度仍有提升空间。如何在保持通用能力的同时，通过领域适配（domain adaptation）、提示工程（prompt engineering）和轻量化解耦进一步提升遥感专用精度，是下一阶段的核心研究方向。

![表3 SAM系列方法对比](05_图表素材/表3_SAM系列方法对比.png)

![图13 SAM系列架构演进示意图](05_图表素材/图5_SAM系列架构演进.png)
> （自绘：展示SAM(2023)的PVS架构 → SAM-Road++(2024)的几何+拓扑两阶段架构 → SAM 3(2025)的统一PCS架构）

---

## 7 多源融合与多任务学习方法

### 7.1 多源数据融合

单一光学遥感影像在复杂城市环境中存在固有的信息局限：光谱相似性导致道路与bareland、建筑物与阴影易于混淆。多源数据融合通过引入互补信息源，有效缓解了这一问题。光学影像与LiDAR点云的融合是其中最为成功的方向之一——LiDAR提供的高度信息能够清晰区分建筑物与裸地、道路与停车场[75]。SAR（合成孔径雷达）数据不受光照和天气条件限制，可与光学影像形成全天候互补。数字表面模型（DSM）和数字地形模型（DTM）则为建筑物高度提取和道路坡度分析提供了三维几何约束。多光谱与高光谱数据的光谱分辨率优势，有助于区分沥青道路与水泥屋顶等材质相似但光谱特性不同的地物。范荣双等[83]系统综述了基于深度学习的高分辨率遥感影像建筑物提取方法，指出多源数据融合是提升提取精度的关键路径之一。

### 7.2 多任务联合提取

建筑物与道路在空间分布上存在强相关性——建筑物通常沿道路两侧分布，道路网络则连接着不同的建筑群。这一空间互补关系为多任务联合学习提供了物理基础。Guo等[84]在IEEE TGRS 2024发表的CRIN（Cross-task and Cross-scale Interaction Network）是这一方向的标志性工作。该研究通过可视化分析发现：仅使用建筑物标签训练的U-Net在特征空间中自动学习了道路区域的信息，反之亦然。基于这一观察，CRIN设计了多任务交互模块（MTI），将特征空间显式分离为建筑物专用、道路专用和任务共享三个子空间，在共享空间中实现跨任务信息互补，在专用空间中保留任务独特性，有效缓解了简单多任务学习中常见的"跷跷板现象"（一个任务性能提升导致另一任务下降）。此外，跨尺度交互模块（CSI）通过尺度注意力机制自适应地为不同任务选择最优感受野（7×7、11×11、21×21），并以行列分解策略将计算量降至传统大核卷积的1/600。实验表明，CRIN以单模型同时提取建筑物和道路，推理时间减半，且两个任务的精度均优于独立训练的单任务模型。

### 7.3 多尺度与跨分辨率处理

VHR遥感影像的分辨率跨度巨大（从卫星亚米级到航空厘米级），不同分辨率下同一地物的视觉特征差异显著。针对超高分大场景影像（如URUR的5120×5120像素），直接输入网络会导致显存溢出，因此需要设计高效的分块-融合推理策略。滑窗重叠推理是最直接的方案，但边界效应和计算冗余是需要权衡的问题。金字塔特征融合结构（如FPN、PANet）通过自顶向下的特征融合，在不同分辨率层级上同时优化大目标和小目标的分割效果。域自适应技术则致力于消除不同传感器、不同分辨率数据之间的域差异，使模型在跨分辨率场景中保持稳定性能[29]。

### 7.4 小结

多源融合与多任务学习代表了遥感目标提取从"单一数据源、单一目标"向"多源协同、多目标联合"的发展趋势。多源数据的互补信息能够有效突破单一模态的感知瓶颈，而多任务联合学习则通过挖掘地物间的空间相关性实现了"1+1>2"的效果。然而，多源数据的精确配准、异构特征的有效对齐、多任务损失函数的动态平衡等问题仍是制约该方法大规模应用的瓶颈。

![表4 多源融合与多任务方法对比](05_图表素材/表4_多源融合方法对比.png)

---

## 8 三维建筑物与道路信息提取

### 8.1 三维建筑物提取

二维轮廓提取虽然是当前遥感解译的主流，但三维几何信息（高度、体积、立面结构）对于城市三维建模、容积率分析、太阳能潜力评估和通风模拟等高级应用至关重要。如图14所示，当前三维建筑物提取已形成三条并行发展的技术路线。

**路线一：影像-DSM融合方法。** 从卫星立体像对（如WorldView、GeoEye）或多视角航空影像中，通过半全局匹配（SGM）或多视角立体（MVS）算法重建数字表面模型（DSM），再利用DSM与数字地形模型（DTM）的差值获取 normalized DSM（nDSM），从而将二维语义分割轮廓赋予高度信息。该方法的优势在于数据源广泛、成本较低，但受限于立体匹配的精度——在纹理匮乏区域（如水面、大面积屋顶）和遮挡边界处，DSM往往存在高程跳变和空洞，导致建筑物高度估计失真。为此，研究者将深度学习引入DSM优化：Alidoost等[85]利用生成对抗网络对低质量DSM进行超分辨率重建和空洞修复；Shu等[86]提出端到端的"影像→三维模型"网络，直接从多视角影像回归建筑物三维边界框和高度。

**路线二：LiDAR点云深度学习方法。** 机载和车载LiDAR以厘米级精度获取海量三维点云，为建筑物精细建模提供了高质量数据。PointNet[87]开创性地利用共享多层感知机（MLP）和对称函数（max pooling）实现了无序点云的特征学习；PointNet++[88]进一步引入层次化特征聚合结构，通过球查询和k近邻构建局部点集，在多尺度上逐步抽象几何特征。后续发展中，KPConv[89]以核点卷积替代传统点云卷积，在不规则点云上实现了与规则网格CNN相当的表达能力；PointTransformer[90]则将自注意力机制引入点云处理，在多个三维基准数据集上取得了优异性能。在遥感建筑物提取中，直接对机载LiDAR点云进行实例分割，可同时获取建筑物的平面轮廓和立面细节，避免了"影像→DSM→三维"级联 pipeline 中的误差累积。然而，点云数据的获取成本高昂、覆盖范围有限，制约了该方法的大范围推广。

**路线三：神经辐射场与三维高斯溅射。** 神经辐射场（NeRF）[91]通过多层感知机将三维空间坐标和视角方向映射为颜色和密度，从多视角影像中学习隐式三维场景表示。其改进版本Instant-NGP[92]利用哈希编码将训练速度提升了数个数量级，使得城市级场景的三维重建成为可能。2023年提出的三维高斯溅射（3D Gaussian Splatting, 3DGS）[93]以显式的三维高斯椭球替代NeRF的隐式网络，在保持渲染质量的同时实现了实时渲染和显式几何编辑。这两项技术为从无人机影像和街景影像中提取建筑物精细三维模型开辟了新路径——用户仅需环绕拍摄一组照片，即可在数分钟内重建出带有纹理的三维网格模型。不过，NeRF和3DGS目前主要适用于小规模精细场景，对于卫星和航空级别的城市场景，其训练效率和几何精度仍有待提升。

如图14所示，三条技术路线最终 converge 于统一的CityGML或IFC标准三维矢量模型，但其数据源、处理流程和适用场景各不相同，在实际应用中需根据精度需求、数据可用性和计算资源进行权衡选择。

![图14 三维建筑物与道路信息提取技术路线示意图](05_图表素材/图11_三维建筑物提取技术路线.png)
>
> （自绘：展示从立体影像/DSM、LiDAR点云、NeRF/3DGS三条技术路线到三维建筑物模型和三维道路网络的技术流程）

### 8.2 三维道路网络提取

三维道路信息对于自动驾驶高精地图、交通规划和基础设施维护具有关键意义。当前的主流策略是"先二维后三维"：首先利用前述深度学习方法提取道路中心线或区域分割结果，再与DSM叠加赋予高程信息，进而构建包含坡度、曲率、超高（superelevation）和横断面属性的三维道路图网络。

在坡度提取方面，沿道路中心线对DSM进行线性插值即可获得纵断面高程 profile，再通过差分计算局部坡度。然而，DSM的噪声会传播至坡度估计，因此通常需要进行平滑处理。曲率计算则依赖于道路中心线的平面几何形态：将二维中心线投影至三维空间后，利用Frenet标架或离散曲率公式计算每个节点的平面曲率和竖曲率。对于复杂立交和匝道场景，三维道路网络的拓扑关系构建尤为困难——不同高程层面的道路在二维投影中可能重叠，需要借助连通性分析和高度阈值进行分层处理。

直接从LiDAR点云提取三维道路是另一条重要路径。车载LiDAR沿道路采集的点云具有高密度和高精度的特点，通过地面点滤波（如渐进形态学滤波、布料模拟滤波）分离路面点后，可利用RANSAC平面拟合提取道路表面，进而估计横坡和纵坡。机载LiDAR则更适合大范围道路网的快速三维建模。SegEarth-OV3在STPLS3D数据集上的实验表明，SAM 3的二维语义预测可以通过多视角投影有效扩展到三维点云分割，展示了foundation model向三维延伸的巨大潜力[81]。

三维道路提取仍面临多重挑战：下穿通道和隧道中的GPS信号缺失导致DSM不连续；桥梁和架空道路的悬空结构在DSM中表现为异常高程；不同等级道路（高速公路、城市主干道、乡村小路）的几何特征差异巨大，难以用统一模型处理。未来，融合惯性导航、高精度地图先验和多模态传感器（LiDAR+影像+雷达）的联合推理，有望实现全天候、全场景的三维道路自动提取。

### 8.3 数字孪生与城市信息模型

道路与建筑物的三维提取是构建城市数字孪生（Digital Twin）和城市信息模型（City Information Model, CIM）的基础数据层。从二维语义分割结果到三维标准模型的自动化转换 pipeline，涉及几何重建、语义映射、拓扑关系构建和语义丰富化等多个环节，是目前学术界和产业界共同关注的前沿方向。

CityGML作为开放式地理数据建模标准，将三维城市对象按细节层次（Level of Detail, LOD）划分为五个等级（图15）。LOD0为二维轮廓；LOD1为简单块体模型（平顶、无立面细节）；LOD2增加了标准屋顶结构（如人字顶、四坡顶）和纹理映射；LOD3进一步包含详细的立面几何（窗户、门、阳台）和屋顶突出物；LOD4则扩展至室内空间结构（房间、楼层、家具）。如图15所示，随着LOD等级的提升，模型的几何复杂度和语义丰富度呈指数增长，而自动化生成的难度也急剧上升。当前深度学习方法已能较为可靠地生成LOD1-LD2级别的建筑物模型，但LOD3以上的精细立面重建和LOD4的室内建模仍高度依赖人工干预或昂贵的倾斜摄影测量数据。

![图15 CityGML标准中建筑物LOD层级定义示意图](05_图表素材/图12_CityGML_LOD层级.png)
>
> （自绘：展示从LOD0二维轮廓到LOD4室内结构的五个细节层次，体现三维城市模型由粗到细的渐进构建思想）

在数据格式方面，3D Tiles规范通过层次化细节（HLOD）和流式传输机制，支持海量三维城市数据在Web端的实时可视化，为CIM的在线应用提供了技术基础。IFC（Industry Foundation Classes）标准则侧重于建筑信息模型（BIM）的语义表达，其丰富的属性定义（材料、结构、设备）为建筑物的全生命周期管理提供了数据支撑。

数字孪生的核心价值在于"虚实映射、实时交互"。通过在三维城市模型中集成IoT传感器数据（交通流量、空气质量、能耗监测），可以实现城市运行状态的实时监控和预测性分析。在灾害应急场景中，三维建筑物模型与洪水淹没模拟、地震破坏评估相结合，能够为救援决策提供空间化的信息支持。在自动驾驶领域，高精三维地图（HD Map）已成为L4级自动驾驶系统的必备基础设施，其厘米级精度和丰富的语义标注（车道线、交通标志、路面箭头）对三维道路提取提出了极高要求。

### 8.4 三维信息提取的数据集与挑战

三维信息提取的发展离不开高质量数据集的支撑。在建筑物三维重建领域，WHU Aerial数据集提供了带 DSM 的航空影像和精细的二维标注，但其三维真值主要来源于 LOD1 级别的简化模型。STPLS3D[94]是一个大规模合成航拍点云数据集，包含超过14亿个点和16个语义类别，为点云分割算法的训练和评估提供了基准。SensatUrban[95]收集了英国多个城市的高密度机载LiDAR点云，涵盖道路、建筑物、植被等地物，是目前城市级别真实场景三维语义分割的重要数据集。ShapeNet[96]虽然主要面向室内物体，但其部件级标注为建筑物组件（屋顶、窗户、门）的识别提供了预训练知识。

在评价指标方面，三维建筑物提取除沿用二维的IoU和F1-score外，还引入了专门针对三维几何的度量：Chamfer Distance（CD）衡量预测点云与真值点云之间的平均最近邻距离；3D IoU通过三维边界框或体素化网格的重叠度评估空间一致性；Hausdorff Distance则关注最坏情况下的边界偏差。这些三维指标对几何误差的惩罚比二维指标更为敏感，推动了三维提取方法向更高精度的方向发展。

尽管技术不断进步，三维信息提取仍面临若干根本性挑战。**遮挡与完整性**：高层建筑之间的相互遮挡、树木对建筑物的遮挡，导致从单一视角获取的三维信息不完整，多视角融合和语义推理是潜在的解决方向。**高度歧义**：屋顶设备、天台植被和光伏板在DSM中表现为异常高程，如何从建筑物主体高度中准确分离这些附属物，是高度估计的关键难点。**计算成本**：城市级三维模型的数据量极其庞大（一个城市可能产生TB级别的点云和网格数据），如何在保证精度的前提下实现高效存储、流式传输和实时渲染，是制约大规模应用的工程瓶颈。**几何拓扑一致性**：自动生成的三维模型往往存在面片相交、法向不一致、非流形结构等几何缺陷，需要复杂的后处理才能满足下游应用（如3D打印、CFD模拟）的质量要求。

### 8.5 小结

三维信息提取代表了从"二维制图"到"三维建模"的升维发展方向。DSM融合、LiDAR点云深度学习和NeRF/3DGS三条技术路线各具优势，分别适用于不同的数据条件和精度需求。CityGML LOD体系和CIM框架为三维城市数据的标准化组织和应用提供了规范。尽管立体遥感、LiDAR和神经辐射场等技术为三维重建提供了多元化手段，但从二维影像直接端到端提取三维矢量模型仍面临遮挡恢复、高度歧义、几何拓扑一致性等严峻挑战。Foundation Model向三维领域的扩展，以及多模态数据（影像+点云+矢量）的联合推理，将是突破这些瓶颈的关键路径。未来，随着三维城市数据集的丰富、计算能力的提升和标准化体系的完善，城市级精细三维模型的自动化生成有望从研究走向工程化应用。

---

## 9 研究热点与未来展望

### 9.1 当前研究热点

基于上述技术脉络的梳理，当前城市路网与建筑物提取领域呈现出以下五大研究热点：

**（1）基础模型的领域适配**。如何在保持foundation model通用能力的前提下，通过adapter、LoRA、prompt tuning、视觉提示等参数高效技术，进一步提升其在遥感专用场景（细小道路、密集建筑群、复杂城中村）上的精度，是当前的焦点问题。Road-SAM等工作已证明轻量微调的可行性，但最优适配策略尚未形成共识。

**（2）拓扑与几何一致性保持**。从像素级分割结果到实际可用矢量地图的转换过程中，道路网络的拓扑连通性、建筑物轮廓的几何规则性是关键质量指标。TopoRF-Net、SAM-Road++等方法从不同角度探索了这一问题，但离完全自动化的"像素-矢量"无损转换仍有距离。

**（3）开放词汇与任意目标分割**。SAM 3和SegEarth-OV3引领了从封闭类别集合向"任意文本描述→目标分割"的范式转变。未来遥感解译系统可能不再需要为每个新类别重新训练模型，而是通过自然语言指令直接实现开放域地物提取。

**（4）大范围高效推理**。城市级乃至全球级道路/建筑物提取对计算效率和存储优化提出了极高要求。如何在保持精度的同时实现大场景影像的高效滑窗推理、结果拼接与全局拓扑优化，是制约实际应用部署的瓶颈。

**（5）多模态大模型融合**。将SAM 3等多模态基础模型与遥感领域知识图谱、GIS先验规则相结合，构建能够响应复杂语义查询（如"提取宽度大于6米且连通至主干道的所有支路"）的智能解译系统，代表了下一代遥感AI的发展方向。

### 9.2 未来发展方向

展望未来，以下五个方向有望取得重要突破：

**（1）统一的城市要素提取大模型**。构建专门针对遥感城市场景预训练的基础模型，同时支持道路、建筑、植被、水体、车辆等多类地物的开放词汇提取，实现"一个模型、任意任务、零样本响应"的通用遥感解译能力。

**（2）时序一致性提取与变化检测**。从静态单时相提取拓展至动态时序监测，利用视频/时序遥感数据保持提取结果的时间一致性，实现道路新建、建筑拆迁等变化的自动检测与更新。

**（3）矢量地图直接生成**。跳过像素级分割的中间步骤，设计端到端网络直接从遥感影像生成道路 polyline 和建筑物 polygon 的矢量表示，从根本上避免栅格-矢量转换过程中的信息损失和拓扑破坏。

**（4）知识驱动的提取**。将GIS先验知识（如道路网络拓扑规则、建筑布局模式、城市规划约束）以可微分方式嵌入深度学习模型，利用知识引导提升提取结果的合理性和可用性。

**（5）边缘部署与实时处理**。面向无人机机载处理、移动终端等场景，通过知识蒸馏、神经架构搜索、模型量化等技术设计轻量化网络，在资源受限环境下实现近实时的道路与建筑物提取。

### 9.3 挑战与建议

尽管技术进步迅速，该领域仍面临若干根本性挑战：高质量道路拓扑标注和建筑精确边界标注的获取成本高昂，亟需发展基于foundation model的半自动/自动标注工具；不同传感器（光学/SAR/LiDAR）、不同地域（城市/乡村/山区）、不同季节的域迁移问题尚未得到系统性解决；大模型的高精度与高效率之间的权衡依然是实际应用中的核心矛盾。建议未来研究在以下方面加强：（1）构建更大规模、更多样化的遥感解译基准数据集；（2）发展物理可解释的深度学习方法，使模型决策过程透明化；（3）推动产学研深度融合，加速算法从实验室向实际业务系统的转化。

---

## 10 结论

本文以技术演进为主线，系统回顾了从高分辨率遥感影像中提取城市路网与建筑物的方法发展历程。全文可概括为"三个阶段、两次跃迁"：

**三个阶段**——传统图像处理与面向对象分析阶段奠定了方法论基础，机器学习方法实现了特征组合的自动化，深度学习方法则通过端到端表示学习将提取精度推向了新的高度。

**两次跃迁**——第一次跃迁发生在2015年前后，以FCN和U-Net为标志，CNN与编码器-解码器架构将遥感目标提取从"特征工程"带入"架构工程"时代，CFENet、TopoRF-Net等专用网络进一步针对遥感场景优化了多尺度融合与拓扑保持能力。第二次跃迁始于2020年的Vision Transformer，并在2023年后由SAM系列基础模型加速推进：自注意力机制突破了CNN的感受野限制，开放词汇分割打破了预定义类别的约束，大规模预训练知识则大幅降低了对领域标注数据的依赖。SAM 3的Promptable Concept Segmentation与SegEarth-OV3在遥感零样本分割中的成功实践，预示着"通用模型+领域适配"将成为未来遥感解译的主流范式。

展望未来，多源数据融合、多任务联合学习、三维信息重建以及基础模型的轻量化适配，将持续推动城市路网与建筑物提取技术向更高精度、更强泛化、更广适用性的方向发展。Foundation Model的兴起正在深刻重塑遥感目标提取的技术范式——从专用模型的从头训练走向通用模型的知识迁移，从封闭类别的有限识别走向开放词汇的任意分割，从人工标注的高昂成本走向人机协同的数据引擎。这一变革不仅将提升学术研究的效率，更将为智慧城市、自动驾驶、灾害应急等前沿应用提供更加 robust 和 scalable 的空间信息基础设施。

---

## 参考文献

[1] United Nations, Department of Economic and Social Affairs, Population Division. World Urbanization Prospects: The 2018 Revision. New York: United Nations, 2019.

[2] Guo H, Su X, Wu C, et al. Building-road collaborative extraction from remote sensing images via cross-task and cross-scale interaction[J]. IEEE Transactions on Geoscience and Remote Sensing, 2024, 62: 5617416.

[3] 钱晓亮, 等. 遥感影像道路提取研究综述[J]. 遥感学报, 2024. (Qian et al., E07)

[4] 范荣双, 等. 基于深度学习的高分辨率遥感影像建筑物提取方法综述[J]. 测绘学报, 2021. (C04)

[5] Fu J, Wang C, Lv H, et al. TopoRF-Net: Topology-aware road segmentation in multi-resolution remote sensing via multi-receptive field adaptation[J]. Sensors, 2025, 25(24): 7428.

[6] Li K, Zhang S, Wang Y, et al. SegEarth-OV3: Exploring SAM 3 for open-vocabulary semantic segmentation in remote sensing images[J]. arXiv preprint arXiv:2512.08730, 2025.

[7] Chen Z, Wang C, Wen C, et al. Road extraction in remote sensing data: A survey[J]. International Journal of Applied Earth Observation and Geoinformation, 2022, 112: 102833.

[8] 邵振峰, 等. 智能优化学习的高空间分辨率遥感影像语义分割[J]. 测绘学报, 2021. (C08)

[9] Breiman L. Random forests[J]. Machine Learning, 2001, 45(1): 5-32.

[10] Boykov Y, Funka-Lea G. Graph cuts and efficient N-D image segmentation[J]. International Journal of Computer Vision, 2006, 70(2): 109-131.

[11] Long J, Shelhamer E, Darrell T. Fully convolutional networks for semantic segmentation[C]//CVPR, 2015: 3431-3440.

[12] Ronneberger O, Fischer P, Brox T. U-Net: Convolutional networks for biomedical image segmentation[C]//MICCAI, 2015: 234-241.

[13] Chen L C, Zhu Y, Papandreou G, et al. Encoder-decoder with atrous separable convolution for semantic image segmentation[C]//ECCV, 2018: 801-818.

[14] Fu J, et al. TopoRF-Net[J]. Sensors, 2025. (E08)

[15] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16x16 words: Transformers for image recognition at scale[C]//ICLR, 2021.

[16] Liu Z, Lin Y, Cao Y, et al. Swin Transformer: Hierarchical vision transformer using shifted windows[C]//ICCV, 2021: 10012-10022.

[17] Kirillov A, Mintun E, Ravi N, et al. Segment anything[C]//ICCV, 2023: 4015-4026.

[18] Carion N, Gustafson L, Hu Y T, et al. SAM 3: Segment anything with concepts[J]. arXiv preprint arXiv:2511.16719, 2025.

[19] 钱晓亮, 等. ISPRS, 2025. (E06)

[20] Hetang S, et al. SAM-Road[C]//CVPR, 2024. (E01)

[21] Mnih V. Machine learning for aerial image labeling[D]. University of Toronto, 2013.

[22] Demir I, Koperski K, Lindenbaum D, et al. DeepGlobe 2018: A challenge to parse the earth through satellite images[C]//CVPR Workshops, 2018.

[23] Zhu L, et al. CHN6-CUG road dataset[J]. 2021.

[24] Van Etten A, Lindenbaum D, Bacastow T M. SpaceNet: A remote sensing dataset and challenge series[J]. arXiv preprint arXiv:1807.01232, 2018.

[25] Ji S, Wei S, Lu M. Fully convolutional networks for multisource building extraction from an open aerial and satellite imagery data set[J]. IEEE TGRS, 2019, 57(1): 574-586.

[26] Maggiori E, Tarabalka Y, Charpiat G, et al. Can semantic labeling methods generalize to any city? The Inria aerial image labeling benchmark[C]//IGARSS, 2017: 3226-3229.

[27] Gupta R, et al. xBD: A dataset for assessing building damage from satellite imagery[J]. arXiv, 2019.

[28] Xia G S, Bai X, Ding J, et al. OpenEarthMap: A benchmark dataset for global high-resolution land cover mapping[C]//CVPRW, 2023.

[29] Wang J, Zheng Z, Ma A, et al. LoveDA: A remote sensing land-cover dataset for domain adaptive semantic segmentation[C]//NeurIPS Datasets and Benchmarks, 2021.

[30] Ji D, Zhao F, Lu H, et al. Ultra-high resolution segmentation with ultra-rich context: A novel benchmark[C]//CVPR, 2023: 23621-23630.

[31] OpenStreetMap contributors. Planet dump[DB/OL]. https://www.openstreetmap.org, 2023.

[32] 黄冬青, 等. 基于DeeplabV3+网络的高分遥感影像分类[J]. 测绘通报, 2020. (C02)

[33] 周荣荣, 等. 基于语义分割的遥感影像建筑物自动提取方法[J]. 遥感信息, 2020. (C06)

[34] 陈嘉浩, 等. 融合级联CRFs和U-Net深度学习模型的遥感影像建筑物自动提取[J]. 测绘通报, 2021. (C11)

[35] 吴盛葳, 等. 基于改进压缩与激活块的遥感影像语义分割方法[J]. 测绘科学, 2021. (C03)

[36] Blaschke T, Hay G J, Kelly M, et al. Geographic object-based image analysis – Towards a new paradigm[J]. ISPRS Journal of Photogrammetry and Remote Sensing, 2014, 87: 180-191.

[37] 周家厚, 等. 改进的UNet3+网络高分辨率遥感影像道路提取[J]. 测绘科学, 2022. (C09)

[38] 邵振峰, 等. 智能优化学习的高空间分辨率遥感影像语义分割[J]. 测绘学报, 2021. (C08)

[39] Lowe D G. Distinctive image features from scale-invariant keypoints[J]. International Journal of Computer Vision, 2004, 60(2): 91-110.

[40] 卢晓燕, 等. 面向高分辨率遥感影像大范围道路提取的深度学习方法研究[J]. 测绘通报, 2021. (C13)

[41] Lafferty J, McCallum A, Pereira F C N. Conditional random fields: Probabilistic models for segmenting and labeling sequence data[C]//ICML, 2001.

[42] 田普光, 等. 基于混合损失函数的U-Net网络建筑物提取[J]. 测绘科学, 2021. (C05)

[43] 卢晓燕, 等. 面向高分辨率遥感影像大范围道路提取的深度学习方法研究[J]. 测绘通报, 2021. (C13)

[44] 李佳优, 等. 级联融合边缘特征的高分辨率遥感影像道路提取[J]. 测绘科学, 2022. (C10)

[45] Krahenbuhl P, Koltun V. Efficient inference in fully connected CRFs with Gaussian edge potentials[C]//NIPS, 2011: 109-117.

[46] Long J, Shelhamer E, Darrell T. Fully convolutional networks for semantic segmentation[C]//CVPR, 2015: 3431-3440.

[47] Ronneberger O, Fischer P, Brox T. U-Net: Convolutional networks for biomedical image segmentation[C]//MICCAI, 2015: 234-241.

[48] Zhang Z, Liu Q, Wang Y. Road extraction by deep residual U-Net[J]. IEEE Geoscience and Remote Sensing Letters, 2018, 15(5): 749-753.

[49] 陈嘉浩, 等. 融合级联CRFs和U-Net深度学习模型的遥感影像建筑物自动提取[J]. 测绘通报, 2021. (C11)

[50] Zhang Z, Liu Q, Wang Y. Road extraction by deep residual U-Net[J]. IEEE GRSL, 2018. (Extra相关工作)

[51] Oktay O, Schlemper J, Folgoc L L, et al. Attention U-Net: Learning where to look for the pancreas[J]. arXiv preprint arXiv:1804.03999, 2018.

[52] Badrinarayanan V, Kendall A, Cipolla R. SegNet: A deep convolutional encoder-decoder architecture for image segmentation[J]. IEEE TPAMI, 2017, 39(12): 2481-2495.

[53] Chen L C, Papandreou G, Schroff F, et al. Rethinking atrous convolution for semantic image segmentation[J]. arXiv preprint arXiv:1706.05587, 2017.

[54] 黄冬青, 等. 基于DeeplabV3+网络的高分遥感影像分类[J]. 测绘通报, 2020. (C02)

[55] Wang H, Yu F, Xie J, et al. Road extraction based on improved DeepLabV3 plus in remote sensing image[J]. International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 2022, 48: 67-72.

[56] Zhou L, Zhang C, Wu M. D-LinkNet: LinkNet with pretrained encoder and dilated convolution for high resolution satellite imagery road extraction[C]//CVPR Workshops, 2018: 182-186.

[57] Zhao H, Shi J, Qi X, et al. Pyramid scene parsing network[C]//CVPR, 2017: 2881-2890.

[58] Chen K, Wei P, Chen C, et al. CFENet: A concise feature enhancement network for remote sensing image building extraction[J]. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2022, 15: 5194-5207. (E05)

[59] Ran B, et al. BMFRNet[J]. IEEE TGRS, 2021. (Extra)

[60] 罗松强, 等. 多尺度特征增强的ResUNet+遥感影像建筑物提取[J]. 测绘通报, 2022. (C07)

[61] Milletari F, Navab N, Ahmadi S A. V-Net: Fully convolutional neural networks for volumetric medical image segmentation[C]//3DV, 2016: 565-571.

[62] Berman M, Triki A R, Blaschko M B. The Lovász-softmax loss: A tractable surrogate for the optimization of the intersection-over-union measure in neural networks[C]//CVPR, 2018: 4413-4421.

[63] 田普光, 等. 基于混合损失函数的U-Net网络建筑物提取[J]. 测绘科学, 2021. (C05)

[64] 田普光, 等. 基于混合损失函数的U-Net网络建筑物提取[J]. 测绘科学, 2021. (C05)

[65] 陈嘉浩, 等. 融合级联CRFs和U-Net深度学习模型的遥感影像建筑物自动提取[J]. 测绘通报, 2021. (C11)

[66] He H, Li S, Chen B, et al. Sat2Graph: Road graph extraction through graph-tensor encoding[C]//ECCV, 2020: 51-67.

[67] Xu S, Xiong Z, Cao Z, et al. RNGDet++: An efficient iterative framework for road network graph extraction[J]. arXiv, 2022.

[68] Mosinska A, Marquez-Neila P, Kozinski M, et al. Beyond the pixel-wise loss for topology-aware delineation[C]//CVPR, 2018: 3136-3145.

[69] Fu J, Wang C, Lv H, et al. TopoRF-Net: Topology-aware road segmentation in multi-resolution remote sensing via multi-receptive field adaptation[J]. Sensors, 2025, 25(24): 7428. (E08)

[70] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16x16 words: Transformers for image recognition at scale[C]//ICLR, 2021.

[71] Liu Z, Lin Y, Cao Y, et al. Swin Transformer: Hierarchical vision transformer using shifted windows[C]//ICCV, 2021: 10012-10022.

[72] Cao H, Wang Y, Chen J, et al. Swin-Unet: Unet-like pure transformer for medical image segmentation[C]//ECCV Workshops, 2022: 205-218.

[73] Xie E, Wang W, Yu Z, et al. SegFormer: Simple and efficient design for semantic segmentation with transformers[C]//NeurIPS, 2021: 12077-12090. (E10)

[74] Wang J, Xu C, Yang S, et al. A transformer-based method for building extraction from remote sensing images[J]. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2022, 15: 8947-8960. (E17)

[75] Chen C, et al. HTC: Height-constrained Transformer for building extraction[J]. IEEE TGRS, 2023. (E16)

[76] Feng W, Guan F, Sun C, et al. Road-SAM: Adapting the segment anything model to road extraction from large very-high-resolution optical remote sensing images[J]. IEEE Geoscience and Remote Sensing Letters, 2024, 21: 6012605. (E12)

[77] RSAM-Seg, 2025. (E11)

[78] Hetang S, et al. SAM-Road: Segment anything model for road network graph extraction[C]//CVPR, 2024. (E01)

[79] Yin Y, et al. SAM-Road++: Global-scale road network graph extraction with enhanced topology reasoning[J]. 2024. (E02)

[80] Carion N, Gustafson L, Hu Y T, et al. SAM 3: Segment anything with concepts[J]. arXiv preprint arXiv:2511.16719, 2025. (E04)

[81] Li K, Zhang S, Wang Y, et al. SegEarth-OV3: Exploring SAM 3 for open-vocabulary semantic segmentation in remote sensing images[J]. arXiv preprint arXiv:2512.08730, 2025. (E03)

[82] Radford A, Kim J W, Hallacy C, et al. Learning transferable visual models from natural language supervision[C]//ICML, 2021: 8748-8763.

[83] 范荣双, 等. 基于深度学习的高分辨率遥感影像建筑物提取方法[J]. 测绘学报, 2021. (C04)

[84] Guo H, Su X, Wu C, et al. Building-road collaborative extraction from remote sensing images via cross-task and cross-scale interaction[J]. IEEE TGRS, 2024, 62: 5617416. (E14)

[85] Qi C R, Su H, Mo K, et al. PointNet: Deep learning on point sets for 3D classification and segmentation[C]//CVPR, 2017: 652-660.

[86] 徐辛超, 等. 一种基于MBFF-Net的遥感影像建筑物提取方法[J]. 测绘通报, 2022. (C01)

[87] 邵攀, 等. 面向高分辨率遥感影像的细节增强和尺度选择道路提取网络[J]. 测绘科学, 2023. (C14)

[88] 王丽梅, 等. 测绘通报, 2023. (待补充)

[89] 光学精密工程, 2024. 双分支建筑物提取. (待补充)

