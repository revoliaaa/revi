import sys, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); import c4
from gate import OVR
from multiprocessing import Pool
C = ["Kas Penjualan Kredit", "Pendapatan Kotor Penjualan Kredit", "Biaya Penerbitan dan Registri", "Biaya Verifikasi Tahunan", "Biaya Monitoring MRV", "Biaya Transaksi Penjualan", "Pajak dan Pungutan Karbon",
     "Biaya Penggantian Reversal", "Biaya Transaksi dan MRV", "Surplus Sebelum Pemulihan", "Kekurangan Biaya Bersama Ditanggung Mitra", "Pemulihan Defisit Biaya Bersama", "Defisit Biaya Bersama Belum Dipulihkan",
     "Pemulihan Talangan Sebelum Bagi Hasil", "Pemulihan Talangan Sesudah Bagi Hasil", "Pendanaan Awal Belum Terpulihkan", "Realisasi Pembiayaan Jembatan", "Realisasi Pembiayaan Awal", "Biaya Modal Pendanaan Awal Rp",
     "Penghapusan Talangan", "Pendapatan Karbon Bersih yang Dapat Didistribusikan", "Kas Masuk LPHD Karbon", "Kas Masuk LPHD Non Karbon", "Dana Mitra dari Karbon", "Arus Kas Mitra", "Arus Kas Proyek Karbon",
     "Arus Kas Proyek Keseluruhan", "Biaya Pengembangan Proyek Efektif", "Saldo Dana LPHD", "Saldo Dana LPHD dari Karbon", "Dana Desa Diterima", "Penggunaan Dana Desa", "Penggunaan Dana Pengelolaan",
     "Upah Dibayar dari Kas LPHD", "Upah Patroli dari Kas LPHD", "Upah Pengendalian Kebakaran", "Upah Penanaman Didanai Karbon", "Upah Patroli Berbayar", "Hari Patroli Didanai Jembatan", "Upah Kegiatan PS",
     "Realisasi Belanja Perlindungan", "Realisasi Belanja Pengendalian Kebakaran", "Realisasi Belanja Rehabilitasi Efektif", "Realisasi Belanja Pengembangan KUPS", "Realisasi Belanja Operasional LPHD",
     "Realisasi Belanja Penguatan Kelembagaan", "NPV Mitra", "NPV Proyek Keseluruhan", "NPV Inkremental Perdagangan Karbon", "Kredit REDD Terjual", "Kredit ARR Terjual", "Kredit Pengganti Reversal Kumulatif",
     "Reversal Belum Terkompensasi", "Kewajiban Reversal Belum Diselesaikan", "Pendapatan KUPS Total", "Kehilangan Pendapatan Agregat", "Rumah Tangga Bergantung Hutan", "RT Terdampak Akses", "Populasi",
     "Pendapatan Bersih per RT Bergantung", "Pendapatan Hutan per RT Bergantung", "Pendapatan Program per RT Bergantung", "Kehilangan Pendapatan Pembatasan Akses per RT", "Kehilangan per RT Terdampak",
     "Pendapatan KUPS untuk Pendapatan RT", "Porsi Manfaat Program untuk RT Bergantung", "Indeks Ketersediaan Sumber Daya Hutan", "Pengurangan Relatif Deforestasi", "Efek Pengelolaan PS Aktif"] + list(OVR) + list(OVR.values())
C = list(dict.fromkeys(C))
def run(p):
    m = c4.model(); m.reload(); return m.run(params=p, return_timestamps=c4.TS, return_columns=C, progress=False)
def job(args):
    h, akses = args; s = run({"Skenario Kebijakan": 1, "Pengali Kehilangan Akses": akses})
    ov = {k: pd.Series(s[v].values, index=s.index) for k, v in OVR.items()}
    return args, {"S1": s, "S2": run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h, "Pengali Kehilangan Akses": akses}, **ov))}
if __name__ == "__main__":
    keys = [(h, a) for h in [20, 35] for a in [1.0, 0.0, 0.5, 0.75, 1.5]] + [(10, 1.0), (10, 0.0), (10, 0.5), (10, 1.5)]
    with Pool(4) as p: R = dict(p.map(job, keys))
    pd.to_pickle(R, "fase6/rekon_runs.pkl"); print("ok", len(R))
