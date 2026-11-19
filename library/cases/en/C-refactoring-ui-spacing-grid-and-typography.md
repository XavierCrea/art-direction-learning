# Refactoring UI Non-Linear Spacing Scale, Anti-12-Column Grid Dogma & Typographic Discipline

[English Case Index](../README.en.md) · [简体中文](../C-refactoring-ui-spacing-grid-and-typography.md) · Spacing Systems, Responsive Grids & Web Typography Teardown

- **Case ID**: `C-refactoring-ui-spacing-grid-and-typography`
- **Source**: `S-wathan-schoger-refactoring-ui-2018` — Adam Wathan & Steve Schoger, *Refactoring UI* (PDF p.24–33, 65–136)
- **Case Type**: `editorial_teardown` (Spacing Scale, Grid & Typography Refactoring)
- **Channels**: `landing_page`, `pdp`, `spec_sheet`, `catalog`, `ad_banner`
- **Linked Method**: `M-021` (Non-Linear Spacing Scale ≥25% Jumps, 45–75 Char Measure & Inverse Line-Height)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Layouts feel cramped because they start with minimal padding; designers waste time debating between `120px` and `125px`; fluid 12-column grids stretch sidebars to comical widths on large monitors or crush card content on tablets; paragraphs stretch across `100+` characters per line; or mixed font sizes (`$29` + `/ month`) look misaligned when vertically centered.

---

## 2. What the Source Material Shows (`observations`)
1. ***"Choose a personality"* via Three Concrete Levers (PDF p.16–23)**:
   - Visual personality is governed by **Font Choice** (serif = classic/editorial; rounded sans = playful; neutral geometric sans = clean/technical), **Color** (blue = safe/trustworthy; gold/dark = luxury), and **Border Radius** (where the authors note verbatim: **`"using no border radius at all feels much more serious and formal"`**, small `2–4px` radius feels neutral, and large `12–9999px` radius feels playful). Never mix rounded corners with sharp `0px` corners in the same interface.
2. ***"Start with too much white space"* & the `≥25%` Non-Linear Spacing Scale (PDF p.66–73)**:
   - Defaulting to tight layouts only gives elements the bare minimum room to survive. Start with overly generous whitespace and subtract until it feels right.
   - Instead of a linear pixel scale, define a non-linear scale anchored at `16px` where **`"no two values in your scale are ever closer than about 25%"`**:
     `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px, 192px, 256px, 384px, 512px, 640px, 768px`.
3. ***"You don't have to fill the whole screen"*, *"Grids are overrated"*, & *"Relative sizing doesn't scale"* (PDF p.74–95)**:
   - If a module only needs `600–800px`, never stretch it to `1440px` just to fill the viewport; use a **two-column split layout** (`Left column: section title + summary` / `Right column: stacked cards or form`, PDF p.82–83).
   - **Don't force everything into a 12-column percentage grid**: Give sidebars (`240–320px`) and cards (`max-width: 380px`) fixed or max widths so they only shrink when the viewport gets smaller than their optimal size.
   - **Scale typography and padding non-proportionally across viewports**: A `45px` desktop headline (`2.8x` body text) must shrink to `24–28px` (`1.5x–1.75x` body text) on mobile, and card padding should tighten from `40–48px` on desktop to `20–24px` on mobile.
4. ***"Avoid ambiguous spacing"* (PDF p.96–99)**:
   - When form labels or card captions have equal spacing above and below (`margin-top == margin-bottom`), the eye cannot tell which input or image they belong to. Always make the **outer gap between groups at least `2x–3x` the inner gap** between a label and its target.
5. **Typographic Discipline: Hand-Crafted Scale, `45–75` Char Measure, Baseline Alignment & Inverse Line-Height (PDF p.102–135)**:
   - **Ditch rigid modular ratios (`4:5`, `1.618` Golden Ratio)**: Golden-ratio scales produce awkward fractional pixels (`16px, 25.88px, 41.88px`) with too few steps. Use a **hand-crafted integer scale**: `12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px, 48px, 60px, 72px` (and avoid `em` units in nested components).
   - ***"Keep your line length in check"* (`45–75 characters` / `20–35em`, PDF p.112–115)**: Even inside a `1200px` wide layout, constrain prose blocks to `max-width: 30–35em` so readers never lose track of the next line.
   - ***"Baseline, not center"* (PDF p.116–117)**: When pairing a large price or headline (`$29`, `36px`) with a small unit or action link (`/ month`, `14px`) on the same row, align them by their **text baseline (`align-items: baseline`)**, never `center`.
   - ***"Line-height is proportional"* (PDF p.118–121)**: Line-height is **directly proportional to line width** (wider columns need `1.6–1.75`; narrow card columns need `1.4–1.5`) and **inversely proportional to font size** (`14–16px` body copy needs `1.5–1.75`, whereas `36–60px` display headlines must tighten to **`1.0–1.2`** so two-line headlines don't drift apart).
   - **Letter-Spacing (`Tracking`, PDF p.132–135)**: Tighten tracking slightly (`-0.02em` to `-0.03em`) on large headlines, and widen tracking (`+0.05em` to `+0.1em`) on small `ALL-CAPS` badges/eyebrows.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Constrained `45–75 char` (`20–35em`) measure + two-column split layouts (`Left Title / Right Content`)** prevent short copy from stretching into thin, unreadable horizontal noodles on wide desktop monitors while turning left-column whitespace into a structural navigation anchor.
- **Tight `1.0–1.15` headline line-height + baseline alignment (`$149` + `USD / kit`)** binds multi-line headlines and price-unit pairs into a cohesive visual unit.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Lock the Discrete Spacing & Type Scales Up Front**: Restrict all margins, paddings, and gaps to `{4, 8, 12, 16, 24, 32, 48, 64, 96, 128}px` and all font sizes to `{12, 14, 16, 18, 20, 24, 30, 36, 48, 60}px`.
2. **Cap Paragraph Width at `20–35em` (`45–75 chars`)**: When a section container is `1100–1280px` wide, either left-align the `600px` text block or split the section into a `1/3` left heading column + `2/3` right content column.
3. **Apply Inverse Line-Height & Baseline Alignment**: Set body text to `line-height: 1.5–1.65`, large headlines (`>=30px`) to `line-height: 1.0–1.15` with `letter-spacing: -0.02em`, and mixed-size rows to `align-items: baseline`.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Defined target viewport breakpoints (Desktop vs. Mobile) and brand personality tier (`0px` sharp industrial vs. `6–8px` modern neutral vs. `16px+` consumer friendly).
- **Transfer Limit**: The `45–75 character` measure rule applies to **Latin alphabets**; for **Chinese/CJK text**, the equivalent optimal single-column measure is **`22–38 Chinese characters per line`** (`22–38em`).
