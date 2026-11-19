# 视觉策划案例与方法资料库 (Visual Planning Library)

[English homepage](../README.md) · [项目中文首页](../README.zh-CN.md) · [English Case Index](README.en.md)

这里收录经核验的电商 UX 实验、落地页改版案例、界面层级战术、经典平面设计/网格系统著作、可用性工程法则与**用户×Agent 街头实拍正反对比实战共创拆解**，以及从中提炼出的可检索视觉方法（`M-001`–`M-028`）与中英双语单篇案例拆解卡（`C-*`，共 23 篇）。

- 检索脚本：`../scripts/library.py`（支持 `summary`、中英双语+症状加权+习得来源过滤 `search --origin <book_canon|benchmark_study|co_dissected_teardown|task_feedback>`、多 ID 批量 `get`、`validate --check-files` 与原子化入库 `apply-patch`）
- 结构化双语索引：`catalog.json`（每条记录均显式标注 `learning_origin`，严格区分**静态原著典籍 `book_canon`**、**外部实验基准 `benchmark_study`**、**实战共创正反拆解 `co_dissected_teardown`** 与 **任务反馈 `task_feedback`**）
- 英文译本与 SHA-256 校验表：`translations.en.json`

## 核心视觉方法 (`M-001` – `M-028`)

| 编号 | 方法名称 | 解决的视觉卡点 (`when_stuck`) | 适用载体 |
| :--- | :--- | :--- | :--- |
| `M-001` | **同框比例参照法 (In-Scale Reference)** | 写了长宽高数字但只放白底图，买家对实际体积大小没概念 | PDP 主图画廊、选型册 |
| `M-002` | **图文引线标注与移动端字号守卫 (Descriptive Callouts)** | 局部特写看不懂拍的是哪，或防水/口袋尺寸等卖点藏在正文被漏看 | PDP 卖点图、结构图 |
| `M-003` | **标配全家福与选配隔离标注法 (Included vs. Optional Accessories)** | 买家漏看随机附赠配件而嫌贵，或误以为选配附件包含在售价内 | PDP 装箱图、套餐图 |
| `M-004` | **首屏产品运转实景直出与五要素闭环 (Product-in-Action Hero)** | 首屏放了抽象插画或大段文字，访客 3 秒内看不懂卖什么实物 | 着陆页首屏、店铺首页 |
| `M-005` | **单栏语义分组与斑马纹参数表法 (Scannable Spec Sheet)** | 参数表太长像一堵墙、视线串行，或双栏参数被误认为两款产品对比 | PDP 参数表、规格书 |
| `M-006` | **纵向展开分节与吸顶目录布局法 (Expanded Sections + Sticky ToC)** | 核心参数、CAD 图纸或评价藏在横向 Tab 里，买家向下滚屏时完全漏看 | B2B/B2C 详情页结构 |
| `M-007` | **字重色阶降噪与无边框分组法 (Weight/Color Hierarchy & Borderless Grouping)** | 页面到处是密集黑灰边框、字号失控、深色背景上灰字/半透明白字发脏看不清 | UI 卡片、详情页模块 |
| `M-008` | **按钮重要性金字塔与小图标容器化 (Button Pyramid & Contained Icons)** | 一屏多个鲜艳实心按钮抢视线，或小图标强行拉大显得粗糙笨重 | 着陆页、操作面板 |
| `M-009` | **多维交付物视觉打包与主推档位版面倾斜 (Value Bundling & Tier Framing)** | 高单价产品被拿去跟低端单品比价，或买家只选最便宜的基础档 | 定价区、定制方案包 |
| `M-010` | **核心视觉识别资产守卫与零思考具象传达 (Distinctive Visual Asset Guard)** | 改版时为了追求极简好看，误把最具辨识度的具象视觉锤改成平庸色块 | 包装改版、列表页主图 |
| `M-011` | **亲密性分群与眯眼停顿计数法 (Proximity Grouping & Eye-Stop Count)** | 元素塞满四角不敢留白、小标题与上下段等距，视线乱跳超过 5 次找不到重点 | 名片、海报、详情页模块 |
| `M-012` | **硬边对齐线与去居中化法则 (Hard-Edge Alignment & Anti-Centering)** | 混用居中/左对齐，或通篇默认居中导致边缘软弱、图文间卡着零碎截留空白 | 全品类网页、画册、广告 |
| `M-013` | **重复视觉锚点与强烈对比法则 (Repetitive Anchors & Bold Contrast)** | 多屏页面像拼凑散页，或全页灰蒙蒙缺乏焦点、12pt 配 14pt 微弱对比像失误 | 多屏详情页、画册、海报 |
| `M-014` | **12 色轮取色、色质拉开与冷退暖进面积比 (Color Wheel, Value & Cool/Warm Ratio)** | 纯色搭配俗气像玩具、深底暗字色质太近发抖模糊，或暖色面积过大压迫视线 | 品牌配色、海报、详情页 |
| `M-015` | **字体禁同门冲突与六维叠加对比法 (Anti-Conflict & 6-Dimension Type Contrast)** | 同页混用两种相似字体打架、手写体配斜体冲突，或全大写长标题占空间难识别 | 标题排版、白皮书、海报 |
| `M-016` | **正文行高模数网格与页边距递进法 (Baseline Modular Grid & Margin Ratios)** | 多图文页面图片高低错落、图注漂浮、文字行与图片顶底边缘对不齐 | 画册、选型册、详情页 |
| `M-017` | **多格矩阵远近景配对与空白格留白法 (8/20/32-Field Matrix & Scale Pairing)** | 多图画册呆板枯燥，或把所有网格 100% 塞满导致画面窒息 | 产品画册、B2B 技术手册 |
| `M-018` | **色块防贴边铁律（字锁格块外扩 / 块锁格字内缩）(Color Field Padding & Bleed)** | 文字放进彩色底框后四周紧贴色块边缘，显得憋屈廉价 | 卖点卡片、海报色带、表格 |
| `M-019` | **展会邀请函无单品构成与展位 170cm 视平线法则 (Typographic Event Poster & 170cm Eye-Level)** | 邀请函硬塞单品抠图成促销传单，或线下展板文字排在下半截被桌椅挡住 | 展会邀请函、展位墙、易拉宝 |
| `M-020` | **去冗余标签、合并键值与表格多维富化法 (De-Labeling, Spec Label Flip & Rich Tables)** | 到处是呆板的 `Label: Value`，或多列表格/单选框干瘪拥挤难以扫视 | 参数表、选型表、商品卡 |
| `M-021` | **非线性间距字阶、行宽 45–75 字符与行高反比铁律 (Non-Linear Scale, 45–75 Chars & Inverse Line-Height)** | 宽屏把 600px 内容硬拉满 1400px 导致百字长行，或大标题行距松垮、同行大小字错位 | 全站排版骨骼、响应式页面 |
| `M-022` | **HSL 9 阶色板、感知亮度色相旋转与对比度翻转法 (9-Shade HSL, Hue Rotation & Flipped Contrast)** | 黄色调暗变泥褐色、颜色调亮发白，或深色徽章配白字抢走主视觉焦点 | 品牌色板、标签徽章、看板 |
| `M-023` | **顶光模拟、双层阴影海拔与图文叠层控对比法 (Top-Light Dual Shadows & Hero Image Contrast)** | 卡片扁平死板、背景照片压字看不清、全屏截图缩成蚊子字或白底图出血融边 | 首屏海报、卡片叠层、画廊 |
| `M-024` | **“别让我思考”60 英里广告牌视觉法则 (Billboard Design 101 & Anti-Visual Noise)** | 自创怪异按钮名、触屏扁平化看不出哪能点、横条乱跨栏或全屏叹号咆哮 | 着陆页、详情页、店铺首页 |
| `M-025` | **Krug 第三定律（字数砍半再砍半）与“后备箱测试”路牌体系 (Cut Half Twice & Trunk Test)** | 页面堆满自嗨欢迎词和说明段、当前 Tab 指示太弱，或落入内页找不到层级方向 | 全站导航、详情页、规格书 |
| `M-026` | **首屏“大爆炸理论”：50ms 第一印象、6–8 词区分度口号与防公地悲剧 (Homepage Big Bang & Tagline)** | 访客 3 秒看不懂公司干什么、口号像大空话，或各部门往首页硬塞横幅沦为公地悲剧 | 独立站首页、国际站旺铺首屏 |
| `M-027` | **“善意储蓄罐”视觉守护、真 FAQ 去伪与前缀关键词双模扫视法 (Goodwill Reservoir & Ear-Scanning)** | 故意隐藏价格/运费耗尽买家耐心、拿自吹自擂假 FAQ 充数，或标题/列表前半句雷同 | 询盘转化页、定价区、FAQ |
| `M-028` | **[实战共创] 高噪商圈/展会巨幕的纯色场降噪、L屏景别递进与打卡背景板法则 (High-Noise Billboard Color-Field Denoising & L-Screen Progression)** | 商圈外墙或展会主背板被周围红黄霓虹灯吞没、少字风景图依然发灰紧绷，或 L 屏被白底膏药块割裂 | 商圈户外巨幕、L屏、展会主背板 |

