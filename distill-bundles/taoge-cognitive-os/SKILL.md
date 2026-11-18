---
name: taoge-cognitive-os
version: 2.3.0
agent_created: true
display_name: "认知操作系统"
display_name_en: "Cognitive OS"
description: >-
  把「听过的课」变成「能调用的能力」的认知操作系统总入口：路由 63 个 taoge 能力包，
  覆盖双轨——豆包侧律层（4616 条 D 律、71 门课登记）与 WorkBuddy 侧卡层（34 门课、
  2265 张蒸馏卡、31371 节点、68 个原始能力包）。提供课程网页→原文→蒸馏卡→知识网络→
  技能包的端到端流水线、批量蒸馏协作铁律、字段与关系质量门、正确自检命令口径。
  用于新增一门课的蒸馏作业、批量补卡与断点续跑、全库体检与图修复、给某个具体问题
  找该调用哪个能力包、技能包升版与双侧同步、跨项目（卡层↔律层）对账与缺口判定。
  当用户问「这个知识点在哪门课」「下一步该学什么」「怎么把新课做成 skill」
  「卡片自检为什么全挂」「图里有孤岛怎么办」「两个项目哪份口径算数」时使用。
  不存放具体知识结论——具体律与模型一律去子包读；不做图书四维蒸馏（用 taoge-book-forge）、
  不做视频提示词、不做投资实盘建议。
last_synced: 2026-11-18
---

# 认知操作系统 · 总入口（v2.3.0）

> **v2.3.0 升级（2026-11-18，WorkBuddy 总包对账与选择性接入）**：本机技能根新增 9 个包
> （7 个七域知识网络包＋清华公开课 61 集索引＋Agent 输出评测方法包），路由口径 54→63；
> 资产盘点改为**双轨**（豆包律层 / WorkBuddy 卡层），新增
> `references/07-workbuddy-sync.md` 记录 68 包构成、装/不装判据、源数据根依赖与缺口。
> 办公四件套（pdf/xlsx/docx/pptx）判定不装，沿用本机原生 `pdf`/`sheet`/`word`/`ppt`。

> **v2.2.0 升级（2026-11-09，外部抓取链路实战复盘）**：`references/05-agent-ops.md` 新增第九章
> 「外部抓取链路的坑」7 条——浏览器沙盒毒化（必须用户终端启动、Agent 只走 CDP）、
> localhost 代理拦截、分块转写防 OOM、av 兼容、镜像策略、参数守卫覆盖、版本漂移留痕。
> 知识包内容未变，54 包不升版。

> **v2.1.0 升级（2026-11-08，基于 agent 执行复盘）**：把三条反复踩坑的口头铁律下沉到脚本——
> `check_cards.py` 自动判域 + 关系本体前置校验、`pipeline.py --full` 一键全库收口、
> 新增 `references/05-agent-ops.md` 记录 9 类失败模式与责任边界。知识包内容未变，故不升版。

> **一句话定位**：这不是第 52 个知识包，而是**调度层**。它不回答「什么是二阶思维」，
> 它回答「这个问题该去哪个包找、那条知识是否合格、下一步该学什么、新课怎么进来」。

## 结论先行：双轨资产盘点（2026-11-18 对账）

**两套账不是重复，是同一项目的两个层**：卡层保证据与关系，律层保结论与动作。任何数字只在本轨内自洽，跨轨必须标轨道名。

| 轨道 | 归属 | 课程 | 产物 | 规模 | 质量口径 |
|---|---|---|---|---|---|
| **卡层** | WorkBuddy | 34 门 | 蒸馏卡 + 知识图谱 + 能力包 | 2291 篇 raw / **2265 卡（100%）** / 31371 节点 / 40709 边（语义 28955） | 逐字率 **99.82%**（46 段非逐字已标注）；连通分量 1、链深 12、孤儿 0、环 0 |
| **律层** | 豆包侧（本项目） | 71 条登记（去重约 55 门） | D 律台账 + 驱动包 | **4616 条律**（最大号 4625）/ 78 批 / 域补丁 987 键 / 扩池 10 of 20 | 重复 0；precheck 仅 3 处历史断档 WARN |
| **调度层** | 本机技能根 | — | taoge-cognitive-os + 子包 | **63 个可调用包**（知识网络 29 / 驱动 30 / 索引 3 / 方法 1） | 路由表逐包可查；导入包坐标链接 408 条全可达 |

