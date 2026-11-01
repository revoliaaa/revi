# FINAL GIS HANDOFF: Delta Kapuas 25 HD → Vensim REV3

**Versi beku:** `DKP-GIS-MASTER v1.0 (2026-11-01)`. Checksum setiap file master dan parameter ada di `VERSION_FREEZE.json`.
**Status:** QA final selesai, dan **analisis GIS dihentikan pada versi ini**. Perubahan berikutnya hanya lewat versi baru (v1.1+) dengan changelog.
Model `.mdl` tidak diubah, dan tidak ada kredit karbon yang dihitung dari stok tanah.

## Ringkasan keputusan untuk REV3

| Keputusan | Jumlah baris | Isi utama |
|---|---|---|
| **SIAP_DIGUNAKAN** | 19 | Luas Project Area (111.123,16 ha UTM / 111.134,95 ha geodesik; per lanskap); luas SK 124.941 ha (tabel; per lanskap); `Proporsi Kredit REDD dalam Project Area` = 0,8535 sebagai nilai dasar; epoch HCV hutan alam yang lolos uji (Padang Tikar 2000–2019; Kubu 2000, 2003; Pulau Maya 2000; agregat 2000); lantai derau validasi HCV ≈ 6.310 ha |
| **HANYA_SENSITIVITAS** | 139 | Laju gross tree-cover loss (0,248 / 0,217 / 0,441 %/th; per lanskap); pulsa 2015–2016 (5,4 %); R2 = 0,682 (0,54–0,78 per periode) dan R1 = 0,903 sebagai alternatif 0,8535; faktor konversi tutupan pohon → hutan 0,835; tutupan pohon 2000/2024; mangrove GMW; **luas gambut ≥ 50 cm** (PA 41.436 ha; SK 47.185 ha); sedimen mangrove; seri harmonisasi satelit; epoch HCV berstatus peringatan |
| **BELUM_LAYAK** | 21 | Epoch HCV bermasalah (Kubu 2009; Pulau Maya 2014/2019/2024; agregat 2009–2024); semua **stok karbon tanah** (laporan maupun per HD) sebagai input emisi/kredit; luas hutan 2024 (tidak ada klasifikasi tervalidasi) |

Rinciannya ada di `03_VENSIM_INPUT/DKP_VENSIM_SPATIAL_PARAMETERS.xlsx` (sheet `A_SIAP_REV3`, `B_SENSITIVITAS`, `C_BELUM_LAYAK`). Setiap baris memuat UNIT, DOMAIN_SPASIAL, TAHUN_PERIODE, SUMBER, STATUS_VALIDASI, KEPUTUSAN_REV3 dan SYARAT_NAIK_STATUS; kelengkapannya diuji otomatis (`s22_finalize_freeze.py`). Sebanyak 36 baris berkelas "perlu konversi/kalibrasi" dimasukkan ke HANYA_SENSITIVITAS sampai syarat di kolom SYARAT_NAIK_STATUS terpenuhi.

---

## QA 1: Rekonsiliasi kelas tanah vs Project Area

Angka 111.061 ha adalah jumlah luas **geodesik**, sedangkan 111.123 ha adalah luas PA **planar UTM 49S**. Selisih 61,95 ha mencampur dua basis luas. Dengan basis yang sama (`FINAL_QA/Q1_SOIL_VS_PA_RECONCILIATION.csv`):

| Komponen (UTM 49S) | ha |
|---|---|
| Luas PA | 111.123,16 |
| Jumlah kelas tanah di PA (gambut + sedimen mangrove + mineral) | 111.049,44 |
| **Selisih** | **73,73** |
| – PA di luar geometri SK (serpihan tepi; layer tanah hanya mencakup SK) | 65,31 |
| – PA di dalam SK yang tidak tercakup poligon kelas tanah (celah layer tanah, seluruhnya di Kemboja) | 8,41 |
| – residu overlay | 0,002 |
| Komponen beda satuan (geodesik − UTM) pada jumlah kelas tanah | 11,78 |

Serpihan di luar SK per HD: Kemboja 22,51 ha, Dusun Kecil 12,58 ha, Batu Ampar 10,81 ha, Dusun Besar 9,97 ha, Kubu 9,32 ha, dan < 0,1 ha untuk HD lain. **Kesimpulan:** selisih sepenuhnya terjelaskan, yaitu 99,99 % oleh ketidaksesuaian tepi PA–SK dan celah layer tanah. Penyebabnya bukan kehilangan data.

## QA 2: Sumber dan legalitas geometri SK

