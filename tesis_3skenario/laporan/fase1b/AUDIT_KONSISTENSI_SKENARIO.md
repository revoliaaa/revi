# Audit Konsistensi Skenario (Fase 1B)

**Lingkup:** konsistensi S1 dan S2 pada persamaan usulan (`FASE1B_MATRIKS_PERSAMAAN_FINAL.md`).

**Metode:** penelusuran persamaan secara statis dan perhitungan analitis dari persamaan. **Tidak ada simulasi yang dijalankan.** Angka di dokumen ini adalah turunan langsung dari parameter, bukan keluaran model.

---

## 1. Invarian antarskenario

| Komponen | S1 | S2 | Sumber perbedaan |
|---|---|---|---|
| Kondisi awal 2024 (semua stok) | sama | sama | – |
| `Switch PS`, `Switch Rehabilitasi`, `Switch Pendanaan Awal` | 1 | 1 | – |
| Patroli 2024 / 2025 | 2.533 / 3.011 HOK | 2.533 / 3.011 HOK | – |
| Tim baru 2024 / 2025 | 61 / 10 orang | 61 / 10 orang | – |
| Patroli reguler 2026+ | 254 × 11,85 × k × indeks | sama | – |
| Kas non-karbon | `Dana Operasional Non Karbon Tunai` (default 0) | sama | – |
| Dukungan material rehabilitasi non-karbon | default 0 | sama | – |
| Pendampingan kelembagaan non-tunai | default 0 | sama | – |
| Penerbitan dan penjualan kredit, biaya MRV | 0 | aktif | `Switch Karbon` |
| Kas karbon ke LPHD (60 %) dan mitra (40 %) | 0 | aktif setelah kas pertama | `Switch Karbon` |
| Belanja kegiatan dari kas karbon | 0 | endogen | respons model |

**Pemakai `Switch Karbon` setelah usulan** (hasil penelusuran statis): `Kredit REDD Diajukan`, `Kredit ARR Diajukan`, `Kredit Gambut Diajukan`, `Biaya Monitoring MRV`, `Biaya Verifikasi Tahunan`, dan `Pendanaan Awal Proyek Karbon` (besarannya 0). Tidak ada kegiatan PS yang digerbang `Switch Karbon`.

**Konsekuensi yang dapat diuji (U4):** semua variabel fisik dan sosial S1 dan S2 identik sampai saat pertama kas karbon dibelanjakan. Yang boleh berbeda lebih awal hanyalah variabel kredit dan biaya MRV (sejak 2024), yang ditanggung mitra.

---

## 2. Patroli: hubungan K1 dan K2, dan risiko pengurangan ganda

### 2.1 Masalah pada rancangan Fase 1

Fase 1 mengusulkan dua mekanisme penurunan sekaligus:
- **K1:** patroli = anggota × 11,85 × k;
- **K2:** penggantian anggota = 0,625 (rasio kapasitas), sehingga anggota menyusut ±1,9 %/th.

Akibatnya patroli S1 turun dua kali: sekali lewat k, sekali lewat penyusutan anggota. Pada k = 0,5, patroli akan turun dari ±1.506 HOK (2026) menjadi ±475 HOK (2087). **Kedua penurunan tidak punya dasar data dan saling bertumpuk.** Ini pengurangan ganda yang tidak dapat dibenarkan.

### 2.2 Perbaikan final (Fase 1B)

- **Satu tuas untuk tingkat partisipasi:** `Tingkat Keberlanjutan Patroli Reguler` k (0–1).
- **Satu tuas opsional untuk tren waktu:** `Laju Penurunan Partisipasi Sukarela` (default 0; sensitivitas 0–3 %/th).
- **Keanggotaan dipertahankan** dengan penggantian 1, sama seperti A1, sehingga roster tidak ikut menurunkan patroli. Penggantian 0,625 hanya menjadi uji sensitivitas, dan **tidak boleh** dikombinasikan dengan laju penurunan dalam satu run dasar.
- **Basis patroli reguler = MIN(anggota aktif, 254).** Anggota yang direkrut dengan dana karbon (S2) menambah kapasitas patroli berbayar, tetapi tidak menambah patroli sukarela. Dengan begitu kenaikan sukarela tidak dihitung sebagai dampak karbon.

### 2.3 Persamaan yang menghubungkan kelima unsur

