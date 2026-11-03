import json, pandas as pd
R = json.load(open("fase3b/mek_hasil.json"))
def f(x, d=0):
    if x is None or x != x: return "–"
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
M = lambda x: f(x / 1e9, 2)
Y = lambda x: "–" if x is None or x != x else f"{x:.2f}".replace(".", ",")
MK = [("A", "A|{}"), ("B", "B|{}"), ("C-J1", "C|{}|J1|d5|h0|m0"), ("C-JP", "C|{}|JP|d5|h0|m0")]
out = []
out.append("| Harga | Mek. | Kredit diajukan (ribu tCO₂e) | Terbit | Terjual | Kas diterima (Rp M) | Biaya MRV dll. (Rp M) | Kas LPHD (Rp M) | Dana mitra 40 % (Rp M) | Kredit diajukan pertama | Kas penjualan pertama | Kas LPHD pertama |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for h in [6, 10, 15, 20, 35]:
    for m, k in MK:
        r = R[k.format(h)]
        out.append(f"| {h} | {m} | {f((r['Kredit REDD diajukan (tCO2e)']+r['Kredit ARR diajukan (tCO2e)'])/1e3,1)} | {f(r['Kredit terbit (tCO2e)']/1e3,1)} | {f(r['Kredit terjual (tCO2e)']/1e3,1)} | {M(r['Kas penjualan diterima (Rp)'])} | {M(r['Biaya MRV, transaksi, pajak (Rp)'])} | {M(r['Kas masuk LPHD karbon (Rp)'])} | {M(r['Dana mitra 40 % (Rp)'])} | {Y(r['Tahun kredit pertama diajukan'])} | {Y(r['Tahun kas penjualan pertama'])} | {Y(r['Tahun kas LPHD karbon pertama'])} |")
out.append("\nTABEL2\n")
out.append("| Harga | Mek. | Deforestasi dihindari S2−S1 (ha) | Emisi dihindari S2−S1 (ribu tCO₂e) | Emisi dihindari thd BAU (ribu tCO₂e) | Talangan/jembatan (Rp M) | Sisa talangan 2087 (Rp M) | Defisit MRV 2087 (Rp M) | Eksposur mitra maks. (Rp M) | NPV proyek (Rp M) | NPV mitra inkremental (Rp M) | Cakupan LPHD (%) | Δ FTE berupah |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for h in [6, 10, 15, 20, 35]:
    for m, k in MK:
        r = R[k.format(h)]
        out.append(f"| {h} | {m} | {f(r['Deforestasi dihindari S2−S1 (ha)'])} | {f(r['Emisi deforestasi dihindari S2−S1 (tCO2e)']/1e3,1)} | {f(r['Emisi deforestasi dihindari thd BAU (tCO2e)']/1e3,1)} | {M(r['Pokok talangan kumulatif (Rp)'])} | {M(r['Sisa talangan 2087 (Rp)'])} | {M(r['Defisit biaya bersama 2087 (Rp)'])} | {M(r['Eksposur kas mitra maks. di luar pembiayaan historis (Rp)'])} | {M(r['NPV proyek keseluruhan (Rp) [SEMENTARA]'])} | {M(r['NPV mitra inkremental thd S1 (Rp) [SEMENTARA]'])} | {f(r['Cakupan kebutuhan minimum LPHD 2030–2055 (%)'],1)} | {f(r['Δ FTE berupah 2030–2055'],1)} |")
print("\n".join(out))
print("S1 NPV proyek", M(R["S1"]["NPV proyek keseluruhan (Rp) [SEMENTARA]"]))
