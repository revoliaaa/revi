import sys, json, numpy as np, openpyxl
sys.path.insert(0, sys.argv[1]); from lib import *
SP = sys.argv[1] + "/.."
m = load(sys.argv[2])
kinds = {r[0]: r[3] for r in json.load(open(SP + "/vars.json"))[1:]}
wb = openpyxl.load_workbook(SP + "/paket/REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx", read_only=True)
lst = {r[0]: r for r in wb["1 Daftar skenario"].iter_rows(values_only=True)}
sheets = {"2030": "4 Hasil 2030", "2050": "5 Hasil 2050", "2087": "6 Hasil 2087", "avg": "7 Rerata 2030-2055", "cum": "8 Kumulatif 2025-2086"}
ref = {}
for k, sh in sheets.items():
    rows = list(wb[sh].iter_rows(values_only=True)); H = rows[0]
    for r in rows[1:]:
        for j, c in enumerate(H[4:], 4):
            if r[j] not in (None, ""): ref[(k, r[0], c)] = float(r[j])
for c in sys.argv[3].split(","):
    params = {}
    for kv in lst[c][4].split(";"):
        k, v = kv.split("="); params[k.strip()] = {"0.1333":2/15,"0.0667":1/15}.get(v.strip(), float(v))
    df = run(m, params)
    S = summaries(df, kinds)
    n = bad = 0; worst = []
    for (k, v, cc), val in ref.items():
        if cc != c or v not in S: continue
        x = S[v][k]; n += 1
        if abs(x - val) / max(abs(val), 1e-6) > 1e-4 and abs(x - val) > 1e-6:
            bad += 1; worst.append((abs(x-val)/max(abs(val),1e-6), k, v, val, x))
    worst.sort(reverse=True)
    print(f"{c}: {n} dibandingkan, {bad} berbeda"); [print("   ", w) for w in worst[:6]]; print("   vars:", sorted(set(w[2] for w in worst)))
