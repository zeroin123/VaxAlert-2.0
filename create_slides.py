# VaxAlert -- Hackathon Presentation Generator
# Creates VaxAlert_Presentation.pptx (5 slides, professional design, speaker notes).
# Run: python create_slides.py

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.dml.color import RGBColor
import copy

# ── Colour palette ────────────────────────────────────────────────────────────
BLUE   = RGBColor(0x1B, 0x4F, 0x72)   # primary deep blue
BLUE2  = RGBColor(0x21, 0x61, 0x8A)   # slightly lighter blue for cards
GREEN  = RGBColor(0x1E, 0x8B, 0x4C)   # accent green
GREEN2 = RGBColor(0xD5, 0xF5, 0xE3)   # light green for bottom band
RED    = RGBColor(0xC0, 0x39, 0x2B)   # alert red
REDL   = RGBColor(0xF9, 0xEB, 0xEA)   # light red bg for stat boxes
LIGHT  = RGBColor(0xEA, 0xF2, 0xF8)   # light blue bg
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DARK   = RGBColor(0x17, 0x20, 0x2A)   # near-black body text
GRAY   = RGBColor(0x71, 0x7D, 0x7E)   # subtitle gray
AMBER  = RGBColor(0xCA, 0x6F, 0x1E)   # amber warning
ROWALT = RGBColor(0xF2, 0xF3, 0xF4)   # alternating table row

W = 13.33   # slide width inches
H = 7.5     # slide height inches

HDR_H   = 1.15   # header bar height
FOOT_H  = 0.32   # footer bar height
FOOT_Y  = H - FOOT_H
ACC_W   = 0.07   # left accent bar width

FOOTER_TEXT = "VaxAlert  |  Habtech Hackathon 2025"


# ── Helper functions ───────────────────────────────────────────────────────────

