"""Grafik makalah Seminar Hasil final dua skenario (Gambar 1–7).

Semua data dibaca dari workbook final melalui data.py; tidak ada angka ilustratif.
"""
import os
import shutil
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.ticker import FuncFormatter
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import data as D

OUT = os.path.join(D.ROOT, "makalah_semhas_final_2skenario", "GRAFIK_MAKALAH")
os.makedirs(OUT, exist_ok=True)
MAP_SRC = sys.argv[1] if len(sys.argv) > 1 else None

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8,
    "axes.labelsize": 7.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 6.8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "legend.frameon": False, "savefig.dpi": 300, "axes.titleweight": "bold",
    "axes.titlelocation": "left",
})
# Warna konsisten: S1 abu-abu; S2 hijau (gelap = harga lebih tinggi);
# pembiayaan awal jingga; aktivasi mekanisme karbon hijau.
C_S1 = "#7a7a7a"
C_P = {10: "#9ccfb5", 20: "#3f9d77", 35: "#105f44"}
C_AWAL = "#d98a2b"
C_KARBON = "#2f8a66"
C_NEG = "#b8483b"
C_INK = "#2b2b2b"
FMT0 = FuncFormatter(lambda v, _: D.fmt(v, 0))
FMT1 = FuncFormatter(lambda v, _: D.fmt(v, 1))
SRC = "Sumber: "


def note(fig, text):
    fig.text(0.01, 0.005, text, fontsize=6, color="#555555", ha="left", va="bottom")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


# ---------------------------------------------------------------- Gambar 1
if MAP_SRC:
    shutil.copy(MAP_SRC, os.path.join(OUT, "Gambar1_peta_lokasi.png"))

