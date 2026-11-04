# Laporan Verifikasi Fase 5

**Tanggal:** 4 November 2026

**Status:**
- Model `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` dibekukan (md5 `639083f9…`; tidak ada persamaan atau variabel baru).
- PySD 3.14.3; **Vensim native: BELUM DIVERIFIKASI NATIVE**.
- NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Referensi S1 berpasangan dipakai di semua konfigurasi S2.
- D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. Selisihnya adalah dekomposisi menurut asumsi model, **bukan identifikasi kausal empiris**.

## 1. Hasil verifikasi

Lembar 5 `HASIL_EKSPERIMEN_D0_D3.xlsx`.

| Uji | Hasil (selisih/nilai maks) | Status |
|---|---|---|
| D0 = S1 Fase 4 (190 variabel) | 0.00e+00 | LULUS |
| D2 USD10 = S2-C-J1 Fase 4 (190 variabel) | 0.00e+00 | LULUS |
| D2 USD20 = S2-C-J1 Fase 4 (190 variabel) | 0.00e+00 | LULUS |
| D2 USD35 = S2-C-J1 Fase 4 (190 variabel) | 0.00e+00 | LULUS |
| D1 tanpa kredit, MRV, kas penjualan | 0.00e+00 | LULUS |
| D1 jembatan = kerugian mitra diakui (hibah), sisa talangan 0 | 0.00e+00 | LULUS |
| D3 kredit (semua harga dan variasi) | 0.00e+00 | LULUS (kredit 0: tidak dipaksa) |
| Dekomposisi aditif D2−D0 = (D1−D0) + (D2−D1), semua indikator dan variasi | 6.10e-05 | LULUS (identitas aritmetis) |
| D0: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D1: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 4.56e-08 | LULUS |
| D2|10: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 4.56e-08 | LULUS |
| D3|10: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D3h|10: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D2|20: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 1.19e-07 | LULUS |
| D3|20: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D3h|20: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D2|35: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 9.54e-07 | LULUS |
| D3|35: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| D3h|35: cek kawasan/karbon/neraca LPHD/arus kas/referensi S1 (maks) | 6.05e-08 | LULUS |
| DT 0,0625 vs 0,03125 (D0): selisih hutan 2087 / NPV mitra (%) | 1.49e-01 | LULUS (< 2 %) |
| DT 0,0625 vs 0,03125 (D1): selisih hutan 2087 / NPV mitra (%) | 1.49e-01 | LULUS (< 2 %) |
| DT 0,0625 vs 0,03125 (D2|20): selisih hutan 2087 / NPV mitra (%) | 3.69e-01 | LULUS (< 2 %) |
| DT 0,0625 vs 0,03125 (D2|35): selisih hutan 2087 / NPV mitra (%) | 9.33e-02 | LULUS (< 2 %) |
| DT 0,0625 vs 0,03125 (D3|20): selisih hutan 2087 / NPV mitra (%) | 1.49e-01 | LULUS (< 2 %) |

## 2. Pemeriksaan per permintaan

| No | Pemeriksaan | Hasil |
|---|---|---|
| 1 | Kesetaraan D0 dengan S1 | Selisih 0 pada 190 variabel |
| 2 | Kesetaraan D2 dengan S2-C-J1 | Selisih 0 (USD 10/20/35) |
| 3 | Satuan dan referensi persamaan | Model tidak diubah. Hasil Fase 4 tetap berlaku: 0 referensi tak dikenal, 0 loop aljabar, satuan 933/933 konsisten (model utama) dan 960/960 (model alokasi). Penimpaan D1 dan D3 hanya mengganti nilai konstanta/variabel berdimensi sama (Dmnl, Year) |
| 4 | Neraca biaya dan pendapatan | Identitas arus kas ≤ 10⁻⁶ Rp; neraca LPHD ≤ 4·10⁻⁴ Rp; D1: jembatan = kerugian mitra diakui (selisih 0), sisa talangan 0; rekonsiliasi lengkap arus kas D2 di `AUDIT_AKADEMIK_FINAL_PWD.md` |
| 5 | Stok dan aliran ekologis | \|Check Total Kawasan\| ≤ 2·10⁻¹⁰ ha; \|Check Konservasi Karbon\| ≤ 7·10⁻⁸ |
| 6 | Timestep (argumen `time_step` PySD) | DT 0,0625 vs 0,03125: selisih hutan 2087 ≤ 0,003 %; NPV mitra ≤ 0,37 % |
| 7 | Konfigurasi Referensi S1 | Hutan Referensi S1 = D0 di semua run (selisih 0) |
| 8 | Keberlanjutan pembiayaan sesudah 2030 | Dilaporkan (indikator E10, F10, S3) |
| 9 | Kondisi ekstrem | Tanpa harga (Fase 4 E1/E1b); tanpa kredit (D1); tanpa jembatan (D3): semua berperilaku sesuai definisi |
| 10 | Rekonsiliasi dengan Fase 4 | D0 dan D2 identik dengan Fase 4. Kontras D2 − D0 sama dengan hasil S2 − S1 Fase 4 (deforestasi dihindari 287 / 454 / 4.954 ha) |

**Vensim native:** tidak tersedia di lingkungan ini. Status: **BELUM DIVERIFIKASI NATIVE** (Units Check dan pembandingan lintasan).

## 3. Temuan dokumentasi (bukan kesalahan persamaan)

Komentar parameter `Biaya per Hari Patroli` di berkas model masih menulis "Upah Rp130.000/orang-hari + logistik Rp130.000". Persamaan model sudah benar: upah Rp150.000 di variabel `Upah Harian Patroli Berbayar`, dan komponen non-upah diturunkan sebagai Rp110.000.

Model dibekukan sehingga komentar tidak diubah. Koreksi dicatat di register parameter dan harus diterapkan pada versi model berikutnya (bila ada).

## 4. Kesimpulan

Konfigurasi D0–D3 lulus semua pemeriksaan yang dapat dijalankan di PySD. Monte Carlo baru tidak diperlukan, karena dekomposisi deterministik dan sensitivitas terarah (10 variasi × 3 harga) sudah menjawab pertanyaan atribusi, dan hasilnya konsisten di semua variasi.
