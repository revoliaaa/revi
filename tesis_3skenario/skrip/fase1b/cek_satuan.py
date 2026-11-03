"""Pemeriksaan dimensional statis: satuan setiap persamaan diturunkan dari satuan yang dideklarasikan pada variabel masukannya."""
import re, sys, json, sympy as sp
sys.path.insert(0, "fase1b"); import os, importlib; P = importlib.import_module(os.environ.get("USULAN", "usulan")).P
txt = open(__import__("os").environ.get("MDL", "out/DKP_25HD_FINAL_3SKENARIO.mdl"), encoding="utf-8").read().split("\\\\\\---///")[0]
E, U, LK = {}, {}, set()
for blk in txt.split("|\n"):
    m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
    if m:
        n = m.group(1).replace("{UTF-8}", "").strip(); E[n] = re.sub(r"\s+", " ", m.group(3).strip()); U[n] = m.group(4).strip()
        if m.group(2).startswith("("): LK.add(n)
extra_units = {}
for k, v in P.items(): E[k] = v[0]; U[k] = v[1]
syms = {}
def unit(s):
    s = re.sub(r"\[.*?\]", "", str(s)).strip()
    if s in ("", "Dmnl", "None", "1"): return sp.Integer(1)
    t = re.sub(r"[A-Za-z][A-Za-z0-9_]*", lambda m: "D" if m.group(0) == "Dmnl" else f"S_{m.group(0)}", s)
    for w in re.findall(r"S_[A-Za-z0-9_]+", t): syms.setdefault(w, sp.Symbol(w, positive=True))
    return sp.sympify(t.replace("^", "**"), locals={**syms, "D": 1})
class Q:
    def __init__(s, u, w=False, v=None): s.u, s.w, s.v = u, w, v
    def _c(a, b, op):
        if a.w or b.w: return Q(b.u if a.w else a.u, a.w and b.w)
        if sp.simplify(a.u / b.u) != 1: raise ValueError(f"{op}: {a.u} vs {b.u}")
        return Q(a.u)
    def __add__(a, b): return a._c(b, "+")
    __radd__ = __add__
    def __sub__(a, b): return a._c(b, "-")
    __rsub__ = lambda a, b: b._c(a, "-")
    def __mul__(a, b): return Q(a.u * b.u, a.w and b.w)
    def __truediv__(a, b): return Q(a.u / b.u, a.w and b.w)
    def __neg__(a): return a
    def __pow__(a, b):
        if not b.w and sp.simplify(b.u) != 1: raise ValueError("pangkat bersatuan")
        if a.w or sp.simplify(a.u) == 1: return Q(sp.Integer(1), a.w)
        if b.v is not None: return Q(a.u ** b.v)
        raise ValueError(f"basis bersatuan {a.u} dengan pangkat variabel")
    def cmp(a, b): a._c(b, "banding"); return Q(sp.Integer(1))
W = lambda v=None: Q(sp.Integer(1), True, v)
def same(*xs):
    r = xs[0]
    for x in xs[1:]: r = r._c(x, "MIN/MAX/IF")
    return r
F = {"MIN": lambda a, b: same(a, b), "MAX": lambda a, b: same(a, b), "ZIDZ": lambda a, b: a / b, "XIDZ": lambda a, b, c: same(a / b, c),
     "IFTE": lambda c, a, b: same(a, b), "STEP": lambda h, t: (t._c(Q(unit("Year")), "STEP waktu"), h)[1], "EXP": lambda x: (dl(x), Q(sp.Integer(1)))[1],
     "LN": lambda x: (dl(x), Q(sp.Integer(1)))[1], "INITIAL": lambda x: x, "SMOOTHI": lambda x, d, i: (d._c(Q(unit("Year")), "SMOOTH waktu"), same(x, i))[1],
     "SMOOTH": lambda x, d: x, "DELAYFIXED": lambda x, d, i: (d._c(Q(unit("Year")), "DELAY waktu"), same(x, i))[1], "SAMPLEIFTRUE": lambda c, x, i: same(x, i),
     "PULSETRAIN": lambda a, b, c, d: Q(sp.Integer(1)), "INTEG": None, "ABS": lambda x: x, "SQRT": lambda x: Q(sp.sqrt(x.u), x.w)}