# ---------------------------------------------------------------- Gambar 2
def gambar2():
    fig, ax = plt.subplots(figsize=(6.3, 3.6))
    ax.set_xlim(0, 107); ax.set_ylim(1, 60); ax.axis("off")
    W, H = 21, 8
    X = [2, 27, 52, 77]
    boxes = {
        "jem": (X[0], 50, "Pembiayaan jembatan\nmitra 2026–2030", "#fbe3c6", "--"),
        "pat": (X[1], 50, "Patroli tambahan\n(HOK berupah)", "#e3efe9", "-"),
        "int": (X[2], 50, "Intensitas\nperlindungan", "#e3efe9", "-"),
        "stk": (X[3], 50, "Stok hutan\n(deforestasi ↓)", "#e3efe9", "-"),
        "aks": (X[2], 38.5, "Kehilangan akses\n(asumsi kelas D)", "#f8dcd8", "--"),
        "kup": (X[0], 26, "KUPS: modal,\nreinvestasi, surplus", "#f3e6f0", "-"),
        "upa": (X[1], 26, "Upah kerja\nberupah", "#f3e6f0", "-"),
        "rt": (X[2], 26, "Pendapatan bersih\nRT bergantung hutan", "#f8dcd8", "-"),
        "sda": (X[3], 26, "Ketersediaan\nsumber daya hutan", "#e3efe9", "-"),
        "lph": (X[0], 4, "Kas LPHD (60 %)\ndan kapasitas", "#dfe8f3", "-"),
        "kas": (X[1], 4, "Kas bersih sesudah\nbiaya & pemulihan mitra", "#dfe8f3", "-"),
        "kre": (X[2], 4, "Kredit model\n(MRV, jeda terbit)", "#dfe8f3", "-"),
        "mit": (X[3], 4, "Mitigasi bersih thd\nReferensi S1 berpasangan", "#dfe8f3", "-"),
    }
    for k, (x, y, t, c, ls) in boxes.items():
        ax.add_patch(FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc=c, ec="#555555", lw=0.7, ls=ls))
        ax.text(x + W / 2, y + H / 2, t, ha="center", va="center", fontsize=5.9)

    def edge(k, side, f=0.5):
        x, y = boxes[k][0], boxes[k][1]
        return {"l": (x - 0.7, y + H * f), "r": (x + W + 0.7, y + H * f),
                "t": (x + W * f, y + H + 0.7), "b": (x + W * f, y - 0.7)}[side]

    def arr(pa, pb, sign, rad=0.0, col=C_INK, off=(0.6, 0.6)):
        ax.add_patch(FancyArrowPatch(pa, pb, arrowstyle="-|>", mutation_scale=7, lw=0.8,
                                     color=col, connectionstyle=f"arc3,rad={rad}"))
        if sign:
            mx, my = (pa[0] + pb[0]) / 2 + off[0], (pa[1] + pb[1]) / 2 + off[1]
            ax.text(mx, my, sign, fontsize=7.5, fontweight="bold",
                    color=C_NEG if sign == "−" else "#1d6b4f", ha="center", va="bottom")
    G = "#1d6b4f"
    arr(edge("jem", "r"), edge("pat", "l"), "+", off=(0, 0.3))
    arr(edge("pat", "r"), edge("int", "l"), "+", col=G, off=(0, 0.3))
    arr(edge("int", "r"), edge("stk", "l"), "+", col=G, off=(0, 0.3))
    arr(edge("stk", "r", 0.6), edge("mit", "r", 0.4), "+", rad=-0.35, col=G, off=(6.5, 0))
    arr(edge("mit", "l"), edge("kre", "r"), "+", col=G, off=(0, 0.3))
    arr(edge("kre", "l"), edge("kas", "r"), "+", col=G, off=(0, 0.3))
    arr(edge("kas", "l"), edge("lph", "r"), "+", col=G, off=(0, 0.3))
    arr(edge("lph", "t", 0.92), edge("pat", "b", 0.08), "+", col=G, off=(1.6, 2))
    arr(edge("lph", "t", 0.45), edge("kup", "b", 0.45), "+", off=(-2.2, -1))
    arr(edge("pat", "b", 0.5), edge("upa", "t", 0.5), "+", off=(1.5, -1))
    arr(edge("upa", "r"), edge("rt", "l"), "+", off=(0, 0.3))
    arr(edge("sda", "l"), edge("rt", "r"), "+", off=(0, 0.3))
    arr(edge("stk", "b"), edge("sda", "t"), "+", off=(1.5, -1))
    arr(edge("int", "b"), edge("aks", "t"), "+", off=(1.5, -0.8))
    arr(edge("aks", "b"), edge("rt", "t"), "−", off=(1.5, -0.9))
    arr(edge("kup", "b", 0.75), edge("rt", "b", 0.25), "+", rad=0.28, off=(0, -6.5))
    ax.text(25, 17.3, "penerimaan anggota", fontsize=5.8, color="#1d6b4f", ha="center")
    ax.text(64, 17.5, "R", fontsize=11, fontweight="bold", color=G, ha="center", va="center")
    ax.text(64, 15.0, "reinvestasi kas karbon", fontsize=5.6, color=G, ha="center")
    ax.text(2, 59.5, "Hijau tua = loop penguat pembiayaan; garis putus pada kotak = masukan "
            "eksperimen/asumsi; + searah; − berlawanan arah", fontsize=5.6, color="#555555")
    save(fig, "Gambar2_struktur_konseptual_SD.png")


