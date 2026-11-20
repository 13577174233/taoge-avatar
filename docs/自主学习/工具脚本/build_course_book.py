#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""15 门迁入档 → 库内合订本（全文合订本 + 笔记合订本）

全文合订本：源 `05_自主学习/02-原始材料/_raw_*.txt`（`===== [标题] =====` 块格式），真原文。
笔记合订本：源各课程目录逐讲 md（摘要/S 级笔记）。
两者并存，逐讲 md 与 raw txt 均不删不改。
口径：
  字符 = 块正文（去掉块标题行）字符数，含标点、不含换行。
  底稿类型 = 块均 ≥2,500 → 全文级。
用法：
  python3 10_工具脚本/build_course_book.py --dry            # 只看统计
  python3 10_工具脚本/build_course_book.py                  # 生成全部
  python3 10_工具脚本/build_course_book.py --only 小马宋营销实战22讲
"""
import os, re, sys, hashlib, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "04_课程学习")
RAW = os.path.join(ROOT, "05_自主学习/02-原始材料")

# 课程 → (编号前缀, raw 文件列表)
RAW_MAP = {
    "5分钟商学院·实战": ("SW", ["_raw_5分钟商学院·实战_全文.txt"]),
    "何刚财经大课": ("HG", ["_raw_何刚·财经大课_01-96.txt", "_raw_何刚·财经大课_97-336.txt"]),
    "刘润商业洞察力30讲": ("BI", ["_raw_刘润商业洞察力30讲_全文.txt"]),
    "刘澜领导力30讲": ("LD", ["_raw_刘澜领导力30讲_全文.txt"]),
    "吴军阅读写作50讲": ("WXW", ["_raw_吴军·阅读与写作50讲.txt"]),
    "宁向东管理学课": ("MG", ["_raw_宁向东管理学课_全文-v2B.txt"]),
    "小马宋营销实战22讲": ("YX", ["_raw_小马宋营销实战22讲_全文.txt"]),
    "李笑来财富自由之路": ("CF", ["_raw_李笑来·通往财富自由之路_全文.txt"]),
    "梁宁产品增长": ("G", ["_raw_梁宁·产品思维30讲_全文.txt", "_raw_梁宁·增长思维30讲_全文.txt"]),
    "薛兆丰经济学课": ("E", ["_raw_薛兆丰经济学课_全文.txt"]),
    "认知训练营": ("K", ["_raw_认知训练营_全文.txt"]),
    "贾宁财务思维课": ("FN", ["_raw_贾宁财务思维课_全文.txt"]),
    "跟华杉学品牌营销30讲": ("BR", ["_raw_跟华杉学品牌营销30讲_全文.txt"]),
    "陆蓉行为金融学": ("XJ", ["_raw_陆蓉行为金融学_全文.txt"]),
    "香帅北大金融学课": ("J", ["_raw_香帅北大金融学课_全文.txt"]),
}
NOTE_PREFIX = {  # 笔记合订本编号前缀（同全文）
    k: v[0] for k, v in RAW_MAP.items()
}
SKIP = ("目录索引", "合订本", "学习情报", "收官总结")


def blocks(path):
    """解析 raw txt 的 ===== [标题] ===== 块，返回 [(标题, 正文)]。"""
    t = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"^=====\s*\[?(.+?)\]?\s*=====$", t, flags=re.M)
    out = []
    # parts[0] 是文件头（采集日期/规模/结构说明），不是讲次正文，跳过
    for i in range(1, len(parts) - 1, 2):
        out.append((parts[i].strip(), clean_head(parts[i + 1])))
    return out


# 讲次正文开头的节目头（mp3 文件名／时长／「某某亲述」等），最多剥 6 行
HEAD_PATS = (re.compile(r".+\.(mp3|m4a)\s*$", re.I),
             re.compile(r"^约?\d+\s*分(\d+\s*秒)?$"),
             re.compile(r"^(约|时长)\s*[:：]?\s*\d+"),
             re.compile(r"^\S{2,8}(亲述|讲述|转述)$"))


def clean_head(body, limit=6):
    lines = body.split("\n")
    k = 0
    while k < len(lines) and k < limit:
        ln = lines[k].strip()
        if not ln:
            k += 1
            continue
        if any(p.match(ln) for p in HEAD_PATS):
            k += 1
            continue
        break
    return "\n".join(lines[k:]).lstrip("\n")


def chars_of(s):
    return len(re.sub(r"\n", "", s.strip()))


def code_of(title, pre, idx):
    m = re.match(r"^([A-Z]{1,6})(\d{1,3})", title.strip())
    if m and re.match(r"^[A-Z]{1,4}", pre):
        return f"{m.group(1)}{int(m.group(2)):03d}"
    return f"{pre}{idx:03d}"


def lecture_key(fn):
    s = fn[:-3]
    m = re.match(r"^([A-Z]{1,4})(\d{1,3})-", s)
    if m:
        return (0, int(m.group(2)), s)
    m = re.match(r"^第(\d+)讲", s)
    if m:
        return (1, int(m.group(1)), s)
    m = re.match(r"^(\d{1,3})-", s)
    if m:
        return (1, int(m.group(1)), s)
    if s.startswith("发刊词"):
        return (0, 0, s)
    return (2, 9999, s)


def body_of(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<!--\s*sha256:.*?-->\s*$", "", t.strip(), flags=re.S)
    lines = t.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def build_full(d, dry=False):
    pre, raws = RAW_MAP[d]
    entries = []
    for rf in raws:
        for title, body in blocks(os.path.join(RAW, rf)):
            entries.append((title, body))
    n = len(entries)
    per = sum(chars_of(b) for _, b in entries) / n if n else 0
    total = sum(chars_of(b) for _, b in entries)
    grade = "全文级" if per >= 2500 else "笔记级"
    name = f"{d}｜{'全文合订本' if grade == '全文级' else '笔记合订本'}.md"
    out = os.path.join(BASE, d, name)
    r = dict(kind="全文", course=d, n=n, chars=total, per=round(per), grade=grade, out=name,
             exists=os.path.exists(out))
    if dry:
        return r

    rows = []
    for i, (title, body) in enumerate(entries, 1):
        rows.append((i, code_of(title, pre, i), title, chars_of(body),
                     hashlib.sha256(body.encode("utf-8")).hexdigest()[:12], body))
    srcs = "＋".join(f"`{rf}`" for rf in raws)
    L = [f"# {d} · {'全文合订本' if grade == '全文级' else '笔记合订本'}（{n} 讲）",
         f"> **底稿类型**：{grade}｜块 {n}／块均 {per:,.0f} 字符｜判据：块均 ≥2,500 为全文级｜分级 2026-11-20（迁入转档）", "",
         f"> **合并日期**：2026-11-20 ｜ **来源**：{srcs} ｜ **讲数**：{n} ｜ **字符**：{total:,}",
         f"> **编号**：{pre} 编号＝讲次序号；逐讲 md（摘要）另存 `{d}｜笔记合订本.md`，二者并存、互不覆盖。",
         "> **清洗**：正文按 raw 原样保留，未做页脚剔除；每讲末尾 `<!-- sha256:… -->` 为正文指纹（sha256 前 12 位）。", "",
         "## 目录", "", "| # | 编号 | 标签 | 字符 | 指纹 |", "|---|---|---|---|---|"]
    for i, cd, title, c, fp, _ in rows:
        L.append(f"| {i} | {cd} | {title} | {c:,} | `{fp}` |")
    L += ["", "---", ""]
    for i, cd, title, c, fp, body in rows:
        L += [f"## {cd}｜{title}", "", body.strip(), "", f"<!-- sha256:{fp} -->", "", "---", ""]
    open(out, "w", encoding="utf-8").write("\n".join(L).rstrip() + "\n")
    r["bytes"] = os.path.getsize(out)
    return r


def build_notes(d, dry=False):
    pre = NOTE_PREFIX[d]
    p = os.path.join(BASE, d)
    fs = [f for f in os.listdir(p) if f.endswith(".md") and not f.startswith("_")
          and not any(k in f for k in SKIP)]
    fs.sort(key=lecture_key)
    bodies = [body_of(os.path.join(p, f)) for f in fs]
    chars = [chars_of(b) for b in bodies]
    n = len(fs)
    total = sum(chars)
    per = total / n if n else 0
    name = f"{d}｜笔记合订本.md"
    out = os.path.join(p, name)
    r = dict(kind="笔记", course=d, n=n, chars=total, per=round(per), grade="笔记级", out=name,
             exists=os.path.exists(out))
    if dry:
        return r
    ids = [code_of(f[:-3].split("-")[0] if re.match(r"^[A-Z]{1,4}\d", f) else f[:-3], pre, i)
           for i, f in enumerate(fs, 1)]
    L = [f"# {d} · 笔记合订本（{n} 讲）",
         f"> **底稿类型**：笔记级（逐讲摘要/S 级归档）｜块 {n}／块均 {per:,.0f} 字符｜分级 2026-11-20", "",
         f"> **合并日期**：2026-11-20 ｜ **来源**：`04_课程学习/{d}` 逐讲 md ｜ **讲数**：{n} ｜ **字符**：{total:,}",
         f"> **编号**：{pre} 编号＝讲次序号；原文全文见同名 `｜全文合订本.md`，本件为摘要级，不作引用底稿。",
         "> **清洗**：保留逐讲 md 原样（含来源 URL、评级）；每讲末尾 `<!-- sha256:… -->` 为 md 文件指纹。", "",
         "## 目录", "", "| # | 编号 | 标签 | 字符 | 指纹 |", "|---|---|---|---|---|"]
    for i, (f, c) in enumerate(zip(fs, chars), 1):
        fp = hashlib.sha256(open(os.path.join(p, f), "rb").read()).hexdigest()[:12]
        L.append(f"| {i} | {ids[i-1]} | {d}｜{f[:-3]} | {c:,} | `{fp}` |")
    L += ["", "---", ""]
    for i, (f, b, c) in enumerate(zip(fs, bodies, chars), 1):
        fp = hashlib.sha256(open(os.path.join(p, f), "rb").read()).hexdigest()[:12]
        L += [f"## {ids[i-1]}｜{f[:-3]}", "", b, "", f"<!-- sha256:{fp} -->", "", "---", ""]
    open(out, "w", encoding="utf-8").write("\n".join(L).rstrip() + "\n")
    r["bytes"] = os.path.getsize(out)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--skip-notes", action="store_true")
    a = ap.parse_args()
    targets = [a.only] if a.only else list(RAW_MAP)
    tf = tn = 0
    for d in targets:
        r = build_full(d, a.dry)
        tf += r["chars"]
        print(f"[全文] {d} | {r['n']} 讲 | {r['chars']:,} 字符 | 块均 {r['per']:,} | {r['grade']} | {r['out']}"
              + (f" | {r['bytes']/1024/1024:.1f} MB" if not a.dry else (" | 已存在" if r["exists"] else "")))
        if not a.skip_notes:
            r2 = build_notes(d, a.dry)
            tn += r2["chars"]
            print(f"[笔记] {d} | {r2['n']} 讲 | {r2['chars']:,} 字符 | 块均 {r2['per']:,} | {r2['out']}"
                  + (f" | {r2['bytes']/1024/1024:.1f} MB" if not a.dry else (" | 已存在" if r2["exists"] else "")))
    print(f"合计 {len(targets)} 门 | 全文 {tf:,} 字符 | 笔记 {tn:,} 字符")


if __name__ == "__main__":
    main()
