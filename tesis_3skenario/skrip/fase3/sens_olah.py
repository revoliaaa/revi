import json, sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = json.load(open("fase3/sens_hasil.json")); OUT, GD = sys.argv[1], sys.argv[2]
IND = {  # nama: fungsi(S1, S2) per harga
 "Deforestasi dihindari S2−S1 (ha)": lambda a, b: a["Deforestasi kumulatif 2025–2086 (ha)"] - b["Deforestasi kumulatif 2025–2086 (ha)"],
 "Emisi deforestasi dihindari S2−S1 (ribu tCO2e)": lambda a, b: (a["Emisi deforestasi biomassa kumulatif (tCO2e)"] - b["Emisi deforestasi biomassa kumulatif (tCO2e)"]) / 1e3,
 "NPV inkremental [SEMENTARA] (Rp miliar)": lambda a, b: b["NPV inkremental karbon (Rp) [SEMENTARA]"] / 1e9,
 "NPV mitra [SEMENTARA] (Rp miliar)": lambda a, b: b["NPV mitra (Rp) [SEMENTARA]"] / 1e9,
 "Cakupan kebutuhan minimum S2 (%)": lambda a, b: b["Cakupan kebutuhan minimum rerata 2030–2055 (%)"],
 "Δ FTE berupah S2−S1": lambda a, b: b["FTE berupah rerata 2030–2055"] - a["FTE berupah rerata 2030–2055"],
 "Δ pendapatan bersih per RT S2−S1 (Rp)": lambda a, b: b["Pendapatan bersih per RT bergantung rerata (Rp/RT/th)"] - a["Pendapatan bersih per RT bergantung rerata (Rp/RT/th)"],
 "Potensi kredit REDD BAU (ribu tCO2e)": lambda a, b: b["Potensi kredit REDD vs baseline BAU (tCO2e)"] / 1e3,
 "Porsi kredit BAU dari perlindungan tingkat S1 (%)": lambda a, b: 100 * (1 - b["Potensi kredit REDD konservatif (pelaporan, tCO2e)"] / b["Potensi kredit REDD vs baseline BAU (tCO2e)"]) if b["Potensi kredit REDD vs baseline BAU (tCO2e)"] > 1 else np.nan,
 "KUPS 2087 S2": lambda a, b: b["KUPS aktif 2087"]}
S1IND = {"Hutan 2087 S1 (ha)": "Hutan 2087 (ha)", "Deforestasi kumulatif S1 (ha)": "Deforestasi kumulatif 2025–2086 (ha)", "Cakupan kebutuhan S1 (%)": "Cakupan kebutuhan minimum rerata 2030–2055 (%)",
         "KUPS 2087 S1": "KUPS aktif 2087", "Pendapatan bersih per RT S1 (Rp)": "Pendapatan bersih per RT bergantung rerata (Rp/RT/th)", "Kehilangan akses per RT terdampak S1 (Rp)": "Kehilangan akses per RT terdampak rerata (Rp/RT/th)",
         "Nilai non-tunai S1 (Rp juta/th)": "Nilai kontribusi non-tunai rerata (Rp/th)"}
rows = []
for e in H:
    r = e["hasil"]; base = {"Grup": e["grup"], "Level": e["level"]}
    for k, ky in S1IND.items(): base[k] = r["S1"][ky] / (1e6 if "juta" in k else 1)
    for h in [10, 20, 35]:
        for k, f in IND.items(): base[f"{k} | USD{h}"] = f(r["S1"], r[f"S2 USD{h}"])
    rows.append(base)
T = pd.DataFrame(rows)
# klasifikasi robust/sensitif per grup × indikator
cls = []
for g, sub in T.groupby("Grup", sort=False):
    for col in [c for c in T.columns if "|" in c or c in S1IND]:
        v = sub[col].astype(float).dropna()
        if len(v) < 2: continue
        lo, hi = v.min(), v.max(); mid = np.median(np.abs(v)) if np.median(np.abs(v)) > 0 else np.nan
        sign = "berubah tanda" if (lo < -1e-9 and hi > 1e-9) else "tanda tetap"
        rel = (hi - lo) / mid * 100 if mid and np.isfinite(mid) else np.nan
        lab = "SENSITIF (arah)" if sign == "berubah tanda" else ("SENSITIF (besaran)" if (np.isfinite(rel) and rel > 50) else ("AGAK SENSITIF" if np.isfinite(rel) and rel > 15 else "ROBUST"))
        if not np.isfinite(rel) and abs(hi - lo) < 1e-6: lab = "ROBUST"
        cls.append({"Grup": g, "Indikator": col, "Min": lo, "Maks": hi, "Rentang relatif thd median (%)": rel, "Tanda": sign, "Klasifikasi": lab})
