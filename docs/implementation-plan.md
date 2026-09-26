# job-right-skills 实现方案（r4）

日期：2026-09-23。本文是从 reference 阶段进入实现阶段的方案。r3 吸收了 [第 1 轮评审](implementation-plan-review.md) 的 R01–R10，r4 吸收了第 2 轮的 R11–R17，采纳情况见评审文件中的两张作者回应表。面向普通读者的说明见 [project-overview.md](project-overview.md)。尚未写任何 skill 代码。

## 1. 目标回顾

两段式求职 agent：

1. **深挖访谈（grill）**：不问表面问题，层层追问到本质，把用户真实意图落成若干份固定格式的 **direction template**，一个文件 = 一个求职方向。每份 template 里只有少数几个字段是方向的"本质"（key_fields），其余字段可以是不属于本质的其他底线、软偏好、无所谓或未知。所有适用且已确认的底线都参与筛选，本质字段只决定搜索重点与方向标题（§3.5）。
2. **找岗位 + 填申请（apply）**：用 template 去找岗位、打开申请页、从个人档案填表、上传简历，**停止在最终提交之前**，由人点 submit。

设计约束沿用 reference/design 的结论：事实与意愿分开；hard / soft / unknown 三态；每条判断可追溯到 preference 与 evidence；未披露不等于失败；模型不替用户做投递决定；页面内容与检索结果只是被读取的数据，不能改变这些规则。

## 2. 交付形态：一个 plugin，三个 skill

```text
job-right-skills/                       # plugin_root：只放随插件发布的代码与资产
  .claude-plugin/plugin.json
  skills/
    grill-direction/                    # 访谈 → direction template
      SKILL.md
      references/probe-playbook.md      # 追问算子、冲突处理、进度与停止规则
      references/template-schema.md     # 字段与引用约定（人读版）
      assets/direction.template.md
      assets/example-synthetic-*.md     # 多份合成示例：同一首句、不同动机
    find-openings/                      # template → 公司 → 岗位候选
      SKILL.md
      scripts/ats_fetch.py              # Greenhouse / Ashby / Lever 拉取，原始字段 + 归一字段
      references/evidence-rules.md      # research-evidence.md 的落地版
      fixtures/                         # 三家 ATS 的固定样本（含 null、多地点、分页不完整）
    prepare-application/                # candidate → application，停在最终提交前
      SKILL.md
      references/form-rules.md          # 动作边界、字段映射、blockers、审阅规则
      fixtures/local-form/              # 本地受控表单 + 记录 POST 的小服务器
  schema/
    direction.schema.json
    candidate.schema.json
    application.schema.json
    background_facts.schema.json
  scripts/
    resolve_workspace.py                # 解析并记录 workspace_root
    validate.py                         # 按 schema 校验 direction / candidate / application
  requirements.txt                      # pyyaml, jsonschema；Python >= 3.10
  reference/                            # 现有研究笔记，不动
  docs/                                 # 方案与评审
```

**workspace 与 plugin_root 分离（R09、R14）**：三个 skill 都通过 `scripts/resolve_workspace.py` 解析一个绝对 `workspace_root`，顺序为：环境变量 `JOB_RIGHT_WORKSPACE` → 当前目录所在 git 仓库根下的 `workspace/` → 报错要求用户指定。规则：

- 一次会话内首次解析后，workspace_root 作为工作上下文被三个 skill 显式复用；后续检测到当前目录变化导致解析结果不同时，先向用户说明并让其选择，不默默新建第二份档案。
- plugin_root 只用于定位 scripts、schema、assets、fixtures。禁止写入已安装插件的缓存与资产目录（已安装插件可能被复制进版本化缓存并在更新后清理）；环境变量指向这类位置时拒绝。开发 checkout 本身被用户显式指定为工作仓库时允许使用其 `workspace/`，并给出一次提示。
- **忽略规则随 workspace 创建**：首次创建 workspace 时在其内部写入专用 `.gitignore`（内容为 `*`、`!.gitignore`、`!README.md`），这样无论 workspace 落在哪个仓库都受保护；首次写私人资料前用 `git check-ignore -v` 在实际目标仓库验证，已被跟踪的文件不能声称受 ignore 保护。

workspace 目录结构：

```text
<workspace_root>/
  .gitignore                             # 随 workspace 创建，忽略除自身与 README 外的全部内容
  .job-right.json                        # workspace_root、plugin 版本、创建时间
  README.md
  profile/background_facts.yaml          # 履历事实（私有）
  directions/<direction-id>.md
  candidates/<direction-id>.md
  applications/<opening-id>.md
  evidence/
    boards/<provider>/<board>/<check-id>/ # 招聘板列表请求的观察记录：零结果与整板失败也能落盘
    openings/<opening-id>/                # 岗位详情原始快照（JD 正文、详情 JSON）
```

