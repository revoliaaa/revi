import sys, json; sys.path.insert(0, "fase3")
from multiprocessing import Pool
LEV = []
def L(grp, lab, p): LEV.append((grp, lab, p))
for k in [0, 0.25, 0.5, 0.75, 1]: L("1 Keberlanjutan patroli reguler (k)", f"k={k}", {"Tingkat Keberlanjutan Patroli Reguler": k})
for e in [0.075, 0.2, 0.37, 0.5, 0.59]: L("2 Efektivitas perlindungan", f"{e}", {"Efektivitas Perlindungan Penuh terhadap Deforestasi": e})
for v in [0, 1e9, 3e9, 6e9]: L("3 Kas non-karbon (Rp/th, 2026–2087)", f"{v/1e9:g} miliar", {"Switch Dana Non Karbon": 1 if v else 0, "Dana Operasional Non Karbon Tunai": v})
for v, pay in [(0, 0), (100.5e6, 0), (201e6, 0), (100.5e6, 1)]: L("4 Dukungan material rehabilitasi non-karbon", f"Rp {v/1e6:g} juta/th; upah dibayar={pay}", {"Dukungan Material Rehabilitasi Non Karbon": v, "Porsi Tenaga Penanaman Non Karbon Dibayar": pay})
for r in [12.5e6, 25e6, 50e6]:
    for q in [0.5, 1.0]: L("5 KUPS: biaya reaktivasi × reinvestasi", f"reaktivasi Rp {r/1e6:g} juta; reinvestasi {q}", {"Biaya Reaktivasi KUPS": r, "Porsi Laba Ditahan untuk Reinvestasi": q})
for d in [3, 4, 5]: L("6 Waktu penerbitan dan penerimaan", f"verifikasi {d} th; bayar 0", {"Delay Verifikasi dan Penerbitan Kredit": d})
for b in [0.5, 1]: L("6 Waktu penerbitan dan penerimaan", f"verifikasi 3 th; bayar {b} th", {"Delay Pembayaran Penjualan": b})
for f in [0.5, 1, 1.5]: L("7a Biaya MRV", f"×{f}", {"Biaya Monitoring per Ha per Tahun": 1980 * f, "Biaya Verifikasi per Kejadian": 7.425e8 * f})
for c in [0, 2.5e8, 5e8]: L("7b Biaya pengembangan proyek (Rp/th, konstan)", f"Rp {c/1e6:g} juta/th", {"Biaya Pengembangan Proyek": c})
for st, sw, lab in [(0, 1, "hibah"), (1, 1, "talangan, dipulihkan sebelum bagi hasil"), (1, 0, "talangan, dipulihkan sesudah bagi hasil")]: L("8 Status pembiayaan awal", lab, {"Status Pembiayaan Awal": st, "Switch Pemulihan Talangan Sebelum Bagi Hasil": sw})
for r in [0.06, 0.10, 0.14]: L("9 Tingkat diskonto", f"{r:.0%}", {"Tingkat Diskonto": r})
PR = [10, 20, 35]
def job(i):
    from common import run, summary
    grp, lab, p = LEV[i]
    out = {"S1": summary(run({**p, "Skenario Kebijakan": 1}))}
    for h in PR: out[f"S2 USD{h}"] = summary(run({**p, "Skenario Kebijakan": 2, "Harga Karbon": h}))
    return i, out
if __name__ == "__main__":
    with Pool(4) as pool: res = dict(pool.map(job, range(len(LEV))))
    json.dump([{"grup": g, "level": l, "param": p, "hasil": res[i]} for i, (g, l, p) in enumerate(LEV)], open("fase3/sens_hasil.json", "w"))
    print("selesai", len(LEV), "level")
