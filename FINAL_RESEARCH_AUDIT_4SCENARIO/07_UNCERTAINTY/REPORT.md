# 07 — Ketidakpastian dan Robustness (OUTPUT 6)

Data: `robustness_oat.csv`.

**Metode.** Rerun PySD satu-parameter-per-satu (OAT) pada berkas skenario yang ada, dengan nilai ditimpa saat run tanpa mengubah persamaan. Nilai uji diambil dari **rentang yang tercantum di dokumentasi model**, kecuali yang ditandai "uji audit".

**Ini bukan Monte Carlo.** Uji OAT tidak menangkap interaksi antar-parameter. Hasilnya adalah frekuensi atau besaran pada asumsi yang diuji, bukan peluang nyata.

## Hasil

| Varian | S2−S1 (ha) | S3−S2 (ha) | S4−S3 USD10 (ha) | S4−S3 USD20 (ha) | NPV USD10 (Rp M) | NPV USD20 (Rp M) | Belanja/kebutuhan USD20 | ΔRT S4−S3 USD10 (Rp) |
|---|---|---|---|---|---|---|---|---|
| **Dasar** | 1.720 | 276 | 535 | 3.588 | 2,07 | 11,50 | 49,7 % | −39.560 |
| Efektivitas 0,075 (batas bawah dok.) | 299 | 55 | 0 | 8 | −2,88 | −1,33 | 1,3 % | +1 |
| Efektivitas 0,20 (uji audit) | 898 | 148 | 60 | 389 | −0,68 | 2,84 | 14,6 % | −4.360 |
| Efektivitas 0,50 (uji audit) | 2.356 | 377 | 1.503 | 9.230 | 4,66 | 21,08 | 94,5 % | −103.294 |
| Efektivitas 0,59 (batas atas dok.) | 2.799 | 447 | 2.793 | 11.411 | 6,80 | 27,18 | 119,7 % | −176.998 |
| Monitoring MRV ×2 (Rp 3.960/ha) | 1.720 | 276 | 283 | 2.951 | 0,60 | 9,62 | 43,3 % | −25.738 |
| Monitoring MRV batas atas (Rp 5.775/ha) | 1.720 | 276 | 137 | 2.384 | −0,81 | 7,89 | 37,5 % | −13.142 |
| Verifikasi batas atas (Rp 1,07 M) | 1.720 | 276 | 454 | 3.408 | 1,76 | 11,08 | 48,0 % | −35.797 |
| Verifikasi ×2 (uji audit, di atas rentang) | 1.720 | 276 | 364 | 3.186 | 1,36 | 10,57 | 45,9 % | −31.098 |
| Jeda penerbitan 5 th (uji audit) | 1.720 | 276 | 523 | 3.070 | 0,98 | 7,64 | 38,7 % | −36.379 |
| Proporsi PA 0,541 (pembanding bawah) | 1.720 | 276 | 293 | 1.760 | 0,73 | 6,98 | 30,4 % | −24.041 |
| Proporsi PA 0,903 (pembanding atas) | 1.720 | 276 | 1.060 | 6.574 | 4,46 | 20,27 | 90,8 % | −70.187 |
| Buffer 0,20 (rentang uji dok.) | 1.720 | 276 | 420 | 2.611 | 1,47 | 9,35 | 40,3 % | −32.353 |
| Kebocoran 0,20 (uji audit) | 1.720 | 276 | 397 | 2.443 | 1,34 | 8,92 | 38,5 % | −30.874 |
| Diskonto 6 % | – | – | – | – | 4,17 | 22,45 | – | – |
| Diskonto 15 % | – | – | – | – | 0,71 | 5,87 | – | – |
| Kapasitas realisasi penuh 1,0 | 1.720 | 276 | 534 | 3.505 | 2,17 | 11,64 | 47,8 % | −39.100 |
| **Basis kredit A2 register (CLOSURE)** | 1.720 | 276 | **31** | **192** | **−2,23** | **0,63** | lihat LPHD csv | – |
| Basis A2 tanpa faktor penutup (diagnostik audit) | 1.720 | 276 | 67 | 422 | −1,35 | 2,79 | 12,4 % | – |
| Pengali akses 0 / 1 / 3,24 | – | – | – | – | – | – | – | +34.403 / −39.560 / −205.238 |

