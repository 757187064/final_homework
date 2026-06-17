# deepseekers 钢板缺陷检测项目提交说明

本目录用于课程 Gitee 最终提交，项目任务来自 Kaggle `Severstal: Steel Defect Detection`。研究目标是使用深度学习方法识别钢板表面 4 类缺陷，并输出符合 Kaggle 要求的 `ImageId_ClassId,EncodedPixels` 格式提交文件。

## 队伍信息

| 角色 | 姓名 | 学号 | 主要负责内容 |
|---|---|---|---|
| 01 | 吴旭浦 | 23374093 | 项目统筹、提交材料、实验报告整合、格式检查 |
| 02 | 李彦霖 | 23376342 | 数据分析、类别分布统计、Mask 可视化 |
| 03 | 赵榕达 | 23375064 | 模型训练、代码实现、Kaggle 推理提交 |
| 04 / 组长 | 吴晓旭 | 23374382 | 汇报统筹、消融实验整理、PPT 与答辩 |

## 当前提交目录结构

```text
提交文件/
├── 代码/                         # 完整代码，以单层文件形式放置
├── 实验报告补充/                 # 实验报告、图表、结果证据、Prompt、资源记录，全部单层放置
├── .keep
├── AGENTS.md                     # 智能体协作与角色说明
├── README.md                     # 本说明文件
├── SKILL.md                      # 项目专用智能体技能说明
├── requirements.txt              # 根目录依赖备份
└── 钢板缺陷检测汇报1(2).pptx      # 当前已有汇报 PPT 文件，最终可按课程要求另存为 PDF
```

按你的最新要求，`代码/` 和 `实验报告补充/` 内部都不再继续分子文件夹，所有材料均以单个文件平铺保存。

## 课程提交要求对应

| 课程要求 | 当前对应位置 | 状态 |
|---|---|---|
| 完整可运行代码 | `代码/` | 已整理为单层文件；入口、配置、源码、测试均在其中 |
| README.md | `README.md`、`代码/README.md` | 已补充项目说明、环境配置和复现指南 |
| 依赖配置文件 | `requirements.txt`、`代码/requirements.txt` | 已具备 |
| Markdown 实验报告 | `实验报告补充/实验报告.md` | 已具备 |
| 实验报告 PDF | `实验报告补充/实验报告.pdf` | 已具备，可用于打印或备份 |
| 现场汇报 PPT | `钢板缺陷检测汇报1(2).pptx` | 已有 PPTX；最终仍需导出 PDF 上传 |
| PPT PDF | 暂无正式 PDF | 需要 PPT 完成后导出 |
| 纸质实验报告 4 份 | 线下打印 | 需要汇报前打印 |
| Gitee 仓库提交 | 整个 `提交文件/` 与必要工程内容 | 需要最终推送到课程 Gitee |

## 代码说明

`代码/` 中采用扁平文件名，前缀用于表示原始用途：

- `configs_*.yaml`：训练、消融和优化实验配置。
- `scripts_*.py` / `scripts_*.bat`：训练、推理、数据分析和自动消融入口。
- `src_severstal_*.py`：核心数据读取、RLE、模型、损失、训练、推理和可视化模块。
- `tests_*.py`：RLE 与数据格式测试。
- `requirements.txt`：运行依赖。
- `README.md`：代码复现说明。

由于代码已按要求平铺，运行时直接使用同层文件名，例如：

```bash
python scripts_train.py --config configs_baseline.yaml
python scripts_infer.py --config configs_baseline.yaml --checkpoint outputs/baseline_unet_resnet34/best_model.pth --output outputs/baseline_unet_resnet34/submission.csv
```

## 实验报告补充说明

`实验报告补充/` 中保存报告正文和报告支撑材料：

- `实验报告.md`：课程 Markdown 实验报告。
- `实验报告.pdf`：当前导出的报告 PDF。
- `图表素材_*.png/.csv`：类别分布、样本 Mask、补充可视化图。
- `实验结果证据_*.csv/.png/.yaml`：Baseline、Full Pipeline、No Augmentation、No Scheduler 等实验结果。
- `扩展实验证据_*.csv/.yaml`：04 号同学补充的扩展消融实验。
- `智能体Prompt记录.md`、`智能体证据_*.md`：智能体使用与 Prompt 证据。
- `资源使用与经费记录.md`：本地 4060、Kaggle GPU、Codex 和 token 费用记录。
- `技术博客分享稿.md`：博客加分项分享稿，发布后补链接。

## 主实验结果口径

| 实验 | 本地 Val Dice | Kaggle Private Score | Kaggle Public Score | 结论 |
|---|---:|---:|---:|---|
| Baseline | 0.6450 | 0.84233 | 0.80548 | Public 最优，稳定备选 |
| Full Pipeline | 0.6613 | 0.74355 | 0.73140 | 本地验证较好，但 Kaggle 分数下降 |
| No Augmentation | 0.6373 | 0.84558 | 0.80372 | Private 最优，最终主结果 |
| No Scheduler | 0.6281 | 0.83704 | 0.79335 | 略低，说明 scheduler 有一定作用 |

最终汇报建议口径：No Augmentation 作为 Private 最优主结果，Baseline 作为 Public 最优稳定备选，Full Pipeline 作为“本地验证与榜单不一致”的反思案例。

## 资源使用记录

| 资源 | 使用情况 | 费用 |
|---|---|---:|
| 本地 RTX 4060 | 约 20 小时 | 0 元 |
| Kaggle GPU | 约 20 小时 | 0 元 |
| Codex | 项目统筹、代码检查、报告整理 | 约 20 美元 |
| Token 额度 | 100 元额度，未完全用完 | 100 元以内 |

## 仍需提交前确认

- PPT 完成后导出正式 PDF，并放在本目录根部或按老师要求上传。
- 纸质实验报告需要现场打印 4 份。
- 最终把本目录推送到课程 Gitee 仓库。
- 若老师要求模型权重，需另行确认 `.pth` 文件是否上传或通过网盘补充。

GitHub 仓库链接：<https://github.com/757187064/final_homework>
