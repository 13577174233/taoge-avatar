#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 03_思维模型库/神经网络连接图v5.0.html 重构成 Obsidian 原生双向链接网络。

源：v5.0 HTML 内的 lens/core 数据（77 透镜 / 284 模型 / 6 核心模型）
产出：
  12-神经网络/00 神经网络总图.md        L0 中枢
  12-神经网络/01 分域/<Gxx 名称>.md      L1 语义群（40）
  12-神经网络/02 透镜/<code>·<name>.md   L2 透镜（77）
  12-神经网络/03 模型/<id>·<name>.md     L3 模型（284）
  12-神经网络/README-Obsidian.md        使用说明
  .obsidian/*.json                      vault 配置（graph 默认只看 12-神经网络）

用法：python3 10_工具脚本/build_obsidian_vault.py [--dry-run]
自检：生成后统计节点/边/断链，断链必须为 0。
"""
import os, re, json, sys, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "03_思维模型库", "神经网络连接图v5.0.html")
VAULT = os.path.join(ROOT, "12-神经网络")
DRY = "--dry-run" in sys.argv

GROUP_NAME = {
    0: "经济与政策", 1: "金融与财务", 2: "管理与商业", 3: "营销与增长",
    4: "认知训练", 5: "思维工具与读写", 6: "医学与健康", 7: "心理",
    8: "法律", 9: "教育与升学", 10: "历史与关系", 11: "行为金融与投资",
    12: "宏观与博弈", 13: "信息论", 14: "公司治理", 15: "科技史",
    16: "美术史", 17: "体验设计", 18: "社会网络", 19: "创意流水线",
    20: "财商与家庭财富", 21: "心理学基础", 22: "科学减重", 23: "抑郁症",
    24: "学习方法", 25: "组织人才", 26: "供应链", 27: "创意传播",
    28: "传统智慧", 29: "职业路径", 30: "国际贸易争端", 31: "内容影响力",
    32: "偏移待补", 33: "逻辑统计", 34: "案例经营",
    35: "系统动力学与间隔重复", 36: "财务预测与可比公司",
    37: "法律风险与组织变革", 38: "调试与评测", 39: "清华公开课",
}

# 透镜 → 已有全量清单（存在才链接）
LIST_FILES = {
    "E": "E系列全量清单-薛兆丰经济学课.md",
    "F": "F系列全量清单-李笑来财富自由之路.md",
}

# 跨透镜横向接线（无向；两条方向都会写入，reason 写在发起侧）
BRIDGES = [
    ("E", "J", "价格与利率是同一枚硬币两面：微观机制要接到金融定价上才落地"),
    ("E", "Z", "价格信号必须放进政策与制度约束里读，否则会把管制当成市场"),
    ("E", "H", "宏观叙事最终要回到供求与成本，否则只是故事"),
    ("E", "F", "储蓄与负债都是时间定价，先懂机会成本再谈复利"),
    ("E", "XJ", "同一套价格机制，人在里面会系统性犯错"),
    ("J", "TX", "公司金融是金融透镜的企业侧镜像：同一笔钱，投资人与公司两个视角"),
    ("J", "FN", "报表口径决定金融判断的输入质量"),
    ("J", "ZXY", "风险度量先于收益判断：波动率、肥尾、杠杆三件事"),
    ("J", "ZYU", "个人账户是金融透镜的最小实践单元"),
    ("XJ", "YJF", "行为金融与行为经济学共用偏误清单，一个看市场一个看选择"),
    ("YJF", "C", "偏误要被训练成可自检的清单，否则只是标签"),
    ("C", "W", "认知训练给判断，通用工具给流程，二者合起来才是可执行"),
    ("C", "LZJ", "统计与逻辑是认知训练的地基：没有分母的结论都是修辞"),
    ("W", "R", "读写是思维工具的输出端：想清楚＝写清楚"),
    ("W", "HSL", "方法层与学习层互证：方法给结构，学习给节奏"),
    ("HSL", "SPD", "学习方法要落到间隔与到期管理，否则只是愿望"),
    ("HSL", "WJ", "同一套方法，孩子侧要降维成家庭可执行的版本"),
    ("WJ", "CXJ", "教育方法与青春期家庭同域：方法失灵多半是关系先坏"),
    ("WJ", "DX", "提分要接到专业与院校的选择约束上，不然是空转"),
    ("DX", "CAR", "选专业＝职业路径的前置决策"),
    ("CXJ", "LXN", "青春期家庭与家长必修是同一问题的两个视角"),
    ("CXJ", "LJ", "家庭冲突先看心理机制，再谈沟通技巧"),
    ("LJ", "WH", "心理学基础与武志红互为解释层：机制与关系动力"),
    ("LJ", "PP", "基础心理学给病与常的边界，积极心理学给增益方向"),
    ("MG", "LD", "管理与领导力是同一组织的两套动作：秩序与方向"),
    ("MG", "TM", "团队管理是管理透镜的最小执行单元"),
    ("MG", "OH", "组织人才回答「谁来做」，管理回答「怎么组织」"),
    ("MG", "LSB", "公司治理是管理的制度底座：权责与制衡"),
    ("LSB", "CHG", "治理结构不改，变革只能靠开会推"),
    ("BI", "SW", "商业洞察给判断，商业实战给动作"),
    ("BI", "HBS", "洞察要拿案例校验，否则是漂亮话"),
    ("SW", "FN", "实战决策最后都要过财务口径"),
    ("FN", "ECO", "同业内比倍数、同口径比结构，二者必须合读"),
    ("ECO", "FNF", "可比公司给横截面，财务预测给时间轴"),
    ("FNF", "SYS", "预测进系统才有回路：单点外推必然过冲"),
    ("SYS", "GB", "系统回路与博弈结构互证：谁在响应谁的策略"),
    ("GB", "TZ", "传统智慧多是不完全信息下的博弈经验"),
    ("TZ", "SN", "关系与网络是传统智慧里最硬的那部分"),
    ("SN", "YKK", "内容影响力本质是社会网络的传播结构"),
    ("YKK", "CP", "影响力靠内容，内容靠传播结构"),
    ("CP", "HN", "创意流水线把传播从灵感变成产线"),
    ("HN", "MOT", "创意落地要过体验设计：用户在哪一刻被说服"),
    ("YX", "BR", "营销实战与品牌营销：一次转化 vs 长期记忆"),
    ("BR", "LP", "品牌承诺最终由产品兑现"),
    ("LP", "LG", "产品给价值，增长给规模；顺序反了就是烧钱买空"),
    ("LG", "ZCC", "增长假设必须由市场调研校验"),
    ("LP", "SC", "产品结构受供应链约束：能卖的首先是能供的"),
    ("SC", "HBS", "供应链问题常以案例形式出现：看别人怎么断的"),
    ("LT", "CC", "法律思维给判断框架，民法典给条文依据"),
    ("LT", "LAW", "法律风险是法律思维在企业场景的执行版"),
    ("LAW", "CHG", "合规改造往往是组织变革的触发器"),
    ("ZXY", "FNF", "风险预算与预测同源：先算最坏，再算期望"),
    ("ZXY", "SYS", "风险多来自延迟与回路，不是单点失误"),
    ("HX", "JJD", "宏观与贸易争端是同一外部约束的内外两面"),
    ("HX", "Z", "宏观判断要落到政策工具与时序"),
    ("J", "ECO", "估值是金融与财务的接口"),
    ("CSH", "LFP", "财商训练与家庭财富：能力与账户两端"),
    ("CSH", "F", "财商是财富自由的前置能力"),
    ("LFP", "ZYU", "家庭财富管理与个人投资共用仓位与期限纪律"),
    ("KJS", "XL", "科技史与信息论互证：技术跃迁多半是信息成本下降"),
    ("MOT", "SN", "体验设计读的是人与场景的网络关系"),
    ("DBG", "AGE", "调试验证与 Agent 评测同属可验证性：都要可复现"),
    ("THU", "W", "公开课给广度，工具透镜给可用度"),
    ("ZXY", "ZXY0", "占位，不存在则忽略"),
]

# 饕哥三关切（图上导航用）
CONCERNS = [
    ("电商怎么做", ["E", "Z", "MG", "BI", "SW", "YX", "BR", "LP", "LG", "ZCC", "SC", "FN", "ECO", "C"]),
    ("投资怎么看", ["J", "FN", "XJ", "YJF", "ZXY", "ZYU", "TX", "HX", "Z", "F", "ECO", "GB"]),
    ("IP 与内容", ["YKK", "CP", "HN", "MOT", "SN", "BR", "W", "R", "C"]),
    ("孩子与家庭", ["WJ", "CXJ", "LXN", "DX", "HSL", "LJ", "WH", "PP", "CAR"]),
    ("身体与健康", ["HF", "HT", "HU", "HG", "HL", "HE", "DMD", "MD", "NT", "ML", "FX", "WLM"]),
]


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "－", name).strip()


def parse_source():
    s = open(SRC, encoding="utf-8").read()
    # lens 数组
    i = s.find("lens:[")
    start = s.find("[", i)
    d, end = 0, None
    for k in range(start, len(s)):
        if s[k] == "[":
            d += 1
        elif s[k] == "]":
            d -= 1
            if d == 0:
                end = k
                break
    arr, o = s[start + 1:end], 0
    blocks, d, st = [], 0, None
    for k, ch in enumerate(arr):
        if ch == "{":
            if d == 0:
                st = k
            d += 1
        elif ch == "}":
            d -= 1
            if d == 0 and st is not None:
                blocks.append(arr[st:k + 1])
                st = None
    lens = []
    for b in blocks:
        g = lambda k, dd=None: (re.search(k + r':"((?:[^"\\]|\\.)*)"', b) or [None, dd])[1]
        m = re.search(r'group:(\d+)', b)
        c = re.search(r'count:(\d+)', b)
        e = re.search(r'engine:(true|false)', b)
        ms = re.findall(r'\{id:"([^"]*)",name:"([^"]*)",d:"([^"]*)"\}', b)
        lens.append(dict(
            code=g("code"), name=g("name"),
            count=int(c.group(1)) if c else 0,
            group=int(m.group(1)) if m else 0,
            color=g("color"), engine=(e.group(1) == "true") if e else False,
            source=g("source"), detail=g("detail", ""),
            models=[dict(id=x[0], name=x[1], d=x[2]) for x in ms],
        ))
    core = [dict(id=x[0], name=x[1], detail=x[2]) for x in
            re.findall(r'\{id:"([^"]*)",name:"([^"]*)",detail:"([^"]*)"\}', s)]
    return lens, core


LAW_ROW = re.compile(r'^\|\s*([A-Z]{2,4}[0-9]{2,4})\s*\|\s*([^|]{1,40})\|', re.M)


def load_law_lists():
    """从 04_课程学习/*/_laws_*.md 抽 透镜码 → [(id, 短名)]，用于内嵌全量清单。
    只做只读抽取，不再造双链：图表节点数不受影响。"""
    out = {}
    for f in glob.glob(os.path.join(ROOT, "04_课程学习", "*", "_laws_*.md")):
        try:
            t = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in LAW_ROW.finditer(t):
            code = re.match(r"[A-Z]{2,4}", m.group(1)).group(0)
            name = m.group(2).strip()
            if not name:
                continue
            lst = out.setdefault(code, [])
            if (m.group(1), name) not in lst:
                lst.append((m.group(1), name))
    return {k: v for k, v in out.items() if v}


def build():
    lens, core = parse_source()
    LAWS = load_law_lists()
    today = datetime.date.today().isoformat()
    created = []
    edges = 0

    def w(rel, text):
        p = os.path.join(VAULT, rel)
        created.append(os.path.splitext(os.path.basename(p))[0])
        if DRY:
            return
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)

    groups = {}
    for L in lens:
        groups.setdefault(L["group"], []).append(L)

    # 横向接线（双向；只对存在的码生效）
    byc = {L["code"]: L for L in lens}
    nbr = {}
    for a, b, why in BRIDGES:
        if a in byc and b in byc and a != b:
            nbr.setdefault(a, []).append((b, why))
            nbr.setdefault(b, []).append((a, why))
    bridge_note_count = 1

    # 模型级突触（历史台账 _synapses.json，缺失则跳过）
    byid = {}
    for L in lens:
        for m in L["models"]:
            byid[m["id"]] = m
    for c in core:
        byid.setdefault(c["id"], c)
    SYN = []
    sp = os.path.join(ROOT, "03_思维模型库", "_synapses.json")
    if os.path.exists(sp):
        SYN = [r for r in json.load(open(sp, encoding="utf-8")) if r.get("from") in byid and r.get("to") in byid]
    syn_by = {}
    for r in SYN:
        syn_by.setdefault(r["from"], []).append((r["to"], r["why"]))
        syn_by.setdefault(r["to"], []).append((r["from"], r["why"]))

    # ---------- L0 总图 ----------
    tot_models = sum(len(L["models"]) for L in lens)
    engines = [L for L in lens if L["engine"]]
    rows = []
    for gi in sorted(groups):
        gl = groups[gi]
        n = sum(x["count"] for x in gl)
        rows.append(f"| [[G{gi:02d} {GROUP_NAME.get(gi,'群'+str(gi))}]] | {GROUP_NAME.get(gi,'—')} | {len(gl)} | {n:,} | "
                    + "、".join(f"[[{x['code']}·{x['name']}]]" for x in gl) + " |")
        edges += 1
    core_rows = [f"| [[CORE {c['id']} {c['name']}]] | {c['detail']} |" for c in core]
    edges += len(core)
    eng_rows = [f"- [[{L['code']}·{L['name']}]] — {L['count']:,} 条｜{L['source']}" for L in engines]
    edges += len(engines)

    conc_rows, bridge_rows = [], []
    for title, codes in CONCERNS:
        alive = [c for c in codes if c in byc]
        conc_rows.append(f"| {title} | " + "、".join(f"[[{c}·{byc[c]['name']}]]" for c in alive) + " |")
        edges += len(alive)
    for a, b, why in BRIDGES:
        if a in byc and b in byc:
            bridge_rows.append(f"| {a}·{byc[a]['name']} | {b}·{byc[b]['name']} | {why} |")
    syn_rows = [f"| {r['from']} {byid[r['from']]['name']} | {r['to']} {byid[r['to']]['name']} | {r['why']} |" for r in SYN]

    t0 = f"""---
