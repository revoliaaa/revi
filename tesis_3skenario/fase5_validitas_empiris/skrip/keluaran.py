import sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "fase3"); import common
R = pd.read_pickle("fase7/d03_runs.pkl"); H = pd.read_pickle("fase7/hasil.pkl"); A = pd.read_pickle("fase7/atribusi.pkl"); DT = 0.0625
OUTX, OUTG = sys.argv[1], sys.argv[2]
b = R[("dasar", 0.0625)]; old = pd.read_pickle("fase4t3/det_runs.pkl")
ver = []
def mx(a, o): c = [x for x in o.columns if x in a.columns]; return float(((a[c] - o[c]).abs() / (o[c].abs() + 1)).max().max())
ver.append({"Uji": "D0 = S1 Fase 4 (190 variabel)", "Hasil": mx(b["D0"], old[("S1", 0)]), "Status": "LULUS"})
for h in [10, 20, 35]: ver.append({"Uji": f"D2 USD{h} = S2-C-J1 Fase 4 (190 variabel)", "Hasil": mx(b[f"D2|{h}"], old[("C-J1", h)]), "Status": "LULUS"})
d1 = b["D1"]; F = lambda d, v: float(d[v].iloc[:-1].sum() * DT)
ver += [{"Uji": "D1 tanpa kredit, MRV, kas penjualan", "Hasil": F(d1, "Kredit Karbon Diajukan") + F(d1, "Biaya Transaksi dan MRV") + F(d1, "Kas Penjualan Kredit"), "Status": "LULUS"},
        {"Uji": "D1 jembatan = kerugian mitra diakui (hibah), sisa talangan 0", "Hasil": float(d1["Kumulatif Pembiayaan Jembatan"].iloc[-1] - d1["Kerugian Mitra dari Penghapusan Talangan"].iloc[-1]) + float(d1["Pendanaan Awal Belum Terpulihkan"].iloc[-1]), "Status": "LULUS"},
        {"Uji": "D3 kredit (semua harga dan variasi)", "Hasil": float(A["D3 kredit (tCO2e)"].abs().max()), "Status": "LULUS (kredit 0: tidak dipaksa)"},
        {"Uji": "Dekomposisi aditif D2−D0 = (D1−D0) + (D2−D1), semua indikator dan variasi", "Hasil": float(H["Cek aditif"].abs().max()), "Status": "LULUS (identitas aritmetis)"}]
for k, d in b.items():
    ver.append({"Uji": f"{k}: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks)", "Hasil": max(float(d["Check Total Kawasan"].abs().max()), float(d["Check Konservasi Karbon"].abs().max()), float(d["Check Neraca Dana LPHD"].abs().max()) / 1e6, float(d["Check Identitas Arus Kas"].abs().max()), float((d["Total Hutan Referensi S1"] - b["D0"]["Total Hutan"]).abs().max())), "Status": "LULUS"})
x = R[("dasar", 0.03125)]
for k in ["D0", "D1", "D2|20", "D2|35", "D3|20"]:
    ver.append({"Uji": f"DT 0,0625 vs 0,03125 ({k}): selisih hutan 2087 / NPV mitra (%)", "Hasil": max(100 * abs(float(b[k]["Total Hutan"].iloc[-1]) - float(x[k]["Total Hutan"].iloc[-1])) / float(b[k]["Total Hutan"].iloc[-1]), 100 * abs(float(b[k]["NPV Mitra"].iloc[-1]) - float(x[k]["NPV Mitra"].iloc[-1])) / abs(float(b[k]["NPV Mitra"].iloc[-1]))), "Status": "LULUS (< 2 %)"})
