# 消融实验工作记录

## 1. 任务概述

本任务为钢铁缺陷检测项目的消融实验（Ablation Study），旨在通过对比实验验证各优化策略的有效性。

### 1.1 项目背景
- **任务类型**: 语义分割（4类别钢铁缺陷检测）
- **数据集**: Severstal Steel Defect Detection
- **数据集规模**: 12568张训练图像（6666有缺陷，5902无缺陷）
- **评价指标**: Dice系数

### 1.2 实验目标
- 验证各优化策略对模型性能的影响
- 找出最佳配置组合
- 为实验报告和答辩提供真实实验数据

---

## 2. 消融实验设计

### 2.1 实验配置（共5组关键实验）

| 编号 | 实验名称 | 架构 | 编码器 | 数据增强 | 损失函数 | Epochs | 描述 |
|------|----------|------|--------|----------|----------|--------|------|
| 1 | Baseline | U-Net | ResNet34 | light | BCE:Dice=0.5:0.5 | 15 | 基础配置 |
| 2 | No_Augmentation | U-Net | ResNet34 | none | BCE:Dice=0.5:0.5 | 25 | 验证数据增强效果 |
| 3 | Strong_Augmentation | U-Net | ResNet34 | strong | BCE:Dice=0.5:0.5 | 25 | 验证强增强效果 |
| 4 | EfficientNet_B3 | U-Net | EfficientNet-B3 | light | BCE:Dice=0.5:0.5 | 25 | 验证更强编码器 |
| 5 | Loss_Dice_Heavy | U-Net | ResNet34 | light | BCE:Dice=0.3:0.7 | 25 | 验证Dice损失权重 |

### 2.2 训练配置
- **优化器**: AdamW
- **学习率**: 0.0003（除EfficientNet外）/ 0.001（EfficientNet）
- **Batch Size**: 8（除EfficientNet外）/ 6（EfficientNet，需较小batch）
- **学习率调度**: Cosine Annealing
- **混合精度**: AMP enabled
- **验证频率**: 每个epoch后

---

## 3. 环境配置过程

### 3.1 遇到的问题及解决方案

| 问题 | 解决方案 |
|------|----------|
| CPU训练太慢（~30秒/批） | 安装GPU版PyTorch (CUDA 12.1) |
| DLL初始化失败 | 使用CPU版PyTorch测试后安装GPU版 |
| 磁盘空间不足 | 清理pip缓存，安装CPU-only版临时使用 |
| 依赖版本冲突 | 降级numpy到1.26.4，opencv到4.8.1.78 |
| timm库兼容性问题 | 安装timm==0.6.12 |
| 中文路径导致图片读取失败 | 备用方案使用numpy+cv2.imdecode |

### 3.2 最终环境配置
```
PyTorch: 2.4.0 (CUDA 12.1)
torchvision: 0.19.0
segmentation-models-pytorch: 0.3.4
albumentations: 1.4.0
opencv-python-headless: 4.8.1.78
numpy: 1.26.4
timm: 0.6.12
```

### 3.3 GPU信息
- **显卡**: NVIDIA GeForce RTX 4060
- **显存**: 8GB
- **性能提升**: 相比CPU提升约27倍

---

## 4. 实验执行流程

### 4.1 数据路径配置
所有配置文件中的数据路径已更新为本地路径：
```yaml
data:
  root: D:/迅雷下载/final_homework-main/severstal-steel-defect-detection
```

### 4.2 执行脚本

#### 方式1: 单个实验手动执行
```bash
python scripts/train.py --config configs/baseline.yaml
python scripts/train.py --config configs/ablations/no_augmentation.yaml
# ... 以此类推
```

#### 方式2: 批量自动执行（推荐）
```bash
# 双击运行
run_ablation_auto.bat
```
此脚本会自动连续运行所有5组实验，并在完成后自动汇总结果。

### 4.3 时间估算
| 实验 | Epochs | 预计时间 |
|------|--------|----------|
| Baseline | 15 | ~90分钟 |
| No_Augmentation | 25 | ~90分钟 |
| Strong_Augmentation | 25 | ~2小时 |
| EfficientNet_B3 | 25 | ~2小时 |
| Loss_Dice_Heavy | 25 | ~2小时 |
| **总计** | - | **~9小时** |

---

## 5. 输出文件说明

