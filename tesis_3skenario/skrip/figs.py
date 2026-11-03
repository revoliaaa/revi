import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 13, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
H = json.load(open("work/hasil_3s.json")); R = H["res"]; S = H["series"]; G = H["grid"]; BE = H["breakeven"]
A = json.load(open("work/alokasi_3s.json"))["res"]
C = {"S1": "#8a8a8a", "S2": "#2b6fd6", "S3 USD10": "#86d1b0", "S3 USD20": "#1aa874", "S3 USD35": "#0b6b4a", "S3 USD6": "#c2e8d6", "S3 USD15": "#55bd92"}
def fmt(x, d=0):
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
OUT = "fig/"
D = "Deforestasi kumulatif 2025-2086 (ha)"
# ---------- Gambar 4
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [1.15, 1]})
yrs = np.array(S["S1"]["years"])
lab = {"S1": "S1 tanpa PS aktif", "S2": "S2 PS + pembiayaan awal", "S3 USD10": "S3 USD 10", "S3 USD20": "S3 USD 20", "S3 USD35": "S3 USD 35"}
yl = {}
for k in ["S1", "S2", "S3 USD10", "S3 USD20", "S3 USD35"]:
    y = np.array(S[k]["Total Hutan"]) / 1000
    ax[0].plot(yrs, y, color=C[k], lw=2.6 if k != "S1" else 2.4, ls="--" if k == "S1" else "-", zorder=3 if k == "S2" else 2)
    yl[k] = y[-1]
pos = {"S1": yl["S1"] - 0.55, "S2": yl["S2"] + 0.05, "S3 USD10": yl["S3 USD10"] + 0.6, "S3 USD20": yl["S3 USD20"] + 1.15, "S3 USD35": yl["S3 USD35"]}
for k, p in pos.items(): ax[0].text(2088.5, p, lab[k], va="center", fontsize=12.5)
ax[0].set_xlim(2024, 2087); ax[0].set_ylim(80, 95); ax[0].set_ylabel("Luas hutan (ribu ha)"); ax[0].set_title("(a) Lintasan stok hutan 2024–2087", fontsize=14)
ax[0].text(2027, 81.0, f"S2 − S1 pada 2087: +{fmt(R['S2']['Hutan 2087 (ha)'] - R['S1']['Hutan 2087 (ha)'])} ha\n(patroli 2024–2025 saja; tidak berlanjut)", fontsize=11.5, color="#555")
ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v)))
pr = [6, 10, 15, 20, 35]; a = [R["S1"][D] - R["S2"][D]] * 5; b = [R["S2"][D] - R[f"S3 USD{p}"][D] for p in pr]
x = np.arange(5)
ax[1].bar(x, a, color="#2b6fd6", width=0.62, label="PS + pembiayaan awal (S2 − S1)")
ax[1].bar(x, b, bottom=a, color="#1aa874", width=0.62, label="Perdagangan karbon (S3 − S2)")
for i in range(5):
    t = a[i] + b[i]; ax[1].text(i, t + 40, fmt(t), ha="center", fontsize=12)
ax[1].set_xticks(x, [str(p) for p in pr]); ax[1].set_xlabel("Harga karbon (USD/tCO$_2$e)"); ax[1].set_ylabel("Deforestasi dihindari vs S1 (ha)")
ax[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v)))
ax[1].set_title("(b) Sumber deforestasi dihindari, 2025–2086", fontsize=14); ax[1].legend(frameon=False, loc="upper left", fontsize=12); ax[1].set_ylim(0, 2800)
fig.tight_layout(); fig.subplots_adjust(wspace=0.45); fig.savefig(OUT + "gambar4.png", dpi=200, bbox_inches="tight"); plt.close(fig)
# ---------- Gambar 5
fig, ax = plt.subplots(1, 2, figsize=(14, 5.4))
qs = sorted(G, key=float); q = np.array([float(v) for v in qs])
npv = np.array([G[k]["npv"] for k in qs]) / 1e9; cov = np.array([G[k]["cov"] for k in qs])
m = q <= 60
ax[0].plot(q[m], npv[m], color="#2b6fd6", lw=2.6, label="NPV proyek (Rp miliar, sumbu kiri)"); ax[0].axhline(0, color="#444", lw=1)
ax[0].set_xlabel("Harga karbon (USD/tCO$_2$e)"); ax[0].set_ylabel("NPV proyek 10 % (Rp miliar)")
a2 = ax[0].twinx(); a2.plot(q[m], cov[m], color="#e8692c", lw=2.6, ls="--"); a2.axhline(100, color="#e8692c", lw=1, alpha=.5)
a2.set_ylabel("Cakupan kebutuhan minimum LPHD (%)", color="#c4521c")
from matplotlib.lines import Line2D
ax[0].legend([Line2D([],[],color="#2b6fd6",lw=2.6),Line2D([],[],color="#e8692c",lw=2.6,ls="--")],["NPV proyek (sumbu kiri)","Cakupan kebutuhan LPHD (sumbu kanan)"],frameon=False,loc="upper left",fontsize=11.5); a2.spines["right"].set_visible(True); a2.grid(False)
for v, c, t in [(BE["npv"], "#2b6fd6", f"NPV = 0\nUSD {fmt(BE['npv'], 2)}"), (BE["cov"], "#e8692c", f"cakupan 100 %\nUSD {fmt(BE['cov'], 2)}")]:
    ax[0].axvline(v, color=c, lw=1.2, ls=":"); ax[0].text(v + 0.8, -4.2 if c == "#2b6fd6" else 22, t, color=c, fontsize=11.5)
