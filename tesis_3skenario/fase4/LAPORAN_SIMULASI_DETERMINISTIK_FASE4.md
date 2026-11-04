# Laporan Simulasi Deterministik Final (Fase 4 Tahap 3)

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (946 variabel, 16 View; md5 `639083f9…`).

**Status:**
- Lolos final gate dengan keputusan SIAP BERSYARAT (`FINAL_GATE_FASE4_PWD.md`).
- **Vensim native BELUM DIVERIFIKASI.**
- **NPV SEMENTARA.**

**Data:** `HASIL_SIMULASI_FINAL_PWD.xlsx`. **Grafik:** `GRAFIK_FINAL_PWD/F1–F5`.

**Konfigurasi:**

| Unsur | Isi |
|---|---|
| S1 | PS dengan pembiayaan terbatas |
| S2 | PS dengan perdagangan karbon, mekanisme C: kredit konservatif endogen terhadap Referensi S1 (protokol berpasangan) + pembiayaan jembatan 2026–2030 |
| Jembatan J1 | Rp782,86 juta/th, setara pembiayaan mitra 2025 |
| Jembatan JP | Kebutuhan patroli tambahan penuh, ±Rp1,69 miliar/th |
| Harga | USD 6, 10, 15, 20, 35/tCO₂e |
| Talangan | Biaya modal 0; dipulihkan sebelum bagi hasil |
| *Reversal* | Aturan 2 |
| MRV | Berjalan sepanjang periode kredit (aturan henti nonaktif) |
| Asumsi kerja kelas D | k = 0,5; efektivitas 0,37; kas non-karbon 0; dukungan material 0; biaya patroli Rp260.000/HOK (upah Rp150.000 terkonfirmasi); pengali kehilangan akses 1 |

Jembatan J1 dan JP **bukan komitmen aktual mitra**.

Angka S2 − S1 adalah selisih menurut asumsi model, bukan estimasi kausal empiris. Kredit model bukan kredit terverifikasi. FTE bukan jumlah orang. Dana LPHD bukan pendapatan rumah tangga. Tidak ada klaim tentang kemiskinan atau ketimpangan.

---

## Ringkasan temuan

1. **Ekologi (RQ1).** Mekanisme C menambah perlindungan hutan di atas S1 pada semua harga, karena jembatan membiayai patroli tambahan sejak 2026. Besarnya sangat bergantung pada harga dan besaran jembatan:
   - C-J1: 287–454 ha deforestasi dihindari pada USD 6–20, dan 4.954 ha pada USD 35;
   - C-JP: 620–1.338 ha pada USD 6–20, dan 7.487 ha pada USD 35.

   Pada USD ≤ 20, patroli tambahan habis sebelum 2060, dan sebagian mitigasi hilang kembali (*reversal*).
2. **Pembiayaan (RQ2).**
   - Siklus kredit → kas → patroli bertahan sampai 2087 hanya pada USD 35.
   - Pada USD ≤ 20, LPHD menerima kas karbon hanya 0–28 dari 62 tahun, dan cakupan kebutuhan minimum sesudah 2060 praktis 0 %.
   - NPV mitra inkremental [SEMENTARA] positif hanya pada C-JP USD 20 (+Rp2,51 M) dan pada USD 35 (+Rp6,66 M J1; +Rp16,54 M JP).
   - Pada USD ≤ 20, mitra menanggung defisit MRV Rp11–19 M nominal hingga 2087.
3. **Sosial-ekonomi (RQ3).**
   - Kerja berupah bertambah 0,4–2,7 FTE (J1, USD ≤ 20) sampai 17,4–41,7 FTE (USD 35) pada 2030–2055. Pada USD ≤ 20, kerja ini hilang sesudah 2060.
   - Perubahan KUPS kecil pada USD ≤ 20.
   - Pendapatan bersih per RT bergantung hutan **turun** di semua konfigurasi, karena tambahan kehilangan akses lebih besar daripada tambahan pendapatan hutan dan program. Kompensasi belum ada di model utama.
4. **Kelembagaan dan distribusi (RQ4).**
   - LPHD sepenuhnya bergantung pada kas karbon (100 % kas LPHD berasal dari karbon; kas non-karbon 0).
   - Manfaat tertunda: kas LPHD pertama 2032–2036, sesudah defisit MRV dan talangan dipulihkan.
   - Beban pembatasan akses jatuh pada rumah tangga terdampak (±3.000 RT): +96 ribu s.d. +1,37 juta Rp/RT/th, sementara kompensasi = 0.


