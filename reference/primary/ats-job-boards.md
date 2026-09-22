# 官方 ATS：公司、团队与岗位之间能证明什么

核实日期：2026-09-22（America/Los_Angeles）。阅读官方字段与 GET 说明；未对任何公司执行职位采集。以下映射是本项目建议。

## Greenhouse Job Board API

一手来源：[官方文档](https://docs.greenhouse.io/job-board.html)，阅读 Authentication、List jobs、Retrieve a job 与 Departments。

- **可借鉴机制：**公开 GET 提供已发布职位；`content=true` 可附岗位内容、部门与办公室；`id` 是 job post ID，`internal_job_id` 是内部 job ID，`updated_at` 是来源更新时间。
- **不应照搬之处：**department 不保证具体团队；`internal_job_id=null` 的 prospect post 不能无条件当作具体 vacancy；更新时间不等于首次发布时间或我们的核实时间。
- **对 job-right-skills 的映射：**保留 board、post ID、canonical URL、department 和原始更新时间；另设 team evidence、posting kind 与 verified_at。有岗位信息仍需逐条核实。

## Ashby Job Postings API

一手来源：[官方文档](https://developers.ashbyhq.com/docs/public-job-posting-api)，阅读 API 字段表。

- **可借鉴机制：**接口列出 currently published postings，区分 `department` 与 `team`；含 `workplaceType`、`publishedAt`、`jobUrl`；官方明确源数据缺失时响应也缺失。
- **不应照搬之处：**`isListed=false` 意为仅通过直链访问，不等于关闭；`publishedAt` 是最近发布，不能当首次发布。字段形状也不保证所有公司填写完整。
- **对 job-right-skills 的映射：**区分 publication visibility、opening status 和团队关联；团队字段缺失时 unknown；证据必须归属于经公司官网确认的招聘板。

## Lever Postings API

一手来源：[官方文档仓库](https://github.com/lever/postings-api)，阅读 Introduction、Get a list / specific job posting、JSON 字段。

- **可借鉴机制：**公开接口限 published 职位；分页使用 skip/limit；categories 包含 team/department；country 可为 null；hostedUrl 与申请 URL 分开。
- **不应照搬之处：**漏翻页或区域站点错误不能解释为岗位关闭；team 标签不证明经理、成员或当前职责；申请接口不是研究接口。
- **对 job-right-skills 的映射：**记录 provider/site/posting ID、读取覆盖范围与原始链接；country=null → unknown；只把官方标签作为团队关联证据之一。

## 跨来源研究结论

三个接口均可用于定位岗位资料，不能据此承诺 headcount、内推资格或雇佣结果。公司官网到招聘板的关联也要有证据，不能只猜 board slug。公开展示、当前可申请、真实在招是不同层次的结论。

本项目拟采用 [证据与状态规则](../design/research-evidence.md)：成功读取完整列表与读取失败分开；页面过期、打不开、被移除、明确关闭分别处理；相同 URL 的重复转载不增加独立证据数量。

置信度：高（本次读到的字段语义）；具体公司数据、运行稳定性及未来接口变化未验证。
