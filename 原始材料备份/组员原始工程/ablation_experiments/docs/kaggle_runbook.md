# Kaggle Notebook 运行指南

## 1. 创建 Notebook

1. 打开 Kaggle 竞赛页面：`Severstal: Steel Defect Detection`。
2. 新建 Notebook，并在右侧 Add data 中添加竞赛数据集。
3. 打开 GPU：Notebook Settings -> Accelerator -> GPU。

## 2. 安装依赖

```bash
pip install segmentation-models-pytorch albumentations opencv-python-headless
```

## 3. 上传项目代码

推荐方式：

- 把本项目压缩后上传为 Kaggle Dataset；
- 或者把代码推到课程仓库后，在 Notebook 中拉取。

如果数据路径是 Kaggle 默认路径，请把配置文件中的：

```yaml
data:
  root: data/raw
```

改成：

```yaml
data:
  root: /kaggle/input/severstal-steel-defect-detection
```

## 4. 先跑数据分析

```bash
python scripts/analyze_data.py \
  --data-root /kaggle/input/severstal-steel-defect-detection \
  --output-dir outputs/data_analysis
```

输出：

- `class_distribution.csv`
- `class_distribution.png`
- `sample_masks.png`

这些图可以直接放进实验报告和 PPT。

## 5. 跑 Baseline

```bash
python scripts/train.py --config configs/baseline.yaml
```

如果 Kaggle Notebook 没有开启网络，`encoder_weights: imagenet` 可能下载失败。最省事的做法是先开启 Internet；如果课程环境不允许联网，就把配置中的：

```yaml
encoder_weights: imagenet
```

改成：

```yaml
encoder_weights: null
```

训练结束后重点保存：

- `outputs/baseline_unet_resnet34/history.csv`
- `outputs/baseline_unet_resnet34/history.png`
- `outputs/baseline_unet_resnet34/val_predictions/*.png`
- `outputs/baseline_unet_resnet34/best_model.pth`

## 6. 生成 submission.csv

```bash
python scripts/infer.py \
  --config configs/baseline.yaml \
  --checkpoint outputs/baseline_unet_resnet34/best_model.pth \
  --output outputs/baseline_unet_resnet34/submission.csv
```

生成后可提交到 Kaggle 页面获取分数。

## 7. 消融实验运行指南

### 7.1 实验配置文件清单

| 实验编号 | 配置文件 | 核心变量 | 预期目标 |
|---|---|---|---|
| E0 | `configs/baseline.yaml` | U-Net + ResNet34 + light aug + scheduler | 基准性能 |
| E1 | `configs/full_pipeline.yaml` | 更强增强 + 更长训练 | 完整方案对比 |
| E2 | `configs/ablations/no_augmentation.yaml` | 去掉数据增强 | 验证增强效果 |
| E3 | `configs/ablations/no_scheduler.yaml` | 去掉学习率调度 | 验证调度器效果 |
| A1 | `configs/ablations/30_epochs.yaml` | 训练30轮 | 轮数对比 |
| A2 | `configs/ablations/50_epochs.yaml` | 训练50轮 | 轮数对比 |
| A3 | `configs/ablations/efficientnet_b3.yaml` | EfficientNet-B3编码器 | 编码器对比 |
| A4 | `configs/ablations/se_resnext50.yaml` | SE-ResNeXt50编码器 | 编码器对比 |
| A5 | `configs/ablations/loss_bce_heavy.yaml` | BCE权重0.7 | 损失权重对比 |
| A6 | `configs/ablations/loss_dice_heavy.yaml` | Dice权重0.7 | 损失权重对比 |
| A7 | `configs/ablations/lr_high.yaml` | 学习率0.001 | 学习率对比 |
| A8 | `configs/ablations/lr_low.yaml` | 学习率0.0001 | 学习率对比 |
| A9 | `configs/ablations/aug_very_strong.yaml` | 极强数据增强 | 增强强度对比 |
| A10 | `configs/ablations/pseudo_labeling.yaml` | 伪标签策略 | 半监督学习 |
| E4 | `configs/optimization/resnet50.yaml` | U-Net + ResNet50 | 更深编码器 |
| E5 | `configs/optimization/fpn_resnet50.yaml` | FPN + ResNet50 | 架构对比 |
| E6 | `configs/optimization/deeplabv3plus_resnet50.yaml` | DeepLabV3Plus + ResNet50 | 架构对比 |

### 7.2 批量运行脚本

运行所有消融实验：

```bash
bash kaggle_run_all_ablation.sh
```

或分步运行：

```bash
# 基础实验
python scripts/train.py --config configs/baseline.yaml
python scripts/train.py --config configs/full_pipeline.yaml
python scripts/train.py --config configs/ablations/no_augmentation.yaml
python scripts/train.py --config configs/ablations/no_scheduler.yaml

# 训练轮数对比
python scripts/train.py --config configs/ablations/30_epochs.yaml
python scripts/train.py --config configs/ablations/50_epochs.yaml

# 编码器对比
python scripts/train.py --config configs/ablations/efficientnet_b3.yaml
python scripts/train.py --config configs/ablations/se_resnext50.yaml
python scripts/train.py --config configs/optimization/resnet50.yaml

# 损失权重对比
python scripts/train.py --config configs/ablations/loss_bce_heavy.yaml
python scripts/train.py --config configs/ablations/loss_dice_heavy.yaml

# 学习率对比
python scripts/train.py --config configs/ablations/lr_high.yaml
python scripts/train.py --config configs/ablations/lr_low.yaml

# 增强强度对比
python scripts/train.py --config configs/ablations/aug_very_strong.yaml

# 伪标签实验
python scripts/train.py --config configs/ablations/pseudo_labeling.yaml

# 架构对比
python scripts/train.py --config configs/optimization/fpn_resnet50.yaml
python scripts/train.py --config configs/optimization/deeplabv3plus_resnet50.yaml
```

### 7.3 结果收集

训练完成后，收集各实验的 `history.csv` 文件，提取最终 Val Dice 填入实验报告。

## 8. MacBook 设备建议

你的本地 MacBook 不建议跑完整训练。推荐用途：

- 检查代码结构；
- 跑 RLE 单元测试；
- 用小样本跑 `configs/debug.yaml`；
- 写报告、整理图表、准备 PPT。

正式训练建议交给 Kaggle GPU，避免本地 CPU/MPS 长时间训练导致耗时过长或内存不足。
