# Steve Krug's Third Law ("Cut Half, Then Half Again") & the 6-Item "Trunk Test" for Page Navigation

[English Case Index](../README.en.md) · [简体中文](../C-krug-omit-words-and-trunk-test-navigation.md) · Copy Pruning (`103` to `34` Words) & Trunk Test Wayfinding Teardown

- **Case ID**: `C-krug-omit-words-and-trunk-test-navigation`
- **Source**: `S-krug-dmmt-3e-2014` — Steve Krug, *Don’t Make Me Think, Revisited (Third Edition)* (Chapters 4–6 & 13, PDF p.70–113, 224)
- **Case Type**: `editorial_teardown` (Two-Pass Word Pruning & 6-Item Trunk Test Wayfinding Audit)
- **Channels**: `landing_page`, `pdp`, `spec_sheet`, `catalog`, `storefront`
- **Linked Methods**: `M-025` (Krug's Third Law Copy Pruning & "Trunk Test" Wayfinding System)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: Pages open with self-congratulatory "Happy Talk" welcome paragraphs and long instructional blocks explaining how to use the page; users landing directly on a deep PDP or technical page from search or a shared link cannot tell what site they are on, what section they are in, or how to step up one level; or active navigation tabs look virtually identical to inactive tabs.

---

## 2. What the Source Material Shows (`observations`)
1. ***"Krug’s Second Law of Usability"* & "Brief, Timely, Unavoidable" Guidance (Chapter 4, PDF p.70–76)**:
   - Krug states verbatim:
     > ***"It doesn’t matter how many times I have to click, as long as each click is a mindless, unambiguous choice."*** (*"Three mindless, unambiguous clicks equal one click that requires thought."*)
   - When an interface genuinely needs explanation, guidance must be **1) Brief** (the smallest amount of information that will help), **2) Timely** (placed right where and when the user needs it), and **3) Unavoidable** (formatted so they can't miss it).
2. ***"Krug’s Third Law of Usability"* & the `103` $\rightarrow$ `56` $\rightarrow$ `34 Word` Pruning Proof (Chapter 5, PDF p.77–81)**:
   - Krug states his Third Law verbatim:
     > ***"Get rid of half the words on each page, then get rid of half of what’s left."***
   - Why? Cutting `75%` of filler words **1) reduces the noise level of the page**, **2) makes the remaining useful content stand out**, and **3) makes pages shorter so users see more above the fold without scrolling**.
   - **Two Prime Targets**: ***"Happy talk must die"*** (promotional filler welcoming users and praising how great the section is, containing zero hard information) and ***"Instructions must die"*** (make interfaces self-explanatory instead of writing a paragraph explaining how to use them).
   - **Real 3-Stage Survey Instruction Pruning (`67%` Reduction, PDF p.81)**:
     - *Pass 0 (`103 words`)*: A dense 5-sentence paragraph explaining questionnaire statuses, how to click the name, how to view errors, and how to re-validate.
     - *Pass 1 (`56 words`)*: Strips repetitive explanations down to 3 sentences.
     - *Pass 2 (`34 words`, final)*:
       > *"To see any errors in your survey, select the questionnaire name and click **View Errors**. If there are any errors, you’ll have to fix them before the survey can be approved and made live."*
3. **Web Navigation 101: Persistent Navigation, Page Names, `"You are here"`, Breadcrumbs & Active Tabs (Chapter 6, PDF p.83–109)**:
   - On the Web there is **no physical sense of scale, no sense of direction, and no sense of location**; users rely on visual hierarchy and ***"Page names, which are the street signs of the Web"*** (PDF p.87–95).
   - **Persistent Navigation (`5` Essential Elements, PDF p.92–97)**: Every page (except during **Forms/Checkout**, where persistent navigation should be stripped to a bare minimum of `Site ID + Help` to prevent distraction) needs: **1) Site ID** (top-left), **2) Sections** (primary navigation), **3) Utilities** (`≤ 4–5` items; move the rest to the footer), **4) A way home**, and **5) Search** (`1 input box + 1 button` labeled `"Search"` or a magnifying glass—never `"Quick Search"`, `"Keyword Search"`, or default scoped dropdowns).
   - **Every Page Needs a Name (PDF p.98–99)**: The Page Name must **1) be on every page**, **2) be in the right place** (visually framing the unique page content), **3) be the most prominent text on the page**, and **4) match the exact words the user clicked to get there**.
   - **`"You are here"` Indicators & Physical Tab Metaphor (PDF p.100–105)**: Subtle navigation highlights fail completely. Krug warns verbatim:
     > ***"If you think the cue you’re using is already sticking out like a sore thumb, make it twice as prominent."***
     Combine `2–3` visual cues (color/shade contrast + bold weight + pointer/underline). For Tabs, the **active tab must be a lighter/contrasting shade that physically connects with the content area below it by breaking the bottom border line**, while inactive tabs stay closed off behind a continuous bottom line.
   - **Breadcrumbs (`4` Best Practices, PDF p.102–103)**: Put them **at the top**, use **`>`** between levels, **bold the last item** (the current page name), and **do not make the last item a link**.
4. **The 6-Item "Trunk Test" (Chapter 6, PDF p.106–113)**:
   - Imagine you have been blindfolded, locked in the trunk of a car, driven around, and dumped onto a random deep page of a website. Holding the printed page at arm's length, you must be able to circle these **6 items within seconds**:
     1. **What site is this? (`Site ID`)**
     2. **What page am I on? (`Page name`)**
     3. **What are the major sections of this site? (`Sections`)**
     4. **What are my options at this level? (`Local navigation`)**
     5. **Where am I in the scheme of things? (`"You are here"` indicators)**
     6. **How can I search?**

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Two-pass copy pruning (`Cut 50%` $\rightarrow$ `Cut 50%`) + bolding exact button labels inside microcopy (`click View Errors`)** clears away `70%` of gray text walls so visual modules rise above the fold.
- **Exact lexical match between clicked link text and the destination `Page Name` + double-prominence `"You are here"` cues + physically connected active tabs** anchors the user's spatial mental model on every page.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Run Two-Pass Krug Pruning on Every Module**: Delete all introductory "Happy Talk" and cut instructional blocks by `50%–75%`; never put form field labels *inside* input boxes as disappearing placeholder text (Chapter 13, PDF p.224).
2. **Style Active Navigation & Tabs with Double Prominence**: Combine at least `2` visual cues (`fill/color change + bold weight + indicator bar`) for `"You are here"` states; if using tabs, remove the bottom border under the active tab so its background merges directly into the content canvas below.
3. **Run the 6-Item Trunk Test on Deep Pages**: Before shipping any PDP, spec page, or documentation view, verify at arm's length that `Site ID`, `Page Name` (matching the clicked link), `Sections`, `Local Options`, `"You are here"` state, and `Search` can all be circled in under `3 seconds`.

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Clear site information architecture (`Sections` vs. `Subsections` vs. `Utilities`) and exact incoming link labels.
- **Transfer Limit**: The **Forms Exception** (PDF p.93): on multi-step checkout, RFQ submission, or registration pages, **deliberately hide global `Sections`, `Search`, and `Utilities`**, leaving only the `Site ID` and essential step progress so users aren't lured out of the conversion funnel.
