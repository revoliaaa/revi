# Laporan Verifikasi Vensim–PySD dan Sensitivitas: Model FINAL 3 SKENARIO

Laporan ini memisahkan **verifikasi komputasi**, yaitu apakah model dihitung dengan benar sesuai persamaannya, dari **validasi perilaku**, yaitu apakah perilaku model cukup mewakili sistem nyata.

## A. Verifikasi komputasi

### A1. Vensim native vs PySD (model revisi)

**Status: BELUM DILAKUKAN.** Perangkat Vensim tidak tersedia di lingkungan komputasi ini, sehingga perbandingan untuk model revisi belum ada.
Hasil lama (99,87–100 % identik) berlaku untuk model empat skenario dan **tidak** dianggap sebagai verifikasi model revisi.

Langkah yang perlu dijalankan peneliti:
1. Buka `DKP_25HD_FINAL_3SKENARIO.mdl` di Vensim, lalu jalankan *Units Check* dan *Check Model*.
2. Jalankan 7 run: `S1`, `S2`, `S3_USD6`, `S3_USD10`, `S3_USD15`, `S3_USD20`, `S3_USD35`. Ubah `Skenario Kebijakan` (1/2/3) dan `Harga Karbon`.
3. Ekspor setiap run ke `.tab`. Jangan membukanya lewat Excel berlocale Indonesia.
4. Jalankan `python bandingkan_vensim_pysd.py DKP_25HD_FINAL_3SKENARIO.mdl S1.tab S2.tab S3_USD10.tab ...`. Kriteria cocok: selisih relatif ≤ 10⁻⁵ atau absolut ≤ 10⁻⁶.

### A2. Rekonstruksi model terhadap hasil resmi FINAL A1

Berkas `.mdl` asli tidak ada di paket, jadi model direkonstruksi dari register variabel. Hasilnya diuji terhadap register data resmi:

| Uji | Nilai dibandingkan | Berbeda > 0,01 % |
|---|---|---|
| A1 S1–S4 USD6–35 (8 skenario) | 17.472 | 0 |
| Eksperimen alokasi (7 run B0–R2) | 15.596 | 0 |
| NPV, harga impas (6,83 / 7,40), cakupan 100 % (USD 28,04), S2−S1 (1.720 ha), S4−S3 (535 / 3.588 ha) | – | 0 |

Model revisi juga dibaca PySD dengan opsi pemisahan View; ke-16 View terbaca dan hasilnya identik dengan versi tanpa pemisahan.

### A3. Uji struktur, penempatan patroli, kondisi ekstrem, dan langkah waktu

| Uji | Status | Rincian |
|---|---|---|
| Neraca luas & karbon S1 | PASS | |Check Total Kawasan| maks 1.60e-10 ha; |Check Konservasi Karbon| maks 3.59e-08; Total Kawasan 124941.00 ha konstan |
| Neraca luas & karbon S2 | PASS | |Check Total Kawasan| maks 1.89e-10 ha; |Check Konservasi Karbon| maks 7.64e-08; Total Kawasan 124941.00 ha konstan |
| Neraca luas & karbon S3-10 | PASS | |Check Total Kawasan| maks 1.75e-10 ha; |Check Konservasi Karbon| maks 5.87e-08; Total Kawasan 124941.00 ha konstan |
| Neraca luas & karbon S3-35 | PASS | |Check Total Kawasan| maks 1.16e-10 ha; |Check Konservasi Karbon| maks 3.59e-08; Total Kawasan 124941.00 ha konstan |
| Patroli 2024-2025 hanya dari pembiayaan awal (S2) | PASS | HOK 2024 2533.0; 2025 3011.0; swadaya maks 0.0; belanja karbon patroli 2024-25 0 Rp; patroli pembiayaan awal sesudah 2025 0.0 |
| Nilai pembiayaan awal = HOK x biaya (S2) | PASS | 1,441,440,000 Rp = (2.533 + 3.011) x Rp 260.000 |
| Patroli 2024-2025 hanya dari pembiayaan awal (S3-10) | PASS | HOK 2024 2533.0; 2025 3011.0; swadaya maks 0.0; belanja karbon patroli 2024-25 0 Rp; patroli pembiayaan awal sesudah 2025 0.0 |
| Nilai pembiayaan awal = HOK x biaya (S3-10) | PASS | 1,441,440,000 Rp = (2.533 + 3.011) x Rp 260.000 |
| Patroli 2024-2025 hanya dari pembiayaan awal (S3-35) | PASS | HOK 2024 2533.0; 2025 3011.0; swadaya maks 0.0; belanja karbon patroli 2024-25 0 Rp; patroli pembiayaan awal sesudah 2025 0.0 |
| Nilai pembiayaan awal = HOK x biaya (S3-35) | PASS | 1,441,440,000 Rp = (2.533 + 3.011) x Rp 260.000 |
| S1 tanpa patroli & tanpa pembiayaan awal | PASS | semua 0 |
| S2 tanpa penerimaan karbon | PASS | penerimaan kredit & dana LPHD = 0 |
| Ekstrem: patroli 2024-2025 = 0 -> efek patroli S2 hilang | PASS | deforestasi S2 tanpa patroli 29870.4 ha vs S1 29812.3 ha (sisa selisih -58.1 ha = efek penghidupan/KUPS PS) |
| Ekstrem: efektivitas = 0 -> patroli tidak mengubah deforestasi | PASS | S2 efektivitas 0: 29870.367 ha; S2 tanpa patroli: 29870.367 ha |
| Ekstrem: harga karbon 0 -> S3 = S2 (hutan) | PASS | S3 USD0 29686.725 ha vs S2 29686.725 ha; dana LPHD 0 |
| Ekstrem: harga USD500 -> intensitas <= 1, stok >= 0 | PASS | intensitas maks 1.000; hutan min 90408 ha |
| Ekstrem: patroli 10x -> intensitas dibatasi 1 | PASS | intensitas maks 1.000 |
| Monoton: deforestasi tidak naik saat harga naik | PASS | grid USD1-60 |
| Uji langkah waktu DT 0,0625 vs 0,03125 | PASS | selisih relatif maks 0.635 % (5 indikator x 3 skenario) |