ax[0].set_title("(a) Ambang kelayakan proyek dan kecukupan LPHD", fontsize=14)
ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v)))
for k, c in [("S3 USD20", "#1aa874"), ("S3 USD35", "#0b6b4a")]:
    ax[1].plot(yrs, np.array(S[k]["Penggunaan Dana Pengelolaan"]) / 1e9, color=c, lw=2.4, label=f"Belanja dana LPHD, {k.replace('USD', 'USD ')}")
ax[1].bar(yrs, np.array(S["S2"]["Realisasi Pembiayaan Awal"]) / 1e9, color="#2b6fd6", width=0.8, label="Pembiayaan awal 2024–2025 (S2, S3)")
ax[1].plot(yrs, np.array(S["S2"]["Kebutuhan Dana Minimum"]) / 1e9, color="#e8692c", lw=2, ls="--", label="Kebutuhan minimum LPHD")
ax[1].set_xlim(2024, 2087); ax[1].set_ylim(0, 7.4); ax[1].set_ylabel("Rp miliar per tahun"); ax[1].legend(frameon=False, fontsize=11, loc="upper center", ncol=2)
ax[1].set_title("(b) Belanja LPHD dan kebutuhan minimum per tahun", fontsize=14)
ax[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v)))
fig.tight_layout(); fig.subplots_adjust(wspace=0.5); fig.savefig(OUT + "gambar5.png", dpi=200, bbox_inches="tight"); plt.close(fig)
# ---------- Gambar 6
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ks = ["S1", "S2", "S3 USD6", "S3 USD10", "S3 USD15", "S3 USD20", "S3 USD35"]; lb = ["S1", "S2", "S3\nUSD 6", "S3\nUSD 10", "S3\nUSD 15", "S3\nUSD 20", "S3\nUSD 35"]
f = [R[k]["FTE rerata"] for k in ks]
ax[0].bar(range(7), f, color=["#8a8a8a", "#2b6fd6"] + ["#1aa874"] * 5, width=0.62)
for i, v in enumerate(f): ax[0].text(i, v + 0.4, fmt(v, 1), ha="center", fontsize=12)
ax[0].set_xticks(range(7), lb); ax[0].set_ylabel("Pekerja setara penuh (FTE)"); ax[0].set_title("(a) Pekerja setara penuh, rerata 2030–2055", fontsize=14)
ks2 = ["S2", "S3 USD10", "S3 USD20", "S3 USD35"]
pg = [R[k]["Pendapatan program per RT (Rp/RT/th)"] / 1000 for k in ks2]; ls_ = [R[k]["Kehilangan akses rata-rata per RT (Rp/RT/th)"] / 1000 for k in ks2]
x = np.arange(4); w = 0.36
ax[1].bar(x - w/2, pg, w, color="#1aa874", label="Pendapatan program per RT")
ax[1].bar(x + w/2, ls_, w, color="#e8692c", label="Kehilangan akses per RT (asumsi)")
for i in range(4):
    ax[1].text(x[i] - w/2, pg[i] + 8, fmt(pg[i], 1), ha="center", fontsize=11); ax[1].text(x[i] + w/2, ls_[i] + 8, fmt(ls_[i], 1), ha="center", fontsize=11)
