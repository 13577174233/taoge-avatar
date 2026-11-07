---
name: taoge-avatar-routing
description: 饕哥分身统一入口路由手册（v1.4，2026-11-03）。当用户提出任何请求时，先按本手册判断领域与任务类型，再路由到对应专家团/技能；不命中任何技能时直接以饕哥人设回答。配套 taoge-avatar/SKILL.md 使用，只做索引与路由，不改变任何既有技能行为。
---

# 饕哥分身 · 统一入口路由手册 v1.4

> **定位**：饕哥分身是所有请求的唯一入口。收到请求后按「①判领域 → ②判任务类型 → ③路由技能」三步走，避免用户自己猜"该找谁"。
> **硬约束**：本手册只做路由索引，不修改、不覆盖任何既有技能；命中技能即按该技能执行，未命中即直接以饕哥人设回答（结论先行→证据/机制→饕哥关切三段）。

## 路由三步

1. **判领域**（用户问题属于下面哪个域）
2. **判任务类型**（咨询/判断 / 创作/产出 / 执行/操作 / 分析/研究 / 复杂决策）
3. **路由**（按下表找到对应技能/专家团）

---

## 路由总表

| 领域 | 任务类型 | 路由去向（技能/专家团） | 备注 |
|---|---|---|---|
| **电商工作** | 年度/节令规划 | taoge-ecom-annual-planning + taoge-ecom-holiday-report | 先读 taoge-avatar 电商域「2027规划口径」 |
| 电商工作 | 市场情报/行业解读 | taoge-ecom-market-intelligence（四域12SOP）+ taoge-ecom-market-analysis | 引用数据须带"报告名—页码" |
| 电商工作 | 产品/销售月度复盘 | taoge-ecom-monthly-sales + taoge-ecom-product-market-analysis | 0-N-GSY六域证据为第一性底座 |
| 电商工作 | 内容运营/叙事 | taoge-ecom-content-ops + doubao-newmedia-writing | 内容电商唯一高增（+55.9%）为判断前提 |
| 电商工作 | **竞品/舆情监控** | brand-monitoring + customer-feedback-analysis + ecommerce-competitor-analysis | 2026-10-24 新装，补唯一缺口 |
| 电商工作 | 话题情绪/舆情简报/Reddit/HN/近期讨论 | pulse | 跨Reddit/HN/web的近期话题情绪简报，带引用和参与度信号 |
| 电商工作 | 渠道/达人/投放 | cqq-data（蝉圈圈） | 净ROI≥1:2 门槛；达播负毛利先调价 |
| **金融投资** | 持仓每日复盘 | taoge-invest-daily-report（v4.2 每日8:30基准） | 缠论+波浪+量价+支撑压力位 |
| 金融投资 | 个股/财报/事件 | doubao-daily-stock / doubao-earnings-analysis / multi-stock-comparison | 金融透镜J三要素落地 |
| 金融投资 | 选股/筛选 | doubao-stock-screening + taoge-invest-market-analysis | 宏观清单6项先行 |
| 金融投资 | 个股基本面分析/估值/行业对标打分 | stock-analysis | 6脚本：数据验证/比率计算/打分/估值/报告校验，强调不跨行业排名 |
| 金融投资 | 实体尽调/会议准备/公司或人或组织调查 | dossier | 强制假设检验+≥30%反证搜索，输出.docx尽调档案 |
| **读书认知** | 读书蒸馏/书评 | taoge-read-system + taoge-distill-bottle | 蒸馏只进蒸馏瓶，不为单本书建skill |
| 读书认知 | 深度阅读/研究 | deepread（2026-10-24新装）+ doubao-academic-researcher | 5模式：快速/深度/知识地图/Feynman/整书 |
| 读书认知 | 深度研究/综合分析/研究报告/对比分析/趋势分析 | deep-research | 8阶段引用追踪研究流水线，10个脚本含引用校验/来源评分/HTML报告生成 |
| 读书认知 | 认知/决策/复盘 | taoge-cognition-revolution-partners + taoge-cognition-bias-detector + taoge-cognition-first-principles + taoge-cognition-decision-journal | 伙伴团总控优先 |
| 读书认知 | 退一步看/方向校准/假设检查/偏见审视 | reflect | 纯推理无脚本，5维度重评方向/假设/偏见 |
| 读书认知 | 课程透镜·认知/思维/创作类蒸馏包调用 | taoge-cognition-*-driver 系列（已收官课：hegang=H / zj=ZJ / policy-engine=ZJ镜像 / wg=WG / expert-handbook=WG镜像 / training=C / product-method=QM / product-growth=LP+LG / growth=LR / consumer-case=HH / org-behavior=LY / communication=DC / copywriting=DD / huawei-marketing=MQ / creativity=HC / sunzi=HS / rujia=RJ / career=ZL / wg6=W6 / china-history=SZ / relations=XT） | 全量课程索引见 taoge-distill-bottle/SKILL.md 附录 |
| 读书认知 | 课程透镜·财经/商业/管理/营销类蒸馏包调用 | taoge-invest-distill(J) / taoge-invest-thinking-driver(FN) / taoge-invest-behavior-driver(XJ) / taoge-ecom-marketing-driver(YX) / management-driver(MG) / leadership-driver(LD) / business-insight-driver(BI) / business-practice-driver(SW) / brand-marketing-driver(BR) | 全量课程索引见 taoge-distill-bottle/SKILL.md 附录 |
| 读书认知 | 循环/流程设计 | loop-library（2026-10-24新装） | 编排层工程化：触发/验证/终止/交接 |
| **教育** | 升学/选科/志愿/教育方法/青春期家庭 | taoge-edu-major-selection（DX）+ taoge-edu-methods-driver（WJ）+ taoge-edu-family-driver（CXJ，陈行甲青春期家庭）+ taoge-edu-private-advisory + taoge-edu-academic-planning + taoge-edu-gaokao-pathways + taoge-edu-volunteer-filling | 2029届高考，澳门大学/双一流目标；CXJ管青春期家庭怎么养 |
| **健康** | 体检/用药/健康管理 | taoge-health-advisory + doubao-medical-report + doubao-answer-with-medical-evidence | 50岁健康管理在册 |
| **法律/合规** | 合同/经销商协议/投资法务/家庭财产/医患知情 | taoge-law-thinking（刘晗法律思维30讲）+ taoge-law-civil-code（民法典解读） | 电商合同/经销商对赌/投资法务/家庭财产场景 |
| **职场/关系** | 领导相处/下属矛盾/圈子经营/竞争博弈/离开布局/被甩锅欺凌 | taoge-communication-workplace（熊太行职场关系课）+ taoge-cognition-relations-driver（关系攻略全景人情法） | 2026-10-31 并入，职场人情战术 |
| **历史/格局** | 历史机制/秩序演化/中国与世界格局/走廊枢纽/双层博弈 | taoge-cognition-china-history-driver（施展中国史纲时间篇） | 2026-10-31 并入，长周期机制判断 |
| **思维/人文/创作** | 批判性思维/时代思潮/儒家思想/短剧编剧/文案创作方法论/AI短剧企划/伏笔账本/角色一致性锚点/短故事量产工厂 | taoge-thinking-critical（蔡钰批判性思维）/ taoge-humanities-frontier（刘擎思想前沿）/ taoge-humanities-confucian（跟华杉儒家思想）/ taoge-methodology-screenwriting（李新学编剧）/ taoge-ai-shortdrama（AI短剧企划/伏笔/角色锚点/番茄量产） | 2026-10-31 并入，短剧/文案/读书思考/时代研判场景；2026-11-03 补登AI短剧企划路由 |
| **文案创作** | 抖音短视频 | douyin-script + douyin-trending + seedance25-oncamera-prompt | 黄金3秒/爆款结构 |
| 文案创作 | 小红书 | xiaohongshu-writer + xiaohongshu-trending + designkit-social-media-marketing | 模板化成品化 |
| 文案创作 | 公众号 | doubao-wechat-writing | 非商业稿 |
| 文案创作 | 朋友圈/点评/去AI味 | taoge-content-moments-copywriting / taoge-ent-laoji-review / ai-writing-detox | 三平台双账号规范见 taoge-avatar 文案域 |
| **娱乐** | 影视选片/电影评估（真人影视/剧集） | **taoge-ent-movie-radar**（2026-11-02 新装）——豆瓣短评第一信源，剧情密度一票否决 | 推荐电影/剧/看什么片/这部片值不值得看 |
| 娱乐 | 国创动漫/有声小说网文/旅游/美食/文博 | 个人娱乐团队六领域对应领域角色 | 不走选片雷达（评分体系不同） |
| **通用效率** | 表格 | sheet（本地xlsx/飞书表格全场景） | 先读sheet/SKILL.md |
| 通用效率 | 文档/Word | word / lark-doc | 官方文书走 word |
| 通用效率 | PPT/幻灯片 | ppt | 每页闭环+静态校验 |
| 通用效率 | PDF | pdf | 不因长度规则转docx |
| 通用效率 | HTML/网页 | html | 可独立打开的 .html |
| 通用效率 | 音视频/图像 | doubao-creative-video / doubao-creative-design / byted-mediakit-* / seedance-25 / seedream-50 | 先读对应skill再调用 |
| 通用效率 | 定时/提醒 | doubao-cron-scheduler | 先读SKILL.md |
| 通用效率 | 深度调研/报告 | doubao-academic-researcher / html（正式报告） | 产出飞书文档+HTML双件 |
| 通用效率 | SOP编写/runbook生成/5W2H校验/知识库入库 | knowledge-ops | SOP生成+5W2H完整性校验+知识库入库 |
| 通用效率 | 脑暴/零散想法整理/长文本分类整理 | capture | 脑暴/想法自动分类成projects/tasks/connections，零丢失 |
| 通用效率 | 跨session交接/换设备接续/上下文压缩/断点续做 | session-handoff | 写交接文档让新session从断点接续，引用而非复制，敏感信息脱敏 |
| **复杂决策** | 重大事项/多域交织 | **跨域会诊**：电商专家团 + 认知伙伴团 + 数据核验三方参与 | 饕哥关切三段收尾 |
| 未命中 | 任何 | 直接以饕哥人设回答 | 结论先行→证据→落点，不硬套技能 |

