"""Eksperimen mekanisme kredit/pembiayaan A/B/C pada S2 (S1 tetap acuan kebijakan)."""
import sys, json, pickle, itertools, os
sys.path.insert(0, "fase3"); import common
from multiprocessing import Pool
common.MDL = "fase3b/DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl"
X = ["Kredit ARR Terbit", "Kredit Karbon Terbit", "Kredit Karbon Diajukan", "Realisasi Pembiayaan Jembatan", "Hari Patroli Didanai Jembatan", "Pendanaan Awal Belum Terpulihkan",
     "Pemulihan Pendanaan Awal", "Arus Kas Mitra", "Arus Kas Proyek Keseluruhan", "Arus Kas Proyek Karbon", "Defisit Biaya Bersama Belum Dipulihkan", "Pokok Talangan Kumulatif",
     "Kumulatif Pembiayaan Jembatan", "PV Pembiayaan Jembatan", "Porsi Mitigasi Adisional terhadap S2", "Efek Pengelolaan PS Aktif", "Efek Pengelolaan PS Tanpa Karbon",
     "Pemulihan Defisit Biaya Bersama", "Biaya Modal Pendanaan Awal Rp", "Check Identitas Arus Kas", "Check Identitas Patroli", "Kapasitas Hari Patroli Anggota", "Hari Patroli Tambahan Dibutuhkan",
     "Emisi Deforestasi Dihindari terhadap Baseline", "Pengurangan Emisi REDD Bruto", "Pengurangan Emisi Eligible REDD"]
COLS = list(dict.fromkeys(common.V + X))
J1 = 3011 * 260000.0          # setara tingkat pembiayaan mitra 2025
JFULL = 1e12                  # plafon tidak mengikat -> dibatasi kebutuhan tambahan & kapasitas
RUNS = {"S1": {"Skenario Kebijakan": 1}}
for h in [6, 10, 15, 20, 35]:
    b = {"Skenario Kebijakan": 2, "Harga Karbon": h}
    RUNS[f"A|{h}"] = dict(b)
    RUNS[f"B|{h}"] = dict(b, **{"Switch Baseline Kredit Konservatif": 1})
    for nm, bes in [("J1", J1), ("JP", JFULL)]:
        for dur in [3, 5, 8]:
            for henti in [0, 1]:
                for bm in [0, 0.1]:
                    RUNS[f"C|{h}|{nm}|d{dur}|h{henti}|m{bm}"] = dict(b, **{"Switch Baseline Kredit Konservatif": 1, "Switch Pembiayaan Jembatan Karbon": 1,
                        "Besaran Pembiayaan Jembatan per Tahun": bes, "Durasi Pembiayaan Jembatan": dur, "Switch Henti Jembatan saat Kas Karbon Pertama": henti, "Biaya Modal Pendanaan Awal": bm})
    # diagnostik
    RUNS[f"Dg-B-tanpaMRV|{h}"] = dict(b, **{"Switch Baseline Kredit Konservatif": 1, "Biaya Monitoring per Ha per Tahun": 0, "Biaya Verifikasi per Kejadian": 0})
    RUNS[f"Dg-C-1th|{h}"] = dict(b, **{"Switch Baseline Kredit Konservatif": 1, "Switch Pembiayaan Jembatan Karbon": 1, "Besaran Pembiayaan Jembatan per Tahun": JFULL, "Durasi Pembiayaan Jembatan": 1})
    RUNS[f"Dg-C-1th-tanpaMRV|{h}"] = dict(RUNS[f"Dg-C-1th|{h}"], **{"Biaya Monitoring per Ha per Tahun": 0, "Biaya Verifikasi per Kejadian": 0})
    RUNS[f"Dg-C-penuh-sampai2087|{h}"] = dict(b, **{"Switch Baseline Kredit Konservatif": 1, "Switch Pembiayaan Jembatan Karbon": 1, "Besaran Pembiayaan Jembatan per Tahun": JFULL, "Durasi Pembiayaan Jembatan": 62})
RUNS["Dg-S1-tanpa-patroli-mitra-2024-25"] = {"Skenario Kebijakan": 1, "Switch Pendanaan Awal": 0}
RUNS["Dg-A20-tanpa-patroli-mitra-2024-25"] = {"Skenario Kebijakan": 2, "Harga Karbon": 20, "Switch Pendanaan Awal": 0}
RUNS["Dg-S1-k0"] = {"Skenario Kebijakan": 1, "Tingkat Keberlanjutan Patroli Reguler": 0}
RUNS["Dg-A20-k0"] = {"Skenario Kebijakan": 2, "Harga Karbon": 20, "Tingkat Keberlanjutan Patroli Reguler": 0}
def one(k):
    return k, common.run(RUNS[k], COLS)
if __name__ == "__main__":
    os.makedirs("fase3b/runs", exist_ok=True)
    todo = [k for k in RUNS if not os.path.exists(f"fase3b/runs/{k.replace('|','_')}.pkl")]
    print(len(RUNS), "run;", len(todo), "belum", flush=True)
    with Pool(4) as p:
        for i, (k, df) in enumerate(p.imap_unordered(one, todo)):
            df.to_pickle(f"fase3b/runs/{k.replace('|','_')}.pkl")
            if i % 10 == 0: print(i, k, flush=True)
    json.dump(RUNS, open("fase3b/runs.json", "w"), indent=1)