**关于 allowed-tools（R07）**：SKILL.md 的 `allowed-tools` 是调用时的工具预授权，不是隔离边界。三个 skill 分开的理由是职责与评测分离；"不提交"由 §5 的操作边界、回读与本地测试保证，不依赖工具列表。

## 3. grill-direction：访谈 skill 设计

### 3.1 借鉴什么

- **grill-me**：按"轮"提问，每轮问完当前 frontier（前置已答完的问题），frontier 为空即结束；用户拥有 scope。借轮次与停止思路，不借无状态。
- **agent-data/job-search 访谈 skill**：跳过无关维度、回读确认。借纠错机制，不借 prose brief 与"缺失即拒绝"；当前改为每批简短总结、收尾完整回读。
- **example-critiquing**：用 2–3 个合成情境让用户说出愿意牺牲什么。这是替代方案测试与强度确认的依据。

### 3.2 核心机制：why-ladder，含义与强度分开确认（R01、R03）

每条用户表述走同一条追问链：

| 步骤 | 做什么 | 例子 |
|---|---|---|
| stated | 记原话，生成 `source_ref` | "想在美国工作" |
| why | 问这个选择给你带来什么 | "美国哪里吸引你？" → "年轻人多、tech 聚集" |
| attribute | 抽象成可独立确认的字段，并记录用户认可的**可观察依据** | `location.city_profile`，依据示例：科技公司密度、25–35 岁从业者比例高、有活跃的技术社区 |
| alt_test | 用满足同一属性的其他选项测试**含义** | "深圳、新加坡这类城市可以吗？" → 可以 ⇒ 属性是城市氛围而不是国家；不可以 ⇒ 追问差异，可能拆出 `location.country` 或 `legal.work_authorization_goal` 等新字段 |
| strength | 单独确认**强度** | "如果一个岗位其他都很好，但所在城市没有这种氛围，你还会拒绝吗？" → 会 ⇒ hard；看情况 ⇒ soft |
| resolve | 写入字段：value、kind、scope、`alt_test_ref`、`hard_confirmation_ref` | 见 §3.4 |

规则：

- **替代方案可接受 ≠ 不可退让**。alt_test 只确定字段含义；kind=hard 必须有独立的 `hard_confirmation_ref`。用户前文已明确说过底线的，引用那句原话即可，不机械重问。
- **字段独立确认**。城市氛围与工作方式（remote/hybrid）是两个字段，各有自己的 kind 与引用；公司人数与融资阶段亦然。只有用户把组合条件整体表述并整体测试过，才作为一个组合字段，且不能为凑数或规避数量限制而打包。
- **举例 vs 清单**。`examples` 是帮助理解属性的城市举例；`allowed_values` 才是限定清单。两者分开记录。
- **按批并行追问**：默认每轮 6–8 个简短问题，按主题稳定编号；每条 ladder 每轮只问一个前置已满足的步骤，下轮根据各自回答继续。用户可以只答部分；未答不等于跳过、不知道或同意，不自动在下一批重复催问。已解决主题退出，有价值的问题少就少问，不凑数。
- **kind 与 status 分开（R12）**。`kind` 表示偏好性质：hard / soft / any（用户确认无偏好）/ unspecified（强度未问或未答）。`status` 表示确认状态：confirmed / pending / conflict / skipped / unknown。"无偏好 / 跳过 / 暂不知道"三种回答分别写成 kind=any+status=confirmed、status=skipped、status=unknown，不互换，不自动重新进入 frontier。
- 每个字段可带 `scope`（生效时间、地点、角色）。scope 不明与岗位证据不明是两回事，分别记录。
- 每批开头用一两句话总结新发现及接下来问什么；收尾或确认前完整回读，误解或用户要求时可提前回读。不为每题插入单独确认回合；每批回答集中保存一次，逐题保留独立引用。
- **开场与时间预算**：先说明会得到一份区分底线、偏好和待确认事项的方向草稿，预计 20–30 分钟，以及可按编号回答或直接说、只答部分、跳过、暂停恢复。语音以 30 分钟内收尾为目标，用实际时钟在轮间检查（含回答等待和处理时间）；约 20 分钟停止新主题，25 分钟开始回读保存，30 分钟不再开新轮，除非用户主动延长。未完成保留 draft 和 open_questions，不为赶时间补造 hard。不能看列表时可缩短语音批次。

### 3.3 冲突、拆方向、进度与停止（R04）

