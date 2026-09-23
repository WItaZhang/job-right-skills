# job-right-skills

以个人偏好和可核实证据为起点的求职 agent skills。先通过深挖访谈弄清用户真正想要的工作方向，再带着方向找岗位、解释依据，最后把选中的申请准备到人工审阅与提交之前。

**当前阶段：M0 脚手架与 M1 访谈 skill 已实现，结构校验与 workspace 保护规则有测试；访谈行为、岗位采集、浏览器填表尚未验证。** 详见 [M0/M1 报告](docs/m0-m1-report.md)。

## 三个 skill

| skill | 做什么 | 状态 |
|---|---|---|
| `grill-direction` | 层层追问到本质，把方向写成 direction template；含义与强度分开确认 | 已实现，行为评测未运行 |
| `find-openings` | 读 template，公司 → 官方招聘板 → 岗位，按适用的已确认底线做 pass/fail/unknown | 骨架 |
| `prepare-application` | 在用户自己的 Chrome 里填表、传简历、起草自由题，停止在最终提交前 | 骨架 |

## 目录

```text
.claude-plugin/plugin.json      # plugin 清单：job-right
skills/<name>/SKILL.md          # 三个 skill；grill-direction 含 references/ assets/ evals/
schema/*.schema.json            # direction / candidate / application / background_facts
scripts/resolve_workspace.py    # 私人 workspace 解析、创建与保护
scripts/validate.py             # 按 schema 与跨字段规则校验
tests/                          # pytest：正反例
docs/                           # 方案、评审、报告、普通读者说明
reference/                      # 研究笔记（设计依据）
```

## 运行

```bash
pip install -r requirements.txt
python3 -m pytest tests -q
python3 scripts/validate.py direction skills/grill-direction/assets/example-synthetic-city-profile.md
```

私人运行数据放在用户自己选择的工作仓库的 `workspace/` 下（或 `JOB_RIGHT_WORKSPACE` 指定的目录），由 workspace 自带的 `.gitignore` 保护；插件目录只放代码与资产。

## 阅读顺序

1. [项目说明](docs/project-overview.md)：普通读者版。
2. [实现方案 r4](docs/implementation-plan.md) 与 [评审记录](docs/implementation-plan-review.md)。
3. [reference 索引](reference/README.md)：研究依据。

`assets/` 与 `tests/` 中的人物、原话、公司均为 synthetic，不代表任何真实用户。真实个人档案不放入公开仓库。原创内容沿用 MIT 许可证；第三方来源保留各自许可。
