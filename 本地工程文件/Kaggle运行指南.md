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

## 7. MacBook 设备建议

你的本地 MacBook 不建议跑完整训练。推荐用途：

- 检查代码结构；
- 跑 RLE 单元测试；
- 用小样本跑 `configs/debug.yaml`；
- 写报告、整理图表、准备 PPT。

正式训练建议交给 Kaggle GPU，避免本地 CPU/MPS 长时间训练导致耗时过长或内存不足。
