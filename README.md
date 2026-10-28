# OI Teaching Workflows

面向青少儿 C++、Python 教学的工作流套件。通过 **编程教学工作台 `teaching-workflows`** 统一发起备课、课件交付与竞赛/等级考试解析，按需读取配套 Skills。

`v0.4.0` 包含 **1个统一入口＋3个专门工作流＋4个完整能力模块**，共八个技能目录。统一入口组织流程，各模块保留独立调用。工作流源码、已安装技能和课程材料分别保存；同步 GitHub 不会自动更新本机技能，也不会改动课程。

| 模块 | 职责 |
| --- | --- |
| **`teaching-workflows` 编程教学工作台** | 判断任务、确定范围、安排交接、读取进度与续做 |
| `lesson-preparation` 备课讲义 | 来源核对、教学主线、教师讲稿、练习/作业/拓展、程序验收 |
| `courseware-delivery` 课件交付 | 从确定讲义或解析制作分镜、PPTX、原生教师备注与验收 |
| `contest-exam-analysis` 竞赛与等级考试解析核验 | 单题、GESP一至八级、CSP-J/S初复赛逐题解析，多视角与分层完整代码 |
| `gesp-solver` | GESP逐选项、判断与编程题分析及等级考点参考 |
| `solve-with-computational-thinking` | 题意、建模、朴素方法、算法选择、证明、复杂度和代码推导 |
| `interactive-algorithm-demo` | 可修改数据、逐步执行、代码与状态同步的离线HTML演示，附模板和自检 |
| `csp-contest-author` | 命题、改编、组卷、数据与验题包；正式原卷题解由解析工作流负责 |

## 安装：先取得固定版本，再启用

以下为 **macOS/Linux、本地 Codex 的个人技能安装路径**。有本地文件权限的 Codex 是本仓库实际验证的使用环境。普通 ChatGPT 对话不会因为 GitHub 中存在这些文件就能访问本机课程；插件宿主加载是另一条途径，见后文。

### 1. 准备环境与仓库权限

