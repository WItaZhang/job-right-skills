# M0 / M1 实现报告（第 2 版）

日期：2026-09-23。对应方案 r4.1。第 2 版处理了 Codex 对 d9f064a 的实现评审 R18–R27（全部采纳），逐条回应见 [评审文件](implementation-plan-review.md) 的"M0/M1 作者回应表"。本报告如实区分"已验证"、"已实现未验证"、"未实现"。

## 本轮修复摘要

| 编号 | 修复 | 验证 |
|---|---|---|
| R18 | 两个骨架 SKILL.md 的 description 改为 `>-` 折叠块 | 三个 frontmatter 用 PyYAML 独立解析通过；`claude plugin validate .` 通过；**实际会话加载三个 skill 均列出**（见下） |
| R19 | 所有 git 子进程显式 `encoding="utf-8"`，`LC_ALL` 缺省 C.UTF-8，`core.quotepath=off`，stdout 重配置为 UTF-8；`git_root()` 对空输出返回 None | 新增中文路径仓库测试（`中文仓库 项目/子目录`，子进程 `LANG=C LC_ALL=C`），解析、初始化、忽略验证通过 |
| R20 | 已有 .gitignore 缺保护块时追加带标记的块；验证改为探测全部六个私有子目录 + 嵌套 README 探针 + 所有既有私人文件；已跟踪白名单只放行 workspace 根下确切的 README.md 与 .gitignore | 新增测试：旧 ignore 只保护 profile/ 被补齐；带标记但规则弱的 ignore 报退出码 4；嵌套已跟踪 README 报退出码 4；六类私人文件均不出现在 `git status` |
| R21 | candidate 校验重写：applicability 与 field_results 内 field_id 重复即拒；每个 applicable 字段必须有且仅有一个结果；按方案顺序重算期望状态（fail → rejected；not_confirmed 或 pending_fields 或零适用 → needs_clarification；unknown → needs_verification；否则 eligible），与记录不符即拒 | 评审四个反例各有测试；另有"只有 pass 却标 rejected"与"fail 优先于待澄清"两个方向的测试 |
| R22 | "kind=hard 且 status=confirmed 必须有 hard_confirmation_ref"以及 key_fields 逐项资格检查移到所有模式；confirmed 模式只保留数量与"不得有 pending hard / conflict" | 新增测试：draft 中冒充已确认但缺引用的 hard 被拒；draft 中 pending hard 可保存；draft 中 key_fields 指向 soft 被拒。template-schema.md 与方案 §3.5 同步改写 |
| R23 | 开发例外收窄：仅当目标恰为 plugin_root/workspace、plugin_root 本身是 git 工作树顶层、且路径不含 `plugins/cache`、`plugins/marketplaces`、`.claude/plugins` 段时允许；plugin 内其他任何路径拒绝 | 新增测试：自定义缓存根（无 `.claude`）拒绝；非 git 的插件副本拒绝；`skills/.../assets/private-runtime` 拒绝；真实开发 checkout 的 workspace/ 允许并警告 |
| R24 | 追问链 id 只从 `## 追问链` 节内收集，先剥离代码围栏 | 新增测试：id 只在修订记录中、id 只在代码块中，均被拒 |
| R25 | candidate：evidence id 唯一，evidence_refs 必须能在同一候选的 evidence 中解析，pass/fail 至少一条引用；application：filled 字段必须有 value_readback 与 source，fact/document/direction_rationale 来源必须带 ref；facts：F-id 与 document id 唯一 | 三类各有反例测试 |
| R26 | YAML loader 拒绝重复 mapping key（含嵌套），报行号 | 新增测试：顶层重复 status、嵌套重复 value、facts 重复键，均为单条 parse 错误 |
| R27 | eval 3 改为"规模 hard 保留、股权含义 pending 追问、不宣布冲突、不拆"；新增 eval 5 真冲突（同范围已确认的到岗与不到岗）；note 中写明 transcript 评测无法覆盖 frontier/回读/暂停恢复，需至少一次真实多轮会话 | 未运行 |

## 已验证

