# 01 — Hasil Ekologis

Data: `ecological_summary.csv` (kumulatif) dan `ecological_annual.csv` (per tahun, 2024–2086, per skenario).

## Neraca stok-aliran hutan (ha)

| Skenario | Hutan 2024 | Neto 2024 | Deforestasi 2025–86 | Regenerasi alami | Rehabilitasi → hutan | Hutan 2087 | Residu |
|---|---|---|---|---|---|---|---|
| S1 | 94.307,9 | −283,8 | 29.812,3 | 17.678,0 | 0,0 | 81.889,8 | 0,000 |
| S2 | 94.307,9 | −283,8 | 28.091,9 | 17.166,4 | 516,4 | 83.615,0 | 0,000 |
| S3 | 94.307,9 | −283,8 | 27.815,6 | 17.054,1 | 516,4 | 83.779,0 | 0,000 |
| S4 USD6 | 94.307,8 | −283,8 | 27.695,6 | 17.009,5 | 535,2 | 83.873,1 | 0,000 |
| S4 USD10 | 94.307,8 | −283,8 | 27.280,7 | 16.890,7 | 598,9 | 84.232,9 | 0,000 |
| S4 USD15 | 94.307,8 | −283,8 | 26.321,8 | 16.650,6 | 754,3 | 85.107,2 | 0,000 |
| S4 USD20 | 94.307,8 | −283,8 | 24.227,4 | 16.206,3 | 1.109,6 | 87.112,5 | 0,000 |
| S4 USD35 | 94.307,9 | −283,8 | 21.023,2 | 15.332,6 | 2.364,6 | 90.698,1 | 0,000 |

**Status: VERIFIED.** Identitas Hutan2087 = Hutan2025 − deforestasi + regenerasi + rehabilitasi tertutup tepat di semua skenario.

**Penjelasan angka "284" di naskah.** Angka ini adalah **perubahan bersih tahun 2024**: deforestasi 522,2 ha dikurangi regenerasi 238,4 ha. Neraca S1 di naskah benar, tetapi angka 284 perlu dinamai.

## Membedakan empat besaran

| Besaran | S2 vs S1 | S4 USD20 vs S3 |
|---|---|---|
| Deforestasi bruto kumulatif dihindari | 1.720,4 ha | 3.588,3 ha |
| Selisih stok hutan 2087 | 1.725,2 ha | 3.333,5 ha |
| Selisih regenerasi alami | −511,6 ha | −847,8 ha |
| Selisih rehabilitasi | +516,4 ha | +593,2 ha |

- Selisih stok **tidak sama** dengan deforestasi dihindari.
- Lebih banyak hutan berarti lebih sedikit lahan nonhutan, sehingga regenerasi alami turun.
- Rehabilitasi bertambah karena ada dana.
- Naskah memakai keduanya (1.720 di teks, 1.725 di Gambar 4a), jadi labelnya harus dibedakan.

## Laju tahunan dan perlindungan (rerata 2030–2055)

| | S1 | S2 | S3 | USD10 | USD20 | USD35 |
|---|---|---|---|---|---|---|
| Deforestasi (ha/th) | 493,6 | 462,9 | 462,2 | 445,5 | 394,6 | 342,0 |
| Intensitas perlindungan | 0 | 0,295 | 0,295 | 0,387 | 0,683 | 0,971 |
| Efek Pengelolaan PS Aktif | 0 | 0,071 | 0,076 | 0,113 | 0,221 | 0,332 |

## Catatan struktural (CONDITIONAL)

- **Satu-satunya jalur penekan deforestasi yang aktif adalah perlindungan/patroli.** Efek Penghidupan dan Efek Pengendalian Kebakaran bernilai 0 di semua run. Efek Izin PS juga 0. Dengan demikian, PS dimodelkan hanya sebagai patroli, sedangkan hak kelola itu sendiri tidak berefek.
- **Pengendalian kebakaran tidak mengurangi deforestasi.** HOK pengendalian kebakaran dihitung sebagai pekerjaan, tetapi tidak memengaruhi deforestasi.
- **Efektivitas 0,37 (Oldekop et al. 2019, Nepal; kelas C).** Rentang dokumentasi model 0,075–0,59. Dokumentasi juga mencatat bahwa tidak ada studi yang menghubungkan intensitas patroli komunitas dengan laju kehilangan hutan.
- **Hansen tree-cover loss ≠ deforestasi regulasi.** Validasi aliran terhadap Hansen dilaporkan lemah (MAPE 73,3 %, UNVERIFIED). Karena itu laju tahunan model belum tervalidasi.
- **Emisi bersih kumulatif S1 = 80,7 juta tCO₂e (2025–2086).** Sebagian besar berasal dari gambut, karena emisi deforestasi biomassa hanya 10,3 juta. Emisi dihindari di Tabel 4 mencakup komponen gambut dan serapan, sedangkan kredit hanya biomassa REDD.
