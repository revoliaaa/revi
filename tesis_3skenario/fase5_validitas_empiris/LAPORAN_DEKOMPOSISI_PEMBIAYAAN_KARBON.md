# Laporan Dekomposisi Pembiayaan Karbon (D0–D3)

**Tanggal:** 4 November 2026

**Data:** `HASIL_EKSPERIMEN_D0_D3.xlsx`. **Grafik:** `GRAFIK_ATRIBUSI_PEMBIAYAAN/G1–G7`.

**Status:**
- Model `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` dibekukan (md5 `639083f9…`; tidak ada persamaan atau variabel baru).
- PySD 3.14.3; **Vensim native: BELUM DIVERIFIKASI NATIVE**.
- NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Referensi S1 berpasangan dipakai di semua konfigurasi S2.
- D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. Selisihnya adalah dekomposisi menurut asumsi model, **bukan identifikasi kausal empiris**.

## 1. Konfigurasi

Semua konfigurasi dibentuk hanya dengan menimpa parameter atau variabel yang sudah ada.

| Kode | Jembatan 2026–2030 | Penjualan kredit | Implementasi |
|---|---|---|---|
| D0 | Tidak | Tidak | S1 |
| D1 | Ya (J1, Rp0,78 M/th), **hibah** | Tidak | S2; `Status Proyek Karbon Aktif` := 0, sehingga tanpa kredit, MRV, maupun penerimaan; talangan dihapus 2031 dan diakui sebagai kerugian/hibah mitra |
| D2 | Ya (J1), talangan dipulihkan dari surplus | Ya | S2-C-J1 Fase 4 |
| D3 | Tidak | Hanya bila layak secara endogen | S2; `Switch Pembiayaan Jembatan Karbon` = 0; aturan MRV sama dengan D2. D3h: + aturan henti MRV prospektif |

**Pemeriksaan sebelum interpretasi:**
- D0 = S1 Fase 4 dan D2 = S2-C-J1 Fase 4 (USD 10/20/35): selisih **0** pada 190 variabel.
- D1 tidak mengandung kredit, biaya MRV, kas penjualan, maupun utang tanpa sumber.
- D3 tidak memaksa kredit terbit.

## 2. Hasil dasar

### 2.1 USD 10