类型: 总图
tags: [神经网络, MOC]
更新: {today}
透镜数: {len(lens)}
模型数: {tot_models}
节点数: {1 + len(groups) + len(lens) + tot_models + len(core)}
来源: 神经网络连接图v5.0.html
---

# 神经网络总图

> 一句话：{len(lens)} 个透镜 × {tot_models} 个模型 ＝ 一张可按图索骥的判断网。上层给视角，中层给机制，底层给动作。
> 全量清单：能抽到律表的透镜，已在各自笔记里用「全量清单（折叠）」内嵌（纯文本、不上图）；无律表的透镜只有抽样。\n> 口径：图内 {tot_models} 个是**代表模型**（v5.0 抽样），全库模型约 6,297（v2.95）不在图上；跨域突触 {len(SYN)} 条为历史记录可回溯部分（台账见 [[04 横向接线总表]]）。
> 这是 Obsidian 里的**可编辑主图**；HTML 快照只读留档，见文末。

## 五层结构

| 层 | 内容 | 数量 | 说明 |
|---|---|---|---|
| L0 | 总图（本页） | 1 | 只做入口与口径，不复述模型 |
| L1 | 分域 | {len(groups)} | 语义群，回答「这类问题归谁管」 |
| L2 | 透镜 | {len(lens)} | 单一视角，回答「用哪把尺子」 |
| L3 | 模型 | {tot_models} | 单条机制，回答「具体怎么判」 |
| L4 | 核心骨架 | {len(core)} | 跨域通用，优先调用 |