# ---------------------------------------------------------------- Gambar 3
def gambar3():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.45), gridspec_kw={"width_ratios": [1.25, 1]})
    yrs, s1 = D.lin("S1", "Total Hutan")
    for h in D.HARGA:
        _, s2 = D.lin(f"C-J1 USD{h}", "Total Hutan")
        dy = [0.0] + [y2 - y1 for y1, y2 in zip(s1, s2)]
        a.plot([2025] + yrs, dy, color=C_P[h], lw=1.4, marker="o", ms=2.2, label=f"USD {h}")
    a.axvspan(2026, 2030, color=C_AWAL, alpha=0.12, lw=0)
    a.text(2028, a.get_ylim()[1] * 0.93 if a.get_ylim()[1] > 0 else 1, "jembatan", fontsize=6,
           ha="center", color="#8a5410")
    a.set_yscale("symlog", linthresh=500)
    a.yaxis.set_major_formatter(FMT0)
    a.set_yticks([0, 100, 200, 300, 400, 500, 1000, 2000, 5000])
    a.set_xlabel("Tahun")
    a.set_ylabel("Δ luas hutan S2 − S1 (ha)")
    a.set_title("(a) Selisih stok hutan S2 − S1 (C-J1)")
    a.legend(loc="upper left", ncol=1)
    x = np.arange(3)
    awal = [D.d03("dasar", h, "…dari jembatan D1−D0 (ha)") for h in D.HARGA]
    akt = [D.d03("dasar", h, "…dari penjualan D2−D1 (ha)") for h in D.HARGA]
    b.bar(x, awal, color=C_AWAL, width=0.6, label="Pembiayaan awal\n(D1−D0)")
    b.bar(x, akt, bottom=awal, color=C_KARBON, width=0.6,
          label="Aktivasi mekanisme\nkarbon (D2−D1)")
    for i in range(3):
        tot = awal[i] + akt[i]
        b.text(i, tot + 80, D.fmt(tot), ha="center", fontsize=6.6, fontweight="bold")
        b.text(i, awal[i] / 2, D.fmt(awal[i]), ha="center", va="center", fontsize=6.2,
               color="white")
        if akt[i] > 300:
            b.text(i, awal[i] + akt[i] / 2, D.fmt(akt[i]), ha="center", va="center",
                   fontsize=6.2, color="white")
        elif akt[i] > 0:
            b.text(i + 0.33, awal[i] + akt[i] / 2 + 60, "+" + D.fmt(akt[i]), ha="left",
                   va="center", fontsize=6.2, color=C_KARBON)
    b.set_xticks(x, [f"USD {h}" for h in D.HARGA])
    b.yaxis.set_major_formatter(FMT0)
    b.set_ylabel("Deforestasi dihindari 2025–2086 (ha)")
    b.set_title("(b) Dekomposisi D2 − D0")
    b.set_ylim(0, 6300)
    b.legend(loc="upper left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    note(fig, SRC + "HASIL_SIMULASI_FINAL_PWD.xlsx (lembar 3); HASIL_EKSPERIMEN_D0_D3.xlsx "
         "(lembar 3). Sumbu (a) linear sampai 500 ha, logaritmik di atasnya.")
    save(fig, "Gambar3_perlindungan_hutan.png")


# ---------------------------------------------------------------- Gambar 4
def gambar4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.75), gridspec_kw={"width_ratios": [1.3, 1]})
    comp = [("Biaya dibayar dari kas", "#9a9a9a"), ("Pemulihan defisit MRV", "#c9a27a"),
            ("Pemulihan talangan", C_AWAL), ("Kas LPHD (60 %)", C_KARBON),
            ("Bagian mitra (40 %)", "#4f6fa8")]
    for j, h in enumerate([20, 35]):
        tot = D.kas(h, "1a Kas penjualan diterima")
        surplus = D.kas(h, "9 Surplus sebelum pemulihan")
        vals = [tot - surplus, D.kas(h, "11 Pemulihan defisit MRV historis"),
                D.kas(h, "12 Pemulihan talangan jembatan"), D.kas(h, "14 Bagian LPHD 60 %"),
                D.kas(h, "15 Bagian mitra 40 %")]
        left = 0
        for (lab, c), v in zip(comp, vals):
            w = v / tot * 100
            a.barh(j, w, left=left, color=c, height=0.55, label=lab if j == 0 else None)
            if w >= 6:
                a.text(left + w / 2, j, D.fmt(v, 1 if v < 100 else 0), ha="center",
                       va="center", fontsize=6.0, color="white")
            left += w
        a.text(101, j, f"Rp{D.fmt(tot, 1)} M", va="center", fontsize=6.4)
    a.set_yticks([0, 1], ["USD 20", "USD 35"])
    a.set_xlim(0, 125)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel("Porsi kas penjualan 2024–2086 (%); label = Rp miliar")
    a.set_title("(a) Penggunaan kas penjualan (C-J1)")
    a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=3, fontsize=5.8, columnspacing=0.8, handlelength=1.2)
    for h in D.HARGA:
        yrs, r = D.lin(f"C-J1 USD{h}", "Rasio Cakupan Kebutuhan Minimum")
        b.plot(yrs, [v * 100 for v in r], color=C_P[h], lw=1.4, marker="o", ms=2.2,
               label=f"USD {h}")
    yrs, r = D.lin("S1", "Rasio Cakupan Kebutuhan Minimum")
    b.plot(yrs, [v * 100 for v in r], color=C_S1, lw=1.0, ls="--", label="S1")
    b.axhline(100, color="#999999", lw=0.6, ls=":")
    b.set_ylabel("Cakupan kebutuhan\nminimum LPHD (%)")
    b.set_xlabel("Tahun")
    b.set_title("(b) Kecukupan pembiayaan LPHD")
    b.legend(loc="upper left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    note(fig, SRC + "TABEL_REKONSILIASI_AUDIT_AKADEMIK_PWD.xlsx (lembar 1–2); "
         "HASIL_SIMULASI_FINAL_PWD.xlsx (lembar 3, tahun terpilih). Biaya yang ditalangi mitra "
         "di luar kas tidak tampak di (a).")
    save(fig, "Gambar4_keberlanjutan_pembiayaan.png")


