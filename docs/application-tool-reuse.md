# 申请准备阶段：复用现有求职工具的建议

这是接入建议，不是新的全面评审，也没有替换现有实现。本轮阅读了 reference、GitHub 文档和下述指定源文件；没有运行上游填表工具，没有读取或迁移真实个人档案。

## 给用户的结论

可以复用，而且值得先做一个小接入验证。job-right-skills 继续负责访谈、方向文件和有依据的岗位判断；用户选中岗位后，由已有工具读取经确认的个人档案、上传指定简历和填表。现有 prepare-application 保留为入口和记录协调层，填表执行可以换成现有工具，不必自己承担所有网站适配。

预期流程：**方向与岗位判断 → 用户选中 → 个人档案与简历 → 现有工具填表 → 回读与人工提交。**

这是对 M3 执行方式的候选调整，不是宣布已完成集成；现有 Claude in Chrome 路线仍保留，是否换用其他执行方式由一次受控验证决定。

## 看过哪些项目

| 项目 | 本轮核实范围 | 可复用部分 | 建议 |
|---|---|---|---|
| [Pickle-Pixel/ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot) | README、profile.example.json、cli.py、apply/prompt.py、apply/launcher.py、database.py 的相关实现；固定提交 `4a8d521f67f5139811c0a910ef37410f8e6d836a` | 个人档案、简历资料、浏览器填表、指定岗位执行与运行记录 | 优先做接入试验，因为用户已使用同源项目；不能直接继承全部默认行为 |
| [aravindpranav/job-agent](https://github.com/aravindpranav/job-agent) | README，以及 answer_bank.py、filler.py、submit.py 的相关实现；固定提交 `cfd549913c224e39b8896c4eed32ac7bf06fdccc` | 可复用答案库、字段到来源的映射、未知项保留、人工审阅与独立提交状态 | 作为档案和填写计划的重点参考；其美国工作授权、默认来源等设定不能当作本用户事实 |
| [geckguy/AutoApply](https://github.com/geckguy/AutoApply) | README；读取时提交 `6c5fbc42833278acaa45981e86b5d99ae97d77a0`，未审查执行代码或运行 | 文档描述了浏览器扩展、档案、保存答案、修正复用及人工最终提交 | 若更看重浏览器中的可见操作，可作为后续候选，不同时接三套 |
| reference 中的 [JSON Resume](../reference/projects/jsonresume.md)、[career-ops](../reference/projects/career-ops.md)、[llm-job-pipeline](../reference/projects/llm-job-pipeline.md) | 仓库现有研究笔记 | 履历结构、偏好与事实分开、状态和证据记录 | 这些笔记主要研究访谈与岗位研究，不能据此声称已验证它们的填表执行能力 |

GitHub 有多个同名 ApplyPilot。本次核对的是用户现有安装所指向的 Pickle-Pixel/ApplyPilot 上游；没有把其他同名项目的特性混进来。用户安装中已有的定制修改未在本轮审查，以下上游发现不等于断言用户当前版本仍有同样行为。

## ApplyPilot 能接，但需要适配的几个具体地方

1. **可以承接个人信息和填写。** 上游 profile 示例按联系方式、工作授权、可到岗时间、薪酬、经历等组织；CLI 提供指定 URL 与填表 dry-run。[profile 示例](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/profile.example.json)、[CLI](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/src/applypilot/cli.py)
2. **指定 URL 仍依赖内部岗位队列和简历路径。** acquire_job 会从数据库查找岗位并要求 tailored_resume_path；它不是一个可以无条件接收任意新 URL 的独立填表函数。需要受控导入用户选中的一条岗位和指定简历，避免再跑一遍发现/评分流程。[launcher.py](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/src/applypilot/apply/launcher.py)
3. **dry-run 不等于现成的 ready_for_review。** prompt 中 dry-run 要求不点最终按钮，却仍输出 RESULT:APPLIED；launcher 将 applied 结果计入已申请，结束还会清理浏览器。接入需要独立的“已准备待审阅”结果，并让用户能接手当前页面，不能把准备过的岗位误记成已投递。[prompt.py](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/src/applypilot/apply/prompt.py)、[launcher.py](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/src/applypilot/apply/launcher.py)
4. **必须使用本项目的事实规则。** 上游提示词允许对同领域工具经验积极回答 Yes，与“只填经确认事实”冲突。应替换实际执行提示词中的这类规则，并去掉未经确认的身份/自我识别等默认答案；不能只在外层追加一句“不要编造”。这些是静态源码发现，未在真实申请中运行验证。[prompt.py](https://github.com/Pickle-Pixel/ApplyPilot/blob/4a8d521f67f5139811c0a910ef37410f8e6d836a/src/applypilot/apply/prompt.py)

因此建议把 ApplyPilot 当作可调用、可适配的执行器候选，而非未经验证直接替代整个 M3。

## 个人资料怎样保存，才能不重复填写

只维护一份经用户确认的事实主档案，沿用 `workspace/profile/background_facts.yaml`；需要时转换成执行工具要求的 profile 格式。已有 ApplyPilot 档案可以导入，保留来源，沿用有依据的既有确认；新增、含糊和冲突的内容才再问用户。不要让两份可独立编辑的档案长期漂移。

- **稳定事实：** 姓名、联系方式、教育与经历、指定简历及其版本。
- **经确认的常用申请答案：** 到岗时间、搬迁意愿、按国家/地区区分的工作授权等；改变时更新确认与版本。
- **岗位相关草稿：** 为什么申请这家公司、如何描述相关经验；每份申请生成并交给用户审阅，不能把上一家公司的回答当成通用事实。

job-agent 的 `AnswerBank` 和 `FillPlan` 值得参考：数据与字段映射分开，填写项带来源，无法回答的项单独列出。其 `submit.py` 也区分 submitted / dry_run / skipped。本项目仍只接入准备阶段，不开放自动最终提交。[答案库](https://github.com/aravindpranav/job-agent/blob/cfd549913c224e39b8896c4eed32ac7bf06fdccc/src/job_agent/apply/answer_bank.py)、[字段映射](https://github.com/aravindpranav/job-agent/blob/cfd549913c224e39b8896c4eed32ac7bf06fdccc/src/job_agent/apply/filler.py)、[提交状态](https://github.com/aravindpranav/job-agent/blob/cfd549913c224e39b8896c4eed32ac7bf06fdccc/src/job_agent/apply/submit.py)

## 给 Claude 的最小实施建议

先完成一个“选定岗位 → ApplyPilot 准备申请 → 写回 applications 记录”的小试验。先确认所用 ApplyPilot 版本及已有定制，以免重复修改。保留三个 skill 的入口、现有个人档案和候选判断；不接入它的批量投递、重新评分或自动提交流程。

使用合成资料和已有三页测试表单即可。执行器运行数据放隔离目录，不使用用户现有 ApplyPilot 数据库。验收只看这些结果：档案中的值是否正确填入；无依据的必填事实是否停下询问；简历是否正确上传；最终提交与注册次数是否为零；是否产出有来源的审阅记录，并保留可人工接手的浏览器页面。dry-run 不得改写成“已申请”。

这个试验通过，再决定是否让 ApplyPilot 成为 M3 默认执行器；如果改造成本明显高，就保留现有浏览器执行，并只借鉴答案库和字段映射。无需先再做一轮全仓评审，也不承诺任何工具仅凭 README 就能可靠处理所有招聘网站。
