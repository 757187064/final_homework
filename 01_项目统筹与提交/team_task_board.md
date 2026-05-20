# 队伍任务看板

> 用法：组会时把“负责人”和“截止时间”填上；会后每次同步只更新状态和产出链接。

## 状态说明

- 待开始：还没人处理。
- 进行中：已经有人认领。
- 待检查：产出已完成，等组内确认。
- 已完成：可以进入最终报告/PPT。

## 任务总表

| 状态 | 任务 | 负责人 | 截止时间 | 产出位置 | 检查标准 |
|---|---|---|---|---|---|
| 待开始 | 补全选题报告 | 待填 | 待填 | `docs/topic_info_report_draft.md` | 队名、成员、理由、收获、可行性完整 |
| 待开始 | 数据类别分布统计 | 待填 | 待填 | `outputs/data_analysis/class_distribution.*` | 有 CSV 和 PNG，能解释类别不平衡 |
| 待开始 | 缺陷样本可视化 | 待填 | 待填 | `outputs/data_analysis/sample_masks.png` | 至少展示多张缺陷图和 mask 叠加 |
| 待开始 | RLE 与数据管道说明 | 待填 | 待填 | `02_数据分析与可视化/RLE与数据管道说明.md` 或报告草稿 | 能讲清 train.csv、RLE、4 通道 Mask、Dataset 输出 |
| 待开始 | 数据增强解释 | 待填 | 待填 | 报告方法部分/PPT 优化策略页 | 能解释增强策略和 w/o Augmentation 消融意义 |
| 待开始 | Baseline 训练 | 待填 | 待填 | `outputs/baseline_unet_resnet34/` | 有 best model、history、预测图、Val Dice |
| 待开始 | Kaggle 提交 | 待填 | 待填 | `submission.csv`、分数记录 | 成功提交并记录 Public Score |
| 待开始 | Full Pipeline 实验 | 待填 | 待填 | `outputs/full_pipeline_unet_resnet34/` | 可与 Baseline 对比 |
| 待开始 | w/o Augmentation 实验 | 待填 | 待填 | `outputs/ablation_no_augmentation/` | 用于分析数据增强贡献 |
| 待开始 | w/o Scheduler 实验 | 待填 | 待填 | `outputs/ablation_no_scheduler/` | 用于分析学习率调度贡献 |
| 待开始 | 消融实验表整理 | 待填 | 待填 | `experiments/ablation_plan.md` | 每组有配置、指标和结论 |
| 待开始 | 资源使用记录 | 待填 | 待填 | `experiments/resource_usage_log.md` | 记录 Kaggle GPU、智能体服务、费用 |
| 待开始 | Prompt 迭代记录 | 待填 | 待填 | `docs/prompt_log_template.md` | 至少 2-3 个真实案例 |
| 待开始 | 报告初稿 | 待填 | 待填 | `docs/project_report_draft.md`、`实验报告模板.md` | 覆盖竞赛、方法、实验、智能体、总结 |
| 待开始 | PPT 初稿 | 待填 | 待填 | PPT 文件 | 12-14 页，能支撑 12 分钟讲解 |
| 待开始 | 答辩准备 | 待填 | 待填 | `docs/defense_question_bank.md` | 每人至少熟悉 2 个问题 |
| 待开始 | 最终提交检查 | 待填 | 待填 | `docs/grading_coverage_checklist.md` | 8 个评分维度都有证据 |

## 每日同步模板

```text
今天完成：
遇到问题：
明天计划：
需要别人协助：
```

## 实验结果同步模板

```text
实验名：
配置文件：
训练平台：
训练耗时：
Val Dice：
Kaggle Public Score：
输出文件：
结论：
```