**冲突处理**：发现两条要求不一致时，先检查时间、地点、角色 scope 是否相同 → 不同 scope 则补齐 scope 而非判冲突 → 同 scope 再区分：两个 hard 不可同时满足（阻塞冲突，标 conflict，问一个能改变判断的最小问题）／soft 取舍（记录取舍，不判自相矛盾）／用户接受的备选路线。**只有用户明确确认两条路线可以各自独立接受时，才拆成两份 template**；拆分不是消除冲突的自动手段，也不能把用户要求的 A AND B 变成 A OR B。

**进度与字段状态分开**：访谈进度记录每个维度是 not_asked / asked；字段状态用 §3.2 的 status 枚举记录：confirmed / pending / conflict / skipped / unknown（kind=any 表示"无偏好"，是 kind 不是 status）。在时间允许时，相关的 not_asked 维度可与已有线索同批提问，优先追问已答主题，不必等所有 ladder 结束；已问过但回答 unknown 或 skipped 的不重开，除非新信息使原问题重新有意义。仅漏答的问题保留在 open_questions，不虚构字段状态或来源。

**停止**：用户要求暂停、当前范围已无有价值的可追问项，或到了时间预算的收尾阶段，即保存并停止。confirmed 另有校验条件（§3.5），不要求为了结束访谈填满所有维度。收尾说明方向、已确认条件、待确认项、文件位置和下一步；draft 可以恢复继续。

### 3.4 产出：direction template

Markdown 文件。**frontmatter 是当前 revision 的快照**；正文 `## 追问链` 记录每条 ladder 的引用内容，`## 修订记录` 追加旧值、新值、原因、来源。不在同一 YAML mapping 里重复追加同名键。

合成示例（完整回答链下的预期，不是所有"想去美国"输入的固定答案）。示例末尾含一个 status=pending 的 hard 字段，因此按 §3.5 整体只能是 draft；同一方向去掉该字段或把它确认后的 confirmed 版本见 `skills/grill-direction/assets/example-synthetic-city-profile.md`：

```yaml
id: dir-001
title: 年轻科技聚集城市里的中型 AI infra 公司，做 IC
revision: 3
status: draft                    # draft | confirmed；此例因含 pending hard 而为 draft
created_at: 2026-09-23T10:00:00+08:00
key_fields: [location.city_profile, role.nature, company.size]
fields:
  location.city_profile:
    value: tech_hub_young
    observable_criteria: [科技公司密度高, 25–35 岁从业者比例高, 有活跃线下技术社区]
    examples: [深圳, 新加坡, 旧金山湾区]
    kind: hard
    status: confirmed
    scope: {valid_from: 2026-10, roles: all}
    source_ref: I-003
    alt_test_ref: I-007
    hard_confirmation_ref: I-009
  location.workplace_type:
    value: [hybrid, onsite]
    kind: soft
    status: confirmed
    source_ref: I-011
    alt_test_ref: null
  role.nature:
    value: IC
    kind: hard
    status: confirmed
    source_ref: I-014
    alt_test_ref: I-015
    hard_confirmation_ref: I-016
  company.size:
    value: {min: 50, max: 500}
    kind: hard
    status: confirmed
    source_ref: I-018
    alt_test_ref: I-019
    hard_confirmation_ref: I-020
  company.funding_stage:
    value: [series_b, series_c, growth]
    kind: soft
    status: confirmed
    source_ref: I-021
  industry:
    value: [AI infra, developer tools]
    kind: soft
    status: confirmed
    source_ref: I-005
  compensation.base:
    value: null
    kind: unspecified
    status: unknown
    note: 币种与期间口径未定
  location.workplace_type_after_move:      # 未来才生效的条件，靠 scope 而不是靠删除来处理
    value: [hybrid]
    kind: hard
    status: pending                        # 用户说了"必须"，但还没做强度确认
    scope: {valid_from: 2027-06}
    source_ref: I-023
search_hints:
  keywords: [infrastructure engineer, platform engineer, ML infra]
  deprioritize: [manager, lead]      # 只影响发现排序，不是拒绝证据
open_questions:
  - "薪酬底线口径未定（币种、base/total）"
interview_progress:
  asked: [兴趣动力, 地点与时间, 角色与成长, 风险容忍]
  not_asked: [压力承受, 团队环境, 人生方向, 薪酬与身份]
```

正文 `## 追问链` 中每个 `I-xxx` 是一条访谈引用：时间、用户原话（私有）、访谈者问题、得出的结论。

### 3.5 key_fields 与 hard 的关系（R02，对第 7 节规则含义的明确）

