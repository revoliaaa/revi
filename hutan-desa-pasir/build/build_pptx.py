# -*- coding: utf-8 -*-
"""Bangun deck roadmap Hutan Desa Pasir (16:9).

    python3 build_pptx.py ../Roadmap_HD_Pasir_PVClimate.pptx
"""
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.dml import MSO_LINE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from data import ACTIVITIES, COMPLETION, MILESTONES, STEP2, TRANSITION, month_label

TEAL = RGBColor(0x0E, 0x7C, 0x6B)
TEAL_TINT = RGBColor(0xE3, 0xF1, 0xEE)
TEAL_MID = RGBColor(0x7F, 0xBC, 0xB1)
NAVY = RGBColor(0x1F, 0x2A, 0x44)
NAVY_TINT = RGBColor(0xE6, 0xE9, 0xEF)
NAVY_MID = RGBColor(0x8A, 0x93, 0xA8)
AMBER = RGBColor(0xC2, 0x6A, 0x0A)
INK = RGBColor(0x1B, 0x24, 0x20)
MUTED = RGBColor(0x5F, 0x6B, 0x65)
HAIR = RGBColor(0xD5, 0xDB, 0xD6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

BODY = "Calibri"
DISPLAY = "Cambria"


# ---------------------------------------------------------------- helpers
def text(slide, x, y, w, h, s, size=10, bold=False, color=INK, align=PP_ALIGN.LEFT,
         font=BODY, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = anchor
    for i, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
        r.font.color.rgb = color
    return tb


def rich(slide, x, y, w, h, runs, size=9, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """runs: list of paragraphs; each paragraph a list of (text, bold, color)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(2)
        for t, b, c in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = b
            r.font.name = BODY
            r.font.color.rgb = c
    return tb


def box(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=0.75, dash=None):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
        if dash:
            sh.line.dash_style = dash
    sh.shadow.inherit = False
    return sh


def line(slide, x1, y1, x2, y2, color=HAIR, w=1.0, dash=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(w)
    if dash:
        c.line.dash_style = dash
    return c


def shape_text(sh, s, size=10, bold=True, color=WHITE):
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = s
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = BODY
    r.font.color.rgb = color


def header(slide, eyebrow, title, page):
    text(slide, 0.4, 0.28, 10, 0.25, eyebrow, size=9, bold=True, color=TEAL)
    text(slide, 0.4, 0.5, 12.5, 0.8, title, size=21, font=DISPLAY, color=INK)
    text(slide, 12.3, 7.1, 0.65, 0.25, str(page), size=8, color=MUTED, align=PP_ALIGN.RIGHT)


def footer(slide, s):
    text(slide, 0.4, 7.08, 11.8, 0.3, s, size=7, color=MUTED)


def node(slide, cx, cy, m, step_color):
    """Penanda milestone: lingkaran = internal, belah ketupat = persetujuan eksternal."""
    if m["type"] == "EXT":
        d = 0.6
        sh = box(slide, cx - d / 2, cy - d / 2, d, d, fill=WHITE, line=step_color, shape=MSO_SHAPE.DIAMOND, lw=2.25)
        shape_text(sh, m["code"], size=10.5, color=step_color)
    else:
        d = 0.46
        sh = box(slide, cx - d / 2, cy - d / 2, d, d, fill=step_color, shape=MSO_SHAPE.OVAL)
        shape_text(sh, m["code"], size=10.5)


# ---------------------------------------------------------------- slide 1
def slide_roadmap(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "HUTAN DESA PASIR · MEMPAWAH, KALIMANTAN BARAT · PLAN VIVO PV CLIMATE",
           "SETAPAK 4 membawa proyek sampai gerbang Plan Vivo Pipeline —\n"
           "kredit karbon baru lahir di fase pengembangan berikutnya", 1)

    gate_x = 8.2
    s1_x0, s1_x1 = 0.4, 7.95
    s2_x0, s2_x1 = 8.45, 12.93

    # Pita STEP
    b = box(s, s1_x0, 1.42, s1_x1 - s1_x0, 0.42, fill=TEAL)
    rich(s, s1_x0 + 0.08, 1.42, s1_x1 - s1_x0 - 0.1, 0.42,
         [[("STEP 1 · SETAPAK 4 (didukung TAF)  ", True, WHITE),
           ("Persiapan → PIN → Pipeline · SAMPAN Kalimantan & LPHD Pasir · Okt 2026 – ±Apr 2028", False, WHITE)]],
         size=10, anchor=MSO_ANCHOR.MIDDLE)
    box(s, s2_x0, 1.42, s2_x1 - s2_x0, 0.42, fill=NAVY)
    rich(s, s2_x0 + 0.08, 1.42, s2_x1 - s2_x0 - 0.1, 0.42,
         [[("STEP 2 · POST-SETAPAK 4  ", True, WHITE),
           ("PDD → kredit → penjualan · 2028+ (indikatif)", False, WHITE)]],
         size=10, anchor=MSO_ANCHOR.MIDDLE)

    # Garis gerbang SETAPAK 4
    line(s, gate_x, 1.3, gate_x, 5.55, color=AMBER, w=2.25, dash=MSO_LINE.DASH)
    pill = box(s, gate_x - 0.62, 1.95, 1.24, 0.3, fill=AMBER, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    shape_text(pill, "TRANSITION GATE", size=8)

    # Jalur milestone
    track_y = 2.75
    s1 = [m for m in MILESTONES if m["step"] == 1]
    s2 = [m for m in MILESTONES if m["step"] == 2]
    xs1 = [0.92 + i * 1.08 for i in range(len(s1))]
    xs2 = [8.95 + i * 0.95 for i in range(len(s2))]
    line(s, xs1[0], track_y, gate_x, track_y, color=TEAL, w=3)
    line(s, gate_x, track_y, xs2[-1], track_y, color=NAVY, w=3)

    for m, cx in zip(s1, xs1):
        text(s, cx - 0.55, 2.27, 1.1, 0.2, f"{month_label(m['start'])[:3]} {month_label(m['start'])[-2:]}"
             f"–{month_label(m['end'])[:3]} {month_label(m['end'])[-2:]}", size=7.5, color=MUTED, align=PP_ALIGN.CENTER)
        node(s, cx, track_y, m, TEAL)
        text(s, cx - 0.55, 3.08, 1.1, 0.4, m["short"], size=9, bold=True, color=INK, align=PP_ALIGN.CENTER)
        text(s, cx - 0.55, 3.47, 1.1, 0.4, m["output"], size=7.5, color=MUTED, align=PP_ALIGN.CENTER)
    for m, cx in zip(s2, xs2):
        text(s, cx - 0.5, 2.27, 1.0, 0.2, m["years"], size=7.5, color=MUTED, align=PP_ALIGN.CENTER)
        node(s, cx, track_y, m, NAVY)
        text(s, cx - 0.5, 3.08, 1.0, 0.4, m["short"], size=9, bold=True, color=INK, align=PP_ALIGN.CENTER)
        text(s, cx - 0.5, 3.47, 1.0, 0.4, m["output"], size=7.5, color=MUTED, align=PP_ALIGN.CENTER)

    # ---- Lajur paralel STEP 1 (bulan 1–19)
    lane_y = 4.12
    mx0, mx1 = 0.85, 7.95

    def mx(m):
        return mx0 + (m - 1) / 19.0 * (mx1 - mx0)

    text(s, 0.4, lane_y - 0.22, 4, 0.2, "Lajur kerja (bulan program)", size=7.5, bold=True, color=MUTED)
    for i, m in enumerate(s1):
        y = lane_y + i * 0.17
        text(s, 0.4, y - 0.04, 0.4, 0.17, m["code"], size=7, color=MUTED)
        fill = AMBER if m["type"] == "EXT" else (TEAL if m["code"] in ("M3", "M4", "M5") else TEAL_MID)
        box(s, mx(m["start"]), y, mx(m["end"] + 1) - mx(m["start"]), 0.11, fill=fill)
    for mm in (1, 4, 7, 10, 13, 16, 19):
        lbl = month_label(mm)
        text(s, mx(mm) - 0.3, lane_y + 7 * 0.17 + 0.0, 0.6, 0.18, f"{lbl[:3]} {lbl[-2:]}", size=6.5,
             color=MUTED, align=PP_ALIGN.CENTER)
    # braket paralel
    bx0, bx1 = mx(4), mx(13)
    box(s, bx0, lane_y + 2 * 0.17 - 0.035, bx1 - bx0, 3 * 0.17 + 0.0, line=TEAL, lw=1, dash=MSO_LINE.DASH)
    text(s, mx(13) + 0.05, lane_y + 2 * 0.17 - 0.02, 1.9, 0.5,
         "∥ M3 · M4 · M5 berjalan paralel\n(bulan 4–12)", size=7.5, bold=True, color=TEAL)

    # ---- Lajur STEP 2 (tahun 2028–2035)
    yx0, yx1 = 8.45, 12.93

    def yx(t):
        return yx0 + (t - 2028.0) / 7.0 * (yx1 - yx0)

    text(s, 8.45, lane_y - 0.22, 4.4, 0.2, "Lajur kerja (tahun, indikatif)", size=7.5, bold=True, color=MUTED)
    bars = [("M8", 2028.3, 2029.8, NAVY_MID, None), ("M9", 2029.6, 2030.6, NAVY, None),
            ("M10", 2030.5, 2035.0, NAVY_MID, None), ("M11", 2032.0, 2032.7, NAVY, None),
            ("M12", 2028.6, 2035.0, NAVY_TINT, NAVY_MID)]
    for i, (code, a, z, f, ln) in enumerate(bars):
        y = lane_y + i * 0.17
        text(s, 8.25, y - 0.04, 0.3, 0.17, code, size=7, color=MUTED, align=PP_ALIGN.RIGHT)
        box(s, yx(a), y, yx(z) - yx(a), 0.11, fill=f, line=ln, lw=0.5)
    # verifikasi berulang
    box(s, yx(2034.4), lane_y + 3 * 0.17, yx(2035.0) - yx(2034.4), 0.11, line=NAVY, lw=0.75, dash=MSO_LINE.DASH)
    for yr in range(2028, 2036, 1):
        text(s, yx(yr) - 0.25, lane_y + 5 * 0.17 + 0.02, 0.5, 0.18, str(yr) if yr < 2035 else "", size=6.5,
             color=MUTED, align=PP_ALIGN.CENTER)
    text(s, 8.45, lane_y + 6 * 0.17 + 0.04, 4.45, 0.3,
         "M12 dimulai paralel sejak M8 (offtake/pre-finance); transaksi unit mengikuti issuance",
         size=7, color=MUTED, italic=True)

    # ---- Strip bawah: legenda · gerbang · jenis unit
    yb = 5.72
    line(s, 0.4, yb - 0.08, 12.93, yb - 0.08, color=HAIR, w=0.75)
    # legenda
    o = box(s, 0.45, yb + 0.06, 0.24, 0.24, fill=TEAL, shape=MSO_SHAPE.OVAL)
    text(s, 0.75, yb + 0.05, 2.6, 0.25, "Milestone internal (dikendalikan tim)", size=8)
    d = box(s, 0.43, yb + 0.38, 0.28, 0.28, fill=WHITE, line=TEAL, shape=MSO_SHAPE.DIAMOND, lw=1.75)
    text(s, 0.75, yb + 0.4, 2.6, 0.25, "Persetujuan eksternal (Plan Vivo / VVB)", size=8)
    line(s, 0.45, yb + 0.86, 0.7, yb + 0.86, color=AMBER, w=2, dash=MSO_LINE.DASH)
    text(s, 0.75, yb + 0.75, 2.7, 0.25, "Batas cakupan SETAPAK 4", size=8)
    box(s, 0.45, yb + 1.06, 0.25, 0.1, line=TEAL, lw=1, dash=MSO_LINE.DASH)
    text(s, 0.75, yb + 1.0, 2.7, 0.25, "Aktivitas paralel", size=8)

    rich(s, 3.55, yb, 4.45, 1.3, [
        [("Arti gerbang: ", True, AMBER),
         ("PIN disetujui Plan Vivo → proyek tercantum di Project pipeline. Pengajuan PIN (M6) belum berarti diterima; "
          "review ±6 minggu + putaran CAR/NIR (±4 minggu tiap putaran).", False, INK)],
        [("Pipeline ≠ registrasi ≠ issuance. ", True, INK),
         ("Registrasi baru setelah validasi (M9). PDD wajib diajukan ≤3 tahun setelah PIN disetujui.", False, INK)],
    ], size=8)
    rich(s, 8.3, yb, 4.65, 1.3, [
        [("Unit Plan Vivo (PVC) di STEP 2: ", True, NAVY)],
        [("fPVC ", True, INK), ("saat validasi — hanya intervensi serapan (restorasi)", False, INK)],
        [("rPVC ", True, INK), ("dari monitoring di Annual Report, belum diverifikasi", False, INK)],
        [("vPVC ", True, INK), ("setelah verifikasi (≤5 th pasca-validasi) — satu-satunya unit yang dapat di-retire", False, INK)],
    ], size=8)

    footer(s, "Sumber: Plan Vivo PV Climate Procedures Manual V3.9 (Bab 1–9, 14); Project Requirements V5.7; Participatory Toolkit V1.0. "
              "Tanggal STEP 2 dan seluruh persetujuan eksternal bersifat indikatif.")
    s.notes_slide.notes_text_frame.text = (
        "Pesan utama: SETAPAK 4 selesai ketika PIN disetujui dan proyek tercantum di pipeline Plan Vivo. "
        "Itu bukan registrasi dan belum menghasilkan kredit. STEP 2 (PDD, validasi, registrasi, monitoring, verifikasi, "
        "issuance, penjualan) membutuhkan pendanaan dan mitra lanjutan. Belah ketupat = keputusan pihak luar, "
        "tanggalnya tidak bisa dijamin.")


# ---------------------------------------------------------------- slide 2
def slide_timeline(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "OUTPUT 4 · TIMELINE & CRITICAL PATH",
           "Jalur kritis melewati FPIC dan keputusan metodologi —\nPIN dikirim paling lambat bulan ke-14 (Nov 2027)", 2)

    x_lab, x0, x1 = 0.4, 3.35, 12.93
    months = 19
    cw = (x1 - x0) / months
    y0 = 1.5
    # header bulan
    for m in range(1, months + 1):
        lbl = month_label(m)
        fill = TEAL_TINT if m <= 14 else RGBColor(0xF6, 0xEB, 0xDD)
        box(s, x0 + (m - 1) * cw, y0, cw - 0.01, 0.36, fill=fill)
        text(s, x0 + (m - 1) * cw, y0 + 0.01, cw, 0.36, f"{lbl[:3]}\n{lbl[-2:]}", size=6.5, color=MUTED,
             align=PP_ALIGN.CENTER)
    rows = [a for a in ACTIVITIES]
    rh = (6.7 - (y0 + 0.42)) / len(rows)
    y = y0 + 0.42
    current = None
    for a in rows:
        code, ms, name, _, _, _, _, _, _, st, en, _, _, crit = a
        if ms != current:
            current = ms
            line(s, x_lab, y, x1, y, color=HAIR, w=0.5)
        text(s, x_lab, y - 0.015, 0.45, rh, code, size=6.5, bold=crit, color=TEAL if crit else MUTED)
        text(s, x_lab + 0.42, y - 0.015, 2.5, rh, name, size=6.5, color=INK)
        ext = ms == "M7"
        fill = AMBER if ext else (TEAL if crit else TEAL_MID)
        box(s, x0 + (st - 1) * cw + 0.01, y + rh * 0.2, (en - st + 1) * cw - 0.02, rh * 0.6, fill=fill)
        y += rh
    # garis submission & gate
    xs = x0 + 14 * cw
    line(s, xs, y0, xs, y, color=TEAL, w=1.25, dash=MSO_LINE.DASH)
    text(s, xs - 1.6, y0 - 0.25, 1.55, 0.22, "PIN submitted (M6.6)", size=7, bold=True, color=TEAL,
         align=PP_ALIGN.RIGHT)
    xg = x0 + 19 * cw
    text(s, xg - 2.5, y0 - 0.25, 2.5, 0.22, "Target indikatif pipeline (M7.5)", size=7, bold=True, color=AMBER,
         align=PP_ALIGN.RIGHT)

    # legenda
    ly = 6.82
    box(s, 0.4, ly + 0.05, 0.3, 0.1, fill=TEAL)
    text(s, 0.75, ly, 1.8, 0.2, "Jalur kritis", size=7.5)
    box(s, 2.0, ly + 0.05, 0.3, 0.1, fill=TEAL_MID)
    text(s, 2.35, ly, 1.8, 0.2, "Ada float", size=7.5)
    box(s, 3.4, ly + 0.05, 0.3, 0.1, fill=AMBER)
    text(s, 3.75, ly, 4.0, 0.2, "Bergantung review Plan Vivo (tanggal tidak pasti)", size=7.5)
    text(s, 7.2, ly, 5.7, 0.2, "STEP 2 jangka panjang: M8 2028–29 · M9 2029–30 · M10 2030→ · M11 ≤5 th pasca-validasi · M12 paralel",
         size=7.5, color=NAVY, bold=True)
    footer(s, "Bulan 1 = Oktober 2026. Review PIN: awal ±6 minggu; tanggapan CAR/NIR ±4 minggu; revisi wajib ≤6 bulan, maks. 3 putaran "
              "(Procedures Manual V3.9 §2.2, §9).")


# ---------------------------------------------------------------- slide 3
def slide_step2(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "OUTPUT 3 · POST-SETAPAK 4 ROADMAP",
           "Lima milestone lanjutan membutuhkan pendanaan baru —\nmetodologi mangrove yang disetujui adalah syarat pertama PDD", 3)
    cols = STEP2
    x0, w, gap = 0.4, 2.42, 0.11
    titles = {m["code"]: m["title"] for m in MILESTONES}
    for i, c in enumerate(cols):
        x = x0 + i * (w + gap)
        ext = c["code"] in ("M9", "M11")
        hb = box(s, x, 1.42, w, 0.55, fill=NAVY if not ext else WHITE, line=NAVY, lw=1.5)
        rich(s, x + 0.05, 1.42, w - 0.1, 0.55, [[(c["code"] + "  ", True, WHITE if not ext else NAVY),
                                                  (titles[c["code"]], True, WHITE if not ext else NAVY)]],
             size=9, anchor=MSO_ANCHOR.MIDDLE)
        blocks = [("Syarat mulai", c["prereq"]), ("Durasi indikatif", c["duration"]),
                  ("Pendanaan (indikatif)", c["funding"]), ("Mitra potensial", c["partners"]),
                  ("Bergantung pada STEP 1", c["dep"]), ("Batas waktu standar", c["deadline"])]
        y = 2.07
        for lab, val in blocks:
            text(s, x + 0.06, y, w - 0.12, 0.18, lab.upper(), size=7, bold=True, color=NAVY_MID)
            text(s, x + 0.06, y + 0.18, w - 0.12, 0.6, val, size=8.5, color=INK)
            y += 0.83
        box(s, x, 1.42, w, 6.95 - 1.42, line=HAIR, lw=0.5)
    footer(s, "Durasi review dari Procedures Manual V3.9 §9; batas 3 tahun §2.2 & §4.4; verifikasi §8. Angka biaya = asumsi perencanaan, "
              "bukan tarif Plan Vivo — konfirmasi lewat penawaran VVB/IE dan dokumen Costs & fees.")


# ---------------------------------------------------------------- slide 4
def slide_transition(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "OUTPUT 5 · TRANSITION READINESS CHECKLIST",
           "Enam belas syarat memindahkan proyek dari pipeline ke penyusunan PDD", 4)
    groups = []
    for t in TRANSITION:
        if not groups or groups[-1][0] != t[1]:
            groups.append((t[1], []))
        groups[-1][1].append(t)
    x_cols = [0.4, 6.75]
    y = [1.45, 1.45]
    for gi, (g, items) in enumerate(groups):
        col = 0 if gi < 3 else 1
        x = x_cols[col]
        text(s, x, y[col], 6.0, 0.25, g.upper(), size=8.5, bold=True, color=TEAL if "gap" not in g else AMBER)
        y[col] += 0.28
        for code, _, req, src in items:
            box(s, x + 0.02, y[col] + 0.04, 0.16, 0.16, line=MUTED, lw=0.75)
            text(s, x + 0.28, y[col], 0.45, 0.3, code, size=8, bold=True, color=MUTED)
            text(s, x + 0.7, y[col], 4.3, 0.42, req, size=8.5)
            text(s, x + 5.0, y[col], 1.1, 0.3, src, size=7.5, color=MUTED, align=PP_ALIGN.RIGHT)
            y[col] += 0.43
        y[col] += 0.1
    footer(s, "Kolom kanan = milestone sumber bukti. Data gap (T08–T10) belum menjadi kewajiban SETAPAK 4 dan diselesaikan di M8.")


def main(out):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_roadmap(prs)
    slide_timeline(prs)
    slide_step2(prs)
    slide_transition(prs)
    prs.save(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "roadmap.pptx")