| 层 | 卡层 | 律层 |
|---|---|---|
| 原子 / 模型 / 误区 / 证据 | 11754 / 2265 / 5598 / 11754 | 4616 律（无独立误区节点，误区写在律卡内） |
| 平均度 / 最长链 / 孤立率 | 4.13 / 12 / 0 | 不做图，按域补丁挂载 |
| 掌握度 | 平均 0.0，22 个模型 0.6 手工标记，1 个已复习至 0.85 | 不做掌握度，按批次推进 |

**判定标准只有一条**：产物能不能在没看过原文的情况下，直接指导一次具体动作。卡层用「证据行可回溯」验，律层用「换个人照做能执行」验。

## 一、能力路由：先查表，再读包

**规则**：用户问的是「要做什么」，不是「哪门课」。按情境命中子包，
**不要**把 63 个包全读一遍；命中后只读该包的 `SKILL.md`，需要细节再进它的 `references/`。

| 用户要做什么 | 走哪类包 | 代表包 |
|---|---|---|
| 健康/用药/慢病指标判断 | 知识网络包·医药 10 个 | `taoge-medicine-hypertension`、`taoge-medicine-literacy` |
| 自我理解、亲密关系、积极心理 | 知识网络包·心理 2 个 | `taoge-psych-wuzhihong`、`taoge-psych-positive` |
| 法律思维、民法典条文 | 知识网络包·法律 2 个 | `taoge-law-thinking`、`taoge-law-civil-code` |
| 论证审视、编剧、儒家、前沿、职场 | 知识网络包·人文 5 个 | `taoge-thinking-critical`、`taoge-methodology-screenwriting` |
| 快速调一条可复用心法/判断律 | 驱动包 30 个 | 按主题查 `references/04-registry.md` |
| 精英日课 3/4/5/6 某一讲讲了什么 | 索引层包 | `taoge-cognition-elite-daily` |
| 复习计划、间隔重复、FSRS 参数与插件边界 | 知识网络包·学习 | `taoge-learning-spaced` |
| 系统动力学建模、PySD、存量流量与拟合 | 知识网络包·系统 | `taoge-systems-dynamics` |
| 财务预测流程、外部回归变量、回测口径 | 知识网络包·财务 | `taoge-finance-forecasting` |
| 同业估值、可比公司、财报指引与偏差 | 知识网络包·经济 | `taoge-economics-comps-earnings` |
| 合规自查、风险登记册、风险处置优先级 | 知识网络包·法律 | `taoge-law-risk-assessment` |
| 组织变革推进、战略取舍、阻力与干系人 | 知识网络包·管理 | `taoge-management-change-strategy` |
| 反复出现的 bug、根因排查、交付前验证 | 知识网络包·方法 | `taoge-methodology-debug-verify` |
| Agent 输出自评、评审管道、LLM-as-judge | 方法包（external） | `taoge-methodology-agentic-eval` |
| 清华公开课某一集/某学科课堂模型 | 索引层包 | `taoge-thinking-thu-open61` |
| 多智能体调度 / 评测治理 / 工作流设计 | 外部能力（v2.1.0 评估后安装） | `agent-team-orchestrator`、`agent-orchestration`、`ai-agent-workshop` |
| 经典图书筛选 → 四维蒸馏成技能 | 外部工厂（不在本体系内） | `taoge-book-forge` |
| 价值投资八书框架 | 外部 DRAFT 包 | `taoge-investment-value`（**DRAFT，禁作实盘依据**） |

**路由三不**：
- **不**用课程编号找包（`c14` 对调用者无意义）。
- **不**按讲次找包（讲次是学习单元，不是能力单元）。
- **不**在总入口里复述子包的知识结论（会与子包产生双份口径，属重复）。

> 上表 3 个外部技能是用户级独立能力，**不计入 63 包口径**；调度层只做指针，
> 不复述其内容、不复制其门禁规则，避免与本项目质量门形成两套口径。

## 二、端到端流水线（S0–S5）

| 阶段 | 输入 → 产出 | 关键命令 |
|---|---|---|
| S0+S1 取源 | 课程页 → `raw/cNN/*.md` | `ingest.py --course cNN --name "课程名"` |
| S2 蒸馏 | 原文 → `distill/cNN/NNN.md` | 五道工序：切块→原子化→定边界→连边→过闸 |
| S3 建图 | 卡 → `graph/*.jsonl` | `graph_build.py`（**全量**）→ `break_cycles.py --write` → `graph_lint.py` |
| S4 沉淀 | 子图 → `skills/taoge-*/` | `graph_export.py --skill <pkg> --write` → 写/升 `SKILL.md` |
| S5 迭代 | 反馈 → 升版 | 补边界、修边、`CHANGELOG.md` 记一行、双侧同步 |

**铁律**：S3 的 lint 不通过，绝不进 S4。图是脏的，skill 一定是错的。

