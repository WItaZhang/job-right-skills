# JSON Resume

[上游仓库](https://github.com/jsonresume/jsonresume.org) · 核心：履历事实结构

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:53.0454955+00:00`。
默认分支 `master`；归档：否；许可：MIT（已读取许可文件）。
固定提交 [`dd0155358c8d`](https://github.com/jsonresume/jsonresume.org/commit/dd0155358c8d85a134d434e49834705243b5eede)，提交时间 `2026-09-09T17:42:32Z`。

## 一手证据与阅读范围

- [packages/schema/schema.json](https://github.com/jsonresume/jsonresume.org/blob/dd0155358c8d85a134d434e49834705243b5eede/packages/schema/schema.json)
- [packages/schema/README.md](https://github.com/jsonresume/jsonresume.org/blob/dd0155358c8d85a134d434e49834705243b5eede/packages/schema/README.md)
- [packages/schema/LICENSE.md](https://github.com/jsonresume/jsonresume.org/blob/dd0155358c8d85a134d434e49834705243b5eede/packages/schema/LICENSE.md)

当前 canonical schema 位于 monorepo 的 packages/schema，可表达 work、education、skills、projects 等；包 README 说明从旧 resume-schema 仓库迁入，并把 job schema 标为 draft。

## 可借鉴机制

履历事实使用有类型、可校验的字段，与未来希望从事的工作分开。为每条经历附内部证据引用，而不是从角色名称推断能力。

## 不应照搬之处

简历中做过管理不等于以后想管理；interests 不等于完整人生方向或风险偏好。不能把 draft job schema 当稳定标准，也不需要引入整个网站和主题系统。

## 对 job-right-skills 的映射

映射到 background_facts；preference profile 另含 kind、status、scope、用户确认与变更记录。当前仅字段研究，不发布真实简历，不复制 schema。

结论置信度：高（schema、包文档与许可文件）；未安装依赖。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
