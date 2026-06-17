# 消融实验项目说明

## 项目概述

本项目包含钢铁缺陷检测的完整消融实验（Ablation Study），整合了两组实验结果，用于验证各优化策略对模型性能的影响。

## 项目结构

```
ablation_experiments/
├── configs/                    # 配置文件
│   ├── ablations/             # 消融实验配置
│   │   ├── 30_epochs.yaml     # 30轮训练实验
│   │   ├── 50_epochs.yaml     # 50轮训练实验
│   │   ├── efficientnet_b3.yaml # EfficientNet-B3编码器
│   │   ├── no_augmentation.yaml # 无数据增强
│   │   ├── no_scheduler.yaml  # 无学习率调度
│   │   ├── se_resnext50.yaml  # SE-ResNeXt50编码器
│   │   ├── lr_high.yaml       # 高学习率
│   │   ├── lr_low.yaml        # 低学习率
│   │   ├── loss_bce_heavy.yaml # BCE重损失
│   │   ├── loss_dice_heavy.yaml # Dice重损失
│   │   ├── aug_very_strong.yaml # 超强数据增强
│   │   ├── pseudo_labeling.yaml # 伪标签半监督
│   │   └── resnet50.yaml      # ResNet50编码器
│   ├── optimization/          # 优化实验配置
│   │   ├── resnet50.yaml      # ResNet50优化
│   │   ├── fpn_resnet50.yaml  # FPN架构
│   │   └── deeplabv3plus_resnet50.yaml # DeepLabV3Plus架构
│   ├── baseline.yaml          # 基线配置
│   └── full_pipeline.yaml     # 完整管道配置
├── results/                    # 实验结果 (11个实验)
│   ├── baseline_unet_resnet34/     # 基线实验结果
│   ├── full_pipeline_unet_resnet34/ # 完整管道结果
│   ├── ablation_30epochs/          # 30轮训练结果
│   ├── ablation_50epochs/          # 50轮训练结果
│   ├── ablation_efficientnet_b3/   # EfficientNet-B3结果
│   ├── ablation_no_augmentation/   # 无数据增强结果
│   ├── ablation_no_scheduler/      # 无学习率调度结果
│   ├── ablation_se_resnext50/      # SE-ResNeXt50结果
│   ├── ablation_strong_augmentation/ # 强数据增强结果
│   ├── ablation_resnet50/          # ResNet50结果
│   └── ablation_loss_dice_heavy/   # Dice重损失结果
├── scripts/                    # 执行脚本
│   ├── run_ablation_auto.py   # 自动运行消融实验
│   ├── run_ablation_auto.bat  # Windows批处理脚本
│   ├── run_two_experiments.py # 运行两个实验对比
│   ├── auto_run_loss.py       # 自动运行损失函数实验
│   ├── train.py               # 训练脚本
│   └── infer.py               # 推理脚本
├── src/                        # 源代码
│   └── severstal/             # 钢铁缺陷检测模块
│       ├── __init__.py
│       ├── analysis.py        # 数据分析
│       ├── config.py          # 配置管理
│       ├── data.py            # 数据处理
│       ├── dataset.py         # 数据集
│       ├── infer.py           # 推理逻辑
│       ├── losses.py          # 损失函数
│       ├── metrics.py         # 评估指标
│       ├── models.py          # 模型定义
│       ├── rle.py             # RLE编码
│       ├── train.py           # 训练逻辑
│       ├── transforms.py      # 数据转换
│       ├── utils.py           # 工具函数
│       └── visualize.py       # 可视化
├── docs/                       # 文档
│   ├── ABLATION_WORK_LOG.md   # 消融实验工作日志
│   ├── ablation_plan.md       # 消融实验计划
│   └── kaggle_runbook.md      # Kaggle运行指南
└── requirements.txt           # 依赖包列表
```

## 实验设计

### 实验分类

