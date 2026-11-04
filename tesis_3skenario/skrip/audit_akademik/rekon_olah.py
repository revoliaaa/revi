import numpy as np, pandas as pd, json
R = pd.read_pickle("fase6/rekon_runs.pkl"); DT = 0.0625; KURS = 16500
PER = [("2024–2028", 2024, 2029), ("2029–2033", 2029, 2034), ("2034–2050", 2034, 2051), ("2051–2086", 2051, 2087), ("Total 2024–2086", 2024, 2087)]
def I(d, v, a, b): s = d[v]; m = (s.index >= a) & (s.index < b); return float(s[m].sum() * DT)
def at(d, v, t): return float(d[v][d.index <= t + 1e-9].iloc[-1]) if t > 2024 else 0.0
out = {}; ind = {}
for h in [20, 35]:
    d, s = R[(h, 1.0)]["S2"], R[(h, 1.0)]["S1"]; rows = []
    for lab, a, b in PER:
        g = lambda v: I(d, v, a, b) / 1e9
        r = {"Periode": lab,
             "1 Pendapatan kotor penjualan kredit": g("Pendapatan Kotor Penjualan Kredit"), "1a Kas penjualan diterima": g("Kas Penjualan Kredit"),
             "2 Monitoring MRV": g("Biaya Monitoring MRV"), "3 Verifikasi": g("Biaya Verifikasi Tahunan"), "4 Penerbitan dan registri": g("Biaya Penerbitan dan Registri"),
             "5 Transaksi penjualan": g("Biaya Transaksi Penjualan"), "6 Pajak dan pungutan": g("Pajak dan Pungutan Karbon"), "7 Pembelian kredit pengganti": g("Biaya Penggantian Reversal"),
             "8 Total biaya bersama periode berjalan": g("Biaya Transaksi dan MRV"),
             "9 Surplus sebelum pemulihan": g("Surplus Sebelum Pemulihan"), "10 Kekurangan biaya ditalangi mitra": g("Kekurangan Biaya Bersama Ditanggung Mitra"),
             "11 Pemulihan defisit MRV historis": g("Pemulihan Defisit Biaya Bersama"), "12 Pemulihan talangan jembatan": g("Pemulihan Talangan Sebelum Bagi Hasil") + g("Pemulihan Talangan Sesudah Bagi Hasil"),
             "13 Pendapatan bersih dapat dibagi": g("Pendapatan Karbon Bersih yang Dapat Didistribusikan"), "14 Bagian LPHD 60 %": g("Kas Masuk LPHD Karbon"), "15 Bagian mitra 40 %": g("Dana Mitra dari Karbon"),
             "16 Pembiayaan jembatan (keluar dari mitra)": g("Realisasi Pembiayaan Jembatan"), "17 Biaya modal talangan": g("Biaya Modal Pendanaan Awal Rp"), "18 Penghapusan talangan": g("Penghapusan Talangan"),
             "19 Defisit MRV belum dipulihkan, akhir periode": at(d, "Defisit Biaya Bersama Belum Dipulihkan", b) / 1e9,
             "20 Talangan belum dipulihkan, akhir periode": at(d, "Pendanaan Awal Belum Terpulihkan", b) / 1e9,
             "21 Saldo LPHD, akhir periode": at(d, "Saldo Dana LPHD", b) / 1e9, "22 Belanja LPHD (termasuk upah)": g("Penggunaan Dana Desa"), "22a …upah tunai dibayar LPHD": g("Upah Dibayar dari Kas LPHD"),
             "23 Upah tunai jembatan (dibayar mitra)": I(d, "Hari Patroli Didanai Jembatan", a, b) * 150000 / 1e9,
             "24 Arus kas mitra S2 − S1": (I(d, "Arus Kas Mitra", a, b) - I(s, "Arus Kas Mitra", a, b)) / 1e9, "25 Arus kas proyek karbon": g("Arus Kas Proyek Karbon"),
             "26 Debit reversal belum diselesaikan, akhir (ribu tCO2e)": at(d, "Reversal Belum Terkompensasi", b) / 1e3, "27 Nilai kewajiban reversal pada harga berjalan, akhir": at(d, "Kewajiban Reversal Belum Diselesaikan", b) / 1e9}
        # cek rekonsiliasi (dihitung dari komponen, bukan variabel check model)
        r["Cek A: 1a − 8 − (9 − 10)"] = r["1a Kas penjualan diterima"] - r["8 Total biaya bersama periode berjalan"] - (r["9 Surplus sebelum pemulihan"] - r["10 Kekurangan biaya ditalangi mitra"])
        r["Cek B: 9 − 11 − 12 − 14 − 15"] = r["9 Surplus sebelum pemulihan"] - r["11 Pemulihan defisit MRV historis"] - r["12 Pemulihan talangan jembatan"] - r["14 Bagian LPHD 60 %"] - r["15 Bagian mitra 40 %"]
        r["Cek C: 14/(14+15) (harus 0,6)"] = r["14 Bagian LPHD 60 %"] / (r["14 Bagian LPHD 60 %"] + r["15 Bagian mitra 40 %"]) if (r["14 Bagian LPHD 60 %"] + r["15 Bagian mitra 40 %"]) > 1e-9 else np.nan
        d0 = at(d, "Defisit Biaya Bersama Belum Dipulihkan", a) / 1e9; t0 = at(d, "Pendanaan Awal Belum Terpulihkan", a) / 1e9; l0 = at(d, "Saldo Dana LPHD", a) / 1e9
        r["Cek D: defisit awal + 10 − 11 − akhir"] = d0 + r["10 Kekurangan biaya ditalangi mitra"] - r["11 Pemulihan defisit MRV historis"] - r["19 Defisit MRV belum dipulihkan, akhir periode"]
        r["Cek E: talangan awal + 16 + 17 − 12 − 18 − akhir"] = t0 + r["16 Pembiayaan jembatan (keluar dari mitra)"] + r["17 Biaya modal talangan"] - r["12 Pemulihan talangan jembatan"] - r["18 Penghapusan talangan"] - r["20 Talangan belum dipulihkan, akhir periode"]
        r["Cek F: saldo LPHD awal + 14 − 22 − akhir"] = l0 + r["14 Bagian LPHD 60 %"] + g("Kas Masuk LPHD Non Karbon") - r["22 Belanja LPHD (termasuk upah)"] - r["21 Saldo LPHD, akhir periode"]
        r["Cek G: arus mitra = 15 + 11 + 12 − 10 − 16"] = r["24 Arus kas mitra S2 − S1"] - (r["15 Bagian mitra 40 %"] + r["11 Pemulihan defisit MRV historis"] + r["12 Pemulihan talangan jembatan"] - r["10 Kekurangan biaya ditalangi mitra"] - r["16 Pembiayaan jembatan (keluar dari mitra)"])
        rows.append(r)
    out[h] = pd.DataFrame(rows).set_index("Periode").T
    # hitung ulang independen komponen dari penggerak primer (total)
    t = lambda v: I(d, v, 2024, 2087)
    terjual = t("Kredit REDD Terjual") * h + t("Kredit ARR Terjual") * 20
    ind[h] = {"Pendapatan = Σ(kredit REDD terjual × harga + ARR terjual × USD 20) × kurs": (terjual * KURS / 1e9, t("Pendapatan Kotor Penjualan Kredit") / 1e9),
              "Monitoring = Σ status × 111.123,17 ha × Rp1.980": (float((d["Biaya Monitoring MRV"] > 0).sum() * DT) * 111123.17 * 1980 / 1e9, t("Biaya Monitoring MRV") / 1e9),
              "Transaksi = 0,22 % × kas": (0.0022 * t("Kas Penjualan Kredit") / 1e9, t("Biaya Transaksi Penjualan") / 1e9), "Pajak = 5 % × kas": (0.05 * t("Kas Penjualan Kredit") / 1e9, t("Pajak dan Pungutan Karbon") / 1e9),
              "Pengganti = kredit pengganti × harga × kurs": (float(d["Kredit Pengganti Reversal Kumulatif"].iloc[-1]) * h * KURS / 1e9, t("Biaya Penggantian Reversal") / 1e9),
              "Jembatan = HOK jembatan × Rp260.000": (t("Hari Patroli Didanai Jembatan") * 260000 / 1e9, t("Realisasi Pembiayaan Jembatan") / 1e9),
              "Upah jembatan = HOK jembatan × Rp150.000": (t("Hari Patroli Didanai Jembatan") * 150000 / 1e9, None)}
pd.to_pickle({"rek": out, "ind": ind}, "fase6/rekon_hasil.pkl")
pd.set_option("display.width", 250)
for h in [20, 35]:
    print("==== C-J1 USD", h); print(out[h].map(lambda x: f"{x:,.3f}" if isinstance(x, float) else x).to_string())
    for k, (a, b) in ind[h].items(): print("  ", k, round(a, 3), round(b, 3) if b is not None else "")
