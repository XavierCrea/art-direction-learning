# 实证美术指导指南 (Evidence-Based Art Direction Guide)

## 一、 核心原则：从传播目的与现有素材出发，去形容词化

实证美术指导不是给美工或 AI 生图工具堆砌“高端、大气、科技感、简约”等空泛形容词，而是先回答三个具体问题：
1. **希望读者看完记住什么 / 做什么（Purpose & Action）**：是帮专业买家核对尺寸、配件和接口，还是让观众认出一个场馆入口、记住活动日期并扫码预约，或是对一幅画面停下来看第二眼？
2. **手头哪份现有素材最能做到（Asset-First Entry）**：有官方场馆照就可以让建筑入口立住到场感；有清晰产品实拍就可以直接裁切排字；只有展名和日期时可以让文字本身成为画面。
3. **图和字怎么分工（Copy-Visual Synergy）**：标题与画面如何互相支撑而不是机械重复？哪一句提出了可验证的产品主张，就必须配齐对应的客观视觉证据。

---

## 二、 第一步：按任务决定起点（产品主张走“事实 $\rightarrow$ 画面证据”三阶梯）

- **非产品主导任务**（如展会邀请函、纯品牌态度海报、用户明确无需产品素材的创意广告）：直接从**传播目的 + 现有素材（场馆、人物、展名、核心情绪）**切入，查阅 [poster-patterns.md](poster-patterns.md) 的“按传播任务找案例”路由表选定起点。
- **含可验证产品主张的任务**（详情页卖点屏、规格选型、硬件对比）：凡画面或文案提出具体产品性能、尺寸、工艺、测试或配件主张，逐条过一遍三阶推导表：

| 阶梯 | 核心问题 | 示例 1（工业/硬件设备） | 示例 2（多配件消费品/工具） |
| :--- | :--- | :--- | :--- |
| **1. 已核实事实 (Confirmed Fact)** | 哪一句提出了可验证的尺寸、工艺、测试或配件事实？ | 48kWh 储能柜，宽深高 600×800×2000mm，支持 ≤10ms 并离网切换 | 厨师机含主机 + 3 个不锈钢搅拌头（标配），压面器需另购（选配） |
| **2. 具象画面动作 (Concrete Visual Element)** | 用什么参照物、景别或图示让读者一眼看懂？ | **比例参照图（In-Scale）**：机柜置于标准工业配电房通道，旁立 175cm 工程师作体量参照；辅以清晰的并离网切换机理示意 | **标配全家福（Included Accessories）**：主机与 3 个标配搅拌头同框陈列并标 `Included`；选配压面器清晰隔离并标 `Sold Separately` |
| **3. 素材前提与禁用边界 (Asset Prerequisite & Limit)** | 必须核对什么真实素材？绝对不能伪造什么？ | 需真实机柜长宽高比例；无实测示波器图时用清晰逻辑图，**严禁伪造假示波器截图** | 需核实 BOM 标配清单；**严禁把选配附件混入主图却不加文字声明** |

---

## 三、 第二步：常见视觉困境与用户原话的“症状诊断路由（Symptom-to-Case Routing）”

将用户的自然描述或当前页面的卡点转成中英文检索词，运行 `python3 scripts/library.py search "关键词或口语句" --brief`（支持中文自然口语、CJK bi-gram 与轻量同义词召回；需完整字段时省略 `--brief` 或传 `--verbose`），再按需用 `get` 批量读取完整记录与关联案例：