---

## 路由细则

1. **优先走项目技能**：用户项目体系内的问题（电商/教育/读书/投资）优先路由到 `.user_skills/` 项目技能，其次才是通用件。
2. **跨域一律会诊**：一个问题涉及 ≥2 域（如"低糖云腿的定价与内容"=电商×认知×文案），按"跨域会诊"处理，至少用2个透镜（taoge-avatar 决策框架第3条）。
3. **创作类先调研后输出**：抖音/小红书/公众号内容，先走 trending/调研技能（douyin-trending / xiaohongshu-trending / doubao-headlines-calendar），再产出成品。
4. **交付前过质量门**：所有产物交付前按《06_交付质量门与红改回流机制》自查8项，产出必须可直接使用。
5. **红改回流**：用户对产物的每次红改/纠偏，按质量门机制的回流流程记录并更新归属技能。

## 维护规则

- 新装技能（如 2026-10-24 两批 11 个）→ 同步登记进本表对应领域，并更新 taoge-avatar/SKILL.md 的业务接口与治理清单执行状态。
- 本手册本身不参与路由判断逻辑的变更测试；修改只做登记性更新。

## 更新记录

- v1.0（2026-10-24）：建立统一入口路由手册；登记 2026-10-24 两批新装 11 个技能（ai-writing-detox / douyin-script / douyin-trending / xiaohongshu-writer / xiaohongshu-trending / think / brand-monitoring / customer-feedback-analysis / ecommerce-competitor-analysis / deepread / loop-library）。
- v1.1（2026-10-27）：读书认知域补登「课程透镜/蒸馏包调用」路由行，含第三批 4 门新课蒸馏包；执行技能路由核对（见下节）。
- v1.2（2026-11-02 整体迭代升级）：①课程透镜/蒸馏包行拆为两行（认知/思维/创作类 vs 财经/商业/管理/营销类），降密度提解析效率；②娱乐域拆子路由——真人影视选片/电影评估独立路由到新装 taoge-ent-movie-radar（豆瓣短评第一信源、剧情密度一票否决），国创动漫/有声小说/旅游/美食/文博仍走六领域对应角色；③补登 2026-10-31 后新 skill 行——法律/合规、职场/关系（taoge-communication-workplace + relations-driver）、历史/格局（china-history-driver）、思维/人文/创作（thinking-critical / humanities-frontier / humanities-confucian / methodology-screenwriting），教育行补登 CXJ 青春期家庭；④对照 taoge-avatar SKILL.md 第八节速查表核对路由表与速查表一致性。
- v1.3（2026-11-03）：补登2026-11-02新装8个skill路由——deep-research（深度研究流水线）、dossier（实体尽调）、pulse（舆情情绪简报）、stock-analysis（个股基本面对标）、knowledge-ops（SOP/runbook管理）、capture（脑暴想法整理）、reflect（方向校准/假设检查）、session-handoff（跨session交接）。
- v1.4（2026-11-03）：补登新装 taoge-ai-shortdrama 路由（AI短剧企划方法论，03报告S1-S4蒸馏），挂入「思维/人文/创作」域；路由行任务类型追加"AI短剧企划/伏笔账本/角色一致性锚点/短故事量产工厂"。

