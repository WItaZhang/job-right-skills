---
id: dir-001
title: 年轻科技聚集城市里的中型 AI infra 公司，做 IC
revision: 4
status: confirmed
created_at: 2026-09-23T10:00:00+08:00
updated_at: 2026-09-23T11:20:00+08:00
key_fields: [location.city_profile, role.nature, company.size]
fields:
  location.city_profile:
    value: tech_hub_young
    observable_criteria: [科技公司密度高, 25–35 岁从业者比例高, 有活跃的线下技术社区]
    examples: [深圳, 新加坡, 旧金山湾区]
    kind: hard
    status: confirmed
    scope: {valid_from: "2026-10", roles: all}
    source_ref: I-003
    alt_test_ref: I-007
    hard_confirmation_ref: I-009
    rationale: 要的是年轻科技聚集的氛围，不是美国本身
  location.workplace_type:
    value: [hybrid, onsite]
    kind: soft
    status: confirmed
    source_ref: I-011
    alt_test_ref: null
    hard_confirmation_ref: null
    rationale: 更想在办公室认识人，但不是底线
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
    rationale: 太小没有系统可维护，太大只能做一小块
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
    source_ref: I-022
    note: 用户说还没想过底线；币种与期间口径未定
  location.workplace_type_after_move:
    value: [hybrid]
    kind: soft
    status: confirmed
    scope: {valid_from: "2027-06", note: 搬家后}
    source_ref: I-023
    alt_test_ref: null
    hard_confirmation_ref: null
    rationale: 用户在 I-024 确认这是希望而不是底线
search_hints:
  keywords: [infrastructure engineer, platform engineer, ML infra, developer platform]
  deprioritize: [manager, head of, director]
open_questions:
  - 薪酬底线口径未定（币种、base/total）
  - 压力承受与团队环境两个维度尚未展开
interview_progress:
  asked: [兴趣动力, 地点与时间, 角色与成长, 风险容忍, 薪酬与身份, 人生方向]
  not_asked: [压力承受, 团队环境]
---

# 年轻科技聚集城市里的中型 AI infra 公司，做 IC

本质：在一个年轻、科技公司密集的城市，进一家 50–500 人的公司，继续做技术 IC。国家不是条件，城市氛围才是。

**这是合成示例。** 人物、原话与时间都是虚构的，用来说明 template 格式与追问链写法，不代表任何真实用户。

## 追问链

### I-001
- 时间：2026-09-23T10:02+08:00
- 用户原话：我想去美国做 AI 相关的工作。
- 访谈者问题：（开场）
- 结论：stated。开两条 ladder：地点（美国）、内容（AI）。

### I-002
- 时间：10:03
- 用户原话：主要是那边机会多吧，公司也多。
- 访谈者问题：美国哪一点最吸引你？如果只能留一个原因，是什么？
- 结论：why 第一层，仍然笼统，继续追。

### I-003
- 时间：10:05
- 用户原话：其实是想要那种年轻人多、大家都在做 tech 的感觉，像硅谷那样。
- 访谈者问题：“机会多”具体指什么？是岗位数量、薪资、还是身边的人？
- 结论：attribute 浮现：城市氛围，不是国家。source_ref for location.city_profile。

### I-004
- 时间：10:06
- 用户原话：对，科技公司密集，同龄人多，周末有技术活动。
- 访谈者问题：如果让你描述“硅谷那样的感觉”，你会看哪几件事来判断一个城市有没有它？
- 结论：observable_criteria 由用户给出。

### I-005
- 时间：10:08
- 用户原话：AI infra 或者开发者工具，模型本身我不太想做。
- 访谈者问题：AI 相关里，你更想做哪一层？
- 结论：industry soft，source_ref。

### I-006
- 时间：10:09
- 用户原话：算是加分项，不是必须。
- 访谈者问题：如果一家公司城市氛围很对、规模也合适，但做的是别的方向，你会考虑吗？
- 结论：industry 强度为 soft。

### I-007
- 时间：10:11
- 用户原话：可以啊，深圳我去过，那种感觉挺像的。新加坡也行。
- 访谈者问题：那么深圳、新加坡这类同样年轻、科技公司密集的城市，可以吗？
- 结论：alt_test 通过。属性含义确认为城市氛围，美国不是条件。

### I-008
- 时间：10:12
- 用户原话：不算，我没有必须去美国的理由。
- 访谈者问题：确认一下，“去美国”本身对你还算一个条件吗？比如身份、家庭？
- 结论：排除国家字段与身份动机。

### I-009
- 时间：10:13
- 用户原话：会拒绝。我在一个很安静的城市待过两年，再好的公司我也不想重来。
- 访谈者问题：如果一个岗位其他都很好，公司、薪资、内容都对，但城市没有这种氛围，你还会拒绝吗？
- 结论：strength 确认 hard。hard_confirmation_ref for location.city_profile。

