import pandas as pd, numpy as np
S = pd.read_pickle("fase4t3/ringkasan.pkl"); D = pd.read_pickle("fase4t3/selisih.pkl")
def f(x, d=0):
    if x is None or (isinstance(x, float) and x != x): return "–"
    if abs(x) < 0.5 * 10**-d: x = 0.0
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
H = [6, 10, 15, 20, 35]
def tab(title, rows, src="D"):
    out = [f"\n**{title}**\n", "| Indikator | " + " | ".join(f"{m} USD{h}" for m in ["C-J1", "C-JP"] for h in H) + " |", "|---|" + "---|" * 10]
    for lab, key, sc, d, sign in rows:
        T = D if src == "D" else S
        out.append(f"| {lab} | " + " | ".join(f(sign * T.loc[key, f"{m}|{h}"] / sc, d) for m in ["C-J1", "C-JP"] for h in H) + " |")
    return "\n".join(out)
txt = []
txt.append(tab("Tabel 1. Ekologi: selisih S2 − S1 (USD 6 s.d. 35)", [
 ("Deforestasi dihindari 2025–2086 (ha)", "E Deforestasi kumulatif 2025–2086 (ha)", 1, 0, -1), ("Δ hutan 2087 (ha)", "E Hutan 2087 (ha)", 1, 0, 1),
 ("Emisi deforestasi dihindari (ribu tCO₂e)", "E Emisi deforestasi biomassa kumulatif (tCO2e)", 1e3, 1, -1), ("Emisi bersih biomassa dihindari (ribu tCO₂e)", "E Emisi bersih biomassa kumulatif (tCO2e)", 1e3, 1, -1),
 ("Tambahan serapan rehabilitasi (ribu tCO₂e)", "E Serapan rehabilitasi kumulatif (tCO2e)", 1e3, 1, 1), ("Tambahan rehabilitasi (ha)", "E Rehabilitasi kumulatif (ha)", 1, 0, 1),
 ("Δ intensitas perlindungan 2030–2055", "E Intensitas perlindungan rerata 2030–2055", 1, 3, 1), ("Patroli kas LPHD 2060–2080 (HOK/th)", "E Patroli kas LPHD rerata 2060–2080 (HOK/th)", 1, 0, 1)]))
txt.append(tab("Tabel 2. Pembiayaan dan keuangan proyek (nilai S2; Rp miliar nominal kecuali NPV)", [
 ("Kredit REDD diajukan (ribu tCO₂e)", "F Kredit REDD diajukan (tCO2e)", 1e3, 1, 1), ("Kredit ARR diajukan (ribu tCO₂e)", "F Kredit ARR diajukan (tCO2e)", 1e3, 1, 1),
 ("Kredit terjual (ribu tCO₂e)", "F Kredit terjual (tCO2e)", 1e3, 1, 1), ("Potensi thd BAU, pelaporan (ribu tCO₂e)", "F Potensi kredit REDD thd BAU (pelaporan, tCO2e)", 1e3, 1, 1),
 ("Kas penjualan", "F Kas penjualan (Rp)", 1e9, 2, 1), ("Biaya MRV, transaksi, pajak, pengganti", "F Biaya MRV, transaksi, pajak, pengganti (Rp)", 1e9, 2, 1),
 ("…di antaranya biaya kredit pengganti", "F Biaya kredit pengganti reversal (Rp)", 1e9, 2, 1), ("Debit reversal belum diselesaikan 2087 (ribu tCO₂e)", "F Debit reversal belum diselesaikan 2087 (tCO2e)", 1e3, 1, 1),
 ("Pembiayaan jembatan", "F Pembiayaan jembatan (Rp)", 1e9, 2, 1), ("Sisa talangan 2087", "F Sisa talangan 2087 (Rp)", 1e9, 2, 1), ("Defisit MRV ditalangi mitra 2087", "F Defisit MRV ditalangi mitra 2087 (Rp)", 1e9, 2, 1),
 ("Kas LPHD karbon", "F Kas LPHD karbon (Rp)", 1e9, 2, 1), ("Dana mitra 40 %", "F Dana mitra 40 % (Rp)", 1e9, 2, 1),
 ("NPV inkremental karbon [SEMENTARA]", "F NPV inkremental karbon (Rp) [SEMENTARA]", 1e9, 2, 1)], src="S"))