# ---------------------------------------------------------------- Gambar 5
def gambar5():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.5))
    x = np.arange(3); w = 0.26
    hut = [D.akses(h, 1.0, "Δ pendapatan hutan/RT") / 1e3 for h in D.HARGA]
    prg = [D.akses(h, 1.0, "Δ program/RT") / 1e3 for h in D.HARGA]
    hil = [-D.akses(h, 1.0, "Δ kehilangan/RT bergantung") / 1e3 for h in D.HARGA]
    net = [D.akses(h, 1.0, "Δ pendapatan bersih/RT bergantung") / 1e3 for h in D.HARGA]
    a.bar(x - w, hut, w, color=C_KARBON, label="Pendapatan hutan")
    a.bar(x, prg, w, color="#8fb7d6", label="Pendapatan program")
    a.bar(x + w, hil, w, color=C_NEG, label="Kehilangan akses")
    a.scatter(x, net, marker="D", s=14, color="black", zorder=3, label="Δ bersih")
    for i in range(3):
        a.text(x[i] + 0.05, net[i] - 22 if net[i] < 0 else net[i] + 8, D.fmt(net[i], 1),
               fontsize=6.0, ha="left")
    a.axhline(0, color="black", lw=0.6)
    a.set_xticks(x, [f"USD {h}" for h in D.HARGA])
    a.yaxis.set_major_formatter(FMT0)
    a.set_ylabel("Δ S2 − S1 (ribu Rp/RT/th)")
    a.set_title("(a) Komponen Δ per RT bergantung")
    a.legend(loc="lower left", fontsize=6.0)
    ms = np.linspace(0, 1.5, 31)
    for h in D.HARGA:
        g0 = D.akses(h, 0.0, "Δ pendapatan bersih/RT bergantung")
        g1 = D.akses(h, 1.0, "Δ pendapatan bersih/RT bergantung")
        t0 = D.akses(h, 0.0, "Δ pendapatan RT terdampak")
        t1 = D.akses(h, 1.0, "Δ pendapatan RT terdampak")
        b.plot(ms, (g0 + (g1 - g0) * ms) / 1e3, color=C_P[h], lw=1.4, label=f"USD {h}")
        b.plot(ms, (t0 + (t1 - t0) * ms) / 1e3, color=C_P[h], lw=1.0, ls="--")
        mg = g0 / (g0 - g1); mt = t0 / (t0 - t1)
        b.plot([mg], [0], "o", color=C_P[h], ms=3.5)
        b.plot([mt], [0], "s", color=C_P[h], ms=3.0, mfc="white")
    # verifikasi linearitas terhadap titik tabel audit
    for _, r in D.AKSES.iterrows():
        h = int(r["Harga"]); m = r["Pengali akses"]
        b.plot([m], [r["Δ pendapatan bersih/RT bergantung"] / 1e3], ".", color="black", ms=2)
    b.axhline(0, color="black", lw=0.6)
    b.axvline(1.0, color="#999999", lw=0.6, ls=":")
    b.text(1.02, b.get_ylim()[1] * 0.9 if b.get_ylim()[1] > 0 else 50, "nilai dasar", fontsize=6)
    b.set_xlabel("Pengali kehilangan akses (kelas D)")
    b.set_ylabel("Δ S2 − S1 (ribu Rp/RT/th)")
    b.set_title("(b) Sensitivitas dan titik impas")
    b.yaxis.set_major_formatter(FMT0)
    b.set_xticks([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]); b.xaxis.set_major_formatter(FuncFormatter(lambda v, _: D.fmt(v, 2)))
    b.legend(loc="lower left", fontsize=5.8, title="utuh = RT bergantung\nputus = RT terdampak",
             title_fontsize=5.6, alignment="left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    note(fig, SRC + "TABEL_REKONSILIASI_AUDIT_AKADEMIK_PWD.xlsx (lembar 5), C-J1, rerata "
         "2030–2055. Titik hitam = run audit; bulat/persegi = titik impas.")
    save(fig, "Gambar5_sosial_ekonomi.png")


