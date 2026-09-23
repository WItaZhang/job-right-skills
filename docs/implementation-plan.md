# job-right-skills 实现方案（待确认）

日期：2026-09-23。本文是从 reference 阶段进入实现阶段的方案草案，尚未写任何 skill 代码。确认后按"里程碑"逐步实现。

## 1. 目标回顾

两段式求职 agent：

1. **深挖访谈（grill）**：不问表面问题，层层追问到本质，把用户真实意图落成若干份固定格式的 **direction template**，一个文件 = 一个求职方向。每份 template 只有少数几个字段是真正关键的（key_fields），其余字段是软偏好、无所谓或未知。
2. **找岗位 + 填申请（apply）**：用 template 去找岗位、打开申请页、从个人档案填表、上传简历，**停在提交前**，由人点 submit。

设计约束沿用 reference/design 的结论：事实与意愿分开；hard / soft / unknown 三态；每条判断可追溯到 preference_id 与 evidence_id；未披露不等于失败；模型不替用户做投递决定。

## 2. 交付形态：一个 plugin，三个 skill

```text
job-right-skills/
  .claude-plugin/plugin.json          # plugin 元数据，skill 以 /job-right:<name> 调用
  skills/
    grill-direction/                  # 访谈 → 产出 direction template
      SKILL.md
      references/probe-playbook.md    # 追问算子、维度清单、停止条件
      references/template-schema.md   # template 字段定义
      assets/direction.template.md    # 空白模板
      assets/example-synthetic.md     # 合成示例（非真实用户）
    find-openings/                    # 读 template → 公司 → 岗位候选
      SKILL.md
      scripts/ats_fetch.py            # Greenhouse / Ashby / Lever 公开接口拉取与字段归一
      references/evidence-rules.md    # 引用 reference/design/research-evidence.md 的落地版
    prepare-application/              # 打开申请页、填表、上传简历、停在 submit 前
      SKILL.md
      references/form-rules.md        # 禁止事项、字段映射、停止规则
  schema/
    direction.schema.json             # template frontmatter 的 JSON Schema，用于校验
    background_facts.schema.json      # 个人事实档案
  workspace/                          # 运行时数据目录（默认 gitignore）
    profile/background_facts.yaml     # 履历事实（私有）
    directions/*.md                   # 每个方向一份 template
    candidates/<direction-id>.md      # 该方向的岗位候选与证据
    applications/<opening-id>.md      # 填表记录，状态止于 ready_for_review
  reference/                          # 现有研究笔记，不动
  docs/implementation-plan.md         # 本文
```

选 plugin 而不是单个 skill 的原因：三段职责不同、工具权限不同（访谈不需要网络，填表需要浏览器），分开后可以各自限定 allowed-tools，也方便单独 eval。

## 3. grill-direction：访谈 skill 设计

### 3.1 借鉴什么

- **grill-me（Matt Pocock）**：按"轮"提问，每轮问完当前 frontier（前置已答完的所有问题），frontier 为空即结束；用户拥有 scope。我们借它的轮次与停止条件，但**不照搬无状态**：我们必须落盘。
- **agent-data/job-search 的访谈 skill**：11 个维度、跳过无关维度、每 4–5 轮回读确认。我们借"回读确认"，不借 prose brief 和 must-have 缺失即拒绝。
- **example-critiquing 论文**：用 2–3 个合成情境让用户说出愿意牺牲什么。这是"替代方案测试"的依据。

### 3.2 核心机制：why-ladder + 替代方案测试

每条用户表述都走同一条追问链：

| 步骤 | 做什么 | 例子 |
|---|---|---|
| stated | 记下原话 | "想在美国工作" |
| why | 问这个选择给你带来什么 | "美国哪里吸引你？" → "年轻人多、tech 聚集" |
| attribute | 把回答抽象成可观察属性 | city_profile = 年轻科技聚集城市 |
| alt_test | 用满足同一属性的其他选项测试 | "深圳、新加坡这类城市可以吗？" |
| resolve | 根据回答决定字段值与强度 | 可以 → 城市字段变成属性集合，kind=hard；不可以 → 追问差异（身份？语言？薪资？），可能拆出新字段 |

规则：

- 一次只推进一个 ladder，但一轮可以并行开多个 ladder（frontier）。
- 每个 key_field 至少经过一次 alt_test 才能标 confirmed；没做过 alt_test 的字段最多是 draft。
- 追问发现用户其实有两条互不兼容的动机（如"硅谷式城市"与"拿美国身份"），**拆成两份 template**，不硬塞进一份。
- 允许"无偏好 / 跳过 / 暂不知道"三种回答，分别写成 any / skipped / unknown，不互换。
- 每 4–5 轮回读一次当前 template 草稿，让用户纠正。
- 停止条件：每份 template 的 key_fields 都 confirmed，其余字段至少标了 soft/any/unknown，且 frontier 为空。

