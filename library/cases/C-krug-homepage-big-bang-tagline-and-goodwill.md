# C-krug-homepage-big-bang-tagline-and-goodwill：首屏“大爆炸理论（50ms 第一印象）”、Tagline vs. Motto 定位与买家“善意储蓄罐（Goodwill Reservoir）”

[中文案例索引](../README.md) · [English](en/C-krug-homepage-big-bang-tagline-and-goodwill.md)

- **来源**：`S-krug-dmmt-3e-2014`（Steve Krug, *Don’t Make Me Think, Revisited: A Common Sense Approach to Web Usability*, Third Edition, 2014, Chapter 7, Chapter 10, Chapter 11 & Chapter 12, PDF p.114–135, p.175–186, p.203–222）
- **关联方法**：`M-027`（首屏“大爆炸理论”、价值口号定位与买家善意储蓄罐守卫）
- **案例类型**：`design_critique`（首屏认知拆解、Tagline 正反例对比与用户体验心理账户模型）

---

## 1. 卡点症状 (`when_stuck`)

- 买家点进首页或落地页首屏，看了 5 秒钟还搞不清楚“这家公司到底是卖什么的？跟别的贸易商有什么区别？我该点哪里开始选型？”；
- 品牌 Logo 旁边挂着一句像“共创美好未来 / 追求卓越品质（We bring good things to life）”这样放之四海而皆准的空洞座右铭（Motto），或者在首屏放了一大段选美小姐发言式的企业使命宣言（Mission Statement）；
- 业务部门轮流往首页塞自己的推广位（“这里还有一块空白，把新活动横幅也塞进去！”），引发“公地悲剧（Tragedy of the Commons）”，把原本下金蛋的首页彻底挤爆；
- 为了逼买家留资，故意把产品价格区间、运费规则、规格书下载或客服联系方式藏起来，或者在注册/询盘表单里强迫买家填一堆非必要隐私字段，瞬间掏空买家的耐心与信任。

---

## 2. 客观画面与可用性观察 (`observations`)

1. **首屏“大爆炸理论”与 50 毫秒第一印象（PDF p.114–122）**：
   - 引用加拿大卡尔顿大学（Carleton University）研究：用户仅需 **50 毫秒（1/20 秒）** 就会对网页视觉形成第一印象，且后续行为高度受此初始判断支配（PDF p.120）；
   - 即便用户是从内页深链接进站，一旦迷路也会像潜水员一样“浮出水面（Bob up to the surface）”回到首页找方向（PDF p.121–122）。
2. **首屏必须在几秒内无需思考回答的 5 个问题（PDF p.119, p.128–129）**：
   - **Q1：What is this?（这是什么网站/什么品类？）**
   - **Q2：What do they have here?（这里提供什么产品/内容？）**
   - **Q3：What can I do here?（我在这里能完成什么操作？）**
   - **Q4：Why should I be here—and not somewhere else?（为什么选你而不是去别家？）**
   - **Q5：Where do I start?（我从哪里开始？——必须一眼看到 `How to search`、`How to browse`、`How to sample their best stuff` 三大起点，PDF p.128–129）**。
   - **正面标杆（Kickstarter 首屏，PDF p.124）**：顶部通栏直接写明 `Kickstarter is the world's largest funding platform for creative projects.`，下方紧跟真实项目卡片，1 秒回答全部大问题。
3. **Tagline（价值口号）vs. Motto（企业座右铭）vs. Mission Statement（企业使命）（PDF p.122–128）**：
   - **拒绝用企业使命充当首屏导语（PDF p.124–125）**：银行或制造厂常把“本司致力于以世界级标准提供全方位解决方案……”贴在首屏，Krug 指出这就像选美比赛选手说“我的愿望是世界和平”一样毫无信息量；
   - **Tagline 与 Motto 的本质区别（PDF p.126–127）**：
     - **Motto（座右铭）**表达的是企业崇高理想（如通用电气 *"We bring good things to life"*、*"You can with a Nissan"*），换任何一家公司都能套用；
     - **Tagline（价值口号）**紧贴在 `Site ID` 旁边或下方，用 **6–8 个词** 直接交代“整个网站做什么 + 核心差异化好处”（如明尼苏达州立大学 *"Real college. Real-world ready."*，PDF p.126–127）；
   - **好 Tagline 的 6 条黄金标准（PDF p.126–127）**：① 清晰且有信息量（Clear and informative）；② 刚好 6–8 个词（Just long enough, six to eight words）；③ 传达差异化与明确利益（Convey differentiation and a clear benefit）；④ **通过 Jakob Nielsen 唯一性测试**（“世界上没有第二家竞争对手能原封不动照抄这句话，除非你的价值主张确实是同类中真正的行业第一”）；⑤ 活力凝练、不喊泛泛口号（Personable, lively, and sometimes clever without being generic）；⑥ 紧挨 Site ID 放置。
