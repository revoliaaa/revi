# Final Gate Sebelum Implementasi: Model Dua Skenario

**Status pekerjaan:** audit desain.
- **Berkas `.mdl` tidak diubah** (md5 `5af5a34e…` tetap) dan **tidak ada simulasi**.
- Semua bukti di bawah berasal dari penelusuran teks persamaan, identitas aljabar, dan pemeriksaan dimensional otomatis atas persamaan model ditambah rancangan (`skrip/fase1b/usulan.py`).

**Alat pemeriksaan (statis, tanpa simulasi):**
- `cek_statis.py`: referensi tak dikenal, loop aljabar (komponen terhubung kuat, Tarjan), dan pemakai `Switch Karbon`.
- `cek_satuan.py`: dimensi diturunkan dari satuan deklarasi tiap masukan.
  - Aturan: `+ − MIN MAX IF` harus sama satuan; `INTEG` aliran = stok/Year; argumen waktu `STEP`, `SMOOTHI`, dan `DELAY` = Year; argumen `EXP` tak berdimensi.
  - Literal angka dianggap tak berdimensi (wildcard). Ini keterbatasan alat.
- **Uji negatif pemeriksa:** empat persamaan yang sengaja salah semuanya tertangkap, yaitu Rp + Rp/Year, HOK × orang sebagai Rp/Year, stok dengan aliran Rp, dan `EXP(Time)`.

| Pemeriksaan | Hasil |
|---|---|
| Referensi ke variabel yang tidak ada (model + 163 persamaan rancangan) | **0** |
| Loop aljabar | **0** |
| Konsistensi dimensional: model saat ini (787 persamaan) | **787/787 konsisten** |
| Konsistensi dimensional: persamaan rancangan | **163/163 konsisten** |
| Pemakai `Switch Karbon` | `Kredit REDD/ARR/Gambut Diajukan`, `Biaya Monitoring MRV`, `Biaya Verifikasi Tahunan`, `Biaya Pengembangan Proyek Efektif`, `Pendanaan Awal Proyek Karbon` (besaran 0). **Tidak ada kegiatan PS** |

> Catatan proses: pada putaran pertama pemeriksaan, nama variabel pertama di berkas terbaca dengan awalan header `{UTF-8}`. Galat parser ini sudah diperbaiki di keempat skrip, dan semua pemeriksaan dijalankan ulang.

---

## A. Koreksi wajib

### A1. K3: patroli historis 2.533 / 3.011 HOK (G1)

**Persamaan bermasalah (rancangan Fase 1B):**
- `Pendanaan Awal untuk Patroli = MIN(Pendanaan Awal Proyek Karbon, Hari Patroli Tambahan Dibutuhkan*Biaya per Hari Patroli)` tetap tersambung ke 7 variabel. Itu adalah jalur pembiayaan awal kedua yang hanya bernilai 0 karena `Besaran` = 0.
- `Hari Patroli Tambahan Dibutuhkan` aktif pada 2024–2025. Bila kas non-karbon diberi nilai mulai 2024, model dapat "membeli" patroli di atas 2.533/3.011 HOK, padahal angka itu adalah **total** patroli tahun tersebut.
- `Manfaat Kolektif Non Tunai` hanya mengurangkan upah dari kas karbon. Upah dari kas non-karbon terhitung sebagai manfaat kolektif non-tunai, padahal sudah dibayar sebagai upah.