## 视觉拆解案例卡 (`library/cases/*.md` & `library/cases/en/*.md`)

### 实战共创与街头实拍正反对比拆解（`learning_origin: co_dissected_teardown` · 1 篇）
> 区别于下方静态投喂的设计原著（`book_canon`）与外部实验室报告（`benchmark_study`），本分组记录**用户与 Agent 在真实商业观察中通过连续追问（`inquiry_chain`）与同行街头实拍正反对比共同推演、并经用户确认入库（`status: validated`）的鲜活实战智慧**。可用 `python scripts/library.py search "商圈" --origin co_dissected_teardown` 单独检索。

- [2026 新一代小米 SU7 × 舒淇「卡布里蓝」商圈巨幕 vs. 同行车企大屏正反对比：为什么顶级商圈外墙不谈参数，且纯色场完胜风景图？](cases/C-xiaomi-su7-2026-mall-billboard-teardown.md) · [English](cases/en/C-xiaomi-su7-2026-mall-billboard-teardown.md)（`C-xiaomi-su7-2026-mall-billboard-teardown` · 关联 `M-028`、`F-002`）

### Baymard Institute 电商 UX 眼动与可用性基准（5 篇）
- [Baymard 比例参照实验：用已知尺寸参照物消除 42% 买家的体积误判](cases/C-baymard-in-scale-reference.md) · [English](cases/en/C-baymard-in-scale-reference.md)（`C-baymard-in-scale-reference`）
- [Baymard 图文引线标注实验：用图内结构引线与短标签弥合“只看图不读字”的断层](cases/C-baymard-descriptive-callouts.md) · [English](cases/en/C-baymard-descriptive-callouts.md)（`C-baymard-descriptive-callouts`）
- [Baymard 标配与选配附件图实验：用“标配全家福”与“单独出售”微文案消除价值误判](cases/C-baymard-included-optional-accessories.md) · [English](cases/en/C-baymard-included-optional-accessories.md)（`C-baymard-included-optional-accessories`）
- [Baymard 参数表视觉扫描实验：用单栏语义分组与斑马纹底色取代“参数墙”](cases/C-baymard-spec-sheet-scannability.md) · [English](cases/en/C-baymard-spec-sheet-scannability.md)（`C-baymard-spec-sheet-scannability`）
- [Baymard 详情页导航实验：弃用隐藏核心内容的“横向 Tab”，改用纵向展开分节与吸顶目录](cases/C-baymard-avoid-horizontal-tabs.md) · [English](cases/en/C-baymard-avoid-horizontal-tabs.md)（`C-baymard-avoid-horizontal-tabs`）

