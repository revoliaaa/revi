# Audit Akuntansi Karbon dan NPV (Fase 1B)

**Lingkup:** baseline, indikator karbon, jeda kas, arus keuangan, dan NPV pada persamaan usulan.

**Belum ada simulasi.** Angka di dokumen ini diturunkan langsung dari parameter.

---

## 1. Tiga jalur yang harus dibedakan

| Jalur | Di model | Fungsi | Patroli |
|---|---|---|---|
| **Baseline BAU** (referensi internal) | rantai stok `… Baseline`, `Faktor Tekanan Deforestasi Baseline` = 1, laju BAU terkalibrasi, tanpa penanaman (`Aliran Penanaman ke Rehabilitasi Baseline` = 0) | Acuan potensi kredit | tidak ada |
| **S1** (skenario kebijakan) | run `Skenario Kebijakan` = 1 | Pembanding kebijakan | historis 2024–2025 + reguler |
| **S2** (skenario kebijakan) | run `Skenario Kebijakan` = 2 | PS + karbon | S1 + tambahan dari kas karbon |

Baseline **berbeda dari S1**: S1 memuat patroli reguler dan rehabilitasi non-karbon, baseline tidak. Baseline dihitung di dalam setiap run dan identik di S1 dan S2, karena hanya bergantung pada stok awal dan laju BAU.

---

## 2. Indikator karbon yang dilaporkan terpisah

| No | Indikator | Definisi | Satuan | Catatan |
|---|---|---|---|---|
| 1 | Perubahan deforestasi S2 terhadap S1 | Σ `Deforestasi Total`(S1) − Σ `Deforestasi Total`(S2), 2025–2086 | ha | Selisih antar-run |
| 2 | Tambahan emisi dihindari S2 terhadap S1 | Σ `Emisi Deforestasi Biomassa`(S1) − (S2) | tCO₂e | **Hanya deforestasi.** Serapan dilaporkan terpisah (no. 2b) |
| 2b | Tambahan serapan rehabilitasi S2 − S1 | Σ `Serapan Rehabilitasi`(S2) − (S1) | tCO₂e | – |
| 3 | Potensi kredit terhadap baseline BAU | Σ `Kredit Karbon Diajukan` pada `Switch Baseline Kredit Konservatif` = 0 | tCO₂e | Setelah kebocoran 10 %, buffer 12 %, proporsi PA 0,682 |
| 4 | Potensi kredit konservatif | idem, dengan switch = 1 | tCO₂e | Lihat bagian 3 |
| 5 | Kredit terbit / terjual / dibayar | `Kredit Karbon Terbit`; `Kredit … Terjual`; `Kas Penjualan Kredit` ÷ harga ÷ kurs | tCO₂e; Rp | Jeda 3 th + penjualan 70 %/th + jeda bayar |

Semua indikator 3–5 adalah **potensi kredit hasil model**. Tidak satu pun berarti kredit terverifikasi, kredit VCU, atau kredit yang memenuhi persyaratan Verra.

**Mengapa no. 1–2 ≠ no. 3:**
- No. 1–2 adalah selisih dua kebijakan.
- No. 3 adalah selisih S2 terhadap baseline tanpa PS. Angka ini mencakup juga efek patroli reguler dan historis yang ada di S1, sehingga no. 3 hampir pasti > no. 2.
- No. 4 mendekati no. 2, karena dirancang untuk mengeluarkan efek S1.

---

## 3. Pendekatan konservatif: double counting dan additionality

**Mekanisme REDD (A1, dipertahankan):**
`Kredit REDD Diajukan = Eligible × (1 − Switch × (1 − Porsi Mitigasi Adisional))`, dengan `Porsi Mitigasi Adisional = (Efek Aktif − Efek Tanpa Karbon)/Efek Aktif`.

**Perubahan Fase 1B:** `Indeks Intensitas Perlindungan Tanpa Karbon` kini memuat patroli reguler, patroli historis 2024–2025, dan patroli dari kas non-karbon, yaitu semua patroli yang juga ada di S1.

**Pemeriksaan:**

