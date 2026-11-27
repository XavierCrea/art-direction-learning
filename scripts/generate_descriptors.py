#!/usr/bin/env python3
"""Generate zero-copyright vector Descriptor Cards (descriptor.svg) for every verified style archetype.

Pure Python 3.9+ standard library. Cards visualize each archetype's verified color ramp,
typography scale, whitespace ratio, layout geometry, and lighting direction so the skill
remains visually grounded even on fresh installs without local copyrighted brand photos.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any


STYLE_SPECS: list[dict[str, Any]] = [
    {
        "id": "apple-dark-pro",
        "title": "Apple Dark Pro Theater Hardware",
        "subtitle": "Dark Dramatic Hardware · Zero Neon · Two-Step Neutral Dark",
        "bg": "#0A0A0C",
        "panel": "#141417",
        "border": "#2A2A2E",
        "ink": "#F5F5F7",
        "muted": "#86868B",
        "accent": "#0071E3",
        "palette": [
            ("#000000", "Canvas 60%"),
            ("#1D1D1F", "Alt Stage 35%"),
            ("#F5F5F7", "Primary Type"),
            ("#86868B", "Muted Prose"),
            ("#0071E3", "CTA Blue <3%"),
            ("#00D959", "Power/Stat"),
        ],
        "type_scale": [
            ("Display H1", "96px / 600 · -0.015em", 36, "#FFFFFF", 700),
            ("Section H2", "56px / 600 · -0.005em", 24, "#F5F5F7", 600),
            ("Inline Highlight Prose", "17px · Muted #86868B + Bold #FFF key phrase", 14, "#86868B", 400),
        ],
        "whitespace": "45%–60% Pure Dark Breathing Space (Hero up to 85%)",
        "lighting": "Single Overhead Spotlight Cone + Subtle Lens/Edge Specular",
        "layout_mode": "dark_spotlight_bento",
        "atomic_moves": [
            "Two-step #000000 / #1D1D1F borderless 28px cards",
            "Inline white highlight inside #86868B prose",
            "One-fact-per-tile 6-cell KPI Bento",
        ],
    },
    {
        "id": "apple-light-gallery",
        "title": "Apple Light Minimalist Gallery",
        "subtitle": "Clean Minimalist · Copy-Outside-Frame · Bold Lead-In Prose",
        "bg": "#FFFFFF",
        "panel": "#F5F5F7",
        "border": "#E5E5EA",
        "ink": "#1D1D1F",
        "muted": "#6E6E73",
        "accent": "#0071E3",
        "palette": [
            ("#FFFFFF", "Canvas 55%"),
            ("#F5F5F7", "Card Surface 40%"),
            ("#1D1D1F", "Lead Ink"),
            ("#6E6E73", "Body Gray"),
            ("#0071E3", "Action Blue"),
            ("#D4EAF6", "Hero Tint"),
        ],
        "type_scale": [
            ("Gallery Display", "80px / 600 · -0.015em", 34, "#1D1D1F", 700),
            ("Hero / H3", "48px–64px · Tight LH 1.08", 22, "#1D1D1F", 600),
            ("Bold Lead-In Prose", "17px · First sentence bold #1D1D1F + rest #6E6E73", 14, "#6E6E73", 400),
        ],
        "whitespace": "45%–55% Pure White / Cloud Gray · 128–160px Section Gaps",
        "lighting": "Overhead Diffused Softbox · Shadowless Precision Edges",
        "layout_mode": "light_frame_outside_copy",
        "atomic_moves": [
            "Copy-Outside-Frame: 0 text inside 28px hardware card",
            "Bold Lead-In Prose replaces micro subheads",
            "1px hairline vertical divider + naked KPI multiples",
        ],
    },
    {
        "id": "xiaomi-dark-flagship-hardware",
        "title": "Xiaomi Dark Flagship Black-Gold Hardware",
        "subtitle": "Dark Dramatic Hardware · Cool Silver Rim Light · Champagne Gold KPI",
        "bg": "#080808",
        "panel": "#111111",
        "border": "#2B261D",
        "ink": "#FFFFFF",
        "muted": "#999999",
        "accent": "#E0BB7D",
        "palette": [
            ("#000000", "Canvas 65%"),
            ("#0F0F0F", "Dark Card 29%"),
            ("#FFFFFF", "Headline"),
            ("#999999", "Body Gray"),
            ("#E9C993", "Gold High"),
            ("#DBB472", "Gold Accent <6%"),
        ],
        "type_scale": [
            ("Chapter Title", "67.5px · Crisp Medium Sans", 32, "#FFFFFF", 600),
            ("Section / Eyebrow", "34px White + 22px Champagne Gold Eyebrow", 20, "#E0BB7D", 600),
            ("Body & Footnote", "17px #999999 · Footnote 11px #666666", 14, "#999999", 400),
        ],
        "whitespace": "45%–55% Pure Black Stage · Copy Area <= 20%",
        "lighting": "Cool Silver Oblique Rim Light + Subtle Brushed-Stone Reflection",
        "layout_mode": "dark_split_gold_kpi",
        "atomic_moves": [
            "Borderless 3x2 Champagne-Gold test-metric matrix",
            "1px hollow gold chapter pill (Speed / Smart)",
            "Smoked-glass cutaway instead of cyber neon",
        ],
    },
    {
        "id": "xiaomi-light-luxury-studio",
        "title": "Xiaomi Light Luxury White Studio",
        "subtitle": "Clean Minimalist · Jewelry Softbox · Product-Derived Warm Gold Accent",
        "bg": "#FFFFFF",
        "panel": "#F5F5F5",
        "border": "#E8E3D9",
        "ink": "#191919",
        "muted": "#666666",
        "accent": "#B89B78",
        "palette": [
            ("#FFFFFF", "White Studio 58%"),
            ("#F5F5F5", "Soft Card 34%"),
            ("#191919", "Charcoal Ink"),
            ("#666666", "Secondary Ink"),
            ("#B89B78", "Satin Gold <8%"),
            ("#EAE3D5", "Watermark Tint"),
        ],
        "type_scale": [
            ("Studio Headline", "2.5x–3x Body · Clean Modern Sans", 30, "#191919", 600),
            ("Hero KPI Metric", "Oversized Bold #B89B78 (e.g. 9h / 38h)", 22, "#B89B78", 700),
            ("Spec Line", "Quiet #666666 + 1px Champagne Callout Hairline", 14, "#666666", 400),
        ],
        "whitespace": "40%–55% High-Key White / Pale Warm Gray",
        "lighting": "High-Key Jewelry Diffused Softbox + Soft Mirror Ground Bounce",
        "layout_mode": "light_split_watermark",
        "atomic_moves": [
            "Zero loud brand orange — derive accent from product finish",
            "Giant low-contrast watermark behind chapter portrait",
            "Mid-gray #B7B8B7 contrast swap only for water-droplet screen",
        ],
    },
    {
        "id": "luxury-tactile-editorial",
        "title": "Warm Tactile Paper & Editorial Luxury",
        "subtitle": "Warm Tactile Editorial · 45° Diagonal Order · Cotton Stock & Gold Foil",
        "bg": "#F9F4EC",
        "panel": "#F2EBE2",
        "border": "#DFD3C3",
        "ink": "#231F1D",
        "muted": "#6E6258",
        "accent": "#E27A2E",
        "palette": [
            ("#F9F4EC", "Cotton Ivory 48%"),
            ("#F2EBE2", "Warm Almond 24%"),
            ("#E27A2E", "Terracotta 16%"),
            ("#231F1D", "Espresso Ink"),
            ("#B79056", "Matte Gold Foil"),
            ("#EED5C9", "Blush Paper"),
        ],
        "type_scale": [
            ("Flared Luxury Serif", "High-Contrast Editorial Wordmark", 34, "#231F1D", 600),
            ("Wide-Tracked Meta", "SMALL CAPS · +0.12em ——— HAIRLINE", 15, "#6E6258", 600),
            ("Editorial Note", "Short poetic copy in generous >=50% cotton margin", 14, "#6E6258", 400),
        ],
        "whitespace": "50%+ Editorial Paper Breathing Space · Zero Pure #FFF/#000",
        "lighting": "Soft Sculpted Top-Side Light Casting Short Paper-Edge Shadows",
        "layout_mode": "diagonal_editorial",
        "atomic_moves": [
            "30°–45° modular diagonal still-life arrangement",
            "Physical paper thickness + crisp short contact shadow",
            "Wide-tracked uppercase footer split by long em-rule",
        ],
    },
    {
        "id": "outdoor-brutalist-technical",
        "title": "Outdoor Brutalist Hard-Light Technical",
        "subtitle": "Brutalist Hard-Light Technical · Razor Sunlight Shadow · Acid-Lime Signal",
        "bg": "#EFECE4",
        "panel": "#E3DFD5",
        "border": "#BDB9AE",
        "ink": "#0E0F10",
        "muted": "#525556",
        "accent": "#C8F135",
        "palette": [
            ("#0E0F10", "Carbon Shadow 38%"),
            ("#7A7D7E", "Raw Concrete 30%"),
            ("#EFECE4", "Warm Plaster 27%"),
            ("#FFFFFF", "Sharp White"),
            ("#C8F135", "Acid Lime <5%"),
        ],
        "type_scale": [
            ("GEOMETRIC CAPS", "Left-Aligned Sharp Sans · 1 Keyword in #C8F135", 30, "#0E0F10", 700),
            ("06 / SWISS INDEX", "Wide Tracking +0.20em · 2px Accent Rule", 16, "#525556", 600),
            ("Technical Micro", "Monospace Spec Tag in Shadow Corner", 13, "#525556", 400),
        ],
        "whitespace": "40%+ Hard Diagonal Shadow Copy Zone + 25–30% Plaster Sidebar",
        "lighting": "Unfiltered Hard Directional Sunlight · Razor-Edged Diagonal Shadows",
        "layout_mode": "brutalist_diagonal_sidebar",
        "atomic_moves": [
            "Use natural hard shadow as text field (no translucent box)",
            "25–30% warm plaster Swiss numbered sidebar (06 /)",
            "Single-verb acid-lime highlight (<5% total area)",
        ],
    },
    {
        "id": "industrial-precision-instrument",
        "title": "Precision Engineering Instrument Editorial",
        "subtitle": "Precision Engineering · 90% Lab White/Slate + 5–10% Brand Accent",
        "bg": "#FFFFFF",
        "panel": "#EEF1F5",
        "border": "#D1D9E2",
        "ink": "#1E3246",
        "muted": "#4B5563",
        "accent": "#E90029",
        "palette": [
            ("#FFFFFF", "Lab White 55%"),
            ("#EEF1F5", "Cool Lab Gray 25%"),
            ("#1E3246", "Deep Slate 12%"),
            ("#4B5563", "Spec Charcoal"),
            ("#E90029", "Ruler Red 5%"),
            ("#FFC20E", "CTA Amber 5%"),
        ],
        "type_scale": [
            ("Engineering Display", "Light/Bold Modern Sans · Crisp Precision", 30, "#1E3246", 600),
            ("INSTRUMENT FORMULA", "Condensed Uppercase Equation · Key Term Accent", 16, "#E90029", 700),
            ("Spec Bullet & Readout", "Tabular-Nums Readout (10.000000 V) · Left Aligned", 14, "#4B5563", 400),
        ],
        "whitespace": "45%–60% Clean White Frame · Strictly 5%–10% Brand Accent",
        "lighting": "Shadowless Lab White Studio OR Cool Slate-Gray Gradient Bench",
        "layout_mode": "precision_ruler_facet",
        "atomic_moves": [
            "Full-width precision ruler ticks linking lab gear -> field scene",
            "Diagonal geometric facet dividing studio photo & spec list",
            "Strictly cap brand color at 5%–10% (zero glowing neon)",
        ],
    },
]


def _render_layout_diagram(spec: dict[str, Any], x: int, y: int, w: int, h: int) -> str:
    mode = spec["layout_mode"]
    accent = spec["accent"]
    ink = spec["ink"]
    muted = spec["muted"]
    if mode == "dark_spotlight_bento":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#000000" stroke="#2D2D32"/>
        <polygon points="{x+w*0.32},{y} {x+w*0.68},{y} {x+w*0.80},{y+h*0.56} {x+w*0.20},{y+h*0.56}" fill="#FFFFFF" fill-opacity="0.09"/>
        <rect x="{x+w*0.34}" y="{y+h*0.18}" width="{w*0.32}" height="{h*0.30}" rx="10" fill="#1D1D1F" stroke="#52525B"/>
        <text x="{x+w*0.50}" y="{y+h*0.36}" text-anchor="middle" fill="#FFFFFF" font-size="12" font-weight="600">HERO STAGE</text>
        <rect x="{x+18}" y="{y+h*0.62}" width="{w*0.28}" height="{h*0.30}" rx="10" fill="#1D1D1F"/>
        <rect x="{x+18+w*0.31}" y="{y+h*0.62}" width="{w*0.28}" height="{h*0.30}" rx="10" fill="#1D1D1F"/>
        <rect x="{x+18+w*0.62}" y="{y+h*0.62}" width="{w*0.28}" height="{h*0.30}" rx="10" fill="#1D1D1F"/>
        <text x="{x+18+w*0.14}" y="{y+h*0.80}" text-anchor="middle" fill="#F5F5F7" font-size="10">1 KPI</text>
        <text x="{x+18+w*0.45}" y="{y+h*0.80}" text-anchor="middle" fill="{accent}" font-size="10">1 KPI</text>
        <text x="{x+18+w*0.76}" y="{y+h*0.80}" text-anchor="middle" fill="#00D959" font-size="10">1 KPI</text>'''
    if mode == "light_frame_outside_copy":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="#D1D5DB"/>
        <rect x="{x+24}" y="{y+18}" width="{w-48}" height="{h*0.54}" rx="18" fill="#F5F5F7"/>
        <rect x="{x+w*0.30}" y="{y+h*0.20}" width="{w*0.40}" height="{h*0.24}" rx="6" fill="#D4EAF6" stroke="#93C5FD"/>
        <text x="{x+w*0.50}" y="{y+h*0.35}" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="600">0-TEXT HARDWARE FRAME</text>
        <rect x="{x+28}" y="{y+h*0.78}" width="{w*0.34}" height="8" rx="3" fill="#1D1D1F"/>
        <rect x="{x+28+w*0.36}" y="{y+h*0.78}" width="{w*0.44}" height="8" rx="3" fill="#AEAEB2"/>
        <rect x="{x+28}" y="{y+h*0.87}" width="{w*0.72}" height="7" rx="3" fill="#C7C7CC"/>'''
    if mode == "dark_split_gold_kpi":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#000000" stroke="#332B1E"/>
        <rect x="{x+18}" y="{y+22}" width="{w*0.22}" height="18" rx="9" fill="none" stroke="{accent}" stroke-width="1.2"/>
        <text x="{x+18+w*0.11}" y="{y+35}" text-anchor="middle" fill="{accent}" font-size="9">SPEED</text>
        <rect x="{x+18}" y="{y+52}" width="{w*0.36}" height="12" rx="3" fill="#FFFFFF"/>
        <rect x="{x+18}" y="{y+72}" width="{w*0.30}" height="7" rx="2" fill="#777777"/>
        <rect x="{x+w*0.50}" y="{y+20}" width="{w*0.43}" height="{h*0.44}" rx="8" fill="#161616" stroke="#3F3F46"/>
        <line x1="{x+w*0.50}" y1="{y+20}" x2="{x+w*0.50}" y2="{y+20+h*0.44}" stroke="#D4D4D8" stroke-width="2"/>
        <text x="{x+w*0.715}" y="{y+20+h*0.24}" text-anchor="middle" fill="#D4D4D8" font-size="11">RIM-LIT UNIT</text>
        <rect x="{x+18}" y="{y+h*0.70}" width="{w-36}" height="{h*0.22}" rx="8" fill="#0F0F0F"/>
        <text x="{x+w*0.22}" y="{y+h*0.84}" text-anchor="middle" fill="{accent}" font-size="12" font-weight="700">3.6Gbps</text>
        <text x="{x+w*0.50}" y="{y+h*0.84}" text-anchor="middle" fill="{accent}" font-size="12" font-weight="700">220,000×</text>
        <text x="{x+w*0.78}" y="{y+h*0.84}" text-anchor="middle" fill="{accent}" font-size="12" font-weight="700">715 Nodes</text>'''
    if mode == "light_split_watermark":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="#E5E1D8"/>
        <text x="{x+w*0.50}" y="{y+h*0.56}" text-anchor="middle" fill="#EAE3D5" font-size="52" font-weight="700" letter-spacing="8">DESIGN</text>
        <rect x="{x+20}" y="{y+24}" width="{w*0.32}" height="11" rx="3" fill="#191919"/>
        <rect x="{x+20}" y="{y+43}" width="{w*0.26}" height="7" rx="2" fill="#888888"/>
        <circle cx="{x+w*0.72}" cy="{y+h*0.52}" r="{min(w, h)*0.22}" fill="#F5F5F5" stroke="{accent}" stroke-width="1.5"/>
        <polyline points="{x+w*0.50},{y+h*0.52} {x+w*0.42},{y+h*0.76} {x+w*0.22},{y+h*0.76}" fill="none" stroke="{accent}" stroke-width="1.2"/>
        <text x="{x+w*0.22}" y="{y+h*0.72}" fill="{accent}" font-size="11" font-weight="700">9h / 38h</text>'''
    if mode == "diagonal_editorial":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#F9F4EC" stroke="#DFD3C3"/>
        <g transform="rotate(-24 {x+w*0.55} {y+h*0.48})">
          <rect x="{x+w*0.18}" y="{y+h*0.28}" width="{w*0.30}" height="{h*0.42}" rx="4" fill="#E27A2E" fill-opacity="0.92"/>
          <rect x="{x+w*0.48}" y="{y+h*0.20}" width="{w*0.32}" height="{h*0.46}" rx="4" fill="#F2EBE2" stroke="#B79056" stroke-width="1.4"/>
        </g>
        <text x="{x+24}" y="{y+h-16}" fill="#231F1D" font-size="10" letter-spacing="2">45° DIAGONAL · COTTON &amp; FOIL</text>'''
    if mode == "brutalist_diagonal_sidebar":
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#7A7D7E" stroke="#525556"/>
        <rect x="{x}" y="{y}" width="{w*0.28}" height="{h}" rx="12" fill="#EFECE4"/>
        <text x="{x+14}" y="{y+30}" fill="#0E0F10" font-size="11" font-weight="700" letter-spacing="1.5">06 /</text>
        <rect x="{x+14}" y="{y+40}" width="26" height="3" fill="{accent}"/>
        <polygon points="{x+w*0.28},{y} {x+w*0.76},{y} {x+w*0.42},{y+h} {x+w*0.28},{y+h}" fill="#0E0F10" fill-opacity="0.92"/>
        <text x="{x+w*0.33}" y="{y+h*0.46}" fill="#FFFFFF" font-size="14" font-weight="700">HARD SHADOW</text>
        <text x="{x+w*0.33}" y="{y+h*0.58}" fill="{accent}" font-size="14" font-weight="700">COPY ZONE.</text>'''
    # precision_ruler_facet
    ticks = "".join(
        f'<line x1="{x + 14 + i * 16}" y1="{y + int(h * 0.42)}" x2="{x + 14 + i * 16}" y2="{y + int(h * 0.42) + (12 if i % 5 == 0 else 6)}" stroke="{accent}" stroke-width="1.2"/>'
        for i in range(int((w - 28) / 16))
    )
    return f'''
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="#CBD5E1"/>
    <polygon points="{x+w*0.54},{y} {x+w},{y} {x+w},{y+h} {x+w*0.42},{y+h}" fill="#EEF1F5"/>
    <line x1="{x+w*0.54}" y1="{y}" x2="{x+w*0.42}" y2="{y+h}" stroke="#1E3246" stroke-width="1.5"/>
    <line x1="{x+12}" y1="{y+h*0.42}" x2="{x+w-12}" y2="{y+h*0.42}" stroke="{accent}" stroke-width="1.4"/>
    {ticks}
    <text x="{x+20}" y="{y+34}" fill="{ink}" font-size="12" font-weight="700">LAB GEAR → FIELD</text>
    <text x="{x+20}" y="{y+h-20}" fill="{muted}" font-size="10">90% WHITE/SLATE · 5–10% ACCENT</text>
    <polygon points="{x+w-78},{y+h-28} {x+w-12},{y+h-28} {x+w-12},{y+h-10} {x+w-88},{y+h-10}" fill="#FFC20E"/>'''


def render_descriptor_svg(spec: dict[str, Any]) -> str:
    w, h = 1200, 760
    bg = spec["bg"]
    panel = spec["panel"]
    border = spec["border"]
    ink = spec["ink"]
    muted = spec["muted"]
    accent = spec["accent"]

    swatches = []
    sw_w = 172
    for idx, (hx, label) in enumerate(spec["palette"]):
        sx = 48 + idx * (sw_w + 14)
        sy = 140
        swatches.append(f'''
        <g>
          <rect x="{sx}" y="{sy}" width="{sw_w}" height="68" rx="8" fill="{hx}" stroke="{border}" stroke-width="1.2"/>
          <text x="{sx}" y="{sy+88}" fill="{ink}" font-size="14" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{hx}</text>
          <text x="{sx}" y="{sy+106}" fill="{muted}" font-size="12">{html.escape(label)}</text>
        </g>''')

    type_rows = []
    ty = 318
    for name, meta, fsize, color, weight in spec["type_scale"]:
        type_rows.append(f'''
        <text x="68" y="{ty}" fill="{color}" font-size="{fsize}" font-weight="{weight}">{html.escape(name)}</text>
        <text x="68" y="{ty + 20}" fill="{muted}" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{html.escape(meta)}</text>''')
        ty += fsize + 36

    moves = []
    my = 592
    for move in spec["atomic_moves"]:
        moves.append(
            f'<text x="68" y="{my}" fill="{ink}" font-size="14">• {html.escape(move)}</text>'
        )
        my += 26

    diagram = _render_layout_diagram(spec, 646, 304, 486, 224)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <title>Style Descriptor Card — {html.escape(spec['id'])}</title>
  <rect width="{w}" height="{h}" fill="{bg}"/>
  <g font-family="system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif">
    <!-- Header -->
    <rect x="48" y="34" width="10" height="48" rx="3" fill="{accent}"/>
    <text x="72" y="58" fill="{ink}" font-size="28" font-weight="700">{html.escape(spec['title'])}</text>
    <text x="72" y="82" fill="{muted}" font-size="14">{html.escape(spec['subtitle'])}  ·  ID: {html.escape(spec['id'])}</text>
    <text x="{w - 48}" y="58" text-anchor="end" fill="{muted}" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">ZERO-COPYRIGHT DESCRIPTOR CARD</text>
    <line x1="48" y1="104" x2="{w - 48}" y2="104" stroke="{border}" stroke-width="1"/>

    <!-- Section 1: Color Ramp -->
    <text x="48" y="128" fill="{muted}" font-size="12" font-weight="700" letter-spacing="1.4">01 / VERIFIED COLOR RAMP &amp; PROPORTION</text>
    {''.join(swatches)}

    <!-- Section 2: Left Typography & Atomic Moves -->
    <rect x="48" y="274" width="560" height="270" rx="14" fill="{panel}" stroke="{border}"/>
    <text x="68" y="296" fill="{muted}" font-size="12" font-weight="700" letter-spacing="1.4">02 / TYPOGRAPHY HIERARCHY</text>
    {''.join(type_rows)}

    <!-- Section 3: Right Layout & Lighting Wireframe -->
    <rect x="628" y="274" width="524" height="270" rx="14" fill="{panel}" stroke="{border}"/>
    <text x="646" y="296" fill="{muted}" font-size="12" font-weight="700" letter-spacing="1.4">03 / COMPOSITION WIREFRAME &amp; LIGHTING</text>
    {diagram}

    <!-- Section 4: Bottom Atomic Moves & Lighting/Whitespace -->
    <rect x="48" y="562" width="560" height="160" rx="14" fill="{panel}" stroke="{border}"/>
    <text x="68" y="580" fill="{muted}" font-size="11" font-weight="700" letter-spacing="1.4">04 / ATOMIC MOVES (L2 BORROWABLE WITHOUT FULL CLONE)</text>
    {''.join(moves)}

    <rect x="628" y="562" width="524" height="160" rx="14" fill="{panel}" stroke="{border}"/>
    <text x="648" y="584" fill="{muted}" font-size="11" font-weight="700" letter-spacing="1.4">05 / WHITESPACE &amp; LIGHT DIRECTION</text>
    <text x="648" y="616" fill="{ink}" font-size="14" font-weight="600">Whitespace:</text>
    <text x="648" y="638" fill="{muted}" font-size="13">{html.escape(spec['whitespace'])}</text>
    <text x="648" y="674" fill="{ink}" font-size="14" font-weight="600">Lighting:</text>
    <text x="648" y="696" fill="{muted}" font-size="13">{html.escape(spec['lighting'])}</text>
  </g>
</svg>
'''


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    refs_root = skill_root / "library" / "style-refs"
    written = []
    for spec in STYLE_SPECS:
        out_dir = refs_root / spec["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "descriptor.svg"
        out_file.write_text(render_descriptor_svg(spec), encoding="utf-8")
        written.append(str(out_file))
    print(f"Generated {len(written)} descriptor cards:")
    for path in written:
        print(" -", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
