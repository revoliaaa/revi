# Audit Konseptual dan Struktural S2: Model FINAL 3 Skenario

**Objek audit:** `DKP_25HD_FINAL_3SKENARIO.mdl` (md5 `5af5a34ea1328310b719f8eeacad2ae6`), skenario S2 (`Skenario Kebijakan` = 2).

**Cara audit:**
- **Persamaan dan sumber.** Persamaan dibaca dari berkas model. Sumber dan kelas parameter diambil dari `REGISTER_VARIABEL_PER_VIEW_A1.xlsx`.
- **Nilai 2030, 2050, dan 2087.** Diambil dari keluaran S2 yang sudah tersimpan di `REGISTER_HASIL_SIMULASI_3SKENARIO.xlsx` (lembar 6–10).
- **Nilai 2024, 2025, dan 2026.** Tersedia untuk 19 variabel kunci di seri tahunan. Untuk variabel lain, nilai diturunkan langsung dari persamaan (konstanta dan fungsi waktu) atau diambil dari keluaran run yang sama yang sudah tercatat sebelumnya. Bila tidak tersedia, ditulis "tt" (tidak tersimpan).
- **Tidak ada persamaan yang diubah dan tidak ada simulasi baru.**

**Konvensi nilai:** stok = nilai awal tahun; aliran/auxiliary = rerata dalam tahun. Kolom 2087 untuk aliran = nilai pada FINAL TIME.

**Kelas temuan:** A = kesalahan terkonfirmasi; B = asumsi lemah atau belum didukung data; C = konsisten; D = belum dapat dipastikan.

---

## 0. Jawaban atas pertanyaan khusus

**Apakah model keliru menyamakan berakhirnya pembiayaan proyek dengan berakhirnya seluruh kegiatan PS? Ya, untuk patroli dan perlindungan. Ini kesalahan terkonfirmasi (A), dan sebagian besar berasal dari revisi saya sendiri.** Penyebabnya berlapis:

1. **Revisi REV-3S.**
   - Saya menambahkan `Switch Patroli Swadaya Reguler = 0` ke dalam `Hari Patroli Swadaya`. Akibatnya, setelah 2025 tidak ada satu pun jalur patroli pada S2.
   - Master prompt berbunyi: "aktivitas reguler di luar pembiayaan awal hanya dapat digunakan jika dasar datanya tersedia secara terpisah." Saya menafsirkannya sebagai "patroli reguler = 0". Mestinya ini saya angkat sebagai keputusan yang perlu ditetapkan peneliti, bukan asumsi nol yang diam-diam.
   - Di makalah, nilai nol itu kemudian disajikan sebagai hasil ("perlindungan hanya bertahan selama patroli didanai"). Kesimpulan itu adalah artefak asumsi, bukan temuan.
2. **Struktur bawaan model A1 yang tidak saya ubah.**
   - Semua jalur belanja LPHD dikalikan `Switch Karbon`: operasional, patroli, kebakaran, rehabilitasi, kelembagaan, dan KUPS.
   - Bahkan `Dana Program Eksogen` (Rp 2 miliar/th; sumber non-karbon) ikut dikalikan `Switch Karbon`.
   - Jadi pada S2 tidak ada sumber dana apa pun yang dapat membiayai kegiatan. Model lama tidak merasakan masalah ini, karena patroli S2 lama (2.355 HOK) berjalan tanpa dana sebagai swadaya.
3. **Perlakuan antarkegiatan tidak seragam.** Pada S2 setelah 2025:
   - rehabilitasi tetap berjalan (20,13 ha/th, upah Rp 181 juta/th);
   - KUPS dipertahankan ±33 unit dengan penggantian penuh;
   - 254 anggota patroli tetap dipertahankan dan diganti setiap tahun;
   - model menghitung biaya `Dana PS Eksisting` Rp 1,42 miliar/th untuk "patroli sukarela, penanaman, dan pendampingan KUPS";
   - tetapi patroli = 0 HOK dan pengendalian kebakaran = 0.
   Kegiatan PS lain dianggap berlanjut tanpa dana, sedangkan patroli dianggap berhenti.

**Data patroli final tidak diubah:** 2024 = 2.533 HOK dan 2025 = 3.011 HOK, keduanya bagian dari pembiayaan awal. Angka 2.355 HOK/th **tidak** direkomendasikan sebagai nilai empiris pasca-2025 (lihat R1).

---

