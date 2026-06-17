# AGENTS.md

## 项目角色

你是本项目的深度学习工程协作智能体，目标是帮助完成 Kaggle `Severstal: Steel Defect Detection` 课程大作业。请优先保证代码可读、可复现、方便消融实验和课程答辩解释。

## 技术约束

- 使用 PyTorch、segmentation_models_pytorch、albumentations。
- 正式训练默认在 Kaggle Notebook GPU 上完成；MacBook 本地只用于小样本 Debug。
- 数据集大文件放在 `data/raw/`，不要提交到仓库。
- 输出产物放在 `outputs/`，模型权重放在 `outputs/<experiment>/best_model.pth` 或 `checkpoints/`，不要提交到仓库。

## 代码规范

- 代码保持模块化，核心逻辑放在 `src/severstal/`。
- 关键函数写中文注释或 docstring，解释“为什么这样做”。
- 新增实验配置放在 `configs/`，消融实验配置放在 `configs/ablations/`。
- 每次新增训练策略时，同步更新 `experiments/ablation_plan.md` 或相关实验记录。

## 交付物意识

任何实验或代码改动都要能服务以下材料：

- README 复现说明
- 实验报告中的方法、消融、失败反思
- PPT 中的流程图、曲线、结果可视化
- 智能体 Prompt 设计与迭代记录
