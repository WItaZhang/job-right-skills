# Windows 本机就绪检查

检查人：Codex。基线：`e12838dfb65151bb2fd05a6b9de056b5a2338221`。本轮只检查能否进入试用和 Chrome 预检的前提，不开展第六轮全面评审，也未修改实现。

## 结论

可以进入 MVP 试用验收。此前必须先修的 R28 已改成不落盘的忽略检查，文件保留回归通过；R29、R30 的新增回归也通过。接下来处理一个小的 Windows 输出格式问题，并准备本机 Chrome 环境即可，不需要先展开新一轮边角问题评审。

报告里的 run 1、run 2、run 3 提供了访谈、找岗位和无浏览器时正确阻塞的运行记录。run 3 并未填写表单；Playwright 驱动受控表单通过，也不能替代 Claude in Chrome 实际调用 skill 的验收。

## 实际执行

环境：Windows，含中文的仓库路径，Python 3.10.20；独立临时 venv，按 requirements.txt 安装的 PyYAML、jsonschema、pytest。没有添加 Playwright，也没有升级用户的 Claude 安装。

```text
python -m pytest tests -q --tb=short
1 failed, 96 passed, 1 skipped in 12.03s

FAILED tests/test_ats_fetch.py::test_shortlist_ranks_and_pushes_down
expected prefix: evidence/openings/
actual prefix:   evidence\openings\

claude --version
2.1.126 (Claude Code)
```

- 唯一失败位于 shortlist 输出的 snapshot 路径：`skills/find-openings/scripts/shortlist.py:110` 使用 `str(p.relative_to(workspace))`，Windows 产生反斜杠，测试要求正斜杠。这是跨平台序列化格式不一致，不是找岗位逻辑整体失败。建议统一记录中的相对路径格式，例如使用 `.as_posix()`，然后复跑对应测试。
- `test_local_form.py` 在模块级调用 `pytest.importorskip("playwright.sync_api")`。本环境缺少 Playwright，因此整个模块跳过，包含四个 HTTP 测试和两个浏览器测试；pytest 汇总中的 `1 skipped` 是模块跳过，不代表只缺一个表单用例。本轮不能声称复现了容器中的 103 passed。
- R28 成功、失败、Git 报错时保持既有文件不变，以及不创建目录的回归均通过；R29 的 pending 范围和 R30 的围栏回归均通过。

## Chrome 预检尚未执行

仓库清单要求 Claude Code 至少 2.1.211，本机当前为 2.1.126，尚未满足该前提。本轮未升级 CLI、未检查扩展版本或连接、未启动 Claude in Chrome，也未上传文件、点击表单。因此没有创建或标记 `chrome-precheck` 成功记录。

本机预检应在准备好 CLI 和扩展后，使用合成资料、隔离 workspace 和受控本地表单执行，保存真实调用对话、请求日志及 application 校验结果。确认 `final_submits=0`、`registers=0`，并记录实际上传与回读结果；不能用其他浏览器工具的运行替代这一项。

## 建议的下一步

1. Claude 修复 snapshot 路径格式；可开 PR 展示 MVP，说明 Chrome 实操尚未验证，不需要先再做一轮全面评审。
2. 补充资历/目标级别的访谈问题，并用修改后的 skill 再跑一次多轮访谈与搜索，确认候选不再无意集中到实习或校招。用户当前经历属于事实，目标级别属于偏好，仍不能未经确认就设为硬条件。
3. 本机完成 Chrome 预检，再将受控填表流程标为通过。它证明在该测试表单上的行为，不承诺所有真实招聘网站都兼容。