## 1. Patroli reguler dan patroli yang dibiayai (View 04)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Hari Patroli Pembiayaan Awal` | `Switch Pendanaan Awal*(HOK…2024*(STEP(1,2024)-STEP(1,2025)) + HOK…2025*(STEP(1,2025)-STEP(1,2026)))` | 2.533 dan 3.011 HOK/th; rekap final peneliti (A) | 2.533 | 3.011 | 0 | 0 | 0 | 0 | berhenti sesuai data | Konsisten dengan data dan periode dana | Tidak ganda: satu-satunya jalur patroli 2024–2025. HOK/Year ✓ | **C** |
| `Hari Patroli Swadaya` | `Switch PS*Switch Patroli Swadaya Reguler*(1-Periode Pembiayaan Awal)*MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota` | `Switch Patroli Swadaya Reguler` = 0 (REV-3S, Desain); `Hari Patroli Swadaya per Anggota` = 12,87 (log 2023, B lemah) | 0 | 0 | 0 | 0 | 0 | 0 | **berhenti total** | **Tidak masuk akal secara konseptual.** S2 didefinisikan sebagai PS yang tetap dikelola, tetapi tidak ada patroli sama sekali selama 62 tahun. Nol tidak didukung data, sama halnya dengan 2.355 | Faktor `(1-Periode…)` sudah mencegah ganda 2024–2025 ✓ | **A** |
| `Hari Patroli Didanai` | `(Pendanaan Awal untuk Patroli + Realisasi Belanja Perlindungan)/Biaya per Hari Patroli + Hari Patroli Pembiayaan Awal` | `Biaya per Hari Patroli` Rp 260.000/HOK (Perbup Kobar 29/2020, C) | 2.533 | 3.011 | 0 | 0 | 0 | 0 | berhenti | Benar secara mekanis; satu-satunya sumber dana pasca-2025 adalah karbon (lihat bagian 2) | Rupiah/(Rupiah/HOK) = HOK ✓ | C (struktur) / A (akibat bagian 2) |
| `Anggota Patroli Aktif` (stok) | `INTEG(Penambahan−Pengurangan, 183)`; penambahan = penggantian penuh bila `Switch PS`=1, + tim baru 61 (2024) dan 10 (2025) bila `Switch Pendanaan Awal`=1 | Awal 183 (MR1, B); tim baru 61/10 (MR1, A); keluar 5 %/th (D); penggantian 1 (D) | 183 | 244 | 254 | 254 | 254 | 254 | tetap | **Tidak konsisten:** 254 anggota dipertahankan dan 12,7 orang/th direkrut ulang, tetapi kerjanya 0 HOK. Kapasitas 12.190 HOK/th tidak terpakai | – | **A** |
| `Kapasitas Hari Patroli Anggota` | `Anggota Patroli Aktif*48*Pengali Kapasitas Mode Lama` | 48 HOK/orang/th (D) | 8.784 | tt | 12.190 | 12.190 | 12.190 | 12.190 | tetap | Kapasitas ada, aktivitas nol | ✓ | B |
| `Kebutuhan Hari Patroli` | `Jumlah Anggota per Regu*Total Kawasan/Cakupan Kawasan per Regu*Frekuensi Patroli Ideal per Anggota` | 4 orang/regu (tanpa sumber); 750 ha/regu (tanpa sumber); 12 HOK/orang/th (D) | 7.996 | 7.996 | 7.996 | 7.996 | 7.996 | 7.996 | tetap | Norma kebutuhan tidak bersumber, padahal menentukan penyebut intensitas dan kebutuhan dana Rp 2,08 miliar | ✓ | **B** |
| `Indeks Intensitas Perlindungan` | `MIN(1,(Swadaya+Didanai)/Kebutuhan)` | – | 0,317 | 0,377 | 0 | 0 | 0 | 0 | berhenti | Akibat langsung dari dua baris A di atas. Tahun 2024: patroli 20 HD dibagi kebutuhan 25 HD (tidak diekstrapolasi, sesuai instruksi) | Dmnl ✓ | A (akibat) |
| `Nilai Kontribusi Swadaya`, `HOK Patroli`, `Manfaat Ekonomi Patroli` | `Hari Patroli Swadaya*Rp 260.000`; `= Hari Patroli Swadaya`; `HOK Patroli*0` | `Upah Patroli per HOK` = 0 | 0 | 0 | 0 | 0 | 0 | 0 | berhenti | Kontribusi tenaga non-tunai S2 hilang seluruhnya | ✓ | A (akibat) |

