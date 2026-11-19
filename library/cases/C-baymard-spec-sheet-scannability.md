# Baymard 参数表视觉扫描实验：用单栏语义分组与斑马纹底色取代“参数墙”

[中文案例索引](../README.md) · [English](en/C-baymard-spec-sheet-scannability.md)

[返回视觉案例库](../README.md) · 独立可用性测试与眼动追踪研究

- **卡点症状 (`when_stuck`)**　工程或科技产品参数多达几十项，直接排成密密麻麻的“参数墙（Wall of Specs）”或为了省高度排成左右两栏，导致买家找不到关键指标，甚至把同一款产品的左右两栏参数误认为“两款型号的对比表”。
- **适用载体**　产品详情页参数规格表（PDP Spec Sheet）、B2B 选型手册、PDF 规格书（Datasheet）。

## 原材料里看到什么 (`observations`)

- Baymard Institute 评测发现，**50%** 的头部电商网站参数表存在严重的视觉可扫描性缺陷：
  1. **23% 网站未做语义分组（Lowe's vs. Tesco）**：Lowe's 将冰箱所有参数混成一张无分组长表，受试者找尺寸和保修期极为吃力；Tesco 将超过 20 项的参数按品类语义拆分为带小标题的子区块（如 `Dimensions & Weight`），扫视速度大幅提升。
  2. **仅 3% 网站提取顶部核心参数摘要（Costco vs. Best Buy）**：面对超过两屏高的参数表，Best Buy 在顶部单独提炼了 `Key Specs`（核心参数摘要），同时在下方完整分组表中保留原项，兼顾快速初筛与深度核对。
  3. **23% 网站缺乏水平视线引导（Sears vs. REI 眼动追踪）**：Sears 参数名与参数值之间距离宽且无底色交替，买家视线横向移动时极易串行；REI 采用**交替行底色（斑马纹 Alternating Row Shading）**，眼动实验证实受试者能先纵向扫视左列标签，再顺着色带精准横向定位右侧数值。
  4. **20% 网站误用双栏排版（Grainger vs. B&H Photo）**：Grainger 将单款产品的参数分成左右并排的两大列，测试中多名买家直接将其误认为“两款不同产品的对比表”；B&H 采用严格的单栏列表，零误读。

## 图字如何分工 (`copy_visual_synergy`)

- **版面结构与色带负责“引导眼动轨迹”**：通过分组留白、小标题字重、斑马纹底色与单栏对齐，建立“先纵向找组 $\rightarrow$ 再纵向找字段名 $\rightarrow$ 再顺色带横向读数值”的低摩擦视觉通道。
- **分组命名与数值格式负责“降低认知负荷”**：按产品真实属性命名分组（如电池类分为 `Electrical Specs`、`Mechanical & Dimensions`、`Protection & Certifications`），并统一全站同品类的单位格式。

## 可迁移的视觉动作 (`reusable_move`)

1. **满 15–20 项参数强制语义分组**：将长参数表拆成 3–5 个具象子模块，每组配加粗分组小标题，把买家最高频检索的组（如核心性能、尺寸重量）排在最上方。
2. **超长表置顶 `Key Specs` 摘要栏**：若完整参数超过 2 屏，在表头上方用 4–6 格图标/大字卡片提取核心指标，同时在下方完整表中保留对应条目。
3. **加斑马纹或细分割线**：左列参数名与右列参数值之间使用交替浅灰底色（如 `#F8FAFC` 与 `#FFFFFF`）或浅色水平细线，控制单行最大宽度，防止横向视线串行。
4. **单品参数表严禁排成左右双栏**：单款产品的参数一律保持单栏结构；仅在真正对比多款型号（Model A vs. Model B）时才使用多列矩阵。

## 素材前提与迁移边界 (`asset_prerequisites` & `transfer_limits`)

- **素材前提**：所有参数值必须先完成标准化清洗（统一单位与命名，不可直接粘贴供应商杂乱无章的原始表格）。
- **禁用边界**：置顶 `Key Specs` 摘要后，不能把这几项从下方的完整分组表中删掉（部分直接跳到对应分组查找的买家会以为缺失该参数）。

## 已知效果与出处

- **证据属性**：独立可用性测试、眼动追踪实验与 60 家顶级网站基准统计（50% 存在扫描缺陷、20% 误用多栏、23% 未分组）。
- **出处**：Edward Scott, *Product Spec Sheets: 4 Ways to Make Spec Sheets More Scannable for Users (50% of Sites Get It Wrong)*, Baymard Institute, 2018-03-27 (`https://baymard.com/research-articles/spec-sheet-scannability`)。
- **关联方法**：`M-005`（单栏语义分组与斑马纹视线引导法）。
