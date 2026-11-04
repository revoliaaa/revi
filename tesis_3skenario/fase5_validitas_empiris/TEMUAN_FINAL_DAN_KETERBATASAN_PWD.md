# Temuan Final dan Keterbatasan (PWD)

**Tanggal:** 4 November 2026

**Status:**
- Model `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` dibekukan (md5 `639083f9…`; tidak ada persamaan atau variabel baru).
- PySD 3.14.3; **Vensim native: BELUM DIVERIFIKASI NATIVE**.
- NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Referensi S1 berpasangan dipakai di semua konfigurasi S2.
- D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. Selisihnya adalah dekomposisi menurut asumsi model, **bukan identifikasi kausal empiris**.

## Keputusan akademik

**1. Apakah dua skenario lebih dapat dipertanggungjawabkan daripada empat skenario lama?**

Ya. Patroli 2023–2025 dibiayai mitra proyek karbon, sehingga skenario "PS swadaya" tidak berdasar data, dan "tanpa PS" bukan alternatif kebijakan yang tersedia. Dua skenario memperlakukan sejarah pembiayaan sebagai fakta bersama. Asumsi yang tersisa (jembatan masa depan) kini terukur lewat D1 − D0.

**2. Seberapa besar tambahan perlindungan S2 disebabkan pembiayaan awal dibanding penjualan karbon?**

Menurut model, deforestasi dihindari pada konfigurasi dasar:

| Harga | Dari pembiayaan awal | Dari penjualan karbon |
|---|---|---|
| USD 10 | 287 ha (100 %) | 0 |
| USD 20 | 287 ha (63 %) | 167 ha (37 %) |
| USD 35 | 287 ha (6 %) | 4.667 ha (94 %) |

Pada USD 20, porsi pembiayaan awal berkisar 8–100 % antarvariasi, sangat bergantung pada efektivitas perlindungan dan biaya per HOK.

**3. Kapan pendapatan penjualan karbon mempertahankan kegiatan sesudah dana awal berakhir?**

Hanya pada harga tinggi (USD 35 pada konfigurasi dasar), atau pada USD 20 bila efektivitas tinggi (0,6) atau biaya per HOK rendah (Rp150.000):
- FTE berupah 2060–2086 +16,7 (efektivitas 0,6) dan +30,3 (Rp150.000), sedangkan konfigurasi dasar = 0;
- kas LPHD bertahan.

Pada USD 10 tidak pernah, dan pada USD 20 dasar hanya sampai ±2055. Tanpa pembiayaan awal (D3) siklus tidak pernah dimulai pada kondisi mana pun yang diuji (*bootstrap problem*).

**4. Apakah tambahan kas karbon cukup untuk memperkuat LPHD dan KUPS?**

- **USD 20:** tidak. Dana LPHD Rp7,7 M (cakupan kebutuhan 5,2 % pada 2030–2055 dan 0 % sesudah 2060); KUPS +0,3 pada 2087; kapasitas LPHD tetap 0,50.
- **USD 35:** ya menurut model. Dana LPHD Rp214 M, cakupan 90 % pada 2060–2086, KUPS 2087 +44,7.
- Pembiayaan awal sendiri (D1) tidak menambah dana LPHD maupun KUPS.

**5. Konsekuensi terhadap rumah tangga terdampak?**

Pada pengali kehilangan akses 1, setiap tambahan perlindungan, baik dari jembatan maupun penjualan, memperbesar kehilangan akses:

| Harga | Δ pendapatan RT terdampak (Rp/th) |
|---|---|
| USD 20 | −125.222 |
| USD 35 | −496.878 |

Kompensasi tidak ada pada B0. Arah dampak berbalik bila pengali < 0,30 (USD 20). Karena pengali adalah asumsi D, **arah dampak belum dapat diklaim final**. Yang dapat diklaim: beban terkonsentrasi pada ±2.144 (2024) hingga ±3.000 (rerata 2030–2055) pemegang garapan, dan manfaat tunai kegiatan (upah) mengalir ke kelompok yang tidak selalu sama.

**6. Bagian temuan yang didukung data vs proyeksi bersyarat**