环境：本容器，Linux，Python 3.11.15，PyYAML 6.0.1，jsonschema 4.26.0，pytest 9.1.1，Claude Code CLI 2.1.281。

```
$ claude plugin validate .
√ Validation passed

$ claude --plugin-dir . -p 'List the names of every skill available to you whose name starts with "job-right:" ...' --max-turns 1
job-right:find-openings
job-right:grill-direction
job-right:prepare-application

$ python3 -m pytest tests -q
68 passed in 2.19s

$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-city-profile.md   → ok
$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-family-us.md      → ok
$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-family-us.md --mode confirmed
  → 2 problem(s): key_fields must have 2-4 entries, got 1; hard field location.commute_to_family is still pending
```

注意：本容器的 CLI 2.1.281 在修复前也报 `Validation passed`，而评审人的 2.1.126 报 frontmatter 解析失败；两版对 skill frontmatter 的校验严格度不同。修复以 PyYAML 独立解析为准，请评审人在其 CLI 上复跑一次。

测试覆盖（68 例）按规则分组：

| 组 | 用例数 | 来源 |
|---|---|---|
| direction 正例与 CLI | 4 | |
| direction confirmed-only 规则 | 4 | §3.5、R02、R12 |
| direction 全模式规则（key_fields 资格、confirmed hard 引用、draft 保留 pending） | 5 | R01、R22 |
| direction 引用完整性（不存在、只在修订记录、只在代码块、重复、缺节、key 非字段） | 6 | R01、R24 |
| direction kind/status 语义与旧枚举 | 4 | R12 |
| YAML 重复键 | 3 | R26 |
| candidate（含 R21 四反例与两个反向、R25 证据关联） | 13 | R12、R13、R21、R25 |
| application（含 R25 来源与回读） | 7 | R15、R16、R25 |
| facts | 4 | R11、R25 |
| workspace 解析（子目录、中文路径、环境变量、相对路径、非 git、--expect） | 7 | R09、R14、R19 |
| workspace 保护（第二仓库六类文件、弱 ignore 补齐、弱 ignore 报错、嵌套 README 已跟踪、私人文件已跟踪） | 5 | R14、R20 |
| 插件目录边界（缓存路径、自定义缓存根、非 git 副本、assets 路径、开发 checkout、启发式单元） | 6 | R09、R23 |

## 已实现但未验证

- **grill-direction 的真实访谈行为**。五个 eval 用例已修正（R27），仍未运行；transcript 型评测也不覆盖 frontier、定期回读与暂停恢复，需要至少一次带脚本化用户角色的真实多轮会话。
- **skill 被实际调用并执行工作流**。本轮只验证了三个 skill 在会话中被列出，没有调用 `/job-right:grill-direction` 跑完一次访谈。
- **Windows 本机**。R19 的修复在 Linux 容器里用 `LANG=C` 子进程复现了非 UTF-8 区域设置，但没有在 Windows GBK 控制台实测；请评审人在原环境复跑 `python -m pytest tests -q`。
- **SKILL.md 中的脚本路径** `${CLAUDE_SKILL_DIR}/../../scripts/...` 在插件安装后的解析未实测。
- **date-time 格式**：容器缺 rfc3339-validator，时间戳只保证是字符串。

## 未实现

- Chrome 环境预检（需用户本机）。
- `scripts/ats_fetch.py` 与三家 ATS fixtures（M2）。
- `find-openings/references/evidence-rules.md`、`prepare-application/references/form-rules.md`、`fixtures/local-form/`（M2/M3）。
- M2/M3 首条端到端流程。
- R25 提到的跨文件校验入口（candidate 引用的 direction revision 是否存在、application 引用的 facts 是否 confirmed）：单文件校验不覆盖，留给 M3 消费入口或后续 `validate.py workspace` 子命令。

## 对下一轮评审的建议关注点

1. `candidate_rules` 的期望状态计算把 `pending_fields` 非空一律视为待澄清，即使该 pending 字段与本岗位无关；是否过严。
2. `verify_ignore` 会在 workspace 内临时写探针文件再删除；在只读或受同步软件监控的目录里是否合适。
3. R23 的开发例外要求 plugin_root 是 git 顶层；用 git worktree 或 submodule 方式开发时可能误拒。
4. 重复键拒绝对用户手工编辑的容忍度：报错只给行号，是否需要更友好的修复提示。

