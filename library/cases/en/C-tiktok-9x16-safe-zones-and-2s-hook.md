# TikTok Creative Center 9:16 Safe Zones & First 2–3s Visual Hook: Pixel-Exact UI Margins & Early Product Visibility Benchmarks

[English Case Index](../README.en.md) · [简体中文](../C-tiktok-9x16-safe-zones-and-2s-hook.md) · Official Vertical Social Feed Benchmark

- **Symptom (`when_stuck`)**: Headlines, prices, or key product details on 9:16 vertical creatives (TikTok / Douyin / Reels) get covered by the right-side engagement rail or bottom caption/CTA overlay; or slow TV-style intros cause viewers to swipe away within 2 seconds with near-zero brand recall.
- **Channels**: 9:16 Vertical Social Feeds (TikTok / Douyin / Instagram Reels / YouTube Shorts).

## What the Source Material Shows (`observations`)

- **Standard `1080 × 1920 px` (9:16) In-Feed Safe Zone Pixel Specifications**:
  - **Top Margin**: Keep clear by at least **`240 px`** (~`12.5%–14%` from top) for status bar and feed tabs;
  - **Bottom Margin**: Keep clear by at least **`660 px`** (~`35%` from bottom) for account handle, captions, audio ticker, and native CTA button (expands higher with longer captions or anchor overlays);
  - **Left Margin**: Keep clear by at least **`120 px`**;
  - **Right Margin**: Keep clear by at least **`120 px`** on the upper half, expanding to **`180–300 px`** on the lower half to clear the avatar, like, comment, bookmark, and share engagement rail.
- **First 2–3 Seconds Visual Hook & Platform Lift Benchmarks**:
  - TikTok Creative Center warns against slow TV-commercial pacing: dynamic motion, a direct question, or an unmistakable visual problem must land within the **first 2 seconds** to beat the scroll reflex, and the core message/product/brand must appear within the **first 2–3 seconds**.
  - Published platform research benchmarks:
    - Showing the product clearly early drives up to a **+65% brand affinity lift**;
    - The opening window captures up to **90% of total ad recall value**;
    - **88% of TikTok users** consider audio vital to the experience, requiring synchronized voiceover/sound + on-screen safe-zone captions within the first 3 seconds.

## How Copy and Visuals Work Together (`copy_visual_synergy`)

- **The upper-middle safe frame (`y: 240–1260px`, clearing right `180–300px` lower rail) carries both the product action and short high-contrast captions** with zero UI collision.
- **Dual-channel opening (sound + kinetic safe-zone text)**: Visuals demonstrate the conflict or product in action during seconds 0–2 while concise on-screen text reinforces the hook for both sound-on (`88%`) and sound-off viewers.

## Reusable Visual Move (`reusable_move`)

1. **Lock Every 9:16 Asset to the `1080×1920` Safe-Zone Grid Before Rendering**:
   - Keep all critical text, prices, and focal subjects inside `x: 120–780px` (lower half) and `y: 240–1260px` while allowing background imagery to bleed edge-to-edge; embed this mask directly in Channel 2 (Python PIL/SVG) templates and video timelines.
2. **Kill Slow Intros—Enforce "Product & Visual Tension in Seconds 0–2"**:
   - Open directly on physical movement, problem contrast, or active product demonstration within the first 2–3 seconds instead of holding the reveal until the end.
3. **Sync Audio Hook + Safe-Zone Captions in the Opening 3 Seconds**:
   - Pair immediate voiceover/sound cues with large, readable 6–10 word captions inside the safe zone.

## Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)

- **Asset Prerequisite**: Requires platform-specific Safe Zone overlay templates (note TopView ads have a distinct 3-second zoom-in takeover margin) and real dynamic product/action footage for the opening 2 seconds.
- **Transfer Limit**: Never leave the bottom `660 px` as a dead blank bar—let background scenes bleed full-frame while keeping only critical text/subjects inside the safe zone.

## Outcome Evidence & Source

- **Evidence Type**: Official platform creative specifications & lift research (`Usability & Platform Benchmark`).
- **Source**: TikTok for Business & TikTok Creative Center (`https://ads.tiktok.com/business/creativecenter`).
- **Linked Method**: `M-033` (9:16 Vertical Safe-Zone Pixel Grid & First 2–3s Visual Hook Rule).
