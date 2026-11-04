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
| PS (patroli swadaya) menurunkan deforestasi dibanding S1 | **Robust arah**. Besarannya sangat bergantung efektivitas (299–2.799 ha) |
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
