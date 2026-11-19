# 视觉策划指南 (Visual Planning Guide)

## 一、 核心原则：去形容词化，用“画面物理动作”回答买家疑问

视觉策划不是给美工或 AI 生图工具堆砌“高端、大气、科技感、简约”等空泛形容词，而是解决三个具体问题：
1. **视线停在哪（Focal Point & Eye Path）**：读者以 60 英里时速扫视页面的前 3 秒，哪个物理细节让他停下来？
2. **图和字怎么分工（Copy-Visual Synergy）**：标题说了主张之后，画面提供什么**不可辩驳的物理证据或直觉参照**？（切忌让画面机械重复标题的字面意思）。
3. **读者靠什么做判断（Decision Input）**：他是在判断**实际体积大小（Scale）**、**真材实料（Craft Detail）**、**包装里到底含不含配件（Bundle Scope）**、**安装接在哪一步（Workflow Step）**，还是**多型号规格对比（Spec Scannability）**？

---

## 二、 第一步：建立“事实 $\rightarrow$ 画面元素 $\rightarrow$ 素材边界”三阶推导梯子

在动笔写分镜脚本或生图提示词前，先把产品事实（或由 `copywriting-learning` 交付的卖点文案）过一遍三阶推导表：

| 阶梯 | 核心问题 | 示例 1（便携/机柜工业设备） | 示例 2（多配件消费品/工具） |
| :--- | :--- | :--- | :--- |
| **1. 已核实事实 (Confirmed Fact)** | 产品有哪些可证实的尺寸、工艺、测试或配件事实？ | 48kWh 储能柜，宽深高 600×800×2000mm，支持 ≤10ms 并离网切换 | 厨师机含主机 + 3 个不锈钢搅拌头（标配），压面器需另购（选配） |
| **2. 具象画面动作 (Concrete Visual Element)** | 用什么参照物、景别或图示让读者“不用算就能看懂”？ | **比例参照图（In-Scale）**：机柜置于标准工业配电房通道，旁立 175cm 工程师作体量参照；右下角嵌波纹切换对比小窗 | **标配全家福（Included Accessories）**：主机居中，3 个标配搅拌头同框陈列并加绿标 `Included`；选配压面器用虚线框隔离并标 `Sold Separately` |
| **3. 素材前提与禁用边界 (Asset Prerequisite & Limit)** | 必须向用户索要什么真实素材？绝对不能伪造什么？ | 需真实机柜长宽高比例；无实测示波器图时用清晰的逻辑原理图，**严禁伪造假示波器截图** | 需核实 BOM 标配清单；**严禁把选配附件混入主图却不加文字声明** |

---

## 三、 第二步：常见视觉困境的“症状诊断路由（Symptom-to-Case Routing）”

将当前页面或草图的痛点转成中英文检索词，用 `python scripts/library.py search` 检索并调用 `get` 批量读取对应方法与案例：

| 当你遇到以下视觉痛点（Symptom / `when_stuck`） | 推荐检索词 (`search`) | 优先调取的核心方法与案例 (`M-001`–`M-027`) |
| :--- | :--- | :--- |
| **写了尺寸数字，买家还是对大小没概念 / 嫌太大或太小** | `比例 参照 尺寸` 或 `in-scale size` | `M-001` · `C-baymard-in-scale-reference` |
| **放了局部特写图，买家看不懂拍的是哪、有什么用** | `特写 引线 图注` 或 `callout caption crop` | `M-002` · `C-baymard-descriptive-callouts` |
| **买家搞不清图片里的配件到底送不送 / 产生售后纠纷** | `配件 标配 选配` 或 `accessories included` | `M-003` · `C-baymard-included-optional-accessories` |
| **首屏放了漂亮插画或大段文字，转化率却很低** | `首屏 实景 演示` 或 `above the fold hero` | `M-004` · `C-me-above-the-fold-visual` · `C-me-rows-live-product-hero` |
| **参数表太长像一堵墙、视线串行，或双栏被误认为两款对比** | `参数表 扫描 分组` 或 `spec sheet scannability` | `M-005`、`M-020` · `C-baymard-spec-sheet-scannability` · `C-refactoring-ui-data-labels-and-tables` |
| **详情页把核心参数/CAD藏在横向 Tab 里，买家根本没点开** | `横向标签 折叠 导航` 或 `horizontal tabs` | `M-006` · `C-baymard-avoid-horizontal-tabs` |
| **页面边框太多太杂、字号乱放大、按钮全是鲜艳实心色** | `层级 边框 按钮` 或 `hierarchy borders buttons` | `M-007`、`M-008` · `C-refactoring-ui-hierarchy-tactics` |
| **高单价产品显得太贵、或者想引导买家选高配套餐** | `高价 锚点 套餐` 或 `pricing tier framing` | `M-009` · `C-me-refactoring-ui-pricing-tier` |
| **改版包装或主图时，不小心把最有辨识度的视觉资产改丢了** | `辨识度 包装 视觉锤` 或 `distinctive asset rebrand` | `M-010` · `C-me-tropicana-angostura-visual-assets` |
| **元素塞满四角、居中软弱无力、缺少视觉焦点或字体打架** | `亲密性 对齐 对比 字体` 或 `crap alignment typography` | `M-011`–`M-015` · `C-williams-crap-layout-makeovers` · `C-williams-color-wheel-value-warmth` · `C-williams-typography-conflict-vs-contrast` |
| **多图文画册高低错落、色块贴边憋屈、展会海报像传单或展板被挡** | `网格 基线 色块 展位` 或 `modular grid booth 170cm` | `M-016`–`M-019` · `C-muller-brockmann-modular-grid-construction` · `C-muller-brockmann-color-fields-and-posters` · `C-muller-brockmann-industrial-catalog-exhibition` |
| **间距纠结、百字长行、HSL 调色发脏、深色徽章抢戏或背景图吃字** | `间距 行宽 HSL 阴影` 或 `spacing hsl shadow contrast` | `M-021`–`M-023` · `C-refactoring-ui-spacing-grid-and-typography` · `C-refactoring-ui-hsl-color-depth-and-images` |
| **按钮名字费脑、扁平化看不出可点、说明文太长、内页迷路或首屏公地悲剧** | `广告牌 噪音 砍半 后备箱 口号` 或 `billboard trunk test tagline goodwill` | `M-024`–`M-027` · `C-krug-billboard-scanning-and-visual-noise` · `C-krug-omit-words-and-trunk-test-navigation` · `C-krug-homepage-big-bang-tagline-and-goodwill` |
| **商圈外墙/展会停车场大牌被环境噪点吞没、少字风景图依然发灰紧绷、L屏被白底割裂或没人打卡** | `商圈 户外大屏 纯色场 L屏 打卡` 或 `mall billboard color field L-screen`（可加 `--origin co_dissected_teardown`） | `M-028` · `C-xiaomi-su7-2026-mall-billboard-teardown` |

