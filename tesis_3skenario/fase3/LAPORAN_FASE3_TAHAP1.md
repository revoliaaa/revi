# Laporan Fase 3 Tahap 1: Prasyarat, Simulasi Deterministik, dan Sensitivitas Prioritas

**Model:** `DKP_25HD_FINAL_2SKENARIO.mdl` (md5 `aa1428df…`). Model tiga skenario tidak diubah.

**Perangkat:** PySD 3.14.3, Euler, DT 0,0625, 2024–2087.

**Status verifikasi:** Units Check dan pembandingan native Vensim–PySD **TERTUNDA** (Vensim tidak tersedia di lingkungan ini). Semua angka di bawah adalah "terverifikasi PySD".

**Asumsi kerja (bukan data):**
- keberlanjutan patroli reguler k = 0,5;
- kas non-karbon 0 dan dukungan material rehabilitasi 0;
- pembiayaan awal berstatus hibah;
- biaya pengembangan proyek 0; diskonto 10 %;
- biaya reaktivasi KUPS Rp 50 juta; porsi reinvestasi 0,5.

NPV berstatus **SEMENTARA**. Monte Carlo, PRCC, benefit sharing, dan revisi makalah **belum** dijalankan.

**Berkas tahap ini:**
- `HASIL_SIMULASI_FINAL_2SKENARIO.xlsx`
- `ANALISIS_SENSITIVITAS_FINAL.xlsx`
- `GRAFIK_HASIL_FINAL/` (G1–G9)

---

## 1. Pemeriksaan prasyarat

| Prasyarat | Status | Temuan |
|---|---|---|
| Kronologi kredit → kas → patroli | **Konsisten** | Di semua harga: kredit diajukan 2025 (efek perlindungan aktif mulai 2025), terbit 2028,0, terjual dan dibayar 2028,06. Biaya MRV sejak 2024 ditalangi mitra, lalu defisitnya dilunasi lebih dulu. Baru setelah itu kas mengalir ke LPHD. Belanja, patroli tambahan, dan penurunan deforestasi menyusul berturut-turut satu DT |
| "Patroli tambahan pertama 2029" vs "kas pertama USD 10 pada 2031,875" | **Bukan kesalahan: harga berbeda** | 2029 berasal dari USD 20 (kas LPHD 2029,81; patroli 2029,88) dan USD 35 (2029,19; 2029,25). 2031,875 adalah kas LPHD pertama pada USD 10, dengan patroli 2031,94. USD 15: kas 2030,38 dan patroli 2030,44 |
| USD 6 | **Konsisten, tanpa kas LPHD** | Defisit biaya MRV terus naik sampai Rp 8,0 miliar dan tidak pernah lunas. LPHD tidak menerima kas karbon, sehingga S2 USD 6 identik secara fisik dengan S1 |
| Konsistensi indikator sosial-ekologis dengan pembiayaan | **Konsisten** | Uji Fase 2 U3, U4, U7, U10–U12, dan P1–P7 lulus pada berkas yang sama |
| Units Check Vensim | **TERTUNDA** | Pemeriksaan satuan statis: 813/813 konsisten |
| Pembandingan native Vensim–PySD | **TERTUNDA** | `bandingkan_vensim_pysd.py` tersedia |
| Penandaan asumsi | **Selesai** | Lembar "8 Register asumsi" dan komentar `PERINGATAN D1/D3` di `.mdl` |

## 2. Hasil deterministik

### 2.1 Dampak perdagangan karbon menurut model (S2 − S1)

Kumulatif 2025–2086, kecuali disebut lain. Pada USD 6 semua selisih = 0.

| Indikator | USD 10 | USD 15 | USD 20 | USD 35 |
|---|---|---|---|---|
| Δ hutan 2087 (ha) | +67 | +382 | +1.018 | +6.268 |
| Deforestasi dihindari (ha) | 78 | 415 | 1.072 | 6.045 |
| Emisi deforestasi dihindari (ribu tCO₂e, fisik) | 27 | 140 | 361 | 2.036 |
| Tambahan serapan rehabilitasi (ribu tCO₂e) | 6 | 29 | 74 | 538 |
| Patroli tambahan dari kas, rerata 2030–2055 (HOK/th) | 136 | 491 | 991 | 3.887 |
| Δ intensitas perlindungan | +0,017 | +0,061 | +0,124 | +0,486 |
| Δ FTE berupah | +0,9 | +3,3 | +6,8 | +27,6 |
| Kas LPHD dari karbon (Rp miliar, 2024–2086) | 3,6 | 18,5 | 48,2 | 335,7 |
| Cakupan kebutuhan minimum LPHD, rerata 2030–2055 | 2,1 % | 7,5 % | 15,2 % | 62,3 % |
| NPV inkremental karbon (Rp miliar) [SEMENTARA] | 0,87 | 3,97 | 8,03 | 30,68 |
| Δ KUPS aktif 2087 | +0,2 | +0,9 | +2,6 | +69,3 |
| Δ pendapatan bersih per RT bergantung (Rp/RT/th) | −7.138 | −25.565 | −51.939 | −210.572 |
| Δ pendapatan program per RT (Rp/RT/th) | +610 | +2.172 | +4.335 | +17.221 |
| Δ kehilangan akses per RT terdampak (Rp/RT/th) | +30.522 | +106.200 | +209.547 | +788.597 |