**Perbaikan:**
```
Pendanaan Awal untuk Patroli = 0                     ~ Rupiah/Year  (jalur generik diputus; variabel dipertahankan untuk sketch)
Hari Patroli Didanai Kas LPHD = Realisasi Belanja Perlindungan/Biaya per Hari Patroli          ~ HOK/Year
Hari Patroli Tambahan Dibutuhkan = Switch PS*Periode Pasca Pembiayaan Awal
       *MAX(0, MIN(Hari Patroli Target, Kapasitas Hari Patroli Anggota)-HOK Patroli Reguler PS)  ~ HOK/Year
Kebutuhan Dana Perlindungan = Hari Patroli Tambahan Dibutuhkan*Biaya per Hari Patroli            ~ Rupiah/Year
Upah Dibayar dari Kas LPHD = Upah Patroli dari Kas LPHD+Upah Pengendalian Kebakaran+Upah Penanaman Didanai Karbon
Manfaat Kolektif Non Tunai = MAX(0, Penggunaan Dana Pengelolaan-Upah Dibayar dari Kas LPHD)
Upah Kegiatan Didanai Karbon = Upah Dibayar dari Kas LPHD*Porsi Kas Karbon dalam Saldo
```

**Jejak aliran 2.533 HOK (2024).** Pola yang sama berlaku untuk 3.011 HOK pada 2025.

| Tujuan | Persamaan | Masuk | Dihitung |
|---|---|---|---|
| Aktivitas | `Hari Patroli Pembiayaan Awal` = 2.533 | 1× | `Hari Patroli Didanai = Pembiayaan Awal + Kas LPHD`; `HOK Patroli Reguler PS` = 0 karena `Periode Pasca` = 0; `Kas LPHD` = 0 karena `Kebutuhan Dana Perlindungan` = 0 pada 2024–2025 |
| Intensitas | `(Reguler + Didanai)/7.996` = (0 + 2.533)/7.996 = 0,317 | 1× | `Indeks … Tanpa Karbon` memakai 2.533 juga, tetapi sebagai **indikator alternatif** untuk varian kredit konservatif, bukan penjumlah intensitas |
| Biaya (investasi mitra) | `Realisasi Pembiayaan Awal = 2.533 × Rp 260.000` = Rp 658,58 juta | 1× | Masuk `Arus Kas Proyek Keseluruhan` dan `Arus Kas Mitra` sebagai −F. **Tidak** masuk `Penggunaan Dana Pengelolaan` atau saldo LPHD |
| Upah (pendapatan RT) | `Upah Patroli Berbayar = Hari Patroli Didanai × Rp 130.000` = Rp 329,29 juta | 1× | Bagian dari Rp 260.000 per HOK. Biaya pembayar dan pendapatan penerima adalah dua sudut pandang, tidak dijumlahkan dalam ukuran yang sama |
| Kebutuhan dan kesenjangan | `Hari Patroli Tambahan Dibutuhkan` = 0 pada 2024–2025; `Kesenjangan = MAX(0, Kebutuhan − Penggunaan)` | 0× | Pembiayaan awal tidak lagi dikurangkan dua kali (tidak di HOK dan tidak di rupiah) |
| Upah karbon | `Upah Kegiatan Didanai Karbon` hanya dari kas LPHD × porsi karbon | 0× | Patroli historis bukan upah karbon |

**Identitas (U3, U17):**
- `Total HOK Patroli = Hari Patroli Pembiayaan Awal + HOK Patroli Reguler PS + Hari Patroli Didanai Kas LPHD`
- `Check Identitas Patroli = Total HOK Patroli − (HOK Patroli Reguler PS + Hari Patroli Didanai)` = 0
- Pada 2024: total = 2.533; pada 2025: total = 3.011; kumulatif biaya = Rp 1.441.440.000.

### A2. C2: hibah dan talangan (G2)

**Persamaan bermasalah (Fase 1B):**
```
Pendanaan Awal Belum Terpulihkan = INTEG(Pendanaan Awal untuk Patroli + Realisasi Pembiayaan Awal*Status
                                         + Biaya Modal Pendanaan Awal Rp − Pemulihan, 0)
```
`Pendanaan Awal untuk Patroli` masuk ke pokok **tanpa** dikali `Status`. Pada status hibah, jalur ini (bila nonzero) tetap menjadi piutang yang dipulihkan.

