# Laporan Perubahan Persamaan Model: FINAL A1 (4 skenario) → FINAL 3 SKENARIO

**Model baru:** `DKP_25HD_FINAL_3SKENARIO.mdl`. Berisi 723 variabel, 39 stok, dan 16 View; Euler, DT 0,0625, 2024–2087.
**Model eksperimen alokasi:** `DKP_25HD_FINAL_3SKENARIO_ALOKASI.mdl`. Model ini adalah model utama ditambah 16 variabel alokasi dan 6 persamaan bersyarat switch.
**Tanggal revisi:** 3 November 2026. Tag pada komentar persamaan: `REV-3S 2026-11-03`.

Berkas model dan makalah sebelumnya tidak ditimpa.

---

## 1. Cara berkas model disusun (penting dibaca)

Berkas `DELTA_KAPUAS_25HD_SD_FINAL_A1.mdl` **tidak ada** di paket serah-terima. Karena itu model direkonstruksi dari `REGISTER_VARIABEL_PER_VIEW_A1.xlsx` (lembar "2 Semua variabel"). Lembar itu memuat persamaan, satuan, dan dokumentasi lengkap ke-724 variabel.

Rekonstruksi diverifikasi sebelum revisi apa pun diterapkan. Model hasil rekonstruksi dijalankan ulang dan dibandingkan dengan hasil resmi di `REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx` (lembar Hasil 2030, 2050, 2087, Rerata 2030–2055, dan Kumulatif 2025–2086).

| Model yang dibandingkan | Skenario | Nilai dibandingkan | Berbeda > 0,01 % |
|---|---|---|---|
| A1 (rekonstruksi) | S1, S2, S3, S4 USD 6/10/15/20/35 | 8 × 2.184 = 17.472 | **0** |
| Eksperimen alokasi (rekonstruksi) | B0-10, B1-10, B2-6, B3-35, B4-20, R1-10, R2-20 | 7 × 2.228 = 15.596 | **0** |
| Analisis turunan | NPV proyek/mitra, harga impas 6,83/7,40, cakupan LPHD 100 % pada USD 28,04, S2−S1 1.720 ha, S4−S3 535/3.588 ha | – | **0** |

Kesimpulannya, persamaan dasar yang direvisi identik secara numerik dengan model FINAL A1 yang dibekukan.

**Keterbatasan berkas .mdl.** Bagian sketch (diagram 16 View) dibuat otomatis, karena tata letak diagram asli hanya tersimpan di berkas .mdl asli.
- Setiap View memuat variabel aslinya, variabel bayangan (abu-abu) untuk masukan dari View lain, dan panah sebab-akibat.
- Aliran digambar sebagai variabel biasa, bukan pipa dan katup.
- PySD membaca ke-16 View dengan benar, dan hasil simulasinya identik.
- **Rekomendasi:** bila diagram asli ingin dipertahankan, terapkan 12 perubahan pada bagian 3 langsung ke berkas .mdl asli di Vensim. Persamaannya pendek dan dapat disalin dari lembar "2 Perubahan persamaan" di register hasil.

---

## 2. Masalah pada model lama yang diperbaiki

| No | Masalah | Bukti di model lama |
|---|---|---|
| P1 | Patroli swadaya S2 ±2.355 HOK/th diturunkan dari log 2023 (183 anggota × 12,87 HOK) dan **berlanjut sepanjang 2024–2087 tanpa sumber dana** | `Hari Patroli Swadaya = Switch PS*MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota` |
| P2 | Patroli pembiayaan awal diestimasi dari angka lama (1.045 kegiatan 2024 − 427,6 kegiatan swadaya 2023) × 5,51 HOK/kegiatan = 3.402 HOK/th. Nilai yang sama diulang untuk 2025 | `Hari Patroli Tambahan Tercatat 2024`; `Hari Patroli Pembiayaan Awal` |
| P3 | Pembiayaan awal Rp 1,77 miliar **dihitung dari angka patroli lama** (3.402 HOK × Rp 260.000 × 2 tahun), bukan input independen | `Realisasi Pembiayaan Awal = Hari Patroli Pembiayaan Awal*Biaya per Hari Patroli` |
| P4 | Tahun 2024–2025 dihitung dua lapis: patroli swadaya 2.355 HOK ditambah patroli pembiayaan awal 3.402 HOK = 5.757 HOK/th | `Indeks Intensitas Perlindungan = (Hari Patroli Swadaya + Hari Patroli Didanai)/Kebutuhan` |
| P5 | Empat skenario memisahkan "PS reguler" dan "pembiayaan awal". Padahal patroli aktual 2024–2025 adalah satu kegiatan yang didukung pembiayaan awal | `Switch Pendanaan Awal = Skenario Kebijakan>=3`; `Switch Karbon = Skenario Kebijakan=4` |

