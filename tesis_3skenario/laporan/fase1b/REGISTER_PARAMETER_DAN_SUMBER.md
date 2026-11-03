# Register Parameter dan Sumber (Fase 1B)

**Kelas:** A empiris terverifikasi; B empiris parsial/turunan; C literatur; D asumsi eksploratif; Desain.

**Status:**
- **TETAP** = dipakai apa adanya;
- **PERLU DATA** = nilai default hanya penanda, jangan dilaporkan sebagai fakta;
- **SENSITIVITAS** = hanya dapat dibenarkan sebagai rentang uji.

## 1. Parameter baru atau berubah makna

| Parameter | Nilai dasar | Satuan | Rentang uji | Sumber | Kelas | Status |
|---|---|---|---|---|---|---|
| `Skenario Kebijakan` | 1 / 2 | Dmnl | – | Desain | Desain | TETAP |
| `HOK Patroli Pembiayaan Awal Aktual 2024` | 2.533 | HOK/Year | – | Rekap final peneliti (20 HD) | A | TETAP |
| `HOK Patroli Pembiayaan Awal Aktual 2025` | 3.011 | HOK/Year | – | Rekap final peneliti (25 HD) | A | TETAP |
| `Anggota Patroli Roster 2025` | 254 | People | – | MR1 roster 2025 (catatan register A1) | B | TETAP; mohon konfirmasi |
| `HOK Patroli per Anggota 2025` | 11,85 | HOK/(People·Year) | – | 3.011 ÷ 254 | B | TETAP |
| `Tingkat Keberlanjutan Patroli Reguler` (k) | 0,5 | Dmnl | 0 / 0,25 / 0,5 / 0,75 / 1 | Asumsi; tidak ada data pasca-2025 | D | SENSITIVITAS |
| `Laju Penurunan Partisipasi Sukarela` | 0 | 1/Year | 0 / 0,01 / 0,03 | Asumsi | D | SENSITIVITAS |
| `Proporsi Penggantian Anggota Patroli` | 1 | Dmnl | 1 / 0,625 (jangan dikombinasikan dengan laju > 0) | A1 | D | SENSITIVITAS |
| `Keikutsertaan Patroli 2023` | 2.160 | HOK/Year | 0 / 1.568 / 2.160 | 392 kegiatan × 5,51 orang (estimasi peneliti; 5,51 dari MR1 2024) | B | TETAP + SENSITIVITAS |
| `Switch Dana Non Karbon`, `Dana Operasional Non Karbon Tunai` | 0, 0 | Dmnl, Rp/Year | data | Tidak ada data dana desa/APBD/program 2026+ | D | **PERLU DATA** |
| `Tahun Mulai/Akhir Dana Non Karbon` | 2026 / 2087 | Year | data | Asumsi | D | PERLU DATA |
| `Dukungan Material Rehabilitasi Non Karbon` | 0 | Rp/Year | 0 / ±100 juta (20,13 ha × Rp 4,99 juta) | Belum diketahui pembiayaan realisasi historis 0,0123 | D | **PERLU DATA** |
| `Porsi Tenaga Penanaman Non Karbon Dibayar` | 0 | Dmnl | 0 / 1 | Belum diketahui apakah penanaman historis berupah | D | PERLU DATA |
| `Biaya Bibit dan Material per Ha` | 4,99 juta | Rp/Ha | ±30 % | Turunan: Rp 14 juta − 85 × Rp 106.000 | B | TETAP |
| `Nilai Pendampingan Kelembagaan Non Tunai` | 0 | Rp/Year | data | Program pendampingan pemerintah/NGO belum tercatat | D | PERLU DATA |
| `Laju Pembelajaran Kelembagaan` | 0 | Dmnl | 0 / 0,1 / 0,2 | Asumsi | D | SENSITIVITAS |
| `Porsi Laba Ditahan untuk Reinvestasi` | 0,5 | Dmnl | 0 / 0,5 / 1 | Asumsi | D | SENSITIVITAS |
| `Biaya Reaktivasi KUPS` | 50 juta (= pembentukan) | Rp/Unit | 12,5 / 25 / 50 juta | Asumsi | D | SENSITIVITAS |
| `Upah Setara Non Tunai Patroli` | 130.000 | Rp/HOK | – | = upah patroli berbayar (Perbup Kobar 29/2020, cuplikan) | C | TETAP |
| `Delay Pembayaran Penjualan` | 0 | Year | 0 / 0,5 / 1 | Asumsi | D | SENSITIVITAS |
| `Delay Verifikasi dan Penerbitan Kredit` | 3 | Year | 3 / 4 / 5 | Liu dan Gurrola-Perez 2025 | A (register A1) | TETAP + SENSITIVITAS |
| `Status Pembiayaan Awal` | 0 (hibah) | Dmnl | 0 / 1 | Status aktual belum diketahui | D | **PERLU DATA**; dua varian |
| `Switch Baseline Kredit Konservatif` | 0 (BAU) | Dmnl | 0 / 1 | Desain | Desain | dua varian dilaporkan |
| `Faktor Rekonsiliasi Reversal Kredit A2` | 1 | Dmnl | – | Kalibrasi lama per harga dihapus | Desain | TETAP |
| `Tingkat Diskonto` | 0,10 | 1/Year | 0,06 / 0,10 / 0,14 | Tidak bersumber | D | SENSITIVITAS; mohon dasar (SBN/WACC) |
| `Biaya Pengembangan Proyek` | 0 | Rp/Year | data | PDD/validasi/registrasi belum tercatat | D | **PERLU DATA** |

## 2. Parameter A1 yang dipertahankan dan relevan dengan revisi