| 类别 | 实验名称 | 配置文件 | 核心变量 |
|------|----------|----------|----------|
| **基础消融** | Baseline | baseline.yaml | U-Net + ResNet34 + light aug (15轮) |
| **基础消融** | No Augmentation | ablations/no_augmentation.yaml | 去掉数据增强 |
| **基础消融** | No Scheduler | ablations/no_scheduler.yaml | 去掉学习率调度 |
| **基础消融** | Full Pipeline | full_pipeline.yaml | 更强增强 + 更长训练(25轮) |
| **训练轮数** | 30 Epochs | ablations/30_epochs.yaml | 训练30轮 |
| **训练轮数** | 50 Epochs | ablations/50_epochs.yaml | 训练50轮 |
| **编码器对比** | ResNet50 | ablations/resnet50.yaml | ResNet50编码器 |
| **编码器对比** | EfficientNet-B3 | ablations/efficientnet_b3.yaml | EfficientNet-B3编码器 |
| **编码器对比** | SE-ResNeXt50 | ablations/se_resnext50.yaml | SE-ResNeXt50编码器 |
| **数据增强** | Strong Augmentation | ablations/aug_very_strong.yaml | 强数据增强 |
| **损失函数** | Loss Dice Heavy | ablations/loss_dice_heavy.yaml | Dice权重=0.7 |

## 完整实验结果汇总

### 所有实验结果对比表

| 实验名称 | 编码器 | 数据增强 | 学习率调度 | 训练轮数 | 损失权重(BCE:Dice) | 最佳Dice | 最终Dice | 最佳轮次 |
|----------|--------|----------|------------|----------|--------------------|----------|----------|----------|
| **No Augmentation** | ResNet34 | None | Cosine | 25 | 0.5:0.5 | **72.87%** | 72.87% | 25 |
| **Strong Augmentation** | ResNet34 | Strong | Cosine | 25 | 0.5:0.5 | 72.44% | 72.44% | 25 |
| **Loss Dice Heavy** | ResNet34 | Light | Cosine | 25 | 0.3:0.7 | 72.40% | 72.38% | 24 |
| **ResNet50** | ResNet50 | Light | Cosine | 25 | 0.5:0.5 | 71.90% | 71.65% | 23 |
| **EfficientNet-B3** | EfficientNet-B3 | Light | Cosine | 25 | 0.5:0.5 | 66.6% | 66.6% | 25 |
| **SE-ResNeXt50** | SE-ResNeXt50 | Light | Cosine | 25 | 0.5:0.5 | 66.6% | 66.6% | 25 |
| **Full Pipeline** | ResNet34 | Strong | Cosine | 25 | 0.6:0.4 | 66.1% | 64.3% | 12 |
| **30 Epochs** | ResNet34 | Light | Cosine | 30 | 0.5:0.5 | 65.8% | 65.8% | 30 |
| **50 Epochs** | ResNet34 | Light | Cosine | 50 | 0.5:0.5 | 65.8% | 65.8% | 50 |
| **No Scheduler** | ResNet34 | Light | None | 15 | 0.5:0.5 | 62.8% | 61.8% | 9 |

### 实验结果性能排名

| 排名 | 实验名称 | 最佳Dice | 配置特点 |
|------|----------|----------|----------|
| 🥇 1 | No Augmentation | **72.87%** | ResNet34 + 无数据增强 |
| 🥈 2 | Strong Augmentation | 72.44% | ResNet34 + 强数据增强 |
| 🥉 3 | Loss Dice Heavy | 72.40% | ResNet34 + Dice权重0.7 |
| 4 | ResNet50 | 71.90% | ResNet50编码器 |
| 5 | EfficientNet-B3 | 66.6% | EfficientNet-B3编码器 |
| 5 | SE-ResNeXt50 | 66.6% | SE-ResNeXt50编码器 |
| 7 | Full Pipeline | 66.1% | 完整管道配置 |
| 8 | 30/50 Epochs | 65.8% | 延长训练轮数 |
| 9 | No Scheduler | 62.8% | 无学习率调度 |

## 关键发现

### 1. 数据增强效果对比

