# Kekurangan Bukti Validasi: Model 4 Skenario (S1–S4)

## Status yang dipakai

**BELUM DAPAT DIVERIFIKASI** berarti klaim mungkin benar, tetapi berkas yang diperlukan untuk menghitung ulang tidak ada di paket audit. **Status ini bukan GAGAL.** Tidak ada uji di dokumen ini yang dinyatakan gagal hanya karena log tidak tersedia.

## Berkas yang diperiksa

- `MODEL_VENSIM.zip`: 10 `.mdl`, 9 `.vdfx`, 8 ekspor `.txt`, 2 `.xlsx`.
- Naskah PDF.
- Branch lain di repo `revoliaaa/revi`:
  - `claude/relaxed-bohr-qopx49`: paket GIS `delta-kapuas-gis/`.
  - `claude/new-session-bao4rv`: `tesis_3skenario/`, versi model 3/2 skenario.
  - `claude/eloquent-galileo-53dhud`: salinan `.mdl` 4 skenario.

**Peringatan versi:** berkas di `claude/new-session-bao4rv` milik **model revisi 3/2 skenario** dengan persamaan dan input berbeda. Isinya **tidak boleh** dipakai sebagai bukti validasi S1–S4. Isinya hanya dikutip sebagai keterangan tentang ketersediaan berkas model lama.

---

## 1. MAPE stok hutan (3,92 %; pembanding 8,88 % dan 8,43 %)

| Unsur | Isi |
|---|---|
| Klaim makalah | hlm. 6: "MAPE stok hutan model sebesar 3,92 %, lebih rendah daripada pembanding sederhana (8,88 % dan 8,43 %)" |
| Yang tersedia | (a) Data tutupan HCV yang diharmonisasi di `claude/relaxed-bohr-qopx49:delta-kapuas-gis/04_VALIDATION/` (`HCV_HARMONISED_SERIES.csv`, `HCV_NATURAL_FOREST_SERIES.csv`, `HCV_EPOCH_RELIABILITY.csv`, `HCV_VS_SATELLITE_TESTS.csv`). (b) Register: "kalibrasi 2003–2014; validasi 2019/2024"; skrip disebut `d25/calib25.py`. (c) Laporan branch 3 skenario baris 67–70: angka ini berasal dari "model lama", dan "skrip hindcast-nya tidak ada di paket". |
| Mengapa belum dapat dihitung ulang | Model S1–S4 di ZIP dimulai pada 2024. Run historis (hindcast) 2003/2000–2024 butuh konfigurasi model lain (`INITIAL TIME`, kondisi awal tahun dasar, deret pemicu historis) yang tidak disertakan. |
| Bukti yang diperlukan | 1. Berkas model hindcast (`.mdl` atau `.py`) beserta md5-nya, dan penjelasan perbedaannya dari model A1. 2. Skrip kalibrasi `d25/calib25.py` dan keluaran parameternya (kdef 0,6737; kreg 0,4381; D2 × 1,53). 3. Tabel observasi stok hutan per tahun epoch (2019, 2024), dengan sumber peta, satuan (ha), cakupan wilayah (SK 124.941 ha atau subset), dan kelas yang dihitung sebagai hutan. 4. Keluaran simulasi pada tahun yang sama. 5. Rumus MAPE yang dipakai, termasuk agregasi per lanskap atau total dan jumlah titik. 6. Definisi kedua pembanding (linear; laju konstan), periode pembentuknya, dan keluarannya. 7. Catatan selisih transkripsi 37,94 ha (2024) dan inkonsistensi epoch Kubu 2009 / Pulau Maya 2014–2024 yang dicatat register. |
| Cara reproduksi | Jalankan model hindcast, ambil `Total Hutan` pada tahun observasi, hitung MAPE = rerata(\|sim − obs\| / obs) dan pembandingnya. Simpan `.csv` input dan output beserta md5. |
| Status | **BELUM DAPAT DIVERIFIKASI** |

## 2. MAPE aliran kehilangan tutupan pohon Hansen (73,3 %; pembanding 60,4 %)