## 五大引擎（常驻优先调用）

{chr(10).join(eng_rows)}

## 分域入口（{len(groups)} 群）

| 分域 | 名称 | 透镜数 | 覆盖条数 | 透镜 |
|---|---|---|---|---|
{chr(10).join(rows)}

## 核心骨架（{len(core)}）

| 模型 | 一句话 |
|---|---|
{chr(10).join(core_rows)}

## 五关切入口（按事找人，不按学科找人）

| 关切 | 主用透镜 |
|---|---|
{chr(10).join(conc_rows)}

## 怎么用这张图

1. **先定域**：从问题反推分域（价格问题→经济与政策；身体问题→医学与健康）。
2. **再选透镜**：同域内选 1–2 个透镜，不要一次拉 5 个，视角多等于没视角。
3. **落到模型**：每个透镜下挑 1–3 条模型做判断依据，其余留作反证。
4. **写判断**：判断落 `05_判断日志/` 的 J 卡，依据最多 3 条，到期回收验证。

## 与旧版关系

- 只读快照：[神经网络连接图v5.0.html](../03_思维模型库/神经网络连接图v5.0.html)（v4.6→v4.9→v5.0 线性演化，不再改）
- 重算入口：`10_工具脚本/build_obsidian_vault.py`（改 HTML 数据后重跑即可，本目录整体重建）
- 口径说明：透镜 `count` 是该透镜覆盖的原始条目数，模型数是 HTML 里给出的**代表性模型**，两者不等号。