def dl(x):
    if not x.w and sp.simplify(x.u) != 1: raise ValueError(f"argumen EXP/LN bersatuan {x.u}")
names = sorted(E, key=len, reverse=True)
BIG = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z0-9_])")
idmap = {n: f"vv{i}x" for i, n in enumerate(names)}
def to_py(eq):
    s = " " + eq + " "
    s = BIG.sub(lambda m: f" V['{idmap[m.group(1)]}'] ", s)
    s = re.sub(r"IF THEN ELSE\s*\(", "IFTE(", s); s = s.replace("DELAY FIXED", "DELAYFIXED").replace("SAMPLE IF TRUE", "SAMPLEIFTRUE").replace("PULSE TRAIN", "PULSETRAIN")
    s = s.replace(":AND:", " and ").replace(":OR:", " or ").replace("<>", "!=")
    s = re.sub(r"(?<![<>!=])=(?!=)", "==", s); s = s.replace("^", "**")
    s = re.sub(r"(?<![A-Za-z_'\]\d])(\d+\.?\d*(?:[eE][+-]?\d+)?)", r"W(\1)", s)
    s = re.sub(r"\bTime\b", "TIME_", s)
    return s
class Vd(dict):
    def __missing__(s, k): raise KeyError(k)
def evaluate(n):
    eq = E[n]; uv = unit(U[n])
    if n in LK: return "lookup", None
    if eq.startswith("INTEG("):
        inner = eq[6:eq.rfind(")")]
        d = 0
        for i, ch in enumerate(inner):
            d += {"(": 1, ")": -1}.get(ch, 0)
            if ch == "," and d == 0: flow, init = inner[:i], inner[i+1:]; break
        r1 = ev(flow); r2 = ev(init)
        Q(uv / unit("Year"))._c(r1, "aliran stok"); Q(uv)._c(r2, "nilai awal stok"); return "ok", None
    r = ev(eq); Q(uv)._c(r, "deklarasi"); return "ok", None
class CmpQ(Q): pass
def ev(eq):
    py = to_py(eq)
    V = {idmap[k]: (Q(unit(U[k])) if k not in LK else (lambda x: Q(sp.Integer(1)))) for k in E}
    # lookup dipanggil sebagai fungsi
    for k in LK: py = py.replace(f"V['{idmap[k]}'] (", f"V['{idmap[k]}'](")
    py = re.sub(r"(Q\(|W\()", r"\1", py)
    env = {"V": V, "W": lambda v: W(v), "TIME_": Q(unit("Year")), **F}
    # perbandingan
    def wrap(a): return a
    Q.__gt__ = Q.__lt__ = Q.__ge__ = Q.__le__ = Q.__eq__ = Q.__ne__ = lambda a, b: a.cmp(b if isinstance(b, Q) else W(b))
    Q.__and__ = Q.__or__ = lambda a, b: Q(sp.Integer(1))
    return eval(py, env)
targets = sys.argv[1] if len(sys.argv) > 1 else "usulan"
check = list(P) if targets == "usulan" else [n for n in E if U.get(n) is not None]
res = {"ok": 0, "galat": {}}
for n in check:
    if n in ("INITIAL TIME", "FINAL TIME", "TIME STEP", "SAVEPER"): continue
    try: evaluate(n); res["ok"] += 1
    except Exception as e: res["galat"][n] = f"{type(e).__name__}: {e}"
print(f"{targets}: {res['ok']} persamaan konsisten; {len(res['galat'])} bermasalah")
for k, v in res["galat"].items(): print("  -", k, "|", v, "|", U[k], "|", E[k][:150])
json.dump(res, open(f"fase1b/cek_satuan_{targets}.json", "w"), indent=1, default=str)