## 2. Sumber pembiayaan dan biaya operasional LPHD (View 14, 13, 16)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Alokasi Dana Operasional/Perlindungan/Pengendalian Kebakaran/Rehabilitasi/Penguatan Kelembagaan/Pengembangan KUPS` (6 variabel) | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi…, Kebutuhan…)` | Proporsi 10/30/10/15/15/20 % (D) | 0 | 0 | 0 | 0 | 0 | 0 | nol | **Kesalahan struktural:** LPHD hanya bisa membelanjakan dana karbon. Tidak ada saluran dana desa, APBD, program KLHK/BPDAS, atau donor | Rupiah/Year ✓ | **A** |
| `Dana Desa Diterima` | `IF Switch Dana Program Eksogen=1 THEN Switch Karbon*Dana Program Eksogen*(periode) ELSE Dana Program PS dari Karbon` | `Dana Program Eksogen` Rp 2 miliar/th, 2026–2055 (Desain); switch = 0 | 0 | 0 | 0 | 0 | 0 | 0 | nol | **Dana non-karbon dikalikan `Switch Karbon`**, sehingga tidak pernah dapat dipakai di S2 | ✓ | **A** |
| `Dana PS Eksisting` = `Biaya Pengelolaan PS Non Karbon` | `Switch PS*Anggota Patroli Aktif*1,19 juta + Switch Rehabilitasi*0,0123*1.636,8*(1-Periode Historis)*Rp 14 juta + Switch PS*Jumlah KUPS Aktif*Rp 25 juta` | 1,19 juta/anggota/th (File A, C); Rp 14 juta/ha (C); Rp 25 juta/KUPS (D) | tt | tt | 1,42 miliar | 1,42 miliar | 1,42 miliar | 1,42 miliar | tetap | **Variabel buntu:** dihitung (patroli sukarela Rp 302,8 juta + penanaman Rp 281,9 juta + pendampingan KUPS Rp 835,5 juta), tetapi tidak dipakai variabel lain. Biaya patroli sukarela dihitung untuk patroli yang nol | Bisa ganda bila nanti disambungkan tanpa mengurangi kebutuhan | **A** |
| `Kebutuhan Dana Minimum` | `Operasional + Perlindungan + Kebakaran` | Operasional Rp 50 juta/LPHD (D); patroli 7.996 × Rp 260.000; kebakaran 25 regu × Rp 108 juta | 6,03 miliar | 6,03 miliar | 6,03 miliar | 6,03 miliar | 6,03 miliar | 6,03 miliar | tetap | Seluruh kebutuhan patroli dianggap harus dibiayai, karena swadaya = 0 | ✓ | B |
| `Kesenjangan Pembiayaan Minimum` | `MAX(0, Kebutuhan − Penggunaan Dana − Realisasi Pembiayaan Awal)` | – | 5,37 miliar | 5,25 miliar | 6,03 miliar | 6,03 miliar | 6,03 miliar | 6,03 miliar | naik lalu tetap | Pembiayaan awal dikurangkan sekali ✓. Kesenjangan S2 = 100 % kebutuhan karena tidak ada sumber lain di model | ✓ | C (mekanis) / A (akibat bagian ini) |
| `Pendanaan Awal Belum Terpulihkan` | `INTEG(Realisasi Pembiayaan Awal*Porsi Talangan − Pemulihan, 0)`; pemulihan hanya dari dana mitra karbon | Porsi talangan = 1 (D) | 0 | 0,66 miliar | 1,44 miliar | 1,44 miliar | 1,44 miliar | 1,44 miliar | tetap | Pada S2 pembiayaan awal diperlakukan sebagai talangan yang tidak pernah kembali. Status hibah vs talangan belum diketahui | Hanya pelaporan; masuk NPV mitra, bukan NPV S2 | **D** |

