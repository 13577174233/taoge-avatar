#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""04_课程学习 目录口径核对（B7 建立，B8 迁入后 v2）
只读扫描，输出：
  04_课程学习/_目录口径核对-20261120.md
  04_课程学习/_目录清单-20261120.csv
切法（迁入后）：
  目录层 = 04_课程学习 下全部一级目录
  内容层 = 目录层去掉服务目录（_学习规划／_采集中转）
  正课   = 内容层去掉「（原文）」结尾的原典
  全库正课 = 库内正课 ＋ 00_收件箱残留课程档
说明：2026-11-20 起 00_收件箱 16 门已迁入；马江博原始逐讲版作为子目录并入
      马江博政经参考2025/_原始逐讲版，不单独计一门课。
"""
import os, re, csv, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "04_课程学习")
INBOX = os.path.join(ROOT, "00_收件箱")
OUT_MD = os.path.join(BASE, "_目录口径核对-20261120.md")
OUT_CSV = os.path.join(BASE, "_目录清单-20261120.csv")
SERVICE = {"_学习规划", "_采集中转"}

# 2026-11-20 从 00_收件箱 迁入的 15 门（原始逐讲档，未转合订本／律表）
MIGRATED = {
    "5分钟商学院·实战", "何刚财经大课", "刘润商业洞察力30讲", "刘澜领导力30讲",
    "吴军阅读写作50讲", "宁向东管理学课", "小马宋营销实战22讲", "李笑来财富自由之路",
    "梁宁产品增长", "薛兆丰经济学课", "认知训练营", "贾宁财务思维课",
    "跟华杉学品牌营销30讲", "陆蓉行为金融学", "香帅北大金融学课",
}
# 并入既有课程目录的原始版（不新增一级目录）
MERGED = {"马江博政经参考": "马江博政经参考2025/_原始逐讲版"}


def scan_dir(p, d):
    mds = glob.glob(os.path.join(p, "*.md"))
    return dict(dir=d, md=len(mds),
                laws=sum(1 for m in mds if "_laws" in os.path.basename(m)),
                catalog=sum(1 for m in mds if "_catalog" in os.path.basename(m)),
                subdir=sum(1 for x in os.listdir(p) if os.path.isdir(os.path.join(p, x))),
                bytes=sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(p) for f in fs))


def main():
    rows = []
    for d in sorted(x for x in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, x))):
        r = scan_dir(os.path.join(BASE, d), d)
        if d in SERVICE:
            r["kind"] = "服务目录"
        elif d.endswith("（原文）"):
            r["kind"] = "基础原典"
        elif d in MIGRATED:
            r["kind"] = "正课（迁入·原始档）"
        else:
            r["kind"] = "正课"
        rows.append(r)

    course = [r for r in rows if r["kind"].startswith("正课")]
    source = [r for r in rows if r["kind"] == "基础原典"]
    service = [r for r in rows if r["kind"] == "服务目录"]
    migrated = [r for r in rows if r["kind"] == "正课（迁入·原始档）"]

    inbox = []
    if os.path.isdir(INBOX):
        for d in sorted(os.listdir(INBOX)):
            p = os.path.join(INBOX, d)
            if os.path.isdir(p) and glob.glob(os.path.join(p, "*.md")):
                r = scan_dir(p, d)
                r["kind"] = "收件箱正课"
                r["dup"] = ""
                inbox.append(r)

    n_dir = len(rows)
    n_content = len(course) + len(source)
    n_course_all = len(course) + len(inbox)
    n_total = n_course_all + len(source)
    n_laws = sum(1 for r in course if r["laws"] > 0)
    no_laws = [r["dir"] for r in course if r["laws"] == 0]
    n_left = len(course) - len(migrated)

    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["dir", "kind", "md", "laws", "catalog", "subdir", "bytes", "dup"])
        w.writeheader()
        for r in sorted(rows + inbox, key=lambda r: (r["kind"], r["dir"])):
            r.setdefault("dup", "")
            w.writerow({k: r[k] for k in ["dir", "kind", "md", "laws", "catalog", "subdir", "bytes", "dup"]})

    L = ["# 04_课程学习 目录口径核对（2026-11-20，迁入后）", "",
         "> 只读实测（`ls`＋`glob`＋`os.path.getsize` 现算），非估算。生成器 `10_工具脚本/audit_course_dirs.py`，逐目录清单见 `_目录清单-20261120.csv`。",
         "> 2026-11-20 已按拍板执行：`00_收件箱` 16 门迁入，马江博原始逐讲版并入既有课程目录，收件箱清空。", "",
         "## 一、结论：一个数只能有一种切法", "",
         "| 切法 | 数字 | 构成 | 谁能复现 |", "|---|---|---|---|",
         f"| 目录层（磁盘一级目录） | **{n_dir}** | 内容 {n_content} ＋ 服务 {len(service)} | `ls -d 04_课程学习/*/` |",
         f"| 内容层（课＋原典） | **{n_content}** | 正课 {len(course)} ＋ 基础原典 {len(source)} | 本核对 |",
         f"| 正课（全库） | **{n_course_all}** | 库内 {len(course)} ＋ 收件箱残留 {len(inbox)} | 本核对 |",
         f"| 课程＋原典总量 | **{n_total}** | 正课 {n_course_all} ＋ 原典 {len(source)} | 本核对 |", "",
         f"迁入前：目录 97＝内容 95（正课 {n_left}＋原典 {len(source)}）＋服务 2；全库正课 68＝53＋收件箱 16－重复 1。迁入后 97→{n_dir}、53→{len(course)}、68 不变。", "",
         "## 二、四条旧宣称逐条对账", "",
         "| 出处 | 原话 | 实测 | 判定 |", "|---|---|---|---|",
         "| 索引 v2.95 | 「课程 95→97 门（55 正课＋42 基础原典）」 | 97 是当时的目录数；55 从未在磁盘出现 | **构成错**，已加注更正 |",
         f"| 索引 v2.88 | 「目录 95 门 ＝ 课程 {n_left} ＋ 原典 {len(source)}」 | {n_left}＋{len(source)}＝95 | 当时正确，现为迁入前口径 |",
         f"| 图 v5.0 副标 | 「97 门课（55 正课＋42 基础原典）」 | 正课 {len(course)}、总量 {n_total} | **待重建时改 {n_total}（{n_course_all}＋{len(source)}）** |",
         "| `00-课程库总览.md` | 「53 门实测」／「52 门有律表」 | 迁入前 53／52 | 当时正确，现表已扩到 68 门 |", "",
         "## 三、16 门迁入落点", "",
         "| 原收件箱目录 | 落点 | md | 体积 |", "|---|---|---|---|"]
    for r in sorted(migrated, key=lambda x: -x["md"]):
        L.append(f"| {r['dir']} | `04_课程学习/{r['dir']}` | {r['md']} | {r['bytes']/1024/1024:.1f} MB |")
    mp = os.path.join(BASE, MERGED["马江博政经参考"])
    nmd = len(glob.glob(os.path.join(mp, "**/*.md"), recursive=True))
    nby = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(mp) for f in fs)
    L += [f"| 马江博政经参考 | `04_课程学习/{MERGED['马江博政经参考']}`（并入既有课程，不新增一级目录） | {nmd} | {nby/1024/1024:.1f} MB |", "",
          f"15 门新目录＋1 门并入，内容均为原始逐讲档（`_全文对照.md`＋逐讲 md，何刚与马江博另有 `_原文备份`），**未转库内三件套**（完整目录索引／笔记合订本／全文合订本／`_laws` 律表）。迁移只挪目录，未改一字。", "",
          "## 四、正课 68 门明细", "",
          "| # | 课程目录 | md | 律表 | 目次表 | 体积 | 来源 |", "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(sorted(course, key=lambda x: x["dir"]), 1):
        src = "迁入·原始档" if r["dir"] in MIGRATED else "库内"
        L.append(f"| {i} | {r['dir']} | {r['md']} | {r['laws']} | {r['catalog']} | {r['bytes']/1024/1024:.1f} MB | {src} |")
    L += ["", f"律表 **{n_laws}/{len(course)}** 门；无律表 {len(no_laws)} 门：{'、'.join(no_laws)}。其中 15 门为迁入原始档（待转档，非缺失），1 门为「吴军来信2（年度日更）」（透镜已撤下）。", "",
          "## 五、42 部基础原典", "", "| # | 原典目录 | 文件 | 体积 |", "|---|---|---|---|"]
    for i, r in enumerate(sorted(source, key=lambda x: x["dir"]), 1):
        L.append(f"| {i} | {r['dir']} | {r['md']} | {r['bytes']/1024/1024:.1f} MB |")
    L += ["", "## 六、服务目录", ""]
    for r in service:
        L.append(f"- `{r['dir']}/`：md {r['md']} 篇，{r['bytes']/1024/1024:.1f} MB（规划／中转用，不计课程数）")
    L += ["", "## 七、统一写法（此后照此）", "",
          f"1. 课程总量：**{n_total} 门＝{n_course_all} 正课＋{len(source)} 基础原典**；",
          f"2. 库内规模：**04_课程学习 内容目录 {n_content}＝正课 {len(course)}＋原典 {len(source)}**（其中 {len(migrated)} 门为 2026-11-20 迁入原始档）；",
          f"3. 磁盘目录：**{n_dir} 个一级目录＝内容 {n_content}＋服务 {len(service)}**；",
          "4. 迁入档未建三件套，引用时注明「原始逐讲档」；",
          "5. 三种切法不得互换或相加；写数字必须带层名。", "",
          "## 八、待办", "",
          "① 15 门迁入档转库内三件套（目录索引／笔记合订本／全文合订本／律表）；② 图 v5.0 副标「55 正课」下次重建时改为 110；③ 马江博合订本＋原始逐讲双版本长期并存是否接受。"]
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L))
    print(f"目录 {n_dir} | 内容 {n_content}（正课 {len(course)}＋原典 {len(source)}）| 收件箱 {len(inbox)} | 正课合计 {n_course_all} | 课＋原典 {n_total} | 律表 {n_laws}/{len(course)}")


if __name__ == "__main__":
    main()
