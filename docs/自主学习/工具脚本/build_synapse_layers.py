#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""突触双层口径生成器（B7）
层一 L1：神经网络连接图v5.0.html 的 LINKS 数组，逐条跨域接线（对外报「图内接线」）。
层二 L2：03_思维模型库/_synapses.json，落到模型级笔记横向连线的台账（对外报「模型级台账」）。
输出：
  - 03_思维模型库/_突触双层口径对照.csv（113 行，标层与版本来源）
  - stdout 汇总（L1/L2/交集/仅 L1/仅 L2）
只读，不改图、不改台账。
"""
import re, json, csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(ROOT, "03_思维模型库", "神经网络连接图v5.0.html")
SYN = os.path.join(ROOT, "03_思维模型库", "_synapses.json")
OUT = os.path.join(ROOT, "03_思维模型库", "_突触双层口径对照.csv")


def load_lens_map(html):
    """透镜码 -> (透镜名, 来源课程, 组)；模型 id -> 透镜码。"""
    seg = html[html.index("lens:["):]
    blocks = re.split(r"\n\s*{code:\"", seg)
    lens, model2lens = {}, {}
    for b in blocks[1:]:
        code = b.split('"')[0]
        name = re.search(r'name:"([^"]*)"', b)
        src = re.search(r'source:"([^"]*)"', b)
        lens[code] = (name.group(1) if name else "", src.group(1) if src else "")
        mseg = b.split("models:[")[1] if "models:[" in b else ""
        for mid in re.findall(r'id:"([A-Za-z0-9]+)"', mseg):
            model2lens.setdefault(mid, code)
    # 内核决策环模型（core/decision）无透镜归属，单独登记
    cseg = html[html.index("decision:["):html.index("lens:[")]
    for mid in re.findall(r'id:"([A-Za-z0-9]+)"', cseg):
        model2lens.setdefault(mid, "__CORE__")
    lens["__CORE__"] = ("认知内核", "决策环（六核心）")
    return lens, model2lens


def load_edges(html):
    seg = html[html.index("var LINKS"):]
    seg = seg[:seg.index("};")]
    out = []
    for b in re.split(r"/\*\s*", seg):
        tag = b.split("*/")[0].strip() if "*/" in b else "v5.0 基线"
        body = b.split("*/")[-1] if "*/" in b else b
        ver = re.match(r"(v[0-9.]+)", tag)
        label = ver.group(1) if ver else "v5.0 基线（沿袭）"
        if re.match(r"v5\.0\s*新增", tag):
            label = "v5.0 新增"
        for src, dst in re.findall(r'"([A-Za-z0-9]+)"\s*:\s*\[([^\]]*)\]', body):
            for d in re.findall(r'"([A-Za-z0-9]+)"', dst):
                out.append((src, d, label))
    return out


def main():
    html = open(GRAPH, encoding="utf-8").read()
    lens, m2l = load_lens_map(html)
    edges = load_edges(html)

    syn = json.load(open(SYN, encoding="utf-8"))
    l2 = {}
    for s in syn:
        l2[frozenset((s["from"], s["to"]))] = s.get("why", "")

    rows = []
    for i, (a, b, ver) in enumerate(edges, 1):
        k = frozenset((a, b))
        layer = "L1+L2" if k in l2 else "仅L1"
        rows.append({
            "序号": i,
            "从": a,
            "到": b,
            "从透镜": lens.get(m2l.get(a, ""), ("", ""))[0],
            "到透镜": lens.get(m2l.get(b, ""), ("", ""))[0],
            "层级": layer,
            "引入版本": ver,
            "模型级理由": l2.get(k, "（仅图内接线，未落模型级台账）"),
        })

    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n_l1 = len(edges)
    n_l2b = len(rows) and sum(1 for r in rows if r["层级"] == "L1+L2")
    print(f"L1 图内接线 {n_l1} | L2 模型级台账 {len(syn)} | 交集 {n_l2b} | 仅L1 {n_l1-n_l2b} | 仅L2 {len(syn)-n_l2b}")


if __name__ == "__main__":
    main()
