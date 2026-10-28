# 教学工作流整合包

本包将统一入口、三个专门工作流和四个自有能力模块一起分发，共八个完整技能，包含各技能的SKILL.md、参考资料、模板、脚本和示例资源。运行任务时按需要读取模块，不把所有指令一次性加载。

统一入口为 [teaching-workflows：编程教学工作台](skills/teaching-workflows/SKILL.md)。它识别目标与执行范围、按需分派、衔接来源与核验记录，并在续做时定位未完成和受影响阶段；各模块仍可独立调用。

| 工作流入口 | 主要任务 |
| --- | --- |
| [lesson-preparation](skills/lesson-preparation/SKILL.md) | 教师讲义、课堂练习、作业、拓展与按难点配交互 |
| [courseware-delivery](skills/courseware-delivery/SKILL.md) | PPT分镜、视觉协作、可编辑PPTX、原生备注与验收 |
| [contest-exam-analysis](skills/contest-exam-analysis/SKILL.md) | 单题、GESP与CSP整卷解析、多视角、分层完整代码及核验 |

| 内置完整能力 | 主要作用 |
| --- | --- |
| [gesp-solver](skills/gesp-solver/SKILL.md) | GESP逐选项、判断与编程题分析 |
| [solve-with-computational-thinking](skills/solve-with-computational-thinking/SKILL.md) | 从题意、建模和朴素方法推导到算法、证明与代码 |
| [interactive-algorithm-demo](skills/interactive-algorithm-demo/SKILL.md) | 可修改数据、逐步回退、代码与状态同步的离线演示；附前缀和模板与自检 |
| [csp-contest-author](skills/csp-contest-author/SKILL.md) | CSP命题、改编、组卷、数据与验题；原卷题解由解析入口负责 |

## 安装与使用

整合包采用根目录plugin.json和skills/的portable plugin布局。支持此格式的宿主可把它作为一个插件加载；本包没有新增MCP服务、账号连接或生命周期钩子。
本版经过验证的路径是使用官方skill-installer，从固定标签v0.4.0把skills/下八个完整目录先安装到空的暂存位置，再核对资源、备份旧版并复制到当前环境实际发现的个人技能目录。逐步命令、启用检查与回退见[GitHub安装说明](https://github.com/tsetsetse/oi-teaching-workflows#安装先取得固定版本再启用)。选择一种启用方式，避免把旧的独立安装与插件中的同名模块同时当作两套入口使用。portable插件宿主加载尚未实测。

已有同名安装时，先核对内容并完整备份到技能发现目录之外，再安装本包的固定快照；安装失败恢复备份。不要把开发源码目录直接作为固定安装副本。安装后在教学项目的新对话中使用 `$teaching-workflows` 发起任务；三个工作流与四个能力也保留独立调用方式。源码同步、文件复制与宿主发现分别验证，不互相替代。

各入口负责按原卷/项目规则确定语言、题量、评分、学生基础、输出与核验范围；这些要求优先于旧模块中的默认题量、分值或编译版本。课程原稿、真实试卷、学生资料和成品保存在使用者的课程项目，不放进技能目录。

## 外部扩展和运行条件

本包完整包含上述八个模块。huashu-design是课件新视觉设计使用的外部技能；Obsidian、PPT/PDF制作和浏览器能力按宿主环境提供，需要时由工作流发现并读取。它们没有被声明为已经内嵌。缺能力时说明受影响阶段，不假称调用或验证完成。

Python脚本采用3.10+标准库；编译例程另需对应C++编译器，交互模板自检需要Node.js。解包后可以用Python解释器调用三个入口附带的检查器，交互自检为：

```sh
node skills/interactive-algorithm-demo/assets/prefix-sum.test.cjs
```

## 内容与校验

bundle-manifest.json列出八个模块及每个实际载荷文件的SHA-256；它不对自身做递归哈希。ZIP旁的.sha256文件校验整个压缩包。排除系统缓存、编译缓存和Git元数据，构建时拒绝软链接及其他隐藏配置。
仓库内构建输出限定为dist目录中的ZIP，也可明确指定仓库外的ZIP位置。覆盖已有包前核对ZIP及校验文件目标；替换失败时恢复已有产物，避免输出参数误写破坏源码或丢失旧包。

四个能力来自用户授权纳入的本机自有技能快照，随本套件维护，保留原技能正文与资源。未给本包附加新的公开许可证；第三方扩展和课程材料的权利分别处理。

该文件布局依据[OpenAI官方插件打包说明](https://developers.openai.com/plugins/build/plugins)。文件与算法自检通过不代表已经在插件宿主中加载、完成真实考试整卷或课堂试用；每次安装和使用仍分别记录实际结果。
