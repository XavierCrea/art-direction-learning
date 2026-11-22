# Laws of UX Zeigarnik Effect & Goal-Gradient Effect: Unfinished-Loop Swipe Tension & Progress-Cue Momentum

[English Case Index](../README.en.md) · [简体中文](../C-lawsofux-zeigarnik-and-goal-gradient.md) · Cognitive Psychology & Carousel / Multi-Step Retention

- **Symptom (`when_stuck`)**: A swipe carousel (Xiaohongshu / IG), horizontal gallery, or multi-step product selector has solid content, yet readers drop off after Slide 1 or abandon halfway because the layout creates no visual pull to keep swiping or finish.
- **Channels**: Social Swipe Carousels (Xiaohongshu / IG / TikTok Photo Mode), Multi-Step Selectors & Forms, Long PDPs.

## What the Source Material Shows (`observations`)

- **Zeigarnik Effect**:
  - Discovered in the **1920s** by Soviet psychologist **Bluma Zeigarnik**: *"People remember uncompleted or interrupted tasks better than completed tasks."* Incomplete tasks create cognitive tension that stays active in working memory until the loop is closed.
  - Key design takeaways on `lawsofux.com`: Invite completion by clearly signaling unfinished progress, open loops, and easy resumption cues.
- **Goal-Gradient Effect**:
  - Proposed by **Clark Hull (1932)** and verified in human consumer studies by **Kivetz, Urminsky, and Zheng (2006)**: *"The tendency to approach a goal increases with proximity to the goal."* Effort and completion motivation accelerate as the finish line becomes visibly closer—and giving users an artificial **"head start"** (e.g., pre-completed initial steps) boosts follow-through significantly.
  - Key design takeaways on `lawsofux.com`: Show clear visual progress indicators across multi-step journeys and lower the barrier to Step 1 so users feel immediate momentum.

## How Copy and Visuals Work Together (`copy_visual_synergy`)

- **Frame edges create physical unfinished tension**: Cross-slide connecting lines, right-edge cropped visuals, subtle directional cues, and horizontal card peeks (`15%–25%` of the next card visible) physically signal "the story continues right."
- **Step counters and progress bars create finish-line certainty**: Compact corner indicators (`01/05`, `Step 2 of 4`, `3-Step Model Picker`) eliminate uncertainty about total length and trigger acceleration as the user nears the end.

## Reusable Visual Move (`reusable_move`)

1. **Engineer an Open Visual Loop on Slide 1 & Horizontal Galleries (Zeigarnik)**:
   - Open Slide 1 with a concrete open question or numbered promise (e.g., `"3 spec traps — #2 is missed by 80% of buyers"`) paired with a **right-edge visual bleed or directional cue** that pulls the thumb to swipe;
   - In horizontal carousels (accessories, reviews, cases), expose **`15%–25%` of the next card** at the right viewport edge (`Card Peek`) instead of locking one card to 100% width.
2. **Mount Lightweight Visible Progress Cues & a Frictionless Step 1 (Goal-Gradient)**:
   - Stamp consistent slide/step indicators (`1/5 Scale` $\rightarrow$ `2/5 Teardown` $\rightarrow$ `5/5 Checklist`) in a fixed corner so readers feel the finish line approaching;
   - In multi-step configurators or lead forms, place the easiest 1-tap choice first so the progress bar immediately advances (Head Start effect).

## Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)

- **Asset Prerequisite**: Every subsequent slide or step must genuinely pay off the open loop introduced on Slide 1, within a bounded, predictable step count (typically 4–7 slides).
- **Transfer Limit**: Never manufacture hollow clickbait cliffhangers (delivering fluff on Slide 6 destroys the Goodwill Reservoir `M-027`); never disguise endless feeds as bounded progress bars.

## Outcome Evidence & Source

- **Evidence Type**: Established behavioral & cognitive psychology experiments and UX heuristics (`Usability & Cognitive Benchmark`).
- **Source**: Jon Yablonski, *Laws of UX* (`https://lawsofux.com/zeigarnik-effect/`, `https://lawsofux.com/goal-gradient-effect/`); Original studies: Bluma Zeigarnik (1920s), Clark Hull (1932), Kivetz et al. (2006).
- **Linked Method**: `M-031` (Unfinished-Loop Tension & Goal-Gradient Progress Cues).