| | SK 25 HD | Project Area |
|---|---|---|
| Dasar | 25 SK HPHD (MENLHK 2017–2020; Kemboja KEPMENLHK 8492/2024) | Batas proyek karbon (PDD) |
| Luas resmi | **124.941 ha** (jumlah Tabel 1 laporan HCV) | **111.123,20 ha** (PDD) |
| Geometri yang dipakai | *SHP Gabungan Hutan Desa Delta Kapuas* (kompilasi SAMPAN Kalimantan, ArcGIS, 2025); 125.456,31 ha UTM | `Delta_Kapuas_Project_Boundary_(Update).shp`; 111.123,16 ha UTM |
| Peran di model | domain sistem lahan (124.941 ha) | domain kredit/biaya proyek |

**Status legal geometri SK: kompilasi operasional, bukan salinan peta lampiran SK yang tersertifikasi.** Buktinya dari metadata dan atribut:
- **Kemboja** (9 bagian) berasal dari layer *"pengajuan_Baru_Setelah_Vertek"* (pengajuan setelah verifikasi teknis) yang dipotong dengan PL 2023. Atribut tidak memuat nomor SK. SK 8492/2024 terbit kemudian (10-06-2024), sehingga geometri ini belum tentu sama dengan peta lampiran SK.
- **Bagian-bagian Pulau Maya** membawa atribut "Hasil Delineasi Batas Desa 2018" (Perbup). `NAMA_LPHD` tertimpa nama desa administratif, sehingga nomor SK dipakai sebagai kunci.
- **Kualitas atribut:** tanggal `TGL_HPHD` Teluk Bakung (2017-02-14) tidak sesuai SK (26-12-2019); `TGL_SK_PAK` 2016-07-20 tersalin ke hampir semua HD tanpa nomor PAK; nomor SK Teluk Bakung dan Ambawang mengandung karakter baris baru; tanggal Pulau Maya kosong (1899-12-30).
- **Kesesuaian luas geometri vs tabel SK:** 18 HD dalam ±0,3 %. Selisih 0,3–1 %: Tanjung Beringin +100,4 ha (+0,96 %), Kemboja −34,1 ha (−0,68 %). Selisih > 1 %: **Ambawang +347,6 ha (+10,6 %)**, Kubu +140,8 ha (+3,0 %), Satai Lestari +23,5 ha (+2,4 %), Dusun Kecil −59,8 ha (−1,3 %), Padang Tikar 1 +2,0 ha (+1,1 %).
- **Konsistensi spasial:** penugasan HD menurut nomor SK cocok dengan overlay PA (37/37 bagian); 99,94 % PA berada di dalam SK; tidak ada tumpang tindih antar-SK.

**Keputusan:** geometri SK **SIAP** dipakai untuk analisis spasial (rasio PA/SK, statistik domain SK). Untuk keperluan legal atau verifikasi kredit, geometri ini perlu dicocokkan dengan peta lampiran SK resmi (Go-KUPS/PIAPS). Luas resmi untuk model tetap **124.941 ha (tabel SK)**.

## QA 3: Sedimen mangrove (laporan) vs mangrove GMW 2020

Pemeriksaan ini tidak melakukan koreksi otomatis dengan GMW. Hasilnya (`FINAL_QA/Q3_*.csv`, grid asli GMW):

| Domain SK | ha |
|---|---|
| Sedimen mangrove (laporan) | 52.710 |
| Mangrove GMW 2020 | 46.128 |
| Irisan keduanya | 43.808 (kesesuaian 0,80) |
| Hanya sedimen | **8.901** |
| – ≤ 30 m dari GMW (registrasi/resolusi piksel) | 1.906 (21 %) |
| – 30–1.000 m dari GMW (tepi/peralihan) | 3.089 (35 %) |
| – > 1 km dari GMW (patch terpisah) | **3.906 (44 %)** |
| – di antaranya bertutupan pohon > 30 % (Hansen 2000) | 8.836 (99 %) |
| Hanya GMW | 2.319, dan 95 % di antaranya ≤ 250 m dari sedimen. Dalam layer laporan dipetakan sebagai mineral (1.954) atau gambut (356). |
| Kelas mangrove HCV 2024 (tabel) | 52.398 |

**Kesimpulan atribusi penyebab:**
1. **Kesalahan spasial (registrasi/resolusi): ±21 %.** Pita ≤ 30 m di sepanjang tepi; dominan di Batu Ampar, Kubu dan Dusun Kecil.
2. **Perbedaan definisi ekosistem: ±35 %.** Pita 30–1.000 m di sisi darat, yaitu mangrove belakang, nipah atau peralihan rawa yang vegetatif (99 % bertutupan pohon) tetapi tidak masuk definisi GMW. Dominan di Tanjung Harapan, Dabong, Mengkalang, Seruat Dua dan Kemboja.
3. **Masker/klasifikasi: ±44 %.** Patch > 1 km dari mangrove GMW mana pun, terkonsentrasi di **Dusun Besar (1.782 ha), Tanjung Satai (1.166 ha) dan Tanjung Beringin (793 ha)**. Total sedimen (52.710 ha) hampir sama dengan kelas mangrove HCV 2024 (52.398 ha), sehingga masker laporan kemungkinan mengikuti peta tutupan lahan HCV 2024 yang sudah terbukti inkonsisten di Pulau Maya.

