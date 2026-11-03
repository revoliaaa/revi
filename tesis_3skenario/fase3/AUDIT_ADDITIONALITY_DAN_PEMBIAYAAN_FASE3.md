# Audit Additionality dan Mekanisme Pembiayaan S2 (Fase 3, sebelum Monte Carlo)

**Tanggal:** 3 November 2026

**Status:** eksplorasi. Hasil ini belum menjadi dasar makalah, dan Monte Carlo/PRCC belum dijalankan.

**Perangkat:** PySD 3.14.3. *Units Check* dan run native Vensim belum dilakukan (U0c tertunda).

**Konvensi:**
- NPV berstatus SEMENTARA.
- "Kredit" adalah kredit menurut model, bukan kredit terverifikasi (VCU).
- "M" = miliar rupiah, nominal kecuali NPV.

**Skenario kebijakan tetap dua:**
- S1: Perhutanan Sosial dengan Pembiayaan Terbatas.
- S2: Perhutanan Sosial dengan Perdagangan Karbon.

Mekanisme A, B, dan C adalah eksperimen akuntansi dan pembiayaan **di dalam S2**, bukan skenario kebijakan baru.

---

## 0. Ringkasan

1. **Kredit A melebihi mitigasi tambahan S2 terhadap S1 di semua harga.**
   - Kredit A dihitung terhadap baseline BAU model, yaitu kondisi tanpa Perhutanan Sosial sama sekali.
   - Sekitar 200 ribu tCO₂e kredit A berasal dari perlindungan yang juga terjadi di S1. Angka ini hampir konstan di semua harga.
   - Rasio kredit terhadap mitigasi tambahan eligible S2−S1:

     | Harga | USD 6 | USD 10 | USD 15 | USD 20 | USD 35 |
     |---|---|---|---|---|---|
     | Rasio | ∞ | 14,7 | 3,6 | 2,0 | 1,19 |

   - Pada USD 6, A menerbitkan 197,5 ribu tCO₂e walaupun S2 tidak mengubah apa pun secara fisik dibanding S1.
   - Kelayakan finansial A pada harga rendah–menengah sebagian besar bersumber dari pengkreditan perlindungan tingkat S1. Siklus pendanaannya **disubsidi oleh kredit non-adisional**.
2. **B memang tidak dapat memulai siklus, di semua harga.**
   - Penyebabnya struktural, yaitu aturan atribusinya melingkar:
     - kredit konservatif hanya mengakui mitigasi dari patroli yang dibiayai kas karbon;
     - kas karbon hanya ada bila sudah ada kredit.
   - Biaya MRV **bukan** penyebab: tanpa biaya MRV, kredit tetap 0.
   - Kas non-karbon juga tidak memicu siklus, dan memang tidak seharusnya.
   - Model memiliki dua variabel "pendanaan awal" lama yang **tidak terhubung ke patroli** (temuan T-h). Mengisinya tidak memulai siklus, tetapi justru mencatat utang talangan tanpa kegiatan.
   - Akibat B: mitra menanggung biaya MRV Rp 22,8 M nominal tanpa penerimaan apa pun, dan NPV mitra inkremental −Rp 3,48 M.
3. **C dapat memulai siklus, dengan tiga keterbatasan.**
   - Definisi C: mitra membiayai patroli tambahan 2026–2030 secara eksplisit sebagai talangan, lalu memulihkannya dari surplus kredit.
   - **Pertama: kelayakan finansial baru tercapai di atas ±USD 15–20.**
     - C-J1 (plafon setara pembiayaan mitra 2025, Rp 0,78 M/th) layak bagi mitra hanya pada USD 35. Pada USD 20, NPV mitra inkremental −0,23 M.
     - C-JP (kebutuhan penuh, ±Rp 1,69 M/th) layak bagi mitra mulai USD 20 (+2,49 M).
   - **Kedua: siklus tidak mandiri di bawah ±USD 30.** Sesudah jembatan berakhir, setiap rupiah kredit konservatif hanya membiayai sebagian patroli yang menghasilkannya, sehingga siklus meluruh.
     - Pada USD 20, patroli yang didanai kas LPHD hilang menjelang 2060.
     - Siklus baru bertahan sampai 2087 pada ±USD 30–32,5 (C-JP) atau ±USD 32,5–35 (C-J1).
   - **Ketiga: pendekatan porsi dalam model masih memberi kredit lebih banyak** daripada selisih S2−S1 berpasangan, yaitu 1,16–1,34× pada USD ≤ 20. Karena itu kredit C harus dipotong ex post.
4. **Dampak fisik dan keuangan C dibanding A.**
   - Pada USD 10–20, C-JP menghasilkan **lebih banyak** deforestasi dihindari S2−S1 daripada A: 687 vs 78 ha (USD 10), dan 1.338 vs 1.072 ha (USD 20). Penyebabnya, jembatan membiayai patroli sejak 2026, sedangkan patroli tambahan A baru mulai 2029–2032.
   - Sebaliknya, C menghasilkan kredit dan NPV yang lebih kecil, dan kas LPHD pertama datang lebih lambat (2033–2036 vs 2029–2032).
5. **Rekomendasi (§9).** Gunakan **C** sebagai mekanisme utama interpretasi S2:
   - kredit konservatif terhadap S1 yang dipotong ex post;
   - jembatan eksplisit dengan nilai dasar J1 selama 5 tahun, dipulihkan sebelum bagi hasil, tanpa biaya modal; JP dan biaya modal 10 % sebagai sensitivitas.

   A dilaporkan hanya sebagai batas atas "potensi kredit terhadap baseline BAU model" disertai peringatan additionality. B dilaporkan sebagai temuan diagnostik. Mekanisme ini dipilih karena paling dapat dipertanggungjawabkan, bukan karena memberi kredit atau NPV terbesar. Keputusan akhir ada pada peneliti (§11).

---

## 1. Cakupan, dan apa yang tidak diubah

**Yang tidak diubah:**
- `DKP_25HD_FINAL_2SKENARIO.mdl` (md5 `aa1428df…`) tidak ditimpa.
- Parameter ekologis terkalibrasi tidak diubah.
- Asumsi kerja lain sama dengan Tahap 1: k = 0,5; kas non-karbon 0; pembiayaan mitra historis 2024–2025 sebagai hibah; diskonto 10 %.