- **参与过滤的是"适用的已确认 hard"（R12）**：kind=hard、status=confirmed，且 scope 在当前判断范围内（如 valid_from 未到的字段不适用，单独说明排除原因）。status=pending 或 conflict 的字段不能作为拒绝依据。**它们是否让某个岗位待澄清，按岗位逐个判断（R29）**：candidate 的 applicability 必须为方向里每个 hard 字段和每个 pending/conflict 字段给出状态；明确 `not_applicable` 且带 scope 原因的不阻塞该岗位，`not_confirmed`（与该岗位相关但未确认）才触发 needs_clarification；漏列不等于证明无关，validator 报错。方向级 pending_fields 只用于展示。
- **key_fields 是方向的"本质"**：从已确认 hard 中选出 2–4 个，用于搜索重点、方向标题和向用户解释"这个方向到底是什么"。key_fields ⊆ 已确认 hard。
- **direction status=confirmed 的条件**：key_fields 数量 2–4；每个 key_field 有 alt_test_ref 与 hard_confirmation_ref；不存在 status=conflict 的字段；不存在 kind=hard 且 status=pending 的字段。
- **draft 是合法的持久状态**：不受数量限制，允许 pending 与 conflict 字段存在。但"方向是否完成"与"字段是否真的已确认"是两回事（R22）：任何模式下，kind=hard 且 status=confirmed 的字段都必须有 hard_confirmation_ref，key_fields 的每一项都必须是合格的已确认 hard；draft 只豁免数量规则与"不得有 pending hard / conflict"。强度未确认的字段保持 pending，不能冒充 confirmed。两种校验是同一脚本的两个入口。用户只有一个 hard，或说"没有硬条件"，都忠实记录，方向停在 draft。
- **对 draft 运行 find-openings**：允许，输出的 candidate 标 `basis: exploratory`，并列出尚待确认的字段。**适用的已确认 hard 为零时不能得到 eligible_for_comparison**：按 reference 规则 4（偏好本身未确认 → 先澄清），结果为 needs_clarification，原因写"没有可用于筛选的已确认底线"。实现上不能让空列表的 all() 静默成 true。
- 有五个同范围已确认 hard 时全部保留并逐一过滤，key_fields 取其中 4 个，不丢弃、不合并、不自动拆方向。

这是对原"只对 key_fields 做 hard 判断"的修正：只检查 key_fields 会漏掉第五个 hard。

**validator 能证明什么**：`scripts/validate.py` 校验结构、引用存在、引用关联一致（如 confirmed hard 必有 hard_confirmation_ref 且该引用在追问链里存在；key_fields 引用的字段存在且为已确认 hard）。它不能证明引用内容真的支持判断，那是 §6 行为评测的事。

### 3.6 访谈维度

沿用 reference/design/preference-profile.md 的 8 个维度：兴趣动力、人生方向、压力承受、风险容忍、角色与成长、地点与时间、薪酬与身份、团队环境。不按顺序问遍，从用户第一句话展开 ladder。身份与工作授权只记用户陈述，不从目标地点或求职动机推断。

## 4. find-openings：找岗位 skill 设计

输入：一份或多份 direction（confirmed 或 draft）+ background_facts。输出：`candidates/<direction-id>.md`。

### 4.1 流程

1. **公司发现**：用 key_fields 与 search_hints 做 WebSearch，或用户直接给公司名单。公司被发现不等于被选中。`search_hints.deprioritize` 只影响发现与排序，不作为拒绝证据。
2. **招聘板确认**：从公司官网找到招聘板链接，记录 official_site → board 的关联证据；找不到官方 ATS 的记 unknown，不猜 board slug。
3. **岗位拉取**：`scripts/ats_fetch.py` 按 provider 拉取（R06、R17）：
   - 列表请求的观察记录写入 `evidence/boards/<provider>/<board>/<check-id>/`（请求参数、分页范围、retrieval_status、checked_at、原始响应），零结果与整板失败也在此落盘；岗位详情快照写入 `evidence/openings/<opening-id>/`。归一字段与原始字段并列，不覆盖。
   - 岗位身份：provider + board/site + 原生 posting_id；缺原生 ID 时用官方 canonical URL 派生并标 `id_source: derived_from_url`。
   - 字段：title、department（原始）、team（原始，null 则 null，不用 department 补）、locations[]、workplace_type、job_url、apply_url、jd_content 或快照引用、salary（原始结构，Lever 有 currency/interval/min/max，可用于口径判断）、source_published_at、source_updated_at、checked_at、retrieval_status（success / partial / failed / not_checked）、coverage（分页范围）。
   - 时间语义按 provider 单独映射：Ashby publishedAt → source_published_at；Greenhouse updated_at → source_updated_at；**Lever 官方公开字段表没有任何时间字段，两者均为 null**；实际响应中若出现未在文档中列出的时间字段，只留在原始快照，不升级为发布或更新时间。checked_at 始终是本次读取时间。
   - 404 / 超时 → retrieval_status=failed、opening_status=unknown，保留 last_successful_check_at；分页不完整 → partial；完整读取零结果 → success 且零结果。
   - **opening_status 与 freshness（R13）**：每次读取更新 opening_status（published_present / explicitly_closed / unknown）与 freshness_status（current / stale / unknown）及 recheck_reason，沿用 reference 的判定表。
