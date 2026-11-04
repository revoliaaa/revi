import sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "fase3"); import common
R = pd.read_pickle("fase4t3/det_runs.pkl"); S = pd.read_pickle("fase4t3/ringkasan.pkl"); D = pd.read_pickle("fase4t3/selisih.pkl")
OUTX, OUTG = sys.argv[1], sys.argv[2]
clean = lambda x: 0.0 if isinstance(x, float) and x == x and abs(x) < 1e-3 else x
W = pd.ExcelWriter(OUTX, engine="openpyxl")
pd.DataFrame({"Isi": ["HASIL SIMULASI DETERMINISTIK FINAL – Fase 4 Tahap 3 – MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl (md5 639083f9…), 2026-11-04",
 "Dua skenario kebijakan: S1 = PS dengan pembiayaan terbatas; S2 = PS dengan perdagangan karbon. Mekanisme C (kredit konservatif endogen terhadap Referensi S1 + pembiayaan jembatan) adalah konfigurasi utama S2: J1 = Rp782,86 juta/th 2026–2030; JP = kebutuhan patroli tambahan penuh 2026–2030. Mekanisme A (baseline BAU) hanya pembanding eksploratif.",
 "Protokol: Referensi S1 berpasangan (7 masukan dari run S1 mandiri dengan parameter identik). Aturan penyelesaian reversal 2 (buffer → pembatalan stok → pengganti, pada verifikasi 5 tahunan). Biaya modal 0; pemulihan talangan sebelum bagi hasil; aturan henti MRV nonaktif.",
 "Asumsi kerja kelas D (bukan data): k = 0,5; efektivitas 0,37; kas non-karbon 0; dukungan material rehabilitasi 0; biaya patroli total Rp260.000/HOK (upah Rp150.000 terkonfirmasi); biaya MRV; KUPS reaktivasi Rp50 juta dan reinvestasi 0,5; pengali kehilangan akses 1; jembatan J1/JP bukan komitmen aktual mitra.",
 "STATUS: terverifikasi PySD; Vensim native BELUM DIVERIFIKASI. NPV SEMENTARA (tanpa biaya pengembangan dan material aktual). Kredit model ≠ kredit terverifikasi/VCU. FTE ≠ jumlah orang; dana LPHD ≠ pendapatan RT; omzet ≠ penerimaan anggota. Tidak ada klaim kemiskinan/ketimpangan.",
 "Konvensi: kumulatif 2024–2086 (keuangan/kredit) atau 2025–2086 (fisik); rerata tahunan 2030–2055 kecuali disebut; Rp nominal kecuali NPV; awalan indikator: E ekologi, F pembiayaan, L kelembagaan LPHD, S sosial-ekonomi."]}).to_excel(W, sheet_name="0 README", index=False)
S.map(clean).to_excel(W, sheet_name="1 Ringkasan per run")
D.map(clean).to_excel(W, sheet_name="2 Selisih S2−S1")
yrs = [2026, 2028, 2030, 2032, 2035, 2040, 2045, 2050, 2055, 2060, 2070, 2080, 2087]
V = ["Total Hutan", "Deforestasi Total", "Emisi Deforestasi Biomassa", "Kredit REDD Diajukan", "Kas Penjualan Kredit", "Biaya Transaksi dan MRV", "Kas Masuk LPHD Karbon", "Penggunaan Dana Pengelolaan",
     "Rasio Cakupan Kebutuhan Minimum", "Hari Patroli Didanai Jembatan", "Hari Patroli Didanai Kas LPHD", "HOK Berupah PS", "Kesempatan Kerja Berupah Setara Penuh", "Upah Kegiatan PS", "Jumlah KUPS Aktif",
     "Pendapatan KUPS Total", "Pendapatan Program per RT Bergantung", "Kehilangan Pendapatan Pembatasan Akses per RT", "Pendapatan Bersih per RT Bergantung", "Indeks Kapasitas LPHD", "Saldo Mitigasi REDD Belum Dikreditkan", "Defisit Biaya Bersama Belum Dipulihkan"]
rows = []
for k in [("S1", 0)] + [(m, h) for m in ["C-J1", "C-JP"] for h in [10, 20, 35]]:
    an = common.annual(R[k])
    for v in V:
        rows.append(dict({"Run": "S1" if k[0] == "S1" else f"{k[0]} USD{k[1]}", "Variabel": v}, **{str(y): clean(float(an[v].loc[min(y, 2087)])) for y in yrs}))
