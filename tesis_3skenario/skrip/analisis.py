"""Indikator RQ1-RQ3 dan analisis finansial (NPV, harga impas) dari keluaran model."""
import numpy as np, pandas as pd
from lib import run, yearly, DT
VARS = ["Total Hutan","Deforestasi Total","Total Emisi Bersih","Kredit REDD Diajukan","Pendapatan Kotor Penjualan Kredit",
 "Biaya Transaksi dan MRV","Dana Desa Diterima","Dana Mitra dari Karbon","Realisasi Pembiayaan Awal","Penggunaan Dana Pengelolaan",
 "Kekurangan Biaya Bersama Ditanggung Mitra","Pemulihan Defisit Biaya Bersama","Kebutuhan Dana Minimum","Kesenjangan Pembiayaan Minimum",
 "Hari Patroli Didanai","Hari Patroli Swadaya","Hari Patroli Pembiayaan Awal","Indeks Intensitas Perlindungan","Rasio Realisasi Belanja",
 "Kesempatan Kerja PS","Kesempatan Kerja Setara Penuh","Upah Kegiatan PS","Jumlah KUPS Aktif","Anggota KUPS Aktif","Penjualan KUPS",
 "Manfaat Ekonomi KUPS","Pendapatan KUPS Total","Pendapatan Bersih per RT Bergantung","Pendapatan Program per RT Bergantung",
 "Kehilangan Pendapatan Pembatasan Akses per RT","Kehilangan per RT Terdampak","Rumah Tangga Bergantung Hutan","RT Terdampak Akses",
 "Kehilangan Pendapatan Agregat","Realisasi Belanja Perlindungan","Realisasi Belanja Pengembangan KUPS","Realisasi Belanja Rehabilitasi",
 "Realisasi Belanja Pengendalian Kebakaran","Kebutuhan Dana Rehabilitasi","Kebutuhan Dana Pengendalian Kebakaran","Saldo Dana LPHD",
 "Pemulihan Pendanaan Awal","Pendanaan Awal Belum Terpulihkan","Efek Pengelolaan PS Aktif","Kebutuhan Hari Patroli"]
ALLOC_VARS = ["Pendapatan Bersih per RT Terdampak","Kompensasi per RT Terdampak","Rasio Kompensasi terhadap Kehilangan Akses",
              "Realisasi Kompensasi RT Terdampak","Dana Fleksibel LPHD"]
def disc(df, r=0.10):
    t = df.index.values; m = t < 2087 - 1e-9
    d = (1 + r) ** -(t - 2024)
    return m, d
def npv(df, r=0.10):
    m, d = disc(df, r)
    proj = df["Pendapatan Kotor Penjualan Kredit"] - df["Biaya Transaksi dan MRV"] - df["Realisasi Pembiayaan Awal"] - df["Penggunaan Dana Pengelolaan"]
    mitra = df["Dana Mitra dari Karbon"] - df["Realisasi Pembiayaan Awal"] - df["Kekurangan Biaya Bersama Ditanggung Mitra"] + df["Pemulihan Defisit Biaya Bersama"]
    return float((proj * d)[m].sum() * DT), float((mitra * d)[m].sum() * DT)
def fin_cum(df, v):
    m = df.index.values < 2087 - 1e-9
    return float(df[v][m].sum() * DT)          # 2024-2086
