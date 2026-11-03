import sys, json; sys.path.insert(0, "work"); from lib import *; from analisis import *
mo = load("work/A1_rekonstruksi.mdl"); mn = load("work/FINAL_3S.mdl")
D = "Deforestasi kumulatif 2025-2086 (ha)"
I = lambda m, p: indicators(run(m, p, VARS))
o = {"S1": I(mo, {"Skenario Kebijakan": 1}), "S2": I(mo, {"Skenario Kebijakan": 2}), "S3": I(mo, {"Skenario Kebijakan": 3}), "S4-10": I(mo, {"Skenario Kebijakan": 4, "Harga Karbon": 10}), "S4-20": I(mo, {"Skenario Kebijakan": 4, "Harga Karbon": 20})}
dg = {"S2": I(mn, {"Skenario Kebijakan": 2, "Switch Patroli Swadaya Reguler": 1}), "S3-10": I(mn, {"Skenario Kebijakan": 3, "Harga Karbon": 10, "Switch Patroli Swadaya Reguler": 1}), "S3-20": I(mn, {"Skenario Kebijakan": 3, "Harga Karbon": 20, "Switch Patroli Swadaya Reguler": 1})}
n = json.load(open("work/hasil_3s.json"))["res"]
out = {
 "Lama: S3(lama)-S1 [PS swadaya + pembiayaan awal lama]": o["S1"][D] - o["S3"][D],
 "Lama: S2(lama)-S1 [PS swadaya saja]": o["S1"][D] - o["S2"][D],
 "Diagnostik: patroli final 2024-25 + swadaya lama 2.355 HOK sesudah 2025": o["S1"][D] - dg["S2"][D],
 "Baru: S2-S1 [patroli final 2024-25, tanpa swadaya]": n["S1"][D] - n["S2"][D],
 "Lama: S4-S3 USD10": o["S3"][D] - o["S4-10"][D], "Diagnostik USD10 (dengan swadaya)": dg["S2"][D] - dg["S3-10"][D], "Baru: S3-S2 USD10": n["S2"][D] - n["S3 USD10"][D],
 "Lama: S4-S3 USD20": o["S3"][D] - o["S4-20"][D], "Diagnostik USD20 (dengan swadaya)": dg["S2"][D] - dg["S3-20"][D], "Baru: S3-S2 USD20": n["S2"][D] - n["S3 USD20"][D],
 "Lama NPV USD10 (Rp)": o["S4-10"]["NPV proyek 10% (Rp)"], "Diagnostik NPV USD10": dg["S3-10"]["NPV proyek 10% (Rp)"], "Baru NPV USD10": n["S3 USD10"]["NPV proyek 10% (Rp)"],
 "Lama kebutuhan minimum LPHD (Rp/th)": o["S4-10"]["Kebutuhan dana minimum LPHD rerata (Rp/th)"], "Baru kebutuhan minimum LPHD (Rp/th)": n["S3 USD10"]["Kebutuhan dana minimum LPHD rerata (Rp/th)"],
 "Lama pembiayaan awal (Rp)": o["S3"]["Pembiayaan awal 2024-2025 (Rp)"], "Baru pembiayaan awal (Rp)": n["S2"]["Pembiayaan awal 2024-2025 (Rp)"],
 "Lama HOK patroli 2024 S3": o["S3"]["HOK patroli 2024"], "Lama HOK patroli 2025 S3": o["S3"]["HOK patroli 2025"],
}
json.dump(out, open("work/dekomposisi.json", "w"), indent=1)
for k, v in out.items(): print(f"{k}: {v:,.1f}")
