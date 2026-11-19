#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从全库 md 记录里抽出「模型级跨域突触」，落成权威台账。

判定口径：两端 id 必须都在 神经网络连接图v5.0.html 的模型集合里，
否则是 D 号律或其它系统的编号，不算突触。
产出：
  03_思维模型库/_跨域突触台账.md   （人读）
  03_思维模型库/_synapses.json    （机器读，供 build_obsidian_vault.py）
用法：python3 10_工具脚本/extract_synapses.py
"""
import re, os, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "03_思维模型库", "神经网络连接图v5.0.html")
OUT_MD = os.path.join(ROOT, "03_思维模型库", "_跨域突触台账.md")
OUT_JSON = os.path.join(ROOT, "03_思维模型库", "_synapses.json")
REASONS = os.path.join(ROOT, "03_思维模型库", "_synapse_reasons.json")   # 推断补写，逐条带「推断：」前缀
SKIP_DIRS = {"_archive", "_历史版本归档", ".obsidian", ".git", "12-神经网络"}

PAIR = re.compile(r'([A-Z]{1,4}[0-9]{2,4})\s*(→|↔|×)\s*([A-Z]{1,4}[0-9]{2,4}|W[0-9]{2,3})')
WHY = re.compile(r'（([^）]{2,40})）')
CJK = re.compile(r'\s+([^\s，。；、|（）]{3,30})')


def model_ids():
    s = open(SRC, encoding="utf-8").read()
    i = s.find("lens:[")
    st = s.find("[", i)
    d = 0
    for k in range(st, len(s)):
        if s[k] == "[":
            d += 1
        elif s[k] == "]":
            d -= 1
            if d == 0:
                arr = s[st + 1:k]
                break
    ids = set(re.findall(r'\{id:"([^"]*)"', arr))
    c = s.find("core:[")
    ids |= set(re.findall(r'\{id:"([^"]*)"', s[c:c + 3000]))
    return ids


def main():
    mids = model_ids()
    rec = collections.defaultdict(lambda: {"why": set(), "from": set()})
    for dp, dns, fs in os.walk(ROOT):
        dns[:] = [x for x in dns if x not in SKIP_DIRS]
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for m in PAIR.finditer(t):
                a, b = m.group(1), m.group(3)
                if a not in mids or b not in mids or a == b:
                    continue
                key = (a, b)
                tail = t[m.end():m.end() + 60]
                w = WHY.match(tail)
                if w:
                    rec[key]["why"].add(w.group(1).strip())
                else:
                    w2 = CJK.match(tail)
                    if w2 and re.search(r'[\u4e00-\u9fff]', w2.group(1)):
                        rec[key]["why"].add(w2.group(1).strip())
                rec[key]["from"].add(os.path.relpath(p, ROOT))

    reasons = json.load(open(REASONS, encoding="utf-8")) if os.path.exists(REASONS) else {}
    rows = []
    BAD = ("坏边", "作废", "移除", "已废")
    BLOCK = {("GB051", "C77"), ("C77", "GB051")}   # v4.1 遗留坏边，已判废
    for (a, b), v in sorted(rec.items()):
        why = "；".join(sorted(v["why"]))
        if (a, b) in BLOCK or any(k in why for k in BAD):   # 历史已判废的边不进台账
            continue
        if not why or "未给串线说明" in why:
            why = reasons.get(f"{a}|{b}") or reasons.get(f"{b}|{a}") or "（原文只记连线，未给串线说明）"
        rows.append({"from": a, "to": b,
                     "why": why,
                     "src": sorted(v["from"])[0],
                     "src_n": len(v["from"])})
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    md = ["# 跨域突触台账（模型级）", "",
          f"> 口径：两端 id 都是 v5.0 图内模型，共 **{len(rows)}** 条；由 `10_工具脚本/extract_synapses.py` 从全库 md 记录回抽。",
          f"> 用途：`build_obsidian_vault.py` 据此生成模型笔记之间的横向连线。", "",
          "| # | 从 | 到 | 串起来能回答什么 | 记录出处 |", "|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        md.append(f"| {i} | {r['from']} | {r['to']} | {r['why']} | {r['src']} |")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"模型级突触 {len(rows)} 条 → {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
