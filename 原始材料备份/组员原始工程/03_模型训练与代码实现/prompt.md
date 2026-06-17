# Severstal 代码修改说明

## 项目结构

- `src/severstal/data.py` — 数据读取、CSV 聚合
- `src/severstal/infer.py` — 推理与提交文件生成
- `src/severstal/models.py` — 模型构建
- `src/severstal/dataset.py` — PyTorch Dataset 定义
- `configs/baseline.yaml`、`configs/debug.yaml`、`configs/full_pipeline.yaml`、`configs/ablations/no_augmentation.yaml`、`configs/ablations/no_scheduler.yaml` — 实验配置
- `tests/test_dataframe.py` — 测试文件

---

## 一、数据格式适配（`data.py`）

### 1. `prepare_train_dataframe`：适配三列分开的 train.csv

**问题**：原代码假设 train.csv 有 `ImageId_ClassId` 合并列，实际数据是 `ImageId`、`ClassId`、`EncodedPixels` 三列分开。

**修改**：
- 删除 `parse_image_class_id` 函数
- 直接读取 `ImageId`、`ClassId`、`EncodedPixels` 三列
- 支持列名大小写兼容（`imageid` / `ImageId` / `image_id` 都能识别）
- 通过 `pivot` 聚合成一张图一行 4 类别的格式，输出不变

### 2. `prepare_test_dataframe`：适配 `ImageId_ClassId` 合并列

**问题**：sample_submission.csv 是 Kaggle 标准格式，第一列为 `ImageId_ClassId`（如 `a.jpg_1`），不是分开列。

**修改**：
- 自动检测列名：是 `ImageId_ClassId` 合并列还是 `ImageId` 分开列
- 合并列时通过 `rsplit("_", 1)` 提取不重复的 ImageId
- 同时兼容两种格式

---

## 二、推理修复（`infer.py`）

### 3. `create_submission`：正确处理 sample_submission.csv

**问题**：
- 原代码用 `ImageId_ClassId` 合并列遍历，后改为 `ImageId` + `ClassId` 分开列读取，导致 `ClassId` 全为 0
- 行数仅为实际的 1/4

**修改**：
- 自动检测 sample_submission.csv 是合并列还是分开列，两种都能正确解析
- 合并列时通过 `rsplit("_", 1)` 解析 image_id 和 class_id
- 最终输出的 CSV 必须是 `ImageId_ClassId` + `EncodedPixels` 两列格式
- 输出行数恢复为正确的 20000+ 行

### 4. 断网环境兼容

**问题**：Kaggle 不开网络时，`segmentation_models_pytorch` 会尝试下载 ImageNet 预训练权重导致报错。而且 checkpoint 文件中存的是训练时的 `encoder_weights: imagenet`，修改 YAML 文件无法覆盖。

**修改**：在 `model.load_state_dict` 之前强制设置 `model_config["encoder_weights"] = None`，因为后续 `load_state_dict` 会把训练好的权重全部覆盖，下载预训练权重是多余的。

---

## 三、断网兼容（默认值 + 配置文件）

### 5. `models.py`：修改默认值

将 `encoder_weights` 的默认值从 `"imagenet"` 改为 `None`，防止任何遗漏导致下载。

### 6. 所有 YAML 配置文件

以下 5 个文件的 `encoder_weights` 从 `imagenet` 改为 `null`：

- `configs/baseline.yaml`
- `configs/debug.yaml`
- `configs/full_pipeline.yaml`
- `configs/ablations/no_augmentation.yaml`
- `configs/ablations/no_scheduler.yaml`

---

## 四、测试同步（`tests/test_dataframe.py`）

### 7. 测试用例更新

测试用的 CSV 构造从 `ImageId_ClassId` 合并列改为 `ImageId` + `ClassId` + `EncodedPixels` 三列分开的格式，与实际 train.csv 格式一致。

---

## 实验配置对比

| 配置项 | baseline | no_aug | no_scheduler | full_pipeline | debug |
|---|---|---|---|---|---|
| 目的 | 基准对照 | 消融：验证增强效果 | 消融：验证调度器效果 | 全量最优配置 | 快速冒烟测试 |
| epochs | 15 | 15 | 15 | **25** | **1** |
| batch_size | 8 | 8 | 8 | 8 | 2 |
| image_size | 256×1600 | 256×1600 | 256×1600 | 256×1600 | **128×800** |
| augmentation | light | **none** | light | **strong** | light |
| use_scheduler | ✅ | ✅ | **❌** | ✅ | ❌ |
| loss 权重 | BCE 0.5 + Dice 0.5 | 同 | 同 | **BCE 0.4 + Dice 0.6** | 同 |
| max_samples | 全量 | 全量 | 全量 | 全量 | **训练32 / 验证16** |

---

## 推理流程总览

```
sample_submission.csv (ImageId_ClassId 模板骨架, 20000+ 行)
    ↓ 提取唯一 ImageId
test_df: [a.jpg, b.jpg, ...]  约 5000 张图
    ↓ SeverstalDataset: resize(256,1600) + normalize
    ↓ DataLoader(batch_size=8)
model(images) → sigmoid → predictions dict
    ↓ {"a.jpg": mask(256,1600,4), ...}
遍历 sample 的 20000+ 行:
    "a.jpg_1" → predictions["a.jpg"][:,:,0] → rle_encode → 字符串
    → 填回 EncodedPixels 列
    ↓
submission.csv (ImageId_ClassId + EncodedPixels, 20000+ 行)
```

---

## 训练不会出现格式问题

- **训练**使用 `train.csv`，格式为 `ImageId` + `ClassId` + `EncodedPixels` 三列分开 → 已正确适配
- **推理**使用 `sample_submission.csv`，格式为 `ImageId_ClassId` 合并列 → 已正确适配
- 两份 CSV 格式不同，修改后代码同时兼容两种
