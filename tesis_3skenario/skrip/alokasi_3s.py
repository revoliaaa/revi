import sys, json; sys.path.insert(0, "work"); from lib import *; from analisis import *
ma = load("work/ALOKASI_3S.mdl"); mf = load("work/FINAL_3S.mdl")
ALT = {"B0": None, "B1": (0.4, 0.2, 0.1, 0.2, 0.1), "B2": (0.3, 0.15, 0.1, 0.25, 0.2), "B3": (0.2, 0.1, 0.1, 0.45, 0.15),
       "B4": (0.2, 0.1, 0.1, 0.25, 0.35), "R1": (0.4, 0.2, 2/15, 1/15, 0.2), "R2": (0.5, 0.15, 0.1, 0.05, 0.2)}
P = ["Porsi Dana Fleksibel Patroli", "Porsi Dana Fleksibel Rehabilitasi", "Porsi Dana Fleksibel Pengendalian Kebakaran", "Porsi Dana Fleksibel Pengembangan KUPS", "Porsi Dana Fleksibel Kompensasi RT Terdampak"]
def prm(alt, price, extra=None):
    p = {"Skenario Kebijakan": 3, "Harga Karbon": price, "Switch Alokasi Dana Fleksibel": 0 if ALT[alt] is None else 1}
    if ALT[alt]: p.update(dict(zip(P, ALT[alt])))
    p.update(extra or {}); return p
VA = VARS + ALLOC_VARS
# identitas B0 = S3
for price in [10, 35]:
    a = indicators(run(ma, prm("B0", price), VA)); b = indicators(run(mf, {"Skenario Kebijakan": 3, "Harga Karbon": price}, VARS))
    dif = max(abs(a[k]-b[k])/max(abs(b[k]), 1e-9) for k in b if isinstance(b[k], float) and np.isfinite(b[k]))
    print("B0 vs S3 USD", price, "selisih relatif maks", dif)
res = {}
for price in [6, 10, 15, 20, 35]:
    for alt in ALT:
        res[f"{alt}-{price}"] = indicators(run(ma, prm(alt, price), VA))
# sensitivitas 22 kombinasi
VAR = {"dasar": {}, "efektivitas 0,075": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.075}, "efektivitas 0,59": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.59},
       "akses 0": {"Pengali Kehilangan Akses": 0}, "akses 3,24": {"Pengali Kehilangan Akses": 3.24},
       "laju BAU x0,68": {k: v*0.684 for k, v in {"Laju HMS menjadi NonHutan BAU": 0.00261092, "Laju HRS menjadi NonHutan BAU": 0.00955847, "Laju HLKS menjadi NonHutan BAU": 0.00492777}.items()},
       "laju BAU x1,46": {k: v*1.462 for k, v in {"Laju HMS menjadi NonHutan BAU": 0.00261092, "Laju HRS menjadi NonHutan BAU": 0.00955847, "Laju HLKS menjadi NonHutan BAU": 0.00492777}.items()},
       "biaya MRV x0,5": {"Biaya Monitoring per Ha per Tahun": 990, "Biaya Verifikasi per Kejadian": 3.7125e8}, "biaya MRV x1,5": {"Biaya Monitoring per Ha per Tahun": 2970, "Biaya Verifikasi per Kejadian": 1.11375e9},
       "kapasitas LPHD 0,3": {"Indeks Kapasitas LPHD Awal": 0.3}, "kapasitas LPHD 0,7": {"Indeks Kapasitas LPHD Awal": 0.7}}
sens = {}
for price in [10, 20]:
    for vn, ex in VAR.items():
        for alt in ALT:
            x = indicators(run(ma, prm(alt, price, ex), VA))
            sens[f"{alt}|{vn}|{price}"] = {"hutan": x["Hutan 2087 (ha)"], "pend_terdampak": x["Pendapatan Bersih per RT Terdampak rerata"], "kups": x["Penerimaan anggota KUPS rerata (Rp/th)"]}
json.dump({"res": res, "sens": sens}, open("work/alokasi_3s.json", "w"), indent=1)
for price in [10, 20, 35]:
    b0 = res[f"B0-{price}"]
    print(f"USD{price}: B0 hutan2087 {b0['Hutan 2087 (ha)']:.0f}, pend terdampak {b0['Pendapatan Bersih per RT Terdampak rerata']:.0f}, dana fleksibel {b0['Dana Fleksibel LPHD rerata']/1e6:.1f} jt/th, kehilangan agregat {b0['Kehilangan pendapatan agregat rerata (Rp/th)']/1e6:.1f} jt/th")
    for alt in ALT:
        x = res[f"{alt}-{price}"]
        print(f"   {alt}: dHutan {x['Hutan 2087 (ha)']-b0['Hutan 2087 (ha)']:+.0f} ha  dPendTerdampak {x['Pendapatan Bersih per RT Terdampak rerata']-b0['Pendapatan Bersih per RT Terdampak rerata']:+.0f}  kompensasi/kehilangan {100*x['Rasio Kompensasi terhadap Kehilangan Akses rerata']:.1f}%  dKUPS anggota {(x['Penerimaan anggota KUPS rerata (Rp/th)']-b0['Penerimaan anggota KUPS rerata (Rp/th)'])/1e6:+.2f} jt  belanja patroli {x['Belanja patroli rerata (Rp/th)']/1e6:.1f} jt")
