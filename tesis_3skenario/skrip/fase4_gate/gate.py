"""Gerbang verifikasi: kesetaraan Referensi S1 (endogen dan berpasangan) terhadap S1 mandiri."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); import c4
from multiprocessing import Pool
TOL = {"endogen_hutan_ha": 1.0, "endogen_emisi_kum_rel_sinyal": 1e-3, "berpasangan_rel": 1e-9}   # ditetapkan sebelum melihat hasil
LAND = ["Hutan Lahan Kering Sekunder", "Hutan Mangrove Sekunder", "Hutan Rawa Sekunder", "NonHutan", "Perkebunan", "Areal Rehabilitasi Belum Berhutan", "Defisit Karbon Hutan Regenerasi"]
CD = {"Hutan Lahan Kering Sekunder": 135.148, "Hutan Mangrove Sekunder": 81.6202, "Hutan Rawa Sekunder": 123.69, "NonHutan": 11.5667, "Perkebunan": 29.9578, "Areal Rehabilitasi Belum Berhutan": 11.5667, "Defisit Karbon Hutan Regenerasi": -1}
CMP = ["Total Hutan", "Deforestasi Total", "Emisi Deforestasi Biomassa", "Emisi Bersih Biomassa"]
OVR = {"Faktor Tekanan Deforestasi Referensi S1": "Faktor Tekanan Deforestasi", "Aliran Penanaman ke Rehabilitasi Referensi S1": "Penambahan Luas Penanaman",
       "Rehabilitasi Menjadi Hutan Referensi S1": "Rehabilitasi Menjadi Hutan", "Kegagalan Rehabilitasi Referensi S1": "Kegagalan Rehabilitasi",
       "Faktor Ekspansi Kebun Referensi S1": "Faktor Ekspansi Kebun", "Faktor Gangguan Gambut Tersisa Referensi S1": "Faktor Gangguan Gambut Tersisa", "Emisi Kebakaran Gambut Referensi S1": "Emisi Kebakaran Gambut"}
REF = lambda v: v + " Referensi S1"
COLS = list(dict.fromkeys(c4.COLS + LAND + [REF(v) for v in LAND] + [REF(v) for v in CMP] + list(OVR) + list(OVR.values()) +
        ["Buffer REDD Tersedia", "Penggunaan Buffer Reversal", "Pembatalan Stok Kredit Reversal", "Kumulatif Penggunaan Buffer Reversal", "Kumulatif Pembatalan Stok Kredit Reversal", "Kewajiban Reversal Belum Diselesaikan", "Pulsa Verifikasi Reversal"]))
NK = {"Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9}
CFG = {"dasar": {}, "k0": {"Tingkat Keberlanjutan Patroli Reguler": 0}, "k1": {"Tingkat Keberlanjutan Patroli Reguler": 1},
       "NK3": NK, "NK3_k0": dict(NK, **{"Tingkat Keberlanjutan Patroli Reguler": 0}), "NK3_k1": dict(NK, **{"Tingkat Keberlanjutan Patroli Reguler": 1}),
       "eff0.2": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.2}, "eff0.6": {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.6},
       "rehab_dukungan": {"Dukungan Material Rehabilitasi Non Karbon": 1e8}, "rehab_dukungan_NK3": dict(NK, **{"Dukungan Material Rehabilitasi Non Karbon": 1e8}),
       "rehab_keberhasilan0.5": {"Tingkat Keberhasilan Rehabilitasi Dasar": 0.5},
       "dt0.03125": {"_dt": 0.03125}, "dt0.03125_NK3": dict(NK, _dt=0.03125), "USD35_NK3": dict(NK, _h=35), "USD10_NK3": dict(NK, _h=10)}
def ts(dt): return [round(2024 + i * dt, 8) for i in range(int(round(63 / dt)) + 1)]
def run(p, dt):
    m = c4.model(); m.reload(); return m.run(params=p, time_step=dt, return_timestamps=ts(dt), return_columns=COLS, progress=False)
def job(name):
    cfg = dict(CFG[name]); dt = cfg.pop("_dt", 0.0625); h = cfg.pop("_h", 20)
    s1 = run(dict({"Skenario Kebijakan": 1}, **cfg), dt)
    s2e = run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **cfg), dt)
    ov = {k: pd.Series(s1[v].values, index=s1.index) for k, v in OVR.items()}
    s2p = run(dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **cfg, **ov), dt)
    return name, {"S1": s1, "S2_endogen": s2e, "S2_berpasangan": s2p, "dt": dt, "h": h}
if __name__ == "__main__":
    json.dump(TOL, open("fase4g/toleransi.json", "w"))
    with Pool(4) as pool: R = dict(pool.map(job, list(CFG)))
    pd.to_pickle(R, "fase4g/gate_runs.pkl"); print("ok", len(R))
