"""Fase 4 Tahap 3: simulasi deterministik final (model v2, Referensi S1 berpasangan)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); import c4, sosek
from gate import OVR
from multiprocessing import Pool
COLS = list(dict.fromkeys(sosek.COLS + list(OVR) + list(OVR.values()) + ["Stok Karbon Biomassa Efektif", "Total Serapan", "Kontribusi Buffer REDD", "Buffer REDD Tersedia", "Kumulatif Penggunaan Buffer Reversal",
        "Kumulatif Pembatalan Stok Kredit Reversal", "Kewajiban Reversal Belum Diselesaikan", "Pulsa Verifikasi Reversal", "Kredit REDD Terbit", "Kredit Karbon Terjual",
        "Realisasi Belanja Operasional LPHD", "Realisasi Belanja Penguatan Kelembagaan", "Proporsi Alokasi Efektif Perlindungan"]))
H = [6, 10, 15, 20, 35]
MEK = {"C-J1": {}, "C-JP": {"Besaran Pembiayaan Jembatan per Tahun": 1e12}, "A": {"Switch Baseline Kredit Konservatif": 0, "Switch Pembiayaan Jembatan Karbon": 0}}
def run(p):
    m = c4.model(); m.reload(); return m.run(params=p, return_timestamps=c4.TS, return_columns=COLS, progress=False)
def job(key):
    mk, h = key
    ov = {k: pd.Series(S1[v].values, index=S1.index) for k, v in OVR.items()}
    return key, run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **MEK[mk], **ov))
if __name__ == "__main__":
    S1 = run({"Skenario Kebijakan": 1})
    keys = [(m, h) for m in MEK for h in H]
    with Pool(4) as p: R = dict(p.map(job, keys))
    R[("S1", 0)] = S1
    pd.to_pickle(R, "fase4t3/det_runs.pkl"); print("ok", len(R))
