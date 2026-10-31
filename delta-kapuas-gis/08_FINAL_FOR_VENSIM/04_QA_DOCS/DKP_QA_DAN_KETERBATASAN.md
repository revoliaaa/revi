# Laporan QA dan Keterbatasan: Master Spasial 25 HD Delta Kapuas

Tanggal: 31-10-2026. Semua angka berasal dari skrip `07_REPRODUCIBLE_CODE/src` (s03, s06, s14, s15, s16). Uji keras otomatis ditulis sebagai `assert` di `s15_master_spatial.py`: jika salah satu gagal, paket tidak dibangun.

## 1. Hasil pemeriksaan

| # | Pemeriksaan | Hasil | Status |
|---|---|---|---|
| 1 | Jumlah poligon | 25 poligon, 1 per HD, HD_ID unik, tidak ada HD yang hilang | PASS |
| 2 | Luas Project Area vs PDD | UTM 49S planar 111.123,16 ha vs PDD 111.123,20 ha (−0,04 ha). Geodesik 111.134,95 ha (+11,8 ha, distorsi skala UTM). | PASS |
| 3 | CRS | EPSG:4326 (.prj). Riwayat `.shp.xml` memuat dua kali *DefineProjection*; koordinat diverifikasi sebagai derajat geografis di lokasi yang benar. | PASS |
| 4 | Validitas geometri | 0 invalid, 0 kosong, 0 duplikat, 0 tumpang tindih > 0,01 ha | PASS |
| 5 | Konservasi luas raster↔vektor | Rasio jejak raster / poligon geodesik = 0,9973–1,0013 per HD | PASS |
| 6 | Konsistensi overlay (master vs layer tematik) | Tutupan pohon persisten: raster 99.084,87 ha = master 99.084,87 ha. Loss 2001–2024: raster 11.723,68 ha = master 11.723,68 ha. Mangrove: vektor 45.039,3 ha vs master 45.050,5 ha (−0,02 %; maks. 3,5 ha per HD; selisih = piksel tepi, karena vektor dipotong eksak sedangkan master memakai aturan pusat-piksel). | PASS |
| 7 | Aritmetika atribut | LOSS0114 + LOSS1516 + LOSS1724 = LOSS0124 untuk 25 HD; TREE24 ≥ 0; loss ≤ TREE00 | PASS |
| 8 | Sensitivitas definisi (ambang kanopi) | Loss 2001–2024 PA: 11.730 / 11.724 / 11.695 ha (10/30/50 %), rentang 0,3 % | PASS |
| 9 | Nama atribut SHP | Semua ≤ 10 karakter; nama lengkap di GPKG dan kamus data | PASS |
| 10 | Kualitas data historis HCV | Kubu 2009 dan Pulau Maya 2014/2019/2024 menyimpang > 10 % dari seri harmonisasi. Pulau Maya 2003/2009 dan Kubu 2014: kelas mangrove melebihi batas GMW. Seri agregat ALL_25 tidak dapat dipakai untuk 2009–2024. | DICATAT (lihat `HCV_EPOCH_RELIABILITY`) |

## 2. Definisi yang dipisahkan secara tegas

- **Tutupan pohon** (Hansen) = vegetasi > 5 m dengan kanopi > 30 %. Ini **bukan** hutan dalam arti regulasi atau metodologi karbon.
- **Gross tree-cover loss** = hilangnya tutupan pohon (stand-replacing) pada tahun tertentu. **Bukan net forest loss** (regrowth tidak dihitung) dan **bukan deforestasi** regulasi.
- **TREE_2024_HA** = tutupan pohon 2000 tanpa loss terdeteksi sampai 2024 (tutupan persisten). Ini batas bawah tutupan pohon 2024, **bukan** luas hutan 2024.
- **FOREST_2024_HA**: dikosongkan. Tidak ada klasifikasi hutan 2024 yang tervalidasi, dan kelas HCV 2024 terbukti inkonsisten antar-epoch.
- **Mangrove** (GMW v3.0) = ekstensi tegakan mangrove menurut GMW. Definisinya berbeda dari kelas *Hutan Mangrove* HCV maupun dari **sedimen mangrove** di laporan gambut. Sedimen mangrove adalah material tanah; luasnya (52.703 ha) mengikuti masker tutupan lahan mangrove yang hampir identik dengan kelas mangrove HCV 2024 (52.398 ha).
- **Gambut** (laporan 2025) = tanah gambut ≥ 50 cm hasil *ordinary kriging*. Kedalaman < 50 cm diperlakukan sebagai tanah mineral.
- **Stok karbon tanah ≠ emisi yang dapat dikreditkan.** Emisi WRC gambut bergantung pada drainase/oksidasi dan subsidensi, bukan pada besarnya stok.

## 3. Temuan QA atas Laporan Gambut dan Mangrove (2025)