4. **适用性判断先于证据判断（R12）**：先按 §3.5 选出"适用的已确认 hard"，不适用或未确认的字段单独列出排除原因；再对每个适用 hard 做 pass / fail / unknown，绑定 field_id、direction revision、facts revision、evidence 引用；软字段列符合 / 取舍 / 未知。缺正文证据保持 unknown，不凭模型对公司或城市的印象判 pass。薪酬缺币种、期间或 base/total 口径时不比较。
5. **结果与状态**：match_status 四选一，按 reference 顺序：任一适用已确认 hard 已证实 fail → rejected；applicability 中存在 not_confirmed 条目，或适用已确认 hard 为零 → needs_clarification；hard 证据缺失 → needs_verification；全部适用 hard pass → eligible_for_comparison。draft 方向的结果另标 `basis: exploratory`。四组都出现在输出里。**匹配通过不等于岗位仍开放**：opening_status 与 match_status 并列展示，旧匹配结果作为历史保留，不重写为今天已核实。
6. **用户决定**：`user_decision` 独立字段，undecided / interested / not_interested，只由用户填写。eligible 不自动变 interested；用户对 needs_verification 的岗位选 interested 时允许，候选记录中的未解决项原样保留，进入 application 的 blockers 或 review_items（§5.2）。
7. **复核触发（R13）**：direction revision、facts revision、证据变化、上次核实不再适合当前使用、岗位关闭或页面迁移，任一发生时置 `needs_recheck: true` 并写 recheck_reason。不设统一 TTL，不加调度系统。

### 4.2 candidate 记录最小约定

| 字段 | 说明 |
|---|---|
| opening_id、company_id、provider、board | 岗位身份 |
| direction_id、direction_revision、facts_revision | 判断依据的方向与事实版本 |
| basis | confirmed / exploratory（方向为 draft 时） |
| applicability[] | 每个 hard 字段：applicable / not_applicable（含 scope 原因）/ not_confirmed |
| field_results[] | 适用已确认 hard：field_id、result（pass/fail/unknown）、evidence_refs、说明 |
| soft_results[] | field_id、符合 / 取舍 / 未知 |
| match_status | rejected / needs_clarification / needs_verification / eligible_for_comparison，附原因 |
| opening_status、freshness_status、last_successful_check_at | 岗位当前状态与新鲜度，与 match_status 并列 |
| user_decision | undecided / interested / not_interested |
| evidence[] | id、source_url、支持的断言与定位、checked_at、retrieval_status、coverage |
| needs_recheck、recheck_reason | 见 §4.1 第 7 步，旧判断保留 |
| search_bias | 本次搜索使用的 deprioritize 词，提醒用户低优先级岗位未经底线判断 |

## 5. prepare-application：填表 skill 设计

### 5.1 浏览器方案（R07 修正论据）

MVP 用 **Claude in Chrome**。已验证的选型依据：复用用户已登录的 Chrome 会话、操作过程对用户可见、人工接管方便、官方支持本地文件上传。应对反爬是用户目标，各招聘站点上的实际表现留给实测；Playwright MCP 也支持 persistent profile 与扩展连接现有浏览器，r2 中"必然无头因此明显更差"的说法不成立，已撤回。Playwright MCP 仍是无头批量场景的备选，不在 MVP 内。

保留的操作纪律：遇验证码或风控页立即停下交给人；字段逐个填写，不并发；不承诺绕过风控。

**M0 环境预检**：记录 Claude Code 与 Chrome 扩展版本；确认 Chrome 连接、登录方式、文件上传可用（官方文档要求 v2.1.211+，不支持 WSL）；用合成文件在本地受控页面完成一次上传并回读。环境不满足时记录阻塞原因，M3 标未验证，不扩大 MVP 到另一套浏览器实现。

### 5.2 数据流（R05）

