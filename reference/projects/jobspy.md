# JobSpy

[上游仓库](https://github.com/speedyapply/JobSpy) · 补充：多来源字段归一化

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:50.9728483+00:00`。
默认分支 `main`；归档：否；许可：MIT（已读取许可文件）。
固定提交 [`fda080a373e8`](https://github.com/speedyapply/JobSpy/commit/fda080a373e8226f3fd60635323f5da9af9892b1)，提交时间 `2026-02-18T19:39:52Z`。

## 一手证据与阅读范围

- [README.md](https://github.com/speedyapply/JobSpy/blob/fda080a373e8226f3fd60635323f5da9af9892b1/README.md)
- [LICENSE](https://github.com/speedyapply/JobSpy/blob/fda080a373e8226f3fd60635323f5da9af9892b1/LICENSE)

README 展示跨平台职位采集及统一结果字段，包括 company、job_url、location、date_posted 和薪酬来源。

## 可借鉴机制

把 provider 字段转为一致的岗位记录，同时保留来源标识、原始岗位 URL 和原始薪酬语义。

## 不应照搬之处

搜索命中不证明当前开放，统一字段不证明具体团队；date_posted 不能代替我们核实的时间。不能把抓取缺失变成零岗位，不沿用代理绕限或邮件提取作为本项目能力；本次没有运行采集器。

## 对 job-right-skills 的映射

映射到未来 opening source adapter 的字段研究：provider、posting_id、canonical_url、source_url、source_updated_at、verified_at。职位聚合源用于发现，官方招聘页用于核实。

结论置信度：中（README 与字段列表）；采集实现和实时稳定性未审计。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
