# 评分要求覆盖自查表

> 用于最终提交前核对材料是否覆盖课程评分点。建议在 2026-06-10 提交前由组长逐项确认。

## 提交物核对

| 要求 | 当前材料位置 | 状态 | 提交前动作 |
|---|---|---|---|
| 现场汇报 PPT/PDF | `docs/ppt_outline.md` | 待制作 | 按大纲制作 PPT，并导出 PDF 上传 Gitee |
| 实验报告 Markdown | `docs/project_report_draft.md`、`实验报告模板.md` | 草稿中 | 补实验分数、图表、排名、反思 |
| 纸质版实验报告 | 最终实验报告 | 待打印 | 汇报当天带 4 份 |
| 完整代码仓库 | `README.md`、`src/`、`configs/`、`scripts/` | 已有样板 | 最终确认可复现指令 |
| 分组与队伍信息 | 待填 | 待补 | 补队名、组员、组长、学号 |
| 选题信息报告 | `docs/topic_info_report_draft.md` | 草稿中 | 2026-05-22 24:00 前提交 |

## 评分维度覆盖

| 评分维度 | 分值 | 已覆盖材料 | 还需补充证据 |
|---|---:|---|---|
| 选题与研究价值 | 10 | `docs/topic_info_report_draft.md`、`docs/project_report_draft.md` | Kaggle 链接、选择理由最终版 |
| 内容完整性与深度 | 15 | `docs/ppt_outline.md`、`docs/project_report_draft.md` | 数据图、训练曲线、预测可视化 |
| 技术方案与创新性 | 15 | `docs/project_report_draft.md`、`README.md` | Baseline 分数、优化前后对比 |
| 实验设计与分析质量 | 15 | `experiments/ablation_plan.md` | 至少 3 组结果，建议 4 组；统一指标分析 |
| 智能体使用展示 | 10 | `docs/prompt_log_template.md`、`docs/collaboration_guide.md` | 工具名称/版本、真实 Prompt 迭代截图或记录 |
| 报告讲解表现 | 15 | `docs/ppt_outline.md` | 12 分钟讲稿、计时彩排记录 |
| 答辩表现 | 10 | `docs/defense_question_bank.md` | 每个成员至少准备 2 个可回答问题 |
| 团队协作展示 | 5 | `docs/collaboration_guide.md` | 每人具体贡献和答辩分工 |

## 加分项准备

| 加分项 | 可准备材料 | 当前建议 |
|---|---|---|
| ≥4 组消融实验 | `experiments/ablation_plan.md` | 做 E0-E3 四组，优先保证变量单一 |
| 技术博客 | 博客链接、截图、摘要 | 实验稳定后再写，避免空泛 |
| 经费效率 | `experiments/resource_usage_log.md` | 从第一次使用 GPU/智能体服务开始记录 |
| 组长加分 | 组长姓名学号、统筹工作说明 | 在报告贡献分工中明确写出 |
| 主持人加分 | 任课安排证明 | 如担任主持人再补 |

## 最终风险清单

- 实验表中不要只写“提升明显”，必须写同一指标下的数值对比。
- 智能体使用记录要展示“初始 Prompt -> 问题 -> 迭代 Prompt -> 改进结果”，不要只列工具名。
- 资源使用情况即使没有花满 500 元，也要说明算力平台、时长和费用，低成本完成反而可作为经费效率亮点。
- 答辩中每个关键结论都要能追溯到实验表、曲线、可视化或代码配置。
