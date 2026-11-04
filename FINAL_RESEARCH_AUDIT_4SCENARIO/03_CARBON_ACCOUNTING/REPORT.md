# 03 — Akuntansi Karbon dan Adisionalitas

Data:
- `carbon_accounting_A1.csv`: rantai kredit per harga.
- `diagnostic_A2_additional_to_S2_rerun.csv`: rerun diagnostik.

**Semua kuantitas di sini adalah kredit model, bukan VCU atau kredit terverifikasi.**

## Struktur perhitungan kredit di model (dibaca dari `.mdl`)

```
Pengurangan Emisi REDD Bruto   = MAX(0, MIN(Emisi Def. Biomassa Baseline − Emisi Def. Biomassa, Pengurangan Emisi Biomassa))
Pengurangan Emisi Eligible REDD = Bruto × (1 − 0,10 kebocoran) × (1 − 0,12 buffer) × 0,682 porsi PA
Kredit REDD Diajukan           = Eligible × Switch Karbon × Switch Periode Kredit × (1 − SwitchKonservatif × (1 − Porsi Mitigasi Adisional thd S2)) × Faktor Rekonsiliasi (=1)
Kredit REDD Terbit             = DELAY FIXED(Diajukan, 3 th)
Terjual                        = stok belum terjual × 0,7/th;  kedaluwarsa 0,1/th
```

| Unsur | Status | Catatan |
|---|---|---|
| 1. Pengurangan emisi fisik | VERIFIED | Emisi deforestasi biomassa S1 − S4 |
| 2. Kontrafaktual kebijakan | VERIFIED | S1 (PS berhenti 2024) |
| 3. Baseline kredit | **INCONSISTENT dengan kaidah adisionalitas** | Deret "Baseline" di model = run S1 (selisih 0). Dengan Switch Baseline Kredit Konservatif = 0, pengurangan akibat patroli swadaya dan pembiayaan awal ikut dikreditkan |
| 4. Adisionalitas | CONDITIONAL / berisiko | 24 dari 25 HD ber-SK 2017–2020, sebelum proyek 2024. Porsi kredit dari efek PS 68 % dan dari pembiayaan awal 11 % (USD 10) |
| 5. Kebocoran | CONSISTENT | 10 % tetap; tidak dimodelkan dinamis |
| 6. Buffer non-permanen | CONSISTENT | 12 % (PDD; ex-ante, belum divalidasi Verra). Pembalikan (reversal) tidak dimodelkan |
| 7. Pembatasan areal proyek | CONDITIONAL | Proporsi 0,682 berbasis aktivitas loss Hansen (provisional). Pembanding dokumentasi: 0,541–0,903 |
| 8. Jeda verifikasi/penerbitan | VERIFIED | 3 tahun; penerimaan pertama setelah 2027 |
| 9. Penjualan | VERIFIED | 70 %/th dari stok; kedaluwarsa 10 %/th. Pada USD 10, 56.130 tCO₂e kedaluwarsa |
| 10. Reversal/liabilitas | NOT TESTED | Tidak ada di struktur A1 |

## Rantai kredit A1 (ribu tCO₂e, 2024–2086)

| Harga | Bruto vs baseline | Eligible = Diajukan | Terbit | Terjual REDD | Kedaluwarsa | ARR diajukan | Terjual total |
|---|---|---|---|---|---|---|---|
| USD 6 | 713,7 | 385,5 | 376,7 | 326,3 | 46,6 | 0,8 | 327,1 |
| USD 10 | 852,1 | 460,3 | 452,6 | 392,9 | 56,1 | 2,0 | 394,6 |
| USD 15 | 1.174,7 | 634,5 | 625,6 | 543,5 | 77,6 | 4,6 | 547,6 |
| USD 20 | 1.883,2 | 1.017,2 | 995,4 | 861,3 | 123,0 | 10,1 | 870,2 |
| USD 35 | 2.989,5 | 1.614,8 | 1.548,9 | 1.330,8 | 190,1 | 77,8 | 1.396,2 |

"Kredit model" di Tabel 4 naskah = kolom **Diajukan**.

## Diagnostik adisionalitas

**(a) Statis (tanpa rerun).** Kredit yang hanya berasal dari efek karbon (S3−S4) × 0,9 × 0,88 × 0,682:

| Harga | Kredit hanya efek karbon | Rasio terhadap kredit A1 |
|---|---|---|
| USD 6 | 22,2 ribu | 5,8 % |
| USD 10 | 98,2 ribu | 21,3 % |
| USD 15 | 273,3 ribu | 43,1 % |
| USD 20 | 654,6 ribu | 64,3 % |
| USD 35 | 1.248,5 ribu | 77,3 % |

Diagnostik ini statis: penerimaan masih dihitung dari A1, jadi tidak konsisten secara umpan balik.

**(b) Dinamis: rerun dengan `Switch Baseline Kredit Konservatif = 1` (A2).** Ini parameter yang sudah ada di model, dan persamaannya tidak diubah. Label: **DIAGNOSTIK/SENSITIVITAS, bukan hasil utama dan bukan penerbitan yang disetujui.**

| Harga | Kredit A2 (ribu) | Kredit A1 (ribu) | S4−S3 A2 (ha) | S4−S3 A1 (ha) | NPV proyek A2 (Rp miliar) | Belanja/kebutuhan A2 |
|---|---|---|---|---|---|---|
| USD 6 | 74,8 | 385,5 | 15 | 120 | −2,67 | 0,5 % |
| USD 10 | 86,6 | 460,3 | 67 | 535 | −1,35 | 2,0 % |
| USD 15 | 111,9 | 634,5 | 181 | 1.494 | 0,50 | 5,4 % |
| USD 20 | 160,7 | 1.017,2 | 422 | 3.588 | 2,79 | 12,4 % |
| USD 35 | 1.144,6 | 1.614,8 | 6.176 | 6.792 | 16,26 | 72,5 % |

## Simpulan audit karbon

- **Kredit A1 kemungkinan besar terlalu tinggi** bila dibaca sebagai kredit yang layak diterbitkan.
- **Besaran S4−S3 dan kelayakan pada USD 10–20 sangat bergantung pada pengkreditan efek PS.** Pada A2, NPV proyek baru positif di antara USD 10 dan USD 15.
- **Pada USD 35, efek karbon tetap besar di bawah A2.** Loop dana→patroli tetap bekerja meskipun basis kreditnya ketat.
- **Rekomendasi:** pertahankan A1 sebagai hasil utama sesuai desain, tetapi:
  1. beri label "kredit model basis A1 (baseline = S1)";
  2. nyatakan porsi 68 %/11 %;
  3. laporkan satu kalimat sensitivitas A2.

  Tidak perlu mengganti persamaan.