def indicators(df):
    avg, first = yearly(df)
    A = lambda v: float(avg[v].loc[2030:2055].mean())
    C = lambda v: float(avg[v].loc[2025:2086].sum())
    out = {
     "Hutan 2024 (ha)": float(df["Total Hutan"].iloc[0]),
     "Hutan 2030 (ha)": float(first["Total Hutan"].loc[2030]), "Hutan 2050 (ha)": float(first["Total Hutan"].loc[2050]),
     "Hutan 2087 (ha)": float(df["Total Hutan"].iloc[-1]),
     "Deforestasi kumulatif 2025-2086 (ha)": C("Deforestasi Total"),
     "Laju deforestasi rerata 2030-2055 (ha/th)": A("Deforestasi Total"),
     "Emisi bersih kumulatif 2025-2086 (tCO2e)": C("Total Emisi Bersih"),
     "Kredit REDD model diajukan (tCO2e)": C("Kredit REDD Diajukan"),
     "Penerimaan kotor karbon 2024-2086 (Rp)": fin_cum(df, "Pendapatan Kotor Penjualan Kredit"),
     "Biaya MRV, transaksi, pajak 2024-2086 (Rp)": fin_cum(df, "Biaya Transaksi dan MRV"),
     "Dana LPHD diterima 2024-2086 (Rp)": fin_cum(df, "Dana Desa Diterima"),
     "Dana mitra 2024-2086 (Rp)": fin_cum(df, "Dana Mitra dari Karbon"),
     "Pembiayaan awal 2024-2025 (Rp)": fin_cum(df, "Realisasi Pembiayaan Awal"),
     "Belanja dana LPHD 2024-2086 (Rp)": fin_cum(df, "Penggunaan Dana Pengelolaan"),
     "HOK patroli 2024": float(avg["Hari Patroli Didanai"].loc[2024] + avg["Hari Patroli Swadaya"].loc[2024]),
     "HOK patroli 2025": float(avg["Hari Patroli Didanai"].loc[2025] + avg["Hari Patroli Swadaya"].loc[2025]),
     "Hari patroli didanai rerata 2030-2055 (HOK/th)": A("Hari Patroli Didanai"),
     "Hari patroli swadaya rerata 2030-2055 (HOK/th)": A("Hari Patroli Swadaya"),
     "Intensitas perlindungan rerata 2030-2055": A("Indeks Intensitas Perlindungan"),
     "Intensitas perlindungan 2025": float(avg["Indeks Intensitas Perlindungan"].loc[2025]),
     "Rasio realisasi belanja rerata 2030-2055": A("Rasio Realisasi Belanja"),
     "Kebutuhan dana minimum LPHD rerata (Rp/th)": A("Kebutuhan Dana Minimum"),
     "Belanja dana LPHD rerata 2030-2055 (Rp/th)": A("Penggunaan Dana Pengelolaan"),
     "Kesenjangan pembiayaan minimum rerata (Rp/th)": A("Kesenjangan Pembiayaan Minimum"),
     "HOK kegiatan PS rerata (HOK/th)": A("Kesempatan Kerja PS"), "FTE rerata": A("Kesempatan Kerja Setara Penuh"),
     "Upah kegiatan PS rerata (Rp/th)": A("Upah Kegiatan PS"),
     "KUPS aktif rerata": A("Jumlah KUPS Aktif"), "Anggota KUPS rerata": A("Anggota KUPS Aktif"),
     "Omzet KUPS rerata (Rp/th)": A("Penjualan KUPS"), "Surplus KUPS rerata (Rp/th)": A("Manfaat Ekonomi KUPS"),
     "Penerimaan anggota KUPS rerata (Rp/th)": A("Pendapatan KUPS Total"),
     "Pendapatan bersih per RT bergantung (Rp/RT/th)": A("Pendapatan Bersih per RT Bergantung"),
     "Pendapatan program per RT (Rp/RT/th)": A("Pendapatan Program per RT Bergantung"),
     "Kehilangan akses rata-rata per RT (Rp/RT/th)": A("Kehilangan Pendapatan Pembatasan Akses per RT"),
     "Kehilangan akses per RT terdampak (Rp/RT/th)": A("Kehilangan per RT Terdampak"),
     "RT bergantung rerata": A("Rumah Tangga Bergantung Hutan"),
     "Kehilangan pendapatan agregat rerata (Rp/th)": A("Kehilangan Pendapatan Agregat"),
     "Belanja patroli rerata (Rp/th)": A("Realisasi Belanja Perlindungan"), "Belanja KUPS rerata (Rp/th)": A("Realisasi Belanja Pengembangan KUPS"),
     "Belanja rehabilitasi rerata (Rp/th)": A("Realisasi Belanja Rehabilitasi"), "Belanja kebakaran rerata (Rp/th)": A("Realisasi Belanja Pengendalian Kebakaran"),
     "Kebutuhan rehabilitasi rerata (Rp/th)": A("Kebutuhan Dana Rehabilitasi"), "Kebutuhan kebakaran rerata (Rp/th)": A("Kebutuhan Dana Pengendalian Kebakaran"),
    }
    out["Cakupan kebutuhan minimum LPHD (%)"] = 100 * out["Belanja dana LPHD rerata 2030-2055 (Rp/th)"] / out["Kebutuhan dana minimum LPHD rerata (Rp/th)"] if out["Kebutuhan dana minimum LPHD rerata (Rp/th)"] else np.nan
    p, mi = npv(df); out["NPV proyek 10% (Rp)"] = p; out["NPV mitra 10% (Rp)"] = mi
    for v in ALLOC_VARS:
        if v in df.columns: out[v + " rerata"] = A(v)
    return out
def run_ind(model, params, extra=()):
    cols = VARS + [v for v in extra]
    return indicators(run(model, params, cols)), None
def root(f, lo, hi, tol=1e-3):
    flo, fhi = f(lo), f(hi)
    if np.sign(flo) == np.sign(fhi): return None
    for _ in range(40):
        mid = (lo + hi) / 2; fm = f(mid)
        if np.sign(fm) == np.sign(flo): lo, flo = mid, fm
        else: hi = mid
        if hi - lo < tol: break
    return (lo + hi) / 2
