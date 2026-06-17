# 智能体 Prompt 记录模板

用于填写实验报告中的“典型 Prompt 设计与迭代过程”。

## 案例 1：项目总蓝图与工程结构

### 初始 Prompt

```text
请你作为资深计算机视觉与深度学习算法工程师，帮助我规划 Kaggle Severstal 钢板缺陷分割项目。
```

### 智能体初始输出

智能体初始输出给出了常规图像分割项目路线，例如数据读取、U-Net Baseline、训练与推理流程，但内容偏技术方案本身，缺少课程评分要求、组内协作交接、MacBook 本地算力较弱、Kaggle GPU 正式训练、Prompt 记录和最终报告/PPT 交付物等约束。

### 迭代后 Prompt

```text
请结合课程评分标准、消融实验要求、MacBook 本地算力较弱、Kaggle Notebook 正式训练等约束，输出可交给组员协作的完整项目计划。
```

### 最终效果

最终形成了按 01/02/03/04 拆分的工程与协作结构，包括项目统筹、数据分析、模型训练、实验汇报四个工作包，并同步生成任务看板、评分覆盖检查表、Kaggle 运行指南、消融实验记录和报告/PPT 材料入口。该案例说明，Prompt 中加入评分标准、算力约束、交付物和协作对象后，智能体输出会更可执行。

## 案例 2：RLE 与 Dataset 模块

### 初始 Prompt

```text
请实现 Severstal 的 RLE 编解码和 PyTorch Dataset。
```

### 可能问题

初始实现容易遗漏 Kaggle RLE 的列优先顺序、像素从 1 开始计数、空 RLE 的处理，以及 `train.csv` 可能存在 `ImageId_ClassId + EncodedPixels` 或 `ImageId + ClassId + EncodedPixels` 两种格式。若不明确这些约束，Dataset 可能无法稳定输出一张图对应 4 通道 Mask。

### 迭代后 Prompt

```text
请严格按照 Kaggle RLE 的列优先顺序实现编码/解码，并把 train.csv 聚合成 image_id + 4 个类别 RLE 的格式，代码需要中文注释和单元测试。
```

### 最终效果

最终形成了更符合 Kaggle 格式的数据处理思路：RLE 编解码按列优先顺序处理，`train.csv` 可整理为一张图片一行、4 个类别各一列的训练表，Dataset 输出 3 通道图片和 4 通道 Mask，并通过轻量单元测试和 debug 配置降低格式错误风险。该案例说明，数据格式类 Prompt 必须明确输入输出格式、边界条件和验证方式。

## 案例 3：消融实验设计

### 初始 Prompt

```text
请帮我设计 Severstal 项目的消融实验。
```

### 迭代后 Prompt

```text
请根据课程要求设计至少 4 组实验，包含 Baseline、Full Pipeline、w/o 数据增强、w/o 学习率调度，并说明每组只改变哪个变量、如何记录结果。
```

### 最终效果

最终形成 Baseline、Full Pipeline、No Augmentation、No Scheduler 四组实验记录框架，并在最新结果中补入本地 Val Dice 和 Kaggle Public/Private Score。该案例也帮助报告形成最终解释口径：No Augmentation 是 Private 最优主结果，Baseline 是 Public 最优稳定备选，Full Pipeline 虽然本地验证较好但 Kaggle 分数偏低，应作为失败尝试与反思案例。

## 证据补充说明

本项目已补充两份真实智能体材料，放在 `提交文件/智能体证据/`：

- `02数据分析智能体Prompt记录.md`：记录 02 数据分析负责人使用 SOLO（Trae IDE 内置智能体）完成任务理解、数据分析执行、格式纠偏、逐概念追问和过程总结的 Prompt 案例。
- `03代码修改与推理说明.md`：记录代码侧围绕 `train.csv` 三列格式适配、`sample_submission.csv` 合并列解析、推理生成 submission、离线权重兼容和配置文件调整的修改说明。

最终提交或答辩展示时，可从上述两份文件中截取 2-3 个代表性片段，作为“Prompt 设计与迭代过程”的证据。

