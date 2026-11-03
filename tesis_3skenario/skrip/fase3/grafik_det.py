import sys, json, pickle, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "fase3"); from common import *
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
runs = pickle.load(open("fase3/det_runs.pkl", "rb")); S = json.load(open("fase3/det_summary.json"))
O = sys.argv[1] + "/"
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v))
C = {"S1": "#2b6fd6", "S2 USD10": "#86d1b0", "S2 USD20": "#1aa874", "S2 USD35": "#0b6b4a", "baseline": "#8a8a8a"}
an = {k: annual(d) for k, d in runs.items()}; yrs = an["S1"].index.values
NOTE = "Asumsi kerja: k = 0,5; kas non-karbon 0; hibah. Verifikasi PySD; Vensim tertunda."
# G1 hutan
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(yrs, an["S1"]["Total Hutan Baseline"] / 1000, ls=":", color=C["baseline"], lw=2, label="Baseline referensi karbon (tanpa PS)")
for k in ["S1", "S2 USD10", "S2 USD20", "S2 USD35"]: ax.plot(yrs, an[k]["Total Hutan"] / 1000, color=C[k], lw=2.4, ls="--" if k == "S1" else "-", label={"S1": "S1 PS pembiayaan terbatas"}.get(k, k.replace("USD", "USD ")))
ax.set_xlim(2024, 2087); ax.set_ylabel("Luas hutan (ribu ha)"); ax.legend(frameon=False, fontsize=11); ax.set_title("Lintasan tutupan hutan 2024–2087"); ax.yaxis.set_major_formatter(FM)
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G1_lintasan_hutan.png", dpi=200); plt.close(fig)
# G2 dihindari S2-S1 vs baseline credits
pr = [6, 10, 15, 20, 35]; x = np.arange(5); s1 = S["S1"]
dav = [s1["Emisi deforestasi biomassa kumulatif (tCO2e)"] - S[f"S2 USD{p}"]["Emisi deforestasi biomassa kumulatif (tCO2e)"] for p in pr]
bau = [S[f"S2 USD{p}"]["Potensi kredit REDD vs baseline BAU (tCO2e)"] for p in pr]; kon = [S[f"S2 USD{p}"]["Potensi kredit REDD konservatif (pelaporan, tCO2e)"] for p in pr]
fig, ax = plt.subplots(figsize=(10, 5.2)); w = 0.27
ax.bar(x - w, np.array(dav) / 1000, w, color="#1aa874", label="Emisi deforestasi dihindari S2 − S1 (fisik)")
ax.bar(x, np.array(kon) / 1000, w, color="#86d1b0", label="Potensi kredit REDD konservatif (di atas S1)")
ax.bar(x + w, np.array(bau) / 1000, w, color="#e8692c", label="Potensi kredit REDD terhadap baseline BAU")
ax.set_xticks(x, [f"USD {p}" for p in pr]); ax.set_ylabel("ribu tCO₂e, kumulatif"); ax.legend(frameon=False, fontsize=11); ax.yaxis.set_major_formatter(FM)
ax.set_title("Dampak S2 − S1 vs potensi kredit terhadap baseline (bukan kredit terverifikasi)")
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G2_dampak_vs_kredit.png", dpi=200); plt.close(fig)
# G3 kronologi kas
fig, axs = plt.subplots(1, 3, figsize=(15, 4.8), sharey=False)
for ax, h in zip(axs, [10, 20, 35]):
    a = an[f"S2 USD{h}"]; r = slice(2024, 2045)
    ax.plot(a.loc[r].index, a.loc[r, "Kas Penjualan Kredit"] / 1e9, color="#2b6fd6", lw=2, label="Kas penjualan kredit")
    ax.plot(a.loc[r].index, a.loc[r, "Biaya Transaksi dan MRV"] / 1e9, color="#e8692c", lw=2, ls="--", label="Biaya MRV, transaksi, pajak")
    ax.plot(a.loc[r].index, a.loc[r, "Kas Masuk LPHD Karbon"] / 1e9, color="#1aa874", lw=2.4, label="Kas masuk LPHD (60 %)")
    ax.set_title(f"USD {h}/tCO₂e"); ax.set_ylabel("Rp miliar/th")
