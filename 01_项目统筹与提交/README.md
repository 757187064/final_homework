# Severstal Steel Defect Detection 课程大作业指南

本项目用于完成 Kaggle `Severstal: Steel Defect Detection` 竞赛课程大作业。目标是在钢板表面图像中识别 4 类缺陷，并使用语义分割模型预测像素级 Mask，最终生成 Kaggle 要求的 RLE 格式 `submission.csv`。

这份 README 不只是代码说明，也是一份从“准备选题”到“最终汇报”的完整操作指南。你可以先按它独立跑通全流程，之后再把任务交给组员分工完善。

## 给组员的 10 分钟快速入口

如果你是第一次加入项目，不需要立刻读完整代码。先按这个顺序看：

1. 看本 README 的“项目定位”和“生成的材料怎么用”，知道项目在做什么。
2. 看 [docs/team_kickoff_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_kickoff_guide.md)，理解组内启动会和整体路线。
3. 看 [docs/collaboration_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/collaboration_guide.md)，确认自己负责哪条线。
4. 看 [docs/team_task_board.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_task_board.md)，填写自己的任务状态和截止时间。
5. 如果你负责训练，再看 [docs/kaggle_runbook.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/kaggle_runbook.md) 和 `configs/`。
6. 如果你负责报告/PPT，再看 [docs/project_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/project_report_draft.md)、[docs/ppt_outline.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/ppt_outline.md) 和 [docs/defense_question_bank.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/defense_question_bank.md)。

每位组员第一次同步时，请说明：

```text
我负责的方向：
我今天能完成的第一件事：
我需要别人提供什么：
我预计的交付时间：
```

## 你现在应该怎么用这个项目

建议按下面顺序推进：

1. 先阅读本 README，理解整体流程。
2. 填写 [docs/topic_info_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/topic_info_report_draft.md)，完成 5 月 22 日前的选题信息报告。
3. 在 Kaggle Notebook 中跑数据分析，生成类别分布和样本可视化图。
4. 跑通 Baseline 训练，拿到第一组 Dice、曲线和预测可视化。
5. 按 [experiments/ablation_plan.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/experiments/ablation_plan.md) 完成至少 4 组实验。
6. 把实验结果填进 [docs/project_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/project_report_draft.md) 和课程的 `实验报告模板.md`。
7. 按 [docs/ppt_outline.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/ppt_outline.md) 制作 12 分钟汇报 PPT。
8. 用 [docs/defense_question_bank.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/defense_question_bank.md) 准备答辩。
9. 提交前用 [docs/grading_coverage_checklist.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/grading_coverage_checklist.md) 逐项检查评分点。

## 项目定位

- 赛题：Kaggle `Severstal: Steel Defect Detection`
- 任务：4 类钢板缺陷语义分割
- 标注格式：RLE，存储在 `train.csv`
- 框架：PyTorch + `segmentation_models_pytorch` + `albumentations`
- Baseline：U-Net + ResNet34 Encoder + BCE/Dice 混合损失
- 训练平台：Kaggle Notebook 正式训练，本地 MacBook 只做小样本调试
- 课程目标：完整流程、可复现代码、消融实验、智能体协作记录、报告和 PPT

> 你的 MacBook 适合调试代码、检查数据格式、整理报告和做小样本验证；完整训练建议放到 Kaggle GPU。

## 目录结构和用途

```text
.
├── AGENTS.md                         # 智能体协作规则，报告中可作为 AGENTS.md 设计材料
├── configs/                          # 训练配置与消融实验配置
│   ├── debug.yaml                     # 本地小样本调试
│   ├── baseline.yaml                  # Baseline 正式训练
│   ├── full_pipeline.yaml             # 完整方案
│   └── ablations/                     # 消融实验配置
├── docs/                             # 报告、PPT、答辩、协作材料
├── experiments/                      # 消融实验和资源使用记录
├── scripts/                          # 可直接运行的命令入口
├── src/severstal/                    # 核心代码
├── tests/                            # 轻量测试
├── requirements.txt                  # Python 依赖
└── README.md                         # 当前指南
```

## 生成的材料怎么用

| 文件 | 作用 | 什么时候用 |
|---|---|---|
| [AGENTS.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/AGENTS.md) | 说明智能体如何按本项目规则工作 | 报告“AGENTS.md 设计”部分 |
| [docs/topic_info_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/topic_info_report_draft.md) | 选题信息报告草稿 | 5 月 22 日前提交 |
| [docs/team_kickoff_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_kickoff_guide.md) | 组内启动会讲解稿和分工话术 | 给三位队友讲项目时使用 |
| [docs/team_task_board.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_task_board.md) | 队伍任务看板 | 组会现场认领任务，会后更新状态 |
| [docs/project_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/project_report_draft.md) | 实验报告素材初稿 | 实验跑完后补数字和图 |
| [docs/ppt_outline.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/ppt_outline.md) | 现场 12 分钟 PPT 大纲 | 做汇报 PPT 时使用 |
| [docs/prompt_log_template.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/prompt_log_template.md) | 智能体 Prompt 迭代记录模板 | 报告“智能体使用记录”部分 |
| [docs/collaboration_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/collaboration_guide.md) | 后续组员分工和交接说明 | 组员加入时发给他们 |
| [docs/defense_question_bank.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/defense_question_bank.md) | 答辩问题清单 | 汇报前彩排 |
| [docs/grading_coverage_checklist.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/grading_coverage_checklist.md) | 评分点覆盖自查表 | 最终提交前检查 |
| [docs/kaggle_runbook.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/kaggle_runbook.md) | Kaggle Notebook 运行步骤 | 正式训练时照着做 |
| [experiments/ablation_plan.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/experiments/ablation_plan.md) | 消融实验记录表 | 每跑完一组实验就填写 |
| [experiments/resource_usage_log.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/experiments/resource_usage_log.md) | GPU、智能体和经费使用记录 | 支撑资源使用和加分项 |