| Unsur | Isi |
|---|---|
| Klaim | Konteks peneliti: "MAPE 73,3 %, lebih buruk dari pembanding 60,4 %". Laporan branch 3 skenario menulis periode 2017–2024. **Angka ini tidak disebut di makalah.** |
| Yang tersedia | Data Hansen GFC v1.13 dan tren tahunan di `claude/relaxed-bohr-qopx49:delta-kapuas-gis/` (`02_REMOTE_SENSING_DATA/`, `03_LAND_COVER_CHANGE/TRENDS_PROJECT_AREA_ANNUAL.csv`, `ZONAL_SK_HD*.csv`). Register mencatat loss bruto 2001–2024 sebesar 17.183,4 ha. |
| Bukti yang diperlukan | 1. Deret observasi tahunan yang dipakai: wilayah (SK atau PA), ambang kanopi (> 30 %), dan tahun. 2. Deret simulasi `Deforestasi Total` hindcast pada tahun yang sama. 3. Penjelasan konversi definisi: Hansen tree-cover loss ≠ deforestasi regulasi (loss bruto mencakup rotasi/gangguan, tanpa gain). 4. Definisi pembanding 60,4 %. 5. Skrip perhitungan. |
| Catatan | MAPE aliran yang lebih buruk dari pembanding adalah hasil **valid untuk dilaporkan sebagai keterbatasan**, bukan alasan menyembunyikan validasi stok. |
| Status | **BELUM DAPAT DIVERIFIKASI**; disarankan disebut di makalah sebagai keterbatasan |

## 3. Monte Carlo (13 parameter; seed 20261101; n = 3.000 pada USD 10 dan 1.500 pada USD 20)

| Unsur | Isi |
|---|---|
| Klaim makalah | hlm. 5, 6, 8: S2<S1 pada 100 % tarikan; median S2−S1 1.561 ha (P5–P95 671–2.740); S4<S3 92,6 % / 99,5 %; median S4−S3 265 ha (0–1.705) dan 1.780 ha (86–9.889); NPV>0 60,9 % / 94,6 %; kebutuhan LPHD tertutup 0 % / 4,2 %; pendapatan RT naik 6,5 % / 4,9 % |
| Yang tersedia | Tidak ada di ZIP. Laporan branch 3 skenario (`LAPORAN_VERIFIKASI_VENSIM_PYSD_SENSITIVITAS_3S.md`, bagian C) menyatakan "Skrip dan berkas Monte Carlo lama tidak ada di paket". Spesifikasi yang disusun ulang di sana, dijalankan pada "model lama" dengan n = 200, memberi angka yang mendekati (median S2−S1 1.555 ha; S4>S3 USD 10 92,0 %; NPV>0 58,5 %). **Itu uji kewajaran dengan spesifikasi rekonstruksi, bukan reproduksi MC asli**, dan berkasnya tidak diaudit di sini. |
| Bukti yang diperlukan | 1. Daftar 13 parameter dengan nama variabel model persis. 2. Sebaran tiap parameter (jenis, batas/parameter, sumber atau alasan). 3. Metode sampling (LHS atau acak), seed 20261101, n per harga, dan apakah tarikan S3 dan S4 berpasangan (sampel sama). 4. Berkas model yang dijalankan beserta md5, dan basis kredit (A1, `Switch Baseline Kredit Konservatif = 0`, faktor = 1). 5. Tabel keluaran per tarikan: parameter + indikator (S2−S1, S4−S3, NPV, cakupan LPHD, ΔRT), dengan definisi periode masing-masing indikator. 6. Skrip MC (PySD atau Vensim Sensitivity), versi perangkat, dan log run (jumlah run gagal, bila ada). 7. Definisi "kebutuhan minimum LPHD tertutup" per tarikan: rasio belanja total (seperti Tabel 4) atau berbasis kesenjangan. **Definisi ini menentukan arti angka 0 % / 4,2 % (lihat Temuan 2).** |
| Cara reproduksi | Dengan butir 1–4, MC dapat dijalankan ulang dengan PySD 3.14.3 pada `.mdl` di ZIP, lalu dibandingkan dengan butir 5. |
| Status | **BELUM DAPAT DIVERIFIKASI** |

## 4. PRCC (+0,77 laju BAU; −0,79; +0,95 efektivitas)

| Unsur | Isi |
|---|---|
| Klaim | Makalah hlm. 6: efektivitas PRCC +0,95 untuk deforestasi dihindari (S2−S1). Makalah hlm. 9: PRCC −0,79 dikaitkan dengan "asumsi akses". Konteks peneliti: −0,79 untuk **biaya MRV**. |
| Ketidaksesuaian label | Nilai −0,79 dikaitkan dengan dua parameter berbeda. Bisa jadi dua PRCC berbeda kebetulan sama, atau salah satu label keliru. Ini **perlu klarifikasi**, bukan bukti kesalahan. |
| Konsistensi arah | **CONSISTENT.** Uji OAT audit (`07_UNCERTAINTY/robustness_oat.csv`) menunjukkan efektivitas dominan pada S2−S1, biaya MRV menurunkan S4−S3, dan pengali akses menentukan tanda ΔRT. Ini konsistensi arah, **bukan** verifikasi angka PRCC. |
| Bukti yang diperlukan | 1. Matriks tarikan MC (butir 3.5). 2. Skrip PRCC (transformasi peringkat, regresi parsial, penanganan parameter konstan). 3. Untuk setiap PRCC: parameter, indikator keluaran, harga, dan periode. 4. Uji signifikansi atau interval, bila dilaporkan. |
| Status | **BELUM DAPAT DIVERIFIKASI** |

