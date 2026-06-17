# 消融实验项目说明

## 项目概述

本项目包含钢铁缺陷检测的完整消融实验（Ablation Study），用于验证各优化策略对模型性能的影响。

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
├── results/                    # 实验结果
│   ├── baseline_unet_resnet34/     # 基线实验结果
│   ├── full_pipeline_unet_resnet34/ # 完整管道结果
│   ├── ablation_30epochs/          # 30轮训练结果
│   ├── ablation_50epochs/          # 50轮训练结果
│   ├── ablation_efficientnet_b3/   # EfficientNet-B3结果
│   ├── ablation_no_augmentation/   # 无数据增强结果
│   ├── ablation_no_scheduler/      # 无学习率调度结果
│   └── ablation_se_resnext50/      # SE-ResNeXt50结果
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
│       └── utils.py           # 工具函数
├── docs/                       # 文档
│   ├── ABLATION_WORK_LOG.md   # 消融实验工作日志
│   ├── ablation_plan.md       # 消融实验计划
│   └── kaggle_runbook.md      # Kaggle运行指南
└── requirements.txt           # 依赖包列表
```

## 实验设计

### 基础消融实验

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| Baseline | baseline.yaml | U-Net + ResNet34 + light aug + scheduler (15轮) | 基准性能 |
| Full Pipeline | full_pipeline.yaml | 更强增强 + 更长训练(25轮) + Dice权重更高(0.6) | 验证完整方案 |
| No Augmentation | ablations/no_augmentation.yaml | 去掉数据增强 | 验证数据增强效果 |
| No Scheduler | ablations/no_scheduler.yaml | 去掉学习率调度 | 验证调度器重要性 |

### 训练轮数对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| 30 Epochs | ablations/30_epochs.yaml | 训练30轮 | 验证更长训练效果 |
| 50 Epochs | ablations/50_epochs.yaml | 训练50轮 | 验证极限训练效果 |

### 编码器对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| EfficientNet-B3 | ablations/efficientnet_b3.yaml | EfficientNet-B3编码器 | 验证更强编码器 |
| SE-ResNeXt50 | ablations/se_resnext50.yaml | SE-ResNeXt50编码器 | 验证注意力机制 |
| ResNet50 | ablations/resnet50.yaml | ResNet50编码器 | 验证更深网络 |

### 损失函数对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| BCE Heavy | ablations/loss_bce_heavy.yaml | BCE:0.7 + Dice:0.3 | 验证BCE权重 |
| Dice Heavy | ablations/loss_dice_heavy.yaml | BCE:0.3 + Dice:0.7 | 验证Dice权重 |

### 学习率对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| High LR | ablations/lr_high.yaml | lr=0.001 | 验证高学习率 |
| Low LR | ablations/lr_low.yaml | lr=0.0001 | 验证低学习率 |

### 数据增强对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| Very Strong Aug | ablations/aug_very_strong.yaml | 超强数据增强 | 验证极限增强 |

### 架构对比

| 实验名称 | 配置文件 | 核心变量 | 目的 |
|----------|----------|----------|------|
| FPN | optimization/fpn_resnet50.yaml | FPN + ResNet50 | 验证特征金字塔 |
| DeepLabV3Plus | optimization/deeplabv3plus_resnet50.yaml | DeepLabV3Plus + ResNet50 | 验证空洞卷积 |

## 如何使用

### 1. 环境配置

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 运行单个实验

```bash
# 使用配置文件运行单个实验
python scripts/train.py --config configs/baseline.yaml
```

### 3. 批量运行消融实验

```bash
# 使用Python脚本自动运行所有消融实验
python scripts/run_ablation_auto.py

# 或使用Windows批处理脚本
scripts\run_ablation_auto.bat
```

### 4. 查看实验结果

每个实验的结果都保存在对应的 `results/` 目录下：

- `history.csv`: 训练历史记录
- `history.png`: 训练曲线可视化
- `config.yaml`: 使用的配置文件副本
- `submission.csv`: 提交文件（如果有）
- `val_predictions/`: 验证集预测可视化

### 5. 分析结果

```bash
# 查看训练历史
cat results/baseline_unet_resnet34/history.csv

# 查看训练曲线
open results/baseline_unet_resnet34/history.png
```

## 实验结果总结

### 主要发现

1. **数据增强的重要性**: 去掉数据增强后性能下降约0.89%
2. **学习率调度的关键作用**: 去掉调度器后性能明显下降4.06%
3. **完整方案的综合收益**: 完整管道相比基线提升约0.04%
4. **训练轮数的影响**: 更长的训练时间可以带来性能提升

### 性能对比

| 实验配置 | Val Dice | 相对基线提升 |
|----------|----------|--------------|
| Baseline (15 epochs) | 0.6430 | - |
| Full Pipeline (25 epochs) | 0.6434 | +0.04% |
| No Augmentation | 0.6373 | -0.89% |
| No Scheduler | 0.6179 | -4.06% |

## 文档说明

- [ABLATION_WORK_LOG.md](docs/ABLATION_WORK_LOG.md): 详细的消融实验工作记录，包含任务概述、实验设计、环境配置、执行流程等
- [ablation_plan.md](docs/ablation_plan.md): 消融实验计划表，用于记录实验结果和结论
- [kaggle_runbook.md](docs/kaggle_runbook.md): Kaggle平台运行指南

## 注意事项

1. **数据路径**: 配置文件中的数据路径需要根据实际情况调整
2. **GPU要求**: 建议使用GPU进行训练，CPU训练速度较慢
3. **磁盘空间**: 每个实验约需2-3GB磁盘空间
4. **训练时间**: 完整的消融实验预计需要9小时左右

## 技术栈

- **框架**: PyTorch 2.4.0
- **分割模型**: segmentation-models-pytorch 0.3.4
- **数据增强**: albumentations 1.4.0
- **优化器**: AdamW
- **学习率调度**: Cosine Annealing
- **混合精度训练**: AMP

## 联系与支持

如有问题，请参考项目文档或查看实验日志。

---

*最后更新: 2026-06-17*