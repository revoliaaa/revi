"""Reproduce the six poster figures for the A0 seminar poster.

    python make_figures.py                      # all figures, data from ../data
    python make_figures.py --only 3 4           # selected figures
    python make_figures.py --hd-shapefile HD.shp --landscape-col LANSKAP \
        [--admin-shapefile kec.shp] [--kalbar-shapefile kalbar.shp] [--indonesia-shapefile idn.shp]

Without --hd-shapefile, figure 01 is the non-spatial fallback (area per Hutan
Desa from Tabel 1), clearly marked as such: no polygon or coordinate is ever
invented.

Figures are drawn at their final print size for one column of an A0
landscape poster (about 36 cm wide), so the font sizes below are the printed
sizes in points.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT

# --------------------------------------------------------------------------
# Fixed palette (meaning is constant across all figures)
# --------------------------------------------------------------------------
C = {
    "eco": "#287D63",        # ekologi / hutan
    "ps": "#548A72",         # perhutanan sosial
    "initfin": "#6385A6",    # pembiayaan awal
    "carbon": "#204F75",     # perdagangan karbon
    "lphd": "#446C86",       # keuangan LPHD
    "social": "#3D887B",     # dampak sosial positif
    "loss": "#C47B56",       # kehilangan akses / trade-off negatif
    "ref": "#8B949A",        # referensi / baseline
    "text": "#24343D",
    "grid": "#E3E8E8",
}

CM = 1 / 2.54
COL_W = 36 * CM  # one poster column

plt.rcParams.update({
    "font.family": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 20,
    "text.color": C["text"],
    "axes.edgecolor": C["text"],
    "axes.labelcolor": C["text"],
    "axes.linewidth": 1.2,
    "axes.labelsize": 21,
    "axes.titlesize": 26,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.titlepad": 18,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": C["text"],
    "ytick.color": C["text"],
    "xtick.labelsize": 19,
    "ytick.labelsize": 19,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.major.width": 1.2,
    "ytick.major.width": 1.2,
    "legend.frameon": False,
    "legend.fontsize": 18,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "svg.fonttype": "none",   # text stays editable in Illustrator/Inkscape
    "pdf.fonttype": 42,
})

NOTE_FS = 14.5   # source/definition footnotes
ANNO_FS = 18.5   # in-plot annotations


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def fmt(x: float, dec: int = 0, sign: bool = False) -> str:
    """Indonesian number format: 1.234,5 ; true minus sign."""
    s = f"{abs(x):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if x < 0:
        return "−" + s
    return ("+" + s) if sign else s


def thousands_formatter(dec: int = 0, sign: bool = False):
    return matplotlib.ticker.FuncFormatter(lambda v, _: fmt(v, dec, sign and v > 0))


def footnote(fig, text: str, y: float = 0.012, width: int = 138):
    """Footnote reflowed to the column width (paragraphs split on blank lines)."""
    import textwrap
    paras = [" ".join(p.split()) for p in text.split("\n\n")]
    body = "\n".join(textwrap.fill(p, width) for p in paras)
    fig.text(0.012, y, body, ha="left", va="bottom", fontsize=NOTE_FS,
             color="#4A5A63", linespacing=1.35)


def save(fig, stem: str, pdf_pages: PdfPages | None):
    for ext in ("png", "svg", "pdf"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(OUT / f"{stem}.{ext}", **kw)
    if pdf_pages is not None:
        pdf_pages.savefig(fig)
    plt.close(fig)
    print("saved", stem)


def table() -> pd.DataFrame:
    t = pd.read_csv(DATA / "scenario_table.csv")
    return t.pivot(index="indicator", columns="scenario", values="value")


# --------------------------------------------------------------------------
# 01  Lokasi penelitian
# --------------------------------------------------------------------------
LANDSCAPES = ["Padang Tikar", "Kubu", "Pulau Maya"]
LS_COLOR = {"Padang Tikar": C["eco"], "Kubu": C["ps"], "Pulau Maya": "#93B8A6"}


def fig01_fallback(pp):
    """Non-spatial fallback: SK area of the 25 HD (Tabel 1), grouped by landscape."""
    hd = pd.read_csv(DATA / "hutan_desa_tabel1.csv")
    assert len(hd) == 25 and hd.luas_ha.sum() == 124_941

    fig = plt.figure(figsize=(COL_W, 40 * CM))
    ax = fig.add_axes([0.30, 0.13, 0.62, 0.74])

    y, ticks, labels, heads = 0, [], [], []
    for ls in LANDSCAPES:
        sub = hd[hd.lanskap == ls].sort_values("luas_ha", ascending=False)
        heads.append((y, ls, len(sub), sub.luas_ha.sum()))
        y += 1.25
        for _, r in sub.iterrows():
            ax.barh(y, r.luas_ha, height=0.72, color=LS_COLOR[ls], edgecolor="none")
            ax.text(r.luas_ha + 300, y, fmt(r.luas_ha), va="center", fontsize=16.5)
            ticks.append(y)
            labels.append(r.hutan_desa)
            y += 1
        y += 0.55
    for y0, ls, n, a in heads:
        ax.text(-0.47, y0, f"{ls}", transform=ax.get_yaxis_transform(),
                fontsize=20, fontweight="bold", color=LS_COLOR[ls] if ls != "Pulau Maya" else "#5E8C78",
                va="center")
        ax.text(1.0, y0, f"{n} HD · {fmt(a)} ha", transform=ax.get_yaxis_transform(),
                fontsize=18, ha="right", va="center", color=C["text"])
        ax.axhline(y0 + 0.55, color=C["grid"], lw=1.2, xmin=-0.47, clip_on=False)

    ax.set_yticks(ticks, labels, fontsize=16.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 36_000)
    ax.xaxis.set_major_formatter(thousands_formatter())
    ax.set_xlabel("Luas areal berdasarkan SK (ha)")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=C["grid"], lw=1)
    ax.set_axisbelow(True)

    fig.text(0.012, 0.975, "Wilayah penelitian: 25 Hutan Desa, tiga lanskap",
             fontsize=26, fontweight="bold", va="top")
    fig.text(0.012, 0.942,
             "Total 124.941 ha (areal SK). Luas proyek karbon yang dipakai model: 111.123,17 ha.",
             fontsize=18, va="top")
    # Explicit data-availability flag (the map itself cannot be drawn honestly).
    fig.text(0.012, 0.908,
             "PETA: DATA TIDAK TERSEDIA — shapefile batas Hutan Desa belum diberikan. "
             "Grafik ini pengganti non-spasial.",
             fontsize=16, va="top", color=C["loss"], fontweight="bold")
    footnote(fig,
             "Sumber: Tabel 1 makalah (Laporan Kajian Identifikasi NKT Hutan Desa Lanskap Kubu, Padang Tikar, dan Pulau Maya).\n"
             "Untuk peta: jalankan make_figures.py --hd-shapefile <batas_HD.shp> --landscape-col <kolom lanskap>.")
    save(fig, "01_peta_lokasi", pp)


def fig01_map(pp, hd_shp, landscape_col, admin_shp=None, kalbar_shp=None, idn_shp=None):
    """GIS map from the original research shapefile (requires geopandas)."""
    import geopandas as gpd

    utm = "EPSG:32749"  # UTM 49S covers the study area (~108.8-110.2 E, 0-1.4 S)
    hd = gpd.read_file(hd_shp).to_crs(utm)
    missing = set(hd[landscape_col].unique()) - set(LANDSCAPES)
    if missing:
        raise SystemExit(f"Landscape values not in {LANDSCAPES}: {missing}")

    fig = plt.figure(figsize=(COL_W, 30 * CM))
    ax = fig.add_axes([0.02, 0.10, 0.70, 0.80])
    if admin_shp:
        adm = gpd.read_file(admin_shp).to_crs(utm)
        adm.boundary.plot(ax=ax, color=C["ref"], lw=0.8)
    for ls in LANDSCAPES:
        hd[hd[landscape_col] == ls].plot(ax=ax, color=LS_COLOR[ls], edgecolor="white", lw=0.4)
    xmin, ymin, xmax, ymax = hd.total_bounds
    pad = 0.06 * max(xmax - xmin, ymax - ymin)
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True); s.set_color(C["ref"]); s.set_linewidth(0.8)

    # Scale bar (projected metres) and north arrow.
    span = (xmax - xmin) / 4
    km = max(5, int(round(span / 1000 / 5) * 5))
    x0, y0 = xmin - pad * 0.5, ymin - pad * 0.6
    ax.add_patch(Rectangle((x0, y0), km * 1000, pad * 0.12, color=C["text"]))
    ax.text(x0 + km * 500, y0 + pad * 0.2, f"{km} km", ha="center", va="bottom", fontsize=16)
    ax.annotate("U", xy=(0.95, 0.95), xytext=(0.95, 0.85), xycoords="axes fraction",
                ha="center", va="center", fontsize=18, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=C["text"], lw=1.5))

    # Legend.
    lax = fig.add_axes([0.74, 0.50, 0.25, 0.40]); lax.axis("off")
    for i, ls in enumerate(LANDSCAPES):
        sub = hd[hd[landscape_col] == ls]
        lax.add_patch(Rectangle((0, 0.85 - i * 0.16), 0.12, 0.09, color=LS_COLOR[ls],
                                transform=lax.transAxes))
        lax.text(0.17, 0.895 - i * 0.16, f"{ls}\n{len(sub)} HD", transform=lax.transAxes,
                 va="center", fontsize=16)

    # Insets (only when boundaries are supplied).
    for k, (shp, rect) in enumerate([(idn_shp, [0.74, 0.27, 0.24, 0.18]),
                                     (kalbar_shp, [0.74, 0.07, 0.24, 0.18])]):
        if not shp:
            continue
        g = gpd.read_file(shp).to_crs(utm if k else "EPSG:4326")
        iax = fig.add_axes(rect)
        g.plot(ax=iax, color="#EEF1F1", edgecolor=C["ref"], lw=0.4)
        hd.to_crs(g.crs).plot(ax=iax, color=C["eco"])
        iax.set_xticks([]); iax.set_yticks([])

    fig.text(0.012, 0.975, "Wilayah penelitian: 25 Hutan Desa, tiga lanskap",
             fontsize=26, fontweight="bold", va="top")
    footnote(fig, "Sumber: batas Hutan Desa dari shapefile penelitian; proyeksi WGS 84 / UTM 49S.")
    save(fig, "01_peta_lokasi", pp)


# --------------------------------------------------------------------------
# 02  Diagram mekanisme
# --------------------------------------------------------------------------
def fig02_mechanism(pp):
    fig = plt.figure(figsize=(COL_W, 25 * CM))
    ax = fig.add_axes([0.0, 0.12, 1.0, 0.80])
    ax.set_xlim(0, 20); ax.set_ylim(-0.2, 11.0); ax.axis("off")

    nodes = {
        "pen": (2.55, 8.6, 3.9, 1.35, "Penerimaan\nkarbon", C["carbon"], "-"),
        "dana": (8.35, 8.6, 3.9, 1.35, "Dana kolektif\nLPHD (60%)", C["lphd"], "-"),
        "pat": (14.1, 8.6, 3.6, 1.35, "Hari patroli\ndidanai", C["lphd"], "-"),
        "init": (18.15, 8.6, 3.3, 1.35, "Pembiayaan awal\n2024–2025", C["initfin"], "-"),
        "int": (14.1, 5.35, 3.6, 1.35, "Intensitas\nperlindungan", C["eco"], "-"),
        "ps": (18.15, 5.35, 3.3, 1.35, "Hak kelola PS &\npatroli swadaya", C["ps"], "-"),
        "def": (8.35, 5.35, 3.0, 1.35, "Deforestasi", C["eco"], "-"),
        "emi": (2.55, 5.35, 3.9, 1.35, "Emisi dihindari\n& kredit model", C["carbon"], "-"),
        "akses": (14.1, 1.75, 3.6, 1.35, "Kehilangan akses\nRT (asumsi)", C["loss"], "--"),
        "rt": (8.35, 1.75, 3.9, 1.35, "Pendapatan RT\nterdampak", C["social"], "-"),
    }
    for x, y, w, h, label, col, ls in nodes.values():
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="white", ec=col, lw=2.6, ls=ls))
        ax.text(x, y, label, ha="center", va="center", fontsize=18.5, linespacing=1.15)

    def edge(n1, side1, n2, side2):
        def pt(n, side):
            x, y, w, h = nodes[n][:4]
            return {"r": (x + w / 2, y), "l": (x - w / 2, y), "t": (x, y + h / 2),
                    "b": (x, y - h / 2)}[side]
        return pt(n1, side1), pt(n2, side2)

    def arrow(p, q, sign, col=C["text"], ls="-", rad=0.0, sign_off=(0.0, 0.0)):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=24, lw=2.2,
                                     color=col, ls=ls, shrinkA=2, shrinkB=4,
                                     connectionstyle=f"arc3,rad={rad}"))
        sx = q[0] + sign_off[0]; sy = q[1] + sign_off[1]
        ax.text(sx, sy, sign, ha="center", va="center", fontsize=22, fontweight="bold", color=col)

    PLUS, MINUS = "+", "−"
    # Reinforcing loop (clockwise).
    arrow(*edge("pen", "r", "dana", "l"), PLUS, sign_off=(-0.35, 0.35))
    arrow(*edge("dana", "r", "pat", "l"), PLUS, sign_off=(-0.35, 0.35))
    arrow(*edge("pat", "b", "int", "t"), PLUS, sign_off=(0.32, 0.3))
    arrow(*edge("int", "l", "def", "r"), MINUS, sign_off=(0.35, 0.35))
    arrow(*edge("def", "l", "emi", "r"), MINUS, sign_off=(0.35, 0.35))
    arrow(*edge("emi", "t", "pen", "b"), PLUS, sign_off=(-0.32, -0.3))
    # Drivers.
    arrow(*edge("init", "l", "pat", "r"), PLUS, sign_off=(0.3, 0.35))
    arrow(*edge("ps", "l", "int", "r"), PLUS, sign_off=(0.3, 0.35))
    # Social pathway: access loss is a model assumption.
    arrow(*edge("int", "b", "akses", "t"), PLUS, col=C["loss"], ls="--", sign_off=(0.32, 0.3))
    arrow(*edge("akses", "l", "rt", "r"), MINUS, col=C["loss"], ls="--", sign_off=(0.35, 0.35))
    # Compensation only exists in the allocation experiment (R1).
    p = (nodes["dana"][0] - 1.55, nodes["dana"][1] - 0.675)
    q = (nodes["rt"][0] - 1.55, nodes["rt"][1] + 0.675)
    arrow(p, q, PLUS, col=C["ref"], ls=":", rad=0.42, sign_off=(-0.5, 0.05))
    ax.text(4.95, 3.55, "kompensasi\n(hanya alternatif R1)", ha="center", va="center",
            fontsize=15.5, color="#5F6B71", style="italic")

    # Exogenous inputs (plain text, no boxes).
    for x, txt, sign in [(2.55, "Harga karbon USD6–35/tCO₂e", PLUS),
                         (8.35, "Biaya MRV, transaksi, pajak", MINUS)]:
        ax.text(x, 10.75, txt, ha="center", va="center", fontsize=16, color="#5F6B71")
        arrow((x, 10.42), (x, 9.3), sign, col=C["ref"], sign_off=(0.3, 0.3))

    # Loop marker.
    from matplotlib.patches import Arc
    cx, cy = 8.35, 6.98
    ax.add_patch(Arc((cx, cy), 1.25, 1.0, theta1=120, theta2=420, lw=2, color=C["carbon"]))
    ax.annotate("", xy=(cx - 0.36, cy + 0.42), xytext=(cx - 0.47, cy + 0.30),
                arrowprops=dict(arrowstyle="-|>", color=C["carbon"], lw=2, mutation_scale=18))
    ax.text(cx, cy, "R", ha="center", va="center", fontsize=22, fontweight="bold", color=C["carbon"])
    ax.text(cx + 0.95, cy, "loop penguat\ndana–patroli", ha="left", va="center",
            fontsize=15.5, color=C["carbon"])

    # Legend (bottom row, data coordinates).
    items = [("-", C["text"], "struktur model"),
             ("--", C["loss"], "asumsi model, diuji sensitivitas"),
             (":", C["ref"], "hanya eksperimen alokasi")]
    x = 0.2
    for ls, col, lab in items:
        ax.plot([x, x + 1.0], [0.3, 0.3], ls=ls, color=col, lw=2.6)
        ax.text(x + 1.2, 0.3, lab, va="center", fontsize=15.5)
        x += 1.2 + 0.155 * len(lab) + 0.8
    ax.text(19.9, 10.75, "+ searah   \u2212 berlawanan arah", va="center", ha="right", fontsize=15.5)

    fig.text(0.012, 0.975, "Mekanisme inti model", fontsize=26, fontweight="bold", va="top")
    footnote(fig,
             "Disederhanakan dari Gambar 3 makalah (model Vensim: 724 variabel, 39 stok; 2024–2087, DT 0,0625 tahun). "
             "Efektivitas perlindungan 0,37 dari literatur\n(Oldekop et al. 2019; Sze et al. 2022). "
             "Loop dibatasi biaya MRV dan kemampuan LPHD merealisasikan belanja. Dana LPHD = dana kolektif program, bukan transfer tunai RT.")
    save(fig, "02_mekanisme_sistem", pp)


# --------------------------------------------------------------------------
# 03  Waterfall
# --------------------------------------------------------------------------
def fig03_waterfall(pp):
    sc = pd.read_csv(DATA / "stepwise_contrasts.csv")
    s21 = sc.loc[sc.contrast.str.startswith("S2-S1"), "defor_avoided_ha"].item()
    s32 = sc.loc[sc.contrast.str.startswith("S3-S2"), "defor_avoided_ha"].item()
    s43 = sc.loc[sc.contrast.str.startswith("S4-S3") & (sc.price_usd == 20), "defor_avoided_ha"].item()
    tot = sc.loc[(sc.contrast == "S4-S1") & (sc.price_usd == 20), "defor_avoided_ha"].item()
    assert abs(s21 + s32 + s43 - tot) < 1e-6
    # Cross-check against the paper (Tabel 4 / text).
    assert (round(s21), round(s32), round(s43), round(tot)) == (1720, 276, 3588, 5585)

    fig = plt.figure(figsize=(COL_W, 26 * CM))
    ax = fig.add_axes([0.13, 0.25, 0.84, 0.61])

    steps = [("Perhutanan sosial\nreguler", "S2 − S1", s21, 0, C["ps"]),
             ("Pembiayaan awal", "S3 − S2", s32, s21, C["initfin"]),
             ("Perdagangan karbon\nUSD20", "S4 − S3", s43, s21 + s32, C["carbon"]),
             ("Total", "S4 − S1", tot, 0, C["eco"])]
    w = 0.62
    for i, (lab, con, v, b, col) in enumerate(steps):
        ax.bar(i, v, bottom=b, width=w, color=col, edgecolor="none", zorder=3)
        txt = fmt(v) if i == 3 else fmt(v, sign=True)
        ax.text(i, b + v + 110, txt, ha="center", va="bottom", fontsize=23, fontweight="bold")
        if i < 3:
            top = b + v
            ax.plot([i + w / 2, i + 1 - w / 2], [top, top], color=C["ref"], lw=1.4, ls=(0, (4, 3)), zorder=2)
    ax.set_xticks(range(4), [f"{s[0]}\n{s[1]}" for s in steps], fontsize=18.5)
    ax.tick_params(axis="x", length=0, pad=10)
    ax.set_ylim(0, 6600)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1000))
    ax.yaxis.set_major_formatter(thousands_formatter())
    ax.set_ylabel("Deforestasi dihindari (ha)")
    ax.grid(axis="y", color=C["grid"], lw=1, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    share = s43 / tot
    ax.annotate(f"Pada USD20, perdagangan karbon menyumbang\n{fmt(share * 100)}% deforestasi dihindari terhadap S1.",
                xy=(2 - w / 2 - 0.03, 4300), xytext=(-0.3, 4300),
                fontsize=ANNO_FS, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=C["text"], lw=1.2, shrinkA=0, shrinkB=0,
                                mutation_scale=16))

    fig.text(0.012, 0.975, "Kontribusi bertahap terhadap deforestasi yang dihindari",
             fontsize=26, fontweight="bold", va="top")
    fig.text(0.012, 0.915, "Hasil simulasi, kumulatif 2025–2086, 25 Hutan Desa (124.941 ha)",
             fontsize=18.5, va="top")
    footnote(fig,
             "Deforestasi dihindari = selisih deforestasi kumulatif antarskenario. S1 tanpa PS aktif; S2 PS swadaya; "
             "S3 S2 + pembiayaan awal 2024–2025;\nS4 S3 + perdagangan karbon USD20/tCO₂e. "
             f"Label dibulatkan; total dari nilai presisi ({fmt(s21, 1)} + {fmt(s32, 1)} + {fmt(s43, 1)} = {fmt(tot, 1)} ha), "
             "sehingga jumlah label (5.584) berbeda 1 ha.\nHasil model, bukan dampak kausal terukur. "
             "Sumber: Tabel 4 makalah; FINAL_THESIS_RESULTS.xlsx lembar 2.")
    save(fig, "03_waterfall_deforestasi", pp)


# --------------------------------------------------------------------------
# 04  Threshold
# --------------------------------------------------------------------------
def fig04_threshold(pp):
    g = pd.read_csv(DATA / "price_grid.csv")
    be = pd.read_csv(DATA / "break_even_prices.csv").set_index("item").usd_per_tco2e
    p_npv = be["harga impas NPV proyek = 0"]
    p_cov = be["harga menutup kebutuhan minimum LPHD 2030-55"]
    cov = g.set_index("price_usd").coverage_min_share * 100
    assert (round(p_npv, 2), round(p_cov, 2)) == (6.83, 28.04)
    assert (round(cov[10], 1), round(cov[20], 1)) == (11.8, 49.7)
    need = table().loc["lphd_min_need_rp_bn_yr", "S4 USD20"]

    fig = plt.figure(figsize=(COL_W, 30 * CM))
    a1 = fig.add_axes([0.13, 0.57, 0.83, 0.27])
    a2 = fig.add_axes([0.13, 0.19, 0.83, 0.33], sharex=a1)

    for a in (a1, a2):
        a.axvspan(p_npv, p_cov, color="#EEF1F1", zorder=0, lw=0)
        for p in (p_npv, p_cov):
            a.axvline(p, color=C["text"], lw=1.3, ls=(0, (5, 3)), zorder=1)
        a.grid(axis="y", color=C["grid"], lw=1, zorder=0)
        a.spines["left"].set_visible(False)
        a.tick_params(axis="y", length=0)

    a1.plot(g.price_usd, g.npv_project_rp_bn, color=C["carbon"], lw=3, zorder=3,
            marker="o", ms=3.5)
    a1.axhline(0, color=C["ref"], lw=1.4, zorder=2)
    a1.plot(p_npv, 0, "o", ms=13, mfc="white", mec=C["carbon"], mew=2.6, zorder=4)
    a1.text(p_npv - 0.6, 6.5, f"NPV = 0\nUSD{fmt(p_npv, 2)}", ha="right", va="bottom",
            fontsize=ANNO_FS, fontweight="bold", color=C["carbon"])
    a1.set_ylabel("NPV proyek\n(Rp miliar)")
    a1.set_ylim(-6, 40)
    a1.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(10))
    a1.yaxis.set_major_formatter(thousands_formatter())
    a1.tick_params(axis="x", labelbottom=False)
    a1.text(0.5 * (p_npv + p_cov), 31, "proyek layak,\nkebutuhan LPHD belum tercukupi",
            ha="center", va="center", fontsize=17, color="#4A5A63", style="italic")

    a2.plot(cov.index, cov.values, color=C["lphd"], lw=3, zorder=3, marker="o", ms=3.5)
    a2.axhline(100, color=C["ref"], lw=1.4, zorder=2)
    a2.text(29.3, 95, "kebutuhan minimum LPHD = 100%", fontsize=15.5, va="top", ha="left",
            color="#4A5A63")
    for p, xy in [(10, (10.4, 40)), (20, (20.6, 44))]:
        a2.plot(p, cov[p], "o", ms=13, color=C["lphd"], zorder=4)
        a2.annotate(f"USD{p}: {fmt(cov[p], 1)}%", xy=(p, cov[p]), xytext=xy,
                    fontsize=ANNO_FS, ha="left", va="bottom" if p == 10 else "top",
                    fontweight="bold", color=C["lphd"],
                    arrowprops=dict(arrowstyle="-", color=C["lphd"], lw=1.2, shrinkB=8))
    a2.plot(p_cov, 100, "o", ms=13, mfc="white", mec=C["lphd"], mew=2.6, zorder=4)
    a2.text(p_cov - 0.6, 108, f"100% pada\nUSD{fmt(p_cov, 2)}", ha="right", va="bottom",
            fontsize=ANNO_FS, fontweight="bold", color=C["lphd"])
    a2.set_ylabel("Cakupan kebutuhan\nminimum LPHD (%)")
    a2.set_ylim(0, 165)
    a2.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(50))
    a2.set_xlim(0, 40)
    a2.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    a2.set_xlabel("Harga karbon (USD/tCO₂e, harga tetap)")
    a2.spines["bottom"].set_visible(True)

    fig.text(0.012, 0.975, "Kelayakan proyek dan kecukupan pembiayaan LPHD",
             fontsize=26, fontweight="bold", va="top")
    fig.text(0.012, 0.925,
             f"Ambang kelayakan investasi (USD{fmt(p_npv, 2)}) jauh di bawah ambang kecukupan operasional (USD{fmt(p_cov, 2)})",
             fontsize=18.5, va="top")
    footnote(fig,
             "NPV proyek: diskonto 10%, harga konstan 2024, 2024–2086, cakupan biaya model (tanpa biaya pengembangan proyek). "
             f"Cakupan = belanja LPHD ÷ kebutuhan minimum\n(Rp{fmt(need, 2)} miliar/tahun), rerata 2030–2055: "
             "rata-rata periode, bukan jaminan pada setiap tahun (2024–2027 belum ada belanja dari kredit). "
             "Titik = 40 simulasi deterministik\npada harga bulat USD1–40; garis hanya penghubung visual. "
             "Sumber: FINAL_THESIS_RESULTS.xlsx lembar 3–4; teks hlm. 7 makalah.")
    save(fig, "04_threshold_pembiayaan", pp)


# --------------------------------------------------------------------------
# 05  Diverging bars
# --------------------------------------------------------------------------
def fig05_diverging(pp):
    t = table()
    ben = {p: t.loc["hh_programme_income_rp", f"S4 USD{p}"] for p in (10, 20)}
    loss = {p: t.loc["hh_access_loss_rp", f"S4 USD{p}"] for p in (10, 20)}
    assert [round(ben[p]) for p in (10, 20)] == [6315, 16331]
    assert [round(loss[p]) for p in (10, 20)] == [227077, 448032]

    fig = plt.figure(figsize=(COL_W, 25 * CM))
    ax = fig.add_axes([0.14, 0.31, 0.82, 0.52])
    ys = {10: 1, 20: 0}
    h = 0.5
    for p, y in ys.items():
        ax.barh(y, -loss[p] / 1000, height=h, color=C["loss"], edgecolor="none", zorder=3)
        ax.barh(y, ben[p] / 1000, height=h, color=C["social"], edgecolor="none", zorder=3)
        ax.text(-loss[p] / 1000 + 10, y, "−Rp" + fmt(loss[p]), ha="left", va="center",
                fontsize=21, fontweight="bold", color="white")
        ax.text(ben[p] / 1000 + 8, y, "+Rp" + fmt(ben[p]), ha="left", va="center",
                fontsize=21, fontweight="bold", color=C["text"])
    ax.set_yticks(list(ys.values()), [f"USD{p}" for p in ys], fontsize=21, fontweight="bold")
    ax.tick_params(axis="y", length=0, pad=12)
    ax.axvline(0, color=C["text"], lw=1.8, zorder=4)
    ax.set_xlim(-560, 560)
    ax.set_ylim(-0.6, 1.95)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(100))
    ax.xaxis.set_major_formatter(thousands_formatter(sign=True))
    ax.set_xlabel("Rp ribu per RT per tahun (rerata 2030–2055, skenario S4)")
    ax.grid(axis="x", color=C["grid"], lw=1, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.text(-10, 1.62, "← Kehilangan akses (asumsi model)",
            ha="right", va="center", fontsize=17, color=C["loss"], fontweight="bold")
    ax.text(10, 1.62, "Manfaat program per RT →", ha="left", va="center",
            fontsize=17, color=C["social"], fontweight="bold")
    r10, r20 = loss[10] / ben[10], loss[20] / ben[20]
    ax.text(250, 0.5, f"Kehilangan akses ≈ {fmt(r10)}× (USD10)\ndan {fmt(r20)}× (USD20)\nmanfaat program",
            ha="center", va="center", fontsize=ANNO_FS, color=C["text"], linespacing=1.3)

    fig.text(0.012, 0.975, "Manfaat program dan potensi kehilangan pendapatan RT",
             fontsize=26, fontweight="bold", va="top")
    fig.text(0.012, 0.915,
             "Kedua komponen dihitung pada skala yang sama; besaran kehilangan bergantung pada asumsi pembatasan akses",
             fontsize=18.5, va="top")
    footnote(fig,
             "Manfaat program = pendapatan program per RT; kehilangan akses = rata-rata per RT, asumsi model (kelas D), bukan kerugian terukur. "
             "Keduanya komponen,\nbukan perubahan total pendapatan terhadap baseline (rerata pendapatan bersih RT S1: Rp41,25 juta/RT/tahun). "
             "Sensitivitas: pengali kehilangan akses diuji 0–3,24;\nPRCC terhadap pendapatan RT −0,79. "
             "Tanpa kehilangan akses, selisih pendapatan S4−S3 menjadi +Rp34.402 (USD10) dan +Rp118.629 (USD20).\n"
             "Sumber: teks hlm. 8–9 makalah; FINAL_THESIS_RESULTS.xlsx lembar 1A.")
    save(fig, "05_diverging_pendapatan", pp)


# --------------------------------------------------------------------------
# 06  Quadrant scatter
# --------------------------------------------------------------------------
def fig06_quadrant(pp):
    d = pd.read_csv(DATA / "alokasi_manfaat_makalah.csv")
    d["y"] = d.d_pendapatan_rt_terdampak_vs_B0_rp / 1000
    d["x"] = d.d_defor_dihindari_vs_B0_ha
    full = d.dropna(subset=["x", "y"])
    get = lambda a, p, c: d.loc[(d.alternatif == a) & (d.harga_usd == p), c].item()

    fig = plt.figure(figsize=(COL_W, 30 * CM))
    ax = fig.add_axes([0.14, 0.27, 0.62, 0.58])
    X0, X1, Y0, Y1 = -3300, 3000, -260, 740
    ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1)
    # Quadrants: very light tints, meaning from the fixed palette.
    ax.add_patch(Rectangle((X0, 0), -X0, Y1, color=C["loss"], alpha=0.07, lw=0, zorder=0))
    ax.add_patch(Rectangle((0, 0), X1, Y1, color=C["social"], alpha=0.07, lw=0, zorder=0))
    ax.add_patch(Rectangle((0, Y0), X1, -Y0, color=C["eco"], alpha=0.04, lw=0, zorder=0))
    ax.axhline(0, color=C["text"], lw=1.4, zorder=1)
    ax.axvline(0, color=C["text"], lw=1.4, zorder=1)
    qfs = 16
    ax.text(X0 + 80, Y1 - 25, "pendapatan naik,\nperlindungan berkurang", va="top", fontsize=qfs, color="#9A5A3A")
    ax.text(80, Y1 - 25, "keduanya naik atau\ntidak berkurang", va="top", fontsize=qfs, color="#2E6B60")
    ax.text(1356, -170, "perlindungan naik,\npendapatan turun", va="center", ha="center", fontsize=qfs, color="#1F6650")
    ax.text(X0 + 80, Y0 + 20, "keduanya turun", va="bottom", fontsize=qfs, color="#5F6B71")

    ms = 13
    def mark(x, y, p, col, z=5):
        if p == 10:
            ax.plot(x, y, "o", ms=ms, mfc="white", mec=col, mew=2.6, zorder=z)
        else:
            ax.plot(x, y, "o", ms=ms, color=col, zorder=z)

    # B0 reference.
    ax.plot(0, 0, "s", ms=13, color=C["text"], zorder=7)
    ax.text(-70, -22, "B0", ha="right", va="top", fontsize=19, fontweight="bold")
    # B1 (grey) and R1 (emphasised) on X = 0.
    for p in (10, 20):
        mark(0, get("B1", p, "y"), p, C["ref"], z=5)
        mark(0, get("R1", p, "y"), p, C["social"], z=6)
    ax.text(110, get("R1", 20, "y"), "R1", fontsize=22, fontweight="bold", color=C["social"], va="center")
    ax.text(110, get("B1", 20, "y"), "B1", fontsize=19, fontweight="bold", color="#5F6B71", va="center")
    ax.annotate(f"R1: +Rp{fmt(get('R1', 10, 'd_pendapatan_rt_terdampak_vs_B0_rp'))} (USD10)\n"
                f"     +Rp{fmt(get('R1', 20, 'd_pendapatan_rt_terdampak_vs_B0_rp'))} (USD20)\n"
                "tanpa penurunan deforestasi\ndihindari terhadap B0",
                xy=(60, get("R1", 20, "y") + 8), xytext=(900, 330), fontsize=17, va="center",
                color=C["social"], arrowprops=dict(arrowstyle="-", color=C["social"], lw=1.2))

    # B4 at USD20 (upper bound of B3-B4).
    b4x, b4y = get("B4", 20, "x"), get("B4", 20, "y")
    mark(b4x, b4y, 20, C["loss"])
    ax.text(b4x + 100, b4y + 10, f"B4  ({fmt(b4x)} ha; +Rp{fmt(b4y * 1000)})", fontsize=17,
            fontweight="bold", color="#9A5A3A", va="center")
    # B3 at USD20: x reported, y only bounded (0, B4].
    b3x = get("B3", 20, "x")
    ax.plot([b3x, b3x], [6, b4y - 22], color=C["loss"], lw=2.2, ls=(0, (2, 2)), zorder=3)
    ax.text(b3x + 100, 250, "B3 (USD20): X sama,\nY > 0 dan ≤ B4;\nnilai tidak dilaporkan",
            fontsize=15, color="#9A5A3A", va="center")
    # R2: x reported; y negative but not reported.
    for p, dx, ha in [(10, 70, "left"), (20, -70, "right")]:
        x = get("R2", p, "x")
        ax.annotate("", xy=(x, Y0 + 8), xytext=(x, -6),
                    arrowprops=dict(arrowstyle="-|>", color=C["eco"], lw=2.2, ls=(0, (2, 2)), mutation_scale=18))
        ax.text(x + dx, Y0 + 12, f"USD{p}", ha=ha, va="bottom",
                fontsize=15.5, fontweight="bold", color=C["eco"])
    ax.text(1356, -58, "R2: +237 / +2.475 ha\n\u0394 pendapatan < 0\n(besaran tidak dilaporkan)",
            fontsize=15, color=C["eco"], ha="center", va="center")

    ax.set_xlabel("Δ deforestasi dihindari terhadap B0 (ha, kumulatif 2025–2086)")
    ax.set_ylabel("Δ pendapatan RT terdampak terhadap B0\n(Rp ribu/RT/tahun)")
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1000))
    ax.xaxis.set_major_formatter(thousands_formatter(sign=True))
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(100))
    ax.yaxis.set_major_formatter(thousands_formatter(sign=True))
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)

    # Side panel: legend + data gaps.
    sx = 0.785
    fig.add_artist(matplotlib.lines.Line2D([sx + 0.01], [0.80], marker="o", ms=ms, mfc="white",
                                           mec=C["text"], mew=2.4, transform=fig.transFigure))
    fig.text(sx + 0.035, 0.80, "USD10", va="center", fontsize=18)
    fig.add_artist(matplotlib.lines.Line2D([sx + 0.01], [0.755], marker="o", ms=ms, color=C["text"],
                                           transform=fig.transFigure))
    fig.text(sx + 0.035, 0.755, "USD20", va="center", fontsize=18)
    fig.add_artist(matplotlib.lines.Line2D([sx + 0.01], [0.71], marker="s", ms=12, color=C["text"],
                                           transform=fig.transFigure))
    fig.text(sx + 0.035, 0.71, "B0 acuan", va="center", fontsize=18)
    fig.text(sx, 0.64,
             "DATA TIDAK\nTERSEDIA\ndalam makalah:\n• B2 (USD10, USD20)\n• B3, B4 (USD10)\n"
             "• Y untuk B3 (USD20)\n• Y untuk R2\n\nDibutuhkan: tabel\nkeluaran eksperimen\nalokasi (ΔX, ΔY\nper alternatif\ndan harga).",
             va="top", fontsize=15, color=C["loss"], linespacing=1.3)

    fig.text(0.012, 0.975, "Trade-off alokasi manfaat karbon: konservasi dan pendapatan",
             fontsize=26, fontweight="bold", va="top")
    fig.text(0.012, 0.925,
             "Hanya titik dengan nilai numerik di makalah yang digambar; tidak ada posisi yang dibaca dari gambar",
             fontsize=18.5, va="top")
    footnote(fig,
             "B0 = alokasi asli dana fleksibel LPHD (identik dengan S4). R1 = porsi patroli, rehabilitasi, dan kebakaran seperti B0; 20% dana fleksibel dialihkan dari KUPS ke\n"
             "kompensasi RT terdampak. R2 = porsi patroli 50%. B3, B4 = porsi patroli 40% → 20%. Tujuh alternatif diuji; R1 bukan solusi optimal untuk semua desa.\n"
             "B1 dibulatkan ke Rp100 (kotak Gambar 7). B4: nilai tertinggi B3–B4 dari teks (“hingga”), dikaitkan ke B4 sesuai Gambar 7. "
             "Kehilangan akses = asumsi model.\nSumber: teks hlm. 9 dan Gambar 7 makalah; data/alokasi_manfaat_makalah.csv.")
    save(fig, "06_quadrant_alokasi", pp)


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", type=int)
    ap.add_argument("--hd-shapefile")
    ap.add_argument("--landscape-col", default="LANSKAP")
    ap.add_argument("--admin-shapefile")
    ap.add_argument("--kalbar-shapefile")
    ap.add_argument("--indonesia-shapefile")
    a = ap.parse_args()
    sel = set(a.only or range(1, 7))

    with PdfPages(OUT / "poster_visual_preview.pdf") as pp:
        if 1 in sel:
            if a.hd_shapefile:
                fig01_map(pp, a.hd_shapefile, a.landscape_col, a.admin_shapefile,
                          a.kalbar_shapefile, a.indonesia_shapefile)
            else:
                fig01_fallback(pp)
        if 2 in sel:
            fig02_mechanism(pp)
        if 3 in sel:
            fig03_waterfall(pp)
        if 4 in sel:
            fig04_threshold(pp)
        if 5 in sel:
            fig05_diverging(pp)
        if 6 in sel:
            fig06_quadrant(pp)


if __name__ == "__main__":
    main()
