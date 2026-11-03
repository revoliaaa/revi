import sys, json; sys.path.insert(0, "work"); from lib import *; from analisis import *
m = load("work/FINAL_3S.mdl"); out = []
def T(name, ok, detail): out.append({"uji": name, "status": "PASS" if ok else "GAGAL", "rincian": detail}); print(("PASS " if ok else "GAGAL ") + name, "|", detail)
D = "Deforestasi kumulatif 2025-2086 (ha)"
base = {k: run(m, p, VARS + ["Check Total Kawasan", "Check Konservasi Karbon", "Total Kawasan"]) for k, p in
        {"S1": {"Skenario Kebijakan": 1}, "S2": {"Skenario Kebijakan": 2}, "S3-10": {"Skenario Kebijakan": 3, "Harga Karbon": 10}, "S3-35": {"Skenario Kebijakan": 3, "Harga Karbon": 35}}.items()}
# 1 neraca
for k, df in base.items():
    a = df["Check Total Kawasan"].abs().max(); c = df["Check Konservasi Karbon"].abs().max(); tk = df["Total Kawasan"]
    T(f"Neraca luas & karbon {k}", a < 1e-6 and c < 1e-2 and abs(tk.max()-tk.min()) < 1e-6, f"|Check Total Kawasan| maks {a:.2e} ha; |Check Konservasi Karbon| maks {c:.2e}; Total Kawasan {tk.iloc[0]:.2f} ha konstan")
# 2 penempatan patroli & penghitungan ganda
for k in ["S2", "S3-10", "S3-35"]:
    avg, _ = yearly(base[k])
    ok = abs(avg["Hari Patroli Didanai"][2024]-2533) < 1e-6 and abs(avg["Hari Patroli Didanai"][2025]-3011) < 1e-6 and avg["Hari Patroli Swadaya"].abs().max() < 1e-9 \
         and avg["Realisasi Belanja Perlindungan"].loc[2024:2025].abs().max() < 1e-6 and avg["Hari Patroli Pembiayaan Awal"].loc[2026:].abs().max() < 1e-9
    T(f"Patroli 2024-2025 hanya dari pembiayaan awal ({k})", ok, f"HOK 2024 {avg['Hari Patroli Didanai'][2024]:.1f}; 2025 {avg['Hari Patroli Didanai'][2025]:.1f}; swadaya maks {avg['Hari Patroli Swadaya'].max():.1f}; belanja karbon patroli 2024-25 {avg['Realisasi Belanja Perlindungan'].loc[2024:2025].max():.0f} Rp; patroli pembiayaan awal sesudah 2025 {avg['Hari Patroli Pembiayaan Awal'].loc[2026:].max():.1f}")
    cum = base[k]["Realisasi Pembiayaan Awal"].sum()*DT
    T(f"Nilai pembiayaan awal = HOK x biaya ({k})", abs(cum - (2533+3011)*260000) < 1, f"{cum:,.0f} Rp = (2.533 + 3.011) x Rp 260.000")
