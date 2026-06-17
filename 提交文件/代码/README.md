# 代码复现说明

本文件夹保存 Severstal 钢板缺陷检测项目的完整代码。按照最终提交整理要求，代码不再分 `configs/`、`scripts/`、`src/`、`tests/` 子文件夹，而是全部以单个文件平铺在当前目录中。

## 文件命名规则

| 前缀 | 含义 | 示例 |
|---|---|---|
| `configs_` | 训练、消融和优化实验配置 | `configs_baseline.yaml` |
| `scripts_` | 可直接执行的训练、推理、可视化和批处理脚本 | `scripts_train.py` |
| `src_severstal_` | 核心功能模块 | `src_severstal_train.py` |
| `tests_` | 简单测试文件 | `tests_test_rle.py` |

## 环境配置

建议使用 Python 3.10 或 3.11，并在有 NVIDIA GPU 的环境中训练。安装依赖：

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

默认配置中的数据目录为：

```text
data/raw/
├── train.csv
├── sample_submission.csv
├── train_images/
└── test_images/
```

如果在 Kaggle Notebook 中运行，可以把配置文件中的：

```yaml
data:
  root: data/raw
```

改为：

```yaml
data:
  root: /kaggle/input/severstal-steel-defect-detection
```

项目兼容两种训练标注格式：

- `ImageId_ClassId,EncodedPixels`
- `ImageId,ClassId,EncodedPixels`

最终提交文件应为两列：

```text
ImageId_ClassId,EncodedPixels
```

并保持 22025 行含表头。

## 数据分析与可视化

生成类别分布和样本 Mask 图：

```bash
python scripts_analyze_data.py --data-root data/raw --output-dir outputs/data_analysis
```

补充可视化脚本：

```bash
python scripts_extract_raw.py
python scripts_per_class_masks.py
python scripts_stitch_samples.py
```

## Debug 小样本训练

先运行 Debug 配置检查依赖、数据路径和训练流程：

```bash
python scripts_train.py --config configs_debug.yaml
```

## 正式训练

Baseline：

```bash
python scripts_train.py --config configs_baseline.yaml
```

Full Pipeline：

```bash
python scripts_train.py --config configs_full_pipeline.yaml
```

消融实验：

```bash
python scripts_train.py --config configs_ablation_no_augmentation.yaml
python scripts_train.py --config configs_ablation_no_scheduler.yaml
python scripts_train.py --config configs_ablation_resnet50.yaml
```

扩展消融配置包括训练轮数、学习率、损失权重、编码器和增强策略等，文件名以 `configs_optimization_` 开头。

## 生成 Kaggle 提交文件

以 Baseline 为例：

```bash
python scripts_infer.py --config configs_baseline.yaml --checkpoint outputs/baseline_unet_resnet34/best_model.pth --output outputs/baseline_unet_resnet34/submission.csv
```

生成后检查：

- 表头为 `ImageId_ClassId,EncodedPixels`。
- 总行数为 22025 行含表头。
- 空预测保留空字符串，不要删除行。

## 自动消融脚本

```bash
python scripts_run_ablation_auto.py
python scripts_run_two_experiments.py
python scripts_auto_run_loss.py
```

Windows 批处理版本：

```bat
scripts_run_ablation_auto.bat
```

## 测试

如果本地 Python 环境可用，可以运行：

```bash
pytest tests_test_rle.py tests_test_dataframe.py
```

当前整理环境中用户说明全局 `python` 和 `py` 命令不可用，因此本轮只做文件结构和静态整理，没有重新跑完整训练。

## 已整理的关键结果

关键实验结果和图表不放在代码目录中，而放在同级的 `实验报告补充/` 文件夹内，用于实验报告和答辩引用。