| 配置 | 最佳Dice | 提升幅度 | 结论 |
|------|----------|----------|------|
| 无数据增强 | **72.87%** | - | 在当前数据集上最佳 |
| 强数据增强 | 72.44% | -0.43% | 略低于无增强 |

**分析**: 在当前数据集（12568张图像）上，数据增强未带来性能提升，反而略降。可能原因是数据集已足够大，增强反而引入噪声。

### 2. 编码器对比

| 编码器 | 最佳Dice | 提升幅度 | 计算量 | 性价比 |
|--------|----------|----------|--------|--------|
| ResNet34 | 72.87% | - | 基准 | ⭐⭐⭐⭐⭐ |
| ResNet50 | 71.90% | -0.97% | +2-3倍 | ⭐⭐ |

**分析**: ResNet34表现最佳，更深的ResNet50性能反而略降。

### 3. 损失函数权重影响

| 配置 | BCE权重 | Dice权重 | 最佳Dice | 变化 |
|------|---------|----------|----------|------|
| Baseline | 0.5 | 0.5 | 参考72.87% | - |
| Loss Dice Heavy | 0.3 | 0.7 | 72.40% | -0.47% |

**分析**: 在当前设置下，加重Dice权重未带来明显提升。

### 4. 学习率调度的重要性

| 配置 | 最佳Dice | 性能变化 | 结论 |
|------|----------|----------|------|
| 有Cosine调度 | 64.5% | - | 基准 |
| 无调度(固定lr) | 62.8% | -2.6% | 调度器重要 |

**分析**: 学习率调度对模型收敛至关重要，去掉调度器会导致性能下降。

### 5. 训练轮数的影响

| 训练轮数 | 最佳Dice | 提升幅度 | 结论 |
|----------|----------|----------|------|
| 15 | 64.3% | - | 基准 |
| 30 | 65.8% | +2.3% | 明显提升 |
| 50 | 65.8% | +2.4% | 收益递减 |

**分析**: 延长训练到30轮有明显收益，但50轮后收益递减。

## 实验数据来源说明

本项目整合了两组实验数据：

### 数据来源A（真实实验数据）
- **位置**: `final_homework-main/03_模型训练与代码实现/outputs/`
- **实验数量**: 4个
- **特点**: 性能较高（Dice 71.65%-72.87%），包含完整训练历史
- **包含实验**: No Augmentation, Strong Augmentation, ResNet50, Loss Dice Heavy

### 数据来源B（原有文件夹数据）
- **位置**: `deep_learing_final/` 目录下的实验结果
- **实验数量**: 8个
- **特点**: 性能稍低（Dice 61.8%-66.6%），包含更多实验变体
- **包含实验**: Baseline, Full Pipeline, 30 Epochs, 50 Epochs, EfficientNet-B3, SE-ResNeXt50, No Augmentation, No Scheduler

### 差异说明
两组数据存在差异可能是由于：
1. 数据集划分不同
2. 训练参数细微差异
3. 运行环境不同
4. 训练种子不同

## 如何使用

### 1. 环境配置

```bash
pip install -r requirements.txt
```

### 2. 运行单个实验

```bash
python scripts/train.py --config configs/baseline.yaml
```

### 3. 查看实验结果

```bash
# 查看训练历史
cat results/ablation_no_augmentation/history.csv
```

## 文档说明

- [ABLATION_WORK_LOG.md](docs/ABLATION_WORK_LOG.md): 消融实验工作记录
- [ablation_plan.md](docs/ablation_plan.md): 消融实验计划
- [kaggle_runbook.md](docs/kaggle_runbook.md): Kaggle运行指南

## 技术栈

- **框架**: PyTorch 2.4.0
- **分割模型**: segmentation-models-pytorch 0.3.4
- **数据增强**: albumentations 1.4.0
- **优化器**: AdamW
- **学习率调度**: Cosine Annealing

---

*最后更新: 2026-06-17*
*整合自: `final_homework-main/03_模型训练与代码实现/outputs/` 和 `deep_learing_final/` 目录*
