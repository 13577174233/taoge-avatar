#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐讲对账：全文合订本 vs 笔记合订本（逐讲 md 派生），按讲次给缺口。

口径：
  · 讲数以两份合订本的「## 目录」行为准（全文＝raw 块，笔记＝逐讲 md）；
  · 标题先剥离课程名/编号/「第N讲」，再用 difflib 相似度 ≥0.7 判定同一讲；
  · 命中率 ≥60% 的课才逐讲列缺口；低于 60% 判为「命名体系不同」，只报讲数差。

输出：04_课程学习/_讲次对账-20261120.md、_讲次缺口-20261120.csv
"""
import re, os, difflib, csv

PAIRS = [("5分钟商学院·实战","SW"),("何刚财经大课","H"),("刘润商业洞察力30讲","BI"),("刘澜领导力30讲","LD"),
 ("吴军阅读写作50讲","WXW"),("宁向东管理学课","MG"),("小马宋营销实战22讲","YX"),("李笑来财富自由之路","CF"),
 ("梁宁产品增长","G"),("薛兆丰经济学课","E"),("认知训练营","C"),("贾宁财务思维课","FN"),
 ("跟华杉学品牌营销30讲","BR"),("陆蓉行为金融学","XJ"),("香帅北大金融学课","J")]

def cat_rows(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"## 目录\n(.*?)\n## ", t, re.S)
    if not m:
        return []
    body = [l for l in m.group(1).split("\n") if l.startswith("|")][2:]
    out = []
    for l in body:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 3:
            out.append((c[1], c[2]))
    return out

def norm(s):
    for k in ["5分钟商学院·实战","何刚财经大课","刘润商业洞察力30讲","刘澜领导力30讲","吴军阅读写作50讲",
              "宁向东管理学课","小马宋营销实战22讲","李笑来财富自由之路","梁宁产品增长","薛兆丰经济学课",
              "认知训练营","贾宁财务思维课","跟华杉学品牌营销30讲","陆蓉行为金融学","香帅北大金融学课"]:
        s = s.replace(k, "")
    s = re.sub(r"第\d+讲", "", s)
    s = re.sub(r"[^0-9A-Za-z\u4e00-\u9fa5]", "", s)
    s = re.sub(r"^[A-Z]{1,5}\d{2,4}", "", s)
    s = re.sub(r"^\d+", "", s)
    return s

rep, gaps = [], []
for d, pre in PAIRS:
    full = cat_rows(f"04_课程学习/{d}/{d}｜全文合订本.md")
    note = cat_rows(f"04_课程学习/{d}/{d}｜笔记合订本.md")
    nf = [norm(x[1]) for x in full]
    nn = [norm(x[1]) for x in note]
    matched, miss = 0, []
    for (code, title), n in zip(full, nf):
        if not n:
            continue
        best = max((difflib.SequenceMatcher(None, n, y).ratio() for y in nn), default=0)
        if best >= 0.7:
            matched += 1
        else:
            miss.append((code, title))
    rate = matched / len(full) if full else 0
    rep.append((d, pre, len(full), len(note), matched, rate, len(miss)))
    # 只有「未命中条数」与「讲数差」基本相等时，未命中的才算真缺口；否则是标题写法差异
    diff = max(0, len(full) - len(note))
    if rate >= 0.6 and abs(len(miss) - diff) <= 2:
        for code, title in miss:
            gaps.append((d, pre, code, title))

with open("04_课程学习/_讲次缺口-20261120.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["课程", "前缀", "讲次编号", "讲标题（仅列可对齐课程）"])
    for r in gaps:
        w.writerow(r)

L = ["# 迁入 15 门 · 逐讲对账（2026-11-20）", "",
     "> 口径：全文讲数＝`全文合订本` 目录行（raw 块）；逐讲篇数＝`笔记合订本` 目录行（逐讲 md 派生）。两本标题各自沿用采集时的命名，命中去课程名/编号后按相似度 ≥0.7 判定。", "",
     "| 课程 | 前缀 | 全文讲数 | 逐讲篇数 | 标题命中 | 命中率 | 状态 |",
     "|---|---|---|---|---|---|---|"]
T = [0, 0, 0]
for d, pre, nf, nn, m, rate, gap in rep:
    T = [T[0] + nf, T[1] + nn, T[2] + m]
    st = "一致" if nf == nn else ("缺 %d 讲" % (nf - nn) if nf > nn else "多 %d 篇" % (nn - nf))
    L.append(f"| {d} | {pre} | {nf} | {nn} | {m} | {rate*100:.0f}% | {st} |")
L.append(f"| **合计** | — | **{T[0]}** | **{T[1]}** | **{T[2]}** | {T[2]/T[0]*100:.0f}% | — |")
L += ["", "## 逐讲未对齐（标题未匹配，未必缺讲；仅列未对齐数≈讲数差的课）", ""]
by = {}
for r in gaps:
    by.setdefault(r[0], []).append(r)
if not by:
    L.append("无（可对齐课程全部覆盖）。")
for d in sorted(by, key=lambda x: -len(by[x])):
    L += [f"### {d}（净讲数差 {next(r[2]-r[3] for r in rep if r[0]==d)}，未对齐 {len(by[d])} 条）", ""]
    for _, _, code, title in by[d][:20]:
        L.append(f"- `{code}` {title}")
    if len(by[d]) > 20:
        L.append(f"- ……另 {len(by[d])-20} 讲见 `_讲次缺口-20261120.csv`")
    L.append("")
L += ["", "## 只报讲数差、不逐讲指认的课", "",
      "两类课不进缺口清单：一是标题命名体系不一致（命中率 <60%）；二是未命中条数远多于讲数差（说明多数「未命中」只是同一讲换了写法，不是缺讲）。", ""]
low = [r for r in rep if not (r[5] >= 0.6 and abs(r[6] - max(0, r[2]-r[3])) <= 2) and r[2] != r[3]]
for d, pre, nf, nn, m, rate, miss in low:
    L.append(f"- {d}（{pre}）：全文 {nf} 讲／逐讲 {nn} 篇，差 {nf-nn} 讲，标题命中 {rate*100:.0f}%，未命中 {miss} 条")
L += ["", "## 读法", "",
      "- 讲数差为正＝全文有正文但逐讲 md 未成篇（多见于问答、加餐、预告）；为负＝md 有拆篇或重复收录。",
      "- 「未对齐」＝该讲在全文合订本有正文，但逐讲合订本里没有相似度 ≥0.7 的标题；净讲数一致时多为改名或同讲拆篇，不一定是缺讲。",
      "- 本文只做对账，不改动任何讲次文件；确认缺讲后再回采集通道补抓。", ""]
open("04_课程学习/_讲次对账-20261120.md", "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L[:22]))
