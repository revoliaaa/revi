import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4g"); from gate import LAND, CD, CMP, REF
R = pd.read_pickle("fase4g/gate_runs.pkl"); TOL = json.load(open("fase4g/toleransi.json")); FE = (1-.1)*(1-.12)*.682
def ck(d, ref=False): return sum((d[REF(v)] if ref else d[v]) * CD[v] for v in LAND)
rows = []
for name, r in R.items():
    s1, dt = r["S1"], r["dt"]
    for mode in ["S2_endogen", "S2_berpasangan"]:
        d = r[mode]; o = {"konfigurasi": name, "mode": mode.replace("S2_", ""), "harga": r["h"], "DT": dt}
        for v in CMP:
            a, b = d[REF(v)], s1[v]; o[f"maks |Δ| {v}"] = float((a - b).abs().max()); o[f"maks rel {v}"] = float(((a - b).abs() / (b.abs() + 1)).max())
        o["maks |Δ| stok karbon (tC)"] = float((ck(d, True) - ck(s1)).abs().max())
        e = d[REF("Emisi Deforestasi Biomassa")] - s1["Emisi Deforestasi Biomassa"]
        o["Δ emisi deforestasi kumulatif (tCO2e)"] = float(e.iloc[:-1].sum() * dt)
        sig = float((s1["Emisi Deforestasi Biomassa"] - d["Emisi Deforestasi Biomassa"]).iloc[:-1].sum() * dt)
        o["sinyal mitigasi S1−S2 kumulatif (tCO2e)"] = sig
        o["galat relatif thd sinyal"] = abs(o["Δ emisi deforestasi kumulatif (tCO2e)"]) / abs(sig) if abs(sig) > 1 else (0.0 if abs(o["Δ emisi deforestasi kumulatif (tCO2e)"]) < 1e-6 else np.inf)
        o["kredit REDD diajukan"] = float(d["Kredit REDD Diajukan"].iloc[:-1].sum() * dt)
        if mode == "S2_endogen":
            ok = o["maks |Δ| Total Hutan"] <= TOL["endogen_hutan_ha"] and o["galat relatif thd sinyal"] <= TOL["endogen_emisi_kum_rel_sinyal"]
        else:
            ok = max(o[f"maks rel {v}"] for v in CMP) <= TOL["berpasangan_rel"]
        o["status"] = "SETARA" if ok else "SELISIH MATERIAL"
        rows.append(o)
df = pd.DataFrame(rows); df.to_pickle("fase4g/gate_tabel.pkl")
pd.set_option("display.width", 250)
print(df[["konfigurasi", "mode", "maks |Δ| Total Hutan", "maks |Δ| Deforestasi Total", "maks |Δ| stok karbon (tC)", "Δ emisi deforestasi kumulatif (tCO2e)", "sinyal mitigasi S1−S2 kumulatif (tCO2e)", "galat relatif thd sinyal", "status"]].to_string(float_format=lambda x: f"{x:.3g}"))