Nilai ΔRT pada pengali 3,24 dihitung dari `05/access_multiplier_sweep.csv`.

## Simpulan yang tetap didukung pada rentang yang diuji

| Simpulan | Status |
|---|---|
| PS (patroli swadaya) menurunkan deforestasi dibanding S1 | **Robust arah terhadap efektivitas patroli** (299–2.799 ha), tetapi **TIDAK robust terhadap efek izin PS**: pada efek izin −0,15 (Kraus dkk. 2021) S2−S1 = −1.624 ha (lihat bagian uji tambahan) |
| Biaya MRV/verifikasi yang tetap menjadi penghambat utama pada harga rendah | **Robust** |
| Ada jeda dana 2024–2027/28 sebelum belanja LPHD | **Robust** (struktural; jeda 3 tahun) |
| Kenaikan harga meningkatkan perlindungan secara nonlinear | **Robust arah** |
| Perubahan pendapatan rata-rata RT kecil (< 0,5 % hingga USD 20) | **Robust** pada pengali 0–1 |

## Simpulan yang sangat bergantung asumsi

| Simpulan | Bergantung pada |
|---|---|
| Besaran S4−S3 pada USD 10–20 (535 / 3.588 ha) | Efektivitas, proporsi PA, biaya MRV, dan terutama **basis kredit A1** |
| NPV positif pada USD 10 | Negatif pada: MRV batas atas, efektivitas ≤ 0,20, basis A2 |
| Ambang USD 6,83 dan USD 28,04 | Seluruh rantai biaya; definisi cakupan (K1) |
| Tanda dampak pendapatan RT | Berbalik pada pengali 0,40–0,61 |

## Monte Carlo dan PRCC yang dilaporkan peneliti

- **Status: UNVERIFIED.** Konfigurasi (13 parameter, distribusi, seed 20261101) dan keluarannya tidak disertakan.
- Yang dapat dinyatakan: Monte Carlo menggambarkan **frekuensi hasil pada distribusi yang diasumsikan**, bukan peluang nyata. Menambah jumlah replikasi tidak menambah validitas.
- **Konsistensi arah:** hasil OAT di atas konsisten dengan klaim PRCC bahwa efektivitas perlindungan dominan dan biaya MRV berpengaruh negatif terhadap efek karbon. Ini konsistensi arah, bukan verifikasi angka PRCC.
- **Klaim "nilai deterministik di atas median MC"** tidak dapat dinilai tanpa distribusi parameter yang dipakai, sehingga statusnya UNVERIFIED.

## Uji OAT tambahan untuk matriks leveling (DIAGNOSTIK AUDIT, 23 November 2026)

Data: `robustness_oat3.csv`, dibuat oleh `../code/robust3.py`. Model dan parameter dasar tidak diubah; parameter ditimpa saat run PySD. Nilai dasar direproduksi persis (S4−S3 USD 10 = 535 ha; NPV USD 10 = 2,07 Rp M; ΔRT = −39.560).

