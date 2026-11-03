import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "work"); from lib import *; from analisis import *; from revisi_3s import OVERRIDES, NEW, REMOVE
OUT = sys.argv[1]
V = json.load(open("vars.json")); H = V[0]; RR = [r for r in V[1:] if r[0] not in REMOVE]
kinds = {r[0]: r[3] for r in RR}; kinds.update({n[0]: n[2] for n in NEW})
m = load("work/FINAL_3S.mdl")
SC = {"S1": {"Skenario Kebijakan": 1}, "S2": {"Skenario Kebijakan": 2}}
for p in [6, 10, 15, 20, 35]: SC[f"S3 USD{p}"] = {"Skenario Kebijakan": 3, "Harga Karbon": p}
allv = {}; annual = {}
for k, p in SC.items():
    df = run(m, p); df = df[[c for c in df.columns if c in kinds]]
    S = summaries(df, kinds); allv[k] = S
    avg, first = yearly(df)
    for v in ["Total Hutan", "Deforestasi Total", "Total Emisi Bersih", "Hari Patroli Didanai", "Hari Patroli Pembiayaan Awal", "Hari Patroli Swadaya", "Indeks Intensitas Perlindungan",
              "Realisasi Pembiayaan Awal", "Pendapatan Kotor Penjualan Kredit", "Biaya Transaksi dan MRV", "Dana Desa Diterima", "Penggunaan Dana Pengelolaan", "Kebutuhan Dana Minimum",
              "Kesenjangan Pembiayaan Minimum", "Kredit REDD Diajukan", "Kesempatan Kerja Setara Penuh", "Jumlah KUPS Aktif", "Pendapatan Bersih per RT Bergantung", "Anggota Patroli Aktif"]:
        s = first[v] if kinds.get(v) == "Stok" else avg[v]
        annual[(k, v)] = s
units = {r[0]: r[6] for r in RR}; units.update({n[0]: n[4] for n in NEW}); view = {r[0]: r[1] for r in RR}; view.update({n[0]: n[1] for n in NEW})
eqs = {r[0]: r[4] for r in RR}; eqs.update({k: v[0] for k, v in OVERRIDES.items()}); eqs.update({n[0]: n[3] for n in NEW})
W = pd.ExcelWriter(OUT, engine="openpyxl")
readme = ["REGISTER HASIL SIMULASI – MODEL DKP 25 HD FINAL 3 SKENARIO (revisi 2026-11-03)",
 "Model: DKP_25HD_FINAL_3SKENARIO.mdl (723 variabel, 39 stok, 16 View). Disimulasikan dengan PySD 3.14.3, Euler, DT 0,0625, 2024–2087.",
 "Skenario: S1 tanpa PS aktif; S2 PS + pembiayaan awal (patroli aktual 2.533 HOK 2024 dan 3.011 HOK 2025); S3 = S2 + perdagangan karbon USD 6/10/15/20/35.",
 "Konvensi: stok = nilai awal tahun; aliran/auxiliary = rerata langkah DT dalam [t, t+1); fisik kumulatif 2025–2086; keuangan kumulatif 2024–2086; tahunan rerata 2030–2055.",
 "Hasil model empat skenario lama TIDAK dipakai; lembar 'Lama vs baru' hanya pembanding.",
 "Kredit model ≠ VCU; frekuensi Monte Carlo ≠ peluang; FTE ≠ jumlah orang; dana LPHD ≠ pendapatan RT; omzet ≠ penerimaan anggota.",
 "Verifikasi Vensim native untuk model revisi BELUM dilakukan (perlu dijalankan peneliti; skrip bandingkan_vensim_pysd.py disertakan)."]
pd.DataFrame({"Isi": readme}).to_excel(W, sheet_name="0 README", index=False)
pd.DataFrame([{"Kode": k, "Skenario Kebijakan": p["Skenario Kebijakan"], "Harga Karbon (USD/tCO2e)": p.get("Harga Karbon", "–"),
               "Uraian": {"S1": "Tanpa PS aktif", "S2": "PS + pembiayaan awal (patroli 2024–2025 aktual)"}.get(k, f"S2 + perdagangan karbon USD {p.get('Harga Karbon')}")} for k, p in SC.items()]).to_excel(W, sheet_name="1 Daftar skenario", index=False)