r = ["| Indikator | " + " | ".join(f"{m} USD{h}" for m in ["C-J1", "C-JP"] for h in H) + " |", "|---|" + "---|" * 10]
r.append("| NPV mitra inkremental thd S1 (Rp miliar) [SEMENTARA] | " + " | ".join(f(D.loc["F NPV mitra (Rp) [SEMENTARA]", f"{m}|{h}"] / 1e9, 2) for m in ["C-J1", "C-JP"] for h in H) + " |")
r.append("| Tahun kas LPHD pertama | " + " | ".join(("–" if S.loc["F Tahun kas LPHD pertama", f"{m}|{h}"] != S.loc["F Tahun kas LPHD pertama", f"{m}|{h}"] else f"{S.loc['F Tahun kas LPHD pertama', f'{m}|{h}']:.1f}".replace(".", ",")) for m in ["C-J1", "C-JP"] for h in H) + " |")
txt.append("\n" + "\n".join(r))
txt.append(tab("Tabel 3. Keberlanjutan pembiayaan dan kelembagaan LPHD (nilai S2; S1 = 0 untuk semua indikator kas)", [
 ("Cakupan kebutuhan minimum 2030–2055 (%)", "L Cakupan kebutuhan minimum LPHD rerata 2030–2055 (%)", 1, 1, 1), ("Cakupan kebutuhan minimum 2060–2086 (%)", "L Cakupan kebutuhan minimum LPHD rerata 2060–2086 (%)", 1, 1, 1),
 ("Tahun kebutuhan minimum tercukupi (dari 62)", "L Tahun kebutuhan minimum tercukupi ≥ 99,9 % (2025–2086)", 1, 0, 1), ("Tahun dengan kas LPHD > 0 (dari 62)", "L Tahun dengan kas LPHD > 0 (2025–2086)", 1, 0, 1),
 ("Kas LPHD 2030–2055 (Rp juta/th)", "L Kas LPHD rerata 2030–2055 (Rp/th)", 1e6, 0, 1), ("Kas LPHD 2060–2086 (Rp juta/th)", "L Kas LPHD rerata 2060–2086 (Rp/th)", 1e6, 0, 1),
 ("Belanja operasional + kelembagaan (Rp juta/th)", "L Belanja operasional + kelembagaan LPHD rerata (Rp/th)", 1e6, 0, 1), ("Kapasitas LPHD 2087 (S1 = 0,50)", "L Kapasitas LPHD 2087", 1, 2, 1)], src="S"))
txt.append(tab("Tabel 4. Sosial-ekonomi: selisih S2 − S1 (rerata 2030–2055 kecuali disebut)", [
 ("HOK berupah PS", "S HOK berupah PS", 1, 0, 1), ("…patroli berbayar", "S HOK patroli berbayar", 1, 0, 1), ("…penanaman berupah", "S HOK penanaman berupah", 1, 0, 1), ("…pengendalian kebakaran", "S HOK pengendalian kebakaran", 1, 0, 1),
 ("HOK sukarela PS", "S HOK sukarela PS", 1, 0, 1), ("FTE berupah", "S FTE berupah", 1, 1, 1), ("FTE berupah 2060–2086", "S FTE berupah rerata 2060–2086", 1, 1, 1),
 ("Upah kegiatan PS (Rp juta/th)", "S Upah kegiatan PS (Rp/th)", 1e6, 1, 1), ("KUPS aktif", "S KUPS aktif rerata", 1, 1, 1), ("KUPS aktif 2087", "S KUPS aktif 2087", 1, 1, 1),
 ("Anggota KUPS", "S Anggota KUPS", 1, 0, 1), ("Omzet KUPS (Rp juta/th)", "S Omzet KUPS (Rp/th)", 1e6, 1, 1), ("Surplus KUPS (Rp juta/th)", "S Surplus KUPS (Rp/th)", 1e6, 1, 1),
 ("Penerimaan anggota KUPS (Rp juta/th)", "S Penerimaan anggota KUPS (Rp/th)", 1e6, 1, 1), ("Modal usaha KUPS 2087 (Rp juta)", "S Modal usaha KUPS 2087 (Rp)", 1e6, 1, 1),
 ("Pendapatan hutan per RT (Rp/th)", "S Pendapatan hutan per RT (Rp/th)", 1, 0, 1), ("Pendapatan program per RT (Rp/th)", "S Pendapatan program per RT (Rp/th)", 1, 0, 1),
 ("Kehilangan akses per RT bergantung (Rp/th)", "S Kehilangan akses per RT bergantung (Rp/th)", 1, 0, 1), ("Kehilangan per RT terdampak (Rp/th)", "S Kehilangan per RT terdampak (Rp/th)", 1, 0, 1),
 ("Kompensasi (Rp/th)", "S Kompensasi (Rp/th)", 1, 0, 1), ("Pendapatan bersih per RT bergantung (Rp/th)", "S Pendapatan bersih per RT bergantung (Rp/th)", 1, 0, 1),
 ("Kehilangan pendapatan agregat (Rp juta/th)", "S Kehilangan pendapatan agregat (Rp/th)", 1e6, 0, 1)]))
