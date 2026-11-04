"""Eksperimen benefit sharing B0–B4, R1, R2 pada mekanisme C (model v2 + struktur alokasi), Referensi S1 berpasangan."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); sys.path.insert(0, "fase3"); import c4, common
from gate import OVR
from multiprocessing import Pool
c4.common.MDL = "fase5/MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl"
ALT = {"B0": None, "B1": (0.4, 0.2, 0.1, 0.2, 0.1), "B2": (0.3, 0.15, 0.1, 0.25, 0.2), "B3": (0.2, 0.1, 0.1, 0.45, 0.15),
       "B4": (0.2, 0.1, 0.1, 0.25, 0.35), "R1": (0.4, 0.2, 2/15, 1/15, 0.2), "R2": (0.5, 0.15, 0.1, 0.05, 0.2)}
P = ["Porsi Dana Fleksibel Patroli", "Porsi Dana Fleksibel Rehabilitasi", "Porsi Dana Fleksibel Pengendalian Kebakaran", "Porsi Dana Fleksibel Pengembangan KUPS", "Porsi Dana Fleksibel Kompensasi RT Terdampak"]
VAR = {"dasar": {}, "k 0": {"Tingkat Keberlanjutan Patroli Reguler": 0}, "k 1": {"Tingkat Keberlanjutan Patroli Reguler": 1},
       "efektivitas 0,2": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.2}, "efektivitas 0,6": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.6},
       "akses 0": {"Pengali Kehilangan Akses": 0}, "akses 1,5": {"Pengali Kehilangan Akses": 1.5},
       "biaya patroli 150.000": {"Biaya per Hari Patroli": 150000}, "biaya patroli 300.000": {"Biaya per Hari Patroli": 300000},
       "jembatan JP": {"Besaran Pembiayaan Jembatan per Tahun": 1e12}, "biaya MRV ×1,5": {"Biaya Monitoring per Ha per Tahun": 2970, "Biaya Verifikasi per Kejadian": 1.11375e9}}
COLS = list(dict.fromkeys(c4.COLS + list(OVR) + list(OVR.values()) + ["Dana Fleksibel LPHD", "Jumlah Porsi Dana Fleksibel", "Alokasi Dana Kompensasi RT Terdampak", "Realisasi Kompensasi RT Terdampak",
        "Kumulatif Realisasi Kompensasi", "Kompensasi per RT Terdampak", "Kompensasi Rata rata per RT Bergantung", "Rasio Kompensasi terhadap Kehilangan Akses", "Pendapatan Bersih per RT Terdampak",
        "Pendapatan Bersih per RT Tidak Terdampak", "Total Alokasi Dana Program", "Check Anggaran Alokasi", "Check Neraca Dana LPHD", "Penggunaan Dana Desa", "Kebutuhan Dana Kompensasi",
        "Realisasi Belanja Pengendalian Kebakaran", "Realisasi Belanja Rehabilitasi Efektif", "Realisasi Belanja Pengembangan KUPS", "Realisasi Belanja Perlindungan", "Realisasi Belanja Operasional LPHD", "Realisasi Belanja Penguatan Kelembagaan"]))
DT = 0.0625
def run(p):
    m = c4.model(); m.reload(); return m.run(params=p, return_timestamps=c4.TS, return_columns=COLS, progress=False)
def prm(alt, h, ex, ov):
    p = dict({"Skenario Kebijakan": 2, "Harga Karbon": h, "Switch Alokasi Dana Fleksibel": 0 if ALT[alt] is None else 1}, **ex, **ov)
    if ALT[alt]: p.update(dict(zip(P, ALT[alt])))
    return p
def job(key):
    var, h = key; ex = VAR[var]; s = run(dict({"Skenario Kebijakan": 1}, **ex))
    ov = {k: pd.Series(s[v].values, index=s.index) for k, v in OVR.items()}
    return key, {"S1": s, **{alt: run(prm(alt, h, ex, ov)) for alt in ALT}}
if __name__ == "__main__":
    keys = [("dasar", h) for h in [10, 20, 35]] + [(v, 20) for v in VAR if v != "dasar"]
    with Pool(4) as p: R = dict(p.map(job, keys))
    pd.to_pickle(R, "fase5/alokasi_runs.pkl"); print("ok", len(R))
