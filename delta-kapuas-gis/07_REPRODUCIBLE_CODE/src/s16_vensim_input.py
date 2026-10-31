"""Vensim REV3 spatial input database (CSV + XLSX) from the master spatial database.

The Vensim .mdl was NOT available: the only real model variable name used is the one
supplied by the researcher ("Proporsi Kredit REDD dalam Project Area"). Every other row
carries TARGET_VENSIM_VARIABLE = "BELUM DIPETAKAN" and a conceptual target; names are
never invented.

Categories (KATEGORI):
  1_OBSERVASI_EMPIRIS    measured map/table quantities
  2_ESTIMASI_SPASIAL     derived from observations by a stated formula
  3_PARAMETER_KANDIDAT   candidate values for model parameters
  4_ASUMSI_SENSITIVITAS  values that rest on an explicit assumption; sensitivity only
Usage classes (KELAS_PENGGUNAAN):
  LANGSUNG | PERLU_KONVERSI_ATAU_KALIBRASI | SENSITIVITAS_SAJA | TIDAK_DAPAT_DIGUNAKAN

Usage: python s16_vensim_input.py
"""
import geopandas as gpd
import numpy as np
import pandas as pd

from common import HCV_AREA_HA, ROOT, VENSIM_PROP_KREDIT_REDD

OUT = ROOT / "08_FINAL_FOR_VENSIM" / "03_VENSIM_INPUT"
NOVAR = "BELUM DIPETAKAN (daftar variabel .mdl tidak tersedia)"
PROP = "Proporsi Kredit REDD dalam Project Area"
H = "Hansen GFC-2025-v1.13 (UMD); zonal statistik per poligon PA, area geodesik"
GMW = "Global Mangrove Watch v3.0 (doi:10.5281/zenodo.6894273)"
LAP = "Laporan Gambut dan Mangrove Delta Kapuas Project (2025)"
HCV = "Laporan HCV Kubu/Padang Tikar/Pulau Maya (Tabel 1, 14-16)"
LANDS = ["Kubu", "Padang Tikar", "Pulau Maya"]


def row(**k):
    base = dict(VAR_ID="", KATEGORI="", TARGET_VENSIM_VARIABLE=NOVAR, KONSEP_TARGET="", CAKUPAN="ALL_25",
                UNIT="", NILAI=np.nan, TAHUN_PERIODE="", DOMAIN_SPASIAL="PROJECT_AREA (111.134,95 ha geodesik)",
                SUMBER="", METODE="", KETIDAKPASTIAN="", STATUS_DATA="", KELAS_PENGGUNAAN="", REKOMENDASI="",
                DAMPAK_STRUKTUR_MODEL="")
    base.update(k)
    return base