| # | Temuan | Bukti | Konsekuensi |
|---|---|---|---|
| G1 | Angka stok tidak konsisten antar-bab | Tabel 15: 154.675.959 tC (gambut 144.114.915; mangrove 10.561.044; 3.054,53 dan 200,39 tC/ha). Simpulan (hal. 74): 145.825.054 tC (gambut 133.521.424; mangrove 12.303.630; 4.446,12 dan 1.299,63 tC/ha). Angka Simpulan menyiratkan basis luas lain (≈ 30.031 ha gambut, ≈ 9.467 ha mangrove). | Tidak ada angka stok yang boleh dipakai sebelum diklarifikasi |
| G2 | Label kelas "≥ 50 cm" untuk sedimen mangrove keliru | 52.703,14 ha mencakup kelas < 50 cm (41.696,7 ha); kelas ≥ 50 cm hanya 11.006,4 ha | Luas sedimen mangrove harus dibaca beserta kelasnya |
| G3 | Evaluasi interpolasi tidak independen | 409 titik evaluasi (survei, Padang Tikar 2017, Murdiyarso 2015) juga merupakan input kriging. Kriging nyaris mereproduksi titik inputnya sendiri, sehingga R² = 0,99 dan RMSE 13 cm tidak mengukur akurasi prediksi. | Akurasi peta kedalaman belum diketahui; perlu validasi silang (leave-one-out) atau titik independen |
| G4 | Mayoritas titik interpolasi adalah data bangkitan | 5.778 titik termasuk titik `rnorm()` dari kelas kedalaman BBSDLP (1:250.000) dan Kubu Peatland Project; survei baru hanya 186 plot (17 dari 25 desa) | Peta kedalaman sangat dipengaruhi peta nasional skala kasar |
| G5 | Ketidakpastian stok terlalu kecil | U = 1,1 % (gambut) dan 5,9 % (mangrove) hanya dari Monte Carlo atas rata-rata BD, C-org dan kedalaman; galat interpolasi spasial tidak dimasukkan | Ketidakpastian riil jauh lebih besar |
| G6 | Domain laporan ≠ Project Area | Jumlah kelas Tabel 14 = 125.461 ha (≈ luas SK 124.941 ha; PA = 111.135 ha). Permukiman, tambak dan tubuh air dikecualikan. | Stok laporan tidak dapat dipetakan ke PA tanpa raster |
| G7 | Cakupan survei | Tidak ada plot di Kubu, Dabong, Sungai Bemban, Seruat Dua, Padang Tikar 1, Dusun Besar, Dusun Kecil, Kemboja | Atribut kedalaman survei kosong untuk HD tersebut |
| G8 | Raster tidak diserahkan | `PeatDepth_Interpolated_10m_cm_49S_ABS.tif` tidak tersedia di sesi ini | PEAT_HA tidak dapat dihitung per HD |

Kedalaman rata-rata per desa (Tabel 11) dimasukkan ke master hanya sebagai **rata-rata titik survei** (PT_DEPTH, MG_DEPTH). Nilai ini tidak dipakai untuk membuat poligon atau luas gambut.

## 4. Klaim yang sengaja TIDAK dibuat

- Tidak ada klaim regenerasi hutan dari perubahan kelas HCV. Contohnya mangrove Pulau Maya +3.773 ha (2019→2024): Landsat 8/9 hanya menemukan 3–11 ha area yang baru bervegetasi di PA, dan GMW stabil sejak 1996.
- Tidak ada poligon gambut dari titik survei.
- Tidak ada angka luas hutan 2024 atau luas gambut per HD yang diisi asumsi.
- Tidak ada konversi tutupan pohon, loss atau stok tanah menjadi kredit karbon.
- Tidak ada nama variabel Vensim yang dikarang. Hanya `Proporsi Kredit REDD dalam Project Area` yang dipakai, karena diberikan oleh peneliti.

## 5. Keterbatasan

1. Semua luas berbasis peta (pixel counting) tanpa sampel referensi probabilistik, sehingga tidak ada akurasi atau selang kepercayaan desain (Olofsson et al. 2014 direkomendasikan).
2. Hansen: tahun 2001–2010 belum diproses ulang (patahan metode 2011). Pulsa kebakaran 2015–2016 menyumbang 51 % loss PA.
3. Geometri SK 25 HD tidak tersedia, sehingga pangsa aktivitas deforestasi PA/SK (pengganti terukur 0,8535) belum dapat dihitung.
4. GMW berakhir 2020; tidak ada peta mangrove independen 2024.
5. Raster gambut dan peta gambut publik (GFW, perlu API key) tidak tersedia.
6. Nilai HCV ditranskripsi dari ekstraksi teks PDF. Sel rekonstruksi diberi flag (`QUALITY`) dan perlu dicek ke PDF asli.
