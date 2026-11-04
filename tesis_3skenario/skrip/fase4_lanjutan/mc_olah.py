import sys, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.stats import rankdata
sys.path.insert(0, "fase5"); from mc import PAR, SEED, N
OUTX, OUTG = sys.argv[1], sys.argv[2]
R = pd.read_pickle("fase5/mc_hasil.pkl"); X = pd.read_csv("fase5/mc_sampel.csv")
err = R[R["galat"] != ""]; R = R[R["galat"] == ""].copy()
CEKTOL = 1e-6
R["pasangan_setara"] = (R["_cek_hutan_ref"] <= CEKTOL) & (R["_cek_emisi_ref"] <= CEKTOL)
# kriteria proporsi (ditetapkan sebelum melihat hasil)
CRIT = {
 "1 Tambahan perlindungan hutan S2−S1 (deforestasi dihindari > 0)": lambda d: d["Deforestasi dihindari S2−S1 (ha)"] > 0,
 "2a Manfaat karbon bersih kumulatif 2087 > 0": lambda d: d["Manfaat karbon bersih kumulatif 2087 (tCO2e)"] > 0,
 "2b …dan tidak turun > 10 % dari puncaknya": lambda d: (d["Manfaat karbon bersih kumulatif 2087 (tCO2e)"] > 0) & (d["Manfaat karbon bersih kumulatif 2087 (tCO2e)"] >= 0.9 * d["Puncak manfaat karbon bersih (tCO2e)"]),
 "3a Kas LPHD masih mengalir 2075–2086 (rerata > 0)": lambda d: d["Kas LPHD rerata 2075–2086 (Rp/th)"] > 1,
 "3b Cakupan kebutuhan minimum LPHD 2060–2086 ≥ 50 %": lambda d: d["Cakupan kebutuhan minimum 2060–2086 (%)"] >= 50,
 "4a NPV inkremental proyek > 0 [SEMENTARA]": lambda d: d["NPV inkremental proyek [SEMENTARA] (Rp)"] > 0,
 "4b NPV mitra inkremental > 0 [SEMENTARA]": lambda d: d["NPV mitra inkremental [SEMENTARA] (Rp)"] > 0,
 "5a Pendapatan bersih RT bergantung NAIK (Δ > 0)": lambda d: d["Δ pendapatan bersih per RT bergantung (Rp/th)"] > 0,
 "5b Pendapatan bersih RT bergantung TURUN (Δ < 0)": lambda d: d["Δ pendapatan bersih per RT bergantung (Rp/th)"] < 0,
 "5c Pendapatan RT terdampak NAIK (Δ > 0)": lambda d: d["Δ pendapatan per RT terdampak (Rp/th)"] > 0,
 "6 KUPS aktif 2087 ≥ 90 % KUPS aktif 2026 (S2)": lambda d: d["KUPS aktif 2087 S2"] >= 0.9 * d["KUPS aktif 2026 S2"],
 "6b (pembanding) KUPS aktif 2087 ≥ 90 % 2026 pada S1": lambda d: d["KUPS aktif 2087 S1"] >= 0.9 * d["KUPS aktif 2026 S2"],
 "7 Kerja berupah tambahan bertahan 2060–2086 (Δ FTE > 0,5)": lambda d: d["Δ FTE berupah 2060–2086"] > 0.5}
OUT = [c for c in R.columns if c not in ("sampel", "harga", "galat", "pasangan_setara") and not c.startswith("_")]
summ, prop, prcc = [], [], []
def PRCC(Xm, y):
    Xr = np.column_stack([rankdata(Xm[:, j]) for j in range(Xm.shape[1])]); yr = rankdata(y); out = []
    for j in range(Xm.shape[1]):
        o = np.delete(Xr, j, axis=1); A = np.column_stack([np.ones(len(yr)), o])
        rx = Xr[:, j] - A @ np.linalg.lstsq(A, Xr[:, j], rcond=None)[0]; ry = yr - A @ np.linalg.lstsq(A, yr, rcond=None)[0]
        out.append(float(np.corrcoef(rx, ry)[0, 1]) if np.std(ry) > 0 and np.std(rx) > 0 else np.nan)
    return out
