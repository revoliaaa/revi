import sys, json; sys.path.insert(0, "work"); from lib import *; from analisis import *
m = load("work/FINAL_3S.mdl")
SC = {"S1": {"Skenario Kebijakan": 1}, "S2": {"Skenario Kebijakan": 2}}
for p in [6, 10, 15, 20, 35]: SC[f"S3 USD{p}"] = {"Skenario Kebijakan": 3, "Harga Karbon": p}
res, series = {}, {}
for k, p in SC.items():
    df = run(m, p, VARS); res[k] = indicators(df)
    avg, first = yearly(df)
    series[k] = {"Total Hutan": first["Total Hutan"].tolist(), "Deforestasi Total": avg["Deforestasi Total"].tolist(),
                 "Penggunaan Dana Pengelolaan": avg["Penggunaan Dana Pengelolaan"].tolist(), "Kebutuhan Dana Minimum": avg["Kebutuhan Dana Minimum"].tolist(),
                 "Indeks Intensitas Perlindungan": avg["Indeks Intensitas Perlindungan"].tolist(), "Hari Patroli Didanai": avg["Hari Patroli Didanai"].tolist(),
                 "Pendapatan Kotor Penjualan Kredit": avg["Pendapatan Kotor Penjualan Kredit"].tolist(), "Realisasi Pembiayaan Awal": avg["Realisasi Pembiayaan Awal"].tolist(),
                 "Kesempatan Kerja Setara Penuh": avg["Kesempatan Kerja Setara Penuh"].tolist(), "years": [int(y) for y in avg.index]}
f = lambda q, i: npv(run(m, {"Skenario Kebijakan": 3, "Harga Karbon": q}, VARS))[i]
def cov(q): return indicators(run(m, {"Skenario Kebijakan": 3, "Harga Karbon": q}, VARS))["Cakupan kebutuhan minimum LPHD (%)"] - 100
grid = {}
for q in [1,2,3,4,5,6,8,10,12,15,18,20,25,30,35,40,50,60]:
    x = indicators(run(m, {"Skenario Kebijakan": 3, "Harga Karbon": q}, VARS))
    grid[q] = {"npv": x["NPV proyek 10% (Rp)"], "npv_mitra": x["NPV mitra 10% (Rp)"], "cov": x["Cakupan kebutuhan minimum LPHD (%)"], "def": x["Deforestasi kumulatif 2025-2086 (ha)"]}
def bracket(key, target=0):
    qs = sorted(grid)
    for a, b in zip(qs, qs[1:]):
        if (grid[a][key]-target) * (grid[b][key]-target) <= 0 and grid[a][key] != grid[b][key]: return a, b
    return None
be = {}
for key, fn in [("npv", lambda q: f(q, 0)), ("npv_mitra", lambda q: f(q, 1)), ("cov", cov)]:
    br = bracket(key, 100 if key == "cov" else 0)
    be[key] = root(fn, *br) if br else None
json.dump({"res": res, "series": series, "grid": grid, "breakeven": be}, open("work/hasil_3s.json", "w"), indent=1)
D = "Deforestasi kumulatif 2025-2086 (ha)"; E = "Emisi bersih kumulatif 2025-2086 (tCO2e)"
for k in res: print(k, "hutan2087", round(res[k]["Hutan 2087 (ha)"]), "def", round(res[k][D]), "dihindari vs S1", round(res["S1"][D]-res[k][D]), "vs S2", round(res["S2"][D]-res[k][D]), "emisi dihindari vs S1", round(res["S1"][E]-res[k][E]), "kredit", round(res[k]["Kredit REDD model diajukan (tCO2e)"]), "NPV", round(res[k]["NPV proyek 10% (Rp)"]/1e9,2), "cov", round(res[k]["Cakupan kebutuhan minimum LPHD (%)"],1), "int", round(res[k]["Intensitas perlindungan rerata 2030-2055"],3), "FTE", round(res[k]["FTE rerata"],1), "pend RT", round(res[k]["Pendapatan bersih per RT bergantung (Rp/RT/th)"]))
print("impas", be); print({q: (round(v["npv"]/1e9,2), round(v["cov"],1)) for q, v in grid.items()})