Kesimpulan untuk butir 4 Master Prompt: Rp 1,77 miliar **bukan** input independen. Karena itu nilai ini dihitung ulang dari input patroli final (lihat bagian 4).

---

## 3. Daftar perubahan persamaan

### 3.1 Struktur skenario (View 16 Scenario Controls)

| Variabel | Lama | Baru |
|---|---|---|
| `Skenario Kebijakan` | 4 (1 = S1, 2 = S2, 3 = S3, 4 = S4) | **3** (1 = S1 tanpa PS aktif; 2 = S2 PS + pembiayaan awal; 3 = S3 S2 + karbon) |
| `Switch Pendanaan Awal` | `IF THEN ELSE(Skenario Kebijakan>=3, 1, 0)` | `IF THEN ELSE(Skenario Kebijakan>=2, 1, 0)` |
| `Switch Karbon` | `IF THEN ELSE(Skenario Kebijakan=4, STEP(1,Tahun Mulai Karbon), 0)` | `IF THEN ELSE(Skenario Kebijakan=3, STEP(1,Tahun Mulai Karbon), 0)` |
| `Switch PS`, `Switch Rehabilitasi` | `Skenario Kebijakan>=2` | **tidak berubah** (aktif di S2 dan S3) |

### 3.2 Patroli pembiayaan awal (View 04 Forest Patrol Protection)

**Variabel baru**

| Variabel | Persamaan | Satuan | Keterangan |
|---|---|---|---|
| `HOK Patroli Pembiayaan Awal Aktual 2024` | 2533 | HOK/Year | Rekap final peneliti, 20 HD; 1 keikutsertaan = 1 HOK |
| `HOK Patroli Pembiayaan Awal Aktual 2025` | 3011 | HOK/Year | Rekap final peneliti, 25 HD |
| `Periode Pembiayaan Awal` | `STEP(1, Tahun Awal Pembiayaan Awal)-STEP(1, Tahun Akhir Pembiayaan Awal+1)` | Dmnl | Bernilai 1 pada 2024–2025 |
| `Switch Patroli Swadaya Reguler` | 0 | Dmnl | Patroli swadaya di luar pembiayaan awal hanya boleh diaktifkan bila ada data terpisah |

**Persamaan diubah**

```
Hari Patroli Pembiayaan Awal =
  Switch Pendanaan Awal*(
     HOK Patroli Pembiayaan Awal Aktual 2024*(STEP(1, Tahun Awal Pembiayaan Awal)-STEP(1, Tahun Awal Pembiayaan Awal+1))
   + HOK Patroli Pembiayaan Awal Aktual 2025*(STEP(1, Tahun Akhir Pembiayaan Awal)-STEP(1, Tahun Akhir Pembiayaan Awal+1)))
  ~ HOK/Year
```

Persamaan lama memakai `MIN(... Hari Patroli Tambahan Tercatat 2024 ..., MAX(0, Kapasitas Hari Patroli Anggota-Hari Patroli Swadaya))`. Pembatas kapasitas dihapus karena angka ini adalah data aktual, bukan rencana. Kapasitas anggota pada 2024 (≥ 8.784 HOK) juga jauh di atas 2.533 HOK.

```
Hari Patroli Swadaya =
  Switch PS*Switch Patroli Swadaya Reguler*(1-Periode Pembiayaan Awal)
  *MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota
  ~ HOK/Year
```

Dengan `Switch Patroli Swadaya Reguler = 0`, nilai ini 0 di semua skenario, sehingga angka 2.355 HOK tidak dipakai. Faktor `(1-Periode Pembiayaan Awal)` menjaga agar, kalaupun switch diaktifkan kelak dengan data baru, patroli 2024–2025 tetap tidak dihitung dua kali.

**Variabel dihapus**, karena tidak dipakai lagi dan menjadi dasar estimasi lama:
- `Kegiatan Patroli Tercatat 2024` (1.045)
- `Kegiatan Patroli Swadaya Tahunan 2023` (427,6)
- `Orang Hari per Kegiatan Patroli` (5,51)
- `Porsi Kenaikan Patroli 2024 dari Pembiayaan Awal` (1)
- `Hari Patroli Tambahan Tercatat 2024`

### 3.3 Komponen pembiayaan (View 13–14)