**Keputusan:** luas sedimen mangrove dan pemisahan gambut/mangrove **HANYA_SENSITIVITAS**. Untuk Dusun Besar, Tanjung Satai dan Tanjung Beringin, gambut kemungkinan underestimate. GMW **tidak** dipakai untuk mengoreksi layer laporan; rekonsiliasi masker adalah tanggung jawab penyusun laporan.

## QA 4: Dampak `make_valid`

| Layer | Fitur | Invalid | Δ luas setelah `make_valid` | `make_valid` vs `buffer(0)` | Overlap sebelum / sesudah | Catatan |
|---|---|---|---|---|---|---|
| Project Area | 25 | 0 | 0 | – | 0 / 0 ha | – |
| SK (Gabungan HD) | 38 | 1 (Mengkalang) | 0,000 ha | identik | 0 / 0 ha | 1 bagian degenerasi 1,4 m² (badan air Dusun Kecil) dibuang di s18, bukan karena `make_valid` |
| Soil_Depth_rev120425 | 22 | 7 | 0,000 ha | identik | 0 / 0 ha | celah SK tidak tercakup 14,23 ha; kelas Mangrove 500–600 cm = 0,003 ha (dipertahankan) |
| Gambut_Data_WAS | 14 | 0 | 0 | – | 0 / 0 ha | – |
| Mangrove_Data_WAS | 7 | 6 | 0,000 ha | identik | 0 / 0 ha | – |

Semua 14 geometri invalid berjenis *Ring Self-intersection* pada satu titik sudut. Ini artefak khas vektorisasi raster (piksel bersinggungan di sudut). **`make_valid` tidak mengubah luas, jumlah fitur maupun topologi.** Rincian per fitur ada di `FINAL_QA/Q4_MAKE_VALID_PER_FEATURE.csv`.

## QA 5: Finalisasi master dan parameter

- `DKP_25HD_MASTER_SPATIAL.shp/.shx/.dbf/.prj/.cpg` dan `.gpkg` (layer utama + `SK_25HD_BOUNDARY`): 25 poligon PA asli, 49 atribut termasuk `VERSION`. Uji keras otomatis ada di `s15_master_spatial.py`.
- `DKP_25HD_DATA_DICTIONARY.csv`: setiap atribut punya UNIT, DOMAIN, TAHUN_PERIODE, SOURCE, STATUS_VALIDASI, KEPUTUSAN_REV3 dan SYARAT_NAIK_STATUS. Pembagian keputusan: 18 SIAP (kunci, luas, metadata), 28 SENSITIVITAS, 3 BELUM_LAYAK (FOREST_2024 dan dua stok karbon tanah).
- `DKP_VENSIM_SPATIAL_INPUT.csv/.xlsx`: 179 baris, semua kolom wajib terisi.

## Langkah integrasi REV3 (ringkas)

1. Simpan salinan `.mdl`, lalu jalankan dari file data/changes. Jangan mengedit persamaan.
2. Petakan `TARGET_VENSIM_VARIABLE` di sheet `CROSSWALK_GIS_VENSIM` ke nama variabel REV3 yang sebenarnya.
3. Pakai hanya baris **SIAP_DIGUNAKAN** untuk run dasar. Baris **HANYA_SENSITIVITAS** dipakai untuk run sensitivitas, misalnya S4 dengan 0,8535 / 0,682 / 0,903, laju loss alternatif, dan luas gambut.
4. Untuk kalibrasi, keluarkan epoch berstatus BELUM_LAYAK, atau gunakan seri harmonisasi satelit sebagai run sensitivitas.
5. Jangan menambah struktur karbon tanah, dan jangan menghitung kredit dari stok.

## Hal yang tetap terbuka (di luar versi beku ini)

| Data/aksi | Membuka |
|---|---|
| Definisi persamaan `Proporsi Kredit REDD dalam Project Area` di `.mdl` | Keputusan R2 (0,682) vs 0,8535 |
| Peta lampiran SK resmi (terutama Kemboja, Ambawang, Kubu) | Status legal geometri SK |
| Validasi silang kedalaman gambut dan rekonsiliasi masker mangrove oleh penyusun laporan | Luas gambut/sedimen naik ke SIAP |
| Sampel akurasi stratifikasi di PA/SK | Laju gross loss naik ke status kalibrasi |