| Butir | Varian | S2−S1 (ha) | S3−S2 (ha) | S4−S3 USD 10 (ha) | NPV USD 10 (Rp M) | Belanja/kebutuhan USD 20 | Catatan |
|---|---|---|---|---|---|---|---|
| – | **Dasar** | 1.720 | 276 | 535 | 2,07 | 49,7 % | |
| D05 | Laju BAU ×0,654 (tanpa pengali pulsa; dok.) | 1.300 | 206 | 229 | 0,27 | 25,1 % | |
| D05 | Laju BAU ×1,5 (uji audit) | 2.152 | 352 | 1.116 | 4,80 | 95,1 % | |
| D07 | Harga turun 40 % dalam 10 th (uji audit) | 1.720 | 276 | 147 | **−0,06** | 19,3 % | NPV berbalik |
| D07 | Harga naik 2× sampai 2050 (uji audit) | 1.720 | 276 | 2.450 | 6,03 | 120,7 % | |
| D08 | Tahun kering ekstrem (dok., uji struktur) | 1.720 | 276 | 535 | 2,07 | 49,7 % | Emisi kum. S4 USD 10 79,9 → 159,4 juta tCO₂e; tidak ada efek lain |
| D08 | Alokasi kebakaran 0,20 (uji audit) | 1.720 | 276 | 461 | 1,95 | 45,8 % | |
| D09 | Operasional LPHD Rp 25 / 100 juta (dok.) | 1.720 | 276 | 535 | 2,07 | 56,2 / 40,4 % | Hanya cakupan LPHD |
| D10 | Biaya patroli/hari −25 % / +25 % (uji audit) | 1.720 | 276 | 880 / 384 | 2,82 / 1,49 | 68,7 / 38,3 % | |
| D11 | Efek izin PS −0,15 (dok.) | **−1.624** | 288 | 113 | **−0,43** | 21,7 % | **Arah PS berbalik** |
| D11 | Efek izin PS 0,169 (dok.) | 6.185 | 260 | 1.342 | 5,70 | 86,3 % | |
| D12 | RT bergantung 2.144 / 19.038 (dok.) | 1.720 | 276 | 535 | 2,07 | 49,7 % | Indikator per RT tidak berubah |
| D14 | Bagi hasil 50 % / 70 % (uji audit) | 1.720 | 276 | 405 / 695 | 2,60 / 1,49 | 35,0 / 69,2 % | |
| D19 | Atribusi patroli 2024 ke pembiayaan awal = 0 (dok.) | 1.720 | **0** | 437 | 1,15 | 27,7 % | **Efek pembiayaan awal hilang** |
| D19 | Atribusi = 0,5 (uji audit) | 1.720 | 138 | 482 | 1,62 | 38,5 % | |
| D22 | Densitas biomassa ×0,8 / ×1,2 (uji audit) | 1.720 | 276 | 289 / 855 | 0,70 / 3,60 | 29,9 / 77,3 % | |
| D24 | Pertumbuhan penduduk 1,37 / 1,91 % (dok.) | 1.720 | 276 | 535 | 2,07 | 49,7 % | ΔRT berubah < 0,4 % |

**Temuan baru:**
1. **Arah kontribusi PS tidak robust terhadap efek izin** (D11). Model menetapkan efek izin = 0. Pada −0,15, yaitu batas bawah yang didokumentasikan dari Kraus dkk. (2021), S2−S1 menjadi −1.624 ha. Klaim bahwa arah efek PS konsisten hanya berlaku bila izin tidak menaikkan kehilangan hutan.
2. **Efek pembiayaan awal sepenuhnya bergantung pada asumsi atribusi** (D19). Bila kenaikan patroli 2024 adalah swadaya (pilihan 0 yang didokumentasikan di `.mdl`), S3−S2 = 0 ha.
3. **NPV pada USD 10 berbalik negatif bila harga turun 40 % dalam 10 tahun** (D07).
4. **Kebakaran tidak terhubung ke deforestasi, kredit, atau kebutuhan dana** (D08). Tahun kering ekstrem menggandakan emisi bersih kumulatif tetapi tidak mengubah hasil lain, karena kebutuhan dana kebakaran dihitung dari jumlah regu yang tetap. Ini temuan struktural, bukan hasil kebijakan.
5. **Jumlah RT bergantung tidak memengaruhi indikator per RT** (D12). Pengaruhnya hanya pada total agregat, yang tidak diuji di sini.
