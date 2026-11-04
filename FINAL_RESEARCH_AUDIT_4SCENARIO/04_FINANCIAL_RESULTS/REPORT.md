# 04 — Audit Keuangan

Data:
- `financial_summary.csv`: kumulatif dan rerata.
- `annual_cashflow.csv`: arus kas per tahun per skenario.

Satuan: Rp miliar, kumulatif 2024–2086, kecuali disebut lain.

## Rantai keuangan di model

```
Kredit terjual × harga × Rp16.500  → Penerimaan kotor
− (monitoring/ha + verifikasi tiap 5 th + penerbitan/kredit + transaksi 0,22 % + pajak 5 %)
= Surplus (≥0); kekurangan ditanggung mitra → dipulihkan dari surplus berikutnya
→ Pendapatan bersih terdistribusi → 60 % Dana LPHD (kolektif) | 40 % Dana Mitra
   Dana Mitra memulihkan pembiayaan awal (talangan 100 %)
Dana LPHD → saldo → belanja (alokasi × rasio realisasi kapasitas LPHD) → patroli, operasional, kebakaran, rehabilitasi, kelembagaan, KUPS
```

## Ringkasan

| | S3 | USD 6 | USD 10 | USD 15 | USD 20 | USD 35 |
|---|---|---|---|---|---|---|
| Penerimaan kotor | 0 | 32,54 | 65,39 | 135,86 | 287,16 | 790,14 |
| — monitoring MRV | 0 | 13,86 | 13,86 | 13,86 | 13,86 | 13,86 |
| — verifikasi | 0 | 8,91 | 8,91 | 8,91 | 8,91 | 8,91 |
| — penerbitan/registri | 0 | 1,56 | 1,87 | 2,60 | 4,15 | 6,70 |
| — transaksi penjualan | 0 | 0,07 | 0,14 | 0,30 | 0,63 | 1,74 |
| — pajak/pungutan | 0 | 1,63 | 3,27 | 6,79 | 14,36 | 39,51 |
| Total biaya MRV + transaksi + pajak | 0 | 26,03 | 28,06 | 32,46 | 41,91 | 70,72 |
| Kekurangan biaya ditanggung mitra (sementara) | 0 | 3,18 | 1,08 | 1,07 | 1,07 | 1,06 |
| Defisit belum pulih 2087 | 0 | 2,07 | 0 | 0 | 0 | 0 |
| Pendapatan bersih terdistribusi | 0 | 8,59 | 37,33 | 103,40 | 245,25 | 719,42 |
| Dana kolektif LPHD (60 %) | 0 | 5,15 | 22,40 | 62,04 | 147,15 | 431,65 |
| Dana mitra (40 %) | 0 | 3,43 | 14,93 | 41,36 | 98,10 | 287,77 |
| Pembiayaan awal (S3, 2024–2025) | 1,77 | 1,77 | 1,77 | 1,77 | 1,77 | 1,77 |
| Pembiayaan awal belum pulih 2087 | 1,77 | 0 | 0 | 0 | 0 | 0 |
| Belanja LPHD total | 0 | 5,15 | 22,38 | 61,65 | 145,39 | 422,62 |
| Saldo LPHD tak terbelanja 2087 | 0 | 0,00 | 0,02 | 0,39 | 1,76 | 9,02 |
| **NPV proyek 10 % (parsial)** | **−1,62** | **−0,50** | **2,07** | **6,09** | **11,50** | **30,79** |
| **NPV mitra 10 % (parsial)** | −1,62 | −0,72 | 1,46 | 4,90 | 9,61 | 26,33 |

Pada USD 3 (arsip): defisit biaya 9,72 miliar dan pembiayaan awal 1,74 miliar tidak pulih.

## Definisi NPV yang direkonstruksi

**Status: VERIFIED (rekonstruksi; cocok di semua titik naskah).** Definisi ini tidak tertulis di naskah.

- **NPV proyek** = ∫ (1,1)^−(t−2024) × [penerimaan kotor − biaya MRV/transaksi/pajak − pembiayaan awal − belanja LPHD] dt.
- **NPV mitra** = ∫ (1,1)^−(t−2024) × [dana mitra + pemulihan defisit biaya bersama − kekurangan biaya yang ditanggung mitra − pembiayaan awal] dt.
- **Harga impas** dari sapuan harga: proyek **USD 6,83** (NPV −0,0008 miliar); mitra **USD 7,40** (−0,0007 miliar).

