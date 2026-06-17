# 消融实验记录表

本表用于后续实验后直接填入报告。所有实验建议使用同一份训练/验证划分、同一随机种子、同一评价指标。

## 基础消融实验（4组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | Baseline：U-Net + ResNet34 + light aug + scheduler (15轮) | 0.6430 | 待填 | Kaggle GPU | 基准性能，作为对比参照 |
| E1 | `configs/full_pipeline.yaml` | 更强增强 + 更长训练(25轮) + Dice权重更高(0.6) | 0.6434 | 待填 | Kaggle GPU | 略优于Baseline，提升0.04% |
| E2 | `configs/ablations/no_augmentation.yaml` | 去掉数据增强 | 0.6373 | 待填 | Kaggle GPU | 性能下降0.89%，数据增强有效 |
| E3 | `configs/ablations/no_scheduler.yaml` | 去掉学习率调度 | 0.6179 | 待填 | Kaggle GPU | 性能明显下降4.06%，调度器至关重要 |

## 训练轮数对比（3组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | 训练15轮 | 0.6430 | 待填 | Kaggle GPU | 基准 |
| A1 | `configs/ablations/30_epochs.yaml` | 训练30轮 | 待填 | 待填 | Kaggle GPU | 待填 |
| A2 | `configs/ablations/50_epochs.yaml` | 训练50轮 | 待填 | 待填 | Kaggle GPU | 待填 |

## 编码器对比（4组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | ResNet34 | 0.6430 | 待填 | Kaggle GPU | 基准 |
| E4 | `configs/optimization/resnet50.yaml` | ResNet50 | 待填 | 待填 | Kaggle GPU | 待填 |
| A3 | `configs/ablations/efficientnet_b3.yaml` | EfficientNet-B3 | 待填 | 待填 | Kaggle GPU | 待填 |
| A4 | `configs/ablations/se_resnext50.yaml` | SE-ResNeXt50 | 待填 | 待填 | Kaggle GPU | 待填 |

## 损失权重对比（3组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | BCE:0.5 + Dice:0.5 | 0.6430 | 待填 | Kaggle GPU | 基准 |
| A5 | `configs/ablations/loss_bce_heavy.yaml` | BCE:0.7 + Dice:0.3 | 待填 | 待填 | Kaggle GPU | 待填 |
| A6 | `configs/ablations/loss_dice_heavy.yaml` | BCE:0.3 + Dice:0.7 | 待填 | 待填 | Kaggle GPU | 待填 |

## 学习率对比（3组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | lr=0.0003 | 0.6430 | 待填 | Kaggle GPU | 基准 |
| A7 | `configs/ablations/lr_high.yaml` | lr=0.001 | 待填 | 待填 | Kaggle GPU | 待填 |
| A8 | `configs/ablations/lr_low.yaml` | lr=0.0001 | 待填 | 待填 | Kaggle GPU | 待填 |

## 增强强度对比（3组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | light aug | 0.6430 | 待填 | Kaggle GPU | 基准 |
| E1 | `configs/full_pipeline.yaml` | strong aug | 0.6434 | 待填 | Kaggle GPU | 待填 |
| A9 | `configs/ablations/aug_very_strong.yaml` | very_strong aug | 待填 | 待填 | Kaggle GPU | 待填 |

## 半监督学习实验（1组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| A10 | `configs/ablations/pseudo_labeling.yaml` | 伪标签 + strong aug | 待填 | 待填 | Kaggle GPU | 待填 |

## 架构对比（3组）

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E4 | `configs/optimization/resnet50.yaml` | U-Net + ResNet50 | 待填 | 待填 | Kaggle GPU | 待填 |
| E5 | `configs/optimization/fpn_resnet50.yaml` | FPN + ResNet50 | 待填 | 待填 | Kaggle GPU | 待填 |
| E6 | `configs/optimization/deeplabv3plus_resnet50.yaml` | DeepLabV3Plus + ResNet50 | 待填 | 待填 | Kaggle GPU | 待填 |

## 记录规范

- 每次实验保存配置文件、`history.csv`、`history.png`、最佳模型和预测可视化。
- 只改一个关键变量，避免无法解释提升来自哪里。
- 如果实验失败，也记录失败原因，例如显存不足、过拟合、训练不稳定、提交格式错误。

## 报告可用结论模板

- 数据增强的贡献：对比 E0 与 E2。
- 学习率调度的贡献：对比 E0 与 E3。
- 完整方案的综合收益：对比 E0 与 E1。
- 资源效率：记录 Kaggle GPU 使用时长，说明本地只做 Debug，正式训练使用免费/低成本 GPU。
