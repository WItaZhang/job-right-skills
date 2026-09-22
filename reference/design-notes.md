# 从参考资料到 job-right-skills 的映射

日期：2026-09-22。以下是研究阶段的采纳与不采纳决定；模块名表示未来职责，当前没有对应 agent 实现。

| 需求 | 依据 | 采纳的机制 | 本项目补充/不采纳 |
|---|---|---|---|
| 结构化 preference profile | [JSON Resume](projects/jsonresume.md)、[career-ops](projects/career-ops.md)、[job-scout](projects/job-scout.md) | 履历与目标分开、维度化记录 | 增加用户确认、scope、revision、unknown；不继承任何示例人物 |
| hard / soft | [Job Search](projects/job-search.md)、[llm-job-pipeline](projects/llm-job-pipeline.md) | 硬门槛与偏好影响分开 | hard 采用 pass/fail/unknown，不用软分抵消；不继承阈值 |
| 冲突澄清 | [Job Search](projects/job-search.md)、[偏好引导论文](primary/preference-elicitation.md) | 逐步提问、用具体情境澄清 | 硬冲突与软取舍分开，确认后修订，不静默覆盖 |
| company→team→opening | [llm-job-pipeline](projects/llm-job-pipeline.md)、[ATS 文档](primary/ats-job-boards.md) | 公司作为研究入口、来源和岗位分开 | 团队是独立证据层；不从标题或部门猜测团队 |
| 来源与核实时间 | [PROV-O / JobPosting](primary/jobposting-provenance.md) | 来源、派生结论、时间语义分离 | checked_at/verified_at/source_updated_at 分开；当前不用 RDF |
| 匹配理由 | [career-ops](projects/career-ops.md)、[Job Search](projects/job-search.md) | 逐项依据、优势、缺口 | 绑定 preference_id/evidence_id，不只是给总分 |
| 置信度 / unknown | [Job Search](projects/job-search.md)、[官方字段](primary/ats-job-boards.md) | 未披露即未知、来源字段缺失保留 | 每个 claim 单独定性置信度；未知不当负面，也不当通过 |
| 有界研究与采集 | [Open Deep Research](projects/open-deep-research.md)、[JobSpy](projects/jobspy.md) | 明确研究问题、归一字段、预算边界 | 暂不运行、安装或引入整个框架 |

## 当前优先结论

先定义 [偏好与冲突语义](design/preference-profile.md)，再定义 [关系、证据和时效](design/research-evidence.md)。核心是让任何后续判断都能解释“依据哪一版偏好、哪条证据、什么时间核实、哪些仍未知”。

先使用逐项定性说明。数字匹配分可以成为以后独立评估的议题，目前没有标注数据证明它可靠；confidence 也不解释成录用概率。

## 本轮复核纠正

- 旧名称 `career-scout-skills` 已按用户要求改为 `job-right-skills`；保留已有研究和 Git 历史。
- 历史简报中的 `owieschon/career-scout` 当前 API 返回 404；缓存机制线索保留在 [候选笔记](projects/career-scout.md)，不写成已验证实现。
- `noircir/job-scout` README 自述 MIT，但没有找到完整许可文件；仅作机制比较。
- JSON Resume 使用当前 monorepo `packages/schema`，旧仓库只说明迁移历史。
- Open Deep Research 已归档，作为研究架构参考而非当前运行依赖。
- 没有发现可直接证明整个严格 company→team→opening 链路都完整满足本项目要求的单一参考项目；团队关系证据、冲突修订和核实状态是本项目需要自行明确的部分。

## 研究交付验收

已为每条项目与一手资料写明可借鉴机制、不应照搬之处和映射；已记录来源、阅读范围、核实日期及 Git 固定版本；已提供合成场景和未来人工验收预期。未安装上游、未运行 agent、未建立真实个人 profile、未投递或联系公司。没有将文档检查描述为运行测试或 CI 成功。