**Kondisi S1 (pembanding):**
- Patroli reguler 1.506 HOK/th, intensitas 0,19, deforestasi kumulatif 28.640 ha, hutan 2087 82.799 ha.
- LPHD tanpa kas, sehingga kesenjangan kebutuhan minimum = 100 % (Rp 5,64 miliar/th).
- KUPS turun dari 33,4 (2026) menjadi 5,7 (2087), di bawah dua asumsi D. Lihat bagian 3.

### 2.2 Terhadap baseline referensi karbon (dilaporkan terpisah dari S2 − S1)

| | S1 | S2 USD 6 | S2 USD 10 | S2 USD 20 | S2 USD 35 |
|---|---|---|---|---|---|
| Deforestasi dihindari vs baseline (ha) | 1.173 | 1.173 | 1.251 | 2.245 | 7.217 |
| Potensi kredit REDD vs baseline BAU (ribu tCO₂e) | – | 198 | 212 | 395 | 1.310 |
| Potensi kredit REDD konservatif, di atas S1 (ribu tCO₂e) | – | 0 | 15 | 182 | 1.071 |
| **Porsi kredit BAU yang berasal dari perlindungan tingkat S1** | – | **100 %** | **93 %** | **54 %** | **18 %** |
| Kredit REDD terjual (ribu tCO₂e) | – | 166 | 179 | 334 | 1.059 |
| Kas penjualan (Rp miliar) | – | 16,4 | 29,5 | 110,4 | 619,8 |

Emisi "fisik" S2 − S1 belum dikalikan faktor eligible (kebocoran 0,9 × buffer 0,88 × porsi areal proyek 0,682 = 0,54). Potensi kredit sudah dikalikan. Kredit ARR baru muncul pada USD 35 (33 ribu tCO₂e). Semua angka kredit adalah **potensi model**, bukan kredit terverifikasi.

## 3. Sensitivitas prioritas (berpasangan S1–S2)

Desain: satu-per-satu di sekitar asumsi kerja, 41 level × (S1 + S2 pada USD 10, 20, 35) = 164 run. Klasifikasi lengkap ada di lembar "2 Klasifikasi robust".

| Parameter | Rentang uji | Deforestasi dihindari S2−S1, USD 20 (ha) | Temuan |
|---|---|---|---|
| **k patroli reguler** | 0 – 1 | **38 – 3.976** | **Paling menentukan.** k juga menentukan S1 (deforestasi 29.702 → 27.561 ha). Lihat 3.1 |
| **Efektivitas perlindungan** | 0,075 – 0,59 | **0 – 9.384** | Pada 0,075, loop karbon tidak dimulai (0 ha; NPV negatif) |
| **Kas non-karbon** | 0 – 6 miliar/th | 1.072 – 4.807 | Tidak monoton. Pada USD 35, dampak karbon justru **turun** (6.045 → 3.064 ha) bila kas non-karbon besar, karena S1 sudah lebih terlindungi. KUPS S1 2087: 5,7 → 51,2 |
| Dukungan material rehabilitasi | 0 – 201 juta | 1.072 – 1.282 | Terkunci pada laju realisasi historis 20,13 ha/th. Menambah hutan S1, tetapi juga sedikit menaikkan deforestasi absolut S1 karena stok hutan lebih besar |
| Biaya reaktivasi × reinvestasi KUPS | 12,5–50 juta × 0,5–1 | tidak berpengaruh | **KUPS S1 2087: 5,7 – 33,4.** Sepenuhnya ditentukan dua asumsi D. Tidak memengaruhi hutan |
| Waktu penerbitan dan pembayaran | 3–5 th; 0–1 th | 939 – 1.072 | Agak sensitif: setiap tahun penundaan mengurangi dampak ±6 % dan NPV ±16 % |
| Biaya MRV | ×0,5 – ×1,5 | 690 – 1.462 | **Sangat menentukan pada USD 10:** 270 → 78 → 0 ha |
| Biaya pengembangan (proksi tahunan) | 0 – 500 juta/th | tetap | Hanya NPV: 8,0 → 2,8 miliar |
| Hibah vs talangan | 3 varian | 1.006 – 1.072 | Kecil; pada USD 10: 78 → 48 ha. Talangan sesudah bagi hasil = hibah, karena pemulihan dari bagian mitra sendiri |
| Diskonto | 6 – 14 % | tetap | Hanya NPV: 16,7 / 8,0 / 4,4 miliar |

### 3.1 Temuan metodologis terpenting: loop karbon bertumpu pada kredit atas perlindungan tingkat S1