ax[1].set_xticks(x, ["S2", "S3 USD 10", "S3 USD 20", "S3 USD 35"]); ax[1].set_ylabel("Ribu Rp per RT per tahun"); ax[1].legend(frameon=False, loc="upper left")
ax[1].set_title("(b) Neraca manfaat–beban per RT bergantung", fontsize=14)
fig.tight_layout(); fig.subplots_adjust(wspace=0.3); fig.savefig(OUT + "gambar6.png", dpi=200, bbox_inches="tight"); plt.close(fig)
# ---------- Gambar 7
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2))
mk = {"B1": "o", "B2": "s", "B3": "^", "B4": "D", "R1": "*", "R2": "P"}; col = {"B1": "#2b6fd6", "B2": "#7a5bd6", "B3": "#e8692c", "B4": "#c43c3c", "R1": "#1aa874", "R2": "#0b6b4a"}
for j, price in enumerate([20, 35]):
    b0 = A[f"B0-{price}"]
    for alt in mk:
        x_ = A[f"{alt}-{price}"]; dh = x_["Hutan 2087 (ha)"] - b0["Hutan 2087 (ha)"]; di = x_["Pendapatan Bersih per RT Terdampak rerata"] - b0["Pendapatan Bersih per RT Terdampak rerata"]
        ax[j].scatter(dh, di / 1000, s=170 if alt == "R1" else 110, marker=mk[alt], color=col[alt], zorder=3)
        ax[j].annotate(alt, (dh, di / 1000), xytext=(8, 6), textcoords="offset points", fontsize=12.5)
    ax[j].axhline(0, color="#444", lw=1); ax[j].axvline(0, color="#444", lw=1)
    ax[j].set_xlabel("Δ hutan 2087 terhadap B0 (ha)"); ax[j].set_ylabel("Δ pendapatan RT terdampak (ribu Rp/RT/th)")
    ax[j].set_title(f"({'ab'[j]}) USD {price}/tCO$_2$e", fontsize=14)
    ax[j].xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v)))
fig.tight_layout(); fig.subplots_adjust(wspace=0.3); fig.savefig(OUT + "gambar7.png", dpi=200, bbox_inches="tight"); plt.close(fig)
# ---------- Gambar 2 & 3 (diagram)
def box(ax, x, y, w, h, title, body, ec, fc, fs=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", ec=ec, fc=fc, lw=2))
    ax.text(x + w/2, y + h*0.68, title, ha="center", va="center", fontsize=fs + 1.5, weight="bold")
    ax.text(x + w/2, y + h*0.3, body, ha="center", va="center", fontsize=fs, linespacing=1.15)
def arr(ax, x1, y1, x2, y2, **k): ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="-|>", color="#555", lw=2, **k))
fig, ax = plt.subplots(figsize=(14.8, 7.3)); ax.set_xlim(0, 14.8); ax.set_ylim(0, 7.3); ax.axis("off"); ax.grid(False)
G1, B1, Gr = ("#b9b9b4", "#f4f4f1"), ("#2b78d6", "#edf4fd"), ("#1fa37a", "#e8f6ef")
for i, (t, b) in enumerate([("Data spasial dan kawasan", "SK 25 HD; tutupan HCV 2024;\nHansen 2001–2024"), ("Data sosial-ekonomi", "SAMPAN; rekap patroli 2024–2025;\nMR1 2024; status KUPS 2026"), ("Data karbon dan keuangan", "PDD; harga pasar 2024; pajak;\nbiaya MRV (literatur)")]):
    box(ax, 0.1 + i*4.95, 5.9, 4.7, 1.3, t, b, *G1); arr(ax, 2.45 + i*4.95, 5.9, 2.45 + i*4.95, 5.5)
ax.plot([2.45, 12.35], [5.5, 5.5], color="#555", lw=2); arr(ax, 7.4, 5.5, 7.4, 5.15)
st = [("Konseptualisasi", "diagram umpan balik;\n16 subsistem"), ("Model Vensim", "723 variabel, 39 stok;\nkalibrasi 2001–2014"), ("Validasi", "struktural; MAPE;\nreplikasi PySD"), ("Simulasi skenario", "S1, S2, S3 USD 6–35;\nB0–B4, R1–R2"), ("Ketidakpastian", "Monte Carlo;\nPRCC")]
for i, (t, b) in enumerate(st):
    box(ax, 0.1 + i*2.97, 3.6, 2.72, 1.5, t, b, *B1)
    if i < 4: arr(ax, 2.85 + i*2.97, 4.35, 3.05 + i*2.97, 4.35)
arr(ax, 7.4, 3.6, 7.4, 3.2); ax.plot([1.85, 12.95], [3.15, 3.15], color="#555", lw=2)
rq = [("RQ1  Ekologis", "tutupan, deforestasi,\nemisi (S2−S1, S3−S1)"), ("RQ2  Pembiayaan", "S3−S2; NPV, harga impas,\nkesenjangan LPHD"), ("RQ3  Sosial-ekonomi", "HOK, FTE, KUPS,\npendapatan & beban RT"), ("RQ4  Alokasi manfaat", "Δ hutan dan Δ pendapatan\nRT terdampak vs B0")]
for i, (t, b) in enumerate(rq):
    xx = 0.1 + i*3.7; box(ax, xx, 1.55, 3.5, 1.4, t, b, *Gr); arr(ax, xx + 1.75, 3.15, xx + 1.75, 2.97); ax.plot([xx + 1.75, xx + 1.75], [1.55, 1.15], color="#555", lw=2)
