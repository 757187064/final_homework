# Severstal 钢板缺陷分割项目 README

本目录是课程最终提交用的可复现代码工程，任务来自 Kaggle `Severstal: Steel Defect Detection`。项目目标是对钢板图像中的 4 类表面缺陷进行语义分割，并生成 Kaggle 要求的 `submission.csv`。

## 项目结构

```text
训练与推理代码/
├── configs/                  # 训练配置
│   ├── baseline.yaml
│   ├── debug.yaml
│   ├── full_pipeline.yaml
│   └── ablations/
│       ├── no_augmentation.yaml
│       ├── no_scheduler.yaml
│       └── resnet50.yaml
├── scripts/                  # 命令行入口
│   ├── analyze_data.py
│   ├── infer.py
│   ├── normalize_train_csv.py
│   └── train.py
├── src/severstal/            # 核心数据、模型、训练、推理代码
├── tests/                    # RLE 与数据格式测试
├── requirements.txt
└── README.md
```

## 环境配置

建议使用 Python 3.10 或 3.11，并在有 NVIDIA GPU 的环境中训练。Windows 本地可用于阅读代码、整理材料和小规模调试；正式训练建议使用 Kaggle GPU。

```bash
pip install -r requirements.txt
```

主要依赖包括：

- `torch`、`torchvision`
- `segmentation-models-pytorch`
- `albumentations`
- `opencv-python-headless`
- `pandas`、`numpy`、`scikit-learn`
- `matplotlib`、`PyYAML`、`pytest`

## 数据准备

默认配置假设数据位于：

```text
data/raw/
├── train.csv
├── sample_submission.csv
├── train_images/
└── test_images/
```

如果在 Kaggle Notebook 中运行，通常需要把配置文件里的：

```yaml
data:
  root: data/raw
```

改为实际 Kaggle 数据路径，例如：

```yaml
data:
  root: /kaggle/input/severstal-steel-defect-detection
```

本工程训练数据兼容两种常见标注格式：

- `ImageId_ClassId, EncodedPixels`
- `ImageId, ClassId, EncodedPixels`

最终生成的提交文件应为：

```text
ImageId_ClassId,EncodedPixels
```

## 数据分析与可视化

```bash
python scripts/analyze_data.py --data-root data/raw --output-dir outputs/data_analysis
```

输出内容包括类别分布统计、类别分布图和样本 Mask 叠加图，可用于实验报告和汇报 PPT。

## 快速调试

先运行小样本配置，确认数据路径、依赖和模型流程可用：

```bash
python scripts/train.py --config configs/debug.yaml
```

该配置只使用少量样本，主要用于检查流程，不用于最终成绩。

## 正式训练

Baseline：

```bash
python scripts/train.py --config configs/baseline.yaml
```

Full Pipeline：

```bash
python scripts/train.py --config configs/full_pipeline.yaml
```

消融实验：

```bash
python scripts/train.py --config configs/ablations/no_augmentation.yaml
python scripts/train.py --config configs/ablations/no_scheduler.yaml
python scripts/train.py --config configs/ablations/resnet50.yaml
```

训练输出默认保存在对应配置的 `outputs/` 子目录中，通常包括：

- `config.yaml`
- `history.csv`
- `history.png`
- `best_model.pth`
- `val_predictions/`

## 生成 Kaggle 提交文件

以 Baseline 为例：

```bash
python scripts/infer.py \
  --config configs/baseline.yaml \
  --checkpoint outputs/baseline_unet_resnet34/best_model.pth \
  --output outputs/baseline_unet_resnet34/submission.csv
```

生成后需要确认 `submission.csv` 为两列：

```text
ImageId_ClassId,EncodedPixels
```

如用于 Kaggle Notebook 提交，建议复制到：

```text
/kaggle/working/submission.csv
```

## 已整理的实验结果

组员补充的训练结果已整理到：

```text
提交文件/01_课程提交涉及材料/实验结果证据/
```

其中包含四组实验的 `config.yaml`、`history.csv`、`history.png`、`submission.csv` 和一张验证集预测示例图：

- `baseline_unet_resnet34`
- `full_pipeline_unet_resnet34`
- `ablation_no_augmentation`
- `ablation_no_scheduler`

大体积模型权重位于原始补充目录：

```text
F:\codex move\deeplearing\deep_learing_final\models\
```

这些 `.pth` 文件每个约 98 MB。若课程仓库不要求提交模型权重，建议不要直接上传；如老师要求复核模型，可单独说明保存位置或上传到网盘。

## 测试

如本地 Python 环境可用，可运行：

```bash
pytest
```

当前 Windows 环境中用户说明 `python` 和 `py` 命令不可用，因此本轮未实际运行测试。

## 复现建议

1. 安装依赖。
2. 准备 Severstal 数据集并修改配置中的 `data.root`。
3. 先运行 `configs/debug.yaml` 检查流程。
4. 运行 `configs/baseline.yaml` 或指定消融配置。
5. 使用 `scripts/infer.py` 生成 `submission.csv`。
6. 将报告、PPT PDF、代码仓库一起推送至课程 Gitee 仓库。
