# 七阶段归档索引（涛哥股海模型V1.0 交付）

> 生成日期：2026-11-20　|　分类法：总纲 / 需求 / 技术 / 设计 / 开发 / 测试 / 交付
> 版本关系：v3 基线（2026-11-19）→ 豆包评测（2026-11-20）→ V1.0 = v3 + 组合级回撤熔断

| 阶段 | 索引项 | 路径 | 检索关键词 | 证据等级 |
|---|---|---|---|---|
| 总纲 | V1.0 完整说明书 | `MODEL_SPEC.md` | 涛哥股海、V1.0、v5-b、回撤熔断、免责 | A（实算+可复现） |
| 需求 | 任务边界与豆包使用约定 | `references/04-boundaries-and-qa.md` | 不构成投资建议、不推荐股票、命名全称 | A |
| 技术 | 数据口径与指标参数 | `references/01-strategy-spec.md` | 前复权、T+1、MACD(12,26,9)、ATR14、illiq | A |
| 设计 | 五层结构 + L5 组合级回撤熔断 | `references/01-strategy-spec.md` | L0–L5、宽度、拥挤度过滤、滞回 | A |
| 开发 | 逐日执行伪代码与参数表 | `references/01-strategy-spec.md` | 伪代码、max_pos、max_rs20、dd_break | A |
| 测试 | 随机基准与 W3 归因 | `references/03-factor-ic-and-duel.md` | 500 次随机、98.8 百分位、Top10 66.3% | A |
| 测试 | 四项消融与参数路径依赖 | `references/03-factor-ic-and-duel.md` | 熔断纳入、illiq 否决、brk 漂移 | A |
| 测试 | 24 个月滚动验证与胜率 | `references/02-backtest-results.md` | 196 笔、37.76%、−9.52%、t=1.42 | A |
| 交付 | 豆包阅读件与技能包 | `README.md` / `CHECKSUMS.sha256` | 上传、shasum、ASCII 文件名 | B（豆包格式未获官方文档，需真机实测） |

## 自检项
- [x] `SKILL.md` frontmatter 可解析，`description` 块标量缩进 2 空格、长度 ≤ 1024
- [x] 包内文件名全 ASCII，规避中文名解压乱码
- [x] `CHECKSUMS.sha256` 使用解压后目录内相对路径
- [x] `references/` 由单一真源 `MODEL_SPEC.md` 自动切片，无内容分叉
- [x] 免责声明在入口、README、说明书首尾三处出现
- [x] 新版本全称「涛哥股海模型V1.0」在入口铁律、README、说明书三处出现
