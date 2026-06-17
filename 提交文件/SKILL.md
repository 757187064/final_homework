# SKILL.md

## 技能名称

Severstal 钢板缺陷检测项目整理与复现技能

## 适用场景

当需要整理、复现或检查本项目时使用本技能。项目任务是 Kaggle `Severstal: Steel Defect Detection`，目标是完成 4 类钢板表面缺陷的语义分割，并整理为课程期末汇报大作业提交材料。

## 项目目录约定

```text
提交文件/
├── 代码/
├── 实验报告补充/
├── AGENTS.md
├── README.md
├── SKILL.md
├── requirements.txt
└── 钢板缺陷检测汇报1(2).pptx
```

`代码/` 和 `实验报告补充/` 内部均不再分子文件夹，所有文件平铺保存。

## 代码文件规则

| 文件类型 | 命名规则 | 说明 |
|---|---|---|
| 配置文件 | `configs_*.yaml` | Baseline、Full Pipeline、消融和优化配置 |
| 脚本入口 | `scripts_*.py`、`scripts_*.bat` | 训练、推理、数据分析、自动消融 |
| 核心模块 | `src_severstal_*.py` | 数据、RLE、模型、损失、训练、推理、可视化 |
| 测试文件 | `tests_*.py` | RLE 和数据格式测试 |

常用命令：

```bash
python scripts_train.py --config configs_baseline.yaml
python scripts_train.py --config configs_ablation_no_augmentation.yaml
python scripts_infer.py --config configs_baseline.yaml --checkpoint outputs/baseline_unet_resnet34/best_model.pth --output outputs/baseline_unet_resnet34/submission.csv
```

## 数据与提交格式

默认本地数据目录：

```text
data/raw/
├── train.csv
├── sample_submission.csv
├── train_images/
└── test_images/
```

Kaggle 环境中可把 `data.root` 改为：

```text
/kaggle/input/severstal-steel-defect-detection
```

最终 submission 必须满足：

- 表头：`ImageId_ClassId,EncodedPixels`
- 行数：22025 行含表头
- 每张测试图对应 4 个类别
- 空预测保留空字符串，不删除行

## 实验报告材料规则

`实验报告补充/` 中所有文件平铺保存：

| 材料 | 作用 |
|---|---|
| `实验报告.md` | Markdown 实验报告正文 |
| `实验报告.pdf` | 报告 PDF 版本，可用于打印或备份 |
| `图表素材_*.png/.csv` | 数据分析和可视化证据 |
| `实验结果证据_*.csv/.png/.yaml` | 主实验训练曲线、配置、submission 和预测示例 |
| `扩展实验证据_*.csv/.yaml` | 04 号同学补充的扩展消融结果 |
| `智能体Prompt记录.md` | 报告中的智能体 Prompt 案例 |
| `智能体证据_*.md` | 真实 Prompt 和代码协作证据 |
| `资源使用与经费记录.md` | GPU、Codex、token 费用记录 |
| `技术博客分享稿.md` | 博客加分项草稿，发布后补链接 |

## 实验结果口径

| 实验 | Val Dice | Private | Public | 说明 |
|---|---:|---:|---:|---|
| Baseline | 0.6450 | 0.84233 | 0.80548 | Public 最优，稳定备选 |
| Full Pipeline | 0.6613 | 0.74355 | 0.73140 | 本地验证更高但榜单下降 |
| No Augmentation | 0.6373 | 0.84558 | 0.80372 | Private 最优，最终主结果 |
| No Scheduler | 0.6281 | 0.83704 | 0.79335 | 验证 scheduler 有一定作用 |

说明时必须区分本地 Val Dice 与 Kaggle Public/Private Score，不能把两类指标混为同一评价。

## 提交前检查

1. README、AGENTS、SKILL、requirements 文件齐全。
2. `代码/` 中不存在子文件夹，入口命令使用平铺文件名。
3. `实验报告补充/` 中不存在子文件夹，图片引用指向同层文件。
4. PPT 完成后导出 PDF。
5. 纸质实验报告打印 4 份。
6. 最终推送至课程 Gitee 仓库。