## 3. Rehabilitasi dan perlindungan hutan (View 06)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Penambahan Luas Penanaman` | `Switch Rehabilitasi*(1-Periode Historis)*MIN(Proporsi Realisasi Penanaman*Target Penanaman, …)` | Realisasi BAU 0,0123 (File A, C); target 1.636,8 ha/th (RKPS, Desain) | 0 | 20,13 | 20,13 | 20,13 | 20,13 | 20,13 | tetap | Penanaman berlanjut 62 tahun tanpa variabel sumber dana. Laju 20 ha/th berasal dari realisasi historis, jadi masuk akal sebagai "program non-karbon yang sudah berjalan" | ha/th ✓ | **B** |
| `Manfaat Ekonomi Penanaman` (upah) | `HOK Penanaman*Rp 106.000` | 85 HOK/ha (C); Rp 106.000/HOK (UMK, B) | 0 | 181 juta | 181 juta | 181 juta | 181 juta | 181 juta | tetap | Upah dibayar tanpa sumber dana di model, lalu masuk pendapatan RT. Ini asimetris dengan patroli | Rupiah/Year ✓ | **A** (asimetri) |
| `Tingkat Keberhasilan Rehabilitasi` | dasar 0,45 + bonus pemeliharaan × fraksi terpelihara | 0,45 (C); 0,62 dengan pemeliharaan (B) | 0,45 | 0,45 | 0,45 | 0,45 | 0,45 | 0,45 | tetap | Tanpa dana pemeliharaan, keberhasilan dasar dipakai. Konsisten | ✓ | C |
| `Luas Penanaman Program` (kumulatif) | `Luas Penanaman − 1,798` | – | 0 | tt | tt | 110 | 513 | 1.248 | naik | Menambah hutan S2 sekitar +441 ha pada 2087 dibanding S1 | ✓ | C |

## 4. Pencegahan dan penanganan kebakaran (View 05)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Regu Pengendalian Kebakaran Terlaksana` | `Realisasi Belanja Pengendalian Kebakaran/Biaya per Regu` | Rp 108 juta/regu/th (D) | 0 | 0 | 0 | 0 | 0 | 0 | nol | Tidak ada kegiatan pencegahan kebakaran pada S2, termasuk 2024–2025. Apakah ada MPA/regu swadaya di 25 HD belum diketahui | ✓ | **B / D** |
| `Faktor Pengendalian Risiko Kebakaran` | `MAX(0,2, 1 − Efektivitas Patroli terhadap Kebakaran*Kecukupan − Efek Program)` | Efektivitas patroli terhadap kebakaran = 0 (B) | 1 | 1 | 1 | 1 | 1 | 1 | tetap | Patroli tidak memengaruhi kebakaran. Konsisten dengan parameter, tetapi tidak diuji | ✓ | B |
| `Luas Karhutla Tahunan` | Historis 355,19 (2024), 331,06 (2025); lalu `2,736 × 121 × Faktor` | File A (B) | 355,2 | 331,1 | 331,1 | 331,1 | 331,1 | 331,1 | tetap | Sama dengan S1. `Efek Pengendalian Kebakaran terhadap Deforestasi` = 0 karena `Proporsi Deforestasi Terkait Kebakaran` = 0 (D). Kebakaran tidak memengaruhi deforestasi di model mana pun | ✓ | **B** |

## 5. Kelembagaan LPHD dan kapasitas pengelolaan (View 11)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Indeks Kapasitas LPHD` (stok) | `INTEG((Target − Indeks)/3, 0,5)`; target naik hanya lewat `Faktor Penguatan Kelembagaan dari Karbon` | Awal 0,5 (D); waktu 3 th (D) | 0,5 | 0,5 | 0,5 | 0,5 | 0,5 | 0,5 | tetap | Kapasitas LPHD hanya dapat tumbuh dari dana karbon. Pendampingan dan program pemerintah tidak dimodelkan | ✓ | **B** |
| `Rasio Realisasi Belanja` | `MIN(1, Indeks Kapasitas/0,8)` | 0,8 (D) | 0,625 | 0,625 | 0,625 | 0,625 | 0,625 | 0,625 | tetap | Tidak bekerja pada S2 karena belanja = 0 | ✓ | C |
| `Total Partisipasi Kegiatan PS` | `Anggota KUPS + Anggota Patroli Aktif + Penerima Penanaman` | – | tt | tt | tt | 795 | 788 | 785 | tetap | Memasukkan 254 anggota patroli yang tidak berpatroli, sehingga partisipasi dan `Manfaat Ekonomi PS per Peserta` menjadi bias | ✓ | **A** (akibat bagian 1) |
| `Total Partisipasi Referensi`, `Tingkat Kecukupan Patroli Referensi` | `SAMPLE IF TRUE(Time <= 2025, X, X)` | – | – | – | 755,5 / 0,377 | sama | sama | sama | dibekukan | Acuan dibekukan pada 2025, saat patroli pembiayaan awal sedang puncak. `Indeks Perubahan Patroli` S2 menjadi −0,604, tetapi sensitivitasnya = 0 sehingga tidak berdampak sekarang. Akan menyimpang bila sensitivitas diaktifkan | ✓ | **B** |