## 数据放置方式

请不要把 Kaggle 大数据提交到课程仓库。下载数据后按下面结构放置：

```text
data/raw/
├── train.csv
├── sample_submission.csv
├── train_images/
│   ├── 0002cc93b.jpg
│   └── ...
└── test_images/
    ├── 004f40c73.jpg
    └── ...
```

在 Kaggle Notebook 中，常见数据路径是：

```text
/kaggle/input/severstal-steel-defect-detection/
```

如果使用 Kaggle 路径，请把配置文件里的：

```yaml
data:
  root: data/raw
```

改成：

```yaml
data:
  root: /kaggle/input/severstal-steel-defect-detection
```

## 环境安装

建议使用 Python 3.10 或 3.11。你当前本机 Python 3.14 对 PyTorch 生态可能不稳定，因此正式训练放 Kaggle 更稳。

本地环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Kaggle Notebook 中通常已经有 PyTorch，只需要补充：

```bash
pip install segmentation-models-pytorch albumentations opencv-python-headless
```

## 第 1 阶段：完成选题报告

打开 [docs/topic_info_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/topic_info_report_draft.md)，补充：

- 队伍名称
- 组长姓名和学号
- 组员姓名和学号
- 如果老师要求，补充提交日期或课程信息

这份草稿已经覆盖课程要求的三部分：

- 选题理由
- 预期收获
- 可行性分析

## 第 2 阶段：本地轻量检查

没有完整数据时，先检查 RLE 编解码和代码语法。

```bash
PYTHONPATH=src python3 - <<'PY'
import numpy as np
from severstal.rle import rle_encode, rle_decode
mask = np.zeros((4, 5), dtype=np.uint8)
mask[0, 0] = 1
mask[1, 0] = 1
assert np.array_equal(mask, rle_decode(rle_encode(mask), shape=mask.shape))
print("RLE smoke test passed")
PY
```

安装好依赖后再跑单元测试：

```bash
python3 -m pytest tests
```

如果本地有少量数据，可以用 debug 配置检查训练闭环：

```bash
python3 scripts/train.py --config configs/debug.yaml
```

`configs/debug.yaml` 已经把输入缩小到 `128x800`，适合 MacBook 小样本调试。

## 第 3 阶段：数据分析和可视化

这一步会生成报告/PPT 需要的数据图。

本地运行：

```bash
python3 scripts/analyze_data.py \
  --data-root data/raw \
  --output-dir outputs/data_analysis
```

Kaggle 运行：

```bash
python scripts/analyze_data.py \
  --data-root /kaggle/input/severstal-steel-defect-detection \
  --output-dir outputs/data_analysis
```

输出文件：

```text
outputs/data_analysis/
├── class_distribution.csv
├── class_distribution.png
└── sample_masks.png
```

使用方式：

- `class_distribution.csv`：填入报告“数据集介绍/类别不平衡分析”
- `class_distribution.png`：放入 PPT“数据分析”页
- `sample_masks.png`：放入报告和 PPT 的样本可视化页

## 第 4 阶段：跑 Baseline

在 Kaggle GPU 上运行：

```bash
python scripts/train.py --config configs/baseline.yaml
```

训练输出：

```text
outputs/baseline_unet_resnet34/
├── best_model.pth
├── config.yaml
├── history.csv
├── history.png
└── val_predictions/
```

这些文件的用途：

- `best_model.pth`：生成提交文件
- `config.yaml`：证明实验可复现
- `history.csv`：填消融实验表
- `history.png`：放进报告/PPT 的训练曲线
- `val_predictions/*.png`：放进报告/PPT 的预测效果可视化

## 第 5 阶段：生成 Kaggle 提交文件

Baseline 训练完成后运行：

```bash
python scripts/infer.py \
  --config configs/baseline.yaml \
  --checkpoint outputs/baseline_unet_resnet34/best_model.pth \
  --output outputs/baseline_unet_resnet34/submission.csv
```

然后把 `submission.csv` 上传到 Kaggle，记录 Public Score 和排名。分数填入：

- [experiments/ablation_plan.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/experiments/ablation_plan.md)
- [docs/project_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/project_report_draft.md)
- 最终实验报告模板中的“最终成绩与排名”