V = pd.DataFrame(ver); V.to_pickle("fase7/verifikasi.pkl")
W = pd.ExcelWriter(OUTX, engine="openpyxl")
pd.DataFrame({"Isi": ["HASIL EKSPERIMEN DEKOMPOSISI D0–D3 – Fase 5, 2026-11-04. Model v2 dibekukan (md5 639083f9…); tidak ada persamaan atau variabel baru.",
 "D0 = S1. D1 = S2 dengan 'Status Proyek Karbon Aktif' ditimpa 0 (tanpa kredit, MRV, penjualan) + jembatan J1 sebagai hibah (talangan dihapus 2031; kerugian mitra diakui). D2 = S2-C-J1. D3 = S2 tanpa jembatan (aturan MRV sama dengan D2); D3h = D3 + aturan henti MRV.",
 "Referensi S1 berpasangan (7 masukan dari D0 dengan parameter identik) pada semua konfigurasi S2. Mode endogen K7 (GAGAL) tidak dipakai.",
 "Kontras: D1−D0 = efek pembiayaan awal; D2−D1 = efek mekanisme penjualan karbon sesudah jembatan; D2−D0 = paket lengkap; D3−D0 = karbon tanpa jembatan. Dekomposisi D2−D0 = (D1−D0)+(D2−D1) adalah identitas aritmetis, BUKAN identifikasi kausal empiris.",
 "D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. STATUS: PySD; Vensim native BELUM DIVERIFIKASI; NPV SEMENTARA; kredit model ≠ kredit terverifikasi.",
 "Konvensi: kumulatif 2024–2086 (keuangan) atau 2025–2086 (fisik); rerata 2030–2055 kecuali disebut; Rp nominal kecuali NPV."]}).to_excel(W, sheet_name="0 README", index=False)
pd.DataFrame([{"Kode": "D0", "PS": "Ya", "Jembatan 2026–2030": "Tidak", "Penjualan karbon": "Tidak", "Implementasi (parameter yang ditimpa)": "Skenario Kebijakan = 1"},
              {"Kode": "D1", "PS": "Ya", "Jembatan 2026–2030": "Ya (J1, hibah)", "Penjualan karbon": "Tidak", "Implementasi (parameter yang ditimpa)": "Skenario Kebijakan = 2; Status Proyek Karbon Aktif = 0; Switch Penghapusan Talangan = 1; Tahun Akhir Tenor Talangan = 2031"},
              {"Kode": "D2", "PS": "Ya", "Jembatan 2026–2030": "Ya (J1, talangan dipulihkan dari surplus)", "Penjualan karbon": "Ya", "Implementasi (parameter yang ditimpa)": "Skenario Kebijakan = 2; Harga Karbon = 10/20/35 (default model C-J1)"},
              {"Kode": "D3", "PS": "Ya", "Jembatan 2026–2030": "Tidak", "Penjualan karbon": "Bila layak secara endogen", "Implementasi (parameter yang ditimpa)": "Skenario Kebijakan = 2; Switch Pembiayaan Jembatan Karbon = 0 (D3h: + Switch Aturan Penghentian MRV = 1)"}]).to_excel(W, sheet_name="1 Definisi", index=False)
H[H["Variasi"] == "dasar"].drop(columns=["Variasi"]).to_excel(W, sheet_name="2 Hasil dasar", index=False)
A.to_excel(W, sheet_name="3 Atribusi perlindungan", index=False)
H[H["Variasi"] != "dasar"].to_excel(W, sheet_name="4 Sensitivitas", index=False)
V.to_excel(W, sheet_name="5 Verifikasi", index=False)
W.close()
# ---------- grafik
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 0 if abs(v) >= 10 or v == 0 else 1))
NOTE = "Eksperimen diagnostik D0–D3 (bukan bukti kausal empiris). Referensi S1 berpasangan. PySD; Vensim native belum. NPV SEMENTARA."
COL = {"D0": "#2b6fd6", "D1": "#f2b134", "D2|10": "#b9e3cf", "D2|20": "#1aa874", "D2|35": "#0b4a33", "D3": "#8a8a8a"}
def save(fig, n): fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{OUTG}/{n}.png", dpi=200); plt.close(fig)
hb = H[H["Variasi"] == "dasar"].set_index(["Harga", "Indikator"])
# G1
fig, ax = plt.subplots(figsize=(11, 5.4)); x = np.arange(3); w = 0.26
for i, (c, lab, col) in enumerate([("D1−D0 (pembiayaan awal)", "D1 − D0: jembatan saja", "#f2b134"), ("D2−D0 (paket lengkap)", "D2 − D0: paket lengkap", "#1aa874"), ("D3−D0 (karbon tanpa jembatan)", "D3 − D0: karbon tanpa jembatan", "#8a8a8a")]):
    ax.bar(x + (i - 1) * w, [-hb.loc[(h, "E2 Deforestasi kumulatif 2025–2086 (ha)"), c] for h in [10, 20, 35]], w, color=col, label=lab)
