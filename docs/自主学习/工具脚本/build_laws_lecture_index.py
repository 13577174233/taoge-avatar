#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 · 律号溯源表 v2：把 03-蒸馏入库 的每条律映射到「课名 + 讲次/块次 + 来源文件」。
v1 缺陷（2026-11-19 审计实锤）：
  1) 只认「### D1234 标题」空格格式，`### D1234｜律名｜k1 标题` 竖线格式全漏 → 律名空、讲次空、落 B；
  2) 课名按文件首条来源写死并回灌全文 → 早期多课合辑文件整文件被标成同一课。
v2 改法：
  1) 新增竖线格式；k 块记为「k001」精度 A（块），第N讲记为「第NNN讲」精度 A；
  2) 课名优先取文件头「# 新增律 …｜课名（…）」，否则逐行取本条来源里的课名，取不到标「未标注课程」。
只读扫描，不改既有文件。
"""
import os, re, csv, glob, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "05_自主学习/03-蒸馏入库")
OUT = os.path.join(BASE, "05_自主学习/00-缺口账/_laws_lecture_index.csv")
REPORT = os.path.join(BASE, "05_自主学习/00-缺口账/_laws_lecture_index_报告.md")

LAW = re.compile(r"^#{2,4}\s*[【\[]?([A-Z]{1,3}\d{3,4})[】\]]?\s*([^｜|]*?)\s*(?:｜|\||$)")
LAW_PIPE = re.compile(r"^#{2,4}\s*[【\[]?([A-Z]{1,3}\d{3,4})[】\]]?\s*｜\s*([^｜|]+?)\s*(?:｜\s*(.*))?$")
LAW_B = re.compile(r"^\*\*(.+?)｜\s*([A-Z]{1,3}\d{3,4})\s*｜(.+?)\*\*")
SRCLINE = re.compile(r"^\s*-?\s*(?:\*\*)?来源(?:\*\*)?[：:]\s*(.+)$")
ANCHOR = re.compile(r"锚点句[：:]\s*「(.+?)」")
LEC = re.compile(r"第(\d{1,3})讲")
KEC = re.compile(r"[kK](\d{1,3})")
LOC = re.compile(r"(第[0-9一二三四五六七八九十百]+[讲章篇节])[丨|｜|：: ]?\s*(.{0,40})")
RAW = re.compile(r"_raw_([^_\n]+?)(?:_全文|\.txt)")

rows = []
files = [f for f in sorted(glob.glob(os.path.join(SRC, "*.md"))) if not os.path.basename(f).startswith("_")]
for f in files:
    name = os.path.basename(f)
    text = open(f, encoding="utf-8", errors="ignore").read()
    head = next((l for l in text.splitlines() if l.startswith("# ")), "")
    m_raw = RAW.search(text)
    course = ""
    if m_raw:
        course = m_raw.group(1)
    else:
        mh = re.match(r"#\s*新增律.*?｜([^（(｜]+)[（(]", head)
        if not mh:
            mh = re.match(r"#\s*分?律?表?\s*｜\s*([^（(｜]+)[（(]", head)
        if mh:
            course = mh.group(1).strip()[:24]
    if course.startswith("<"):
        course = ""
    if not course:
        mfn = re.match(r"\d{8}-新增律[A-Z0-9\-]+?-([^B\-]+?)(?:B\d|-\d+讲|\d+讲|\.md)", name)
        if mfn:
            cand = mfn.group(1).strip("-_")[:24]
            course = "" if ("门课" in cand or "合辑" in cand or "多课" in cand) else cand
    lects = re.findall(r"(?:本批读|读完|读)\s*[0-9]*\s*讲[：:]\s*([0-9A-Za-z/－\-–、,， ]{6,})", text)
    file_lects = ""
    if lects:
        file_lects = "、".join(sorted(set(re.findall(r"\b\d{1,3}\b", lects[0])), key=lambda x: int(x))[:80])
    m_range = re.search(r"第?(\d{1,3})\s*[–\-~]\s*(\d{1,3})\s*讲", name + head)
    file_range = f"{m_range.group(1)}–{m_range.group(2)}讲" if m_range else file_lects

    lines = text.splitlines()
    for i, ln in enumerate(lines):
        t = ln.strip()
        mp = LAW_PIPE.match(t)
        m = None if mp else LAW.match(t)
        mb = LAW_B.match(t) if not (mp or m) else None
        if not (mp or m or mb):
            continue
        if mp:
            lid, title, rest = mp.group(1), (mp.group(2) or "").strip(" 丨|｜"), (mp.group(3) or "").strip()
            row_course = course
            if not row_course:
                row_course = re.split(r"｜|\|", rest)[0].strip()[:24] or "未标注课程"
                src_c = ""
                for j in range(i + 1, min(i + 8, len(lines))):
                    sm = SRCLINE.match(lines[j].strip())
                    if sm:
                        src_c = re.split(r"（|\||｜", sm.group(1))[0].strip()[:30]
                        break
                if src_c:
                    row_course = src_c
            mk = KEC.search(rest)
            ml = LEC.search(rest)
            if ml:
                lect, prec = "第%03d讲" % int(ml.group(1)), "A"
            elif mk:
                lect, prec = "k%03d" % int(mk.group(1)), "A（块）"
            else:
                lect, prec = "", "B"
            ltitle = re.sub(r"^(?:[kK]\d{1,3}|第\d{1,3}讲)\s*", "", rest)
            rows.append([lid, title, row_course, lect, ltitle[:40] or title[:40], prec,
                         file_range, "", name, rest[:60]])
            continue
        if mb:
            title, lid, srcfield = mb.group(1).strip(), mb.group(2), mb.group(3)
            lect, prec = "", "B"
            ml = LEC.search(srcfield)
            if ml:
                lect, prec = "第%03d讲" % int(ml.group(1)), "A"
            rows.append([lid, title, row_course, lect,
                         re.split(r"[（(]", srcfield, maxsplit=1)[0].strip()[:40], prec,
                         file_range, "", name, srcfield[:60]])
            continue
        # 空格格式：向下找来源行
        lid, title = m.group(1), (m.group(2) or "").strip(" 丨|｜")
        lect, ltitle, anchor, prec = "", "", "", "B"
        appended = False
        for j in range(i + 1, min(i + 16, len(lines))):
            s = SRCLINE.match(lines[j].strip())
            if not s:
                continue
            raw = s.group(1)
            ma = ANCHOR.search(raw)
            if ma:
                anchor = ma.group(1)[:160]
            ml = LEC.search(raw)
            mk = KEC.search(raw)
            if ml:
                lect = "第%03d讲" % int(ml.group(1)); prec = "A"
                rest = raw.split("讲", 1)[1] if "讲" in raw else ""
                ltitle = re.split(r"[丨|｜|]|锚点句", rest, maxsplit=1)[0].strip(" 丨|｜：:「」")[:40]
            elif mk:
                lect, prec = "k%03d" % int(mk.group(1)), "A（块）"
                ltitle = re.split(r"[丨|｜|]|锚点句", raw, maxsplit=1)[0].strip()[:40]
            elif ("私董会" in raw) and (ms := re.search(r"SW(\d{3})", raw)):
                # 私董会/实战块：块号 SWxxx ≠ 讲号，按 A（块）口径入表；
                # 混排块若文内已注明「讲NNN」（讲次=SW号−1），以讲号为准
                if (ms2 := re.search(r"讲(\d{3})", raw)):
                    lect, prec = "第%s讲" % ms2.group(1), "A"
                else:
                    lect, prec = "SW" + ms.group(1), "A（块）"
                ltitle = re.split(r"[丨|｜|]|锚点句", raw, maxsplit=1)[0].strip()[:40]
            else:
                mo = LOC.search(raw)
                if mo:
                    lect, ltitle = mo.group(1), mo.group(2).strip(" 丨|｜。：:「」")[:40]
            ltitle = ltitle or raw[:40].strip()
            if not course:
                head_part = re.split(r"[丨|｜]", raw)[0].strip()
                head_part = re.sub(r"^(?:第\d{1,3}讲|[kK]\d{1,3})\s*[：:丨|｜]?\s*", "", head_part)
                if 4 <= len(head_part) <= 24 and not head_part.startswith("第"):
                    row_course = head_part[:24]
                else:
                    row_course = "未标注课程"
            else:
                row_course = course
            rows.append([lid, title, row_course, lect, ltitle, prec,
                         file_range, anchor, name, raw[:60]])
            appended = True
            break
        if not appended:
            rows.append([lid, title, row_course, "", title[:40], "B",
                         file_range, "", name, title[:60]])

dedup = {}
for r in rows:
    cur = dedup.get(r[0])
    if cur is None or (cur[5] == "B" and r[5] != "B"):
        dedup[r[0]] = r
if os.path.exists(OUT):
    try:
        prev = {r["D号"]: r for r in csv.DictReader(open(OUT, encoding="utf-8-sig"))}
        for k, r in list(dedup.items()):
            q = prev.get(k)
            if q and q.get("精度", "").startswith("A") and r[5] == "B":
                r[3], r[4], r[5] = q["讲次/章次"], q["定位标题"], q["精度"]
            if q and not r[7] and q.get("锚点句"):
                r[7] = q["锚点句"]
                if r[5] == "A":
                    r[5] = "A（锚定）"
    except Exception as e:
        print("merge skipped:", e)
rows = [dedup[k] for k in sorted(dedup, key=lambda x: (len(x), x))]

# ---- 课名归一段：清碎片、贴白名单 ----
def _norm_c(s):
    s = re.sub(r"[·\s_（）()]", "", s).replace("的", "")
    s = re.sub(r"(全文|试读.*)", "", s)
    s = re.sub(r"\d+讲|课$|上部", "", s)
    return s

def _clean_c(s):
    s = re.sub(r"\s*[Bb]\d{1,3}\s*$", "", s).strip()
    s = re.sub(r"^(第\d{1,3}讲|[kK]\d{1,3}|[A-Z]{1,3}\d{2,4})\s*[：:丨|｜]?\s*", "", s).strip()
    if not s or re.fullmatch(r"[A-Z]{1,3}\d{2,4}", s) or ("批" in s) or ("首蒸" in s) or ("门课" in s):
        return ""
    return s

wl = {}
lp = os.path.join(BASE, "05_自主学习/00-缺口账/_已读登记.json")
if os.path.exists(lp):
    import json as _json
    for k in _json.load(open(lp, encoding="utf-8")).get("courses", {}):
        wl.setdefault(_norm_c(k), k)
wl.setdefault("香帅北大金融学", "香帅北大金融学课")
wl.setdefault("何刚财经大", "何刚财经大课")

# 头部/行内简称 → 白名单课名（仅在候选串含该简称时启用）
ALIAS = {
    "来信2": "吴军来信2（年度日更）",
    "硅谷来信": "吴军·硅谷来信3",
    "论语": "靳大成·论语通读（上部）",
    "金刚经": "王路·金刚经50讲",
    "Dr.魏": "Dr. 魏的家庭教育宝典",
    "Dr魏": "Dr. 魏的家庭教育宝典",
    "Dr. 魏": "Dr. 魏的家庭教育宝典",
    "启发俱乐部": "罗辑思维·启发俱乐部",
    "科技参考": "卓克·科技参考5",
    "中世纪史纲": "李筠·中世纪史纲30讲",
    "小店创业": "黄碧云·怎样让店铺持续增长",
    "智能交通": "李彦宏·智能交通7讲",
    "民法典": "清华法学院解读民法典",
    "文明之旅": "《文明之旅》节目说明书",
    "风险管理": "张晓燕·风险管理课_全文",
    "批判性思维": "蔡钰批判性思维17讲",
    "家庭教育宝典": "Dr. 魏的家庭教育宝典",
    "科技史纲": "吴军·科技史纲60讲_全文",
    "信息论": "吴军·信息论40讲_全文",
    "香帅": "香帅北大金融学课",
    "陆蓉": "陆蓉行为金融学",
    "施展": "施展中国史纲时间篇",
    "梁宁·产品增长": "梁宁产品增长",
    "梁宁产品增长": "梁宁产品增长",
    "万维钢·现代思维": "万维钢·现代思维工具121讲",
    "万维钢精英日课": "万维钢精英日课6",
    "李笑来财富自由": "李笑来财富自由之路",
    "宁向东": "宁向东管理学课",
    "马江博": "马江博·政经参考（2026）",
    "薄世宁": "薄世宁·医学通识50讲",
    "刘润商业洞察": "刘润商业洞察力30讲",
    "小马宋营销": "小马宋营销23讲",
    "仝卿": "仝卿营养科学20讲",
}

def _external_class(raw):
    """非得到课程的来源，按证据类型归类，避免整库塞满「未标注课程」。"""
    r = raw or ""
    if re.search(r"arXiv|doi\.org|Journal|论文|期刊|SSRN|NBER|working paper|综述|Review", r, re.I):
        return "外部源·学术论文"
    if re.search(r"10-[KQ]|10-Q|10-K|年报|季报|财报|公告|SEC|EDGAR", r, re.I):
        return "外部源·公司披露"
    if re.search(r"白皮书|蓝皮书|报告|研究院|统计局|CNNIC|协会|Gartner|McKinsey|艾瑞|研报|券商", r):
        return "外部源·机构报告"
    if re.search(r"《|》|出版社|第[0-9一二三四五六七八九十]+章|教材|LibreTexts|CERN|教科书|百科|官方", r):
        return "外部源·教材与经典"
    if re.search(r"http|www\.|博客|专栏|公众号|演讲|访谈", r, re.I):
        return "外部源·网络公开材料"
    return "外部源·其他"

def _canon(s, raw=""):
    c = _clean_c(s)
    if not c and raw:
        c = _clean_c(raw[:60])
    n = _norm_c(c)
    if n in wl:
        return wl[n]
    # 白名单名整串被候选串包含（如「XL001 吴军·信息论40讲」「FN01贾宁财务思维课发刊词」）
    for wn, disp in sorted(wl.items(), key=lambda x: -len(x[0])):
        if len(wn) >= 5 and wn in n:
            return disp
    # 简称别名
    for a, disp in ALIAS.items():
        if _norm_c(a) in n:
            return disp
    for wn, disp in wl.items():
        if len(n) >= 4 and len(wn) >= 4 and (n.startswith(wn[:4]) or wn.startswith(n[:4])):
            if abs(len(n) - len(wn)) <= 8:
                return disp
    # 候选串定位不到课时，回到「出处摘要」里挖课名（早期批次的来源行只写「某课第N讲」）
    nr = _norm_c(raw or "")
    for wn, disp in sorted(wl.items(), key=lambda x: -len(x[0])):
        if len(wn) >= 5 and wn in nr:
            return disp
    for a, disp in ALIAS.items():
        if _norm_c(a) in nr:
            return disp
    if re.search(r"第\d{2,3}\s*封|问答\s*\d+", raw or ""):
        return "吴军来信2（年度日更）"
    if re.search(r"第\d{2,3}\s*封|问答\s*\d+", c):
        return "吴军来信2（年度日更）"
    if len(re.findall(r"[\u4e00-\u9fa5]", c)) >= 4 and not raw:
        return c[:26]
    return _external_class(raw) if raw else "未标注课程"

for r in rows:
    r[2] = _canon(r[2], r[9])

# 文件级补课名：整文件未标注率 ≥90% 时，用文件头部与文件名反查白名单/别名（修复合辑与批日志的课名丢失）
_byfile = {}
for r in rows:
    _byfile.setdefault(r[8], [0, 0])
    _byfile[r[8]][0 if r[2] == "未标注课程" or r[2].startswith("外部源") else 1] += 1
_headtext = {}
for fpath in files:
    _headtext[os.path.basename(fpath)] = "\n".join(
        open(fpath, encoding="utf-8", errors="ignore").read().splitlines()[:12]
    )
_fix_default = {}
for fn, (un, lab) in _byfile.items():
    if lab > max(2, un * 0.1):
        continue  # 已有足够明确课名，不做文件级覆盖
    txt = _headtext.get(fn, "") + " " + fn
    n_txt = _norm_c(txt)
    hit = ""
    for wn, disp in sorted(wl.items(), key=lambda x: -len(x[0])):
        if len(wn) >= 5 and wn in n_txt:
            hit = disp
            break
    if not hit:
        for a, disp in ALIAS.items():
            if _norm_c(a) in n_txt:
                hit = disp
                break
    if not hit:
        full = _headtext.get(fn, "") + " " + fn
        if "硅谷来信3" in full:
            hit = "吴军·硅谷来信3"
        elif "来信2" in full:
            hit = "吴军来信2（年度日更）"
        elif re.search(r"第\d{2,3}\s*[-–~至]?\s*\d{0,3}\s*封", full) and "封" in full:
            hit = "吴军来信2（年度日更）"   # 信件批次默认来信2（硅谷来信3 已在上游优先命中）
        elif "阿那亚" in full:
            hit = "跟阿那亚学服务客户"
    if hit:
        _fix_default[fn] = hit
for r in rows:
    if r[2] == "未标注课程" or r[2].startswith("外部源"):
        if r[8] in _fix_default:
            r[2] = _fix_default[r[8]]

# 文件名点名校准：文件名里出现的白名单课名优先于正文抽取（修复分律表误标）
# 但合辑文件（逐行已解析出 ≥2 门课）一律跳过，避免一刀切覆盖
_mixfile = set()
_bycourse = {}
for r in rows:
    if r[2] in ("未标注课程",) or r[2].startswith("外部源"):
        continue
    _bycourse.setdefault(r[8], set()).add(r[2])
for fn, cs in _bycourse.items():
    if len(cs) >= 2:
        _mixfile.add(fn)
_nfn = {}
for r in rows:
    fname = _norm_c(r[8] or "")
    for wn, disp in sorted(wl.items(), key=lambda x: -len(x[0])):
        if len(wn) >= 6 and wn[:3] in fname:
            _nfn.setdefault(r[8], disp)
            break
for r in rows:
    d = _nfn.get(r[8])
    if d:
        r[2] = d

# 混编批次：同一文件内多门课无来源行，按批次构成/块内关键词定点校准
ROW_COURSE = {}
for _n in range(4454, 4459):
    ROW_COURSE[f"D{_n}"] = "贾宁·财务分析课"
ROW_COURSE["D4459"] = "罗辑思维·启发俱乐部"
for _n in range(4460, 4464):
    ROW_COURSE[f"D{_n}"] = "外部源·学术论文"
for _n in range(4516, 4519):
    ROW_COURSE[f"D{_n}"] = "罗辑思维·启发俱乐部"
for _n in range(4519, 4526):
    ROW_COURSE[f"D{_n}"] = "外部源·机构报告"
for r in rows:
    if r[0] in ROW_COURSE:
        r[2] = ROW_COURSE[r[0]]
    if "D4184-D4193" in r[8]:
        _n = int(r[0][1:]) if r[0].startswith("D") else 0
        if 4184 <= _n <= 4186:
            r[2] = "李彦宏·智能交通7讲"
        elif 4187 <= _n <= 4192:
            r[2] = "清华法学院解读民法典"
        elif _n == 4193:
            r[2] = "《文明之旅》节目说明书"

for r in rows:
    if "D1212-D1249" in r[8] or "小马宋营销+蔡钰" in r[8]:
        r[2] = "小马宋营销实战22讲" if ("小马宋" in (r[4] or "") + (r[9] or "")) else "蔡钰批判性思维17讲"

MED_KEYS = [("高血脂", "冯雪·高血脂医学课"), ("高血糖", "冯雪·高血糖医学课"),
            ("高尿酸", "冯雪·高尿酸医学课"), ("高血压", "冯雪·高血压医学课")]
for r in rows:
    if r[2] == "冯雪·家庭健康管理100讲" or r[2].startswith("外部源") or r[2] == "未标注课程":
        for kw, disp in MED_KEYS:
            if kw in (r[4] or "") + (r[9] or ""):
                r[2] = disp
                break

# 硬校准：整文件课名明确但正文串被别课名污染的文件
HARD_FILE = {"第2周-阿那亚服务客户律": "跟阿那亚学服务客户"}
for r in rows:
    for k, disp in HARD_FILE.items():
        if k in r[8]:
            r[2] = disp

# 频次过滤：非白名单课名若只出现 1–2 次，多半是讲标题被误当课名，回退未标注
from collections import Counter as _C
_wlset = set(wl.values())
_freq = _C(r[2] for r in rows)
for r in rows:
    c = r[2]
    if c in _wlset or c.startswith("外部源"):
        continue
    if _freq[c] < 3 and (len(c) >= 14 or re.search(r"讲|封|第|问答|加餐|复盘", c)):
        r[2] = "未标注课程"
    elif _freq[c] < 2 and len(re.findall(r"[\u4e00-\u9fa5]", c)) < 5:
        r[2] = "未标注课程"

# 判级修正：律文件内标注「证据等级**：B–」的条目，精度降为「B–（学员观点）」
_downgraded = set()
_dist = os.path.join(BASE, "05_自主学习/03-蒸馏入库")
if os.path.isdir(_dist):
    for fn in os.listdir(_dist):
        if not fn.endswith(".md"):
            continue
        try:
            txt = open(os.path.join(_dist, fn), encoding="utf-8").read()
        except Exception:
            continue
        for m in re.finditer(r"(?ms)^### (D\d{4})[^\n]*\n(.*?)(?=^### D\d{4}|\Z)", txt):
            if re.search(r"\*\*证据等级\*\*：\s*B–", m.group(2)):
                _downgraded.add(m.group(1))
for r in rows:
    if r[0] in _downgraded:
        r[5] = "B–（学员观点）"

with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["D号", "律名", "课名", "讲次/章次", "定位标题", "精度", "来源文件可覆盖讲次", "锚点句", "来源文件", "出处摘要"])
    w.writerows(rows)

from collections import Counter
cnt = Counter(r[5] for r in rows)
print("入表 %d／%d｜精度 %s｜锚点 %d" % (len(rows), len(dedup), dict(cnt), sum(1 for r in rows if r[7])))
print("输出:", OUT)
