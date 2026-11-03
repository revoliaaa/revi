# Laporan Koreksi Upah dan Biaya Patroli

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD.mdl`. Model ini adalah salinan baru; `DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl`, `DKP_25HD_FINAL_2SKENARIO.mdl`, dan `DKP_25HD_FINAL_3SKENARIO.mdl` tidak ditimpa.

**Perangkat:** PySD 3.14.3. *Units Check* Vensim native belum dilakukan.

**Tanggal:** 3 November 2026

## 1. Ringkasan

| Unsur | Sebelum | Sesudah | Status data |
|---|---|---|---|
| `Upah Harian Patroli Berbayar` | Rp130.000/HOK | **Rp150.000/HOK** | Dikonfirmasi peneliti (1 HOK = 1 orang × 1 hari) |
| `Upah Setara Non Tunai Patroli` (= upah patroli) | Rp130.000/HOK | **Rp150.000/HOK** | Nilai ekuivalen tenaga sukarela; **bukan** pendapatan tunai |
| `Biaya per Hari Patroli` (biaya total) | Rp260.000/HOK | Rp260.000/HOK (tetap) | **Asumsi kerja, belum terverifikasi** sebagai biaya total aktual |
| `Komponen Non Upah Biaya Patroli` (baru, turunan) | – | 260.000 − 150.000 = Rp110.000/HOK | Turunan asumsi; **bukan** biaya logistik aktual terverifikasi |
| `Biaya Operasional Patroli Sukarela per Anggota per Tahun` | 9,17 × Rp130.000 = Rp1.192.050 (konstanta) | 9,17 × Rp110.000 = **Rp1.008.700** (turunan) | Nilai non-tunai logistik patroli reguler; kualitas C |
| `Hari Logistik Swadaya per Anggota` (baru) | tertanam dalam konstanta | 9,17 HOK/anggota/th | Log 2023; kualitas C |

Total HOK historis tidak diubah. Upah adalah **komponen** biaya total, bukan tambahan biaya.

## 2. Tiga besaran yang dibedakan

| Besaran | Definisi di model | Masuk kas? | Masuk NPV? | Masuk pendapatan RT? |
|---|---|---|---|---|
| **Upah aktual** | `Upah Patroli Berbayar` = HOK patroli yang dibiayai (pembiayaan historis, kas LPHD, jembatan) × Rp150.000 | Ya, sebagai bagian dari biaya patroli | Ya, sebagai bagian dari biaya | Ya, melalui `Upah Kegiatan PS` × porsi tambahan bersih 0,5 |
| **Nilai ekuivalen tenaga sukarela** | `Nilai Kontribusi Tenaga Non Tunai` = HOK patroli reguler × Rp150.000 (+ penanaman sukarela × Rp106.000) | Tidak | Hanya di `PV Kontribusi Non Tunai` (terpisah) | **Tidak** |
| **Biaya operasional patroli total** | HOK dibiayai × Rp260.000 (`Realisasi Pembiayaan Awal`, `Realisasi Belanja Perlindungan`, `Realisasi Pembiayaan Jembatan`) | Ya | Ya | Hanya bagian upahnya |

## 3. Rekonsiliasi patroli historis

| Tahun | HOK | Upah Rp150.000/HOK | Biaya total pada asumsi Rp260.000/HOK | Komponen non-upah implisit |
|---|---|---|---|---|
| 2024 (20 HD) | 2.533 | Rp379.950.000 | Rp658.580.000 | Rp278.630.000 |
| 2025 (25 HD) | 3.011 | Rp451.650.000 | Rp782.860.000 | Rp331.210.000 |
| **Total** | **5.544** | **Rp831.600.000** | **Rp1.441.440.000** | **Rp609.840.000** |

Bukti uji W1 (run S1 dan S2-C USD 20): keluaran model sama persis dengan tabel di atas.
- Upah 2024 = Rp379.950.000; 2025 = Rp451.650.000; total Rp831.600.000.
- HOK 2.533 dan 3.011.
- Biaya total historis tetap Rp1.441.440.000.

Pembiayaan historis 2024–2025 berlaku sama di S1 dan S2. Patroli dan biayanya tidak dihitung dua kali (U3 dan N3 lulus).

Patroli 2023 (392 kegiatan, ±2.160 keikutsertaan) tetap hanya menjadi kondisi awal respons perlindungan. Patroli itu tidak diklasifikasikan sebagai swadaya, dan model tidak mencatat arus kas 2023.

## 4. Audit biaya total Rp260.000/HOK

**Asal-usul:**
- Komentar parameter (REV-V4): "Upah Rp130.000/orang-hari + logistik Rp130.000 (BBM, konsumsi, alat)".
- Sumber: cuplikan Perbup Kotawaringin Barat 29/2020. Itu bukan kabupaten lokasi penelitian, dan nominalnya tahun 2020. Kualitas C.
- Pembanding: rencana anggaran patroli WAS Rp966,84 juta/th untuk 20 HD (setara 3.719 hari-orang pada Rp260.000).

**Konsekuensi upah Rp150.000:**
- Bila biaya total Rp260.000 dipertahankan, komponen non-upah implisit menjadi Rp110.000/HOK, bukan Rp130.000.
- Angka Rp110.000 **tidak** diperlakukan sebagai biaya logistik aktual. Nilai itu hanya sisa dari dua angka yang salah satunya masih asumsi.

**Kemungkinan biaya total:**

| Kemungkinan | Biaya total/HOK | Dasar | Dipakai sebagai |
|---|---|---|---|
| (a) Rp260.000 benar sebagai biaya total | 260.000 | Asumsi kerja saat ini | **Nilai dasar** |
| (b) Tidak ada biaya selain upah | 150.000 | Batas bawah; tidak boleh dipakai tanpa bukti | Sensitivitas bawah |
| (c) Proporsi upah : logistik 50 : 50 seperti sumber awal | 300.000 | Mempertahankan rasio Perbup | Sensitivitas atas |

Ketiganya dijalankan sebagai sensitivitas pada Tahap 3–4. Nilai dasar tidak diubah diam-diam.

**Pemeriksaan hitung ganda:**

| No | Pemeriksaan | Hasil |
|---|---|---|
| 1 | Upah patroli berbayar ≤ biaya patroli total di semua t (S1, A20, C20, C35) | Lulus. Rasio upah/biaya = 0,576923 = 150/260 tepat (uji W2); upah tidak ditambahkan di atas biaya |
| 2 | Patroli reguler (sukarela) tidak dibebani biaya Rp260.000 | Benar. Hanya HOK yang dibiayai (historis, kas LPHD, jembatan) masuk biaya |
| 3 | Logistik patroli reguler (non-tunai) vs biaya patroli berbayar | Tidak tumpang tindih: logistik non-tunai dihitung dari anggota yang berpartisipasi pada patroli **reguler** saja. Kini diturunkan dari komponen non-upah agar konsisten (9,17 × Rp110.000) |
| 4 | Nilai non-tunai tidak masuk pendapatan RT | Lulus. Logistik non-tunai ×10 → \|Δ pendapatan bersih per RT\| = 0 (uji W3) |
| 5 | `Manfaat Ekonomi Patroli` (= HOK × `Upah Patroli per HOK` = 0) | Variabel lama, bernilai 0, tidak dipakai di pendapatan. Tidak ada hitung ganda |
| 6 | Upah pengendalian kebakaran (`Upah Harian Pengendalian Kebakaran` = Rp130.000) | **Tidak diubah.** Aktivitas berbeda (tim pengendalian karhutla), sumbernya standar biaya MPA (Perbup Kobar), dan merupakan komponen `Biaya per Regu`. Perlu konfirmasi peneliti: [PERLU DIISI]. Sensitivitas Rp150.000 disiapkan |
| 7 | Upah penanaman (Rp106.000/HOK) | Tidak diubah; bukan patroli |

## 5. Dampak koreksi (uji W5; S1, dibanding upah lama)

| Indikator | Upah Rp130.000 | Upah Rp150.000 |
|---|---|---|
| Pendapatan program per RT bergantung 2024 | Rp7.765 | Rp8.960 |
| Upah kegiatan PS 2025 | Rp391.430.000 | Rp451.650.000 |
| Nilai tenaga non-tunai patroli reguler S1 (2030) | 1.505,5 HOK × Rp130.000 = Rp195,7 juta | 1.505,5 × Rp150.000 = Rp225,8 juta |
| Hutan 2087, biaya kas, NPV | tidak berubah | tidak berubah (biaya total tetap Rp260.000) |

Di S2, upah patroli yang dibiayai jembatan dan kas LPHD naik 15,4 % per HOK. HOK, biaya kas, dan NPV tidak berubah, karena upah sudah berada di dalam biaya total.

## 6. Dokumen lama yang masih memuat Rp130.000 sebagai upah patroli

Dokumen berikut **tidak ditimpa** (arsip proses) dan **digantikan** oleh laporan ini untuk nilai upah patroli:
- `laporan/AUDIT_S2_MODEL_3SKENARIO.md`
- `laporan/RANCANGAN_KOREKSI_DUA_SKENARIO_FASE1.md`
- `laporan/fase1b/REGISTER_PARAMETER_DAN_SUMBER.md` (baris upah dan upah setara)
- `laporan/fase1b/AUDIT_KONSISTENSI_SKENARIO.md`
- `laporan/fase1b/FINAL_GATE_SEBELUM_IMPLEMENTASI.md`
- `laporan/fase1b/RENCANA_UJI_FASE2.md` (kriteria U3 "2.533 × 130.000")

Semua hasil Fase 4 dan sesudahnya memakai Rp150.000.

## 7. Yang masih perlu dikonfirmasi

1. Apakah Rp260.000/HOK adalah biaya total aktual, dan apa saja komponennya (BBM, konsumsi, alat, transport). Bila ada data realisasi biaya mitra 2024–2025, nilai dasar dapat diganti.
2. Upah tim pengendalian kebakaran.
3. Status pembayaran upah 2024–2025: apakah seluruh 5.544 HOK benar-benar dibayar Rp150.000 tunai kepada anggota.
