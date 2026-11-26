# Steve Krug's "Billboard Design 101": Why Users Don't Read Pages, How Visual Nesting Breaks, and How to Eliminate the 3 Types of Visual Noise

[English Case Index](../../README.en.md) · [简体中文](../C-krug-billboard-scanning-and-visual-noise.md) · Scanning Behavior, Visual Nesting & Affordance Teardown

- **Case ID**: `C-krug-billboard-scanning-and-visual-noise`
- **Source**: `S-krug-dmmt-3e-2014` — Steve Krug, *Don’t Make Me Think, Revisited: A Common Sense Approach to Web Usability (Third Edition)* (Chapters 1–3 & 10, PDF p.28–69, 194–197)
- **Case Type**: `editorial_teardown` (Usability Laws, Scanning Behavior & Visual Hierarchy Teardown)
- **Channels**: `landing_page`, `pdp`, `spec_sheet`, `catalog`, `ad_banner`
- **Linked Methods**: `M-024` ("Don't Make Me Think" Billboard Design 101: Visual Nesting, Unambiguous Clickability & Eliminating the 3 Types of Visual Noise)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Designers build pages assuming buyers will methodically read every paragraph, invent clever custom labels or trendy "Flat Design" ghost elements that force users to guess what is clickable, let section headers span across unrelated sidebars or float midway between two paragraphs, or allow every badge and promotion to shout with exclamation marks and bright colors.

---

## 2. What the Source Material Shows (`observations`)
1. ***"Krug’s First Law of Usability: Don’t make me think!"* (Chapter 1, PDF p.28–38)**:
   - Every element on a page that is not ***"self-evident"*** (or at minimum ***"self-explanatory"***) puts a cognitive **question mark (`?`)** over the user's head (*"Where am I?"*, *"Where should I start?"*, *"Is that a button or a banner?"*).
   - **The Job-Site Button Continuum (PDF p.34)**:
     - `Jobs` $\rightarrow$ **Zero milliseconds of thought** (standard convention);
     - `Employment Opportunities` $\rightarrow$ Requires a fraction of a second of translation;
     - `Job-o-Rama` $\rightarrow$ Requires active decoding (*"What the heck is Job-o-Rama? Is that jobs, or a game?"*).
2. **How We *Really* Use the Web: Scan, Satisfice, and Muddle Through (Chapter 2, PDF p.39–47)**:
   - Krug contrasts ***"What Designers Build For"*** (a calm user reading left-to-right, weighing every option, and figuring out how the site works) against ***"What Users Actually Do"***:
     1. ***"Fact of life #1: We don’t read pages. We scan them."*** Users race past At **60 miles per hour** like drivers passing a highway billboard, seeing only the tiny fraction of words tied to their current task and trigger words (`Free`, `Sale`, `Datasheet`, `Spec`).
     2. ***"Fact of life #2: We don’t make optimal choices. We satisfice."*** Users pick the **first reasonable option** (`good enough`) the moment they spot a link that might lead to their goal.
     3. ***"Fact of life #3: We don’t figure out how things work. We muddle through."***
3. ***"Billboard Design 101"*: Conventions, Visual Hierarchy Flaws & `$25,000 Pyramid` Page Areas (Chapter 3, PDF p.48–69)**:
   - ***"Clarity trumps consistency"*** (PDF p.52): Follow established web conventions first; if making something slightly inconsistent makes it dramatically clearer, choose clarity.
   - **Two Common Visual Hierarchy Bugs (PDF p.54)**:
     - *Bug 1 (Over-Spanning Header)*: A section heading bar stretches all the way across a right-hand column that is **not** logically part of that section;
     - *Bug 2 (Floating Subhead)*: A subhead sits equidistant between the paragraph above and the paragraph below instead of hugging the paragraph it governs.
   - **`$25,000 Pyramid` Visual Grouping (PDF p.55)**: Within a split second, cleanly bordered or background-grouped zones let users name every region of the page (*"Things I can buy"*, *"Today's deals"*, *"Stuff about this company"*).
4. ***"No cursor = no hover = no clue"* & Flat Design Affordance Traps (Chapter 3 PDF p.56–59 & Chapter 10 PDF p.194–197)**:
   - On desktop, users often sweep the mouse looking for the cursor to turn from an arrow into a pointing finger (`hover`). On touchscreens, ***"No cursor = no hover = no clue"***.
   - **Flat Design Trap**: Stripping `3D` button bevels, shadows, and link underlines—or giving non-clickable headings the exact same color/pill styling as clickable buttons—forces users to guess what can be tapped.
5. **The Three Types of Visual Noise (Chapter 3, PDF p.60–61)**:
   - Krug states the core rule verbatim:
     > ***"Presume everything is visual noise until proven innocent."***
   - **1) Shouting**: Everything clamors for attention at once via `ALL CAPS`, exclamation marks (`!`), bright contrasting badges, and animation—when everything shouts, nothing is heard.
   - **2) Disorganization**: Elements sit off-grid with no clear visual hierarchy, looking like a ransom note.
   - **3) Clutter**: Too much stuff crammed into too little space with zero breathing room.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Conventional labels (`Specifications`, `Wiring Diagram`, `Request Quote`) + unmistakable button affordances** eliminate every cognitive `?` so scanning buyers click immediately.
- **Strict visual nesting (section headers spanning only their child columns + subheads locked closer to the paragraph below) + `3–5 word` bold lead-ins** let 60-mph scanners extract the page's structure in `2 seconds`.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Audit Every Label & Button for `0ms` Self-Evidence**: Replace internal jargon or cute labels (`Job-o-Rama`, `Power Matrix`) with standard conventions (`Jobs`, `Specifications`), and give clickable buttons a distinct shape/shadow/color never shared by static headings.
2. **Fix Both Visual Nesting Bugs**: Ensure every section header bar spans **strictly the exact width of the columns it governs**, and set every subhead's top margin to `>= 2x` its bottom margin (`margin-top >= 2x margin-bottom`).
3. **Eliminate Shouting, Disorganization, and Clutter**: Limit any viewport to **1 primary visual shout**; keep paragraphs short; use bulleted lists with `1.5x` inter-item spacing; and bold only the `2–4` most decisive trigger words per bullet.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Clear inventory of which UI elements are interactive links/buttons versus static informational badges.
- **Transfer Limit**: Bolding key phrases helps rapid scanning, but **bolding entire sentences or more than `20%` of a paragraph turns bolding itself into "Shouting" visual noise**—keep bold accents short and selective.
