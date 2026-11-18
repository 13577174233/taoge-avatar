---
name: taoge-systems-dynamics
description: >-
  系统动力学建模的知识网络：把系统动力学模型带入数据科学工具栈、用模型拟合/ML 替代组件/多尺度比较做标准分析。当用户要判断系统动力学工具选型、把存量流量模型接入数据科学流程、或设计模型拟合与交叉验证路径时使用。本包只存坐标与来源口径，不复述卡片知识结论。
version: 1.2.0
last_synced: 2026-11-18
node_count: 44
graph_snapshot: "20261118"
---

# 系统动力学 · PySD 开放文档

> 来自 `c29` 的 6 个模型 / 44 个节点，
> 原文逐字取自 GitHub `SDXorg/pysd`（MIT），可逐条回溯到 raw 原行。
> **本包只做定位与坐标**：命题、机制、动作与证据都在卡片里，不在本包复述。

## 先定位：你现在要查什么

| 用户在说什么 | 读哪一册 |
|---|---|
| 想知道本域有哪些可调用模型与动作 | [references/01-card-index.md](references/01-card-index.md)（逐卡坐标） |
| 要核对原文、许可与出处 | [references/02-source-and-license.md](references/02-source-and-license.md) |
| 需要模型间依赖与误区关系 | `assets/subgraph.json`（由 `skill_finalize.py` 导出） |

## 几条不可协商的红线

1. **不编造**：任何命题必须能在 `raw/c29/NNN.md` 找到整行原文。
2. **许可**：源仓库为 MIT，保留署名与许可文本；未核实许可的源不进发布区。
3. **域口径**：模型 id 前缀 `kp.systems.c29lNNNm`，不得借学科名越域引用其他包。
4. **不复制律**：本包不复制 30 个驱动包的律条目，也不复述知识网络包的模型结论。

## 用法

1. 在 `references/01-card-index.md` 定位卡号 → 打开 `distill/c29/NNN.md` 读 14 字段卡。
2. 需要关系查 `assets/subgraph.json`；需要原文按卡内证据行回 `raw/c29/NNN.md`。
3. 体检走 `check_cards.py --course c29`（auto 判域），收口走 `pipeline.py --full`。

## 相关

- 调度入口 `taoge-cognitive-os`｜总索引 `skills/_INDEX.md`｜对账 `skills/_SYNC_LEDGER.md`
- 卡片 `distill/c29/NNN.md`｜原文 `raw/c29/NNN.md`｜审计 `graph/audit_evidence.md`


## 源数据根（导入注记，2026-11-18）

- 本包只存坐标与来源口径；卡片、原文与图数据在 WorkBuddy 项目根：
  `/Users/tanghaitao/WorkBuddy/2026-10-28-16-35-40/cognitive-revolution`
- 本包正文中出现的 `distill/`、`raw/`、`graph/`、`skills/` 路径均**相对该根**解析，
  不要在技能目录下按相对路径查找。
- 根目录缺失或迁移时，按同名重定位后再读；本包内容未做改写，保持上游 v1.2.0 口径。