## 接回主库

- [[00-体系说明与索引]]
- 主题库：[[模型地图]]
- 学习链：[[_laws_lecture_index_报告]]
"""
    w("00 神经网络总图.md", t0)

    # ---------- 横向接线总表 ----------
    w("04 横向接线总表.md", f"""---
类型: 索引
tags: [神经网络, 索引, 接线]
更新: {today}
接线数: {len(bridge_rows)}
突触数: {len(syn_rows)}
---

# 横向接线总表

> 上级 [[00 神经网络总图]]｜透镜级接线 {len(bridge_rows)} 条 ＋ 模型级突触 {len(syn_rows)} 条
> 规则：只在「同一问题需要两把尺子」时才接线；接得太多等于没接。
> **本页是索引，故意不加双链**：表内透镜与模型一律用纯文本名，避免它变成与总图并列的第二枢纽。要跳转请回 [[00 神经网络总图]]，或在搜索里直接打 id。
> 标注「推断：」的串线说明是按两个模型语义补写的，非原文记录；无标注的才是台账原文。

## 一、透镜级接线（{len(bridge_rows)}）

| 透镜 A | 透镜 B | 为什么接 |
|---|---|---|
{chr(10).join(bridge_rows) if bridge_rows else '| — | — | 暂无 |'}

