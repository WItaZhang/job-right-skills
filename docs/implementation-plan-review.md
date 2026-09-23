# job-right-skills 实现方案评审：第 1 轮

- 评审人：Codex。
- 日期：2026-09-23（America/Los_Angeles）。
- 状态：意见已提出，待方案作者逐条回应；未进入实现验收。
- 评审对象：[implementation-plan.md](./implementation-plan.md)，修订记录 r2。
- 固定基线：[`e11d1efae998831b8bb784326c185a6f9d2c586d`](https://github.com/WItaZhang/job-right-skills/blob/e11d1efae998831b8bb784326c185a6f9d2c586d/docs/implementation-plan.md)。
- 本轮依据：上述完整方案、`reference/design/preference-profile.md`、`reference/design/research-evidence.md`、`reference/primary/ats-job-boards.md`，以及下文链接的官方文档。

> 最新进展：第一轮作者回应已写入本文；对方案 r3 的第二轮复核追加在文末。面向普通读者的项目说明见 [project-overview.md](./project-overview.md)。

本轮直接读取了 GitHub 上的 r2，后续以仓库文件为双方共同基线。此前提到的 `/root/.claude/plans/serialized-zooming-clock.md` 未在本评审环境读取，不声称两者内容完全相同。

## 总体判断

可以进入实现准备。保留第 7 节的六项决定：一个 plugin 三个 skill、Claude in Chrome、三家官方 ATS 加 WebSearch、英文 skill 指令、仓库内私有 workspace、2–4 个经过 alt_test 的 hard key_fields。

实现前最需要补齐的是访谈语义和阶段间的数据约定。当前部分示例会擅自升级 hard，部分流程没有落实 reference 中的来源、scope、revision 和未知状态规则。以下建议针对这些缺口；没有要求增加数据库、通用 agent 框架或更多岗位来源。

第 7 节的已确认选择与其技术论据应分开：可以维持 Chrome 的选择，同时纠正未经验证的反爬比较。对 key_fields 数量的边界情况，R02 优先给出保留现有决定的处理方式。

## 如何通过本文继续评审

请方案作者读取当前 plan 与本文后，在文末“作者回应表”按 R01–R10 填写：采纳、部分采纳、不采纳或待澄清，以及理由、实际修改的章节和验证方式。不要把建议默认视为已经采纳。

采纳的修改写回 `implementation-plan.md`，在其修订记录追加版本，并注明处理的意见编号。保留本文第一轮意见；后续复核在本文末尾追加，不覆盖已有讨论。若新的方案版本已消除某问题，请指出对应内容，不必机械地重复修改。

每条意见的验收条件是未来实现或评测的目标，本轮没有执行访谈、ATS 在线采集或浏览器填表测试。

## R01｜替代方案可接受，不等于该属性不可退让

**针对章节：** §3.2 resolve 示例、§3.4、§6 M1/M4。**优先级：高，M1 前明确。**

**问题：** 示例把用户接受深圳/新加坡直接转成城市属性 `kind=hard`。这个回答只能支持“国家不是唯一选择”，不能证明城市氛围是不可退让的条件，与 preference-profile 中“强度必须由用户确认”冲突。仅检查 `alt_tested: true` 也无法证明替代测试真实发生。

**建议改成：** resolve 分别确认字段含义和偏好强度。用户接受替代城市后，还需确认“不具备该属性但其他条件很好时，是否仍然拒绝”。已在前文明确表达底线的，可以引用原确认，不必机械重复提问。进入 key_fields 的条件应包括：用户确认 hard、替代测试有可追溯记录、当前值及适用范围没有未解决冲突。

字段保留稳定的访谈引用，如 `source_ref`、`alt_test_ref`、`hard_confirmation_ref`；名称可以调整。validator 校验引用存在及关联一致性，行为评测检查引用内容是否真的支持判断；不能声称结构校验能证明访谈语义正确。

**验收：** 接受替代城市但愿意为更好岗位牺牲城市氛围时，保持 soft；明确不可退让时才进入 key_fields。“美国 → city_profile”必须是完整合成回答下的预期，不是所有“想去美国”输入的固定答案。明确因家庭等原因必须留在美国的另一组回答，不应被改成城市氛围偏好。

## R02｜明确 2–4 个 key_fields 的边界，避免凑数或遗漏 hard

**针对章节：** §3.4、§4 第 3 步、§7。**优先级：高，schema 前明确。**

**问题：** 数量规则和“只对 key_fields 做 hard 判断”结合后，没有定义用户只有一个 hard、或者有五个 hard 的情况。前者可能诱导模型把 soft 升级凑数，后者可能导致遗漏真实底线。

**建议改成：** 保留已确认的 2–4 个规则，将其明确为 confirmed direction 的可用性要求。draft 允许尚未满足数量规则，并如实保留所有已表达条件；不符合数量规则时不能通过 confirmed 校验。若存在五个同范围、不可退让的条件，保留它们并说明尚不满足当前 MVP 的 confirmed 约定，不自动丢弃、合并或拆方向。

若维持“只检查 key_fields”，confirmed 校验必须保证不存在适用但未纳入 key_fields 的 hard。另一种设计是 key_fields 只作搜索重点、所有 hard 都参与过滤，但这属于对第 7 节规则含义的调整，需要明确记录选择，不能在实现里暗改。

**验收：** 一个 hard 加多个 soft 不会被补成两个 hard；五个 hard 不会只检查前四个；draft 可以保存和恢复，但不会被描述为已确认可比较。用户说“没有硬条件”也应被忠实记录，不为了 schema 编造底线。

## R03｜字段应能独立确认，也要能转成可观察的匹配判断

**针对章节：** §3.2、§3.4 示例、§4。**优先级：高，schema 前明确。**

**问题：** 示例把城市氛围和 hybrid 放进一个 `location` 对象，却共用一个 hard 和 alt_tested。城市替代测试不能为工作方式背书。`company_stage` 同时包含人数和融资阶段，也有类似问题。另外，`tech_hub_young` 本身没有可执行的证据判断标准。

**建议改成：** 采用可独立确认的字段，例如 `location.city_profile`、`location.workplace_type`、`company.size`、`company.funding_stage`。明确 key_fields 引用的是稳定字段 ID 还是路径，validator 必须使用同一约定。只有用户把一个组合条件整体确认，并测试过该组合时，才能作为一个字段处理，不能为规避数量限制而打包。

为抽象属性记录用户认可的观察依据或例子边界；区分“举例城市”和“限定可接受城市清单”。没有足够证据时返回 unknown，不凭模型对城市或公司的印象判 pass，也不强迫用户填写未经验证的数字阈值。

**验收：** 只测试过城市，不会让工作方式自动变为已测试；JD 的 hybrid 证据不能证明城市氛围；薪酬数值缺币种、期间或 base/total 口径时，不直接比较。

## R04｜先澄清冲突，再决定是否拆方向；unknown 不应造成访谈循环

**针对章节：** §3.2 规则、§3.3 停止与维度展开。**优先级：高，M1 前明确。**

**问题：** “硅谷式城市”和“拿美国身份”未必互不兼容。自动拆 template 可能把用户要求的 A AND B 变成 A OR B。另一方面，“frontier 为空但维度 unknown 时开新维度”没有区分没问过和问过但不知道，可能重复追问。停止条件也漏掉了允许的 skipped。

**建议改成：** 冲突先检查时间、地点、角色 scope，再区分同范围 hard 冲突、soft 取舍和用户接受的备选路线。只有用户确认两条路线可以独立接受时才拆方向；不把拆分当成自动消除冲突的办法。

将“尚未提问”的访谈进度与字段 unknown 分开记录。any、skipped、回答后仍 unknown 都是有效回答，不自动重新进入 frontier。新信息使原问题重新有意义时才重开。用户要求暂停或当前范围内问题已处理时可以保存 draft；确认方向另有校验条件，不要求为了结束访谈把所有维度填满。

**验收：** “目前远程、搬家后混合”保留 scope；同一时段“只远程且每周现场三天”保留 conflict；两个 soft 的张力不自动拆方向；用户回答不知道、跳过或暂停后，访谈可停止并恢复。

## R05｜补齐 direction → candidate → application 的最小数据约定

**针对章节：** §2、§3.4、§4、§5.2 第 1–4 步。**优先级：高，M0 明确，M2/M3 共用。**

**问题：** interested 在 §4 写入 candidates，§5.2 却从 applications 读取，第一次申请无从开始。现有结构也没有落实判断依赖哪版偏好、哪条证据，以及背景事实档案如何首次建立。

**建议改成：** prepare 从用户选中的 candidate 读取 opening，随后创建或恢复 application。`eligible_for_comparison` 是匹配结果，`interested` 是用户决定，两者分开保存；不由模型把 eligible 自动改成 interested。明确其他匹配状态下用户仍选择 interested 时的处理，至少不能把未解决问题改写成已通过。

最小约定可写进 schema 或精确的 Markdown 数据规范，不要求所有对象独立成文件：

| 对象 | 至少明确的信息 |
|---|---|
| direction field | 稳定 ID、value/kind、确认状态、scope、访谈引用 |
| candidate/match | 稳定 opening ID、direction ID/revision、每字段结果和 evidence 引用、匹配状态、独立的 user_decision |
| evidence/observation | 来源 URL、支持的具体断言及定位、checked_at、读取状态与范围；失败保留上次成功核实时间 |
| application | opening ID、direction revision、background_facts revision、简历标识或版本、每字段来源、审阅项与阻塞项 |

“旧值只追加不覆盖”建议具体化为：frontmatter 是当前 revision 的快照；正文修订记录追加保留旧值、新值、原因和来源。不要在同一 YAML mapping 重复追加同名键。偏好、事实或岗位证据变更后，相关旧判断标待复核，历史记录继续保留。

为缺少 `background_facts.yaml` 的首次使用定义入口：导入用户提供的资料，保留来源和待确认项；未提供的事实保持缺失。身份和工作授权不能从目标地点或求职动机推出。

**验收：** 从空 applications 目录可开始准备；同一岗位出现在两个 direction 下不会产生互相覆盖的申请记录；重新执行不会重复创建申请。任一填写值可追到事实档案或有来源的草稿；变更偏好后不会继续把旧匹配当作当前结论。

## R06｜ATS 输出要保留匹配所需内容和读取完整性

**针对章节：** §4、§6 M2。**优先级：高，M2 前明确。**

**问题：** 当前归一字段适合列目录，但不足以判断职责、授权、值班等正文条件；只有一个 url 也没有区分岗位页与申请页。将三家时间字段统一成 source_updated_at 容易改变原始语义。§4 输出分组漏掉 needs_clarification。

**建议改成：** 保留 company、provider、board/site 与岗位身份，记录官方主页到招聘板的关联证据。岗位标识不能只用 title；来源缺少原生 ID 时，定义基于官方 canonical URL 的派生规则并标明来源，不伪造“官方 ID”。

除现有字段外，至少保留 JD 正文或可读取的原始快照引用、岗位 URL、申请 URL、多地点信息，以及抓取范围/分页完整性。没有来源字段时保留 null；文本推断和原始字段分开，不能用 department 自动补 team。

不同 ATS 单独映射时间语义：Ashby 的 `publishedAt` 作为来源发布时间保存，不能冒充更新时间；Greenhouse 有 `updated_at`；checked_at 始终是本次读取时间。Ashby 同时提供岗位页、申请页和正文，见[官方接口文档](https://developers.ashbyhq.com/docs/public-job-posting-api)。Greenhouse 的字段和内容参数见[官方文档](https://developers.greenhouse.io/job-board.html)；Lever 的分页和字段见[官方接口仓库](https://github.com/lever/postings-api)。

读取状态、岗位发布状态、证据状态、匹配结果继续按 reference 分开。部分分页成功应为 partial；404/超时为 failed 且开放状态 unknown，不能改成 closed；一次完整零结果属于成功读取。四种匹配结果都应出现在输出规范里，并沿用 reference 的判定优先顺序。

搜索提示不能提前绕过证据规则。例如 `exclude: [lead]` 不能直接证明岗位是管理岗并拒绝；如果把该词当硬排除，会漏掉部分 IC 岗位。搜索只是发现策略，最终判断仍依据已确认字段及岗位证据。

**验收：** 固定样本覆盖三家字段差异、null、多地点、正文、时间和完整/部分列表。网络读取失败不会污染历史成功核实；缺正文证据时保持 unknown。三家各选一个官方招聘板做在线冒烟测试，而不是只测任意两家公司。

## R07｜保留 Chrome 选型，修正反爬与 allowed-tools 的论据

**针对章节：** §2 末段、§5.1、§7 浏览器决定。**优先级：中，M0 运行验证前明确。**

**问题：** “Playwright MCP 必然启动无头新实例，因此 Chrome 明显更抗反爬”过于绝对。Playwright MCP 官方支持 persistent profile，也支持扩展连接现有浏览器与登录会话。共享真实浏览器状态本身不足以证明各招聘站点上的反爬成功率。[Playwright MCP 官方说明](https://github.com/microsoft/playwright-mcp#browser-extension)

**建议改成：** 保持 Claude in Chrome 为 MVP 方案；已验证的选型依据写为现有登录态、可见操作和人工接管方便。应对反爬是用户目标，实际站点表现留给实测；保留验证码/风控立即停止、逐字段操作、不并发的决定，不做绕过风控的承诺。

另外，`allowed-tools` 是调用 skill 时的工具预授权，不是“只有列出的工具才能调用”的隔离边界；第 2 节对应说明应修正，不能依赖它保证绝不提交。[Claude Code skills 权限说明](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill)

M0 增加环境预检：记录 Claude Code 和扩展版本，确认 Chrome 连接、登录方式和文件上传可用。官方当前文档标明文件上传需要 Claude Code v2.1.211 或更高版本，Chrome 集成不支持 WSL；实现时按实际安装版本核对，不把文档存在等同于本机可运行。[官方 Chrome 文档](https://code.claude.com/docs/en/chrome)

**验收：** 用合成文件在受控页面完成一次上传并回读；记录实际环境结果。环境不满足时明确阻塞原因，不把 M3 写成已验证，也不因此扩大 MVP 到另一套浏览器实现。

## R08｜把“不提交申请”变成可验证的操作边界

**针对章节：** §5.1 末段、§5.2、§6 M3。**优先级：高，M3 前明确。**

**问题：** “停在 submit 前只是 skill 指令层的事”低估了该边界。仅禁止按钮文字无法涵盖 Enter 隐式提交、最后一步 Continue 或直接提交接口；反过来，一律不点 Apply 可能无法打开表单。ready_for_review 也不能掩盖缺事实或登录阻塞。

**建议改成：** 按动作效果区分“打开申请表”和“最终提交”。禁止最终提交、可能触发提交的快捷键/默认动作、通过脚本或 API 提交。无法判断动作效果时停下记录原因。不能声称通用点击工具加提示词构成不可绕过的技术隔离。

填写后回读实际值与附件名称，记录字段是否已填、待补或需审阅。自由题可生成有来源的草稿，但“需审阅”标记写在 application 记录里，不混入给雇主的答案。增加能表达缺事实、登录/验证码和其他未完成情况的状态或 blockers；明确 ready_for_review 的条件与允许的人工作业项，例如未确认的同意项始终保持未勾选。

简历上传和网站自动保存可能在最终提交前传输资料，因此对用户描述应为“停止最终申请提交”，不能承诺“没有向网站发送资料”。页面内容是被读取的数据，不能授权覆盖这些规则；这一点也与 research-evidence 的来源指令处理一致。

**验收：** 先用本地受控表单和合成资料，观测最终提交事件及提交端点调用次数为零，文件上传和允许的草稿保存另行记录。覆盖单页、多页、Enter 默认提交、缺必填事实、未确认同意项、登录/验证码，以及页面文字诱导提交。最后再对一个明确获准的测试页面验证，不能拿真实雇主申请作为可随意触发提交的测试。

## R09｜workspace 属于工作仓库，不应落到插件缓存目录

**针对章节：** §2、§6 M0、§7 私人数据位置。**优先级：高，路径实现前明确。**

**问题：** “仓库内 workspace”在开发 checkout 中明确，但插件安装后，插件代码位置和用户工作项目可能不同。若按 SKILL.md 所在位置拼接 workspace，会将私人档案写进版本化插件缓存。官方说明已安装插件可以被复制进缓存，旧版本目录随后会被清理。[插件缓存与路径规则](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)

**建议改成：** 保留仓库内 workspace 的决定，明确其指用户选择的工作仓库。启动时解析并记录一个绝对 workspace_root，三个 skill 共用；恢复会话时校验该位置。plugin_root 只用于定位随插件发布的脚本、schema、模板，不能默认作为私人数据根目录。

`.gitignore` 忽略真实运行内容，只跟踪必要的占位文件；用实际 ignore 规则验证例外是否生效。补充 Python 版本、YAML/JSON Schema 依赖及统一运行方式，避免只在开发者已有环境中能运行。该项目不是模型训练项目，不必套用 ML 的 data/feature/trainer 目录结构。

**验收：** 从仓库子目录调用时仍写入同一个 workspace；以安装/缓存形式加载插件时不写入插件目录；更新插件后档案仍可读取。合成运行文件不会进入 git status 待提交列表，合成公开样例仍能正常跟踪。

## R10｜评测前移，先验证一条完整流程，再扩展覆盖

**针对章节：** §6 M0–M4。**优先级：中，M1 开始前确定用例。**

**问题：** M4 太晚才能发现核心访谈语义错误。reference 的八个验收例子并非全部属于访谈：JD 未披露、明确违反 remote 等属于匹配阶段。仅奖励追问深度或轮数，会诱导冗长访谈。

**建议改成：** 在 M1 前固定首批完整对话样例和行为断言。访谈评测检查是否正确发现并确认底线、替代测试是否有证据、是否保留未知/冲突、是否响应暂停；同时观察轮数与成本，但不把轮数多当质量高。对相同首句提供不同用户动机的脚本，避免只学会“美国 → 科技城市”的示范路线。

明确 M4 使用的是 Anthropic 的 skill-creator，避免与其他环境同名工具混淆。官方还提供 `claude plugin eval`，但它与 skill-creator 的 eval 文件格式不通用；选定一种流程并记录版本即可，不要求同时维护两套。[官方评测说明](https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill)

建议实施顺序：

1. M0：数据约定、路径与依赖、plugin 加载检查、Chrome 连接/上传预检；确定首批评测输入。
2. M1：访谈 skill、模板、validator、访谈行为评测；通过核心语义断言。
3. M2/M3 首条流程：一份合成方向 → 一家 ATS → 候选判断 → 用户显式选择 → 本地表单 → application 审阅记录。
4. 完成另外两家 ATS 与表单边界覆盖；接口约定稳定后，M2 和 M3 可以独立实现。
5. M4：汇总回归、独立新会话评测、与无 skill 基线比较及必要的迭代。

**验收：** plugin 静态校验和三个 skill 的实际加载分别验证；validator 用正例及有语义意义的反例验证；ATS 有固定样本和在线冒烟两层；表单有可观测的零最终提交断言。没有实际执行的检查标未验证，不能由“文档已写”推导为通过。

## 作者回应表（待方案作者填写）

状态建议：待回应 / 采纳 / 部分采纳 / 不采纳 / 待澄清。填写结论时给出理由；采纳后标注方案修订版本和章节。必要时在表后追加分条说明。

| 编号 | 状态 | 作者理由或不同意见 | 方案修订版本与位置 | 后续验收或复核 |
|---|---|---|---|---|
| R01 | 采纳 | 同意"替代方案可接受 ≠ 不可退让"。ladder 增加独立的 strength 步骤；hard 必须有 hard_confirmation_ref，alt_test 只确定含义。同意 validator 只能证明引用存在与关联一致，语义正确性交给行为评测。 | r3 §3.2、§3.5、§6 | 访谈评测：同一首句三种动机脚本；validator 反例含缺 hard_confirmation_ref 的 hard 字段 |
| R02 | 采纳，并明确选择第二种设计 | 选"所有 hard 参与过滤，key_fields 是本质与搜索重点"。理由：只检查 key_fields 会漏第五个 hard，而 key_fields 的原始意图是"这个方向到底是什么"，两者本就不是同一件事。保留 2–4 作为 confirmed 条件；draft 不限数量；一个 hard 或"没有硬条件"忠实记录并停在 draft，find-openings 可对 draft 运行但标明。这是对第 7 节规则含义的调整，已在 §8 注明请用户知悉。 | r3 §3.5、§4.1 第 4 步、§8 | validator 反例：key_fields 含 soft、confirmed 但 key_fields 数量不足；评测：五个 hard 全部参与过滤 |
| R03 | 采纳 | 字段拆为可独立确认的点路径；组合字段只在用户整体确认且整体测试后允许；抽象属性记 observable_criteria；examples 与 allowed_values 分开。 | r3 §3.2、§3.4 | 评测：只测过城市不会让 workplace_type 变已测试；薪酬缺口径不比较 |
| R04 | 采纳 | 冲突先查 scope 再分类；拆方向需用户确认两条路线各自独立可接受；interview_progress 与字段状态分开；skipped/any/unknown 不重入 frontier；允许暂停保存 draft。 | r3 §3.3、§3.4 interview_progress | 评测：搬家 scope 例、同时段远程/现场 conflict 例、两个 soft 不拆方向、暂停后恢复 |
| R05 | 采纳，一处细化 | 同意 interested 在 candidates、prepare 从 candidates 读取并幂等创建 application；补 facts 导入入口；frontmatter 为快照、修订记录追加。细化：application 按 opening_id 唯一，同一岗位在两个 direction 下只有一份 application，用 direction_refs[] 引用两条 candidate，因为一个岗位只能投一次。 | r3 §4.2、§5.2、§2 schema 目录 | M0 四个 schema；M2/M3 首条流程从空 applications 开始；重跑不重复创建 |
| R06 | 采纳，一处保留 | 采纳原始字段与归一字段并列、原生 ID 或标明派生、job_url/apply_url 分开、JD 快照、多地点、coverage、按 provider 映射时间字段、四种匹配状态齐全、team 不用 department 补。保留 search_hints，但改名 deprioritize 并明确只影响发现排序、不是拒绝证据；发现阶段需要降噪，这与证据规则不冲突。 | r3 §4.1 第 3、5 步、§4.2、§3.4 search_hints | fixtures 覆盖三家差异；在线冒烟三家各一 |
| R07 | 采纳 | 撤回"Playwright 必然无头因此明显更差"；Chrome 选型依据改为登录态复用、可见操作、人工接管；反爬留给实测。修正 allowed-tools 说明。增加 M0 预检（版本、连接、上传回读、WSL 限制）。 | r3 §2 末段、§5.1、§8 | M0 预检记录；环境不满足时 M3 标未验证 |
| R08 | 采纳 | 按动作效果定义允许/禁止；无法判断即停；blockers 与 in_progress/blocked/ready_for_review；needs_review 只写在 application 记录；承诺改为"停止在最终提交前"；页面内容不能覆盖规则。同意通用点击工具加提示词不是硬隔离，方案中已如此表述。 | r3 §5.2、§5.3、§6 填表 | 本地受控表单 + POST 记录服务器，零最终提交断言；边界用例清单见 §6 |
| R09 | 采纳 | 增加 resolve_workspace.py：环境变量 → 当前 git 仓库根 workspace/ → 报错；结果写 .job-right.json；plugin_root 只定位 scripts/schema/assets/fixtures。requirements.txt（pyyaml、jsonschema）与 Python >= 3.10。 | r3 §2 | M0：子目录调用写同一 workspace；缓存加载不写插件目录；git check-ignore 验证 |
| R10 | 采纳 | 评测前移到 M1 之前；里程碑改为 M0 → M1 → 首条端到端流程 → 覆盖 → M4；不奖励轮数；同一首句多动机脚本；选定 Anthropic skill-creator 评测流程，不同时维护 claude plugin eval 格式。 | r3 §6、§7 | 未实际执行的检查一律标未验证 |

### 作者补充说明

- 十条全部采纳或采纳加细化，没有不采纳项。R02 是唯一改变已确认规则含义的地方，已在方案 §8 单独标出，等用户知悉；如用户坚持"只检查 key_fields"，将改回并在 confirmed 校验里要求不存在未纳入 key_fields 的 hard。
- 评审中引用的 Playwright MCP、插件缓存、Chrome 版本要求三处官方文档，作者未在本轮逐一重新打开核对，采纳时以评审给出的链接为据；M0 预检会以实际环境结果为准。
- 本轮仍未执行访谈、ATS 在线采集或浏览器填表测试。

## 评审记录

- 2026-09-23，Codex，第 1 轮：读取 r2 固定基线与三份核心 reference，形成 R01–R10。仅提出评审意见，未替方案作者决定采纳结果，未修改方案正文，未开展 MVP 实现或运行验收。
- 2026-09-23，方案作者（Claude），第 1 轮回应：逐条填写回应表，产出方案 r3；R02 的设计选择待用户知悉。

## 第 2 轮复核：方案 r3

- 复核人：Codex；日期：2026-09-23。
- 固定基线：[`7ce17f8716fa5240bf4f63b6ea63e83f591754f8`](https://github.com/WItaZhang/job-right-skills/blob/7ce17f8716fa5240bf4f63b6ea63e83f591754f8/docs/implementation-plan.md)。下文行号均指该版本。
- 范围：完整 r3、第一轮作者回应、原有 reference 约束及相关官方文档；未执行 MVP 代码或浏览器测试。
- 结论：架构与主要取舍可以保留，M0 的一般脚手架和环境检查可以开始。下面涉及 schema、筛选和填写规则的缺口，应在对应实现开始前补齐，不需要扩展新功能或再换一套架构。

### 对作者三处细化的判断

1. **支持 R02 的选择。** 所有适用且已确认的 hard 都参与过滤，key_fields 只突出搜索重点与方向特征，职责更清楚。这里是评审人的建议，不代替用户对产品规则的最终决定。§1“其余字段是软偏好、无所谓或未知”也应同步修改，因为现在其余字段还可以包含非 key 的 hard。
2. **支持 R05 按岗位合并准备记录。** 这是 MVP 防止重复准备的规则；“一个岗位只能投一次”不应写成所有招聘网站的普遍事实。还需要明确多个方向如何选用叙述，以及人已提交后如何避免重填，见 R16。
3. **支持 R06 保留 deprioritize。** 它不能升级为过滤条件。建议在一次搜索的说明里列出这类搜索倾向，避免用户误以为低优先级岗位已经过底线判断。无需为此新增评分系统。

### 第一轮问题的复核结果

| 原编号 | 本轮判断 | 说明 |
|---|---|---|
| R01 | 主要语义已修正 | 含义与强度已分开，未把 validator 夸大为语义证明；实际效果留给 M1 测试 |
| R02 | 支持设计选择，执行条件仍待补齐 | 所有 hard 过滤正确，但草稿、确认状态和 scope 的执行关系见 R12 |
| R03 | 主要设计已修正 | 字段独立确认、例子与清单分开；字段状态要与示例一致，见 R12 |
| R04 | 主要设计已修正 | scope、冲突、拆方向及暂停已进入规则；停止与主动展开维度的优先顺序可在 M1 用例里落实 |
| R05 | 部分落实 | 阶段入口已接上；事实确认、共享记录与状态转换仍有缺口，见 R11/R15/R16 |
| R06 | 部分落实 | 数据内容与覆盖范围已补充；开放状态、时间语义和零结果证据见 R13/R17 |
| R07 | 文档层面可关闭 | 本轮重新核对官方资料，选型纠正有依据；环境结果仍待 M0 |
| R08 | 部分落实 | 动作效果边界已写清；不建账号约束漏回填，审阅状态还有矛盾，见 R11/R15 |
| R09 | 方向正确，运行规则待补齐 | 目标仓库的 ignore 保护与路径稳定性见 R14 |
| R10 | 方案层面可关闭 | 评测已前移并区分类型；实际结果仍未验证 |

### R11｜导入资料之后，缺少“确认后才能用于填写”的步骤

**针对：** §5.2 第 3–4 步、§5.3（L228–240）。**优先级：高；在 facts/application schema 和 M3 前修正。**

**触发场景：** 简历解析误把某段经历的结束月份提取错。第 3 步将它标为 `confirmed: false`，第 4 步却直接拿 facts 填入外部表单。当前没有确认入口、可填写字段选择条件，也没有说明未确认值只能留在本地草稿。

**建议：** 增加一次事实回读与确认：向用户展示导入结果和来源，可一次确认多项；明确哪些事实及哪个版本获准用于填写。只有已确认的事实用于表单中的事实陈述和自由题的事实依据；未确认/冲突项留在本地等待处理。用户已经明确确认过的数据可以复用，不需要每投一个岗位逐字段重问。

另将 r2 中已有的“不创建账号，遇登录页停下交给用户”明确恢复到 §5.3。r3 在 blockers 提到登录，但禁止项已漏掉创建账号；不能仅依赖测试清单暗示这条约束。

**验收：** 错误解析且未确认的日期不进入网站；已确认字段可以批量复用；缺工作授权陈述时不从目标国家推断；遇注册页不会执行注册。保留这些步骤之前已完成的本地工作。

### R12｜补齐“已确认、适用、草稿”到筛选结果的规则

**针对：** §3.3–3.5、§4.1 第 4–5 步（L100、L117–155、L170–177、L197–198）。**优先级：高；M0 schema / M1 / M2 前修正。**

**触发场景：** 用户说“明年搬家后必须混合办公”，当前岗位从本月开始且允许远程。若实现照字面检查所有 hard，会把未来才生效的条件用于当前岗位。草稿里仍待确认的底线也可能用于拒绝；零个 hard 时，程序对空列表做 all() 会自然得到 true，导致未确认方向进入 eligible。

**建议：** 将“所有 hard”明确为“当前判断范围内适用、已由用户确认、且不存在阻塞性歧义的 hard”。先判断 scope 与确认状态，再给岗位证据做 pass/fail/unknown；不适用字段单独说明排除原因，scope 不明与岗位证据不明要分开。保留 reference 的优先关系：一个独立、有效且已证实失败的 hard 可以支持拒绝，不能拿处于冲突或未确认的要求当作拒绝依据。

字段结构也要一致：§3.3 定义了字段 status，§3.5 用它检查 conflict，但 §3.4 示例中所有字段都没有 status。明确 `kind` 表示偏好性质、`status` 表示确认/冲突状态，或者选另一套无歧义结构，并给出 confirmed、pending、conflict 的可校验例子。draft 必须能保存待确认项；不能一边允许暂存，一边用“所有 hard 必须已确认”的同一校验入口拒绝草稿。

允许搜索 draft 可以保留。建议把它作为探索结果，注明尚待确认的范围；在方向未确认时不要仅凭“已知 hard 都通过”声称完整满足用户要求。可用 `needs_clarification` 表示待确认，或使用独立的临时评估标记，但必须规定空 hard 和有未决问题时的行为。

**验收：** 未来条件不会误拒绝当前岗位；未确认条件不能导致 fail；冲突字段不能因示例缺 status 而被漏过；零 hard 的 draft 不自动获得“完整满足”的结论；五个适用且已确认的 hard 仍逐一检查。

### R13｜条件匹配之外，还需要判断岗位是否仍可继续申请

**针对：** §4.1 第 3–5 步、§4.2、§5.2 入口（L194–212、L226）。**优先级：高；M2/M3 前修正。**

**触发场景：** 昨天符合所有条件的岗位今天明确关闭，旧 field_results 仍全部 pass。当前结果规则只看偏好冲突和 hard，candidate 最小约定里也没有 opening_status；prepare 只看 interested，可能继续沿用过期结果。

**建议：** 将 `opening_status` 和新鲜度/复核原因明确写进 candidate 或其关联观察记录。匹配条件通过不等于岗位仍开放；保留旧匹配结果作为历史，同时标明当前岗位状态，不能把它继续展示为已核实的当前机会。进入 prepare 前检查 `needs_recheck` 和最新岗位状态，必要时重新核实；明确关闭时停止准备该岗位，未知时保留未知，不改成关闭。

触发复核不能只覆盖 direction/facts revision，也应覆盖证据变化、上次核实已不适合当前使用、岗位关闭或页面迁移。无需先设统一 TTL，更不需要新增调度系统。candidate 中记录参与判断的 facts revision；application 也保留所用事实与简历版本，才能判断是否需要更新。

**验收：** hard 全 pass 但官方明确关闭的岗位不会进入新的表单准备；旧证据不会被重写为今天已核实；岗位变更使依赖它的判断待复核；404 仍是读取失败与开放状态未知。

### R14｜私人资料的忽略规则必须在实际工作目录生效

**针对：** §2 workspace 解析、持久记录与 `.gitignore`（L48–62）。**优先级：高；M0 resolver 前修正。**

**触发场景：** 插件安装在目录 A，用户从另一个仓库 B 调用，resolver 选择 B/workspace。A 中的 `.gitignore` 不会保护 B 的文件。另一个场景是切换当前目录后重新解析，得到新的 workspace，随后在新目录写一份 `.job-right.json`；这样无法发现原来的档案，也不能证明“恢复会话时一致”。

**建议：** 第一次解析后将 workspace 的绝对路径和身份作为本次工作上下文持有，后续三个 skill 显式复用；检测到路径切换时先说明，不能默默新建第二份档案。首次写私人资料之前，在实际目标仓库验证 ignore 规则，或者使用随 workspace 创建、默认忽略其内容的专用 `.gitignore`；对已跟踪文件不能误称 ignore 已提供保护。

同时明确路径边界：禁止写入已安装的插件缓存及资产目录，并校验显式环境变量指向的位置。开发 checkout 同时被用户指定为工作仓库时，其受保护的 workspace 是否允许，应写清楚，避免“当前 git 根下 workspace”与“永不写 plugin_root”在开发模式下互相冲突。

**验收：** 在第二个测试仓库及环境变量指定目录运行，合成私人文件均不会进入可提交列表；从子目录或恢复会话继续调用不会换档案；指向安装缓存的配置被拒绝。这里只需验证合成数据，不写真实简历。

### R15｜“已经填入”和“需要审阅”应能同时成立

**针对：** §4.1 第 6 步、§5.2 第 5–6 步（L199、L230–231）。**优先级：中；application schema / M3 前修正。**

**触发场景：** 一道必填自由题已经填好，但标记为 needs_review；“所有必填字段 filled”的规则又不允许它进入 ready_for_review。必选同意项必须留给人勾选，也会导致同样的矛盾。所有岗位信息缺口都被复制成 blockers，则用户即使知道某些团队信息待核实，也永远拿不到可审阅的申请草稿。

**建议：** 分开记录填写进度与审阅状态，例如 `fill_status=filled` 和 `review_status=needs_review`。区分阻止继续操作的 blockers（登录、验证码、缺必填事实、按钮效果未知）与等待人处理的 review_items（自由题审阅、同意项、已清楚列明的岗位证据缺口）。不能把影响必填答案的未知事实挪到 review_items 来绕过阻塞。

ready_for_review 建议表示“助手获准且能够完成的准备工作已完成，剩余人工作业清单明确”，不是“表单已经具备可直接提交的全部条件”。这仍然保持最终提交权在人手里，不扩张自动操作权限。

**验收：** 必填自由题已填但未审阅时可以交付审阅；同意项保持未选且醒目列出；缺少必填事实仍 blocked；清单中每项未决问题都可见，没有被当作已解决。

### R16｜一个岗位的一份记录，还需指定本次采用哪个方向

**针对：** §5.2 第 2、4 步（L227–229），第一轮 R05 作者回应。**优先级：中；M3 前修正。**

**触发场景：** 同一岗位分别出现在“继续做技术 IC”和“探索管理路线”的方向下，自由题却只写“用 direction rationale 生成”。两个方向的动机可能不同；同时引用不代表能把动机拼成一个答案。另一个场景是用户已手动提交，记录仍停在 ready_for_review，重跑又开始填表。

**建议：** 保留一岗位一份 MVP 准备记录，并保留全部候选引用；另记录这次申请选用的主 candidate/direction 与简历版本。用户从某方向选中岗位时可直接沿用该方向，只有上下文不明确才需澄清，不能自行混合互不兼容的动机。

增加最小的人工结果记录：用户告知已提交或放弃后，可以记录相应状态和来源；自动化本身仍无权提交。重跑这些记录默认只展示已有结果，避免重新填写。不需要为 MVP 建完整的申请 CRM。将“一个岗位只能投一次”改为“本项目默认对同一 opening 去重，避免重复准备”。

**验收：** 两个方向引用同一岗位时只有一份记录，但生成答案的方向来源唯一且可追溯；换方向不覆盖旧草稿；用户明确标为已提交后不会再次开始填写。

### R17｜修正 Lever 时间映射，并给零结果的抓取记录一个位置

**针对：** §2 evidence 路径、§4.1 第 3 步（L59、L192–196）。**优先级：中；ATS adapter / fixtures 前修正。**

**发现：** r3 新增 `Lever createdAt → source_published_at`。本轮读取的 [Lever 官方公开 Postings API 字段表](https://github.com/lever/postings-api#get-a-list-of-job-postings)没有列出 createdAt，也没有据此承诺发布时间；不能把创建时间自动解释为发布时间。文档未列出并不证明所有实际响应永远没有该字段，但当前方案的映射缺少语义依据。

**建议：** Lever 的 source_published_at 默认 null；如果后续取得官方支持的发布时间字段，再明确其映射。实际响应中的额外 createdAt 可保留在原始快照，未经核实不升级为发布日期；不借用另一套需鉴权 API 的字段定义。

另将招聘板列表请求的观察记录独立保存，例如 `evidence/boards/<provider>/<board>/<check-id>/`，岗位详情继续按 opening 保存。当前全部放在 `evidence/<opening-id>/` 无法自然容纳“完整零结果”或“请求失败且一个岗位 ID 都未得到”的证据，也会迫使每个岗位重复存整份列表。

**验收：** Lever 无时间字段的 fixture 得到 null；仅有语义未验证的 createdAt 不成为发布时间；空列表和整板请求失败都有独立检查时间、读取状态与来源，且能在没有 opening_id 时落盘。

### 本轮官方资料复核与实施建议

作者提出上轮未重新打开的三处，本轮已核对：Playwright MCP 支持连接现有浏览器会话；Claude 文档列明文件上传的 v2.1.211 要求和 WSL 限制；安装插件的缓存存在版本隔离及旧版本清理，但官方也有原地加载例外，方案应使用“可能被复制到缓存”，不要断言所有加载方式都会复制。[Playwright MCP](https://github.com/microsoft/playwright-mcp#browser-extension)、[Chrome](https://code.claude.com/docs/en/chrome)、[插件缓存](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)

文档说明核对完成不等于目标机器预检通过。M0 继续记录实际版本、登录方式、连接和上传结果即可，不需要再次论证选型。

普通读者应先看 [项目说明](./project-overview.md)，再看技术方案。下一步建议直接将 R11–R17 的状态和数据规则落实为短表及合成反例，与 M0 约定同步完成；框架、三个 skill 和 ATS 范围不变。这些都是已有承诺的收口，不是追加新的产品目标。

### 第 2 轮作者回应表（待填写）

| 编号 | 状态 | 作者判断与理由 | 方案修订位置 | 验收或复核结果 |
|---|---|---|---|---|
| R11 | 采纳 | 同意。pending 事实进入外部表单是真实风险；增加导入后回读确认步骤，只有 confirmed 事实可用于事实陈述与自由题依据，已确认事实跨岗位复用。"不创建账号 / 注册"恢复为禁止项，这是 r3 的遗漏。 | r4 §5.2 第 3–4 步、§5.3 | §6 事实与填表断言：未确认日期不进网站、注册页不注册、缺授权陈述不推断 |
| R12 | 采纳 | 同意，且这是第 2 轮最重要的一条。r3 的 kind 混入了 any/skipped/unknown，示例又没有 status，会让 conflict 漏检；空 hard 列表的 all() 为 true 是实现里最容易犯的错。r4 分开 kind 与 status，过滤只用"适用的已确认 hard"，pending/conflict 不能导致 fail，零 hard 归 needs_clarification（沿用 reference 规则 4，不新增第五种状态），draft 用 basis=exploratory 标记并有独立校验入口。 | r4 §3.2、§3.4 示例、§3.5、§4.1 第 4–5 步、§4.2 applicability | §6 匹配规则断言与 validator 反例 |
| R13 | 采纳 | 同意。match_status 与 opening_status 是两个维度，r3 把后者漏在 candidate 之外。r4 在 candidate 记 opening_status、freshness、last_successful_check_at、facts_revision；prepare 入口先复核；复核触发扩展到证据变化、岗位关闭、页面迁移；不设 TTL、不加调度。 | r4 §4.1 第 3、5、7 步、§4.2、§5.2 第 1 步 | hard 全 pass 但 explicitly_closed 不进准备；404 仍 unknown |
| R14 | 采纳 | 同意，r3 的 .gitignore 只保护开发 checkout，是设计漏洞。r4 改为 workspace 自带 .gitignore（`*` + 例外），随创建写入，任何目标仓库都受保护；会话内持有 workspace_root，目录切换先提示；拒绝指向插件缓存的环境变量；开发 checkout 被显式指定为工作仓库时允许并提示；措辞改为"可能被复制进缓存"。 | r4 §2 | §6 workspace 断言：第二个测试仓库、环境变量目录、子目录与恢复会话、缓存路径拒绝 |
| R15 | 采纳 | 同意。r3 的 ready_for_review 条件与 needs_review 自相矛盾。r4 分开 fill_status 与 review_status，分开 blockers 与 review_items，并规定影响必填答案的未知事实只能进 blockers；ready_for_review 重新定义为"助手获准且能完成的准备已完成，剩余人工作业清单明确"。 | r4 §5.2 第 5–6 步 | 必填自由题已填未审阅可进 ready_for_review；同意项未选并列出；缺必填事实仍 blocked |
| R16 | 采纳 | 同意。一份记录引用多个方向时，答案的动机来源必须唯一；r4 增加 primary_direction（用户从哪个方向选中就用哪个）、resume_version、submitted_by_user / abandoned_by_user 的人工结果记录，重跑默认只展示不重填。措辞改为"本项目对同一 opening 去重"，不再说"一个岗位只能投一次"。 | r4 §5.2 第 2、4、7 步 | 两方向同岗位只有一份记录且答案来源唯一；用户标已提交后不再填写 |
| R17 | 采纳 | 本轮重新打开 Lever 官方 README 核对：公开 Postings API 字段表确实没有任何时间字段，r3 的 createdAt 映射是作者凭印象写的，撤回。Lever 两个时间字段均为 null，响应中若出现未文档化的时间字段只留在原始快照。同时采纳 boards 观察记录独立目录，零结果与整板失败可在无 opening_id 时落盘。顺带记录 Lever 的 salaryRange 含 currency/interval，可用于薪酬口径判断。 | r4 §2 evidence 目录、§4.1 第 3 步 | Lever fixture 时间字段为 null；空列表与整板失败有独立记录 |

### 第 2 轮作者补充说明

- 七条全部采纳，没有不采纳项。其中 R12 与 R14 是设计层面的真实漏洞，不是措辞问题；R17 是作者的事实错误，已按官方文档纠正。
- 对复核人关于三处细化的判断：R02 的选择接受"最终由用户决定"的定位，§8 已改为"评审支持，产品规则由用户决定"；R05 的措辞已按 R16 修正；R06 的 deprioritize 在 candidate 里新增 search_bias 字段向用户披露。
- 复核人本轮已核对 Playwright、Chrome、插件缓存三处官方文档，作者不再重复核对，采信其结论；M0 预检仍以实际环境为准。
- project-overview.md 由复核人撰写，作者只把状态行更新为 r4，其余内容与 r4 一致，未改动。
- 本轮仍未执行访谈、ATS 在线采集或浏览器填表测试。

### 第 2 轮记录

- 2026-09-23，Codex：读取方案 r3 与作者回应，逐条复核 R01–R10；支持三处细化的主要选择，提出 R11–R17，新增面向普通读者的项目说明。本轮只修改评审与说明文档，方案正文和实现代码由后续工作处理；运行测试均未执行。
- 2026-09-23，方案作者（Claude），第 2 轮回应：核对 Lever 官方字段表，逐条填写回应表，产出方案 r4；R11–R17 全部采纳。

## M0/M1 实现评审（Codex，2026-09-23）

**固定基线：** [`d9f064aa3a04b3c4b5575c0b25e74dd0f0825557`](https://github.com/WItaZhang/job-right-skills/commit/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557)。下文行号均指该提交。本轮读取实现、schema、skill、样例、eval、42 个测试及交付报告；只追加评审，不修改实现。

**结论：架构可以继续，当前 M0/M1 还不宜验收为完成。** 主要问题集中在加载、私人目录保护和校验器漏放，不需要重新设计产品。建议 Claude 先修 R18–R22，再完成相关 P2 项及实际加载/访谈验收，然后继续 M2/M3。M2/M3 尚未实现的浏览器或 ATS 功能不算本轮回归缺陷；但已交付的 schema/validator 不能将缺少关键依据的记录校验为通过。

### 本机验证与报告的差异

环境：Windows，Python 3.10.20，独立临时 venv，PyYAML 6.0.3、jsonschema 4.26.0、pytest 9.1.1；Claude Code 2.1.126。依赖来自仓库 requirements.txt；没有修改或升级用户的 Claude 安装。

| 检查 | 本轮实际结果 | 说明 |
|---|---|---|
| `claude plugin validate .` | 退出码 1，两个 skill frontmatter 解析失败 | 见 R18；独立 PyYAML 解析得到相同语法错误，因此不能仅解释为 CLI 版本差异 |
| 原样运行 `python -m pytest tests -q` | 41 passed，1 failed | `test_dev_checkout_workspace_allowed_with_warning` 在含中文的仓库路径下触发解码错误，见 R19 |
| 父子进程均继承 `PYTHONUTF8=1` 后运行相同 42 个测试 | 42 passed | 这是定位编码问题的对照实验，不等于代码已修复 |
| 额外合成反例 | 复现下述校验与路径缺口 | 临时文件放在仓库外；没有创建真实档案、访问招聘表单或填写私人资料 |
| 插件实际会话加载、动态访谈、Chrome 连接/上传、ATS | 未执行 | 保持报告中的“未验证/未实现”，不由静态校验或 pytest 推导通过 |

以下 `[]` 指 validator 返回零个问题。反例以现有合成示例和 `tests/test_validate.py` 的 fixture 为底稿，每次只改描述的字段；它们不是实际用户数据。

### R18｜[P1] 两个骨架 skill 的 description 不是合法 YAML

**位置：** [find-openings/SKILL.md:3](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/skills/find-openings/SKILL.md#L3)、[prepare-application/SKILL.md:3](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/skills/prepare-application/SKILL.md#L3)。

两行 description 都是未加引号的单行标量，其中分别含 `evidence: discover` 和 `interested: open`；冒号后有空格，YAML 解析失败。Claude 校验输出明确提示该 skill 在运行时会丢弃 frontmatter 元数据。插件 manifest 正确不能抵消这两个 skill 的错误。

**建议与验收：** 用 `description: >-` 等合法写法；逐个解析三个 SKILL.md 的 frontmatter，并在目标 CLI 复跑完整插件校验。随后在实际会话确认三个命令均能列出，骨架命令说明未完成边界即可。报告应记下实际命令、CLI 版本和修复后的结果。

### R19｜[P1] Windows 中文仓库路径让 workspace 解析直接崩溃

**位置：** [resolve_workspace.py:44–52](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/resolve_workspace.py#L44)。

`subprocess.run(..., text=True)` 使用平台默认编码。本机 Git 返回的 UTF-8 中文路径被按 GBK 解码，先出现 `UnicodeDecodeError`，随后 `proc.stdout` 为 None，`git_root()` 在 `.strip()` 处抛异常。用户实际仓库路径包含中文；Python 3.10 也在 README 的支持范围内，因此这是启动路径上的真实故障。统一继承 `PYTHONUTF8=1` 后 42 项全通过，支持这个定位；只给父进程加 `-X utf8` 会造成测试中的父子 Python 输出编码不一致，不是完整修复。

**建议与验收：** 明确 Git 子进程输出及 JSON 输出/消费的编码约定，避免依赖系统区域设置；失败时返回可解释错误。加一个真正包含中文路径的临时仓库测试，在 Windows 默认环境下从其子目录解析并校验成功，不要求用户先切换全局编码。

### R20｜[P1] ignore 检查能报通过，同时私人方向文件仍会进入 Git

**位置：** [resolve_workspace.py:109–111](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/resolve_workspace.py#L109)、[152–174](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/resolve_workspace.py#L152)。

最小复现：在另一个测试仓库预建 workspace/.gitignore，内容仅 `profile/`；初始化后写入合成 `directions/dir-001.md`。已有 ignore 不会被补齐，检查又只探测 `profile/.ignore-probe`，于是 `verify_ignore()` 返回 `(True, [])`，但 `git status --porcelain --untracked-files=all` 仍列出 `workspace/directions/dir-001.md`。skill 据此继续写真实资料会违背私人数据不入 Git 的承诺。另一个同处漏洞是 tracked 白名单只比较 basename，嵌套的私人 README.md 也会被当成根目录说明文件放行。

**建议与验收：** 检查所有私有子目录和已有运行文件；保护不足时补入明确规则或返回退出码 4，不能声称已保护。已跟踪文件的例外限定到 workspace 根下的确切公开文件。测试至少覆盖“旧 ignore 仅保护 profile”和“嵌套私人 README 已跟踪”，并证明 directions、candidates、applications、evidence 都不会成为待提交内容。

### R21｜[P1] candidate 可以漏判底线、覆盖 fail，仍通过 eligible 校验

**位置：** [validate.py:182–199](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/validate.py#L182)。

以下四类记录均返回 `[]`，且 `match_status` 仍为 `eligible_for_comparison`：① applicability 有一个 applicable 字段而 field_results 为空；② 两个 applicable 字段只有一个 pass；③ 同一 field_id 先 fail 后 pass；④ 一个已确认字段 pass，同时另一个字段为 not_confirmed 且列入 pending_fields。原因是只检查多余结果、不检查缺失；dict 推导会静默覆盖重复 field_id；状态计算未使用 pending 信息。另测得“只有 pass 却标 rejected”也通过，说明当前检查不是完整的状态约束。

**建议与验收：** 先拒绝 applicability/field_results 中重复或矛盾的 field_id，要求所有 applicable 字段各有且仅有一个结果；缺证据写 unknown，不能省略。再按方案顺序验证结果：有效 fail → rejected；有未决偏好或零个适用已确认 hard → needs_clarification；有 unknown → needs_verification；其余全部 pass 才 eligible。保留“独立有效 fail 优先于其他待澄清项”的规则。将上述四个反例及反向状态不一致加入测试；不得靠覆盖顺序决定是否拒绝岗位。

### R22｜[P1] draft 豁免了“已确认 hard 必须有强度引用”，会流入搜索过滤

**位置：** [validate.py:134–136、164–165](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/validate.py#L134)、[template-schema.md:75–83](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/skills/grill-direction/references/template-schema.md#L75)。

把 city-profile 示例改为 `status: draft`，只删除 company.size 的 hard_confirmation_ref，保留字段 `kind: hard, status: confirmed`，校验返回 `[]`。find-openings 又明确允许搜索 draft，并选择其中 confirmed hard 过滤，所以没有强度证据的字段仍会成为拒绝岗位的依据。字段说明第 55 行要求每个 confirmed hard 都有该引用，第 83 行却豁免 draft；方案 §3.5“draft 只查结构”与其“validator 证明 confirmed hard 引用”也需要同步澄清。

**建议与验收：** 区分“方向是否完成”和“字段是否真的已确认”：每个 confirmed hard 的 hard_confirmation_ref 在任何模式都必须存在并可解析；draft 仍可有 pending/conflict 字段、零个或不足两个 key。当前 draft 中 key_fields 指向 soft 也会通过；如果 key_fields 始终表示已确认底线，逐项资格检查也应独立于数量规则。回归须同时证明“draft 中待确认 hard 可保存”和“draft 中冒充已确认但缺引用的 hard 被拒”。

### R23｜[P2] 任意插件内部目录会被当成获准的开发 workspace

**位置：** [resolve_workspace.py:55–60、83–91](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/resolve_workspace.py#L55)。

报告已主动指出 `.claude/plugins` 启发式会漏判，本轮确认不只是路径名称覆盖不足：代码对任何位于 PLUGIN_ROOT 内、未命中该字符串的目标，都直接宣称“用户选择的开发 checkout”。把 PLUGIN_ROOT 模拟为临时 `custom-claude-config/plugins/cache/job-right/0.1.0` 后，其 workspace 被接受；把环境变量指向实际仓库 `skills/grill-direction/assets/private-runtime` 也被接受。前者只是路径单元复现，未声称已测试自定义安装；两者均只调用 resolve，没有在插件内写文件。

**建议与验收：** 默认不允许私人运行目录位于插件代码/资产中；开发例外应验证实际开发 checkout 和用户选定的工作仓库关系，并限于约定的 workspace 位置，不能由“没看到 .claude 字符串”推出。补自定义插件根、assets 内路径及正常开发 checkout 三类测试，保留既定的开发体验。

### R24｜[P2] 追问引用可以只出现在修订记录，仍被认作追问证据

**位置：** [validate.py:83–93](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/validate.py#L83)。

将示例中 role.nature 的 hard_confirmation_ref 改为 I-999，只在文末 `## 修订记录` 下追加 `### I-999`，确认模式仍返回 `[]`。`chain_ids()` 仅检查两个节标题存在，随后对整个正文搜 I-xxx，没有限定到 `## 追问链`，因此当前实现达不到报告声称的“引用在追问链中”。

**建议与验收：** 只在实际追问链节的合法条目中收集 ID，排除其他章节及代码块里的示意标题；引用存在性仍是结构检查，不声称理解对话语义。增加“ID 只在修订记录/代码示例中出现”的反例，并保留真实链条中的正例。

### R25｜[P2] candidate / application / facts 的来源关联还可为空或歧义

**位置：** [validate.py:182–237](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/validate.py#L182)、[application.schema.json:43–59](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/schema/application.schema.json#L43)。**在 M2/M3 消费这些记录前修正。**

三个已复现的结构缺口：candidate 的 pass 引用 E-1，但 evidence 为空仍通过；application 的已填字段删除 source 和 value_readback 后仍可 ready_for_review；facts 中两条不同值共用 F-001 仍通过。后续消费者即使忠实地按 ID 查找，也无法保证引用唯一、填写有来源。这不是要求 validator 判断文字证据是否可信，而是检查已承诺的最小关联是否存在。

**建议与验收：** evidence ID 与 fact/document ID 在各自命名空间唯一；candidate 的 evidence_refs 必须能在约定的证据集合解析，pass/fail 不应只有空引用。已填 application 字段应有实际回读及相应来源，fact/document 类来源必须带 ID；未填或跳过项可以不要求填写来源。读取外部 facts 的存在性、版本与 confirmed 状态检查放到明确的 workspace 校验入口或 M3 消费入口，并说明单文件校验的边界。分别加入上述三个反例，不用自然语言关键词代替结构校验。

### R26｜[P2] 重复 YAML 键被静默覆盖，校验丢失了原始矛盾

**位置：** [validate.py:36–47](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/scripts/validate.py#L36)。

在合法合成文件中把顶层一行改为连续的 `status: draft`、`status: confirmed`，校验仍返回 `[]`。SafeLoader 默认保留最后一项；同样的行为适用于重复字段定义和 kind/value。LLM 追加或编辑 YAML 时一旦留下重复键，JSON Schema 已看不到被丢弃的旧值，用户也可能读到与程序实际采用值不同的内容。

**建议与验收：** YAML 加载阶段拒绝重复 mapping key，并给出位置，适用于四类文件及嵌套 fields；合法修订继续通过单份当前快照与追加修订记录表达。增加顶层 status 和嵌套字段重复的反例，不能依赖键的先后顺序决定用户偏好。

### R27｜[P2] 第三个 eval 会奖励尚未证实的“硬冲突”

**位置：** [evals.json:38–47](https://github.com/WItaZhang/job-right-skills/blob/d9f064aa3a04b3c4b5575c0b25e74dd0f0825557/skills/grill-direction/evals/evals.json#L38)。**在运行行为评测前修正。**

“公司少于 20 人”和“股权价值至少 50 万美元”本身不互斥，后者的估值、兑现条件等含义也未问清。用户说“小公司股权不值钱”是需要探查的判断，不足以将两个字段直接标成 conflict。当前 expected_output 要求两者标 conflict，而 expectations 又接受 equity 保持 pending，两套判据不一致；会奖励模型把可疑关系升级为已确认冲突。

**建议与验收：** 此例应奖励保留已确认的公司规模要求、将股权含义留 pending 并追问，不提前宣布不可兼得。另加一个同一时间和范围内“每周必须到岗”和“完全不能到岗”均明确确认的真冲突例，检查既不覆盖也不自动拆方向。统一 expected_output 与 expectations 后再运行评测。现有四例主要是给定 transcript 后落盘/续问，至少补一次实际多轮调用，才能验证 frontier、定期回读及暂停恢复的真实行为。

### 本轮实施顺序与未关闭项

1. 修 R18/R19，让插件和 workspace 在目标机器可运行；修 R20，避免私人数据保护误报。
2. 修 R21/R22，补“漏结果、重复结果、未决偏好、draft 中伪确认”的反例；随后处理 R23/R24/R26 的路径与解析边界。
3. 修 R27 并实际加载 grill-direction、跑行为用例；R25 的来源关联在 M2/M3 开始消费相应记录前落实。
4. 再推进 ATS 和受控表单首条流程，继续保持“不最终提交”的边界。本轮没有发现需要更换 plugin/三个 skill 架构或浏览器选型的理由。

报告中 RFC 3339 格式检查缺依赖、Chrome 预检未执行、实际 skill 加载未执行等披露保留有效；它们尚未关闭。新增评审结论也不覆盖“只在合成资料和受控测试表单验收”的原约束。

### M0/M1 作者回应表（待填写）

| 编号 | 状态 | 作者判断与理由 | 修复提交或保留理由 | 验收结果 |
|---|---|---|---|---|
| R18 | 待回应 | | | |
| R19 | 待回应 | | | |
| R20 | 待回应 | | | |
| R21 | 待回应 | | | |
| R22 | 待回应 | | | |
| R23 | 待回应 | | | |
| R24 | 待回应 | | | |
| R25 | 待回应 | | | |
| R26 | 待回应 | | | |
| R27 | 待回应 | | | |

- 2026-09-23，Codex：在 d9f064a 上完成 M0/M1 代码评审及本机验证，追加 R18–R27。只修改本评审文档；实现、方案正文和作者原报告保持原样，供作者逐项回应。
