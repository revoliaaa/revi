import sys, json, numpy as np
from scipy.stats import rankdata
d = json.load(open(sys.argv[1])); X = np.array(d["X"]); R = d["res"]; names = [s[0] for s in d["spec"]]
D = "Deforestasi kumulatif 2025-2086 (ha)"; base = "S3" if d["mode"] == "old" else "S2"
def prcc(y, Xs):
    Xr = np.column_stack([rankdata(c) for c in Xs.T]); yr = rankdata(y); out = []
    for j in range(Xr.shape[1]):
        o = np.delete(Xr, j, 1); A = np.column_stack([np.ones(len(yr)), o])
        rx = Xr[:, j] - A @ np.linalg.lstsq(A, Xr[:, j], rcond=None)[0]; ry = yr - A @ np.linalg.lstsq(A, yr, rcond=None)[0]
        out.append(float(np.corrcoef(rx, ry)[0, 1]))
    return out
S = {}
s21 = np.array([r["S1"][D] - r["S2"][D] for r in R]); S["S2-S1"] = {"freq_S2_lt_S1": float((s21 > 0).mean()), "median": float(np.median(s21)), "p5": float(np.percentile(s21, 5)), "p95": float(np.percentile(s21, 95)), "prcc": dict(zip(names, prcc(s21, X)))}
for price in [10, 20]:
    idx = [i for i, r in enumerate(R) if f"C{price}" in r]
    if not idx: continue
    Xp = X[idx]; RR = [R[i] for i in idx]
    add = np.array([r[base][D] - r[f"C{price}"][D] for r in RR])
    npv = np.array([r[f"C{price}"]["NPV proyek 10% (Rp)"] for r in RR]); cov = np.array([r[f"C{price}"]["Cakupan kebutuhan minimum LPHD (%)"] for r in RR])
    inc = np.array([r[f"C{price}"]["Pendapatan bersih per RT bergantung (Rp/RT/th)"] - r[base]["Pendapatan bersih per RT bergantung (Rp/RT/th)"] for r in RR])
    S[f"USD{price}"] = {"n": len(idx), "freq_karbon_tambah_perlindungan": float((add > 1e-6).mean()), "median_tambahan_ha": float(np.median(add)), "p5": float(np.percentile(add, 5)), "p95": float(np.percentile(add, 95)),
        "freq_NPV_pos": float((npv > 0).mean()), "median_NPV": float(np.median(npv)), "freq_kebutuhan_tertutup": float((cov >= 100).mean()), "median_cakupan": float(np.median(cov)),
        "freq_pendapatan_naik": float((inc > 0).mean()), "median_dpendapatan": float(np.median(inc)),
        "prcc_tambahan": dict(zip(names, prcc(add, Xp))), "prcc_NPV": dict(zip(names, prcc(npv, Xp))), "prcc_dpendapatan": dict(zip(names, prcc(inc, Xp)))}
json.dump(S, open(sys.argv[2], "w"), indent=1)
for k, v in S.items():
    print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items() if not a.startswith("prcc")})
    for a, b in v.items():
        if a.startswith("prcc"): print("   ", a, {n: round(c, 2) for n, c in sorted(b.items(), key=lambda t: -abs(t[1]))[:4]})
