"""Analisis statis (tanpa simulasi): referensi tak dikenal, loop aljabar, dan pemakai Switch Karbon pada persamaan usulan."""
import re, sys, json
sys.path.insert(0, "fase1b"); from usulan import P
txt = open("out/DKP_25HD_FINAL_3SKENARIO.mdl", encoding="utf-8").read().split("\\\\\\---///")[0]
base = {}
for blk in txt.split("|\n"):
    m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
    if m and "********" not in m.group(1): base[m.group(1).replace("{UTF-8}", "").strip()] = (m.group(3).strip(), m.group(4).strip(), "lookup" if m.group(2).startswith("(") else "")
# variabel model alokasi
alloc_extra = {"Alokasi Dana Kompensasi RT Terdampak", "Dana Fleksibel LPHD"}
E = {k: v[0] for k, v in base.items()}
for k, v in P.items(): E[k] = v[0]
lookups = {k for k, v in base.items() if v[2]}
names = sorted(E, key=len, reverse=True)
FUN = ["INTEG", "SMOOTHI", "DELAY FIXED", "SAMPLE IF TRUE", "INITIAL"]
def strip_dynamic(eq):
    # buang argumen fungsi berstatus (input tidak berpengaruh seketika)
    out = eq
    for f in FUN:
        while True:
            i = out.find(f + "(")
            if i < 0: break
            j = i + len(f) + 1; d = 1
            while d and j < len(out):
                d += {"(": 1, ")": -1}.get(out[j], 0); j += 1
            out = out[:i] + " 0 " + out[j:]
    return out
BIG = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z0-9_])")
def refs(eq):
    return list(dict.fromkeys(BIG.findall(" " + re.sub(r"\s+", " ", eq) + " ")))
KW = {"IF","THEN","ELSE","MIN","MAX","STEP","EXP","ZIDZ","INTEG","SMOOTHI","DELAY","FIXED","INITIAL","SAMPLE","TRUE","AND","OR","Time","PULSE","TRAIN","ABS","LN","SQRT"}
unknown = {}
for k in P:
    eq = P[k][0]; rest = " " + eq + " "
    rest = BIG.sub(" ", re.sub(r"\s+", " ", rest))
    toks = [t for t in re.findall(r"[A-Za-z][A-Za-z ]*[A-Za-z]|[A-Za-z]", rest) if t.strip() not in KW and not all(w in KW for w in t.split())]
    if toks: unknown[k] = toks
print("REFERENSI TAK DIKENAL:", unknown or "tidak ada")
G = {k: [r for r in refs(strip_dynamic(E[k])) if r != k] for k in E}
# Tarjan SCC
idx = {}; low = {}; st = []; on = set(); sccs = []; c = [0]
sys.setrecursionlimit(100000)
def sc(v):
    idx[v] = low[v] = c[0]; c[0] += 1; st.append(v); on.add(v)
    for w in G.get(v, []):
        if w not in E: continue
        if w not in idx: sc(w); low[v] = min(low[v], low[w])
        elif w in on: low[v] = min(low[v], idx[w])
    if low[v] == idx[v]:
        comp = []
        while True:
            w = st.pop(); on.discard(w); comp.append(w)
            if w == v: break
        if len(comp) > 1: sccs.append(comp)
for v in E:
    if v not in idx: sc(v)
print("LOOP ALJABAR (komponen terhubung kuat):", sccs or "tidak ada")
sk = [k for k in E if re.search(r"(?<![A-Za-z])Switch Karbon(?![A-Za-z])", E[k])]
print("PEMAKAI Switch Karbon setelah usulan:", sk)
# pemakai variabel yang diganti
for v in ["Hari Patroli Swadaya", "HOK Patroli", "Realisasi Pembiayaan Awal", "Dana Desa Diterima", "Faktor Penguatan Kelembagaan dari Karbon", "Pendapatan Kotor Penjualan Kredit", "Kas Penjualan Kredit", "Porsi Kas Karbon dalam Saldo", "Indeks Intensitas Perlindungan Tanpa Karbon", "Proporsi Realisasi Penanaman BAU", "Manfaat Ekonomi Penanaman", "Total Partisipasi Kegiatan PS", "Penanaman Didanai Karbon"]:
    print(f"  dipakai oleh [{v}]:", [k for k in E if k != v and v in refs(E[k])])
json.dump({"unknown": unknown, "scc": sccs, "switch_karbon": sk}, open("fase1b/cek_statis.json", "w"), indent=1)