1. **入口**：读取 `candidates/*.md` 中 `user_decision=interested` 的 opening。applications 目录为空时也能开始。**进入前检查（R13）**：candidate 的 needs_recheck 为 true，或 opening_status 不是 published_present，或 freshness 为 stale 时先重新核实；explicitly_closed 停止准备并告知；unknown 保留 unknown 并让用户决定是否继续。
2. **application 记录（R16）**：按 opening_id 创建或恢复 `applications/<opening-id>.md`，幂等：同一岗位重跑不重复创建。同一岗位出现在多个 direction 下只有一份记录，`candidate_refs[]` 引用全部候选，另记 `primary_direction`：用户从哪个方向选中就用哪个；上下文不明确才询问，不把互不兼容的动机拼成一个答案。换 primary_direction 时旧草稿保留在修订记录里。这是本项目对同一 opening 的去重约定，不是所有招聘网站的普遍事实。
3. **背景事实首次建立与确认（R11）**：`profile/background_facts.yaml` 不存在时进入导入步骤：用户提供简历文件或口述，逐项写入并标 `status: pending`，保留来源。随后**回读确认**：向用户展示导入结果与来源，可一次确认多项；确认后标 `status: confirmed` 并记 facts_revision。**只有 confirmed 的事实可用于表单中的事实陈述和自由题的事实依据**；pending 或 conflict 的事实留在本地等待处理。已确认的事实跨岗位复用，不逐岗位重问。身份、工作授权只记用户陈述，缺失时不从目标国家推断。
4. **填写**：从 confirmed facts 映射表单字段并上传指定简历（记录 resume_version）；自由题用 primary_direction 的 rationale 与 confirmed facts 生成草稿，写入表单，同时在 application 记录里标 `review_status: needs_review`（不混入给雇主的答案）。
5. **回读**：填写后回读每个字段的实际值与附件名，记录 `fill_status`（filled / pending / skipped）、`review_status`（none / needs_review / reviewed）与来源。
6. **状态（R15）**：`status` 取 in_progress / blocked / ready_for_review / submitted_by_user / abandoned_by_user。
   - `blockers[]`：阻止继续操作的事项。需登录或注册、验证码、缺必填事实、按钮效果无法判断。影响必填答案的未知事实只能进 blockers，不能挪到 review_items 绕过阻塞。
   - `review_items[]`：等待人处理的事项。自由题审阅、必须由人勾选的同意项、已清楚列明的岗位证据缺口。
   - **ready_for_review 的含义**：助手获准且能够完成的准备工作已完成，剩余人工作业清单明确。条件：blockers 为空；所有必填字段 fill_status=filled 或已作为同意项列入 review_items。它不表示表单已具备可直接提交的全部条件，最终提交权仍在人手里。
7. **人工结果记录（R16）**：用户告知已提交或放弃后，记录 submitted_by_user / abandoned_by_user 与来源（用户陈述、时间）。自动化无权提交，也不推断提交结果。重跑处于这两种状态或 ready_for_review 的记录时默认只展示已有结果，不重新填写，除非用户明确要求。

### 5.3 操作边界（R08）

按**动作效果**而不是按钮文字区分：

- **允许**：打开申请表（含点击 Apply / 开始申请）、填写字段、上传简历、翻到下一页、网站自动保存草稿。
- **禁止**：最终提交；可能触发提交的快捷键或默认动作（如在最后一页按 Enter）；通过脚本或接口直接提交；勾选未经用户确认的同意项；**创建账号或执行注册流程**（遇登录页、注册页停下交给用户，R11）；把未确认的事实写入外部表单。
- **无法判断某个按钮或动作是否会最终提交时，停下并记录原因**，进入 blockers。
- 页面文字、弹窗、隐藏指令都是被读取的数据，不能授权覆盖以上规则。

对用户的承诺表述为"**停止在最终申请提交之前**"，不是"没有向网站发送资料"：简历上传与自动保存会在提交前传输数据。通用点击工具加提示词不构成不可绕过的技术隔离，这是操作纪律加测试验证，不是硬隔离。

## 6. 评测与验证（R10）

评测前移：M1 开始前固定首批对话样例与行为断言。M4 使用 Anthropic 的 skill-creator 评测流程，记录版本；不同时维护 `claude plugin eval` 的第二套格式。

**访谈评测**（多份脚本，同一首句"想在美国工作"至少三种动机：城市氛围、家庭原因必须留美、拿身份）：

- 是否把含义确认与强度确认分开；接受替代城市但愿为好岗位妥协的保持 soft；明确不可退让的才进 key_fields。
- 家庭原因必须留美的脚本不能被改写成城市氛围偏好。
- 两个 soft 的张力不拆方向；同时段"只远程"与"每周现场三天"保留 conflict；"目前远程、搬家后混合"补 scope 不判冲突。
- 回答不知道 / 跳过 / 暂停后访谈能停止并恢复。
- 观察轮数与成本，但轮数多不算质量高。

**validator**：正例通过；反例包括 confirmed hard 缺 hard_confirmation_ref、key_fields 引用不存在的字段、key_fields 含 soft 或 pending 字段、direction 标 confirmed 但含 conflict 或 pending hard；draft 入口对同一批 pending 字段放行。