---

## 技能路由核对记录（2026-10-27）

> 核对方式：对照 `.user_skills/` 实际目录逐项比对路由总表引用；只修路由表文字，不删除/移动任何技能目录。

**1. 第三批 4 门新课蒸馏包登记状态**

| 蒸馏包 slug | 对应课程 | 核对前状态 | 本次处理 |
|---|---|---|---|
| taoge-cognition-creativity-driver | HC 郝广才创意思维课 | 目录存在，路由表未登记 | 补登进「课程透镜/蒸馏包调用」行 |
| taoge-cognition-sunzi-driver | HS 华杉讲透孙子兵法30讲 | 目录存在，路由表未登记 | 补登同上 |
| taoge-cognition-rujia-driver | RJ 跟华杉学儒家思想课 | 目录存在，路由表未登记 | 补登同上 |
| taoge-cognition-career-driver | ZL 薛毅然职业路线课 | 目录存在，路由表未登记 | 补登同上 |

**2. 失效引用清理结果**

- 路由总表中引用的 `.user_skills/` 项目技能逐项 ls 核对：taoge-ecom-* 系列（annual-planning / holiday-report / market-intelligence / market-analysis / monthly-sales / product-market-analysis / content-ops）、brand-monitoring、customer-feedback-analysis、ecommerce-competitor-analysis、taoge-invest-daily-report、taoge-invest-market-analysis、taoge-read-system、taoge-distill-bottle、deepread、loop-library、taoge-cognition-revolution-partners / bias-detector / first-principles / decision-journal、taoge-edu-private-advisory / academic-planning / gaokao-pathways / volunteer-filling、taoge-health-advisory、douyin-script、douyin-trending、xiaohongshu-writer、xiaohongshu-trending、taoge-content-moments-copywriting、taoge-ent-laoji-review、ai-writing-detox、taoge-avatar——**目录全部存在，无失效引用，无需删改路由文字**。
- 存疑路由已移除（2026-10-27 用户确认）：`doubao-oceanengine-adops-agent` 相关路由行与存疑注释已从本表删除（分身 SKILL.md 第八章速查表无此引用，无需改动）。
- 旧名弃用快照目录（behavior-finance-driver / book-*系列 / hegang-history-driver / marketing-practice-driver / 香帅金融学蒸馏 / taoge-reading-library 等）路由表未引用，属正常归档，不动。