### Marketing Examples (Harry Dry) 落地页与品牌识别拆解（4 篇）
- [Marketing Examples 首屏五要素视觉架构：用“产品运转实景”取代抽象插画](cases/C-me-above-the-fold-visual.md) · [English](cases/en/C-me-above-the-fold-visual.md)（`C-me-above-the-fold-visual`）
- [Rows 首屏实测与 Haako 视觉重塑：用“可直视/可交互的产品工作台”取代大段文字说明](cases/C-me-rows-live-product-hero.md) · [English](cases/en/C-me-rows-live-product-hero.md)（`C-me-rows-live-product-hero`）
- [Refactoring UI 与 Basecamp 定价视觉锚定：用版面面积、字号对比与交付物拆解重塑价格感知](cases/C-me-refactoring-ui-pricing-tier.md) · [English](cases/en/C-me-refactoring-ui-pricing-tier.md)（`C-me-refactoring-ui-pricing-tier`）
- [Tropicana 5500 万美元改版教训与 Angostura 超大酒标：守住“零思考识别”的视觉锤](cases/C-me-tropicana-angostura-visual-assets.md) · [English](cases/en/C-me-tropicana-angostura-visual-assets.md)（`C-me-tropicana-angostura-visual-assets`）

### Robin Williams《写给大家看的设计书（第 4 版）》（3 篇）
- [Robin Williams 四大基本原则（CRAP）版式重构实录：从“视线停顿 5 次的业余名片与广告”到专业秩序感](cases/C-williams-crap-layout-makeovers.md) · [English](cases/en/C-williams-crap-layout-makeovers.md)（`C-williams-crap-layout-makeovers`）
- [Robin Williams 色轮与视觉色感实验：用暗色/亮色、色质差与“冷退暖进”法则终结廉价配色](cases/C-williams-color-wheel-value-warmth.md) · [English](cases/en/C-williams-color-wheel-value-warmth.md)（`C-williams-color-wheel-value-warmth`）
- [Robin Williams 字体冲突与六维对比实验：为什么“长得很像的两种字体”是版面大忌？](cases/C-williams-typography-conflict-vs-contrast.md) · [English](cases/en/C-williams-typography-conflict-vs-contrast.md)（`C-williams-typography-conflict-vs-contrast`）

