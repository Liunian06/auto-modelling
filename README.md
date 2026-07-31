<div align="center">

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

下载或克隆本仓库后，在仓库根目录执行。

### Windows PowerShell

~~~powershell
$target = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force ".codex\skills\math-modeling-competition" $target
~~~

### macOS / Linux

~~~bash
mkdir -p ~/.codex/skills
cp -R .codex/skills/math-modeling-competition ~/.codex/skills/
~~~

安装后重新开始一个 Codex 任务，并直接描述建模需求：

~~~text
使用数学建模竞赛 Skill，帮我准备 2025 年国赛 A 题。
工作目录是 E:\数学建模。
~~~

用户未提供工作目录时，Skill 会先询问；比赛数据不会保存在 Skill 安装目录中。

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
