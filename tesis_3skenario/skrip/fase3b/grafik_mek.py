import sys, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "fase3"); import common
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
O = sys.argv[1] + "/"; R = json.load(open("fase3b/mek_hasil.json")); DT = 0.0625
L = lambda k: pd.read_pickle(f"fase3b/runs/{k.replace('|','_')}.pkl")
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v))
NOTE = "Eksperimen akuntansi/pembiayaan pada S2. Asumsi kerja: k = 0,5; kas non-karbon 0. Verifikasi PySD; Vensim tertunda. NPV SEMENTARA. Kredit model ≠ kredit terverifikasi."
COL = {"A": "#e8692c", "B": "#8a8a8a", "C-J1": "#86d1b0", "C-JP": "#0b6b4a"}
# G10: kredit vs mitigasi tambahan thd S1
pr = [6, 10, 15, 20, 35]; FE = (1 - .1) * (1 - .12) * 0.682; s1 = L("S1"); es1 = float(s1["Emisi Deforestasi Biomassa"].iloc[:-1].sum() * DT)
fig, axs = plt.subplots(1, 2, figsize=(15, 5.4)); x = np.arange(5); w = 0.2
keys = {"A": "A|{}", "B": "B|{}", "C-J1": "C|{}|J1|d5|h0|m0", "C-JP": "C|{}|JP|d5|h0|m0"}
for i, (m, kf) in enumerate(keys.items()):
    kr = [R[kf.format(h)]["Kredit REDD diajukan (tCO2e)"] / 1e3 for h in pr]
    mit = [(es1 - float(L(kf.format(h))["Emisi Deforestasi Biomassa"].iloc[:-1].sum() * DT)) * FE / 1e3 for h in pr]
    axs[0].bar(x + (i - 1.5) * w, kr, w, color=COL[m], label=m)
    axs[0].scatter(x + (i - 1.5) * w, mit, marker="_", s=260, color="black", zorder=3, label="Mitigasi eligible terhadap S1" if i == 0 else None)
    axs[1].bar(x + (i - 1.5) * w, [R[kf.format(h)]["Deforestasi dihindari S2−S1 (ha)"] for h in pr], w, color=COL[m], label=m)
axs[0].set_title("Kredit REDD model vs mitigasi tambahan terhadap S1"); axs[0].set_ylabel("ribu tCO₂e, kumulatif")
axs[1].set_title("Deforestasi dihindari S2 − S1"); axs[1].set_ylabel("ha, kumulatif 2025–2086")
for ax in axs: ax.set_xticks(x, [f"USD {p}" for p in pr]); ax.yaxis.set_major_formatter(FM); ax.legend(frameon=False, fontsize=10)
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G10_mekanisme_kredit_vs_mitigasi.png", dpi=200); plt.close(fig)
# G11: dinamika USD 20 dan 35
fig, axs = plt.subplots(2, 3, figsize=(16, 8.4), sharex=True)
for row, h in enumerate([20, 35]):
    for m, kf in [("A", "A|{}"), ("C-J1", "C|{}|J1|d5|h0|m0"), ("C-JP", "C|{}|JP|d5|h0|m0")]:
        d = L(kf.format(h)); a = common.annual(d); y = a.index.values
        axs[row, 0].plot(y, (a["Hari Patroli Didanai Kas LPHD"] + a["Hari Patroli Didanai Jembatan"]), color=COL[m], lw=2, label=m)
        axs[row, 1].plot(y, a["Kas Penjualan Kredit"] / 1e9, color=COL[m], lw=2, label=m)
        cm = ((d["Arus Kas Mitra"] - s1["Arus Kas Mitra"]).iloc[:-1] * DT).cumsum() / 1e9
        axs[row, 2].plot(cm.index, cm.values, color=COL[m], lw=2, label=m)
    axs[row, 1].plot(y, common.annual(L(f"A|{h}"))["Biaya Transaksi dan MRV"] / 1e9, color="black", ls=":", lw=1.5, label="biaya MRV (A)")
    axs[row, 0].set_ylabel(f"USD {h}\nHOK/th"); axs[row, 1].set_ylabel("Rp miliar/th"); axs[row, 2].set_ylabel("Rp miliar (tak terdiskonto)"); axs[row, 2].axhline(0, color="#999", lw=1)
axs[0, 0].set_title("Patroli tambahan (kas LPHD + jembatan)"); axs[0, 1].set_title("Kas penjualan kredit"); axs[0, 2].set_title("Kumulatif arus kas mitra − S1")
for ax in axs.flat: ax.set_xlim(2024, 2087); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 0 if abs(v) >= 10 or v == 0 else 1)))
axs[0, 1].legend(frameon=False, fontsize=10)
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G11_dinamika_mekanisme_USD20_35.png", dpi=200); plt.close(fig)
# G12: ambang harga siklus mandiri (C, jembatan 5 th)
fig, ax = plt.subplots(figsize=(10, 5.2)); hs = [20, 22.5, 25, 27.5, 30, 32.5, 35]
for m, j in [("C-J1", "J1"), ("C-JP", "JP")]:
    v = []
    for h in hs:
        k = f"C|{h}|{j}|d5|h0|m0" if h in (20, 35) else f"Th-C-{j}-d5|{h}"
        a = common.annual(L(k)); v.append(a["Hari Patroli Didanai Kas LPHD"].loc[2060:2080].mean())
    ax.plot(hs, v, marker="o", color=COL[m], lw=2, label=m)
ax.axhline(6490.7, color="#999", ls=":", label="Kebutuhan patroli tambahan (6.491 HOK/th)")
ax.set_xlabel("Harga kredit REDD (USD/tCO₂e)"); ax.set_ylabel("Patroli didanai kas LPHD, rerata 2060–2080 (HOK/th)"); ax.yaxis.set_major_formatter(FM)
ax.set_title("Mekanisme C: patroli yang bertahan setelah jembatan 2026–2030 berakhir"); ax.legend(frameon=False, fontsize=11)
fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(O + "G12_ambang_harga_siklus_mandiri.png", dpi=200); plt.close(fig)
print("ok")