| Indikator | D0 | D1 | D2 | D3 | D1−D0 (pembiayaan awal) | D2−D1 (penjualan sesudah jembatan) | D2−D0 (paket) | D3−D0 |
|---|---|---|---|---|---|---|---|---|
| Deforestasi kumulatif 2025–2086 (ha) | 28.640 | 28.353 | 28.353 | 28.640 | -287 | 0 | -287 | 0 |
| …2025–2030 (ha) | 2.909 | 2.713 | 2.713 | 2.909 | -196 | 0 | -196 | 0 |
| …2031–2086 (ha) | 25.731 | 25.640 | 25.640 | 25.731 | -91 | 0 | -91 | 0 |
| Hutan 2087 (ha) | 82.799 | 82.975 | 82.975 | 82.799 | 176 | 0 | 176 | 0 |
| Manfaat karbon bersih 2087 thd D0 (ribu tCO₂e) | 0,0 | 81,7 | 81,7 | 0,0 | 81,7 | 0,0 | 81,7 | 0,0 |
| Puncak manfaat karbon bersih (ribu tCO₂e) | 0,0 | 127,4 | 127,4 | 0,0 | 127,4 | 0,0 | 127,4 | 0,0 |
| Patroli kas LPHD 2031–2086 (ribu HOK) | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| Pembiayaan jembatan (Rp M) | 0,00 | 3,91 | 3,91 | 0,00 | 3,91 | 0,00 | 3,91 | 0,00 |
| Kas penjualan kredit (Rp M) | 0,00 | 0,00 | 9,94 | 0,00 | 0,00 | 9,94 | 9,94 | 0,00 |
| Biaya MRV, transaksi, pajak, pengganti (Rp M) | 0,00 | 0,00 | 25,70 | 22,77 | 0,00 | 25,70 | 25,70 | 22,77 |
| Pemulihan modal mitra (Rp M) | 0,00 | 0,00 | 4,96 | 0,00 | 0,00 | 4,96 | 4,96 | 0,00 |
| Kerugian mitra diakui/hibah (Rp M) | 0,00 | 3,91 | 0,00 | 0,00 | 3,91 | -3,91 | 0,00 | 0,00 |
| Defisit MRV belum dipulihkan 2087 (Rp M) | 0,00 | 0,00 | 18,95 | 22,77 | 0,00 | 18,95 | 18,95 | 22,77 |
| Arus kas mitra nominal (Rp M) | -1,44 | -5,36 | -21,11 | -24,21 | -3,91 | -15,76 | -19,67 | -22,77 |
| Dana kolektif LPHD (Rp M) | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| Cakupan kebutuhan LPHD 2030–2055 (%) | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| Cakupan kebutuhan LPHD 2060–2086 (%) | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| NPV mitra (Rp M) [SEMENTARA] | -1,31 | -3,89 | -4,13 | -4,79 | -2,58 | -0,24 | -2,82 | -3,48 |
| NPV proyek keseluruhan (Rp M) [SEMENTARA] | -1,31 | -3,89 | -4,13 | -4,79 | -2,58 | -0,24 | -2,82 | -3,48 |
| HOK patroli berupah kumulatif (ribu) | 5,5 | 20,6 | 20,6 | 5,5 | 15,1 | 0,0 | 15,1 | 0,0 |
| FTE berupah 2030–2055 | 0,0 | 0,4 | 0,4 | 0,0 | 0,4 | 0,0 | 0,4 | 0,0 |
| FTE berupah 2060–2086 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| Upah tunai kegiatan PS (Rp M) | 0,83 | 3,09 | 3,09 | 0,83 | 2,26 | 0,00 | 2,26 | 0,00 |
| KUPS aktif 2087 | 5,7 | 5,7 | 5,7 | 5,7 | 0,0 | 0,0 | 0,0 | 0,0 |
| Penerimaan anggota KUPS (Rp M) | 0,76 | 0,76 | 0,76 | 0,76 | 0,00 | 0,00 | 0,00 | 0,00 |
| Pendapatan bersih per RT bergantung (Rp/th) | 41.213.553 | 41.213.283 | 41.213.283 | 41.213.553 | -270 | 0 | -270 | 0 |
| Pendapatan per RT terdampak (Rp/th) | 41.077.220 | 41.019.609 | 41.019.609 | 41.077.220 | -57.610 | 0 | -57.610 | 0 |
| Kehilangan akses agregat (Rp M) | 53,22 | 62,82 | 62,82 | 53,22 | 9,60 | 0,00 | 9,60 | 0,00 |
| Kompensasi B0 (Rp) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### 2.2 USD 20

