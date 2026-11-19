# Josef Müller-Brockmann's 8/20/32-Field Modular Grids & Baseline Alignment System

[English Case Index](../README.en.md) · [简体中文](../C-muller-brockmann-modular-grid-construction.md) · Systematic Grid Construction & Typographic Alignment Teardown

- **Case ID**: `C-muller-brockmann-modular-grid-construction`
- **Source**: `S-muller-brockmann-grid-systems` — Josef Müller-Brockmann, *Grid systems in graphic design: A visual communication manual for graphic designers, typographers and three dimensional designers* (PDF p.16–50)
- **Case Type**: `design_critique` (Systematic Grid Mathematical Derivation & Layout Examples)
- **Channels**: `catalog`, `spec_sheet`, `landing_page`, `pdp`, `print_collateral`
- **Linked Methods**: `M-016` (Baseline Modular Grid & Progressive Margin Ratios), `M-017` (8/20/32-Field Matrix, Scale Pairing & Deliberate Empty Fields)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Multi-image and text layouts (B2B catalogs, spec sheets, multi-section landing pages) look disjointed because images have arbitrary heights, captions float at inconsistent offsets, text baselines fail to align with image bottom edges, or overly wide columns and uniform page margins make reading tiring.

---

## 2. What the Source Material Shows (`observations`)
1. **Column Width & Leading Measurements (*"Width of column"* & *"Leading"*, PDF p.16–20)**:
   - At a normal reading distance of `30–35 cm`, a column width averaging **`7 to 10 words per line`** is optimal for effortless eye tracking; overly long lines make it hard to find the next line, while overly narrow columns break reading rhythm.
   - If leading (line-spacing) is too tight, the eye is distracted by the line above and below simultaneously; if too wide, lines break apart into isolated stripes.
2. **The Four Margin Proportion Experiments (*"Margin proportions"*, Figs. 1–4, PDF p.20–21)**:
   - **Fig. 1** (margins too wide) cramps the type area; **Fig. 2** (margins too narrow) leaves no room for fingers to hold the page and risks `1–3 mm` trim errors; **Fig. 3** (equal top, left, and right margins) looks static and lifeless; **Fig. 4** uses a progressive ratio of **`1 : 1.5 : 2 : 3` (`inner : top : outer : bottom`)**, providing thumb space at the foot and dynamic visual tension.
3. **Deriving Grid Fields Directly from Body Text Line-Height (*"Construction of the type area and grid"*, PDF p.28–35)**:
   - Starting from a column of `57` lines of body text divided into `4` vertical grid fields: subtracting `3` horizontal **"empty lines"** (gutters between the 4 fields) leaves `54` lines. Because `54 ÷ 4 = 13.5` (and half a line of type is impossible), the total column height is adjusted to **`55 lines` (`4 fields × 13 body lines + 3 empty-line gutters = 55 lines`)**.
   - **Cap-Height & Baseline Lock**: Every photograph, diagram, and table is cropped so its **top edge aligns flush with the cap-height of the first line of text** in that grid row, and its **bottom edge aligns flush with the baseline of the last line of text**. Captions sit `1 empty line` below the image, with caption leading scaled so subsequent body text returns seamlessly to the master baseline grid (e.g., two lines of `6pt/6pt` caption = `12pt`, matching one `10pt/12pt` body line).
4. **Evolution Across the 8-, 20-, and 32-Field Grids (*"Text and pictures in the 8-, 20- and 32-field grid"*, PDF p.36–50)**:
   - **8-Field Grid (`2 columns × 4 rows`, PDF p.36–41)**: Ideal for posters, covers, and focused single-screen modules.
   - **20-Field Grid (`4 columns × 5 rows`, PDF p.42–46)**: Places a spanning headline at the top, aligns body columns along a unified horizontal **hang-line**, and steps images across fields while preserving contiguous empty fields.
   - **32-Field Grid (`4 columns × 8 rows`, PDF p.47–50)**: Enables dramatic **scale pairing**—combining a large `2 × 3` field context photo with an adjacent `1 × 1` field macro detail shot (PDF p.49–50).

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **The baseline-derived modular grid and horizontal hang-line** lock headlines, body columns, multi-scale images, and captions into a single mathematical skeleton.
- **Multi-field spanning photos** establish spatial context, **single-field macro shots** prove material/engineering detail, and **grid-locked italic/small captions** explain each visual without disrupting body copy flow.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Lock Line-Height Before Drawing Grid Cells**: Define body font size and line-height first; set every vertical grid field to `N × body line-height` and every horizontal gutter to `1–2 × body line-height`. Never draw arbitrary pixel boxes detached from typographic leading.
2. **Align Image Top & Bottom Edges to Cap-Height & Baseline**: Crop all photos and diagrams to span an integer number of grid fields so their top and bottom edges sit flush with adjacent text lines.
3. **Pair Wide + Macro Shots & Reserve `20%–35%` Contiguous Empty Fields**: Anchor columns to a shared horizontal hang-line, pair a `2×2` or `2×3` hero image with `1×1` detail crops, and leave `20%–35%` contiguous grid fields completely empty.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Source photos and diagrams must allow cropping to modular grid aspect ratios (`1:1`, `2:1`, `2:3` fields) without cutting off critical product features.
- **Transfer Limit**: Never fill 100% of grid cells (filling every cell turns a modular grid into a suffocating classified-ad page); never force justified alignment on narrow columns with fewer than 5 words per line.
