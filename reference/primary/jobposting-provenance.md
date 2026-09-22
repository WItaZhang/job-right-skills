# 岗位语义与来源溯源

核实日期：2026-09-22（America/Los_Angeles）。这是字段与证据关系研究，没有接入知识图谱。

## Schema.org JobPosting

一手来源：[JobPosting 类型定义](https://schema.org/JobPosting)。阅读岗位属性表，重点为 hiringOrganization、jobLocation、jobLocationType、applicantLocationRequirements、datePosted、validThrough。

- **可借鉴机制：**区分雇主、工作地点、远程工作类型与申请者所在地要求；发布时间和截止时间有独立语义。
- **不应照搬之处：**结构化标记可以陈旧或不完整；有 `validThrough` 不证明当前仍开放，无截止时间不证明长期有效。公司对象不是团队对象。
- **对 job-right-skills 的映射：**保留源字段，再增加 observation/verification 时间与核实结论；远程标记不能自动解释为任意国家可工作。具体团队和开放状态仍需一手证据。

## W3C PROV-O

一手来源：[PROV-O Recommendation](https://www.w3.org/TR/prov-o/)，阅读 Starting Point terms 和 Expanded terms（Entity、Activity、Agent、wasDerivedFrom、hadPrimarySource、generatedAtTime、invalidatedAtTime）。

- **可借鉴机制：**将来源材料、核实活动与派生结论分别建模，保留谁在何时依据什么材料生成了结论。
- **不应照搬之处：**有溯源记录不等于信息正确；该标准不给出求职匹配分数或置信度校准方法。当前无需引入 RDF/OWL 全套实现。
- **对 job-right-skills 的映射：**轻量 evidence record 保存 source_url、checked_at、claim_id、derived_from、reviewer/method 与失效原因；明确本项目字段是简化设计，不宣称 PROV-O 合规。

## 本项目建议

把“事实是否有证据”“证据是否新鲜”“岗位是否符合偏好”分开记录。来源缺失时，value=null 并说明 unknown_reason；数字 0、空字符串和 false 都不能用作通用缺失值。详细字段与示例见 [研究证据规则](../design/research-evidence.md)。

置信度：高（标准术语与字段语义）；本项目映射尚未实现，也未经过互操作验证。