**Perbaikan:**
```
Pendanaan Awal Belum Terpulihkan = INTEG((Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal)*Status Pembiayaan Awal
                                         +Biaya Modal Pendanaan Awal Rp-Pemulihan Pendanaan Awal, 0)        ~ Rupiah
Biaya Modal Pendanaan Awal Rp = Pendanaan Awal Belum Terpulihkan*Biaya Modal Pendanaan Awal               ~ Rupiah/Year (A1; tarif 0, D)
Pemulihan Pendanaan Awal = MIN(MAX(0, Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama),
                               Pendanaan Awal Belum Terpulihkan/TIME STEP)                                ~ Rupiah/Year
Pokok Talangan Kumulatif = INTEG((Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal)*Status Pembiayaan Awal, 0)
Biaya Modal Kumulatif    = INTEG(Biaya Modal Pendanaan Awal Rp, 0)
Pemulihan Kumulatif      = INTEG(Pemulihan Pendanaan Awal, 0)
```

**Bukti:**
- **Hibah** (`Status` = 0): aliran masuk pokok = 0. Biaya modal = 0 × tarif = 0. Stok tetap 0, sehingga `Pemulihan` = MIN(·, 0/TIME STEP) = 0. **Pemulihan pokok = 0.**
- **Talangan** (`Status` = 1): stok(t) = pokok kumulatif + biaya modal kumulatif − pemulihan kumulatif. Pemulihan per langkah ≤ stok/TIME STEP, sehingga stok ≥ 0. Karena itu **pemulihan kumulatif ≤ pokok + biaya modal** (U15).
- Biaya modal hanya timbul atas saldo yang belum pulih, dengan tarif `Biaya Modal Pendanaan Awal` (default 0, D). Ini satu-satunya tambahan di atas pokok yang sah.
- Pemulihan dibayar dari surplus **sebelum** bagi hasil 60/40, setelah defisit biaya bersama dipulihkan. Pada A1, pemulihan diambil dari bagian 40 % mitra sendiri. Itu kesalahan konseptual: mitra membayar dirinya sendiri.
- Dalam S1 tidak ada surplus, sehingga talangan tidak pernah pulih dan secara ekonomi menjadi hibah. Ini dilaporkan.

### A3. K4–K5: neraca LPHD (G3)

**Pembatas agregat.**
- Mode alokasi tetap: `Alokasi_i = MIN(Dana Desa Tersedia × Proporsi_i, Kebutuhan_i)`. Proporsi: operasional 0,10 + perlindungan 0,30 + rehabilitasi 0,15 + kelembagaan 0,15 + KUPS 0,20 + kebakaran 0,10 = **1,00**. Jadi Σ alokasi ≤ `Dana Desa Tersedia`.
- Mode berbasis kebutuhan: alokasi prioritas dihitung berurutan dari `Dana Pengelolaan Tersedia`, dengan setiap pos dikurangi pos sebelumnya. Σ ≤ dana tersedia.
- Model eksperimen alokasi: `Dana Fleksibel = Tersedia − Op − Kelembagaan`, dan porsi B0–R2 masing-masing berjumlah 1 (R1: 0,4 + 0,2 + 2/15 + 1/15 + 0,2 = 1). Kompensasi masuk `Penggunaan Dana Desa`.
- Realisasi = alokasi × rasio realisasi (≤ 1). Sisa tetap di saldo.
- **Pemeriksa baru:** `Jumlah Proporsi Alokasi Efektif` (harus ≤ 1) dan `Check Neraca Dana LPHD = Saldo − (Σ masuk − Σ guna)` (harus 0).

