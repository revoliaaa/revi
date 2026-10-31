# DELTA KAPUAS 25 HD: Paket GIS Final untuk Integrasi Vensim REV3

**Inti paket:**
- satu database spasial 25 HD: `DKP_25HD_MASTER_SPATIAL` (GPKG sebagai versi utama, SHP untuk kompatibilitas);
- satu tabel parameter numerik: `DKP_VENSIM_SPATIAL_INPUT.csv` / `.xlsx`.

Model `.mdl` **tidak diubah**. Daftar variabel `.mdl` tidak tersedia, sehingga crosswalk hanya memakai nama variabel yang diberikan peneliti.

## Isi paket

| Folder | File | Keterangan |
|---|---|---|
| `01_MASTER_SPATIAL/` | `DKP_25HD_MASTER_SPATIAL.gpkg` | **Versi utama**: 25 poligon Project Area asli, nama atribut lengkap |
| | `DKP_25HD_MASTER_SPATIAL.shp/.shx/.dbf/.prj/.cpg` | Versi Shapefile (nama atribut ≤ 10 karakter) |
| | `DKP_25HD_DATA_DICTIONARY.csv` | Nama SHP ↔ GPKG, unit, definisi, sumber, kelas data |
| `02_THEMATIC_LAYERS/` | `DKP_TREECOVER_STATUS_2024_PA.tif` | 1 = tanpa tutupan pohon 2000; 2 = tutupan pohon persisten 2000–2024 (**proksi, bukan hutan**); 3 = loss 2001–2024 |
| | `DKP_TREECOVER_LOSS_YEAR_2001_2024_PA.tif` | Tahun gross loss (2001–2024) dalam tutupan pohon 2000 > 30 % |
| | `DKP_MANGROVE_GMW2020_PA.tif` + `.gpkg/.shp` | Mangrove GMW 2020 dalam PA (raster asli + poligon piksel-eksak per HD) |
| | `source_AOI/` | Raster Hansen asli (grid 0,00025°) untuk seluruh AOI |
| | *(gambut)* | **Tidak dibuat**: tidak ada geometri gambut yang sah (lihat QA G8) |
| `03_VENSIM_INPUT/` | `DKP_VENSIM_SPATIAL_INPUT.csv` | 121 baris parameter, siap diimpor (UTF-8) |
| | `DKP_VENSIM_SPATIAL_PARAMETERS.xlsx` | Sheet per kategori, CROSSWALK, RINGKASAN_KELAS, PER_HD |
| `04_QA_DOCS/` | `DKP_QA_DAN_KETERBATASAN.md` | QA, definisi, temuan laporan gambut, keterbatasan |
| | dokumen validasi pendukung | audit boundary, investigasi Pulau Maya, ketidakpastian |
| `05_QUICKLOOK/` | `DKP_THEMATIC_QUICKLOOK.png` | Pratinjau peta layer tematik |
| | `MANIFEST.csv` | Daftar file + SHA-256 + referensi raster yang tidak disertakan |

## Ringkasan nilai (Project Area, kanopi > 30 %)

| | Kubu | Padang Tikar | Pulau Maya | Total |
|---|---|---|---|---|
| Luas PA (ha, geodesik) | 29.505,6 | 66.321,1 | 15.308,3 | 111.135,0 |
| Luas SK (ha, tabel) | 32.468 | 76.370 | 16.103 | 124.941 |
| Tutupan pohon 2000 (ha) | 29.465,2 | 66.117,9 | 15.225,5 | 110.808,6 |
| Tutupan pohon persisten 2024 (ha, proksi) | 27.786,0 | 58.331,5 | 12.967,3 | 99.084,9 |
| Gross loss 2001–2014 (ha) | 735,3 | 1.946,6 | 1.170,2 | 3.852,1 |
| Gross loss 2015–2016 (ha) | 397,3 | 4.757,1 | 797,4 | 5.951,8 |
| Gross loss 2017–2024 (ha) | 546,7 | 1.082,6 | 290,5 | 1.919,8 |
| Gross loss 2001–2024 (ha) | 1.679,2 | 7.786,3 | 2.258,1 | 11.723,7 |
| Laju rata-rata (ha/tahun) | 70,0 | 324,4 | 94,1 | 488,5 |
| Mangrove GMW 2020 (ha) | 9.021,5 | 29.707,2 | 6.321,8 | 45.050,5 |

## Klasifikasi penggunaan parameter