1. **Tidak ada double counting antar-indikator.** Kredit BAU dan kredit konservatif adalah **dua varian alternatif** dari variabel yang sama, bukan dua aliran kredit. Dilaporkan berdampingan, bukan dijumlahkan.
2. **Pendekatan ini aproksimasi, bukan selisih antar-run.** Porsi dihitung di dalam run S2 dari dua komponen efek, sedangkan stok hutan S2 dan S1 sudah berbeda. Efek juga bekerja secara multiplikatif dengan efek penghidupan dan kebakaran. Karena itu kredit konservatif ≈ (S1 − S2) × faktor eligible, tetapi tidak persis sama. Dilaporkan sebagai batas bawah, dan dibandingkan dengan no. 2 × faktor eligible (U16).
3. **Patroli historis 2024–2025.** Dalam varian konservatif, efeknya tidak dikreditkan karena juga ada di S1. Dalam varian BAU, efeknya dikreditkan. Patroli ini dibiayai mitra proyek karbon yang sama, jadi secara proyek ia aktivitas proyek. Tetapi karena juga terjadi di S1, perlakuannya adalah **pilihan metodologis**, bukan fakta.
4. **Additionality.**
   - SK 24 HD terbit 2017–2020, sebelum proyek karbon.
   - Patroli sudah didukung mitra sejak 2023.
   - S1 mengasumsikan patroli berlanjut tanpa karbon.
   - Bila S1 benar, sebagian kredit BAU tidak memenuhi uji additionality. Varian konservatif menunjukkan seberapa besar kredit yang tersisa bila hanya mitigasi di atas S1 yang dihitung.
   - Kedua varian harus disajikan bersama, dengan pernyataan bahwa uji additionality standar karbon tidak dimodelkan.
5. **ARR (perlu diperbaiki, C3).**
   - Di A1, `Pengurangan Emisi ARR Bruto` = seluruh serapan di atas baseline. Baseline tanpa penanaman, jadi rehabilitasi non-karbon S1 ikut dikreditkan.
   - Varian konservatif membatasi ARR pada porsi penanaman yang didanai kas karbon (`Porsi ARR Adisional`).
   - Porsi ini berbasis aliran tanam, padahal serapan tertunda bertahun-tahun. Aproksimasi kelas B.
6. **Harga ARR (catatan).** `Harga Karbon Removal` tetap USD 20 di semua harga REDD. Variasi USD 6–35 tidak berlaku untuk ARR. Ini **dipertahankan dari A1**, tetapi harus ditulis di Metode. Alternatifnya, disamakan dengan harga REDD bila peneliti menghendaki.
7. **`Faktor Rekonsiliasi Reversal Kredit A2`.** Faktor ini dulu dikalibrasi per harga (0,72–0,76) agar cocok dengan hasil lain. Diusulkan **ditetapkan 1**, karena kalibrasi per harga tidak punya dasar fisik.

---

## 4. Jeda kas karbon

| Tahap | Persamaan | Waktu |
|---|---|---|
| Penurunan emisi terjadi | `Kredit REDD Diajukan` (aliran) | mulai 2024 (`Tahun Mulai Karbon`) |
| Verifikasi dan penerbitan | `DELAY FIXED(Diajukan, 3, 0)` | kredit pertama terbit 2027 |
| Penjualan | inventori × 0,7/th | mulai 2027 |
| Pembayaran (baru) | `Kas Penjualan Kredit = IF jeda>0 THEN DELAY FIXED(Pendapatan Kotor, jeda, 0) ELSE Pendapatan Kotor` | jeda 0 / 0,5 / 1 th |
| Kas ke LPHD | 60 % × (kas − biaya − pemulihan) | sejak kas pertama |
| Belanja kegiatan | `Dana Desa Tersedia = Saldo/1 th`, dibatasi saldo | tidak ada belanja sebelum saldo > 0 |

**Sensitivitas kas pertama:**
- `Delay Verifikasi` = 3 / 4 / 5 menghasilkan kas pertama ±2027 / 2028 / 2029.
- Dikombinasikan dengan jeda pembayaran 0 / 0,5 / 1.

**Catatan B:** penerbitan di model kontinu, bukan per peristiwa verifikasi lima tahunan. Penerbitan berkala akan membuat kas tersendat dan lebih terlambat. Ini keterbatasan, tidak diubah.

---

## 5. Peta arus keuangan (S2)

| Arus | Variabel | Ditanggung / diterima | Masuk NPV |
|---|---|---|---|
| Investasi: pembiayaan awal 2024–2025 (estimasi biaya patroli) | `Realisasi Pembiayaan Awal` Rp 1,44 miliar | mitra | Proyek keseluruhan, mitra |
| Investasi: biaya pengembangan proyek (PDD, validasi, registrasi) | `Biaya Pengembangan Proyek` (baru, default 0) | mitra | Proyek, inkremental, mitra |
| Biaya MRV: monitoring | 111.123 ha × Rp 1.980 = Rp 220 juta/th sejak 2024 | proyek (didahului mitra) | Proyek, inkremental |
| Biaya MRV: verifikasi | Rp 742,5 juta/5 th = Rp 148,5 juta/th sejak 2027 | idem | idem |
| Biaya penerbitan | USD 0,25/kredit terbit | idem | idem |
| Biaya transaksi dan pajak | (0,22 % + 5 %) × kas penjualan | dipotong dari kas | idem |
| Pembayaran kredit | `Kas Penjualan Kredit` | proyek | Proyek, inkremental |
| Talangan biaya sebelum kas cukup | `Kekurangan Biaya Bersama Ditanggung Mitra` (keluar), `Pemulihan Defisit Biaya Bersama` (masuk) | mitra | Mitra (bukan proyek: arus internal) |
| Pemulihan pembiayaan awal (bila talangan) | `Pemulihan Pendanaan Awal`, dipotong **sebelum** bagi hasil | mitra menerima | Mitra (bukan proyek: arus internal) |
| Transfer bagi hasil 60 % | `Dana Program PS dari Karbon` → `Saldo Dana LPHD` | LPHD | Kecukupan LPHD (bukan NPV proyek) |
| Transfer bagi hasil 40 % | `Dana Mitra dari Karbon` | mitra | Mitra |
| Belanja kegiatan LPHD | `Penggunaan Dana Pengelolaan` | LPHD | **Tidak** masuk NPV proyek: ini penggunaan bagian 60 % |

