#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""迁入课程 → 律表 `_laws_<PFX>.md` + `_catalog_<PFX>.txt`

律条种子来自已 S 级归档的技能包律表（编号/短名/一句话），本脚本只做两件事：
  1) 把每条律钉到全文合订本的某一讲（优先用块标题里的同号编号，否则按关键词打分取最高）；
  2) 从该讲原文里取一句最佳锚点句，并按「锚点是否逐字命中」判 原文摘句／近似句／提炼句。

证据口径与 `_laws_GB.md` 一致：只看锚点是否命中原文，不沿用学术 A–E 等级。
用法：
  python3 10_工具脚本/build_laws.py --course 小马宋营销实战22讲 --prefix YX --seed 10_工具脚本/_seed/YX.tsv
  python3 10_工具脚本/build_laws.py --course 小马宋营销实战22讲 --prefix YX --seed 10_工具脚本/_seed/YX.tsv --dry
"""
import os, re, sys, argparse, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_course_book import RAW_MAP, RAW, blocks, chars_of

STOP = set("的了是在有和与就不都很个这那你我他们为以对从到把被而或但也就还只可要会能得地说做想要一个什么怎么如果因为所以这样那样我们你们他们".split())


def norm(s):
    return re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", s)


def kw(s):
    """2-gram 关键词，去掉停用字组合。"""
    s = norm(s)
    out = set()
    for i in range(len(s) - 1):
        g = s[i:i + 2]
        if g[0] in STOP or g[1] in STOP:
            continue
        out.add(g)
    return out


def sentences(t):
    s = re.sub(r"\s*\n\s*", "\n", t)
    parts = re.split(r"(?<=[。？！])|\n", s)
    return [p.strip() for p in parts if p.strip()]


def load_seed(path, native=False):
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        a, b, c = line.split("|")
        if native:
            rows.append((a.strip(), b.strip(), c.strip()))
            continue
        m = re.match(r"([A-Z]{1,5})(\d{1,4})", a.strip())
        # 三位号（如 SW105）统一补零；四位以上原生编号（E1394/F900）保持原样
        code = f"{m.group(1)}{int(m.group(2)):03d}" if m and len(m.group(2)) <= 3 else a.strip()
        rows.append((code, b.strip(), c.strip()))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--seed", default="")
    ap.add_argument("--no-num-fallback", action="store_true")
    ap.add_argument("--note", default="技能包 S 级律表")
    ap.add_argument("--codes", default="pre", choices=["pre", "native"])
    ap.add_argument("--restrict", default="", help="按编号前缀限定候选讲次区间，如 LP:0:42;LG:42:78")
    ap.add_argument("--catalog-only", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    d, pre = a.course, a.prefix
    raws = RAW_MAP[d][1]
    bks = []
    for rf in raws:
        for title, body in blocks(os.path.join(RAW, rf)):
            bks.append((title, body))
    seeds = [] if a.catalog_only else load_seed(a.seed, a.codes == "native")
    restrict = {}
    if a.restrict:
        for part in a.restrict.split(";"):
            k, lo, hi = part.split(":")
            restrict[k] = (int(lo), int(hi))

    # 讲次编号（与全文合订本一致）
    import build_course_book as B
    titles = [t for t, _ in bks]
    codes = [B.code_of(t, pre, i) for i, t in enumerate(titles, 1)]

    rows = []
    for code, name, line in seeds:
        k = kw(name + " " + line)
        # 1) 块标题自带同号编号 → 直取
        rk = next((k for k in restrict if code.startswith(k)), None)
        lo, hi = restrict.get(rk, (0, len(bks))) if rk else (0, len(bks))
        cand = range(lo, min(hi, len(bks)))
        same = [i for i in cand if re.match(r"^" + re.escape(code) + r"(\D|$)", bks[i][0])]
        if same:
            i = same[0]
        else:
            # 2) 关键词打分取最佳；全无命中才退回「编号＝讲次」
            scored = []
            for j in cand:
                t, b = bks[j]
                scored.append((len(k & kw(t + " " + b[:3000])), j))
            scored.sort(reverse=True)
            best_i, best_s = scored[0][1], scored[0][0]
            num = int(re.sub(r"[A-Z]", "", code))
            if best_s >= 2:
                i = best_i
            elif not a.no_num_fallback and 1 <= num <= len(bks):
                i = num - 1          # 关键词全无命中时才退回「编号＝讲次」
            else:
                i = best_i
        body = bks[i][1]
        best, bs = "", -1
        for st in sentences(body):
            if not (20 <= len(st) <= 150):
                continue
            # 排除讲内小标题行（如「02｜结构模块：…？」「1. 引言」）与纯问句标题
            if re.match(r"^\d{1,2}\s*[｜|]\.?", st) or re.match(r"^\d{1,2}\s*\.\s", st):
                continue
            if len(st) < 30 and "，" not in st and st.endswith("？"):
                continue
            if "｜" in st or "|" in st:          # 讲内标题行（「20讲 ｜ 标题」，含半角竖线）
                continue
            if not st.endswith(("。", "？", "！", "”")) and "，" not in st:
                continue
            sc = len(k & kw(st)) * 2 + min(len(st), 60) / 60.0
            if sc > bs:
                best, bs = st, sc
        hit = 0
        for g in k:
            if g in best:
                hit += 1
        if hit >= max(6, len(k) // 3):
            verdict = "原文摘句"
        elif hit >= 3:
            verdict = "近似句（全文）"
        else:
            verdict = "提炼句"
        anchor = best if verdict != "提炼句" else "≈" + best
        src = f"{codes[i]}｜{titles[i]}"
        rows.append((code, name, line, src, verdict, anchor, chars_of(body),
                     hashlib.sha256(body.encode()).hexdigest()[:12]))

    dist = {}
    for r in rows:
        dist[r[4]] = dist.get(r[4], 0) + 1
    dist_s = "／".join(f"{k} {v}" for k, v in sorted(dist.items()))
    total = sum(r[6] for r in rows)
    print(f"律 {len(rows)} 条｜覆盖讲次 {len(set(r[3] for r in rows))}/{len(bks)}｜证据 {dist_s}｜锚点字符 {total:,}")
    if a.dry:
        for r in rows[:3]:
            print("  样例:", r[0], r[1], "|", r[4], "|", r[5][:60])
        return

    out_dir = os.path.join("04_课程学习", d)
    md = os.path.join(out_dir, f"_laws_{pre}.md")
    L = [f"# {d} · 律表（全文级，{len(rows)} 律）", "",
         f"> **底稿类型**：全文级｜依据 `{d}｜全文合订本.md`（合并自 {len(raws)} 份 raw，{len(bks)} 讲／{sum(chars_of(b) for _, b in bks):,} 字符）",
         f"> **重蒸日期**：2026-11-20 ｜ **校验方式**：逐条锚点回源——律条取自{a.note}，锚点句按关键词命中从对应讲原文直取，可在合订本内检索命中",
         f"> **编号**：" + (f"{rows[0][0]}–{rows[-1][0]}（沿用课程原生模型号，与 03_思维模型库 对齐）" if a.codes=="native" else f"{pre}001–{pre}{len(rows):03d}，与技能包同名系列一致") + "；**讲次定位**见「来源」列",
         f"> **证据分布**：{dist_s}",
         "> **旧件**：无（本课未建过独立律表）", "",
         "## 锚点判级读法", "",
         "| 措辞 | 含义 | 引用方式 |", "|---|---|---|",
         "| 原文摘句 | 锚点句与全文底稿逐字重合，且律条关键词命中 ≥1/3 | 可直接加引号引用，注明讲次 |",
         "| 近似句（全文） | 锚点句取自原文，但律条用词与原文不同 | 只能转述，标「大意」，不得当原话 |",
         "| 提炼句 | 原文无对应句，由多句归纳（锚点带 ≈） | 只能作为断言引用，不得倒注为讲师原话 |", "",
         "## 律表", "", "| 编号 | 短名 | 一句话 | 来源（讲次） | 证据 | 原文锚点 |",
         "|---|---|---|---|---|---|"]
    def esc(x):
        return x.replace("|", "｜")

    for code, name, line, src, verdict, anchor, c, fp in rows:
        L.append(f"| {code} | {esc(name)} | {esc(line)} | {esc(src)} | {verdict} | {esc(anchor)} |")
    L += ["", "## 口径与边界", "",
          f"- 字符口径：锚点所在讲正文 `len()` 去换行；全课合计 {sum(r[6] for r in rows):,} 字符（仅统计被锚定的讲）。",
          f"- 讲次覆盖率 {len(set(r[3] for r in rows))}/{len(bks)}：{len(bks)-len(set(r[3] for r in rows))} 讲未承载律条（发刊词/结语类）。",
          f"- 律条内容未改动{a.note}原文，本轮新增的是「讲次定位 + 原文锚点」；如与该来源表述不一致，以原文锚点为准。", ""]
    open(md, "w", encoding="utf-8").write("\n".join(L))

    cat = os.path.join(out_dir, f"_catalog_{pre}.txt")
    C = [f"{d}｜讲次目录（{len(bks)} 讲）", f"生成 2026-11-20｜源 {'＋'.join(raws)}", ""]
    for i, (t, b) in enumerate(bks, 1):
        C.append(f"{i:03d}\t{codes[i-1]}\t{t}\t{chars_of(b)}\t{hashlib.sha256(b.encode()).hexdigest()[:12]}")
    open(cat, "w", encoding="utf-8").write("\n".join(C) + "\n")
    print("写出", md, os.path.getsize(md), "B；", cat, os.path.getsize(cat), "B")


if __name__ == "__main__":
    main()
