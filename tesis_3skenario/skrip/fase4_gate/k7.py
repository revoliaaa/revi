"""K7: rekonsiliasi tahunan Referensi S1 (di dalam S2) terhadap S1 mandiri; dekomposisi per saluran; konvergensi DT."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); import c4
from multiprocessing import Pool
NK = {"Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9}
C = ["Faktor Tekanan Deforestasi", "Faktor Tekanan Deforestasi Referensi S1", "Penambahan Luas Penanaman", "Aliran Penanaman ke Rehabilitasi Referensi S1",
     "Tingkat Keberhasilan Rehabilitasi", "Efek Pengelolaan PS Tanpa Karbon", "Efek Pengelolaan PS Aktif", "Hari Patroli Didanai Kas LPHD", "Hari Patroli Didanai Kas Non Karbon",
     "Hari Patroli Dapat Didanai Kas Non Karbon", "Porsi ARR Adisional", "Porsi Kas Karbon dalam Saldo", "Emisi Deforestasi Biomassa", "Emisi Deforestasi Biomassa Referensi S1",
     "Total Hutan", "Total Hutan Referensi S1", "Emisi Bersih Biomassa", "Emisi Bersih Biomassa Referensi S1", "Indeks Intensitas Perlindungan Tanpa Karbon", "Indeks Intensitas Perlindungan",
     "Kredit REDD Diajukan", "Mitigasi REDD Eligible Bersih Proyek", "Hari Patroli Didanai Jembatan", "Saldo Dana LPHD", "Saldo Dana LPHD dari Karbon", "Rasio Realisasi Belanja"]
def ts(dt): return [round(2024 + i * dt, 8) for i in range(int(round(63 / dt)) + 1)]
def run(args):
    key, p, dt = args
    m = c4.model(); m.reload(); p = dict(p); p["TIME STEP"] = dt
    return key, m.run(params=p, return_timestamps=ts(dt), return_columns=C, progress=False)
if __name__ == "__main__":
    jobs = []
    for dt in [0.0625, 0.03125, 0.015625]:
        jobs += [(f"S1|{dt}", dict({"Skenario Kebijakan": 1}, **NK), dt), (f"C20|{dt}", dict({"Skenario Kebijakan": 2, "Harga Karbon": 20}, **NK), dt)]
    with Pool(4) as pool: R = dict(pool.map(run, jobs))
    pd.to_pickle(R, "fase4g/k7_runs.pkl")
    # override bertahap pada DT dasar
    s1 = R["S1|0.0625"]; s1_ = s1.iloc[:-1]
    ser = lambda v: pd.Series(s1[v].values, index=s1.index)
    O = {"O1_tekanan": {"Faktor Tekanan Deforestasi Referensi S1": ser("Faktor Tekanan Deforestasi")},
         "O2_tekanan_tanam": {"Faktor Tekanan Deforestasi Referensi S1": ser("Faktor Tekanan Deforestasi"), "Aliran Penanaman ke Rehabilitasi Referensi S1": ser("Penambahan Luas Penanaman")}}
    jobs = [(k, dict({"Skenario Kebijakan": 2, "Harga Karbon": 20}, **NK, **v), 0.0625) for k, v in O.items()]
    with Pool(2) as pool: R2 = dict(pool.map(run, jobs))
    pd.to_pickle(R2, "fase4g/k7_override.pkl"); print("ok")
