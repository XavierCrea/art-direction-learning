# Refactoring UI 数据展示、参数表反强调与富表格重构：从呆板 Label: Value 到高密度可扫描界面

[中文案例索引](../README.md) · [English](en/C-refactoring-ui-data-labels-and-tables.md)

## 基本信息
- **案例 ID**：`C-refactoring-ui-data-labels-and-tables`
- **来源**：`S-wathan-schoger-refactoring-ui-2018`（Adam Wathan & Steve Schoger, *Refactoring UI*, 2018，原书及 PDF p.48–55、p.130、p.220–222、p.242–248）
- **关联方法**：`M-020`（去冗余标签、合并键值与表格多维富化法）、`M-005`（单栏语义分组与斑马纹参数表法）
- **适用渠道**：`spec_sheet`、`pdp`、`catalog`、`landing_page`

---

## 一、原书对照实验与视觉观察（Verified Book Evidence）

### 1. 摆脱 `Label: Value` 机械直出与键值合并（PDF p.48–50）
- **反例病灶（p.48）**：直接把数据库字段排成 `Name: Jane Doe`、`Email: janedoe@example.com`、`Phone: (555) 765-4321`、`Department: Customer Support`，导致每一项数据权重相等，完全无法建立视觉层级（*"every piece of data is given equal emphasis"*）。
- **正例重构（p.48–50）**：
  1. **靠格式与上下文免除标签（p.48–49）**：`janedoe@example.com`、`(555) 765-4321`、`$19.99` 无需标签即可一眼认出；员工姓名下方的 `"Customer Support"` 靠上下文即知是所属部门。
  2. **将标签与数值合并为单一语义单元（Combine labels and values, p.49–50）**：
     - 电商库存把 `"In stock: 12"` 改为 **`"12 left in stock"`**（p.49）；
     - 房产卡片把 `"Bedrooms: 3"` 改为 **`"3 bedrooms"`**（p.50），使数值与量词融为一体，极易做粗细与字号分级。

### 2. 数据看板 vs. 技术参数表的“标签反强调”分流（PDF p.50–53）
- **常规数据卡片（Labels are secondary, p.50–51）**：在展示多块可扫描数据（如财务看板）时，数据本身才是主角，标签只是辅助说明——应将标签压小、降低对比度或减轻字重。
- **技术规格参数表（When to emphasize a label, p.51–53）**：
  - 原书明确指出：**在信息密集的技术规格表（Technical specifications of a product）中，买家是在扫视寻找标签名称（如寻找 `"depth"`，而不是寻找 `"7.6mm"`）**（*"If a user is trying to find out the dimensions of a smartphone, they're probably scanning the page for words like 'depth', not '7.6mm'"*, p.51）。
  - **正例做法（p.52–53）**：在技术参数表中反过来**加重参数名标签（深色/中粗体）**，而将右侧参数值设为稍微浅一档的深灰色（*"Simply using a darker color for the label and a slightly lighter color for the value is often enough"*, p.52），既方便纵向扫视定位参数项，又不牺牲参数值本身的可读性。

### 3. 视觉层级与 HTML 文档标签脱钩（PDF p.54–55）
- 许多界面把 `<h1>Manage Account</h1>` 排得巨大无比，抢走了表单内容本身的焦点。实际上分节标题往往只起辅助标签作用（*"section titles act more like labels than headings — they are supportive content"*），应根据视觉层级需要将其字号压小，绝不被 `h1/h2` 语义标签绑架字号。

### 4. 打破传统单调表格与单选框：合并关联列、富化状态与卡片化选项（PDF p.130, p.220–222, p.242–248）
- **数字列右对齐（Right-align numbers, p.130）**：含数字/金额的表格列强制右对齐，使小数点垂直共线，一眼即可纵向对比大小。
- **合并无需单独排序的关联列（p.244–245）**：
  - **反例（p.244 上图）**：6 列表格（`NAME | ROLE | POLICY | POLICY TYPE | LOCATION | STATUS`），每列只放一个纯文本字段，显得扁平拥挤且毫无层级。
  - **正例（p.244 下图 & p.245 上图）**：将不需要单独排序的关联列合并为双层单元格——把 `Role`（`VP of Sales`，浅灰小字）叠放在 `Name`（`Molly Sanders`，深色粗体）正下方并左配圆形头像；把 `Policy Type`（`All-inclusive Policy`）叠放在金额 `$20,000` 正下方；将 `Status` 纯文字升级为浅绿底深绿字胶囊标签（`Approved`），表格从 6 列精简为 4 列，可读性与专业感倍增。
- **把干瘪单选框升级为可点选对比卡片（Selectable cards, p.245–246）**：
  - 将垂直堆叠的 4 个单选圆点（`Hobby - 1 GB ($5/mo)` 等，p.245 下图）重构为 4 张横向并排的视觉选型卡（p.246 上图）：顶部小号大写档位名（`GROWTH`）+ 右上角勾选徽章 + 中部超大字号核心规格（**`5 GB`**）+ 底部价格（`$10 / mo`）+ 选中态彩色描边。
- **升级默认列表符号（Supercharge the defaults, p.220–221）**：将普通圆点列表替换为语义图标（勾选图标 `✓` 或安全锁图标 `🔒`），将客户证言的引号放大染色转为背景视觉装饰。

---

## 二、图文协同机制（Copy-Visual Synergy）
- **文案合并释放视觉层级**：当文案把 `"In stock: 12"` 改写为 `"12 left in stock"` 时，消除了冒号分割带来的左右分裂，视觉可以直接对整句或数字做高亮。
- **参数名深、参数值稳**：在 B2B 选型表与规格书中，买家按“维度名称”检索，用深色锁住左列标签、用右对齐锁住数值小数点，彻底打通“扫标签 → 读数值”的眼动链路。

---

## 三、可复用视觉动作（Reusable Move）
1. **清理废话标签**：删掉邮箱、电话、价格、部门等自明字段前的 `Label:`，将库存/数量/配置改写为“数值+名词”自然短语。
2. **区分看板与参数表的强调方向**：核心指标概览卡用“大号深色数值 + 小号浅灰标签”；到底部完整技术规格表时切换为“深色加粗参数名 + 次深色右对齐参数值”。
3. **重构多列表格与选型交互**：将无需独立排序的从属字段（如型号+封装、姓名+职位、价格+计费周期）上下双层合并到同一列，加入状态色标胶囊，并将核心档位切换从单选按钮升级为横向可点选规格卡。

---

## 四、迁移边界（Transfer Limits）
- 若表格某一列必须支持用户点击表头独立排序或筛选，则该列核心对比字段仍应保持独立或确保合并后主排序字段在首行突出；
- 技术参数表中“突出标签”不等于“弱化数值到看不清”，数值仅比标签浅半档（如 `#0F172A` 配 `#334155`），严禁将重要工程参数值设成浅灰。
