import numpy as np, pandas as pd, pysd, warnings, json; warnings.filterwarnings("ignore")
DT = 0.0625; ts = list(np.round(np.arange(2024, 2087.0001, DT), 6))
M = pysd.read_vensim("fase2/DKP_25HD_FINAL_2SKENARIO.mdl")
C = ["Kredit REDD Diajukan", "Kredit REDD Terbit", "Kredit REDD Terjual", "Pendapatan Kotor Penjualan Kredit", "Kas Penjualan Kredit", "Biaya Transaksi dan MRV", "Surplus Sebelum Pemulihan",
     "Defisit Biaya Bersama Belum Dipulihkan", "Kas Masuk LPHD Karbon", "Penggunaan Dana Pengelolaan", "Realisasi Belanja Perlindungan", "Hari Patroli Didanai Kas LPHD", "Deforestasi Total", "Indeks Intensitas Perlindungan"]
M.reload(); s1 = M.run(params={"Skenario Kebijakan": 1}, return_timestamps=ts, return_columns=C, progress=False)
rows = []
first = lambda s, cond: (float(s.index[cond][0]) if cond.any() else None)
for h in [6, 10, 15, 20, 35]:
    M.reload(); d = M.run(params={"Skenario Kebijakan": 2, "Harga Karbon": h}, return_timestamps=ts, return_columns=C, progress=False)
    dd = d["Deforestasi Total"] - s1["Deforestasi Total"]
    rows.append({"Harga": h, "Kredit diajukan pertama": first(d, d["Kredit REDD Diajukan"] > 0), "Kredit terbit pertama": first(d, d["Kredit REDD Terbit"] > 0),
                 "Kredit terjual pertama": first(d, d["Kredit REDD Terjual"] > 0), "Kas penjualan pertama": first(d, d["Kas Penjualan Kredit"] > 0),
                 "Kas > biaya MRV pertama (surplus)": first(d, d["Surplus Sebelum Pemulihan"] > 0),
                 "Defisit biaya bersama puncak (Rp juta)": float(d["Defisit Biaya Bersama Belum Dipulihkan"].max() / 1e6),
                 "Defisit lunas (t)": first(d, (d.index > 2028) & (d["Defisit Biaya Bersama Belum Dipulihkan"] <= 1) & (d["Defisit Biaya Bersama Belum Dipulihkan"].shift(1) > 1)),
                 "Kas LPHD karbon pertama": first(d, d["Kas Masuk LPHD Karbon"] > 0), "Belanja LPHD pertama": first(d, d["Penggunaan Dana Pengelolaan"] > 0),
                 "Patroli tambahan dari kas pertama": first(d, d["Hari Patroli Didanai Kas LPHD"] > 0), "Deforestasi S2<S1 pertama": first(d, dd < -1e-6),
                 "Kas LPHD karbon kumulatif (Rp juta)": float(d["Kas Masuk LPHD Karbon"].iloc[:-1].sum() * DT / 1e6)})
k = pd.DataFrame(rows); k.to_json("fase3/kronologi.json", orient="records"); print(k.T.to_string())
