# M0 / M1 实现报告（第 1 版）

日期：2026-09-23。对应方案 r4（[implementation-plan.md](implementation-plan.md)），处理了第 3 轮复核指出的两处不一致（§3.3 状态枚举、§3.4 示例 status）。本报告如实区分"已验证"、"已实现未验证"、"未实现"。

## 交付清单

| 路径 | 内容 | 里程碑 |
|---|---|---|
| `.claude-plugin/plugin.json` | plugin 清单，名称 `job-right` | M0 |
| `schema/direction.schema.json` | direction frontmatter：kind 与 status 分开、scope、引用字段、search_hints、interview_progress | M0 |
| `schema/candidate.schema.json` | applicability、field_results、match_status、opening_status、freshness、user_decision、evidence、search_bias | M0 |
| `schema/application.schema.json` | fill_status 与 review_status 分开、blockers 与 review_items 分开、primary_direction、user_outcome | M0 |
| `schema/background_facts.schema.json` | 事实条目 pending/confirmed/conflict、来源、documents | M0 |
| `scripts/resolve_workspace.py` | 解析顺序、缓存路径拒绝、开发 checkout 提示、workspace 自带 .gitignore、`--expect` 变化检测、`git check-ignore` 与已跟踪文件检查 | M0 |
| `scripts/validate.py` | 四类文件校验；direction 的 confirmed 与 draft 两个入口；candidate 的空 hard 陷阱、fail 必 rejected；application 的 ready_for_review 条件 | M0 |
| `requirements.txt` | pyyaml、jsonschema、pytest；Python ≥ 3.10 | M0 |
| `skills/grill-direction/SKILL.md` | 访谈 skill 指令（英文），105 行 | M1 |
| `skills/grill-direction/references/probe-playbook.md` | ladder 五步、对比情境、冲突流程、拆方向规则、维度清单、措辞、回读模板 | M1 |
| `skills/grill-direction/references/template-schema.md` | 字段人读说明、kind/status 组合表、confirmed 规则 | M1 |
| `skills/grill-direction/assets/direction.template.md` | 空模板 | M1 |
| `skills/grill-direction/assets/example-synthetic-city-profile.md` | 合成示例 A：同首句，动机为城市氛围，confirmed | M1 |
| `skills/grill-direction/assets/example-synthetic-family-us.md` | 合成示例 B：同首句，动机为家庭必须留美，draft（1 个 key_field、1 个 pending hard、1 个 skipped） | M1 |
| `skills/grill-direction/evals/evals.json` | 4 个行为评测用例（含 expectations），**未运行** | M1 |
| `skills/find-openings/SKILL.md` | M0 骨架：工作流契约与未完成项 | M0 |
| `skills/prepare-application/SKILL.md` | M0 骨架：动作边界、工作流契约、未完成项 | M0 |
| `tests/test_validate.py`、`tests/test_resolve_workspace.py` | 42 个用例 | M0 |

## 已验证

命令与结果（本容器，Python 3.11.15，PyYAML 6.0.1，jsonschema 4.26.0，pytest 9.1.1，Claude Code CLI 2.1.281）：

```
$ claude plugin validate .
√ Validation passed

$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-city-profile.md
ok
$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-family-us.md
ok
$ python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-family-us.md --mode confirmed
2 problem(s): key_fields must have 2-4 entries, got 1; hard field location.commute_to_family is still pending

$ python3 -m pytest tests -q
42 passed
```

测试覆盖的规则（每条对应方案或评审编号）：

| 规则 | 正例 | 反例 | 来源 |
|---|---|---|---|
| confirmed 方向含 pending hard 被拒；同文件标 draft 通过 | ✓ | ✓ | R02、R12 |
| key_fields 含 soft、数量 1 或 5、缺 alt_test_ref、缺 hard_confirmation_ref | | ✓ | R01、R02 |
| conflict 字段阻止 confirmed 且要求 conflicts_with | | ✓ | R04、R12 |
| 引用不存在于追问链、追问链 id 重复、缺 `## 修订记录` 节 | | ✓ | R01、R05 |
| skipped/unknown 不能是 hard；kind=any 的 status 约束；旧枚举值 `kind: unknown` 被 schema 拒绝 | | ✓ | R12、第 3 轮 |
| candidate：零个适用 hard 不得 eligible；fail 必 rejected；不适用字段不得有结果 | ✓ | ✓ | R12、R13 |
| application：已填但需审阅可进 ready_for_review；有 blockers 不可；必填未填且非同意项不可；submitted 需 user_outcome；primary_direction 必须被引用 | ✓ | ✓ | R15、R16 |
| facts：work_authorization 只能来自用户陈述；confirmed 需 confirmed_at | | ✓ | R11 |
| workspace：从子目录解析到同一 git 根；第二个仓库中私人文件不出现在 `git status`；环境变量目录同样受保护；相对路径拒绝；非 git 且无环境变量报错；插件缓存路径拒绝；`--expect` 不一致退出码 3；已被跟踪的私人文件报退出码 4；开发 checkout 允许并警告 | ✓ | ✓ | R09、R14 |

## 已实现但未验证

- **grill-direction 的真实访谈行为**。SKILL.md 与 playbook 已写，`evals/evals.json` 定义了 4 个用例（同首句两种动机、scope 与真实冲突、暂停恢复）并附 expectations，但没有用 skill-creator 流程实际运行过。validator 通过只证明示例文件结构正确，不证明模型按 playbook 提问。
- **skill 在 Claude Code 会话中的实际加载**。`claude plugin validate` 只校验清单；没有在实际会话里用 `--plugin-dir` 加载并调用 `/job-right:grill-direction`。
- **SKILL.md 中的脚本路径**。使用 `${CLAUDE_SKILL_DIR}/../../scripts/...`，在仓库布局下正确；插件安装后的解析未实测（`${CLAUDE_PLUGIN_ROOT}` 可能更稳，待加载测试后决定）。
- **date-time 格式检查**。jsonschema 的 FormatChecker 在缺少 rfc3339-validator 时静默跳过格式校验；本容器未安装该包，因此时间戳只保证是字符串，不保证合法 RFC 3339。

## 未实现

- Chrome 环境预检（版本、连接、上传回读）。本容器无浏览器扩展环境，无法执行；必须在用户本机做。
- `scripts/ats_fetch.py` 与三家 ATS fixtures（M2）。
- `skills/find-openings/references/evidence-rules.md`、`skills/prepare-application/references/form-rules.md`、`fixtures/local-form/`（M2/M3）。
- M2/M3 首条端到端流程。

## 对 Codex 下一轮评审的建议关注点

1. `schema/direction.schema.json` 与 `template-schema.md` 的 kind/status 组合表是否与方案 §3.2 完全一致。
2. `validate.py` 的 candidate 规则现在检查 fail→rejected、unknown→不得 eligible、全 pass→不应 needs_verification；是否还有漏掉的状态组合。
3. `resolve_workspace.py` 的缓存路径判定只看路径中是否出现 `.claude/plugins`，自定义安装位置会漏判；是否需要额外读 plugin.json 位置。
4. SKILL.md 是否过度依赖示例（评审 R10 的担忧），特别是 "Things that go wrong" 一节。
5. evals.json 的 expectations 是否可由 grader 客观判定。
