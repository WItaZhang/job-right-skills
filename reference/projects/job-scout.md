# job-scout

[上游仓库](https://github.com/noircir/job-scout) · 受限参考：结构化偏好；许可信息待补齐

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:56.7941239+00:00`。
默认分支 `main`；归档：否；许可：README 自述 MIT；许可文件未发现，GitHub 未识别。
固定提交 [`9330f4a531b7`](https://github.com/noircir/job-scout/commit/9330f4a531b741b8b6708c3a242121a54068c07c)，提交时间 `2026-04-04T02:48:42Z`。

## 一手证据与阅读范围

- [README.md](https://github.com/noircir/job-scout/blob/9330f4a531b741b8b6708c3a242121a54068c07c/README.md)
- [config/profile.json.sample](https://github.com/noircir/job-scout/blob/9330f4a531b741b8b6708c3a242121a54068c07c/config/profile.json.sample)

config/profile.json.sample 分开 hard_constraints、preferences、target_roles、skills_for_matching，并列出 reasoning 和 gaps 等输出字段。README 声称 MIT，但 GitHub license 元数据为空，递归文件树未发现 LICENSE 文件。公开可读不等于已核实完整开源许可。

## 可借鉴机制

偏好带理由、技能区分已掌握与不主张、硬条件与软信号分组，方便解释为何某一岗位值得进一步研究。

## 不应照搬之处

不继承示例地理条件、权重、7 分阈值、技能重合百分比或“宁漏不误”策略；对跨境雇佣和工作授权的简化假设不能用来推断个人资格。未知条件不能压成布尔 false，也不能从 LLM 分数得出可靠概率。

## 对 job-right-skills 的映射

映射到 preference record 的 kind/value/rationale 和 match explanation 的 positives/gaps。增加 unknown、conflict、source_ref、confirmed_at；仅原创机制分析，许可证未补齐前不作代码复用候选。

结论置信度：高（已读样例字段）；可复用许可与评分效果未验证。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
