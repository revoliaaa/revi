# Rancangan Koreksi Model: Dua Skenario (Fase 1, belum diterapkan)

**Status:** rancangan untuk ditinjau peneliti. **Belum ada persamaan yang diubah dan belum ada simulasi yang dijalankan.**

**Dasar:**
- model `DKP_25HD_FINAL_3SKENARIO.mdl` (rekonstruksi A1 + REV-3S);
- audit `AUDIT_S2_MODEL_3SKENARIO.md`;
- register variabel A1.

**Keterbatasan dasar.** Berkas `.mdl` A1 asli tidak tersedia di paket. Rekonstruksi disusun dari register variabel dan mereproduksi hasil resmi A1 tanpa selisih (33.068 nilai). Kecocokan ini membuktikan persamaannya setara, **bukan bahwa berkasnya identik**: tata letak sketch, komentar lengkap, dan pengaturan Vensim lain dapat berbeda. Bila `.mdl` A1 asli tersedia, seluruh perubahan di bawah sebaiknya diterapkan langsung pada berkas itu.

**Konvensi kode skenario baru:** `Skenario Kebijakan` = 1 → **S1** PS dengan pembiayaan terbatas; = 2 → **S2** PS + perdagangan karbon.

**Kelas sumber:** A empiris terverifikasi; B empiris parsial; C literatur; D asumsi eksploratif; Desain.

---

## 1. Prinsip desain

1. **S1 dan S2 identik kecuali mekanisme karbon.** Semua switch PS, pembiayaan historis, patroli reguler, rehabilitasi, KUPS, dan kelembagaan aktif di kedua skenario. Satu-satunya pembeda adalah `Switch Karbon`, dan switch ini hanya menggerbang **penerbitan kredit, penjualan, dan penerimaan kas karbon**, bukan kegiatan.
2. **Kegiatan dibatasi sumber daya, bukan oleh switch.** Belanja tunai LPHD dibatasi saldo kas. Kerja sukarela dibatasi anggota dan kapasitas. Tidak ada kas yang muncul tanpa aliran masuk yang dimodelkan.
3. **Empat jenis sumber daya dipisah:**
   - (i) pembiayaan awal historis mitra 2024–2025;
   - (ii) kas operasional non-karbon (default 0 sampai ada data);
   - (iii) kontribusi tenaga dan sumber daya non-tunai;
   - (iv) kas karbon (S2).
4. **Baseline kredit karbon adalah jalur referensi akuntansi**, bukan skenario kebijakan. Rantai stok `… Baseline` yang sudah ada dipertahankan.
5. **Struktur 16 View, stok-aliran, dan parameter ekologis terkalibrasi dipertahankan.**

---

## 2. Matriks persamaan: lama vs usulan

### 2.1 Kesalahan struktural yang wajib diperbaiki