**Tabel 1. Ekologi: selisih S2 − S1 (USD 6 s.d. 35)**

| Indikator | C-J1 USD6 | C-J1 USD10 | C-J1 USD15 | C-J1 USD20 | C-J1 USD35 | C-JP USD6 | C-JP USD10 | C-JP USD15 | C-JP USD20 | C-JP USD35 |
|---|---|---|---|---|---|---|---|---|---|---|
| Deforestasi dihindari 2025–2086 (ha) | 287 | 287 | 338 | 454 | 4.954 | 620 | 686 | 905 | 1.338 | 7.487 |
| Δ hutan 2087 (ha) | 176 | 176 | 217 | 313 | 4.842 | 380 | 433 | 613 | 982 | 7.237 |
| Emisi deforestasi dihindari (ribu tCO₂e) | 97,9 | 97,9 | 115,4 | 155,1 | 1.662,8 | 211,6 | 234,3 | 309,3 | 457,4 | 2.537,9 |
| Emisi bersih biomassa dihindari (ribu tCO₂e) | 81,7 | 81,7 | 98,7 | 137,8 | 1.675,8 | 176,6 | 198,7 | 272,3 | 419,8 | 2.564,0 |
| Tambahan serapan rehabilitasi (ribu tCO₂e) | 0,0 | 0,0 | 3,9 | 12,4 | 303,4 | 0,0 | 5,0 | 21,1 | 52,3 | 557,8 |
| Tambahan rehabilitasi (ha) | 0 | 0 | 18 | 57 | 1.567 | 0 | 24 | 96 | 235 | 2.691 |
| Δ intensitas perlindungan 2030–2055 | 0,014 | 0,014 | 0,028 | 0,057 | 0,324 | 0,031 | 0,048 | 0,103 | 0,203 | 0,697 |
| Patroli kas LPHD 2060–2080 (HOK/th) | 0 | 0 | 0 | 0 | 5.562 | 0 | 0 | 0 | 13 | 6.491 |

**Tabel 2. Pembiayaan dan keuangan proyek (nilai S2; Rp miliar nominal kecuali NPV)**

| Indikator | C-J1 USD6 | C-J1 USD10 | C-J1 USD15 | C-J1 USD20 | C-J1 USD35 | C-JP USD6 | C-JP USD10 | C-JP USD15 | C-JP USD20 | C-JP USD35 |
|---|---|---|---|---|---|---|---|---|---|---|
| Kredit REDD diajukan (ribu tCO₂e) | 68,8 | 68,8 | 78,0 | 100,7 | 897,3 | 148,9 | 159,0 | 201,1 | 282,3 | 1.369,2 |
| Kredit ARR diajukan (ribu tCO₂e) | 0,0 | 0,0 | 0,0 | 0,0 | 11,5 | 0,0 | 0,0 | 0,0 | 0,0 | 23,0 |
| Kredit terjual (ribu tCO₂e) | 60,2 | 60,2 | 68,2 | 88,1 | 711,3 | 130,3 | 139,1 | 175,9 | 247,0 | 1.143,1 |
| Potensi thd BAU, pelaporan (ribu tCO₂e) | 241,6 | 241,6 | 250,8 | 272,0 | 1.102,7 | 292,9 | 304,8 | 344,6 | 428,3 | 1.576,4 |
| Kas penjualan | 5,96 | 9,94 | 16,88 | 29,07 | 408,71 | 12,90 | 22,96 | 43,54 | 81,53 | 655,24 |
| Biaya MRV, transaksi, pajak, pengganti | 24,64 | 25,70 | 26,72 | 27,55 | 47,58 | 26,81 | 28,60 | 30,53 | 30,12 | 62,47 |
| …di antaranya biaya kredit pengganti | 1,27 | 2,12 | 2,75 | 2,84 | 0,00 | 2,76 | 3,98 | 4,66 | 1,92 | 0,00 |
| Debit reversal belum diselesaikan 2087 (ribu tCO₂e) | 2,5 | 2,5 | 2,9 | 3,9 | 0,0 | 5,4 | 5,9 | 7,8 | 11,3 | 0,0 |
| Pembiayaan jembatan | 3,91 | 3,91 | 3,91 | 3,91 | 3,91 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| Sisa talangan 2087 | 3,91 | 0,73 | 0,00 | 0,00 | 0,00 | 2,95 | 0,00 | 0,00 | 0,00 | 0,00 |
| Defisit MRV ditalangi mitra 2087 | 18,68 | 18,95 | 17,68 | 15,20 | 0,00 | 19,40 | 19,13 | 17,12 | 11,06 | 0,00 |
| Kas LPHD karbon | 0,00 | 0,00 | 2,36 | 7,69 | 214,33 | 0,00 | 3,03 | 13,02 | 32,42 | 350,60 |
| Dana mitra 40 % | 0,00 | 0,00 | 1,57 | 5,12 | 142,89 | 0,00 | 2,02 | 8,68 | 21,61 | 233,73 |
| NPV inkremental karbon [SEMENTARA] | -4,16 | -2,82 | -0,84 | 1,75 | 18,36 | -4,94 | -1,81 | 3,13 | 9,62 | 44,05 |

