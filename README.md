# OI Teaching Workflows

面向青少儿 C++、Python 教学的工作流套件。通过 **编程教学工作台 `teaching-workflows`** 统一发起阶段规划、项目教学与作品验收、备课、课件交付、竞赛/等级考试解析及作业测评与学情反馈，按需读取配套 Skills。

**当前正式版 v0.7.0 包含 1 个统一入口＋6 个专门工作流＋4 个完整能力模块，共 11 个技能目录。** 统一入口组织流程，各模块也能独立使用。工作流源码、已安装技能和课程材料分别保存；同步 GitHub 不会自动更新本机技能或改动课程。

## 当前包含哪些内容

统一入口负责判断任务和安排交接；六个工作流组织完整的教学交付；四个能力模块提供可复用的解题、演示和命题能力。它们作为完整技能目录一起打包，使用时只读取本次需要的部分。

| 模块 | 职责 |
| --- | --- |
| **`teaching-workflows` 编程教学工作台** | 判断任务、确定范围、安排交接、读取进度与续做 |
| `curriculum-planning` 阶段课程规划与学习路径 | 标准课程母版、学生/班级阶段计划、课时与先修核算、达标检查及进度调整 |
| `project-teaching` 项目教学与作品验收 | 各知识点情境化、项目课改造/创建、阶段版本、教师支架及功能/解释/独立/迁移验收 |
| `lesson-preparation` 备课讲义 | 来源核对、教学主线、教师讲稿、练习/作业/拓展、程序验收 |
| `courseware-delivery` 课件交付 | 从确定讲义或解析制作分镜、PPTX、原生教师备注与验收 |
| `contest-exam-analysis` 竞赛与等级考试解析核验 | 单题、GESP一至八级、CSP-J/S初复赛逐题解析，多视角与分层完整代码 |
| `practice-assessment-feedback` 作业测评与学情反馈 | 本课作业、阶段测试、考前/赛前模拟；详细教师诊断、完整补练及鼓励型家长草稿 |
| `gesp-solver` | GESP逐选项、判断与编程题分析及等级考点参考 |
| `solve-with-computational-thinking` | 题意、建模、朴素方法、算法选择、证明、复杂度和代码推导 |
| `interactive-algorithm-demo` | 可修改数据、逐步执行、代码与状态同步的离线HTML演示，附模板和自检 |
| `csp-contest-author` | 命题、改编、组卷、数据与验题包；正式原卷题解由解析工作流负责 |