**Satuan dan TIME STEP:**
- `Saldo` [Rp]; `Dana Desa Tersedia = Saldo/Waktu Pembelanjaan` [Rp/Year], dengan waktu pembelanjaan = 1 Year.
- Euler: Saldo(t + DT) = Saldo + (Masuk − Guna)·DT, dengan Guna ≤ Saldo/1 Year. Maka Saldo(t + DT) ≥ Saldo·(1 − DT/1 Year) ≥ 0 **selama DT ≤ Waktu Pembelanjaan** (0,0625 ≤ 1 ✓). Syarat ini dicatat untuk uji DT.
- Pelacak `Saldo Dana LPHD dari Karbon`: keluar = Guna × S_K/S ≤ S_K/1 Year, sehingga S_K ≥ 0. Dengan cara yang sama, S − S_K ≥ 0. Jadi 0 ≤ S_K ≤ S.
- **Tidak ada penggunaan saldo di luar `Penggunaan Dana Desa`** (hasil jejak: pemakai `Saldo Dana LPHD` hanya `Dana Desa Tersedia` dan `Porsi Kas Karbon`).
- **Perbaikan tambahan (G5):** belanja rehabilitasi kini dicatat sebesar kas yang benar-benar keluar, bukan alokasi (lihat A5).

### A4. K7: modal KUPS (G4)

**Kesalahan baru yang ditemukan pada rancangan Fase 1B:** `Penggantian KUPS Berbasis Modal` (yang mengurangi modal) aktif sejak 2024, padahal sebelum `Tahun Akhir Data KUPS` (2026) `Penambahan KUPS` memakai data historis dan mengabaikan penggantian. Akibatnya modal berkurang tanpa ada KUPS yang diganti.

**Perbaikan:**
```
Penggantian KUPS Berbasis Modal = IF THEN ELSE(Time < Tahun Akhir Data KUPS, 0,
       MIN(KUPS Menjadi Tidak Aktif, Modal Usaha KUPS/TIME STEP/Biaya Reaktivasi KUPS))     ~ Unit/Year
```

**Identitas yang diturunkan dari persamaan A1 dan rancangan:**
```
(1) Penjualan KUPS = Biaya Operasional KUPS Implisit + Manfaat Ekonomi KUPS              [definisi A1: biaya implisit = penjualan − surplus]
(2) Manfaat Ekonomi KUPS (surplus) = Pendapatan KUPS Total + Laba KUPS Ditahan            [definisi A1: laba ditahan = surplus − bagian anggota]
(3) Laba KUPS Ditahan = Akumulasi Modal KUPS + Laba Ditahan Tidak Direinvestasi           [rancangan]
(4) d(Modal Usaha KUPS)/dt = Akumulasi Modal KUPS − Penggunaan Modal KUPS
(5) Penggunaan Modal KUPS = Penggantian KUPS Berbasis Modal × Biaya Reaktivasi KUPS
```

- **Laba ditahan tidak dipakai di tempat lain.** Hasil jejak: `Laba KUPS Ditahan` hanya dipakai `Akumulasi Modal KUPS`.
- **Bagian anggota** (`Pendapatan KUPS Total` = 26,3 % surplus) satu-satunya yang masuk pendapatan RT, melalui `Tambahan Pendapatan KUPS di Atas 2024`.
- **Pembentukan KUPS dari kas LPHD** dibiayai `Realisasi Belanja Pengembangan KUPS`, bukan dari modal. Jadi tidak ada dua sumber untuk satu KUPS.
- **Pemeriksa:** `Check Identitas Surplus KUPS` = (2) − (3) = 0; `Check Identitas Penjualan KUPS` = (1) = 0.

### A5. K9: rehabilitasi mengikuti luas aktual (G5)

**Persamaan bermasalah:**
- `Penanaman Didanai Karbon = MIN(Dana Penanaman/Biaya per Ha, Target, sisa restorasi eligible)` **tidak** dibatasi luas nonhutan maupun sisa target RKPS.
- Ketika `Penambahan Luas Penanaman` dipotong batas lahan:
  - kas tetap tercatat terbelanjakan (`Penggunaan Dana Pengelolaan` memakai `Realisasi Belanja Rehabilitasi` penuh);
  - stok `Luas Tanam Didanai Karbon` dan upahnya memakai luas rencana, bukan aktual.

