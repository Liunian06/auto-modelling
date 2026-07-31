<div align="center">

<p>
  <img src="docs/final-logo.png" alt="Auto Modelling Logo" width="240">
</p>

<h1>Auto Modelling</h1>

<p><strong>把数学建模竞赛流程变成可复用、可交接、可验证的中文 Skill</strong></p>

<p>适用于 CUMCM、MCM/ICM 及其他“赛题—建模—论文”类竞赛。</p>

<p>
  <img src="https://img.shields.io/badge/Skill-Codex-111827?style=flat-square" alt="Codex Skill">
  <img src="https://img.shields.io/badge/Workflow-CUMCM%20%7C%20MCM%2FICM-2563EB?style=flat-square" alt="CUMCM and MCM/ICM">
  <img src="https://img.shields.io/badge/Paper-LaTeX-008080?style=flat-square&logo=latex" alt="LaTeX">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="MIT License"></a>
</p>

<p>
  <a href="#能完成什么">能力</a> ·
  <a href="#不能完成什么">边界</a> ·
  <a href="#安装">安装</a> ·
  <a href="#skill-架构">架构</a> ·
  <a href="#许可证">许可证</a>
</p>

</div>

---

Auto Modelling 不是一组零散提示词，而是一套面向不同 LLM 的统一数学建模竞赛 Workflow。它将赛前资料学习、赛中九步建模、LaTeX 论文产出和赛后复盘串成连续流程，并通过本地目录与交接日志保存探索过程。

所有过程性说明使用中文 Markdown；正式论文使用 UTF-8 LaTeX，并保留可编译源码与最终 PDF。

## 能完成什么

| 能力 | 说明 |
|---|---|
| 赛前学习 | 整理历年赛题，收集多篇参考论文，完成单篇分析与横向比较 |
| 赛中建模 | 按问题整理、问题分析、数据预处理、模型选择、模型构建、模型调优、论文编写、论文优化、论文审核九步推进 |
| 方案探索 | 比较基线与候选模型，记录实验结果以及采用、放弃或暂停理由 |
| 无缝交接 | 持续维护进度、关键决定、文件位置、阻塞与下一步，让其他 LLM 或 Agent 接续工作 |
| 论文交付 | 生成 Markdown 过程文档，以 LaTeX 编写正式论文，并按赛事要求选择模板与编译引擎 |
| 赛事适配 | 默认适配国赛 CUMCM 与美赛 MCM/ICM，同时允许按其他比赛的官方规则调整 |
| 赛后复盘 | 归档材料，复盘模型、实验、论文、时间与协作，沉淀跨比赛可复用经验 |

## 不能完成什么

| 边界 | 说明 |
|---|---|
| 不保证获奖 | Skill 提供一致流程和质量约束，但不能保证奖项或不同 LLM 产出完全相同 |
| 不替代官方规则 | 当届模板、页数、匿名、提交和 AI 使用要求必须以官方来源为准 |
| 不伪造证据 | 不生成虚构数据、运行结果、参考论文、引用或无法复核的结论 |
| 不自动提交 | 不登录竞赛系统，不代替参赛者完成最终提交或合规确认 |
| 不内置全部模型 | 不提供覆盖所有题型的算法库，模型仍需根据题目、数据和验证结果选择 |
| 不替代人工终审 | 数学正确性、结果意义、引用和提交版本仍需要参赛团队最终确认 |

## 安装

### 使用 AI Agent 安装

把下面的指令完整发送给能够执行 Git 和本地文件操作的 AI Agent：

~~~text
请安装 Auto Modelling 数学建模竞赛 Skill：

1. 使用 Git 克隆 https://github.com/Liunian06/auto-modelling.git 。如果本地已有该仓库，先确认工作区没有未提交修改，再拉取最新的 main 分支；不要覆盖用户修改。
2. Skill 源目录是仓库中的 .codex/skills/math-modeling-competition/，不要把整个仓库当作一个 Skill 安装。
3. 先读取该目录下的 SKILL.md，确认 Skill 名称为 math-modeling-competition，并检查 references/、scripts/ 以及它们被引用的文件是否完整。
4. 确定本机 Codex Skill 目录。优先使用 $CODEX_HOME/skills；如果没有设置 CODEX_HOME，则 Windows 使用 %USERPROFILE%/.codex/skills，macOS/Linux 使用 ~/.codex/skills。
5. 将整个 math-modeling-competition 目录复制到 Skill 目录中，最终入口应为 <Skill目录>/math-modeling-competition/SKILL.md。
6. 如果目标目录已经存在，不要直接覆盖。先比较现有版本与仓库版本，并询问用户是更新、备份后替换，还是取消安装。
7. 安装后检查 SKILL.md、6 个 references Markdown 文件和 scripts/workspace_manager.py 均存在，再告诉用户重新开始一个 Codex 任务以加载 Skill。
8. 不要在 Skill 安装目录或本仓库中创建比赛 data。比赛数据只能放在用户明确指定的工作目录下。
~~~

Agent 安装时需要识别的源目录结构：

~~~text
auto-modelling/
└── .codex/
    └── skills/
        └── math-modeling-competition/  <- 复制这个目录
            ├── SKILL.md                <- Skill 入口
            ├── references/
            └── scripts/
