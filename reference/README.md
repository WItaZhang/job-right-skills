# Reference 索引

核实日期：**2026-09-22（America/Los_Angeles）**。项目文档固定到本次读取的 commit；官方网页记录 URL、日期和阅读范围。完整记录见 [sources.json](sources.json)。

## 选择方法

选择能定位到一手文件、机制可解释、与偏好优先的求职研究直接相关的项目；不以 star 数或 README 的效果宣称代替质量判断。逐项检查默认分支、当前提交、归档与许可，读关键文件；没有安装或运行上游项目。本文的“核心”表示适合当前设计研究，不是生产可用性背书。

本轮在既有 5 项笔记上重新核实，增加 company-first 项目、历史候选复核及官方数据/溯源资料。搜索主要围绕 job preference / hard constraints / company-first / JobPosting / provenance / example-critiquing；历史简报中的 3 个项目全部保留核实结论。

## 项目比较

| 项目笔记 | 可借鉴机制 | 不应照搬 | 本项目映射 | 取舍 |
|---|---|---|---|---|
| [Job Search](projects/job-search.md) | 访谈、逐岗位理由、未知项 | prose-only、缺失硬条件语义不一致 | interview → profile → explanation | 核心；MIT |
| [career-ops](projects/career-ops.md) | 档案维度、要求与证据对照 | 缺省布尔、示例履历、固定评分 | background facts、逐项报告 | 核心；MIT |
| [llm-job-pipeline](projects/llm-job-pipeline.md) | company-first、独立状态、偏好修订 | 完整应用与数值评分；团队层未证实 | company → team → opening | 核心；MIT |
| [JSON Resume](projects/jsonresume.md) | 履历事实结构 | 将履历当意愿；draft job schema 当标准 | background_facts | 核心；MIT |
| [JobSpy](projects/jobspy.md) | 多来源字段归一 | 聚合结果当开放证明 | opening source adapter 研究 | 补充；MIT |
| [Open Deep Research](projects/open-deep-research.md) | 有界研究、先澄清 | 完整框架和 benchmark 承诺 | company/team research brief | 已归档；MIT |
| [job-scout](projects/job-scout.md) | hard/soft 分组、理由与技能缺口 | 示例身份假设、权重与阈值 | preference record | README 自述 MIT，许可文件未发现 |
| [career-scout](projects/career-scout.md) | 缓存中的 gate/复查/decision log 线索 | 将缓存当当前实现 | 暂缓；可追踪候选 | API 404，当前版本与许可 unknown |

6 个许可明确的开源项目；1 个公开可读但许可信息待补齐的项目；1 个访问待核实候选。后两项不会被标成已验证可复用组件。

## 一手资料

| 来源 | 本轮读到的机制 | 笔记 |
|---|---|---|
| Greenhouse Job Board API | published jobs、岗位 ID、部门、更新时间 | [ATS 数据接口](primary/ats-job-boards.md) |
| Ashby Job Postings API | team/department、缺失值、isListed | [ATS 数据接口](primary/ats-job-boards.md) |
| Lever Postings API | published、分页、team/department、unknown country | [ATS 数据接口](primary/ats-job-boards.md) |
| Schema.org JobPosting | 岗位语义、地点限制、日期 | [岗位语义与溯源](primary/jobposting-provenance.md) |
| W3C PROV-O | 来源、派生关系、生成/失效时间 | [岗位语义与溯源](primary/jobposting-provenance.md) |
| Example-Critiquing with Suggestions（JAIR 2006） | 用候选对比逐步澄清偏好 | [偏好引导论文](primary/preference-elicitation.md) |

## 建议阅读顺序

1. Job Search + JSON Resume：分开“我做过什么”和“我想要什么”。
2. [偏好档案](design/preference-profile.md)：字段、hard/soft、冲突澄清与合成案例。
3. llm-job-pipeline + ATS 官方文档：实体与状态分开，补足团队关系证据。
4. [研究证据](design/research-evidence.md)：来源、时效、置信度、unknown 与逐项匹配理由。
5. [设计映射](design-notes.md)：记录采纳、不采纳与未来验收条件。

设计目录是原创研究结论，不是已实现 schema、运行配置或 skill。没有加入真实个人档案、真实公司推荐或岗位开放声明。只复述机制，不复制代码、完整提示词或第三方文档。