| Unsur | Persamaan | Nilai pada parameter dasar |
|---|---|---|
| Kapasitas tenaga | `Kapasitas Hari Patroli Anggota = Anggota Patroli Aktif*48` | 254 × 48 = 12.192 HOK/th |
| Intensitas partisipasi | `HOK Patroli per Anggota 2025 × k × Indeks Keberlanjutan Partisipasi` | 11,85 × 0,5 × 1 = 5,93 HOK/orang/th |
| Patroli reguler | `MIN(kapasitas, MIN(anggota, 254) × partisipasi)` | ±1.506 HOK/th |
| Kebutuhan operasional | `Hari Patroli Tambahan Dibutuhkan = MAX(0, MIN(target 7.996, kapasitas) − reguler − historis)`; `Kebutuhan Dana Perlindungan = × Rp 260.000` | (7.996 − 1.506) × Rp 260.000 ≈ Rp 1,69 miliar/th |
| Sumber daya tunai | `Realisasi Belanja Perlindungan` dari saldo LPHD (kas non-karbon + kas karbon) | S1: 0 bila kas non-karbon = 0 |
| Sumber daya non-tunai | tenaga (HOK reguler × Rp 130.000) dan logistik (anggota berpartisipasi × Rp 1,19 juta, File A) | ±Rp 196 juta + ±Rp 151 juta per tahun |
| Patroli tambahan dari kas karbon | `Hari Patroli Didanai Kas LPHD × Porsi Kas Karbon dalam Saldo` | S2 saja |

### 2.4 Mengapa patroli S1 dapat berlangsung tanpa penerimaan karbon, dan batas klaimnya

- Di model, patroli S1 setelah 2025 berjalan dengan tenaga dan logistik non-tunai dari anggota dan LPHD. Ini tercatat sebagai `Nilai Kontribusi Swadaya`, bukan kas.
- Patroli juga dapat ditambah kas non-karbon bila datanya ada.
- Patroli S1 tidak membutuhkan kas karbon, karena kegiatan tidak lagi digerbang `Switch Karbon`.
- **Bukan bukti empiris.** Patroli 2023–2025 seluruhnya didukung mitra. Belum ada data patroli tanpa pembiayaan. Karena itu k adalah **asumsi eksploratif (D)** dan hasil S1 serta S2 harus dilaporkan untuk k = 0, 0,25, 0,5, 0,75, dan 1.
- **k = 0 adalah batas bawah yang sah,** yaitu kasus bila tanpa pembiayaan tidak ada patroli. Nilai ini tidak dipakai sebagai nilai dasar.
- **Keterbatasan yang harus ditulis:** model tidak membatasi patroli sukarela dengan ketersediaan logistik. Nilai logistik dicatat, tetapi tidak menghentikan kegiatan bila tidak tersedia. Bila peneliti ingin pembatas logistik, perlu parameter ketersediaan logistik non-tunai (D) atau data.

### 2.5 Interaksi dengan rekrutmen A1 (catatan B)

- Cabang rekrutmen A1 (`IF Alokasi Dana Perlindungan > 0`) merekrut hingga `Anggota Patroli Dibutuhkan untuk Target` = 7.996/(48 × 0,5) = 333 orang dengan laju ≤ 20 × kapasitas orang/th.
- Rekrutmen ini terjadi begitu ada alokasi berapa pun besarnya. Ini perilaku A1 yang dipertahankan.
- Akibatnya anggota bisa melebihi yang dapat dibayar, tetapi tidak menimbulkan HOK fiktif: patroli berbayar tetap dibatasi rupiah, dan patroli sukarela dibatasi 254.

---

## 3. Rehabilitasi

**Struktur biaya per hektare penanaman** (`Biaya Penanaman per Ha` = Rp 14 juta, kelas C):

| Komponen | Persamaan | Nilai | Catatan |
|---|---|---|---|
| Tenaga | 85 HOK/ha × Rp 106.000 | Rp 9,01 juta/ha | HOK dan upah kelas C/B |
| Bibit, material, logistik, alat | 14 juta − 9,01 juta | Rp 4,99 juta/ha | Residual turunan (B). Tidak dapat dipisah lagi tanpa data |
| Pemeliharaan | Rp 1,4 juta/ha/th × 3 th | – | D. Tidak dipisah tenaga/material; dibiayai dari kas LPHD bila ada |

**Mekanisme S1 (K9):**
- `Penanaman Non Karbon = MIN(realisasi historis 0,0123 × 1.636,8 = 20,13 ha/th, Dukungan Material Rehabilitasi Non Karbon / Rp 4,99 juta)`.
- Bibit dan material **harus** punya sumber. Tenaga dapat sukarela (dicatat non-tunai) atau dibayar program (`Porsi Tenaga Penanaman Non Karbon Dibayar`).
- **Default dukungan material = 0, sehingga penanaman S1 = 0.** Ini bukan penghentian otomatis. Ini konsekuensi tidak adanya sumber material yang tercatat.
- Bila peneliti dapat menunjukkan bahwa realisasi historis 0,0123 berasal dari program yang berlanjut (misalnya persemaian BPDAS, BRGM, atau mitra), isi ±Rp 100 juta/th (20,13 × Rp 4,99 juta) dengan sumbernya.

