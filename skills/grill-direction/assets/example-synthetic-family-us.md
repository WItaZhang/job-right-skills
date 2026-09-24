---
id: dir-002
title: 留在美国、可照顾家人的 AI 应用岗位（草稿）
revision: 2
status: draft
created_at: 2026-09-23T14:00:00-07:00
updated_at: 2026-09-23T14:25:00-07:00
key_fields: [location.country]
fields:
  location.country:
    value: US
    allowed_values: [US]
    kind: hard
    status: confirmed
    scope: {roles: all, note: 父母在美国需要照顾，至少未来三年}
    source_ref: I-003
    alt_test_ref: I-005
    hard_confirmation_ref: I-006
    rationale: 家庭原因必须留在美国；城市氛围不是这个方向的条件
  location.city_profile:
    value: null
    kind: any
    status: confirmed
    source_ref: I-007
    rationale: 用户明确说城市氛围无所谓
  location.commute_to_family:
    value: {max_drive_minutes: 90, anchor: 用户父母所在城市（私有）}
    kind: hard
    status: pending
    source_ref: I-008
    alt_test_ref: null
    hard_confirmation_ref: null
    note: 用户说“最好在车程一个半小时内”，强度尚未确认
  industry:
    value: [AI applications]
    kind: soft
    status: confirmed
    source_ref: I-002
  role.nature:
    value: null
    kind: unspecified
    status: skipped
    source_ref: I-009
    note: 用户说这个问题先跳过
search_hints:
  keywords: [machine learning engineer, applied AI, AI product engineer]
  deprioritize: []
open_questions:
  - location.commute_to_family 的强度未确认：是底线还是希望？
  - 工作授权只记用户陈述，尚未询问
interview_progress:
  asked: [地点与时间, 兴趣动力, 人生方向]
  not_asked: [压力承受, 风险容忍, 角色与成长, 薪酬与身份, 团队环境]
---

# 留在美国、可照顾家人的 AI 应用岗位（草稿）

本质：必须留在美国，最好离家人不远。这与 dir-001 的首句相同（“想去美国做 AI”），但动机完全不同，所以不能套用 dir-001 的城市氛围结论。

**这是合成示例。** 用于说明：同一首句、不同动机时，访谈不能把“美国”改写成“城市氛围”；以及 draft 允许只有一个 key_field、允许 pending hard 与 skipped 字段。

## 追问链

### I-001
- 时间：2026-09-23T14:01-07:00
- 用户原话：我想在美国找 AI 相关的工作。
- 访谈者问题：（开场）
- 结论：stated。

### I-002
- 时间：14:02
- 用户原话：做应用层的，把模型用到产品里那种。
- 访谈者问题：AI 相关里你想做哪一层？
- 结论：industry soft（用户随后表示“方向可以谈”）。

### I-003
- 时间：14:04
- 用户原话：不是机会的问题，我父母在这边，身体不太好，我得留在美国。
- 访谈者问题：美国哪一点最吸引你？
- 结论：why 直接指向家庭。source_ref for location.country。

### I-004
- 时间：14:05
- 用户原话：至少三年吧，看情况。
- 访谈者问题：这个情况大概会持续多久？
- 结论：scope 备注。

### I-005
- 时间：14:06
- 用户原话：不行，我得能在一天之内到他们那儿。
- 访谈者问题：那如果加拿大温哥华、或者别的科技城市有很好的岗位，可以吗？
- 结论：alt_test 未通过。属性确实是“国家/可达性”，不是城市氛围。

### I-006
- 时间：14:07
- 用户原话：会拒绝，这个没得谈。
- 访谈者问题：如果一个岗位其他都好，但在美国以外，你会拒绝吗？
- 结论：strength 确认 hard。

### I-007
- 时间：14:09
- 用户原话：无所谓，我不在乎城市热闹不热闹。
- 访谈者问题：城市本身呢，你在乎它是不是科技氛围浓的城市吗？
- 结论：kind=any，status=confirmed。

### I-008
- 时间：14:11
- 用户原话：最好在车程一个半小时内。
- 访谈者问题：在美国范围内，离家人的距离有要求吗？
- 结论：新字段 location.commute_to_family。强度未问，status=pending。

### I-009
- 时间：14:13
- 用户原话：这个先跳过吧，我还没想好。
- 访谈者问题：角色上想继续做 IC 还是带团队？
- 结论：status=skipped，不重问。

### I-010
- 时间：14:20
- 用户原话：我先去接个电话，晚点继续。
- 访谈者问题：（回读草稿后）
- 结论：用户暂停。保存 draft。frontier 中还有 commute_to_family 的强度问题未问。

## 修订记录

- r1 2026-09-23 14:10：创建，location.country（hard，已确认）、location.city_profile（any）、industry（soft）。
- r2 2026-09-23 14:25：新增 location.commute_to_family（hard，pending）、role.nature（skipped）。用户暂停，保存为 draft。下次恢复时优先问 commute_to_family 的强度。
