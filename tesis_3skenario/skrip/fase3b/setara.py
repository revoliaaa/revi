import pickle, pandas as pd, numpy as np, json
old = pickle.load(open("fase3/det_runs.pkl", "rb"))
L = lambda k: pd.read_pickle(f"fase3b/runs/{k}.pkl")
out = {}
for ko, kn in [("S1", "S1")] + [(f"S2 USD{h}", f"A_{h}") for h in [6, 10, 15, 20, 35]]:
    a, b = old[ko], L(kn)[old[ko].columns]
    rel = ((a - b).abs() / (a.abs() + 1)).max().max(); ab = (a - b).abs().max().max()
    out[kn] = {"maks selisih absolut": float(ab), "maks selisih relatif": float(rel), "kolom": len(a.columns)}
print(json.dumps(out, indent=1)); json.dump(out, open("fase3b/setara.json", "w"), indent=1)
