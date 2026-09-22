# 求职 agent 开源参考

核实日期：**2026-09-21，America/Los_Angeles**。
通过 GitHub API 与项目原始文档核实；每项保留默认分支、commit、归档状态和许可证。
这里的置信度指“资料支持设计分析的程度”，不代表项目性能或岗位匹配概率。

| 项目 | 主要参考价值 | 建议顺序 | GitHub 识别许可证 |
|---|---|---|---|
| [Job Search](projects/job-search.md) | 偏好访谈、单岗位匹配判断 | 优先读 | MIT |
| [career-ops](projects/career-ops.md) | 个人档案结构、可审阅岗位报告 | 优先读 | MIT |
| [JobSpy](projects/jobspy.md) | 多来源职位字段归一化 | 数据适配参考 | MIT |
| [JSON Resume](projects/jsonresume.md) | 履历事实的 schema | 结构化档案参考 | MIT |
| [Open Deep Research](projects/open-deep-research.md) | 公司/团队研究的任务分解 | 归档架构参考 | MIT |

选择依据：贴合偏好访谈、可解释判断、研究溯源、履历结构和数据适配中的具体环节；
能够定位到上游文件；能区分可借鉴设计与未经验证的效果声明。没有按 star 数堆项目。

优先读前两项，再读 [设计取舍与下一步验收案例](design-notes.md)。
机器可读的核实记录在 [sources.json](sources.json)。全部链接固定到核实时的 commit，
便于日后对比更新；仓库主页链接用于检查最新情况。

**筛选结果与边界：**旧 `jsonresume/resume-schema` 已迁移，改收录当前 monorepo；
Open Deep Research 已归档，降为架构参考。没有把自动批量投递作为本项目起点。
上游示例职业、经历和偏好不属于用户事实；实时岗位、团队归属及运行性能均未验证。

未安装任何参考项目，没有导入个人数据、连接职位服务、投递或联系公司。
原创笔记采用本仓库许可证；第三方许可证应在实际复用时按对应文件再次检查。