**Model varian:** mekanisme C membutuhkan struktur yang belum ada, sehingga dibuat `DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl` (md5 `93af77f807675b636b4472d4fe5d39d2`, 828 variabel). Isinya model dua skenario ditambah:
- **11 variabel baru:** `Switch Pembiayaan Jembatan Karbon`, `Besaran Pembiayaan Jembatan per Tahun`, `Tahun Awal Pembiayaan Jembatan`, `Durasi Pembiayaan Jembatan`, `Switch Henti Jembatan saat Kas Karbon Pertama`, `Kumulatif Kas Masuk LPHD Karbon`, `Periode Pembiayaan Jembatan`, `Hari Patroli Didanai Jembatan`, `Realisasi Pembiayaan Jembatan`, `Kumulatif Pembiayaan Jembatan`, dan `PV Pembiayaan Jembatan`.
- **8 persamaan yang diperluas:** `Hari Patroli Didanai`, `Total HOK Patroli`, `Kebutuhan Dana Perlindungan`, `Pendanaan Awal Belum Terpulihkan`, `Pokok Talangan Kumulatif`, `Arus Kas Proyek Karbon`, `Arus Kas Mitra`, dan `Penggunaan Dana Perlindungan Total`.

Semua tambahan bernilai default nonaktif.

**Verifikasi varian:**

| Pemeriksaan | Hasil |
|---|---|
| Reproduksi model dua skenario (switch nonaktif) | Persis: selisih absolut **0** pada 77 variabel untuk S1 dan S2 × 5 harga |
| Analisis statis | 0 referensi tak dikenal; 0 loop aljabar; pemakai `Switch Karbon` = 9 lama + `Hari Patroli Didanai Jembatan` |
| Pemeriksaan satuan statis | 824 persamaan konsisten, 0 bermasalah |
| `Check Identitas Arus Kas` (semua run) | ≤ 9,5·10⁻⁷ Rp/th |
| `Check Identitas Patroli` (semua run) | 0 |

---

## 2. Audit baseline dan additionality (bagian A)

### 2.1 Jejak pembentukan kredit

| Kredit | Rantai di model | Catatan |
|---|---|---|
| **REDD** | Emisi deforestasi biomassa Baseline − emisi deforestasi biomassa run → `Pengurangan Emisi REDD Bruto` (dibatasi pengurangan emisi biomassa bersih) × (1 − leakage 0,10) × (1 − buffer 0,12) × porsi Project Area 0,682 → `Pengurangan Emisi Eligible REDD` × `Switch Karbon` × `Switch Periode Kredit` (2024–2087) × [A: 1; B/C: `Porsi Mitigasi Adisional terhadap S2`] → `Kredit REDD Diajukan` → DELAY FIXED 3 th → `Terbit` → inventori, laju jual 0,7/th → `Terjual` → `Kas Penjualan Kredit` | Faktor eligible gabungan 0,5401 |
| **ARR** | Sisa pengurangan emisi biomassa di atas REDD (serapan) × (1 − leakage ARR) × (1 − buffer) × [A: 1; B/C: `Porsi ARR Adisional` = porsi penanaman yang dibiayai kas karbon aktual] | Harga removal tetap USD 20. ARR praktis hanya muncul pada USD 35 |
| **Gambut** | `Switch Klaim Kredit Gambut` = 0 | Tidak dikreditkan di semua mekanisme |

`Porsi Mitigasi Adisional terhadap S2` = (Efek Pengelolaan PS Aktif − Efek … Tanpa Karbon) ÷ Efek … Aktif.
- Efek "tanpa karbon" mencakup patroli reguler S1, patroli yang dibiayai mitra 2024–2025, dan patroli dari kas non-karbon.
- Efek "aktif" menambahkan patroli dari kas karbon LPHD dan (di varian) patroli jembatan.

### 2.2 Apa baseline BAU model

Run S1 dengan `Switch PS` = 0 menghasilkan emisi deforestasi kumulatif **10.493.961 tCO₂e, identik dengan rantai Baseline**. Jadi baseline BAU model adalah **kontrafaktual tanpa Perhutanan Sosial sama sekali**, termasuk tanpa sisa respons patroli 2023 dan tanpa patroli mitra 2024–2025.

Baseline ini adalah konstruksi internal model, **bukan**:
- tingkat referensi resmi (FREL nasional/subnasional);
- baseline terjurisdiksi atau baseline yang dialokasikan menurut metodologi standar mana pun;
- S1 kebijakan.

### 2.3 Dua besaran yang harus dipisahkan

Emisi deforestasi dihindari kumulatif 2024–2086 (tCO₂e, bruto sebelum faktor eligible):

| | USD 6 | USD 10 | USD 15 | USD 20 | USD 35 |
|---|---|---|---|---|---|
| S2(A) terhadap BAU | 390.481 | 417.106 | 530.773 | 751.507 | 2.426.891 |
| S1 terhadap BAU (sama untuk semua harga) | 390.481 | 390.481 | 390.481 | 390.481 | 390.481 |
| **S2(A) − S1 (tambahan perdagangan karbon)** | **0** | **26.626** | **140.292** | **361.026** | **2.036.410** |

Hanya baris terakhir yang mengukur mitigasi akibat perdagangan karbon. Dua baris pertama mencampur efek kebijakan PS yang juga terjadi tanpa karbon.

### 2.4 Dekomposisi "S1 terhadap BAU" (390.481 tCO₂e)

Urutan atribusi memengaruhi hasil karena terdapat interaksi:
- pembiayaan mitra 2024–2025 merekrut 61 + 10 anggota (183 → 254);
- patroli reguler S1 memakai roster 254 itu;
- tanpa pembiayaan mitra, anggota tetap 183 dan HOK reguler 1.084,7, bukan 1.505,5.

| Komponen | Urutan 1: warisan mitra lebih dulu | Urutan 2: patroli reguler lebih dulu |
|---|---|---|
| Sisa respons perlindungan 2023 (kondisi awal) | 17.783 | 17.783 |
| Patroli dibiayai mitra 2024–2025, termasuk warisan rekrutmen | 19.939 | 119.441 |
| Patroli reguler S1 pasca-2025 (k = 0,5) | 352.759 | 253.257 |

Untuk A pada USD 20 (751.507 tCO₂e terhadap BAU):
- 52 % adalah perlindungan tingkat S1;
- 48 % adalah tambahan S2.

