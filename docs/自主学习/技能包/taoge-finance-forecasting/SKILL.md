---
name: taoge-finance-forecasting
description: >-
  财务预测工作流知识网络：自动特征工程/回测/模型选择、多频率预测、外部回归变量的仅历史与历史+未来两类口径、云端并行规模化。当用户要设计公司财务预测流程、决定外部变量怎么接、或评估自动预测框架时使用。本包只存坐标与来源口径，不复述卡片知识结论。
version: v1.2.1
last_synced: 2026-11-18
node_count: 44
graph_snapshot: "20261118"
---

# 财务预测 · Microsoft Finn 开放文档

> 来自 `c31` 的 6 个模型 / 44 个节点，
> 原文逐字取自 GitHub `microsoft/dstoolkit-corporate-financial-forecasting`（MIT），可逐条回溯到 raw 原行。
> **本包只做定位与坐标**：命题、机制、动作与证据都在卡片里，不在本包复述。

## 先定位：你现在要查什么

| 用户在说什么 | 读哪一册 |
|---|---|
| 想知道本域有哪些可调用模型与动作 | [references/01-card-index.md](references/01-card-index.md)（逐卡坐标） |
| 要核对原文、许可与出处 | [references/02-source-and-license.md](references/02-source-and-license.md) |
| 需要模型间依赖与误区关系 | `assets/subgraph.json`（由 `skill_finalize.py` 导出） |

## 几条不可协商的红线

1. **不编造**：任何命题必须能在 `raw/c31/NNN.md` 找到整行原文。
2. **许可**：源仓库为 MIT，保留署名与许可文本；未核实许可的源不进发布区。
3. **域口径**：模型 id 前缀 `kp.finance.c31lNNNm`，不得借学科名越域引用其他包。
4. **不复制律**：本包不复制 30 个驱动包的律条目，也不复述知识网络包的模型结论。

## 用法

1. 在 `references/01-card-index.md` 定位卡号 → 打开 `distill/c31/NNN.md` 读 14 字段卡。
2. 需要关系查 `assets/subgraph.json`；需要原文按卡内证据行回 `raw/c31/NNN.md`。
3. 体检走 `check_cards.py --course c31`（auto 判域），收口走 `pipeline.py --full`。

## 相关

- 调度入口 `taoge-cognitive-os`｜总索引 `skills/_INDEX.md`｜对账 `skills/_SYNC_LEDGER.md`
- 卡片 `distill/c31/NNN.md`｜原文 `raw/c31/NNN.md`｜审计 `graph/audit_evidence.md`


## 源数据根（导入注记，2026-11-18）

- 本包只存坐标与来源口径；卡片、原文与图数据在 WorkBuddy 项目根：
  `/Users/tanghaitao/WorkBuddy/2026-10-28-16-35-40/cognitive-revolution`
- 本包正文中出现的 `distill/`、`raw/`、`graph/`、`skills/` 路径均**相对该根**解析，
  不要在技能目录下按相对路径查找。
- 根目录缺失或迁移时，按同名重定位后再读；本包内容未做改写，保持上游 v1.2.0 口径。

## 适用边界（2026-11-20 补）

- 只回答「预测怎么设计、外部变量怎么接、怎么回测与规模化」，不产出具体公司的预测数字。
- 不适用：财务模型搭建与估值（走 `doubao-finance-model-builder`）、预算编制流程。

## 失败模式与兜底

- 如果历史样本不足 → 降级为单变量外推，并标置信度低。
- 如果外部变量未来值不可得 → 只用历史口径，注明「未接未来变量」。
- 如果多频率预测相互冲突 → 以主决策频率为准，其余作参考。

## 速查表

| 用户问 | 先看什么 | 落到哪 |
|---|---|---|
| 预测流程怎么搭 | 自动特征工程与模型选择 | 流程骨架 |
| 外部变量怎么接 | 仅历史/历史+未来两口径 | 选口径 |
| 回测怎么算 | 滚动前推 | 误差与稳定性 |