| Indikator | C-J1 USD6 | C-J1 USD10 | C-J1 USD15 | C-J1 USD20 | C-J1 USD35 | C-JP USD6 | C-JP USD10 | C-JP USD15 | C-JP USD20 | C-JP USD35 |
|---|---|---|---|---|---|---|---|---|---|---|
| NPV mitra inkremental thd S1 (Rp miliar) [SEMENTARA] | -4,16 | -2,82 | -1,54 | -0,27 | 6,66 | -4,94 | -2,66 | -0,31 | 2,51 | 16,54 |
| Tahun kas LPHD pertama | – | – | 2035,1 | 2034,1 | 2032,8 | – | 2035,7 | 2034,1 | 2033,4 | 2032,3 |

**Tabel 3. Keberlanjutan pembiayaan dan kelembagaan LPHD (nilai S2; S1 = 0 untuk semua indikator kas)**

| Indikator | C-J1 USD6 | C-J1 USD10 | C-J1 USD15 | C-J1 USD20 | C-J1 USD35 | C-JP USD6 | C-JP USD10 | C-JP USD15 | C-JP USD20 | C-JP USD35 |
|---|---|---|---|---|---|---|---|---|---|---|
| Cakupan kebutuhan minimum 2030–2055 (%) | 0,0 | 0,0 | 1,6 | 5,2 | 38,1 | 0,0 | 2,1 | 8,9 | 21,1 | 95,2 |
| Cakupan kebutuhan minimum 2060–2086 (%) | 0,0 | 0,0 | 0,0 | 0,0 | 90,5 | 0,0 | 0,0 | 0,0 | 0,2 | 115,4 |
| Tahun kebutuhan minimum tercukupi (dari 62) | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 46 |
| Tahun dengan kas LPHD > 0 (dari 62) | 0 | 0 | 9 | 17 | 55 | 0 | 8 | 17 | 28 | 55 |
| Kas LPHD 2030–2055 (Rp juta/th) | 0 | 0 | 91 | 296 | 2.299 | 0 | 116 | 501 | 1.218 | 5.689 |
| Kas LPHD 2060–2086 (Rp juta/th) | 0 | 0 | 0 | 0 | 5.181 | 0 | 0 | 0 | 0 | 6.423 |
| Belanja operasional + kelembagaan (Rp juta/th) | 0 | 0 | 23 | 74 | 537 | 0 | 29 | 125 | 298 | 1.425 |
| Kapasitas LPHD 2087 (S1 = 0,50) | 0,50 | 0,50 | 0,50 | 0,50 | 0,87 | 0,50 | 0,50 | 0,50 | 0,50 | 0,86 |

**Tabel 4. Sosial-ekonomi: selisih S2 − S1 (rerata 2030–2055 kecuali disebut)**