| Kelas | Parameter | Dampak pada struktur model |
|---|---|---|
| **Dapat langsung digunakan** | Luas PA (111.123,2 ha UTM / 111.135,0 ha geodesik); luas SK 124.941 ha; nilai dasar `Proporsi Kredit REDD dalam Project Area` = 0,8535 (tetap); epoch HCV yang lolos (Padang Tikar semua; Kubu 2000/2003/2019/2024; Pulau Maya 2000); lantai derau validasi ≈ 4.200 ha | Tidak mengubah struktur |
| **Perlu konversi / kalibrasi** | Tutupan pohon 2000 (definisi pohon → hutan); mangrove GMW (definisi GMW → stratum mangrove model) | Nilai awal stok; perlu faktor konversi definisi yang dikalibrasi terhadap epoch HCV yang lolos |
| **Hanya untuk sensitivitas** | Laju gross loss 0,248 %/th (2001–2014), 0,217 %/th (2017–2024), 0,441 %/th (2001–2024), per lanskap; pulsa 2015–2016 = 5,4 % tutupan pohon; pangsa luas PA/SK 0,8895 (0,909 / 0,868 / 0,950); tutupan persisten 2024; seri harmonisasi satelit; rata-rata kedalaman gambut per desa | Laju aliran deforestasi, nilai awal 2024, skala kredit S4. Pulsa kebakaran memerlukan struktur PULSE yang belum ada di model, jadi hanya diuji jika peneliti menyetujui perubahan struktur. |
| **Tidak dapat digunakan** | FOREST_2024_HA; PEAT_HA per HD; pangsa aktivitas R2 (butuh geometri SK); epoch HCV bermasalah (Kubu 2009; Pulau Maya 2014/2019/2024; ALL_25 2009–2024); angka stok karbon laporan gambut sebagai input kredit/emisi | – |

## Prosedur integrasi REV3 (disarankan)

1. **Jangan ubah `.mdl`.** Simpan salinan model, lalu jalankan semua uji lewat file data atau changes file (`.cin`/`.vdf`/`.xlsx` via `GET XLS DATA`), bukan dengan mengedit persamaan.
2. **Petakan variabel.** Isi kolom `TARGET_VENSIM_VARIABLE` pada sheet `CROSSWALK_GIS_VENSIM` dengan nama variabel REV3 yang sebenarnya (dari *Document* atau *Variable list* di Vensim). Baris yang tidak punya padanan dibiarkan "BELUM DIPETAKAN".
3. **Cek unit.** Laju di tabel memakai `1/tahun` (fraksi). Jika model memakai %/tahun atau ha/tahun, konversikan secara eksplisit, lalu jalankan *Units Check* di Vensim.
4. **Domain.** Model memakai domain 124.941 ha (SK), sedangkan nilai satelit dihitung pada PA (111.135 ha). Jangan menskalakan nilai PA ke SK secara diam-diam. Gunakan seri harmonisasi (yang menyatakan asumsi skalanya) atau jalankan skenario.
5. **Kalibrasi ulang (sensitivitas):**
   - A: data HCV asli (benchmark lama, RMSE SD 5.445 ha vs linear 4.991 ha);
   - B: tanpa epoch berstatus `TIDAK_DAPAT_DIGUNAKAN`, idealnya per lanskap;
   - C: seri harmonisasi satelit.

   Laporkan ketiganya. Selisih galat < ≈ 4.200 ha tidak dapat dibedakan dengan data HCV.
6. **Skenario S1–S4.** Untuk S1 (tanpa intervensi), jangan gunakan laju 2017–2024 sebagai baseline tanpa proyek: periode itu jatuh setelah SK HD dan dapat memuat efek intervensi. Untuk S4, uji `Proporsi Kredit REDD dalam Project Area` = 0,8535 (dasar) dan 0,8895 (pangsa luas).
7. **Karbon tanah.** Jangan menambah struktur karbon tanah gambut/mangrove dari angka laporan. Stok ≠ emisi yang dapat dikreditkan, dan angka laporan tidak konsisten (QA G1).

## Data yang dibutuhkan untuk menaikkan status parameter

| Data | Parameter yang terbuka |
|---|---|
| Poligon SK 25 HD | Pangsa aktivitas R2 → pengganti terukur 0,8535 |
| Raster `PeatDepth_Interpolated_10m` + klarifikasi versi angka laporan | PEAT_HA per HD (dengan catatan validasi G3–G5) |
| ± 300 titik referensi sampel stratifikasi di PA | Akurasi dan luas terkoreksi; laju loss dapat naik ke kelas "perlu kalibrasi" |
| Daftar variabel `.mdl` REV3 | Crosswalk lengkap |