| Indikator | D0 | D1 | D2 | D3 | D1−D0 (pembiayaan awal) | D2−D1 (penjualan sesudah jembatan) | D2−D0 (paket) | D3−D0 |
|---|---|---|---|---|---|---|---|---|
| Deforestasi kumulatif 2025–2086 (ha) | 28.640 | 28.353 | 28.186 | 28.640 | -287 | -167 | -454 | 0 |
| …2025–2030 (ha) | 2.909 | 2.713 | 2.713 | 2.909 | -196 | 0 | -196 | 0 |
| …2031–2086 (ha) | 25.731 | 25.640 | 25.473 | 25.731 | -91 | -167 | -258 | 0 |
| Hutan 2087 (ha) | 82.799 | 82.975 | 83.112 | 82.799 | 176 | 137 | 313 | 0 |
| Manfaat karbon bersih 2087 thd D0 (ribu tCO₂e) | 0,0 | 81,7 | 137,8 | 0,0 | 81,7 | 56,2 | 137,8 | 0,0 |
| Puncak manfaat karbon bersih (ribu tCO₂e) | 0,0 | 127,4 | 186,4 | 0,0 | 127,4 | 58,9 | 186,4 | 0,0 |
| Patroli kas LPHD 2031–2086 (ribu HOK) | 0,0 | 0,0 | 8,9 | 0,0 | 0,0 | 8,9 | 8,9 | 0,0 |
| Pembiayaan jembatan (Rp M) | 0,00 | 3,91 | 3,91 | 0,00 | 3,91 | 0,00 | 3,91 | 0,00 |
| Kas penjualan kredit (Rp M) | 0,00 | 0,00 | 29,07 | 0,00 | 0,00 | 29,07 | 29,07 | 0,00 |
| Biaya MRV, transaksi, pajak, pengganti (Rp M) | 0,00 | 0,00 | 27,55 | 22,77 | 0,00 | 27,55 | 27,55 | 22,77 |
| Pemulihan modal mitra (Rp M) | 0,00 | 0,00 | 5,57 | 0,00 | 0,00 | 5,57 | 5,57 | 0,00 |
| Kerugian mitra diakui/hibah (Rp M) | 0,00 | 3,91 | 0,00 | 0,00 | 3,91 | -3,91 | 0,00 | 0,00 |
| Defisit MRV belum dipulihkan 2087 (Rp M) | 0,00 | 0,00 | 15,20 | 22,77 | 0,00 | 15,20 | 15,20 | 22,77 |
| Arus kas mitra nominal (Rp M) | -1,44 | -5,36 | -11,52 | -24,21 | -3,91 | -6,16 | -10,08 | -22,77 |
| Dana kolektif LPHD (Rp M) | 0,00 | 0,00 | 7,69 | 0,00 | 0,00 | 7,69 | 7,69 | 0,00 |
| Cakupan kebutuhan LPHD 2030–2055 (%) | 0,0 | 0,0 | 5,2 | 0,0 | 0,0 | 5,2 | 5,2 | 0,0 |
| Cakupan kebutuhan LPHD 2060–2086 (%) | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| NPV mitra (Rp M) [SEMENTARA] | -1,31 | -3,89 | -1,58 | -4,79 | -2,58 | 2,31 | -0,27 | -3,48 |
| NPV proyek keseluruhan (Rp M) [SEMENTARA] | -1,31 | -3,89 | 0,44 | -4,79 | -2,58 | 4,33 | 1,75 | -3,48 |
| HOK patroli berupah kumulatif (ribu) | 5,5 | 20,6 | 29,5 | 5,5 | 15,1 | 8,9 | 23,9 | 0,0 |
| FTE berupah 2030–2055 | 0,0 | 0,4 | 2,7 | 0,0 | 0,4 | 2,3 | 2,7 | 0,0 |
| FTE berupah 2060–2086 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| Upah tunai kegiatan PS (Rp M) | 0,83 | 3,09 | 5,49 | 0,83 | 2,26 | 2,40 | 4,65 | 0,00 |
| KUPS aktif 2087 | 5,7 | 5,7 | 6,1 | 5,7 | 0,0 | 0,3 | 0,3 | 0,0 |
| Penerimaan anggota KUPS (Rp M) | 0,76 | 0,76 | 0,81 | 0,76 | 0,00 | 0,05 | 0,05 | 0,00 |
| Pendapatan bersih per RT bergantung (Rp/th) | 41.213.553 | 41.213.283 | 41.195.644 | 41.213.553 | -270 | -17.639 | -17.909 | 0 |
| Pendapatan per RT terdampak (Rp/th) | 41.077.220 | 41.019.609 | 40.951.998 | 41.077.220 | -57.610 | -67.612 | -125.222 | 0 |
| Kehilangan akses agregat (Rp M) | 53,22 | 62,82 | 69,54 | 53,22 | 9,60 | 6,72 | 16,32 | 0,00 |
| Kompensasi B0 (Rp) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### 2.3 USD 35