---

## 四、 第三步：与 `copywriting-learning` 的双技能组合交接协议（Combo Protocol）

当与 `copywriting-learning` 打组合拳时，按 **`[文案意图] $\rightarrow$ [画面分镜] $\rightarrow$ [图字排版]`** 咬合输出：

1. **检查“图字同义重复（Redundancy Check）”**：
   - 坏配合：标题写 *“Waterproof Outdoor Speaker”*，画面只放一个干巴巴的白底音箱。
   - 好配合（互补求证）：标题写结果或场景（*“Keep the music playing through sudden downpours.”*），画面用 **飞溅水花动态特写 + `IPX7 Waterproof (1m / 30min)` 图标角标** 直接给出视觉证明（源自 `C-baymard-descriptive-callouts`）。
2. **保护移动端可读性（Mobile Viewport Guard）**：
   - 凡需要在图片内部压字（Embedded Text / Callout），字号必须在手机缩略至 `375px` 宽时依然清晰可读（只压大字号短标签，如 `≤10ms Switch`、`3 Included Blades`）；超过 2 行的解释性文字一律移出图片，作为 HTML 文本或下方图注（Caption）呈现。

---

## 五、 第四步：交付颗粒度与输出格式

- **场景 A：单屏广告 / 首屏 Hero / 展会海报 / 主图创意探索**
  默认提供 **2–3 个不同视觉案例驱动的构图方案（Visual Angles）**，每个方案写明：
  1. **借用依据**：引用了哪条方法/案例（如 `M-001` 比例参照 vs. `M-019` 瑞士网格无单品构成）；
  2. **画面构图与机位（Composition & Grid）**：主体、参照物、分栏网格与视线焦点；
  3. **图上标注与文字位置（Overlay & Caption）**：主标题、角标、引线标注的精确位置；
  4. **适用条件与所需素材（Prerequisites）**。
- **场景 B：完整详情页分镜（PDP Storyboard）或落地页全页改版**
  默认交付 **1 套完整连贯的分屏执行表**（从首屏 Hero `M-004`/`M-026` $\rightarrow$ 核心工作流/卖点引线图 `M-002` $\rightarrow$ 比例参照与标配清单 `M-001`/`M-003` $\rightarrow$ 单栏语义分组斑马纹参数表 `M-005`/`M-020` $\rightarrow$ 善意储蓄罐真 FAQ `M-027`）。
- **场景 C：线下展会 / 商业空间 `100m → 10m → 1m` 全触点接力方案**
  按观众移动距离与扫视时间切分视觉任务：
  1. **`100m` 远距截停触点（展馆停车场海报 / 商圈外立面巨幕 `M-028` + `M-019`）**：1.5 秒扫视，采用 `≥75%` 单一高纯度品牌色场切开环境噪点，砍掉参数表、多宫格价格、底部小字与二维码，只保留**品类/情绪钩子短句 + 放大 6 倍的展位号（`BOOTH #XXXX`）或品牌视觉锤**；
  2. **`10m` 中距引流触点（展位门楣 / `170cm` 视平线主背板 `M-019`）**：锁死与停车场海报完全一致的品牌主色形成跨空间认知识别，将核心主张与主推方案锚定在 `170cm` 站立视平线上下；
  3. **`1m` 近距成交触点（展台实物陈列 / 桌面单页选型表 / PDP `M-001`–`M-005`、`M-020`）**：交付完整规格矩阵、接口引线标注与真实认证证据。
- **四条下游落地通道选择（Downstream Channels）**：
  1. **AI 生图/改图 Prompt（`image_generate` / `image_edit`）**：适合自然实景、人像光影、产品场景合成；
  2. **代码级精确平面渲染（Python PIL / SVG 脚本直出 PNG/PDF）**：适合需要严格模数网格对齐、精确品牌 HEX 色值、锋利无误的文字排版与 100% 可扫描二维码（`zxingcpp` 核验）的几何海报、展会邀请函、停车场大牌与对比长图；
  3. **响应式网页/组件代码（HTML / CSS / React / Widget）**：适合店铺装修、单页交互选型表、斑马纹参数表；
  4. **实拍与美工执行单**：适合严禁 AI 伪造的车间测试、真实线束全家福与证书扫描件排版。