---

# 第 3 版补充：M1 真实多轮访谈（run 1）

日期：2026-09-23。按 Codex 建议，在修复 R28/R30 后用合成用户在隔离 workspace（`JOB_RIGHT_WORKSPACE=/tmp/jr-live-1`，仓库外）实际调用 `/job-right:grill-direction`。驱动方式：`claude -p --plugin-dir . --session-id/--resume`，每个用户回合一次调用；合成用户的回答由作者按预设人物卡给出。完整对话与最终文件见 [docs/live-runs/run-1/](live-runs/run-1/)。

**人物卡（合成）**：首句"想去美国做 AI"；真实动机是年轻科技城市氛围但**愿为好内容妥协**（应落 soft）；真正底线是底层系统方向与 IC；公司规模选择"跳过"；薪酬"不知道"；第 13 回合暂停，之后在**新会话**中恢复。

| 检查项 | 结果 | 证据 |
|---|---|---|
| 不把偏好擅自升级为硬条件 | **通过** | 城市氛围在第 5 回合用 A/B 对比情境测强度，用户说"看情况"，落 `kind: soft`；最终文件中仍为 soft |
| 替代方案测试改变了字段含义 | **通过** | 第 7 回合主动用"数据库内核、分布式存储"测"AI 是否必须"，用户接受后 `role.domain` 写成"底层系统/性能规模化"，AI 降为 example |
| 硬条件有独立强度确认 | **通过** | `role.domain` hard_confirmation_ref=I-009（第 9 回合"会直接拒绝"）；`role.people_management` hard_confirmation_ref=I-012 |
| 追问到底而不是接受结论 | **通过** | 第 2 回合把"机会多"识别为结论继续追；第 10 回合把"应用层内容"与"业务拉扯"拆成两个字段分别确认 |
| 定期回读 | **部分通过** | 第 10 回合才第一次回读，晚于 SKILL.md 的 4–5 轮；回读内容准确并被用户确认 |
| 跳过 / 不知道 分别记录且不重问 | **通过** | company.size status=skipped，compensation.floor status=unknown；恢复后未重问 |
| 暂停保存草稿 | **通过** | 第 13 回合保存 draft、运行 validator、报告状态与下一问 |
| 新会话从文件恢复 | **通过** | 第 14 回合新 session 读取 dir-001.md，直接问上次未答的 workplace_type 问题 |
| 确认前运行 validator | **通过** | 第 16 回合确认前运行 validate.py，两个 key_fields 均有 alt_test 与 hard_confirmation 引用 |
| 一条消息一个问题 | **一处违反** | 第 6 回合把"什么吸引你"与"应用层为什么不行"合在一条消息 |
| alt_test 是访谈者提供的替代项 | **一处违反** | `role.people_management.alt_test_ref=I-011` 与 source_ref 相同：用户自己说了"tech lead 可以"，模型把它当作替代测试而没有自己再问一次 |

成本：两个会话累计约 1.6 美元（session 1 约 1.21，session 2 约 0.44），用户回合 16 次。

**据此做的三处修改**（本次提交）：

1. validator 新增规则：`alt_test_ref` 或 `hard_confirmation_ref` 与 `source_ref` 相同即拒。用它回验 run 1 的最终文件，正确报出 `role.people_management` 那一处；文件保留原样作为证据。
2. SKILL.md §3 把回读节奏改为可数的触发条件（第 4 或第 5 个问题前先回读），并注明本次实测滑到第 10 回合。
3. SKILL.md "Things that go wrong" 新增两条：不能把用户自述当作替代测试；不要把两个问题合在一条消息。

**判断**：M1 的核心语义断言（不升级 hard、含义与强度分开、跳过/未知/暂停/恢复）在这一次真实运行中成立，可以进入 M2。仍未验证的：其他四个 eval 场景（同首句家庭动机、scope 与未证实张力、真冲突）只有定义没有运行；一次运行不能说明稳定性；修改后的 SKILL.md 没有再跑第二次。