**Siapa menanggung biaya sebelum penjualan menghasilkan kas** (S2, 2024–2027): mitra. Rinciannya:
- monitoring sejak 2024 dan verifikasi sejak 2027, melalui `Kekurangan Biaya Bersama Ditanggung Mitra`, dipulihkan dari surplus kemudian;
- pembiayaan awal 2024–2025;
- biaya pengembangan proyek.

LPHD tidak menanggung biaya karbon apa pun dan tidak menerima kas sebelum ada surplus.

---

## 6. Persamaan NPV (di dalam model; diskonto kontinu per DT)

`Faktor Diskonto = 1/((1+Tingkat Diskonto*Satu Tahun)^((Time−INITIAL TIME)/Satu Tahun))`, dengan diskonto 10 % (D, tidak bersumber).

| Ukuran | Persamaan arus (Rp/th) | S1 | S2 |
|---|---|---|---|
| **NPV proyek keseluruhan** | `Kas Penjualan − Biaya Transaksi dan MRV − Biaya Pengembangan − Realisasi Pembiayaan Awal` | −PV(pembiayaan awal) | penuh |
| **NPV inkremental perdagangan karbon** | `Kas Penjualan − Biaya Transaksi dan MRV − Biaya Pengembangan` | 0 | = NPV proyek(S2) − NPV proyek(S1) |
| **NPV mitra** | `Dana Mitra + Pemulihan Defisit + Pemulihan Pendanaan Awal − Kekurangan Biaya Bersama − Realisasi Pembiayaan Awal − Biaya Pengembangan` | −PV(pembiayaan awal) | penuh |
| **Kecukupan LPHD** | PV(`Dana Desa Diterima`) vs PV(`Kebutuhan Dana Minimum`); `Rasio Cakupan` tahunan; `Kesenjangan Pembiayaan Minimum` tahunan | kas non-karbon saja | + kas karbon |

**Identitas tanpa double counting (dibuktikan dari persamaan).** Misalkan S = MAX(0, Kas − B), K = MAX(0, B − Kas), Rd = pemulihan defisit, Rp = pemulihan pembiayaan awal, dan D = S − Rd − Rp.
- Arus mitra = 0,4 D + Rd + Rp − K − F − Dev.
- Arus LPHD = 0,6 D.
- Jumlahnya = S − K − F − Dev = (Kas − B) − F − Dev = **arus proyek keseluruhan**.
- Jadi NPV proyek = NPV mitra + PV kas karbon LPHD, untuk setiap status talangan.

Ini diuji sebagai identitas numerik di U15.

**Perbedaan dengan NPV lama:**
- NPV lama mengurangkan belanja LPHD sebagai biaya, padahal belanja itu adalah penggunaan bagian 60 %. Akibatnya NPV lama lebih rendah daripada NPV proyek keseluruhan yang konsisten.
- Harga impas akan berubah karena definisi. Perubahan ini harus dijelaskan dan tidak disajikan sebagai "perbaikan hasil".

**Hibah vs talangan (C2):**
- Hibah (status 0): pembiayaan awal adalah biaya mitra tanpa pengembalian.
- Talangan (status 1): pembiayaan awal dipulihkan dari surplus sebelum bagi hasil. Bagian LPHD berkurang dan NPV mitra naik. NPV proyek keseluruhan tidak berubah.
- Pada model lama, "talangan" dipulihkan dari bagian 40 % mitra sendiri. Ini tidak bermakna ekonomi, sehingga diperbaiki.
- Status aktual belum diketahui (D). Kedua varian dijalankan (U15).

---

## 7. Ringkasan status

| Komponen | Status |
|---|---|
| Baseline BAU dibedakan dari S1 | konsisten; dipertahankan |
| Lima indikator terpisah | siap; definisi di atas |
| Varian konservatif REDD | siap sebagai sensitivitas; aproksimasi (B) |
| Varian konservatif ARR | usulan baru; aproksimasi (B) |
| Harga ARR tetap USD 20 | perlu keputusan peneliti |
| Jeda kas | siap; nilai perlu sensitivitas |
| NPV 4 ukuran + identitas | siap; diskonto (D) dan biaya pengembangan (perlu data) |
| Status hibah/talangan | perlu data; dua varian |