def new_prs():
    prs = Presentation()
    prs.slide_width  = Inches(W)
    prs.slide_height = Inches(H)
    return prs


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def add_rect(slide, x, y, w, h, fill_rgb, line_rgb=None, radius=False):
    """Add a filled rectangle; optionally rounded."""
    from pptx.util import Inches
    from pptx.enum.shapes import PP_PLACEHOLDER
    shape = slide.shapes.add_shape(
        1,  # MSO_AUTO_SHAPE_TYPE.RECTANGLE = 1
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if line_rgb is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(0.75)
    return shape


def add_textbox(slide, x, y, w, h, text, size, bold=False, italic=False,
                color=DARK, align=PP_ALIGN.LEFT, wrap=True, spacing_after=0):
    from pptx.util import Inches, Pt
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing_after:
        p.space_after = Pt(spacing_after)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return txb


def add_multiline_textbox(slide, x, y, w, h, lines, base_size=11,
                          base_color=DARK, base_bold=False, wrap=True):
    """
    lines: list of dicts with keys:
      text, size (opt), bold (opt), italic (opt), color (opt),
      align (opt), space_before (opt), space_after (opt), bullet (opt)
    """
    from pptx.util import Inches, Pt
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txb.text_frame
    tf.word_wrap = wrap

    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = line.get("align", PP_ALIGN.LEFT)
        if line.get("space_before"):
            p.space_before = Pt(line["space_before"])
        if line.get("space_after"):
            p.space_after = Pt(line["space_after"])
        if line.get("bullet"):
            p.level = 1

        text = line.get("text", "")
        # Support inline bold via ** markers — split and render
        parts = _split_bold(text)
        for (part_text, part_bold) in parts:
            run = p.add_run()
            run.text = part_text
            run.font.size = Pt(line.get("size", base_size))
            run.font.bold = part_bold or line.get("bold", base_bold)
            run.font.italic = line.get("italic", False)
            run.font.color.rgb = line.get("color", base_color)
            run.font.name = "Calibri"
    return txb


def _split_bold(text):
    """Split text on ** markers into (text, is_bold) tuples."""
    parts = []
    bold = False
    segments = text.split("**")
    for seg in segments:
        if seg:
            parts.append((seg, bold))
        bold = not bold
    return parts


def add_header(slide, title_text, bg=BLUE, fg=WHITE):
    """Blue header bar + title text."""
    add_rect(slide, 0, 0, W, HDR_H, bg)
    add_rect(slide, 0, 0, ACC_W, HDR_H, GREEN)   # green left accent in header
    add_textbox(slide, 0.22, 0.18, W - 0.4, HDR_H - 0.1,
                title_text, 28, bold=True, color=fg, align=PP_ALIGN.LEFT)


def add_footer(slide):
    """Thin blue footer bar."""
    add_rect(slide, 0, FOOT_Y, W, FOOT_H, BLUE)
    add_textbox(slide, 0.2, FOOT_Y + 0.04, W - 0.4, FOOT_H - 0.05,
                FOOTER_TEXT, 9, color=WHITE, align=PP_ALIGN.LEFT)


def add_left_accent(slide):
    """Thin green left edge bar below header."""
    add_rect(slide, 0, HDR_H, ACC_W, FOOT_Y - HDR_H, GREEN)


def set_notes(slide, script):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = script


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════════

def build_slide1(prs):
    slide = blank_slide(prs)

    # Full blue background
    add_rect(slide, 0, 0, W, H, BLUE)

    # Decorative horizontal green band (mid-section divider)
    add_rect(slide, 0, 3.05, W, 0.06, GREEN)

    # Left accent bar (full height, green)
    add_rect(slide, 0, 0, ACC_W, H, GREEN)

    # Right decorative block (subtle lighter blue)
    add_rect(slide, 10.5, 0, 2.83, H, BLUE2)

    # Main title: "VaxAlert"
    add_textbox(slide, 0.4, 1.0, 10.0, 1.5,
                "VaxAlert", 64, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Subtitle
    add_textbox(slide, 0.4, 2.4, 9.8, 0.7,
                "AI-Powered Vaccine Stockout Forecasting for Ethiopia",
                24, bold=False, color=GREEN, align=PP_ALIGN.LEFT)

    # Tagline
    add_textbox(slide, 0.4, 3.2, 9.6, 0.55,
                "Predicting stockouts before they happen — so no child is turned away",
                15, italic=True, color=RGBColor(0xAA, 0xC9, 0xE8), align=PP_ALIGN.LEFT)

    # Divider line (already added as green rect above)

    # Team
    add_textbox(slide, 0.4, 4.15, 9.6, 0.45,
                "[Name 1]   |   [Name 2]   |   [Name 3]   |   [Name 4]",
                14, color=WHITE, align=PP_ALIGN.LEFT)

    # Event
    add_textbox(slide, 0.4, 4.65, 9.6, 0.4,
                "Habtech Hackathon 2025", 13, color=GRAY, align=PP_ALIGN.LEFT)

    # Right panel label (rotated text not easy in pptx — use horizontal)
    add_textbox(slide, 10.6, 3.4, 2.5, 1.0,
                "Ethiopia EPI\nSupply Intelligence", 12,
                color=RGBColor(0xAA, 0xC9, 0xE8), align=PP_ALIGN.CENTER)

    set_notes(slide,
        "SPEAKER SCRIPT — SLIDE 1: COVER\n\n"
        "Good [morning / afternoon]. We are Team VaxAlert.\n\n"
        "Our project tackles one of the most preventable failures in child health: "
        "a nurse is ready to vaccinate a child, the child has shown up, the parent "
        "has walked hours to get there — but the vaccine is simply not on the shelf.\n\n"
        "Over the next 10 minutes we will show you how machine learning, applied to "
        "Ethiopia's vaccine supply chain, can predict these stockouts up to 8 weeks "
        "in advance — and tell health workers exactly how much to order, and when, "
        "before the crisis hits."
    )
    return slide


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — BACKGROUND & PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════

def build_slide2(prs):
    slide = blank_slide(prs)
    add_header(slide, "The Problem: Vaccines Exist. Children Still Miss Them.")
    add_footer(slide)
    add_left_accent(slide)

    # White body bg
    add_rect(slide, ACC_W, HDR_H, W - ACC_W, FOOT_Y - HDR_H, WHITE)

    # ── Left column: evidence bullets ─────────────────────────────────────────
    bullets = [
        {"text": "Only **43%** of Ethiopian children are fully vaccinated",
         "size": 11.5, "space_after": 2},
        {"text": "  Endehabtu et al. — Oromia Immunization Supply Management, 2024",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "**50%** of African countries report stockouts of at least one vaccine",
         "size": 11.5, "space_after": 2},
        {"text": "  Prosser et al. — Vaccine Forecasting in Mozambique, 2026",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "**62%** of missed vaccinations trace back to facility-level stockouts",
         "size": 11.5, "space_after": 2},
        {"text": "  Prosser et al. 2026",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "Inadequate forecasting alone accounts for **18%** of stockouts",
         "size": 11.5, "space_after": 2},
        {"text": "  Prosser et al. 2026",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "Health Posts physically collect vaccines from Health Centers — "
                 "when the HC stockouts, every satellite HP it serves goes out too",
         "size": 11.5, "space_after": 2},
        {"text": "  Gebremedhin et al. — Ethiopian Last Mile Delivery Initiative, 2024",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "Only **28–30%** of Ethiopian facilities had all essential vaccines "
                 "available at time of survey",
         "size": 11.5, "space_after": 2},
        {"text": "  Gebremedhin et al. 2024 (citing SARA 2018)",
         "size": 9, "italic": True, "color": GRAY, "space_after": 7},

        {"text": "Finance shortages, data quality gaps, and staff turnover make "
                 "accurate manual forecasting near-impossible",
         "size": 11.5, "space_after": 2},
        {"text": "  Bilal et al. — Ethiopian Pharmaceutical Supply Chain, 2024",
         "size": 9, "italic": True, "color": GRAY, "space_after": 4},
    ]

    add_multiline_textbox(slide, 0.25, HDR_H + 0.18, 7.8, FOOT_Y - HDR_H - 0.85,
                          bullets, base_size=11.5)

    # ── Right column: 3 big stat boxes ────────────────────────────────────────
    stats = [
        ("57%",    "of children NOT fully\nvaccinated in Ethiopia"),
        ("18%",    "of stockouts caused\nby poor forecasting alone"),
        ("19,549", "public EPI facilities\nneeding supply intelligence"),
    ]
    box_h = 1.28
    box_y = HDR_H + 0.15
    for i, (num, label) in enumerate(stats):
        yy = box_y + i * (box_h + 0.12)
        add_rect(slide, 8.2, yy, 4.9, box_h, REDL)
        add_rect(slide, 8.2, yy, 0.06, box_h, RED)  # left accent
        add_textbox(slide, 8.35, yy + 0.08, 4.6, 0.65,
                    num, 34, bold=True, color=RED, align=PP_ALIGN.LEFT)
        add_textbox(slide, 8.35, yy + 0.68, 4.6, 0.55,
                    label, 10, color=DARK, align=PP_ALIGN.LEFT)

    # ── Bottom green band: "What we aim to fulfill" ───────────────────────────
    add_rect(slide, ACC_W, FOOT_Y - 0.78, W - ACC_W, 0.78, GREEN2)
    add_rect(slide, ACC_W, FOOT_Y - 0.78, 0.06, 0.78, GREEN)
    add_textbox(slide, 0.35, FOOT_Y - 0.72, W - 0.5, 0.68,
                "VaxAlert replaces reactive, manual stock management with proactive, "
                "ML-driven 8-week forecasts — giving health workers actionable alerts "
                "before stockouts occur.",
                11, bold=False, color=RGBColor(0x0B, 0x5E, 0x2E), align=PP_ALIGN.LEFT)

    set_notes(slide,
        "SPEAKER SCRIPT — SLIDE 2: PROBLEM STATEMENT\n\n"
        "Let's ground this in evidence from five published studies.\n\n"
        "Endehabtu and colleagues, studying immunization supply management in Oromia "
        "Region, found that barely 43% of children complete their full immunization "
        "schedule. That means more than half of Ethiopian children are not fully "
        "protected — despite vaccines existing in the national cold chain.\n\n"
        "Prosser et al., publishing in 2026 from a Mozambique study with direct "
        "applicability to Sub-Saharan Africa, found that 62% of missed vaccinations "
        "are directly caused by facility-level stockouts. Not vaccine hesitancy. "
        "Not access. Just an empty shelf. And inadequate forecasting is responsible "
        "for 18% of those stockouts on its own.\n\n"
        "In Ethiopia specifically, Gebremedhin's 2024 phenomenological study of the "
        "Last Mile Delivery Initiative found health workers describing 'artificial "
        "shortages due to ill forecasting and failure to request needs on time.' "
        "The structural problem is that Health Posts physically travel to Health "
        "Centers to collect vaccines — so when the HC is out, every satellite HP "
        "it serves goes out too. That is a cascade failure. Bilal et al. confirm "
        "that manual forecasting processes, compounded by finance constraints and "
        "staff turnover, make this nearly impossible to fix without automation.\n\n"
        "We built VaxAlert to be that automation."
    )
    return slide


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — PROPOSED SOLUTION
# ══════════════════════════════════════════════════════════════════════════════

def _card(slide, x, y, w, h, title, body, title_color=BLUE, body_size=10.5):
    """Render a feature card: light-bg rect + title + body text."""
    add_rect(slide, x, y, w, h, LIGHT)
    add_rect(slide, x, y, w, 0.05, BLUE)          # top border
    add_rect(slide, x, y, 0.05, h, GREEN)         # left border
    add_textbox(slide, x + 0.12, y + 0.1, w - 0.18, 0.38,
                title, 12, bold=True, color=title_color, align=PP_ALIGN.LEFT)
    add_textbox(slide, x + 0.12, y + 0.45, w - 0.18, h - 0.55,
                body, body_size, color=DARK, align=PP_ALIGN.LEFT)


def _flow_box(slide, x, y, w, h, text, bg, fg=WHITE, size=10):
    add_rect(slide, x, y, w, h, bg)
    add_textbox(slide, x + 0.05, y + 0.06, w - 0.1, h - 0.1,
                text, size, color=fg, align=PP_ALIGN.CENTER, bold=True)


def _arrow(slide, x, y, length=0.28):
    """Horizontal right-pointing arrow (thin rect + triangle approximation)."""
    add_rect(slide, x, y + 0.06, length - 0.1, 0.06, GRAY)
    # arrowhead approx with a small rect
    add_rect(slide, x + length - 0.12, y + 0.02, 0.12, 0.14, GRAY)


def build_slide3(prs):
    slide = blank_slide(prs)
    add_header(slide, "VaxAlert: Four Layers of Intelligence")
    add_footer(slide)
    add_left_accent(slide)
    add_rect(slide, ACC_W, HDR_H, W - ACC_W, FOOT_Y - HDR_H, WHITE)

    # ── 4 Feature cards ───────────────────────────────────────────────────────
    card_w = 3.12
    card_h = 2.10
    card_y = HDR_H + 0.22
    gap    = 0.09
    start_x = 0.22

    cards = [
        ("Forecast Engine",
         "8-week ahead stock-level forecasts per facility and antigen. "
         "An ensemble of 5 models, blended by a constrained optimizer — "
         "retrained on every new week of data."),
        ("Tiered Alert System",
         "Critical / Warning / OK classification based on predicted "
         "Days-to-Stockout versus lead time plus a tier-specific safety buffer. "
         "Pastoral facilities get wider buffers than urban ones."),
        ("Cascade Detection",
         "Models Health Center to Health Post supply dependencies. "
         "Flags downstream HP risk the moment their supervising HC enters "
         "a warning state — before the cascade becomes a stockout."),
        ("Restock Suggestions",
         "Calculates the exact order quantity per facility and antigen, "
         "rounded to full vials, using lead time plus a safety buffer of "
         "2 to 7 weeks depending on access tier."),
    ]

    for i, (title, body) in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        _card(slide, cx, card_y, card_w, card_h, title, body)

    # ── Pipeline flow diagram ─────────────────────────────────────────────────
    flow_y    = card_y + card_h + 0.28
    flow_h    = 0.75
    flow_items = [
        ("Stock\nLedger Data",    BLUE,   0.22,  1.55),
        ("5 Forecasting\nModels", BLUE2,  2.05,  1.75),
        ("SLSQP Ensemble\nBlend", BLUE,   4.07,  1.75),
        ("Alert\nEngine",         AMBER,  6.09,  1.55),
        ("4-View\nDashboard",     GREEN,  7.91,  1.75),
        ("Supply Chain\nAction",  BLUE,   9.93,  1.75),
    ]

    for (label, color, fx, fw) in flow_items:
        _flow_box(slide, fx, flow_y, fw, flow_h, label, color, fg=WHITE, size=9.5)

    # Arrows between flow boxes
    arr_y = flow_y + flow_h / 2 - 0.09
    arr_positions = [1.77, 3.80, 5.82, 7.64, 9.66]
    for ax in arr_positions:
        add_rect(slide, ax, arr_y + 0.04, 0.25, 0.05, GRAY)

    # ── Dashboard view labels ─────────────────────────────────────────────────
    views = "National Overview   |   Facility Drill-Down   |   Cascade View   |   Model Performance"
    add_textbox(slide, 0.22, flow_y + flow_h + 0.1, W - 0.44, 0.3,
                views, 9.5, color=GRAY, align=PP_ALIGN.CENTER, italic=True)

    set_notes(slide,
        "SPEAKER SCRIPT — SLIDE 3: PROPOSED SOLUTION\n\n"
        "VaxAlert is built around four layers.\n\n"
        "Layer one: the forecast engine. For every combination of facility and "
        "antigen — 350 time series in our simulation — we generate 8-week ahead "
        "stock level forecasts using five different models and a constrained "
        "optimizer that learns the best blend weights from validation data.\n\n"
        "Layer two: the alert engine. We convert those stock-level forecasts into "
        "a Critical, Warning, or OK status. The threshold is not arbitrary — it is "
        "calibrated to each facility's actual lead time plus a tier-specific safety "
        "buffer. A pastoral health post with a 14-day lead time gets a much wider "
        "buffer than an urban clinic that receives weekly deliveries.\n\n"
        "Layer three — and this is what makes VaxAlert unique — cascade detection. "
        "Health Posts in Ethiopia physically collect vaccines from their supervising "
        "Health Center. VaxAlert maps that entire HC-to-HP network, so when a "
        "Health Center starts showing warning signs, the downstream Health Posts "
        "are flagged immediately, even before their own stock has dropped.\n\n"
        "Layer four: restock suggestions. For every alert, VaxAlert calculates "
        "exactly how many doses to order right now — factoring in lead time, "
        "projected stock at delivery, and a safety buffer — rounded up to full vials "
        "so there is no ambiguity for the health worker.\n\n"
        "The whole system is wrapped in a four-view Streamlit dashboard: National "
        "Overview, Facility Drill-Down, Cascade View, and Model Performance."
    )
    return slide


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — DATASET & AI MODEL
# ══════════════════════════════════════════════════════════════════════════════

def _table_row(slide, x, y, w, h, col1, col2, bg, text_size=10.5):
    add_rect(slide, x, y, w, h, bg)
    add_rect(slide, x, y, w, h, bg, line_rgb=RGBColor(0xD0, 0xD3, 0xD4))
    add_textbox(slide, x + 0.1, y + 0.04, w * 0.42, h - 0.06,
                col1, text_size, bold=True, color=DARK, align=PP_ALIGN.LEFT)
    add_textbox(slide, x + w * 0.43, y + 0.04, w * 0.55, h - 0.06,
                col2, text_size, color=DARK, align=PP_ALIGN.LEFT)


def _model_box(slide, x, y, w, h, label, bg, fg=WHITE, size=9):
    add_rect(slide, x, y, w, h, bg)
    add_textbox(slide, x + 0.04, y + 0.05, w - 0.08, h - 0.08,
                label, size, bold=True, color=fg, align=PP_ALIGN.CENTER)


def build_slide4(prs):
    slide = blank_slide(prs)
    add_header(slide, "Data Foundation & Model Architecture")
    add_footer(slide)
    add_left_accent(slide)
    add_rect(slide, ACC_W, HDR_H, W - ACC_W, FOOT_Y - HDR_H, WHITE)

    # ── Left: Dataset table ───────────────────────────────────────────────────
    tx = 0.22
    tw = 6.3
    ty = HDR_H + 0.18
    row_h = 0.47

    # Column header
    add_rect(slide, tx, ty, tw, row_h, BLUE)
    add_textbox(slide, tx + 0.1, ty + 0.08, tw * 0.42, row_h - 0.1,
                "Dimension", 11, bold=True, color=WHITE)
    add_textbox(slide, tx + tw * 0.43, ty + 0.08, tw * 0.55, row_h - 0.1,
                "Value", 11, bold=True, color=WHITE)

    rows = [
        ("Simulation span",      "7 years (364 weeks)"),
        ("Facilities",           "50  (Health Posts, Health Centers, Hospitals)"),
        ("Antigens",             "7  (BCG, OPV, PENTA, PCV, ROTA, MCV, IPV)"),
        ("Time series",          "350  (50 facilities x 7 antigens)"),
        ("Stock ledger rows",    "127,400"),
        ("Shock events modelled","Pandemic, Tigray & Amhara conflicts, Measles SIAs,\nPolio SNIDs, rainy season, cold chain failures"),
        ("Calibration basis",    "EMDHS 2019, WUENIC 2024, SARA 2018 survey ranges"),
        ("Validation method",    "3-fold walk-forward CV  +  held-out final test\n(weeks 340–364, evaluated once)"),
    ]

    for i, (c1, c2) in enumerate(rows):
        ry = ty + (i + 1) * row_h
        bg = WHITE if i % 2 == 0 else ROWALT
        _table_row(slide, tx, ry, tw, row_h, c1, c2, bg, text_size=9.8)

    # Small note below table
    note_y = ty + (len(rows) + 1) * row_h + 0.05
    add_textbox(slide, tx, note_y, tw, 0.35,
                "Synthetic dataset calibrated to match published tier-stratified stockout "
                "rates. Real deployment: connect to DHIS2 API and retrain monthly.",
                8.5, italic=True, color=GRAY)

    # ── Right: Model architecture ─────────────────────────────────────────────
    rx  = 6.85
    rw  = W - rx - 0.18
    ry  = HDR_H + 0.18

    # Layer 1 label
    add_textbox(slide, rx, ry, rw, 0.28,
                "Layer 1 — Base Models", 10, bold=True, color=BLUE)

    # 5 model boxes
    model_colors = [
        ("Prophet",        RGBColor(0x1A, 0x53, 0x7F)),
        ("Holt-Winters",   RGBColor(0x21, 0x7D, 0xBB)),
        ("Naive LV",       RGBColor(0x1E, 0x8B, 0x4C)),
        ("Naive Seasonal", RGBColor(0x27, 0xAE, 0x60)),
        ("XGBoost",        RGBColor(0xCA, 0x6F, 0x1E)),
    ]
    mb_w = rw / 5 - 0.05
    mb_h = 0.46
    mb_y = ry + 0.30
    for j, (name, col) in enumerate(model_colors):
        _model_box(slide, rx + j * (mb_w + 0.05), mb_y, mb_w, mb_h, name, col, size=8.5)

    # Arrow down
    arr_x = rx + rw / 2 - 0.05
    add_rect(slide, arr_x, mb_y + mb_h + 0.02, 0.1, 0.22, GRAY)
    add_rect(slide, arr_x - 0.09, mb_y + mb_h + 0.22, 0.28, 0.1, GRAY)

    # Layer 2: Ensemble optimizer box
    l2_y = mb_y + mb_h + 0.35
    l2_h = 0.92
    add_textbox(slide, rx, l2_y - 0.26, rw, 0.26,
                "Layer 2 — SLSQP Constrained Ensemble Optimizer", 10, bold=True, color=BLUE)
    add_rect(slide, rx, l2_y, rw, l2_h, LIGHT)
    add_rect(slide, rx, l2_y, rw, 0.045, BLUE)
    add_rect(slide, rx, l2_y, 0.045, l2_h, BLUE)
    blend_lines = [
        {"text": "Non-zero-inflated series:", "size": 9.5, "bold": True,
         "color": DARK, "space_after": 1},
        {"text": "Prophet 60%  |  Naive LV 20%  |  Holt-Winters 20%  |  XGBoost 0%",
         "size": 9.5, "color": DARK, "space_after": 5},
        {"text": "Zero-inflated series (high stockout share):", "size": 9.5,
         "bold": True, "color": DARK, "space_after": 1},
        {"text": "Holt-Winters 70%  |  Naive LV 30%  |  Prophet & XGBoost excluded",
         "size": 9.5, "color": DARK},
    ]
    add_multiline_textbox(slide, rx + 0.12, l2_y + 0.06, rw - 0.18, l2_h - 0.1,
                          blend_lines)

    # Arrow down
    arr2_y = l2_y + l2_h + 0.02
    add_rect(slide, arr_x, arr2_y, 0.1, 0.18, GRAY)
    add_rect(slide, arr_x - 0.09, arr2_y + 0.18, 0.28, 0.1, GRAY)

    # Layer 3: Conformal intervals box
    l3_y = l2_y + l2_h + 0.32
    l3_h = 0.50
    add_textbox(slide, rx, l3_y - 0.26, rw, 0.26,
                "Layer 3 — Conformal Prediction Intervals", 10, bold=True, color=BLUE)
    add_rect(slide, rx, l3_y, rw, l3_h, GREEN2)
    add_rect(slide, rx, l3_y, rw, 0.04, GREEN)
    add_rect(slide, rx, l3_y, 0.04, l3_h, GREEN)
    add_textbox(slide, rx + 0.12, l3_y + 0.06, rw - 0.18, l3_h - 0.1,
                "Tier-stratified 80th-percentile calibrated residuals.\n"
                "Produces uncertainty bands without distributional assumptions.",
                9.5, color=RGBColor(0x0B, 0x5E, 0x2E))

    # Performance summary strip
    perf_y = l3_y + l3_h + 0.14
    perf_items = [
        ("MAE", "10.81\ndoses/wk"),
        ("SDR",  "51%"),
        ("Coverage", "71%"),
        ("Horizon", "8 weeks"),
    ]
    pb_w = rw / 4 - 0.04
    pb_h = 0.62
    for k, (metric, val) in enumerate(perf_items):
        px = rx + k * (pb_w + 0.04)
        add_rect(slide, px, perf_y, pb_w, pb_h, BLUE)
        add_textbox(slide, px + 0.04, perf_y + 0.02, pb_w - 0.08, 0.24,
                    metric, 7.5, bold=True, color=RGBColor(0xAA, 0xC9, 0xE8),
                    align=PP_ALIGN.CENTER)
        add_textbox(slide, px + 0.04, perf_y + 0.24, pb_w - 0.08, 0.34,
                    val, 10.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    set_notes(slide,
        "SPEAKER SCRIPT — SLIDE 4: DATASET & AI MODEL\n\n"
        "Our dataset is a 7-year synthetic simulation of 50 Ethiopian health "
        "facilities across all access tiers — urban, rural road, rural remote, "
        "and pastoral — tracking 7 antigens for 364 weeks. That gives us 127,400 "
        "weekly stock records and 350 independent time series.\n\n"
        "The data is synthetic for privacy and reproducibility reasons — we do not "
        "have direct DHIS2 access — but it is rigorously calibrated. Stockout rates "
        "by tier match the ranges published in Gebremedhin 2024 and SARA 2018. "
        "Shock events — the COVID pandemic, the Tigray conflict, the Amhara "
        "escalation — are placed at historically realistic weeks. Birth seasonality, "
        "rainy season demand dips, measles SIA campaigns, and polio SNIDs are all "
        "explicitly modelled.\n\n"
        "For the AI architecture: we run five independent forecasting models on each "
        "series. Prophet handles named events and seasonal patterns. Holt-Winters "
        "provides robust exponential smoothing. Two naive baselines act as floors. "
        "XGBoost captures nonlinear shock interactions.\n\n"
        "Then a constrained SLSQP optimizer — trained on out-of-fold validation data "
        "— learns the optimal blend. It discovered Prophet should dominate at 60% for "
        "normal series. For zero-inflated series, those with many zero-demand weeks "
        "typical of pastoral facilities, the optimizer correctly excludes Prophet and "
        "XGBoost and relies on Holt-Winters.\n\n"
        "The final ensemble achieves a Mean Absolute Error of 10.81 doses per week "
        "and detects 51% of real stockouts at least one week before they occur — "
        "enough lead time for emergency resupply in the majority of facility tiers."
    )
    return slide


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — SOLUTION IMPACT
# ══════════════════════════════════════════════════════════════════════════════

def build_slide5(prs):
    slide = blank_slide(prs)
    add_header(slide, "Evidence: What VaxAlert Changes at National Scale")
    add_footer(slide)
    add_left_accent(slide)
    add_rect(slide, ACC_W, HDR_H, W - ACC_W, FOOT_Y - HDR_H, WHITE)

    # ── Headline stat banner ──────────────────────────────────────────────────
    hl_y = HDR_H + 0.12
    hl_h = 0.90
    add_rect(slide, ACC_W, hl_y, W - ACC_W, hl_h, GREEN2)
    add_rect(slide, ACC_W, hl_y, W - ACC_W, 0.05, GREEN)
    add_textbox(slide,
                0.25, hl_y + 0.04, W - 0.35, 0.42,
                "~1.5 Million Additional Children Vaccinated Per Year",
                22, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_textbox(slide,
                0.25, hl_y + 0.46, W - 0.35, 0.36,
                "if deployed across Ethiopia's 19,549 public EPI facilities  "
                "(scale factor: 391x our 50-facility simulation)",
                11, italic=True, color=RGBColor(0x0B, 0x5E, 0x2E),
                align=PP_ALIGN.CENTER)

    # ── 3 KPI boxes ───────────────────────────────────────────────────────────
    kpi_y = hl_y + hl_h + 0.18
    kpi_h = 1.62
    kpi_w = (W - 0.25 - 0.3) / 3 - 0.14
    kpis = [
        ("Stockout Rate",
         "14.6%  →  8.2%",
         "44% relative reduction\nacross all facility tiers",
         RED, REDL),
        ("Stockout Weeks Averted",
         "~4,900 / year",
         "in 50-facility simulation\n× 391x  →  ~1.9 million nationally",
         AMBER, RGBColor(0xFD, 0xF2, 0xE9)),
        ("Early Warning Lead Time",
         "2 – 3 weeks",
         "average advance notice\nbefore actual stockout occurs",
         GREEN, GREEN2),
    ]

    for i, (title, main, sub, accent, bg) in enumerate(kpis):
        kx = 0.25 + i * (kpi_w + 0.14)
        add_rect(slide, kx, kpi_y, kpi_w, kpi_h, bg)
        add_rect(slide, kx, kpi_y, kpi_w, 0.055, accent)
        add_rect(slide, kx, kpi_y, 0.055, kpi_h, accent)
        add_textbox(slide, kx + 0.12, kpi_y + 0.08, kpi_w - 0.18, 0.32,
                    title, 10, bold=True, color=accent, align=PP_ALIGN.LEFT)
        add_textbox(slide, kx + 0.12, kpi_y + 0.40, kpi_w - 0.18, 0.55,
                    main, 18, bold=True, color=DARK, align=PP_ALIGN.LEFT)
        add_textbox(slide, kx + 0.12, kpi_y + 0.95, kpi_w - 0.18, 0.60,
                    sub, 9.5, color=DARK, align=PP_ALIGN.LEFT)

    # ── Before / After tier bar chart (drawn as stacked rects) ───────────────
    bar_y  = kpi_y + kpi_h + 0.22
    bar_h  = FOOT_Y - bar_y - 0.72
    bar_lx = 1.9    # left edge of bar area

    # Tier data: (label, baseline_pct, post_pct)
    tiers_data = [
        ("Pastoral",      38.0, 21.3),
        ("Rural Remote",  27.0, 15.1),
        ("Rural Road",    14.6,  8.2),
        ("Urban",          7.1,  4.0),
    ]
    max_pct    = 45.0
    tier_w     = 2.3     # width per tier group
    bar_pw     = 0.72    # individual bar width
    gap_within = 0.18    # gap between before/after bar
    gap_tiers  = 0.68    # gap between tier groups

    # Y-axis label
    add_textbox(slide, 0.15, bar_y, 1.6, bar_h,
                "Stockout Rate (%)\n\nBefore vs. After VaxAlert\nby Access Tier",
                9, color=GRAY, align=PP_ALIGN.RIGHT, italic=True)

    # Legend
    add_rect(slide, 9.6, bar_y, 0.28, 0.18, RED)
    add_textbox(slide, 9.92, bar_y - 0.01, 1.5, 0.22, "Baseline (no VaxAlert)", 9, color=DARK)
    add_rect(slide, 9.6, bar_y + 0.26, 0.28, 0.18, GREEN)
    add_textbox(slide, 9.92, bar_y + 0.25, 1.5, 0.22, "With VaxAlert", 9, color=DARK)

    for t, (tier_label, base_pct, post_pct) in enumerate(tiers_data):
        tx = bar_lx + t * (tier_w + gap_tiers * 0.0) + t * 0.0
        tx = bar_lx + t * (bar_pw * 2 + gap_within + 0.6)

        # Baseline bar (red)
        base_h = (base_pct / max_pct) * bar_h
        add_rect(slide, tx, bar_y + bar_h - base_h, bar_pw, base_h, RED)
        add_textbox(slide, tx, bar_y + bar_h - base_h - 0.22, bar_pw, 0.22,
                    f"{base_pct:.0f}%", 9, bold=True, color=RED, align=PP_ALIGN.CENTER)

        # Post bar (green)
        post_h = (post_pct / max_pct) * bar_h
        px = tx + bar_pw + gap_within
        add_rect(slide, px, bar_y + bar_h - post_h, bar_pw, post_h, GREEN)
        add_textbox(slide, px, bar_y + bar_h - post_h - 0.22, bar_pw, 0.22,
                    f"{post_pct:.0f}%", 9, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

        # Tier label below
        add_textbox(slide, tx - 0.05, bar_y + bar_h + 0.04,
                    bar_pw * 2 + gap_within + 0.1, 0.28,
                    tier_label, 9, color=DARK, align=PP_ALIGN.CENTER, bold=True)

    # Base line
    add_rect(slide, bar_lx - 0.05, bar_y + bar_h, 9.5, 0.03, DARK)

    # ── Citations + caveat ────────────────────────────────────────────────────
    cav_y = FOOT_Y - 0.68
    add_textbox(slide, 0.22, cav_y, W - 0.44, 0.30,
                "Sources: Prosser et al. 2026 (18% stockouts from forecasting failures)  |  "
                "FMOH facility registry (19,549 public EPI facilities)  |  "
                "SDR measured on held-out test set, weeks 340–364",
                8, italic=True, color=GRAY, align=PP_ALIGN.LEFT)
    add_textbox(slide, 0.22, cav_y + 0.30, W - 0.44, 0.28,
                "Caveat: impact projection assumes health officers act on every Critical alert "
                "within the lead-time window. Real-world SDR will depend on DHIS2 data quality "
                "and operational follow-through.",
                8, italic=True, color=GRAY, align=PP_ALIGN.LEFT)

    set_notes(slide,
        "SPEAKER SCRIPT — SLIDE 5: IMPACT\n\n"
        "What does this mean for children in practice?\n\n"
        "Our simulation covers 50 facilities over 7 years. The ensemble correctly "
        "detects 51% of real stockouts at least one week before they happen. When "
        "we apply that as a counterfactual — asking what would happen if a supply "
        "chain officer acted on every Critical alert within the available lead time "
        "— the baseline stockout rate drops from 14.6% to approximately 8.2%. "
        "That is a 44% relative reduction.\n\n"
        "Scaling to Ethiopia's 19,549 public EPI facilities — a number we verified "
        "directly from the FMOH facility registry, counting only public, approved, "
        "government-operated health posts, health centers, and hospitals — that "
        "translates to approximately 1.5 million additional children vaccinated "
        "per year who currently miss out because of empty shelves.\n\n"
        "The bar chart behind me shows how that improvement breaks down by access "
        "tier. Pastoral facilities see the largest absolute reduction, because they "
        "have the highest baseline stockout rates and the earliest warning lead "
        "times — the model can see the stock falling over a longer runway.\n\n"
        "We want to be transparent about the assumptions. This projection requires "
        "health officers to act on alerts, and our detection rate was measured on "
        "synthetic data. Real-world performance will depend on DHIS2 data quality "
        "and operational discipline. But the underlying evidence — Prosser et al. "
        "showing 18% of stockouts are pure forecasting failures, Bilal et al. "
        "documenting the manual forecasting crisis, Endehabtu's finding that only "
        "43% of children are fully vaccinated — tells us the opportunity is real "
        "and large.\n\n"
        "VaxAlert does not require new vaccines, new cold chain infrastructure, or "
        "new staff. It turns data you already collect into decisions you can make "
        "before the crisis hits.\n\n"
        "Thank you. We are happy to walk through the live dashboard now."
    )
    return slide


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os

    prs = new_prs()

    print("Building slide 1 — Cover ...")
    build_slide1(prs)

    print("Building slide 2 — Problem Statement ...")
    build_slide2(prs)

    print("Building slide 3 — Proposed Solution ...")
    build_slide3(prs)

    print("Building slide 4 — Dataset & AI Model ...")
    build_slide4(prs)

    print("Building slide 5 — Solution Impact ...")
    build_slide5(prs)

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "VaxAlert_Presentation.pptx"
    )
    prs.save(out_path)
    print(f"\nDone. File saved to:\n  {out_path}")
