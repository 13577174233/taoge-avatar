#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B6：生成「透镜 ↔ 课程 ↔ 律号」对照表与课程前缀律表索引。

输入（只读）：
- 12-神经网络/02 透镜/*.md          透镜 frontmatter（码/群/条数/来源）+ 全量清单
- <S2>/*/SKILL.md                   技能包律表（| 律号 | 律名 | 一句话 |）
- 03_思维模型库/模型地图.md         仅在前两者都取不到时用于「推定」id 区间
- 05_自主学习/00-缺口账/_laws_lecture_index.csv   D 系列律号溯源表（4,844 行，另建）

输出：
- 03_思维模型库/_课程前缀律表索引.csv
- 03_思维模型库/_透镜课程律号对照表.csv
- 03_思维模型库/透镜课程律号对照表.md

口径：区间一律由「实际存在的编号」计算，不采用文档头部的宣称（宣称与实际不符会写进「差异」列）。
"""
import re, os, glob, csv, json, collections

ROOT = "/Users/tanghaitao/DoubaoWork/chats/2026-10-12/new-chat-1/认知操作系统"
S2 = "/Users/tanghaitao/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills"
LENS_DIR = os.path.join(ROOT, "12-神经网络/02 透镜")
MMAP = os.path.join(ROOT, "03_思维模型库/模型地图.md")


def load_lenses():
    out = {}
    for f in sorted(glob.glob(os.path.join(LENS_DIR, "*.md"))):
        t = open(f, encoding="utf-8").read()

        def fm(k):
            m = re.search(rf"^{k}: (.+)$", t, re.M)
            return m.group(1).strip() if m else ""

        code = fm("码")
        body = t.split("全量清单", 1)[-1] if "全量清单" in t else ""
        codes = re.findall(r"\|[ \t]*([A-Z]{1,5}[0-9]{3})[ \t]*\|", body)
        codes = [c for c in codes if re.fullmatch(rf"{re.escape(code)}[0-9]{{3}}", c)]
        seen = []
        for c in codes:
            if c not in seen:
                seen.append(c)
        out[code] = dict(name=os.path.basename(f)[:-3], grp=fm("群"), n=fm("条数"),
                         src=fm("来源"), listed=seen)
    return out


def load_packages():
    """返回 {前缀: {num: (律号, 律名, 一句话, 技能包名字)}} 与 {技能包: 行数}"""
    pref = collections.defaultdict(dict)
    for f in glob.glob(os.path.join(S2, "*/SKILL.md")):
        pkg = os.path.basename(os.path.dirname(f))
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^\|\s*([A-Z]{1,5})(\d{2,4})\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", t, re.M):
            p, num, name, one = m.group(1), int(m.group(2)), m.group(3).strip(), m.group(4).strip()
            pref[p].setdefault(num, (p + m.group(2), name, one, pkg))
    return pref


def load_modelmap():
    mmap = collections.defaultdict(set)
    t = open(MMAP, encoding="utf-8").read()
    for p, n in re.findall(r"^\|\s*([A-Z]{1,5})(\d{2,4})\s*\|", t, re.M):
        mmap[p].add(int(n))
    return mmap


def load_lecture_index():
    """D 系列溯源表：课名 -> [编号]（去重）"""
    path = os.path.join(ROOT, "05_自主学习/00-缺口账/_laws_lecture_index.csv")
    if not os.path.exists(path):
        return {}
    def norm(x):
        x = re.sub(r"[（(].*?[）)]", "", x)
        for ch in "· 　_":
            x = x.replace(ch, "")
        x = re.sub(r"[《》]", "", x)
        return re.sub(r"课$", "", x).strip()
    d = collections.defaultdict(set)
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        m = re.search(r"(\d{2,4})$", r["D号"])
        if m:
            d[norm(r["课名"])].add(int(m.group(1)))
    return d


def match_courses(src, lectures):
    """把透镜的来源课程切成若干段，逐段在溯源表里找课；返回命中的课名"""
    segs = [x for x in re.split(r"[＋+加]", re.sub(r"[（(].*?[）)]", "", src)) if x.strip()]
    found = []
    def norm(x):
        for ch in "· 　_":
            x = x.replace(ch, "")
        return re.sub(r"课$", "", re.sub(r"[《》]", "", x)).strip()
    for seg in segs:
        n = norm(seg)
        if not n:
            continue
        for k in lectures:
            if not k or len(k) < 3:
                continue
            if n == k or (len(k) >= 4 and (k in n or n in k)):
                if k not in found:
                    found.append(k)
                break
    return found


def rng(prefix, nums):
    return f"{prefix}{min(nums):03d}–{prefix}{max(nums):03d}" if nums else ""


def main():
    lenses = load_lenses()
    pref = load_packages()
    mmap = load_modelmap()
    lectures = load_lecture_index()

    # 1) 课程前缀律表索引
    out_pkg = os.path.join(ROOT, "03_思维模型库/_课程前缀律表索引.csv")
    pkg_rows = []
    for p, d in sorted(pref.items()):
        for num, (code, name, one, pkg) in sorted(d.items()):
            pkg_rows.append([code, name, one, pkg, p])
    with open(out_pkg, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["律号", "律名", "一句话", "技能包", "前缀"])
        w.writerows(pkg_rows)

    # 2) 透镜对照表
    rows = []
    for c, v in sorted(lenses.items()):
        try:
            ni = int(v["n"])
        except ValueError:
            ni = 0
        lst = v["listed"]
        diff = ""
        if lst and ni and len(lst) != ni:
            if len(lst) > ni:
                diff = f"条数字段只记代表模型（清单 {len(lst)}，声明 {ni}）"
            else:
                diff = f"清单缺口 {len(lst)}/{ni}"
        # 区间来源优先级：清单 > 技能包律表 > 模型地图推定 > 无
        if lst:
            r, basis = f"{lst[0]}–{lst[-1]}", "透镜全量清单"
        elif c in pref:
            r, basis = rng(c, pref[c].keys()), f"技能包律表（{len(pref[c])} 条）"
        elif match_courses(v["src"], lectures):
            cs = match_courses(v["src"], lectures)
            segs = []
            for k in cs[:3]:
                nums = lectures[k]
                segs.append(f"D{min(nums):03d}–D{max(nums):03d}")
            r = "；".join(segs)
            basis = f"课程对齐（{len(cs)} 门：{'、'.join(cs[:2])}{'…' if len(cs)>2 else ''}）"
        elif mmap.get(c):
            r, basis = f"{c}{min(mmap[c]):03d}–{c}{max(mmap[c]):03d}", "模型地图 id（推定）"
        else:
            r, basis = "", "无"
        if basis.startswith("技能包律表") and ni and len(pref[c]) != ni:
            diff = (diff + "；" if diff else "") + f"律表行 {len(pref[c])} 与透镜模型数 {ni} 口径不同"
        rows.append([c, v["name"], v["grp"], ni, len(lst),
                     "完整" if lst and len(lst) == ni else ("无全量清单" if not lst else "清单不全"),
                     r, basis, v["src"], diff])

    out_csv = os.path.join(ROOT, "03_思维模型库/_透镜课程律号对照表.csv")
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["透镜码", "透镜名", "群", "声明条数", "清单条数", "清单状态",
                    "律号区间", "区间依据", "来源课程", "差异"])
        w.writerows(rows)

    # 3) Markdown
    basis_c = collections.Counter(r[7].split("（")[0] for r in rows)
    md = ["# 透镜 ↔ 课程 ↔ 律号 对照表", "",
          "> 生成于 2026-11-20（B6）。区间一律按实际存在的编号计算，不采用文档头部的宣称。",
          "> 数据源：`12-神经网络/02 透镜/*.md`、技能包律表（<S2>/*/SKILL.md）、`模型地图.md`（仅推定用）。",
          "> 机器可读版：同目录 `_透镜课程律号对照表.csv`；律号明细见 `_课程前缀律表索引.csv`；D 系列溯源见 `05_自主学习/00-缺口账/_laws_lecture_index.csv`。", "",
          "## 一、结论", ""]
    md.append(f"- 透镜 **{len(rows)}** 个，全部带「来源课程」；区间可定位 **{sum(1 for r in rows if r[6])}** 个，无区间 **{sum(1 for r in rows if not r[6])}** 个。")
    md.append("- 区间依据分布：" + "、".join(f"{k} {v} 个" for k, v in basis_c.items()))
    md.append(f"- 口径提示 **{sum(1 for r in rows if r[9])}** 个（清单缺口 / 条数字段语义 / 律表与模型数口径不同，见第三节）。")
    md.append("")
    md.append("## 二、全部透镜（%d）" % len(rows))
    md.append("")
    md.append("| 透镜码 | 透镜名 | 群 | 声明 | 清单 | 律号区间 | 区间依据 | 来源课程 |")
    md.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(f"| {r[0]} | {r[1]} | G{r[2]} | {r[3]} | {r[4]} | {r[6] or '—'} | {r[7]} | {r[8]} |")
    md.append("")
    md.append("## 三、差异与待补")
    md.append("")
    bad = [r for r in rows if r[9] or not r[6]]
    if bad:
        md.append("| 透镜码 | 问题 | 来源课程 |")
        md.append("|---|---|---|")
        for r in bad:
            md.append(f"| {r[0]} | {r[9] or '无律号区间（技能包与模型地图都取不到）'} | {r[8]} |")
    else:
        md.append("无。")
    md.append("")
    md.append("## 四、怎么用")
    md.append("")
    md.append("1. 问「某透镜有哪些律」→ 查本表第 `律号区间` 列，再按区间去 `_课程前缀律表索引.csv` 或 `_laws_lecture_index.csv` 取明细。")
    md.append("2. 问「这条律出自哪门课第几讲」→ D 系列查 `_laws_lecture_index.csv`（含讲次/精度/锚点句）；课程前缀系列查 `_课程前缀律表索引.csv` 再回到技能包正文。")
    md.append("3. 问「哪个透镜还没上全量」→ 本表 `清单状态=无全量清单` 的行。")
    md.append("")

    out_md = os.path.join(ROOT, "03_思维模型库/透镜课程律号对照表.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(md) + "\n")

    print("透镜", len(rows), "| 有区间", sum(1 for r in rows if r[6]),
          "| 依据", dict(basis_c), "| 差异行", sum(1 for r in rows if r[9]))
    print("课程前缀律表行", len(pkg_rows), "前缀", len(pref))


if __name__ == "__main__":
    main()