ax.plot([1.85, 12.95], [1.15, 1.15], color="#555", lw=2); arr(ax, 7.4, 1.15, 7.4, 0.82)
ax.add_patch(FancyBboxPatch((1.3, 0.12), 12.2, 0.68, boxstyle="round,pad=0.02,rounding_size=0.06", ec="#e8692c", fc="#fff3ea", lw=2))
ax.text(7.4, 0.46, "Simpulan dan saran: pembiayaan pengelolaan, ekonomi desa, dan pembagian manfaat PS", ha="center", va="center", fontsize=15, weight="bold")
fig.savefig(OUT + "gambar2.png", dpi=200, bbox_inches="tight"); plt.close(fig)
fig, ax = plt.subplots(figsize=(15.4, 7.2)); ax.set_xlim(-0.35, 15.1); ax.set_ylim(0, 7.2); ax.axis("off"); ax.grid(False)
def nb(x, y, t, ec="#2b78d6", fc="#edf4fd", w=2.8, h=0.8, bold=True, fs=14):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", ec=ec, fc=fc, lw=2))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal", linespacing=1.05)
P = {"pen": (2.3, 5.4), "dana": (7.1, 5.4), "hari": (11.9, 5.4), "int": (11.9, 2.95), "def": (7.1, 2.95), "emi": (2.3, 2.95)}
nb(*P["pen"], "Penerimaan\nkarbon"); nb(*P["dana"], "Dana kolektif\nLPHD (60 %)"); nb(*P["hari"], "Hari patroli\ndidanai"); nb(*P["int"], "Intensitas\nperlindungan"); nb(*P["def"], "Deforestasi"); nb(*P["emi"], "Emisi dihindari\n& kredit model")
def sign(x, y, s): ax.text(x, y, s, color="#2b78d6" if s == "+" else "#e8692c", fontsize=17, ha="center", va="center", weight="bold")
arr(ax, 3.75, 5.4, 5.65, 5.4); sign(5.4, 5.68, "+"); arr(ax, 8.55, 5.4, 10.45, 5.4); sign(10.2, 5.68, "+")
arr(ax, 11.9, 4.98, 11.9, 3.38); sign(12.2, 3.65, "+"); arr(ax, 10.45, 2.95, 8.55, 2.95); sign(8.8, 3.25, "−"); arr(ax, 5.65, 2.95, 3.75, 2.95); sign(4.0, 3.25, "−"); arr(ax, 2.3, 3.38, 2.3, 4.98); sign(2.0, 4.7, "+")
ax.text(7.1, 4.25, "R", color="#2b78d6", fontsize=34, weight="bold", ha="center"); ax.text(7.1, 3.75, "loop penguat dana–patroli (hanya S3)", ha="center", fontsize=13, style="italic", color="#555")
for (x, y, t, tx, ty, s) in [(1.1, 6.75, "Harga karbon\n(USD 6–35)", 1.9, 5.85, "+"), (5.0, 6.75, "Biaya MRV, transaksi,\npajak (tetap)", 6.4, 5.85, "−"), (9.4, 6.75, "Kapasitas realisasi\nbelanja LPHD", 11.1, 5.85, "+"), (13.6, 6.75, "Pembiayaan awal 2024–2025\n(2.533 dan 3.011 HOK)", 12.6, 5.85, "+")]:
    nb(x, y, t, ec="#b9b9b4", fc="#f4f4f1", w=2.75 if x != 13.6 else 2.4, h=0.78, bold=False, fs=12.5 if x != 13.6 else 11.5); arr(ax, x + (0.3 if x < 7 else -0.3), 6.35, tx, ty); sign(tx + 0.3 * (1 if x < 7 else -1), ty + 0.12, s)
nb(2.3, 0.75, "Kompensasi\n(eksperimen alokasi)", ec="#e8692c", fc="#fff3ea", bold=False); nb(7.1, 0.75, "Pendapatan RT\nterdampak", ec="#e8692c", fc="#fff3ea", bold=False); nb(11.9, 0.75, "Kehilangan akses\nRT (asumsi)", ec="#e8692c", fc="#fff3ea", bold=False)
arr(ax, 11.9, 2.53, 11.9, 1.18); sign(12.2, 1.5, "+"); arr(ax, 10.45, 0.75, 8.55, 0.75); sign(8.8, 1.05, "−"); arr(ax, 3.75, 0.75, 5.65, 0.75); sign(5.4, 1.05, "+")
ax.annotate("", (2.9, 1.18), (6.4, 4.98), arrowprops=dict(arrowstyle="-|>", color="#555", lw=2, ls="--")); sign(4.0, 2.2, "+")
fig.savefig(OUT + "gambar3.png", dpi=200, bbox_inches="tight"); plt.close(fig)
print("ok")