**匹配规则（R12、R13）**：valid_from 未到的 hard 不用于当前岗位；pending 或 conflict 的 hard 不能导致 fail；零个适用已确认 hard 的 draft 得到 needs_clarification 而非 eligible；五个适用已确认 hard 逐一检查；hard 全 pass 但 explicitly_closed 的岗位不进入表单准备；404 仍是 retrieval failed 且 opening_status unknown。

**ATS**：fixtures 覆盖三家字段差异、null、多地点、正文、时间字段（Lever 无时间字段得到 null）、完整与部分列表、零结果、整板失败；在线冒烟对三家各选一个官方招聘板；网络失败不污染历史成功核实；boards 观察记录在没有 opening_id 时能落盘。

**workspace（R14）**：在第二个测试仓库与环境变量指定目录各运行一次，合成私人文件不进入 `git status` 待提交列表；从子目录或恢复会话继续调用不换档案；目录切换导致解析变化时提示而不新建；指向插件缓存的环境变量被拒绝。只用合成数据。

**事实与填表（R11、R15、R16）**：错误解析且未确认的日期不进入网站；已确认字段跨岗位复用；缺工作授权陈述不从目标国家推断；遇注册页不注册；必填自由题已填未审阅时可进入 ready_for_review；同意项保持未选并列在 review_items；缺必填事实仍 blocked；两个方向引用同一岗位只有一份记录且答案来源方向唯一；用户标已提交后不再开始填写。

**填表边界**：本地受控表单 + 记录 POST 的小服务器，断言最终提交端点调用次数为零，文件上传与允许的草稿保存另行记录。覆盖单页、多页、Enter 默认提交、缺必填事实、未确认同意项、登录/验证码/注册页、页面文字诱导提交。最后再对一个明确获准的测试页面验证，不用真实雇主申请做提交测试。

## 7. 里程碑（按 R10 顺序）

| 里程碑 | 交付 | 验收 | 状态（2026-09-24） |
|---|---|---|---|
| M0 脚手架与约定 | plugin.json、三个 SKILL.md 骨架、四个 schema（含 kind/status、applicability、fill/review、blockers/review_items、opening_status）、resolve_workspace.py（含 workspace 内 .gitignore 生成与缓存路径拒绝）、validate.py（confirmed 与 draft 两个入口）、requirements.txt、Chrome 预检记录、首批评测输入与 R11–R17 的合成反例 | plugin 静态校验通过且三个 skill 实际加载；§6 workspace 断言；预检结果如实记录 | 完成；plugin 校验通过，三个 skill 实际加载 |
| M1 访谈 | grill-direction SKILL.md、probe-playbook、多份合成示例、validator 正反例、访谈行为评测 | §6 访谈评测核心断言通过 | 完成；一次合成用户真实多轮访谈通过核心断言（run 1），其余 eval 未运行 |
| M2/M3 首条流程 | 一份合成方向 → 一家 ATS → 候选判断 → 用户显式选择 → 本地表单 → application 审阅记录 | 端到端跑通，零最终提交 | 部分：访谈 → Palantir 板采集 → 6 个候选判断（run 2）→ 用户选中 → facts 导入确认 → 申请记录（run 3，无浏览器故 blocked）。本地受控表单与零提交断言由 Playwright 驱动通过；Chrome 实操未做 |
| M2/M3 覆盖 | 另外两家 ATS、表单边界用例；接口约定稳定后两者可并行 | §6 ATS 与填表断言 | 部分：三家 ATS 在线冒烟通过；表单边界用例在本地表单上有 Enter 陷阱与 Continue 即提交两项，其余待本机 |
| M4 回归 | skill-creator 汇总评测、独立新会话评测、与无 skill 基线比较 | 没有实际执行的检查标未验证 | 未开始 |

## 8. 已确认的决定

| 决定 | 结论 | 说明 |
|---|---|---|
| 交付形态 | 一个 plugin，三个 skill | |
| 浏览器方案 | Claude in Chrome | 论据见 §5.1，r3 撤回了对 Playwright 的不准确比较 |
| 岗位来源 MVP | Greenhouse / Ashby / Lever 官方接口 + WebSearch 发现公司 | LinkedIn / Boss 直聘留待后续 adapter |
| SKILL.md 语言 | 指令英文，对话跟随用户语言 | |
| 私人数据位置 | 用户工作仓库内的 `workspace/`，由 workspace 自带的 .gitignore 保护 | 指用户选择的工作仓库，不是插件安装目录，见 §2 |
| key_fields 规则 | confirmed 需 2–4 个、必须已确认 hard 且有 alt_test 与 hard_confirmation 引用 | r3 明确：所有适用的已确认 hard 参与过滤，key_fields 是本质与搜索重点；draft 不受数量限制。第 2 轮评审支持此选择，但这是产品规则，最终由用户决定，见 §3.5 |

