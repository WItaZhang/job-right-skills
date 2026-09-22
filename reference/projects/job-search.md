# Job Search

[上游仓库](https://github.com/agent-data/job-search) · 核心：偏好访谈与 unknown

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:47.1694227+00:00`。
默认分支 `main`；归档：否；许可：MIT（已读取许可文件）。
固定提交 [`dba0c0992e9d`](https://github.com/agent-data/job-search/commit/dba0c0992e9d7fc6533dd1be3003df7a311168f0)，提交时间 `2026-08-13T05:39:21Z`。

## 一手证据与阅读范围

- [skills/job-preference-interview/SKILL.md](https://github.com/agent-data/job-search/blob/dba0c0992e9d7fc6533dd1be3003df7a311168f0/skills/job-preference-interview/SKILL.md)
- [skills/evaluate-job-fit/SKILL.md](https://github.com/agent-data/job-search/blob/dba0c0992e9d7fc6533dd1be3003df7a311168f0/skills/evaluate-job-fit/SKILL.md)
- [LICENSE](https://github.com/agent-data/job-search/blob/dba0c0992e9d7fc6533dd1be3003df7a311168f0/LICENSE)

访谈 skill 将意图整理为 prose brief；单岗位评价 skill 按硬条件、未知项、定性匹配理由输出。评价文档明确：未说明的条件保留 unknown，未知硬条件进入人工核实。

## 可借鉴机制

把访谈与匹配评价分开；将“文化好”“工作生活平衡”等抽象要求追问为可观察条件；把背景经历与当前意愿分别记录。每个匹配理由引用具体岗位信息。

## 不应照搬之处

不能整套照搬 prose brief。访谈文档的 must-have 桶写有“absent or violated = reject”，而评价文档把未证实条件保留为 unknown；本项目明确采用三态规则，避免把未披露当失败。快速访谈中的自动分类和隐含推断也不能替代用户确认；不接入其 CLI/API。

## 对 job-right-skills 的映射

映射到 preference interview、profile revision、match explanation。硬条件结果为 pass/fail/unknown；缺失字段进入澄清队列。匹配理由绑定 preference_id 与 evidence_id，初期使用定性结论。

结论置信度：高（文档机制）；运行效果未验证。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