正式套件下载见 [GitHub Release v0.7.0](https://github.com/tsetsetse/oi-teaching-workflows/releases/tag/v0.7.0)，附件含完整 ZIP 及 SHA-256 校验文件。

## 统一入口怎样组织工作

[teaching-workflows](skills/teaching-workflows/SKILL.md) 是日常使用入口。说明目标、指定材料和本次范围后，它会读取当前教学项目的规则与已有成果，选择所需模块，并沿用已经确认的学生基础、课时、语言版本和输出位置。

例如，同一份课程材料可以只做备课，也可以继续制作 PPT 和作业；一份已确定的题解可以直接制作课件。只要交互演示时直接使用演示模块。各阶段共用来源、代码、输入输出和检查记录，避免重复生成有效成果。

创建或修改任务可使用[任务进度模板](skills/teaching-workflows/assets/progress-template.md)记录来源、已完成阶段、检查证据和下一步。说“继续”时先核对材料变化，再续做尚未完成或受影响的部分。只读讨论在对话中完成，不创建课程文件。

## 六个工作流详解

### 1. 阶段课程规划与学习路径

[curriculum-planning](skills/curriculum-planning/SKILL.md) 用于回答“接下来学什么、怎样安排、达到什么程度再继续”。适合整理多章课程母版、设计一个阶段的学习路线，或根据新学情调整后续课次。

主要功能：

- **整理标准课程母版**：从已有教材、讲义或课程目录提取章节、知识关系、先修条件、核心与拓展内容。已有成熟材料可以直接映射，不必重新编写整套课程。
- **制定班级或学生计划**：根据起点、目标、可用课次和时长，安排逐课任务、分段时间、练习方向和预期成果。已有课程、目标倒推、薄弱补强和项目驱动四类路径可按需组合。
- **设置达标与调整分支**：写清进入下一阶段需要的证据、未达标时的补强，以及稳定独立完成后的迁移或拓展；核算单课与阶段总时间。
- **根据反馈续排课程**：保留已完成课次和实际记录，只调整获准的未来或受影响安排；目标与时间冲突时明确列出取舍。

**典型交付**：标准课程总表、知识前置关系、阶段计划、逐课卡、检查与补强分支、进度调整记录；家长规划说明按需提供。缺少个人学情仍可整理标准母版，课程假设与孩子实际掌握分别记录。

**后续衔接**：选定某课后交给项目教学或备课；测评节点交给作业测评与反馈。只要求规划时，完成计划即可。

[完整自编案例](examples/curriculum-planning/README.md) · [验证记录](examples/curriculum-planning/verification.md)

### 2. 项目教学与作品验收

[project-teaching](skills/project-teaching/SKILL.md) 用于让孩子知道“今天的知识可以解决什么问题”，并在完成任务的过程中理解它。支持把已有讲义改成项目课、围绕知识点创建新课，以及验收学生已有作品。

主要功能：

- **用情境产生学习需求**：建立“功能需求 → 旧方法遇到的困难 → 新知识或机制 → 作品变化 → 解释与迁移证据”的对应关系，先预测、手算或尝试，再引入知识。
- **安排可完成的阶段版本**：将任务拆为能观察成果的小版本，说明每轮新增的功能和知识。可以是一课一个小项目、同一项目连续升级，也可以是操作实验。
- **设计教师支架与撤除过程**：区分教师提供的界面、起始代码和学生完成部分，安排从示范、补全到独立实现与迁移的过程。
- **从四个维度验收**：检查功能是否正确、能否解释过程、独立完成程度，以及能否换情境使用。作品能运行只是其中一项证据。

**适用范围**：Python 覆盖整个语法阶段及相应综合应用，包含变量、表达式、输入、条件、循环、字符串、容器、函数等；Turtle 到语法的衔接是其中一个场景。C++ 按基础语法、算法应用和综合实践的深度，补充题目契约、建模、数据范围、复杂度与程序验证。

**典型交付**：项目设计单、学生任务、阶段版本与相应完整程序、支架安排、四维验收和迁移任务；具体内容随本次授权确定。仅验收已有作品时，依据实际代码、测试与观察记录评价。

**后续衔接**：项目设计确定后交给备课细化讲稿，再按需制作课件、交互演示和课后作业；多课项目路线由阶段规划组织。

[自编充能课例](examples/project-teaching/README.md) · [开发验证](docs/project-teaching-validation.md)

### 3. 备课讲义

[lesson-preparation](skills/lesson-preparation/SKILL.md) 将 C++、Python 课程原稿整理为可直接授课的教师讲义。既支持完整备课，也支持保留现有结构的局部修订和只读审阅。

主要功能：

- **核对来源与题目**：确认课号、学生已学范围、题意、输入输出、数据范围和样例，保留原稿及课程链接。可以提炼参考讲义的结构和梳理方式用于本课。
- **建立教学主线**：按照情境、预测与观察、原理推导、方法与代码、纠错、练习迁移安排内容，给出板书和符合课时的时间分配。
- **编写可直接使用的教师讲稿**：每个核心段落包含讲解、提问、预期回答和检查点，用具体数据或状态追踪解释关键写法。
- **组织 Bug 实验与分层练习**：展示错误状态、原因、最小修复与复验；包含课堂练习、课后作业、可选拓展和参考答案，按目标项目约定折叠答案。
- **核验程序与教学内容**：结构检查和实际执行分别记录；提供显式测试清单后运行已审阅代码，图形或平台程序使用对应环境核验。

**典型交付**：保留原稿的 `-讲义版.md`、参考代码、测试清单与验收记录；需要观察动态过程时选配离线交互演示。

**后续衔接**：确定讲义可交给课件交付；单独设计作业、批改或个人学情反馈时交给测评反馈模块。讲义内常规练习由备课流程完成。

[讲义结构说明](skills/lesson-preparation/references/teaching-structure.md) · [自编讲义示例](examples/intro-loop/source-讲义版.md)

### 4. 课件交付

[courseware-delivery](skills/courseware-delivery/SKILL.md) 将已经确定的讲义或题解变成学生可看、教师可讲、可携带使用的课堂课件，也支持修改和验收已有 PPT。

主要功能：

- **设计课堂分镜**：建立来源段落、投影页、揭示步骤、教师动作、学生操作与检查点之间的映射，按项目实践或算法推导组织课堂推进。
- **区分学生屏与教师备注**：投影呈现问题、完整任务、必要图表、代码和当前状态；逐页原生备注保存讲稿、预期回答、误答追问、时间、操作与转场。
- **完成视觉与真实文件制作**：新视觉配合外部 `huashu-design` 选型，再用当前环境的制作能力交付真实 PPTX。代码、公式、数值和状态表按要求使用可编辑对象。
- **组织可携带的配套材料**：图片和音视频嵌入课件，本地演示按相对路径组织，并说明打开时机；需要时保留静态关键步骤。
- **分层验收**：分别核对内容、程序与状态、PPTX 包与备注、实际渲染、交付副本和必要的浏览器或原生播放行为。

**典型交付**：分镜、PPTX、逐页教师备注、必要附件与交付检查记录。PDF、HTML 和参考程序按本次需求提供；设计稿或缩略图不能替代真实课件验收。

**后续衔接**：可以直接接收已确定题解，无须额外生成讲义；需要动态观察时调用演示模块。外部设计与制作工具的要求见[后文](#外部设计与制作能力)。

[分镜与课件示例](examples/README.md) · [设计协作说明](skills/courseware-delivery/references/design-collaboration.md)

### 5. 竞赛与等级考试解析核验

[contest-exam-analysis](skills/contest-exam-analysis/SKILL.md) 用于把原题或整卷整理成来源可追溯、逐题完整、推导可讲、代码有验证证据的中文解析。

支持三类任务：

- **单个竞赛题目**：从题意、手算和模型出发，说明朴素方法、优化过程、不同解题视角、正确性、复杂度、易错点与参考实现。
- **GESP 一至八级整卷**：按指定年月、语言和等级核对原卷，覆盖实际题型与题量；选择题逐选项分析，判断题说明依据和反例，编程题给出完整推导与代码。
- **CSP-J / CSP-S 初赛与复赛整卷**：锁定年份、组别和轮次。初赛覆盖每个选项、小问与程序空，代码题提供执行追踪；复赛逐题给出完整解法及有教学价值的部分分方法。

**分层得分要求**：依据原题测试点、子任务分值和评分规则，建立解法、利用条件、覆盖范围、复杂度、得分依据与验证的对照表。**每个列出的解法或分层方案都配独立完整程序**，同分档的不同视角也说明实现与取舍。理论可覆盖分数、本地实测分数和待核对正式分数分别标记；不同提交程序的分数不能直接相加。

**典型交付**：Markdown 解析、逐题覆盖清单、各层完整程序、测试清单与核验记录；交互演示按难点选配。原卷识别、人工审查、编译运行和正式评测分别说明，本地通过不等于官方通过。

**后续衔接**：GESP 细项解析复用 `gesp-solver`，推导复用计算思维；确定解析可转为课件，学生实际作答可交给测评反馈。原创命题和模拟题包制作按需求使用命题能力。

[解析核验示例](examples/exam-analysis/README.md) · [多视角与分层代码规范](skills/contest-exam-analysis/references/programming-and-scores.md)

### 6. 作业测评与学情反馈

[practice-assessment-feedback](skills/practice-assessment-feedback/SKILL.md) 将学习目标转成可检查的任务，并依据实际作答、课堂观察等证据，形成具体诊断、补练和家长反馈。

主要功能：

- **设计四类任务**：本课课后作业、阶段测试、等级考试前模拟、竞赛前模拟。按目标、已学范围、时长和难度形成评价蓝图，提供学生卷与教师答案。
- **批改与核验**：逐项记录题号、知识点、评分依据、提示程度和订正状态，保留原始作答与新版本；独立完成、提示后完成、缺答和未测分别记录。
- **详细教师诊断**：对每个主要问题说明具体表现与证据、已确认原因和待确认假设、下一步教学改动、需要补练的知识关系，以及可直接使用的完整习题、提示、答案或完整程序、测试与复验标准。
- **鼓励型家长反馈**：保留学习内容、实际表现、具体亮点、需要巩固的环节、下一步和家庭配合，用委婉通俗的文字说明问题与老师的帮助安排，适合复制到微信。
- **跟进订正与阶段调整**：有新证据后更新受影响结论；需要重排多课学习进度时，再把事实和未达标目标交给阶段规划。

**可以出 GESP 或 CSP 模拟卷。** 严格对齐某次考试时先核对官方范围、题型与规则；CSP 第二轮原创/改编编程题包可交给 `csp-contest-author` 制作数据与验题，确定题目的详细解析可交给解析工作流。自编模拟卷会标明性质，不作通过率保证。

**典型交付**：学生任务、教师答案与测试、评分或达标方案、详细教师问题卡、补练与复验安排、家长文字草稿。只要求其中一部分时按本次范围交付。

只有课程材料时可以设计作业和测试；个体反馈须有相应表现证据。只有课堂观察也可写它支持的反馈，缺失事实保持待核对。家长反馈以真实表现为依据，提示后订正不会写成独立掌握；文字交给老师审核发送。

[完整自编案例](examples/practice-feedback/README.md) · [实际验证](examples/practice-feedback/verification.md)

## 四个配套能力模块怎样使用

这些是整合包内的完整技能，包含各自实际使用的参考、脚本、模板或资源。统一入口和各工作流按需读取，也可以单独指定。

| 能力模块 | 具体用途 | 常见配合方式 |
| --- | --- | --- |
| [gesp-solver](skills/gesp-solver/SKILL.md) | 对 GESP 单选的各选项、判断与编程题进行细致分析，提供等级考点参考；适用版本仍以本次官方资料为准 | 整卷解析与 GESP 模拟测评 |
| [solve-with-computational-thinking](skills/solve-with-computational-thinking/SKILL.md) | 把题目条件连接到手算、问题分解、模型、朴素方法、规律、算法、证明、复杂度和代码 | 备课、项目中的算法环节、题解与补练 |
| [interactive-algorithm-demo](skills/interactive-algorithm-demo/SKILL.md) | 制作可离线打开的单文件 HTML，用修改数据、逐步执行和代码/状态同步帮助观察过程 | 讲义、题解、课件共用同一演示；也可只做演示 |
| [csp-contest-author](skills/csp-contest-author/SKILL.md) | 命制或改编 CSP-J/S 第二轮编程题与模拟赛，提供题面、题解、标准与暴力程序、可复现数据及验题记录 | 原创/改编题包、赛前模拟与数据核验 |

## 安装：先取得固定版本，再启用

三种工具安装的是同一套 11 个完整技能，入口和调用方式各有不同。**推荐先完整安装，再在任务中按需调用。** 仅安装统一入口不会同时安装它引用的其他模块。

| 工具 | 推荐安装方式 | 安装后怎样开始 |
| --- | --- | --- |
| Codex 本地桌面版 / CLI | 将 11 个目录放入个人 `~/.agents/skills/`，或使用官方安装器暂存后启用 | 输入 `$teaching-workflows` 并描述任务 |
| Claude Code 本地环境 | 将 11 个目录放入个人 `~/.claude/skills/`；也可选项目 `.claude/skills/` | 输入 `/teaching-workflows` 并描述任务 |
| WorkBuddy | 解开整合包，将每个完整技能分别打包，通过“技能 → 添加技能 → 上传技能”导入并启用 | 在对话中明确要求使用 `teaching-workflows` |

以下宿主路径与界面说明于 **2026-10-30** 对照官方资料核对。本仓库已有本地 Codex 的实际安装记录；Claude Code、WorkBuddy 的以下步骤属于按官方机制整理的安装指引，尚未完成本套件在这两个宿主的实际导入和教学任务验证。最终以当前宿主的识别与执行结果为准。

文中的 `~` 表示当前使用者的个人主目录。Windows 文件资源管理器可用 `%USERPROFILE%\.agents\skills` 或 `%USERPROFILE%\.claude\skills` 打开对应个人位置；在 WSL 中运行工具时，使用该 Linux 环境的主目录。先确认工具实际运行在哪个环境，再复制技能。

### 1. 通用准备：下载并核对 v0.7.0

**图形界面方式：**

1. 使用有仓库访问权限的 GitHub 账号，打开 [v0.7.0 Release](https://github.com/tsetsetse/oi-teaching-workflows/releases/tag/v0.7.0)。当前为私有仓库，没有权限时无法下载。
2. 下载附件 `oi-teaching-workflows-0.7.0.zip` 和同名 `.zip.sha256`，放在同一文件夹。
3. 核对 ZIP 校验值，再解压到普通下载或暂存目录。进入能看到 `plugin.json` 和 `skills/` 的那一层，后文称为“解包目录”。
4. 查看 `skills/`：应包含总表中的 11 个完整技能目录，每个都有 `SKILL.md`。`agents/`、`references/`、`assets/`、`scripts/` 等实际资源都要保留。

macOS/Linux 可在下载文件夹中校验：

```sh
shasum -a 256 -c oi-teaching-workflows-0.7.0.zip.sha256
```

Windows PowerShell 可分别读取实际值和校验文件，对比其中的 SHA-256：

```powershell
Get-FileHash .\oi-teaching-workflows-0.7.0.zip -Algorithm SHA256
Get-Content .\oi-teaching-workflows-0.7.0.zip.sha256
```

**Git 方式：**也可使用已配置的 GitHub Git 认证，克隆固定标签到新的普通目录：

```sh
git clone --branch v0.7.0 --depth 1 \
  https://github.com/tsetsetse/oi-teaching-workflows.git oi-teaching-workflows-v0.7.0
```

使用 SSH 认证时，将仓库地址换成 `git@github.com:tsetsetse/oi-teaching-workflows.git`。不要将令牌写进命令或课程文件。可先用下列只读命令确认标签可访问；返回标签记录后再下载：

```sh
git ls-remote https://github.com/tsetsetse/oi-teaching-workflows.git refs/tags/v0.7.0
```

克隆所得目录也可作为后文的解包目录，里面的 `skills/` 内容相同。首次安装按对应宿主的步骤操作；已有同名技能时，先按[更新与回退](#更新与回退)备份，再整体替换，不直接合并旧目录。

**运行能力另外准备：**安装技能目录本身不需要编译器；运行本套件 Python 检查脚本需 Python 3.10+，运行 C++ 用例需对应编译器，交互模板自检需 Node.js。PPT、PDF、浏览器与设计能力见[外部设计与制作能力](#外部设计与制作能力)。

### 2. 在 Codex 中安装

**方式 A：复制完整技能目录，适合已下载整合包的使用者。**

1. 打开个人主目录下的 `.agents/skills/`，不存在就创建。macOS 可在 Finder“前往文件夹”中输入 `~/.agents/skills/`。
2. 把解包目录 `skills/` **里面的 11 个文件夹**整体复制到该位置。最终结构应为：

   ```text
   ~/.agents/skills/
     teaching-workflows/SKILL.md
     curriculum-planning/SKILL.md
     project-teaching/SKILL.md
     lesson-preparation/SKILL.md
     courseware-delivery/SKILL.md
     contest-exam-analysis/SKILL.md
     practice-assessment-feedback/SKILL.md
     gesp-solver/SKILL.md
     solve-with-computational-thinking/SKILL.md
     interactive-algorithm-demo/SKILL.md
     csp-contest-author/SKILL.md
   ```

3. 对照解包目录核对全部文件，保留各技能配套资源。不要多套一层 `skills/skills/`，也不要只复制 11 份 `SKILL.md`。
4. 在 Codex 打开日常课程项目，新对话中输入 `$teaching-workflows` 并执行下文的只读试用。技能未出现时重启 Codex，再检查层级、禁用配置与同名重复安装。

Codex 官方支持个人 `~/.agents/skills/` 与项目 `.agents/skills/`；只在一个课程项目使用时，可选择项目位置。按当前环境选定一个有效位置，避免同时启用同名副本；已有 `CODEX_HOME` 或历史别名的环境先核对实际发现位置。[Codex 官方技能说明](https://learn.chatgpt.com/docs/build-skills)

**方式 B：让 Codex 使用官方安装器，适合直接从 GitHub 取得固定版本。**

可以把下面这段任务交给 Codex：

> 使用 $skill-installer，从 tsetsetse/oi-teaching-workflows 的 v0.7.0 取得 README 列出的全部 11 个 skills 目录。先安装到新建的临时目录，核对资源完整性，再安装到当前环境实际发现的个人技能目录。已有同名技能先核对差异并完整备份到技能发现目录之外，保留自定义修改及原有别名关系；不要直接覆盖或合并旧目录。完成后报告版本、安装位置、备份位置和实际核验结果。

<details>
<summary>展开：macOS/Linux 官方安装器命令</summary>

官方安装器通常随 Codex 的系统技能提供；若文件不存在，让 Codex 定位当前 `skill-installer` 脚本。下面先写入空的暂存目录，不直接启用或覆盖旧安装：

```sh
workflow_installer="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py"
workflow_stage="$(mktemp -d /tmp/oi-teaching-install.XXXXXX)"
python3 "$workflow_installer" \
  --repo tsetsetse/oi-teaching-workflows \
  --ref v0.7.0 \
  --method git \
  --dest "$workflow_stage" \
  --path \
    skills/teaching-workflows \
    skills/curriculum-planning \
    skills/project-teaching \
    skills/lesson-preparation \
    skills/courseware-delivery \
    skills/contest-exam-analysis \
    skills/practice-assessment-feedback \
    skills/gesp-solver \
    skills/solve-with-computational-thinking \
    skills/interactive-algorithm-demo \
    skills/csp-contest-author
```

`--method git` 使用已有 Git 认证，HTTPS 失败后安装器会尝试 SSH。检查暂存内容后，把其中 11 个完整目录按方式 A 启用；不是把暂存目录本身复制进 `skills/`。

官方安装器遇已有同名目录会停止，多目录失败不保证自动撤回先前复制的目录。失败时检查暂存内容，修正问题后换一个空目录重试。

</details>

### 3. 在 Claude Code 中安装

**个人安装，适合在多个教学项目中复用：**

1. 按通用准备取得 v0.7.0，打开个人主目录下的 `.claude/skills/`，不存在就创建。
2. 把解包目录 `skills/` 里面的 11 个完整技能文件夹复制进去；已有同名目录先备份。最终入口应为 `~/.claude/skills/teaching-workflows/SKILL.md`，其余十个与它同级。
3. 在 Claude Code 中打开自己的课程项目，开始新会话。
4. 输入下列任务，检查是否读取入口和所选模块：

   ```text
   /teaching-workflows 只读检查当前项目规则和我指定的课程原稿，说明应进入哪个工作流、还缺什么材料；暂不写文件。
   ```

5. 需要单独调用时使用 `/lesson-preparation`、`/project-teaching` 等对应名称，再描述本次目标。未识别时核对目录和名称，重新启动会话，并检查组织策略是否限制自定义技能。

**只给一个项目使用：**改为复制到课程项目根目录的 `.claude/skills/`，例如 `<课程项目>/.claude/skills/teaching-workflows/SKILL.md`；其他技能同级放置。个人与项目安装选一种即可。

以上采用 Claude Code 官方的个人/项目技能目录与 `/技能名` 调用方式；本机个人安装不等于 Claude 网页、Cowork 或云端会话已经启用。本仓库的 portable `plugin.json` 也不是 Claude Code 插件安装声明，本节按技能目录安装。[Claude Code 官方技能说明](https://code.claude.com/docs/en/skills)

### 4. 在 WorkBuddy 中安装

本节使用 WorkBuddy 的**本地技能包上传**，不要求先把私有仓库发布到技能市场。官方入口为“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”；对话中的“查找技能”面向技能市场，不能代替自有包上传。[WorkBuddy 官方技能说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

**先准备单技能包：**本仓库 Release ZIP 的根目录是 `plugin.json` 与 `skills/`，属于多技能整合包。先解开它，再将 `skills/` 下每个完整技能分别打成 ZIP，避免把 portable 整合包直接当作一个技能上传。每个单技能 ZIP 根部放该技能的 `SKILL.md` 及全部配套资源，结构例如：

```text
teaching-workflows.zip
  SKILL.md
  agents/
  assets/
```

其他技能保留各自实际资源，不照抄上面两个子目录的名称。技能的定义与配套资源结构可参照 [WorkBuddy 官方开发说明](https://open.workbuddy.cn/docs/skill)；本节是个人导入，未包含向市场发布所需的展示资料或审核流程。

<details>
<summary>展开：用 Python 一次准备 11 个单技能 ZIP</summary>

在刚下载解开的干净目录中运行以下命令（能看到 `skills/` 的那一层），需要 Python 3.10+。下面的终端写法适用于 macOS/Linux；Windows 可将 `from pathlib` 到 `print(...)` 的 Python 正文保存为解包目录中的 `package_workbuddy.py`，在该目录用 PowerShell 运行 `py -3 package_workbuddy.py`。命令只创建 `workbuddy-skill-zips-v0.7.0/`，不改动技能，不安装到 WorkBuddy；同名输出目录已存在时会停止，避免覆盖：

```sh
python3 - <<'PYCODE'
from pathlib import Path
from shutil import make_archive

source = Path("skills")
skills = sorted(p for p in source.iterdir() if (p / "SKILL.md").is_file())
if len(skills) != 11:
    raise SystemExit("应有 11 个技能，请确认当前目录和 v0.7.0 包是否完整")
output = Path("workbuddy-skill-zips-v0.7.0")
output.mkdir()
for skill in skills:
    print(make_archive(str(output / skill.name), "zip", root_dir=skill))
PYCODE
```

仅对干净发行副本打包，避免混入本机运行缓存或个人文件。生成的 ZIP 保留全部技能内容；这一步的文件检查不能证明 WorkBuddy 已接受该包。

</details>

**导入与启用：**

1. 打开 WorkBuddy，进入“专家·技能·连接器 → 技能”。
2. 点击“添加技能 → 上传技能”，选择一个单技能 ZIP，按照当前界面的检测与提示完成导入。
3. 对其余技能重复操作，在“已安装”中逐项核对总表的 11 个名称及启用状态。已有同名版本时先保留旧副本和自定义内容，再按宿主提供的更新方式处理，避免重复版本。
4. 打开课程工作空间，将要处理的材料放在可访问位置，开始新任务并明确调用入口：

   > 请使用已安装的 teaching-workflows 编程教学工作台，只读检查当前工作空间规则和我指定的课程原稿，说明应进入哪个工作流；暂不创建或修改文件。

5. 核对是否实际读取入口、所选模块和相对资源。若当前版本导入失败，记录宿主版本及具体报错，核对 ZIP 层级、元数据和资源，再适配暂存副本重试；保留固定版本原包。不要把失败步骤记成已安装。

本仓库尚未实测 WorkBuddy 的整套导入与自动衔接，不把 CodeBuddy CLI 的目录规则当作 WorkBuddy 桌面安装规则，也不假定 `$技能名` 或 `/技能名` 与其他工具通用。以“已安装”状态和实际只读试用共同判断是否可用。

### 5. 安装后核验与常见问题

三种宿主均按以下层次检查：

1. **文件完整**：11 个完整技能与固定版本副本逐文件一致，入口层级正确，同名旧目录和别名已处理。
2. **宿主识别**：新对话或新任务能够读取入口及所选模块，遵守只读范围，识别正确课程材料。
3. **小任务可执行**：用一个自编小课例试用，再按需要验证代码执行、浏览器演示、PPT 等具体能力。看到技能名称不代表教学任务已经跑通。

有对应运行环境时，可对安装副本做两项配套自检；将 `<技能安装根目录>` 替换为实际包含 11 个技能的目录：

```sh
node "<技能安装根目录>/interactive-algorithm-demo/assets/prefix-sum.test.cjs"
python3 "<技能安装根目录>/csp-contest-author/scripts/audit_package.py" --self-test
```

缺少 Node.js 时将交互自检记为未测。以上分别覆盖模板算法与题包结构，不证明浏览器、真实试卷或全部教学结果正确。记录固定标签、安装位置、备份位置、实际核验和未测项目；确认成功前保留暂存副本。

| 现象 | 优先检查 |
| --- | --- |
| GitHub 显示 404 或下载失败 | 是否登录有权账号、私有仓库权限、网络与 Git 认证，避免用公开下载假设判断 |
| 能看到入口，提示缺少模块 | 是否完整安装了其余十个技能，名称、启用状态和相对资源是否正确 |
| 复制后没有出现技能 | 是否多套目录、只复制了说明文件、放错宿主位置或被配置禁用；开启新会话重查 |
| 可以备课，不能生成 PPT 或打开演示 | 当前宿主是否提供相应设计/制作/浏览器工具，以及所需运行环境 |
| 同一技能出现多个版本 | 清点个人、项目、别名和导入副本，只保留本次计划启用的版本，先备份再处理 |

## 日常使用与按需衔接

### 怎样描述任务

日常优先使用统一入口，在请求中提供**要做的事、材料、学生基础、课时、输出位置和本次范围**。已经确认的信息可以直接沿用；未知事实保持待确认。将下列例子的调用前缀换成当前工具对应的形式：

| 工具 | 调用写法 |
| --- | --- |
| Codex | `使用 $teaching-workflows，……` |
| Claude Code | `/teaching-workflows ……` |
| WorkBuddy | `请使用已安装的 teaching-workflows 编程教学工作台，……` |

例如在 Codex 中：

> 使用 $teaching-workflows，根据指定 Python 变量原稿，为四年级、学过简单循环和初步变量的孩子设计 90 分钟项目课。让变量解决项目中的具体问题，保留原稿，输出到当前课程目录。先在对话中给完整方案，暂不写文件。

方案确认后可直接说：

> 按刚才确认的项目方案开始实施，保留原稿，完成本次讲义、阶段程序和验收记录。

### 常用调用示例

| 本次需要 | 示例任务内容（接在对应调用前缀之后） |
| --- | --- |
| 阶段规划 | 根据课程目录安排六次 90 分钟的学习路径，列出逐课任务、先修、达标检查与未达标分支；本次只做计划。 |
| 普通备课 | 把这篇 C++ 原稿整理成 120 分钟教师讲义，保留原稿，包含状态追踪、Bug 修复、课堂练习、作业和可选拓展。 |
| 项目课与验收 | 将本课 Python 变量讲义改为情境项目课，说明每个版本的新需求和教师支架，安排解释与独立迁移；依据实际代码验收已有作品时，只评价有证据的部分。 |
| 课件交付 | 根据已确定讲义制作课堂 PPTX，保留完整任务、代码与状态对应，配齐逐页教师备注；新视觉按设计协作流程选型。 |
| 整卷解析 | 根据我指定年月与等级的 GESP 原卷完成整卷解析，逐选项说明；编程题各分层方案给独立完整程序，按原测试点规则论证得分并分别验证。 |
| 模拟测评 | 按指定 GESP 等级或 CSP-J/S 组别、轮次和当前适用规则设计模拟卷，说明已核对的范围，提供学生卷、教师答案、评分依据和验证记录。 |
| 学情反馈 | 根据本次实际作答和课堂观察，逐个分析具体问题，给出详细补练题、答案和复验安排，再写鼓励为主的家长草稿。 |
| 只做交互 | 为已确定的前缀和代码制作离线演示，可修改数据、逐步观察代码与状态；本次只交付演示及检查记录。 |
| 续做 | 读取上次产物和任务记录，核对来源变化，继续未完成部分；已通过且未变化的成果沿用。 |

已知要使用哪个模块时，可以直接调用。Codex 使用 `$lesson-preparation` 等名称，Claude Code 使用 `/lesson-preparation`，WorkBuddy 在对话中明确指定已安装模块即可。独立调用仍遵守对应技能的范围和验收要求。

### 多个工作流怎样衔接

各模块按本次目标组合。常见路线如下，后续步骤只在需要相应交付时进入：

| 场景 | 衔接方式 | 交接的主要内容 |
| --- | --- | --- |
| 一个阶段的项目课程 | 阶段规划 → 选定单课的项目教学 → 备课 → 课件 → 作业与反馈 | 逐课目标、时间、已学范围、项目版本和达标标准 |
| 一篇日常讲义 | 备课 → 课件，难点处选配交互 | 确定讲义、完整题面、代码、状态、演示打开时机 |
| 一份竞赛试卷 | 解析核验 → 课件或交互 → 有实际作答后的反馈 | 原卷身份、题号清单、各层代码、评分依据和测试证据 |
| 一次赛前模拟 | 测评蓝图 → 按需命题与验题 → 解析 → 实际作答后的诊断补练 | 目标范围、时长、难度、学生卷、数据、评分与作答 |
| 根据学情调整后续学习 | 测评反馈 → 阶段规划 → 获准修改的后续课程 | 具体表现、提示程度、未达标关系、已完成课次和可调整时间 |

例如，可以先完成一个阶段计划；确认后说“把第 3 课做成项目课并写成教师讲义”；再说“基于已确定讲义制作 PPT”；课后提供实际记录，让入口生成诊断和家长反馈。跨阶段沿用同一来源、代码和进度，不必每次重新说明全部背景。

只修改演示时直达演示模块；仅要题解时停在解析；只要求家长文字时按已有证据写草稿。新视觉选择沿用有效确认记录，来源或代码变化时复核受影响部分。任务记录和课程产物保存到日常教学项目，技能目录与源码仓库只保存可复用能力。

## 可选：让指定教学项目优先使用统一入口

安装后可以显式调用，也可能按描述自动匹配。若希望某个教学项目优先使用统一入口，可将以下约定合并到该宿主实际读取的项目指令中：Codex 使用项目 `AGENTS.md`；Claude Code 可放入项目 `CLAUDE.md`；WorkBuddy 使用当前工作空间提供的项目指令配置。保留已有规则，不覆盖整份文件，也不假定三个工具读取同一种文件。

```markdown
## 编程教学工作流

在本项目进行阶段课程规划、知识点情境化与项目教学、作品验收、编程备课、课件制作、竞赛/等级考试解析、作业测评与学情反馈，或续做相关任务时，优先读取可用的 teaching-workflows 统一入口，再按本次目标选用模块。用户明确指定某个专门技能时遵从该选择。只读讨论不写文件，课程材料和产物保存在本项目。与教学无关的任务不启用该流程。
```

技能也会要求读取目标项目适用的 `AGENTS.md`。若 Claude Code 项目已有该文件，可在同级 `CLAUDE.md` 中加入 `@AGENTS.md` 导入，再补充必要的宿主约定，复用现有规则并避免两处冲突。具体加载方式以当前版本与配置为准，见 [Claude Code 项目指令官方说明](https://code.claude.com/docs/en/memory)。

这是项目范围的引导，仍需验证触发与执行。套件没有安装全局会话钩子，也不会修改所有项目的规则；不承诺隐式匹配每次都进入入口。其他项目指令、定时任务和外部发布按后续明确需求配置。

## 外部设计与制作能力

四项自有能力完整打包；`huashu-design`、Obsidian、PPT/PDF制作与浏览器能力按宿主环境另行提供。只有需要相应阶段时读取，不假称它们已经内嵌。

新课件视觉设计必须配合可用的 `huashu-design`：展示候选缩略图和三个方向各两页真实代表页，选定后再展开整套；已有有效方向沿用。缺少能力时完成可做的规划并说明受影响阶段。详见[设计协作与制作衔接](skills/courseware-delivery/references/design-collaboration.md)。套件不自动安装第三方技能、发布到OJ、同步GitHub或创建定时任务，这些动作需有相应用户授权。

## 更新与回退

1. 用新固定标签先取得空的暂存副本，核对该版本的全部技能和所需资源（v0.7.0为十一个）；不要移动已发布标签，也不要用 `main` 代替安装版本。
2. 清点实际发现目录中的同名目录与别名，检查原技能是否有自定义修改。完整备份受影响旧目录到发现目录以外，例如 `~/.agents/skill-backups/oi-teaching-workflows/<日期>-<旧版本>/`；记录真实目标和别名关系。不要把备份留在 `skills/` 内以免被再次发现。
3. 将对应旧目录移出发现位置，再复制完整新目录，逐文件核对。保留其他技能与系统技能；不要删除或合并整个个人技能目录。失败时移出已放入的新版目录，恢复本次备份和别名。
4. 在新对话中完成只读入口检查和小课例；确认后保留版本及安装记录。版本标签、源码仓库、个人安装分别核对，不能把推送成功当作安装完成。
5. 回退时同样先保留当前安装，再恢复旧版完整备份或重新安装旧标签；复核别名与入口可用性，不覆盖当前课程成品。

## 源码、整合ZIP与开发验证

需要维护源码或构建整合包时，另克隆固定标签到技能目录之外：

```sh
git clone --branch v0.7.0 --depth 1 \
  https://github.com/tsetsetse/oi-teaching-workflows.git oi-teaching-workflows-v0.7.0
cd oi-teaching-workflows-v0.7.0
python3 scripts/build_bundle.py --output dist/oi-teaching-workflows-0.7.0.zip
```

ZIP采用根 `plugin.json` 与 `skills/` 的portable插件布局，含十一个完整技能、整包说明、逐文件哈希清单，旁置整个ZIP的SHA-256。它用于整包携带与支持该格式宿主的后续测试；**生成或下载ZIP不等于宿主已加载/启用**。个人技能安装与portable插件宿主加载分别核验，不把后者列为已通过。[官方打包说明](https://developers.openai.com/plugins/build/plugins)

在macOS/Linux可核对整个ZIP：

```sh
cd dist
shasum -a 256 -c oi-teaching-workflows-0.7.0.zip.sha256
```

开发检查从源码仓库根目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 skills/lesson-preparation/scripts/check_lesson.py \
  examples/intro-loop/source-讲义版.md --cases examples/intro-loop/cases.json
python3 skills/lesson-preparation/scripts/check_lesson.py \
  examples/project-teaching/lesson.md --cases examples/project-teaching/cases.json
python3 skills/contest-exam-analysis/scripts/check_inventory.py \
  examples/exam-analysis/inventory-mini.json
python3 skills/contest-exam-analysis/scripts/check_inventory.py \
  examples/exam-analysis/inventory-pairs.json
node skills/interactive-algorithm-demo/assets/prefix-sum.test.cjs
python3 skills/csp-contest-author/scripts/audit_package.py --self-test
```

讲义检查器不传 `--cases` 只做结构检查；传测试清单才执行已审阅程序。清单工具只检查人工题号和本地文件关系，不读原卷、不执行程序或计算得分；PPT包检查不替代实际渲染/播放。静态检查、实际运行、人工审查与未测范围分别报告。

```text
skills/teaching-workflows/  统一入口、元数据与任务进度模板
skills/curriculum-planning/ 阶段课程路径与实施计划（v0.6.0）
skills/project-teaching/   知识点情境化、项目课与作品验收（v0.7.0）
skills/practice-assessment-feedback/ 作业测评与两版反馈
skills/<其他模块>/         三个工作流及四项完整自有能力
scripts/build_bundle.py     标准库整合包构建器
examples/                  自编课程规划、讲义、课件与考试/测评验证案例
tests/                     检查器与构建器测试
docs/                      实施计划与验证记录
.local/                    本机安装、真实课程试运行记录（忽略，不提交）
dist/                      构建归档（忽略，不自动随Git提交）
```

整包内容见[BUNDLE.md](BUNDLE.md)，开发证据见[项目教学验证](docs/project-teaching-validation.md)，本版发布与安装证据见[v0.7.0验证记录](docs/v0.7.0-release-validation.md)；早期统一入口见[验证记录](docs/unified-entry-validation.md)，教学样例见[示例与验证](examples/README.md)。真实学生信息、密钥、付费课程与整套日常成品不进入源码仓库。

当前以私有仓库维护，未选择公开许可证。四项自有技能按用户授权纳入，第三方扩展未被自动复制或重新授权；课程材料的权利单独处理。