| Status | Temuan |
|---|---|
| Didukung data/terverifikasi | Fakta pembiayaan historis 2023–2025 dan HOK; upah patroli; konsistensi internal model (identitas, rekonsiliasi kas, kesetaraan referensi, DT) |
| Proyeksi bersyarat (bergantung C/D) | Semua besaran S2 − S1 dan D1 − D0 / D2 − D1; ambang harga keberlanjutan; arah dampak pendapatan RT; manfaat KUPS; NPV |
| Belum dapat diklaim | Kausalitas empiris; kredit terverifikasi; NPV final; arah kesejahteraan; alokasi optimal per desa; kesetaraan Vensim native |

---

## Temuan per tujuan penelitian

### RQ1: Ekologi

- Paket S2 menambah perlindungan di atas S1: 287 / 454 / 4.954 ha (USD 10 / 20 / 35).
- Pembiayaan awal saja (D1) menghasilkan 287 ha, sebagian besar pada 2025–2030 (196 ha).
- Manfaat karbon bersih D1 turun dari puncak 127 ribu menjadi 82 ribu tCO₂e pada 2087 (non-permanensi).
- Penjualan karbon menambah manfaat yang bertahan hanya bila siklus pembiayaannya mandiri.

### RQ2: Pembiayaan

| Konfigurasi | Hasil |
|---|---|
| D1 (hibah jembatan) | Biaya mitra Rp3,91 M; tanpa beban MRV |
| D2 USD 10 | MRV dan transaksi Rp25,7 M; penerimaan Rp9,9 M; defisit Rp19,0 M ditanggung mitra |
| D2 USD 20 | Mitra nominal −Rp10,1 M (NPV −Rp0,27 M [SEMENTARA]) |
| D2 USD 35 | Mitra +Rp141,4 M; LPHD Rp214 M |
| D3 (tanpa jembatan) | Kerugian MRV Rp22,8 M (Rp2,9 M dengan aturan henti) |

Kredit model tidak dihitung sebagai pendapatan sebelum terjual dan kasnya diterima.

### RQ3: Sosial-ekonomi

- Upah tunai tambahan USD 20: Rp4,65 M, dari jembatan (dibayar mitra) Rp2,26 M dan dari kas LPHD Rp2,40 M. Kontribusi sukarela tidak dihitung sebagai tunai.
- Kerja berupah sesudah 2060 hanya pada USD 35.
- KUPS hanya menguat pada USD 35.
- Pendapatan RT bersyarat pada pengali akses.

### RQ4: Distribusi

- Penjualan sesudah jembatan menambah dana LPHD hanya bila harga ≥ ±USD 15–20. Dana itu memperkuat KUPS dan mempertahankan perlindungan hanya pada USD 35.
- Kompensasi hanya mungkin bila ada dana LPHD (lihat eksperimen alokasi Fase 4).
- Ketergantungan pada mitra tetap tinggi pada USD ≤ 20: mitra membiayai jembatan dan menalangi defisit MRV. Pada USD 35 ketergantungan berkurang, karena LPHD membiayai patroli sendiri sejak ±2033.

## Keterbatasan

1. Vensim native belum diverifikasi.
2. Parameter kelas D menentukan besaran dan arah sebagian temuan (lihat register).
3. Jembatan adalah asumsi eksperimen. Komitmen dan kontrak mitra tidak tersedia.
4. Aturan MRV dan *reversal* adalah aturan model.
5. NPV belum memuat biaya pengembangan dan material.
6. Satuan populasi: pekerja SDA = RT (proksi); pemegang garapan = RT; keduanya tumbuh mengikuti penduduk.
7. Hasil berlaku untuk agregat 25 HD, bukan per desa.
8. Tidak ada indikator kemiskinan atau ketimpangan.

## Saran pengumpulan data (prioritas untuk validasi)

1. Realisasi biaya patroli per komponen 2024–2025.
2. Komitmen pembiayaan mitra pasca-2025 dan ketentuan bagi hasil/talangan.
3. Anggaran MRV dan biaya pengembangan proyek.
4. Survei kehilangan pendapatan pemegang garapan.
5. Daftar RT bergantung hutan dan RT unik pemegang garapan.
6. Data keuangan KUPS 2024–2025.
7. Units Check dan run Vensim native.