s1 = ["\n**Nilai S1 (acuan)**\n", "| Indikator | S1 |", "|---|---|"]
for lab, k, sc, d in [("Hutan 2087 (ha)", "E Hutan 2087 (ha)", 1, 0), ("Deforestasi 2025–2086 (ha)", "E Deforestasi kumulatif 2025–2086 (ha)", 1, 0), ("Laju deforestasi 2030–2055 (ha/th)", "E Laju deforestasi rerata 2030–2055 (ha/th)", 1, 0),
    ("Patroli reguler sukarela (HOK/th)", "S HOK patroli reguler rerata (sukarela)", 1, 0), ("FTE sukarela", "S FTE sukarela", 1, 1), ("Nilai kontribusi non-tunai (Rp juta/th)", "S Nilai kontribusi non-tunai (Rp/th)", 1e6, 0),
    ("KUPS aktif rerata / 2087", None, 1, 1), ("Penerimaan anggota KUPS (Rp juta/th)", "S Penerimaan anggota KUPS (Rp/th)", 1e6, 1), ("Pendapatan bersih per RT bergantung (Rp juta/th)", "S Pendapatan bersih per RT bergantung (Rp/th)", 1e6, 2),
    ("Kehilangan akses per RT terdampak (Rp/th)", "S Kehilangan per RT terdampak (Rp/th)", 1, 0), ("NPV keseluruhan (Rp miliar) [SEMENTARA]", "F NPV proyek keseluruhan (Rp) [SEMENTARA]", 1e9, 2)]:
    v = f"{f(S.loc['S KUPS aktif rerata','S1'],1)} / {f(S.loc['S KUPS aktif 2087','S1'],1)}" if k is None else f(S.loc[k, "S1"] / sc, d)
    s1.append(f"| {lab} | {v} |")
txt.append("\n".join(s1))
A = ["\n**Pembanding eksploratif mekanisme A (baseline BAU; tidak lolos uji additionality model)**\n", "| Indikator | " + " | ".join(f"A USD{h}" for h in H) + " |", "|---|" + "---|" * 5]
for lab, k, sc, d, sg in [("Kredit REDD diajukan (ribu tCO₂e)", "F Kredit REDD diajukan (tCO2e)", 1e3, 1, 0), ("Deforestasi dihindari S2−S1 (ha)", "E Deforestasi kumulatif 2025–2086 (ha)", 1, 0, -1), ("NPV mitra inkremental (Rp miliar)", "F NPV mitra (Rp) [SEMENTARA]", 1e9, 2, 1)]:
    A.append(f"| {lab} | " + " | ".join(f((S.loc[k, f'A|{h}'] if sg == 0 else sg * D.loc[k, f'A|{h}']) / sc, d) for h in H) + " |")
txt.append("\n".join(A))
open("fase4t3/tabel.md", "w").write("\n".join(txt)); print("\n".join(txt)[:6000])