axs[0].legend(frameon=False, fontsize=10); fig.suptitle("Kronologi kas karbon: penjualan 2028, MRV ditalangi mitra, kas LPHD menyusul", fontsize=13)
fig.tight_layout(); fig.savefig(O + "G3_kronologi_kas.png", dpi=200); plt.close(fig)
# G4 LPHD
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(yrs, an["S1"]["Kebutuhan Dana Minimum"] / 1e9, color="#e8692c", lw=2, ls="--", label="Kebutuhan minimum LPHD")
for k in ["S2 USD10", "S2 USD20", "S2 USD35"]: ax.plot(yrs, an[k]["Penggunaan Dana Pengelolaan"] / 1e9, color=C[k], lw=2.2, label=f"Belanja LPHD {k.replace('USD', 'USD ')}")
ax.plot(yrs, an["S1"]["Penggunaan Dana Pengelolaan"] / 1e9, color=C["S1"], lw=2, ls="--", label="Belanja LPHD S1 (kas non-karbon 0)")
ax.set_xlim(2024, 2087); ax.set_ylabel("Rp miliar/th"); ax.legend(frameon=False, fontsize=10); ax.set_title("Belanja LPHD vs kebutuhan minimum")
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G4_kecukupan_LPHD.png", dpi=200); plt.close(fig)
# G5 patroli
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
for k in ["S1", "S2 USD10", "S2 USD20", "S2 USD35"]:
    axs[0].plot(yrs, an[k]["Total HOK Patroli"], color=C[k], lw=2.2, ls="--" if k == "S1" else "-", label=k.replace("USD", "USD "))
    axs[1].plot(yrs, an[k]["Indeks Intensitas Perlindungan"], color=C[k], lw=2.2, ls="--" if k == "S1" else "-", label=k.replace("USD", "USD "))
axs[0].set_title("Total patroli (historis 2024–2025, reguler, tambahan kas)"); axs[0].set_ylabel("HOK/th"); axs[0].yaxis.set_major_formatter(FM)
axs[1].set_title("Intensitas perlindungan"); axs[0].legend(frameon=False)
for a_ in axs: a_.set_xlim(2024, 2087)
fig.text(0.01, 0.005, NOTE + " Patroli reguler pasca-2025 = asumsi eksploratif.", fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G5_patroli.png", dpi=200); plt.close(fig)
# G6 sosial ekonomi
fig, axs = plt.subplots(1, 3, figsize=(16, 4.8)); ks = ["S1", "S2 USD10", "S2 USD20", "S2 USD35"]; lab = ["S1", "USD 10", "USD 20", "USD 35"]
axs[0].bar(lab, [S[k]["FTE berupah rerata 2030–2055"] for k in ks], color="#1aa874", label="berupah"); axs[0].bar(lab, [S[k]["FTE sukarela rerata 2030–2055"] for k in ks], bottom=[S[k]["FTE berupah rerata 2030–2055"] for k in ks], color="#c2e8d6", label="sukarela (non-tunai)")
axs[0].set_title("Pekerja setara penuh, rerata 2030–2055"); axs[0].legend(frameon=False)
for k in ks: axs[1].plot(yrs, an[k]["Jumlah KUPS Aktif"], color=C[k], lw=2.2, ls="--" if k == "S1" else "-", label=k.replace("USD", "USD "))
axs[1].set_title("KUPS aktif (reaktivasi Rp 50 juta, reinvestasi 0,5: D)"); axs[1].legend(frameon=False, fontsize=10); axs[1].set_xlim(2024, 2087)
w = 0.38; xx = np.arange(4)
axs[2].bar(xx - w/2, [S[k]["Pendapatan program per RT rerata (Rp/RT/th)"] / 1000 for k in ks], w, color="#1aa874", label="Pendapatan program per RT")
axs[2].bar(xx + w/2, [S[k]["Kehilangan akses per RT rerata (Rp/RT/th)"] / 1000 for k in ks], w, color="#e8692c", label="Kehilangan akses per RT (asumsi)")
axs[2].set_xticks(xx, lab); axs[2].set_ylabel("ribu Rp/RT/th"); axs[2].legend(frameon=False, fontsize=10); axs[2].set_title("Neraca manfaat–beban per RT")
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G6_sosial_ekonomi.png", dpi=200); plt.close(fig)
print("ok")
