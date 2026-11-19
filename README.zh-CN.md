# 视觉策划与案例学习技能包 (`visual-planning-learning`)

[English README](README.md) · [中文案例与方法索引](library/README.md) · [English Case & Method Index](library/README.en.md) · [结构化双语目录](library/catalog.json)

`visual-planning-learning` 是一个完整、可跨环境移植的**中英双语（`zh` + `en`）视觉策划与版面诊断技能包**。它基于已核实的产品事实、眼动追踪实证、真实转化案例与四大设计/可用性经典原著，帮助 Agent 策划或诊断**电商详情页分镜（PDP Storyboard）、着陆页首屏（Hero Section）、B2B 工业技术参数表与选型册、展会邀请函与展台立面、以及广告构图**。

拒绝用“高端、大气、科技感、简约”等空泛形容词应付视觉策划——本技能通过**症状路由（`when_stuck`）**调用 **28 条可复用视觉方法（`M-001`–`M-028`）** 与 **23 篇中英双语深度案例拆解卡（`C-*`）**，并在结构化目录中通过 `learning_origin` 字段严格区分**经典原著典籍（`book_canon`）**、**外部实证基准（`benchmark_study`）**、**实战共创正反对比拆解（`co_dissected_teardown`）**与**任务实战反馈（`task_feedback`）**。

---

## 知识库全景概览 (`catalog.json` `r10`)

| 信源类别 (`learning_origin`) | 已完整核阅的原始著作、实验与实战拆解（共 `15` 项，`100%` 全文/原图核验） | 提炼的视觉方法（`28` 条）与双语案例卡（`23` 中 + `23` 英） |
| :--- | :--- | :--- |
| **[实战共创] 街头实拍正反对比拆解 (`co_dissected_teardown`)** | **2026 新一代小米 SU7 × 舒淇「卡布里蓝」核心商圈巨幕 vs. 同行车企大屏（捷尼赛思/岚图泰山/腾势 N9/小鹏 X9/别克/吉利/阿维塔）**：由“三连追问”驱动的 6 维视觉与传播拆解 | `M-028`（`validated`）· `1` 篇中英双语案例卡（`C-xiaomi-su7-2026-mall-billboard-teardown`）+ `F-002` |
| **Baymard Institute 电商 UX 基准 (`benchmark_study`)** | `5` 篇大规模眼动与可用性报告：比例参照图（In-Scale）、图文引线标注（Descriptive Callouts）、标配与选配附件图、参数表可扫描性、弃用横向 Tab 导航 | `M-001`–`M-003`、`M-005`–`M-006` · `5` 篇中英双语案例卡（`C-baymard-*`） |
| **Marketing Examples (Harry Dry)** | `4` 组着陆页、定价与品牌改版拆解：Above the Fold 五要素、Rows 实时表格首屏翻倍实验与 Haako 改写、Refactoring UI `$149` 高配锚定与 Basecamp 比价、Tropicana 5500 万美元改版教训与 Angostura 超大酒标 | `M-004`、`M-009`–`M-010` · `4` 篇中英双语案例卡（`C-me-*`） |
| **Robin Williams《写给大家看的设计书（第 4 版）》** | 258 页全书核阅：CRAP 四大原则（亲密性、对齐、重复、对比）、12 色轮（暗色/亮色、色质抖动、冷退暖进面积比）、字体设计（协调/冲突/对比、`giraffe` 词形海岸线） | `M-011`–`M-015` · `3` 篇中英双语案例卡（`C-williams-*`） |
| **Josef Müller-Brockmann《平面设计中的网格系统》** | 85 页全书核阅：`1 : 1.5 : 2 : 3` 页边距递进、正文行高模数网格（`55行 = 4×13 + 3`）、`8/20/32` 格矩阵、色块内边距四图对照（Figs. 1–4）、瑞士无单品构成海报（*musica viva*）、B2B 工业品 30 格手册与三维展位 `170cm` 视平线网格 | `M-016`–`M-019` · `3` 篇中英双语案例卡（`C-muller-brockmann-*`） |
| **Adam Wathan & Steve Schoger《Refactoring UI》** | 252 页原书 + *7 Practical Tips*：字重色阶层级、深色背景同色相浅字、无边框分组、去冗余标签 vs. 参数表标签反强调、`6` 并 `4` 双层富表格、`≥25%` 非线性间距尺、`45–75` 字符行宽、`100–900` HSL 九阶色板与感知亮度色相旋转、翻转对比度过 WCAG `4.5:1`、双层阴影与背景照片单色正片叠底 | `M-007`–`M-008`、`M-020`–`M-023` · `4` 篇中英双语案例卡（`C-refactoring-ui-*`） |
| **Steve Krug《Don't Make Me Think, Revisited（第 3 版）》** | 257 页原书核阅：第一定律（*Don't make me think!*）、60 英里扫视与满意即止、广告牌法则 *Billboard Design 101*、视觉嵌套错位、`No cursor = no hover = no clue`、三大视觉噪音（咆哮/失序/杂乱）、第三定律（`103` $\rightarrow$ `34` 词两轮砍半）、双倍醒目 `"You are here"`、6 项后备箱测试（*Trunk Test*）、首屏大爆炸理论（`50ms`、`6–8` 词 Tagline vs. Motto、公地悲剧）与善意储蓄罐（真 FAQ vs. `QWWPWAs`、读屏用耳扫视） | `M-024`–`M-027` · `3` 篇中英双语案例卡（`C-krug-*`） |

---

## 快速检索与校验命令

在技能根目录（`visual-planning-learning/`）下运行：

```bash
# 1. 查看资料库规模与信源核阅状态
python scripts/library.py summary

# 2. 按视觉卡点症状或中英文关键词加权检索
python scripts/library.py search "参数表 扫描" --kind methods
python scripts/library.py search "billboard visual noise" --kind cases

# 3. 单次批量调取多条方法与中英文案例卡
python scripts/library.py get M-001 M-020 M-024 C-krug-billboard-scanning-and-visual-noise

# 4. 校验 Schema、外键引用、中英文案例卡配对与 SHA-256 指纹
python scripts/library.py validate --check-files
```