chg = [{"Variabel": k, "Jenis perubahan": "Persamaan diubah", "Persamaan baru": v[0], "Persamaan lama (A1)": next((r[4] for r in V[1:] if r[0] == k), ""), "Keterangan": v[1]} for k, v in OVERRIDES.items()]
chg += [{"Variabel": n[0], "Jenis perubahan": "Variabel baru", "Persamaan baru": n[3], "Persamaan lama (A1)": "–", "Keterangan": n[5]} for n in NEW]
chg += [{"Variabel": n, "Jenis perubahan": "Dihapus (tidak dipakai lagi)", "Persamaan baru": "–", "Persamaan lama (A1)": next((r[4] for r in V[1:] if r[0] == n), ""), "Keterangan": "Dasar estimasi patroli lama (1.045 kegiatan 2024 − 427,6 swadaya 2023) × 5,51 HOK; diganti data final."} for n in REMOVE]
pd.DataFrame(chg).to_excel(W, sheet_name="2 Perubahan persamaan", index=False)
Hres = json.load(open("work/hasil_3s.json")); Rs = Hres["res"]
ind = pd.DataFrame(Rs); ind.index.name = "Indikator"; ind.to_excel(W, sheet_name="3 Indikator utama")
D = "Deforestasi kumulatif 2025-2086 (ha)"; E = "Emisi bersih kumulatif 2025-2086 (tCO2e)"
rows = []
for k in [c for c in Rs if c.startswith("S3")]:
    rows.append({"Skenario": k, "S2−S1 deforestasi dihindari (ha)": Rs["S1"][D] - Rs["S2"][D], "S3−S2 (ha)": Rs["S2"][D] - Rs[k][D], "S3−S1 (ha)": Rs["S1"][D] - Rs[k][D],
                 "S2−S1 emisi dihindari (tCO2e)": Rs["S1"][E] - Rs["S2"][E], "S3−S2 emisi (tCO2e)": Rs["S2"][E] - Rs[k][E], "S3−S1 emisi (tCO2e)": Rs["S1"][E] - Rs[k][E],
                 "Porsi S2−S1 dalam S3−S1 (%)": 100 * (Rs["S1"][D] - Rs["S2"][D]) / (Rs["S1"][D] - Rs[k][D])})
pd.DataFrame(rows).to_excel(W, sheet_name="4 Selisih skenario", index=False)
g = Hres["grid"]; be = Hres["breakeven"]
gd = pd.DataFrame([{"Harga (USD/tCO2e)": float(q), "NPV proyek (Rp)": v["npv"], "NPV mitra (Rp)": v["npv_mitra"], "Cakupan kebutuhan minimum LPHD (%)": v["cov"], "Deforestasi kumulatif (ha)": v["def"]} for q, v in g.items()]).sort_values("Harga (USD/tCO2e)")
gd.to_excel(W, sheet_name="5 Grid harga & impas", index=False)
pd.DataFrame([{"Ambang": "NPV proyek = 0", "Harga (USD/tCO2e)": be["npv"]}, {"Ambang": "NPV mitra = 0", "Harga (USD/tCO2e)": be["npv_mitra"]}, {"Ambang": "Cakupan kebutuhan minimum LPHD = 100 %", "Harga (USD/tCO2e)": be["cov"]}]).to_excel(W, sheet_name="5 Grid harga & impas", index=False, startcol=7)
ann = pd.DataFrame({f"{k} | {v}": s for (k, v), s in annual.items()}); ann.index.name = "Tahun"; ann.to_excel(W, sheet_name="6 Seri tahunan")
for lab, key in [("7 Hasil 2030", "2030"), ("8 Hasil 2050", "2050"), ("9 Hasil 2087", "2087"), ("10 Rerata 2030-2055", "avg"), ("11 Kumulatif 2025-2086", "cum")]:
    names = sorted(allv["S1"].keys(), key=lambda n: (str(view.get(n)), n))
    if key == "cum": names = [n for n in names if "/Year" in str(units.get(n))]
    df = pd.DataFrame([{"Nama variabel": n, "View": view.get(n), "Jenis": kinds.get(n), "Satuan": units.get(n), **{k: allv[k][n][key] for k in SC}} for n in names])
    df.to_excel(W, sheet_name=lab, index=False)
