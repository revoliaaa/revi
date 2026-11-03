import re, sys
sys.path.insert(0, "fase1b"); from usulan import P
txt = open("out/DKP_25HD_FINAL_3SKENARIO.mdl", encoding="utf-8").read().split("\\\\\\---///")[0]
E, U = {}, {}
for blk in txt.split("|\n"):
    m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
    if m: E[m.group(1).replace("{UTF-8}", "").strip()] = re.sub(r"\s+", " ", m.group(3).strip()); U[m.group(1).replace("{UTF-8}", "").strip()] = m.group(4).strip()
for k, v in P.items(): E[k] = v[0]; U[k] = v[1]
names = sorted(E, key=len, reverse=True)
BIG = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z0-9_])")
refs = lambda eq: list(dict.fromkeys(BIG.findall(" " + eq + " ")))
users = {}
for k, e in E.items():
    for r in refs(e):
        if r != k: users.setdefault(r, []).append(k)
def show(n): print(f"* {n} [{U.get(n)}] = {E.get(n)}\n     dipakai: {users.get(n, [])}")
for n in sys.argv[1].split(";"): show(n)
