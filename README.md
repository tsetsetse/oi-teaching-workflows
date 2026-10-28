# OI Teaching Workflows

面向青少儿 C++、Python 教学的 ChatGPT / Codex 工作流。源码独立维护，课程资料和成品留在日常教学项目。

工作流分别负责备课与课件交付：

| 工作流 | 用途 | 当前状态 |
| --- | --- | --- |
| **备课讲义 `lesson-preparation`** | 从原稿组织来源核对、教学设计、讲义与程序验收 | v0.2.0，细化教学结构、推导与 Bug 实验 |
| **课件交付 `courseware-delivery`** | 从确定讲义组织投影、教师备注、必要演示与实际成品验收 | v0.2.0 首次发布；完整制作链仍待真实课程试用 |

当前版本为 `v0.2.0`，两个工作流分别安装。竞赛题解与定时任务留待后续需求；源码同步不会自动更新个人技能安装。

```text
GitHub ↔ 工作流源码仓库
               ↓ 安装确定版本的副本
        Codex 个人技能目录
               ↓ 在教学项目调用
      读取原稿 → 整理讲义 → 验收 → 保存成品
```

## 日常使用

先安装技能，然后在 **ObsidianDocs 等教学项目**中发起任务：

> 使用 $lesson-preparation，把第63课原稿整理成120分钟讲义。保留原稿，按本项目规则完成必要验收。

只希望先看建议时：

> 使用 $lesson-preparation，只读审阅第63课，展示教学主线和修改建议，暂不写任何课程文件。

已有进度时：

> 使用 $lesson-preparation，读取这节课的现有讲义和检查记录，核对来源变化，继续尚未完成的工作。

创建讲义默认另存同目录的 `原文件名-讲义版.md`。工作流读取目标项目规则，沿用学生知识范围、完整题面、原始链接、嵌入和笔记格式；缺关键条件时标明待核对。
普通 ChatGPT 对话如果不能访问本地项目，需要提供相关原稿和规则；不能据此声称已读写本机文件。本版实际执行与验证入口是具备本地文件权限的 Codex。

课件交付的源码位于 [courseware-delivery](skills/courseware-delivery/SKILL.md)，可明确指定该文件试用。安装后可这样调用：

> 使用 $courseware-delivery，根据已确定的本课讲义制作40分钟课堂PPT，配齐逐页教师备注，按教学需要安排预测、状态追踪和Bug修复，完成成品验收。

只规划时注明“本次仅做逐页分镜与验收计划，不生成课件”。默认成品是 PPTX、教师备注与必要记录；PDF、HTML和参考程序按本次需求提供。验收分别报告内容与代码、包结构、实际渲染、复制件和必要的交互/播放检查。

课件按学习目标选择[项目实践型或算法推导型](skills/courseware-delivery/references/teaching-paths.md)：前者围绕作品逐步完善并展示解释，后者围绕同一任务从旧方法推导改进并反复验证。两类都记录改进轮次与学生理解证据，基础短课按需择取环节。
新视觉设计配合当前环境单独提供的 `huashu-design`，按其规则展示三方向各两页真实代表页与候选缩略图，用户选定后再展开整套；已有方向的迭代按其豁免规则记录。本仓库不捆绑或自动安装该第三方技能。详见[设计协作与制作衔接](skills/courseware-delivery/references/design-collaboration.md)。
设计所用 HTML、截图与静态 PDF 默认保存在构建/预览目录，不自动增加正式交付格式；最终 PPTX 仍需核对可编辑内容、逐页原生备注并独立验收。

## 讲义的默认组织方式

新建完整讲义默认按“教学目标与前置知识 → 板书与课时 → 逐段讲稿 → 课堂练习 → 课后作业 → 可选拓展 → 易错点总结”组织，短课按实际需要合并。
核心段落从原课情境提出问题，让学生先预测，再通过具体数据或状态追踪推导方法，映射到代码，并用 Bug 实验和同题练习检验理解。
板书呈现核心认知、对照关系和可迁移方法；教师讲稿、预期回答、答案折叠与验收证据相互衔接。详见[教学结构与推导方式](skills/lesson-preparation/references/teaching-structure.md)。

## 安装确定版本

源码目录 `skills/` 用于版本维护；个人技能目录保存经过验证的副本。**不要用指向开发目录的软链接替代固定版本安装。**

