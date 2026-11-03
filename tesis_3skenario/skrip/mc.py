"""Monte Carlo (LHS, 13 parameter) + PRCC. Pemakaian: mc.py <mdl> <mode old|new> <n10> <n20> <out.json>"""
import sys, json, numpy as np
sys.path.insert(0, "work")
from multiprocessing import Pool
from scipy.stats import qmc, norm, rankdata
if __name__ == "__main__": MDL, MODE, N10, N20, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
else: MODE = "new"; MDL = None
SEED = 20261101
BASE = {"Efektivitas Perlindungan Penuh terhadap Deforestasi": 0.37, "Biaya Monitoring per Ha per Tahun": 1980, "Biaya Verifikasi per Kejadian": 7.425e8,
        "Pengali Kehilangan Akses": 1, "Proporsi Leakage Karbon": 0.1, "Proporsi Kredit REDD dalam Project Area": 0.682, "Proporsi Buffer Risiko Karbon": 0.12,
        "Indeks Kapasitas LPHD Awal": 0.5, "Biaya per Hari Patroli": 260000, "Waktu Penyesuaian Efek Pengelolaan PS": 3, "Indeks Kapasitas untuk Realisasi Penuh": 0.8}
DEF = {"Laju HMS menjadi NonHutan BAU": 0.00261092, "Laju HRS menjadi NonHutan BAU": 0.00955847, "Laju HLKS menjadi NonHutan BAU": 0.00492777,
       "Laju HRS menjadi Pr BAU": 0.000233486, "Laju HLKS menjadi Pr BAU": 9.43217e-06}
REG = {"Laju NonHutan menjadi HMS": 0.000763614, "Laju NonHutan menjadi HRS": 0.00739492, "Laju NonHutan menjadi HLKS": 1.41648e-05}
# (nama, sebaran, a, b) ; u in [0,1]
SPEC = [
 ("Efektivitas perlindungan penuh", "unif", 0.075, 0.59),           # register: rentang literatur 0,075-0,59
 ("Pengali laju deforestasi BAU", "logn", 0.0, 0.19),               # SE log kdef 0,19
 ("Pengali laju regenerasi", "logn", 0.0, 0.74),                    # SE log kreg 0,74 (dipotong 0,2-5)
 ("Pengali biaya monitoring MRV", "unif", 0.5, 1.5),
 ("Pengali biaya verifikasi", "unif", 0.5, 1.5),
 ("Pengali kehilangan akses", "unif", 0.0, 3.24),                   # uji 0-3,24 (Angelsen et al. 2014)
 ("Proporsi leakage", "unif", 0.05, 0.20),
 ("Proporsi kredit dalam PA", "unif", 0.541, 0.782),                # register: rentang 0,541-0,782
 ("Proporsi buffer", "unif", 0.10, 0.20),
 ("Indeks kapasitas LPHD awal", "unif", 0.3, 0.7),
 ("Biaya per hari patroli (Rp/HOK)", "unif", 195000, 325000),        # +-25 %
 ("Waktu penyesuaian efek PS (th)", "unif", 1.0, 5.0),
 ("Indeks kapasitas untuk realisasi penuh", "unif", 0.6, 1.0),
]
def draw(n):
    u = qmc.LatinHypercube(d=len(SPEC), seed=SEED).random(n)
    X = np.zeros_like(u)
    for j, (_, d, a, b) in enumerate(SPEC):
        X[:, j] = a + (b - a) * u[:, j] if d == "unif" else np.clip(np.exp(norm.ppf(u[:, j]) * b + a), 0.2, 5)
    return X
def params(x):
    p = {"Efektivitas Perlindungan Penuh terhadap Deforestasi": x[0], "Biaya Monitoring per Ha per Tahun": 1980 * x[3], "Biaya Verifikasi per Kejadian": 7.425e8 * x[4],
         "Pengali Kehilangan Akses": x[5], "Proporsi Leakage Karbon": x[6], "Proporsi Kredit REDD dalam Project Area": x[7], "Proporsi Buffer Risiko Karbon": x[8],
         "Indeks Kapasitas LPHD Awal": x[9], "Biaya per Hari Patroli": x[10], "Waktu Penyesuaian Efek Pengelolaan PS": x[11], "Indeks Kapasitas untuk Realisasi Penuh": x[12]}
    p.update({k: v * x[1] for k, v in DEF.items()}); p.update({k: v * x[2] for k, v in REG.items()})
    return p
CODES = {"old": {"S1": 1, "S2": 2, "S3": 3, "C": 4}, "new": {"S1": 1, "S2": 2, "C": 3}}[MODE]
M = None
def init():
    global M
    from lib import load; M = load(MDL)
def one(args):
    i, x, do20 = args
    from lib import run; from analisis import indicators, VARS
    p = params(x); r = {}
    for k, c in CODES.items():
        if k == "C": continue
        r[k] = indicators(run(M, dict(p, **{"Skenario Kebijakan": c}), VARS))
    for price in ([10, 20] if do20 else [10]):
        r[f"C{price}"] = indicators(run(M, dict(p, **{"Skenario Kebijakan": CODES["C"], "Harga Karbon": price}), VARS))
    keep = ["Deforestasi kumulatif 2025-2086 (ha)", "NPV proyek 10% (Rp)", "NPV mitra 10% (Rp)", "Cakupan kebutuhan minimum LPHD (%)", "Pendapatan bersih per RT bergantung (Rp/RT/th)",
            "Kredit REDD model diajukan (tCO2e)", "Emisi bersih kumulatif 2025-2086 (tCO2e)", "Hutan 2087 (ha)", "Intensitas perlindungan rerata 2030-2055"]
    return i, {k: {q: v[q] for q in keep} for k, v in r.items()}
if __name__ == "__main__":
    X = draw(N10)
    with Pool(4, initializer=init) as pool:
        res = dict(pool.map(one, [(i, X[i], i < N20) for i in range(N10)], chunksize=4))
    json.dump({"spec": SPEC, "X": X.tolist(), "res": [res[i] for i in range(N10)], "mode": MODE, "seed": SEED}, open(OUT, "w"))
    print("selesai", N10)
