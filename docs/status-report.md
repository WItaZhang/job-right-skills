# 状态报告（2026-09-24）

一句话：**三段都实现了；前两段各有一次真实端到端运行记录；第三段除浏览器实操外全部验证，浏览器实操只能在用户本机做，清单已给。**

分支 `claude/implementation-plan`，尚未合入 main。测试 103 个全部通过（`python3 -m pytest tests -q`）。所有运行记录使用合成人物，仓库中没有任何真实个人资料。

## 用户最初要的三件事

| 要求 | 现在能做什么 | 证据 | 还差什么 |
|---|---|---|---|
| 深挖访谈，把真实意图落成 template，只标少数关键字段 | 装上 plugin 后 `/job-right:grill-direction <一句话>`：层层追问，替代方案测含义，单独一问测强度，落成带追问链与修订记录的 direction 文件；含义与强度分开，跳过/不知道/暂停/恢复都能处理 | [run 1](live-runs/run-1/)：16 个用户回合、两个会话，"想去美国"被追到"城市氛围 soft + 底层系统 hard + IC hard"，暂停后新会话从文件恢复 | 只跑过一次；另外四个 eval 场景（家庭动机、未证实张力、真冲突、暂停恢复脚本）只有定义未运行 |
| 用 template 找岗位并解释依据 | `/job-right:find-openings dir-001`：官网确认招聘板 → `ats_fetch.py` 拉全部岗位并留证据 → `shortlist.py` 排序 → 逐个 hard 字段 pass/fail/unknown 带引用 → 四组状态 → 用户自己标 interested | [run 2](live-runs/run-2/)：Palantir Lever 板 318 条完整读取，shortlist 8、判断 6，全部 needs_verification（JD 不谈是否带人，IC 字段保持 unknown 而不是凭标题猜）；ATS 在线冒烟三家 [ats-smoke-1](live-runs/ats-smoke-1/) | 只对一家公司跑过；公司发现（WebSearch）步骤这次由用户直接给了公司名，没有测 |
| 填申请表，停在提交前 | `/job-right:prepare-application <opening-id>`：复核岗位状态 → 一岗位一份记录 → 从简历导入事实、回读让用户批量确认、只有确认过的事实可进表单、工作授权只记用户陈述 → 按动作效果分类操作 → 回读 → blockers 与 review_items 分开 | [run 3](live-runs/run-3/)：无浏览器会话下正确停在 blocked，事实导入 9 条并确认，发现"授权只覆盖新加坡而岗位在纽约"并列为审阅项；本地三页受控表单 + 记录 POST 的服务器，Playwright 按规则填写后 `final_submits=0`，Enter 陷阱确认真的会提交 | **真实 Chrome 填表未做**。需要你本机按 [chrome-precheck.md](chrome-precheck.md) 跑一次 |

## 交付物一览

```text
.claude-plugin/plugin.json                 plugin: job-right（claude plugin validate 通过；三个 skill 在会话中列出）
skills/grill-direction/                    SKILL.md + probe-playbook + template-schema + 模板 + 两份合成示例 + 5 个 eval
skills/find-openings/                      SKILL.md + evidence-rules + ats_fetch.py + shortlist.py + 三家 fixtures
skills/prepare-application/                SKILL.md + form-rules + fixtures/local-form（index.html + server.py）
schema/                                    direction / candidate / application / background_facts
scripts/resolve_workspace.py               私人 workspace 解析、自带 .gitignore、不写文件的忽略验证
scripts/validate.py                        四类文件校验，含 confirmed/draft、状态重算、重复键拒绝、围栏识别
tests/                                     103 个用例（validate 61、workspace 22、ats 14、local-form 6）
docs/implementation-plan.md                方案 r4.3；implementation-plan-review.md 五轮评审 R01–R30 全部回应
docs/live-runs/                            run-1 访谈、run-2 找岗位、run-3 填表记录、ats-smoke-1
docs/chrome-precheck.md                    用户本机预检清单
```

## 已验证（本容器，Linux，Python 3.11，Claude Code CLI 2.1.281）

- `claude plugin validate .` 通过；`claude --plugin-dir . -p` 列出三个 skill；三个 skill 各在真实会话中被调用并完成工作流（run 1/2/3）。
- 103 个测试通过，覆盖 R01–R30 每条评审意见的正反例、ATS 三家 fixtures、本地表单零提交断言与 Enter 陷阱。
- ATS 在线只读：Stripe（Greenhouse）694 条、OpenAI（Ashby）825 条、Palantir（Lever）318 条四页翻页，全部 success。
- 评审人 Codex 在 Windows 中文路径环境复跑过 68 个测试版本，全部通过；之后新增的 35 个用例未在 Windows 复跑。

## 已实现但未验证

- **Chrome 实操**：连接、上传、在真实申请页按动作效果停下。容器无扩展，无法做。
- 访谈的稳定性：只有 run 1 一次；SKILL.md 之后改了三处（回读节奏、替代测试不能引用用户自述、一条消息一个问题、关键词须含英文），改后没有再跑。
- find-openings 的公司发现步骤（WebSearch → 官网 → 招聘板）中"发现"一环。
- Windows 上的新增测试。
- 时间戳格式：容器缺 rfc3339-validator，只保证是字符串。

## 运行中发现并已修的问题（在评审之外）

| 来源 | 问题 | 处理 |
|---|---|---|
| run 1 | 模型把用户自述"tech lead 可以"当作替代测试引用 | validator 拒绝 alt_test_ref 等于 source_ref；SKILL.md 加规则 |
| run 1 | 第一次回读滑到第 10 回合 | SKILL.md 改为可数触发 |
| run 1 → run 2 | 访谈写的关键词全是中文，英文招聘板一个都匹配不上 | shortlist.py 加 `--extra-keyword` 并记录；grill-direction 要求双语关键词 |
| 冒烟 | Greenhouse 正文是实体转义 HTML，去标签顺序错 | 先反转义再去标签，fixture 按真实格式改写 |
| 冒烟 | 同秒两次检查 check-id 碰撞会覆盖证据 | 微秒时间戳 + 存在即加后缀 |
| shortlist | 正文里提到 "Head of Infra" 就把 IC 岗压下去 | 压下只看标题/团队/部门；正文命中只扣分 |
| shortlist | 负分的被压下岗位不显示，透明性不足 | 被压下列表不受分数门限 |
| run 2 | 候选全是 Internship / New Grad | 访谈没有问资历维度；记入待办，不改规则 |

## 待办（不阻塞，按价值排序）

1. 你本机跑 chrome-precheck，把结果放进 `docs/live-runs/chrome-precheck/`。这是把第三段从"未验证"改为"已验证"的唯一路径。
2. grill-direction 加一个资历/年限相关的追问（run 2 的候选全是实习与校招，因为方向里没有这条）。
3. 再跑一次访谈（改后的 SKILL.md）和另外四个 eval 场景，用 skill-creator 流程出 benchmark（M4）。
4. find-openings 的公司发现步骤单独测一次（不给公司名，只给方向）。
5. 大板体积（OpenAI 板 13 MB）：只对用户选中的公司留全量原始页，或压缩。
6. `validate.py workspace` 跨文件校验入口（candidate → direction revision、application → facts confirmed）。
7. Codex 第 6 轮评审。

## 合并建议

分支可以合入 main 了：功能完整、测试齐、私人资料不入库、每处未验证都有标注。合并前如果你希望我开 PR，说一声。
