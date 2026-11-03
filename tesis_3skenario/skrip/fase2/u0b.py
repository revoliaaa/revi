import re, sys, json
sys.path.insert(0, "fase1b"); sys.path.insert(0, "fase2")
from usulan import P
import importlib.util
spec = importlib.util.spec_from_file_location("b", "fase2/build_2s.py")
src = open("fase2/build_2s.py").read(); EXTRA = eval(src[src.index("EXTRA = {") + 8: src.index("}\nmerged")+1])
def parse(path):
    txt = open(path, encoding="utf-8").read().split("\\\\\\---///")[0]; E = {}
    for blk in txt.split("|\n"):
        m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
        if m: E[m.group(1).replace("{UTF-8}", "").strip()] = (re.sub(r"\s+", " ", m.group(3).strip()), m.group(4).strip())
    return E
new = parse(sys.argv[1]); old = parse("out/DKP_25HD_FINAL_3SKENARIO.mdl")
design = {k: (v[0], v[1]) for k, v in P.items()}; design.update({k: (v[0], v[1]) for k, v in EXTRA.items()})
norm = lambda s: re.sub(r"\s+", "", s)
mismatch = [k for k, (eq, u) in design.items() if k not in new or norm(new[k][0]) != norm(eq) or new[k][1].split("[")[0].strip() != u.split("[")[0].strip()]
removed = sorted(set(old) - set(new)); added = sorted(set(new) - set(old))
unchanged_diff = [k for k in old if k in new and k not in design and norm(old[k][0]) != norm(new[k][0])]
res = {"rancangan": len(design), "identik": len(design) - len(mismatch), "tidak_identik": mismatch, "dihapus": removed, "ditambah": len(added),
       "tak_diubah_tapi_berbeda": unchanged_diff, "tak_diubah_identik": sum(1 for k in old if k in new and k not in design and norm(old[k][0]) == norm(new[k][0]))}
print(json.dumps(res, indent=1, ensure_ascii=False)); json.dump(res, open("fase2/u0b_teks.json", "w"), indent=1)
