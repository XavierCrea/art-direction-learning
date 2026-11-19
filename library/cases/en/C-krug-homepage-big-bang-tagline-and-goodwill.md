# Steve Krug's "Big Bang Theory of Web Design": The 50ms First Impression, 6–8 Word Taglines vs. Mottos, the Homepage Tragedy of the Commons, and the Reservoir of Goodwill

[English Case Index](../README.en.md) · [简体中文](../C-krug-homepage-big-bang-tagline-and-goodwill.md) · Homepage Above-the-Fold, Tagline Uniqueness & Goodwill Reservoir Teardown

- **Case ID**: `C-krug-homepage-big-bang-tagline-and-goodwill`
- **Source**: `S-krug-dmmt-3e-2014` — Steve Krug, *Don’t Make Me Think, Revisited (Third Edition)* (Chapters 7, 10, 11 & 12, PDF p.114–134, 175–202, 203–220)
- **Case Type**: `editorial_teardown` (Homepage Architecture, Tagline Analysis, Mobile Trade-Offs & Goodwill Audit)
- **Channels**: `landing_page`, `storefront`, `pdp`, `ad_banner`, `email`
- **Linked Methods**: `M-026` (Homepage "Big Bang Theory": 4-Question Clarity, 6–8 Word Differentiating Tagline & Avoiding the Tragedy of the Commons), `M-027` ("Reservoir of Goodwill" Visual Protection, Candid FAQ vs. QWWPWAs & Front-Loaded Ear-Scanning Hierarchy)

---

## 1. When Stuck (`when_stuck`)
- **Symptom**: First-time visitors stare at a homepage or B2B storefront hero for several seconds and still have to ask *"What does this company actually make or sell?"*; the tagline next to the logo is a vague corporate motto (*"Leading the future of energy innovation"*); every department demands a promotional banner on the homepage until the hero becomes an unreadable grid of competing boxes; or hidden pricing/shipping fees and fake marketing FAQs drain buyer trust before they ever send an inquiry.

---

## 2. What the Source Material Shows (`observations`)
1. ***"The Big Bang Theory of Web Design"*: `50ms` Impression & the 4 Homepage Questions (Chapter 7, PDF p.114–125)**:
   - Like the universe's Big Bang, the first few seconds on a homepage—and research showing users form a visual gut impression in the **first `50 milliseconds` (`1/20th of a second`)**—set the trajectory for everything that follows.
   - As quickly as possible, the homepage must answer **4 questions** in the visitor's head without scrolling (PDF p.118):
     1. ***"What is this?"***
     2. ***"What do they have here?"***
     3. ***"What can I do here?"***
     4. ***"Why should I be here—and not somewhere else?"***
   - Along with answering those 4 questions, the homepage must immediately expose the `3` starting action entry points: **How to Search**, **How to Browse**, and **Examples of their best stuff (Content Samples)** (PDF p.116).
   - Krug warns verbatim (PDF p.120):
     > ***"Just one thing: Don’t use a mission statement as a welcome blurb. Nobody wants to read your mission statement."***
2. **Tagline vs. Corporate Motto & Jakob Nielsen's Uniqueness Test (Chapter 7, PDF p.123–125)**:
   - A **Tagline** sits visually attached right next to or beneath the Site ID/Logo and characterizes the **entire enterprise and its specific differentiation**.
   - **Taglines are NOT Mottos**:
     - *Corporate Motto* (`"We bring good things to life"`, `"You're in good hands"`): Expresses a lofty guiding spirit or aspiration, suitable for established household brands, **not** for telling a stranger what a website or manufacturer actually does;
     - *Effective Tagline* (`"Real college. Real-world ready."`, `"Six to eight words that sum up what you do and why you're different"`): Concrete, informative, **`6–8 words` long**, and conveys clear differentiation.
   - **Jakob Nielsen's Tagline Test (PDF p.124)**: ***"If a tagline could apply equally well to another site if you just swapped the logos, it’s not specific enough."***