Pada USD 10, 94 % kredit A berasal dari perlindungan tingkat S1. Rincian di lembar "4 Dekomposisi BAU".

### 2.5 Dapatkah patroli historis yang dibiayai mitra sejak 2023 dihitung sebagai aktivitas proyek?

**Secara konseptual dapat dipertimbangkan, tetapi tidak otomatis memenuhi additionality.**

Agar patroli 2023–2025 dapat masuk sebagai aktivitas proyek, umumnya diperlukan bukti bahwa:
1. tanggal mulai proyek dan kegiatan terdokumentasi;
2. pembiayaan karbon dipertimbangkan sejak awal (*prior consideration*);
3. kegiatan tidak diwajibkan regulasi (*regulatory surplus*);
4. tanpa prospek pendapatan karbon kegiatan itu tidak akan terjadi pada tingkat yang sama (uji investasi/hambatan, atau uji kinerja menurut metodologi).

Persyaratan rinci, batas waktu pendaftaran, dan metode uji bergantung pada standar dan metodologi yang dipilih, dan **BELUM TERVERIFIKASI** terhadap teks standar yang berlaku. Peneliti perlu menetapkan standar acuan sebelum klaim apa pun ditulis.

**Apa yang ditunjukkan model, dan batasnya:**
- **2023.** Model tidak memiliki arus kas 2023. Patroli 2023 (392 kegiatan, ±2.160 keikutsertaan) hanya masuk sebagai kondisi awal respons perlindungan (17.783 tCO₂e). Data sumber menyatakan kegiatan 2023 dibiayai mitra dan bukan swadaya murni.
- **2024–2025.** Data menunjukkan patroli dibiayai mitra (2.533 dan 3.011 HOK; Rp 1.441.440.000). Dalam model, pembiayaan ini juga membentuk roster 254 anggota yang menopang patroli reguler S1 seterusnya. Atribusinya 19.939–119.441 tCO₂e, bergantung urutan. Bila pembiayaan itu memang bagian proyek karbon, sebagian protection S1 adalah warisan proyek, dan S1 tidak dapat begitu saja dianggap baseline kredit.
- **Acuan alternatif** "S1 tanpa pembiayaan mitra 2024–2025" (lembar "5 Integritas kredit") menambah mitigasi eligible terhadap acuan sebesar **64.515 tCO₂e** di semua mekanisme.
- **Batas analisis ini:**
  - Acuan alternatif adalah atribusi ex post. Penerimaan dalam run tidak dihitung ulang.
  - Hubungan rekrutmen 61 + 10 anggota dengan pembiayaan mitra adalah struktur model. Apakah rekrutmen itu terjadi *karena* pembiayaan mitra belum dibuktikan dengan data.
  - Karena itu pilihan ini **tidak** dijadikan mekanisme utama dan hanya dilaporkan sebagai sensitivitas.

### 2.6 S1 kebijakan bukan baseline kredit resmi

S1 dipakai sebagai acuan **atribusi dampak perdagangan karbon** dalam penelitian ini. S1 tidak sama dengan baseline kredit menurut standar mana pun, karena:
1. S1 sendiri sebagian merupakan hasil pembiayaan mitra (§2.5);
2. S1 bergantung pada asumsi kelas D (k = 0,5);
3. baseline standar biasanya ditetapkan dari data historis atau alokasi terjurisdiksi, bukan dari skenario kebijakan model.

Mekanisme B dan C memakai S1 sebagai acuan **konservatif untuk tujuan penelitian**. Itu tidak sama dengan klaim bahwa kredit tersebut dapat diterbitkan.

### 2.7 Pendekatan kredit: asumsi, keterbatasan, dan konsekuensi

| Pendekatan | Asumsi | Keterbatasan | Konsekuensi terhadap penerimaan dan NPV |
|---|---|---|---|
| **A** (terhadap BAU model) | Tanpa proyek, tidak ada PS sama sekali | Mengkreditkan perlindungan yang juga terjadi tanpa karbon (S1). Rasio kredit/mitigasi tambahan 1,19–∞ | Penerimaan tertinggi dan paling awal (kas 2028). NPV positif mulai USD 10–15. Siklus berjalan karena "subsidi" kredit non-adisional, bukan karena mitigasi tambahan |
| **B** (konservatif thd S1, tanpa talangan) | Hanya patroli dari kas karbon yang adisional | Definisi melingkar: tidak dapat dimulai (§5) | Penerimaan 0. Mitra menanggung biaya MRV Rp 22,8 M nominal (NPV −3,48 M), dengan asumsi MRV tetap berjalan walau tanpa kredit |
| **C** (konservatif + jembatan eksplisit) | Patroli tambahan sejak 2026 dibiayai talangan mitra dan dihitung sebagai aktivitas proyek | Kredit model 0,96–1,34× mitigasi berpasangan → perlu potongan ex post. Siklus meluruh di bawah ±USD 30 | Penerimaan dan NPV lebih kecil daripada A, kas LPHD lebih lambat. Risiko ditanggung mitra secara eksplisit (eksposur Rp 4,8–21 M) |
| **Ex post min(kredit, mitigasi thd S1)** | Kredit tidak boleh melebihi mitigasi tambahan berpasangan | Hanya pelaporan, tanpa umpan balik ke kas | Mengoreksi kelebihan kredit C sebesar 18–40 ribu tCO₂e (USD ≤ 20) |
| **Acuan "S1 tanpa pembiayaan mitra 2024–2025"** | Proyek dimulai 2024 | Butuh bukti *prior consideration* dan sebab-akibat rekrutmen | +64,5 ribu tCO₂e eligible; nilai kotor 64.515 × harga × Rp 16.500 = Rp 6,4–37,3 M pada USD 6–35, sebelum porsi terjual dan biaya. Hanya sensitivitas |

---

## 3. Definisi tiga mekanisme pembiayaan (bagian B)

| | A | B | C |
|---|---|---|---|
| Acuan kredit | Baseline BAU model | S1 (porsi mitigasi dari kas karbon) | S1 (porsi mitigasi dari kas karbon + jembatan) |
| Pembiayaan sebelum kredit pertama | Hanya pembiayaan historis 2024–2025 (hibah) | Sama dengan A | Sama dengan A, ditambah jembatan |
| `Switch Baseline Kredit Konservatif` | 0 | 1 | 1 |
| `Switch Pembiayaan Jembatan Karbon` | 0 | 0 | 1 |

