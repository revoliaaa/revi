# Analisis Alokasi Manfaat dan Kompensasi

**Tanggal:** 4 November 2026

**Data:** `HASIL_BENEFIT_SHARING_PWD.xlsx`. **Grafik:** `GRAFIK_MONTE_CARLO_DAN_BENEFIT_SHARING/A1`.

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

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl` = v2 ditambah dana fleksibel dan kompensasi. Mekanisme C, J1, Referensi S1 berpasangan.

**Alternatif:**

| Alternatif | Patroli | Rehabilitasi | Kebakaran | KUPS | Kompensasi |
|---|---|---|---|---|---|
| B0 | 0,30 | 0,15 | 0,10 | 0,20 | 0 |
| B1 | 0,40 | 0,20 | 0,10 | 0,20 | 0,10 |
| B2 | 0,30 | 0,15 | 0,10 | 0,25 | 0,20 |
| B3 | 0,20 | 0,10 | 0,10 | 0,45 | 0,15 |
| B4 | 0,20 | 0,10 | 0,10 | 0,25 | 0,35 |
| R1 | 0,40 | 0,20 | 2/15 | 1/15 | 0,20 |
| R2 | 0,50 | 0,15 | 0,10 | 0,05 | 0,20 |

- **B0** = alokasi proporsional dasar: porsi di atas adalah porsi dari seluruh dana tersedia, ditambah operasional 0,10 dan kelembagaan 0,15.
- **B1–B4, R1, R2:** operasional dan kelembagaan tetap proporsional. Sisanya menjadi dana fleksibel yang dibagi dengan porsi di atas, masing-masing dibatasi kebutuhan pos.
- **Kompensasi** dibayar dari saldo LPHD (tercatat di `Penggunaan Dana Desa`) dan diterima RT pemegang garapan yang terdampak.

**Konfigurasi run:**
- USD 10, 20, 35;
- sensitivitas pada USD 20: k 0/1, efektivitas 0,2/0,6, akses 0/1,5, biaya patroli Rp150.000/300.000, JP, MRV ×1,5.

**Identitas anggaran** (lembar 6), seluruhnya terpenuhi di 91 run:
- Σ alokasi ≤ dana tersedia (selisih minimum −2·10⁻⁶ Rp);
- penggunaan ≤ dana tersedia;
- saldo ≥ 0;
- neraca saldo seimbang (selisih ≤ 4·10⁻⁴ Rp);
- kompensasi dibayar = diterima RT terdampak.

Kompensasi tidak memakai dana yang sudah dibelanjakan untuk kegiatan lain.

## 2. Hasil

**USD 10:** semua alternatif identik, karena kas karbon tidak pernah sampai ke LPHD (defisit MRV dan talangan menyerap seluruh surplus). Kompensasi = 0. **Alokasi tidak berarti tanpa kas.**

**USD 20 (deterministik)**

| Indikator | B0 | B1 | B2 | B3 | B4 | R1 | R2 |
|---|---|---|---|---|---|---|---|
| Deforestasi dihindari S2−S1 (ha) | 454 | 454 | 392 | 348 | 348 | 454 | 555 |
| FTE berupah | 2,7 | 2,6 | 1,8 | 1,3 | 1,3 | 2,7 | 3,3 |
| Upah kegiatan PS (Rp juta/th) | 109,5 | 104,2 | 75,6 | 55,4 | 55,4 | 109,5 | 136,0 |
| KUPS aktif 2087 | 6,1 | 6,0 | 6,0 | 6,1 | 6,0 | 5,9 | 6,0 |
| Penerimaan anggota KUPS (Rp juta/th) | 17,1 | 16,8 | 16,9 | 17,5 | 16,8 | 16,2 | 16,2 |
| Pendapatan bersih per RT bergantung (Rp ribu/th) | 41.195,6 | 41.198,7 | 41.208,1 | 41.211,0 | 41.215,8 | 41.201,9 | 41.190,9 |
| Pendapatan bersih RT terdampak/pemegang garapan (Rp ribu/th) | 40.952,0 | 40.959,7 | 40.990,5 | 41.004,0 | 41.015,8 | 40.967,6 | 40.932,8 |
| Kehilangan per RT terdampak (Rp ribu/th) | 407,7 | 407,7 | 377,4 | 355,4 | 355,4 | 407,7 | 451,0 |
| Kompensasi per RT terdampak (Rp ribu/th) | 0,0 | 7,8 | 13,4 | 8,9 | 20,8 | 15,6 | 19,1 |
| Kompensasi / kehilangan total (%) | 0,0 | 1,9 | 3,5 | 2,4 | 5,7 | 3,8 | 4,4 |
| Kompensasi / tambahan kehilangan S2−S1 (%) | 0,0 | 3,5 | 7,0 | 5,3 | 12,4 | 7,1 | 7,1 |
| Kapasitas LPHD 2087 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 |
| Cakupan kebutuhan pengelolaan 2030–2055 (%) | 5,2 | 4,8 | 3,7 | 3,4 | 2,8 | 4,5 | 5,6 |
| NPV mitra inkremental (Rp M) [SEMENTARA] | -0,27 | -0,27 | -0,48 | -0,67 | -0,67 | -0,27 | -0,02 |

**USD 35 (deterministik)**

| Indikator | B0 | B1 | B2 | B3 | B4 | R1 | R2 |
|---|---|---|---|---|---|---|---|
| Deforestasi dihindari S2−S1 (ha) | 4.954 | 4.954 | 1.114 | 553 | 553 | 4.954 | 6.443 |
| FTE berupah | 17,4 | 16,4 | 8,8 | 4,4 | 4,4 | 17,4 | 23,7 |
| Upah kegiatan PS (Rp juta/th) | 694,9 | 656,1 | 354,5 | 179,3 | 179,3 | 694,9 | 966,4 |
| KUPS aktif 2087 | 50,4 | 37,8 | 8,1 | 8,0 | 6,8 | 13,6 | 19,4 |
| Penerimaan anggota KUPS (Rp juta/th) | 24,7 | 22,2 | 21,4 | 24,5 | 19,9 | 18,4 | 18,8 |
| Pendapatan bersih per RT bergantung (Rp ribu/th) | 41.080,6 | 41.100,7 | 41.176,1 | 41.200,7 | 41.220,1 | 41.122,0 | 41.047,5 |
| Pendapatan bersih RT terdampak/pemegang garapan (Rp ribu/th) | 40.580,3 | 40.631,4 | 40.861,1 | 40.952,1 | 41.000,7 | 40.683,6 | 40.453,6 |
| Kehilangan per RT terdampak (Rp ribu/th) | 837,1 | 837,1 | 598,6 | 452,4 | 452,4 | 837,1 | 1.144,5 |
| Kompensasi per RT terdampak (Rp ribu/th) | 0,0 | 51,7 | 71,5 | 36,5 | 85,2 | 103,5 | 150,6 |
| Kompensasi / kehilangan total (%) | 0,0 | 6,2 | 12,3 | 8,1 | 18,9 | 12,4 | 12,5 |
| Kompensasi / tambahan kehilangan S2−S1 (%) | 0,0 | 6,2 | 15,9 | 13,4 | 31,3 | 12,3 | 15,3 |
| Kapasitas LPHD 2087 | 0,87 | 0,87 | 0,50 | 0,50 | 0,50 | 0,87 | 0,93 |
| Cakupan kebutuhan pengelolaan 2030–2055 (%) | 38,1 | 35,2 | 21,6 | 14,7 | 12,2 | 32,4 | 45,5 |
| NPV mitra inkremental (Rp M) [SEMENTARA] | 6,66 | 6,66 | 4,14 | 2,78 | 2,78 | 6,66 | 9,09 |

## 3. Uji R1

**Kriteria** (ditetapkan sebelum hasil): R1 lulus bila pendapatan bersih RT terdampak R1 > B0 **dan** deforestasi dihindari R1 tidak lebih buruk dari B0 (toleransi 1 ha). Hasil R1 model empat skenario lama tidak dipakai.

| Variasi | Harga | Δ pendapatan RT terdampak R1 − B0 (Rp/th) | Δ deforestasi dihindari R1 − B0 (ha) | Δ penerimaan anggota KUPS R1 − B0 (Rp juta/th) | Hasil uji |
|---|---|---|---|---|---|
| dasar | USD 10 | 0 | 0 | 0,00 | TIDAK LULUS |
| dasar | USD 20 | 15.605 | 0 | -0,90 | LULUS |
| dasar | USD 35 | 103.265 | 0 | -6,27 | LULUS |
| k 0 | USD 20 | 11.584 | 0 | -0,67 | LULUS |
| k 1 | USD 20 | 24.025 | 0 | -1,36 | LULUS |
| efektivitas 0,2 | USD 20 | 93 | 0 | -0,01 | LULUS |
| efektivitas 0,6 | USD 20 | 80.998 | 0 | -4,43 | LULUS |
| akses 0 | USD 20 | 3.624 | 58 | -0,77 | LULUS |
| akses 1,5 | USD 20 | 15.605 | 0 | -0,90 | LULUS |
| biaya patroli 150.000 | USD 20 | 99.234 | 0 | -5,85 | LULUS |
| biaya patroli 300.000 | USD 20 | 9.216 | 0 | -0,53 | LULUS |
| jembatan JP | USD 20 | 60.886 | 0 | -3,54 | LULUS |
| biaya MRV ×1,5 | USD 20 | 7.897 | 0 | -0,46 | LULUS |

**Bacaan:**
- R1 lulus pada 12 dari 13 konfigurasi. Satu-satunya yang tidak lulus adalah USD 10, karena di sana tidak ada kas untuk dialokasikan.
- **Penyebab protektifnya:** dengan dana fleksibel = 75 % dana tersedia, porsi R1 untuk patroli, rehabilitasi, dan kebakaran sama dengan B0 (0,30 / 0,15 / 0,10 dari dana tersedia). Kompensasi R1 diambil seluruhnya dari porsi KUPS (0,20 → 0,05 dari dana tersedia). Jadi perlindungan R1 = B0 menurut konstruksi.
- **Biaya R1 ditanggung KUPS:** penerimaan anggota KUPS turun Rp0,9 juta/th (USD 20) dan Rp6,3 juta/th (USD 35). KUPS aktif 2087 pada USD 35 turun dari 50,4 menjadi 13,6.
- **Besaran kompensasi R1** hanya 3,8 % (USD 20) dan 12,4 % (USD 35) dari kehilangan akses total, atau 7,1 % dan 12,3 % dari tambahan kehilangan S2 − S1.

## 4. Trade-off antaralternatif

| Alternatif | Dampak |
|---|---|
| **R2** (patroli 0,5) | Perlindungan tertinggi (+101 ha USD 20; +1.490 ha USD 35 dibanding B0) dan NPV mitra tertinggi. Tetapi kehilangan akses per RT terdampak juga tertinggi, sehingga pendapatan RT terdampak lebih rendah daripada B0 walau ada kompensasi |
| **B4** (kompensasi 0,35) | Pendapatan RT terdampak tertinggi (+64 ribu USD 20; +420 ribu USD 35 dibanding B0). Tetapi perlindungan turun tajam (USD 35: 553 vs 4.954 ha), siklus pembiayaan mandiri USD 35 terputus, dan kapasitas LPHD tetap 0,50 |
| **B2, B3** | Melemahkan perlindungan pada USD 35 (1.114 dan 553 ha). Tambahan KUPS kecil |
| **B1** | Hampir sama dengan B0 dengan kompensasi kecil (1,9–6,2 % kehilangan) |

## 5. Kesimpulan alokasi

1. **Tidak ada alternatif yang memaksimalkan semua tujuan.** Perlindungan hutan, penerimaan KUPS, dan kompensasi bersaing pada dana LPHD yang sama.
2. **R1 memenuhi syarat uji** (pendapatan RT terdampak naik tanpa memperburuk perlindungan) pada USD 20–35, **dengan biaya pada KUPS**. Klaim lama bahwa R1 unggul tanpa trade-off tidak berlaku.
3. **Kompensasi maksimum** yang diuji hanya menutup 18,9 % kehilangan total (B4, USD 35). Kompensasi dari dana LPHD tidak cukup untuk menetralkan kehilangan akses menurut asumsi model.
4. Hasil berlaku untuk tujuh alternatif ini dan agregat 25 HD. **Bukan** alokasi optimal untuk setiap desa.