**Perbaikan:**
```
Batas Luas Penanaman = MIN(Target Penanaman, MIN(MAX(Target Total Penanaman RKPS−Luas Penanaman Program,0)/TIME STEP,
                                                  NonHutan*Fraksi Maksimum NonHutan Ditanami per Tahun))          ~ Ha/Year
Kebutuhan Dana Rehabilitasi = Switch PS*(MAX(0, MIN(Batas Luas Penanaman−Penanaman Non Karbon,
                         MAX(0, Luas Restorasi Selektif Eligible−Luas Tanam Didanai Karbon)/TIME STEP))*Biaya Penanaman per Ha
                         + Areal Rehabilitasi Belum Berhutan*Biaya Pemeliharaan Tanaman per Ha per Tahun)              ~ Rupiah/Year
Penanaman Rencana Total = Penanaman Non Karbon + Penanaman Didanai Karbon
Penambahan Luas Penanaman = Switch Rehabilitasi*(1−Periode Historis)*MIN(Penanaman Rencana Total, Batas Luas Penanaman)
Fraksi Penanaman Terealisasi = MIN(1, ZIDZ(Penambahan Luas Penanaman, Penanaman Rencana Total))
Penanaman Non Karbon Aktual = Penanaman Non Karbon × Fraksi ;  Penanaman Didanai Kas Aktual = Penanaman Didanai Karbon × Fraksi
Pengeluaran Kas Penanaman Aktual = Penanaman Didanai Kas Aktual × Biaya Penanaman per Ha
Realisasi Belanja Rehabilitasi Efektif = Dana Pemeliharaan Rehabilitasi + Pengeluaran Kas Penanaman Aktual
Penggunaan Dana Pengelolaan = … + Realisasi Belanja Rehabilitasi Efektif + …           (sisa dana tanam tetap di saldo)
Luas Tanam Didanai Karbon, Luas Tanaman Karbon dalam Pemeliharaan, Upah Penanaman Didanai Karbon, HOK Penanaman Didanai Kas → memakai Penanaman Didanai Kas Aktual
Nilai Dukungan Material Non Karbon Terpakai = Penanaman Non Karbon Aktual × Biaya Bibit dan Material per Ha     (bukan kas LPHD)
Upah Penanaman Program Non Karbon = HOK Penanaman Non Karbon × Porsi Dibayar × Upah per HOK                   (dibayar program, bukan kas LPHD)
```

**Pemisahan empat jenis arus rehabilitasi:**

| Arus | Variabel | Sumber | Masuk kas LPHD | Masuk pendapatan RT |
|---|---|---|---|---|
| Dukungan material (bibit, logistik, alat) | `Nilai Dukungan Material Non Karbon Terpakai` | program non-karbon (data) | tidak | tidak |
| Kas penanaman (tenaga + material) | `Pengeluaran Kas Penanaman Aktual` | saldo LPHD | ya | upahnya ya (`Upah Penanaman Didanai Karbon`) |
| Upah penanaman non-karbon | `Upah Penanaman Program Non Karbon` | program non-karbon | tidak | ya, hanya bila porsi dibayar > 0 |
| Pemeliharaan | `Dana Pemeliharaan Rehabilitasi` | saldo LPHD | ya | tidak (tenaga pemeliharaan tidak dipisah: **B**) |

**Identitas:**
- `Check Identitas HOK Penanaman = HOK Penanaman − (HOK Didanai Kas + HOK Non Karbon)` = 0. Ini berlaku karena `HOK Penanaman = Penambahan × 85` dan `Penambahan = Non Aktual + Kas Aktual`.

**Loop.** `Penggunaan ← Pengeluaran Aktual ← Fraksi ← Penambahan ← Penanaman Didanai ← Dana Penanaman ← Realisasi ← Alokasi ← Dana Desa Tersedia (stok)`. Tidak ada loop; hasil Tarjan sama.

### A6. C4: NPV dan kecukupan LPHD (G6)

**Perbaikan:** `Biaya Pengembangan Proyek Efektif = Biaya Pengembangan Proyek × Switch Karbon`, sehingga biaya pengembangan proyek karbon tidak muncul di S1 dan NPV inkremental S1 tetap 0.