| No | Variabel | Persamaan lama | Persamaan usulan | Alasan | Sumber parameter | Implikasi |
|---|---|---|---|---|---|---|
| K1 | `Hari Patroli Swadaya` → **diganti** `HOK Patroli Reguler PS` | `Switch PS*Switch Patroli Swadaya Reguler*(1-Periode Pembiayaan Awal)*MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota` | `Switch PS*(1-Periode Pembiayaan Awal)*STEP(1, Tahun Akhir Pembiayaan Awal+1)*MIN(Kapasitas Hari Patroli Anggota, Anggota Patroli Aktif*HOK Patroli per Anggota 2025*Tingkat Keberlanjutan Patroli Reguler)` | Audit A1: patroli dipaksa 0. Patroli reguler mulai 2026, tidak tumpang tindih dengan 2024–2025, dan mengikuti jumlah anggota (mekanisme penjelas), bukan konstanta | `HOK Patroli per Anggota 2025` = 3.011/254 = 11,85 HOK/orang/th (data final 2025 ÷ roster 2025; B). `Tingkat Keberlanjutan Patroli Reguler` 0–1 (D; dasar diputuskan peneliti, lihat 4.1) | S1 dan S2 punya patroli reguler yang sama. Tingkat 2025 tidak diulang otomatis: patroli turun bila anggota menyusut (K2) |
| K2 | `Penambahan Anggota Patroli` (cabang penggantian) | `… Pengurangan Anggota Patroli*Proporsi Penggantian Anggota Patroli Swadaya …` (penggantian = 1) | `… Pengurangan Anggota Patroli*Proporsi Penggantian Anggota Patroli Efektif …`, dengan `Proporsi Penggantian Anggota Patroli Efektif = MIN(1, Proporsi Penggantian Dasar*Indeks Kapasitas LPHD/Indeks Kapasitas untuk Realisasi Penuh)` | Penggantian 100 % tanpa mekanisme (audit A5) membuat anggota, dan karena K1 juga patroli, konstan sampai 2087 | `Proporsi Penggantian Dasar` = 1 (D); kapasitas 0,5/0,8 (D) | Pada kapasitas 0,5, penggantian 62,5 % dan anggota turun ±1,9 %/th. Bila kapasitas naik (K6, termasuk lewat dana karbon), penggantian mendekati 100 %. Cabang rekrutmen dana LPHD tetap ada (K4) |
| K3 | `Hari Patroli Didanai` | `(Pendanaan Awal untuk Patroli + Realisasi Belanja Perlindungan)/Biaya per Hari Patroli + Hari Patroli Pembiayaan Awal` | `Hari Patroli Pembiayaan Awal + MIN(MAX(0, Kapasitas Hari Patroli Anggota − HOK Patroli Reguler PS − Hari Patroli Pembiayaan Awal), Realisasi Belanja Perlindungan/Biaya per Hari Patroli)` | Mencegah patroli melampaui kapasitas anggota. Patroli historis hanya masuk sekali (HOK aktual, bukan konversi rupiah) | Rp 260.000/HOK (C; lihat 4.6) | Hari didanai = historis (2024–2025) + tambahan dari kas LPHD. Tidak ada patroli dari kas karbon sebelum kas diterima, karena belanja dibatasi saldo |
| K4 | 6 × `Alokasi Dana …` dan `Penambahan Anggota Patroli` (cabang rekrutmen) | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi…, Kebutuhan…)`; rekrutmen `Switch Karbon*IF(Alokasi Dana Perlindungan>0 …)` | `MIN(Dana Desa Tersedia*Proporsi…, Kebutuhan…)` tanpa `Switch Karbon`; rekrutmen `IF THEN ELSE(Alokasi Dana Perlindungan>0, …)` | Audit A2: `Switch Karbon` menggerbang belanja. Belanja sudah dibatasi `Dana Desa Tersedia` = saldo kas | – | Pada S1 belanja hanya terjadi bila ada kas non-karbon (K5). Bila kas non-karbon = 0, belanja = 0 tanpa kas fiktif |
| K5 | `Dana Desa Diterima` → dipecah | `IF Switch Dana Program Eksogen=1 THEN Switch Karbon*Dana Program Eksogen*(periode) ELSE Dana Program PS dari Karbon` | `Kas Masuk LPHD Karbon + Kas Masuk LPHD Non Karbon`; `Kas Masuk LPHD Karbon = Dana Program PS dari Karbon`; `Kas Masuk LPHD Non Karbon = Switch PS*Dana Operasional Non Karbon Tunai*(STEP(1,Tahun Mulai Dana Non Karbon)-STEP(1,Tahun Akhir Dana Non Karbon+1))` | Audit A2: dana non-karbon dikalikan `Switch Karbon`. Arus kas karbon dan non-karbon dipisahkan | `Dana Operasional Non Karbon Tunai` **default 0** (D, belum ada data). Rentang uji diputuskan peneliti | Tidak ada kas non-karbon fiktif. Kesenjangan pembiayaan S1 terbaca jujur. Bila peneliti punya data dana desa/APBD/program, nilainya masuk di sini dan berlaku sama di S1 dan S2 |
| K6 | `Target Kapasitas LPHD` dan `Faktor Penguatan Kelembagaan dari Karbon` | `Target = Awal + (1−Awal)*Faktor Penguatan Kelembagaan dari Karbon`; faktor = belanja kelembagaan ÷ kebutuhan | `Target = MIN(1, Awal + (1−Awal)*MIN(1, Faktor Penguatan Kelembagaan + Efek Pembelajaran Kelembagaan))`; `Faktor Penguatan Kelembagaan = (Realisasi Belanja Penguatan Kelembagaan + Nilai Pendampingan Kelembagaan Non Tunai)/Kebutuhan Dana Penguatan Kelembagaan`; `Efek Pembelajaran Kelembagaan = Laju Pembelajaran*Indeks Kegiatan PS Terlaksana` | Audit B: kapasitas hanya naik lewat karbon. Kini sumbernya belanja kelembagaan (kas mana pun), pendampingan non-tunai, dan pembelajaran dari kegiatan | `Nilai Pendampingan Kelembagaan Non Tunai` default 0 (D); `Laju Pembelajaran` default 0 (D; sensitivitas 0–0,2); `Indeks Kegiatan PS Terlaksana` = intensitas perlindungan | LPHD tetap aktif di S1. Kapasitas tidak naik otomatis: tanpa sumber, tetap 0,5 |
| K7 | `Penambahan KUPS` (penggantian) | `… KUPS Menjadi Tidak Aktif*Proporsi Penggantian KUPS Tanpa Dana Karbon (=1) …` | `… KUPS Menjadi Tidak Aktif*MIN(1, Proporsi Penggantian KUPS Dasar*Indeks Kapasitas LPHD/Indeks Kapasitas untuk Realisasi Penuh) + Pembentukan KUPS Didanai Dana LPHD …` | Audit B: penggantian 100 % tanpa mekanisme. Pembentukan baru memakai kas LPHD (karbon maupun non-karbon) | Penggantian dasar 1 (D); biaya pembentukan Rp 50 juta (D) | KUPS S1 menurun perlahan bila kapasitas rendah dan tidak ada kas. KUPS tidak berhenti otomatis tanpa karbon |
| K8 | `Pembentukan KUPS Didanai Karbon`, `Penanaman Didanai Karbon`, `Luas Penanaman Karbon Direncanakan`, `Pembentukan KUPS Direncanakan` | `Switch Karbon*…` | Hapus `Switch Karbon`; ganti nama menjadi `… Didanai Dana LPHD` (nama lama dicatat) | Sama dengan K4: dibatasi belanja aktual | – | Kegiatan karbon S2 tetap sama. S1 hanya bila ada kas non-karbon |
| K9 | Rehabilitasi non-karbon: `Penambahan Luas Penanaman` dan `Manfaat Ekonomi Penanaman` | Penanaman 20,13 ha/th tanpa sumber; upah = HOK penanaman × Rp 106.000 dibayar dan masuk pendapatan RT | Penanaman tetap: `Switch Rehabilitasi*(1-Periode Historis)*MIN(Proporsi Realisasi Penanaman*Target Penanaman, …)`. **Upah dipisah:** `HOK Penanaman Berupah = HOK Penanaman*Porsi Penanaman Non Karbon Berupah`; `HOK Penanaman Sukarela = HOK Penanaman − HOK Penanaman Berupah`; `Manfaat Ekonomi Penanaman = HOK Penanaman Berupah*Upah Penanaman per HOK` | Audit A4: upah tanpa pembayaran yang dimodelkan. Laju realisasi historis 0,0123 (File A, C) dipertahankan agar rehabilitasi tidak berhenti | `Porsi Penanaman Non Karbon Berupah` (D): **0** bila tidak ada pembayar yang tercatat; 1 bila peneliti dapat menunjukkan program pemerintah/mitra yang membayar | Pendapatan RT tidak lagi memuat upah tanpa sumber. Nilai kerja sukarela dicatat di K11 |
| K10 | `Dana PS Eksisting` / `Biaya Pengelolaan PS Non Karbon` | 254 anggota × Rp 1,19 juta + 20,13 ha × Rp 14 juta + KUPS × Rp 25 juta = Rp 1,42 miliar/th; tidak terhubung | **Indikator akuntansi**, bukan kas: `Estimasi Biaya Kegiatan PS Non Karbon = Anggota Patroli Berpartisipasi*Biaya Operasional Patroli Sukarela per Anggota per Tahun + Penambahan Luas Penanaman*Biaya Penanaman per Ha*(1−Porsi Didanai Kas) + Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun*(1−Porsi Didanai Kas)` | Audit A3. Komponen patroli kini hanya untuk anggota yang benar-benar berpatroli | Parameter lama (C/D) | Dilaporkan sebagai "biaya kegiatan yang ditanggung non-tunai atau oleh sumber tak tercatat". Tidak masuk saldo LPHD, tidak masuk NPV |
| K11 | Variabel baru: tenaga non-tunai | `Nilai Kontribusi Swadaya = Hari Patroli Swadaya*Rp 260.000` | `HOK Sukarela PS = HOK Patroli Reguler PS + HOK Penanaman Sukarela`; `Nilai Kontribusi Tenaga Non Tunai = HOK Sukarela PS*Upah Setara Non Tunai` | Audit A: kontribusi non-tunai hilang. Dinilai pada upah setara, bukan biaya patroli Rp 260.000 (yang memuat logistik) | `Upah Setara Non Tunai` = Rp 130.000/HOK (setara upah patroli, C) | Tidak masuk pendapatan tunai RT. Dilaporkan terpisah |
| K12 | `Kesempatan Kerja PS` dan `Kesempatan Kerja Setara Penuh` | `Total HOK PS + HOK Patroli Berbayar + HOK Kebakaran` | `HOK Berupah PS = Hari Patroli Didanai + HOK Penanaman Berupah + HOK Penanaman Didanai Dana LPHD + HOK Pengendalian Kebakaran`; `Kesempatan Kerja PS = HOK Berupah PS + HOK Sukarela PS`; FTE dihitung terpisah untuk berupah dan sukarela | F7: pisahkan berupah dan sukarela | 300 HOK/FTE (B) | `Upah Kegiatan PS` hanya dari HOK berupah. Pendapatan RT tidak memuat nilai sukarela |
| K13 | `Total Partisipasi Kegiatan PS`, `Penerima Manfaat Kegiatan PS` | memasukkan semua `Anggota Patroli Aktif` | `Anggota Patroli Berpartisipasi = MIN(Anggota Patroli Aktif, (HOK Patroli Reguler PS + Hari Patroli Didanai)/HOK Patroli per Anggota 2025)` menggantikan `Anggota Patroli Aktif` di kedua persamaan | Audit A5/R7 | – | Partisipasi tidak terdistorsi oleh anggota pasif |
| K14 | `SMOOTHI` pada `Efek Pengelolaan PS Aktif` dan `… Tanpa Karbon` | nilai awal = `Respons Perlindungan` pada 2024 (0,317, dari patroli 2024) | nilai awal = `Respons Perlindungan Awal 2023 = Cakupan dari Indeks Intensitas Patroli 2023`, dengan `Indeks Intensitas Patroli 2023 = Keikutsertaan Patroli 2023/Kebutuhan Hari Patroli` | Audit A6. Patroli sudah berjalan sejak 2023 dengan dukungan mitra, jadi nilai awal mengacu pada 2023, bukan 2024. Nama `Indeks Intensitas Swadaya 2023` diganti (bukan swadaya) | `Keikutsertaan Patroli 2023` ≈ 2.160 (392 kegiatan × 5,51; estimasi peneliti, B); lama: 1.568 (392 × 4) | Efek awal lebih rendah daripada yang memakai 2024, dan jeda penyesuaian 3 tahun benar-benar bekerja. Berlaku sama di S1 dan S2. Narasi makalah harus disesuaikan |
| K15 | `Tingkat Kecukupan Patroli Referensi`, `Total Partisipasi Referensi` | `SAMPLE IF TRUE(Time <= 2025, X, X)` | `INITIAL(X)` (acuan kondisi awal 2024) | Audit B: acuan dibekukan di puncak pembiayaan awal | – | Tidak berdampak selama sensitivitas tekanan = 0. Mencegah bias bila diaktifkan |

### 2.2 Penyesuaian konfigurasi dua skenario

| No | Variabel | Lama | Usulan | Alasan / implikasi |
|---|---|---|---|---|
| S-1 | `Skenario Kebijakan` | 3 (1 tanpa PS / 2 PS+awal / 3 karbon) | **2** (1 = S1 PS terbatas; 2 = S2 PS + karbon) | Dua skenario kebijakan |
| S-2 | `Switch PS` | `Skenario Kebijakan>=2` | **1** (konstanta Desain; PS aktif di kedua skenario) | S1 bukan tanpa PS |
| S-3 | `Switch Rehabilitasi` | `Skenario Kebijakan>=2` | **1** | idem |
| S-4 | `Switch Pendanaan Awal` | `Skenario Kebijakan>=2` | **1** | Pembiayaan historis 2024–2025 sama di S1 dan S2 |
| S-5 | `Switch Karbon` | `Skenario Kebijakan=3 …` | `IF THEN ELSE(Skenario Kebijakan=2, STEP(1, Tahun Mulai Karbon), 0)`, **hanya** dipakai di `Kredit REDD Diajukan`, `Kredit ARR Diajukan`, `Kredit Gambut Diajukan`, `Biaya Monitoring MRV`, dan `Biaya Verifikasi Tahunan` | Satu-satunya pembeda: penerbitan, penjualan, biaya MRV, dan penerimaan kas karbon |
| S-6 | Jalur tanpa PS | skenario S1 lama | dipertahankan **hanya** sebagai rantai stok `… Baseline` (referensi kredit) dan dilaporkan sebagai "jalur referensi BAU", bukan skenario | Bagian G master prompt |
| S-7 | `Koreksi Kontrafaktual Hutan S1`, `Switch S1` | ada, switch = 0 | dipertahankan non-aktif; komentar diperbarui | Tidak relevan lagi; tidak dihapus agar struktur A1 utuh |

### 2.3 Asumsi baru yang membutuhkan sensitivitas

| No | Parameter | Nilai dasar usulan | Rentang uji | Kelas | Catatan |
|---|---|---|---|---|---|
| P1 | `Tingkat Keberlanjutan Patroli Reguler` | **diputuskan peneliti** (usulan 0,5, lihat 4.1) | 0 / 0,25 / 0,5 / 0,75 / 1,0 (= 0 / 753 / 1.506 / 2.258 / 3.011 HOK pada 254 anggota) | D | Sama untuk S1 dan S2 |
| P2 | `Proporsi Penggantian Dasar` (patroli, KUPS) | 1 (dikali rasio kapasitas) | 0,5 / 1 | D | Mekanisme menurunnya anggota |
| P3 | `Dana Operasional Non Karbon Tunai` | 0 | 0 / nilai dari data peneliti | D | Tanpa data, tetap 0 |
| P4 | `Porsi Penanaman Non Karbon Berupah` | 0 | 0 / 1 | D | Menentukan apakah upah rehabilitasi S1 masuk pendapatan RT |
| P5 | `Laju Pembelajaran` dan `Nilai Pendampingan Kelembagaan Non Tunai` | 0 / 0 | 0–0,2 / data | D | Kapasitas LPHD non-karbon |
| P6 | `Delay Verifikasi dan Penerbitan Kredit` | 3 th (A) | 3 / 4 / 5 (kas pertama ±2027 / 2028 / 2029) | A/D | Bagian H |
| P7 | `Delay Pembayaran Penjualan` (baru) | 0 | 0 / 0,5 / 1 th | D | Jeda penjualan ke kas |
| P8 | `Status Pembiayaan Awal` (baru) | 0 = hibah | 0 hibah / 1 talangan dari bagian mitra | D | NPV mitra dan proyek |
| P9 | `Keikutsertaan Patroli 2023` (inisialisasi) | 2.160 | 1.568 / 2.160 / 0 (tanpa efek awal) | B | K14 |
| P10 | Norma kebutuhan patroli (4 orang/regu, 750 ha/regu, 12 HOK/orang) | tetap | ±50 % | B (tanpa sumber) | Penyebut intensitas |
| P11 | Efektivitas perlindungan 0,37; waktu penyesuaian 3 th | tetap | 0,075–0,59; 1–5 th | D | Sudah masuk Monte Carlo |
| P12 | `Biaya Pengembangan Proyek` (baru, NPV) | 0 | 0 / nilai PDD bila ada | D | NPV tanpa biaya pengembangan cenderung optimistis |

### 2.4 Komponen lama yang tetap dipertahankan

- **Tutupan hutan.** Stok HMS/HRS/HLKS/NonHutan/Perkebunan, laju BAU terkalibrasi, regenerasi, dan neraca 124.941 ha.
- **Rantai baseline kredit.** Stok `… Baseline` dengan `Faktor Tekanan Deforestasi Baseline` = 1, kebocoran 10 %, buffer 12 %, proporsi PA 0,682, dan `DELAY FIXED` penerbitan.
- **Kredit.** Inventori kredit (laju jual 0,7/th, kedaluwarsa 0,1/th), biaya MRV (monitoring, verifikasi, transaksi 0,22 %, pajak 5 %, penerbitan USD 0,25), pemulihan defisit biaya bersama, dan bagi hasil 60/40.
- **Kebakaran dan gambut.** `Proporsi Deforestasi Terkait Kebakaran` = 0 **tidak diubah**, karena laju BAU sudah memuat kehilangan akibat kebakaran. Mengaktifkannya berisiko menghitung ganda. Emisi kebakaran gambut tetap dihitung terpisah.
- **KUPS.** Data dan rantai omzet, surplus, dan penerimaan anggota; tambahan historis 2024–2025.
- **Pendapatan dan akses.** Pendapatan RT (Setiawan dkk. 2021) dan kehilangan akses (asumsi, pengali 0–3,24).
- **Patroli historis.** Data 2.533 dan 3.011 HOK; tim baru 61 dan 10 orang.
- **Eksperimen alokasi B0–B4, R1–R2.** Kompatibel. `Dana Fleksibel LPHD` dihitung dari saldo kas, jadi otomatis mencakup kas non-karbon bila ada. Gerbang `Switch Karbon` pada `Alokasi Dana Kompensasi RT Terdampak` diganti pembatas saldo (sama dengan K4).

---

## 3. Akuntansi karbon, jeda kas, dan keuangan

### 3.1 Baseline referensi kredit (bagian G)

- **Usulan dasar.** Baseline kredit = jalur BAU historis tanpa PS (rantai `… Baseline`, laju kalibrasi 2001/2013–2022 dengan `Indeks Perlindungan Baseline` = 0). Ini paling dekat dengan praktik baseline REDD berbasis laju historis dan tidak memakai S1 sebagai baseline.
- **Konsekuensi metodologis.** Karena S1 sekarang memuat patroli reguler, sebagian kredit S2 berasal dari perlindungan yang juga terjadi di S1. Ini **isu additionality**. Kredit model di atas baseline BAU tidak otomatis memenuhi standar.
- **Sensitivitas konservatif (bekas mesin A2).** `Efek Pengelolaan PS Tanpa Karbon` kini dihitung dari patroli reguler S1 (K1), sehingga `Porsi Mitigasi Adisional terhadap S2` bermakna "mitigasi di atas tingkat S1". Jalankan `Switch Baseline Kredit Konservatif` = 1 sebagai batas bawah kredit.
- **`Faktor Rekonsiliasi Reversal Kredit A2`.** Faktor ini dulu dikalibrasi per harga (0,72–0,76). Diusulkan **ditetapkan 1** dan tidak dikalibrasi ulang.
- **Pelaporan terpisah (F10):**
  1. emisi dihindari dari deforestasi: `Emisi Deforestasi Biomassa` S1 − S2;
  2. serapan rehabilitasi: `Komitmen Serapan Rehabilitasi` dan akumulasi regenerasi;
  3. emisi bersih: `Total Emisi Bersih`;
  4. potensi kredit model: `Kredit Karbon Diajukan`, terhadap baseline;
  5. kredit terbit, terjual, dan kas: `Kredit … Terbit`, `Kredit … Terjual`, `Pendapatan Kotor Penjualan Kredit`.

  Butir 1 adalah selisih kebijakan S2 − S1. Butir 4 adalah selisih terhadap baseline. Keduanya tidak boleh disamakan.

### 3.2 Jeda penerimaan karbon (bagian H)

| Tahap | Struktur di model | Usulan |
|---|---|---|
| Kegiatan dan pengukuran | `Kredit REDD Diajukan` (aliran, sejak `Tahun Mulai Karbon` 2024) | Tetap |
| Verifikasi dan penerbitan | `DELAY FIXED(Diajukan, Delay Verifikasi dan Penerbitan Kredit = 3, 0)` | Tetap. Sensitivitas 3/4/5 th |
| Penjualan | inventori × 0,7/th | Tetap |
| Pembayaran | seketika saat terjual | Baru: `Kas Penjualan Kredit = DELAY FIXED(Pendapatan Kotor Penjualan Kredit, Delay Pembayaran Penjualan, 0)` (default 0) |
| Reinvestasi | `Dana Program PS dari Karbon` → saldo LPHD → alokasi dibatasi saldo | Tetap. Uji: tidak ada belanja karbon sebelum kas pertama |

Catatan B: penerbitan di model bersifat kontinu (aliran tertunda), bukan berkala per peristiwa verifikasi (`Periode Verifikasi` = 5 th hanya memengaruhi biaya). Penerbitan berkala akan membuat kas lebih tersendat. Ini dicatat sebagai keterbatasan, tidak diubah.

### 3.3 Pembiayaan awal dan NPV

- **Pembiayaan awal 2024–2025.** 5.544 HOK × Rp 260.000 = Rp 1.441.440.000. Statusnya **estimasi biaya patroli berbasis parameter**, bukan pengeluaran aktual terverifikasi, dan bukan total investasi proyek.
- **2023 sebagai kondisi awal saja** (K14). Arus kas 2023 tidak dipindahkan ke 2024. Batas evaluasi NPV dimulai 1 Januari 2024.
- **Pembiayaan awal sama di S1 dan S2**, sehingga hilang dalam selisih S2−S1.
- **Usulan tiga ukuran keuangan** (sebelumnya satu NPV proyek yang mengurangkan belanja LPHD):

| Ukuran | Arus kas (diskonto 10 %, dasar 2024) | Keterangan |
|---|---|---|
| NPV inkremental karbon (S2 − S1) | penerimaan kas karbon − biaya MRV/transaksi/pajak/penerbitan − `Biaya Pengembangan Proyek` | Ukuran kelayakan perdagangan karbon. Pembiayaan awal tidak masuk karena sama di kedua skenario |
| NPV mitra | bagian 40 % + pemulihan talangan (bila `Status` = 1) − pembiayaan awal − defisit biaya bersama yang ditanggung | Kelayakan bagi mitra |
| Nilai sekarang dana LPHD dan kecukupannya | PV kas masuk LPHD (karbon + non-karbon) vs PV kebutuhan minimum; kesenjangan tahunan | Kecukupan pembiayaan Hutan Desa, dipisah dari kelayakan proyek |

- **Perubahan definisi NPV.** NPV lama mengurangkan belanja LPHD sebagai biaya proyek. Usulan ini tidak, karena belanja LPHD adalah penggunaan bagian masyarakat. Karena itu harga impas akan berbeda dari angka lama, dan ini akibat perubahan definisi, bukan perbaikan hasil.

---

## 4. Parameter tanpa dasar empiris dan keputusan peneliti

### 4.1 Tingkat patroli reguler pasca-2025 (P1)

Tidak ada data patroli 2026 ke atas. Patroli 2023–2025 seluruhnya didukung mitra, jadi tidak ada bukti patroli tanpa pembiayaan. Usulan saya:
- **nilai dasar 0,5** (±1.506 HOK/th pada 254 anggota), dinyatakan sebagai titik tengah eksploratif (D), bukan fakta;
- hasil **selalu dilaporkan sebagai rentang 0–1**;
- jumlah anggota menurun endogen (K2), jadi 1.506 HOK tidak berulang konstan.

Alternatif bila peneliti lebih memilih: nilai dasar 0,25 (konservatif) atau 0 dengan rentang yang sama. Keputusan ini memengaruhi seluruh S1 dan S2 secara sama, tetapi juga memengaruhi kredit S2 lewat baseline BAU (3.1).

### 4.2 Kas non-karbon (P3)

Usulan default 0. Akibatnya S1 berjalan dengan:
- patroli reguler non-tunai;
- rehabilitasi 20,13 ha/th (pelaksana dan pembayar tidak tercatat);
- KUPS yang menurun perlahan.

Bila peneliti punya data dana desa, APBD, program KLHK/BPDAS, atau mitra untuk 2026 dan seterusnya, nilai itu dimasukkan. Tanpa data, kebutuhan Rp 6,03 miliar/th dilaporkan sebagai kesenjangan.

### 4.3 Rehabilitasi berupah atau sukarela (P4)

Laju 0,0123 × 1.636,8 ha berasal dari realisasi historis (File A). Siapa yang membayar penanaman historis itu belum tercatat. Usulan default 0 (dicatat sebagai non-tunai), dengan uji 1.

### 4.4 Inisialisasi efek perlindungan (P9)

Usulan memakai patroli 2023 (±2.160 keikutsertaan). Estimasi ini berasal dari peneliti (392 kegiatan × 5,51 orang), kelas B.

### 4.5 Baseline kredit (3.1)

Usulan: dasar BAU dengan sensitivitas konservatif. Alternatifnya, baseline konservatif sebagai hasil utama.

### 4.6 Rp 260.000 per HOK

- Di model, satuannya dideklarasikan `Rupiah/HOK` (orang-hari), dengan sumber "Perbup Kotawaringin Barat 29/2020 (cuplikan); File 4 Potensi_VCU kolom AL".
- Dokumen sumbernya tidak ada di paket, jadi **belum dapat saya pastikan apakah nilai itu per orang-hari atau per regu-hari**.
- Bila per regu-hari (±4–5,5 orang), biaya per HOK menjadi ±Rp 47.000–65.000, lebih rendah dari upah Rp 130.000/HOK. Ini tidak konsisten, sehingga tafsiran per orang-hari lebih masuk akal.
- Mohon dikonfirmasi dari dokumen asli.

---

## 5. Uji yang akan dijalankan di Fase 2–3 (setelah disetujui)

1. **Struktur:**
   - neraca luas dan karbon;
   - saldo LPHD ≥ 0;
   - tidak ada belanja karbon sebelum kas pertama;
   - patroli 2024–2025 = 2.533/3.011 di kedua skenario;
   - total patroli ≤ kapasitas;
   - S1 = S2 pada semua variabel non-karbon sampai kas karbon pertama masuk.
2. **Satuan.** Pemeriksaan manual pada persamaan baru. *Units Check* Vensim tetap harus dijalankan peneliti.
3. **Kondisi ekstrem:**
   - harga 0 → S2 = S1;
   - keberlanjutan 0 dan 1;
   - kas non-karbon besar → belanja ≤ kebutuhan;
   - DT 0,03125.
4. **Reproduksi.** Dengan setelan yang meniru model lama, struktur baru harus mereproduksi hasil lama. Ini untuk memisahkan pengaruh perubahan definisi dari koreksi persamaan.
5. **Sensitivitas dan Monte Carlo/PRCC.** P1–P12, ditambah parameter Monte Carlo sebelumnya. Distribusinya dinyatakan eksplisit.
6. **Eksperimen alokasi** pada S2.
7. **Verifikasi Vensim native** tidak dapat dilakukan di lingkungan ini. Skrip pembanding disediakan.

---

## 6. Yang perlu disetujui peneliti sebelum Fase 2

1. Persamaan K1–K15 dan konfigurasi S-1 sampai S-7.
2. Nilai dasar P1 (usulan 0,5; atau 0,25 atau 0) dengan rentang 0–1.
3. P3 kas non-karbon = 0, atau data yang tersedia.
4. P4 rehabilitasi non-karbon: sukarela (0) atau berupah (1).
5. P8 status pembiayaan awal: hibah atau talangan.
6. Baseline kredit: BAU dengan sensitivitas konservatif, atau sebaliknya.
7. Definisi NPV pada 3.3.
8. Konfirmasi satuan Rp 260.000/HOK.
