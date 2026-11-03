import json, sys
sys.path.insert(0, sys.argv[1]); from build_mdl import build; from revisi_3s import *
R = json.load(open(sys.argv[2]))[1:]
mode = sys.argv[4]  # 'main' or 'alloc'
R = [r for r in R if r[0] not in REMOVE]
extra = []
for n, v, k, eq, u, c in NEW:
    rr = [None]*23; rr[0]=n; rr[1]=v; rr[3]=k; rr[4]=eq; rr[6]=u; rr[22]=c; extra.append(rr)
ov = dict(OVERRIDES)
if mode == "alloc":
    import importlib.util
    D = json.load(open(sys.argv[5]))[1:]
    for r in D:
        if r[3] == 'Hanya model eksperimen alokasi':
            rr = [None]*23; rr[0]=r[0]; rr[1]="14 LPHD Finance Allocation"; rr[3]=r[4]; rr[4]=r[6]; rr[6]=r[7]; rr[22]=r[19]; extra.append(rr)
    spec = importlib.util.spec_from_file_location("ba", sys.argv[1] + "/alloc_ov.py"); ba = importlib.util.module_from_spec(spec); spec.loader.exec_module(ba)
    ov.update(ba.OV)
build(R, sys.argv[3], overrides=ov, extra=extra)
print("variabel:", len(R) + len(extra))