KEY = ["Deforestasi dihindari S2−S1 (ha)", "Manfaat karbon bersih kumulatif 2087 (tCO2e)", "Kas LPHD rerata 2075–2086 (Rp/th)", "Cakupan kebutuhan minimum 2060–2086 (%)",
       "NPV inkremental proyek [SEMENTARA] (Rp)", "NPV mitra inkremental [SEMENTARA] (Rp)", "Δ pendapatan bersih per RT bergantung (Rp/th)", "Δ pendapatan per RT terdampak (Rp/th)",
       "Δ FTE berupah 2030–2055", "Δ FTE berupah 2060–2086", "KUPS aktif 2087 S2", "Debit reversal belum diselesaikan 2087 (tCO2e)"]
for h in [10, 20, 35]:
    d = R[R["harga"] == h].sort_values("sampel")
    for c in OUT:
        v = d[c].astype(float); summ.append({"Harga": h, "Indikator": c, "Median": v.median(), "P5": v.quantile(.05), "P25": v.quantile(.25), "P75": v.quantile(.75), "P95": v.quantile(.95), "Rerata": v.mean(), "n": int(v.notna().sum())})
    for k, f in CRIT.items(): prop.append({"Harga": h, "Kriteria": k, "Proporsi ensembel (%)": 100 * float(f(d).mean()), "n": len(d)})
    Xm = X.iloc[d["sampel"].values].values
    for c in KEY:
        y = d[c].astype(float).values
        if np.nanstd(y) == 0: continue
        for (pn, *_), r in zip(PAR, PRCC(Xm, y)): prcc.append({"Harga": h, "Indikator": c, "Parameter": pn, "PRCC": r})
S, Pp, PR = pd.DataFrame(summ), pd.DataFrame(prop), pd.DataFrame(prcc)
cek = R.groupby("harga").agg(pasangan=("sampel", "count"), setara=("pasangan_setara", "sum"), galat_hutan_maks=("_cek_hutan_ref", "max"), galat_emisi_maks=("_cek_emisi_ref", "max"), arus_kas_maks=("_cek_arus_kas", "max")).reset_index()
W = pd.ExcelWriter(OUTX, engine="openpyxl")
pd.DataFrame({"Isi": [f"MONTE CARLO LHS BERPASANGAN S1–S2 – MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl; N = {N} sampel; seed {SEED}; harga USD 10/20/35 (S1 sekali per sampel, S2 tiga kali dengan masukan referensi S1 identik).",
 "S2 = mekanisme C (kredit konservatif endogen, Referensi S1 berpasangan; aturan reversal 2). Jembatan J1/JP bukan komitmen mitra; besaran dan durasi disampel.",
 "Frekuensi/proporsi ensembel BUKAN probabilitas empiris: bergantung pada rentang dan bentuk distribusi asumsi (lembar 1).",
 "STATUS: PySD saja; Vensim native BELUM DIVERIFIKASI. NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Aturan reversal = asumsi model. Kredit model ≠ kredit terverifikasi.",
 "Upah patroli Rp150.000/HOK tetap; biaya total per HOK disampel Rp150.000–300.000 (biaya ≥ upah).",
 "PRCC = korelasi parsial berbasis peringkat; |PRCC| besar = parameter berpengaruh kuat secara monoton, dengan parameter lain dikendalikan."]}).to_excel(W, sheet_name="0 README", index=False)
