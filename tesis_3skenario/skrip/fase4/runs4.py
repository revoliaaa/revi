"""Run untuk verifikasi Tahap 2 (model final)."""
import sys, os, json; sys.path.insert(0, "fase4"); import c4
from multiprocessing import Pool
J1 = 782860000.0
S2 = lambda h, **kw: dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **kw)
LEG = {"Upah Harian Patroli Berbayar": 130000, "Biaya Operasional Patroli Sukarela per Anggota per Tahun": 1192050}   # setara Fase 3
R = {
 "S1": {"Skenario Kebijakan": 1},
 # reproduksi Fase 3 (upah lama, mode porsi lama)
 "rep_S1": dict({"Skenario Kebijakan": 1}, **LEG),
 "rep_A20": S2(20, **LEG, **{"Switch Baseline Kredit Konservatif": 0, "Switch Pembiayaan Jembatan Karbon": 0}),
 "rep_C20": S2(20, **LEG, **{"Switch Baseline Kredit Konservatif": 1}),
 "rep_v1_C20": S2(20, **{"Aturan Penyelesaian Reversal": 0}),
 # dasar final
 **{f"C{h}": S2(h) for h in [6, 10, 15, 20, 35]},
 **{f"A{h}": S2(h, **{"Switch Baseline Kredit Konservatif": 0, "Switch Pembiayaan Jembatan Karbon": 0}) for h in [6, 10, 15, 20, 35]},
 **{f"B{h}": S2(h, **{"Switch Pembiayaan Jembatan Karbon": 0}) for h in [20, 35]},
 # ekstrem
 "E_C0": S2(0), "E_C0_tanpajembatan": S2(0, **{"Switch Pembiayaan Jembatan Karbon": 0}),
 "E_S1_k0": {"Skenario Kebijakan": 1, "Tingkat Keberlanjutan Patroli Reguler": 0}, "E_C20_k0": S2(20, **{"Tingkat Keberlanjutan Patroli Reguler": 0}),
 "E_S1_k1": {"Skenario Kebijakan": 1, "Tingkat Keberlanjutan Patroli Reguler": 1}, "E_C20_k1": S2(20, **{"Tingkat Keberlanjutan Patroli Reguler": 1}),
 "E_C20_eff0": S2(20, **{"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0}), "E_S1_eff0": {"Skenario Kebijakan": 1, "Efektivitas Perlindungan Penuh terhadap Deforestasi": 0},
 "E_C500": S2(500), "E_S1_kasbesar": {"Skenario Kebijakan": 1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 1e12},
 "E_C20_kasNK": S2(20, **{"Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9}), "E_S1_kasNK": {"Skenario Kebijakan": 1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9},
 "E_S1_nontunai_x10": {"Skenario Kebijakan": 1, "Hari Logistik Swadaya per Anggota": 91.7, "Upah Harian Patroli Berbayar": 150000},
 # MRV dan talangan
 "M_B20_henti": S2(20, **{"Switch Pembiayaan Jembatan Karbon": 0, "Switch Aturan Penghentian MRV": 1}),
 "M_C20_henti": S2(20, **{"Switch Aturan Penghentian MRV": 1}), "M_C35_henti": S2(35, **{"Switch Aturan Penghentian MRV": 1}),
 "M_C20_tunda": S2(20, **{"Tahun Mulai Monitoring MRV": 2026}),
 "T_C6_bm10": S2(6, **{"Biaya Modal Pendanaan Awal": 0.1}), "T_C6_bm10_hapus": S2(6, **{"Biaya Modal Pendanaan Awal": 0.1, "Switch Penghapusan Talangan": 1}),
 "T_C10_sesudah_bm10": S2(10, **{"Biaya Modal Pendanaan Awal": 0.1, "Switch Pemulihan Talangan Sebelum Bagi Hasil": 0}),
 "T_C20_sesudah": S2(20, **{"Switch Pemulihan Talangan Sebelum Bagi Hasil": 0}),
 "RV_C20_aturan0": S2(20, **{"Aturan Penyelesaian Reversal": 0}), "RV_C20_aturan1": S2(20, **{"Aturan Penyelesaian Reversal": 1}),
 "C20_JP": S2(20, **{"Besaran Pembiayaan Jembatan per Tahun": 1e12}),
 # DT
 "DT_S1": {"Skenario Kebijakan": 1, "TIME STEP": 0.03125}, "DT_C20": S2(20, **{"TIME STEP": 0.03125}),
 # kausal
 "P_C35_putus": S2(35, **{"Proporsi Alokasi Perlindungan": 0}),
}
def one(k):
    p = dict(R[k]); dt = p.pop("TIME STEP", 0.0625)
    ts = [round(2024 + i * dt, 8) for i in range(int(round(63 / dt)) + 1)]
    m = c4.model(); m.reload()
    return k, m.run(params=p, time_step=dt, return_timestamps=ts, return_columns=c4.COLS, progress=False)   # v2: DT lewat argumen time_step (perbaikan U6)
if __name__ == "__main__":
    os.makedirs("fase4/runs_v2", exist_ok=True)
    todo = [k for k in R if not os.path.exists(f"fase4/runs_v2/{k}.pkl")]
    with Pool(4) as p:
        for k, df in p.imap_unordered(one, todo): df.to_pickle(f"fase4/runs_v2/{k}.pkl"); print(k, flush=True)
    json.dump(R, open("fase4/runs4_v2.json", "w"), indent=1)