def main():
    m = gpd.read_file(ROOT / "08_FINAL_FOR_VENSIM" / "01_MASTER_SPATIAL" / "DKP_25HD_MASTER_SPATIAL.gpkg", layer="DKP_25HD_MASTER_SPATIAL")
    hs = pd.read_csv(ROOT / "04_VALIDATION" / "SK_HARMONISED_SERIES.csv")
    rm = pd.read_csv(ROOT / "04_VALIDATION" / "SK_HARMONISED_RMSE.csv").set_index("GROUP")
    rel = pd.read_csv(ROOT / "04_VALIDATION" / "SK_EPOCH_RELIABILITY.csv")
    shares = pd.read_csv(ROOT / "04_VALIDATION" / "SK_SHARES_BY_PERIOD.csv")
    conv = pd.read_csv(ROOT / "04_VALIDATION" / "SK_DEFINITION_CONVERSION_2000.csv").set_index("GROUP")
    skz = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "ZONAL_SK_HD.csv")
    SKG = skz.groupby("LANDSCAPE").sum(numeric_only=True); SKG.loc["ALL_25"] = SKG.sum()
    bm = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "TRENDS_PROJECT_AREA_BENCHMARKS.csv")
    g = m.drop(columns="geometry").groupby("LANDSCAPE").sum(numeric_only=True)
    g.loc["ALL_25"] = g.sum()
    R = []
    n = [0]

    def add(**k):
        n[0] += 1
        R.append(row(VAR_ID=f"DKP{n[0]:03d}", **k))

    for c in ["ALL_25"] + LANDS:
        x = g.loc[c]
        add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Luas domain proyek (Project Area)", CAKUPAN=c, UNIT="ha",
            NILAI=x.AREA_HA, TAHUN_PERIODE="2026 (shp 21-05-2026)", SUMBER="Shapefile Delta_Kapuas_Project_Boundary_(Update)",
            METODE="Luas geodesik elipsoid WGS84; planar UTM49S = %.2f ha (konvensi PDD)" % x.AREA_UTM49S_HA,
            KETIDAKPASTIAN="Geometri: selisih UTM vs PDD -0,04 ha (total)", STATUS_DATA="TERVERIFIKASI (Gate 1 PASS)",
            KELAS_PENGGUNAAN="LANGSUNG", REKOMENDASI="Gunakan sebagai luas Project Area; konsisten dengan PDD 111.123,20 ha (UTM)",
            DAMPAK_STRUKTUR_MODEL="Domain kredit/biaya proyek; tidak mengubah struktur")
        add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Luas SK Hutan Desa (domain sistem lahan model)", CAKUPAN=c, UNIT="ha",
            NILAI=x.SK_AREA_HA, TAHUN_PERIODE="SK 2017-2024", DOMAIN_SPASIAL="HCV/SK (tabel, tanpa geometri)", SUMBER=HCV,
            METODE="Penjumlahan luas SK Tabel 1", KETIDAKPASTIAN="Tabel; geometri SK tidak tersedia", STATUS_DATA="TERTRANSKRIPSI",
            KELAS_PENGGUNAAN="LANGSUNG", REKOMENDASI="Konsisten dengan domain 124.941 ha model", DAMPAK_STRUKTUR_MODEL="Tidak ada (sudah dipakai model)")
        add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Tutupan pohon awal 2000 di PA (BUKAN luas hutan)", CAKUPAN=c, UNIT="ha",
            NILAI=x.TREE_2000_HA, TAHUN_PERIODE="2000", SUMBER=H, METODE="Piksel kanopi >30 % (vegetasi >5 m)",
            KETIDAKPASTIAN="Berbasis peta, tanpa akurasi lokal; sensitivitas ambang kanopi 10/30/50 persen di FOREST_CHANGE_PROJECT_AREA.xlsx (THRESHOLD_SENSITIVITY)",
            STATUS_DATA="OBSERVASI PETA", KELAS_PENGGUNAAN="PERLU_KONVERSI_ATAU_KALIBRASI",
            REKOMENDASI="Bukan stok hutan model; gunakan untuk inisialisasi hanya setelah konversi definisi tutupan pohon -> hutan",
            DAMPAK_STRUKTUR_MODEL="Jika dipakai sebagai stok hutan awal, nilai lebih tinggi dari kelas hutan HCV (tutupan pohon mencakup semak/belukar >5 m)")
        for col, per, note in [("LOSS_2001_2014_HA", "2001-2014", "jendela kalibrasi; 2001-2010 belum diproses ulang UMD"),
                               ("LOSS_2015_2016_HA", "2015-2016", "pulsa kebakaran El Nino"),
                               ("LOSS_2017_2024_HA", "2017-2024", "periode setelah SK HD (mayoritas 2017-2020)"),
                               ("LOSS_2001_2024_HA", "2001-2024", "total")]:
            add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Gross tree-cover loss kumulatif (BUKAN net forest loss / deforestasi)",
                CAKUPAN=c, UNIT="ha", NILAI=x[col], TAHUN_PERIODE=per, SUMBER=H, METODE="Jumlah piksel lossyear dalam tutupan pohon 2000 >30 %",
                KETIDAKPASTIAN="Tanpa sampel akurasi; " + note, STATUS_DATA="OBSERVASI PETA", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
                REKOMENDASI="Benchmark historis untuk aliran deforestasi model; jangan disamakan dengan net loss",
                DAMPAK_STRUKTUR_MODEL="Pembanding laju aliran keluar stok hutan")
        add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Luas mangrove (definisi GMW)", CAKUPAN=c, UNIT="ha", NILAI=x.MANGROVE_HA,
            TAHUN_PERIODE="2020", SUMBER=GMW, METODE="Piksel GMW 2020 dalam PA (grid asli 0,8\")",
            KETIDAKPASTIAN="Global; tepi laut/pasang surut; 1996 = %.0f ha (stabil)" % x.MANGROVE_1996_HA, STATUS_DATA="OBSERVASI PETA",
            KELAS_PENGGUNAAN="PERLU_KONVERSI_ATAU_KALIBRASI",
            REKOMENDASI="Stratum WRC-mangrove/kontrol silang kelas mangrove HCV; bukan akuntansi karbon",
            DAMPAK_STRUKTUR_MODEL="Jika model memisahkan stok mangrove, nilai awal ~0,6 % lebih kecil dari ekstensi 1996")
        add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Tutupan pohon persisten 2000-2024 (proksi tutupan pohon 2024, BUKAN hutan)",
            CAKUPAN=c, UNIT="ha", NILAI=x.TREE_2024_HA, TAHUN_PERIODE="2024", SUMBER=H,
            METODE="TREE_2000 - gross loss 2001-2024 (regrowth tidak dihitung = batas bawah)",
            KETIDAKPASTIAN="Abaikan regrowth & degradasi; selisih vs kelas hutan alam HCV 2024 besar karena beda definisi",
            STATUS_DATA="ESTIMASI", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
            REKOMENDASI="Uji sensitivitas stok awal 2024; jangan isi sebagai FOREST_2024",
            DAMPAK_STRUKTUR_MODEL="Stok awal lebih tinggi dari HCV -> emisi/kredit penghindaran dapat terestimasi lebih besar")
        for per, col, yrs in [("2001-2014", "LOSS_2001_2014_HA", 14), ("2017-2024", "LOSS_2017_2024_HA", 8),
                              ("2001-2024", "LOSS_2001_2024_HA", 24)]:
            add(KATEGORI="3_PARAMETER_KANDIDAT", KONSEP_TARGET="Laju fraksional gross tree-cover loss tahunan",
                CAKUPAN=c, UNIT="1/tahun", NILAI=x[col] / yrs / x.TREE_2000_HA, TAHUN_PERIODE=per, SUMBER=H,
                METODE=f"{col} / {yrs} / TREE_2000_HA",
                KETIDAKPASTIAN="Non-stasioner (pulsa 2015-2016; patahan metode 2011); gross bukan net",
                STATUS_DATA="KANDIDAT", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
                REKOMENDASI={"2001-2014": "Bandingkan dengan laju deforestasi kalibrasi model",
                             "2017-2024": "Pasca-SK: dapat mencerminkan efek intervensi; JANGAN dipakai sebagai baseline tanpa proyek (S1)",
                             "2001-2024": "Rata-rata jangka panjang; uji sensitivitas"}[per],
                DAMPAK_STRUKTUR_MODEL="Mengatur aliran deforestasi; laju konstan menghaluskan pulsa kebakaran")
    A = g.loc["ALL_25"]
    add(KATEGORI="3_PARAMETER_KANDIDAT", KONSEP_TARGET="Fraksi tutupan pohon yang hilang dalam pulsa kebakaran 2015-2016",
        UNIT="fraksi (per kejadian)", NILAI=A.LOSS_2015_2016_HA / A.TREE_2000_HA, TAHUN_PERIODE="2015-2016", SUMBER=H,
        METODE="LOSS_2015_2016 / TREE_2000", KETIDAKPASTIAN="Satu kejadian; frekuensi tidak dapat diestimasi dari 24 tahun",
        STATUS_DATA="KANDIDAT", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
        REKOMENDASI="Jika model diberi pulsa/disturbansi episodik, gunakan sebagai besaran uji", DAMPAK_STRUKTUR_MODEL="Menambah komponen PULSE; tidak ada di model saat ini (struktur berubah - perlu persetujuan peneliti)")
    for c in ["ALL_25"] + LANDS:
        x = g.loc[c]
        add(KATEGORI="3_PARAMETER_KANDIDAT", TARGET_VENSIM_VARIABLE=PROP, KONSEP_TARGET="Pangsa LUAS Project Area terhadap luas SK",
            CAKUPAN=c, UNIT="dimensionless", NILAI=x.AREA_HA / HCV_AREA_HA["TOTAL" if c == "ALL_25" else c],
            TAHUN_PERIODE="statis", DOMAIN_SPASIAL="PA / SK", SUMBER="Shapefile PA + " + HCV, METODE="AREA_HA (geodesik) / luas SK",
            KETIDAKPASTIAN="Pangsa luas != pangsa aktivitas: dengan geometri SK, R2 (aktivitas) = 0,682 dan R1 (tutupan pohon) = 0,903",
            STATUS_DATA="KANDIDAT", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
            REKOMENDASI=f"Pertahankan {VENSIM_PROP_KREDIT_REDD} sebagai nilai dasar; jalankan nilai ini sebagai skenario sensitivitas",
            DAMPAK_STRUKTUR_MODEL="Skala linier kredit REDD (S4) dan sebagian biaya proyek")
    add(KATEGORI="4_ASUMSI_SENSITIVITAS", TARGET_VENSIM_VARIABLE=PROP, KONSEP_TARGET="Nilai saat ini (asumsi pembatas peneliti)",
        UNIT="dimensionless", NILAI=VENSIM_PROP_KREDIT_REDD, TAHUN_PERIODE="statis", DOMAIN_SPASIAL="PA / HCV",
        SUMBER="Model V5.4.2R (brief peneliti)", METODE="Tidak terdokumentasi; tidak direproduksi oleh rasio spasial mana pun",
        KETIDAKPASTIAN="Tidak diketahui", STATUS_DATA="ASUMSI", KELAS_PENGGUNAAN="LANGSUNG",
        REKOMENDASI="Tetap sebagai nilai dasar; 0,8535 berada di antara R2 (0,682) dan R1 (0,903) - pastikan definisinya di persamaan model", DAMPAK_STRUKTUR_MODEL="Tidak ada perubahan")
    for r in shares.itertuples():
        add(KATEGORI="3_PARAMETER_KANDIDAT", TARGET_VENSIM_VARIABLE=PROP,
            KONSEP_TARGET="Pangsa AKTIVITAS gross loss PA terhadap SK (R2)", CAKUPAN=r.GROUP, UNIT="dimensionless",
            NILAI=r.R2_ACTIVITY_SHARE, TAHUN_PERIODE=r.PERIOD, DOMAIN_SPASIAL="PA / SK (geometri)", SUMBER=H + " x SK shp",
            METODE=f"loss PA {r.LOSS_PA_HA:,.0f} ha / loss SK {r.LOSS_SK_HA:,.0f} ha (kanopi >30 %; ambang 10/50 % memberi 0,680-0,686 untuk 2001-2024)",
            KETIDAKPASTIAN="Bergantung periode (0,54 / 0,78 / 0,60); gross loss sebagai proksi deforestasi; tanpa sampel akurasi",
            STATUS_DATA="KANDIDAT TERUKUR", KELAS_PENGGUNAAN="PERLU_KONVERSI_ATAU_KALIBRASI",
            REKOMENDASI=("Kandidat pengganti 0,8535 JIKA persamaan model mendefinisikannya sebagai pangsa aktivitas deforestasi; "
                         "jalankan S4 dengan 0,8535 (dasar), R1 0,903 dan R2 0,682 (rentang 0,54-0,78)") if r.GROUP == "ALL_25" and r.PERIOD == "2001-2024"
                        else "Sensitivitas periode/lanskap",
            DAMPAK_STRUKTUR_MODEL="Skala linier kredit REDD S4; R2 < 0,8535 menurunkan kredit ~20 %")
        if r.PERIOD == "2001-2024":
            add(KATEGORI="3_PARAMETER_KANDIDAT", TARGET_VENSIM_VARIABLE=PROP,
                KONSEP_TARGET="Pangsa TUTUPAN POHON 2000 PA terhadap SK (R1)", CAKUPAN=r.GROUP, UNIT="dimensionless",
                NILAI=r.R1_TREECOVER_SHARE, TAHUN_PERIODE="2000", DOMAIN_SPASIAL="PA / SK (geometri)", SUMBER=H + " x SK shp",
                METODE="TC2000 PA / TC2000 SK (kanopi >30 %; 10/50 %: 0,900-0,906)", KETIDAKPASTIAN="Stok, bukan aktivitas",
                STATUS_DATA="KANDIDAT TERUKUR", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
                REKOMENDASI="Batas atas pangsa kredit bila kredit sebanding stok hutan", DAMPAK_STRUKTUR_MODEL="Skala linier kredit REDD S4")
    for c in ["ALL_25"] + LANDS:
        add(KATEGORI="3_PARAMETER_KANDIDAT", KONSEP_TARGET="Faktor konversi definisi: hutan alam HCV / tutupan pohon Hansen (epoch 2000)",
            CAKUPAN=c, UNIT="dimensionless", NILAI=conv.loc[c, "FOREST_TO_TREECOVER_RATIO_2000_GT30"], TAHUN_PERIODE="2000",
            DOMAIN_SPASIAL="SK HD (geometri)", SUMBER=HCV + " + " + H, METODE="HCV hutan alam 2000 / TC2000 (>30 %) dalam SK",
            KETIDAKPASTIAN="Hanya satu epoch jangkar; kelas HCV lain epoch tidak konsisten", STATUS_DATA="KANDIDAT",
            KELAS_PENGGUNAAN="PERLU_KONVERSI_ATAU_KALIBRASI",
            REKOMENDASI="Gunakan untuk mengonversi stok tutupan pohon -> stok hutan bila model memakai luas hutan HCV",
            DAMPAK_STRUKTUR_MODEL="Nilai awal stok hutan; tidak mengubah struktur")
        add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Gross tree-cover loss 2001-2024 di seluruh SK HD", CAKUPAN=c, UNIT="ha",
            NILAI=sum(SKG.loc[c, f"LOSS_{y}_GT30"] for y in range(2001, 2025)), TAHUN_PERIODE="2001-2024",
            DOMAIN_SPASIAL="SK HD (geometri 125.469,6 ha)", SUMBER=H + " x SK shp", METODE="Piksel lossyear dalam TC2000 >30 %",
            KETIDAKPASTIAN="Berbasis peta", STATUS_DATA="OBSERVASI PETA", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
            REKOMENDASI="Benchmark aliran deforestasi pada domain model (SK)", DAMPAK_STRUKTUR_MODEL="Pembanding laju aliran")
    RANK = {"LANGSUNG": 0, "SENSITIVITAS_SAJA": 1, "TIDAK_DAPAT_DIGUNAKAN": 2}

    def use_class(c, y):
        """Usage class of an HCV natural-forest epoch (SK-domain reliability, s19)."""
        if y == 2000:
            return "LANGSUNG", "anchor 2000"
        v = rel[(rel.LANDSCAPE == c) & (rel.EPOCH == y)].iloc[0]
        why = f"deviasi {v.ABS_D_PCT:.1f}% dari seri harmonisasi domain SK"
        if c != "ALL_25" and bool(v.MANGROVE_OUTSIDE_15PCT):
            why += f"; mangrove HCV/GMW = {v.HCV_OVER_GMW_MANGROVE:.2f}"
        if c == "ALL_25":
            why += "; kelas = terburuk dari komponen lanskap"
        return v.USE_CLASS, why

    for c in ["ALL_25"] + LANDS:
        d = hs[hs.GROUP == c].set_index("YEAR")
        for y in [2000, 2003, 2009, 2014, 2019, 2024]:
            uc, why = use_class(c, y)
            add(KATEGORI="1_OBSERVASI_EMPIRIS", KONSEP_TARGET="Luas hutan alam HCV (data kalibrasi/validasi model saat ini)", CAKUPAN=c,
                UNIT="ha", NILAI=d.loc[y, "HCV_NATURAL_FOREST_HA"], TAHUN_PERIODE=str(y), DOMAIN_SPASIAL="HCV/SK 124.941 ha", SUMBER=HCV,
                METODE="Jumlah kelas hutan lahan kering + mangrove + rawa (primer & sekunder)",
                KETIDAKPASTIAN="Inkonsistensi klasifikasi antar-epoch; " + why,
                STATUS_DATA="HCV - " + why, KELAS_PENGGUNAAN=uc,
                REKOMENDASI={"LANGSUNG": "Dapat dipakai untuk kalibrasi/validasi dengan ketidakpastian eksplisit",
                             "SENSITIVITAS_SAJA": "Pakai hanya dalam uji sensitivitas kalibrasi",
                             "TIDAK_DAPAT_DIGUNAKAN": "Keluarkan dari kalibrasi/validasi atau ganti dengan seri harmonisasi"}[uc],
                DAMPAK_STRUKTUR_MODEL="Target kalibrasi; tidak mengubah struktur")
            add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Seri hutan alam harmonisasi satelit (monoton)", CAKUPAN=c, UNIT="ha",
                NILAI=d.loc[y, "S_SK_HARMONISED_HA"], TAHUN_PERIODE=str(y), DOMAIN_SPASIAL="SK HD (geometri)",
                SUMBER=HCV + " + " + H, METODE="HCV hutan alam 2000 - loss kumulatif Hansen di dalam geometri SK (tanpa penskalaan)",
                KETIDAKPASTIAN="Asumsi: tanpa regrowth; gross loss tutupan pohon dipakai sebagai proksi hilangnya hutan alam", STATUS_DATA="ESTIMASI",
                KELAS_PENGGUNAAN="SENSITIVITAS_SAJA", REKOMENDASI="Target kalibrasi alternatif (uji sensitivitas)",
                DAMPAK_STRUKTUR_MODEL="Tidak mengubah struktur; mengubah target kalibrasi")
    add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Lantai derau validasi HCV (hold-out 2019, 2024)", UNIT="ha",
        NILAI=rm.loc["ALL_25", "RMSE_HOLDOUT_2019_2024_HA"], TAHUN_PERIODE="2019, 2024", DOMAIN_SPASIAL="SK HD (geometri)",
        SUMBER="s19", METODE="RMSE(HCV - seri harmonisasi domain SK)", KETIDAKPASTIAN="Seri acuan juga model; 2003-2024 = %.0f ha" % rm.loc["ALL_25", "RMSE_2003_2024_HA"], STATUS_DATA="ESTIMASI",
        KELAS_PENGGUNAAN="LANGSUNG", REKOMENDASI="Laporkan: galat hold-out model (SD 5.445; linear 4.991 ha) berada di bawah derau data HCV ~6.300 ha; model tidak dapat dibedakan",
        DAMPAK_STRUKTUR_MODEL="Interpretasi validasi; bukan parameter")
    for b in bm[(bm.GROUP == "ALL_25") & (bm.THRESHOLD_PCT == 30)].itertuples():
        add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET=f"Kinerja benchmark {b.BENCHMARK} pada hold-out 2015-2024 (gross loss PA)",
            UNIT="ha/tahun (RMSE)", NILAI=b.RMSE_annual_ha, TAHUN_PERIODE="fit 2001-2014; uji 2015-2024", SUMBER="s05",
            METODE="RMSE tahunan; galat kumulatif %.0f %%" % b.REL_DIFF_CUM_pct, KETIDAKPASTIAN="Satu wilayah, 10 tahun",
            STATUS_DATA="ESTIMASI", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA", REKOMENDASI="Pembanding struktur laju konstan vs tren",
            DAMPAK_STRUKTUR_MODEL="Menunjukkan laju konstan under-predict pada PA karena pulsa 2015")
    # --- Peat & mangrove soil report (third-party; domain = SK ~125k ha) ---
    pr = [("Luas tanah gambut >=50 cm (kriging)", "ha", 47180.78, "Tabel 14"),
          ("Luas sedimen mangrove semua kelas (termasuk <50 cm = 41.696,7 ha)", "ha", 52703.14, "Tabel 14; teks menyebut '>=50 cm' - keliru"),
          ("Stok karbon tanah gambut (versi Bab III)", "tC", 144114915.20, "Tabel 15"),
          ("Stok karbon sedimen mangrove (versi Bab III)", "tC", 10561043.94, "Tabel 15"),
          ("Stok karbon tanah gambut (versi Simpulan)", "tC", 133521424.08, "Bab IV - TIDAK KONSISTEN dengan Tabel 15 dan dengan data spasial (Bab III terkonfirmasi)"),
          ("Stok karbon sedimen mangrove (versi Simpulan)", "tC", 12303629.97, "Bab IV - TIDAK KONSISTEN dengan Tabel 15"),
          ("Rata-rata stok karbon gambut (Bab III)", "tC/ha", 3054.53, "Tabel 15; U = 1,1 % (Tabel 16)"),
          ("Rata-rata stok karbon sedimen mangrove (Bab III)", "tC/ha", 200.39, "Tabel 15; U = 5,9 %"),
          ("Rata-rata BD gambut (lab, n=64)", "g/cm3", 0.1129, "Bab III; U 2,27 %"),
          ("Rata-rata C-organik gambut (lab, n=64)", "%", 49.8, "Bab III"),
          ("Rata-rata kedalaman gambut kelas sangat dalam (plot)", "m", 7.3, "Bab III, 186 plot di 17 desa")]
    for k, u, v, src in pr:
        add(KATEGORI="1_OBSERVASI_EMPIRIS" if ("lab" in k or "plot" in k) else "4_ASUMSI_SENSITIVITAS",
            KONSEP_TARGET=k + " - STOK, BUKAN EMISI YANG DAPAT DIKREDITKAN", UNIT=u, NILAI=v, TAHUN_PERIODE="survei 31-10 s.d. 18-12-2024",
            DOMAIN_SPASIAL="Areal laporan ~125.461 ha (jumlah kelas Tabel 14; ~luas SK, BUKAN PA)", SUMBER=LAP + " " + src,
            METODE="Ordinary kriging 10 m dari 5.778 titik (mayoritas titik bangkitan rnorm dari kelas BBSDLP) x BD x C-org",
            KETIDAKPASTIAN="U% laporan hanya Monte Carlo atas rata-rata input; tidak memasukkan galat interpolasi; evaluasi R2=0,99 tidak independen (titik evaluasi juga input kriging)",
            STATUS_DATA="LAPORAN PIHAK KETIGA - INKONSISTENSI INTERNAL", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA" if u != "tC" else "TIDAK_DAPAT_DIGUNAKAN",
            REKOMENDASI=("Jangan dipakai sebagai input kredit/emisi; minta raster & klarifikasi versi angka sebelum dipakai"
                         if u == "tC" else "Hanya untuk konteks/sensitivitas; tidak per HD; domain bukan PA"),
            DAMPAK_STRUKTUR_MODEL="Stok karbon tanah tidak mengubah aliran emisi tanpa model emisi drainase/oksidasi (di luar cakupan)")
    sd = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "SOIL_DEPTH_BY_HD_WIDE.csv")
    SD = sd.groupby(["DOMAIN", "LANDSCAPE"]).sum(numeric_only=True)
    for dom in ["PROJECT_AREA", "SK_HD"]:
        X = SD.loc[dom].copy(); X.loc["ALL_25"] = X.sum()
        for c in ["ALL_25"] + LANDS:
            x = X.loc[c]
            common = dict(CAKUPAN=c, TAHUN_PERIODE="survei 2024 / peta 2025",
                          DOMAIN_SPASIAL="PROJECT_AREA" if dom == "PROJECT_AREA" else "SK HD (geometri)",
                          SUMBER=LAP + " - data spasial Soil_Depth_rev120425 (kelas = Tabel 14 +/-0,01 ha)",
                          METODE="Overlay poligon kelas kedalaman (ordinary kriging 10 m, divektorkan oleh penyusun) dengan poligon " + ("PA" if dom == "PROJECT_AREA" else "SK"),
                          KETIDAKPASTIAN="Akurasi interpolasi belum divalidasi independen (QA G3-G5)" + ("; Pulau Maya: pemisahan gambut/mangrove mengikuti masker mangrove ~HCV 2024 (QA G9)" if c in ("ALL_25", "Pulau Maya") else ""))
            add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Luas tanah gambut >=50 cm (stratum WRC-gambut)", UNIT="ha", NILAI=x.PEAT_GE50_HA,
                STATUS_DATA="ESTIMASI PIHAK KETIGA", KELAS_PENGGUNAAN="PERLU_KONVERSI_ATAU_KALIBRASI",
                REKOMENDASI="Dapat dipakai sebagai luas stratum gambut setelah validasi; untuk Pulau Maya uji sensitivitas G9",
                DAMPAK_STRUKTUR_MODEL="Nilai awal stratum gambut; tidak menambah struktur emisi", **common)
            add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Luas gambut >=3 m (fungsi lindung gambut)", UNIT="ha", NILAI=x.PEAT_GE300_HA,
                STATUS_DATA="ESTIMASI PIHAK KETIGA", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
                REKOMENDASI="Konteks kebijakan (gambut >=3 m); bukan parameter aliran", DAMPAK_STRUKTUR_MODEL="-", **common)
            add(KATEGORI="2_ESTIMASI_SPASIAL", KONSEP_TARGET="Luas sedimen mangrove (semua kelas)", UNIT="ha", NILAI=x.MANGROVE_SED_HA,
                STATUS_DATA="ESTIMASI PIHAK KETIGA", KELAS_PENGGUNAAN="SENSITIVITAS_SAJA",
                REKOMENDASI="Bandingkan dengan mangrove GMW; selisih menandakan definisi masker berbeda (G9)", DAMPAK_STRUKTUR_MODEL="-", **common)
            add(KATEGORI="4_ASUMSI_SENSITIVITAS", KONSEP_TARGET="STOK karbon tanah gambut (luas kelas x Tabel 15) - BUKAN EMISI, BUKAN KREDIT",
                UNIT="tC", NILAI=x.PEAT_C_TC_CONTEXT, STATUS_DATA="KONTEKS", KELAS_PENGGUNAAN="TIDAK_DAPAT_DIGUNAKAN",
                REKOMENDASI="Jangan dipakai sebagai input kredit/emisi; emisi WRC bergantung drainase/subsidensi",
                DAMPAK_STRUKTUR_MODEL="Tidak ada (tidak menambah struktur karbon tanah)", **common)
    add(KATEGORI="4_ASUMSI_SENSITIVITAS", KONSEP_TARGET="Luas HUTAN 2024 per HD (kelas hutan tervalidasi)", UNIT="ha", NILAI=np.nan,
        TAHUN_PERIODE="2024", SUMBER="-", METODE="Butuh klasifikasi hutan 2024 tervalidasi (sampel referensi)",
        KETIDAKPASTIAN="-", STATUS_DATA="TIDAK TERSEDIA", KELAS_PENGGUNAAN="TIDAK_DAPAT_DIGUNAKAN",
        REKOMENDASI="Gunakan TREE_2024_HA hanya sebagai proksi sensitivitas", DAMPAK_STRUKTUR_MODEL="-")

    df = pd.DataFrame(R)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "DKP_VENSIM_SPATIAL_INPUT.csv", index=False, encoding="utf-8-sig")
    per_hd = m.drop(columns="geometry")
    cw = pd.DataFrame([
        ("AREA_HA / AREA_UTM49S_HA", "Luas Project Area", "Pangsa kredit/biaya proyek", "LANGSUNG", "Tidak ada"),
        ("PA_TO_SK_RATIO (agregat 0,8895)", PROP, "Proporsi kredit REDD (pangsa luas)", "SENSITIVITAS_SAJA", "Skala linier kredit S4"),
        ("R2_ACTIVITY_SHARE (agregat 0,682)", PROP, "Proporsi kredit REDD (pangsa aktivitas)", "PERLU_KONVERSI_ATAU_KALIBRASI", "Skala linier kredit S4"),
        ("R1_TREECOVER_SHARE (agregat 0,903)", PROP, "Proporsi kredit REDD (pangsa stok)", "SENSITIVITAS_SAJA", "Skala linier kredit S4"),
        ("TREE_2000_HA", NOVAR, "Stok hutan awal (setelah konversi definisi)", "PERLU_KONVERSI_ATAU_KALIBRASI", "Nilai awal stok"),
        ("TREE_2024_HA", NOVAR, "Stok hutan awal 2024 (proksi)", "SENSITIVITAS_SAJA", "Nilai awal stok 2024"),
        ("LOSS_* / LOSS_RATE_*", NOVAR, "Laju aliran deforestasi historis", "SENSITIVITAS_SAJA", "Laju aliran keluar"),
        ("LOSS_2015_2016_HA", NOVAR, "Disturbansi episodik (belum ada di model)", "SENSITIVITAS_SAJA", "Perlu struktur PULSE baru"),
        ("MANGROVE_HA", NOVAR, "Stratum mangrove / WRC-mangrove", "PERLU_KONVERSI_ATAU_KALIBRASI", "Nilai awal stratum"),
        ("FOREST_2024_HA", NOVAR, "Stok hutan 2024", "TIDAK_DAPAT_DIGUNAKAN", "-"),
        ("PEAT_HA", NOVAR, "Stratum gambut / WRC-gambut", "TIDAK_DAPAT_DIGUNAKAN", "-"),
        ("PEAT_DEPTH_SURVEY_M", NOVAR, "Kedalaman gambut (konteks)", "SENSITIVITAS_SAJA", "Tidak per HD spasial"),
        ("Seri harmonisasi S2", NOVAR, "Data kalibrasi alternatif", "SENSITIVITAS_SAJA", "Target kalibrasi"),
    ], columns=["FIELD_GIS", "TARGET_VENSIM_VARIABLE", "KONSEP_TARGET", "KELAS_PENGGUNAAN", "DAMPAK_STRUKTUR"])
    readme = pd.DataFrame({"README": [
        "Database input spasial untuk integrasi Vensim REV3 (25 HD, 2024-2087, S1-S4). Model .mdl TIDAK diubah dan TIDAK tersedia di sesi ini.",
        "TARGET_VENSIM_VARIABLE hanya berisi nama yang diberikan peneliti ('Proporsi Kredit REDD dalam Project Area'); lainnya 'BELUM DIPETAKAN' - jangan mengarang nama.",
        "Gross tree-cover loss (Hansen) != net forest loss != deforestasi regulasi. Stok karbon tanah != emisi yang dapat dikreditkan.",
        "Kategori: 1 observasi empiris; 2 estimasi spasial; 3 parameter kandidat; 4 asumsi/sensitivitas. Kelas penggunaan: LANGSUNG / PERLU_KONVERSI_ATAU_KALIBRASI / SENSITIVITAS_SAJA / TIDAK_DAPAT_DIGUNAKAN.",
        "Nilai per HD: sheet PER_HD (= atribut DKP_25HD_MASTER_SPATIAL.gpkg).",
    ]})
    with pd.ExcelWriter(OUT / "DKP_VENSIM_SPATIAL_PARAMETERS.xlsx") as xw:
        readme.to_excel(xw, sheet_name="README", index=False)
        df.to_excel(xw, sheet_name="SEMUA_PARAMETER", index=False)
        for k in ["1_OBSERVASI_EMPIRIS", "2_ESTIMASI_SPASIAL", "3_PARAMETER_KANDIDAT", "4_ASUMSI_SENSITIVITAS"]:
            df[df.KATEGORI == k].to_excel(xw, sheet_name=k[:31], index=False)
        cw.to_excel(xw, sheet_name="CROSSWALK_GIS_VENSIM", index=False)
        df.groupby(["KELAS_PENGGUNAAN", "KATEGORI"]).size().unstack(fill_value=0).to_excel(xw, sheet_name="RINGKASAN_KELAS")
        per_hd.to_excel(xw, sheet_name="PER_HD", index=False)
    print(df.groupby(["KATEGORI", "KELAS_PENGGUNAAN"]).size())
    print(len(df), "rows")


if __name__ == "__main__":
    main()
