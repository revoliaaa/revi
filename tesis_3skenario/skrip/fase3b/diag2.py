import sys, json; sys.path.insert(0, "fase3b"); import mek
from multiprocessing import Pool
EXTRA = {
 "Dg-S1-k0-tanpa-mitra": {"Skenario Kebijakan": 1, "Tingkat Keberlanjutan Patroli Reguler": 0, "Switch Pendanaan Awal": 0},
 "Dg-S1-tanpa-PS": {"Skenario Kebijakan": 1, "Switch PS": 0},
 "Dg-B20-PendanaanAwalPatroli": {"Skenario Kebijakan": 2, "Harga Karbon": 20, "Switch Baseline Kredit Konservatif": 1, "Pendanaan Awal untuk Patroli": 1e9, "Status Pembiayaan Awal": 1},
 "Dg-B20-PendanaanAwalProyek": {"Skenario Kebijakan": 2, "Harga Karbon": 20, "Switch Baseline Kredit Konservatif": 1, "Besaran Pendanaan Awal Proyek Karbon": 1e9},
 "Dg-B20-kasNonKarbon": {"Skenario Kebijakan": 2, "Harga Karbon": 20, "Switch Baseline Kredit Konservatif": 1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9},
 "Dg-S1-kasNonKarbon": {"Skenario Kebijakan": 1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9},
}
mek.RUNS.update(EXTRA)
def one(k): return mek.one(k)
if __name__ == "__main__":
    with Pool(4) as p:
        for k, df in p.imap_unordered(one, list(EXTRA)): df.to_pickle(f"fase3b/runs/{k}.pkl"); print(k, flush=True)
    R = json.load(open("fase3b/runs.json")); R.update(EXTRA); json.dump(R, open("fase3b/runs.json", "w"), indent=1)