## 5. Pengujian Vensim–PySD ("±413.000 nilai tahunan; 99,87–100 % sesuai")

| Unsur | Isi |
|---|---|
| Klaim makalah | hlm. 5: "Dari sekitar 413.000 nilai tahunan, 99,87–100 % sesuai hingga ketelitian ekspor" |
| Yang tersedia | 7 ekspor `.txt` Vensim A1 di ZIP (S1, S2, S3, USD 6, 10, 15, 35) dan 1 ekspor eksperimen alokasi. |
| Hasil uji audit **[DIAGNOSTIK BARU]** | 7 run A1, 324.096 nilai, rtol 5×10⁻⁶: 99,05–99,86 % identik. Selisih terkonsentrasi pada variabel pemeriksa yang nilainya mendekati nol (`Check Total Kawasan`, `Check Konservasi Karbon`) dan variabel ARR kecil. Untuk 16 variabel indikator utama, selisih relatif maksimum ≤ 7×10⁻⁶. Hasil: `06_VALIDATION/pysd_vs_vensim.csv`, `key_vensim_pysd.csv`. |
| Mengapa angka makalah belum dapat dicocokkan | Jumlah nilai, run yang dipakai, dan kriteria toleransi pada uji asli tidak terdokumentasi. Perbedaan 99,05 % vs 99,87 % dapat berasal dari kriteria toleransi absolut untuk nilai mendekati nol, atau dari himpunan run yang berbeda. **Ini bukan bukti ketidaksesuaian model.** |
| Kekurangan lain | (a) Run S4 USD 20 hanya ada sebagai `.vdfx` biner, tanpa ekspor teks. (b) `HASIL SIMULASI VENSIM.xlsx` rusak karena impor dengan locale Indonesia (titik desimal hilang), jadi tidak dapat dipakai. (c) README register menulis "Vensim native belum dijalankan", padahal ekspor Vensim bertanggal 2 November 00:14–00:33, lebih awal dari register (02:04). Pernyataan README kemungkinan usang, tetapi perlu dikonfirmasi peneliti. |
| Bukti yang diperlukan | 1. Daftar run dan berkas ekspor yang dipakai pada uji asli. 2. Kriteria kecocokan (relatif dan/atau absolut; jumlah angka penting). 3. Skrip pembanding dan keluarannya (jumlah nilai, jumlah cocok per run). 4. Versi Vensim. 5. Ekspor `.txt`/`.tab` untuk S4 USD 20 dari `Run/Skenario4USD20.vdfx`, tanpa melalui Excel berlocale Indonesia. |
| Status | Variabel utama **CONSISTENT** (diuji audit). Angka "413.000; 99,87–100 %" **BELUM DAPAT DIVERIFIKASI**. |

## 6. Bukti pendukung lain yang dirujuk tetapi tidak disertakan

| Berkas yang dirujuk register/dokumentasi | Dipakai untuk | Status |
|---|---|---|
| `a1/out/FINAL_THESIS_RESULTS.xlsx` | "Hasil resmi" pada lembar `9 Cek reproduksi` | tidak ada. Angka register cocok dengan run audit. |
| `solve_a1.py`, `solve_closure.py` | Faktor rekonsiliasi A1 (= 1) dan A2 (0,72–0,76) | tidak ada. Nilai faktor tereproduksi hasilnya, tetapi prosedurnya belum. |
| `d25/calib25.py` | Laju BAU terkalibrasi | tidak ada |
| `DELTA_KAPUAS_25HD_SD_FINAL_A1.mdl` (md5 f1bfaa88…) | Model induk | tidak ada. Berkas skenario di ZIP dipakai sebagai sumber. |
| Sumber data KUPS 2023 (15 KUPS; 277 anggota) | Kondisi awal | [PERLU DIISI] |
| PDD Delta Kapuas Appendix 11–12 | Baseline dan metodologi kredit | register: "tidak tersedia" |

## Prioritas sebelum seminar

1. **Ekspor teks S4 USD 20.** Pekerjaan beberapa menit di Vensim, dan langsung melengkapi uji Vensim–PySD.
2. **Spesifikasi MC** (butir 3.1–3.4) dan matriks keluarannya. Tanpa ini, seluruh angka MC di makalah perlu disertai catatan "[berkas pendukung PERLU DIISI]".
3. **Klarifikasi label PRCC −0,79.**
4. **Data dan skrip MAPE**, atau tulis MAPE sebagai hasil yang dilaporkan peneliti tanpa lampiran, dan sebut MAPE aliran 73,3 % sebagai keterbatasan.
