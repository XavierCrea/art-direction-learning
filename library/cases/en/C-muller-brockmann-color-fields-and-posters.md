# Josef Müller-Brockmann's Color-Field Padding Experiments & Product-Free Swiss Typographic Posters

[English Case Index](../README.en.md) · [简体中文](../C-muller-brockmann-color-fields-and-posters.md) · Color-Field Anti-Cramping Proof & Swiss Poster Teardown

- **Case ID**: `C-muller-brockmann-color-fields-and-posters`
- **Source**: `S-muller-brockmann-grid-systems` — Josef Müller-Brockmann, *Grid systems in graphic design* (PDF p.50–64)
- **Case Type**: `design_critique` (4-Figure Color-Field Comparison & Exhibition Poster Teardown)
- **Channels**: `ad_banner`, `print_collateral`, `landing_page`, `presentation`
- **Linked Methods**: `M-018` (Color Field Anti-Cramping Rule: Outset Field or Inset Copy), `M-019` (Product-Free Typographic Event Poster & 170cm Booth Eye-Level Rule)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Text placed inside a colored rectangle (badge, callout card, date strip) looks cramped and cheap because the colored box edges hug the text; or an event invitation, trade show announcement, or brand poster looks like a cluttered supermarket flyer because product cutouts and spec callouts were forced into it.

---

## 2. What the Source Material Shows (`observations`)
1. **The Four-Figure Experiment on *"Coloured areas in the grid system"* (PDF p.50–51, Figs. 1–4)**:
   - **Fig. 1 (Anti-Pattern — Zero Padding)**: The red color field shares the exact same boundary as the text grid field. The letters press directly against the top, bottom, left, and right edges of the red rectangle, creating visual klaustrophobia and reducing the legibility of the first and last lines.
   - **Fig. 2 (Solution A — Text Locked to Grid, Color Field Bleeds Outward)**: The text stays strictly aligned to the master grid column, while the red color field expands outward beyond the grid boundaries (bleeding to the page edge or across the gutter), giving the typography instant breathing room.
   - **Fig. 3 (Solution B — Color Field Locked to Grid, Text Inset)**: The red color field aligns flush with the grid cell edges, while the text block inside is inset by `1 full empty line` at the top and bottom plus horizontal padding on both sides.
   - **Fig. 4 (Solution C — Multi-Field Spanning Color Plane)**: A large colored plane spans across multiple grid fields, uniting a headline, photograph, and body copy inside a single calm visual zone while preserving grid alignment.
2. **Product-Free Typographic & Geometric Event Posters (PDF p.52–64)**:
   - ***"musica viva"* Concert Poster (PDF p.54)**: Built on a `4.5 × 4` grid with zero photos of musical instruments or performers. The letters `m u s i c a` and `v i v a` are locked one letter per grid module in an asymmetric cross formation as the sole hero graphic, while concert dates, venue, and program details sit in small type below, flush-left along the exact same 4 vertical column lines.
   - ***"Der Film"* (PDF p.58) & *"Weniger Lärm"* Posters (PDF p.59)**: Use oversized reversed type on dark fields, high-contrast horizontal rules, or tilted geometric color blocks as the primary visual force, keeping logistical details strictly subordinate.
   - **Zurich Kunsthaus Exhibition Catalogs & Lecture Invitations (PDF p.52–53, 60–64)**: Every invitation makes **the exhibition title, date numerals, and hall/booth identifier themselves the visual hero**, using bold horizontal rules (`2–4pt`) and asymmetric multi-column whitespace—with zero SKU cutouts or spec tables.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **High-contrast geometric color fields, bold horizontal rules, and `4x–8x` oversized titles / dates / booth numbers** take over the role of the `"Hero Graphic"`, communicating event prestige and wayfinding in 1 second.
- **Grid-locked subordinate small type** carries the exact schedule, hall address, and speaker/company details, separated from the hero type by dramatic scale contrast (`≥ 4:1`) and deliberate empty grid fields.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Enforce the Color-Field Anti-Cramping Rule (`Outset Box` or `Inset Copy`)**: Whenever placing a colored backing behind text, either **lock the text to the grid and expand the colored box outward by `12–24px` (or full bleed)**, or **lock the colored box to the grid and inset the text by at least `1 line-height` (`padding`)**. Never let box edges hug text bounds flush (`Fig. 1`).
2. **Use Product-Free Typographic Construction for Event & Trade Show Invitations**: When designing a trade show invitation, forum poster, or brand announcement, omit isolated product cutouts and spec callouts; instead combine a `3–4 column asymmetric grid + 2–3 high-contrast color fields / reversed bands + 4x–8x oversized Booth Number & Date numerals`.
3. **Decouple Grid Skeleton from Historical Ink Colors (`F-001`)**: Borrow Müller-Brockmann's spatial grid proportions and padding rules without blindly copying 1960s two-color print inks (cream/black/vermilion); when a brand palette exists, prioritize a brand-aligned primary palette while offering an exploratory high-contrast option.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Verified event name, booth/hall number, exact date range, venue name, and brand logo/palette.
- **Transfer Limit**: Product-free typographic construction is strictly for **event invitations, brand announcements, catalog covers, and wayfinding posters** (`genre_specific`). Never apply a product-free poster layout to an **e-commerce search thumbnail (`PLP`) or Product Detail Page hero (`PDP`)**, where showing the real physical product (`M-001` / `M-004`) is mandatory.