| Indikator | D0 | D1 | D2 | D3 | D1−D0 (pembiayaan awal) | D2−D1 (penjualan sesudah jembatan) | D2−D0 (paket) | D3−D0 |
|---|---|---|---|---|---|---|---|---|
| Deforestasi kumulatif 2025–2086 (ha) | 28.640 | 28.353 | 23.686 | 28.640 | -287 | -4.667 | -4.954 | 0 |
| …2025–2030 (ha) | 2.909 | 2.713 | 2.713 | 2.909 | -196 | 0 | -196 | 0 |
| …2031–2086 (ha) | 25.731 | 25.640 | 20.973 | 25.731 | -91 | -4.667 | -4.758 | 0 |
| Hutan 2087 (ha) | 82.799 | 82.975 | 87.641 | 82.799 | 176 | 4.666 | 4.842 | 0 |
| Manfaat karbon bersih 2087 thd D0 (ribu tCO₂e) | 0,0 | 81,7 | 1.675,8 | 0,0 | 81,7 | 1.594,2 | 1.675,8 | 0,0 |
| Puncak manfaat karbon bersih (ribu tCO₂e) | 0,0 | 127,4 | 1.678,4 | 0,0 | 127,4 | 1.551,0 | 1.678,4 | 0,0 |
| Patroli kas LPHD 2031–2086 (ribu HOK) | 0,0 | 0,0 | 236,7 | 0,0 | 0,0 | 236,7 | 236,7 | 0,0 |
| Pembiayaan jembatan (Rp M) | 0,00 | 3,91 | 3,91 | 0,00 | 3,91 | 0,00 | 3,91 | 0,00 |
| Kas penjualan kredit (Rp M) | 0,00 | 0,00 | 408,71 | 0,00 | 0,00 | 408,71 | 408,71 | 0,00 |
| Biaya MRV, transaksi, pajak, pengganti (Rp M) | 0,00 | 0,00 | 47,58 | 22,77 | 0,00 | 47,58 | 47,58 | 22,77 |
| Pemulihan modal mitra (Rp M) | 0,00 | 0,00 | 5,50 | 0,00 | 0,00 | 5,50 | 5,50 | 0,00 |
| Kerugian mitra diakui/hibah (Rp M) | 0,00 | 3,91 | 0,00 | 0,00 | 3,91 | -3,91 | 0,00 | 0,00 |
| Defisit MRV belum dipulihkan 2087 (Rp M) | 0,00 | 0,00 | 0,00 | 22,77 | 0,00 | 0,00 | 0,00 | 22,77 |
| Arus kas mitra nominal (Rp M) | -1,44 | -5,36 | 141,45 | -24,21 | -3,91 | 146,80 | 142,89 | -22,77 |
| Dana kolektif LPHD (Rp M) | 0,00 | 0,00 | 214,33 | 0,00 | 0,00 | 214,33 | 214,33 | 0,00 |
| Cakupan kebutuhan LPHD 2030–2055 (%) | 0,0 | 0,0 | 38,1 | 0,0 | 0,0 | 38,1 | 38,1 | 0,0 |
| Cakupan kebutuhan LPHD 2060–2086 (%) | 0,0 | 0,0 | 90,5 | 0,0 | 0,0 | 90,5 | 90,5 | 0,0 |
| NPV mitra (Rp M) [SEMENTARA] | -1,31 | -3,89 | 5,35 | -4,79 | -2,58 | 9,24 | 6,66 | -3,48 |
| NPV proyek keseluruhan (Rp M) [SEMENTARA] | -1,31 | -3,89 | 17,05 | -4,79 | -2,58 | 20,94 | 18,36 | -3,48 |
| HOK patroli berupah kumulatif (ribu) | 5,5 | 20,6 | 257,3 | 5,5 | 15,1 | 236,7 | 251,8 | 0,0 |
| FTE berupah 2030–2055 | 0,0 | 0,4 | 17,4 | 0,0 | 0,4 | 17,0 | 17,4 | 0,0 |
| FTE berupah 2060–2086 | 0,0 | 0,0 | 39,5 | 0,0 | 0,0 | 39,5 | 39,5 | 0,0 |
| Upah tunai kegiatan PS (Rp M) | 0,83 | 3,09 | 67,82 | 0,83 | 2,26 | 64,73 | 66,99 | 0,00 |
| KUPS aktif 2087 | 5,7 | 5,7 | 50,4 | 5,7 | 0,0 | 44,7 | 44,7 | 0,0 |
| Penerimaan anggota KUPS (Rp M) | 0,76 | 0,76 | 2,28 | 0,76 | 0,00 | 1,53 | 1,53 | 0,00 |
| Pendapatan bersih per RT bergantung (Rp/th) | 41.213.553 | 41.213.283 | 41.080.609 | 41.213.553 | -270 | -132.674 | -132.944 | 0 |
| Pendapatan per RT terdampak (Rp/th) | 41.077.220 | 41.019.609 | 40.580.341 | 41.077.220 | -57.610 | -439.268 | -496.878 | 0 |
| Kehilangan akses agregat (Rp M) | 53,22 | 62,82 | 307,21 | 53,22 | 9,60 | 244,40 | 254,00 | 0,00 |
| Kompensasi B0 (Rp) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Identitas aritmetis D2 − D0 = (D1 − D0) + (D2 − D1) berlaku untuk semua indikator dan variasi (selisih maks 6·10⁻⁵).

