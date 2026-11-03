import sys, json; sys.path.insert(0, "work"); from lib import *; from analisis import *
m = load("work/FINAL_3S.mdl"); D = "Deforestasi kumulatif 2025-2086 (ha)"
I = lambda p: indicators(run(m, p, VARS))
out = {"putus_loop": {}, "oat": {}}
s2 = I({"Skenario Kebijakan": 2})
for price in [20, 35]:
    a = I({"Skenario Kebijakan": 3, "Harga Karbon": price}); b = I({"Skenario Kebijakan": 3, "Harga Karbon": price, "Proporsi Alokasi Perlindungan": 0})
    out["putus_loop"][price] = {"S3-S2 utuh": s2[D] - a[D], "S3-S2 tanpa dana ke patroli": s2[D] - b[D], "kredit utuh": a["Kredit REDD model diajukan (tCO2e)"], "kredit putus": b["Kredit REDD model diajukan (tCO2e)"]}
    print("putus loop", price, out["putus_loop"][price])
BAU = {"Laju HMS menjadi NonHutan BAU": 0.00261092, "Laju HRS menjadi NonHutan BAU": 0.00955847, "Laju HLKS menjadi NonHutan BAU": 0.00492777}
OAT = {"Efektivitas perlindungan (0,075 / 0,59)": [{"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.075}, {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.59}],
       "Laju deforestasi BAU (x0,68 / x1,46)": [{k: v*0.684 for k, v in BAU.items()}, {k: v*1.462 for k, v in BAU.items()}],
       "Biaya MRV (x0,5 / x1,5)": [{"Biaya Monitoring per Ha per Tahun": 990, "Biaya Verifikasi per Kejadian": 3.7125e8}, {"Biaya Monitoring per Ha per Tahun": 2970, "Biaya Verifikasi per Kejadian": 1.11375e9}],
       "Biaya per hari patroli (Rp195.000 / Rp325.000)": [{"Biaya per Hari Patroli": 195000}, {"Biaya per Hari Patroli": 325000}],
       "Kapasitas LPHD awal (0,3 / 0,7)": [{"Indeks Kapasitas LPHD Awal": 0.3}, {"Indeks Kapasitas LPHD Awal": 0.7}],
       "Proporsi kredit dalam PA (0,541 / 0,782)": [{"Proporsi Kredit REDD dalam Project Area": 0.541}, {"Proporsi Kredit REDD dalam Project Area": 0.782}],
       "Waktu penyesuaian efek PS (1 / 5 th)": [{"Waktu Penyesuaian Efek Pengelolaan PS": 1}, {"Waktu Penyesuaian Efek Pengelolaan PS": 5}],
       "Kehilangan akses (0 / 3,24)": [{"Pengali Kehilangan Akses": 0}, {"Pengali Kehilangan Akses": 3.24}],
       "Diskonto (6 % / 14 %)": ["r0.06", "r0.14"]}
for name, (lo, hi) in OAT.items():
    row = {}
    for lab, ex in [("rendah", lo), ("tinggi", hi)]:
        if isinstance(ex, str):
            r = float(ex[1:]); df = run(m, {"Skenario Kebijakan": 3, "Harga Karbon": 20}, VARS); dfa = run(m, {"Skenario Kebijakan": 3, "Harga Karbon": 10}, VARS)
            row[lab] = {"NPV USD10": npv(dfa, r)[0], "NPV USD20": npv(df, r)[0]}; continue
        a1 = I(dict({"Skenario Kebijakan": 1}, **ex)); a2 = I(dict({"Skenario Kebijakan": 2}, **ex))
        a20 = I(dict({"Skenario Kebijakan": 3, "Harga Karbon": 20}, **ex)); a35 = I(dict({"Skenario Kebijakan": 3, "Harga Karbon": 35}, **ex))
        a10 = I(dict({"Skenario Kebijakan": 3, "Harga Karbon": 10}, **ex))
        row[lab] = {"S2-S1 (ha)": a1[D]-a2[D], "S3-S2 USD20 (ha)": a2[D]-a20[D], "S3-S2 USD35 (ha)": a2[D]-a35[D], "NPV USD10": a10["NPV proyek 10% (Rp)"], "NPV USD20": a20["NPV proyek 10% (Rp)"],
                    "dPendapatan RT USD20 (S3-S2)": a20["Pendapatan bersih per RT bergantung (Rp/RT/th)"] - a2["Pendapatan bersih per RT bergantung (Rp/RT/th)"]}
    out["oat"][name] = row; print(name, {k: {a: round(b/1e9, 2) if "NPV" in a else round(b, 1) for a, b in v.items()} for k, v in row.items()})
json.dump(out, open("work/sens_oat.json", "w"), indent=1)