pd.DataFrame([{"Parameter": p[0], "Distribusi": {"U": "Uniform", "T": "Segitiga"}[p[1]], "Min": p[2], "Maks": p[3], "Modus": p[4], "Nilai dasar": p[5], "Dasar/kelas": p[6]} for p in PAR]).to_excel(W, sheet_name="1 Distribusi parameter", index=False)
X.to_excel(W, sheet_name="2 Sampel LHS", index_label="sampel")
cek.to_excel(W, sheet_name="3 Cek pasangan", index=False)
pd.DataFrame([{"Catatan": f"Run gagal: {len(err)} baris"}] + [{"Catatan": f"sampel {r.sampel} USD{r.harga}: {r.galat}"} for r in err.itertuples()]).to_excel(W, sheet_name="3 Cek pasangan", startrow=len(cek) + 3, index=False)
S.to_excel(W, sheet_name="4 Ringkasan median P5-P95", index=False); Pp.to_excel(W, sheet_name="5 Proporsi ensembel", index=False)
PR.pivot_table(index=["Harga", "Parameter"], columns="Indikator", values="PRCC").to_excel(W, sheet_name="6 PRCC")
R.drop(columns=["galat"]).to_excel(W, sheet_name="7 Hasil per sampel", index=False)
W.close()
S.to_pickle("fase5/mc_summ.pkl"); Pp.to_pickle("fase5/mc_prop.pkl"); PR.to_pickle("fase5/mc_prcc.pkl"); cek.to_pickle("fase5/mc_cek.pkl")
# ---------- grafik
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 0 if abs(v) >= 10 or v == 0 else 1))
NOTE = f"Monte Carlo LHS berpasangan, N = {N}, seed {SEED}. Proporsi ensembel ≠ probabilitas. PySD; Vensim native belum. NPV SEMENTARA."
def save(fig, n): fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{OUTG}/{n}.png", dpi=200); plt.close(fig)
fig, axs = plt.subplots(2, 3, figsize=(16, 8.8))
for ax, (c, sc, t) in zip(axs.flat, [("Deforestasi dihindari S2−S1 (ha)", 1, "Deforestasi dihindari S2−S1 (ha)"), ("Manfaat karbon bersih kumulatif 2087 (tCO2e)", 1e3, "Manfaat karbon bersih 2087 (ribu tCO₂e)"),
        ("Cakupan kebutuhan minimum 2060–2086 (%)", 1, "Cakupan kebutuhan LPHD 2060–2086 (%)"), ("NPV mitra inkremental [SEMENTARA] (Rp)", 1e9, "NPV mitra inkremental (Rp miliar) [SEMENTARA]"),
        ("Δ pendapatan bersih per RT bergantung (Rp/th)", 1e3, "Δ pendapatan bersih per RT (Rp ribu/th)"), ("Δ FTE berupah 2030–2055", 1, "Δ FTE berupah 2030–2055")]):
    data = [R[R["harga"] == h][c].astype(float).values / sc for h in [10, 20, 35]]
    bp = ax.boxplot(data, whis=(5, 95), showfliers=False, patch_artist=True, widths=0.55)
    for b, col in zip(bp["boxes"], ["#b9e3cf", "#1aa874", "#0b4a33"]): b.set_facecolor(col)
    for m in bp["medians"]: m.set_color("black")
    ax.axhline(0, color="#999", lw=1); ax.set_xticks([1, 2, 3], ["USD 10", "USD 20", "USD 35"]); ax.set_title(t, fontsize=12); ax.yaxis.set_major_formatter(FM)
save(fig, "M1_sebaran_hasil_MC")
pv = PR[PR["Harga"] == 20].pivot_table(index="Parameter", columns="Indikator", values="PRCC")[KEY[:10]]
fig, ax = plt.subplots(figsize=(15, 9)); im = ax.imshow(pv.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_yticks(range(len(pv.index)), [p.replace(" (Tingkat Keberlanjutan Patroli Reguler)", "") for p in pv.index], fontsize=10)
ax.set_xticks(range(len(pv.columns)), [c.replace(" [SEMENTARA]", "*").replace(" (Rp/th)", "").replace(" (Rp)", "").replace(" (tCO2e)", "").replace(" (ha)", "").replace(" (%)", "") for c in pv.columns], rotation=35, ha="right", fontsize=10)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        v = pv.values[i, j]
        if v == v and abs(v) >= 0.2: ax.text(j, i, fmt(v, 2), ha="center", va="center", fontsize=8, color="white" if abs(v) > 0.6 else "black")
fig.colorbar(im, ax=ax, fraction=0.03); ax.set_title("PRCC, USD 20 (angka ditampilkan bila |PRCC| ≥ 0,20; * = SEMENTARA)"); ax.grid(False); save(fig, "M2_PRCC_USD20")
fig, ax = plt.subplots(figsize=(14, 7)); ks = list(CRIT); y = np.arange(len(ks)); w = 0.27
for i, (h, col) in enumerate([(10, "#b9e3cf"), (20, "#1aa874"), (35, "#0b4a33")]):
    ax.barh(y + (i - 1) * w, [Pp[(Pp["Harga"] == h) & (Pp["Kriteria"] == k)]["Proporsi ensembel (%)"].iloc[0] for k in ks], w, color=col, label=f"USD {h}")
ax.set_yticks(y, ks, fontsize=10); ax.invert_yaxis(); ax.set_xlabel("Proporsi ensembel (%), bukan probabilitas"); ax.set_xlim(0, 100); ax.legend(frameon=False); save(fig, "M3_proporsi_ensembel")
print(cek.to_string()); print(len(err), "galat")
print(Pp.pivot_table(index="Kriteria", columns="Harga", values="Proporsi ensembel (%)").round(1).to_string())
print(S[S["Indikator"].isin(KEY)].pivot_table(index="Indikator", columns="Harga", values=["Median", "P5", "P95"]).round(1).to_string())