4. **首页“公地悲剧（Tragedy of the Commons）”与杀金鹅效应（PDF p.129–133）**：
   - 每个部门都想在首页分一块饼宣传自己的栏目，结果满屏都是五颜六色的促销块，视觉焦点彻底瓦解，导致所有部门的点击率一起暴跌。
5. **买家“善意储蓄罐（The Reservoir of Goodwill）”水位计模型（PDF p.203–211）**：
   - 每个买家进站时都带着一个容量有限的“善意储蓄罐”（PDF p.204–205）；
   - **瞬间抽干善意的 6 大恶习（PDF p.206–208）**：
     1. **隐藏我想要的核心信息**（Hiding information that I want：藏起客服电话、隐藏运费/定制门槛、藏起基础价格，逼用户填长表才给看，PDF p.206）；
     2. **因为没按你的格式输入而惩罚我**（Punishing me for not doing things your way：电话号码或卡号不准输空格/横杠，报错重填，PDF p.207）；
     3. **索要并非真正必要的个人/公司隐私信息**（Asking me for information you don't really need，PDF p.207）；
     4. **虚情假意与客套套话**（Shucking and jiving me：如让用户苦等时播报“您的来电对我们非常重要”，PDF p.208）；
     5. **用华而不实的营销大图挡路**（Putting sizzle in my way：在用户急着查参数时强插无信息量的形象大片，PDF p.208）；
     6. **网站长得业余、粗糙、缺乏秩序**（Your site looks amateurish，PDF p.208）。
   - **给善意储蓄罐注水的 7 大动作（PDF p.209–211）**：
     - 把买家最常做的 Top 3 核心任务做成一眼可见且极度顺畅；直接说清所有可能想到的关键事实；省掉多余步骤；公开透明标注价格/运费/限制；提供**真 FAQ（Candid FAQs，真正在客服一线被问爆的问题，严禁放 `QWWPWAs`——Questions We Wish People Would Ask 营销部自问自答软文，PDF p.210）**；提供打印友好版与轻松报错恢复。
6. **移动端恶劣权衡反例与读屏“用耳扫视”（PDF p.178–186, p.220–222）**：
   - **CBS News 移动端 8 页翻页反例（PDF p.181–182）**：为了赚广告曝光，把一篇短新闻在手机上拆成 8 页，每页只有一两句话却逼用户点 8 次 `Next`——属于典型的牺牲可用性换短期指标、抽干善意储蓄罐；
   - **读屏用户的“用耳扫视（Scanning with their ears，PDF p.220）”**：盲人用户使用屏幕阅读器时同样在“扫视”——他们把语速调得极快，只听每个标题或链接的**前几个词**就决定是否跳过。因此，**把核心关键词前置在标题和链接的最开头**，同时惠及普通视觉扫视者与无障碍用户。

---

## 3. 图字分工 (`copy_visual_synergy`)

- **首屏文案（Tagline + Entry Points）**：在左上角 `Site ID` 旁配 6–8 词唯一性价值口号（Tagline），首屏主标题与副标题在 3 秒内交代品类、核心参数优势与适用场景，并将关键触发词置于链接与小标题最前端；
- **首屏视觉布局（Big Bang Layout）**：首屏严禁堆砌多部门碎片横幅，清晰给出 `Search（搜索）`、`Browse（按场景/规格分类浏览）`、`Sample（核心爆款/标杆案例直接预览）` 三大视觉起点，并将真实报价梯度、MOQ、认证或规格书下载入口大方摆在明面。

---

## 4. 可迁移视觉动作 (`reusable_move`)

1. **5 秒首屏五问自检**：遮住内页，只看首屏，检查未接触过本品牌的陌生买家能否在 5 秒内说出“这是卖什么的、有什么核心规格、为什么选这家、第一步点哪里”；
2. **用 6–8 词 Tagline 替换 Motto/使命宣言**：紧贴 Logo 写一句带具体品类与差异化利益的 6–8 词价值口号，删掉首屏一切“致力于行业领先”的公关套话；
3. **执行“善意储蓄罐”清障**：将买家最关心的硬信息（关键参数、MOQ/价格锚点、认证编号、选型表下载、直接联系方式）直接摊开在明处，表单字段砍到最少，FAQ 只回答真实技术/商务顾虑。

---

## 5. 素材前提与迁移边界 (`asset_prerequisites` & `transfer_limits`)

- **素材前提**：需提炼品牌相对于同行真正可验证的差异化事实（如特定应用领域的量产规模、实测电气性能、专属定制交期），以及客服/销售团队最常被买家追问的 3–5 个真实顾虑。
- **迁移边界**：若品牌已是家喻户晓的全球巨头（如 Apple、Nike、Amazon），首屏无需再解释“我们是做什么的”（PDF p.123）；但对于 99% 的垂直品牌与 B2B 制造商而言，首屏清晰传达定位与 Tagline 是生死线。