# ---------------------------------------------------------------- Gambar 6
def gambar6():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.45), gridspec_kw={"width_ratios": [1.2, 1]})
    alts = ["B0", "B1", "B2", "B3", "B4", "R1", "R2"]
    key = {"B0", "R1", "R2", "B4"}
    for h, mk in [(20, "o"), (35, "s")]:
        for al in alts:
            xk = D.bs(h, al, "Kompensasi kumulatif (Rp)") / 1e9
            yk = D.bs(h, al, "Deforestasi dihindari S2−S1 (ha)")
            c = C_P[h] if al in key else "#bbbbbb"
            a.scatter(xk, yk, marker=mk, s=18, color=c, zorder=3,
                      edgecolor="black" if al in key else "none", lw=0.4)
            if h == 35:
                dx, dy = (1.0, 120) if h == 35 else (0.8, 140)
                if h == 35 and al in ("B3", "B4"):
                    dy = -420 if al == "B3" else 160
                a.text(xk + dx, yk + dy, al, fontsize=6.0,
                       color="black" if al in key else "#888888")
    a.set_xlabel("Kompensasi kumulatif 2024–2086 (Rp miliar)")
    a.set_ylabel("Deforestasi dihindari S2 − S1 (ha)")
    a.yaxis.set_major_formatter(FMT0)
    a.set_title("(a) Perlindungan hutan vs kompensasi")
    a.scatter([], [], marker="o", color=C_P[20], s=14, label="USD 20")
    a.scatter([], [], marker="s", color=C_P[35], s=14, label="USD 35")
    a.legend(loc="center right")
    a.text(9, 150, "USD 20: semua alternatif ≤ 555 ha", fontsize=5.8, color=C_P[20])
    sel = ["B0", "R1", "R2", "B4"]
    x = np.arange(len(sel))
    k87 = [D.kups(35, al, "KUPS aktif 2087") for al in sel]
    pen = [D.kups(35, al, "Penerimaan anggota (Rp juta/th)") for al in sel]
    b.bar(x, k87, color=["#4f6fa8", "#a986b5", "#a986b5", "#a986b5"], width=0.6)
    s1k = D.run("S1", "S KUPS aktif 2087")
    b.axhline(s1k, color=C_S1, ls="--", lw=0.8)
    b.text(-0.45, s1k + 1.0, f"S1 = {D.fmt(s1k, 1)}", fontsize=6, ha="left", color=C_S1)
    for i in range(len(sel)):
        b.text(i, k87[i] + 1.2, D.fmt(k87[i], 1), ha="center", fontsize=6.4, fontweight="bold")
        pass
    b.set_xticks(x, [f"{al}\nRp{D.fmt(pv, 1)} jt/th" for al, pv in zip(sel, pen)], fontsize=6.2)
    b.set_ylabel("KUPS aktif tahun 2087 (unit)")
    b.set_title("(b) KUPS pada USD 35")
    b.set_ylim(0, 58); b.set_xlim(-0.5, 3.9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    note(fig, SRC + "HASIL_BENEFIT_SHARING_PWD.xlsx (lembar 2); TABEL_REKONSILIASI_AUDIT_"
         "AKADEMIK_PWD.xlsx (lembar 7). Label sumbu (b) = penerimaan anggota KUPS rerata.")
    save(fig, "Gambar6_tradeoff_benefit_sharing.png")


# ---------------------------------------------------------------- Gambar 7
def gambar7():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.45), gridspec_kw={"width_ratios": [1, 1.3]})
    ind = "Deforestasi dihindari S2−S1 (ha)"
    for i, h in enumerate(D.HARGA):
        y = 2 - i
        p5, p25, med, p75, p95 = (D.mcq(h, ind, s) for s in ("P5", "P25", "Median", "P75", "P95"))
        a.plot([p5, p95], [y, y], color=C_P[h], lw=1.2)
        a.plot([p25, p75], [y, y], color=C_P[h], lw=4.5, solid_capstyle="butt")
        a.plot([med], [y], "o", color="white", mec="black", ms=4, zorder=3)
        det = D.d03("dasar", h, "Deforestasi dihindari D2−D0 (ha)")
        a.plot([det], [y + 0.22], "v", color="black", ms=3.5)
        a.text(p95 * 1.08, y, f"{D.fmt(med)}\n[{D.fmt(p5)}–{D.fmt(p95)}]", va="center",
               fontsize=5.8)
    a.set_xscale("log")
    a.set_xlim(80, 60000)
    a.xaxis.set_major_formatter(FMT0)
    a.set_xticks([100, 1000, 10000])
    a.set_yticks([2, 1, 0], [f"USD {h}" for h in D.HARGA])
    a.set_xlabel("Deforestasi dihindari S2 − S1 (ha, log)")
    a.set_title("(a) Ensembel N = 400")
    a.plot([], [], "v", color="black", ms=3.5, label="deterministik C-J1")
    a.plot([], [], "o", color="white", mec="black", ms=4, label="median")
    a.legend(loc="upper right", fontsize=5.8)
    sub = D.PRCC[D.PRCC.Harga == 20].set_index("Parameter")
    cols = [("Deforestasi dihindari S2−S1 (ha)", "Defor.\ndihindari"),
            ("Cakupan kebutuhan minimum 2060–2086 (%)", "Cakupan\n2060–86"),
            ("NPV mitra inkremental [SEMENTARA] (Rp)", "NPV mitra\n[SEM.]"),
            ("KUPS aktif 2087 S2", "KUPS\n2087"),
            ("Δ pendapatan per RT terdampak (Rp/th)", "Δ pend. RT\nterdampak")]
    short = {
        "Efektivitas Perlindungan Penuh terhadap Deforestasi": "Efektivitas perlindungan",
        "Besaran Pembiayaan Jembatan per Tahun (Rp)": "Besaran jembatan",
        "Biaya per Hari Patroli (Rp/HOK)": "Biaya per HOK",
        "Durasi Pembiayaan Jembatan (th)": "Durasi jembatan",
        "Pengali laju deforestasi BAU": "Laju deforestasi BAU",
        "Proporsi Kredit REDD dalam Project Area": "Proporsi areal proyek",
        "Pengali biaya MRV": "Biaya MRV",
        "Pengali Kehilangan Akses": "Pengali kehilangan akses",
        "Biaya Reaktivasi KUPS (Rp)": "Biaya reaktivasi KUPS",
        "Porsi Laba Ditahan untuk Reinvestasi": "Porsi reinvestasi KUPS",
        "k (Tingkat Keberlanjutan Patroli Reguler)": "k (patroli reguler)",
    }
    rows = list(short)
    M = np.array([[float(sub.loc[r, c]) for c, _ in cols] for r in rows])
    im = b.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    b.set_xticks(range(len(cols)), [c[1] for c in cols], fontsize=5.8)
    b.set_yticks(range(len(rows)), [short[r] for r in rows], fontsize=6.0)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            b.text(j, i, D.fmt(v, 2), ha="center", va="center", fontsize=5.2,
                   color="white" if abs(v) > 0.55 else "black")
    b.set_title("(b) PRCC pada USD 20")
    b.spines[:].set_visible(False)
    b.tick_params(length=0)
    cb = fig.colorbar(im, ax=b, fraction=0.04, pad=0.02)
    cb.ax.tick_params(labelsize=5.5)
    cb.ax.yaxis.set_major_formatter(FMT1)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    note(fig, SRC + "HASIL_MONTE_CARLO_PRCC_PWD.xlsx (lembar 4 dan 6); LHS 20 parameter, seed "
         "20261104, pasangan S1–S2. Batang tebal = P25–P75; garis = P5–P95.")
    save(fig, "Gambar7_ketidakpastian.png")


if __name__ == "__main__":
    gambar2(); gambar3(); gambar4(); gambar5(); gambar6(); gambar7()
    print(sorted(os.listdir(OUT)))
