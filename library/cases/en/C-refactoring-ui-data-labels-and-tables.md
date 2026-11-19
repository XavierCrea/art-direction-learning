# Refactoring UI De-Labeling, Spec-Sheet Label Emphasis & Multi-Column Table Consolidation

[English Case Index](../README.en.md) · [简体中文](../C-refactoring-ui-data-labels-and-tables.md) · Data Presentation, Spec Sheets & Rich Table Teardown

- **Case ID**: `C-refactoring-ui-data-labels-and-tables`
- **Source**: `S-wathan-schoger-refactoring-ui-2018` — Adam Wathan & Steve Schoger, *Refactoring UI* (PDF p.48–53, 128–129, 244–249)
- **Case Type**: `editorial_teardown` (Before/After UI Component Refactoring)
- **Channels**: `pdp`, `spec_sheet`, `catalog`, `landing_page`, `presentation`
- **Linked Method**: `M-020` (De-Labeling, Spec-Sheet Label Emphasis & Multi-Line Rich Table Cells)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Product cards, supplier profiles, or B2B model tables mechanically display every field as `Label: Value` (`"Price: $149"`, `"Stock: 12"`, `"Role: Engineer"`), giving every piece of data equal emphasis; or a multi-column comparison table has `6–8` narrow columns that truncate text or force horizontal scrolling.

---

## 2. What the Source Material Shows (`observations`)
1. ***"Labels are a last resort"* (PDF p.48–49)**:
   - When interfaces present data blindly as `Name: Jane Doe` / `Email: jane@example.com` / `Phone: (555) 555-5555`, ***"it becomes difficult to present the data with any sort of hierarchy; every piece of data is given equal emphasis."***
   - Because email addresses, phone numbers, prices, and job titles are self-evident from their format alone, removing the labels entirely lets you differentiate fields through typography (`20px Bold` for the name, `14px Medium` primary tint for the role, `14px` muted grey for contact details).
2. ***"Combine labels and values"* vs. *"When to emphasize a label"* (PDF p.50–51)**:
   - **Rule A — Combine into a single conversational phrase**: Instead of `In stock: 12` or `Bedrooms: 3`, merge them into **`"12 left in stock"`** or **`"3 bedrooms"`** and bold the number.
   - **Rule B — Emphasize the label on technical spec sheets**: When a user is scanning an engineering datasheet or dimension table, the authors note verbatim:
     > ***"If a user is trying to find out the depth of a smartphone on an online store, they're scanning the page for words like 'depth', not '7.6mm'."***
     In spec sheets, set the **label (`Dimensions`, `Weight`, `Display`) in darker, bolder type** and set the **value (`7.6 mm`, `148 g`) in slightly lighter secondary type**—never let the label become too faint to scan.
3. ***"Separate visual hierarchy from document hierarchy"* (PDF p.52–53)**:
   - Semantic HTML tags (`<h1>`–`<h3>`) dictate document outline, not visual size. In dashboard metric cards or pricing headers, an `<h2>` section title (`"Total Revenue"`) often works best as a quiet `12–14px` uppercase label so the actual metric value (`"$48,250"`) can command visual focus.
4. ***"Right-align numbers"* (PDF p.128–129)**:
   - In any table comparing prices, currents, or dimensions with consistent decimal places, **right-aligning numeric columns** lines up the decimal points vertically so buyers can compare magnitudes (`$92.50` vs. `$1,240.00`) at a glance, using `font-variant-numeric: tabular-nums`.
5. ***"Think outside the box"* & *"Selectable cards"* (PDF p.244–249)**:
   - **Consolidating a 6-Column Table into 4 Rich Columns (PDF p.244–247)**: Instead of giving `Avatar`, `Name`, `Email`, `Role`, `Department`, and `Status` six separate cramped columns, merge non-sortable companion fields into **two-line hierarchical cells** (`Name [Bold Dark]` + `Email [Muted Grey]` in column 1; `Job Title` + `Department` in column 2) and turn plain text statuses into soft color-coded pills (`Active` in pale green fill + dark green text).
   - **Replacing Radio Buttons with Rich Selectable Cards (PDF p.248–249)**: Replace tiny browser radio buttons with rich cards containing the package name, bold price, spec badges, and a colored active border + checkmark badge when selected.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Conversational copy fusion (`"12 left in stock"`, `"200A continuous discharge"`)** frees the layout from rigid `Key: Value` forms so visual typography can spotlight the core number.
- **Two-line cell stacking (`Primary Dark Bold + Secondary Muted Grey`) and color-coded status pills** compress horizontal table width by `30%–40%` while doubling scannability.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Audit Every `Label: Value` Pair by User Scanning Intent**:
   - *Self-evident format* (model title, price, email, phone) $\rightarrow$ **Delete the label** and style by hierarchy;
   - *Highlight metric on a card* $\rightarrow$ **Combine Value + Unit/Noun** (`"4S–24S Smart BMS"`, `"≤ 15 mV balance accuracy"`) and bold the value;
   - *Multi-row technical spec sheet* $\rightarrow$ **Keep the two columns and emphasize the left-hand parameter label** (`#111827` Medium/Semibold) over the right-hand value (`#374151` Regular).
2. **Collapse Wide Comparison Tables via Two-Line Rich Cells**: Merge `Model + Part Number`, `Continuous Current + Peak Current`, or `Dimensions + Weight` into two-line cells, right-align pure numeric columns with `tabular-nums`, and render statuses/certifications as soft-tinted pills.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Clear knowledge of which columns buyers need to sort or compare vertically (never merge two independently sortable numeric metrics into the same cell if users must scan both down a column).
- **Transfer Limit**: Never delete labels from unfamiliar engineering codes (e.g., showing `"RS485 / CAN"` is self-evident to engineers, whereas a bare `"103AT-2"` without `"NTC Thermistor:"` forces buyers to guess).