## 6. KUPS: modal, pertumbuhan, dan ketidakaktifan (View 09)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Jumlah KUPS Aktif` (stok) | Historis +15 (2024) dan +5 (2025); sesudahnya `Switch PS*MIN(keluar × penggantian 1 + 0 + karbon, …)` | Awal 15 (2023, sumber BELUM TERVERIFIKASI); tambahan MR1 (A); keluar 5 %/th (D); penggantian 1 (D) | 15 | 30 | 33,4 | 33,4 | 33,4 | 33,4 | naik lalu tetap | KUPS berlanjut tanpa dana dengan penggantian penuh, padahal patroli dianggap berhenti. Sebaiknya kedua kegiatan diperlakukan sama | ✓ | **B** |
| `Anggota KUPS Aktif` (stok) | +206 (2024), +57 (2025); lalu `penambahan KUPS × 15` | MR1 (B) | 277 | tt | tt | 513 | 505 | 502 | sedikit turun | Wajar | ✓ | C |
| `Proporsi KUPS Produktif` | `SMOOTHI(0,42 + (0,9 − 0,42)*Faktor Dukungan Karbon, 2, …)` | 0,42 (Status KUPS Okt 2026, C) | 0,42 | 0,42 | 0,42 | 0,42 | 0,42 | 0,42 | tetap | Tanpa modal non-karbon, produktivitas tidak dapat naik di S2 | ✓ | B |
| `Penjualan KUPS` / `Manfaat Ekonomi KUPS` / `Pendapatan KUPS Total` | produktif × Rp 9,61 juta / × Rp 6,65 juta / × 0,263 | Status KUPS Okt 2026 (B); MR1 (B) | tt | tt | tt | 135,0 / 93,3 / 24,5 juta | sama | sama | tetap | Konsisten dengan data. Omzet, surplus, dan penerimaan anggota dibedakan ✓ | ✓ | C |
| Modal usaha KUPS | Tidak ada variabel modal. Pembentukan non-karbon = 0 (File A: tidak ada pembentukan 2024–2025; tetapi MR1 mencatat +15 dan +5) | C | – | – | – | – | – | – | – | Ada ketidakselarasan sumber: komentar File A menyebut tidak ada pembentukan, padahal model memakai +15/+5 dari MR1 | – | **D** |

## 7. Kesempatan kerja berupah dan tenaga non-tunai (View 07, 04, 06)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Kesempatan Kerja PS` | `Total HOK PS (patroli swadaya + penanaman) + HOK Patroli Berbayar + HOK Kebakaran` | – | 2.533 | 4.722 | 1.711 | 1.711 | 1.711 | 1.711 | turun tajam lalu tetap | Patroli pembiayaan awal dihitung sebagai kerja berbayar ✓. Setelah 2025 hanya tersisa penanaman | ✓ tidak ganda (swadaya = 0) | A (akibat bagian 1) |
| `Kesempatan Kerja Setara Penuh` | `/300` | 300 HOK/orang/th (PP 36/2021, B) | 8,4 | 15,7 | 5,7 | 5,7 | 5,7 | 5,7 | turun | – | FTE ≠ orang | C |
| `Upah Patroli Berbayar` | `HOK Patroli Berbayar*Rp 130.000` | Rp 130.000/HOK (Perbup Kobar, C) | 329 juta | 391 juta | 0 | 0 | 0 | 0 | berhenti | Biaya Rp 260.000/HOK dipakai untuk nilai pembiayaan awal, upah Rp 130.000/HOK untuk pendapatan. Selisihnya diasumsikan biaya logistik. Belum diverifikasi apakah Rp 260.000 adalah biaya per orang-hari atau per regu-hari | Kemungkinan salah satuan | **D** |
| Tenaga non-tunai (`Nilai Kontribusi Swadaya`) | lihat bagian 1 | – | 0 | 0 | 0 | 0 | 0 | 0 | nol | Kontribusi sukarela anggota tidak tercatat sama sekali | – | A (akibat) |

