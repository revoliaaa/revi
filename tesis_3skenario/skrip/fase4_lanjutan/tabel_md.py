import pandas as pd, numpy as np
def f(x, d=0):
    if x is None or (isinstance(x, float) and x != x): return "–"
    if abs(x) < 0.5 * 10**-d: x = 0.0
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
T = {}
Pp = pd.read_pickle("fase5/mc_prop.pkl"); pv = Pp.pivot_table(index="Kriteria", columns="Harga", values="Proporsi ensembel (%)")
T["mc_prop"] = "| Kriteria (S2 mekanisme C vs S1 berpasangan) | USD 10 | USD 20 | USD 35 |\n|---|---|---|---|\n" + "\n".join(f"| {k} | {f(r[10],1)} % | {f(r[20],1)} % | {f(r[35],1)} % |" for k, r in pv.iterrows())
S = pd.read_pickle("fase5/mc_summ.pkl")
KEY = [("Deforestasi dihindari S2−S1 (ha)", 1, 0, "Deforestasi dihindari S2−S1 (ha)"), ("Δ hutan 2087 (ha)", 1, 0, "Δ hutan 2087 (ha)"), ("Manfaat karbon bersih kumulatif 2087 (tCO2e)", 1e3, 1, "Manfaat karbon bersih 2087 (ribu tCO₂e)"),
       ("Kredit diajukan (tCO2e)", 1e3, 1, "Kredit diajukan (ribu tCO₂e)"), ("Debit reversal belum diselesaikan 2087 (tCO2e)", 1e3, 1, "Debit reversal belum diselesaikan 2087 (ribu tCO₂e)"),
       ("Kas LPHD karbon (Rp)", 1e9, 1, "Kas LPHD karbon kumulatif (Rp M)"), ("Kas LPHD rerata 2075–2086 (Rp/th)", 1e6, 0, "Kas LPHD 2075–2086 (Rp juta/th)"), ("Cakupan kebutuhan minimum 2060–2086 (%)", 1, 1, "Cakupan kebutuhan LPHD 2060–2086 (%)"),
       ("NPV inkremental proyek [SEMENTARA] (Rp)", 1e9, 2, "NPV inkremental proyek (Rp M) [SEMENTARA]"), ("NPV mitra inkremental [SEMENTARA] (Rp)", 1e9, 2, "NPV mitra inkremental (Rp M) [SEMENTARA]"),
       ("Defisit MRV 2087 (Rp)", 1e9, 1, "Defisit MRV ditanggung mitra 2087 (Rp M)"), ("Δ FTE berupah 2030–2055", 1, 1, "Δ FTE berupah 2030–2055"), ("Δ FTE berupah 2060–2086", 1, 1, "Δ FTE berupah 2060–2086"),
       ("Δ upah kegiatan PS (Rp/th)", 1e6, 0, "Δ upah kegiatan PS (Rp juta/th)"), ("Δ penerimaan anggota KUPS (Rp/th)", 1e6, 1, "Δ penerimaan anggota KUPS (Rp juta/th)"), ("KUPS aktif 2087 S2", 1, 1, "KUPS aktif 2087 (S2)"),
       ("KUPS aktif 2087 S1", 1, 1, "KUPS aktif 2087 (S1)"), ("Kapasitas LPHD 2087 S2", 1, 2, "Kapasitas LPHD 2087 (S2)"),
       ("Δ pendapatan bersih per RT bergantung (Rp/th)", 1, 0, "Δ pendapatan bersih per RT bergantung (Rp/th)"), ("Δ pendapatan per RT terdampak (Rp/th)", 1, 0, "Δ pendapatan per RT terdampak (Rp/th)"),
       ("Δ kehilangan per RT terdampak (Rp/th)", 1, 0, "Δ kehilangan per RT terdampak (Rp/th)")]
rows = ["| Indikator | USD 10: median [P5; P95] | USD 20: median [P5; P95] | USD 35: median [P5; P95] |", "|---|---|---|---|"]
for k, sc, d, lab in KEY:
    cells = []
    for h in [10, 20, 35]:
        r = S[(S["Harga"] == h) & (S["Indikator"] == k)].iloc[0]; cells.append(f"{f(r.Median/sc,d)} [{f(r.P5/sc,d)}; {f(r.P95/sc,d)}]")
    rows.append(f"| {lab} | " + " | ".join(cells) + " |")