### 3.3 访谈维度（frontier 的来源）

沿用 reference/design/preference-profile.md 的 8 个维度：兴趣动力、人生方向、压力承受、风险容忍、角色与成长、地点与时间、薪酬与身份、团队环境。skill 不按顺序问遍，而是从用户第一句话出发展开 ladder，只在 frontier 为空但仍有维度完全 unknown 时才主动开一个新维度。

### 3.4 产出：direction template

Markdown 文件，YAML frontmatter 是结构化部分，正文是追问链与备注。frontmatter 示意（合成例子）：

```yaml
id: dir-001
title: 年轻科技聚集城市里的中型 AI infra 公司，做 IC
revision: 2
status: confirmed          # draft | confirmed
created_at: 2026-09-23T10:00:00+08:00
key_fields: [location, role_nature, company_stage]   # 真正关键的 2–4 个
fields:
  location:
    value: {city_profile: tech_hub_young, examples: [深圳, 新加坡, 旧金山湾区], remote: hybrid_ok}
    kind: hard             # hard | soft | any | unknown | skipped
    alt_tested: true
    rationale: "要的是年轻科技聚集的氛围，不是美国本身"
  role_nature:
    value: IC
    kind: hard
    alt_tested: true
  company_stage:
    value: {size: "50-500", stage: [series_b, series_c, growth]}
    kind: hard
    alt_tested: true
  industry:
    value: [AI infra, developer tools]
    kind: soft
  company_style:
    value: {pace: fast, process: light}
    kind: soft
  compensation:
    value: null
    kind: unknown
search_hints:
  keywords: [infrastructure engineer, platform engineer, ML infra]
  exclude: [manager, lead]
open_questions:
  - "薪酬底线口径未定（币种、base/total）"
```

正文部分固定两节：`## 追问链`（每条 ladder 的 stated / why / attribute / alt_test / resolve）和 `## 修订记录`（revision、改了什么、为什么）。旧值不覆盖，只追加。

`schema/direction.schema.json` 用来校验 frontmatter；key_fields 必须是 fields 里 kind=hard 且 alt_tested=true 的字段，数量 2–4。

## 4. find-openings：找岗位 skill 设计

输入：一份 direction template（或多份）+ background_facts。输出：`workspace/candidates/<direction-id>.md`，每个候选带公司→团队→岗位三层证据、hard 字段 pass/fail/unknown、软字段取舍。

流程：

1. **公司发现**：先用 template 的 key_fields 与 search_hints 做 WebSearch，列出候选公司；用户也可以直接给公司名单。公司被发现不等于被选中。
2. **岗位拉取**：对每家公司，先从官网确认其招聘板（Greenhouse / Ashby / Lever 之一），再用 `scripts/ats_fetch.py` 拉取当前已发布岗位，归一成统一字段（provider、posting_id、title、department、team、location、workplace_type、source_updated_at、url、checked_at）。找不到官方 ATS 的公司记 unknown，不猜 board slug。
3. **匹配判断**：只对 key_fields 做 hard 判断（pass/fail/unknown），软字段列取舍；结果四选一：rejected / needs_clarification / needs_verification / eligible_for_comparison。
4. **输出**：candidates 文件按 eligible → needs_verification → rejected 分组，每条带 evidence 与 checked_at；用户在文件里标 user_decision（interested / not_interested）。

MVP 只做官方 ATS 三家 + WebSearch 公司发现。LinkedIn、Boss 直聘等没有公开接口的来源留到 prepare-application 的浏览器阶段处理，或者后续再加 adapter。

## 5. prepare-application：填表 skill 设计

### 5.1 浏览器方案

| 方案 | 能否用用户已登录的浏览器 | 文件上传 | 配置 | 结论 |
|---|---|---|---|---|
| Claude in Chrome | 是，共享 Chrome 登录态 | 支持（读本地文件上传） | `claude --chrome` 或 `/chrome enable` | **推荐** |
| Playwright MCP | 需要另配 persistent profile | 需要走 MCP 文件参数，较绕 | `.mcp.json` | 备选，适合无头批量 |
| computer-use（macOS） | 是 | 通过系统对话框 | `/mcp` 里启用，需 Pro/Max | 过重，不选 |

推荐 Claude in Chrome：申请页多数需要登录（LinkedIn Easy Apply、Workday 账号），共享登录态最省事；文件上传已支持；停在 submit 前只是 skill 指令层的事。