| Indikator | C-J1 USD6 | C-J1 USD10 | C-J1 USD15 | C-J1 USD20 | C-J1 USD35 | C-JP USD6 | C-JP USD10 | C-JP USD15 | C-JP USD20 | C-JP USD35 |
|---|---|---|---|---|---|---|---|---|---|---|
| HOK berupah PS | 116 | 116 | 331 | 806 | 5.209 | 250 | 527 | 1.418 | 3.039 | 12.517 |
| …patroli berbayar | 116 | 116 | 221 | 457 | 2.593 | 250 | 384 | 827 | 1.625 | 5.575 |
| …penanaman berupah | 0 | 0 | 60 | 185 | 1.424 | 0 | 78 | 313 | 752 | 3.775 |
| …pengendalian kebakaran | 0 | 0 | 50 | 164 | 1.193 | 0 | 65 | 278 | 662 | 3.167 |
| HOK sukarela PS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FTE berupah | 0,4 | 0,4 | 1,1 | 2,7 | 17,4 | 0,8 | 1,8 | 4,7 | 10,1 | 41,7 |
| FTE berupah 2060–2086 | 0,0 | 0,0 | 0,0 | 0,0 | 39,5 | 0,0 | 0,0 | 0,0 | 0,0 | 48,1 |
| Upah kegiatan PS (Rp juta/th) | 17,4 | 17,4 | 46,0 | 109,5 | 694,9 | 37,4 | 74,3 | 193,4 | 409,5 | 1.648,2 |
| KUPS aktif | 0,0 | 0,0 | 0,2 | 0,6 | 3,0 | 0,0 | 0,2 | 1,0 | 2,0 | 24,2 |
| KUPS aktif 2087 | 0,0 | 0,0 | 0,1 | 0,3 | 44,7 | 0,0 | 0,1 | 0,6 | 1,5 | 60,1 |
| Anggota KUPS | 0 | 0 | 3 | 8 | 46 | 0 | 4 | 15 | 30 | 364 |
| Omzet KUPS (Rp juta/th) | 0,0 | 0,0 | 2,4 | 7,6 | 49,2 | 0,0 | 3,1 | 13,1 | 29,5 | 237,6 |
| Surplus KUPS (Rp juta/th) | 0,0 | 0,0 | 1,7 | 5,3 | 34,0 | 0,0 | 2,1 | 9,1 | 20,4 | 164,3 |
| Penerimaan anggota KUPS (Rp juta/th) | 0,0 | 0,0 | 0,4 | 1,4 | 9,0 | 0,0 | 0,6 | 2,4 | 5,4 | 43,2 |
| Modal usaha KUPS 2087 (Rp juta) | 0,0 | 0,0 | 0,0 | 0,0 | 141,0 | 0,0 | 0,0 | 0,0 | 0,1 | 1.156,5 |
| Pendapatan hutan per RT (Rp/th) | 37.973 | 37.973 | 42.907 | 52.266 | 100.270 | 82.159 | 88.341 | 106.789 | 131.664 | 233.100 |
| Pendapatan program per RT (Rp/th) | 368 | 368 | 916 | 2.086 | 11.847 | 793 | 1.493 | 3.709 | 7.502 | 28.979 |
| Kehilangan akses per RT bergantung (Rp/th) | 38.611 | 38.611 | 49.116 | 72.261 | 245.061 | 83.616 | 97.149 | 141.094 | 213.282 | 552.157 |
| Kehilangan per RT terdampak (Rp/th) | 95.951 | 95.951 | 122.058 | 179.574 | 608.995 | 207.792 | 241.422 | 350.628 | 530.023 | 1.372.152 |
| Kompensasi (Rp/th) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Pendapatan bersih per RT bergantung (Rp/th) | -270 | -270 | -5.293 | -17.909 | -132.944 | -664 | -7.315 | -30.595 | -74.116 | -290.079 |
| Kehilangan pendapatan agregat (Rp juta/th) | 242 | 242 | 318 | 492 | 1.883 | 524 | 623 | 950 | 1.510 | 4.215 |

**Nilai S1 (acuan)**

| Indikator | S1 |
|---|---|
| Hutan 2087 (ha) | 82.799 |
| Deforestasi 2025–2086 (ha) | 28.640 |
| Laju deforestasi 2030–2055 (ha/th) | 474 |
| Patroli reguler sukarela (HOK/th) | 1.506 |
| FTE sukarela | 5,0 |
| Nilai kontribusi non-tunai (Rp juta/th) | 354 |
| KUPS aktif rerata / 2087 | 21,8 / 5,7 |
| Penerimaan anggota KUPS (Rp juta/th) | 15,8 |
| Pendapatan bersih per RT bergantung (Rp juta/th) | 41,21 |
| Kehilangan akses per RT terdampak (Rp/th) | 228.136 |
| NPV keseluruhan (Rp miliar) [SEMENTARA] | -1,31 |

**Pembanding eksploratif mekanisme A (baseline BAU; tidak lolos uji additionality model)**

| Indikator | A USD6 | A USD10 | A USD15 | A USD20 | A USD35 |
|---|---|---|---|---|---|
| Kredit REDD diajukan (ribu tCO₂e) | 197,5 | 211,9 | 274,1 | 395,5 | 1.310,1 |
| Deforestasi dihindari S2−S1 (ha) | 0 | 78 | 415 | 1.072 | 6.045 |
| NPV mitra inkremental (Rp miliar) | -1,06 | 0,16 | 1,44 | 3,08 | 12,16 |