## 8. Pendapatan rumah tangga dan pembatasan akses (View 08, 10)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Kehilangan Pendapatan Pembatasan Akses per RT` | `Pendapatan Hutan per RT*0,25*Pengurangan Relatif Deforestasi*Pengali` | 0,25 (D); pengali 1 (D) | tt | tt | tt | 56.650 | 63 | ≈0 | turun ke nol | Kehilangan akses hanya muncul bila patroli menekan deforestasi. Pada S2 kehilangan akses ikut hilang karena patroli nol. Konsisten secara internal, tetapi sepenuhnya asumsi | ✓ | B |
| `Pendapatan Program per RT Bergantung` | `(KUPS inkremental + Upah PS*0,5)*porsi/RT` | 0,5 (D) | tt | tt | tt | 4.415 | 3.168 | 1.728 | turun | Memasukkan upah penanaman tanpa sumber dana (bagian 3) | ✓ | B |
| `Pendapatan Bersih per RT Bergantung` | `hutan + non-hutan + program − kehilangan` | Rp 41,76 juta (Setiawan dkk. 2021, harga 2021, B) | 41,75 juta | 41,48 juta | 41,48 juta | 41,54 juta | 41,12 juta | 40,63 juta | sedikit turun | Penurunan mengikuti kondisi hutan. Pengaruh S2 kecil | ✓ | C |

## 9. Intensitas perlindungan dan efektivitas patroli (View 04, 12)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Efek Pengelolaan PS Aktif` | `… + (Switch PS*Switch Dampak Skenario Lahan*SMOOTHI(Respons Perlindungan, 3, Respons Perlindungan(t0))*0,37 − …)*Mutu` | Efektivitas 0,37 (Oldekop dkk. 2019; register FINAL: D); waktu penyesuaian 3 th (D) | 0 | 0,120 | 0,106 | 0,028 | 0,00003 | ≈0 | puncak 2025 lalu meluruh | **SMOOTHI diinisialisasi dengan respons 2024 (0,317)**, padahal patroli 2024 adalah intervensi baru. Akibatnya efek 2025 langsung penuh tanpa jeda. Kalimat makalah "efek patroli bekerja dengan jeda tiga tahun" tidak sesuai perilaku model | ✓ | **A** (narasi) / **B** (struktur) |
| `Switch Dampak Skenario Lahan` | `STEP(1, 2025)` | Desain | 0 | 1 | 1 | 1 | 1 | 1 | – | Patroli 2024 tidak memengaruhi deforestasi 2024, tetapi menentukan nilai awal SMOOTHI. Ini tidak konsisten dengan baris di atas | – | B |
| `Efek Pengelolaan PS Tanpa Karbon`, `Cakupan Risiko Swadaya` | berbasis `Hari Patroli Swadaya` | Rasio risiko 0,651 (C) | 0 | 0 | 0 | 0 | 0 | 0 | nol | Komponen "PS tanpa karbon" model kosong, sehingga basis kredit A2 sama dengan A1 | ✓ | A (akibat bagian 1) |
| `Efek Izin PS terhadap Deforestasi` | konstanta 0 | Kraus dkk. 2021 (C) | 0 | 0 | 0 | 0 | 0 | 0 | – | Hak kelola tanpa kegiatan tidak memberi efek. Didukung literatur agregat, sehingga di S2 seluruh efek PS bergantung pada patroli | ✓ | C |
| `Efek Penghidupan terhadap Deforestasi` | sensitivitas = 0 | D | 0 | 0 | 0 | 0 | 0 | 0 | – | KUPS dan upah tidak memengaruhi deforestasi | ✓ | B |

## 10. Deforestasi, emisi dihindari, dan pengaruh waktu (View 01, 02, 15)

