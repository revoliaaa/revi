# Peta Sumber Data: Sekunder vs Perlu LPHD

Pemetaan ini adalah penilaian audit atas 25 butir di `DATA_UNCERTAINTY_LEVELING.csv` (kolom `kategori_sumber`, `perlu_LPHD`, `peran_LPHD`). Versi interaktif ada di lembar `Sumber_Data` pada `ANALISIS_KETIDAKPASTIAN_DATA.xlsx`. Level mengikuti hasil uji 23 November 2026.

## Ringkasan

| Kategori sumber | Kritis | Tinggi | Sedang | Rendah | Total |
|---|---|---|---|---|---|
| A Sekunder publik/literatur | 2 | 2 | 2 | 1 | 7 |
| B Sekunder dokumen proyek (pengembang/mitra/pendamping) | 2 | 3 | 4 | 0 | 9 |
| C Primer LPHD (arsip dan konfirmasi) | 2 | 2 | 1 | 1 | 6 |
| D Primer survei RT (kerangka sampel melalui LPHD/desa) | 1 | 0 | 1 | 0 | 2 |
| E Berkas peneliti sendiri | 0 | 1 | 0 | 0 | 1 |

| Perlu LPHD? | Kritis | Tinggi | Sedang | Rendah | Total |
|---|---|---|---|---|---|
| YA, sumber utama | 4 | 2 | 1 | 0 | 7 |
| YA, sumber pendukung | 0 | 2 | 2 | 1 | 5 |
| TIDAK | 3 | 4 | 5 | 1 | 13 |

**Inti:** 4 dari 7 butir Kritis membutuhkan LPHD sebagai sumber utama:
- **D01** patroli swadaya 2017–2023;
- **D02** kehilangan akses (survei);
- **D03** efektivitas patroli;
- **D19** atribusi pembiayaan awal.

Tiga butir Kritis lainnya dapat ditutup tanpa LPHD:
- **D04** biaya MRV, dari dokumen proyek;
- **D07** lintasan harga, dari sumber publik;
- **D11** efek izin, dari literatur dan analisis Hansen sebelum/sesudah SK.

## Butir yang perlu LPHD

| ID | Level | Data | Peran LPHD | Utama/pendukung |
|---|---|---|---|---|
| D01 | 1 Kritis | Patroli swadaya 2017–2023 | Satu-satunya sumber catatan patroli sebelum proyek | Utama |
| D02 | 1 Kritis | Kehilangan pendapatan akibat pembatasan akses | Kerangka sampel pemegang garapan; izin dan pendampingan survei | Utama |
| D03 | 1 Kritis | Efektivitas patroli | Log patroli per HD (lokasi, intensitas) untuk dipadankan dengan Hansen per HD | Utama |
| D19 | 1 Kritis | Atribusi pembiayaan awal | Konfirmasi apakah kenaikan patroli 2024 dibiayai proyek atau swadaya | Utama (kontrak dari proyek) |
| D09 | 2 Tinggi | Biaya operasional LPHD | Laporan keuangan dan RKT | Utama |
| D10 | 2 Tinggi | Biaya per hari patroli | Anggaran dan realisasi patroli | Utama |
| D08 | 2 Tinggi | Kebakaran | Catatan kejadian dan kegiatan regu; alokasi dana kebakaran | Pendukung (seri utama dari data publik) |
| D14 | 2 Tinggi | Bagi hasil 60/40 | Salinan perjanjian sebagai pihak penanda tangan | Pendukung |
| D12 | 3 Sedang | Jumlah RT bergantung | Pendataan RT pengguna kawasan bersama desa | Utama |
| D20 | 3 Sedang | Pendapatan dasar RT | Kerangka sampel survei | Pendukung |
| D21 | 3 Sedang | Data awal KUPS | Buku kas dan anggota aktif KUPS | Pendukung |
| D23 | 4 Rendah | Pemegang garapan | Konfirmasi satuan individu vs RT | Pendukung |

## Daftar permintaan ke LPHD

Urutannya menurut level tertinggi butir yang dicakup.

1. **Log/laporan patroli 2017–2025 per HD:** tanggal, rute/lokasi, jumlah anggota, temuan. Mencakup D01, D03, D19.
2. **Catatan sumber dana patroli 2024–2025:** swadaya vs pembiayaan proyek. Mencakup D19, D01.
3. **Daftar RT pengguna kawasan dan pemegang garapan**, sebagai kerangka sampel. Mencakup D02, D12, D20, D23.
4. **Izin dan pendampingan survei rumah tangga pemegang garapan.** Mencakup D02, D20.
5. **Laporan keuangan dan RKT 2020–2025:** biaya operasional, patroli, upah harian. Mencakup D09, D10.
6. **Catatan kebakaran, kegiatan regu pengendalian, dan alokasi dana kebakaran.** Mencakup D08.
7. **Salinan perjanjian bagi manfaat.** Mencakup D14.
8. **Buku kas/omzet KUPS dan daftar anggota aktif.** Mencakup D21.

## Data sekunder (tanpa LPHD)

- **Dokumen proyek** (diminta ke pengembang, mitra, atau pendamping):
  - PDD lengkap beserta lampiran: D06, D13, D15, D22;
  - laporan MR1 dan jadwal verifikasi: D18, D19;
  - anggaran MRV dan kontrak VVB: D04, D16;
  - kontrak pembiayaan awal: D19;
  - rencana penjualan kredit: D07.
- **Publik/literatur:**
  - luas terbakar ≥ 10 tahun (mis. SiPongi KLHK, MODIS/VIIRS): D08;
  - literatur efek izin PS dan analisis Hansen sebelum/sesudah SK: D11;
  - laporan harga pasar karbon: D07;
  - data KUPS resmi dan BPS: D21, D24;
  - Hansen dan peta HCV untuk laju BAU: D05 (sudah tersedia di branch GIS).
- **Berkas peneliti sendiri:** berkas kalibrasi FINAL serta data dan skrip MAPE, Monte Carlo, dan PRCC (D05, D25).

## Catatan

- Kategori dan peran LPHD adalah penilaian audit dari isi data yang dibutuhkan, bukan konfirmasi bahwa dokumen tersebut memang ada di LPHD.
- Data survei RT hanya diminta dalam bentuk agregat; jangan menyimpan nama, NIK, atau nomor telepon dalam berkas model.
