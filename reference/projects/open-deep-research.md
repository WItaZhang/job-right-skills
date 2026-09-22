# Open Deep Research

[上游仓库](https://github.com/langchain-ai/open_deep_research) · 补充：已归档的研究架构参考

核实日期：2026-09-22（America/Los_Angeles）；读取完成时间 `2026-09-22T23:41:55.1721882+00:00`。
默认分支 `main`；归档：是；许可：MIT（已读取许可文件）。
固定提交 [`1b7d2e80db9f`](https://github.com/langchain-ai/open_deep_research/commit/1b7d2e80db9faa586165c60e09096dbbfd483a64)，提交时间 `2026-08-10T18:13:29Z`。

## 一手证据与阅读范围

- [README.md](https://github.com/langchain-ai/open_deep_research/blob/1b7d2e80db9faa586165c60e09096dbbfd483a64/README.md)
- [src/open_deep_research/configuration.py](https://github.com/langchain-ai/open_deep_research/blob/1b7d2e80db9faa586165c60e09096dbbfd483a64/src/open_deep_research/configuration.py)
- [LICENSE](https://github.com/langchain-ai/open_deep_research/blob/1b7d2e80db9faa586165c60e09096dbbfd483a64/LICENSE)

README 描述可配置的研究流程和评估入口；configuration.py 提供澄清开关、研究迭代与并发上限等配置。GitHub 元数据显示仓库已归档。

## 可借鉴机制

给公司研究和团队研究分别定义问题、检索范围、停止条件与输出依据；信息不足时先澄清，有预算边界。

## 不应照搬之处

归档框架不作为当前运行依赖；不为做 reference 引入多 agent、数据库或模型服务。通用研究成绩不能证明求职匹配质量，生成的完整叙述也不能补足团队关系证据。

## 对 job-right-skills 的映射

映射到 company research 与 team research 的有界研究 brief。输出是 claim/evidence/unknown；当前只写文档，任务分解不代表已经实现运行时。

结论置信度：中（README 与配置）；未运行或验证 benchmark。以上映射为本项目的设计建议，不是上游功能承诺。
本页仅含原创摘要和链接，没有复制上游代码、提示词或完整文档。