## 3. Atribusi tambahan perlindungan (semua variasi)

| Variasi | Harga | Deforestasi dihindari D2−D0 (ha) | Dari jembatan D1−D0 (ha) | Dari penjualan D2−D1 (ha) | Porsi jembatan | Porsi penjualan pasca-2030 | Δ FTE 2060–2086 | Arus kas mitra D2−D1 (Rp M) | NPV mitra D2−D1 (Rp M) | Dana LPHD D2 (Rp M) | D3: kredit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dasar | USD 10 | 287 | 287 | 0 | 100,0 % | 0,0 % | 0,0 | -15,76 | -0,24 | 0,00 | 0 |
| dasar | USD 20 | 454 | 287 | 167 | 63,2 % | 64,7 % | 0,0 | -6,16 | 2,31 | 7,69 | 0 |
| dasar | USD 35 | 4.954 | 287 | 4.667 | 5,8 % | 98,1 % | 39,5 | 146,80 | 9,24 | 214,33 | 0 |
| JP | USD 10 | 686 | 620 | 66 | 90,4 % | 25,0 % | 0,0 | -8,67 | 2,90 | 3,03 | 0 |
| JP | USD 20 | 1.338 | 620 | 718 | 46,4 % | 78,5 % | 0,0 | 18,99 | 8,08 | 32,42 | 0 |
| JP | USD 35 | 7.487 | 620 | 6.867 | 8,3 % | 97,2 % | 48,1 | 242,17 | 22,10 | 350,60 | 0 |
| durasi 3 | USD 10 | 172 | 172 | 0 | 100,0 % | 0,0 % | 0,0 | -18,60 | -1,34 | 0,00 | 0 |
| durasi 3 | USD 20 | 218 | 172 | 46 | 78,7 % | 73,6 % | 0,0 | -13,67 | 0,57 | 2,16 | 0 |
| durasi 3 | USD 35 | 1.663 | 172 | 1.491 | 10,3 % | 98,9 % | 9,6 | 47,16 | 4,65 | 67,21 | 0 |
| durasi 8 | USD 10 | 476 | 460 | 16 | 96,7 % | 5,6 % | 0,0 | -11,63 | 0,93 | 0,72 | 0 |
| durasi 8 | USD 20 | 857 | 460 | 396 | 53,7 % | 60,0 % | 0,0 | 6,38 | 4,34 | 17,98 | 0 |
| durasi 8 | USD 35 | 6.645 | 460 | 6.185 | 6,9 % | 95,9 % | 49,2 | 209,78 | 14,18 | 305,28 | 0 |
| efektivitas 0,2 | USD 10 | 154 | 154 | 0 | 100,0 % | 0,0 % | 0,0 | -19,02 | -1,73 | 0,00 | 0 |
| efektivitas 0,2 | USD 20 | 154 | 154 | 1 | 99,7 % | 1,1 % | 0,0 | -15,13 | 0,06 | 0,05 | 0 |
| efektivitas 0,2 | USD 35 | 225 | 154 | 71 | 68,4 % | 59,7 % | 0,0 | -7,46 | 2,05 | 6,31 | 0 |
| efektivitas 0,6 | USD 10 | 588 | 471 | 118 | 80,0 % | 43,6 % | 0,0 | -11,16 | 1,30 | 3,26 | 0 |
| efektivitas 0,6 | USD 20 | 4.706 | 471 | 4.235 | 10,0 % | 96,5 % | 16,7 | 79,43 | 7,39 | 113,27 | 0 |
| efektivitas 0,6 | USD 35 | 12.056 | 471 | 11.586 | 3,9 % | 98,7 % | 71,6 | 387,87 | 25,10 | 575,93 | 0 |
| biaya patroli 150.000 | USD 10 | 660 | 498 | 161 | 75,5 % | 50,5 % | 0,0 | -10,26 | 1,55 | 4,23 | 0 |
| biaya patroli 150.000 | USD 20 | 6.071 | 498 | 5.573 | 8,2 % | 97,2 % | 30,3 | 103,21 | 8,60 | 148,94 | 0 |
| biaya patroli 150.000 | USD 35 | 7.449 | 498 | 6.951 | 6,7 % | 97,8 % | 48,8 | 240,23 | 19,61 | 354,47 | 0 |
| biaya patroli 300.000 | USD 10 | 249 | 249 | 0 | 100,0 % | 0,0 % | 0,0 | -16,70 | -0,67 | 0,00 | 0 |
| biaya patroli 300.000 | USD 20 | 332 | 249 | 83 | 74,9 % | 51,4 % | 0,0 | -9,79 | 1,62 | 4,46 | 0 |
| biaya patroli 300.000 | USD 35 | 1.480 | 249 | 1.232 | 16,8 % | 94,0 % | 5,6 | 44,63 | 6,19 | 62,23 | 0 |
| akses 0 | USD 10 | 287 | 287 | 0 | 100,0 % | 0,0 % | 0,0 | -15,76 | -0,24 | 0,00 | 0 |
| akses 0 | USD 20 | 454 | 287 | 167 | 63,2 % | 64,7 % | 0,0 | -6,16 | 2,31 | 7,69 | 0 |
| akses 0 | USD 35 | 4.954 | 287 | 4.667 | 5,8 % | 98,1 % | 39,5 | 146,80 | 9,24 | 214,33 | 0 |
| akses 1,5 | USD 10 | 287 | 287 | 0 | 100,0 % | 0,0 % | 0,0 | -15,76 | -0,24 | 0,00 | 0 |
| akses 1,5 | USD 20 | 454 | 287 | 167 | 63,2 % | 64,7 % | 0,0 | -6,16 | 2,31 | 7,69 | 0 |
| akses 1,5 | USD 35 | 4.954 | 287 | 4.667 | 5,8 % | 98,1 % | 39,5 | 146,80 | 9,24 | 214,33 | 0 |