Catatan uji ekstrem: tanpa patroli, deforestasi kumulatif S2 sedikit **lebih besar** daripada S1 (+58 ha). Selisih ini bukan galat. Rehabilitasi pada S2 menambah stok hutan, dan deforestasi dihitung proporsional terhadap stok, sehingga hutan yang lebih luas menghasilkan deforestasi absolut yang sedikit lebih besar. Hutan 2087 pada S2 tetap lebih luas daripada S1.

### A4. Uji putus loop (dana karbon → patroli)

| Harga | S3−S2 utuh (ha) | S3−S2 tanpa dana ke patroli (ha) | Kredit utuh (tCO₂e) | Kredit putus (tCO₂e) |
|---|---|---|---|---|
| USD 20 | 139 | −5 | 74.888 | 45.876 |
| USD 35 | 2.243 | −11 | 436.441 | 45.869 |

Seluruh tambahan perlindungan dari karbon bekerja melalui belanja patroli. Kredit yang tersisa saat loop diputus (±45.900 tCO₂e) berasal dari efek patroli pembiayaan awal 2024–2025 terhadap baseline S1.

## B. Validasi perilaku

- **Stok hutan 2019/2024:** MAPE 3,92 %; pembanding linear 8,88 % dan laju konstan 8,43 %. **Aliran kehilangan Hansen 2017–2024:** MAPE 73,3 %.
- Kedua uji itu berasal dari model lama. **Tetap berlaku** untuk model revisi, karena laju BAU, kondisi awal, dan skenario S1 tidak berubah: hasil S1 identik, yaitu hutan 2087 81.890 ha dan deforestasi 29.812 ha.
- Uji perilaku itu tidak dijalankan ulang di sesi ini. Skrip hindcast-nya tidak ada di paket.
- Belum ada data deforestasi pasca-2025 untuk menguji perilaku S2. Penurunan deforestasi 2025 (520 → 458 ha) masih perlu dibandingkan dengan data Hansen 2025 per HD bila tersedia.

## C. Ketidakpastian: Monte Carlo dan PRCC

Desain: hiperkubus Latin, seed 20261101, 13 parameter, n = 3.000 (USD 10) dan 1.500 (USD 20). Spesifikasi sebaran ada di register hasil, lembar 18.
Skrip dan berkas Monte Carlo lama tidak ada di paket, jadi spesifikasi disusun ulang dari rentang ketidakpastian di register variabel.
Sebagai uji kewajaran, spesifikasi ini dijalankan pada model lama (n = 200). Hasilnya mendekati angka MC lama:

| Ukuran (model lama) | MC lama | Spesifikasi baru pada model lama (n = 200) |
|---|---|---|
| Median S2−S1 (ha) | 1.561 | 1.555 |
| S4>S3 pada USD 10 | 92,6 % | 92,0 % |
| Median S4−S3 USD 10 (ha) | 265 | 290 |
| NPV>0 pada USD 10 | 60,9 % | 58,5 % |
| Kebutuhan LPHD tertutup USD 10 | 0 % | 0,0 % |

### Hasil model revisi

