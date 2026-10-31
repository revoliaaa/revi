# DELTA KAPUAS 25 HD: Paket GIS Final untuk Integrasi Vensim REV3

**Inti paket:**
- satu database spasial 25 HD: `DKP_25HD_MASTER_SPATIAL` (GPKG versi utama, SHP untuk kompatibilitas), berisi 25 poligon Project Area asli ditambah atribut domain SK;
- lapisan batas SK 25 HD terverifikasi;
- satu tabel parameter numerik: `DKP_VENSIM_SPATIAL_INPUT.csv` / `.xlsx`, 148 baris.

Model `.mdl` **tidak diubah**. Daftar variabel `.mdl` tidak tersedia, sehingga crosswalk hanya memakai nama variabel yang diberikan peneliti (`Proporsi Kredit REDD dalam Project Area`).

## Isi paket

| Folder | File | Keterangan |
|---|---|---|
| `01_MASTER_SPATIAL/` | `DKP_25HD_MASTER_SPATIAL.gpkg` | **Versi utama.** Layer `DKP_25HD_MASTER_SPATIAL` = 25 poligon PA + 40 atribut. Layer `SK_25HD_BOUNDARY` = batas SK per HD. |
| | `DKP_25HD_MASTER_SPATIAL.shp/.shx/.dbf/.prj/.cpg` | Master versi Shapefile (nama atribut ≤ 10 karakter) |
| | `DKP_25HD_SK_BOUNDARY.shp/...` | Batas SK 25 HD (dari *SHP Gabungan Hutan Desa Delta Kapuas*; 38 bagian → 25 HD; penugasan HD terverifikasi 37/37 lewat nomor SK) |
| | `DKP_25HD_DATA_DICTIONARY.csv` | Nama SHP ↔ GPKG, unit, definisi, sumber, kelas data |
| `02_THEMATIC_LAYERS/` | `DKP_TREECOVER_STATUS_2024_PA.tif` | 1 = tanpa tutupan pohon 2000; 2 = tutupan pohon persisten 2000–2024 (**proksi, bukan hutan**); 3 = loss 2001–2024 |
| | `DKP_TREECOVER_LOSS_YEAR_2001_2024_PA.tif` | Tahun gross loss dalam tutupan pohon 2000 > 30 % |
| | `DKP_MANGROVE_GMW2020_PA.tif` + `.gpkg/.shp` | Mangrove GMW 2020 dalam PA (raster asli + poligon piksel-eksak per HD) |
| | `source_AOI/` | Raster Hansen asli (grid 0,00025°) seluruh AOI |
| | *(gambut)* | **Tidak dibuat**: tidak ada geometri gambut yang sah (QA G8) |
| `03_VENSIM_INPUT/` | `DKP_VENSIM_SPATIAL_INPUT.csv` | 148 baris parameter (UTF-8) |
| | `DKP_VENSIM_SPATIAL_PARAMETERS.xlsx` | Sheet per kategori, CROSSWALK, RINGKASAN_KELAS, PER_HD |
| `04_QA_DOCS/` | `DKP_QA_DAN_KETERBATASAN.md` + audit PA & SK + dokumen validasi | QA, definisi, temuan, keterbatasan |
| `05_QUICKLOOK/` | `DKP_THEMATIC_QUICKLOOK.png`, `MANIFEST.csv` | Pratinjau peta; daftar file + SHA-256 |

## Ringkasan nilai (kanopi > 30 %)

| | Kubu | Padang Tikar | Pulau Maya | Total |
|---|---|---|---|---|
| Luas SK, tabel (ha) | 32.468 | 76.370 | 16.103 | 124.941 |
| Luas SK, geometri (ha, geodesik) | 33.066 | 76.375 | 16.028 | 125.470 |
| Luas PA (ha, geodesik) | 29.505,6 | 66.321,1 | 15.308,3 | 111.135,0 |
| Tutupan pohon 2000, PA (ha) | 29.465 | 66.118 | 15.225 | 110.809 |
| Tutupan pohon persisten 2024, PA (ha, proksi) | 27.786 | 58.332 | 12.967 | 99.085 |
| Gross loss 2001–2024, PA (ha) | 1.679 | 7.786 | 2.258 | 11.724 |
| Gross loss 2001–2024, SK (ha) | 3.092 | 11.563 | 2.528 | 17.183 |
| – di PA 2001–2014 / 2015–2016 / 2017–2024 (ha) | 735 / 397 / 547 | 1.947 / 4.757 / 1.083 | 1.170 / 797 / 291 | 3.852 / 5.952 / 1.920 |
| R1 pangsa tutupan pohon PA/SK | 0,906 | 0,890 | 0,958 | **0,903** |
| R2 pangsa aktivitas loss PA/SK (2001–2024) | 0,543 | 0,673 | 0,893 | **0,682** |
| Faktor konversi hutan HCV / tutupan pohon (2000) | 0,810 | 0,869 | 0,727 | 0,835 |
| Mangrove GMW 2020, PA (ha) | 9.021 | 29.707 | 6.322 | 45.050 |