**Kelas:** PERLU DATA. Rehabilitasi S1 hanya dapat dipertahankan bila sumber material diketahui. Tanpa data, laporkan dua varian (0 dan tingkat historis).

**S2:** penanaman didanai kas LPHD membayar seluruh Rp 14 juta/ha, termasuk upah. HOK-nya dipisah (`HOK Penanaman Didanai Kas`), sehingga upahnya tidak dihitung dua kali dengan penanaman non-karbon.

**Catatan B (dari A1, tidak diubah):** bila `Penambahan Luas Penanaman` dibatasi luas nonhutan atau target RKPS, dana penanaman tetap dibelanjakan walaupun luasnya terpotong. Ini perlu diuji (U11).

---

## 4. KUPS

**Mekanisme usaha (K7):**
- `Modal Usaha KUPS` (stok) = akumulasi laba ditahan × porsi reinvestasi − penggunaan untuk reaktivasi.
- `Laba KUPS Ditahan` = surplus − bagian anggota (A1, dari data Status KUPS Okt 2026 dan MR1). Ini aliran ekonomi yang benar-benar dihasilkan model.
- Penggantian KUPS yang tidak aktif dibatasi modal. Pembentukan baru dari kas LPHD (S2, atau S1 bila ada kas non-karbon).
- KUPS tidak mati otomatis dan tidak bertambah otomatis.

**Konsekuensi analitis per KUPS aktif** (dari persamaan, bukan simulasi):
- Surplus = 0,42 × Rp 6,647 juta = Rp 2,79 juta/th.
- Laba ditahan = 73,7 % × 2,79 juta = Rp 2,06 juta/th.
- Kapasitas reaktivasi = porsi reinvestasi × 2,06 juta / biaya reaktivasi.

| Porsi reinvestasi | Biaya reaktivasi | Kapasitas reaktivasi | Bandingkan laju tidak aktif 0,05/th | Arah KUPS S1 |
|---|---|---|---|---|
| 0,5 | Rp 50 juta | 0,021/th | < 0,05 | turun ±2,9 %/th |
| 1,0 | Rp 50 juta | 0,041/th | < 0,05 | turun ±0,9 %/th |
| 0,5 | Rp 12,5 juta | 0,082/th | > 0,05 | stabil |

Arah KUPS S1 sangat bergantung pada biaya reaktivasi (D) dan porsi reinvestasi (D). Kedua parameter **hanya dapat dibenarkan lewat sensitivitas** sampai ada data biaya reaktivasi.

**Sumber yang belum selaras (D):** komentar File A menyebut tidak ada pembentukan KUPS pada 2024–2025, sedangkan model memakai +15 (2024) dan +5 (2025) dari MR1. Perlu konfirmasi peneliti.

---

## 5. Kelembagaan LPHD

- LPHD aktif di kedua skenario (`Switch PS` = 1). Kebutuhan operasional Rp 1,25 miliar/th tetap dihitung.
- **Kapasitas** (stok, awal 0,5) naik bila ada salah satu dari: belanja penguatan kelembagaan (kas mana pun), pendampingan non-tunai, atau pembelajaran (laju × intensitas perlindungan).
- **Default:** semua sumber non-karbon 0 dan pembelajaran 0. Akibatnya kapasitas S1 tetap 0,5 dan rasio realisasi tetap 0,625. Ini **bukan peningkatan otomatis**.
- Pada S2, kapasitas naik hanya bila kas karbon dibelanjakan untuk kelembagaan.
- `Faktor Penguatan Kelembagaan` juga menurunkan laju tidak aktif KUPS (maksimal 50 %). Pendampingan non-karbon di S1 karena itu ikut memperbaiki ketahanan KUPS.

---

## 6. Pendapatan rumah tangga: hanya pembayaran yang dimodelkan