## 4. Jawaban pertanyaan analitis

1. **Apakah tambahan perlindungan pada USD 10–20 sebagian besar disebabkan talangan awal?**
   - **Ya, menurut model.** Pada konfigurasi dasar, pembiayaan awal menyumbang **100 %** (USD 10) dan **63 %** (USD 20) deforestasi dihindari.
   - Pada USD 10, penjualan karbon tidak menambah perlindungan sama sekali, karena kas karbon tidak pernah sampai ke LPHD.
   - Porsi jembatan naik bila efektivitas rendah (0,2: ±100 % pada USD 10–20) atau biaya per HOK tinggi (Rp300.000: 75–100 %).
   - Porsi jembatan turun bila efektivitas tinggi (0,6: 10 % pada USD 20) atau biaya per HOK rendah (Rp150.000: 8 % pada USD 20).
2. **Apakah penerimaan karbon sesudah jembatan benar-benar mempertahankan tambahan patroli?**
   - **USD 20:** hanya sementara. Patroli dari kas LPHD 2031–2086 hanya 8,9 ribu HOK dan habis sebelum ±2055. Tambahan kerja berupah 2060–2086 = 0.
   - **USD 35:** ya, 236,7 ribu HOK, dan FTE berupah 2060–2086 +39,5.
3. **Apakah pada USD 35 pendapatan karbon menghasilkan penguatan yang bertahan sesudah jembatan?**
   - **Ya:** 94 % deforestasi dihindari berasal dari mekanisme penjualan, dan 98 % dari deforestasi dihindari pasca-2030.
   - LPHD menerima Rp214 M; cakupan kebutuhan 2060–2086 sebesar 90 %; KUPS 2087 +44,7.
   - **Syarat:** pembiayaan awal tetap diperlukan untuk memulai siklus (lihat butir 4).