| Variabel | Persamaan berlaku | Parameter, sumber, kelas | 2024 | 2025 | 2026 | 2030 | 2050 | 2087 | Arah | Penilaian | Ganda / satuan | Kelas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Deforestasi Total` S2 (S1) | stok × laju BAU × `Faktor Tekanan` | Laju BAU kalibrasi (B) | 522 (522) | 458 (520) | 464 (519) | 499 (512) | 486 (484) | 456 (454) | turun 2025 lalu kembali ke S1 ±2035 | Akibat langsung patroli nol. Setelah ±2040 deforestasi S2 sedikit di atas S1 karena stok hutan lebih besar dari rehabilitasi | ✓ | A (akibat) |
| `Deforestasi Total Baseline` | baseline kredit = jalur tanpa PS | – | 522 | 520 | 519 | 512 | 484 | 454 | – | Sama dengan S1 ✓ | ✓ | C |
| Emisi dihindari S2−S1 (91.908 tCO₂e, kumulatif) | `Total Emisi Bersih` = emisi − serapan | – | 0 | 23.100 (968.500 vs 991.600) | tt | tt | tt | tt | – | **Mencampur deforestasi dihindari dan serapan rehabilitasi.** Di makalah ditulis sebagai "emisi dihindari", padahal sebagian adalah serapan rehabilitasi. Porsinya belum dipisahkan | ✓ | **D** |

---

## Ringkasan klasifikasi

| Kelas | Temuan |
|---|---|
| **A. Kesalahan terkonfirmasi** | (A1) Patroli reguler S2 dipaksa nol oleh `Switch Patroli Swadaya Reguler = 0` (REV-3S) tanpa dasar data dan tanpa keputusan peneliti. (A2) Semua belanja LPHD dan `Dana Program Eksogen` dikalikan `Switch Karbon`, sehingga S2 tidak punya sumber dana non-karbon. (A3) `Dana PS Eksisting` Rp 1,42 miliar/th dihitung, termasuk biaya patroli sukarela, tetapi tidak tersambung ke kegiatan. (A4) Perlakuan tidak seragam: rehabilitasi, KUPS, dan anggota patroli berlanjut tanpa dana, sedangkan patroli dan kebakaran berhenti. (A5) 254 anggota patroli dipertahankan dan direkrut ulang dengan aktivitas nol. (A6) Narasi makalah "jeda tiga tahun" tidak sesuai perilaku SMOOTHI. (A7) Kesimpulan makalah "perlindungan hanya bertahan selama patroli didanai" adalah artefak A1–A2 |
| **B. Asumsi lemah** | Norma kebutuhan patroli (4 orang/regu, 750 ha/regu, 12 HOK/orang); inisialisasi SMOOTHI dan `Switch Dampak` 2025; kapasitas LPHD hanya naik dari karbon; acuan `SAMPLE IF TRUE` dibekukan pada 2025; rehabilitasi 20,13 ha/th tanpa sumber dana eksplisit; KUPS dengan penggantian penuh; kebakaran tanpa kegiatan dan tanpa kopling ke deforestasi; kehilangan akses sepenuhnya asumsi; efektivitas 0,37 |
| **C. Konsisten** | Data patroli 2.533/3.011 HOK dan periodenya; tidak ada penghitungan ganda pembiayaan awal; satuan HOK × Rp/HOK; baseline kredit = S1; keberhasilan rehabilitasi; data dan rantai KUPS (omzet, surplus, penerimaan anggota); FTE; tim patroli baru 61/10 |
| **D. Belum dapat dipastikan** | Ada tidaknya patroli swadaya atau reguler setelah 2025 dan besarannya; Rp 260.000 per orang-hari atau per regu-hari; status pembiayaan awal (hibah atau talangan); keberadaan regu MPA; ketidakselarasan sumber pembentukan KUPS 2024–2025; porsi serapan rehabilitasi dalam "emisi dihindari" |

---

## Rekomendasi koreksi (belum diterapkan)

Urutan menurut dampak. Setiap rekomendasi berupa perubahan persamaan yang dapat diuji. Nilai pasca-2025 **tidak** saya tetapkan karena itu keputusan peneliti.

**R1. Patroli reguler PS pasca-2025 sebagai komponen eksplisit, terpisah dari pembiayaan awal (memperbaiki A1, A5).**

Tambahkan:

```
HOK Patroli Reguler PS = Switch PS*(1-Periode Pembiayaan Awal)*STEP(1, Tahun Akhir Pembiayaan Awal+1)
                         *MIN(Kapasitas Hari Patroli Anggota, HOK Patroli Reguler Pasca Pembiayaan Awal)
