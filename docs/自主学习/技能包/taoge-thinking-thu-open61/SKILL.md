---
name: taoge-thinking-thu-open61
description: "清华公开课61集（25 个课程系列、7 大学科、169 张蒸馏卡）的知识网络索引：积极心理学、微积分与代数拓扑、大学物理与杨振宁普通物理、数字电子与电路、C++/Java/操作系统/前端/物联网、人工智能与机器学习、环境工程与碳中和、互联网创新创业。当用户想查清华公开课某一集讲了什么、找某一学科的清华课堂模型与可调用动作、或要从逐字稿证据回溯到具体卡片时使用。本包只存坐标与质量口径，不复制其他包的律条目；ASR 逐字稿质量参差，公式与数值一律不补全。"
version: v1.2.1
last_synced: 2026-11-18
node_count: 1705
graph_snapshot: "20261118"
---

# 清华公开课61集 · 多学科知识网络

> 169 张卡 / 978 个原子 / 169 个模型 / 558 条误区，
> 覆盖 25 个课程系列、7 大学科，全部可逐条回溯到 raw 逐字稿原行。
> **本包只做定位与坐标**：具体命题、机制、动作、证据都在卡片里，不在本包复述。

## 先定位：你现在要查什么

| 用户在说什么 | 读哪一册 |
|---|---|
| 想查 积极心理学相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §1 · 9 卡 |
| 想查 数学相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §2 · 29 卡 |
| 想查 物理相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §3 · 30 卡 |
| 想查 电子与电路相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §4 · 15 卡 |
| 想查 计算机与编程相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §5 · 60 卡 |
| 想查 人工智能相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §6 · 12 卡 |
| 想查 环境与碳中和相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §7 · 11 卡 |
| 想查 创新创业相关讲次、概念或动作 | [references/01-index-by-subject.md](references/01-index-by-subject.md) §8 · 3 卡 |
| 已知卡号，要直接跳到卡片/模型 id | [references/02-index-by-card.md](references/02-index-by-card.md)（169 行全量坐标） |
| 引用逐字稿、判定证据等级、处理 ASR 误识 | [references/03-quality-notes.md](references/03-quality-notes.md) |
| 需要模型间依赖、误区的可计算关系 | `assets/subgraph.json`（由 `skill_finalize.py` 导出） |

## 几条不可协商的红线

1. **不编造**：任何命题必须能在 `raw/c28/NNN.md` 找到整行原文；引文整行逐字照录（含 `[起-止]` 时间戳），不得截断、漏字、多字或改写。
2. **ASR 质量参差**：杨振宁《普通物理》等窗口含大量中英混写与不可判读碎片，系数、公式、数值一律不补全；不可判读内容写进卡片「存疑与未解」而不是猜。
3. **域口径**：本体 `specs/ontology.yaml` 无 physics / mathematics / computing / ai 等域，c28 全课统一 `domain: thinking`；学科信息保留在 raw 元数据与卡片标题，**不得**借学科名越域引用其他包。
4. **不复制律**：本包索引层不复制 30 个驱动包的 1005 条核心律，也不复述知识网络包的模型结论；命中后直接读卡片路径。

## 用法

1. 按学科或讲次在 `references/` 定位卡号 → 打开 `distill/c28/NNN.md` 读 14 字段原子卡。
2. 需要关系时查 `assets/subgraph.json`（节点 id 形如 `kp.thinking.c28lNNNm / aN / misN`）。
3. 需要原文时按卡内「证据」行的时间戳回 `raw/c28/NNN.md` 核对。
4. 卡片体检走 `check_cards.py --course c28`（auto 判域）；全库收口走 `pipeline.py --full`。

## 相关

- 调度入口 `taoge-cognitive-os`｜总索引 `skills/_INDEX.md`｜对账 `skills/_SYNC_LEDGER.md`
- 卡片目录 `distill/c28/`｜逐字稿切片 `raw/c28/`｜审计 `graph/audit_evidence.md`


## 源数据根（导入注记，2026-11-18）

- 本包只存坐标与来源口径；卡片、原文与图数据在 WorkBuddy 项目根：
  `/Users/tanghaitao/WorkBuddy/2026-10-28-16-35-40/cognitive-revolution`
- 本包正文中出现的 `distill/`、`raw/`、`graph/`、`skills/` 路径均**相对该根**解析，
  不要在技能目录下按相对路径查找。
- 根目录缺失或迁移时，按同名重定位后再读；本包内容未做改写，保持上游 v1.2.0 口径。

## 适用边界（2026-11-20 补）

- 只做索引层：某集讲什么、去哪张卡找证据、某学科从哪入门。
- 不适用：替代课程学习本身、学科深度讲解、替孩子排学习计划。

## 失败模式与兜底

- 如果找不到对应集 → 给最近的三集候选并说明依据。
- 如果卡片与逐字稿不一致 → 以逐字稿为准。
- 如果学科跨度过大 → 先给路线图，再给单集。

## 速查表

| 用户问 | 先看什么 | 落到哪 |
|---|---|---|
| 某集讲什么 | 集数索引 | 卡片摘要 |
| 某学科从哪开始 | 路线图 | 3 集起步 |
| 证据在哪 | 逐字稿坐标 | 原文段落 |