T["mc_kuantil"] = "\n".join(rows)
PR = pd.read_pickle("fase5/mc_prcc.pkl"); rows = ["| Indikator | Parameter berpengaruh terbesar (PRCC, USD 20) |", "|---|---|"]
sh = lambda p: p.replace(" (Tingkat Keberlanjutan Patroli Reguler)", "").replace(" terhadap Deforestasi", "").replace(" per Tahun (Rp)", "").replace(" (Rp/HOK)", "").replace(" (th)", "").replace(" (Rp)", "")
for ind, g in PR[PR["Harga"] == 20].groupby("Indikator", sort=False):
    top = g.reindex(g["PRCC"].abs().sort_values(ascending=False).index).head(4)
    rows.append(f"| {ind} | " + "; ".join(f"{sh(r.Parameter)} {f(r.PRCC,2)}" for r in top.itertuples()) + " |")
T["mc_prcc"] = "\n".join(rows)
kk = PR[PR["Parameter"].str.startswith("k ")].pivot_table(index="Indikator", columns="Harga", values="PRCC")
T["mc_k"] = "| Indikator | PRCC k, USD 10 | USD 20 | USD 35 |\n|---|---|---|---|\n" + "\n".join(f"| {i} | {f(r[10],2)} | {f(r[20],2)} | {f(r[35],2)} |" for i, r in kk.iterrows())
df = pd.read_pickle("fase5/alok_df.pkl"); dB = pd.read_pickle("fase5/alok_dB.pkl")
AC = [("Deforestasi dihindari S2−S1 (ha)", 1, 0, "Deforestasi dihindari S2−S1 (ha)"), ("FTE berupah", 1, 1, "FTE berupah"), ("Upah kegiatan PS (Rp/th)", 1e6, 1, "Upah kegiatan PS (Rp juta/th)"),
      ("KUPS aktif 2087", 1, 1, "KUPS aktif 2087"), ("Penerimaan anggota KUPS (Rp/th)", 1e6, 1, "Penerimaan anggota KUPS (Rp juta/th)"),
      ("Pendapatan bersih per RT bergantung (Rp/th)", 1e3, 1, "Pendapatan bersih per RT bergantung (Rp ribu/th)"), ("Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)", 1e3, 1, "Pendapatan bersih RT terdampak/pemegang garapan (Rp ribu/th)"),
      ("Kehilangan per RT terdampak (Rp/th)", 1e3, 1, "Kehilangan per RT terdampak (Rp ribu/th)"), ("Kompensasi per RT terdampak (Rp/th)", 1e3, 1, "Kompensasi per RT terdampak (Rp ribu/th)"),
      ("Rasio kompensasi thd kehilangan akses total (%)", 1, 1, "Kompensasi / kehilangan total (%)"), ("Rasio kompensasi thd TAMBAHAN kehilangan S2−S1 (%)", 1, 1, "Kompensasi / tambahan kehilangan S2−S1 (%)"),
      ("Kapasitas LPHD 2087", 1, 2, "Kapasitas LPHD 2087"), ("Cakupan kebutuhan minimum pengelolaan 2030–2055 (%)", 1, 1, "Cakupan kebutuhan pengelolaan 2030–2055 (%)"), ("NPV mitra inkremental [SEMENTARA] (Rp)", 1e9, 2, "NPV mitra inkremental (Rp M) [SEMENTARA]")]
for h in [20, 35]:
    d = df[(df["Variasi"] == "dasar") & (df["Harga"] == h)].set_index("Alternatif")
    rows = ["| Indikator | B0 | B1 | B2 | B3 | B4 | R1 | R2 |", "|---|---|---|---|---|---|---|---|"]
    for k, sc, dd, lab in AC: rows.append(f"| {lab} | " + " | ".join(f(d.loc[a, k] / sc, dd) for a in ["B0", "B1", "B2", "B3", "B4", "R1", "R2"]) + " |")
    T[f"alok_{h}"] = "\n".join(rows)
r1 = pd.read_pickle("fase5/alok_r1.pkl")
T["r1"] = "| Variasi | Harga | Δ pendapatan RT terdampak R1 − B0 (Rp/th) | Δ deforestasi dihindari R1 − B0 (ha) | Δ penerimaan anggota KUPS R1 − B0 (Rp juta/th) | Hasil uji |\n|---|---|---|---|---|---|\n" + "\n".join(
    f"| {r.Variasi} | USD {r.Harga} | {f(r[3],0)} | {f(r[4],0)} | {f(r[6]/1e6,2)} | {'LULUS' if r[7] else 'TIDAK LULUS'} |" for r in r1.itertuples())
A = pd.read_pickle("fase5/aliran_manfaat.pkl")
T["aliran"] = "| Aliran kumulatif 2024–2086 (Rp miliar, nominal) | C-J1 USD 20 | C-J1 USD 35 | C-JP USD 20 | C-JP USD 35 |\n|---|---|---|---|---|\n" + "\n".join(f"| {i} | " + " | ".join(f(v, 2) for v in r.values) + " |" for i, r in A.iterrows())
import json; json.dump(T, open("fase5/tabel_md.json", "w"), ensure_ascii=False, indent=1)
for k, v in T.items(): print("=====", k); print(v[:2500])
