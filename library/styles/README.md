# 跨行业实证风格母版库 (Evidence-Based Style Archetypes Framework)

本目录用于沉淀**有真实案例与可追溯来源支撑**的跨行业商业风格母版，采用“通用风格库 + 允许垂直行业专精挂载”的结构，避免个人审美狭隘与 AI 风格同质化。

## 实证入库铁律（绝不空想编造）

1. **禁止模型先验凭空撰写母版**：每一份入库的风格母版必须基于**用户实际收集的优秀品牌海报套图**和/或**经逐行核验的开源品牌规范原文件**（如 GitHub `DESIGN.md` 实证仓库），严禁仅凭模型记忆拍脑袋起草。
2. **严格状态分级**：
   - `source_verified`：已逐行核验开源规范原文与/或拆解了真实海报套图，完成 6 项硬约束提炼；
   - `validated`：不仅完成真实案例提炼，且已在本团队实际出图任务中跑通并经用户验收认可。
3. **风格与构图解耦（正交组合）**：本目录只锁定**风格基因**（光影材质、留白预算、色彩字体、容器禁用令、套系节奏）；**画面结构与多图编排**由 [poster-patterns.md](../../references/poster-patterns.md) 独立管理；**三层光影分流与审美验收**由 [output-qa-gate.md](../../references/output-qa-gate.md) 强制兜底。
4. **配套本地视觉锚点**：每新增一个风格母版 `<style-id>.md`，同步在 `library/style-refs/<style-id>/local/` 放入 2–3 张对应的真实标杆海报原图（`local/` 已配置 `.gitignore` 忽略，本地开箱即用，推送 GitHub 零版权风险）。

---

## 5 大通用美学赛道实证母版总表（共 7 套 `source_verified` · 多元来源混采）

| 赛道 | 审美定位 | 已入库实证母版（`source_verified` / `validated`） | 核心来源类型 |
| :--- | :--- | :--- | :--- |
| **1. 消费电子** | 极简陈列、轻奢白棚、暗场黑金硬件、纯黑 Pro 剧场 | • [`apple-light-gallery`](apple-light-gallery.md)（Apple MacBook Air · 浅色极简美术馆陈列）<br>• [`apple-dark-pro`](apple-dark-pro.md)（Apple iPhone 18 Pro · 深色 Pro 剧场硬件）<br>• [`xiaomi-light-luxury-studio`](xiaomi-light-luxury-studio.md)（小米耳夹式耳机 · 白棚轻奢）<br>• [`xiaomi-dark-flagship-hardware`](xiaomi-dark-flagship-hardware.md)（小米路由器 BE6500 Pro · 纯黑暗场黑金硬件） | 品牌官网实测 + GitHub `DESIGN.md` 交叉核验 |
| **2. 奢侈品 / 轻奢** | 触感纸艺、暖调社论、细线烫金与礼赠静物美学 | • [`luxury-tactile-editorial`](luxury-tactile-editorial.md)（kissmiklos `LUUX` · 触感棉纸、赤陶暖橙与烫金衬线社论风） | Behance 顶级设计工作室战役 |
| **3. 家居 / 生活方式** | 自然光影融合、原生材质触感、建筑空间陈列与完整画报排版 | *（待实证入库）* | 待采 |
| **4. 户外 / 机能装备** | 硬质直射斜影、粗粝混凝土、材质微距与竖版户外巨幕 | • [`outdoor-brutalist-technical`](outdoor-brutalist-technical.md)（`AVRYO` · 混凝土硬光切影、单点酸绿与瑞士边栏机能海报风） | Behance 完整品牌与户外战役 |
| **5. 精密工业 / 光学机械** | 精密标尺刻度画报、浅灰波形暗纹、冷灰棚拍斜切单页与 5% 品牌点睛 | • [`industrial-precision-instrument`](industrial-precision-instrument.md)（Keysight 是德科技 + Fluke 福禄克 · 精密标尺与斜切分栏工业画报风）<br>*（注：暗场电子硬件亦可跨界调用 `xiaomi-dark-flagship-hardware` 或 `apple-dark-pro`）* | 国际广告代理商 & 品牌商业档案高清原稿 |

> **如何继续扩充与混采**：既可按 [_TEMPLATE.md](_TEMPLATE.md) 新增全新流派母版，也可向已有母版混采不同来源（官网 / Behance / Ads of the World / Lemanoosh / 线下实拍）的同气质优质样本，并在母版顶部“真实来源登记”中逐项写明出处。
