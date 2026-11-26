# 视觉知识记录约定 (Bilingual Knowledge Contract v1.2)

`catalog.json` 保存中英双语结构化索引与紧凑记录，`library/cases/*.md` 保存中文单篇深度案例拆解卡，`library/cases/en/*.md` 保存对应的英文完整案例拆解卡（保留原书英文原句引用），`library/translations.en.json` 保存全量中英案例对的 SHA-256 指纹与配对清单，`history/` 保存每次 `apply-patch` 变更前的快照。

## 顶层结构
- `schema_version = 1`
- `revision`：正整数，每次更新递增 1。
- `updated_at`：ISO 日期（`YYYY-MM-DD`）。
- 四大记录数组：`sources`、`methods`、`cases`、`feedback`。所有记录 `id` 全库唯一且稳定，更新已有记录时保留 `id` 并递增其 `version`。

## 1. sources（信源登记）
必填字段：`id`、`kind`（`book` / `web` / `research_report` / `user_material`）、`title`、`version`、`reading_status`、`reviewed_locations`、`retrieved_at`，建议同时提供中英文核阅摘要 `coverage_note` 与 `coverage_note_en`。
- `reading_status`：`registered`、`metadata_only`、`partial_review`、`full_review`。
- **书籍核验与跨环境便携约束**：`kind == "book"` 时必须记录 `pdf_pages`（正整数）。采用出版社、版权页、目录与图文完整度的复合核验：拒收 Bookey / Blinkist 等剔除原书排版图例的纯文字商业书摘，但不凭单一字眼（如正版书章节 `Summary`）误杀可用资料；仅读译本时英文提炼须标明为转述。为保证技能包跨机器可移植，外部书籍统一设 `original_availability = "citation_only"` 并省略宿主机绝对路径；若将允许分发的原件归档在库内 `sources/` 下，则记录库内相对路径 `path` 与 `sha256`。

## 证据的独立记录

检索结果里的 `evidence_profile` 分别描述来源、使用情况和效果。一条方法可以同时具备多种证据。

- `source_checked` 表示来源已有实际核阅定位。反馈记录需要已核实的定位和观察。
- `project_status` 分为 `none`、`endorsed`（认可拆解或方案）与 `adopted`（实际项目使用）。在核实的反馈记录中登记，并指明项目或记录位置。旧版已核实的编辑反馈可以支持认可。
- `audience_result` 展示证据状态。可用 `none`、`unverified`、`source_reported` 或 `verified` 表达。对应条目从 `audience_evidence` 读取结果、类型和出处。正面、负面和无明显差异都照实记录。
- `evidence_stage` 是供旧调用读取的摘要，由以上记录推导。旧库中明确保存的标签仍可校验，需要对应证据支持。试稿认可或投放方自述属于各自的证据类型。

## 2. methods（可复用视觉方法 `M-*`）
必填字段：
- `id`、`version`、`title`（中文标题）、`title_en`（英文标题）
- `tags`（中文标签数组）、`tags_en`（英文标签数组）
- `when_stuck`（中英双语结构化症状字典：`{"zh": ["中文症状..."], "en": ["English symptoms..."]}`）
- `channels`（适用载体数组，如 `["pdp", "landing_page", "ad_banner", "spec_sheet", "catalog", "storefront"]`）
- `status`（`reference` / `candidate` / `validated` / `retired`）
- `source_refs`（至少一项，指向 `sources` 中的 `source_id` 及具体页码/段落定位）
- `rule`（中文核心视觉法则）、`rule_en`（英文核心视觉法则，**如原书/原报告有经典英文原句，须在 `rule_en` 中保留原句引用**）
- `applies_when`（适用前提）
- `limits`（迁移边界与防造假禁区）
- `steps`（可执行分步指令）
- `checks`（交付前视觉体检项）
- `validation_refs`（验证反馈引用列表，`status == "validated"` 时必填且须指向 `verified == true` 的反馈）

## 3. cases（真实视觉案例与实验拆解 `C-*`）
必填字段：
- `id`、`version`、`title`、`title_en`
- `tags`、`tags_en`、`when_stuck`（`{"zh": [...], "en": [...]}`）
- `status`、`source_refs`
- `case_type`
- `markdown_path`（指向 `library/cases/<id>.md`）与 `markdown_path_en`（指向 `library/cases/en/<id>.md`，英文卡须保留原书/原报告中的原句引用）
- `observations`（原材料/原画面中客观看到的物理元素、景别、版式对比或实验统计数据）
- `copy_visual_synergy`（图字分工机制：画面演什么、文字说什么、标注引线/图注如何配合）
- `analysis`（为什么这种视觉安排能解决读者的判断障碍）
- `reusable_move`（中文可迁移视觉动作公式）、`reusable_move_en`（英文可迁移视觉动作公式，保留原书关键术语与原句）
- `asset_prerequisites`（执行该视觉动作必须具备的真实素材前提）
- `outcome_evidence` 记录证据类型、结论和核验状态。自己核验过的实测结论用 `verified`。资料方公开的结论可记 `source_reported`，保留出处。识别耗时等无公开实测的推断写在案例分析里。
- `transfer_limits`（迁移时的禁用边界）

## 4. feedback（实战反馈记录 `F-*`）
必填字段包括 `id`、`version`、`title`、`kind`、`evidence_type`、`source_locator`、`observation`、`verified` 和 `task_id`。可选 `project_status` 记录认可或实际采用。若有受众或投放试验，说明比较条件、样本口径与结果。

## 案例文件指纹

新指纹用 UTF-8 内容的 LF 换行计算。Windows CRLF、Mac LF 和 UTF-8 BOM 仅改变保存方式。实际改字仍会触发重新核对。旧库保留的原始指纹兼容读入，原始 PDF 或其他二进制信源继续按原字节核对。

## 5. CLI 工具约定 (`scripts/library.py`)
- `summary`：输出各分组数量、双语支持状态与信源阅读状态。
- `search "<query>"` 支持中英关键词和简短中文症状。返回适用前提、失效边界和 `evidence_profile`。近似匹配以相关性排序，空结果表示暂无足够匹配。
- `get <ID1> [<ID2> ...]`：支持单次传入多个 ID 批量读取，自动校验并解析 `markdown_path` 与 `markdown_path_en`。
- `validate [--check-files]`：校验 Schema、外键引用、页码范围、中英案例卡文件存在性以及 `library/translations.en.json` 的 SHA-256 指纹一致性。
- `apply-patch --file <patch.json> --check-files` 为本次更新的双语案例记录指纹，校验后写入。案例路径相对于所选资料库，兼容 `cases/...`、`library/cases/...` 和旧库中的反斜线。
