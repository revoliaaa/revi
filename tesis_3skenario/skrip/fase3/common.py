import numpy as np, pandas as pd, pysd, warnings, sys; warnings.filterwarnings("ignore")
sys.path.insert(0, "work"); from lib import yearly
MDL = "fase2/DKP_25HD_FINAL_2SKENARIO.mdl"; DT = 0.0625
TS = list(np.round(np.arange(2024, 2087.0001, DT), 6))
STOCK = {"Total Hutan", "Saldo Dana LPHD", "Modal Usaha KUPS", "Anggota Patroli Aktif", "Jumlah KUPS Aktif", "Anggota KUPS Aktif", "Luas Tanam Didanai Karbon", "Indeks Kapasitas LPHD",
         "NPV Proyek Keseluruhan", "NPV Mitra", "NPV Inkremental Perdagangan Karbon", "PV Kas Masuk LPHD", "PV Kebutuhan Dana Minimum", "PV Penggunaan Dana LPHD", "Total Hutan Baseline",
         "PV Kontribusi Non Tunai", "PV Biaya MRV dan Transaksi", "PV Pembiayaan Awal", "PV Kas Penjualan Kredit"}
V = ["Total Hutan", "Total Hutan Baseline", "Deforestasi Total", "Deforestasi Total Baseline", "Emisi Deforestasi Biomassa", "Emisi Deforestasi Biomassa Baseline", "Total Emisi", "Total Serapan",
     "Total Emisi Bersih", "Serapan Rehabilitasi", "Kredit REDD Diajukan", "Kredit ARR Diajukan", "Potensi Kredit REDD Konservatif", "Potensi Kredit ARR Konservatif", "Kredit REDD Terbit",
     "Kredit REDD Terjual", "Kredit ARR Terjual", "Pendapatan Kotor Penjualan Kredit", "Kas Penjualan Kredit", "Biaya Transaksi dan MRV", "Kekurangan Biaya Bersama Ditanggung Mitra",
     "Dana Desa Diterima", "Kas Masuk LPHD Karbon", "Kas Masuk LPHD Non Karbon", "Dana Mitra dari Karbon", "Penggunaan Dana Pengelolaan", "Kebutuhan Dana Minimum", "Total Kebutuhan Dana Pengelolaan",
     "Kesenjangan Pembiayaan Minimum", "Saldo Dana LPHD", "Rasio Cakupan Kebutuhan Minimum", "NPV Proyek Keseluruhan", "NPV Mitra", "NPV Inkremental Perdagangan Karbon", "PV Kas Masuk LPHD",
     "PV Kebutuhan Dana Minimum", "PV Penggunaan Dana LPHD", "PV Kontribusi Non Tunai", "PV Biaya MRV dan Transaksi", "PV Pembiayaan Awal", "PV Kas Penjualan Kredit",
     "HOK Patroli Reguler PS", "Hari Patroli Pembiayaan Awal", "Hari Patroli Didanai Kas LPHD", "Total HOK Patroli", "Indeks Intensitas Perlindungan", "Anggota Patroli Aktif", "Efek Pengelolaan PS Aktif",
     "HOK Berupah PS", "HOK Sukarela PS", "Kesempatan Kerja Berupah Setara Penuh", "Kesempatan Kerja Sukarela Setara Penuh", "Upah Kegiatan PS", "Nilai Kontribusi Swadaya",
     "Jumlah KUPS Aktif", "Anggota KUPS Aktif", "Proporsi KUPS Produktif", "Penjualan KUPS", "Manfaat Ekonomi KUPS", "Pendapatan KUPS Total", "Modal Usaha KUPS",
     "Pendapatan Bersih per RT Bergantung", "Pendapatan Program per RT Bergantung", "Kehilangan Pendapatan Pembatasan Akses per RT", "Kehilangan per RT Terdampak", "Kehilangan Pendapatan Agregat",
     "Rumah Tangga Bergantung Hutan", "Penambahan Luas Penanaman", "Luas Tanam Didanai Karbon", "Indeks Kapasitas LPHD", "Realisasi Belanja Perlindungan", "Realisasi Belanja Pengembangan KUPS",
     "Realisasi Belanja Rehabilitasi Efektif", "Realisasi Belanja Pengendalian Kebakaran", "Realisasi Belanja Operasional LPHD", "Realisasi Belanja Penguatan Kelembagaan", "Realisasi Pembiayaan Awal"]
_M = None
def model():
    global _M
    if _M is None: _M = pysd.read_vensim(MDL)
    return _M
def run(p, cols=V):
    m = model(); m.reload(); return m.run(params=p, return_timestamps=TS, return_columns=cols, progress=False)
def annual(df):
    av, fi = yearly(df)
    out = av.copy()
    for c in df.columns:
        if c in STOCK: out[c] = fi[c]
    out.loc[2087] = df.iloc[-1]
    return out