**Definisi** (diskonto per DT; `Faktor Diskonto = (1 + r)^−(t − 2024)`):

| Ukuran | Arus | Isi |
|---|---|---|
| NPV finansial proyek keseluruhan | `Arus Kas Proyek Keseluruhan` = Kas − B − Dev − F | Investasi (F, Dev) + biaya karbon (B) + pembayaran kredit (Kas) |
| NPV inkremental S2 − S1 | `Arus Kas Proyek Karbon` = Kas − B − Dev | F sama di S1 dan S2, sehingga hilang |
| NPV mitra | 0,4·D + Rd + Rp − K − F − Dev | Transfer 40 % + pemulihan − talangan biaya − investasi |
| Kecukupan LPHD | PV(`Dana Desa Diterima`), PV(`Penggunaan Dana Desa`), PV(`Kebutuhan Dana Minimum`), rasio cakupan dan kesenjangan tahunan | Transfer 60 % dan kas non-karbon vs kebutuhan |

Notasi: B = `Biaya Transaksi dan MRV` (monitoring + verifikasi + penerbitan + transaksi + pajak); S = MAX(0, Kas − B); K = MAX(0, B − Kas); Rd = pemulihan defisit; Rp = pemulihan talangan; D = S − Rd − Rp.

**Identitas akuntansi (dibuktikan aljabar, diuji numerik U15):**
```
Arus Mitra + Kas LPHD Karbon = 0,4D + Rd + Rp − K − F − Dev + 0,6D
                             = D + Rd + Rp − K − F − Dev
                             = S − K − F − Dev                      (karena D = S − Rd − Rp)
                             = (Kas − B) − F − Dev                  (karena S − K = Kas − B untuk MAX/MAX komplementer)
                             = Arus Kas Proyek Keseluruhan  ✓
NPV Proyek Keseluruhan(S2) − NPV Proyek Keseluruhan(S1) = PV(Kas − B − Dev) = NPV Inkremental  ✓  (F identik di S1 dan S2)
```

`Check Identitas Arus Kas` = 0 setiap langkah, untuk hibah maupun talangan.

**Yang tidak dihitung ganda dan tidak hilang:**
- **Pengeluaran kegiatan LPHD** (`Penggunaan Dana Desa`) adalah penggunaan transfer 60 %. Ia **tidak** dikurangkan lagi dari NPV proyek; NPV lama melakukannya. Pengeluaran ini dilaporkan sebagai PV tersendiri (`PV Penggunaan Dana LPHD`), sehingga tidak hilang dari laporan.
- **Upah** adalah bagian dari biaya kegiatan, bukan biaya tambahan.
- **Kontribusi non-tunai, dukungan material, dan upah program non-karbon** dilaporkan sebagai PV terpisah. Ketiganya tidak masuk NPV proyek karena bukan arus kas proyek karbon.
- **Biaya sebelum kas:** monitoring (sejak 2024), verifikasi (sejak 2027), penerbitan, F, dan Dev ditanggung mitra. Monitoring dan verifikasi melewati `Kekurangan Biaya Bersama Ditanggung Mitra` dan dipulihkan dari surplus berikutnya. LPHD tidak menanggung biaya karbon.

---

## B. Temuan material tambahan