- 本机提供 Python 3.10+ 和 Git，Codex 能读取目标教学项目。
- 当前仓库为私有仓库，安装账号需要访问权限。先配置 GitHub 的 Git 认证；不要把令牌写进命令、README、课程或技能文件。
- 个人技能推荐位置为 `~/.agents/skills/`；实际使用其他发现目录或设置过 `CODEX_HOME` 时，先确认当前环境的路径。只启用一份同名技能。[官方技能说明](https://learn.chatgpt.com/docs/build-skills)
- 运行C++用例另需对应编译器，交互模板自检需要Node.js；这些不是“发现技能”的前置条件。

可用只读命令确认固定标签可访问：

```sh
git ls-remote https://github.com/tsetsetse/oi-teaching-workflows.git refs/tags/v0.4.0
```

若本机使用SSH认证，可改用下列预检；官方安装器的Git方式会先尝试HTTPS，失败后尝试SSH：

```sh
git ls-remote git@github.com:tsetsetse/oi-teaching-workflows.git refs/tags/v0.4.0
```

任一方式返回标签记录即可继续。两种方式都失败时，根据Git返回的信息核对网络、仓库访问权限和对应认证；无记录但没有报错时核对该标签是否存在。

### 2. 用官方安装器把八个目录装到空的暂存位置

可以直接给 Codex 下面这段任务：

> 使用 $skill-installer，从 tsetsetse/oi-teaching-workflows 的 v0.4.0 取得 README 列出的全部八个 skills 目录。先安装到新建的临时目录，核对资源完整性，再安装到当前环境实际发现的个人技能目录。已有同名技能先核对差异并完整备份到技能发现目录之外，保留自定义修改及原有别名关系；不要直接覆盖或合并旧目录。完成后报告版本、安装位置、备份位置和实际核验结果。

命令方式如下。官方安装器通常随 Codex 的系统技能提供；若该文件不存在，让 Codex 定位当前 `skill-installer` 的实际脚本，不把下面路径当作所有宿主的固定路径。

```sh
workflow_installer="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py"
workflow_stage="$(mktemp -d /tmp/oi-teaching-install.XXXXXX)"
python3 "$workflow_installer" \
  --repo tsetsetse/oi-teaching-workflows \
  --ref v0.4.0 \
  --method git \
  --dest "$workflow_stage" \
  --path \
    skills/teaching-workflows \
    skills/lesson-preparation \
    skills/courseware-delivery \
    skills/contest-exam-analysis \
    skills/gesp-solver \
    skills/solve-with-computational-thinking \
    skills/interactive-algorithm-demo \
    skills/csp-contest-author
```

`--method git` 使用已有Git认证，避免把私有仓库令牌写进安装步骤。暂存目录应出现上述八个完整文件夹，每个都有 `SKILL.md`；保留其 `agents/`、`references/`、`assets/`、`scripts/` 等实际资源，不能只复制八份说明文件。安装命令失败时检查暂存内容，修正后换一个空目录重试。

官方安装器遇已有同名目录会停止；多目录安装不保证失败时自动撤回先前复制的目录。因此先暂存、后启用，不直接用它覆盖正在使用的旧版。

### 3. 核对暂存资源，完成首次安装或升级

先查看八个目录及其 `SKILL.md`，并可执行包内两项自检：

```sh
node "$workflow_stage/interactive-algorithm-demo/assets/prefix-sum.test.cjs"
python3 "$workflow_stage/csp-contest-author/scripts/audit_package.py" --self-test
```

缺少 Node.js 时保留交互自检为未测，不能记作失败或已通过。上述自检分别覆盖模板算法与题包结构，不证明浏览器、真实试卷或全部教学结果正确。

**首次安装：**确认个人技能目录中没有这八个同名目录或别名后，将暂存目录里的八个文件夹整体复制进去。例如最终应是 `~/.agents/skills/teaching-workflows/SKILL.md`，而不是 `~/.agents/skills/skills/teaching-workflows/SKILL.md`。不要把整个仓库放进去，也不要用指向开发源码的软链接代替固定版本副本。

**升级已有安装：**按“更新与回退”处理；若已有个人定制版，先保留差异，再决定如何并入新版本。不要把暂存文件夹直接合并到旧文件夹，否则旧版本删除的资源可能残留。

复制后逐文件比对暂存与目标的内容，确认八个技能及其全部资源一致。记录固定标签/提交、安装位置、文件校验结果、备份位置与尚未完成的检查。暂存副本在确认安装成功前保留。

### 4. 在教学项目中验证入口

打开或切换到保存课程材料的项目，开始新对话，调用：

> 使用 $teaching-workflows，只读检查当前项目的规则和我指定的这篇原稿，说明应该进入哪个流程、还缺什么材料；暂不写文件。

成功标准：实际读取统一入口与所选模块，识别正确材料，遵守只读范围。能看到技能名称不等于已跑通教学任务。没有发现技能时重启 Codex，再检查安装层级、实际发现目录、禁用配置与同名重复安装。[官方发现与调用说明](https://learn.chatgpt.com/docs/build-skills)

确认入口可用后，再用一个小课例验证制作与验收。仓库的自编示例可以用于试用，真实课程与成品继续保存在日常教学项目。

## 日常使用与按需衔接

统一入口可以这样使用：

> 使用 $teaching-workflows，把这篇C++原稿整理成120分钟教师讲义，保留原稿，并按难点配交互演示。

> 使用 $teaching-workflows，根据指定GESP原卷完成整卷解析，逐选项说明；编程题给出各层得分方案的独立完整程序并分别验证。

> 使用 $teaching-workflows，把已确定的题解转成40分钟课堂PPT，配齐逐页教师备注。

> 使用 $teaching-workflows，读取上次产物和检查记录，核对来源变化，继续尚未完成的部分。

只读、仅规划、制作与局部修改按本次请求区分；只修改演示时直达演示模块，不附带重做讲义/PPT。原稿到讲义再到课件、原题到解析再到课件按需要串联；不要求题解转PPT时先另写一份讲义。三个专门工作流及四项能力仍支持直接指定。

创建/修改时沿用已有任务记录；跨流程缺记录时，统一入口可在本次输出目录使用[任务进度模板](skills/teaching-workflows/assets/progress-template.md)。记录来源、依赖版本、当前阶段、检查证据、未完成项和有效视觉选择。只读时在对话中报告，不创建记录文件。说“继续”后先比对来源与产物，只重验受影响部分。

讲义默认包含教学目标与前置知识、板书与课时、逐段讲稿、课堂练习、课后作业、可选拓展与易错点，按课程合并无关环节。详见[备课结构](skills/lesson-preparation/references/teaching-structure.md)。
竞赛解析按原卷实际题量和评分，逐题/逐小问覆盖；每个被列为解法或分层方案的方法都有独立完整代码，区分理论覆盖、本地实测和未知正式分数。见[解析核验示例](examples/exam-analysis/README.md)。
课件默认交付真实PPTX、原生教师备注与验收记录，PDF/HTML按需求；HTML设计稿和静态渲染不能替代实际课件验收。

## 可选：让指定教学项目优先使用统一入口

个人技能安装后可显式调用，也可能按描述自动匹配；安装本身不保证每个对话先进入工作台。若希望在某个教学项目优先使用它，可将以下约定合并进该项目现有 `AGENTS.md`，保留原有规则，不覆盖整份文件：

```markdown
## 编程教学工作流

在本项目进行编程备课、课件制作、竞赛/等级考试解析，或续做相关任务时，优先读取可用的 teaching-workflows 统一入口，再按本次目标选用模块。用户明确指定某个专门技能时遵从该选择。只读讨论不写文件，课程材料和产物保存在本项目。与教学无关的任务不启用该流程。
```

这是项目范围的引导，仍需在当前环境验证触发与执行。套件没有安装全局会话钩子，也不会修改所有项目的规则；不承诺隐式匹配必达。

## 外部设计与制作能力

四项自有能力完整打包；`huashu-design`、Obsidian、PPT/PDF制作与浏览器能力按宿主环境另行提供。只有需要相应阶段时读取，不假称它们已经内嵌。

新课件视觉设计必须配合可用的 `huashu-design`：展示候选缩略图和三个方向各两页真实代表页，选定后再展开整套；已有有效方向沿用。缺少能力时完成可做的规划并说明受影响阶段。详见[设计协作与制作衔接](skills/courseware-delivery/references/design-collaboration.md)。套件不自动安装第三方技能、发布到OJ、同步GitHub或创建定时任务，这些动作需有相应用户授权。

## 更新与回退

1. 用新固定标签先取得空的暂存副本，核对八个技能和所需资源；不要移动已发布标签，也不要用 `main` 代替安装版本。
2. 清点实际发现目录中的同名目录与别名，检查原技能是否有自定义修改。完整备份受影响旧目录到发现目录以外，例如 `~/.agents/skill-backups/oi-teaching-workflows/<日期>-<旧版本>/`；记录真实目标和别名关系。不要把备份留在 `skills/` 内以免被再次发现。
3. 将对应旧目录移出发现位置，再复制完整新目录，逐文件核对。保留其他技能与系统技能；不要删除或合并整个个人技能目录。失败时移出已放入的新版目录，恢复本次备份和别名。
4. 在新对话中完成只读入口检查和小课例；确认后保留版本及安装记录。版本标签、源码仓库、个人安装分别核对，不能把推送成功当作安装完成。
5. 回退时同样先保留当前安装，再恢复旧版完整备份或重新安装旧标签；复核别名与入口可用性，不覆盖当前课程成品。

## 源码、整合ZIP与开发验证

需要维护源码或构建整合包时，另克隆固定标签到技能目录之外：

```sh
git clone --branch v0.4.0 --depth 1 \
  https://github.com/tsetsetse/oi-teaching-workflows.git oi-teaching-workflows-v0.4.0
cd oi-teaching-workflows-v0.4.0
python3 scripts/build_bundle.py --output dist/oi-teaching-workflows-0.4.0.zip
```

ZIP采用根 `plugin.json` 与 `skills/` 的portable插件布局，含八个完整技能、整包说明、逐文件哈希清单，旁置整个ZIP的SHA-256。它用于整包携带与支持该格式宿主的后续测试；**生成或下载ZIP不等于宿主已加载/启用**。本版验证的是个人技能暂存安装和解包资源，不把portable插件宿主加载列为已通过。[官方打包说明](https://developers.openai.com/plugins/build/plugins)

在macOS/Linux可核对整个ZIP：

```sh
cd dist
shasum -a 256 -c oi-teaching-workflows-0.4.0.zip.sha256
```

开发检查从源码仓库根目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 skills/lesson-preparation/scripts/check_lesson.py \
  examples/intro-loop/source-讲义版.md --cases examples/intro-loop/cases.json
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
skills/<其他模块>/         三个工作流及四项完整自有能力
scripts/build_bundle.py     标准库整合包构建器
examples/                  自编讲义、课件分镜和试卷解析验证案例
tests/                     检查器与构建器测试
docs/                      实施计划与验证记录
.local/                    本机安装、真实课程试运行记录（忽略，不提交）
dist/                      构建归档（忽略，不自动随Git提交）
```

整包内容见[BUNDLE.md](BUNDLE.md)，本版实施证据见[统一入口验证记录](docs/unified-entry-validation.md)；早期整合验证见[七模块开发包记录](docs/bundle-validation.md)，教学样例见[示例与验证](examples/README.md)。真实学生信息、密钥、付费课程与整套日常成品不进入源码仓库。

当前以私有仓库维护，未选择公开许可证。四项自有技能按用户授权纳入，第三方扩展未被自动复制或重新授权；课程材料的权利单独处理。