### Spesifikasi jembatan pada C

Tidak ada kas yang diciptakan: setiap rupiah jembatan adalah arus keluar mitra dan dicatat di `Arus Kas Mitra` serta `Arus Kas Proyek Karbon`.

| Unsur | Isi |
|---|---|
| **Sumber** | Mitra pengembang proyek, yaitu pihak yang membiayai patroli 2024–2025. Sifatnya talangan, bukan hibah |
| **Waktu** | Mulai 2026, sesudah pembiayaan historis berakhir. Dasar 5 tahun (2026–2030); uji 3 dan 8 tahun. Varian "henti saat kas LPHD karbon pertama" hasilnya praktis sama, karena kas LPHD pertama datang sesudah jembatan berakhir |
| **Jumlah** | **J1** = Rp 782.860.000/th (3.011 HOK × Rp 260.000, setara tingkat pembiayaan mitra 2025, satu-satunya jangkar data). **JP** = kebutuhan patroli tambahan penuh (6.490,7 HOK/th × Rp 260.000 ≈ Rp 1,69 M/th; dibatasi kapasitas anggota). Komitmen nyata mitra: **[PERLU DIISI]** |
| **Penggunaan** | Hanya patroli **di atas** patroli reguler S1 (`Hari Patroli Tambahan Dibutuhkan`). Bagian kebutuhan yang dibiayai jembatan tidak dibebankan ke LPHD |
| **Biaya modal** | 0 % (dasar) dan 10 %/th (uji) atas saldo belum pulih |
| **Pemulihan** | Dari surplus kredit sesudah biaya MRV/transaksi/pajak dan sesudah pemulihan defisit MRV yang ditalangi mitra, **sebelum** bagi hasil 60/40. Tanpa penghapusan; sisa 2087 dilaporkan sebagai kerugian mitra |
| **Bukan** | Bukan aturan kontraktual yang disetujui. Bukan klaim bahwa mitra bersedia |

Urutan pemulihan memberi mitra prioritas penuh. Akibatnya LPHD baru menerima kas sesudah defisit MRV dan talangan lunas. Pembagian pemulihan secara proporsional belum diuji.

---

## 4. Hasil (bagian C)

Varian dasar C: jembatan 5 tahun, tanpa henti dini, biaya modal 0. Kisi lengkap (2 plafon × 3 durasi × 2 aturan henti × 2 biaya modal × 5 harga = 120 run) ada di lembar "2 Kisi mekanisme C".

Satuan tabel 4.1: Rp M = miliar rupiah, nominal; tahun = waktu simulasi pertama dengan desimal (langkah DT).

### 4.1 Rantai kredit dan kas

| Harga | Mek. | Kredit diajukan (ribu tCO₂e) | Terbit | Terjual | Kas diterima (Rp M) | Biaya MRV dll. (Rp M) | Kas LPHD (Rp M) | Dana mitra 40 % (Rp M) | Kredit diajukan pertama | Kas penjualan pertama | Kas LPHD pertama |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | A | 197,5 | 192,0 | 165,9 | 16,43 | 24,42 | 0,00 | 0,00 | 2025,00 | 2028,06 | – |
| 6 | B | 0,0 | 0,0 | 0,0 | 0,00 | 22,77 | 0,00 | 0,00 | – | – | – |
| 6 | C-J1 | 71,0 | 71,0 | 62,1 | 6,15 | 23,39 | 0,00 | 0,00 | 2026,06 | 2029,12 | – |
| 6 | C-JP | 152,8 | 152,8 | 133,7 | 13,24 | 24,09 | 0,00 | 0,00 | 2026,06 | 2029,12 | – |
| 10 | A | 211,9 | 206,8 | 179,0 | 29,53 | 25,17 | 3,56 | 2,37 | 2025,00 | 2028,06 | 2031,88 |
| 10 | B | 0,0 | 0,0 | 0,0 | 0,00 | 22,77 | 0,00 | 0,00 | – | – | – |
| 10 | C-J1 | 71,0 | 71,0 | 62,1 | 10,25 | 23,60 | 0,00 | 0,00 | 2026,06 | 2029,12 | – |
| 10 | C-JP | 164,9 | 164,9 | 144,3 | 23,81 | 24,70 | 3,06 | 2,04 | 2026,06 | 2029,12 | 2035,75 |
| 15 | A | 274,1 | 269,1 | 233,4 | 57,75 | 26,90 | 18,52 | 12,34 | 2025,00 | 2028,06 | 2030,38 |
| 15 | B | 0,0 | 0,0 | 0,0 | 0,00 | 22,77 | 0,00 | 0,00 | – | – | – |
| 15 | C-J1 | 81,2 | 81,2 | 71,0 | 17,58 | 24,02 | 2,36 | 1,57 | 2026,06 | 2029,12 | 2035,19 |
| 15 | C-JP | 208,0 | 208,0 | 182,0 | 45,04 | 25,98 | 13,18 | 8,79 | 2026,06 | 2029,12 | 2034,12 |
| 20 | A | 395,5 | 386,6 | 334,5 | 110,38 | 30,13 | 48,15 | 32,10 | 2025,00 | 2028,06 | 2029,81 |
| 20 | B | 0,0 | 0,0 | 0,0 | 0,00 | 22,77 | 0,00 | 0,00 | – | – | – |
| 20 | C-J1 | 104,2 | 104,2 | 91,1 | 30,08 | 24,77 | 7,67 | 5,12 | 2026,06 | 2029,12 | 2034,12 |
| 20 | C-JP | 287,1 | 287,1 | 251,3 | 82,91 | 28,28 | 32,40 | 21,60 | 2026,06 | 2029,12 | 2033,38 |
| 35 | A | 1.343,4 | 1.270,2 | 1.084,1 | 619,83 | 60,37 | 335,68 | 223,79 | 2025,00 | 2028,06 | 2029,19 |
| 35 | B | 0,0 | 0,0 | 0,0 | 0,00 | 22,77 | 0,00 | 0,00 | – | – | – |
| 35 | C-J1 | 698,5 | 660,4 | 563,3 | 325,33 | 42,48 | 167,36 | 111,58 | 2026,06 | 2029,12 | 2032,75 |
| 35 | C-JP | 1.348,0 | 1.291,0 | 1.108,1 | 638,38 | 61,42 | 341,11 | 227,41 | 2026,06 | 2029,12 | 2032,31 |


