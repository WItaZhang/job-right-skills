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