### I-010
- 时间：10:14
- 用户原话：明年 10 月合同到期以后。
- 访谈者问题：这个条件从什么时候开始算？现在就要，还是某个时间点之后？
- 结论：scope.valid_from=2026-10。

### I-011
- 时间：10:16
- 用户原话：最好能去办公室，认识人。全远程有点浪费搬过去的意义。
- 访谈者问题：工作方式呢？远程、混合、现场？
- 结论：location.workplace_type source_ref，倾向 hybrid/onsite。

### I-012
- 时间：10:17
- 用户原话：那倒不至于，远程也不是不行。
- 访谈者问题：如果一家在合适城市的公司只提供全远程，你会因此拒绝吗？
- 结论：workplace_type 强度 soft。

### I-013
- 时间：10:19
- 用户原话：（已回读草稿：城市氛围 hard、行业 soft、工作方式 soft）对，就是这样。
- 访谈者问题：回读第一轮草稿。
- 结论：用户确认草稿。

### I-014
- 时间：10:21
- 用户原话：还是想写代码，不想管人。
- 访谈者问题：角色上，你想继续做 IC，还是带团队？
- 结论：role.nature source_ref。

### I-015
- 时间：10:22
- 用户原话：tech lead 可以，只要不做绩效和招聘。
- 访谈者问题：如果是 tech lead，带方向不带人、不做绩效，算 IC 吗？
- 结论：alt_test：IC 的边界是“不做人员管理”，不是头衔。

### I-016
- 时间：10:23
- 用户原话：会拒绝，我试过，不适合我。
- 访谈者问题：如果一个岗位其他都很好，但明确要带 5 个人做绩效，你会拒绝吗？
- 结论：strength 确认 hard。

### I-017
- 时间：10:25
- 用户原话：对成长的期待就是能碰到规模化的系统问题。
- 访谈者问题：这次换工作最想改变什么？
- 结论：人生方向维度已问；为 company.size 铺垫。

### I-018
- 时间：10:26
- 用户原话：大概几十到几百人，太小没有系统可维护，太大只能做一小块。
- 访谈者问题：什么规模的公司最可能有你说的规模化系统问题？
- 结论：company.size source_ref。

### I-019
- 时间：10:27
- 用户原话：几千人的独立事业部，如果自己有完整系统，也行。
- 访谈者问题：如果是大公司里一个独立的几十人事业部，有自己的系统，可以吗？
- 结论：alt_test：属性是“团队能对完整系统负责”；人数是代理指标。

### I-020
- 时间：10:28
- 用户原话：20 人以下的我不去，几万人的大厂普通岗位也不去。
- 访谈者问题：那我们把规模写成 50–500 人作为底线，20 人以下和万人级大厂普通岗位都拒绝，对吗？
- 结论：strength 确认 hard；值 50–500，边界由用户认可。

### I-021
- 时间：10:30
- 用户原话：B 轮到成长期吧，太早的公司我不太放心。
- 访谈者问题：融资阶段有没有偏好？
- 结论：company.funding_stage soft，用户随即表示“不是底线”。

### I-022
- 时间：10:33
- 用户原话：还没想过，我不知道当地行情。
- 访谈者问题：薪酬有底线吗？按什么口径算？
- 结论：status=unknown，不追问，记入 open_questions。

### I-023
- 时间：10:36
- 用户原话：搬家以后我想至少混合办公，方便照顾家里。
- 访谈者问题：刚才你提到 2027 年中可能搬家，那之后工作方式的要求会变吗？
- 结论：新字段 location.workplace_type_after_move，scope.valid_from=2027-06。不与 I-012 判冲突，因为 scope 不同。

### I-024
- 时间：10:37
- 用户原话：是希望，不是必须。真要是全远程也能安排。
- 访谈者问题：这是搬家后的底线，还是希望？
- 结论：strength 确认 soft。r3 中该字段曾为 pending hard，见修订记录。

## 修订记录

- r1 2026-09-23 10:15：创建，含 location.city_profile（hard）、industry（soft）、location.workplace_type（soft）。
- r2 2026-09-23 10:29：新增 role.nature、company.size（均 hard，已 alt_test 与强度确认）、company.funding_stage（soft）。
- r3 2026-09-23 10:36：新增 compensation.base（unknown）、location.workplace_type_after_move（kind=hard, status=pending，来源 I-023）。方向保持 draft，因为存在 pending hard。
- r4 2026-09-23 11:20：I-024 确认 workplace_type_after_move 为 soft（旧值 kind=hard/status=pending，新值 kind=soft/status=confirmed，原因：用户明确说是希望不是必须）。key_fields 三个均满足条件，方向标 confirmed。压力承受、团队环境仍未展开，记入 open_questions。