Catatan tabel 4.1:
- "Terjual" < "terbit" karena laju penjualan 0,7/th dari inventori.
- Pada C, kredit pertama diajukan 2026, sesudah respons patroli jembatan melewati penyesuaian SMOOTHI 3 tahun.
- **Kas LPHD pertama selalu lebih lambat daripada kas penjualan**, karena surplus lebih dulu memulihkan defisit MRV yang ditalangi mitra dan (pada C) talangan jembatan.

### 4.2 Dampak fisik, pembiayaan, dan NPV

Satuan: Rp M = miliar rupiah. NPV berstatus [SEMENTARA], diskonto 10 %.

| Harga | Mek. | Deforestasi dihindari S2−S1 (ha) | Emisi dihindari S2−S1 (ribu tCO₂e) | Emisi dihindari thd BAU (ribu tCO₂e) | Talangan/jembatan (Rp M) | Sisa talangan 2087 (Rp M) | Defisit MRV 2087 (Rp M) | Eksposur mitra maks. (Rp M) | NPV proyek (Rp M) | NPV mitra inkremental (Rp M) | Cakupan LPHD (%) | Δ FTE berupah |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | A | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 7,99 | 7,99 | -2,37 | -1,06 | 0,0 | 0,0 |
| 6 | B | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 22,77 | 22,77 | -4,79 | -3,48 | 0,0 | 0,0 |
| 6 | C-J1 | 287 | 97,9 | 488,3 | 3,91 | 3,91 | 17,24 | 21,15 | -5,44 | -4,13 | 0,0 | 0,4 |
| 6 | C-JP | 620 | 211,6 | 602,1 | 8,44 | 3,00 | 16,30 | 19,29 | -6,18 | -4,87 | 0,0 | 0,8 |
| 10 | A | 78 | 26,6 | 417,1 | 0,00 | 0,00 | 1,56 | 1,16 | -0,44 | 0,16 | 2,1 | 0,9 |
| 10 | B | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 22,77 | 22,77 | -4,79 | -3,48 | 0,0 | 0,0 |
| 10 | C-J1 | 287 | 97,9 | 488,3 | 3,91 | 0,79 | 16,47 | 17,27 | -4,08 | -2,77 | 0,0 | 0,4 |
| 10 | C-JP | 687 | 234,5 | 625,0 | 8,44 | 0,00 | 14,42 | 12,38 | -3,02 | -2,56 | 2,1 | 1,8 |
| 15 | A | 415 | 140,3 | 530,8 | 0,00 | 0,00 | 0,00 | 1,11 | 2,66 | 1,44 | 7,5 | 3,3 |
| 15 | B | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 22,77 | 22,77 | -4,79 | -3,48 | 0,0 | 0,0 |
| 15 | C-J1 | 338 | 115,4 | 505,8 | 3,91 | 0,00 | 14,29 | 12,72 | -2,10 | -1,47 | 1,6 | 1,1 |
| 15 | C-JP | 909 | 310,6 | 701,1 | 8,44 | 0,00 | 11,35 | 9,29 | 1,88 | -0,24 | 9,1 | 4,8 |
| 20 | A | 1.072 | 361,0 | 751,5 | 0,00 | 0,00 | 0,00 | 1,09 | 6,72 | 3,08 | 15,2 | 6,8 |
| 20 | B | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 22,77 | 22,77 | -4,79 | -3,48 | 0,0 | 0,0 |
| 20 | C-J1 | 454 | 155,1 | 545,5 | 3,91 | 0,00 | 11,40 | 6,28 | 0,45 | -0,23 | 5,3 | 2,7 |
| 20 | C-JP | 1.338 | 457,4 | 847,9 | 8,44 | 0,00 | 7,81 | 8,85 | 8,21 | 2,49 | 21,1 | 10,0 |
| 35 | A | 6.045 | 2.036,4 | 2.426,9 | 0,00 | 0,00 | 0,00 | 1,07 | 29,37 | 12,16 | 62,3 | 27,6 |
| 35 | B | 0 | 0,0 | 390,5 | 0,00 | 0,00 | 22,77 | 22,77 | -4,79 | -3,48 | 0,0 | 0,0 |
| 35 | C-J1 | 4.002 | 1.345,3 | 1.735,8 | 3,91 | 0,00 | 0,00 | 4,82 | 15,67 | 6,10 | 36,0 | 16,4 |
| 35 | C-JP | 7.478 | 2.533,8 | 2.924,3 | 8,44 | 0,00 | 0,00 | 8,18 | 41,90 | 16,20 | 94,4 | 41,1 |

Catatan tabel 4.2:
- **Acuan.** S2−S1 dihitung terhadap S1 yang sama (k = 0,5). "Emisi dihindari thd BAU" mencakup 390,5 ribu tCO₂e perlindungan tingkat S1.
- **NPV proyek S1** = −1,31 M (pembiayaan historis 2024–2025). "NPV mitra inkremental" = NPV mitra S2 − NPV mitra S1.
- **Eksposur mitra maks.** = titik terendah kumulatif arus kas mitra (S2 − S1, tak terdiskonto), termasuk biaya MRV yang ditalangi.
- **Biaya MRV pada B.** Mitra menanggung biaya MRV penuh (Rp 22,8 M) karena model menjalankan MRV sepanjang periode kredit walaupun kredit 0 (T-j).
- **ARR** hanya muncul pada USD 35: A 33,3 ribu; C-JP 7,1 ribu tCO₂e. Kredit gambut 0 di semua run.

### 4.3 Waktu kas positif pertama

| Mekanisme | Kas penjualan pertama | Arus kas mitra positif pertama | Kas LPHD karbon pertama |
|---|---|---|---|
| A | 2028,06 (semua harga) | 2028–2029 | USD 10: 2031,88 · USD 15: 2030,38 · USD 20: 2029,81 · USD 35: 2029,19 · USD 6: tidak pernah |
| B | tidak pernah | tidak pernah | tidak pernah |
| C-J1 | 2029,12 | 2030–2031 | USD 15: 2035,19 · USD 20: 2034,12 · USD 35: 2032,75 · USD 6–10: tidak pernah |
| C-JP | 2029,12 | 2030–2031 | USD 10: 2035,75 · USD 15: 2034,12 · USD 20: 2033,38 · USD 35: 2032,31 · USD 6: tidak pernah |