Sensitivitas k memperlihatkan bahwa **dampak karbon naik ketika S1 sendiri lebih terlindungi**. Pada USD 20: 38 ha (k = 0) → 1.072 ha (k = 0,5) → 3.976 ha (k = 1). Mekanismenya:

1. Kredit dihitung terhadap baseline BAU tanpa PS.
2. Patroli reguler S1 sudah menurunkan deforestasi di bawah baseline, sehingga menghasilkan potensi kredit (100 % pada USD 6; 93 % pada USD 10).
3. Kredit itu dijual dan menjadi kas LPHD.
4. Kas membiayai patroli tambahan.

Dengan akuntansi konservatif yang hanya mengkreditkan perlindungan di atas S1, loop tidak dapat dimulai (temuan F3 Fase 2). Artinya, **dampak S2 − S1 pada harga rendah–menengah bergantung pada diterimanya kredit atas perlindungan yang juga terjadi tanpa perdagangan karbon.** Ini isu additionality yang wajib dibahas, bukan sekadar catatan kaki.

### 3.2 Robust vs sensitif

**Relatif robust (arah tetap di semua uji satu-per-satu):**
- S2 tidak pernah menurunkan tutupan hutan dibanding S1.
- Pada USD 6 tidak ada kas LPHD dan tidak ada dampak.
- Dampak, kas, dan cakupan naik monoton terhadap harga.
- Kas karbon tidak menutup kebutuhan minimum LPHD rata-rata hingga USD 20 (cakupan ≤ 48 % di semua uji kecuali kas non-karbon besar). Pada USD 35, kebutuhan minimum tercukupi 36 dari 62 tahun.
- Jeda kas: tidak ada belanja karbon sebelum 2028–2032.
- Mitra menanggung seluruh biaya karbon sebelum surplus.
- Pendapatan rata-rata RT di S2 lebih rendah daripada S1. **Catatan:** arah ini ditentukan oleh asumsi kehilangan akses (pengali 1, kelas D), yang belum diuji di tahap ini. Bila pengali = 0, arahnya hampir pasti berbalik.

**Sensitif (besaran, kadang ambang):**
- k, efektivitas perlindungan, biaya MRV (terutama USD 10), kas non-karbon, dan parameter KUPS.
- NPV terhadap diskonto, biaya pengembangan, dan waktu penerbitan.

**Sensitif terhadap arah: tidak ada** di antara parameter prioritas, kecuali NPV inkremental. Nilainya negatif pada USD 6, dan negatif pada USD 10 bila efektivitas rendah atau biaya MRV tinggi.

## 4. Ketidakpastian yang masih memengaruhi interpretasi

1. **Verifikasi Vensim native belum ada.**
2. **S1 bertumpu pada asumsi D:** patroli reguler k dan ketersediaan logistik non-tunai, kelangsungan KUPS, rehabilitasi non-karbon, dan kas non-karbon. Hasil S1 dan S2 − S1 adalah konsekuensi asumsi, bukan dampak empiris.
3. **Additionality (3.1):** dampak S2 − S1 bergantung pada kredit atas perlindungan tingkat S1. Keberterimaannya oleh standar karbon tidak dimodelkan.
4. **Kehilangan akses** menentukan arah perubahan pendapatan RT. Ini asumsi D dan belum diuji di tahap ini; masuk Monte Carlo.
5. **NPV sementara:** biaya pengembangan dan material belum tersedia. Parameter biaya pengembangan juga berupa aliran konstan, belum dijadwalkan. **Harga impas tidak dihitung.**
6. **Data yang belum dikonfirmasi:** satuan Rp 260.000, upah patroli 2024–2025, roster 254, KUPS 2024–2025, dan harga ARR (tetap USD 20).
7. **Hasil satu-per-satu tidak menangkap interaksi** antarparameter, misalnya k × efektivitas × biaya MRV. Interaksi akan dicakup Monte Carlo berpasangan.

## 5. Langkah berikutnya (menunggu persetujuan)

- **Tahap 2:** Monte Carlo LHS berpasangan S1–S2 dan PRCC (`HASIL_MONTE_CARLO_PRCC.xlsx`).
  - Parameter: k, efektivitas, laju BAU, regenerasi, biaya MRV, waktu, pengali kehilangan akses, leakage, porsi areal proyek, buffer, kapasitas LPHD, biaya patroli, waktu penyesuaian, reaktivasi dan reinvestasi KUPS.
  - Kas non-karbon diperlakukan sebagai skenario terpisah, bukan distribusi.
- **Tahap 3:** benefit sharing B0–B4, R1, R2 pada S2 (USD 10, 20, 35) (`HASIL_BENEFIT_SHARING_FINAL.xlsx`). Model alokasi perlu dibangun di atas model dua skenario dengan cara yang sama seperti Fase 2.
- **Tahap 4:** `INTERPRETASI_HASIL_TESIS.md` dan `PERBANDINGAN_HASIL_4_VS_2_SKENARIO.md`.
- Makalah tidak disentuh sampai hasil dan status validasi diterima.