| 当遇到以下视觉痛点或用户原话（Symptom / `when_stuck`） | 推荐检索词 (`search`) | 优先调取的核心方法与案例 (`M-001`–`M-042`) |
| :--- | :--- | :--- |
| **写了尺寸数字，但读者对实物没大小概念** | `比例 参照 尺寸` 或 `in-scale size` | `M-001` · `C-baymard-in-scale-reference` |
| **“看不出这是什么”或局部特写不知道拍了哪个部件** | `特写 引线 图注` 或 `callout caption crop` | `M-002` · `C-baymard-descriptive-callouts`。也可参考构图指南 P-01，先展示轮廓和使用位置。 |
| **买家搞不清图片里的配件到底送不送 / 产生售后纠纷** | `配件 标配 选配` 或 `accessories included` | `M-003` · `C-baymard-included-optional-accessories` |
| **首屏放了漂亮插画或大段文字，访客看不出卖什么实物** | `首屏 实景 演示` 或 `above the fold hero` | `M-004` · `C-me-above-the-fold-visual` · `C-me-rows-live-product-hero` |
| **参数表太长像一堵墙、视线串行，或双栏被误认为两款对比** | `参数表 扫描 分组` 或 `spec sheet scannability` | `M-005`、`M-020` · `C-baymard-spec-sheet-scannability` · `C-refactoring-ui-data-labels-and-tables` |
| **详情页把核心参数/CAD藏在横向 Tab 里，买家滚屏时漏看** | `横向标签 折叠 导航` 或 `horizontal tabs` | `M-006` · `C-baymard-avoid-horizontal-tabs` |
| **“像模板 / 边框太多太杂” / 字号乱放大、按钮分不清主次** | `层级 边框 按钮` 或 `hierarchy borders buttons` | `M-007`、`M-008` · `C-refactoring-ui-hierarchy-tactics` |
| **高单价产品显得太贵、或者想引导买家看懂多档位价值差** | `高价 锚点 套餐 梯度` 或 `pricing tier price ladder` | `M-009`、`M-035` · `C-me-refactoring-ui-pricing-tier` · `C-aotw-three-seven-paris-price-scale` |
| **改版包装或主图时，不小心把最有辨识度的视觉资产改丢了** | `辨识度 包装 视觉锤` 或 `distinctive asset rebrand` | `M-010` · `C-me-tropicana-angostura-visual-assets` |
| **元素塞满四角、默认居中软弱、缺视觉焦点或字体打架** | `亲密性 对齐 对比 字体` 或 `crap alignment typography` | `M-011`–`M-015` · `C-williams-crap-layout-makeovers` · `C-williams-color-wheel-value-warmth` · `C-williams-typography-conflict-vs-contrast` |
| **多图文画册高低错落、色块贴边憋屈、活动海报无实物可拍** | `网格 基线 色块 展位` 或 `modular grid booth` | `M-016`–`M-019` · `C-muller-brockmann-modular-grid-construction` · `C-muller-brockmann-color-fields-and-posters` · `C-muller-brockmann-industrial-catalog-exhibition` |
| **间距纠结、百字长行、HSL 调色发脏、深色徽章抢戏或背景图吃字** | `间距 行宽 HSL 阴影` 或 `spacing hsl shadow contrast` | `M-021`–`M-023` · `C-refactoring-ui-spacing-grid-and-typography` · `C-refactoring-ui-hsl-color-depth-and-images` |
| **按钮名字费脑、扁平化看不出可点、说明文太长或内页迷路** | `广告牌 噪音 砍半 后备箱 口号` 或 `billboard trunk test tagline` | `M-024`–`M-027` · `C-krug-billboard-scanning-and-visual-noise` · `C-krug-omit-words-and-trunk-test-navigation` · `C-krug-homepage-big-bang-tagline-and-goodwill` |
| **商圈外墙/展会远距大牌被环境噪点吞没、L 屏割裂或没人打卡** | `商圈 户外大屏 纯色场 L屏 打卡` 或 `mall billboard color field` | `M-028` · `C-xiaomi-su7-2026-mall-billboard-teardown` |
| **信息流封面没人停滑、轮播翻页率低、移动端按钮难按或选择瘫痪** | `孤立效应 峰终 翻页 拇指热区` 或 `von restorff swipe carousel fitts` | `M-029`–`M-032` · `C-lawsofux-*` |
| **9:16 竖屏字被平台控件挡住，或开场缺少接着看的理由** | `9:16 安全区 版位` 或 `9:16 safe zones` | `M-033` · `C-tiktok-9x16-safe-zones-and-2s-hook` |
| **“太像硬广没人点” / 怎么公平对照竞品或排查低点击率素材** | `原生静态图 对比 停滑率` 或 `us vs them native static` | `M-034` · `C-motion-native-statics-and-us-vs-them` |
| **“想让人停一下、再看一眼” / 品牌海报太直白说教 / 日用品想做双关** | `视觉反转 Double-Take 光锥 容器嫁接` 或 `double-take container grafting` | `M-036` · `C-aotw-fnac-visual-subversion-light-cone` · `C-ikea-tomorrow-starts-tonight-container-metaphor` |
| **无实物服务/活动没图可放，硬凑 3D 显得假大空** | `纯字体墙 无实物 二维码` 或 `typographic wall product-free` | `M-037` · `C-aotw-muserk-typographic-wall-poster` |
| **看不见的底层安全/防抖/均衡技术，怎么不靠丑陋示意图讲清** | `符号逐帧演进 隐形技术 静默底注` 或 `icon as diagram whisper reveal` | `M-038` · `C-aotw-mercedes-rollover-sensor-state-sequence` |
| **想让人看懂某个物理动作或材料变化** | `符号 真实形变` 或 `symbol deformation` | `M-039` · `C-coca-cola-recycle-me-deformation` |
| **防眩光/声场/风道/散热等无形物理性能实拍不出、发光箭头太廉价** | `无形物理场 光学射线 通道2矢量` 或 `ray path diagram invisible physics` | `M-040` · `C-louispoulsen-ph-centenary-ray-diagram` |
| **多 SKU 选型矩阵白底枯燥没体积感，或缺豪华实景预算** | `建筑折角灰场 多SKU 双色切面` 或 `architectural corner two-tone` | `M-041` · `C-hay-montana-architectural-corner-blocking` |
| **平价日用品想讲“买得起/有温度”，但一打折就变地摊广告** | `损耗现场 微型价签 空置主角` 或 `micro price tag mishap empty product` | `M-042` · `C-ikea-price-relief-and-empty-product-narrative` |