### 4.4 Integritas kredit: kredit model vs mitigasi tambahan terhadap S1

Mitigasi eligible = emisi deforestasi dihindari S2−S1 × 0,5401 (ex post, lembar "5 Integritas kredit").

| Harga | A: kredit / mitigasi | Rasio A | C-J1: kredit / mitigasi | Rasio C-J1 | C-JP: kredit / mitigasi | Rasio C-JP |
|---|---|---|---|---|---|---|
| USD 6 | 197,5 / 0 | ∞ | 71,0 / 52,9 | 1,34 | 152,8 / 114,3 | 1,34 |
| USD 10 | 211,9 / 14,4 | 14,7 | 71,0 / 52,9 | 1,34 | 164,9 / 126,7 | 1,30 |
| USD 15 | 274,1 / 75,8 | 3,6 | 81,2 / 62,3 | 1,30 | 208,0 / 167,8 | 1,24 |
| USD 20 | 395,5 / 195,0 | 2,0 | 104,2 / 83,8 | 1,24 | 287,1 / 247,1 | 1,16 |
| USD 35 | 1.310,1 / 1.100,0 | 1,19 | 698,5 / 726,7 | 0,96 | 1.340,8 / 1.368,6 | 0,98 |

Satuan: ribu tCO₂e kredit REDD diajukan / mitigasi eligible.

**Bacaan:**
- Kelebihan kredit A hampir konstan, sekitar 197–210 ribu tCO₂e, setara mitigasi eligible S1 terhadap BAU (210,9 ribu). Kelebihan itu adalah kredit atas perlindungan tingkat S1.
- Kelebihan pada C (18–40 ribu tCO₂e) berasal dari pendekatan porsi di dalam run (T-i).

---

## 5. Mengapa B tidak dapat memulai siklus

### 5.1 Penyebab

1. **Lingkaran atribusi (penyebab utama).**
   - `Porsi Mitigasi Adisional terhadap S2` hanya > 0 bila ada patroli yang dibiayai kas karbon LPHD.
   - Kas karbon LPHD hanya ada bila sudah ada kredit terjual.
   - Pembiayaan historis 2024–2025 sengaja dimasukkan ke efek "tanpa karbon", karena juga terjadi di S1.
   - Akibatnya, tanpa sumber dana di luar kredit, porsi itu tetap 0 sepanjang horizon.
   - Ini adalah sifat definisi, bukan galat persamaan. Varian ini menjawab "kredit apa yang muncul bila hanya kas karbon yang dianggap adisional", dan jawabannya: tidak ada.
2. **Biaya MRV bukan penyebab.** Uji B tanpa biaya MRV memberi kredit 0, kas 0, dan dampak 0.
3. **Kas non-karbon tidak memicu siklus**, dan memang tidak seharusnya. Uji B + kas non-karbon Rp 3 M/th: deforestasi turun 2.381 ha, sama persis dengan S1 + kas yang sama, dan kredit 0. Patroli dari dana non-karbon terjadi juga tanpa proyek karbon.
4. **Struktur "pendanaan awal" lama tidak terhubung (T-h).**
   - `Pendanaan Awal untuk Patroli` hanya mengalir ke stok talangan dan `Total Pembiayaan Tambahan S3`. `Hari Patroli Direncanakan` yang memakainya tidak dipakai variabel lain.
   - Uji Rp 1 M/th sebagai talangan: patroli 0, kredit 0, tetapi pokok talangan tercatat Rp 64,4 M (utang tanpa kegiatan).
   - `Besaran Pendanaan Awal Proyek Karbon` → `Pendanaan Awal Proyek Karbon` tidak dipakai persamaan mana pun.
   - Keduanya bernilai 0 secara default, sehingga hasil Tahap 1 tidak terdampak. Variabel jembatan C menggantikan fungsi yang semestinya.

### 5.2 Uji pemicu

| Run (USD 20) | Kredit (ribu tCO₂e) | Deforestasi dihindari S2−S1 (ha) | Kas LPHD (Rp M) | Defisit MRV 2087 (Rp M) | Bacaan |
|---|---|---|---|---|---|
| Jembatan 1 tahun (2026), kebutuhan penuh | 35,4 | 142 | 0,85 | 16,3 | Siklus menyala lalu padam |
| Jembatan 1 tahun, tanpa biaya MRV | 77,5 | 377 | 11,5 | 0 | Tanpa beban MRV, siklus kecil bertahan |
| Jembatan penuh 2026–2087 | 1.408,7 | 8.038 | 140,2 | 0 | Batas atas, bukan mekanisme realistis |

**Kesimpulan:** B memang tidak dapat memulai siklus, dan penyebabnya bukan biaya MRV.
- **Penyebab utama** adalah lingkaran atribusi (§5.1, butir 1).
- **Penyebab kedua** baru bekerja sesudah siklus menyala: biaya MRV tetap sekitar Rp 0,37 M/th, yang harus ditutup lebih dulu dari surplus kredit konservatif yang kecil.
- **Penyebab ketiga** adalah tingkat bagi hasil dan alokasi:
  - hanya 60 % surplus masuk LPHD;
  - LPHD membagi dananya ke beberapa pos;
  - sehingga kas yang kembali ke patroli lebih kecil daripada nilai kredit yang dihasilkan patroli itu (§6).

---

## 6. Dinamika C dan ambang harga siklus mandiri

Lembar "6b Ambang siklus mandiri" dan G11–G12. Patroli yang didanai kas LPHD sesudah jembatan 2026–2030 berakhir:

| Harga | C-JP: 2045 / 2060 / 2080 (HOK/th) | C-J1: 2045 / 2060 / 2080 |
|---|---|---|
| USD 20 | 1.522 / 213 / 0 | 363 / 0 / 0 |
| USD 25 | 2.939 / 1.689 / 6 | 903 / 168 / 0 |
| USD 30 | 4.896 / 5.477 / 3.829 | 1.663 / 1.251 / 54 |
| USD 32,5 | 6.023 / 6.491 / 6.220 | 2.141 / 2.264 / 1.212 |
| USD 35 | 6.491 / 6.491 / 6.491 (penuh) | 2.694 / 3.765 / 4.363 |

