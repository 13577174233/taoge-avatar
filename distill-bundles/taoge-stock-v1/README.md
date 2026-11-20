# 使用说明（豆包办公）· 涛哥股海模型V1.0

## 安装
1. 解压 `涛哥股海模型V1.0-豆包技能包.zip`，得到目录 `taoge-stock-v1/`。
2. 在豆包办公中上传该技能文件夹（保留目录结构，尤其是 `SKILL.md` 与 `references/`）。
3. 上传后可直接提问，或用 `/taoge-stock-v1` 显式调用。

## 包内文件
| 文件 | 用途 |
|---|---|
| `SKILL.md` | 技能入口：描述、路由表、回答铁律（含新版本命名规则） |
| `MODEL_SPEC.md` | 完整自包含说明书（推荐豆包优先读这份） |
| `references/01-strategy-spec.md` | 数据口径 + 策略规格 + 参数表 + L5 熔断 + 伪代码 |
| `references/02-backtest-results.md` | 结论 + 24 个月回测结果 + 胜率口径 + 版本对比 |
| `references/03-factor-ic-and-duel.md` | 随机基准 + W3 归因 + 四项消融裁决 + 参数路径依赖 |
| `references/04-boundaries-and-qa.md` | 免责 + 局限 + 常见问答 + 术语表 |
| `_ARCHIVE_INDEX.md` | 七阶段分类归档索引 |
| `CHECKSUMS.sha256` | 包内文件校验和 |

## 校验完整性
进入解压后的目录执行：

```bash
shasum -c CHECKSUMS.sha256
```

全部显示 OK 即完整。校验和里的路径是**目录内相对路径**，不带顶层目录前缀。

## 只想上传一个文件阅读（不装技能）
直接上传同目录下的 `涛哥股海模型V1.0-豆包阅读版说明书.pdf`；若豆包版本对 PDF 解析不佳，改传 `涛哥股海模型V1.0-豆包阅读版说明书.txt`。
两者内容与 `MODEL_SPEC.md` 完全一致。

## 边界
历史模拟研究，不构成投资建议、不推荐证券、不承诺收益、不可用于实盘。