## Klasifikasi penggunaan parameter

| Kelas | Parameter | Dampak pada struktur model |
|---|---|---|
| **Dapat langsung digunakan** | Luas PA (111.123,2 ha UTM / 111.135,0 ha geodesik); luas SK 124.941 ha (tabel); nilai dasar `Proporsi Kredit REDD dalam Project Area` = 0,8535; epoch HCV yang lolos (**Padang Tikar 2000–2019; Kubu 2000/2003; Pulau Maya 2000**); lantai derau validasi HCV ≈ 6.300 ha | Tidak mengubah struktur |
| **Perlu konversi / kalibrasi** | **R2 = 0,682** (rentang per periode 0,54–0,78) sebagai kandidat pengganti 0,8535, *jika* persamaan model mendefinisikannya sebagai pangsa aktivitas deforestasi; faktor konversi tutupan pohon → hutan 0,835; tutupan pohon 2000; mangrove GMW | Skala kredit S4 (R2 < 0,8535 → kredit turun ±20 %); nilai awal stok |
| **Hanya untuk sensitivitas** | Laju gross loss 0,248 %/th (2001–2014), 0,217 %/th (2017–2024), 0,441 %/th (2001–2024), per lanskap; pulsa 2015–2016 = 5,4 % tutupan pohon; R1 0,903; pangsa luas 0,8895; tutupan persisten 2024; seri harmonisasi satelit domain SK; epoch HCV berstatus sensitivitas; kedalaman gambut per desa | Laju aliran deforestasi, nilai awal 2024. Pulsa kebakaran memerlukan struktur PULSE yang belum ada di model. |
| **Tidak dapat digunakan** | FOREST_2024_HA; PEAT_HA per HD; epoch HCV bermasalah (**Kubu 2009; Pulau Maya 2014/2019/2024; agregat ALL_25 2009–2024**); angka stok karbon laporan gambut sebagai input kredit/emisi | – |

## Prosedur integrasi REV3 (disarankan)

1. **Jangan ubah `.mdl`.** Jalankan uji lewat file data/changes (`.cin`, `.vdf`, atau `GET XLS DATA`), bukan dengan mengedit persamaan.
2. **Petakan variabel.** Isi `TARGET_VENSIM_VARIABLE` di sheet `CROSSWALK_GIS_VENSIM` dengan nama variabel REV3 yang sebenarnya.
3. **Cek unit.** Laju di tabel memakai `1/tahun` (fraksi). Konversi eksplisit bila model memakai %/tahun atau ha/tahun, lalu jalankan *Units Check*.
4. **Domain.** Model memakai domain SK (124.941 ha tabel; 125.470 ha geometri). Nilai SK sekarang **terukur langsung** (kolom `*_SK_*` dan baris "di seluruh SK HD"), sehingga tidak perlu menskalakan dari PA.
5. **Kalibrasi ulang (sensitivitas):**
   - A: data HCV asli (benchmark lama, RMSE SD 5.445 ha vs linear 4.991 ha);
   - B: tanpa epoch `TIDAK_DAPAT_DIGUNAKAN`, idealnya per lanskap;
   - C: seri harmonisasi satelit domain SK.

   Galat hold-out lama (≈ 5.000–5.400 ha) berada di bawah derau HCV (≈ 6.300 ha), sehingga model tidak dapat dibedakan dengan data HCV.
6. **Skenario.** Untuk S1, jangan gunakan laju 2017–2024 sebagai baseline tanpa proyek (pasca-SK; efek intervensi mungkin ada). Untuk S4, jalankan `Proporsi Kredit REDD dalam Project Area` = 0,8535 (dasar), 0,682 (R2), dan 0,903 (R1).
7. **Karbon tanah.** Jangan menambah struktur karbon tanah dari laporan gambut: stok ≠ emisi yang dapat dikreditkan, dan angka laporan tidak konsisten (QA G1).

## Data yang masih dibutuhkan

| Data | Parameter yang terbuka |
|---|---|
| Raster `PeatDepth_Interpolated_10m` + klarifikasi versi angka laporan | PEAT_HA per HD (dengan catatan validasi G3–G5) |
| ± 300 titik referensi sampel stratifikasi di SK/PA | Akurasi dan luas terkoreksi; laju loss dapat naik ke kelas "perlu kalibrasi" |
| Daftar variabel `.mdl` REV3 dan definisi persamaan `Proporsi Kredit REDD dalam Project Area` | Crosswalk lengkap; keputusan R2 vs 0,8535 |