pd.DataFrame([{"Nama variabel": n, "View": view.get(n), "Jenis": kinds.get(n), "Satuan": units.get(n), "Persamaan": eqs.get(n), "Revisi 3S": ("diubah" if n in OVERRIDES else "baru" if n in [x[0] for x in NEW] else "")} for n in sorted(kinds, key=lambda n: (str(view.get(n)), n))]).to_excel(W, sheet_name="12 Persamaan model", index=False)
A = json.load(open("work/alokasi_3s.json"))
ar = []
for key, x in A["res"].items():
    alt, p = key.split("-"); b0 = A["res"][f"B0-{p}"]
    ar.append({"Alternatif": alt, "Harga": int(p), "Hutan 2087 (ha)": x["Hutan 2087 (ha)"], "Δ hutan vs B0 (ha)": x["Hutan 2087 (ha)"] - b0["Hutan 2087 (ha)"],
               "Pendapatan RT terdampak (Rp/RT/th)": x["Pendapatan Bersih per RT Terdampak rerata"], "Δ pendapatan RT terdampak vs B0": x["Pendapatan Bersih per RT Terdampak rerata"] - b0["Pendapatan Bersih per RT Terdampak rerata"],
               "Kompensasi per RT terdampak": x["Kompensasi per RT Terdampak rerata"], "Rasio kompensasi/kehilangan akses (%)": 100 * x["Rasio Kompensasi terhadap Kehilangan Akses rerata"],
               "Penerimaan anggota KUPS (Rp/th)": x["Penerimaan anggota KUPS rerata (Rp/th)"], "Δ penerimaan anggota KUPS vs B0": x["Penerimaan anggota KUPS rerata (Rp/th)"] - b0["Penerimaan anggota KUPS rerata (Rp/th)"],
               "Dana fleksibel LPHD (Rp/th)": x["Dana Fleksibel LPHD rerata"], "Belanja patroli (Rp/th)": x["Belanja patroli rerata (Rp/th)"], "Kehilangan pendapatan agregat (Rp/th)": x["Kehilangan pendapatan agregat rerata (Rp/th)"]})
pd.DataFrame(ar).sort_values(["Harga", "Alternatif"]).to_excel(W, sheet_name="13 Eksperimen alokasi", index=False)
sr = []
for key, v in A["sens"].items():
    alt, vn, p = key.split("|"); b = A["sens"][f"B0|{vn}|{p}"]
    sr.append({"Alternatif": alt, "Varian": vn, "Harga": int(p), "Δ hutan vs B0": v["hutan"] - b["hutan"], "Δ pendapatan RT terdampak": v["pend_terdampak"] - b["pend_terdampak"], "Δ penerimaan KUPS": v["kups"] - b["kups"]})
pd.DataFrame(sr).to_excel(W, sheet_name="14 Sensitivitas alokasi (22)", index=False)
MC = json.load(open("work/mc_3s_sum.json")); MA = json.load(open("work/mc_alok_sum.json"))
mrows = []
for k, v in MC.items():
    for a, b in v.items():
        if not a.startswith("prcc"): mrows.append({"Kelompok": k, "Ukuran": a, "Nilai": b})
pd.DataFrame(mrows).to_excel(W, sheet_name="15 Monte Carlo", index=False)
pr = []
for k, v in MC.items():
    for a, b in v.items():
        if a.startswith("prcc"):
            for n, c in b.items(): pr.append({"Kelompok": k, "Keluaran": a, "Parameter": n, "PRCC": c})
pd.DataFrame(pr).to_excel(W, sheet_name="16 PRCC", index=False)
pd.DataFrame([{"Perbandingan": k, **v} for k, v in MA.items()]).to_excel(W, sheet_name="17 MC alokasi", index=False)
import mc as MCM
pd.DataFrame([{"Parameter": s[0], "Sebaran": "seragam" if s[1] == "unif" else "lognormal (μ, σ log), dipotong 0,2–5", "a": s[2], "b": s[3]} for s in MCM.SPEC]).to_excel(W, sheet_name="18 Spesifikasi MC", index=False)
oat = json.load(open("work/sens_oat.json")); orows = []
for n, v in oat["oat"].items():
    for lab, x in v.items(): orows.append({"Parameter": n, "Nilai": lab, **x})
pd.DataFrame(orows).to_excel(W, sheet_name="19 Sensitivitas OAT", index=False)
pd.DataFrame([{"Harga": k, **v} for k, v in oat["putus_loop"].items()]).to_excel(W, sheet_name="20 Uji putus loop", index=False)
pd.DataFrame(json.load(open("work/verifikasi_3s.json"))).to_excel(W, sheet_name="21 Verifikasi", index=False)
dk = json.load(open("work/dekomposisi.json")); pd.DataFrame([{"Ukuran": k, "Nilai": v} for k, v in dk.items()]).to_excel(W, sheet_name="22 Lama vs baru", index=False)
W.close(); print("ok")