### Batas akuntansi (alasan NPV CONDITIONAL, bukan bukti kelayakan)

1. **Tanpa biaya pengembangan proyek** (studi kelayakan, PDD, validasi awal, pendaftaran). NPV ini bersifat parsial.
2. **Saldo LPHD yang tidak dibelanjakan tidak dikurangkan.** Saldo itu terhitung sebagai surplus proyek (9,02 miliar nominal pada USD 35).
3. **Belanja LPHD (termasuk upah masyarakat) diperlakukan sebagai biaya.** Manfaat avoided deforestation di luar penjualan kredit tidak dihitung.
4. **Diskonto 10 % tidak bersumber.** NPV USD 10 bernilai 4,17 miliar (6 %) dan 0,71 miliar (15 %). Tandanya tetap positif.
5. **NPV proyek dan NPV mitra berbeda batas.** Keduanya tidak boleh dibandingkan langsung, dan keduanya juga tidak sama dengan ketersediaan kas LPHD.
6. **Pembiayaan awal tidak dihitung dua kali.** Ia masuk sekali sebagai biaya dan dipulihkan dari dana mitra (pemulihan 1,77 miliar pada ≥ USD 6).

## Kecukupan dana LPHD — temuan kritis (K1)

`Kebutuhan Dana Minimum` = operasional LPHD + patroli tambahan + pengendalian kebakaran = Rp 5,418 miliar/th. **Ini konstruksi model, bukan anggaran resmi.**

| Rerata 2030–2055 | USD 6 | USD 10 | USD 15 | USD 20 | USD 35 |
|---|---|---|---|---|---|
| (a) Belanja **total** / kebutuhan (= "cakupan" naskah) | 3,6 % | 11,8 % | 26,8 % | 49,7 % | 133,5 % |
| (b) 1 − kesenjangan / kebutuhan | 3,6 % | 11,8 % | 26,8 % | 49,7 % | 95,7 % |
| (c) Belanja **komponen minimum** / kebutuhan | 1,8 % | 5,9 % | 13,4 % | 24,8 % | 57,8 % |

- Metrik (a) memasukkan belanja rehabilitasi, KUPS, dan kelembagaan, yang bukan bagian dari kebutuhan minimum.
- Persamaan `Kesenjangan Pembiayaan Minimum` juga mengurangkan **seluruh** belanja dari kebutuhan minimum.
- Akibatnya, "tertutup pada USD 28,04" berarti belanja total = kebutuhan minimum, **bukan** kebutuhan minimum terpenuhi. Pada USD 28,04 kesenjangan rerata masih Rp 0,62 miliar/th (cakupan b = 88,6 %).
- **Status klaim: INCONSISTENT.** Usulan teks pengganti ada di 08 dan 09.

**Waktu kas.**
- Belanja LPHD pertama kali > 0 pada t = 2029,9 (USD 6), 2029,3 (USD 10), 2028,8 (USD 20), dan 2028,6 (USD 35).
- Jeda 2024–2027 tanpa belanja: VERIFIED.
- Belanja total ≥ kebutuhan minimum hanya pada USD 35, mulai t = 2036,75.

## Apakah "layak secara finansial" tetap berlaku?

- **Pada basis A1, ya, secara parsial.** NPV proyek positif di atas USD 6,83 setelah semua biaya yang dimodelkan, pemulihan, dan pembiayaan awal.
- **Sensitif terhadap asumsi:**
  - biaya monitoring di batas atas dokumentasi (Rp 5.775/ha/th): NPV USD 10 = −0,81 miliar;
  - efektivitas 0,20: NPV USD 10 = −0,68 miliar;
  - basis A2: NPV USD 10 = −1,35 miliar.
- **Kesimpulan:** kelayakan pada USD 10 **rapuh**; pada USD 20 lebih robust. NPV USD 20 tetap positif pada semua uji kecuali efektivitas 0,075 (−1,33).