**Bacaan:**
- Di bawah ±USD 30, siklus konservatif meluruh. Setiap putaran (patroli → kredit → kas → patroli) menghasilkan patroli lebih sedikit daripada putaran sebelumnya.
- Jembatan hanya menunda peluruhan. Sesudah kas habis, biaya MRV yang tetap berjalan membentuk defisit baru yang ditanggung mitra: Rp 7,8–11,4 M pada 2087 di USD 20.
- A tidak meluruh pada USD 20 karena aliran kredit dari perlindungan tingkat S1 (±200 ribu tCO₂e) menopang kas terlepas dari patroli tambahan.

Ambang ini bergantung pada asumsi kelas D:
- biaya MRV;
- porsi bagi hasil 60/40;
- proporsi alokasi LPHD untuk perlindungan;
- biaya Rp 260.000/HOK;
- efektivitas 0,37;
- k = 0,5.

Ambang ini **bukan harga impas yang tervalidasi**.

---

## 7. Kelayakan mekanisme

Kriteria ditetapkan eksplisit. Semuanya adalah kelayakan **menurut model**.

| Kriteria | Isi |
|---|---|
| Integritas | Kredit ≤ mitigasi eligible berpasangan terhadap S1 |
| Mitra | NPV mitra inkremental ≥ 0 dan talangan pulih penuh |
| Keberlanjutan | Defisit MRV 2087 = 0 |
| Manfaat | LPHD menerima kas; deforestasi dihindari S2−S1 > 0 |

| Harga | A | B | C-J1 | C-JP |
|---|---|---|---|---|
| USD 6 | Integritas gagal (kredit tanpa mitigasi tambahan); mitra rugi | Tidak berjalan | Mitra rugi; talangan tak pulih | Mitra rugi; talangan tak pulih (Rp 3,0 M) |
| USD 10 | Integritas gagal (14,7×); mitra +0,16 M; LPHD 2,1 % | Tidak berjalan | Mitra rugi; talangan sisa 0,79 M | Mitra rugi (−2,56 M); talangan pulih |
| USD 15 | Integritas gagal (3,6×); mitra +1,44 M | Tidak berjalan | Mitra rugi (−1,47 M) | Mitra ≈ impas (−0,24 M); meluruh |
| USD 20 | Integritas gagal (2,0×); mitra +3,08 M; LPHD 15,2 % | Tidak berjalan | Mitra ≈ impas (−0,23 M); meluruh | **Mitra +2,49 M**; LPHD 21,1 %; meluruh sesudah ±2050 |
| USD 35 | Integritas mendekati (1,19×); mitra +12,2 M | Tidak berjalan | **Layak penuh** (+6,10 M; bertahan) | **Layak penuh** (+16,2 M; LPHD 94 %; bertahan) |

**Sensitivitas pembiayaan C** (lembar 2):
- **Biaya modal 10 % menggeser kas dari LPHD ke mitra.** Contoh C-J1 USD 20: NPV mitra naik dari −0,23 menjadi +0,13 M, tetapi cakupan LPHD turun dari 5,3 % menjadi 2,9 % dan deforestasi dihindari dari 454 menjadi 380 ha.
- **Bila harga terlalu rendah untuk memulihkan pokok, bunga menumpuk tanpa batas:** sisa talangan 2087 Rp 1.344 M pada USD 6, Rp 824 M pada USD 10 (C-J1). Ini akrual non-tunai dan tidak masuk NPV, tetapi menunjukkan bahwa model memerlukan aturan penghapusan. Temuan T-a sebelumnya ternyata juga berlaku untuk pemulihan **sebelum** bagi hasil.
- **Durasi 8 tahun** memperbaiki hasil pada USD 15–20 (C-JP USD 20: +4,57 M; 2.374 ha), dengan talangan Rp 13,5 M.

---

## 8. Risiko additionality dan keterbatasan data

1. **Baseline.** BAU model adalah kontrafaktual tanpa PS, bukan FREL atau baseline metodologi. Semua angka kredit adalah potensi menurut model.
2. **k = 0,5 (kelas D) menentukan besar bagian S1 dalam kredit A** dan menentukan acuan B/C. Pada k = 0 (dibandingkan dengan S1 pada k = 0), kredit A USD 20 hanya 35,5 ribu tCO₂e untuk 38 ha deforestasi dihindari dan 13,1 ribu tCO₂e emisi dihindari (eligible ±7,1 ribu), sehingga rasio kredit/mitigasi ±5. Additionality A sangat peka terhadap k yang tidak memiliki data.
3. **Status pembiayaan mitra 2023–2025 sebagai aktivitas proyek belum dapat diputuskan** tanpa dokumen proyek (tanggal mulai, *prior consideration*, kontrak). [PERLU DIISI]
4. **Hubungan rekrutmen 183 → 254 anggota dengan pembiayaan mitra** adalah asumsi struktur model.
5. **Kredit konservatif dihitung dengan pendekatan porsi di dalam run.** Pendekatan ini tidak sama dengan selisih berpasangan dan memberi kelebihan hingga 1,34×, sehingga diperlukan potongan ex post.
6. **Biaya MRV** (Rp 1.980/ha/th untuk 111.123 ha; verifikasi Rp 742,5 juta per 5 tahun) dan biaya pengembangan proyek (0) belum berdasar data proyek. NPV tetap SEMENTARA.
7. **Komitmen jembatan mitra** (besaran, durasi, biaya modal, prioritas pemulihan) tidak ada datanya. J1 hanya meniru tingkat 2025.
8. **MRV tetap berjalan walaupun tidak ada kredit** (B; C sesudah peluruhan). Ini memperbesar kerugian mitra. Proyek nyata kemungkinan menghentikan MRV, tetapi aturan penghentian belum dimodelkan.
9. **Penerbitan kontinu, bukan per verifikasi; harga ARR tetap USD 20; gambut tidak dikreditkan.**
10. **Vensim native belum dijalankan.** Semua angka berstatus "terverifikasi PySD".

---

## 9. Rekomendasi mekanisme untuk tujuan penelitian pembangunan perdesaan

**Rekomendasi: C sebagai mekanisme utama interpretasi S2, dengan ketentuan berikut.**