| Ukuran | USD 10 | USD 20 |
|---|---|---|
| Frekuensi karbon menambah perlindungan (S3<S2) | 60,7 % | 87,7 % |
| Median S3−S2 (ha) | 7 | 60 |
| P5–P95 S3−S2 (ha) | 0–129 | 0–1.641 |
| NPV>0 | 2,6 % | 38,7 % |
| Median NPV (Rp miliar) | −2,52 | −0,70 |
| Kebutuhan minimum LPHD tertutup | 0,0 % | 0,0 % |
| Median cakupan kebutuhan (%) | 0,3 | 2,2 |
| Pendapatan RT naik (S3>S2) | 12,3 % | 17,9 % |

S2−S1: positif pada 90,3 % tarikan; median 97 ha (P5–P95 −14–300 ha).

**PRCC (empat parameter terkuat):**

- S2−S1: Efektivitas perlindungan penuh +0,96; Waktu penyesuaian efek PS (th) +0,88; Pengali laju regenerasi +0,75; Pengali laju deforestasi BAU +0,37
- S3−S2 USD 20: Efektivitas perlindungan penuh +0,98; Pengali laju deforestasi BAU +0,79; Waktu penyesuaian efek PS (th) +0,67; Proporsi kredit dalam PA +0,58
- NPV USD 20: Efektivitas perlindungan penuh +0,97; Pengali laju deforestasi BAU +0,76; Waktu penyesuaian efek PS (th) +0,75; Pengali biaya monitoring MRV -0,75
- Δ pendapatan RT USD 20: Pengali kehilangan akses -0,76; Efektivitas perlindungan penuh -0,75; Waktu penyesuaian efek PS (th) -0,24; Proporsi kredit dalam PA -0,18

Frekuensi Monte Carlo adalah proporsi ensembel, bukan peluang kejadian.

## D. Sensitivitas satu-per-satu

| Parameter (rendah / tinggi) | S2−S1 (ha) | S3−S2 USD 20 (ha) | S3−S2 USD 35 (ha) | NPV USD 20 (Rp miliar) |
|---|---|---|---|---|
| Efektivitas perlindungan (0,075 / 0,59) | −21 / 235 | 0 / 1.600 | 1 / 12.725 | −3,34 / 5,33 |
| Laju deforestasi BAU (x0,68 / x1,46) | 99 / 152 | 42 / 481 | 256 / 9.131 | −0,95 / 3,15 |
| Biaya MRV (x0,5 / x1,5) | 126 / 126 | 251 / 79 | 3.440 / 1.169 | 1,89 / −0,96 |
| Biaya per hari patroli (Rp195.000 / Rp325.000) | 126 / 126 | 265 / 95 | 6.842 / 613 | 1,36 / −0,09 |
| Kapasitas LPHD awal (0,3 / 0,7) | 126 / 126 | 131 / 144 | 1.899 / 2.465 | 0,59 / 0,46 |
| Proporsi kredit dalam PA (0,541 / 0,782) | 126 / 126 | 74 / 214 | 473 / 5.788 | −0,64 / 1,44 |
| Waktu penyesuaian efek PS (1 / 5 th) | 38 / 214 | 48 / 232 | 1.169 / 2.472 | −1,21 / 1,55 |
| Kehilangan akses (0 / 3,24) | 126 / 126 | 139 / 139 | 2.243 / 2.243 | 0,51 / 0,51 |
| Diskonto (6 % / 14 %) | – | – | – | 0,38 / 0,19 |

## E. Eksperimen alokasi: kekokohan

- **22 kombinasi sensitivitas** (11 varian × USD 10/20): B1 dan R1 tidak pernah lebih buruk daripada B0 (22/22). R2 menambah hutan pada 18/22 kombinasi, tetapi lebih buruk bagi RT terdampak pada sebagian besar kombinasi. B2–B4 lebih buruk bagi hutan pada 18–20/22.
- **Monte Carlo berpasangan** (n = 1.000):
  - B1-10: tidak lebih buruk 100,0 %; dominan lemah 60,7 %; hutan naik 1,1 %; median Δ pendapatan RT terdampak Rp 394
  - R1-10: tidak lebih buruk 100,0 %; dominan lemah 60,7 %; hutan naik 3,3 %; median Δ pendapatan RT terdampak Rp 764
  - R2-10: tidak lebih buruk 56,5 %; dominan lemah 17,2 %; hutan naik 53,2 %; median Δ pendapatan RT terdampak Rp 0
  - B1-20: tidak lebih buruk 100,0 %; dominan lemah 87,4 %; hutan naik 4,8 %; median Δ pendapatan RT terdampak Rp 3.674
  - R1-20: tidak lebih buruk 100,0 %; dominan lemah 87,4 %; hutan naik 10,1 %; median Δ pendapatan RT terdampak Rp 7.382
  - R2-20: tidak lebih buruk 38,2 %; dominan lemah 25,6 %; hutan naik 81,1 %; median Δ pendapatan RT terdampak Rp −2.716