pd.DataFrame(rows).to_excel(W, sheet_name="3 Lintasan tahunan", index=False)
pd.DataFrame([
 {"Parameter": "Tingkat Keberlanjutan Patroli Reguler (k)", "Nilai": 0.5, "Status": "Asumsi kerja kelas D; rentang 0–1 di MC"},
 {"Parameter": "Upah Harian Patroli Berbayar", "Nilai": 150000, "Status": "Dikonfirmasi peneliti"},
 {"Parameter": "Biaya per Hari Patroli", "Nilai": 260000, "Status": "Asumsi kerja; belum terverifikasi sebagai biaya total"},
 {"Parameter": "Besaran Pembiayaan Jembatan (J1)", "Nilai": 782860000, "Status": "Eksperimen; bukan komitmen mitra"},
 {"Parameter": "Durasi jembatan", "Nilai": 5, "Status": "Eksperimen"},
 {"Parameter": "Aturan Penyelesaian Reversal", "Nilai": 2, "Status": "Asumsi model; tanpa dasar kontraktual"},
 {"Parameter": "Proporsi Buffer Risiko Karbon", "Nilai": 0.12, "Status": "Asumsi; tidak dari penilaian risiko standar"},
 {"Parameter": "Biaya Monitoring per Ha per Tahun / Verifikasi per Kejadian", "Nilai": "1.980 / 742.500.000", "Status": "Asumsi kelas D"},
 {"Parameter": "Pengali Kehilangan Akses", "Nilai": 1, "Status": "Asumsi kelas D; uji 0"},
 {"Parameter": "Upah Harian Pengendalian Kebakaran", "Nilai": 130000, "Status": "Belum dikonfirmasi"},
 {"Parameter": "Kas non-karbon; dukungan material rehabilitasi", "Nilai": 0, "Status": "Tidak ada sumber terdokumentasi"}]).to_excel(W, sheet_name="4 Register asumsi", index=False)
W.close()
# ---------------- grafik
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 0 if abs(v) >= 10 or v == 0 else 1))
NOTE = "S2 = mekanisme C, Referensi S1 berpasangan. Asumsi kerja: k = 0,5; kas non-karbon 0. Verifikasi PySD; Vensim native belum. NPV SEMENTARA."
COL = {"S1": "#2b6fd6", "C-J1": "#86d1b0", "C-JP": "#0b6b4a", "A": "#e8692c"}
H = [6, 10, 15, 20, 35]; x = np.arange(5); w = 0.38
an = {k: common.annual(d) for k, d in R.items()}
def save(fig, n): fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{OUTG}/{n}.png", dpi=200); plt.close(fig)
# F1 ekologi
fig, axs = plt.subplots(1, 2, figsize=(15, 5.4))
for i, m in enumerate(["C-J1", "C-JP"]):
    axs[0].bar(x + (i - .5) * w, [-D.loc["E Deforestasi kumulatif 2025–2086 (ha)", f"{m}|{h}"] for h in H], w, color=COL[m], label=m)
    axs[1].bar(x + (i - .5) * w, [-D.loc["E Emisi deforestasi biomassa kumulatif (tCO2e)", f"{m}|{h}"] / 1e3 for h in H], w, color=COL[m], label=m)
axs[0].set_title("Deforestasi dihindari S2 − S1 (ha, 2025–2086)"); axs[1].set_title("Emisi deforestasi dihindari S2 − S1 (ribu tCO₂e)")
for a in axs: a.set_xticks(x, [f"USD {h}" for h in H]); a.yaxis.set_major_formatter(FM); a.legend(frameon=False)
save(fig, "F1_ekologi_S2_S1")
# F2 lintasan patroli tambahan dan kas LPHD
fig, axs = plt.subplots(1, 2, figsize=(15, 5.4))
for m, ls in [("C-J1", "-"), ("C-JP", "--")]:
    for h, c in [(10, "#b9e3cf"), (20, "#1aa874"), (35, "#0b4a33")]:
        a = an[(m, h)]; y = a.index.values
        axs[0].plot(y, a["Hari Patroli Didanai Jembatan"] + a["Hari Patroli Didanai Kas LPHD"], color=c, ls=ls, lw=2, label=f"{m} USD{h}")
        axs[1].plot(y, a["Kas Masuk LPHD Karbon"] / 1e9, color=c, ls=ls, lw=2, label=f"{m} USD{h}")