### 本轮固化的完整命令链（可直接复制）

```bash
cd cognitive-revolution

# 【首选】全库收口：十步一键，全部幂等（关系修复→跨课连通→全量建图→断环→体检→终审）
python3 scripts/pipeline.py --full

# 卡片层：v2.1.0 起 --domain 默认 auto，按 frontmatter 自动判域（显式传参仍兼容）
python3 scripts/check_cards.py --course c20
python3 scripts/audit_cards.py --evidence --strict        # 全库权威审计

# 展开版（需要逐步排查时才手工跑）
python3 scripts/fix_ontology_edges.py --write --backup
python3 scripts/bridge_auto.py --write --course c20         # v2 真星形
python3 scripts/bridge_cross_course.py --write             # 四门精英日课接主干
python3 scripts/graph_build.py                            # 全量重建，勿用 --course 增量补新课
python3 scripts/break_cycles.py --write
python3 scripts/bridge_islands.py --write                  # components>1 时才需要
python3 scripts/graph_lint.py

# 技能层：升版 / 子图 / 索引 / 发布 / md5 双侧核验
python3 scripts/skill_finalize.py --write
```

**已下沉到脚本、不再靠人记的三件事**：域参数、关系合法性、全量重建顺序。
`check_cards.py` 现在会在**写卡阶段**拦住非法关系名、domain/range 违规、
INHIBITS 正权重、多值目标（负向测试可检出 6 类历史错误）。

## 三、卡片硬格式（写卡前必读）

frontmatter 9 字段 → `# 第 NNN 讲 · 标题 蒸馏卡` → `## 本讲一句话` →
`## 原子知识点`（4–6 个 `### A1 · 标题`）→ `## 本讲结构（L2）` →
`## 关系声明`（≥2 行）→ `## 误区`（≥1 条三行）→ `## 行动卡` → `## 存疑与未解`。

每个原子 **14 字段，顺序固定**：

```
类型 / 命题 / 展开 / 机制 / 量化 / 主体 / 风险 / 适用条件 / 反例 / 动作 / 自测 / 难度 / 证据等级 / 证据
```

**四条最容易翻车的口径**：

1. **`证据等级: E`** → 「适用条件」字段内必须含「此为作者观点，非实证结论」，
   写进「展开」或「机制」都算错。
2. **模型名行**必须是 `- 模型名：中文短名（kp.thinking.cNNlNNNm）`，
   中文名在前；`cNN` 必须是本课编号，**禁止串课前缀**。
3. **关系白名单只有 9 种**：DEPENDS_ON / GENERALIZES / INSTANTIATES / CONTRASTS /
   CAUSES / REFINES / APPLIES_TO / INHIBITS / EVIDENCED_BY。
   且必须符合 `specs/ontology.yaml` 的 domain/range：
   `EVIDENCED_BY` 只能指向 `ev.*`，`INHIBITS` 只能由误区节点发出且权重为负，
   `REFINES` 两端都必须是原子。**v2.1.0 起 `check_cards.py` 在写卡阶段直接拦住**，
   不再等建图后由 `graph_lint` 报出来。
4. **红线词**：一定正确/绝对正确/百试百灵/包教包会/必然成功/一定升职
   （否定句式如「并没有什么一定正确的方向」放行）。

## 四、Agent 执行铁律（血泪版 · v2.1.0 扩为八条）

> 详见 `references/02-collaboration.md`（协作参数）与 `references/05-agent-ops.md`
> （9 类失败模式、责任边界矩阵、决策树、执行时间线）。这里只列不可协商的八条。

1. **前台真并行**：每轮 3–4 批、每批 3–5 讲。**后台 agent 被中断会被全杀、零落盘**。
2. **逐讲落盘**：读一篇 → 写一张 → 立刻写盘。不做额外规划、不反复自我审查。
   一张 22–25KB 卡稳定耗时 4–5 分钟，5 讲/批 = 20–25 分钟无回传是正常吞吐，不是挂起。
3. **子代理不跑自检**：它拿不到正确的域参数，照误报改卡反而改坏；主代理统一体检。
   v2.1.0 后域参数已自动判定，但**责任边界不变**——子代理仍不跑脚本。
4. **中断后先查空洞编号**：被中断的批次常留下「A 批写到 003、D 批写到 017」这类空洞，
   必须从最小缺口补起，别按区间起点盲目续跑。
5. **共享指南只给 3 类必读文件**（样板卡、格式规范、本讲原文），别把全库文档塞进上下文。
6. **429 额度是本方案的硬上限**：并行度别超 4，宁可多轮。
7. **能写成 `if` 的，不写进 prompt**：口头提醒三次仍犯的错，一律固化进脚本
   （本轮已下沉：判域、关系合法性、全量重建顺序、十步链）。
