# job-right-skills

以个人偏好和可核实证据为起点的求职 agent skills 研究项目。

**当前阶段：reference only。** 本仓库整理公开项目、一手文档和原创设计比较；尚未实现完整 agent，也没有实际运行岗位匹配或投递功能。

研究链路：兴趣／人生方向／压力与风险容忍度 → 结构化 preference profile → 硬约束与软偏好 → 冲突澄清 → company → team → current opening → 带来源、核实时间、匹配理由、置信度与 unknown 的解释。

从 [reference 索引](reference/README.md) 开始；优先阅读 [设计映射](reference/design-notes.md)、[偏好档案与冲突澄清](reference/design/preference-profile.md)、[研究链路与证据规则](reference/design/research-evidence.md)。

```text
README.md
LICENSE
.gitignore
reference/
  README.md                 # 筛选方法、参考目录、阅读顺序
  sources.json              # 来源、版本、核实时间与阅读范围
  design-notes.md           # 需求与参考机制的对应关系
  projects/                 # 8 项项目笔记，含 2 项受限/待核实条目
  primary/                  # 6 份官方文档/论文，汇总为 3 篇笔记
  design/                   # profile、冲突、证据及状态的研究结论
```

每项参考说明“可借鉴机制／不应照搬之处／对 job-right-skills 的映射”。个人经历、身份和偏好未提供时保持 unknown；文中的演示案例均为 synthetic，不代表用户事实。

本项目原名 `career-scout-skills`，2026-09-22 改名为 `job-right-skills`，保留原提交历史。最新文献核实日期为 2026-09-22（America/Los_Angeles）。没有复制上游实现，没有投递岗位或联系公司。

原创笔记沿用本仓库 MIT 许可证；第三方来源保留各自许可。真实个人档案不放入公开仓库。
