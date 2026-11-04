# Analisis Ketidakpastian: Monte Carlo Berpasangan dan PRCC

**Tanggal:** 4 November 2026

**Data:** `HASIL_MONTE_CARLO_PRCC_PWD.xlsx`. **Grafik:** `GRAFIK_MONTE_CARLO_DAN_BENEFIT_SHARING/M1–M3`.

**Status verifikasi:**

| Unsur | Status |
|---|---|
| Model | `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (946 variabel); eksperimen alokasi pada `…_v2_ALOKASI.mdl` (964 variabel; satuan 960/960 konsisten; B0 identik dengan v2) |
| Protokol | Referensi S1 berpasangan: lulus pengujian yang telah dilakukan (15/15 konfigurasi gerbang + 1.200/1.200 pasangan MC + 91/91 run alokasi tanpa ketidaksesuaian). Tidak menjamin kesetaraan untuk kombinasi yang belum diuji |
| K7 mode endogen | **GAGAL**; tidak dipakai |
| Vensim native | **BELUM DIVERIFIKASI** |
| NPV | **SEMENTARA** (tanpa biaya pengembangan dan material aktual) |
| Kewajiban *reversal* | Aturan akuntansi model; belum diverifikasi terhadap standar atau kontrak |
| Kredit model | ≠ kredit terverifikasi |

Proporsi ensembel ≠ probabilitas empiris.

## 1. Rancangan

| Unsur | Isi |
|---|---|
| Sampel | Latin Hypercube Sampling, N = 400, seed 20261104 |
| Parameter | 20 parameter; distribusi di lembar 1 |
| Protokol per sampel | Satu run S1 mandiri, lalu S2 mekanisme C pada USD 10, 20, dan 35 dengan tujuh masukan Referensi S1 diambil dari run S1 itu |
| Total | 1.600 run, 1.200 pasangan |

**Parameter yang disampel:**
- keberlanjutan patroli reguler k (0–1);
- efektivitas perlindungan (segitiga 0,2–0,37–0,6);
- laju deforestasi BAU (×0,7–1,3) dan regenerasi (×0,5–1,5);
- biaya patroli total Rp150.000–300.000/HOK (upah Rp150.000 tetap) dan biaya MRV (×0,5–1,5);
- besaran jembatan Rp0,39–1,69 miliar/th (0,5×J1 s.d. JP) dan durasinya (3–8 th);
- jeda penerbitan (2–5 th), jeda pembayaran (0–1 th), dan laju penjualan (0,4–1,0/th);
- pengali kehilangan akses (0–1,5);
- surplus KUPS (×0,7–1,3), porsi reinvestasi (0,25–0,75), dan biaya reaktivasi (Rp12,5–75 juta);
- kapasitas awal LPHD (0,3–0,7) dan pengaruh kapasitas terhadap mutu (0–0,5);
- leakage (0,05–0,2), buffer (0,1–0,2), dan porsi Project Area (0,541–0,903).

Semua rentang adalah asumsi yang dinyatakan (kelas B–D). Proporsi ensembel bergantung pada rentang itu.

**Pemeriksaan pasangan** (lembar 3): 1.200/1.200 pasangan setara.
- Selisih hutan dan emisi Referensi S1 terhadap S1 mandiri = 0.
- Identitas arus kas ≤ 4·10⁻⁶ Rp.
- 0 run gagal.

## 2. Proporsi ensembel

Kriteria ditetapkan sebelum hasil dilihat.

| Kriteria (S2 mekanisme C vs S1 berpasangan) | USD 10 | USD 20 | USD 35 |
|---|---|---|---|
| 1 Tambahan perlindungan hutan S2−S1 (deforestasi dihindari > 0) | 100,0 % | 100,0 % | 100,0 % |
| 2a Manfaat karbon bersih kumulatif 2087 > 0 | 100,0 % | 100,0 % | 100,0 % |
| 2b …dan tidak turun > 10 % dari puncaknya | 0,5 % | 23,8 % | 78,2 % |
| 3a Kas LPHD masih mengalir 2075–2086 (rerata > 0) | 0,5 % | 22,2 % | 74,0 % |
| 3b Cakupan kebutuhan minimum LPHD 2060–2086 ≥ 50 % | 0,2 % | 10,8 % | 57,2 % |
| 4a NPV inkremental proyek > 0 [SEMENTARA] | 13,0 % | 65,8 % | 95,8 % |
| 4b NPV mitra inkremental > 0 [SEMENTARA] | 4,2 % | 46,8 % | 88,8 % |
| 5a Pendapatan bersih RT bergantung NAIK (Δ > 0) | 60,0 % | 47,5 % | 33,8 % |
| 5b Pendapatan bersih RT bergantung TURUN (Δ < 0) | 40,0 % | 52,5 % | 66,2 % |
| 5c Pendapatan RT terdampak NAIK (Δ > 0) | 25,2 % | 19,0 % | 14,5 % |
| 6 KUPS aktif 2087 ≥ 90 % KUPS aktif 2026 (S2) | 15,0 % | 24,8 % | 62,5 % |
| 6b (pembanding) KUPS aktif 2087 ≥ 90 % 2026 pada S1 | 14,5 % | 14,5 % | 14,5 % |
| 7 Kerja berupah tambahan bertahan 2060–2086 (Δ FTE > 0,5) | 1,2 % | 31,8 % | 82,5 % |

## 3. Sebaran hasil

| Indikator | USD 10: median [P5; P95] | USD 20: median [P5; P95] | USD 35: median [P5; P95] |
|---|---|---|---|
| Deforestasi dihindari S2−S1 (ha) | 403 [132; 1.400] | 682 [137; 9.233] | 4.710 [230; 11.381] |
| Δ hutan 2087 (ha) | 252 [87; 946] | 503 [91; 8.311] | 4.648 [162; 10.141] |
| Manfaat karbon bersih 2087 (ribu tCO₂e) | 116,9 [39,5; 424,6] | 212,0 [41,3; 3.048,7] | 1.611,1 [71,1; 3.827,2] |
| Kredit diajukan (ribu tCO₂e) | 94,4 [31,6; 308,8] | 148,6 [33,7; 1.739,1] | 917,3 [53,8; 2.174,2] |
| Debit reversal belum diselesaikan 2087 (ribu tCO₂e) | 1,8 [0,1; 7,8] | 1,5 [0,0; 12,0] | 0,0 [0,0; 5,4] |
| Kas LPHD karbon kumulatif (Rp M) | 0,1 [0,0; 14,1] | 12,5 [0,0; 240,7] | 209,9 [5,1; 557,0] |
| Kas LPHD 2075–2086 (Rp juta/th) | 0 [0; 0] | 0 [0; 4.723] | 4.581 [0; 10.083] |
| Cakupan kebutuhan LPHD 2060–2086 (%) | 0,0 [0,0; 0,0] | 0,0 [0,0; 97,5] | 88,7 [0,0; 178,4] |
| NPV inkremental proyek (Rp M) [SEMENTARA] | -2,88 [-5,44; 2,61] | 2,45 [-3,03; 23,69] | 19,06 [0,35; 60,48] |
| NPV mitra inkremental (Rp M) [SEMENTARA] | -3,03 [-5,44; -0,24] | -0,27 [-3,30; 8,61] | 6,55 [-1,00; 23,44] |
| Defisit MRV ditanggung mitra 2087 (Rp M) | 17,4 [8,8; 26,4] | 10,2 [0,0; 23,5] | 0,0 [0,0; 15,2] |
| Δ FTE berupah 2030–2055 | 1,2 [0,0; 6,8] | 5,0 [0,2; 28,7] | 21,2 [1,9; 61,6] |
| Δ FTE berupah 2060–2086 | 0,0 [0,0; 0,0] | 0,0 [0,0; 40,9] | 38,1 [0,0; 72,0] |
| Δ upah kegiatan PS (Rp juta/th) | 54 [0; 286] | 207 [8; 1.160] | 850 [74; 2.325] |
| Δ penerimaan anggota KUPS (Rp juta/th) | 0,0 [0,0; 2,0] | 1,7 [0,0; 18,6] | 10,0 [0,8; 77,8] |
| KUPS aktif 2087 (S2) | 6,9 [3,0; 33,4] | 9,4 [3,2; 47,9] | 43,9 [4,6; 110,0] |
| KUPS aktif 2087 (S1) | 6,8 [3,0; 33,4] | 6,8 [3,0; 33,4] | 6,8 [3,0; 33,4] |
| Kapasitas LPHD 2087 (S2) | 0,50 [0,32; 0,68] | 0,52 [0,32; 0,81] | 0,80 [0,36; 1,00] |
| Δ pendapatan bersih per RT bergantung (Rp/th) | 6.693 [-69.862; 65.003] | -3.330 [-248.456; 85.831] | -36.233 [-462.996; 133.142] |
| Δ pendapatan per RT terdampak (Rp/th) | -45.164 [-333.062; 47.118] | -91.901 [-942.073; 55.909] | -258.041 [-1.586.783; 73.779] |
| Δ kehilangan per RT terdampak (Rp/th) | 94.087 [7.718; 460.251] | 165.127 [13.918; 1.241.455] | 404.054 [25.695; 1.861.590] |

## 4. PRCC (USD 20; lembar 6 untuk USD 10 dan 35)

| Indikator | Parameter berpengaruh terbesar (PRCC, USD 20) |
|---|---|
| Deforestasi dihindari S2−S1 (ha) | Efektivitas Perlindungan Penuh 0,83; Besaran Pembiayaan Jembatan 0,79; Biaya per Hari Patroli -0,77; Durasi Pembiayaan Jembatan 0,72 |
| Manfaat karbon bersih kumulatif 2087 (tCO2e) | Efektivitas Perlindungan Penuh 0,83; Besaran Pembiayaan Jembatan 0,78; Biaya per Hari Patroli -0,77; Durasi Pembiayaan Jembatan 0,72 |
| Kas LPHD rerata 2075–2086 (Rp/th) | Efektivitas Perlindungan Penuh 0,57; Proporsi Kredit REDD dalam Project Area 0,46; Biaya per Hari Patroli -0,45; Pengali laju deforestasi BAU 0,36 |
| Cakupan kebutuhan minimum 2060–2086 (%) | Efektivitas Perlindungan Penuh 0,81; Biaya per Hari Patroli -0,79; Proporsi Kredit REDD dalam Project Area 0,70; Besaran Pembiayaan Jembatan 0,67 |
| NPV inkremental proyek [SEMENTARA] (Rp) | Efektivitas Perlindungan Penuh 0,84; Biaya per Hari Patroli -0,81; Besaran Pembiayaan Jembatan 0,77; Pengali laju deforestasi BAU 0,76 |
| NPV mitra inkremental [SEMENTARA] (Rp) | Efektivitas Perlindungan Penuh 0,83; Biaya per Hari Patroli -0,82; Pengali laju deforestasi BAU 0,75; Pengali biaya MRV -0,74 |
| Δ pendapatan bersih per RT bergantung (Rp/th) | Pengali Kehilangan Akses -0,89; Efektivitas Perlindungan Penuh -0,39; Biaya per Hari Patroli 0,31; Proporsi Kredit REDD dalam Project Area -0,26 |
| Δ pendapatan per RT terdampak (Rp/th) | Pengali Kehilangan Akses -0,89; Efektivitas Perlindungan Penuh -0,61; Besaran Pembiayaan Jembatan -0,52; Biaya per Hari Patroli 0,51 |
| Δ FTE berupah 2030–2055 | Besaran Pembiayaan Jembatan 0,81; Durasi Pembiayaan Jembatan 0,81; Biaya per Hari Patroli -0,81; Efektivitas Perlindungan Penuh 0,79 |
| Δ FTE berupah 2060–2086 | Efektivitas Perlindungan Penuh 0,81; Biaya per Hari Patroli -0,79; Proporsi Kredit REDD dalam Project Area 0,69; Besaran Pembiayaan Jembatan 0,66 |
| KUPS aktif 2087 S2 | Biaya Reaktivasi KUPS -0,82; Porsi Laba Ditahan untuk Reinvestasi 0,69; Pengali surplus KUPS 0,50; Efektivitas Perlindungan Penuh 0,45 |
| Debit reversal belum diselesaikan 2087 (tCO2e) | Delay Verifikasi dan Penerbitan Kredit 0,38; Besaran Pembiayaan Jembatan 0,21; Proporsi Kredit REDD dalam Project Area -0,19; Efektivitas Perlindungan Penuh -0,18 |

**Peran k** (keberlanjutan patroli reguler S1) kecil hingga sedang. Ini karena k menaikkan perlindungan di S1 dan S2 sekaligus, sehingga pengaruhnya pada selisih berpasangan teredam. Pada Fase 3 (kredit terhadap BAU), k adalah penentu utama; dalam mekanisme C tidak lagi.

| Indikator | PRCC k, USD 10 | USD 20 | USD 35 |
|---|---|---|---|
| Cakupan kebutuhan minimum 2060–2086 (%) | 0,17 | 0,29 | 0,12 |
| Debit reversal belum diselesaikan 2087 (tCO2e) | 0,08 | -0,02 | -0,18 |
| Deforestasi dihindari S2−S1 (ha) | 0,19 | 0,29 | 0,06 |
| KUPS aktif 2087 S2 | 0,07 | 0,09 | 0,05 |
| Kas LPHD rerata 2075–2086 (Rp/th) | 0,08 | 0,14 | -0,01 |
| Manfaat karbon bersih kumulatif 2087 (tCO2e) | 0,20 | 0,29 | 0,06 |
| NPV inkremental proyek [SEMENTARA] (Rp) | 0,22 | 0,20 | 0,12 |
| NPV mitra inkremental [SEMENTARA] (Rp) | 0,27 | 0,22 | 0,13 |
| Δ FTE berupah 2030–2055 | 0,09 | 0,20 | 0,07 |
| Δ FTE berupah 2060–2086 | 0,16 | 0,27 | -0,11 |
| Δ pendapatan bersih per RT bergantung (Rp/th) | 0,00 | -0,08 | -0,04 |
| Δ pendapatan per RT terdampak (Rp/th) | -0,06 | -0,09 | -0,06 |

## 5. Bacaan

1. **Tambahan perlindungan selalu positif** (100 % ensembel pada semua harga), karena jembatan membiayai patroli tambahan. Besarnya sangat lebar:
   - USD 20: median 682 ha [P5 137; P95 9.233];
   - ditentukan oleh efektivitas perlindungan, besaran dan durasi jembatan, serta biaya per HOK.
2. **Manfaat karbon bersih kumulatif 2087 selalu positif**, tetapi pada USD ≤ 20 umumnya turun lebih dari 10 % dari puncaknya (*reversal*). Bagian ensembel yang tidak turun: 0,5 % (USD 10), 23,8 % (USD 20), 78,2 % (USD 35).
3. **Pembiayaan LPHD jangka panjang** hanya berlanjut pada sebagian kecil ensembel USD 20: kas LPHD masih mengalir 2075–2086 pada 22,2 % ensembel, dan cakupan kebutuhan ≥ 50 % pada 10,8 %. Pada USD 35 angkanya 74,0 % dan 57,2 %. Pada USD 10 praktis tidak pernah.
4. **NPV [SEMENTARA].**
   - NPV inkremental proyek positif pada 13,0 / 65,8 / 95,8 % ensembel (USD 10 / 20 / 35).
   - NPV mitra positif pada 4,2 / 46,8 / 88,8 %.
   - Status biaya: biaya pengembangan proyek = 0 dan biaya material = 0, sehingga NPV ini batas atas.
5. **Pendapatan bersih rumah tangga.**
   - RT bergantung hutan: naik pada 60,0 / 47,5 / 33,8 % ensembel dan turun pada sisanya.
   - RT terdampak: naik hanya pada 25,2 / 19,0 / 14,5 %.
   - Pengali kehilangan akses mendominasi (PRCC −0,89).
6. **KUPS 2087 ≥ 90 % tingkat 2026** pada 15,0 / 24,8 / 62,5 % ensembel S2, dibanding 14,5 % pada S1. Penentunya biaya reaktivasi dan porsi reinvestasi, kecuali pada USD 35 ketika kas karbon cukup besar.

## 6. Keterbatasan

- Distribusi parameter bersifat asumsi.
- Harga diperlakukan sebagai skenario (tiga level), bukan disampel.
- Struktur model tetap; ketidakpastian struktural (bentuk respons patroli, mekanisme kehilangan akses) tidak tercakup.
- Aturan *reversal* dan urutan pemulihan dana mitra tidak divariasikan.
