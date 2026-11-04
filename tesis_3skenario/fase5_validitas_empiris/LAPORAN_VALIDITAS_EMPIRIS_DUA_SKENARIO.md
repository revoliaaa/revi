# Laporan Validitas Empiris Dua Skenario

**Tanggal:** 4 November 2026

**Data:** `REGISTER_PARAMETER_DAN_BUKTI_EMPIRIS.xlsx`.

**Status:**
- Model `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` dibekukan (md5 `639083f9…`; tidak ada persamaan atau variabel baru).
- PySD 3.14.3; **Vensim native: BELUM DIVERIFIKASI NATIVE**.
- NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Referensi S1 berpasangan dipakai di semua konfigurasi S2.
- D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. Selisihnya adalah dekomposisi menurut asumsi model, **bukan identifikasi kausal empiris**.

## 1. Dasar empiris pemilihan dua skenario

| Bukti historis | Konsekuensi desain |
|---|---|
| Patroli 2023 (392 kegiatan, ±2.160 keikutsertaan), 2024 (2.533 HOK, 20 HD), dan 2025 (3.011 HOK, 25 HD) dibiayai mitra proyek karbon yang sama | Intensitas patroli historis tidak dapat diperlakukan sebagai patroli swadaya. Skenario lama "PS swadaya" tidak memiliki dasar data |
| PS sudah berjalan (hak kelola 24 HD terbit 2017–2020; HD Kemboja 2024) | Skenario lama "tanpa PS" adalah kontrafaktual hipotetis, bukan alternatif kebijakan yang tersedia |
| Pembiayaan mitra 2024–2025 dan rekrutmen anggota (183 → 254) terjadi sebelum ada penjualan kredit | Pembiayaan historis diperlakukan sebagai fakta bersama S1 dan S2 |

**Keputusan:** dua skenario (S1, S2) lebih dapat dipertanggungjawabkan daripada empat skenario lama. Keduanya hanya berbeda pada unsur yang memang merupakan pilihan kebijakan ke depan (pembiayaan karbon), sedangkan sejarah pembiayaan diperlakukan sama.

**Batas keputusan ini:** S2 tetap memuat asumsi pembiayaan jembatan masa depan (J1) yang tidak berbasis komitmen. Fase 5 memisahkan efek asumsi itu (D1 − D0) dari efek penjualan karbon (D2 − D1). Temuannya: pada USD ≤ 20, sebagian besar hasil S2 berasal dari asumsi jembatan.

## 2. Ringkasan kelas data parameter penting

Rincian lengkap di register; 39 baris.

| Kelas | Jumlah | Contoh |
|---|---|---|
| A: data empiris langsung | 5 | Upah patroli Rp150.000/HOK; HOK 2024/2025; kurs; catatan 2.144 pemegang garapan |
| B: diturunkan dari data | 8 | Keikutsertaan 2023; laju deforestasi terkalibrasi; porsi Project Area; buffer PDD; surplus dan bagi hasil KUPS |
| C: literatur/dokumen resmi | 11 | Efektivitas perlindungan; biaya MRV; biaya penerbitan; pajak/PNBP 5 %; pendapatan dasar; porsi pendapatan hutan; leakage; harga; jeda verifikasi |
| D: asumsi eksploratif | 15 | **Biaya total patroli Rp260.000/HOK**; jembatan J1/JP; biaya pengembangan proyek; **RT bergantung 5.328 (proksi)**; faktor keunikan garapan; **pengali kehilangan akses**; porsi pemicu deforestasi; biaya reaktivasi dan reinvestasi KUPS; k; porsi upah bersih; diskonto; 60/40; kapasitas LPHD; upah kebakaran |

## 3. Pemeriksaan prioritas