8. **改卡必备份、批量必 dry-run**：所有修复脚本默认只报告；
   改前写 `_archive/`，改后跑全库审计与双侧 md5，禁止"凭感觉"机械修复。

## 五、版本与维护规则

| 变更 | 版本 | 必做动作 |
|---|---|---|
| 首版（一门课产出） | 1.0.0 | 建 `_meta.json`、`references/`、`assets/subgraph.json` |
| 新增知识分类或 ≥3 个原子 | 1.2.0 | 更新 `_meta.json` 的 source_courses / node_count，重导子图，`CHANGELOG.md` 记一行 |
| 修正错误/补边界/改文案 | 1.0.1 | 不新增知识，`CHANGELOG.md` 记一行 |
| 结构重组、合并拆分 | 2.0.0 | 同步改路由表与总索引 |
| 跨项目接入/对账口径变化 | 2.3.0 | 改双轨盘点表、路由表、`references/07-workbuddy-sync.md`，并在 `CHANGELOG.md` 记轨道名 |

**双侧同步**：项目 `skills/` 是工作区，`~/.workbuddy/skills/` 是发布区。
每次升版后用 `cmp -s` 或 md5 逐个核对同名包，**同名包两侧逐字节一致**；
驱动包以豆包侧为口径母本，知识网络包只在 WorkBuddy 侧产出。

## 六、跨项目双轨（2026-11-18 接入）

| 事项 | 口径 |
|---|---|
| 卡层源数据根 | `/Users/tanghaitao/WorkBuddy/2026-10-28-16-35-40/cognitive-revolution`（`distill/`、`raw/`、`graph/`、`skills/` 都相对此根） |
| 本机新增 9 包 | 7 个七域知识网络包＋`taoge-thinking-thu-open61`＋`taoge-methodology-agentic-eval`；只存坐标，正文回源读 |
| 判定不装 | 办公四件套 `pdf/xlsx/docx/pptx`（本机原生 `pdf`/`sheet`/`word`/`ppt` 更贴飞书/豆包链路）；`context-map`（单页模板、description 被引号污染） |
| 装包判据 | ①本机无同类能力 ②坐标可用（链接可达）③不与驱动包结论冲突 ④许可清楚（MIT/Apache） |
| 反向同步 | 30 个驱动包母本在豆包侧，卡层只读引用，**不反向改写**；需要时由 WB 在自身仓库升版 |
| 冲突处理 | 同一知识点两侧都有结论时，动作以律层为准、证据以卡层为准，输出标「律层/卡层」 |

详见 [references/07-workbuddy-sync.md](references/07-workbuddy-sync.md)。

## 七、终极检查清单

- [ ] 路由命中了子包，没有在总入口里复述知识结论
- [ ] 跑过 `check_cards.py`（v2.1.0 auto 判域 + 关系本体前置校验）
- [ ] 全库收口优先用 `pipeline.py --full`，而不是手工串 10 条命令
- [ ] `audit_cards.py --evidence --strict` 结构硬伤为 0
- [ ] `graph_lint.py` 零 ERROR，且连通分量 = 1
- [ ] 新增/修改的卡已跑 `fix_ontology_edges.py` 与 `bridge_auto.py`
- [ ] 每次升版都写了 `CHANGELOG.md`、核对了双侧 md5
- [ ] 引用导入包时确认源数据根存在（`test -d <根>`），链接 408 条不得断
- [ ] 跨轨引用标了「律层/卡层」，没有把两套数字混算
- [ ] **一个没读过原课的人，照着产物能不能做出一次动作**

## 深水区

- [references/01-pipeline.md](references/01-pipeline.md) — S0–S5 全流程、脚本职责、标准命令链
- [references/02-collaboration.md](references/02-collaboration.md) — 批量蒸馏协作铁律与历史踩坑
- [references/03-quality-gates.md](references/03-quality-gates.md) — 字段、关系、证据、红线与体检口径
- [references/04-registry.md](references/04-registry.md) — 63 个能力包的路由总表
- [references/05-agent-ops.md](references/05-agent-ops.md) — **Agent 执行复盘**：9 类失败模式、责任边界、幂等契约、决策树、时间线
- [references/06-run-checkpoints.md](references/06-run-checkpoints.md) — 批前/批后自检清单
- [references/07-workbuddy-sync.md](references/07-workbuddy-sync.md) — **跨项目接入**：68 包构成、装/不装判据、源数据根、缺口与下一阶段任务
- [assets/checklist.md](assets/checklist.md) — 可打印的一页检查清单