## 二、模型级突触（{len(syn_rows)}）

> 来源：`03_思维模型库/_跨域突触台账.md`（由 `10_工具脚本/extract_synapses.py` 从全库记录回抽，已剔除判废边）

| 从 | 到 | 串起来能回答什么 |
|---|---|---|
{chr(10).join(syn_rows) if syn_rows else '| — | — | 暂无台账 |'}
""")

    # ---------- L1 分域 ----------
    for gi in sorted(groups):
        gl = groups[gi]
        nm = GROUP_NAME.get(gi, "群" + str(gi))
        n = sum(x["count"] for x in gl)
        body = [f"""---
类型: 分域
群: {gi}
tags: [神经网络, 分域]
更新: {today}
透镜数: {len(gl)}
---

# G{gi:02d} {nm}

> 上级 [[00 神经网络总图]]｜{len(gl)} 个透镜｜覆盖 {n:,} 条

## 透镜

| 透镜 | 条数 | 看什么 |
|---|---|---|
"""]
        for x in gl:
            body.append(f"| [[{x['code']}·{x['name']}]] | {x['count']:,} | {x['detail'][:60] or '—'} |")
            edges += 1
        w(f"01 分域/G{gi:02d} {safe(nm)}.md", "\n".join(body) + "\n")

    # ---------- L2 透镜 / L3 模型 ----------
    for L in lens:
        gi = L["group"]
        gname = GROUP_NAME.get(gi, "群" + str(gi))
        lst = LIST_FILES.get(L["code"])
        rows = []
        for m in L["models"]:
            rows.append(f"| [[{m['id']} {m['name']}]] | {m['d']} |")
            edges += 1
        back = f"\n## 原文清单\n\n- [[{os.path.splitext(lst)[0]}]]\n" if lst and os.path.exists(os.path.join(ROOT, "03_思维模型库", lst)) else ""
        laws = LAWS.get(L["code"], [])
        full = ""
        if laws:
            rows_l = [f"| {i} | {n} |" for i, n in laws]
            full = (f"\n## 全量清单（折叠，{len(laws)} 条）\n\n"
                    f"<details><summary>展开：本透镜全部 {len(laws)} 条（图内只画了 {len(L['models'])} 个代表模型）</summary>\n\n"
                    "| 编号 | 短名 |\n|---|---|\n" + "\n".join(rows_l) +
                    "\n\n</details>\n\n> 清单为纯文本，不加双链——全量上图会把图压成一团；要跳转用搜索打编号。\n")

        nb = nbr.get(L["code"], [])
        bridge = ""
        if nb:
            lines = [f"- [[{byc[c]['code']}·{byc[c]['name']}]] — {w}" for c, w in nb]
            bridge = "\n## 横向接线（跨透镜互证）\n\n" + "\n".join(lines) + "\n"
            edges += len(nb)
        text = f"""---