| Prioritas | Parameter | Nilai | Kelas | Sumber | Kebutuhan verifikasi |
|---|---|---|---|---|---|
| 1 | Upah Harian Patroli Berbayar | 150.000 Rp/HOK | A | Konfirmasi peneliti 2026-11-03 (pelaksana) | Bukti pembayaran 2024–2025 (daftar hadir/kuitansi) untuk menegaskan seluruh 5.544 HOK dibayar tunai |
| 2 | Biaya per Hari Patroli | 260.000 Rp/HOK | D | Cuplikan Perbup Kotawaringin Barat 29/2020 (bukan Kubu Raya); pembanding rencana anggaran WAS Rp966,84 juta/th (File 4) | Realisasi biaya patroli mitra 2024–2025 per komponen (BBM, konsumsi, alat, transport) |
| 3 | HOK Patroli Pembiayaan Awal Aktual 2024 / 2025 | 2.533 / 3.011 HOK/th | A | Rekap final patroli peneliti (20 HD / 25 HD) | – |
| 3 | Keikutsertaan Patroli 2023 | 2.160 HOK/th | B | 392 kegiatan × 5,51 orang/kegiatan (MR1 2024) | Daftar peserta 2023 |
| 4 | Realisasi pembiayaan mitra 2024–2025 (Status Pembiayaan Awal = 0, hibah) | Rp1.441.440.000 (= 5.544 × 260.000) Rp | B (HOK) / D (Rp, status) | HOK = A; biaya per HOK = D; status hibah = D | Bukti pengeluaran mitra 2023–2025; status hibah/talangan; apakah bagian proyek karbon (prior consideration) |
| 5 | Besaran Pembiayaan Jembatan per Tahun / Durasi | 782.860.000 / 5 Rp/th / th | D | Eksperimen: J1 = 3.011 HOK × 260.000 (meniru tingkat 2025) | Komitmen/kontrak mitra (besaran, durasi, status hibah/talangan, prioritas pemulihan) |
| 6 | Biaya Monitoring per Ha per Tahun | 1.980 Rp/(ha·th) | C | Rendon Thompson dkk. 2013 (Peru) | Anggaran MRV proyek Delta Kapuas (PDD/kontrak VVB) |
| 6 | Biaya Verifikasi per Kejadian | 742.500.000 Rp/kejadian | C | WCS/Landscapes and Livelihoods 2024; Beers dkk. 2019; Verra Fee Schedule v1.2 | Penawaran VVB aktual |
| 6 | Biaya Penerbitan per Kredit | 0,25 USD/tCO2e | C (dokumen resmi standar) | Verra Program Fee Schedule v1.2 | – |
| 6 | Proporsi Pajak dan Pungutan Karbon | 0,05 – | C (dokumen resmi) | PP 36/2024; Permenhut 6/2026 Ps. 46 | Perlakuan PPN unit karbon |
| 6 | Biaya Pengembangan Proyek | 0 Rp/th | D | Tidak ada data | Biaya pengembangan PDD, validasi, registrasi aktual |
| 7 | Masyarakat Bergantung pada Hutan Awal | 5.328 orang (= RT) | D (komentar model: kelas bukti D) | PROKSI: 4.104 (20 HD, File A) × pekerja SDA 25 HD/20 HD (24.099/18.563) | Sensus/daftar RT bergantung hutan per HD |
| 8 | RT Pemegang Garapan dalam HD | 2.144 RT (individu) | A (catatan) / D (individu = RT) | File A sheet Ang Kerja (Andil Garapan): pemegang SHM/SKT/turun-temurun di 15 desa, 4.322 ha | Verifikasi RT unik per catatan |
| 8 | Faktor Keunikan Catatan Garapan | 1 – | D | Tidak tersedia | Pencocokan nama/NIK pemegang garapan |
| 8 | Laju Pertumbuhan Penduduk (diterapkan juga ke RT terdampak) | 0,0166 /th | B (laju penduduk) / D (penerapan ke pemegang garapan) | File A sheet All/Vensim_Clean | Apakah jumlah pemegang garapan tumbuh |
| 9 | Pengali Kehilangan Akses | 1 – | D | Angelsen dkk. 2014 (rentang PEN, C); porsi pemicu = asumsi D | Survei kehilangan pendapatan akibat pembatasan akses (pemegang garapan) |
| 9 | Proporsi Pendapatan Hutan dari Aktivitas Pemicu Deforestasi | 0,25 – | D | Asumsi peneliti | Idem |
| 9 | Proporsi Pendapatan dari Hutan | 0,201 – | C | Angelsen dkk. 2014 (PEN Asia; rentang 5,5–32,6 %) | Data pendapatan lokal |
| 9 | Pendapatan Dasar RT Bergantung | 41.760.000 Rp/RT/th | C | Setiawan dkk. 2021, Tabel 4 (70 responden anggota LPHD) | Survei terbaru 25 HD |
| 10 | Biaya Reaktivasi KUPS (= Biaya Pembentukan KUPS) | 50.000.000 Rp/unit | D | Asumsi: 2 × biaya pendampingan tahunan | Biaya nyata pembentukan/reaktivasi KUPS |
| 10 | Porsi Laba Ditahan untuk Reinvestasi | 0,5 – | D | Asumsi | Data keuangan KUPS 2024–2025 |
| 10 | Surplus Operasional per KUPS Produktif | 6.647.300 Rp/unit/th | B | Lembar Status KUPS 25 Desa Minggu IV Okt 2026 (33 unit; 14 menjual) | Pencatatan OPEX in-kind |
| 10 | Porsi Surplus KUPS Dibagikan ke Anggota | 0,263 – | B | Audit 3 unit bagi hasil | Data bagi hasil semua unit |
|  | Tingkat Keberlanjutan Patroli Reguler (k) | 0,5 – | D | Nilai tengah eksploratif | Data patroli pasca-2025 tanpa pembiayaan |
|  | Efektivitas Perlindungan Penuh terhadap Deforestasi | 0,37 – | C / D (bentuk) | Literatur pengelolaan hutan komunitas (Nepal); dosis-respons linear = asumsi struktural | Bukti lokal hubungan intensitas patroli–deforestasi |
|  | Laju deforestasi BAU (mis. Laju HRS menjadi NonHutan BAU) | 0,00956 (HRS) /th | B | Kalibrasi HCV + Hansen GFC; validasi tertahan 2017–2024 rasio 0,98 | – |
|  | Proporsi Kredit REDD dalam Project Area | 0,682 – | B (provisional) | Pangsa loss bruto Hansen di Project Area (DKP-GIS-MASTER v1.0) | Ketentuan metodologi/PDD |
|  | Proporsi Buffer Risiko Karbon | 0,12 – | B | PDD Delta Kapuas hal. 331 (NPR 12 %) | Validasi Verra |
|  | Proporsi Leakage Karbon | 0,10 – | C | Filewod & McCarney 2023; Haya dkk. 2023 (median VM0007 ±11 %) | Nilai PDD |
|  | Harga Karbon | 6 (dasar), uji 10/20/35 USD/tCO2e | C | Ecosystem Marketplace 2025 (rerata REDD+ 2024: 6,03) | Harga kontrak/ERPA |
|  | Nilai Tukar USD ke Rupiah | 16.500 Rp/USD | A | Bank Indonesia SEKI Tabel V.40 | – |
|  | Delay Verifikasi dan Penerbitan Kredit | 3 th | C | Liu & Gurrola-Perez 2025 (rerata 2,76 th) | Jadwal verifikasi proyek |
|  | Proporsi Manfaat Masyarakat (60/40) | 0,6 – | D (belum terverifikasi kontrak) | Instruksi peneliti | Perjanjian bagi hasil |
|  | Porsi Upah sebagai Tambahan Bersih | 0,5 – | D | Asumsi | Data alokasi waktu kerja |
|  | Upah Harian Pengendalian Kebakaran | 130.000 Rp/HOK | D (belum dikonfirmasi untuk lokasi) | Cuplikan Perbup Kobar 29/2020 | Konfirmasi upah MPA lokal |
|  | Tingkat Diskonto | 0,10 /th | D | Tidak bersumber | Pilihan diskonto beralasan |
|  | Anggota Patroli Roster 2025 | 254 orang | A/B | MR1 roster 2025 | – |
|  | Indeks Kapasitas LPHD Awal | 0,5 – | D | Asumsi peneliti | Penilaian kapasitas LPHD |
|  | Hari Logistik Swadaya per Anggota | 9,17 HOK/orang/th | C (komentar model) | Log 2023 | – |

## 4. Implikasi untuk klaim

- **Yang didukung data (A/B):**
  - fakta pembiayaan historis dan HOK 2024–2025;
  - upah patroli;
  - laju deforestasi BAU terkalibrasi;
  - struktur kondisi awal.
- **Yang bergantung literatur (C):** efektivitas perlindungan dan biaya MRV. Efektivitas adalah parameter paling berpengaruh: PRCC 0,83 pada deforestasi dihindari; porsi jembatan USD 20 berkisar 10–100 %.
- **Yang masih asumsi (D) dan menentukan kesimpulan:**
  - biaya total per HOK, yang menentukan atribusi jembatan vs penjualan;
  - pengali kehilangan akses, yang menentukan **arah** dampak pendapatan RT;
  - jembatan, yang menentukan besaran perlindungan pada USD ≤ 20;
  - parameter KUPS;
  - jumlah RT bergantung (proksi).

  Temuan yang bergantung pada parameter-parameter ini hanya dapat disajikan sebagai **proyeksi bersyarat**.
