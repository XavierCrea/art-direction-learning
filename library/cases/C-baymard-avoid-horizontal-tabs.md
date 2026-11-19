# Baymard 详情页导航实验：弃用隐藏核心内容的“横向 Tab”，改用纵向展开分节与吸顶目录

[中文案例索引](../README.md) · [English](en/C-baymard-avoid-horizontal-tabs.md)

[返回视觉案例库](../README.md) · 独立可用性测试（含 B2B 电子元器件与工业品测试）

- **卡点症状 (`when_stuck`)**　为了追求页面“看起来短小整洁”，把规格参数、CAD 图纸、客户评价、物流退换等核心模块藏在非吸顶的“横向标签页（Horizontal Tabs）”里，导致买家一路向下滚动却根本没发现这些内容，以为信息缺失而直接关页。
- **适用载体**　B2B 与 B2C 独立站产品详情页（PDP）、阿里国际站自定义详情页、技术方案着陆页。

## 原材料里看到什么 (`observations`)

- Baymard Institute 多年跨品类可用性测试（含大众电商、DTC 品牌以及 **TE Connectivity、STMicroelectronics 等 B2B 电子元器件与机械网站**）一致证实：用“横向 Tab”承载产品页核心模块表现极差，但仍有 **29%** 的网站在使用。
- **失灵的视觉机制**：买家的本能动作是**纵向向下滚动（Vertical Scrolling）**寻找信息，视线向下移动而非向右移动；且大多数横向 Tab 并非吸顶（Sticky），买家一旦向下滚动阅读默认展开的第一栏，顶部 Tab 栏便滚出屏幕视野。
- **真实测试现场（B2B 工程师与消费买家双双漏看）**：
  - 在 **TE Connectivity**（B2B 电子连接器）测试中，一名电子工程师想确认某连接器是 10 还是 16 触点，因没注意到顶部的 `Features` 横向 Tab，直接放弃该产品页退回列表；
  - 在 **STMicroelectronics** 测试中，工程师已决定购买却找不到藏在顶部 Tab 里的 `Sample and Buy`；
  - 在 Crutchfield / Ashley Furniture / B&H 手机端测试中，**21%** 以上的受试者完全漏看了藏在横向 Tab 里的评价与规格；手机端屏幕窄，横向 Tab 甚至被截断，要求买家“先往上滚几屏找到 Tab 栏，再左右横滑找到隐藏 Tab”，造成极大操作阻力。
- **高表现替代方案（Evo 桌面端 / Lowe's 手机端）**：
  - 桌面端采用 **“纵向全部展开分节（Expanded Sections） + 顶部吸顶目录（Sticky ToC）”**（如 Evo），买家既可顺应本能一路向下滚动看完全部核心模块，也可随时点击始终可见的吸顶锚点一键跳转；
  - 手机端长页面采用 **“纵向手风琴折叠栏（Vertically Collapsed Accordions）”**（如 Lowe's），买家向下滚动时能依次看到所有模块的标题横条，按需点击展开。

## 图字如何分工 (`copy_visual_synergy`)

- **版面流向负责“顺应纵向滚屏本能”**：将概述、卖点图解、技术参数、认证/CAD下载、FAQ 与评价按决策先后顺序纵向串联，保证买家单靠滚轮就能依次撞见每一个核心证据标题。
- **吸顶导航条负责“长页快速空降”**：在视口顶部固定一行轻量锚点（如 `Overview | Specs | Wiring & CAD | Certifications | FAQ`），滚动时高亮当前所在分节。

## 可迁移的视觉动作 (`reusable_move`)

1. **桌面端详情页取消主横向 Tab**：将产品描述、核心参数、图纸/认证、评价、物流保障全部改为纵向依次展开的独立区块（Expanded Sections），每个区块配醒目的全宽标题栏。
2. **加装吸顶锚点目录（Sticky ToC）**：当详情页超过 3 屏时，在滚动过首屏后固定一条置顶横向快速跳转栏（点击仅做锚点平滑滚动，不隐藏下方模块）。
3. **移动端使用纵向手风琴（Vertical Accordions）**：手机端若内容极长，保留每个核心模块的全宽纵向标题条（带 `+` 或下拉箭头），让买家向下滚动时100%看到所有模块名称。
4. **唯一例外**：仅在同一子模块内部的并列维度切换（如同一参数区内的 2–3 个子分类，且手机端无需左右横滑即可看全标签名）时，才允许使用局部小 Tab。

## 素材前提与迁移边界 (`asset_prerequisites` & `transfer_limits`)

- **素材前提**：先清理详情页中穿插在核心内容之间的冗余广告和无关推荐，避免因次要噪音把页面撑得过长。
- **禁用边界**：若对单个超长模块（如 50 行兼容性列表）使用“展开更多（Read More）”截断，必须在截断处保留清晰的渐变遮罩与高对比展开按钮，防止买家误以为内容到此结束。

## 已知效果与出处

- **证据属性**：独立跨行业可用性测试（含 B2B 电子元器件工程师实测与 29% 行业基准统计）。
- **出处**：Alan Blackwood, *Avoid Using “Horizontal Tabs” for the Main Product Page Sections (29% Don’t)*, Baymard Institute, 2018-10-16, updated 2026-07-08 (`https://baymard.com/research-articles/avoid-horizontal-tabs`)。
- **关联方法**：`M-006`（纵向展开分节与吸顶目录布局法）。
