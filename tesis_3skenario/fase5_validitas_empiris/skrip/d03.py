"""Fase 5: eksperimen dekomposisi D0–D3 pada model v2 yang dibekukan (tanpa perubahan persamaan).
D0 = S1. D1 = S2 dengan Status Proyek Karbon Aktif := 0 (tanpa kredit, MRV, penjualan) + jembatan sebagai hibah (talangan dihapus 2031, kerugian mitra diakui).
D2 = S2-C-J1. D3 = S2 tanpa jembatan (aturan MRV sama dengan D2); D3h = D3 + aturan henti MRV prospektif."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); sys.path.insert(0, "fase4t3"); import c4
from gate import OVR
from det import COLS as DCOLS
from multiprocessing import Pool
EXTRA = ["Status Proyek Karbon Aktif", "Kekurangan Biaya Bersama Ditanggung Mitra", "Pemulihan Defisit Biaya Bersama", "Pemulihan Pendanaan Awal", "Penghapusan Talangan", "Kerugian Mitra dari Penghapusan Talangan",
         "Upah Dibayar dari Kas LPHD", "Penggunaan Dana Desa", "Realisasi Belanja Pengembangan KUPS", "Check Identitas Arus Kas", "Check Neraca Dana LPHD", "Check Total Kawasan", "Check Konservasi Karbon"]
COLS = list(dict.fromkeys(DCOLS + EXTRA))
D1 = {"Skenario Kebijakan": 2, "Status Proyek Karbon Aktif": 0, "Switch Penghapusan Talangan": 1, "Tahun Akhir Tenor Talangan": 2031}
VAR = {"dasar": {}, "JP": {"Besaran Pembiayaan Jembatan per Tahun": 1e12}, "durasi 3": {"Durasi Pembiayaan Jembatan": 3}, "durasi 8": {"Durasi Pembiayaan Jembatan": 8},
       "efektivitas 0,2": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.2}, "efektivitas 0,6": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.6},
       "biaya patroli 150.000": {"Biaya per Hari Patroli": 150000}, "biaya patroli 300.000": {"Biaya per Hari Patroli": 300000},
       "akses 0": {"Pengali Kehilangan Akses": 0}, "akses 1,5": {"Pengali Kehilangan Akses": 1.5}}
def run(p, dt=0.0625):
    m = c4.model(); m.reload(); ts = [round(2024 + i * dt, 8) for i in range(int(round(63 / dt)) + 1)]
    return m.run(params=p, time_step=dt, return_timestamps=ts, return_columns=COLS, progress=False)
def job(args):
    var, dt = args; ex = VAR[var]
    s1 = run(dict({"Skenario Kebijakan": 1}, **ex), dt); ov = {k: pd.Series(s1[v].values, index=s1.index) for k, v in OVR.items()}
    out = {"D0": s1, "D1": run(dict(D1, **ex, **ov), dt)}
    for h in [10, 20, 35]:
        out[f"D2|{h}"] = run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **ex, **ov), dt)
        out[f"D3|{h}"] = run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h, "Switch Pembiayaan Jembatan Karbon": 0}, **ex, **ov), dt)
        if var == "dasar": out[f"D3h|{h}"] = run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h, "Switch Pembiayaan Jembatan Karbon": 0, "Switch Aturan Penghentian MRV": 1}, **ex, **ov), dt)
    return args, out
if __name__ == "__main__":
    keys = [(v, 0.0625) for v in VAR] + [("dasar", 0.03125)]
    with Pool(4) as p: R = dict(p.map(job, keys))
    pd.to_pickle(R, "fase7/d03_runs.pkl"); print("ok", len(R))
