import sys, numpy as np, pandas as pd
sys.path.insert(0, "fase3"); import common
R = pd.read_pickle("fase7/d03_runs.pkl"); DT = 0.0625
def met(d, s1):
    an = common.annual(d); A = lambda v, a=2030, b=2055: float(an[v].loc[a:b].mean()); E = lambda v: float(d[v].iloc[-1])
    I = lambda x, v, a=2024, b=2087: float(x[v][(x.index >= a) & (x.index < b)].sum() * DT)
    keb = A("Kebutuhan Dana Minimum"); keb2 = float(an["Kebutuhan Dana Minimum"].loc[2060:2086].mean())
    cum = ((s1["Emisi Bersih Biomassa"] - d["Emisi Bersih Biomassa"]) * DT).cumsum()
    return {
     "E1 Hutan 2087 (ha)": E("Total Hutan"), "E2 Deforestasi kumulatif 2025–2086 (ha)": I(d, "Deforestasi Total", 2025, 2087), "E3 Deforestasi 2025–2030 (ha)": I(d, "Deforestasi Total", 2025, 2031),
     "E4 Deforestasi 2031–2086 (ha)": I(d, "Deforestasi Total", 2031, 2087), "E5 Emisi bersih biomassa kumulatif (tCO2e)": I(d, "Emisi Bersih Biomassa"),
     "E6 Manfaat karbon bersih kumulatif thd D0, 2087 (tCO2e)": float(cum.iloc[-2]), "E7 Puncak manfaat karbon bersih thd D0 (tCO2e)": float(cum.max()),
     "E8 Patroli tambahan dari jembatan (HOK, kumulatif)": I(d, "Hari Patroli Didanai Jembatan"), "E9 Patroli tambahan dari kas LPHD (HOK, kumulatif)": I(d, "Hari Patroli Didanai Kas LPHD"),
     "E10 Patroli tambahan kas LPHD 2031–2086 (HOK)": I(d, "Hari Patroli Didanai Kas LPHD", 2031, 2087),
     "F1 Pembiayaan jembatan (Rp)": E("Kumulatif Pembiayaan Jembatan"), "F2 Kas penjualan kredit (Rp)": I(d, "Kas Penjualan Kredit"), "F3 Biaya MRV, transaksi, pajak, pengganti (Rp)": I(d, "Biaya Transaksi dan MRV"),
     "F4 Pemulihan modal mitra (defisit + talangan) (Rp)": I(d, "Pemulihan Defisit Biaya Bersama") + I(d, "Pemulihan Pendanaan Awal"), "F5 Kerugian mitra diakui (hibah/penghapusan) (Rp)": E("Kerugian Mitra dari Penghapusan Talangan"),
     "F6 Defisit MRV belum dipulihkan 2087 (Rp)": E("Defisit Biaya Bersama Belum Dipulihkan"), "F7 Arus kas mitra nominal kumulatif (Rp)": I(d, "Arus Kas Mitra"), "F8 Dana kolektif LPHD dari karbon (Rp)": I(d, "Kas Masuk LPHD Karbon"),
     "F9 Cakupan kebutuhan minimum LPHD 2030–2055 (%)": 100 * A("Penggunaan Dana Pengelolaan") / keb if keb else np.nan, "F10 Cakupan kebutuhan minimum LPHD 2060–2086 (%)": 100 * float(an["Penggunaan Dana Pengelolaan"].loc[2060:2086].mean()) / keb2 if keb2 else np.nan,
     "F11 NPV mitra (Rp) [SEMENTARA]": E("NPV Mitra"), "F12 NPV proyek keseluruhan (Rp) [SEMENTARA]": E("NPV Proyek Keseluruhan"), "F13 Kredit diajukan (tCO2e)": I(d, "Kredit Karbon Diajukan"),
     "S1 HOK patroli berupah (kumulatif)": I(d, "HOK Patroli Berbayar"), "S2 FTE berupah 2030–2055": A("Kesempatan Kerja Berupah Setara Penuh"), "S3 FTE berupah 2060–2086": float(an["Kesempatan Kerja Berupah Setara Penuh"].loc[2060:2086].mean()),
     "S4 Upah tunai kegiatan PS (Rp, kumulatif)": I(d, "Upah Kegiatan PS"), "S5 KUPS aktif 2087": E("Jumlah KUPS Aktif"), "S6 Penerimaan anggota KUPS (Rp, kumulatif)": I(d, "Pendapatan KUPS Total"),
     "S7 Pendapatan bersih per RT bergantung 2030–2055 (Rp/th)": A("Pendapatan Bersih per RT Bergantung"),
     "S8 Pendapatan RT terdampak 2030–2055 (Rp/th)": A("Pendapatan Hutan per RT Bergantung") + A("Pendapatan Non Hutan per RT Bergantung") + A("Pendapatan Program per RT Bergantung") - A("Kehilangan per RT Terdampak"),
     "S9 Kehilangan akses agregat (Rp, kumulatif)": I(d, "Kehilangan Pendapatan Agregat"), "S10 Kehilangan per RT terdampak 2030–2055 (Rp/th)": A("Kehilangan per RT Terdampak"),
     "S11 Kompensasi (Rp)": 0.0}
rows = []
for (var, dt), out in R.items():
    if dt != 0.0625: continue
    s1 = out["D0"]; M = {k: met(d, s1) for k, d in out.items()}
    for h in [10, 20, 35]:
        D0, D1, D2, D3 = M["D0"], M["D1"], M[f"D2|{h}"], M[f"D3|{h}"]
        for ind in D0:
            r = {"Variasi": var, "Harga": h, "Indikator": ind, "D0": D0[ind], "D1": D1[ind], "D2": D2[ind], "D3": D3[ind],
                 "D1−D0 (pembiayaan awal)": D1[ind] - D0[ind], "D2−D1 (penjualan karbon sesudah jembatan)": D2[ind] - D1[ind], "D2−D0 (paket lengkap)": D2[ind] - D0[ind], "D3−D0 (karbon tanpa jembatan)": D3[ind] - D0[ind]}
            if f"D3h|{h}" in M: r["D3h (henti MRV)"] = M[f"D3h|{h}"][ind]
            r["Cek aditif"] = r["D2−D0 (paket lengkap)"] - r["D1−D0 (pembiayaan awal)"] - r["D2−D1 (penjualan karbon sesudah jembatan)"]
            rows.append(r)
df = pd.DataFrame(rows); df.to_pickle("fase7/hasil.pkl")
print("cek aditif maks", df["Cek aditif"].abs().max())
pd.set_option("display.width", 300); pd.set_option("display.max_rows", 200)
b = df[df["Variasi"] == "dasar"]
for h in [10, 20, 35]:
    print("== USD", h); print(b[b["Harga"] == h].set_index("Indikator")[["D0", "D1", "D2", "D3", "D1−D0 (pembiayaan awal)", "D2−D1 (penjualan karbon sesudah jembatan)", "D2−D0 (paket lengkap)", "D3−D0 (karbon tanpa jembatan)"]].map(lambda x: f"{x:,.4g}").to_string())
