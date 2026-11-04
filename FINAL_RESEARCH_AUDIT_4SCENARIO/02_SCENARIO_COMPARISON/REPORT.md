# 02 — Analisis Kontribusi Skenario (OUTPUT 3)

Data: `decomposition_by_price.csv` dan `annual_avoided_deforestation.csv`.

## Konsistensi antar-skenario

- **Persamaan identik** kecuali `Skenario Kebijakan` dan `Harga Karbon`. Ada pembulatan 9 konstanta pada berkas S1/S2/S3/USD35, dengan dampak ≤ 0,07 ha (lihat 00).
- **Kondisi awal dan pemicu eksogen identik.** Deforestasi 2024 sama di semua skenario (522,15 ha).
- **Baseline kredit internal S4 identik dengan run S1** (selisih 0 pada berkas dengan pembulatan sama).
- **Uji identitas:** S3 − S4 USD3 = 1,0 ha. Pada harga sangat rendah, karbon praktis tidak menambah perlindungan, sesuai harapan.

## Dekomposisi deforestasi dihindari (ha, 2025–2086)

| Harga | S2−S1 (PS) | S3−S2 (pembiayaan awal) | S4−S3 (karbon) | Total vs S1 | Porsi PS / awal / karbon |
|---|---|---|---|---|---|
| USD 6 | 1.720,4 | 276,3 | 120,0 | 2.116,7 | 81 / 13 / 6 % |
| USD 10 | 1.720,4 | 276,3 | 534,9 | 2.531,6 | 68 / 11 / 21 % |
| USD 15 | 1.720,4 | 276,3 | 1.493,8 | 3.490,5 | 49 / 8 / 43 % |
| USD 20 | 1.720,4 | 276,3 | 3.588,3 | 5.585,0 | 31 / 5 / 64 % |
| USD 35 | 1.720,4 | 276,3 | 6.792,4 | 8.789,1 | 20 / 3 / 77 % |

## Dekomposisi emisi bersih dihindari (tCO₂e, 2025–2086)

| Harga | S2−S1 | S3−S2 | S4−S3 | Total vs S1 |
|---|---|---|---|---|
| USD 10 | 597.963 | 77.206 | 186.343 | 861.511 |
| USD 20 | 597.963 | 77.206 | 1.265.358 | 1.940.526 |
| USD 35 | 597.963 | 77.206 | 2.569.847 | 3.245.015 |

## Interpretasi

**S2 − S1 (kontribusi PS yang dimodelkan).**
- Nilainya 1.720 ha / 598 ribu tCO₂e, dan seluruhnya berasal dari patroli swadaya 2.355 HOK/th (intensitas 0,29).
- **CONDITIONAL** pada efektivitas 0,37 dan definisi S1 (PS berhenti 2024, KUPS meluruh ke 0,7 unit pada 2087).
- Arahnya robust; besarnya 299–2.799 ha untuk efektivitas 0,075–0,59.

**S3 − S2 (pembiayaan awal).**
- Nilainya 276 ha.
- Dana berhenti pada 2025, tetapi efeknya meluruh bertahap karena penyesuaian efek pengelolaan (SMOOTH): 93,6 ha (2025), 79,5 (2026), 39,1 (2028), 12,6 (2031).
- **Selisih bruto 2025–2036 = +345,1 ha.**
- **Sejak 2037, S3 justru sedikit lebih tinggi deforestasinya (−1 sampai −2 ha/th; total −68,8 ha).** Penyebabnya struktural: deforestasi = laju × stok hutan, dan stok hutan S3 lebih besar.
- Nilai neto 276 ha adalah hasil kedua bagian itu.
- Kalimat naskah "efeknya tidak berlanjut setelah 2025" perlu diganti menjadi **"dananya berhenti 2025; efeknya meluruh sampai pertengahan 2030-an (bruto ±345 ha), lalu sebagian terkoreksi karena stok hutan yang lebih besar ikut terpapar laju deforestasi"**.
- Pola serupa yang kecil muncul pada S4 USD 10 − S3 setelah 2080 (total −5,7 ha).

**S4 − S3 (mekanisme pembiayaan karbon).**
- Efek baru muncul pada 2029 (0,3 ha), mencapai ±23 ha/th sekitar 2034–2036 pada USD 10, lalu menurun pelan.
- **Ini selisih perlindungan, bukan jumlah kredit yang layak diterbitkan.**
- Besarannya **CONDITIONAL pada basis kredit A1**. Pada uji A2 (kredit hanya aditional terhadap S2), S4−S3 menjadi 15 / 67 / 181 / 422 / 6.176 ha untuk USD 6 / 10 / 15 / 20 / 35 (lihat 03).

## Pemisahan dampak kebijakan dan kuantitas kredit

| Besaran (USD 10) | Nilai | Makna |
|---|---|---|
| Emisi deforestasi biomassa dihindari vs S1 | 860.953 tCO₂e | dampak kebijakan gabungan (PS + awal + karbon) |
| Bagian karbon (S3−S4) | 181.870 tCO₂e (21,1 %) | dampak tambahan mekanisme karbon |
| Kredit REDD diajukan (A1) | 460.252 tCO₂e | kuantitas kredit model setelah kebocoran 10 %, buffer 12 %, porsi PA 0,682 |
| Kredit terjual (REDD+ARR) | 394.620 tCO₂e | dasar penerimaan |

Bagian kredit A1 yang berasal dari efek PS dan pembiayaan awal = 78,9 %.