axs[0].set_title("Patroli tambahan (jembatan + kas LPHD), HOK/th"); axs[1].set_title("Kas LPHD dari karbon (Rp miliar/th)")
for a in axs: a.set_xlim(2024, 2087); a.yaxis.set_major_formatter(FM)
axs[0].legend(frameon=False, fontsize=9, ncol=2); save(fig, "F2_patroli_kas_LPHD")
# F3 keuangan
fig, axs = plt.subplots(1, 2, figsize=(15, 5.4))
for i, m in enumerate(["C-J1", "C-JP"]):
    axs[0].bar(x + (i - .5) * w, [S.loc["F NPV mitra (Rp) [SEMENTARA]", f"{m}|{h}"] / 1e9 - S.loc["F NPV mitra (Rp) [SEMENTARA]", "S1"] / 1e9 for h in H], w, color=COL[m], label=m)
    axs[1].bar(x + (i - .5) * w, [S.loc["L Cakupan kebutuhan minimum LPHD rerata 2030–2055 (%)", f"{m}|{h}"] for h in H], w, color=COL[m], label=m)
axs[0].axhline(0, color="#999", lw=1); axs[0].set_title("NPV mitra inkremental thd S1 (Rp miliar) [SEMENTARA]"); axs[1].set_title("Cakupan kebutuhan minimum LPHD 2030–2055 (%)")
for a in axs: a.set_xticks(x, [f"USD {h}" for h in H]); a.yaxis.set_major_formatter(FM); a.legend(frameon=False)
save(fig, "F3_keuangan_LPHD")
# F4 kerja dan KUPS
fig, axs = plt.subplots(1, 2, figsize=(15, 5.4))
for i, m in enumerate(["C-J1", "C-JP"]):
    axs[0].bar(x + (i - .5) * w, [D.loc["S FTE berupah", f"{m}|{h}"] for h in H], w, color=COL[m], label=f"{m} 2030–2055")
    axs[0].scatter(x + (i - .5) * w, [D.loc["S FTE berupah rerata 2060–2086", f"{m}|{h}"] for h in H], color="black", marker="_", s=250, zorder=3, label="2060–2086" if i == 0 else None)
    axs[1].bar(x + (i - .5) * w, [D.loc["S Penerimaan anggota KUPS (Rp/th)", f"{m}|{h}"] / 1e6 for h in H], w, color=COL[m], label=m)
axs[0].set_title("Δ FTE berupah S2 − S1 (FTE ≠ jumlah orang)"); axs[1].set_title("Δ penerimaan anggota KUPS (Rp juta/th, 2030–2055)")
for a in axs: a.set_xticks(x, [f"USD {h}" for h in H]); a.yaxis.set_major_formatter(FM); a.legend(frameon=False)
save(fig, "F4_kerja_KUPS")
# F5 dekomposisi pendapatan RT
fig, ax = plt.subplots(figsize=(12, 5.4)); cats = [("S Pendapatan hutan per RT (Rp/th)", "pendapatan hutan", "#1aa874", 1), ("S Pendapatan program per RT (Rp/th)", "pendapatan program", "#86d1b0", 1), ("S Kehilangan akses per RT bergantung (Rp/th)", "kehilangan akses", "#e8692c", -1)]
lab = [f"{m}\nUSD{h}" for m in ["C-J1", "C-JP"] for h in [10, 20, 35]]; xx = np.arange(len(lab))
for j, (r, n, c, sg) in enumerate(cats):
    ax.bar(xx + (j - 1) * 0.26, [sg * D.loc[r, f"{m}|{h}"] / 1e3 for m in ["C-J1", "C-JP"] for h in [10, 20, 35]], 0.26, color=c, label=n)
ax.scatter(xx, [D.loc["S Pendapatan bersih per RT bergantung (Rp/th)", f"{m}|{h}"] / 1e3 for m in ["C-J1", "C-JP"] for h in [10, 20, 35]], color="black", zorder=3, label="Δ pendapatan bersih")
ax.axhline(0, color="#999", lw=1); ax.set_xticks(xx, lab); ax.set_ylabel("Δ Rp ribu per RT bergantung per tahun (2030–2055)"); ax.yaxis.set_major_formatter(FM); ax.legend(frameon=False)
ax.set_title("Dekomposisi Δ pendapatan rumah tangga bergantung hutan (S2 − S1); kompensasi = 0 di model utama"); save(fig, "F5_pendapatan_RT")
print("ok")
