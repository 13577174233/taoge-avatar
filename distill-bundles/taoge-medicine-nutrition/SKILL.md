---
name: taoge-medicine-nutrition
description: "仝卿·营养科学20讲的知识网络：营养素的判定条件、代谢四规则、基因与代谢差异、碳水蛋白脂肪纤维水维生素矿物质、饮食比例与热量密度、食物严选与避坑、免疫与疾病营养治疗、减重与美食、精力与大脑。当用户问该怎么吃、某营养素缺不缺、要不要补剂、减脂怎么吃、生病怎么吃、吃什么提神时使用。"
---

# 营养科学 · 处方索引

> 来自 115 个原子知识点、21 个模型、56 条误区，
> 全部取自《仝卿·营养科学20讲》原文，可逐条回溯到原句。

## 先定位：你现在属于哪种情况

| 用户在说什么 | 读哪一章 |
|---|---|
| 想搞清什么算营养素、为什么缺了没感觉、基因检测值不值得做时 | [references/01-nutrient-framework.md](references/01-nutrient-framework.md) |
| 纠结主食吃不吃、蛋白质够不够、油该怎么选、脂肪肝是不是吃出来的时 | [references/02-macronutrients.md](references/02-macronutrients.md) |
| 便秘、想养肠道菌群、每天该喝多少水、尿色怎么看时 | [references/03-fiber-and-water.md](references/03-fiber-and-water.md) |
| 要不要补维生素、晒太阳够不够、钙铁锌硒怎么补、补多了会不会中毒时 | [references/04-vitamins-minerals.md](references/04-vitamins-minerals.md) |
| 想知道一顿饭该怎么配比、为什么算热量没用、怎么用手估份量时 | [references/05-diet-pattern.md](references/05-diet-pattern.md) |
| 买东西怎么看配料表、哪些食物优先、哪些要少吃、致癌物传闻要不要信时 | [references/06-choose-and-avoid.md](references/06-choose-and-avoid.md) |
| 想提高免疫力、生病或术后怎么吃、家人肿瘤治疗期怎么补营养时 | [references/07-immunity-and-treatment.md](references/07-immunity-and-treatment.md) |
| 想减肚子、体重卡住不动、又不想放弃好吃的时 | [references/08-weight-and-pleasure.md](references/08-weight-and-pleasure.md) |
| 下午犯困、脑子跟不上、想靠吃提升专注力时 | [references/09-energy-and-brain.md](references/09-energy-and-brain.md) |

## 几条不可协商的红线

1. **没有一种食物能治病。** 靠吃某样东西治病的说法基本不靠谱，剂量达不到有效浓度；治疗性营养要在医生或临床营养师指导下做。
2. **补剂不能替代饮食，也不是越多越好。** 单一补剂最容易过量，脂溶性维生素与矿物质有明确上限。
3. **特殊人群必须单独评估。** 孕产、儿童、老人、肾病、肝病、痛风、肿瘤患者的目标与普通人不同，不能照搬通用建议。
4. **体重与摄入的异常变化是信号。** 3 个月内体重变化超过 15%、持续吞咽困难或不明原因消瘦，先就医排查。

## 文件结构

- `references/`：按能力分章，共 9 篇
- `references/00-misconceptions.md`：误区对照表
- `assets/checklist.md`：红线与剂量速查
- `assets/subgraph.json`：本 skill 对应的知识子图（可被其它 agent 读取）

## 什么时候不要用这个技能

- 已经确诊的营养缺乏病、进食障碍、重度肥胖、慢性肾病、肝硬化、肿瘤恶液质：**须由临床营养科制定方案**，本课只给原则。
- 需要个体化食谱与克数配餐：只给可执行的框架与估算方法，不给治疗级配餐。
- 婴幼儿喂养、孕期营养补充剂量：本课未覆盖，须查指南或问医生。

## 证据等级怎么读

| 等级 | 含义 | 怎么用 |
|---|---|---|
| A | 指南或大样本研究支持 | 可以直接照做 |
| B | 多项研究支持但结论有分歧 | 可以做，注意个体差异 |
| C | 机制清楚、证据有限 | 作为参考，不替代医生意见 |
| D | 间接证据或专家经验 | 谨慎，只作补充 |
| E | 作者立场，无外部出处 | 知道有这种观点即可，不要当结论转述 |

## 使用方式

1. 先用上表定位章节，只读那一章，不要通读。
2. 每个知识点都有「自测」，答不上就说明没掌握，回到「展开」重读。
3. 给建议时，剂量、人群、红线三样必须同时说清；缺任何一样就不要给结论。