| Masuk pendapatan RT (`Pendapatan Program per RT Bergantung`) | Tidak masuk |
|---|---|
| Upah patroli dari pembiayaan awal 2024–2025 (Rp 130.000/HOK). **Asumsi:** peserta dibayar; perlu konfirmasi | Nilai tenaga sukarela patroli dan penanaman |
| Upah patroli dari kas LPHD | Nilai logistik non-tunai |
| Upah penanaman didanai kas; upah penanaman non-karbon **hanya** bila `Porsi Tenaga Penanaman Non Karbon Dibayar` > 0 | `Biaya Pengelolaan PS Non Karbon` (indikator biaya) |
| Upah pengendalian kebakaran dari kas | Dana kolektif LPHD yang belum dibelanjakan |
| Tambahan pendapatan KUPS di atas 2024 (bagian surplus untuk anggota) | Omzet KUPS |

Kehilangan pendapatan akibat pembatasan akses tetap dikurangkan (asumsi D, pengali 0–3,24). Dengan patroli reguler, kehilangan akses kini juga muncul di S1. Ini konsisten: pembatasan akses berasal dari perlindungan, apa pun sumber dananya.

---

## 7. Nilai awal 2024 dan data historis 2023

- **`Respons Perlindungan Awal`** (K14) memakai 2.160 keikutsertaan 2023 ÷ `INITIAL(Kebutuhan Hari Patroli)` (7.996) = 0,270, lalu dikali rasio penempatan 0,651, menjadi 0,176.
- **Nilai 2024 tidak berubah.** `Switch Dampak Skenario Lahan` = 0 pada 2024, sehingga `Efek Pengelolaan PS Aktif` = 0, deforestasi 2024 = BAU, dan semua stok awal sama. Yang berubah hanya status internal SMOOTHI, yang mulai dari 0,176 (bukan 0,317). Efek 2025 menjadi lebih kecil dan naik mengikuti penyesuaian 3 tahun.
- **Ketidakselarasan yang dibiarkan (dicatat):** `Indeks Intensitas Swadaya 2023` = 0,2251 (1.568/6.966, basis 4 orang/regu) masih dipakai `Efek Patroli Historis 2023 2024`, yang hanya relevan untuk `Koreksi Kontrafaktual Hutan S1` (switch = 0, tidak aktif). Variabel ini tidak memengaruhi hasil, tetapi sebaiknya diberi komentar "tidak aktif; basis berbeda".
- **2023 tidak masuk arus kas.** Batas evaluasi keuangan dimulai 1 Januari 2024.

---

## 8. Konservasi stok dan konsistensi arus kas

| Stok | Aliran masuk | Aliran keluar | Pembatas non-negatif | Status |
|---|---|---|---|---|
| Luas lahan (6 stok + rehabilitasi) | A1 | A1 | A1 (`Check Total Kawasan` ≈ 0) | tidak diubah |
| `Saldo Dana LPHD` | kas karbon + kas non-karbon | `Penggunaan Dana Desa` | belanja ≤ `Dana Desa Tersedia` = saldo/1 th | ✓ |
| `Saldo Dana LPHD dari Karbon` (baru) | kas karbon | penggunaan × porsi karbon | porsi = saldo karbon/saldo ≤ 1 | ✓ invarian: 0 ≤ saldo karbon ≤ saldo |
| `Modal Usaha KUPS` (baru) | laba ditahan × porsi | reaktivasi × biaya | reaktivasi ≤ modal/TIME STEP/biaya | ✓ |
| `Pendanaan Awal Belum Terpulihkan` | pembiayaan awal × status | pemulihan | pemulihan ≤ sisa/TIME STEP | ✓ |
| `Defisit Biaya Bersama Belum Dipulihkan` | biaya > kas | pemulihan | A1 | tidak diubah |
| Stok kredit (REDD/ARR/gambut) | terbit | terjual + kedaluwarsa | A1 | tidak diubah |
| NPV dan PV (baru) | arus × faktor diskonto | – | – | pelaporan |

**Identitas kas yang harus lolos (U15):** setiap saat, `Kas Penjualan Kredit − Biaya Transaksi dan MRV` = `Dana Program PS dari Karbon` + `Dana Mitra dari Karbon` + `Pemulihan Defisit` + `Pemulihan Pendanaan Awal` − `Kekurangan Biaya Bersama Ditanggung Mitra`.

---

## 9. Langkah waktu

- DT 0,0625. Semua titik STEP berada pada tahun bulat. Waktu tunda DELAY FIXED (0,5, 1, 3, 4, dan 5) adalah kelipatan DT.
- Pembatas `/TIME STEP` (modal KUPS, talangan, defisit) adalah pola A1. Hasilnya bergantung pada DT, jadi uji DT 0,03125 wajib (U6).
- `EXP(−laju × (Time − 2026))` bersifat kontinu, sehingga tidak sensitif terhadap DT.
