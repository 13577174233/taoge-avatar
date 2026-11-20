---
name: taoge-law-risk-assessment
description: >-
  法律与合规风险评估的知识网络：识别、评估与缓解运营风险，风险登记册与风险偏好口径。当用户要做合规自查、搭建风险清单、判断风险处置优先级时使用。只存坐标与来源口径；不提供法律意见、不复述卡片知识结论。
version: 1.2.0
last_synced: 2026-11-18
node_count: 21
graph_snapshot: "20261118"
---

# 法律风险评估 · MIT 开放文档

> 来自 `c32` 的 3 个模型 / 21 个节点，
> 原文逐字取自 GitHub `w95/awesome-claude-corporate-skills`（MIT），可逐条回溯到 raw 原行。
> **本包只做定位与坐标**：命题、机制、动作与证据都在卡片里，不在本包复述。

## 先定位：你现在要查什么

| 用户在说什么 | 读哪一册 |
|---|---|
| 想知道本域有哪些可调用模型与动作 | [references/01-card-index.md](references/01-card-index.md)（逐卡坐标） |
| 要核对原文、许可与出处 | [references/02-source-and-license.md](references/02-source-and-license.md) |
| 需要模型间依赖与误区关系 | `assets/subgraph.json`（由 `skill_finalize.py` 导出） |

## 几条不可协商的红线

1. **不编造**：任何命题必须能在 `raw/c32/NNN.md` 找到整行原文。
2. **许可**：源仓库为 MIT，保留署名与许可文本；未核实许可的源不进发布区。
3. **域口径**：模型 id 前缀 `kp.law.c32lNNNm`，不得借学科名越域引用其他包。
4. **不复制律**：本包不复制 30 个驱动包的律条目，也不复述知识网络包的模型结论。

## 用法

1. 在 `references/01-card-index.md` 定位卡号 → 打开 `distill/c32/NNN.md` 读 14 字段卡。
2. 需要关系查 `assets/subgraph.json`；需要原文按卡内证据行回 `raw/c32/NNN.md`。
3. 体检走 `check_cards.py --course c32`（auto 判域），收口走 `pipeline.py --full`。

## 相关

- 调度入口 `taoge-cognitive-os`｜总索引 `skills/_INDEX.md`｜对账 `skills/_SYNC_LEDGER.md`
- 卡片 `distill/c32/NNN.md`｜原文 `raw/c32/NNN.md`｜审计 `graph/audit_evidence.md`


## 源数据根（导入注记，2026-11-18）

- 本包只存坐标与来源口径；卡片、原文与图数据在 WorkBuddy 项目根：
  `/Users/tanghaitao/WorkBuddy/2026-10-28-16-35-40/cognitive-revolution`
- 本包正文中出现的 `distill/`、`raw/`、`graph/`、`skills/` 路径均**相对该根**解析，
  不要在技能目录下按相对路径查找。
- 根目录缺失或迁移时，按同名重定位后再读；本包内容未做改写，保持上游 v1.2.0 口径。

## 适用边界

- 适用：合规自查、风险清单搭建、风险处置优先级排序。
- 不适用：出具法律意见、代拟合同条款、诉讼策略（应交律师；本包只做识别与分级）。
- 纪律：每条风险必须写「触发条件 + 后果 + 现有控制 + 缺口」，不给结论性法律判断。

## 失败模式与兜底

- 法条/监管口径不确定 → 标「待律师确认」，不引用未核实条文。
- 风险清单过长 → 按「可能性×后果」两维排序，只保留前 10 条进处置计划。
- 用户要求「能不能做」的定性答复 → 改为列出「做与不做的风险对照表」。

## 速查表

| 场景 | 先查什么 | 产出 |
|---|---|---|
| 新活动上线 | 平台规则 + 广告法红线 | 风险清单 + 卡点 |
| 数据对外提供 | 个人信息边界 | 授权链 + 缺口 |
| 供应商合作 | 合同责任与验收 | 责任分配表 |