类型: 透镜
码: {L['code']}
群: {gi}
条数: {L['count']}
引擎: {'是' if L['engine'] else '否'}
来源: {L['source']}
tags: [神经网络, 透镜{', 引擎' if L['engine'] else ''}]
更新: {today}
---

# {L['code']}·{L['name']}

> 上级 [[G{gi:02d} {gname}]]｜{L['count']:,} 条｜来源：{L['source']}

## 看什么

{L['detail'] or '（源数据未给口径说明，按透镜名与下方模型判断适用范围。）'}

## 模型（{len(L['models'])}）

| 模型 | 一句话 |
|---|---|
{chr(10).join(rows) if rows else '| — | 该透镜尚未拆出独立模型 |'}
{bridge}{full}{back}
"""
        w(f"02 透镜/{safe(L['code']+'·'+L['name'])}.md", text)

        for m in L["models"]:
            nb = syn_by.get(m["id"], [])
            syn = ""
            if nb:
                lines = [f"- [[{byid[o]['id']} {byid[o]['name']}]] — {w}" for o, w in nb]
                syn = "\n## 模型级突触（跨域主线）\n\n" + "\n".join(lines) + "\n"
            mt = f"""---
类型: 模型
id: {m['id']}
透镜: {L['code']}
群: {gi}
tags: [神经网络, 模型]
更新: {today}
---

# {m['id']} {m['name']}

> 透镜 [[{L['code']}·{L['name']}]]｜分域 [[G{gi:02d} {gname}]]

**一句话**：{m['d']}

## 用法

- 先确认它在你这个问题里成立的前提；前提不成立，机制就不成立。
- 与同透镜其他模型并读，找反例优先于找支持。
{syn}"""
            edges += 2 + len(nb)
            w(f"03 模型/{safe(m['id']+' '+m['name'])}.md", mt)

    # ---------- 核心骨架 ----------
    for c in core:
        w(f"03 模型/CORE {safe(c['id']+' '+c['name'])}.md", f"""---
类型: 核心模型
id: {c['id']}
tags: [神经网络, 核心, 模型]
更新: {today}
---

# CORE {c['id']} {c['name']}

> 上级 [[00 神经网络总图]]

**一句话**：{c['detail']}

## 为什么进核心

跨域通用、调用频率最高；任何领域的问题都可以先用它过一遍。
""")

    # ---------- README ----------
    w("README-Obsidian.md", f"""# 这个文件夹怎么用（Obsidian 版神经网络图）

## 一、打开

1. Obsidian → 「打开本地仓库 / Open folder as vault」→ 选 `认知操作系统` 根目录（**不要选 12-神经网络 子目录**，否则接不回主库）。
2. 首次打开会提示「信任作者、启用社区插件」——本项目不需要社区插件，全部核心功能可跑。

## 二、看图的三个入口

| 想看的 | 打开方式 |
|---|---|
| 全局网络 | 左侧「图谱视图 Graph view」；默认筛选已设为只看 `12-神经网络` |
| 单透镜的上下文 | 打开任一透镜笔记 → 右侧「反向链接 / Backlinks」看谁引用了它 |
| 学一条模型 | 从 [[00 神经网络总图]] → 分域 → 透镜 → 模型，四级下钻 |
| 看跨域连接 | [[04 横向接线总表]]（透镜级接线 ＋ 模型级突触台账） |

## 三、图谱配色（已预置）

- 蓝：分域｜青：透镜｜金：五大引擎｜灰：模型｜红：核心骨架｜紫：索引（接线总表、README）
- 横向交叉的线就是「跨域接线」：透镜级 {len(bridge_rows)} 条 ＋ 模型级 {len(syn_rows)} 条，写在 [[04 横向接线总表]]

## 四、改图规则