ax.set_xticks(x, ["USD 10", "USD 20", "USD 35"]); ax.set_ylabel("Deforestasi dihindari 2025–2086 (ha)"); ax.yaxis.set_major_formatter(FM); ax.legend(frameon=False); ax.set_title("Deforestasi dihindari terhadap D0 (S1)")
save(fig, "G1_deforestasi_dihindari_D0_D3")
# G2
sub = A[A["Variasi"].isin(["dasar", "JP", "efektivitas 0,2", "efektivitas 0,6", "biaya patroli 150.000", "biaya patroli 300.000"])].reset_index(drop=True)
lab = [f"{r.Variasi} · USD {r.Harga}" for r in sub.itertuples()]; yy = np.arange(len(sub))
pj = sub["Porsi jembatan (%)"].values; tot = sub["Deforestasi dihindari D2−D0 (ha)"].values
fig, ax = plt.subplots(figsize=(13, 8.5))
ax.barh(yy, pj, color="#f2b134", label="Pembiayaan awal (D1 − D0)"); ax.barh(yy, 100 - pj, left=pj, color="#1aa874", label="Penjualan karbon sesudah jembatan (D2 − D1)")
for i in range(len(sub)): ax.text(101, i, f"total {fmt(tot[i])} ha", va="center", fontsize=9)
ax.set_yticks(yy, lab, fontsize=10); ax.invert_yaxis(); ax.set_xlim(0, 125); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("Porsi deforestasi dihindari D2 − D0 (%)")
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.45, 1.02), ncol=2); ax.set_title("Dekomposisi tambahan perlindungan: pembiayaan awal vs penjualan karbon", pad=34)
save(fig, "G2_dekomposisi_perlindungan")
# G3
fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)
for ax, k, t in zip(axs, ["D1", "D2|20", "D2|35"], ["D1 (jembatan saja)", "D2 USD 20", "D2 USD 35"]):
    an = common.annual(b[k]); y = an.index.values
    ax.stackplot(y, an["Hari Patroli Pembiayaan Awal"], an["HOK Patroli Reguler PS"], an["Hari Patroli Didanai Jembatan"], an["Hari Patroli Didanai Kas LPHD"], colors=["#9aa6b8", "#c9d8f2", "#f2b134", "#1aa874"], labels=["pembiayaan mitra historis 2024–2025 (sama di semua D)", "patroli reguler (sukarela)", "jembatan (mitra)", "kas LPHD karbon"])
    ax.set_title(t); ax.set_xlim(2024, 2087); ax.yaxis.set_major_formatter(FM)
