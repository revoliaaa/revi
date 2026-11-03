# Laporan Verifikasi Model Final (Fase 4, Tahap 1–2)

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD.mdl`. Turunan dari `DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl` (828 variabel), yang tidak ditimpa.

**Perangkat:** PySD 3.14.3, Euler, DT 0,0625, horizon 2024–2087.

**Status:** **terverifikasi PySD.** *Units Check* dan run native Vensim belum dilakukan.

**Tanggal:** 3 November 2026

## 1. Ringkasan keputusan

**SIAP BERSYARAT untuk Tahap 3 (simulasi deterministik).**

| Kelompok | Hasil |
|---|---|
| Uji | **34 LULUS**, **1 GAGAL minor** (K7), **1 BELUM DILAKUKAN** (V0c Vensim), 1 dilaporkan (W5) |
| Model | 937 variabel, 16 View |
| Analisis statis | 0 referensi tak dikenal, 0 loop aljabar; satuan 933/933 persamaan konsisten |

Satu-satunya uji yang gagal (K7) hanya berlaku bila kas non-karbon > 0:
- galat atribusinya kumulatif +163 tCO₂e (0,05 % kredit);
- kredit bersih tetap di bawah mitigasi berpasangan;
- konfigurasi dasar (kas non-karbon 0) tidak terdampak.

Syarat untuk melanjutkan:
1. Run sensitivitas dengan kas non-karbon > 0 harus melaporkan kredit bersama mitigasi berpasangan.
2. Hasil hanya disebut "terverifikasi PySD" sampai peneliti menjalankan Vensim native.

## 2. Perubahan Tahap 1

| Kelompok | Perubahan | Variabel |
|---|---|---|
| PWD-U upah | Upah patroli Rp150.000/HOK; komponen non-upah turunan (Rp110.000, asumsi); logistik swadaya non-tunai = 9,17 × komponen non-upah | 2 diubah, 2 baru |
| PWD-K kredit endogen | Rantai Referensi S1 (78 variabel); kredit mode 2; saldo mitigasi bertanda; buffer; penggantian *reversal*; atribusi non-karbon lebih dulu; pelaporan potensi BAU/Referensi S1 | 5 diubah, 92 baru |
| PWD-C jembatan | Default mekanisme C (J1, 2026–2030); jembatan mengisi kekurangan sesudah patroli LPHD; kebutuhan LPHD bruto | 1 diubah, 3 baru |
| PWD-M MRV | Aturan penghentian prospektif (opsional): rerata kas penjualan 3 th < biaya MRV tetap sesudah 2033 → proyek berhenti permanen; penundaan monitoring | 2 diubah, 11 baru |
| PWD-T talangan | Biaya modal dibatasi 100 % pokok dan hanya sampai akhir tenor (2045); penghapusan opsional dengan pengakuan kerugian mitra | 2 diubah, 6 baru |

Rincian: `LAPORAN_KOREKSI_UPAH_DAN_BIAYA_PATROLI.md` dan `LAPORAN_KREDIT_ENDOGEN_DAN_ADDITIONALITY.md`.

**Struktur yang dipertahankan:**
- 16 View;
- seluruh subsistem sosial-ekonomi dan kelembagaan (KUPS, tenaga kerja, pendapatan RT, kapasitas LPHD);
- parameter ekologis terkalibrasi.

**Konfigurasi skenario:**

| Skenario | Konfigurasi |
|---|---|
| S1 | `Skenario Kebijakan` = 1. Semua struktur karbon dan jembatan bernilai 0 karena dikalikan `Switch Karbon` |
| S2 | `Skenario Kebijakan` = 2 + default mekanisme C |
| Mekanisme A | Mode 0, tanpa jembatan |
| Mekanisme B | Mode 2, tanpa jembatan |

## 3. Kegagalan yang ditemukan dan tindakannya

| Kode | Uji | Penyebab | Kelas | Tindakan | Status akhir |
|---|---|---|---|---|---|
| F4-1 | K3 | *Reversal*: hutan yang diselamatkan jembatan kembali terdeforestasi sesudah ±2052; `MAX(0, ·)` per tahun mengabaikannya, sehingga kredit 1,30× mitigasi berpasangan pada USD 6 | **Kesalahan model** | Saldo mitigasi bertanda, debit dibawa, buffer, kredit pengganti dibeli (biaya nyata) | LULUS |
| F4-2 | K7 | Jembatan mengurangi kebutuhan LPHD, sehingga dana non-karbon tidak terbelanjakan di S2 tetapi terbelanjakan di S1 (galat acuan 2.600 tCO₂e/th) | **Kesalahan model** (atribusi) | Kebutuhan bruto; jembatan mengisi sisa; atribusi non-karbon lebih dulu (galat turun ke ≤ 327 tCO₂e/th) | **GAGAL minor** (kumulatif +163 tCO₂e) |
| F4-3 | T1 | Pembatas biaya modal memakai stok awal langkah (lebih 1,1 %) | Kesalahan model (numerik) | Pembatas eksak | LULUS |
| F4-4 | E1b | Kas 3·10⁻⁶ Rp pada harga 0; toleransi terlalu ketat | Kesalahan kriteria | Toleransi 1 Rp | LULUS |
| F4-5 | R1 | Indikator kebutuhan LPHD berubah karena F4-2 (perubahan definisi terdaftar) | Kriteria basi | Indikator kebutuhan dikecualikan, selisihnya dilaporkan (16,1 %); semua variabel lain identik | LULUS |
| F4-6 | K3/K7 | Sisa *reversal* 30 tCO₂e (jeda satu DT di akhir horizon); galat positif kecil sesudah 2046 | Toleransi | K3: sisa ≤ 0,5 % *reversal*. K7: galat kumulatif dan kredit bersih | K3 LULUS, K7 GAGAL minor |

Revisi kriteria (F4-4 s.d. F4-6) dilakukan sesudah diagnosis, bukan untuk meloloskan hasil. Kegagalan K7 tetap dilaporkan sebagai GAGAL.

## 4. Hasil uji lengkap

| Kode | Uji | Status | Bukti |
|---|---|---|---|
| V0a | Parsing PySD | **LULUS** | read_vensim berhasil; 937 variabel; 16 View |
| V0b | Referensi dan loop aljabar | **LULUS** | referensi tak dikenal 0; loop aljabar 0; pemakai Switch Karbon 14 (9 lama + jembatan + 4 rantai kredit/pelaporan PWD-K) |
| V0c | Units Check dan run native Vensim | **BELUM DILAKUKAN** | Vensim tidak tersedia di lingkungan ini; harus dijalankan peneliti |
| V18 | Konsistensi dimensional (pemeriksa statis) | **LULUS** | 933 persamaan konsisten, 0 bermasalah |
| R1 | Reproduksi Fase 3 dengan upah lama dan mode kredit lama (kriteria direvisi: indikator kebutuhan dikecualikan) | **LULUS** | selisih relatif maks S1/A20/C20 = 0.0e+00/0.0e+00/0.0e+00 pada semua variabel fisik, keuangan, dan sosial; indikator kebutuhan LPHD C20 berbeda 16.1 % karena perubahan definisi terdaftar (kebutuhan bruto, tidak lagi dikurangi jembatan) |
| W1 | Upah patroli historis Rp150.000/HOK; HOK dan biaya total tidak berubah | **LULUS** | S1: upah 2024 Rp379.950.000, 2025 Rp451.650.000, total Rp831.600.000; HOK 2.533/3.011; biaya total historis Rp1.441.440.000; C20: upah 2024 Rp379.950.000, 2025 Rp451.650.000, total Rp831.600.000; HOK 2.533/3.011; biaya total historis Rp1.441.440.000 |
| W2 | Upah adalah komponen biaya total (tidak ditambahkan) | **LULUS** | upah ≤ biaya patroli total di semua t; rasio upah/biaya = 0.576923 (= 150/260 = 0.576923) di S1, A20, C20, C35 |
| W3 | Nilai non-tunai Rp150.000/HOK dan logistik turunan; tidak masuk pendapatan RT | **LULUS** | logistik swadaya = 9,17 × Rp110.000 = Rp1.008.700/anggota/th (sebelumnya Rp1.192.050); nilai tenaga non-tunai 2030 = 1.505,5 HOK × Rp150.000 = Rp225.825.000; logistik ×10 → /Δ pendapatan RT/ maks 0.0e+00 |
| W4 | Identitas HOK berupah + sukarela = total; identitas patroli | **LULUS** | Kesempatan Kerja PS = HOK berupah + sukarela; Check Identitas Patroli = 0 (S1, A20, C20, C35) |
| W5 | Dampak koreksi upah (S1, terhadap upah lama) | **DILAPORKAN** | pendapatan program per RT 2024: Rp7.765 → Rp8.960; upah kegiatan PS 2025: Rp391.430.000 → Rp451.650.000; hutan 2087 tidak berubah (0,000000 ha) |
| K1 | Rantai Referensi S1 = S1 aktual pada run S1 | **LULUS** | /hutan ref − aktual/ maks 0.0e+00 ha; /emisi bersih biomassa ref − aktual/ maks 0.0e+00 tCO2e/th |
| K2 | B (tanpa jembatan): Referensi S1 = aktual, kredit 0 | **LULUS** | kredit maks B20 0.0e+00, B35 0.0e+00 tCO2e/th: tanpa modal awal tambahan siklus tidak dimulai (diagnostik dipertahankan) |
| K3 | Kredit C endogen: Σ kredit = Σ mitigasi bersih − saldo; mitigasi ≤ berpasangan; reversal diselesaikan buffer + pembelian pengganti (sisa ≤ 0,5 % karena jeda satu DT di akhir horizon) | **LULUS** | USD6: kredit REDD 68.835; mitigasi eligible bersih (bertanda) 44.111; mitigasi deforestasi berpasangan eligible 52.856; reversal 24.724: ditutup buffer 9.387 + kredit pengganti 15.307; kredit bersih sesudah penyelesaian 44.141 ≤ mitigasi 44.111; /emisi ref − S1/ 5.8e-11; USD10: kredit REDD 68.835; mitigasi eligible bersih (bertanda) 44.111; mitigasi deforestasi berpasangan eligible 52.856; reversal 24.724: ditutup buffer 9.387 + kredit pengganti 15.307; kredit bersih sesudah penyelesaian 44.141 ≤ mitigasi 44.111; /emisi ref − S1/ 5.8e-11; USD15: kredit REDD 77.964; mitigasi eligible bersih (bertanda) 53.330; mitigasi deforestasi berpasangan eligible 62.320; reversal 24.634: ditutup buffer 10.631 + kredit pengganti 13.967; kredit bersih sesudah penyelesaian 53.365 ≤ mitigasi 53.330; /emisi ref − S1/ 5.8e-11; USD20: kredit REDD 100.666; mitigasi eligible bersih (bertanda) 74.450; mitigasi deforestasi berpasangan eligible 83.795; reversal 26.216: ditutup buffer 13.727 + kredit pengganti 12.441; kredit bersih sesudah penyelesaian 74.498 ≤ mitigasi 74.450; /emisi ref − S1/ 5.8e-11; USD35: kredit REDD 897.337; mitigasi eligible bersih (bertanda) 897.337; mitigasi deforestasi berpasangan eligible 898.155; reversal -0: ditutup buffer -0 + kredit pengganti 0; kredit bersih sesudah penyelesaian 897.337 ≤ mitigasi 897.337; /emisi ref − S1/ 5.8e-11 |
| K4 | Tanpa hitung ganda REDD dan ARR | **LULUS** | REDD (bertanda) + ARR (≥ 0) = pengurangan biomassa bersih terhadap Referensi S1 di semua t (C6, C10, C20, C35) |
| K5 | Konservasi kredit (diajukan → terbit → terjual/stok/kedaluwarsa) | **LULUS** | stok akhir = Σ terbit − Σ terjual − Σ kedaluwarsa (REDD, ARR); C20: diajukan − terbit = 0 (antrean 3 th terakhir); C35: diajukan − terbit = 67.500 (antrean 3 th terakhir); A20: diajukan − terbit = 8.813 (antrean 3 th terakhir) |
| K6 | Kredit konservatif ≤ potensi terhadap BAU | **LULUS** | C20: Σ kredit REDD 100.666 ≤ potensi BAU 271.969 tCO2e |
| K7 | Kas non-karbon tidak dikreditkan (kriteria direvisi: galat acuan kumulatif konservatif dan kredit bersih) | **GAGAL** | kas non-karbon Rp3 M/th: galat emisi Referensi S1 − S1 berpasangan per tahun ∈ [-327; 93] tCO2e/th, kumulatif 163 tCO2e (negatif = acuan lebih protektif = konservatif); penyimpangan positif sesudah 2046 berjumlah 2,046 tCO2e (atribusi dana yang dapat dipertukarkan); kredit bruto 322.115, kredit bersih sesudah reversal 300.059 ≤ mitigasi berpasangan 314.668 |
| J1 | Pembiayaan jembatan sesuai kegiatan aktual | **LULUS** | HOK jembatan ≤ kebutuhan tambahan; total patroli ≤ kapasitas; Rp = HOK × 260.000; hanya 2026–2030; S1 = 0; C20: Σ jembatan Rp3.914.300.000, HOK 15.055; C6: Σ jembatan Rp3.914.300.000, HOK 15.055; C35: Σ jembatan Rp3.914.300.000, HOK 15.055 |
| N1 | Neraca kas LPHD dan mitra | **LULUS** | /Check Identitas Arus Kas/ maks 9.5e-07 Rp/th di 11 run; saldo ≥ 0; saldo karbon ≤ saldo |
| N2 | Konsistensi NPV | **LULUS** | NPV inkremental S1 = 0.0e+00; /NPV(C20) − NPV(S1) − NPV inkremental(C20)/ = 2.15e-06 Rp; NPV keseluruhan S1 = −PV pembiayaan historis = Rp-1.310.893.298 |
| N3 | S1 = S2 (fisik dan sosial) sebelum kegiatan proyek pertama (2026) | **LULUS** | selisih maks 2024–2025 pada 7 variabel = 0.0e+00 |
| M1 | Penghentian MRV prospektif (B20) | **LULUS** | proyek dihentikan t = 2033.0625; biaya MRV sesudahnya 0; biaya MRV ditanggung mitra Rp2.894.247.632 (vs Rp22.771.504.226 tanpa aturan) |
| M2 | Penghentian MRV pada C20 hanya sesudah penerimaan < biaya | **LULUS** | t henti = 2054.1875; NPV mitra Rp-1.354.264.687 (tanpa aturan Rp-1.586.631.997); defisit MRV 2087 Rp269.543.019 (tanpa aturan Rp16.467.263.120) |
| M3 | Penundaan monitoring MRV | **LULUS** | biaya monitoring 2024–2025 = 0 bila ditunda ke 2026; Σ MRV Rp28.401.286.293 vs Rp28.809.592.266 |
| T1 | Biaya modal dibatasi (perbaikan T-a) | **LULUS** | T_C6_bm10: pokok Rp3.914.300.000, biaya modal Rp3.914.300.000, sisa 2087 Rp7.828.600.000; T_C10_sesudah_bm10: pokok Rp3.914.300.000, biaya modal Rp3.914.300.000, sisa 2087 Rp6.523.222.874 (Fase 3: sisa C6 bm10 = Rp1.344 M) |
| T2 | Penghapusan talangan dengan pengakuan kerugian | **LULUS** | sisa sesudah 2045 = 0.0e+00; kerugian mitra diakui Rp7.828.600.000; identitas pokok + biaya modal − pemulihan − penghapusan − sisa = 5.7e-06 Rp; NPV mitra sama dengan tanpa penghapusan (-5.476.348.929 vs -5.476.348.929) |
| E1 | Harga 0 tanpa jembatan → S2 = S1 | **LULUS** | selisih maks 0.0e+00 |
| E1b | Harga 0 dengan jembatan: kas penjualan 0, mitra menanggung jembatan + MRV | **LULUS** | Δ hutan 2087 = 175,7 ha (efek jembatan saja); NPV mitra Rp-7.485.931.308 |
| E2 | k = 0: patroli reguler S1 = 0 sesudah 2025 | **LULUS** | kredit C20 (k = 0) = 84.466 tCO2e |
| E3 | k = 1: patroli reguler = 3.011 ≤ kapasitas | **LULUS** | HOK reguler 2030 = 3.011,0 |
| E4 | Kas non-karbon sangat besar | **LULUS** | belanja ≤ kebutuhan; intensitas maks 1.000; saldo 2087 Rp60.366.283.690.665 |
| E5 | Harga USD 500 | **LULUS** | stok ≥ 0; intensitas maks 1.000; hutan 2087 89.944 ha |
| E6 | Efektivitas 0: patroli tidak mengubah deforestasi; kredit REDD 0 | **LULUS** | Δ deforestasi 0.0e+00 ha; kredit REDD 0.0e+00 |
| U6 | Langkah waktu 0,0625 vs 0,03125 | **LULUS** | S1 Total Hutan 0.000 %; S1 NPV Mitra 0.000 %; S1 Kredit Karbon Diajukan 0.000 %; C20 Total Hutan 0.000 %; C20 NPV Mitra 0.004 %; C20 Kredit Karbon Diajukan 0.000 % |
| P1 | Urutan kausal jembatan → patroli → deforestasi → kredit → kas → patroli LPHD (C20) | **LULUS** | patroli jembatan 2026.0; deforestasi C20 < S1 2026.0625; kredit diajukan 2026.0625; kredit terbit 2029.0625; kas penjualan 2029.125; kas LPHD karbon 2034.0625; patroli kas LPHD 2034.125 |
| P2 | Putus loop dana LPHD → patroli (C35) | **LULUS** | Δ hutan 2087: 4.842 ha → 220 ha (sisa = efek jembatan + rehabilitasi) |
| P3 | Harga naik → hutan 2087 tidak turun (C) | **LULUS** | 82.975 / 82.975 / 83.016 / 83.112 / 87.641 ha (USD 6–35) |

## 5. Uji yang diminta instruksi bagian J dan pemetaannya

| Permintaan | Uji |
|---|---|
| Parsing PySD | V0a |
| Referensi dan loop aljabar | V0b |
| Dimensional | V18 (pemeriksa statis); V0c Vensim belum |
| Konservasi stok hutan dan karbon | K1, `Check Total Kawasan`, `Check Konservasi Karbon` (U16 Fase 2, struktur tidak berubah); E5 |
| Neraca kas LPHD dan mitra | N1 |
| Rekonsiliasi patroli historis | W1, N3 |
| Identitas HOK berupah dan sukarela | W4 |
| Konsistensi biaya patroli dan upah | W2, W3 |
| Konservasi kredit karbon | K4, K5 |
| Kesesuaian jembatan dengan kegiatan aktual | J1 |
| Kondisi ekstrem | E1–E6 |
| Langkah waktu | U6 |
| Kausal kredit → kas → patroli → deforestasi | P1, P2, P3 |
| Pembiayaan dan penghentian MRV | M1, M2, M3, T1, T2 |
| Konsistensi NPV | N2 |
| Units Check Vensim native dan perbandingan dengan PySD | **BELUM DILAKUKAN** (V0c); skrip pembanding `bandingkan_vensim_pysd.py` tersedia dari Fase 2 |

## 6. Catatan perilaku dari uji (bukan hasil penelitian final)

- **Kronologi C20** (P1): patroli jembatan 2026 → deforestasi S2 < S1 sejak 2026,06 → kredit diajukan 2026,06 → terbit 2029,06 → kas penjualan 2029,13 → kas LPHD 2034,06 → patroli kas LPHD 2034,13.
- **Aturan penghentian MRV:**
  - B20: berhenti 2033,06, sehingga beban MRV mitra turun dari Rp22,8 M menjadi Rp2,9 M.
  - C20: berhenti 2054,19; NPV mitra membaik dari −Rp1,59 M menjadi −Rp1,35 M; defisit MRV 2087 turun dari Rp16,5 M menjadi Rp0,27 M.
- **Biaya modal 10 % pada USD 6:** sisa talangan dibatasi pada pokok + 100 % (Rp7,83 M), bukan Rp1.344 M seperti di Fase 3. Penghapusan pada 2045 mencatat kerugian mitra Rp7,83 M tanpa mengubah arus kas.
- **Jembatan saja pada harga 0** (E1b): Δ hutan 2087 = +176 ha; NPV mitra −Rp7,49 M.

## 7. Batasan yang tetap berlaku

1. Vensim native belum dijalankan.
2. Parameter kelas D (k, efektivitas, biaya Rp260.000, biaya MRV, jembatan, KUPS) harus diperlakukan sebagai rentang pada Tahap 3–4.
3. K7: kredit pada run dengan kas non-karbon > 0 harus dibandingkan dengan mitigasi berpasangan.
4. Varian lama yang tetap tidak boleh dipakai sebagai hasil: mode kredit 1 (porsi) dan varian switch konservatif lama.