| No | Temuan | Perbaikan | Kelas |
|---|---|---|---|
| T1 | `Manfaat Kolektif Non Tunai` hanya mengurangkan upah karbon | Kurangi semua upah dari kas LPHD (G1) | A (dikoreksi) |
| T2 | Modal KUPS terpakai selama periode data (bug rancangan Fase 1B) | Gerbang waktu (G4) | A (dikoreksi) |
| T3 | Kas penanaman dan stok tanam karbon memakai luas rencana | Luas aktual (G5) | A (dikoreksi) |
| T4 | Biaya pengembangan akan muncul di S1 | × `Switch Karbon` (G6) | A (dikoreksi) |
| T5 | `Anggota Patroli Didanai Karbon = Hari Patroli Didanai/24` memakai norma 24 HOK/orang, berbeda dari 11,85 HOK/orang di K1/K13. `Penerima Manfaat Penanaman Aktif` memasukkan penanam sukarela | Dicatat; hanya memengaruhi jangkauan program (`Jangkauan Program ke RT Bergantung` → efek penghidupan, sensitivitas = 0) | B, tidak diubah |
| T6 | Tenaga pemeliharaan tanaman tidak dipisah dari biaya pemeliharaan | Dicatat. Upah pemeliharaan tidak dihitung ke pendapatan RT (konservatif) | B |
| T7 | `Indeks Intensitas Swadaya 2023` (0,2251; basis 1.568/6.966) berbeda dari basis K14 (2.160/7.996 = 0,270) | Hanya dipakai oleh `Koreksi Kontrafaktual Hutan S1` (switch 0, tidak aktif). Diberi komentar | C (tidak berdampak) |
| T8 | Penerbitan kredit kontinu, bukan per verifikasi 5 tahunan | Keterbatasan; kas nyata lebih tersendat | B |
| T9 | `Harga Karbon Removal` (ARR) tetap USD 20 | Keputusan peneliti | D |

---

## C. Parameter tanpa dukungan empiris

**Hanya dapat dibenarkan sebagai sensitivitas:**
- `Tingkat Keberlanjutan Patroli Reguler` (0–1);
- `Laju Penurunan Partisipasi Sukarela`;
- `Proporsi Penggantian Anggota Patroli` (varian 0,625);
- `Porsi Laba Ditahan untuk Reinvestasi`;
- `Biaya Reaktivasi KUPS`;
- `Laju Pembelajaran Kelembagaan`;
- `Delay Pembayaran Penjualan`; `Delay Verifikasi` (varian 4/5);
- `Tingkat Diskonto`; `Biaya Modal Pendanaan Awal`;
- norma kebutuhan patroli (12 HOK, 4 orang, 750 ha);
- `Rasio Risiko Penempatan` 0,651;
- efektivitas 0,37 dan waktu penyesuaian 3 tahun.

**Menunggu data (default 0 hanya penanda):**
- `Dana Operasional Non Karbon Tunai`;
- `Dukungan Material Rehabilitasi Non Karbon`;
- `Porsi Tenaga Penanaman Non Karbon Dibayar`;
- `Nilai Pendampingan Kelembagaan Non Tunai`;
- `Status Pembiayaan Awal`;
- `Biaya Pengembangan Proyek`;
- satuan Rp 260.000 (per orang-hari atau per regu-hari);
- apakah patroli 2024–2025 berupah;
- roster 254;
- data KUPS 2024–2025.

Rincian ada di `REGISTER_PARAMETER_DAN_SUMBER.md`.

---

## D. Kriteria lulus/gagal

Kriteria lengkap ada di `RENCANA_UJI_FASE2.md` (revisi gate). Satu uji gagal pada kelompok **struktural** (U0–U4, U7, U10, U11, U15–U18) menghentikan Fase 3 sampai diperbaiki.

---

## E. Daftar perubahan yang akan diterapkan ke model

Diterapkan pada **salinan baru** (`DKP_25HD_FINAL_2SKENARIO.mdl` dan `DKP_25HD_FINAL_2SKENARIO_ALOKASI.mdl`). Model 3 skenario dan A1 rekonstruksi tidak ditimpa.

