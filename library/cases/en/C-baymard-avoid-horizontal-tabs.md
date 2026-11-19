# Baymard PDP Navigation Study: Ditching Content-Hiding "Horizontal Tabs" for Vertically Expanded Sections and a Sticky ToC

[English Case Index](../README.en.md) · [简体中文](../C-baymard-avoid-horizontal-tabs.md) · Independent Usability Testing (Including B2B Electronic Components & Industrial Sites)

- **Symptom (`when_stuck`)**: To make a product page look "short and tidy," core sections like technical specifications, CAD drawings, customer reviews, or shipping policies are tucked inside non-sticky **"Horizontal Tabs"**—causing vertically scrolling buyers to overlook them completely, assume the information is missing, and leave.
- **Channels**: B2B and B2C e-commerce Product Detail Pages (`PDP`), Alibaba.com custom product descriptions, technical solution landing pages.

## What the Source Material Shows (`observations`)

- Across years of usability testing spanning general retail, DTC brands, and **B2B electronic component and industrial sites (`TE Connectivity`, `STMicroelectronics`)**, Baymard Institute consistently found that using `"Horizontal Tabs"` for main PDP sections performs poorly—yet **29%** of benchmarked sites still use them.
- **Why Horizontal Tabs Fail Visually**: Users' natural browsing instinct is **vertical scrolling**—their eyes move down the page, not sideways across a tab bar. Worse, because most horizontal tab bars are not sticky, the moment a user scrolls down to read the default first tab, the tab headers scroll completely out of the viewport.
- **Documented Test Failures (Both B2B Engineers and Consumer Shoppers)**:
  - On **TE Connectivity** (B2B electronic connectors), an electrical engineer trying to verify whether a connector had `10` or `16` contacts completely missed the `"Features"` horizontal tab at the top and abandoned the product page back to search results.
  - On **STMicroelectronics**, an engineer ready to purchase could not find how to order because the `"Sample and Buy"` option was hidden inside a top horizontal tab.
  - On mobile sites (`Crutchfield`, `Ashley Furniture`, `B&H`, `LG`), **21%+** of mobile test subjects completely overlooked reviews and specs hidden in horizontal tabs; narrow mobile screens even truncated the tab bar, forcing users to scroll several viewports back up and swipe horizontally just to discover hidden tabs.
- **High-Performing Alternatives (Evo Desktop / Lowe's Mobile)**:
  - On desktop, combining **"Vertically Expanded Sections"** with a **"Sticky Table of Contents (`Sticky ToC`)"** (as seen on Evo) lets users naturally scroll through every section in sequence or click an always-visible sticky anchor to jump directly to any module.
  - On mobile, using full-width **"Vertically Collapsed Accordions"** (as seen on Lowe's) ensures that scrolling users encounter every section heading in their vertical path and can tap to expand on demand.

## How Copy and Visuals Work Together (`copy_visual_synergy`)

- **Vertical layout flow aligns with scrolling instinct**: Stacking Overview, Feature Callouts, Technical Specifications, CAD/Certifications, FAQ, and Reviews vertically with full-width section headings guarantees that a mouse wheel alone reveals every piece of evidence.
- **A Sticky ToC bar handles rapid deep-jumping**: Pinning a compact horizontal anchor bar at the top of the viewport (`Overview | Specs | Wiring & CAD | Certifications | FAQ`) highlights the active section as the buyer scrolls.

## Reusable Visual Move (`reusable_move`)

1. **Eliminate Main Horizontal Tabs on Desktop PDPs**: Unpack descriptions, spec tables, CAD/wiring diagrams, reviews, and shipping terms into vertically stacked **Expanded Sections**, each introduced by a clear full-width heading.
2. **Add a Sticky Anchor Bar (`Sticky ToC`)**: For pages longer than 3 viewports, pin a lightweight sticky jump-bar once the user scrolls past the hero section (clicking smooth-scrolls to the section without hiding sibling sections).
3. **Use Full-Width Vertical Accordions on Mobile**: On narrow mobile viewports with long content, render each major section as a full-width vertical accordion bar (`+` / chevron icon) so users see 100% of section titles as they scroll down.
4. **The Only Exception**: Local sub-tabs are acceptable only for switching between `2–3` parallel views inside a single sub-module (provided all tab labels fit on a mobile screen without horizontal scrolling).

## Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)

- **Asset Prerequisite**: Strip out bloated promotional banners or irrelevant cross-sell carousels between core PDP sections so vertical scrolling stays brisk and focused.
- **Transfer Limit**: If an individual section is extraordinarily long (e.g., a 50-row compatibility matrix) and requires a `"Read More"` truncation, always pair it with a visible fade-out gradient and a high-contrast expand button so buyers never mistake the cutoff for the end of the data.

## Outcome Evidence & Source

- **Evidence Type**: Multi-year cross-industry usability testing (including B2B electrical engineers on `TE Connectivity` and `STMicroelectronics`, plus `29%` industry benchmark).
- **Source**: Alan Blackwood, *Avoid Using “Horizontal Tabs” for the Main Product Page Sections (29% Don’t)*, Baymard Institute, 2018-10-16, updated 2026-07-08 (`https://baymard.com/research-articles/avoid-horizontal-tabs`).
- **Linked Method**: `M-006` (Expanded Vertical Sections + Sticky ToC over Horizontal Tabs).