def summary(df):
    an = annual(df); A = lambda v: float(an[v].loc[2030:2055].mean()); C = lambda v: float(an[v].loc[2025:2086].sum()); F = lambda v: float(df[v].iloc[:-1].sum() * DT)
    E = lambda v: float(df[v].iloc[-1])
    return {
     "Hutan 2087 (ha)": E("Total Hutan"), "Hutan baseline 2087 (ha)": E("Total Hutan Baseline"),
     "Deforestasi kumulatif 2025–2086 (ha)": C("Deforestasi Total"), "Deforestasi baseline kumulatif (ha)": C("Deforestasi Total Baseline"),
     "Laju deforestasi rerata 2030–2055 (ha/th)": A("Deforestasi Total"),
     "Emisi deforestasi biomassa kumulatif (tCO2e)": C("Emisi Deforestasi Biomassa"), "Emisi deforestasi baseline kumulatif (tCO2e)": C("Emisi Deforestasi Biomassa Baseline"),
     "Serapan rehabilitasi kumulatif (tCO2e)": C("Serapan Rehabilitasi"), "Emisi bersih kumulatif (tCO2e)": C("Total Emisi Bersih"),
     "Potensi kredit REDD vs baseline BAU (tCO2e)": F("Kredit REDD Diajukan"), "Potensi kredit ARR vs baseline (tCO2e)": F("Kredit ARR Diajukan"),
     "Potensi kredit REDD konservatif (pelaporan, tCO2e)": F("Potensi Kredit REDD Konservatif"), "Potensi kredit ARR konservatif (tCO2e)": F("Potensi Kredit ARR Konservatif"),
     "Kredit REDD terbit (tCO2e)": F("Kredit REDD Terbit"), "Kredit REDD terjual (tCO2e)": F("Kredit REDD Terjual"), "Kredit ARR terjual (tCO2e)": F("Kredit ARR Terjual"),
     "Kas penjualan kredit 2024–2086 (Rp)": F("Kas Penjualan Kredit"), "Biaya MRV, transaksi, pajak (Rp)": F("Biaya Transaksi dan MRV"),
     "Biaya ditalangi mitra sebelum surplus (Rp)": F("Kekurangan Biaya Bersama Ditanggung Mitra"),
     "Kas masuk LPHD karbon (Rp)": F("Kas Masuk LPHD Karbon"), "Kas masuk LPHD non-karbon (Rp)": F("Kas Masuk LPHD Non Karbon"), "Dana mitra (40 %) (Rp)": F("Dana Mitra dari Karbon"),
     "Belanja LPHD 2024–2086 (Rp)": F("Penggunaan Dana Pengelolaan"), "Kebutuhan minimum rerata 2030–2055 (Rp/th)": A("Kebutuhan Dana Minimum"),
     "Belanja LPHD rerata 2030–2055 (Rp/th)": A("Penggunaan Dana Pengelolaan"), "Kesenjangan minimum rerata 2030–2055 (Rp/th)": A("Kesenjangan Pembiayaan Minimum"),
     "Cakupan kebutuhan minimum rerata 2030–2055 (%)": 100 * A("Penggunaan Dana Pengelolaan") / A("Kebutuhan Dana Minimum") if A("Kebutuhan Dana Minimum") else np.nan,
     "PV kas LPHD / PV kebutuhan minimum (%)": 100 * E("PV Kas Masuk LPHD") / E("PV Kebutuhan Dana Minimum"),
     "Tahun kebutuhan minimum tercukupi (jumlah 2025–2086)": int((an["Rasio Cakupan Kebutuhan Minimum"].loc[2025:2086] >= 0.999).sum()),
     "NPV proyek keseluruhan (Rp) [SEMENTARA]": E("NPV Proyek Keseluruhan"), "NPV mitra (Rp) [SEMENTARA]": E("NPV Mitra"), "NPV inkremental karbon (Rp) [SEMENTARA]": E("NPV Inkremental Perdagangan Karbon"),
     "Patroli reguler rerata 2030–2055 (HOK/th)": A("HOK Patroli Reguler PS"), "Patroli tambahan kas rerata 2030–2055 (HOK/th)": A("Hari Patroli Didanai Kas LPHD"),
     "Intensitas perlindungan rerata 2030–2055": A("Indeks Intensitas Perlindungan"), "HOK berupah rerata 2030–2055": A("HOK Berupah PS"), "HOK sukarela rerata 2030–2055": A("HOK Sukarela PS"),
     "FTE berupah rerata 2030–2055": A("Kesempatan Kerja Berupah Setara Penuh"), "FTE sukarela rerata 2030–2055": A("Kesempatan Kerja Sukarela Setara Penuh"),
     "Upah kegiatan PS rerata (Rp/th)": A("Upah Kegiatan PS"), "Nilai kontribusi non-tunai rerata (Rp/th)": A("Nilai Kontribusi Swadaya"),
     "KUPS aktif rerata 2030–2055": A("Jumlah KUPS Aktif"), "KUPS aktif 2087": E("Jumlah KUPS Aktif"), "Anggota KUPS rerata": A("Anggota KUPS Aktif"),
     "Proporsi KUPS produktif rerata": A("Proporsi KUPS Produktif"), "Omzet KUPS rerata (Rp/th)": A("Penjualan KUPS"), "Surplus KUPS rerata (Rp/th)": A("Manfaat Ekonomi KUPS"),
     "Penerimaan anggota KUPS rerata (Rp/th)": A("Pendapatan KUPS Total"),
     "Pendapatan bersih per RT bergantung rerata (Rp/RT/th)": A("Pendapatan Bersih per RT Bergantung"), "Pendapatan program per RT rerata (Rp/RT/th)": A("Pendapatan Program per RT Bergantung"),
     "Kehilangan akses per RT rerata (Rp/RT/th)": A("Kehilangan Pendapatan Pembatasan Akses per RT"), "Kehilangan akses per RT terdampak rerata (Rp/RT/th)": A("Kehilangan per RT Terdampak"),
     "Rehabilitasi kumulatif (ha)": C("Penambahan Luas Penanaman"), "Kapasitas LPHD 2087": E("Indeks Kapasitas LPHD"),
    }