3. **The Homepage *"Tragedy of the Commons"* & the CBS News Mobile Anti-Pattern (Chapter 7 PDF p.129–134 & Chapter 10 PDF p.178–179)**:
   - Just as a shared village pasture is destroyed by ***"overgrazing"*** when every herder adds one more cow, a homepage is destroyed when every product line or stakeholder adds "just one more banner/widget" until visual noise drowns everything out.
   - **CBS News Mobile Failure (Chapter 10, PDF p.178–179)**: Instead of prioritizing top stories on mobile, CBS placed **8 full screens of stacked promotional carousels and department boxes above the fold**, forcing mobile visitors to swipe past `8 pages` before reaching the main news list.
4. ***"The Reservoir of Goodwill"* & Candid FAQs vs. `QWWPWAs` (Chapter 11, PDF p.203–211)**:
   - Every visitor enters a site with a finite mental **"Reservoir of Goodwill"**.
   - **6 Things That Drain It Instantly**: `1)` Hiding what the user wants (support phone numbers, shipping rates, **pricing / MOQ**); `2)` Punishing users for formatting data their way (requiring dashes or forbidding spaces in phone/part numbers); `3)` Asking for unnecessary personal/company info up front; `4)` Phony sincerity; `5)` Putting visual bloat in the way; `6)` Looking amateurish.
   - **7 Things That Fill It Back Up**: `1)` Making the top things people want to do obvious and easy; `2)` **Telling them what they want to know up front** (total costs, lead times, compatibility limits); `3)` Saving them steps wherever possible; `4)` Putting visible effort into helping them decide; `5)` **Answering real questions via a Candid FAQ**—never **`QWWPWAs` (*"Questions We Wish People Would Ask"*)** disguised as FAQs; `6)` Creature comforts like clean print/PDF views; `7)` Easy recovery from errors.
5. **Accessibility & *"Scanning with Their Ears"* (Chapter 12, PDF p.212–220)**:
   - Blind and low-vision users using screen readers **"scan with their ears"** by jumping through Heading levels (`H1` $\rightarrow$ `H2` $\rightarrow$ `H3`) and listening to only the **first few words** of each link or list item before skipping to the next.
   - Therefore, **front-loading the distinguishing keywords into the first `2–4` words of every heading, bullet, and link** helps both sighted visual scanners and screen-reader ear-scanners simultaneously.

---

## 3. How Copy and Visuals Work Together (`copy_visual_synergy`)
- **Logo + `6–8 word` concrete Tagline + Hero Title + Product-in-Action Visual + `Search / Browse / Sample` entry points** work as one unified visual frame that answers all 4 homepage questions within `3 seconds`.
- **Up-front visual transparency cards (MOQ, lead time, compatible battery chemistries, wiring pinouts) + Candid FAQs** refill the buyer's Reservoir of Goodwill before asking them to fill out an inquiry form.

---

## 4. Reusable Visual Move (`reusable_move`)
1. **Lock a `6–8 Word` Concrete Tagline Next to the Site ID**: Test it with Jakob Nielsen's Logo-Swap Test; never let a vague corporate motto or mission statement occupy the hero header.
2. **Verify the 4-Question + 3-Entry Homepage Frame**: Ensure the initial viewport answers *What is this / What do they have / What can I do / Why here* and exposes *Search / Browse / Top Product Samples*, capping above-the-fold modules at `≤ 3–4` to prevent Homepage Overgrazing.
3. **Refill the Goodwill Reservoir Visually**: Surface pricing/MOQ/lead-time ranges, compatibility matrices, and a Candid FAQ (answering real technical & commercial objections rather than `QWWPWAs`) in scannable visual cards *before* the RFQ form.
4. **Front-Load Keywords for Dual Eye/Ear Scanning**: Start every `H1–H3` heading, spec bullet, and button label with its `2–4` most distinctive words, and never begin multiple links with the same repetitive prefix (`"Click here to view..."`).

---

## 5. Asset Prerequisites & Transfer Limits (`asset_prerequisites` & `transfer_limits`)
- **Asset Prerequisite**: Verified company specialization, flagship product samples, real buyer objection logs (for Candid FAQs), and transparent commercial ranges (MOQ / sample policy / lead time).
- **Transfer Limit**: Only globally famous brands (`Nike`, `Apple`, `GE`) can afford abstract image-only homepages or 3-word philosophical mottos; B2B manufacturers, exporters, and vertical SaaS products must always prioritize **zero-thought concrete category and spec clarity** above the fold.
