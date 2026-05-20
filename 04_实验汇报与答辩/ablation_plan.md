# 消融实验记录表

本表用于后续实验后直接填入报告。所有实验建议使用同一份训练/验证划分、同一随机种子、同一评价指标。

| 实验编号 | 配置文件 | 核心变量 | Val Dice | Kaggle Public | 训练平台 | 结论 |
|---|---|---|---:|---:|---|---|
| E0 | `configs/baseline.yaml` | Baseline：U-Net + ResNet34 + light aug + scheduler | 待填 | 待填 | Kaggle GPU | 待填 |
| E1 | `configs/full_pipeline.yaml` | 更强增强 + 更长训练 + Dice 权重更高 | 待填 | 待填 | Kaggle GPU | 待填 |
| E2 | `configs/ablations/no_augmentation.yaml` | 去掉数据增强 | 待填 | 待填 | Kaggle GPU | 待填 |
| E3 | `configs/ablations/no_scheduler.yaml` | 去掉学习率调度 | 待填 | 待填 | Kaggle GPU | 待填 |

## 记录规范

- 每次实验保存配置文件、`history.csv`、`history.png`、最佳模型和预测可视化。
- 只改一个关键变量，避免无法解释提升来自哪里。
- 如果实验失败，也记录失败原因，例如显存不足、过拟合、训练不稳定、提交格式错误。

## 报告可用结论模板

- 数据增强的贡献：对比 E0 与 E2。
- 学习率调度的贡献：对比 E0 与 E3。
- 完整方案的综合收益：对比 E0 与 E1。
- 资源效率：记录 Kaggle GPU 使用时长，说明本地只做 Debug，正式训练使用免费/低成本 GPU。