### Josef Müller-Brockmann《平面设计中的网格系统》（3 篇）
- [米勒-布罗克曼 8/20/32 格模数网格与基线对齐实验：以正文行高统领多图文版面](cases/C-muller-brockmann-modular-grid-construction.md) · [English](cases/en/C-muller-brockmann-modular-grid-construction.md)（`C-muller-brockmann-modular-grid-construction`）
- [色块内边距四图实验与瑞士无产品构成海报：防贴边铁律与活动海报去单品化](cases/C-muller-brockmann-color-fields-and-posters.md) · [English](cases/en/C-muller-brockmann-color-fields-and-posters.md)（`C-muller-brockmann-color-fields-and-posters`）
- [B2B 工业品 30 格技术手册与三维展位 170cm 视平线网格：从复杂图纸册到实体展台](cases/C-muller-brockmann-industrial-catalog-exhibition.md) · [English](cases/en/C-muller-brockmann-industrial-catalog-exhibition.md)（`C-muller-brockmann-industrial-catalog-exhibition`）

### Adam Wathan & Steve Schoger《Refactoring UI》（4 篇）
- [Refactoring UI 界面层级与降噪八法：用字重色阶、同色相浅字、粗重对比平衡与去边框重塑商业级质感](cases/C-refactoring-ui-hierarchy-tactics.md) · [English](cases/en/C-refactoring-ui-hierarchy-tactics.md)（`C-refactoring-ui-hierarchy-tactics`）
- [Refactoring UI 数据展示、参数表反强调与富表格重构：从呆板 Label: Value 到高密度可扫描界面](cases/C-refactoring-ui-data-labels-and-tables.md) · [English](cases/en/C-refactoring-ui-data-labels-and-tables.md)（`C-refactoring-ui-data-labels-and-tables`）
- [Refactoring UI 间距系统、反 12 栏教条与排版微操实验：25% 非线性步进、45–75 字符行宽与基线/行高反比法则](cases/C-refactoring-ui-spacing-grid-and-typography.md) · [English](cases/en/C-refactoring-ui-spacing-grid-and-typography.md)（`C-refactoring-ui-spacing-grid-and-typography`）
- [Refactoring UI 9 阶 HSL 色板、感知亮度色相旋转与双层阴影/背景图控对比实验](cases/C-refactoring-ui-hsl-color-depth-and-images.md) · [English](cases/en/C-refactoring-ui-hsl-color-depth-and-images.md)（`C-refactoring-ui-hsl-color-depth-and-images`）

### Steve Krug《Don't Make Me Think, Revisited（第 3 版）》（3 篇）
- [Steve Krug 60 英里广告牌视觉法则：为什么用户从不阅读网页、视觉嵌套错位如何毁掉层级及三大视觉噪音治理](cases/C-krug-billboard-scanning-and-visual-noise.md) · [English](cases/en/C-krug-billboard-scanning-and-visual-noise.md)（`C-krug-billboard-scanning-and-visual-noise`）
- [Steve Krug 第三定律（字数砍半再砍半）与“后备箱测试”：从 103 词减至 34 词的界面瘦身与防迷路路牌系统](cases/C-krug-omit-words-and-trunk-test-navigation.md) · [English](cases/en/C-krug-omit-words-and-trunk-test-navigation.md)（`C-krug-omit-words-and-trunk-test-navigation`）
- [Steve Krug 首屏“大爆炸理论”：50 毫秒第一印象、6–8 词 Tagline 唯一性测试、首页公地悲剧与善意储蓄罐](cases/C-krug-homepage-big-bang-tagline-and-goodwill.md) · [English](cases/en/C-krug-homepage-big-bang-tagline-and-goodwill.md)（`C-krug-homepage-big-bang-tagline-and-goodwill`）