| Variabel | Perubahan | Alasan |
|---|---|---|
| `Besaran Pendanaan Awal Proyek Karbon` | Tetap 0; komentar diperjelas | Jalur pendanaan awal generik (`Pendanaan Awal untuk Patroli`) dinonaktifkan agar kegiatan yang sama tidak masuk dua komponen pembiayaan |
| `Penggunaan Dana Perlindungan Total` | `+ Realisasi Pembiayaan Awal` | Total belanja perlindungan kini mencakup patroli pembiayaan awal (variabel pelaporan, tidak umpan balik) |
| `Total Pembiayaan Tambahan S3` | `+ Realisasi Pembiayaan Awal` | Nama dipertahankan agar kompatibel; isinya total pembiayaan tambahan S2/S3 (pelaporan) |

### 3.4 Yang tidak diubah

Persamaan lain dipertahankan, termasuk:
- tutupan lahan, laju BAU hasil kalibrasi, karbon, dan gambut;
- efektivitas 0,37 dengan waktu penyesuaian 3 tahun;
- KUPS, pendapatan RT, kehilangan akses, kapasitas LPHD, dan biaya MRV;
- bagi hasil 60/40 dan kebutuhan dana;
- basis kredit A1 (`Switch Baseline Kredit Konservatif` = 0).

---

## 4. Penempatan patroli 2024–2025 dan cek penghitungan ganda

| Komponen | S1 | S2 | S3 |
|---|---|---|---|
| `Hari Patroli Pembiayaan Awal` 2024 / 2025 (HOK) | 0 / 0 | 2.533 / 3.011 | 2.533 / 3.011 |
| `Hari Patroli Swadaya` (seluruh periode) | 0 | 0 | 0 |
| Patroli dari dana karbon 2024–2025 (`Realisasi Belanja Perlindungan`) | 0 | 0 | 0 (kas karbon belum ada) |
| Patroli pembiayaan awal sesudah 2025 | 0 | 0 | 0 |
| `Hari Patroli Didanai` 2024 / 2025 | 0 | 2.533 / 3.011 | 2.533 / 3.011 |
| Intensitas perlindungan 2024 / 2025 | 0 | 0,317 / 0,377 | 0,317 / 0,377 |
| `Kumulatif Realisasi Pembiayaan Awal` | 0 | **Rp 1.441.440.000** | Rp 1.441.440.000 |

**Pembiayaan awal dihitung ulang:**
- 2024: 2.533 HOK × Rp 260.000 = Rp 658.580.000.
- 2025: 3.011 HOK × Rp 260.000 = Rp 782.860.000.
- **Total Rp 1,44 miliar** (sebelumnya Rp 1,77 miliar).

Parameter biaya tetap `Biaya per Hari Patroli` Rp 260.000/HOK (Perbup Kotawaringin Barat 29/2020, kelas C). Upah yang diterima peserta dihitung terpisah: Rp 130.000/HOK (`Upah Harian Patroli Berbayar`).

**Konsistensi satuan pada persamaan yang diubah:**
- HOK/Year × Rupiah/HOK = Rupiah/Year (`Realisasi Pembiayaan Awal`).
- STEP() bersatuan Dmnl.
- Intensitas = (HOK/Year)/(HOK/Year) = Dmnl.

Uji satuan otomatis Vensim (*Units Check*) belum dijalankan, karena perangkat Vensim tidak tersedia di lingkungan ini.

---

## 5. Konsekuensi struktural yang perlu diketahui peneliti

1. **Setelah 2025, tidak ada patroli pada S2.**
   - Intensitas perlindungan turun ke 0.
   - Efek yang sudah terbentuk memudar mengikuti waktu penyesuaian 3 tahun (SMOOTHI).
   - Laju deforestasi S2 kembali setara S1 sekitar 2035.
2. **Kebutuhan dana perlindungan naik.**
   - Seluruh kebutuhan patroli (7.996 HOK/th) kini harus didanai, karena tidak ada lagi swadaya yang mengurangi kebutuhan.
   - Kebutuhan patroli: 7.996 × Rp 260.000 = Rp 2,08 miliar/th, sebelumnya Rp 1,47 miliar.
   - Kebutuhan minimum LPHD menjadi **Rp 6,03 miliar/th**, sebelumnya Rp 5,42 miliar.
3. **Loop karbon pada harga rendah tidak "menyala".**
   - Kredit pada S3 hanya berasal dari efek patroli 2024–2025, karena baseline kredit A1 = S1.
   - Pada USD 6–20, penerimaan tidak cukup menutup biaya MRV tetap, sehingga dana untuk patroli kecil atau nol.
4. **Kode skenario lama tidak kompatibel.** `Skenario Kebijakan = 4` tidak lagi bermakna; S3 memakai kode 3.
5. **Basis kredit A2.** Variabel `Porsi Mitigasi Adisional terhadap S2` tetap ada. Karena patroli swadaya kini 0, basis A2 menjadi praktis sama dengan A1. A2 memang tidak dipakai di makalah.