avg1, _ = yearly(base["S1"])
T("S1 tanpa patroli & tanpa pembiayaan awal", avg1["Hari Patroli Didanai"].abs().max() < 1e-9 and avg1["Realisasi Pembiayaan Awal"].abs().max() < 1e-9 and avg1["Pendapatan Kotor Penjualan Kredit"].abs().max() < 1e-9, "semua 0")
avg2, _ = yearly(base["S2"])
T("S2 tanpa penerimaan karbon", avg2["Pendapatan Kotor Penjualan Kredit"].abs().max() < 1e-9 and avg2["Dana Desa Diterima"].abs().max() < 1e-9, "penerimaan kredit & dana LPHD = 0")
# 3 kondisi ekstrem
def ind(p): return indicators(run(m, p, VARS))
s1 = ind({"Skenario Kebijakan": 1}); s2 = ind({"Skenario Kebijakan": 2})
x = ind({"Skenario Kebijakan": 2, "HOK Patroli Pembiayaan Awal Aktual 2024": 0, "HOK Patroli Pembiayaan Awal Aktual 2025": 0, "Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.37})
T("Ekstrem: patroli 2024-2025 = 0 -> efek patroli S2 hilang", abs(x["Intensitas perlindungan 2025"]) < 1e-12 and x["Pembiayaan awal 2024-2025 (Rp)"] == 0, f"deforestasi S2 tanpa patroli {x[D]:.1f} ha vs S1 {s1[D]:.1f} ha (sisa selisih {s1[D]-x[D]:.1f} ha = efek penghidupan/KUPS PS)")
y = ind({"Skenario Kebijakan": 2, "Efektivitas Perlindungan Penuh terhadap Deforestasi": 0})
T("Ekstrem: efektivitas = 0 -> patroli tidak mengubah deforestasi", abs(y[D]-x[D]) < 1e-6, f"S2 efektivitas 0: {y[D]:.3f} ha; S2 tanpa patroli: {x[D]:.3f} ha")
z = ind({"Skenario Kebijakan": 3, "Harga Karbon": 0})
T("Ekstrem: harga karbon 0 -> S3 = S2 (hutan)", abs(z[D]-s2[D]) < 1e-6 and z["Dana LPHD diterima 2024-2086 (Rp)"] == 0, f"S3 USD0 {z[D]:.3f} ha vs S2 {s2[D]:.3f} ha; dana LPHD {z['Dana LPHD diterima 2024-2086 (Rp)']:.0f}")
w = run(m, {"Skenario Kebijakan": 3, "Harga Karbon": 500}, VARS)
T("Ekstrem: harga USD500 -> intensitas <= 1, stok >= 0", w["Indeks Intensitas Perlindungan"].max() <= 1+1e-12 and w["Total Hutan"].min() > 0 and w["Saldo Dana LPHD"].min() > -1e-3, f"intensitas maks {w['Indeks Intensitas Perlindungan'].max():.3f}; hutan min {w['Total Hutan'].min():.0f} ha")
v = run(m, {"Skenario Kebijakan": 2, "HOK Patroli Pembiayaan Awal Aktual 2024": 25330, "HOK Patroli Pembiayaan Awal Aktual 2025": 30110}, VARS)
T("Ekstrem: patroli 10x -> intensitas dibatasi 1", v["Indeks Intensitas Perlindungan"].max() <= 1+1e-12, f"intensitas maks {v['Indeks Intensitas Perlindungan'].max():.3f}")
# 4 monotonik harga
g = json.load(open("work/hasil_3s.json"))["grid"]; qs = sorted(g, key=float)
dd = [g[q]["def"] for q in qs]
T("Monoton: deforestasi tidak naik saat harga naik", all(b <= a + 1e-6 for a, b in zip(dd, dd[1:])), "grid USD1-60")
# 5 DT
m2 = load("work/FINAL_3S.mdl")
def ind_dt(p, dt):
    m2.reload(); ts = np.round(np.arange(2024, 2087 + dt/2, dt), 6)
    df = m2.run(params=p, time_step=dt, saveper=dt, return_timestamps=ts, return_columns=VARS, progress=False)
    import lib; old = lib.DT; lib.DT = dt
    import analisis; analisis.DT = dt
    r = indicators(df); lib.DT = old; analisis.DT = old; return r
rows = []
for p in [{"Skenario Kebijakan": 2}, {"Skenario Kebijakan": 3, "Harga Karbon": 10}, {"Skenario Kebijakan": 3, "Harga Karbon": 35}]:
    a = ind_dt(p, 0.0625); b = ind_dt(p, 0.03125)
    for k in [D, "Hutan 2087 (ha)", "NPV proyek 10% (Rp)", "Kredit REDD model diajukan (tCO2e)", "Dana LPHD diterima 2024-2086 (Rp)"]:
        rel = abs(a[k]-b[k])/max(abs(a[k]), 1e-9) * 100 if a[k] else 0; rows.append(rel)
    print("  DT", p, {k: (round(a[k], 1), round(b[k], 1)) for k in [D, "NPV proyek 10% (Rp)", "Kredit REDD model diajukan (tCO2e)"]})
T("Uji langkah waktu DT 0,0625 vs 0,03125", max(rows) < 2, f"selisih relatif maks {max(rows):.3f} % (5 indikator x 3 skenario)")
json.dump(out, open("work/verifikasi_3s.json", "w"), indent=1)