---

## Analisis 1: Ekologi (RQ1)

- **Jembatan adalah pemicu utama mitigasi.**
  - Pada USD 6 dan 10, C-J1 memberi hasil fisik identik (287 ha), karena kas karbon tidak pernah mencapai LPHD. Seluruh mitigasi berasal dari patroli jembatan 2026–2030.
  - C-JP menggandakan efek itu (620–686 ha).
- **Harga menentukan apakah mitigasi bertahan.**
  - Pada USD 20, patroli yang dibiayai kas LPHD 2060–2080 ≈ 0 (J1) dan 13 HOK/th (JP).
  - Pada USD 35, patroli itu 5.562 (J1) dan 6.491 HOK/th (JP = kebutuhan penuh).
  - Δ intensitas perlindungan 2030–2055 naik dari 0,014 (J1 USD 6) menjadi 0,697 (JP USD 35).
- **Non-permanensi pada USD ≤ 20.** Hutan yang diselamatkan menghadapi laju deforestasi per ha yang sama sesudah pembiayaan berhenti. Sebagian mitigasi hilang kembali (lihat `FINAL_GATE_FASE4_PWD.md` bagian 2). Δ hutan 2087 lebih kecil daripada deforestasi dihindari kumulatif (C-J1 USD 20: 313 vs 454 ha).
- **Serapan rehabilitasi tambahan hanya bermakna pada USD 35:** 303–558 ribu tCO₂e dan 1.567–2.691 ha tanam. Pada USD ≤ 20 nilainya 0–52 ribu tCO₂e.
- **Pembanding A** (tidak lolos uji additionality) memberi deforestasi dihindari lebih besar pada USD 20–35 (1.072 dan 6.045 ha). Itu karena kredit atas perlindungan tingkat S1 membiayai siklus sejak 2028, bukan karena mitigasi tambahan per kredit lebih tinggi.

## Analisis 2: Keberlanjutan pembiayaan LPHD (RQ2)

- **Urutan arus kas:**
  1. kas penjualan pertama 2029;
  2. surplus lebih dulu menutup defisit MRV yang ditalangi mitra (MRV berjalan sejak 2024);
  3. lalu talangan jembatan;
  4. baru kemudian dibagi 60/40.

  Akibatnya kas LPHD pertama baru datang 2032,3–2035,7, dan tidak pernah datang pada C-J1 USD ≤ 10 dan C-JP USD 6.
- **Kecukupan biaya pengelolaan:**
  - Pada USD ≤ 20, cakupan kebutuhan minimum LPHD 2030–2055 hanya 0–21 %, dan 2060–2086 ≈ 0 %.
  - Kebutuhan minimum tidak pernah tercukupi penuh, kecuali pada USD 35 (8 tahun J1; 46 tahun JP).
- **Kelayakan finansial [SEMENTARA]:**
  - NPV inkremental proyek positif mulai USD 20 (J1) atau USD 15 (JP).
  - NPV mitra inkremental positif hanya pada C-JP USD 20 dan USD 35.
  - Pada USD ≤ 20, defisit MRV yang ditalangi mitra hingga 2087 mencapai Rp11–19 miliar nominal, dan biaya kredit pengganti *reversal* Rp1,3–4,7 miliar.
  - Talangan J1 tidak pulih pada USD 6 (Rp3,91 M) dan sebagian pada USD 10 (Rp0,73 M).
- **Siklus mandiri:** kas LPHD 2060–2086 > 0 hanya pada USD 35 (Rp5,2–6,4 miliar/th).

## Analisis 3: Pekerjaan, KUPS, dan pendapatan rumah tangga (RQ3)

- **Kerja.**
  - Seluruh tambahan kerja S2 adalah kerja **berupah** (patroli, penanaman, pengendalian kebakaran). Patroli reguler sukarela (1.506 HOK/th, 5,0 FTE) sama di S1 dan S2.
  - Pada USD 20: +806 HOK berupah (J1) dan +3.039 HOK (JP), setara +2,7 dan +10,1 FTE, dengan upah kegiatan +Rp110 dan +Rp410 juta/th.
  - Sesudah 2060, tambahan FTE hanya bertahan pada USD 35 (39,5–48,1 FTE).
  - Upah patroli memakai Rp150.000/HOK. Upah pengendalian kebakaran Rp130.000 belum dikonfirmasi.
