# Matriks Leveling Ketidakpastian Data: Model S1–S4

Data lengkap ada di `DATA_UNCERTAINTY_LEVELING.csv` (25 butir), yang dibuat oleh `code/data_leveling.py`. Workbook analisis: `ANALISIS_KETIDAKPASTIAN_DATA.xlsx`. Setiap baris memuat nama variabel di `.mdl`, nilai dasar, sumber dan kelas bukti (dikutip dari catatan persamaan), periode data, besaran dampak, ketersediaan data, dan cara menutupnya.

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

## Grid P final × kelemahan bukti (setelah uji tambahan 23 November 2026)

P final = P teruji bila butir sudah diuji (21 dari 25 butir), selain itu P penilaian. Butir yang levelnya berubah karena uji ditandai ↑ (naik) atau ↓ (turun).

| | W = 1 (kelas B lokal) | W = 2 (proksi / C / provisional) | W = 3 (asumsi / D / sangat pendek) |
|---|---|---|---|
| **P = 3** | – | **D03** efektivitas patroli · **D04** biaya MRV/ha · **D07** lintasan harga ↑ · **D11** efek izin PS ↑ | **D01** patroli swadaya pra-proyek · **D02** kehilangan akses · **D19** atribusi pembiayaan awal ↑ |
| **P = 2** | D15 buffer · D16 verifikasi · D17 diskonto · D18 jeda penerbitan · D22 densitas biomassa | D05 laju BAU · D06 porsi PA · D10 biaya patroli/hari · D13 kebocoran · D14 bagi hasil 60/40 | D08 kebakaran · D09 operasional LPHD · D25 bukti validasi |
| **P = 1** | D23 pemegang garapan · D24 pertumbuhan penduduk | D20 pendapatan dasar RT | D12 jumlah RT bergantung ↓ · D21 KUPS awal |

## Ringkasan per level

| Level | Jumlah | Butir | Besaran dampak utama (REPRODUKSI AUDIT) |
|---|---|---|---|
| **1 KRITIS** | 7 (28 %) | D01 patroli swadaya 2017–2023 | Tambahan perlindungan USD 10: 535 → 31 ha; NPV +2,07 → −2,23 Rp M |
| | | D02 kehilangan akses | Tanda ΔRT berbalik pada pengali 0,40–0,61 |
| | | D03 efektivitas patroli | S2−S1: 299–2.799 ha; S4−S3 USD 10: 0–2.793 ha |
| | | D04 biaya MRV/ha | NPV USD 10 −0,81 Rp M pada batas atas |
| | | D07 lintasan harga ↑ | Harga turun 40 % dalam 10 th: NPV USD 10 −0,06 Rp M |
| | | D11 efek izin PS ↑ | Efek izin −0,15: **S2−S1 = −1.624 ha (arah PS berbalik)** |
| | | D19 atribusi pembiayaan awal ↑ | Atribusi 0: **S3−S2 = 0 ha** |
| **2 TINGGI** | 8 (32 %) | D05, D06, D08, D09, D10, D13, D14, D25 | mis. laju BAU ×0,654–1,5: S4−S3 USD 10 229–1.116 ha; biaya patroli ±25 %: 384–880 ha; operasional LPHD: cakupan 40–56 % |
| **3 SEDANG** | 8 (32 %) | D12 ↓, D15, D16, D17, D18, D20, D21, D22 | mis. buffer 0,20: 420 ha; densitas ×0,8–1,2: 289–855 ha |
| **4 RENDAH** | 2 (8 %) | D23, D24 | – |

**Konsistensi penilaian awal vs uji:** 17 dari 21 butir yang diuji punya P penilaian = P teruji. Empat butir meleset:
- **Dinilai terlalu rendah:** D07, D11, D19.
- **Dinilai terlalu tinggi:** D12.

Ini menunjukkan penilaian tanpa uji cenderung melewatkan asumsi yang bisa membalik arah.

## Cara membaca

- **Level 1 menentukan apakah jawaban tujuan penelitian sahih.** Tiga butir (D01, D02, D19) tidak punya data sama sekali. D03, D04, D07, dan D11 bertumpu pada proksi atau asumsi eksternal.
- **Dua temuan baru langsung mengenai klaim makalah:**
  - Klaim "arah pengurangan konsisten" hanya berlaku bila izin PS tidak menaikkan kehilangan hutan (D11).
  - Klaim "pembiayaan awal menambah 276 ha" hanya berlaku bila kenaikan patroli 2024 memang dibiayai proyek (D19).
- **Skor tetap penilaian terstruktur, bukan hasil statistik.** Uji bersifat satu-parameter (OAT), tanpa interaksi antarparameter.
- Detail varian ada di `07_UNCERTAINTY/REPORT.md` (bagian uji tambahan) dan lembar `Uji_Sensitivitas` di `ANALISIS_KETIDAKPASTIAN_DATA.xlsx`.