4. **Apakah tanpa jembatan muncul *bootstrap problem*?**
   - **Ya, secara struktural.** D3 tidak menghasilkan kredit sama sekali pada **semua** harga dan variasi, termasuk efektivitas 0,6 dan biaya Rp150.000/HOK. Kredit konservatif hanya mengakui mitigasi di atas S1, dan tanpa dana tambahan tidak ada kegiatan di atas S1.
   - Bila MRV tetap dijalankan, mitra menanggung Rp22,8 M tanpa penerimaan. Dengan aturan henti MRV (D3h), kerugian itu Rp2,9 M.
5. **Apakah kesimpulan keuangan dan kesejahteraan berubah bila efek talangan dipisahkan?**
   - **Keuangan.** Pada USD 10, mekanisme penjualan memperburuk posisi mitra dibanding hibah murni: arus kas nominal −Rp15,8 M (MRV tanpa penerimaan cukup). Dampak fisiknya nol.
   - Pada USD 20, NPV mitra naik +Rp2,3 M [SEMENTARA] karena penerimaan datang lebih awal, tetapi arus kas nominal turun −Rp6,2 M karena defisit MRV sesudah 2051.
   - Pada USD 35, posisi mitra naik +Rp146,8 M nominal.
   - **Kesejahteraan.** Penurunan pendapatan RT terdampak terbagi ke dua sumber:
     - pembiayaan awal: −57.610 Rp/th;
     - penjualan: −67.612 Rp/th pada USD 20 dan −439.268 pada USD 35.

     Keduanya berasal dari tambahan perlindungan yang sama-sama memperbesar kehilangan akses. Bila pengali akses 0, keduanya positif (tabel di bawah).

| Variasi | Harga | Δ pendapatan RT terdampak D1−D0 (Rp/th) | Δ D2−D0 (Rp/th) |
|---|---|---|---|
| akses 1 (dasar) | USD 10 | -57.610 | -57.610 |
| akses 1 (dasar) | USD 20 | -57.610 | -125.222 |
| akses 1 (dasar) | USD 35 | -57.610 | -496.878 |
| akses 0 | USD 10 | 38.341 | 38.341 |
| akses 0 | USD 20 | 38.341 | 54.352 |
| akses 0 | USD 35 | 38.341 | 112.117 |
| akses 1,5 | USD 10 | -105.586 | -105.586 |
| akses 1,5 | USD 20 | -105.586 | -215.009 |
| akses 1,5 | USD 35 | -105.586 | -801.376 |

## 5. Keterbatasan khusus

- D1 memperlakukan jembatan sebagai hibah. Pemulihan tidak mungkin tanpa penerimaan, sehingga talangan dicatat sebagai kerugian mitra. Ini pilihan akuntansi diagnostik, bukan klaim tentang kontrak.
- D1 dibentuk dengan menimpa variabel status proyek, bukan dengan switch baru, agar model tetap dibekukan. Di Vensim native, setara dengan menjadikan variabel itu konstanta 0 pada salinan run; **belum diverifikasi native**.
- D3 memakai aturan MRV yang sama dengan D2 (MRV sejak 2024). Varian D3h menunjukkan sensitivitasnya terhadap aturan henti.
