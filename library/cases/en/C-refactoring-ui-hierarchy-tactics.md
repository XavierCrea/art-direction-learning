# Refactoring UI Interface Hierarchy Tactics: 7 Visual Adjustments That Fix Cluttered Layouts Without Changing Copy

[English Case Index](../README.en.md) · [简体中文](../C-refactoring-ui-hierarchy-tactics.md) · UI Hierarchy & Visual Weight Teardown

- **Symptom (`when_stuck`)**: Feature cards, B2B specification modules, or storefront sections feel loud, dark, and cluttered—every headline is oversized, every box has a `1px` border, every button is solid primary color, icons are blown up to `64–80px`, and secondary text on colored headers looks muddy.
- **Channels**: Landing page feature grids, PDP specification cards, B2B comparison tables, and storefront UI components.

## What the Source Material Shows (`observations`)

Adam Wathan and Steve Schoger (*7 Practical Tips for Cheating at Design* & *Refactoring UI* Chapter 2, PDF p.35–64) demonstrate `7` visual hierarchy adjustments using before/after UI comparisons:

1. ***"Size isn't everything"* (`"1. Use color and weight to create hierarchy instead of size"`, Book p.38–41)**:
   - Making primary text huge (`24–36px`) and secondary text tiny creates ragged, awkward layouts. Instead, stick to **`2` font weights** (`400–500` Normal for body, `600–700` Bold for emphasis—avoiding `<400` thin weights for body text) and **`3` text color shades** (dark grey for primary, medium grey for secondary, light grey for tertiary).
2. ***"Don’t use grey text on colored backgrounds"* (Book p.44–45)**:
   - On white backgrounds, reducing saturation/lightness to grey works well; on colored backgrounds (such as a navy or brand-blue banner), grey or `white at 50% opacity` looks washed-out, muddy, and lifeless because the background hue bleeds through. Instead, **hand-pick a new color with the same hue as the background, adjusting its saturation and lightness** until it recedes cleanly.
3. ***"Emulate a light source"* & *"Offset your shadows"* (Book p.172–177)**:
   - Light comes from above. Adding a `2px` vertical offset shadow (`0 4px 6px rgba(0,0,0,0.08)`) paired with a subtle lighter top edge simulates natural overhead lighting instead of a muddy `0px`-offset glow.
4. ***"Use fewer borders"* (Book p.240–243)**:
   - Putting `1px solid` outlines around every card, row, and cell clutters the interface. Replace hard borders with **subtle box shadows**, **adjacent background tint differences** (`#FFFFFF` card on `#F8FAFC` canvas), or **extra spacing (`+16px–24px`)**.
5. ***"Everything has an intended size"* (`"5. Don’t blow up icons that are meant to be small"`, Book p.208–209)**:
   - Scaling a `16–24px` vector icon up to `64–80px` makes its strokes look chunky and amateurish. Keep the icon at `16–24px` and **enclose it inside a `48–64px` colored circular or rounded-square container**.
6. ***"Add color with accent borders"* (Book p.224–227)**:
   - Add a `3–4px` colored accent strip along the top of a card, the left edge of an alert, or under an active navigation item to inject brand polish without graphic noise.
7. ***"Semantics are secondary"* (`"7. Not every button needs a background color"`, Book p.58–63)**:
   - Style actions in a 3-tier pyramid: **Primary** (`1` solid high-contrast button per view), **Secondary** (outline or soft-tint background), and **Tertiary** (plain link-style text). Even destructive actions (`Delete`) should use low-emphasis styling when they are not the primary action on the page, escalating to a bright red solid button only inside the confirmation modal.

## How Copy and Visuals Work Together (`copy_visual_synergy`)

- **Color shades, font weights, and button tiers translate "semantic importance" directly into "eye capture order"**: Set the core numeric value or headline (`18–20px`, `700` bold, `#111827`) above its unit or timestamp (`14px`, `400` normal, `#6B7280`) so the eye reads the fact first without ballooning font sizes.
- **Same-hue high-lightness secondary copy preserves dark-banner legibility**: On a deep navy B2B banner (`#0F172A`), setting the main headline in `#FFFFFF` and the subtitle in icy blue (`#BAE6FD`) instead of `#9CA3AF` grey keeps the copy crisp and luminous.

## Reusable Visual Move (`reusable_move`)

1. **Lock a 3-Shade Text Hierarchy**: Define `Primary` (`#111827`, weight `600–700`), `Secondary` (`#4B5563`, weight `400–500`), and `Tertiary` (`#6B7280`, weight `400`).
2. **Use Same-Hue Tints on Colored Backgrounds**: On dark colored banners, derive secondary text by keeping the background's Hue (`H`) and raising Lightness (`L` to `80%–92%`).
3. **Replace Card Grids' Hard Borders**: Remove `1px` borders around feature cards; use a `#F8FAFC` section background with `#FFFFFF` cards, a `3–4px` top brand accent border, and `24px` grid gaps.
4. **Put Small Icons in Colored Containers**: Place `20–24px` feature icons inside `48×48px` soft-tinted rounded squares (`border-radius: 12px`).
5. **Enforce One Solid Primary Button Per View**: Demote secondary actions (`Download Datasheet`, `Compare Specs`) to outline or soft-fill buttons so the primary conversion CTA (`Request Quote`) stands unchallenged.

## Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)

- **Asset Prerequisite**: SVG icons drawn on a consistent `16–24px` grid; confirmed action priority (`Primary` vs. `Secondary` vs. `Tertiary`).
- **Transfer Limit**: Borderless spacing works well for feature cards and short lists, but high-density multi-row B2B specification sheets still require alternating row shading (`M-005`) or subtle horizontal rules to prevent horizontal eye-tracking drift.

## Outcome Evidence & Source

- **Evidence Type**: Side-by-side UI refactoring visual proofs (`author_assertion`).
- **Source**: Adam Wathan & Steve Schoger, *7 Practical Tips for Cheating at Design* (`S-refactoring-ui-7-tips-2018`) & *Refactoring UI* (`S-wathan-schoger-refactoring-ui-2018`, PDF p.35–64, 172–177, 208–209, 224–227, 240–243).
- **Linked Methods**: `M-007` (Color/Weight Hierarchy & Borderless Grouping), `M-008` (Action Pyramid Button Styling & Contained Small Icons).
