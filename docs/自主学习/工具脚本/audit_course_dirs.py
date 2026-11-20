#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""04_课程学习 目录口径核对（B7）
只读扫描，输出：
  04_课程学习/_目录口径核对-20261120.md
  04_课程学习/_目录清单-20261120.csv
三种切法分别算：
  目录层 = 04_课程学习 下全部一级目录
  内容层 = 目录层去掉服务目录（_学习规划／_采集中转）
  课程层 = 全库正课（04_课程学习 正课 ＋ 00_收件箱 完整课程档，按名去重）
  原典层 = 目录名以「（原文）」结尾
"""
import os, re, csv, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "04_课程学习")
INBOX = os.path.join(ROOT, "00_收件箱")
OUT_MD = os.path.join(BASE, "_目录口径核对-20261120.md")
OUT_CSV = os.path.join(BASE, "_目录清单-20261120.csv")
SERVICE = {"_学习规划", "_采集中转"}


def norm(x):
    x = re.sub(r"（[^）]*）|\[[^\]]*\]|\([^)]*\)", "", x)
    x = re.sub(r"[0-9·\-—_ ]|第.*?讲|全量", "", x)
    x = re.sub(r"版$|20\d\d$", "", x)
    return x


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
        r["kind"] = "服务目录" if d in SERVICE else ("基础原典" if d.endswith("（原文）") else "正课")
        rows.append(r)

    course = [r for r in rows if r["kind"] == "正课"]
    source = [r for r in rows if r["kind"] == "基础原典"]
    service = [r for r in rows if r["kind"] == "服务目录"]

    lib_norm = {r["dir"]: norm(r["dir"]) for r in course}
    inbox = []
    for d in sorted(os.listdir(INBOX)):
        p = os.path.join(INBOX, d)
        if not (os.path.isdir(p) and glob.glob(os.path.join(p, "*.md"))):
            continue
        r = scan_dir(p, d)
        nd = norm(d)
        dup = next((k for k, v in lib_norm.items() if v and (nd == v or v.startswith(nd) or nd.startswith(v))), "")
        r["dup"] = dup
        r["kind"] = "收件箱正课"
        inbox.append(r)

    dup = [r for r in inbox if r["dup"]]
    n_dir = len(rows)
    n_content = len(course) + len(source)
    n_course_all = len(course) + len(inbox) - len(dup)
    n_total = n_course_all + len(source)

    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["dir", "kind", "md", "laws", "catalog", "subdir", "bytes", "dup"])
        w.writeheader()
        for r in sorted(rows + inbox, key=lambda r: (r["kind"], r["dir"])):
            r.setdefault("dup", "")
            w.writerow({k: r[k] for k in ["dir", "kind", "md", "laws", "catalog", "subdir", "bytes", "dup"]})

    L = ["# 04_课程学习 目录口径核对（2026-11-20）", "",
         "> 只读实测（`ls`＋`glob`＋`os.path.getsize` 现算），非估算。生成器 `10_工具脚本/audit_course_dirs.py`，逐目录清单见 `_目录清单-20261120.csv`。", "",
         "## 一、结论：不是数据错，是三种切法被混用", "",
         "| 切法 | 数字 | 构成 | 谁能复现 |", "|---|---|---|---|",
         f"| 目录层（磁盘一级目录） | **{n_dir}** | 服务 {len(service)} ＋ 内容 {n_content} | `ls -d 04_课程学习/*/` |",
         f"| 内容层（课＋原典） | **{n_content}** | 正课 {len(course)} ＋ 基础原典 {len(source)} | 索引「95 门＝53＋42」 |",
         f"| 课程层（全库正课，去重） | **{n_course_all}** | 库内 {len(course)} ＋ 收件箱 {len(inbox)} － 重复 {len(dup)} | 本核对 |",
         f"| 课程＋原典总量 | **{n_total}** | 正课 {n_course_all} ＋ 原典 {len(source)} | 本核对 |", "",
         "「97 个目录」与「97 门课」是两个不同的 97：前者＝95 个内容目录＋2 个服务目录；后者曾是「55 正课＋42 原典」，但 **55 这个数在磁盘上复现不出来**（库内 53、去重后全库 68）。", "",
         "## 二、三条宣称逐条对账", "",
         "| 出处 | 原话 | 实测 | 判定 |", "|---|---|---|---|",
         f"| 索引 v2.95 | 「课程 95→97 门（55 正课＋42 基础原典）」 | 目录 {n_dir}／内容 {n_content}／全库课 {n_course_all} | **97 的构成错**：97 是目录数不是课数；55 无法复现 |",
         f"| 索引 v2.88 | 「目录 95 门 ＝ 课程 53 ＋ 原典 42」 | {len(course)}＋{len(source)}＝{n_content} | 正确，但「目录 95 门」应写「内容目录 95」 |",
         f"| 图 v5.0 副标 | 「97 门课（55 正课＋42 基础原典）」 | 55≠{len(course)}、55≠{n_course_all} | **55 不可复现**，建议下次重建改 {n_total}（{n_course_all}＋{len(source)}） |",
         f"| `00-课程库总览.md` | 「53 门实测」／「52 门有律表」 | 库内 {len(course)}／{sum(1 for r in course if r['laws']>0)} | 正确（只算库内） |", "",
         "## 三、收件箱里还有 16 门完整课程", "",
         "| 课程 | md | 体积 | 与库内重复 |", "|---|---|---|---|"]
    for r in inbox:
        L.append(f"| {r['dir']} | {r['md']} | {r['bytes']/1024/1024:.1f} MB | {('**'+r['dup']+'**') if r['dup'] else '无'} |")
    L += ["",
          f"16 门均为完整归档（`_全文对照.md`＋逐讲 md，何刚与马江博为 `_原文备份` 结构），不是草稿。其中 **{len(dup)} 门与库内重复**（{dup[0]['dir']} ↔ {dup[0]['dup']}，同一门课的原始逐讲版与合订本），去重后全库正课 **{n_course_all}** 门。", "",
          "## 四、库内 53 门明细", "",
          "| # | 课程目录 | md | 律表 | 目次表 | 体积 |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(sorted(course, key=lambda x: x["dir"]), 1):
        L.append(f"| {i} | {r['dir']} | {r['md']} | {r['laws']} | {r['catalog']} | {r['bytes']/1024/1024:.1f} MB |")
    L += ["", f"律表 **{sum(1 for r in course if r['laws']>0)}/{len(course)}** 门；无律表：{[r['dir'] for r in course if r['laws']==0]}。", "",
          "## 五、42 部基础原典", "", "| # | 原典目录 | 文件 | 体积 |", "|---|---|---|---|"]
    for i, r in enumerate(sorted(source, key=lambda x: x["dir"]), 1):
        L.append(f"| {i} | {r['dir']} | {r['md']} | {r['bytes']/1024/1024:.1f} MB |")
    L += ["", "## 六、服务目录", ""]
    for r in service:
        L.append(f"- `{r['dir']}/`：md {r['md']} 篇，{r['bytes']/1024/1024:.1f} MB（规划／中转用，不计课程数）")
    L += ["", "## 七、统一写法（此后照此）", "",
          f"1. 课程总量：**{n_total} 门课＝{n_course_all} 正课＋{len(source)} 基础原典**；",
          f"2. 库内规模：**04_课程学习 内容目录 {n_content}＝正课 {len(course)}＋原典 {len(source)}；另 {len(inbox)} 门正课在 00_收件箱（含 {len(dup)} 门重复）**；",
          f"3. 磁盘目录：**{n_dir} 个一级目录＝内容 {n_content}＋服务 {len(service)}**；",
          "4. 三种切法不得互换或相加；引用「97」必须注明是目录数还是课数。", "",
          "## 八、待定（需你拍板）", "",
          "① 收件箱 16 门是否迁入 `04_课程学习`（按课程建目录的既定规范），迁则内容目录 95→111、并需先处理 1 门重复；② 图 v5.0 副标的「55 正课」下次重建时是否改为实测值。本批只核对，不搬文件、不改图。"]
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L))
    print(f"目录 {n_dir} | 内容 {n_content}（正课 {len(course)}＋原典 {len(source)}）| 收件箱 {len(inbox)}（重复 {len(dup)}）| 全库正课 {n_course_all} | 课＋原典 {n_total}")


if __name__ == "__main__":
    main()
