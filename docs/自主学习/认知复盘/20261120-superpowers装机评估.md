# obra/superpowers 装机评估（2026-11-20）

> 评估口径：GitHub API 实读仓库结构与 15 个技能的 SKILL.md 体积；不引用第三方转述。

## 一、仓库事实

| 项 | 值 |
|---|---|
| 仓库 | `obra/superpowers`（MIT License） |
| 自述 | agentic skills framework & software development methodology |
| 技能数 | **15 个**（`skills/` 下 15 个目录） |
| 技能总体积 | 约 **197 KB**（单文件 3.2–40 KB） |
| 最近提交 | 2026-11-03 |
| 形态 | 纯 Markdown 技能 + 可选 hooks/插件清单，非代码库 |

15 个技能：`brainstorming`、`diagnosing-superpowers`、`dispatching-parallel-agents`、`executing-plans`、`finishing-a-development-branch`、`receiving-code-review`、`requesting-code-review`、`subagent-driven-development`、`systematic-debugging`、`test-driven-development`、`using-git-worktrees`、`using-superpowers`、`verification-before-completion`、`writing-plans`、`writing-skills`。

## 二、与我们现有能力的重叠

| superpowers 技能 | 本机对应 | 重叠度 | 判断 |
|---|---|---|---|
| verification-before-completion（3.6 KB） | 无专包；`output-quality-gate` 只做交付前质量关 | **低（正好是缺口）** | 装 |
| systematic-debugging（29 KB） | `taoge-methodology-debug-verify` | 高（同为根因-假设-证据-复核） | 装，分工：本包讲方法，它给逐条操作 |
| writing-plans（10 KB） | `planning-with-files` | 中（都落磁盘计划） | 装 |
| executing-plans（18 KB） | 无专包 | 低 | 装 |
| dispatching-parallel-agents（6 KB） | 无专包（靠编排层） | 低 | 装 |
| writing-skills（21.7 KB） | `skill-creator-for-work` | 高 | 可选，二选一 |
| subagent-driven-development（40 KB） | `taoge-orchestrator` ＋本环境子代理机制 | 高且耦合深 | 不装 |
| brainstorming（29.5 KB） | `think` | 中 | 不装 |
| test-driven-development（17.8 KB） | 无测试栈（本库以文档/脚本为主） | 无场景 | 不装 |
| requesting / receiving-code-review（15.6 KB） | 无 PR 流程 | 无场景 | 不装 |
| using-git-worktrees / finishing-a-development-branch（14.6 KB） | 无分支开发流 | 无场景 | 不装 |
| diagnosing-superpowers（6.9 KB） | 无 | 自诊断工具，对本库是噪音 | 不装 |
| using-superpowers（3.2 KB） | 无 | **会在会话开始强制加载自身**，干扰现有路由 | 不装 |

## 三、装机方案（建议）

**装 5 个，不装 10 个。**

```
复制目标：<S2>/<技能名>/SKILL.md（保持英文原文，不翻译、不改写）
装：verification-before-completion、systematic-debugging、writing-plans、
    executing-plans、dispatching-parallel-agents
跳过：using-superpowers（强制自加载）、subagent-driven-development（与编排层冲突）、
      brainstorming、writing-skills、test-driven-development、requesting-code-review、
      receiving-code-review、using-git-worktrees、finishing-a-development-branch、
      diagnosing-superpowers
```

理由：

1. **只补缺口，不搬整套**。本库缺的正是「证据先于结论」与「计划→执行→验证」的硬约束，前 5 个正好对应；其余 10 个要么与本机重复，要么场景不存在。
2. **不装 `using-superpowers`**。它设计成会话开始时自动加载，在我们的多包路由体系里会让所有对话先被它接管一次，收益低、干扰高。
3. **不装 `subagent-driven-development`**。它是为 Claude Code 的子代理协议写的（40 KB），与本环境的编排机制不同源，硬装会产生两套并行规则。
4. **不装 hooks 与插件清单**（`.claude-plugin`、`hooks/`、`index.js`）。本环境只用 `skills/` 目录，hooks 不生效也不需要，避免引入自动执行。

## 四、装机风险与处置

| 风险 | 处置 |
|---|---|
| 英文原文，与中文包风格不一致 | 保持原文不动；在 `00-体系说明与索引.md` 的技能表里加一行「英文来源，方法论层」 |
| `systematic-debugging` 与 `taoge-methodology-debug-verify` 语义重叠 | 两者都留：调试时先读我们的包定框架，需要逐条操作再读它 |
| 技能名与现有 458 个包冲突 | 实测无冲突（15 个名字在 S1/S2 均不存在同名目录） |
| 版本不可追溯 | 复制时记录来源 commit 与日期，写入索引；后续不随上游自动更新，按需手动拉 |
| 许可 | MIT，可商用与修改；分发时保留 LICENSE 声明 |

## 五、结论

值得装，但只装 5 个、且只复制 `skills/`。这一步的收益不是「多 5 个技能」，而是把「声称完成前必须跑验证」变成硬规则，正好接上本轮 B1 补「失败模式」的方向。

装机本身约 5 分钟；建议与 B2 批次一起做，装完在 `00-体系说明与索引.md` 增补一节「外部方法论技能（5）」。
