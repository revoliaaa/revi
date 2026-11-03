import sys, json, numpy as np, openpyxl
sys.path.insert(0, sys.argv[1]); from lib import *
SP = sys.argv[1] + "/.."
m = load(sys.argv[2])
vars_ = json.load(open(SP + "/vars.json"))[1:]
kinds = {r[0]: r[3] for r in vars_}
wb = openpyxl.load_workbook(SP + "/paket/REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx", read_only=True)
sheets = {"2030": "4 Hasil 2030", "2050": "5 Hasil 2050", "2087": "6 Hasil 2087", "avg": "7 Rerata 2030-2055", "cum": "8 Kumulatif 2025-2086"}
ref = {}
for k, sh in sheets.items():
    rows = list(wb[sh].iter_rows(values_only=True)); H = rows[0]
    for r in rows[1:]:
        for j, c in enumerate(H[4:], 4):
            if r[j] not in (None, ""): ref[(k, r[0], c)] = float(r[j])
cols = sys.argv[3].split(",")
SC = {"A1 S1": {"Skenario Kebijakan": 1}, "A1 S2": {"Skenario Kebijakan": 2}, "A1 S3": {"Skenario Kebijakan": 3}}
for p in [6, 10, 15, 20, 35]: SC[f"A1 S4-{p}"] = {"Skenario Kebijakan": 4, "Harga Karbon": p}
pysd_names = {}
for c in cols:
    df = run(m, SC[c])
    # map column names
    S = summaries(df, {k: kinds.get(k) for k in df.columns})
    n = bad = 0; worst = []
    for (k, v, cc), val in ref.items():
        if cc != c or v not in S: continue
        x = S[v][k]
        if x is None or not np.isfinite(x): continue
        n += 1
        rel = abs(x - val) / max(abs(val), 1e-6)
        if rel > 1e-4 and abs(x - val) > 1e-6:
            bad += 1; worst.append((rel, k, v, val, x))
    worst.sort(reverse=True)
    print(f"{c}: {n} nilai dibandingkan, {bad} berbeda >1e-4")
    for w in worst[:8]: print("   ", w)
