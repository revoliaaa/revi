import sys, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); import c4, k7
from multiprocessing import Pool
def run(args):
    key, p, dt = args
    m = c4.model(); m.reload()
    return key, m.run(params=p, time_step=dt, return_timestamps=k7.ts(dt), return_columns=k7.C, progress=False)
if __name__ == "__main__":
    jobs = []
    for dt in [0.125, 0.0625, 0.03125, 0.015625]:
        jobs += [(f"S1|{dt}", dict({"Skenario Kebijakan": 1}, **k7.NK), dt), (f"C20|{dt}", dict({"Skenario Kebijakan": 2, "Harga Karbon": 20}, **k7.NK), dt)]
    with Pool(4) as pool: R = dict(pool.map(run, jobs))
    pd.to_pickle(R, "fase4g/k7dt_runs.pkl")
    for dt in [0.125, 0.0625, 0.03125, 0.015625]:
        s, c = R[f"S1|{dt}"], R[f"C20|{dt}"]; e = c["Emisi Deforestasi Biomassa Referensi S1"] - s["Emisi Deforestasi Biomassa"]
        print(dt, len(c), "galat kumulatif %.2f" % float(e.iloc[:-1].sum() * dt), "maks %.2f min %.2f" % (e.max(), e.min()), "| kredit", round(float(c["Kredit REDD Diajukan"].iloc[:-1].sum() * dt)), "| hutan S1 2087 %.3f" % s["Total Hutan"].iloc[-1])