Cdf = pd.DataFrame(cls)
W = pd.ExcelWriter(OUT, engine="openpyxl")
pd.DataFrame({"Isi": ["ANALISIS SENSITIVITAS PRIORITAS – DKP_25HD_FINAL_2SKENARIO.mdl (PySD; Vensim tertunda)",
 "Desain: satu-per-satu (one-at-a-time) di sekitar asumsi kerja; setiap level dijalankan BERPASANGAN: S1 dan S2 (USD 10, 20, 35) dengan parameter yang sama.",
 "Asumsi kerja: k = 0,5; efektivitas 0,37; kas non-karbon 0; dukungan material 0; reaktivasi KUPS Rp 50 juta; reinvestasi 0,5; delay 3 th; bayar 0; MRV ×1; pengembangan 0; hibah; diskonto 10 %.",
 "Klasifikasi per grup × indikator: ROBUST (rentang ≤ 15 % median, tanda tetap); AGAK SENSITIF (15–50 %); SENSITIF (besaran) (> 50 %); SENSITIF (arah) (tanda berubah).",
 "Catatan: biaya pengembangan proyek di model adalah aliran tahunan konstan (tidak dijadwalkan); uji 7b adalah proksi. NPV berstatus SEMENTARA.",
 "Tidak ada interaksi antarparameter yang diuji di sini (akan dicakup Monte Carlo)."]}).to_excel(W, sheet_name="0 README", index=False)
T.to_excel(W, sheet_name="1 Hasil per level", index=False)
Cdf.to_excel(W, sheet_name="2 Klasifikasi robust", index=False)
piv = Cdf[Cdf.Indikator.str.contains(r"\| USD20")].pivot_table(index="Indikator", columns="Grup", values="Klasifikasi", aggfunc="first")
piv.to_excel(W, sheet_name="3 Matriks USD20")
piv2 = Cdf[~Cdf.Indikator.str.contains(r"\|")].pivot_table(index="Indikator", columns="Grup", values="Klasifikasi", aggfunc="first"); piv2.to_excel(W, sheet_name="4 Matriks S1")
W.close()
T.to_json("fase3/sens_tabel.json", orient="records", force_ascii=False); Cdf.to_json("fase3/sens_klas.json", orient="records", force_ascii=False)
# grafik tornado USD20
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False})
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
for col, fn, ttl in [("Deforestasi dihindari S2−S1 (ha) | USD20", "G7_tornado_deforestasi_USD20.png", "Deforestasi dihindari S2−S1 (ha), USD 20"),
                     ("NPV inkremental [SEMENTARA] (Rp miliar) | USD20", "G8_tornado_NPV_USD20.png", "NPV inkremental SEMENTARA (Rp miliar), USD 20")]:
    base = T[(T.Grup.str.startswith("1")) & (T.Level == "k=0.5")][col].iloc[0]
    g = T.groupby("Grup", sort=False)[col].agg(["min", "max"]); g = g.assign(r=g["max"] - g["min"]).sort_values("r")
    fig, ax = plt.subplots(figsize=(11, 5.4))
    for i, (nm, rr) in enumerate(g.iterrows()):
        ax.barh(i, rr["max"] - rr["min"], left=rr["min"], color="#1aa874" if rr["max"] - rr["min"] > 0 else "#ccc")
        ax.text(rr["max"], i, f"  {fmt(rr['min'], 1)} – {fmt(rr['max'], 1)}", va="center", fontsize=10)
    ax.axvline(base, color="#e8692c", ls="--", lw=1.5, label=f"asumsi kerja: {fmt(base, 1)}")
    ax.set_yticks(range(len(g)), [x[2:] if x[0].isdigit() else x for x in g.index]); ax.set_title(ttl + ": rentang antar-level, satu-per-satu"); ax.legend(frameon=False, loc="lower right")
    fig.text(0.01, 0.005, "Sensitivitas berpasangan S1–S2; PySD; Vensim tertunda. NPV SEMENTARA.", fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(GD + "/" + fn, dpi=200); plt.close(fig)
ks = T[T.Grup.str.startswith("1")]
fig, ax = plt.subplots(figsize=(10, 5)); kv = [0, 0.25, 0.5, 0.75, 1]
for h, c in [(10, "#86d1b0"), (20, "#1aa874"), (35, "#0b6b4a")]: ax.plot(kv, ks[f"Deforestasi dihindari S2−S1 (ha) | USD{h}"], marker="o", color=c, lw=2.2, label=f"S2−S1, USD {h}")
ax2 = ax.twinx(); ax2.plot(kv, ks["Deforestasi kumulatif S1 (ha)"], marker="s", color="#2b6fd6", ls="--", lw=2, label="Deforestasi kumulatif S1 (sumbu kanan)"); ax2.spines["right"].set_visible(True)
ax.set_xlabel("Tingkat keberlanjutan patroli reguler k (asumsi)"); ax.set_ylabel("Deforestasi dihindari S2−S1 (ha)"); ax2.set_ylabel("Deforestasi kumulatif S1 (ha)")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=10)
ax.set_title("Pengaruh asumsi patroli reguler terhadap S1 dan dampak karbon")
fig.tight_layout(); fig.savefig(GD + "/G9_sensitivitas_k.png", dpi=200); plt.close(fig)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(T[["Grup", "Level", "Deforestasi kumulatif S1 (ha)", "Deforestasi dihindari S2−S1 (ha) | USD10", "Deforestasi dihindari S2−S1 (ha) | USD20", "Deforestasi dihindari S2−S1 (ha) | USD35",
         "NPV inkremental [SEMENTARA] (Rp miliar) | USD20", "Cakupan kebutuhan minimum S2 (%) | USD20", "Δ pendapatan bersih per RT S2−S1 (Rp) | USD20", "Porsi kredit BAU dari perlindungan tingkat S1 (%) | USD20", "KUPS 2087 S1"]].round(2).to_string())