---

## 四、 第三步：与 `copywriting-learning` 的双技能组合交接协议（Combo Protocol）

当与 `copywriting-learning` 打组合拳时，按 **`[传播目的与文案] $\rightarrow$ [画面分镜与素材] $\rightarrow$ [图字排版]`** 咬合输出：

1. **检查“图字分工（Copy-Visual Synergy）”**：
   - 坏配合：标题写 *“Waterproof Outdoor Speaker”*，画面只放一个干巴巴的白底音箱。
   - 好配合（互补求证）：标题写结果或场景（*“Keep the music playing through sudden downpours.”*），画面用**飞溅水花动态特写 + `IPX7 Waterproof (1m / 30min)` 清晰标注**直接给出视觉证明（源自 `C-baymard-descriptive-callouts`）。
2. **按载体形态决定文字放图内还是图外（Format-Aware Copy Placement）**：
   - **网页 / 电商详情页（图外存在 HTML 正文容器）**：图内优先放核心主标与简短标注，长解释说明可移出图片作为 HTML 正文或下方图注（Caption），既利可读又利检索与响应式适配；
   - **独立转发物料（朋友圈海报、展会邀请函、小红书单图笔记、线下灯箱）**：没有图外 HTML 容器，读者完成任务所需的全部信息（包括超过 2 行的邀请语、日程、地址或书信体正文）必须随图保留；
   - **终端验收**：`375px` 屏宽可作为手机端预览样例，最终一律按**实际发布位置、观看距离与平台 UI 遮挡（如 `M-033` 竖屏安全区）**核验完成任务所需信息是否清晰可读。

---

## 五、 第四步：交付颗粒度、观看条件与下游落地通道

