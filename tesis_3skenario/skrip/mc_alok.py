import sys, json, numpy as np
sys.path.insert(0, "work")
from multiprocessing import Pool
import mc as MC  # reuse SPEC/params/draw
N = int(sys.argv[1]); OUT = sys.argv[2]
ALT = {"B0": None, "B1": (0.4, 0.2, 0.1, 0.2, 0.1), "R1": (0.4, 0.2, 2/15, 1/15, 0.2), "R2": (0.5, 0.15, 0.1, 0.05, 0.2)}
P = ["Porsi Dana Fleksibel Patroli", "Porsi Dana Fleksibel Rehabilitasi", "Porsi Dana Fleksibel Pengendalian Kebakaran", "Porsi Dana Fleksibel Pengembangan KUPS", "Porsi Dana Fleksibel Kompensasi RT Terdampak"]
M = None
def init():
    global M
    from lib import load; M = load("work/ALOKASI_3S.mdl")
def one(a):
    i, x = a
    from lib import run, yearly
    out = {}
    for price in [10, 20]:
        for alt, sh in ALT.items():
            p = dict(MC.params(x), **{"Skenario Kebijakan": 3, "Harga Karbon": price, "Switch Alokasi Dana Fleksibel": 0 if sh is None else 1})
            if sh: p.update(dict(zip(P, sh)))
            df = run(M, p, ["Total Hutan", "Pendapatan Bersih per RT Terdampak"]); avg, first = yearly(df)
            out[f"{alt}-{price}"] = (float(df["Total Hutan"].iloc[-1]), float(avg["Pendapatan Bersih per RT Terdampak"].loc[2030:2055].mean()))
    return i, out
if __name__ == "__main__":
    MC.SEED = 20261102
    X = MC.draw(N)
    with Pool(4, initializer=init) as pool: res = dict(pool.map(one, [(i, X[i]) for i in range(N)], chunksize=4))
    R = [res[i] for i in range(N)]; S = {}
    for price in [10, 20]:
        for alt in ["B1", "R1", "R2"]:
            dh = np.array([r[f"{alt}-{price}"][0] - r[f"B0-{price}"][0] for r in R]); di = np.array([r[f"{alt}-{price}"][1] - r[f"B0-{price}"][1] for r in R])
            S[f"{alt}-{price}"] = {"n": N, "tidak_lebih_buruk": float(((dh >= -0.5) & (di >= -0.5)).mean()), "dominan_lemah": float(((dh >= -0.5) & (di >= -0.5) & ((dh > 0.5) | (di > 0.5))).mean()),
                                   "hutan_naik": float((dh > 0.5).mean()), "median_dhutan": float(np.median(dh)), "median_dpend": float(np.median(di)), "pend_naik": float((di > 0.5).mean())}
    json.dump(S, open(OUT, "w"), indent=1); print(json.dumps(S, indent=1))