| Parameter | Nilai | Satuan | Sumber | Kelas | Catatan |
|---|---|---|---|---|---|
| `Biaya per Hari Patroli` | 260.000 | Rp/HOK | Perbup Kotawaringin Barat 29/2020 (cuplikan); File 4 Potensi VCU kolom AL | C | Model mendeklarasikan per orang-hari. Dokumen asli tidak ada di paket, jadi **belum terverifikasi**. Bila per regu-hari (4–5,5 orang), biayanya ±Rp 47.000–65.000 per HOK, di bawah upah Rp 130.000, sehingga tafsiran per orang-hari lebih masuk akal |
| `Upah Harian Patroli Berbayar` | 130.000 | Rp/HOK | idem | C | Diasumsikan juga dibayarkan pada patroli historis 2024–2025 (perlu konfirmasi) |
| `Biaya Operasional Patroli Sukarela per Anggota per Tahun` | 1,19 juta | Rp/(People·Year) | File A sheet Patroli | C | Kini dipakai sebagai nilai logistik non-tunai |
| `Maksimum Hari Patroli per Anggota` | 48 | HOK/(People·Year) | Asumsi | D | Kapasitas |
| `Frekuensi Patroli Ideal per Anggota`; `Jumlah Anggota per Regu`; `Cakupan Kawasan per Regu` | 12; 4; 750 | – | Asumsi / tidak bersumber | D | Penyebut intensitas (kebutuhan 7.996 HOK). SENSITIVITAS ±50 % |
| `Rasio Risiko Penempatan Patroli Swadaya` | 0,651 | Dmnl | Log patroli 2023 × WAS kolom K | C | Kini berlaku untuk semua patroli non-karbon. SENSITIVITAS 0,651 / 1 |
| `Efektivitas Perlindungan Penuh terhadap Deforestasi` | 0,37 | Dmnl | Oldekop dkk. 2019; Sze dkk. 2022 | D (register FINAL) | Monte Carlo 0,075–0,59 |
| `Waktu Penyesuaian Efek Pengelolaan PS` | 3 | Year | Asumsi | D | Monte Carlo 1–5 |
| `Laju Ketidakaktifan KUPS Dasar`; anggota KUPS | 0,05 | 1/Year | Asumsi | D | – |
| `Surplus Operasional per KUPS Produktif` | 6,647 juta | Rp/(Unit·Year) | Status KUPS Okt 2026 | B (lemah) | Sumber laba ditahan |
| `Porsi Surplus KUPS Dibagikan ke Anggota` | 0,263 | Dmnl | MR1 KUPS | B | – |
| `Proporsi Realisasi Penanaman BAU` | 0,0123 | Dmnl | File A sheet Penanaman | C | Kini batas atas penanaman non-karbon |
| `Biaya Penanaman per Ha` | 14 juta | Rp/Ha | Mongabay 2022 (BRGM) dkk. | C | – |
| `Biaya Pemeliharaan Tanaman per Ha per Tahun` | 1,4 juta | Rp/(Ha·Year) | Asumsi | D | – |
| `Indeks Kapasitas LPHD Awal`; realisasi penuh | 0,5; 0,8 | Dmnl | Asumsi | D | – |
| `Harga Karbon` | 6 / 10 / 15 / 20 / 35 | USD/tCO₂e | Ecosystem Marketplace 2025 (dasar 6) | B | Eksperimen |
| `Harga Karbon Removal` (ARR) | 20 (tetap) | USD/tCO₂e | A1 | – | **Perlu keputusan:** tetap 20 atau ikut harga REDD |
| `Proporsi Manfaat Masyarakat` | 0,6 | Dmnl | Desain proyek | Desain | 60/40 |
| Biaya MRV: monitoring 1.980 Rp/ha/th; verifikasi 742,5 juta/5 th; transaksi 0,22 %; pajak 5 %; penerbitan USD 0,25 | – | – | Rendon Thompson 2013; WCS 2024; IDXCarbon; PP 36/2024 | B/A | – |
| `Proporsi Leakage Karbon`; buffer; proporsi PA | 0,10; 0,12; 0,682 | Dmnl | Filewod dan McCarney 2023; PDD; GIS (provisional) | C; B; B | – |
| `Laju Penjualan Kredit`; kedaluwarsa | 0,7; 0,1 | 1/Year | Proksi | D | – |
| `Nilai Tukar USD ke Rupiah` | 16.500 | Rp/USD | BI SEKI (label kelas tidak konsisten A/C) | A/C | – |
| `Proporsi Deforestasi Terkait Kebakaran` | 0 | Dmnl | Asumsi | D | **Tidak diubah:** laju BAU sudah memuat kehilangan akibat kebakaran; mengaktifkan berisiko menghitung ganda |
| Parameter ekologis (laju BAU, regenerasi, densitas karbon, stok awal) | A1 | – | HCV 2024, Hansen, kalibrasi | A/B/C | **Tidak diubah** |

## 3. Data yang diminta dari peneliti

1. Konfirmasi roster patroli 2025 (254 orang).
2. Konfirmasi apakah peserta patroli 2024–2025 menerima upah (dan berapa).
3. Dokumen sumber Rp 260.000: per orang-hari atau per regu-hari.
4. Data patroli 2026 bila sudah ada (pengganti k).
5. Sumber pembiayaan realisasi penanaman historis (laju 0,0123) dan apakah tenaganya dibayar.
6. Dana non-karbon 2026+ (dana desa, APBD, KLHK/BPDAS, NGO), nilai dan periodenya.
7. Status pembiayaan awal mitra: hibah atau talangan.
8. Biaya pengembangan proyek (PDD, validasi, registrasi).
9. Dasar tingkat diskonto.
10. Konfirmasi pembentukan KUPS 2024–2025 (+15/+5 MR1 vs "tidak ada" File A).
11. Keputusan harga ARR (tetap USD 20 atau mengikuti harga REDD).
