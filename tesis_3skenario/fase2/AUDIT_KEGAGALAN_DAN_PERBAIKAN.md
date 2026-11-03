# Audit Kegagalan dan Perbaikan (Fase 2)

**Model akhir:** `DKP_25HD_FINAL_2SKENARIO.mdl` (md5 `aa1428dffdc27541d531926b9806c50e`).

**Perangkat:** semua uji memakai PySD 3.14.3. Vensim native tidak digunakan.

Setiap kegagalan dicatat beserta penyebab, kelas (kesalahan model atau kesalahan kriteria/parameter uji), perbaikan, dan uji yang diulang. Perbaikan hanya menyentuh persamaan yang bermasalah.

---

## 1. Kegagalan yang ditemukan dan diperbaiki

| No | Uji yang gagal | Gejala | Penyebab | Kelas | Perbaikan | Uji diulang | Status akhir |
|---|---|---|---|---|---|---|---|
| **F1** | U0b (loop aljabar) | Komponen terhubung kuat: `Dana Mitra dari Karbon` → `Pemulihan Pendanaan Awal` → `Pemulihan Talangan Sebelum Bagi Hasil` → `Pendapatan Karbon Bersih …` → `Dana Mitra …` | Penambahan D2 (varian talangan sesudah bagi hasil) menulis kedua varian dalam satu variabel `Pemulihan Pendanaan Awal` yang membaca `Dana Mitra`. Switch memang menolkan salah satu cabang secara numerik, tetapi strukturnya persamaan simultan, dan Vensim akan menolaknya | **Kesalahan model** (implementasi D2) | Dipecah menjadi `Pemulihan Talangan Sebelum Bagi Hasil` (dari surplus) dan `Pemulihan Talangan Sesudah Bagi Hasil` (dari bagian mitra); `Pemulihan Pendanaan Awal` = jumlah keduanya | U0a, U0b, U18, U15, E7, seluruh baterai | LULUS: 0 loop |
| **F2** | U14 | Kas pertama 2028,06 / 2029,06 / 2030,06, bukan "±2027 / 2028 / 2029" | Kriteria di `RENCANA_UJI_FASE2.md` keliru. Pengurangan emisi baru terjadi mulai 2025 (`Switch Dampak Skenario Lahan` = STEP 2025), sehingga kredit pertama diajukan 2025, terbit 2025 + jeda, dan dijual satu langkah DT kemudian | **Kesalahan kriteria uji** | Kriteria diganti relasional: terbit = pengajuan pertama + jeda (± 2 DT); kas ≥ terbit; jeda bayar menggeser kas, bukan penjualan. Model tidak diubah | U14 | LULUS |
| **F3** | U16 (perilaku) | Varian `Switch Baseline Kredit Konservatif` = 1 menghasilkan kredit REDD = 0 pada semua harga | Kredit konservatif hanya mengakui efek patroli yang dibiayai kas karbon, sedangkan kas karbon hanya ada bila sudah ada kredit. Loop tidak pernah dimulai, kecuali ada pendanaan tambahan di luar pembiayaan awal historis. Ini **bukan galat persamaan**, tetapi varian ini tidak dapat menjawab "berapa kredit di atas perlindungan S1" | **Keterbatasan desain C3** | Ditambahkan dua variabel **pelaporan**: `Potensi Kredit REDD Konservatif` dan `Potensi Kredit ARR Konservatif`. Keduanya dihitung di dalam run BAU tanpa memengaruhi penerimaan. Varian switch dipertahankan dan dicatat sebagai degeneratif | U0b, U16, U18, seluruh baterai | LULUS. Kredit konservatif-pelaporan 182.112 tCO₂e (USD 20) vs emisi dihindari S2−S1 × faktor eligible 195.006: dekat, dan selisihnya dari aproksimasi porsi |
| **F4** | U0b (kriteria) | Pemakai `Switch Karbon` = 9, padahal kriteria 7 | Dua variabel pelaporan F3 sah memakai `Switch Karbon` (rantai kredit) | **Kriteria basi** setelah F3 | Kriteria diganti daftar eksplisit 9 variabel (7 rantai kredit/MRV + 2 pelaporan F3) | U0b | LULUS |
| **F5** | U0d | Deforestasi peniru 29.636 vs S2 lama 29.687 ha (0,17 %) | **Parameter uji peniru keliru.** `Rasio Risiko Penempatan` disetel 1 tetapi `Keikutsertaan Patroli 2023` masih dibagi 0,651, sehingga intensitas awal 0,487 (bukan 0,317). Didiagnosis dengan menelusuri variabel pertama yang menyimpang (`Efek Pengelolaan PS Tanpa Karbon`) dan kode PySD-nya | **Kesalahan parameter uji**, bukan model | Peniru: keikutsertaan 2023 = 2.533 dan rasio = 1 | U0d | LULUS: deforestasi 29.686,7 = 29.686,7 ha; hutan 2087 82.331,0 = 82.331,0 ha |
| **F6** | E7 (kriteria) | NPV proyek keseluruhan berubah antara hibah dan talangan (6,72 vs 6,22 miliar pada USD 20) | Kriteria "NPV proyek tidak berubah" hanya benar tanpa umpan balik. Pemulihan talangan sebelum bagi hasil mengurangi kas LPHD, lalu patroli, lalu kredit, lalu penerimaan. Identitas akuntansi tetap terpenuhi (\|selisih\| ≤ 2,4·10⁻⁷ Rp/th) | **Kesalahan kriteria uji** | Kriteria E7 direvisi menjadi identitas arus kas + batas pemulihan ≤ pokok + biaya modal | E7, U15 | LULUS |

