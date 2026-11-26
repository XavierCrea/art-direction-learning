# Refactoring UI 9-Shade HSL Palettes, Perceived-Brightness Hue Rotation, Depth Layers & Hero Image Contrast

[English Case Index](../../README.en.md) · [简体中文](../C-refactoring-ui-hsl-color-depth-and-images.md) · Color Systems, Elevation Shadows & Image Contrast Teardown

- **Case ID**: `C-refactoring-ui-hsl-color-depth-and-images`
- **Source**: `S-wathan-schoger-refactoring-ui-2018` — Adam Wathan & Steve Schoger, *Refactoring UI* (PDF p.137–238)
- **Case Type**: `editorial_teardown` (Color Scales, Depth & Photography Contrast Refactoring)
- **Channels**: `landing_page`, `pdp`, `ad_banner`, `catalog`, `presentation`
- **Linked Methods**: `M-022` (9-Shade HSL Palettes, Perceived-Brightness Hue Rotation & Flipped Contrast), `M-023` (Top-Light Dual Shadows, Overlapping Layers & Hero Image Contrast Control)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Only having 1 brand hex code leaves you guessing alert/hover/background shades; lightening yellow or darkening blue makes the color look washed-out or dirty grey; white text on a colored badge fails WCAG contrast (`<4.5:1`); white text over a busy hero photograph disappears into bright highlights; or scaling down a `1440px` app screenshot into a `400px` card renders its `4px` text unreadable.

---

## 2. What the Source Material Shows (`observations`)
1. ***"Ditch hex for HSL"* & the `100–900` Nine-Shade Palette Architecture (PDF p.138–149)**:
   - A real UI requires **1) Greys (`8–10` shades)**, **2) Primary color(s) (`5–10` shades)**, and **3) Accent colors** (Semantic Red/Yellow/Green + feature tints), each built as a **`100–900` nine-shade scale** (`500` base, `100` lightest background tint at `L≈90%–95%`, `900` darkest text shade at `L≈15%–20%`).
   - **U-Shaped Saturation Compensation (PDF p.148–149)**: In HSL, as Lightness (`L`) approaches `10%` or `95%`, the same saturation percentage looks washed-out. You must **increase Saturation (`S`) at both the lightest (`100–200`) and darkest (`800–900`) ends** of the scale so the full ramp feels equally vibrant.
2. **RGB Perceived Brightness Formula & Hue Rotation (`3 Bright Peaks / 3 Dark Valleys`, PDF p.150–155)**:
   - Every hue has an inherent perceived brightness determined by $\sqrt{0.299r^2 + 0.587g^2 + 0.114b^2}/255$:
     - **3 Bright Peaks**: Yellow (`60°`, brightest), Cyan (`180°`), Magenta (`300°`);
     - **3 Dark Valleys**: Red (`0°`), Green (`120°`), Blue (`240°`, darkest).
   - **Hue Rotation Rule**: Instead of only changing `L` (which makes yellow look muddy brown when darkened or blue look chalky when lightened), **rotate Hue (`H`) by `≤20°–30°` toward the nearest bright peak (`60°`, `180°`, `300°`) to lighten a color, or toward the nearest dark valley (`0°`, `120°`, `240°`) to darken it** (e.g., shifting light yellow `50°` toward `60°` and dark yellow toward `35°` rich amber gold).
3. ***"Greys don't have to be grey"* & *"Flipping the contrast"* (PDF p.156–165)**:
   - Pure `0%` saturation greys feel dead and clinical. Saturate greys with `5%–15%` of **`210°` cool blue** (for crisp tech/industrial UIs) or **`40°` warm yellow-orange** (for warm editorial/consumer UIs).
   - ***"Flipping the contrast"* (PDF p.162–165)**: White text on a saturated colored badge or alert box either fails WCAG `4.5:1` contrast or forces a dark, heavy background that hijacks the whole page. Flip the contrast: use a **soft `100–200` light background tint paired with dark `800–900` text of the same hue**, easily passing WCAG `4.5:1` without visual heaviness.
4. ***"Emulate a light source"*, *"Shadows can have two parts"*, & *"Overlap elements to create layers"* (PDF p.172–197)**:
   - Combine a `1px` lighter top border/inset highlight with a **two-part shadow**: `1)` a larger, soft shadow simulating direct overhead light (`0 10px 15px -3px rgba(0,0,0,0.1)`), plus `2)` a tight, dark shadow simulating ambient occlusion right beneath the card (`0 4px 6px -2px rgba(0,0,0,0.05)`).
   - **Overlap Across Background Transitions (PDF p.192–197)**: Let a white card straddle the boundary between a dark hero banner and the light page canvas (`margin-top: -48px`). When two images overlap, add an **"invisible border"** (`2–4px` solid border matching the background color) so their edges don't clash.
5. **Hero Image Text Contrast, Partial Screenshots & Preventing Background Bleed (PDF p.200–217)**:
   - **4 Ways to Guarantee Text Contrast on Photos (PDF p.200–207)**: `1)` Semi-transparent dark/light overlay; `2)` Lower image contrast + adjust brightness; `3)` **3-Step Monochrome Colorize** (desaturate photo to grayscale $\rightarrow$ boost contrast $\rightarrow$ blend with solid brand color via `background-blend-mode: multiply`); `4)` Soft text shadow (`0 2px 15px rgba(0,0,0,0.5)`).
   - **Never Shrink Full-Screen App Screenshots by 70% (PDF p.210–213)**: Shrinking a `1440px` desktop UI into a `400px` card turns `14px` text into illegible `4px` specks. Show a **tight partial crop** of the key feature, or redraw a **simplified UI illustration** replacing tiny text with clean skeleton bars.
   - ***"Prevent background bleed"* (PDF p.216–217)**: When a white-cornered screenshot or avatar sits on a white page, add `box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1)` so its boundary stays crisp.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Flipped-contrast badges (`100` pale fill + `800` dark text)** let status tags, spec pills, and warning callouts remain effortlessly legible (`>4.5:1` contrast) without competing against the primary solid CTA button.
- **Monochrome `multiply` photo colorizing + partial screenshot cropping** ensures hero headlines stay razor-sharp over real factory/product photos while PC/App companion software screenshots remain readable on mobile cards.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Build `100–900` HSL Ramps with Hue Rotation**: Boost saturation at the `100` and `900` ends and rotate hue `15°–25°` toward `60°/180°/300°` for lighter tints and `0°/120°/240°` for darker shades; tint greys with `210°` cool blue or `40°` warm amber.
2. **Flip Contrast on All Secondary Badges & Alerts**: Use `100`-level pale fills with `800`-level dark same-hue text and a `400`-level `4px` left accent border.
3. **Apply Dual Shadows & Cross-Boundary Card Overlap**: Pair soft direct + tight ambient shadows across a 5-step elevation scale and overlap key summary cards across hero section boundaries.
4. **Crop Screenshots & Lock Photo Contrast**: Tame busy hero photos with dark gradient/multiply overlays, crop software UI screenshots to the active panel (or use simplified skeleton UI), and add a `1px` inner shadow to white-edge images.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Base brand color converted to HSL; high-resolution source photos and software screenshots.
- **Transfer Limit**: Never apply monochrome `multiply` colorizing (`#3` above) to a **product photo where true physical color accuracy is a purchase requirement** (such as apparel, cosmetics, or color-coded wiring harnesses)—use that technique strictly for atmospheric hero backgrounds, and keep product gallery shots color-accurate.