### 5.2 流程与硬规则

1. 读取 `applications/` 里状态为 interested 的 opening，打开其申请 URL。
2. 从 `background_facts.yaml` 映射到表单字段（姓名、联系方式、经历、教育、链接、工作授权陈述），上传指定简历文件。
3. 对每个自由填写题（如"为什么想加入"），用 template 的 rationale 与 background_facts 生成草稿，**写入表单但标记为需人工审阅**。
4. 把每个字段的填写值与来源写入 `applications/<opening-id>.md`，状态置为 `ready_for_review`。
5. **停止**：不点 submit / apply / send，不创建账号，不勾选未经用户确认的同意项，不填 template 或 background_facts 里没有的事实（如未提供的身份状态）。遇到验证码或登录页停下来交给人。

## 6. 里程碑

| 里程碑 | 交付 | 验收 |
|---|---|---|
| M0 脚手架 | plugin.json、三个 skill 骨架、schema、.gitignore（workspace/ 私有）、README 更新 | `claude plugin` 能加载，三个 skill 可列出 |
| M1 访谈 | grill-direction 完整 SKILL.md + probe-playbook + 合成示例 + schema 校验脚本 | 用 reference/design 里的 8 个人工验收例子跑一遍；"美国 → 深圳/新加坡"例子能产出正确 template；冲突不静默覆盖 |
| M2 找岗位 | ats_fetch.py（三家 ATS）+ find-openings SKILL.md | 对 2–3 家公开公司拉取成功；缺字段保留 unknown；读取失败不写成 closed |
| M3 填表 | prepare-application SKILL.md + Chrome 流程 | 在一个测试岗位页上填完并停在 submit 前；applications 记录完整 |
| M4 评测 | 用 skill-creator 给 grill-direction 建 eval 集 | 追问深度、alt_test 覆盖率、是否擅自升级 hard |

M1 是核心，先做。M2 与 M3 互相独立，可以并行。

## 7. 已确认的决定（2026-09-23）

| 决定 | 结论 | 说明 |
|---|---|---|
| 交付形态 | 一个 plugin，三个 skill | M1 先做访谈 |
| 浏览器方案 | Claude in Chrome | 用户的选择标准是"更能应对反爬"。Chrome 方案驱动用户自己已登录的真实 Chrome，带真实指纹与已有 cookie，按人类节奏操作；Playwright MCP 启动的是自动化控制的浏览器实例，LinkedIn / Workday / Cloudflare 类站点会通过 navigator.webdriver 与无头特征识别并拦截。form-rules 补两条：遇验证码或风控页立即停下交给人；字段逐个填写，不做并发。Playwright MCP 只作无头批量的备选，不在 MVP 内 |
| 岗位来源 MVP | 仅 Greenhouse / Ashby / Lever 官方接口 + WebSearch 发现公司 | LinkedIn / Boss 直聘留待后续 adapter |
| SKILL.md 语言 | 指令英文，对话跟随用户语言 | reference 文件可中英混用 |
| 私人数据位置 | 仓库内 `workspace/`，gitignore | 未反对，按推荐执行 |
| key_fields 规则 | 2–4 个，必须 kind=hard 且 alt_tested=true | 未反对，按推荐执行 |

## 7.1 评审回路

本文件供其他 agent 或人评审。评审意见写到 `docs/implementation-plan-review.md`（同一分支 `claude/implementation-plan`），格式不限，建议每条意见标出针对的章节号与"建议改成什么"。作者读取该文件后修订本文并在 `## 修订记录` 追加一条。

## 修订记录

- r1 2026-09-23：初稿，六项待确认决定。
- r2 2026-09-23：写入用户确认的六项决定；浏览器方案按反爬标准定为 Claude in Chrome；增加评审回路。

## 8. 本轮研究来源

- grill-me skill 机制：https://www.aihero.dev/skills-grill-me ；解读文章 https://azukiazusa.dev/en/blog/before-implementation-interview-design-requirements-grill-me/
- Claude Code skills 规范：https://code.claude.com/docs/en/skills.md ；plugins：https://code.claude.com/docs/en/plugins.md
- Claude in Chrome：https://code.claude.com/docs/en/chrome.md ；computer use：https://code.claude.com/docs/en/computer-use.md
- 上游访谈 skill 结构（只看机制，不复制）：agent-data/job-search `skills/job-preference-interview/SKILL.md`，commit dba0c0992e9d
- 同类"填表停在 submit 前"项目：https://github.com/JaySingh79/job-automation-opencode （portal 子 agent、人工提交、不建账号）