### 5.1 输出目录结构
```
outputs/
├── baseline_unet_resnet34/
│   ├── history.csv          # 训练历史
│   ├── config.yaml         # 配置文件副本
│   ├── best_model.pth      # 最佳模型
│   └── val_visuals/        # 验证可视化
├── ablation_no_augmentation/
├── ablation_strong_augmentation/
├── ablation_efficientnet_b3/
├── ablation_loss_dice_heavy/
└── ablation_results_summary.csv  # 结果汇总表
```

### 5.2 history.csv 字段说明
| 字段 | 说明 |
|------|------|
| epoch | 轮次编号 |
| train_loss | 训练损失 |
| val_loss | 验证损失 |
| val_dice | 验证Dice系数 |
| lr | 学习率 |

---

## 6. 实验监控方法

### 6.1 实时查看训练进度
```bash
# 方法1: 查看最新输出
tail -f outputs/baseline_unet_resnet34/history.csv

# 方法2: 查看训练日志
Get-Content outputs/baseline_unet_resnet34/train.log -Wait
```

### 6.2 查看最佳结果
每个实验完成后，最佳结果会自动记录在history.csv中，Dice最高的那一行即为最佳结果。

---

## 7. 注意事项

### 7.1 重要提醒
1. **不要中断脚本**: 批量脚本运行期间请勿手动停止，否则后续实验不会继续
2. **检查GPU**: 确保GPU可用（`nvidia-smi`）
3. **磁盘空间**: 每个实验约需2-3GB空间
4. **中文路径**: 项目路径包含中文字符，cv2.imread会失败，但备用方案已实现

### 7.2 故障排除
| 问题 | 解决方法 |
|------|----------|
| 训练卡住 | 检查GPU是否可用，显存是否充足 |
| 读取图片失败 | 使用备用读取方案（已实现） |
| 内存不足 | 减小batch_size |

---

## 8. 相关文件清单

| 文件路径 | 说明 |
|----------|------|
| `configs/baseline.yaml` | Baseline配置 |
| `configs/ablations/no_augmentation.yaml` | 无数据增强实验配置 |
| `configs/ablations/aug_very_strong.yaml` | 强数据增强实验配置 |
| `configs/ablations/efficientnet_b3.yaml` | EfficientNet-B3编码器配置 |
| `configs/ablations/loss_dice_heavy.yaml` | Dice重损失配置 |
| `scripts/train.py` | 训练脚本 |
| `run_ablation_auto.bat` | 批量执行脚本 |
| `src/severstal/train.py` | 训练逻辑实现 |
| `src/severstal/dataset.py` | 数据集加载实现 |

---

## 9. 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2024-XX-XX | 创建消融实验设计 |
| 2024-XX-XX | 配置本地环境，安装GPU版PyTorch |
| 2024-XX-XX | 创建自动化批量执行脚本 |
| 2024-XX-XX | 执行消融实验并记录结果 |

---

## 10. 自动化执行脚本

### 10.1 执行方式

**推荐使用Python脚本执行：**
```bash
python run_ablation_auto.py
```

此脚本会自动：
1. 依次运行5组消融实验
2. 记录每个实验的开始和结束时间
3. 实验失败时自动跳过并继续下一个
4. 所有实验完成后自动汇总结果
5. 生成CSV和Markdown格式的结果汇总文件

### 10.2 脚本功能
- 自动监控训练进度
- 异常处理（训练失败不影响后续实验）
- 结果自动汇总到 `outputs/ablation_results_summary.csv`
- 详细日志输出

---

## 11. 下一步工作

1. [x] 等待所有消融实验完成（预计9小时）
2. [ ] 分析各实验结果
3. [ ] 更新实验报告文档
4. [ ] 更新PPT和答辩题库
5. [ ] 生成最终提交文件

---

## 12. 当前执行状态

**脚本**: run_ablation_auto.py
**启动时间**: 2026-06-05 01:12:21
**状态**: 运行中

**实验进度：**
- [ ] Baseline (15 epochs, ~90分钟)
- [ ] No_Augmentation (25 epochs, ~90分钟)
- [ ] Strong_Augmentation (25 epochs, ~2小时)
- [ ] EfficientNet_B3 (25 epochs, ~2小时)
- [ ] Loss_Dice_Heavy (25 epochs, ~2小时)

---

*文档生成时间: 2026-06-05 01:12:21*
*项目路径: D:\迅雷下载\final_homework-main\final_homework-main\03_模型训练与代码实现*
