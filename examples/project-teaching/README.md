# 项目教学自编课例

本例完全自编，没有复制真实第03课、学生数据或日常课程成品。原始输入见[source.md](source.md)，设计见[project-design.md](project-design.md)，可运行小课例见[lesson.md](lesson.md)，显式用例清单为[cases.json](cases.json)。

课例通过“探测器充能助手”引入while：先只完成一次充能，再产生重复需要，观察条件、更新和停止；撤去范例后，用消耗氧气的相反变化迁移。并不要求所有Python课使用同一角色、故事或三个版本。

从仓库根目录执行：

```sh
python3 skills/lesson-preparation/scripts/check_lesson.py examples/project-teaching/lesson.md --cases examples/project-teaching/cases.json
```

独立前向测试从source.md和技能开始，不把project-design.md或lesson.md作为预期答案；生成到独立临时目录。模型行为、程序运行、结构检查与课堂效果分别记录，实际结果见[验证记录](verification.md)。