当前推荐的个人技能位置为 `~/.agents/skills/`。官方安装器也支持通过 `--dest` 指定它；不同运行环境可能仍使用 `~/.codex/skills/`，选择一个实际被当前环境发现的位置，避免同名重复安装。[官方技能说明](https://learn.chatgpt.com/docs/build-skills)

在可访问私有仓库的环境中，可以向 Codex 说明：

> 使用 $skill-installer，从 tsetsetse/oi-teaching-workflows 的 v0.2.0 安装 skills/lesson-preparation 和 skills/courseware-delivery，目标为 ~/.agents/skills。已有同名安装先备份到技能发现目录之外。

对应的官方安装器参数是：

```sh
python3 <skill-installer目录>/scripts/install-skill-from-github.py \
  --repo tsetsetse/oi-teaching-workflows \
  --path skills/lesson-preparation skills/courseware-delivery --ref v0.2.0 \
  --dest "$HOME/.agents/skills"
```

私有仓库需要已有的 GitHub 访问权限。安装器不会覆盖已有同名目录。
本地首次安装也可从已验证标签导出快照：

```sh
git archive --format=tar --prefix=lesson-preparation/ \
  v0.2.0:skills/lesson-preparation -o /tmp/lesson-preparation-v0.2.0.tar
```

将归档解压到空的临时目录，确认含 `lesson-preparation/SKILL.md`，再将整个技能文件夹复制到个人技能目录。`courseware-delivery` 可用相同方式分别导出。复制前确认同名目录不存在，保留归档和版本号。
新安装的技能通常在后续对话中自动发现；没有出现时重启 Codex，再确认技能路径和是否被禁用。[官方加载说明](https://learn.chatgpt.com/docs/build-skills)

## 更新与回退

1. 修改源码，运行下面的验证，检查差异，用中文提交。
2. 创建新的版本标签，推送并发布；不要移动已发布的标签。
3. 将新标签导出到临时目录，检查新技能和资源齐全。
4. 把旧安装完整移到**技能发现目录以外**的备份目录，记录旧版本；再安装新快照。新安装失败时恢复旧目录。
5. 用一个小课例调用新版，确认后再日常使用。回退时保留当前副本，恢复旧快照或旧版本备份。

源码、已安装技能、课程成品分别管理。修改源码不会自动更新个人技能，也不会改动已有课程。

## 检查与开发

依赖：Python 3.10+ 标准库；实际运行 C++ 示例另需系统 `c++`（支持 C++14）。技能的 YAML 元数据格式验证可用 Codex 自带的 `skill-creator` 验证器。

```sh
python3 -m unittest discover -s tests -v
python3 skills/lesson-preparation/scripts/check_lesson.py \
  examples/intro-loop/source-讲义版.md \
  --cases examples/intro-loop/cases.json
python3 skills/courseware-delivery/scripts/check_pptx.py <课件绝对路径> \
  --bundle-root <交付根目录>
```

不传 `--cases` 时仅检查围栏并列出代码块，**不会执行代码**。传入测试清单后会执行已经审阅的代码；临时目录不提供安全隔离。详见[检查与测试清单](skills/lesson-preparation/references/verification.md)。
检查结果 `checks_passed` 只代表工具的检查范围，可能仍有跳过或未测程序；题面、来源、教学质量和成品显示需另行审查。

```text
skills/lesson-preparation/   可独立安装的技能与资源
skills/courseware-delivery/  课件交付、分镜模板与只读包检查
examples/intro-loop/        自编小课例、讲义、用例与验收记录
examples/courseware/        自编课例的分镜试做与验证范围
tests/                     检查工具的行为测试
docs/superpowers/plans/     首版实施范围与进度
.local/                    真实课程试运行记录（忽略，不提交）
dist/                      版本归档（忽略，作为发布附件）
```

本仓库的[验证记录](examples/validation.md)区分自动测试、真实课程回归与人工审查。真实课程材料不复制入仓库。
新增课件流程的试做、工具检查和未测范围见[课件交付验证](examples/courseware/validation.md)。
当前以私有仓库维护；未选择公开许可证，不自动对第三方课程内容授权。首版技能与工具为本仓库编写，没有引入参考项目的代码或课件。