| Unsur | Nilai dasar | Sensitivitas |
|---|---|---|
| Kredit | Konservatif terhadap S1, dilaporkan **ex post sebagai min(kredit model, mitigasi eligible berpasangan terhadap S1)** | – |
| Jembatan | J1 (Rp 0,78 M/th; jangkar data 2025), 2026–2030 | JP; 3 dan 8 tahun |
| Pemulihan | Sebelum bagi hasil, biaya modal 0 | Biaya modal 10 %, dengan catatan akrual tanpa batas |
| Harga | Dilaporkan per harga dengan ambang siklus mandiri (§6) | – |

**Alasan pilihan**, yang tidak didasarkan pada besar kredit atau NPV:
1. **Atribusi jujur.** Kredit hanya mencerminkan mitigasi yang tidak terjadi di S1. A mengkreditkan perlindungan yang juga terjadi tanpa karbon, sehingga mencampur dampak PS dengan dampak perdagangan karbon. Itulah perbedaan yang ingin diukur penelitian ini.
2. **Pembiayaan eksplisit.** C memperlihatkan siapa membiayai apa, kapan, dan siapa menanggung risiko:
   - eksposur mitra Rp 6,3–8,9 M pada USD 20;
   - LPHD baru menerima kas 2033–2034;
   - talangan dapat tidak pulih pada harga rendah.

   Informasi ini relevan bagi kelembagaan desa (LPHD, KUPS), sedangkan di A informasi itu tersembunyi di balik kredit non-adisional.
3. **Menjawab pertanyaan pembangunan perdesaan.** Pertanyaannya bukan "berapa kredit maksimum", tetapi "dengan syarat apa perdagangan karbon menambah perlindungan, kerja, dan kas desa di atas yang sudah terjadi". C memberi jawabannya: harga ±USD 20 dengan pembiayaan awal penuh untuk tambahan yang tidak permanen, dan ±USD 30–35 untuk siklus yang mandiri.
4. **B dan A tetap dilaporkan.**
   - **B** sebagai temuan: kredit konservatif tanpa pembiayaan awal tidak pernah menghasilkan kas. Kebutuhan modal awal adalah syarat kelembagaan, bukan detail teknis.
   - **A** sebagai batas atas berlabel "potensi kredit terhadap baseline BAU model, tidak lolos uji additionality model".

**Konsekuensi bagi tahap berikutnya** bila rekomendasi diterima:
- Monte Carlo/PRCC dijalankan pada varian `…_MEKANISME.mdl` dengan C sebagai konfigurasi dasar, ditambah parameter besaran dan durasi jembatan, biaya modal, dan harga.
- Indikator kredit dilaporkan ex post.
- Benefit sharing (B0–B4, R1, R2) diuji di atas C.
- Angka Tahap 1 (yang memakai A) tidak dipakai sebagai hasil utama S2.

---

## 10. Temuan baru untuk register

| Kode | Temuan | Dampak | Usul |
|---|---|---|---|
| T-h | `Pendanaan Awal untuk Patroli` mengalir ke stok talangan dan `Total Pembiayaan Tambahan S3`, tetapi tidak ke patroli (`Hari Patroli Direncanakan` tidak dipakai). `Besaran Pendanaan Awal Proyek Karbon` tidak dipakai persamaan mana pun | Default 0, jadi hasil tidak terdampak. Bila diisi, model mencatat utang tanpa kegiatan (uji: talangan Rp 64,4 M, patroli 0) | Hapus atau ganti dengan struktur jembatan (M1) pada versi akhir |
| T-a (diperluas) | Biaya modal > 0 menumpuk tanpa batas bila surplus tidak cukup, **juga** pada pemulihan sebelum bagi hasil | Akrual non-tunai sangat besar pada USD ≤ 10 | Tambahkan batas penghapusan atau tenor sebelum biaya modal dipakai |
| T-i | Atribusi porsi dalam run memberi kredit 0,96–1,34× mitigasi berpasangan | Kredit B/C sedikit berlebih | Laporkan ex post min(…); jangan pakai kredit run langsung |
| T-j | MRV tetap berjalan tanpa kredit | Kerugian mitra B/C diperbesar | Aturan penghentian MRV (keputusan peneliti) |

---

## 11. Keputusan yang diminta sebelum Monte Carlo dan PRCC final

1. **Mekanisme utama S2:** C (rekomendasi), A, atau lainnya.
2. **Bila C:**
   - plafon jembatan dasar: J1 (tingkat 2025) atau JP (kebutuhan penuh), atau angka komitmen mitra bila ada;
   - durasi;
   - biaya modal;
   - prioritas pemulihan: penuh sebelum LPHD (sekarang) atau proporsional (belum diuji);
   - perlu tidaknya aturan penghapusan.
3. **Status pembiayaan mitra 2023–2025:** aktivitas proyek atau bukan. Bila ya, dokumen *prior consideration* dan tanggal mulai diperlukan; sampai itu tersedia, hanya sensitivitas (+64,5 ribu tCO₂e).
4. **Aturan MRV** bila kredit tidak ada atau berhenti.
5. **Status variabel lama** `Pendanaan Awal untuk Patroli` dan `Besaran Pendanaan Awal Proyek Karbon` (T-h).

Monte Carlo, PRCC, benefit sharing, dan revisi makalah **belum dijalankan** dan menunggu keputusan ini.

---

## 12. Berkas

| Berkas | Isi |
|---|---|
| `fase3/AUDIT_ADDITIONALITY_DAN_PEMBIAYAAN_FASE3.md` | Dokumen ini |
| `fase3/TABEL_PERBANDINGAN_MEKANISME_KREDIT_PEMBIAYAAN.xlsx` | 0 README; 1 Ringkasan A-B-C (semua indikator × 5 harga); 2 Kisi mekanisme C (120 run); 3 Diagnostik B; 4 Dekomposisi BAU; 5 Integritas kredit; 6 Kelayakan; 6b Ambang siklus mandiri; 7 Uji reproduksi varian; 8 Daftar run (171) |
| `fase3/GRAFIK_HASIL_FINAL/G10–G12` | Kredit vs mitigasi; dinamika USD 20/35; ambang harga |
| `model/DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl` | Varian dengan struktur jembatan (default nonaktif) |
| `skrip/fase3b/` | `build_mek.py`, `mek.py`, `diag2.py`, `ambang.py`, `olah.py`, `setara.py`, `xlsx_mek.py`, `grafik_mek.py`, `tabel_md.py`, hasil JSON |
