# llm-job-pipeline

[上游仓库](https://github.com/ncalavera/llm-job-pipeline) · 核心：company-first 与独立状态

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:59.3215906+00:00`。
默认分支 `main`；归档：否；许可：MIT（已读取许可文件）。
固定提交 [`dde24cc1acb3`](https://github.com/ncalavera/llm-job-pipeline/commit/dde24cc1acb3827dc8683d7d36c4e0b61882c447)，提交时间 `2026-09-22T05:52:48Z`。

## 一手证据与阅读范围

- [README.md](https://github.com/ncalavera/llm-job-pipeline/blob/dde24cc1acb3827dc8683d7d36c4e0b61882c447/README.md)
- [config/user_profile.example.md](https://github.com/ncalavera/llm-job-pipeline/blob/dde24cc1acb3827dc8683d7d36c4e0b61882c447/config/user_profile.example.md)
- [CONCEPTS.md](https://github.com/ncalavera/llm-job-pipeline/blob/dde24cc1acb3827dc8683d7d36c4e0b61882c447/CONCEPTS.md)
- [LICENSE](https://github.com/ncalavera/llm-job-pipeline/blob/dde24cc1acb3827dc8683d7d36c4e0b61882c447/LICENSE)

README 以 company-first 为入口；CONCEPTS.md 区分公司、来源、检查结果、数据新鲜度、岗位判断和用户决策。档案区分 filter、penalty、note，文档要求因素强度变更由用户决定。

## 可借鉴机制

公司实体与岗位/来源分开；先理解目标组织，再关注其岗位。检查失败、成功零结果、资料过期各自记录；模型分数与用户决定分开；偏好变化保留用户决策记录。

## 不应照搬之处

不采用其数值评分、自动归档阈值、托管面板、消息摘要与投递材料流程。README 也含岗位板发现路径，不能声称它完整实现严格 company→team→opening；团队证据层是本项目需要另补的研究。

## 对 job-right-skills 的映射

映射到 company shortlist、team evidence、opening verification 和 revision log。为 company→team 与 team→opening 两条边分别存证据；公司被发现不自动等于用户选中。

结论置信度：高（README、概念与档案文档）；没有端到端运行。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