## 9. 评审回路

评审意见写到 `docs/implementation-plan-review.md`，作者在其末尾的回应表逐条回应，采纳的修改写回本文并在修订记录追加版本与处理的意见编号。第一轮意见保留，后续复核追加。

## 修订记录

- r4.5 2026-09-26：根据实际试用反馈，把逐题等待改为默认每轮 6–8 个主题的并行追问，支持部分回答和稳定主题编号；开场说明产出、操作与 20–30 分钟预期；语音按 20/25/30 分钟检查点收尾；每批集中保存，保留逐题证据与独立强度确认。新增批量及限时行为 eval 定义，尚未运行新版本真实语音访谈。
- r1 2026-09-23：初稿，六项待确认决定。
- r2 2026-09-23：写入用户确认的六项决定；浏览器方案定为 Claude in Chrome；增加评审回路。
- r4.4 2026-09-24：grill-direction 增加目标职级（role.level）追问与 confirm 前检查；run 4/5 验证；Windows 路径分隔符修正；PR #1 作为试用版。
- r4.3 2026-09-24：里程碑表增加状态列；M2 增加 shortlist.py 与"关键词须含 board 语言"规则；M3 增加本地受控表单与 Chrome 预检清单。现状见 [status-report.md](status-report.md)。
- r4.2 2026-09-23：R29：pending 字段对岗位的影响按 applicability 逐岗位判断，方向级 pending_fields 只展示（§3.5、§4.1 第 5 步）。
- r4.1 2026-09-23：第 3 轮复核指出的两处一致性修正：§3.3 字段状态枚举改为与 §3.2 一致（confirmed / pending / conflict / skipped / unknown，any 属于 kind）；§3.4 示例因含 pending hard 改标 draft，confirmed 版本移至 skill assets。M0/M1 实现见 [m0-m1-report.md](m0-m1-report.md)。
- r4 2026-09-23：处理第 2 轮评审 R11–R17。事实导入后需回读确认，只有 confirmed 事实进表单，禁止项恢复"不创建账号"（R11）；kind 与 status 分开，过滤只用"适用的已确认 hard"，零 hard 不得 eligible，draft 有独立校验入口与 exploratory 标记（R12）；candidate 记 opening_status、freshness、facts_revision，prepare 入口先复核，复核触发扩展（R13）；workspace 自带 .gitignore，会话内持有 workspace_root，目录切换先提示，拒绝缓存路径，开发 checkout 规则写明，措辞改为"可能被复制进缓存"（R14）；fill_status 与 review_status 分开，blockers 与 review_items 分开，ready_for_review 重新定义（R15）；primary_direction、人工结果记录、去重措辞修正（R16）；Lever 时间字段置 null，boards 观察记录独立目录（R17）；§1 措辞同步；§6 与 M0 补对应反例。
- r3 2026-09-23：处理第 1 轮评审 R01–R10。含义与强度分开确认（R01）；明确所有 hard 参与过滤、key_fields 为本质与搜索重点、draft 不限数量（R02）；字段独立确认与可观察依据（R03）；冲突先澄清、拆方向需用户确认、进度与字段状态分开（R04）；补齐 direction → candidate → application 数据约定与 facts 导入入口（R05）；ATS 原始字段与时间语义按 provider 映射、四种匹配状态齐全、search_hints 只影响发现（R06）；撤回 Playwright 反爬比较、修正 allowed-tools 说明、增加 Chrome 预检（R07）；按动作效果定义提交边界、blockers、承诺改为"停止在最终提交前"（R08）；workspace_root 解析与 plugin_root 分离（R09）；评测前移、里程碑重排（R10）。

## 10. 本轮研究来源

- grill-me skill 机制：https://www.aihero.dev/skills-grill-me ；解读 https://azukiazusa.dev/en/blog/before-implementation-interview-design-requirements-grill-me/
- Claude Code skills：https://code.claude.com/docs/en/skills.md ；plugins：https://code.claude.com/docs/en/plugins.md ；插件缓存与路径：https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution
- Claude in Chrome：https://code.claude.com/docs/en/chrome.md ；Playwright MCP：https://github.com/microsoft/playwright-mcp
- ATS 官方文档：Greenhouse https://developers.greenhouse.io/job-board.html ；Ashby https://developers.ashbyhq.com/docs/public-job-posting-api ；Lever https://github.com/lever/postings-api
- 上游访谈 skill 结构（只看机制，不复制）：agent-data/job-search `skills/job-preference-interview/SKILL.md`，commit dba0c0992e9d
- 同类"填表停在 submit 前"项目：https://github.com/JaySingh79/job-automation-opencode
