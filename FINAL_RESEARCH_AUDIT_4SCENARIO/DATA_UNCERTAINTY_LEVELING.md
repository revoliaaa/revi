# Matriks Leveling Ketidakpastian Data: Model S1–S4

Data lengkap ada di `DATA_UNCERTAINTY_LEVELING.csv` (25 butir), yang dibuat oleh `code/data_leveling.py`. Setiap baris memuat nama variabel di `.mdl`, nilai dasar, sumber dan kelas bukti (dikutip dari catatan persamaan), periode data, besaran dampak, ketersediaan data, dan cara menutupnya.

## Aturan penilaian

**P = pengaruh terhadap kesimpulan naskah**
- **3**: dapat membalik arah atau kesimpulan (tanda, kelayakan, ada/tidaknya efek).
- **2**: menggeser besaran secara berarti tanpa membalik arah.
- **1**: hanya memengaruhi indikator tertentu.

**W = kelemahan bukti**
- **3**: asumsi eksploratif, kelas D, data ≤ 2 tahun, atau berkas tidak ada.
- **2**: proksi eksternal, kelas C, atau provisional.
- **1**: kelas B dengan data lokal.
- **0**: kelas A (observasi).

**Level**
- **1 KRITIS**: P = 3 dan W ≥ 2.
- **2 TINGGI**: P = 3 dengan W ≤ 1, atau P = 2 dengan W ≥ 2.
- **3 SEDANG**: P = 2 dengan W ≤ 1, atau P = 1 dengan W ≥ 2.
- **4 RENDAH**: P = 1 dan W ≤ 1.

**Status bukti besaran dampak**
- **REPRODUKSI AUDIT**: uji OAT/A2 di `07_UNCERTAINTY` dan berkas rekonsiliasi.
- **NASKAH (BELUM DIVERIFIKASI)**: angka dari naskah yang belum bisa dihitung ulang.
- **BELUM DIUJI**: arah pengaruh dinilai dari struktur model. Skor P untuk butir ini adalah **penilaian audit, bukan hasil uji**.

## Grid pengaruh × kelemahan bukti

| | W = 1 (kelas B lokal) | W = 2 (proksi / C / provisional) | W = 3 (asumsi / D / sangat pendek) |
|---|---|---|---|
| **P = 3** | – | **D03** efektivitas patroli · **D04** biaya MRV/ha | **D01** patroli swadaya pra-proyek · **D02** kehilangan akses |
| **P = 2** | D15 buffer · D16 verifikasi · D17 diskonto · D18 jeda penerbitan · D22 densitas biomassa | D05 laju BAU · D06 porsi PA · D07 lintasan harga · D10 biaya patroli/hari · D11 efek izin · D13 kebocoran · D14 bagi hasil 60/40 | D08 kebakaran · D09 operasional LPHD · D12 jumlah RT bergantung · D25 bukti validasi |
| **P = 1** | D23 pemegang garapan · D24 pertumbuhan penduduk | D20 pendapatan dasar RT | D19 pembiayaan awal · D21 KUPS awal |

Arsiran level: sel kanan-atas = Level 1; P2/W≥2 dan P3/W≤1 = Level 2; P2/W1 dan P1/W≥2 = Level 3; P1/W1 = Level 4.

## Ringkasan per level

| Level | Butir | Besaran dampak utama | Hasil yang terancam |
|---|---|---|---|
| **1 KRITIS** | D01 patroli swadaya 2017–2023 | Tambahan perlindungan USD 10: 535 → 31 ha; NPV +2,07 → −2,23 Rp M | Tujuan 2, 4 |
| | D02 kehilangan akses | Tanda ΔRT berbalik pada pengali 0,40–0,61 | Tujuan 3, 4 |
| | D03 efektivitas patroli | S2−S1: 299–2.799 ha; S4−S3 USD 10: 0–2.793 ha | Tujuan 1, 2 |
| | D04 biaya MRV/ha | NPV USD 10 menjadi −0,81 Rp M pada batas atas | Tujuan 2 (kelayakan) |
| **2 TINGGI** | D05, D06, D07, D08, D09, D10, D11, D12, D13, D14, D25 | mis. porsi PA: S4−S3 USD 10 293–1.060 ha; kebocoran 0,20: 397 ha; kebakaran = separuh kebutuhan minimum | Besaran Tujuan 1–2; ambang USD 28; kredibilitas validasi |
| **3 SEDANG** | D15–D22 | mis. buffer 0,20: 420 ha; jeda 5 th: NPV USD 20 11,50 → 7,64 | Indikator finansial dan sosial tertentu |
| **4 RENDAH** | D23, D24 | – | – |

## Cara membaca

- **Level 1 menentukan apakah jawaban tujuan penelitian sahih.** Dua butir di antaranya (D01, D02) tidak punya data sama sekali, sementara D03 dan D04 bertumpu pada proksi dari negara lain. Sebagian datanya kemungkinan bisa diperoleh dari arsip LPHD atau proyek (log patroli, anggaran MRV); lihat kolom `ketersediaan_data`.
- **Level 2 adalah kandidat uji sensitivitas tambahan.** D05, D07, D09, D10, D11, D12, dan D14 belum diuji audit dan bisa diuji dengan parameter yang sudah ada di model tanpa mengubah S1–S4.
- **Skor bersifat penilaian terstruktur, bukan hasil statistik.** Skor P untuk butir "BELUM DIUJI" bisa berubah setelah diuji.
