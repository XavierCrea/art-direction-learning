# 跨行业实证风格母版库 (Evidence-Based Style Archetypes Framework)

本目录用于沉淀**有真实案例与可追溯来源支撑**的跨行业商业风格母版，采用**按「视觉气质与光影语言」分类**（而非按行业赛道硬切）的架构，实现 **产品事实与行业真实性约束 × 视觉气质母版（本目录） × 海报构图骨架（`poster-patterns.md`）** 三轴正交解耦，支持全行业跨界调用与按需自然扩展。

## 实证入库铁律（绝不空想编造）

1. **禁止模型先验凭空撰写母版**：每一份入库的风格母版必须基于**用户实际收集的优秀品牌海报套图**和/或**经逐行核验的开源品牌规范原文件**（如 GitHub `DESIGN.md` 实证仓库），严禁仅凭模型记忆拍脑袋起草。
2. **严格状态分级**：
   - `source_verified`：已逐行核验开源规范原文与/或拆解了真实案例样本，完成视觉特征提炼；
   - `user_endorsed`：已在用户项目或对话中获用户认可/采用；
   - `field_validated`：不仅完成提炼与采用，且已有受众测试或真实投放结果验证。
3. **风格、构图与行业三轴正交解耦（支持整体复刻或单手法借用）**：本目录只记录样本中的**典型视觉气质与光影语言**（而非死板硬边界）；**构图思路与多图编排**由 [poster-patterns.md](../../references/poster-patterns.md) 独立管理；**制作路线与客观验收**由 [output-qa-gate.md](../../references/output-qa-gate.md) 把关。调用时可**整体复刻参考气质**，也可**只单独借用其中某一手法**（例如保留客户品牌蓝，仅借某套母版的侧光纸张质感或留白节奏）。审核时，只有**用户明确指定的品牌规范**可作退稿依据，模型自行挑选的参考风格仅作设计建议。
4. **配套可视化参考卡与本地锚点（三级降级）**：每个风格母版 `<style-id>.md` 配套两层视觉参考——
   - **随包零版权可视化参考卡** `library/style-refs/<style-id>/descriptor.svg`（代码自绘的精确色板 HEX、字阶条、留白框图、网格线稿与光影示意，直接入库可跨机器开箱即用）；
   - **本地商用标杆原图** `library/style-refs/<style-id>/local/`（已被 `.gitignore` 忽略，零版权风险）。按 `L1 整体复刻（≥2 张本地图）/ L2 原子借用（1 张图或 descriptor.svg）/ L3 纯数值规范` 三级调用，换机缺图时自动降级并标注“文字/示意图级参考”，详见 [output-qa-gate.md](../../references/output-qa-gate.md)。

---

## 视觉气质与光影语言母版总表（5 个已实证象限 · 共 7 套 `source_verified`）

| 视觉语言象限 | 核心光影与版式气质 | 已入库实证母版（`source_verified` / `validated`） | 典型跨界适用范围 | 核心来源类型 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 纯净极简陈列**<br>*Clean Minimalist* | 无干扰纯净底场（浅色白棚、空旷盐湖或单色纯场）、高留白与极克制无衬线字阶 | • [`apple-light-gallery`](apple-light-gallery.md)（Apple MacBook Air · 浅色极简美术馆陈列）<br>• [`xiaomi-light-luxury-studio`](xiaomi-light-luxury-studio.md)（小米耳夹式耳机 · 白棚轻奢） | 消费电子、小家电、汽车/大件户外极简、精品 DTC 单品 | 品牌官网实测 + GitHub `DESIGN.md` 交叉核验 |
| **2. 暗场剧场硬件**<br>*Dark Dramatic Hardware* | 纯黑底场、戏剧轮廓光、高反差金属/玻璃与黑金旗舰质感 | • [`apple-dark-pro`](apple-dark-pro.md)（Apple iPhone 18 Pro · 深色 Pro 剧场硬件）<br>• [`xiaomi-dark-flagship-hardware`](xiaomi-dark-flagship-hardware.md)（小米路由器 BE6500 Pro · 纯黑暗场黑金硬件） | 旗舰硬件、高端储能/逆变器、影音设备、专业硬件工具 | 品牌官网实测 + GitHub `DESIGN.md` 交叉核验 |
| **3. 暖调触感社论**<br>*Warm Tactile Editorial* | 棉纸/织物/哑光肌理、暖中性色、细线烫金与杂志级衬线留白 | • [`luxury-tactile-editorial`](luxury-tactile-editorial.md)（kissmiklos `LUUX` · 触感棉纸、赤陶暖橙与烫金衬线社论风） | 轻奢礼赠、香氛个护、精品食品/咖啡、品牌纪念画册 | Behance 顶级设计工作室战役 |
| **4. 硬光粗野机能**<br>*Brutalist Hard-Light Technical* | 粗粝混凝土/自然介质、硬质直射斜影、单点高反差与瑞士边栏大字 | • [`outdoor-brutalist-technical`](outdoor-brutalist-technical.md)（`AVRYO` · 混凝土硬光切影、单点酸绿与瑞士边栏机能海报风） | 户外电源、运动机能装备、硬核载具、工装工具 | Behance 完整品牌与户外战役 |
| **5. 精密工程画报**<br>*Precision Engineering Editorial* | 精密标尺刻度、浅灰波形暗纹、冷灰棚拍斜切分栏与 5% 品牌点睛 | • [`industrial-precision-instrument`](industrial-precision-instrument.md)（Keysight 是德科技 + Fluke 福禄克 · 精密标尺与斜切分栏工业画报风） | 测试仪器、B2B 工业设备、能源/电力系统、精密制造 | 国际广告代理商 & 品牌商业档案高清原稿 |

---

## 按需扩展空白位（Optional Future Visual Clusters · 宁缺毋滥）

现有 5 个实证象限已覆盖约 75%–80% 的中高端商业、消费电子、礼赠、户外与 B2B 工业硬件海报需求。以下 2 个当前空白的视觉大类仅作为按需扩展方向（不设硬性配额，须等遇到兼具真实光影与完整商业字阶系统的标杆案例再入库）：

| 扩展方向 | 视觉定位与典型区别 | 典型参考方向（待实证） |
| :--- | :--- | :--- |
| **扩展位 A · 自然光生活实景画报**<br>*Sunlit Lifestyle Editorial* | 真实室内日光/桌面人居融合 + 明确单品主角 + 完整商业标题/字阶规范（**区别于纯空间摄影、缺商业字阶的家具软装画册**） | MUJI、Sonos、Dyson、IKEA 功能海报等 |
| **扩展位 B · 明快高饱和活力消费**<br>*Bold Pop / High-Chroma Consumer* | 高饱和撞色、粗壮现代无衬线字阶、强停滑卖点直给（补足目前全库偏克制低饱和的另一端） | 快消饮食、大众电商主图、社媒高互动拉新海报 |

> **如何继续扩充与混采**：既可按 [_TEMPLATE.md](_TEMPLATE.md) 新增全新视觉语言母版，也可向已有母版混采不同来源（官网 / Behance / Ads of the World / Lemanoosh / 线下实拍）的同气质优质样本，并在母版顶部“真实来源登记”中逐项写明出处。
