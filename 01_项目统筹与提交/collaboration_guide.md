# 四人小组协作指南

> 这份文档用于把当前项目样板交给三位队友协作。核心原则：每个人负责一条清晰产线，每个产出都能直接服务代码、实验、报告或 PPT。

## 当前项目状态

目前已经完成：

- PyTorch/SMP 分割项目代码骨架。
- RLE 编码/解码、数据读取、Dataset、训练、推理和提交脚本。
- Baseline、Full Pipeline 和两组消融实验配置。
- 报告草稿、PPT 大纲、答辩题库、评分覆盖表、Prompt 记录模板。
- MacBook Debug 和 Kaggle GPU 正式训练的运行说明。

还没有完成：

- Kaggle 正式训练结果。
- 数据分析图和预测可视化成品。
- 消融实验真实分数。
- 最终报告、PPT PDF、纸质报告。

## 四人推荐分工

| 角色 | 建议负责人 | 核心职责 | 直接产出物 |
|---|---|---|---|
| 项目统筹与整合 | 你 | 控制时间线、维护仓库说明、合并报告/PPT、记录智能体使用 | 选题报告、最终报告、Prompt 记录、提交清单 |
| 数据分析负责人 | 队友 A | 负责数据到 Mask：RLE、`train.csv` 聚合、Dataset 输入输出、数据增强、类别分布和样本可视化 | 数据图、样本图、RLE/数据管道说明、报告数据集章节 |
| 模型训练负责人 | 队友 B | 负责 Mask 到预测：U-Net、loss/metric、Kaggle 训练、checkpoint、submission 和调参 | checkpoint、history、预测图、submission、分数 |
| 实验汇报负责人 | 队友 C | 维护消融表、整理失败尝试、制作 PPT 和答辩材料 | 消融表、PPT 初稿、答辩问题、结果分析 |

这样分工后，2 号同学不只是画图，而是负责“原始数据如何进入模型”；3 号同学不需要独自承担全部代码解释，重点放在训练和提交。

## 任务认领表

| 编号 | 任务 | 建议负责人 | 输入 | 输出 | 完成标准 |
|---|---|---|---|---|---|
| T1 | 补全选题信息报告 | 项目统筹 | `docs/topic_info_report_draft.md` | 可提交的选题报告文本 | 队名、成员、选题理由、预期收获、可行性分析完整 |
| T2 | 生成数据分析图 | 数据负责人 | Kaggle 数据、`scripts/analyze_data.py` | `class_distribution.png`、`sample_masks.png` | 图能放进 PPT，能说明类别不平衡和缺陷样本 |
| T3 | 解释 RLE 与数据管道 | 数据负责人 | `rle.py`、`data.py`、`dataset.py`、`transforms.py` | RLE/数据管道说明、报告方法段落 | 写清 RLE、4 通道 Mask、Dataset 输出和数据增强 |
| T4 | 写数据集介绍 | 数据负责人 | 数据分析结果 | 报告 1.3/1.4 草稿 | 写清数据格式、RLE、类别分布、预处理 |
| T5 | 跑 Baseline | 模型负责人 | `configs/baseline.yaml` | `history.csv`、`history.png`、`best_model.pth` | 有 Val Dice、训练曲线和预测可视化 |
| T6 | 生成 Kaggle 提交 | 模型负责人 | Baseline checkpoint、`scripts/infer.py` | `submission.csv`、Kaggle 分数 | 提交格式正确，并记录 Public Score |
| T7 | 跑消融实验 | 模型负责人 + 实验负责人 | `configs/full_pipeline.yaml`、`configs/ablations/` | 3-4 组结果 | 每组只改变一个变量，结果填入消融表 |
| T8 | 维护实验记录 | 实验负责人 | 各次训练输出 | `experiments/ablation_plan.md` 更新版 | 每组有配置、指标、平台、耗时、结论 |
| T9 | 整理失败尝试 | 实验负责人 | 训练日志、问题记录 | 报告“失败尝试与反思”草稿 | 至少 2 条真实问题和解决过程 |
| T10 | 制作 PPT 初版 | 实验/汇报负责人 | `docs/ppt_outline.md`、图表结果 | 12-14 页 PPT | 每页一个重点，能 12 分钟讲完 |
| T11 | 整理智能体使用记录 | 项目统筹 | `docs/prompt_log_template.md`、真实对话 | 2-3 个 Prompt 迭代案例 | 包含初始 Prompt、问题、迭代 Prompt、效果 |
| T12 | 准备答辩 | 全员 | `docs/defense_question_bank.md` | 每人 2 个熟悉问题 | 每人能解释自己负责模块 |
| T13 | 最终提交检查 | 项目统筹 | `docs/grading_coverage_checklist.md` | 提交清单确认 | 代码、报告、PPT、纸质报告、结果材料齐全 |

## 文件交接规则

- 代码改动只改自己负责的模块，改前先说明目的。
- 配置文件每新增一组实验，都要同步更新 `experiments/ablation_plan.md`。
- Kaggle 训练输出要保留 `config.yaml`、`history.csv`、`history.png`、`val_predictions/` 和分数截图。
- 报告里的每个结论要能对应到实验表、曲线、可视化或配置文件。
- 不提交大数据、模型权重和 `outputs/` 里的大文件到课程仓库；需要展示的图片可以选择性保存到报告材料中。

## 推荐时间线

| 时间 | 目标 | 负责人 |
|---|---|---|
| 今天 | 完成组内分工，补全选题报告信息 | 全员 |
| 1-2 天内 | 跑出数据分析图和 Baseline 第一版 | 数据负责人、模型负责人 |
| 3-5 天内 | 完成至少 3 组消融，争取 4 组 | 模型负责人、实验负责人 |
| 6 月 7 日前 | 报告和 PPT 初版完成 | 项目统筹、汇报负责人 |
| 6 月 9 日前 | 彩排、答辩问题准备、补图补表 | 全员 |
| 6 月 10 日前 | 提交仓库、PPT PDF、实验报告 | 项目统筹 |

## 沟通格式

每次同步实验结果时，按这个格式发：

```text
实验名：
配置文件：
训练平台：
训练耗时：
Val Dice：
Kaggle Public Score：
输出位置：
遇到的问题：
结论：
```

每次同步报告/PPT 进度时，按这个格式发：

```text
负责章节/页面：
已完成内容：
缺少的图或实验：
需要谁配合：
下一步：
```

## 交接给组员时可以直接说

```text
我们已经有一个 Severstal 语义分割项目样板，包含数据处理、U-Net 训练、推理提交、消融配置和报告模板。
大家接下来不需要从零搭项目，而是按模块补齐实验结果、图表和分析。
每个人的产出都要能直接放进最终报告或 PPT。
```