~~~

### 人工安装

#### Windows PowerShell

克隆仓库并进入项目目录：

~~~powershell
git clone https://github.com/Liunian06/auto-modelling.git
Set-Location auto-modelling
~~~

复制 Skill；如果已经安装，命令会停止并提示先处理旧版本：

~~~powershell
$skillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME "skills"
} else {
    Join-Path $env:USERPROFILE ".codex\skills"
}
$source = Join-Path (Get-Location) ".codex\skills\math-modeling-competition"
$destination = Join-Path $skillsRoot "math-modeling-competition"

New-Item -ItemType Directory -Force $skillsRoot | Out-Null
if (Test-Path $destination) {
    throw "目标 Skill 已存在：$destination。请先备份、删除或改用更新流程。"
}
Copy-Item -Recurse $source $destination
Test-Path (Join-Path $destination "SKILL.md")
~~~

最后一行应输出 `True`。

#### macOS / Linux

~~~bash
git clone https://github.com/Liunian06/auto-modelling.git
cd auto-modelling

skills_root="${CODEX_HOME:-$HOME/.codex}/skills"
destination="$skills_root/math-modeling-competition"
test ! -e "$destination" || { echo "目标 Skill 已存在：$destination"; exit 1; }
mkdir -p "$skills_root"
cp -R .codex/skills/math-modeling-competition "$skills_root/"
test -f "$destination/SKILL.md" && echo "安装成功"
~~~

安装完成后重新开始一个 Codex 任务，并直接描述建模需求：

~~~text
使用数学建模竞赛 Skill，帮我准备 2025 年国赛 A 题。
工作目录是 E:\数学建模。
~~~

用户未提供工作目录时，Skill 会先询问；比赛数据不会保存在 Skill 安装目录中。

## Data 文件结构

比赛资料不存放在本仓库或 Skill 安装目录中，而是存放在用户明确指定的工作目录下。所有比赛统一使用以下结构：

~~~text
<用户指定的工作目录>/
└── data/
    └── 202509-国赛CUMCM2025/
        └── 202509-国赛CUMCM2025-A题/
            ├── 赛题/                  # 官方赛题、附件、赛题整理 Markdown
            ├── 参考论文/              # 参考论文、单篇分析、横向比较
            ├── 工作区/
            │   ├── 数据/              # 原始、清洗和中间数据
            │   ├── 代码/              # 预处理、建模、实验和出图代码
            │   ├── 结果/              # 实际运行产生的结果、预测数据和指标
            │   ├── 图表/              # 分析和论文使用的图表
            │   ├── 日志/              # 进度、决策、阻塞和 Agent 交接记录
            │   └── 论文/              # UTF-8 LaTeX、.bib、模板、PDF
            └── 复盘/                  # 赛后复盘和可复用经验
~~~

比赛目录使用 `{YYYYMM}-{中文简称}{英文标识}{届次年份}` 命名，例如 `202509-国赛CUMCM2025`、`202502-美赛MCM2025`；赛题目录在比赛目录名后追加题号，例如 `202509-国赛CUMCM2025-A题`。`工作区/结果/` 只保存代码实际运行产生的输出，`工作区/日志/` 专门保存过程和交接信息，过程性描述统一使用 Markdown，正式论文统一使用 UTF-8 LaTeX 并保留成功编译的 PDF。

## Skill 架构

~~~mermaid
flowchart LR
    U["用户需求"] --> S["SKILL.md<br/>入口与强制规则"]
    S --> P{"当前阶段"}
    P --> PRE["赛前<br/>赛题与参考论文"]
    P --> RUN["赛中<br/>九步建模与论文"]
    P --> POST["赛后<br/>复盘与沉淀"]
    PRE --> REF["references/<br/>按需加载中文规范"]
    RUN --> REF
    POST --> REF
    S --> SCRIPT["scripts/<br/>目录初始化与检查"]
    SCRIPT --> DATA["用户工作目录/data/<br/>赛题、数据、代码、结果、日志、论文"]
    RUN --> DATA
~~~

~~~text
.codex/skills/math-modeling-competition/
├── SKILL.md
├── references/
│   ├── 赛前流程.md
│   ├── 赛中九步流程.md
│   ├── 赛后复盘.md
│   ├── 论文与LaTeX规范.md
│   ├── 文件与日志规范.md
│   └── 赛事与论文适配.md
└── scripts/
    └── workspace_manager.py
~~~

- <code>SKILL.md</code>：保存核心 Workflow、目录规则、真实性约束和完成标准。
- <code>references/</code>：按赛前、赛中、赛后、论文和赛事类型加载详细规范。
- <code>scripts/</code>：以确定性脚本创建或检查统一比赛工作区。

Skill 与用户数据严格分离：

~~~text
Skill:  ~/.codex/skills/math-modeling-competition/
Data:   <用户指定的工作目录>/data/
~~~

完整产品要求见 [PRD](docs/PRD-通用数学建模全流程Skill.md)，运行入口见 [SKILL.md](.codex/skills/math-modeling-competition/SKILL.md)。

## 许可证

本项目采用 [MIT License](LICENSE) 开源。你可以自由使用、修改和分发，但需保留原始版权与许可证声明。
