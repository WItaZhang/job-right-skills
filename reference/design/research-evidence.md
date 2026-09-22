# company → team → current opening：研究与证据规则

日期：2026-09-22。以下为原创设计建议，未实现研究 agent，也未核实具体公司的当前岗位。
依据：[llm-job-pipeline](../projects/llm-job-pipeline.md)、[ATS 官方文档](../primary/ats-job-boards.md)、[JobPosting/PROV-O](../primary/jobposting-provenance.md)、[有界研究参考](../projects/open-deep-research.md)。

## 每一层分别回答一个问题

| 阶段 | 输入 | 优先证据 | 输出与停止条件 |
|---|---|---|---|
| company | 已确认 profile、待研究公司线索 | 官方产品、公司介绍、工程博客、招聘主页 | 公司标识、业务事实、偏好关联与 unknown；有足够依据判断是否值得继续研究即可 |
| team | 公司记录、用户关心的工作内容 | 官方团队页、署名工程文章、明确团队的 JD/ATS 字段 | 团队实体及 company→team 证据；找不到则 unknown，不补造团队 |
| current opening | 团队线索、官方招聘主页/ATS | 官方岗位详情、当前列表及明确截止/关闭信息 | 岗位标识、开放状态和 team→opening 证据；记录核实时点、缺口及失败 |
| explanation | 已核实 claim、profile revision | 逐项证据引用 | 硬条件结果、软取舍、匹配理由、置信度与下一步核实问题 |

公司发现也可来自聚合岗位板，但结论仍按公司→团队→岗位逐层组织。未知团队不必丢掉岗位线索；它必须显式显示“团队未核实”，且不能被包装成该团队的确定匹配。

company 与 source 是不同对象；“Engineering”部门不自动成为具体 team；官网的旧博客只能证明文章当时的情况，不能独自证明现在的团队编制或招聘归属。

## 证据粒度与来源优先级

**一个 claim 对应一个可核实断言**，例如“岗位归属推荐平台团队”或“招聘页在某时点列出此岗位”。避免一个 URL 支撑一整段公司文化结论。

优先雇主官方页面及从其官网确认的 ATS；官方团队文章用于有时间边界的职责信息；第三方聚合页用于发现和交叉核实；搜索摘要只作线索。官方文档也可能过期或互相矛盾，来源级别高不等于自动正确。

| 记录 | 最小内容 |
|---|---|
| entity | company_id、team_id、opening_id；unknown 团队不创建虚构实体 |
| relation | company→team / team→opening、evidence_ids、核实时点、unknown_reason |
| evidence | id、source_url、publisher、source_type、页面标题、支持的短摘要/定位 |
| observation | checked_at、retrieval_status、method、覆盖范围、来源发布日期/更新时间（若有） |
| claim | id、subject、predicate、value、status、evidence_ids、反证和推断说明 |
| freshness | last_successful_check_at、freshness_status、recheck_reason |
| match_reason | preference_id、profile_revision、claim_ids、符合点/取舍/缺口 |
| confidence | high / medium / low / unknown，加具体依据；不是录用概率 |

checked_at 是检查动作时间；verified_at 只在完成实质核实后填写；source_updated_at 是来源自己声称的更新时间。三者不互相替代。失败检查保留上次成功时间，但不能把历史结论展示成今天已核实。

## 状态不能混用

| 维度 | 拟议值 | 解释 |
|---|---|---|
| retrieval_status | success / failed / partial / not_checked | 技术读取是否成功、是否完整 |
| claim_status | supported / contradicted / conflict / unknown | 某断言的证据情况 |
| opening_status | published_present / explicitly_closed / unknown | 官网在核实时点仍展示 / 明确关闭 / 无法确认 |
| freshness_status | current / stale / unknown | 是否在该来源与断言的复核周期内 |
| user_decision | undecided / interested / not_interested | 用户自己的决定，不能由模型自动产生 |

published_present 表示官方来源此刻仍发布，不保证招聘负责人仍有名额。页面返回 200、存在 applyUrl、搜索引擎有缓存均不足以单独确认 current opening。

| 观察情况 | 处理 |
|---|---|
| 完整读取官方岗位列表与详情，岗位仍明确列出 | 可记 published_present，并给 as_of 与证据 |
| 页面明确写停止招聘/职位已关闭 | explicitly_closed；保留最后开放记录 |
| 404、访问受限、超时或页面跳转 | unknown + 原因；可能迁移，不能自动写 closed |
| 列表成功但分页不完整或过滤范围不明 | partial；缺席不能证明关闭 |
| 完整列表中未出现，详情也无法确认 | 记录缺席事实，opening_status 仍 unknown，待复核 |
| 截止时间已过，但正文仍表示开放 | conflict/unknown，显示两条证据，不静默选一条 |
| 一次成功检查为零岗位 | 记录该范围内零结果；不等于公司永不招聘 |

复核周期应按岗位、团队、公司信息的变化速度分别确定。当前不规定未经验证的统一 TTL；向用户展示前重新核实动态状态，并标明 as_of 时间。

## 置信度与匹配理由

- **high：**一手材料直接支持这一个断言，时点明确，未发现相互矛盾证据。
- **medium：**材料只部分支持或关系需推断；解释推断步骤，不升级为事实。
- **low：**只有间接、旧或弱材料；只保留研究线索。
- **unknown：**没有充分依据、读取失败或关键冲突未解决；不生成百分比。

上述是研究用分级，不是经过统计校准的模型概率。分别报告公司业务、团队关系、岗位状态的置信度；不要让公司官网的可信度自动传播到团队归属。

匹配解释的最小结构：`profile revision + preference_id → claim/evidence → 满足/不满足/未知 → 理由、反证、核实时间和置信度`。软偏好有利也要展示硬条件缺口；未知薪酬、团队和授权问题独立列出。

## 合成案例（不是实际岗位）

假设 SYN-01 用户已确认：P1=完全远程（hard），P2=更喜欢推荐系统业务（soft）。虚构的岗位 A 官方详情明确 remote；公司旧博客谈推荐技术，但 JD 只写 Engineering，未给具体 team。

预期解释：P1 可由岗位详情证据 E1 支持；P2 只有公司层面的旧线索 E2，岗位是否从事推荐研究仍 unknown。company→team 与 team→opening 没有直接依据，团队匹配不能声称 high。岗位是否仍发布需另记检查时间，不能用旧博客补足。

后续用户若把“必须做推荐系统”确认成 hard，新 profile revision 会使该岗位进入 needs_verification；旧结论保留历史但不继续当作当前判断。若随后网络读取失败，仅更新 retrieval_status=failed，不冒称已关闭。

## 未来人工验收点（未实现）

任一推荐理由可追到已确认偏好和来源；每条关系单独有证据或 unknown；复制转载不算多份独立佐证；来源中的指令性文本仅当作被研究内容；岗位/profile 更新使依赖它们的判断标记待复核。所有核实问题留给后续研究或用户，本轮不联系公司。