## 第 6 阶段：做消融实验

建议至少完成 4 组：

| 实验编号 | 配置文件 | 说明 |
|---|---|---|
| E0 | `configs/baseline.yaml` | Baseline |
| E1 | `configs/full_pipeline.yaml` | 完整方案 |
| E2 | `configs/ablations/no_augmentation.yaml` | 去掉数据增强 |
| E3 | `configs/ablations/no_scheduler.yaml` | 去掉学习率调度 |

运行方式类似：

```bash
python scripts/train.py --config configs/full_pipeline.yaml
python scripts/train.py --config configs/ablations/no_augmentation.yaml
python scripts/train.py --config configs/ablations/no_scheduler.yaml
```

每跑完一组，立刻填写 [experiments/ablation_plan.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/experiments/ablation_plan.md)：

- Val Dice
- Kaggle Public Score
- 训练平台
- 结论
- 是否出现失败或异常

消融实验写报告时要强调：同一随机种子、同一数据划分、同一指标，每次只改变一个关键变量。

## 第 7 阶段：整理实验报告

最终报告建议以课程的 [实验报告模板.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/实验报告模板.md) 为正式文件。

你可以从 [docs/project_report_draft.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/project_report_draft.md) 复制素材，然后补充：

- 数据集规模和类别分布
- Baseline 训练结果
- 消融实验表格
- 训练曲线和预测可视化
- Kaggle 分数和排名
- 失败尝试与反思
- 智能体使用记录
- 组员贡献分工
- 资源使用情况

智能体使用记录可以从 [docs/prompt_log_template.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/prompt_log_template.md) 开始填。建议保留 2-3 个真实案例：

- 项目总蓝图设计
- RLE/Dataset 实现与调试
- 消融实验设计

## 第 8 阶段：制作 PPT

按 [docs/ppt_outline.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/ppt_outline.md) 做 12 分钟 PPT。建议控制在 12-14 页。

优先放这些图：

- `outputs/data_analysis/class_distribution.png`
- `outputs/data_analysis/sample_masks.png`
- `outputs/<experiment>/history.png`
- `outputs/<experiment>/val_predictions/*.png`
- 消融实验结果表

汇报逻辑建议：

1. 为什么选这个赛题
2. 数据和任务难点是什么
3. Baseline 怎么设计
4. 做了哪些优化
5. 消融实验说明每个组件有没有用
6. 智能体如何参与
7. 资源使用和团队分工
8. 总结与反思

## 第 9 阶段：准备答辩和最终检查

答辩前看 [docs/defense_question_bank.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/defense_question_bank.md)，重点准备：

- 为什么这是语义分割，不是普通分类
- RLE 是什么，为什么容易出错
- Dice 指标是什么意思
- 为什么选 U-Net + ResNet34
- BCE + Dice Loss 为什么组合
- 消融实验如何保证公平
- MacBook 跑不动完整训练怎么办
- 智能体生成代码如何验证正确性

提交前用 [docs/grading_coverage_checklist.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/grading_coverage_checklist.md) 检查 8 个评分维度。

## Kaggle 离线权重提醒

`encoder_weights: imagenet` 会让 `segmentation_models_pytorch` 下载预训练权重。Kaggle Notebook 如果关闭网络，可能会在首次创建模型时报错。解决方案有三种：

- Notebook Settings 中开启 Internet；
- 把配置里的 `encoder_weights` 改成 `null`，牺牲一点收敛速度换稳定运行；
- 提前把预训练权重作为 Kaggle Dataset 挂载并放入缓存目录。

## 后续组员加入时怎么分工

先把 [docs/team_kickoff_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_kickoff_guide.md) 发给组员，开会时按里面的 20-30 分钟流程讲；再用 [docs/collaboration_guide.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/collaboration_guide.md) 和 [docs/team_task_board.md](/Users/sakiko/Public/deeplearing/期末汇报大作业/docs/team_task_board.md) 认领任务：

- 数据负责人：跑数据分析、解释类别不平衡、整理样本图
- 模型负责人：跑 Baseline、改模型配置、记录训练结果
- 实验负责人：完成消融实验表、画结果对比图、写结论
- 汇报负责人：制作 PPT、整理 Prompt 记录、准备答辩
- 项目负责人：统一版本、最终报告、提交物检查

如果组员加入较晚，也可以直接从本文档和 `docs/` 材料接上，不需要重新从零理解项目。

## 最终提交清单

- 代码仓库：`src/`、`scripts/`、`configs/`、`tests/`、`README.md`
- 实验报告 Markdown：基于 `实验报告模板.md` 完成
- PPT PDF：按 `docs/ppt_outline.md` 制作并导出
- 纸质报告：现场带 4 份
- Kaggle 结果：Public/Private 分数、排名截图或记录
- 实验材料：训练曲线、预测可视化、消融实验表
- 智能体材料：Prompt 迭代记录、AGENTS.md 说明、协作过程反思
- 资源材料：GPU 时长、经费使用、智能体服务使用记录