- **KUPS.**
  - Di S1, KUPS aktif turun dari rerata 21,8 (2030–2055) menjadi 5,7 pada 2087. Ini ditentukan parameter kelas D (biaya reaktivasi, porsi reinvestasi).
  - Pada USD ≤ 20, S2 hanya menambah 0–2 KUPS dan Rp0–5,4 juta/th penerimaan anggota.
  - Pada USD 35: +44,7 (J1) dan +60,1 KUPS (JP) pada 2087; penerimaan anggota +Rp9,0 dan +Rp43,2 juta/th.
  - Omzet bukan penerimaan anggota: hanya 26,3 % surplus yang dibagikan.
- **Pendapatan RT bergantung hutan** (±7.460 RT; pendapatan bersih S1 Rp41,2 juta/RT/th). Δ pendapatan bersih bernilai −270 s.d. −290.079 Rp/RT/th. Dekomposisi (Tabel 4; lembar 10 gate):
  - pendapatan hutan naik karena ketersediaan sumber daya membaik (+38–233 ribu);
  - pendapatan program naik kecil (+0,4–29 ribu);
  - kehilangan akses naik lebih besar (+39–552 ribu).

  Dengan pengali kehilangan akses 0, Δ bersih pada C-J1 USD 20 menjadi **+54.352**. Arah dampak terhadap pendapatan RT ditentukan oleh asumsi kehilangan akses (kelas D), bukan oleh penerimaan karbon.
- **RT terdampak** (±3.000 RT) menanggung kehilangan +96 ribu (C-J1 USD 6) hingga +1,37 juta Rp/RT/th (C-JP USD 35) di atas S1 (228 ribu). **Kompensasi = 0** di model utama; kompensasi baru diuji di eksperimen benefit sharing (belum dijalankan).

## Analisis 4: Kelembagaan dan distribusi manfaat (RQ4)

- **Ketergantungan.**
  - Tanpa kas non-karbon, 100 % dana LPHD di S2 berasal dari karbon, dan S1 tidak memiliki dana LPHD sama sekali.
  - Kapasitas LPHD hanya naik pada USD 35 (0,50 → 0,86–0,87). Pada USD ≤ 20 tetap 0,50.
  - Belanja operasional dan kelembagaan LPHD 2030–2055: Rp0–298 juta/th pada USD ≤ 20.
- **Penundaan manfaat.**
  - Mitra memperoleh prioritas pemulihan (defisit MRV, lalu talangan), sehingga LPHD menunggu 3–7 tahun sesudah kas penjualan pertama.
  - Pada USD ≤ 20, kas LPHD hanya ada 0–28 dari 62 tahun.
  - Bagi pengelolaan desa, artinya dana kolektif datang terlambat dan berhenti sebelum 2060.
- **Distribusi.**
  - Kas karbon dibagi 60 % LPHD dan 40 % mitra sesudah biaya. Mitra juga menerima pemulihan talangan dan defisit MRV sebelum bagi hasil.
  - Manfaat yang langsung sampai ke rumah tangga hanya berupa upah dan bagian surplus KUPS, yang kecil pada USD ≤ 20.
  - Beban pembatasan akses dan *reversal* tidak dikompensasi di model utama.
  - Rekomendasi alokasi (R1 dan lainnya) belum dapat diberikan sebelum eksperimen B0–B4 dan R1–R2 dijalankan pada mekanisme C.

---

## Ketidakpastian yang memengaruhi tafsiran

1. **k = 0,5 (kelas D)** menentukan tingkat perlindungan S1, sehingga juga menentukan acuan kredit dan ukuran tambahan S2.
2. **Pengali kehilangan akses** (kelas D) menentukan arah dampak terhadap pendapatan rumah tangga.
3. **Biaya MRV dan biaya patroli Rp260.000/HOK** menentukan apakah surplus kredit dapat sampai ke LPHD. Biaya pengembangan proyek masih 0 → NPV SEMENTARA.
4. **Besaran dan durasi jembatan** tidak berbasis komitmen mitra.
5. **Aturan *reversal*** (buffer, pembatalan, pengganti) adalah asumsi model tanpa dasar kontraktual.
6. **Parameter KUPS** (reaktivasi, reinvestasi) menentukan penurunan KUPS S1.
7. **Vensim native** belum dijalankan.

Semua ketidakpastian ini akan diuji pada Monte Carlo/PRCC berpasangan. Monte Carlo, PRCC, benefit sharing, dan revisi makalah **belum dijalankan**.
