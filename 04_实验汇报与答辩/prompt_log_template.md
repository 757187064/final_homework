# 智能体 Prompt 记录模板

用于填写实验报告中的“典型 Prompt 设计与迭代过程”。

## 案例 1：项目总蓝图与工程结构

### 初始 Prompt

```text
请你作为资深计算机视觉与深度学习算法工程师，帮助我规划 Kaggle Severstal 钢板缺陷分割项目。
```

### 智能体初始输出

待填：例如输出了总体路线，但缺少课程评分要求、协作交接和 MacBook 算力约束。

### 迭代后 Prompt

```text
请结合课程评分标准、消融实验要求、MacBook 本地算力较弱、Kaggle Notebook 正式训练等约束，输出可交给组员协作的完整项目计划。
```

### 最终效果

待填：例如得到工程模块、训练路线、消融实验和报告材料同步记录方案。

## 案例 2：RLE 与 Dataset 模块

### 初始 Prompt

```text
请实现 Severstal 的 RLE 编解码和 PyTorch Dataset。
```

### 可能问题

待填：例如 RLE 展开顺序容易写错，`train.csv` 需要从一行一个类别整理为一行一张图。

### 迭代后 Prompt

```text
请严格按照 Kaggle RLE 的列优先顺序实现编码/解码，并把 train.csv 聚合成 image_id + 4 个类别 RLE 的格式，代码需要中文注释和单元测试。
```

### 最终效果

待填：例如通过单元测试，Dataset 可以输出 3 通道图片和 4 通道 Mask。

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

待填：例如形成 `experiments/ablation_plan.md`，后续结果可以直接填报告。
