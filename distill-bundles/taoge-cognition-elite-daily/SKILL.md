---
name: taoge-cognition-elite-daily
version: 1.0.0
agent_created: true
display_name: "精英日课 3–6 逐讲索引"
display_name_en: "Elite Daily Lecture Index"
description: >-
  万维钢·精英日课 3/4/5/6（c20–c23，合计 1277 讲）的统一逐讲索引层：
  按讲次标题定位「哪一讲讲了什么、去哪张蒸馏卡找逐字引文、该调哪条核心律」。
  用于回查某一讲的观点、给文章/视频找原文出处、核对某个模型出自哪一季、
  把 1277 讲与 30 个驱动包的律层对齐。当用户问「精英日课第 X 讲讲了什么」
  「这个说法出自日课几」「日课里有没有讲过 XX」时使用。
  **索引层，不存放知识结论**：具体心法与判断律一律去 taoge-cognition-wg6-driver、
  taoge-cognition-wg-driver、taoge-cognition-expert-handbook-driver 读；
  不重复造律、不做全文检索、不替代总入口 taoge-cognitive-os。
last_synced: 2026-11-08
---

# 精英日课 3–6 · 统一逐讲索引（索引层 v1.0.0）

> **一句话定位**：1277 讲已全部蒸馏成卡，但卡是「学习单元」不是「检索单元」。
> 本包只解决一件事——**从一句话或一个主题，快速落到具体那一讲和那张卡**。

## 去重声明（先看这里）

| 层 | 归谁 | 内容 |
|---|---|---|
| L0 原文 / 蒸馏卡 | `raw/c20–c23/`、`distill/c20–c23/`（2023 张卡中占 1277 张） | 逐讲全文 + 每讲 4–6 个原子、逐字引文、误区 |
| L1 **逐讲索引** | **本包** | 讲次 → 标题 → 卡路径；不写任何律 |
| L2 核心律 / 心法 | `taoge-cognition-wg6-driver`（日课6，52 律）、`taoge-cognition-wg-driver`（高手修炼，40 律）、`taoge-cognition-expert-handbook-driver`（40 律） | 可复用的判断链与心法 |
| L3 调度 | `taoge-cognitive-os` | 路由、质量门、流水线 |

**为什么只建一个索引包**：豆包侧此前判定「精英日课 3/4/5 与日课6 重复，不建包」。
本轮不推翻这个判断，而是把缺口以**索引层**补齐：
四门课共用一套讲次坐标，律层仍只有一份，避免 1005 条律被复制四遍。
若未来要把日课 3/4/5 也提炼成律，应在现有驱动包内升 minor 版，**不新建第二个律包**。

## 四课一览

| 课 | 季 | 应学讲次 | 卡片目录 | 逐讲索引 |
|---|---|---|---|---|
| c20 | 精英日课 3 | 316 | `distill/c20/` | [references/01-c20.md](references/01-c20.md) |
| c21 | 精英日课 4 | 325 | `distill/c21/` | [references/02-c21.md](references/02-c21.md) |
| c22 | 精英日课 5 | 318 | `distill/c22/` | [references/03-c22.md](references/03-c22.md) |
| c23 | 精英日课 6 | 318 | `distill/c23/` | [references/04-c23.md](references/04-c23.md) |
| **合计** | 3–6 季 | **1277** | — | 4 篇 |

跳过登记：c20 的 299（请假预告）、c21 的 2 篇、c22/c23 各 1 篇元内容，
共 5 篇，已在 `config/skipped_lectures.json` 登记为正常跳过，不计入应学。

## 怎么用（三步）

1. **按主题或讲次定位**：在对应季的 `references/` 里搜标题关键词，拿到讲次编号 `NNN`。
2. **回卡取证据**：读 `distill/cNN/NNN.md`，取「证据」字段的逐字引文与「适用条件」边界；
   引用时**不要**脱离边界转述，E 级内容标注为作者观点。
3. **要可复用判断链时**：带着讲次去 L2 驱动包找对应律；
   驱动包的「同作者互挂」说明会指向 `wg-driver` / `expert-handbook-driver` 的上下层关系。

**不适用**：
- 想直接要一条可执行心法 → 去驱动包，本包只有标题与路径。
- 想看知识网络里的依赖/激活传播 → 用 `graph_query.py`，本包不建图、不导出子图。
- 想找精英日课 **1/2 季** → 不在本库四课范围内，本包无数据，不要猜。

## 数据口径

- 索引由 `scripts/skill_finalize.py` 从 1277 张卡的 frontmatter 自动生成，
  **不手写、不编造标题**；卡片改名或新增讲次后重跑脚本即可刷新。
- 卡里的模型 id 统一为 `kp.thinking.cNNlNNNm`，四门课在图中已由
  `bridge_cross_course.py` 接入主干（连通分量 1，零 ERROR）。
- 本包不设 `assets/subgraph.json`：四课合计约 1.1 万节点，导出意义不大，
  需要子图时用 `graph_export.py --domain thinking` 或按 `source_course` 过滤 nodes.jsonl。

## 检查清单

- [ ] 定位到的是讲次编号，不是凭印象写季数
- [ ] 引用前回卡核对了逐字引文与适用条件
- [ ] 没有把索引里的标题当成知识结论转述
- [ ] 需要律时去了 L2 驱动包，没有在本包里复制一份
