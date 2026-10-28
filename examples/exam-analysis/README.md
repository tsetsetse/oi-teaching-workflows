# 竞赛与等级考试解析核验试做

只使用仓库自编材料，不含真实试卷、学生记录或外部付费课程：

- [混合题型小卷](source-mini.md)：选择、判断、阅读程序两小问、完善程序两空，共六个叶子题号；用于检查逐项覆盖与解析机制。
- [相同数对编程题](source-pairs.md)：自编三组计分规则，用于检查不同视角、部分分/组合/完整方法、每层完整程序及理论与实测的区分。

对应的[混合小卷精简解析](mini-analysis.md)覆盖六个叶子项，[分层实现示例](pairs-analysis.md)关联五份独立完整程序；[核验摘要](verification.md)明确理论、本地运行与正式得分的边界。公开副本的[显式用例清单](cases.json)列出7份程序和23组运行；两份[单题清单](inventory-pairs.json)与[小卷清单](inventory-mini.json)可用新工具复验。

这些材料不是 GESP 或 CSP 真题，不代表实际考试的题型数量、等级知识范围或分值。原始来源事实、考纲版本与正式评分仍需在真实任务中逐卷核对。

当前示例与本地独立后测的实际产物、运行证据和未测范围见 [验证记录](validation.md)。真实课程、临时构建和逐次运行日志留在忽略的 `.local/`。

可复做请求：

> 使用本仓库 skills/contest-exam-analysis/SKILL.md，为自编相同数对题编写中文教学题解，给出多视角、按原评分设置的分层完整 C++14 程序及独立测试证据。另按初赛逐题解析规则处理自编混合小卷，覆盖每个小问与空。保留来源，产物放独立临时目录；本次不生成交互网页或PPT。

工具回归：

```sh
python3 -m unittest discover -s tests -v
python3 skills/contest-exam-analysis/scripts/check_inventory.py examples/exam-analysis/inventory-pairs.json
python3 skills/contest-exam-analysis/scripts/check_inventory.py examples/exam-analysis/inventory-mini.json
```

清单检查只验证人工清单和文件，完整程序运行与题解审查须另行执行。模板里的状态与预期不能当作实际验证结果。
