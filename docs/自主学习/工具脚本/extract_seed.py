#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从技能包 SKILL.md 抽律表 → `_seed/<前缀>.tsv`（编号|短名|一句话）

表格列数不固定（有的 3 列、有的首列是「模块」），因此按内容识别：
  含形如 LP03／SW105 的单元格 → 编号；其后第一个短单元格（≤10 字、无句号）→ 短名；
  余下最长单元格 → 一句话。
编号统一补足 3 位（LP3→LP003，SW105 不变）。
用法：python3 10_工具脚本/extract_seed.py <skill.md> [--prefix SW]
"""
import os, re, sys, argparse

CODE = re.compile(r"([A-Z]{1,4})(\d{1,3})")


def rows(text):
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        idx = None
        for i, c in enumerate(cells):
            c2 = c.replace("*", "").strip()
            if CODE.fullmatch(c2):
                idx = i
                break
        if idx is None:
            continue
        code = cells[idx].replace("*", "").strip()
        m = CODE.fullmatch(code)
        pre, num = m.group(1), int(m.group(2))
        code = f"{pre}{num:03d}"
        rest = [c for i, c in enumerate(cells) if i != idx and c]
        name = ""
        for c in rest:
            if 2 <= len(c) <= 10 and "。" not in c and "，" not in c:
                name = c
                break
        line_txt = max(rest, key=len) if rest else ""
        line_txt = re.sub(r"[。]$", "", line_txt).strip()
        if not line_txt or line_txt == name:
            continue
        out.append((code, name or "（未命名）", line_txt))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--prefix", default="")
    a = ap.parse_args()
    t = open(a.src, encoding="utf-8").read()
    rs = rows(t)
    if a.prefix:
        rs = [r for r in rs if r[0].startswith(a.prefix)]
    # 去重（保留首次出现）
    seen, keep = set(), []
    for r in rs:
        if r[0] in seen:
            continue
        seen.add(r[0])
        keep.append(r)
    os.makedirs("10_工具脚本/_seed", exist_ok=True)
    pre = a.prefix or keep[0][0][:2]
    out = f"10_工具脚本/_seed/{pre}.tsv"
    open(out, "w", encoding="utf-8").write("\n".join("|".join(r) for r in keep) + "\n")
    nums = [int(re.sub(r"[A-Z]", "", r[0])) for r in keep]
    gaps = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
    print(f"{pre}: {len(keep)} 律｜号 {min(nums)}–{max(nums)}｜断号 {len(gaps)} 个：{gaps[:12]}{'…' if len(gaps)>12 else ''}｜→ {out}")


if __name__ == "__main__":
    main()