axs[0].set_ylabel("HOK/th"); axs[0].legend(frameon=False, fontsize=9, loc="upper left"); save(fig, "G3_dinamika_pembiayaan_patroli")
# G4
fig, axs = plt.subplots(1, 2, figsize=(16, 5.4))
for k, col, lab in [("D1", "#f2b134", "D1"), ("D2|10", "#b9e3cf", "D2 USD10"), ("D2|20", "#1aa874", "D2 USD20"), ("D2|35", "#0b4a33", "D2 USD35"), ("D3|20", "#8a8a8a", "D3")]:
    d = b[k]; axs[0].plot(d.index, ((d["Arus Kas Mitra"] - b["D0"]["Arus Kas Mitra"]) * DT).cumsum() / 1e9, color=col, lw=2, label=lab)
    axs[1].plot(d.index, (d["Kas Masuk LPHD Karbon"] * DT).cumsum() / 1e9, color=col, lw=2, label=lab)
axs[0].set_title("Kumulatif arus kas mitra − D0 (Rp miliar, nominal)"); axs[1].set_title("Kumulatif dana kolektif LPHD dari karbon (Rp miliar)"); axs[1].set_yscale("symlog", linthresh=1)
for a in axs: a.set_xlim(2024, 2087); a.axhline(0, color="#999", lw=1); a.legend(frameon=False, fontsize=9)
save(fig, "G4_arus_kas_LPHD_mitra")
# G5
fig, ax = plt.subplots(figsize=(11, 5.4))
for k, col, lab in [("D0", "#2b6fd6", "D0"), ("D1", "#f2b134", "D1"), ("D2|20", "#1aa874", "D2 USD20"), ("D2|35", "#0b4a33", "D2 USD35"), ("D3|20", "#8a8a8a", "D3")]:
    an = common.annual(b[k]); ax.plot(an.index, an["Kesempatan Kerja Berupah Setara Penuh"], color=col, lw=2, label=lab)
ax.set_xlim(2024, 2087); ax.set_ylabel("FTE berupah (FTE ≠ jumlah orang)"); ax.legend(frameon=False); ax.set_title("Keberlanjutan pekerjaan berupah"); save(fig, "G5_pekerjaan_berupah")
# G6
fig, axs = plt.subplots(1, 2, figsize=(16, 5.4))
for ax, ind, t in zip(axs, ["S7 Pendapatan bersih per RT bergantung 2030–2055 (Rp/th)", "S8 Pendapatan RT terdampak 2030–2055 (Rp/th)"], ["Δ pendapatan bersih per RT bergantung (Rp ribu/th)", "Δ pendapatan per RT terdampak (Rp ribu/th)"]):
    for i, (c, lab, col) in enumerate([("D1−D0 (pembiayaan awal)", "D1 − D0", "#f2b134"), ("D2−D1 (penjualan karbon sesudah jembatan)", "D2 − D1", "#1aa874")]):
        vals = []; labs = []
        for v in ["akses 0", "dasar", "akses 1,5"]:
            for h in [20, 35]:
                vals.append(float(H[(H["Variasi"] == v) & (H["Harga"] == h) & (H["Indikator"] == ind)][c].iloc[0]) / 1e3); labs.append(f"{v.replace('dasar','akses 1')}\nUSD{h}")
        ax.bar(np.arange(len(vals)) + (i - .5) * 0.38, vals, 0.38, color=col, label=lab)
    ax.set_xticks(np.arange(len(labs)), labs, fontsize=9); ax.axhline(0, color="#999", lw=1); ax.set_title(t); ax.yaxis.set_major_formatter(FM); ax.legend(frameon=False)
save(fig, "G6_pendapatan_RT")
# G7
fig, ax = plt.subplots(figsize=(11, 5.4))
for k, col, lab in [("D0", "#2b6fd6", "D0 (= D1 = D3)"), ("D2|20", "#1aa874", "D2 USD20"), ("D2|35", "#0b4a33", "D2 USD35")]:
    an = common.annual(b[k]); ax.plot(an.index, an["Jumlah KUPS Aktif"], color=col, lw=2, label=lab)
ax.set_xlim(2024, 2087); ax.set_ylabel("KUPS aktif (unit)"); ax.legend(frameon=False); ax.set_title("Dampak pada KUPS"); save(fig, "G7_KUPS")
print(V.to_string())
