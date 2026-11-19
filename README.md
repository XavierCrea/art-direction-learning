# Visual Planning & Case-Based Layout Skill (`visual-planning-learning`)

[简体中文说明](README.zh-CN.md) · [English Case & Method Index](library/README.en.md) · [中文案例与方法索引](library/README.md) · [Searchable Catalog](library/catalog.json)

`visual-planning-learning` is a portable, bilingual (`en` + `zh`) agent skill for planning, diagnosing, and structuring **product detail page (PDP) storyboards, landing page hero sections, B2B technical spec sheets/catalogs, trade-show invitations/booth graphics, and ad compositions** from verified product facts and documented visual evidence.

Instead of vague aesthetic adjectives (*"make it modern, sleek, high-tech"*), this skill routes concrete visual problems (`when_stuck`) to **28 reusable visual methods (`M-001`–`M-028`)** and **23 full-text bilingual case cards (`C-*`)**—explicitly tagging every entry's `learning_origin` (`book_canon`, `benchmark_study`, `co_dissected_teardown`, or `task_feedback`) so live user–agent comparative teardowns are clearly distinguished from static seeded books.

---

## What's Inside the Library (`catalog.json` `r10`)

| Source Category (`learning_origin`) | Reviewed Works & Field Teardowns (`15` Sources, `100%` Full Review) | Methods (`28`) & Bilingual Cases (`23` `zh` + `23` `en`) |
| :--- | :--- | :--- |
| **[Live Co-Dissected] Comparative Field Teardowns (`co_dissected_teardown`)** | **2026 New Xiaomi SU7 × Shu Qi "Capri Blue" Mall Billboards vs. Competitor Outdoor LEDs (Genesis, Voyah Taishan, Denza N9, XPeng X9, Buick, Geely, Avatr)**: 3-question inquiry chain + 6-dimensional street-photo teardown | `M-028` (`validated`) · `1` bilingual case card (`C-xiaomi-su7-2026-mall-billboard-teardown`) + `F-002` |
| **Baymard Institute UX Benchmarks (`benchmark_study`)** | `5` large-scale eye-tracking & usability studies on In-Scale images, Descriptive Callouts, Included/Optional Accessories, Spec Sheet Scannability, and Horizontal Tabs | `M-001`–`M-003`, `M-005`–`M-006` · `5` bilingual case cards (`C-baymard-*`) |
| **Marketing Examples (Harry Dry)** | `4` landing page, pricing & brand teardowns (Above-the-Fold Guide, Rows' Live Spreadsheet A/B Test & Haako Rewrite, Refactoring UI `$149` Tier & Basecamp `$99` Anchor, Tropicana `$55M` Rebrand Loss & Angostura Bitters) | `M-004`, `M-009`–`M-010` · `4` bilingual case cards (`C-me-*`) |
| **Robin Williams — *The Non-Designer's Design Book (4th Ed.)*** | Complete 258-page review: CRAP principles (*Proximity*, *Alignment*, *Repetition*, *Contrast*), 12-Part Color Wheel (*Shades/Tints*, *Value*, *Cool Recedes / Warm Advances*), and Typography (*Concord, Conflict, and Contrast*, `giraffe` vs. `GIRAFFE` word coastlines) | `M-011`–`M-015` · `3` bilingual case cards (`C-williams-*`) |
| **Josef Müller-Brockmann — *Grid systems in graphic design*** | Complete 85-page review: `1 : 1.5 : 2 : 3` progressive margins, baseline modular grids (`55 lines = 4 × 13 + 3`), `8/20/32-field` matrices, Figs. 1–4 *"Coloured areas in the grid system"*, Swiss typographic posters (*"musica viva"*), `30-field` B2B burner manual, and `170 cm` 3D booth eye-level grids | `M-016`–`M-019` · `3` bilingual case cards (`C-muller-brockmann-*`) |
| **Adam Wathan & Steve Schoger — *Refactoring UI*** | Complete 252-page book + *7 Practical Tips*: Color/weight hierarchy, same-hue dark-bg text, borderless spacing, de-labeling vs. spec-sheet label emphasis, `6`-to-`4` col rich tables, `≥25%` spacing scale, `45–75 char` measure, `100–900` HSL ramps with perceived-brightness hue rotation, flipped WCAG `4.5:1` contrast, dual shadows, and monochrome `multiply` hero contrast | `M-007`–`M-008`, `M-020`–`M-023` · `4` bilingual case cards (`C-refactoring-ui-*`) |
| **Steve Krug — *Don't Make Me Think, Revisited (3rd Ed.)*** | Complete 257-page review: First Law (*"Don't make me think!"*), 60-mph scanning/satisficing, *Billboard Design 101*, visual nesting, *"No cursor = no hover = no clue"*, 3 visual noises (**Shouting, Disorganization, Clutter**), Third Law (`103` $\rightarrow$ `34 words` pruning), `"You are here"` cues *"twice as prominent"*, 6-item **Trunk Test**, Homepage *Big Bang Theory* (`50ms`, `6–8 word` Tagline vs. Motto, *Tragedy of the Commons*), and *Reservoir of Goodwill* (**Candid FAQs** vs. `QWWPWAs`, ear-scanning) | `M-024`–`M-027` · `3` bilingual case cards (`C-krug-*`) |

---

## Quick Start & CLI Commands

Run commands from the skill root directory (`visual-planning-learning/`):

```bash
# 1. Inspect library summary and source coverage
python scripts/library.py summary

# 2. Search by visual symptom or keyword (supports English & Chinese)
python scripts/library.py search "wall of specs" --kind methods
python scripts/library.py search "billboard visual noise" --kind cases
python scripts/library.py search "in-scale size" --channel pdp

# 3. Batch-get multiple methods and cases in one call (returns both zh and en markdown paths)
python scripts/library.py get M-001 M-020 M-024 C-krug-billboard-scanning-and-visual-noise

# 4. Validate schema, cross-references, bilingual markdown files, and SHA-256 digests
python scripts/library.py validate --check-files
```

---

## Pairing with `copywriting-learning`

`visual-planning-learning` is designed to work either standalone or in tandem with `copywriting-learning`:
- **`copywriting-learning`** decides *what to say, in what sequence, and with what proof*;
- **`visual-planning-learning`** decides *what physical evidence the camera or layout shows, how items are grouped and aligned on the grid, where leader lines/captions sit, and how hierarchy guides a 60-mph scanner*.
