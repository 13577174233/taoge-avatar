---
name: taoge-medicine-literacy
description: "薄世宁·医学通识50讲的知识网络：医学的本质、疾病的发生逻辑、免疫与代偿、诊断治疗与指南、药与医院与公共卫生、癌症冠心病、医源性损害、医学史、聪明患者与临终选择。当用户问医学到底怎么运作、为什么这个病治不好、怎么当聪明的患者、怎么把自己挡在医院外时使用。"
---

# 医学通识 · 认知索引

> 来自 264 个原子知识点、52 个模型、164 条误区，
> 全部取自《薄世宁·医学通识50讲》原文，可逐条回溯到原句。

## 先定位：你现在属于哪种情况

| 用户在说什么 | 读哪一章 |
|---|---|
| 想搞清医学的边界在哪、为什么说医疗是支持自我修复、医患关系该怎么理解时 | [references/01-medicine-nature.md](references/01-medicine-nature.md) |
| 困惑「病」和「症」的区别、体检突然查出问题、想理解代偿与进化遗留时 | [references/02-disease-logic.md](references/02-disease-logic.md) |
| 老感冒、想提高免疫力、问肠道菌群要不要补时 | [references/03-immunity.md](references/03-immunity.md) |
| 不理解为什么要做一堆检查、医生说的「指南推荐」是什么、想懂循证医学时 | [references/04-diagnosis-and-guideline.md](references/04-diagnosis-and-guideline.md) |
| 医生建议输液或抗生素、家人上呼吸机、想搞清这些手段到底在做什么时 | [references/05-drugs-and-devices.md](references/05-drugs-and-devices.md) |
| 想知道医院为什么这么组织、护理在做什么、传染病怎么被拦住时 | [references/06-hospital-and-public-health.md](references/06-hospital-and-public-health.md) |
| 家人确诊癌症或冠心病、长期疼痛查不出原因、担心衰老时 | [references/07-major-diseases.md](references/07-major-diseases.md) |
| 担心检查与治疗本身带来的伤害、想知道制度怎么降低风险时 | [references/08-medical-harm.md](references/08-medical-harm.md) |
| 想理解医学是怎么一步步走过来的、脑死亡与誓言这类概念从哪来时 | [references/09-history-and-heroes.md](references/09-history-and-heroes.md) |
| 要在信息不全时做决定、想少去医院、面对临终与告别时 | [references/10-smart-patient.md](references/10-smart-patient.md) |
| 想判断新技术的方向、看清继承与叛逆的边界时 | [references/11-future.md](references/11-future.md) |

## 几条不可协商的红线

1. **通识是认知框架，不是诊断工具。** 学完这一套仍不能给自己下诊断；有症状先就医，别用「我懂机制」替代检查。
2. **输液、抗生素、麻醉、呼吸机都是医疗决策。** 不能按科普自行要求，也不能按科普自行拒绝。
3. **癌症与冠心病讲的是机制与筛查逻辑。** 不是个体预后判断，不能用课程里的生存率推算自己。
4. **临终决策要与家属和医生共同完成。** 本课只提供提问框架，不替你选。

## 文件结构

- `references/`：按能力分章，共 11 篇
- `references/00-misconceptions.md`：误区对照表
- `assets/checklist.md`：红线与剂量速查
- `assets/subgraph.json`：本 skill 对应的知识子图（可被其它 agent 读取）

## 什么时候不要用这个技能

- 任何急症（胸痛、呼吸困难、意识改变、大出血、剧烈腹痛）：**直接就医或呼叫急救**，不要检索知识。
- 需要具体诊断、处方或预后判断：本课只给认知框架与要问医生的问题。
- 个体化的治疗方案选择（手术还是保守、用哪种药）：须由主诊医生依据指南与个体情况决定。

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