```

`HOK Patroli Reguler Pasca Pembiayaan Awal` (HOK/Year) diisi peneliti dengan salah satu dasar berikut:
- **(a) Data patroli 2026 bila sudah ada.** Ini dasar terkuat.
- **(b) Tingkat 2025 dikali faktor keberlanjutan** (0–1, kelas D), dengan 3.011 HOK sebagai batas atas yang teramati.
- **(c) Log swadaya 2023** dalam satuan yang sama, yaitu keikutsertaan. Sebagai perbandingan: 392 kegiatan Feb–Des 2023 × 5,51 orang ≈ 2.160 keikutsertaan, atau ±2.355 bila disetahunkan. Angka ini hanya pembanding, bukan nilai pasca-2025, karena dicatat sebelum ada pembiayaan awal.

Lalu `Hari Patroli Swadaya` diganti oleh variabel ini, dan `Switch Patroli Swadaya Reguler` dihapus. Kebutuhan dana patroli dikurangi patroli reguler agar tidak terhitung ganda.

Karena besarannya belum didukung data, **jalankan sebagai rentang sensitivitas** (misalnya 0 / ½ / 1 × tingkat 2025). Laporkan S2−S1 sebagai rentang, bukan satu angka.

**R2. Sumber pembiayaan non-karbon untuk S2 dan S3 (memperbaiki A2).**
- Ganti faktor `Switch Karbon` pada `Dana Desa Diterima` cabang eksogen menjadi `Switch PS`.
- Tambahkan aliran masuk `Dana Pengelolaan PS Non Karbon` ke `Saldo Dana LPHD`, yaitu dana desa, APBD, program pemerintah, dan donor. Nilainya parameter peneliti (default 0 bila tidak ada data, ditulis eksplisit).
- Ganti `Switch Karbon` pada 6 persamaan `Alokasi Dana …` dengan `Switch PS`. Alokasi tetap dibatasi saldo, jadi tanpa dana tetap nol.
- Dana karbon S3 menjadi tambahan di atas dana non-karbon. Selisih S3−S2 tetap hanya mencerminkan karbon.

**R3. Sambungkan atau hapus `Dana PS Eksisting` (memperbaiki A3).**
- Pilihan 1: jadikan sumber dana untuk patroli reguler, penanaman, dan pendampingan KUPS pada S2.
- Pilihan 2: hapus dan pindahkan ke catatan.
- Komponen "operasional patroli sukarela" tidak boleh dihitung bila patroli = 0.

**R4. Perlakuan seragam antarkegiatan PS (memperbaiki A4).** Rehabilitasi (20,13 ha/th), penggantian KUPS, penggantian anggota patroli, dan patroli reguler pasca-2025 sebaiknya mengikuti satu aturan. Ada dua pilihan:
- semuanya berlanjut sebagai kegiatan PS non-karbon, dengan sumber dan intensitas yang dinyatakan; atau
- semuanya bergantung pada dana yang tersedia (R2).

Bila diputuskan sebagai kerja sukarela, catat nilai tenaga non-tunainya (`Nilai Kontribusi Swadaya`) dan jangan hitung sebagai upah.

**R5. Inisialisasi efek perlindungan (memperbaiki A6 dan B).**
- Bila patroli dianggap baru dimulai 2024, set nilai awal SMOOTHI = 0.
- Bila log 2023 dianggap bukti patroli sudah ada, nilai awalnya intensitas 2023 (0,2251 × rasio risiko).
- Selaraskan dengan `Switch Dampak Skenario Lahan` dan perbaiki kalimat "jeda tiga tahun" di makalah.

**R6. Acuan `SAMPLE IF TRUE`.** Bekukan `Tingkat Kecukupan Patroli Referensi` dan `Total Partisipasi Referensi` pada kondisi awal 2024 atau pra-pembiayaan, bukan 2025. Perbaikan ini perlu sebelum sensitivitas tekanan hutan diaktifkan.

**R7. Partisipasi.** Hitung `Total Partisipasi Kegiatan PS` dari anggota patroli yang benar-benar aktif berpatroli (HOK > 0), bukan seluruh stok anggota.

**R8. Kebakaran.** Bila ada data MPA atau regu swadaya, masukkan sebagai kegiatan non-karbon (R2/R4). Kopling kebakaran–deforestasi (`Proporsi Deforestasi Terkait Kebakaran` = 0) dinyatakan sebagai keterbatasan atau diuji sensitivitasnya.

**R9. Pelaporan emisi.** Pisahkan "emisi dihindari dari deforestasi" dan "serapan rehabilitasi" pada indikator S2−S1.

**R10. Verifikasi data (D).**
- Pastikan satuan Rp 260.000 (per orang-hari atau per regu-hari).
- Pastikan status pembiayaan awal (hibah atau talangan).
- Pastikan sumber pembentukan KUPS 2024–2025.
- Pastikan ada tidaknya data patroli 2026.

**Yang tidak direkomendasikan:** memasukkan kembali 2.355 HOK/th sebagai nilai empiris pasca-2025, atau mengekstrapolasi patroli 2024 ke 25 HD.

---

## Keputusan yang diperlukan dari peneliti sebelum revisi

1. Dasar besaran patroli reguler pasca-2025: R1 (a), (b), (c), atau kombinasi sebagai rentang.
2. Apakah S2 mencakup sumber dana non-karbon eksplisit (R2), dan dengan nilai berapa (atau 0 dengan pernyataan eksplisit).
3. Apakah kegiatan PS non-karbon diperlakukan sebagai kerja sukarela (non-tunai) atau kegiatan berupah (R4).
4. Nilai awal efek perlindungan 2024 (R5).