- **场景 A：单张海报 / 广告 / 首屏 Hero / 展会邀请函（及未定调的整套详情页首屏代表图）**
  - **方向未定时**：默认提供 **2–3 个有实质区别的构图方案（Visual Angles）**——其中 **1–2 套**由本技能案例机制与风格母版推导（写明借用依据、信息揭晓顺序、素材依赖与必须保真的细节），**另保留 1 套「原生自由对照位（Blank-Slate Native Option）」**，防止风格库造成审美收敛：
    1. **真隔离优先（兼容任意支持子代理的 Harness）**：若当前运行环境具备独立子代理/独立会话工具（如 `invoke_subagent`、`Agent`、`spawn_agent` 等），**必须并行启动 1 个干净子代理**独立产出该方案（优先选用只读且可读图的子代理类型）；仅当环境无此类工具时，才在同一上下文中脱离 `M-*` / `P-*` / `styles/` 软解绑产出；
    2. **原始输入防污染白名单（关键：开工前冻结原始 brief）**：发给干净子代理的**必须是未经主代理“事实阶梯 / 症状路由 / 体裁诊断”改写的原始输入快照**——只准包含 ① **用户原始需求原文**、画幅载体与用户明确提出的硬约束（如指定品牌色、必含文案/日期/展位）、② 原始素材路径（或其纯客观物理描述，若任务含客观产品参数则仅附用户提供的原始客观事实清单，不夹带主代理的视觉诊断结论）、③ 显式隔离指令——*“禁止读取或调用任何美术/设计/详情图 skill、风格库或案例库，完全凭自身对品类与商业视觉的原生理解独立输出 1 套完整构图与视觉提案”*；严禁传入任何 `M-*` / `P-*` / 风格母版名、主代理诊断框架或主代理正在做的其余方案；
    3. **来源验真标记**：交付提案时显式标注 `[原生自由提案 · 独立干净子代理盲产]` 或 `[原生自由提案 · 当前环境无子代理工具，软解绑产出]`；
    4. **选中后源头防漂移（只套工程门禁、不改审美灵魂）**：若用户认可该原生自由提案，后续起草画面 Prompt / 构图布局也优先延续原生思路（可交由同一干净子代理或不加载既有风格母版的路径起草），主代理仅按 [output-qa-gate.md](output-qa-gate.md) 执行制作通道分流与 `QA-1`–`QA-5` 客观验收红线，严禁用既有风格母版把它“修回模板味”。
  - **方向已定时**：若用户已选定构图方向或给了明确参考图，直接深化 **1 套高质量方案**（不额外强凑自由对照位）。
- **场景 B：完整详情页分镜（PDP Storyboard）或落地页全页改版**
  - 交付 **1 套逻辑连贯的分屏执行表**，按买家认知节奏逐屏解答疑问（如首屏定调 `M-004`/`M-026` $\rightarrow$ 核心细节确证 `M-002` $\rightarrow$ 比例参照与标配 `M-001`/`M-003` $\rightarrow$ 单栏语义规格表 `M-005`/`M-020` $\rightarrow$ 坦诚 FAQ `M-027`）。
- **场景 C：户外海报与线下展会（按实际观看条件选构图）**
  - 保留核心原则——**“远处快速经过先识别，停步走近再读细节”**；具体视距、高度与信息密度取决于真实场地、遮挡以及观众是步行、乘车还是坐着观看：
    - **纯手机/邮件发送的展会邀请函**：直接按聊天窗口或邮件客户端的实际预览验收，无需硬套三段空间距离；
    - **确实同步统筹场外大牌 + 展位背板 + 桌面资料时**：可参考 `100m → 10m → 1m`、`170cm` 站立视平线（`M-019`）与 `≥75%` 单色场（`M-028`）等具体案例做法——远处快速经过优先识别展名、方向或品牌（`75%` 纯色只是候选做法之一）；观众可以停步走近的通道、候车亭或展位内，则完全允许使用叙事照片（`M-036`）、长文信件或可扫二维码（`M-037`）。
- **下游执行通道、风格三级借用与客观验收门禁（单一权威定义源）**：
  - 所有制作路线分流（**通道 0 原片直排 / 通道 1 AI 无字重绘+矢量排字 / 通道 2A 纯平面代码渲染 / 通道 2B 平面底图+抠图混合 / 通道 3 响应式网页代码 / 通道 4 原片证据与拍摄执行单**）、风格参考三级降级规则、**`QA-1`–`QA-5` 一票否决红线**、`scripts/qa_check.py` 机检辅助及代表图确认机制，统一以 [output-qa-gate.md](output-qa-gate.md) 为唯一权威标准，执行前直接对照该文落实。