Catatan proses pada final gate (sebelum Fase 2): parser membaca variabel pertama di berkas dengan awalan header `{UTF-8}`. Galat itu sudah diperbaiki di semua skrip pemeriksa.

---

## 2. Temuan yang belum diperbaiki (tidak menggagalkan uji, tetapi membatasi tafsiran)

| No | Temuan | Bukti | Dampak | Tindak lanjut |
|---|---|---|---|---|
| T-a | **Bunga talangan tanpa batas** pada varian "sesudah bagi hasil" dengan biaya modal > 0 | Biaya modal 20 %/th: sisa talangan 2087 = Rp 1,05·10¹⁴. Bagian 40 % mitra tidak cukup membayar bunga, dan model tidak punya batas penghapusan | Hanya bila `Biaya Modal Pendanaan Awal` > 0 **dan** `Switch Pemulihan Talangan Sebelum Bagi Hasil` = 0. Default (0; sebelum bagi hasil) tidak terdampak | Jangan pakai kombinasi ini tanpa menambahkan batas atau penghapusan; keputusan peneliti |
| T-b | **Varian switch konservatif degeneratif** (F3) | Kredit = 0 | Tidak boleh dipakai sebagai hasil. Gunakan variabel pelaporan | Dilaporkan |
| T-c | **Penurunan KUPS S1** dari 33,4 (2026) menjadi 16,8 (2050) dan 5,7 (2087) | U10 | Ditentukan dua parameter kelas D (biaya reaktivasi Rp 50 juta, porsi reinvestasi 0,5). Dengan reaktivasi Rp 12,5 juta, KUPS bertahan 33,4 (P5) | Wajib sensitivitas di Fase 3; tidak boleh ditafsirkan sebagai temuan |
| T-d | Norma kebutuhan patroli (4 orang/regu, 750 ha, 12 HOK) tanpa sumber | Penyebut intensitas 7.996 HOK | Memengaruhi intensitas, kebutuhan dana, dan rekrutmen | Sensitivitas ±50 % |
| T-e | Jangkauan program memakai norma 24 HOK/anggota dan menghitung penanam sukarela | Final gate T5 | Hanya efek penghidupan (sensitivitas 0) | Dicatat |
| T-f | Penerbitan kredit kontinu, bukan per verifikasi | – | Kas nyata lebih tersendat | Keterbatasan |
| T-g | Harga ARR tetap USD 20 | – | ARR baru muncul pada USD 35 (33.286 tCO₂e) | Keputusan peneliti |

---

## 3. Pengendalian tambahan D1–D4

| Kode | Pengendalian | Pelaksanaan |
|---|---|---|
| **D1** | Logistik non-tunai belum terbukti tersedia | Komentar `PERINGATAN D1` pada 5 variabel di `.mdl` (`HOK Patroli Reguler PS`, `Nilai Logistik Non Tunai Patroli`, `Nilai Kontribusi Tenaga Non Tunai`, `Nilai Kontribusi Swadaya`, `Tingkat Keberlanjutan Patroli Reguler`). Nilai non-tunai tidak masuk pendapatan RT (U12) dan tidak masuk kas/NPV |
| **D2** | Talangan sebelum vs sesudah bagi hasil | `Switch Pemulihan Talangan Sebelum Bagi Hasil` (1/0). Kedua varian diuji (U15, E7). Komentar menyatakan mekanisme ini **bukan aturan kontraktual yang disetujui**. Hasil USD 20, talangan tanpa biaya modal: NPV mitra 2,04 miliar (sebelum) vs 1,77 miliar (sesudah = sama dengan hibah, karena pemulihan dari bagian sendiri bukan arus masuk baru) |
| **D3** | NPV sementara | Komentar `PERINGATAN D3` pada 4 variabel NPV/biaya. Lembar "7 NPV sementara" diberi status SEMENTARA. **Harga impas tidak dihitung** di Fase 2 |
| **D4** | Uji perilaku kausal, bukan hanya identitas | P1–P7 menguji arah dan urutan sebab-akibat lintas sektor (lihat lembar 4 dan `LAPORAN_KELAYAKAN_FASE3.md`), termasuk uji putus loop (P2) dan monotonisitas (P3, P6) |

---

## 4. Identitas vs perilaku

Sesuai instruksi, identitas yang hanya mengulang definisi persamaan tidak dianggap bukti validitas perilaku. Pembedaannya:

- **Identitas definisional** (bukti konsistensi implementasi, bukan perilaku): `Check Identitas Patroli`, `Check Identitas HOK Penanaman`, `Check Identitas Surplus/Penjualan KUPS`, `Check Identitas Arus Kas`.
- **Cek silang yang tidak definisional:**
  - stok akhir vs Σ aliran × DT, dihitung ulang dari keluaran: modal KUPS, luas tanam karbon, `Check Neraca Dana LPHD`;
  - S1 = S2 sebelum kas karbon (U4: 32 variabel berbeda, semuanya keuangan/kredit);
  - harga 0 → S2 = S1 (E1);
  - reproduksi persis model lama dengan parameter setara (U0d);
  - invariansi pendapatan RT terhadap nilai non-tunai (U12, nilai non-tunai dikali 7,7 dan 83).
- **Uji perilaku:** P1–P7, E2–E6, U6 (DT).
- **Belum dilakukan:** validasi perilaku terhadap data empiris pasca-2025. Data itu tidak tersedia.
