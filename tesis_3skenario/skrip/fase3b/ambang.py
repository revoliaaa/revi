import sys, json; sys.path.insert(0, "fase3b"); import mek
from multiprocessing import Pool
EX = {}
for h in [22.5, 25, 27.5, 30, 32.5]:
    EX[f"Th-C-JP-d5|{h}"] = {"Skenario Kebijakan": 2, "Harga Karbon": h, "Switch Baseline Kredit Konservatif": 1, "Switch Pembiayaan Jembatan Karbon": 1, "Besaran Pembiayaan Jembatan per Tahun": 1e12, "Durasi Pembiayaan Jembatan": 5}
    EX[f"Th-C-J1-d5|{h}"] = {"Skenario Kebijakan": 2, "Harga Karbon": h, "Switch Baseline Kredit Konservatif": 1, "Switch Pembiayaan Jembatan Karbon": 1, "Besaran Pembiayaan Jembatan per Tahun": 3011*260000.0, "Durasi Pembiayaan Jembatan": 5}
mek.RUNS.update(EX)
if __name__ == "__main__":
    with Pool(4) as p:
        for k, df in p.imap_unordered(mek.one, list(EX)): df.to_pickle(f"fase3b/runs/{k.replace('|','_')}.pkl")
    R = json.load(open("fase3b/runs.json")); R.update(EX); json.dump(R, open("fase3b/runs.json", "w"), indent=1)
