import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase3"); import common
R = pd.read_pickle("fase4t3/det_runs.pkl"); DT = 0.0625; FE = (1-.1)*(1-.12)*.682
S1 = R[("S1", 0)]
def first(s, thr=1e-6): i = np.where(s.values > thr)[0]; return float(s.index[i[0]]) if len(i) else np.nan
def summ(d):
    an = common.annual(d); A = lambda v, a=2030, b=2055: float(an[v].loc[a:b].mean())
    F = lambda v: float(d[v].iloc[:-1].sum() * DT); E = lambda v: float(d[v].iloc[-1]); C = lambda v: float(an[v].loc[2025:2086].sum())
    keb = A("Kebutuhan Dana Minimum"); rasio = an["Rasio Cakupan Kebutuhan Minimum"].loc[2025:2086]
    pk = an["Hari Patroli Didanai Kas LPHD"]; kas = an["Dana Desa Diterima"]
    o = {
     # ---- 1 ekologi
     "E Hutan 2087 (ha)": E("Total Hutan"), "E Deforestasi kumulatif 2025–2086 (ha)": C("Deforestasi Total"), "E Laju deforestasi rerata 2030–2055 (ha/th)": A("Deforestasi Total"),
     "E Emisi deforestasi biomassa kumulatif (tCO2e)": F("Emisi Deforestasi Biomassa"), "E Emisi bersih biomassa kumulatif (tCO2e)": F("Emisi Bersih Biomassa"),
     "E Serapan rehabilitasi kumulatif (tCO2e)": F("Serapan Rehabilitasi"), "E Rehabilitasi kumulatif (ha)": C("Penambahan Luas Penanaman"), "E Stok karbon biomassa 2087 (tC)": E("Stok Karbon Biomassa Efektif"),
     "E Intensitas perlindungan rerata 2030–2055": A("Indeks Intensitas Perlindungan"), "E Patroli tambahan rerata 2030–2055 (HOK/th)": A("Hari Patroli Didanai Kas LPHD") + A("Hari Patroli Didanai Jembatan"),
     "E Patroli kas LPHD rerata 2060–2080 (HOK/th)": float(pk.loc[2060:2080].mean()),
     # ---- 2 pembiayaan
     "F Kredit REDD diajukan (tCO2e)": F("Kredit REDD Diajukan"), "F Kredit ARR diajukan (tCO2e)": F("Kredit ARR Diajukan"), "F Kredit terbit (tCO2e)": F("Kredit Karbon Terbit"), "F Kredit terjual (tCO2e)": F("Kredit Karbon Terjual"),
     "F Potensi kredit REDD thd BAU (pelaporan, tCO2e)": F("Potensi Kredit REDD terhadap BAU"),
     "F Kas penjualan (Rp)": F("Kas Penjualan Kredit"), "F Biaya MRV, transaksi, pajak, pengganti (Rp)": F("Biaya Transaksi dan MRV"), "F Biaya kredit pengganti reversal (Rp)": F("Biaya Penggantian Reversal"),
     "F Kredit pengganti dibeli (tCO2e)": E("Kredit Pengganti Reversal Kumulatif"), "F Buffer dipakai (tCO2e)": E("Kumulatif Penggunaan Buffer Reversal"), "F Debit reversal belum diselesaikan 2087 (tCO2e)": E("Reversal Belum Terkompensasi"),
     "F Pembiayaan jembatan (Rp)": E("Kumulatif Pembiayaan Jembatan"), "F Sisa talangan 2087 (Rp)": E("Pendanaan Awal Belum Terpulihkan"), "F Defisit MRV ditalangi mitra 2087 (Rp)": E("Defisit Biaya Bersama Belum Dipulihkan"),
     "F Kas LPHD karbon (Rp)": F("Kas Masuk LPHD Karbon"), "F Dana mitra 40 % (Rp)": F("Dana Mitra dari Karbon"),
     "F NPV proyek keseluruhan (Rp) [SEMENTARA]": E("NPV Proyek Keseluruhan"), "F NPV inkremental karbon (Rp) [SEMENTARA]": E("NPV Inkremental Perdagangan Karbon"), "F NPV mitra (Rp) [SEMENTARA]": E("NPV Mitra"),
     "F Tahun kas penjualan pertama": first(d["Kas Penjualan Kredit"]), "F Tahun kas LPHD pertama": first(d["Kas Masuk LPHD Karbon"]),
     "L Cakupan kebutuhan minimum LPHD rerata 2030–2055 (%)": 100 * A("Penggunaan Dana Pengelolaan") / keb if keb else np.nan,
     "L Cakupan kebutuhan minimum LPHD rerata 2060–2086 (%)": 100 * float(an["Penggunaan Dana Pengelolaan"].loc[2060:2086].mean()) / float(an["Kebutuhan Dana Minimum"].loc[2060:2086].mean()),
     "L Tahun kebutuhan minimum tercukupi ≥ 99,9 % (2025–2086)": int((rasio >= 0.999).sum()), "L Tahun dengan kas LPHD > 0 (2025–2086)": int((kas.loc[2025:2086] > 1).sum()),
     "L Kas LPHD rerata 2030–2055 (Rp/th)": A("Dana Desa Diterima"), "L Kas LPHD rerata 2060–2086 (Rp/th)": float(kas.loc[2060:2086].mean()),
     "L Belanja LPHD rerata 2030–2055 (Rp/th)": A("Penggunaan Dana Pengelolaan"), "L Saldo LPHD 2087 (Rp)": E("Saldo Dana LPHD"), "L Kapasitas LPHD 2087": E("Indeks Kapasitas LPHD"),
     "L Belanja operasional + kelembagaan LPHD rerata (Rp/th)": A("Realisasi Belanja Operasional LPHD") + A("Realisasi Belanja Penguatan Kelembagaan"),
     "L Porsi kas LPHD dari karbon (%)": 100 * F("Kas Masuk LPHD Karbon") / F("Dana Desa Diterima") if F("Dana Desa Diterima") > 0 else np.nan,
     # ---- 3 sosial-ekonomi
     "S HOK patroli reguler rerata (sukarela)": A("HOK Patroli Reguler PS"), "S HOK berupah PS": A("HOK Berupah PS"), "S HOK sukarela PS": A("HOK Sukarela PS"),
     "S HOK patroli berbayar": A("HOK Patroli Berbayar"), "S HOK penanaman berupah": A("HOK Penanaman Berupah"), "S HOK penanaman sukarela": A("HOK Penanaman Sukarela"), "S HOK pengendalian kebakaran": A("HOK Pengendalian Kebakaran"),
     "S FTE berupah": A("Kesempatan Kerja Berupah Setara Penuh"), "S FTE sukarela": A("Kesempatan Kerja Sukarela Setara Penuh"), "S FTE berupah rerata 2060–2086": float(an["Kesempatan Kerja Berupah Setara Penuh"].loc[2060:2086].mean()),
     "S Upah kegiatan PS (Rp/th)": A("Upah Kegiatan PS"), "S Upah patroli (Rp/th)": A("Upah Patroli Berbayar"), "S Nilai kontribusi non-tunai (Rp/th)": A("Nilai Kontribusi Swadaya"),
     "S KUPS aktif rerata": A("Jumlah KUPS Aktif"), "S KUPS aktif 2087": E("Jumlah KUPS Aktif"), "S Anggota KUPS": A("Anggota KUPS Aktif"), "S Proporsi KUPS produktif": A("Proporsi KUPS Produktif"),
     "S Omzet KUPS (Rp/th)": A("Penjualan KUPS"), "S Surplus KUPS (Rp/th)": A("Manfaat Ekonomi KUPS"), "S Penerimaan anggota KUPS (Rp/th)": A("Pendapatan KUPS Total"), "S Modal usaha KUPS 2087 (Rp)": E("Modal Usaha KUPS"),
     "S Pendapatan hutan per RT (Rp/th)": A("Pendapatan Hutan per RT Bergantung"), "S Pendapatan program per RT (Rp/th)": A("Pendapatan Program per RT Bergantung"),
     "S Kehilangan akses per RT bergantung (Rp/th)": A("Kehilangan Pendapatan Pembatasan Akses per RT"), "S Kehilangan per RT terdampak (Rp/th)": A("Kehilangan per RT Terdampak"),
     "S Kompensasi (Rp/th)": 0.0, "S Pendapatan bersih per RT bergantung (Rp/th)": A("Pendapatan Bersih per RT Bergantung"),
     "S Kehilangan pendapatan agregat (Rp/th)": A("Kehilangan Pendapatan Agregat"),
    }
    return o
S = {f"{k[0]}|{k[1]}" if k[0] != "S1" else "S1": summ(d) for k, d in R.items()}
df = pd.DataFrame(S); df.to_pickle("fase4t3/ringkasan.pkl")
D = pd.DataFrame({k: df[k] - df["S1"] for k in df.columns if k != "S1"})
inv = [i for i in df.index if i.startswith(("E Deforestasi", "E Emisi", "E Laju", "S Kehilangan"))]
D.to_pickle("fase4t3/selisih.pkl")
pd.set_option("display.width", 320); pd.set_option("display.max_rows", 200)
print(df[["S1"] + [c for c in df.columns if c.startswith("C-J1")]].to_string(float_format=lambda x: f"{x:,.4g}"))
print(D[[c for c in D.columns if c.startswith("C-JP")]].to_string(float_format=lambda x: f"{x:,.4g}"))
