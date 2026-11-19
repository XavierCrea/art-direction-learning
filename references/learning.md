# 学习与更新指南 (Learning & Ingestion Workflow)

## 一、 收到书籍、网页或视觉样稿时的防伪核验

1. **核对原始出处与完整性**：
   - 记录标题、作者/研究机构、发布日期、URL 或 ISBN/版次、获取日期。
   - **书籍 PDF 严格防伪**：先读取封面、版权页、目录及前 15–25 页正文。若发现带有 `Bookey`、`Blinkist`、`Summary`、`Install App to Unlock Full Text`、大字号提纲或缺失原书广告插图，**立即向用户报告该文件为第三方浓缩摘要版，拒绝将其作为原书信源入库**。
   - **已读范围诚实登记**：只登记本轮实际打开并核验过的 `pdf_pages` 或网页段落；未读章节保持未登记状态，绝不凭印象补齐。

---

## 二、 用“五把解剖刀”拆解视觉案例

每拆解一则广告、详情页改版或 UX 报告，强制分离**客观画面观察**与**主观分析**，提炼以下 5 项结构化内容：

1. **卡点症状 (`when_stuck`)**：用中英双语写出设计师或卖家在什么具体痛点下需要搜到这张卡（如：“只放白底图导致买家误判产品体积 / `buyers misjudge size from cutout photos`”）。
2. **客观画面观察 (`observations`)**：只记录肉眼可见的物理布局（景别、参照物、左右分栏比例、字号字重对比、边框/背景色差、实验样本数据）。
3. **图字分工机制 (`copy_visual_synergy`)**：拆解画面与文字是如何配合的——画面承担了哪部分直觉证明？文字或引线标注（Callouts）补充了哪部分非视觉信息？
4. **可迁移视觉动作 (`reusable_move`)**：剥离原品牌与原品类，写成动词开头的通用视觉指令。
5. **素材前提与禁用边界 (`asset_prerequisites` & `transfer_limits`)**：用这招必须具备什么真实图片或工程数据？什么情况下硬套会造成误导或翻车？

---

## 三、 原子化写入与校验（使用 `apply-patch`）

为防止直接编辑数千行的 `catalog.json` 导致格式损坏或遗漏历史备份，所有入库操作统一走 `scripts/library.py apply-patch`：

1. **准备单篇案例 Markdown（如有新增案例）**：
   在 `library/cases/<case_id>.md` 下按标准模板写入完整案例拆解卡。
2. **编写轻量补丁文件（如 `tmp_patch.json`）**：
   只包含本次拟新增或更新的 `sources`、`methods`、`cases`、`feedback` 条目：
   ```json
   {
     "sources": [...],
     "methods": [...],
     "cases": [...]
   }
   ```
3. **展示给用户确认后执行原子入库**：
   ```bash
   python scripts/library.py apply-patch --file tmp_patch.json --check-files
   ```
   脚本会自动完成：
   - 将当前 `catalog.json` 完整备份至 `library/history/catalog-r{旧revision}.json`；
   - 递增顶层 `revision` 并更新 `updated_at`；
   - 按 `id` 合并新增或更新记录；
   - 执行全量 `validate`（若引用缺失、页码越界或缺少必填字段，脚本自动回滚并输出具体错误）。
4. **清理临时补丁文件并汇报**：说明新增/更新了哪些记录 ID、关联页码及当前 `catalog_revision`。
