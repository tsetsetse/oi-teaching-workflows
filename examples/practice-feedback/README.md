# 作业测评与学情反馈自编示例

本目录所有任务、学员代号、作答与教师观察均为自编/合成验证材料，不含真实学生信息，不代表正式GESP/CSP试卷或课堂干预结果。

- [原任务](assignment.md)：本课目标、已学范围、完整题目与评价规则。
- [合成作答](student-work.md)、[事实记录](observations.md)：独立错解S1、提示后订正S2；Q2缺答，没有历史或独立复测。
- [详细教师报告](teacher-feedback.md)：具体机制、教学改动、三道完整补练及C++14参考程序、提示、用例与复验标准。
- [家长草稿](parent-feedback.txt)：温和鼓励，保留提示程度，下一步是计划；未发送。
- [四场景验证请求](scenario-cases.md)、[实际验证记录](verification.md)：路由、缺答/计分、官方对齐、事实与鼓励的核验边界。

程序须先审阅，再从仓库根目录用显式清单运行：

```sh
python3 skills/lesson-preparation/scripts/check_lesson.py examples/practice-feedback/student-work.md --cases examples/practice-feedback/student-cases.json
python3 skills/lesson-preparation/scripts/check_lesson.py examples/practice-feedback/teacher-feedback.md --cases examples/practice-feedback/teacher-cases.json
```

第一条预期返回非零：它忠实检查学生S1的错误，不能改期望答案掩盖失败；S2单独记录通过。第二条核验三份教师参考程序。程序通过不等于学员已经独立完成补练。
