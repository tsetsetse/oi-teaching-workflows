# 课件交付试做

输入使用仓库自编的 [重复输出讲义](../intro-loop/source-讲义版.md)，不含真实学生或外部课程正文。

[逐页分镜示例](storyboard-example.md)来自一次独立的 `courseware-delivery` 调用：仅做40分钟分镜和交付验收计划，不制作课件、不新增编程题。
该案例规划25页，包含问题与答案分开、逐轮状态揭示、原生教师备注、完整题面、同题练习、Bug修复及后续验收。
25页仅属于这个案例，不是工作流对其他课程的页数要求。
示例现已补明同题推进、学生表达与仅教学分镜阶段；未追加真实视觉稿或伪造方向确认记录。

教学结构的两种选择见 [教学推进方式](../../skills/courseware-delivery/references/teaching-paths.md)；视觉与正式 PPTX 的衔接见 [设计协作](../../skills/courseware-delivery/references/design-collaboration.md)。实际新视觉需配合当前环境提供的 `huashu-design`，它不随本仓库分发。

可重做的请求：

> 使用本仓库 skills/courseware-delivery/SKILL.md，根据 examples/intro-loop/source-讲义版.md 制定40分钟课堂课件的逐页分镜与交付验收计划。学生看投影，教师看备注，成品须能带离源资料目录使用。本次仅规划，不生成PPTX、PDF或HTML，不新增编程题。产物放在独立临时课程目录。

检查工具的自动测试：

```sh
python3 -m unittest discover -s tests -p test_check_pptx.py -v
```

测试会在临时目录构造最小ZIP/XML夹具，检查包、备注与关系处理；这些夹具不是可授课课件，不能用来宣称真实渲染通过。
查看 [验证范围](validation.md) 了解本次实际运行与未测内容。
