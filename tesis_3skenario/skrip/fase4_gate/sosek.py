"""A.4 Audit sosial-ekonomi PWD (model v2)."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); import c4
from multiprocessing import Pool
X = ["HOK Patroli Berbayar", "Upah Setara Non Tunai Patroli", "Upah Harian Patroli Berbayar", "HOK Penanaman Non Karbon", "HOK Penanaman Sukarela", "HOK Penanaman Berupah", "HOK Patroli Reguler PS",
     "Pendapatan KUPS untuk Pendapatan RT", "Porsi Manfaat Program untuk RT Bergantung", "Manfaat Ekonomi KUPS", "Penjualan KUPS", "Pendapatan KUPS Total", "Check Identitas Surplus KUPS", "Check Identitas Penjualan KUPS",
     "Kehilangan per RT Terdampak", "Pengurangan Relatif Deforestasi", "Upah Penanaman per HOK", "Upah Harian Pengendalian Kebakaran", "Nilai Dukungan Material Non Karbon Terpakai", "Akumulasi Modal KUPS",
     "Upah Kegiatan Didanai Karbon", "Manfaat Ekonomi Patroli", "Dana Desa Diterima", "Kesenjangan Pembiayaan Minimum"]
COLS = list(dict.fromkeys(c4.COLS + X))
S2 = lambda h, **k: dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **k)
RUN = {"S1": {"Skenario Kebijakan": 1}, "C10": S2(10), "C20": S2(20), "C35": S2(35), "C10_JP": S2(10, **{"Besaran Pembiayaan Jembatan per Tahun": 1e12}),
       "C20_JP": S2(20, **{"Besaran Pembiayaan Jembatan per Tahun": 1e12}), "C35_JP": S2(35, **{"Besaran Pembiayaan Jembatan per Tahun": 1e12}),
       "S1_akses0": {"Skenario Kebijakan": 1, "Pengali Kehilangan Akses": 0}, "C20_akses0": S2(20, **{"Pengali Kehilangan Akses": 0}),
       "S1_nontunaix10": {"Skenario Kebijakan": 1, "Hari Logistik Swadaya per Anggota": 91.7}}
def one(k):
    m = c4.model(); m.reload(); return k, m.run(params=RUN[k], return_timestamps=c4.TS, return_columns=COLS, progress=False)
if __name__ == "__main__":
    with Pool(4) as p: R = dict(p.map(one, list(RUN)))
    pd.to_pickle(R, "fase4g/sosek_runs.pkl"); print("ok")
