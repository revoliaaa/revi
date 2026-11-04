# 05 — Kelembagaan dan Sosial-Ekonomi

Data:
- `socioeconomic_2030_2055.csv`: rerata 2030–2055.
- `access_multiplier_sweep.csv` dan `access_multiplier_zero_crossing.csv`: uji pengali akses.

## Kerja

| Rerata 2030–2055 | S1 | S2 | S3 | USD 10 | USD 20 | USD 35 |
|---|---|---|---|---|---|---|
| HOK total/th | 0 | 4.066 | 4.066 | 5.191 | 9.852 | 19.343 |
| — patroli swadaya (tak berbayar) | 0 | 2.355 | 2.355 | 2.355 | 2.355 | 2.355 |
| — patroli berbayar | 0 | 0 | 0 | 740 | 3.107 | 5.407 |
| — penanaman | 0 | 1.711 | 1.711 | 1.739 | 2.895 | 6.791 |
| — pengendalian kebakaran | 0 | 0 | 0 | 356 | 1.496 | 4.790 |
| FTE = HOK/300 (**bukan jumlah orang**) | 0 | 13,6 | 13,6 | 17,3 | 32,8 | 64,5 |
| Upah didanai karbon (Rp juta/th) | 0 | 0 | 0 | 145,5 | 723,8 | 1.864,0 |
| "Upah Kegiatan PS" di naskah (Rp juta/th) | – | 181,4 | – | 326,9 | 905,2 | – |

- "Upah Kegiatan PS" (Rp 327 dan 905 juta di naskah) **mencakup nilai ekonomi patroli dan penanaman swadaya** (`Manfaat Ekonomi Patroli/Penanaman`). Karena itu S2 tetap bernilai 181 juta walaupun tanpa dana.
- Upah yang benar-benar dibayar dari dana karbon adalah 145,5 dan 723,8 juta.
- **Status: perlu klarifikasi.** Bedakan kerja dibayar dari kerja swadaya. Dalam S1–S3 kerja PS seluruhnya swadaya.

## KUPS

| Rerata 2030–2055 | S1 | S2–S3 | USD 10 | USD 20 | USD 35 |
|---|---|---|---|---|---|
| KUPS aktif (rerata sampel tahunan; konvensi naskah) | 6,7 | 33,4 | 33,4 | 33,4 | 64,2 |
| KUPS aktif (rerata integral) | 6,5 | 33,4 | 33,4 | 33,4 | 65,2 |
| Anggota KUPS | 121 | 508 | 508 | 508 | 985 |
| Omzet KUPS (Rp juta/th) | – | 135,0 | 148,6 | 190,2 | – |
| Penerimaan anggota total (Rp juta/th) | 4,8 | 24,5 | 27,0 | 34,6 | 89,9 |

- **Omzet KUPS ≠ penerimaan anggota.** Penerimaan anggota adalah surplus yang dibagikan.
- **Data awal belum bersumber:** 15 KUPS / 277 anggota (2023) [PERLU DIISI sumber]. Gambar 2 naskah menulis "status KUPS 2026", jadi perlu diseragamkan.
- **Konvensi rerata tidak seragam:** jumlah KUPS memakai sampel tahunan, variabel lain memakai integral. Selisihnya kecil (6,7 vs 6,5 pada S1).
- **S1 mengasumsikan KUPS meluruh** dari 15 menjadi 0,7 unit pada 2087. Ini asumsi desain S1 (CONDITIONAL).

## Rumah tangga

**Proksi 5.328 — temuan K3.**
- Di model, 5.328 adalah `Masyarakat Bergantung pada Hutan Awal`, yaitu **estimasi orang bergantung hutan, kelas bukti D**. Nilainya diperoleh dari 2.144 pemegang garapan + 25,9 % sisa pekerja SDA, lalu diskalakan dari 20 ke 25 HD. Rentang uji di dokumentasi: 2.144–19.038.
- Variabel `Pekerja Berbasis SDA` sendiri bernilai **24.694 orang pada 2024**.
- Model mengasumsikan `Rumah Tangga per Pekerja Bergantung` = 1, sehingga 5.328 orang diperlakukan sebagai 5.328 RT.
- **Implikasi:**
  - jumlah RT bergantung bisa terlalu rendah bila satu RT punya beberapa pekerja, atau terlalu tinggi bila tidak semua orang bergantung adalah kepala RT;
  - rerata per RT dan agregat kehilangan akses ikut bergeser;
  - naskah harus menyebutnya "orang bergantung hutan (estimasi)", **bukan** "pekerja berbasis SDA".
- RT bergantung tumbuh 1,66 %/th menjadi rerata 7.462 (2030–2055). RT terdampak akses (garapan, diperlakukan setara RT) rerata 3.003.

**Pendapatan dan kehilangan akses (rerata 2030–2055; harga 2021; asumsi model).**

| | S1 | S2 | S3 | USD 10 | USD 20 | USD 35 |
|---|---|---|---|---|---|---|
| Pendapatan bersih rata-rata RT bergantung (Rp juta/th) | 41,254 | 41,198 | 41,224 | 41,184 | 41,047 | 40,934 |
| Manfaat program per RT (Rp/th) | −208 | 3.616 | 3.616 | 6.315 | 16.331 | 37.280 |
| Kehilangan akses rata-rata per RT bergantung (Rp/th) | 0 | 141.352 | 153.114 | 227.077 | 448.032 | 682.096 |
| Kehilangan per RT pemegang garapan (Rp/th) | 0 | 351.270 | 380.499 | 564.303 | 1.113.393 | 1.695.059 |

**Mekanisme kehilangan akses (dari persamaan).** Kehilangan = pendapatan hutan per RT × 0,25 (porsi pemicu deforestasi; asumsi D) × pengurangan relatif deforestasi × pengali (1).
- Kehilangan dikaitkan dengan **penurunan deforestasi**, bukan langsung dengan jumlah patroli.
- Model tidak membedakan pemanfaatan legal dan ilegal.
- Peningkatan patroli **tidak boleh** ditafsirkan otomatis membatasi pemanfaatan yang sah.

**Uji pengali akses (rerun PySD).** Selisih pendapatan rata-rata RT (Rp/th):

| Perbandingan | Pengali 0 | Pengali 1 | Titik nol pengali |
|---|---|---|---|
| S2 − S1 | +85.687 | −55.665 | 0,61 |
| S3 − S2 | +37.363 | +25.602 | 3,18 |
| S4 USD 10 − S3 | +34.403 | −39.560 | **0,47** |
| S4 USD 20 − S3 | +118.630 | −176.288 | **0,40** |

Pengali dokumentasi: A0 = 0; A1 = 0,27; A2 = 1; A3 = 3,24. Tanda dampak terhadap pendapatan RT **berbalik di dalam rentang dokumentasi**. Karena itu tanda tersebut **tidak dapat disimpulkan** dari model ini dan bergantung pada asumsi.

## Pembedaan wajib

- **Dana kolektif LPHD ≠ pendapatan rumah tangga.** Hanya bagian yang menjadi upah, surplus KUPS, atau kompensasi yang masuk ke RT.
- **FTE ≠ orang.**
- **Omzet KUPS ≠ penerimaan anggota.**
- **Kehilangan akses** adalah asumsi eksploratif, bukan dampak kesejahteraan yang teramati.
- **Audit ini tidak membuat klaim tentang kemiskinan atau ketimpangan.**