1. **Konfigurasi (S-1 sampai S-5).** `Skenario Kebijakan`; `Switch PS`, `Switch Rehabilitasi`, dan `Switch Pendanaan Awal` = 1; `Switch Karbon` = (Skenario = 2).
2. **Patroli (K1, K2, G1, G7).** Patroli reguler pasca-2025 dengan basis roster 254; penggantian 1; rekrutmen tanpa `Switch Karbon`; patroli historis dikunci pada data; jalur pendanaan awal generik = 0; identitas HOK patroli.
3. **Intensitas dan kebutuhan (K3).** Intensitas total dan tanpa karbon; kesenjangan tanpa pengurangan ganda.
4. **Belanja LPHD (K4, K8).** Tujuh alokasi tanpa `Switch Karbon`, ditambah tiga kegiatan didanai kas dan kompensasi di model alokasi.
5. **Kas LPHD (K5, G3).** Dua aliran masuk, stok pelacak karbon, pemeriksa proporsi, dan neraca.
6. **Kelembagaan (K6).** Dari semua sumber, ditambah pembelajaran.
7. **KUPS (K7, G4).** Modal usaha dari laba ditahan, reaktivasi setelah 2026, dan identitas surplus serta penjualan.
8. **Rehabilitasi (K9, G5).** Material dan tenaga dipisah; batas luas; luas, kas, upah, dan stok memakai luas aktual.
9. **Akuntansi kegiatan (K10–K13, K16–K17).** Biaya non-karbon sebagai indikator, kontribusi non-tunai, kerja berupah dan sukarela, partisipasi aktif, atribusi upah karbon, dan agregat manfaat.
10. **Inisialisasi (K14, K15).** SMOOTHI dari 2023; acuan `INITIAL`.
11. **Kas karbon (C1).** Jeda pembayaran; transaksi dan pajak berbasis kas.
12. **Talangan (C2, G2).** Pokok × status; pemulihan sebelum bagi hasil; tiga pelacak.
13. **Kredit (C3).** Varian konservatif REDD dan ARR; faktor rekonsiliasi = 1.
14. **Keuangan (C4, G6).** NPV keseluruhan, inkremental, mitra, PV per komponen, dan identitas arus kas; biaya pengembangan hanya S2.
15. **Indikator karbon (C5).** Indikator terpisah.

Seluruh persamaan final (163) ada di `FASE1B_MATRIKS_PERSAMAAN_FINAL.md`, yang dihasilkan langsung dari `skrip/fase1b/usulan.py` agar tidak ada salah salin saat implementasi.

---

## F. Keputusan

### **SIAP BERSYARAT**

**Alasan siap:**
- Struktur persamaan konsisten secara statis dan dimensional: 0 referensi tak dikenal, 0 loop aljabar, 163/163 dan 787/787 konsisten.
- Uji negatif membuktikan pemeriksa bekerja.
- Ke-6 koreksi wajib dan 4 temuan material tambahan sudah punya persamaan perbaikan dengan identitas akuntansi atau jejak aliran.
- Tidak ada perubahan pada parameter ekologis atau struktur yang tidak bermasalah.

**Syarat sebelum implementasi dapat dianggap final:**
1. **Persetujuan peneliti atas daftar perubahan bagian E.**
2. **Implementasi boleh dimulai dengan default yang dinyatakan.** Contohnya kas non-karbon = 0, dukungan material = 0, hibah, dan k = 0,5 sebagai nilai tengah.
3. **Hasil belum boleh ditafsirkan** sebelum butir "menunggu data" bagian C dikonfirmasi atau dijalankan sebagai rentang. Terutama: satuan Rp 260.000, status pembiayaan awal, sumber material rehabilitasi, dan kas non-karbon.
4. **Uji struktural Fase 2 (U0–U4, U7, U10, U11, U15–U18) harus lulus seluruhnya** sebelum simulasi skenario (Fase 3).
5. **Units Check dan run native Vensim** dijalankan peneliti. Pemeriksaan dimensional di sini bersifat statis berbasis deklarasi satuan, tidak menggantikan Units Check Vensim.
6. **Keputusan harga ARR** (tetap USD 20 atau mengikuti harga REDD).

**Yang menyebabkan BELUM SIAP bila tidak dipenuhi:** bila peneliti menolak salah satu identitas akuntansi di atas, atau data menunjukkan Rp 260.000 adalah biaya per regu-hari. Dalam kasus terakhir, nilai pembiayaan awal dan kebutuhan patroli harus dihitung ulang sebelum implementasi.