1. **只改数据源，不手改笔记**：模型/透镜有增减，改 `03_思维模型库/神经网络连接图v5.0.html` 的数据段，再跑 `python3 10_工具脚本/build_obsidian_vault.py`，本目录整体重建。
2. 本目录下的 md **会被重建覆盖**，想写私人批注请写到 `05_判断日志/` 或 `02_原子笔记/`。
3. 新增 D 号律不需要进这张图；图上只保留「可复用的判断机制」，不追平 4,800+ 条律的规模。

## 五、规模

- 本次重建：{len(lens)} 透镜｜{sum(len(L['models']) for L in lens)} 代表模型｜{len(core)} 核心｜{len(groups)} 分域｜内部边约 {edges}
- 接线：透镜级 {len(bridge_rows)} 条 ＋ 模型级突触 {len(syn_rows)} 条
- 生成时间：{today}
""")

    # ---------- .obsidian 配置 ----------
    cfgdir = os.path.join(ROOT, ".obsidian")

    def wcfg(name, obj):
        if DRY:
            return
        os.makedirs(cfgdir, exist_ok=True)
        json.dump(obj, open(os.path.join(cfgdir, name), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    wcfg("app.json", {"alwaysUpdateLinks": True, "newLinkFormat": "shortest",
                      "useMarkdownLinks": False, "attachmentFolderPath": "_attachments",
                      "showUnsupportedFiles": False, "defaultViewMode": "preview"})
    wcfg("appearance.json", {"theme": "obsidian", "accentColor": "#00b3a4"})
    wcfg("core-plugins.json", {k: True for k in [
        "file-explorer", "global-search", "switcher", "graph", "backlink",
        "outgoing-link", "tag-pane", "page-preview", "outline", "word-count",
        "file-recovery", "bookmarks", "canvas"]} | {"daily-notes": False, "random-note": False,
                                                    "slides": False, "audio-recorder": False,
                                                    "workspaces": False, "templates": False})
    wcfg("graph.json", {
        "collapse-filter": False,
        "search": 'path:"12-神经网络"',
        "showTags": False, "showAttachments": False, "hideUnresolved": True,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "tag:#分域", "color": {"a": 1, "rgb": 0x3b82f6}},
            {"query": "tag:#透镜", "color": {"a": 1, "rgb": 0x06b6d4}},
            {"query": "tag:#引擎", "color": {"a": 1, "rgb": 0xf59e0b}},
            {"query": "tag:#核心", "color": {"a": 1, "rgb": 0xef4444}},
            {"query": "tag:#模型", "color": {"a": 1, "rgb": 0x94a3b8}},
            {"query": "tag:#索引", "color": {"a": 1, "rgb": 0xa855f7}},
        ],
        "collapse-display": False, "showArrow": True, "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1.2, "lineSizeMultiplier": 1,
        "collapse-forces": False, "centerStrength": 0.5, "repelStrength": 12,
        "linkStrength": 1, "linkDistance": 220, "scale": 1, "close": False,
    })
    return lens, core, groups, created, edges


def check(created, lens, groups):
    """断链自检：[[target]] 必须命中本目录笔记，或主库中已存在的 md。"""
    names = set(created)
    # 主库可解析名（排除归档）
    external = set()
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("_archive", "_历史版本归档", ".obsidian", ".git")]
        for f in files:
            if f.endswith(".md"):
                external.add(os.path.splitext(f)[0])
    broken = []
    for dirpath, _, files in os.walk(VAULT):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            for t in re.findall(r"\[\[([^\]|#]+)", open(p, encoding="utf-8").read()):
                t = t.strip()
                if t.endswith(".html"):
                    continue  # 附件链接，交给 Obsidian
                if t not in names and t not in external:
                    broken.append((os.path.relpath(p, VAULT), t))
    return broken


if __name__ == "__main__":
    lens, core, groups, created, edges = build()
    print(f"透镜 {len(lens)}｜模型 {sum(len(L['models']) for L in lens)}｜核心 {len(core)}｜分域 {len(groups)}")
    print(f"笔记 {len(created)} 篇｜内部边约 {edges}")
    if not DRY:
        b = check(created, lens, groups)
        print(f"断链 {len(b)}")
        for x in b[:10]:
            print("  断链", x)
        assert len(b) == 0, "存在断链，修模板后再跑"
