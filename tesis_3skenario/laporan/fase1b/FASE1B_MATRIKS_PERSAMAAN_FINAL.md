# Fase 1B: Matriks Persamaan Final (usulan, belum diterapkan)

Dihasilkan dari `fase1b/usulan.py`, dan dibandingkan dengan persamaan yang berlaku di `DKP_25HD_FINAL_3SKENARIO.mdl`.
**Belum ada berkas `.mdl` yang diubah dan belum ada simulasi.**

**Pemeriksaan statis atas 723 persamaan model + persamaan usulan** (penelusuran teks persamaan, bukan simulasi):

- Referensi ke variabel yang tidak ada: **tidak ada**.
- Loop aljabar: **tidak ada**. Semua umpan balik melewati stok (INTEG) atau fungsi berstatus (SMOOTHI, DELAY FIXED, INITIAL).
- Pemakai `Switch Karbon` setelah usulan: `Kredit REDD Diajukan`, `Kredit ARR Diajukan`, `Kredit Gambut Diajukan`, `Biaya Verifikasi Tahunan`, `Biaya Monitoring MRV`, `Pendanaan Awal Proyek Karbon`. `Pendanaan Awal Proyek Karbon` tetap 0 karena besarannya 0.

Status per kelompok: **SETUJU** = konsisten secara struktur dan dapat disetujui; **PERLU DATA** = struktur siap, nilai menunggu data; **SENSITIVITAS** = hanya dapat dibenarkan sebagai rentang uji.

## S-1. Kode skenario

**Status:** SETUJU  
**Pengaruh S1/S2:** Menentukan S1/S2  
**Circular dependency:** Tidak ada  
**Risiko double counting:** Tidak ada  
**Uji:** U1 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Skenario Kebijakan` | `3` | `1` | Dmnl | Desain: 1 = S1 PS pembiayaan terbatas; 2 = S2 PS + karbon |

## S-2. PS aktif di kedua skenario

**Status:** SETUJU  
**Pengaruh S1/S2:** S1 tidak lagi tanpa PS; semua kegiatan PS aktif  
**Circular dependency:** Tidak ada  
**Risiko double counting:** Tidak ada  
**Uji:** U1, U2 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch PS` | `IF THEN ELSE(Skenario Kebijakan>=2,1,0)` | `1` | Dmnl | Desain |

## S-3. Rehabilitasi aktif di kedua skenario

**Status:** SETUJU  
**Pengaruh S1/S2:** idem  
**Circular dependency:** Tidak ada  
**Risiko double counting:** Tidak ada  
**Uji:** U2 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch Rehabilitasi` | `IF THEN ELSE(Skenario Kebijakan>=2,1,0)` | `1` | Dmnl | Desain |

## S-4. Pembiayaan awal historis di kedua skenario

**Status:** SETUJU  
**Pengaruh S1/S2:** Patroli 2024–2025 = 2.533/3.011 HOK di S1 dan S2  
**Circular dependency:** Tidak ada  
**Risiko double counting:** Tidak ada: hanya satu jalur patroli 2024–2025  
**Uji:** U3 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch Pendanaan Awal` | `IF THEN ELSE(Skenario Kebijakan>=2, 1, 0)` | `1` | Dmnl | Desain |

## S-5. Switch Karbon hanya pada rantai kredit/MRV

**Status:** SETUJU  
**Pengaruh S1/S2:** Satu-satunya pembeda S1–S2  
**Circular dependency:** Tidak ada  
**Risiko double counting:** Tidak ada  
**Uji:** U1, U4 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch Karbon` | `IF THEN ELSE(Skenario Kebijakan=3, STEP(1,Tahun Mulai Karbon), 0)` | `IF THEN ELSE(Skenario Kebijakan=2, STEP(1, Tahun Mulai Karbon), 0)` | Dmnl | Desain |

## K1. Patroli reguler pasca-2025

**Status:** SETUJU STRUKTUR; NILAI k PERLU SENSITIVITAS  
**Pengaruh S1/S2:** S1 dan S2 identik: 254 × 11,85 × k HOK/th mulai 2026  
**Circular dependency:** Tidak: memakai stok Anggota Patroli Aktif  
**Risiko double counting:** Dicegah: (1−Periode Pembiayaan Awal) dan STEP 2026; basis anggota dibatasi roster 2025 sehingga anggota rekrutan dana karbon tidak menambah patroli sukarela  
**Uji:** U3, U5, U6 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Periode Pasca Pembiayaan Awal` | `— (variabel baru)` | `STEP(1, Tahun Akhir Pembiayaan Awal+1)` | Dmnl | Struktur |
| `Anggota Patroli Roster 2025` | `— (variabel baru)` | `254` | People | MR1 roster 2025 (B) |
| `HOK Patroli per Anggota 2025` | `— (variabel baru)` | `HOK Patroli Pembiayaan Awal Aktual 2025/Anggota Patroli Roster 2025` | HOK/(People*Year) | Turunan data final 2025 (B) |
| `Tingkat Keberlanjutan Patroli Reguler` | `— (variabel baru)` | `0.5` | Dmnl | D, nilai tengah eksploratif; sensitivitas 0-1 |
| `Laju Penurunan Partisipasi Sukarela` | `— (variabel baru)` | `0` | 1/Year | D; sensitivitas 0-0,03 |
| `Indeks Keberlanjutan Partisipasi` | `— (variabel baru)` | `EXP(-Laju Penurunan Partisipasi Sukarela*MAX(0, Time-(Tahun Akhir Pembiayaan Awal+1)))` | Dmnl | Struktur |
| `Anggota Patroli Basis Reguler` | `— (variabel baru)` | `MIN(Anggota Patroli Aktif, Anggota Patroli Roster 2025)` | People | Struktur |
| `HOK Patroli Reguler PS` | `— (variabel baru)` | `Switch PS*Periode Pasca Pembiayaan Awal*MIN(Kapasitas Hari Patroli Anggota, Anggota Patroli Basis Reguler*HOK Patroli per Anggota 2025*Tingkat Keberlanjutan Patroli Reguler*Indeks Keberlanjutan Partisipasi)` | HOK/Year | Struktur |
| `Hari Patroli Swadaya` | `Switch PS*Switch Patroli Swadaya Reguler*(1-Periode Pembiayaan Awal)*MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota` | `HOK Patroli Reguler PS` | HOK/Year | Alias kompatibilitas |

## K2. Penggantian dan rekrutmen anggota

**Status:** SETUJU  
**Pengaruh S1/S2:** Penggantian 1 (A1) → anggota S1 tetap 254; rekrutmen tambahan hanya bila ada alokasi kas perlindungan  
**Circular dependency:** Tidak: Alokasi ← Kebutuhan ← HOK reguler ← stok  
**Risiko double counting:** Pengurangan ganda dihindari: penurunan partisipasi hanya lewat satu tuas (k dan laju penurunan), bukan juga lewat penyusutan anggota  
**Uji:** U5 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Proporsi Penggantian Anggota Patroli` | `— (variabel baru)` | `1` | Dmnl | D (A1: 1); sensitivitas 0,625 (rasio kapasitas) |
| `Penambahan Anggota Patroli` | `IF THEN ELSE(MAX(Periode Historis,Switch PS)=1, Pengurangan Anggota Patroli*Proporsi Penggantian Anggota Patroli Swadaya +Switch Karbon*IF THEN ELSE(Alokasi Dana Perlindungan>0, 1, 0)*MIN(Kapasitas Penambahan Anggota Patroli BAU *Indeks Kapasitas LPHD, MAX(0, Anggota Patroli Dibutuhkan untuk Target-Anggota Patroli Aktif )/TIME STEP), 0) +Switch Pendanaan Awal*(Penambahan Anggota Patroli Tim Baru 2024*(STEP(1, 2024)-STEP(1, 2025)) +Penambahan Anggota Patroli Tim Baru 2025*(STEP(1, 2025)-STEP(1, 2026)))` | `IF THEN ELSE(MAX(Periode Historis,Switch PS)=1, Pengurangan Anggota Patroli*Proporsi Penggantian Anggota Patroli+IF THEN ELSE(Alokasi Dana Perlindungan>0, 1, 0)*MIN(Kapasitas Penambahan Anggota Patroli BAU*Indeks Kapasitas LPHD, MAX(0, Anggota Patroli Dibutuhkan untuk Target-Anggota Patroli Aktif)/TIME STEP), 0)+Switch Pendanaan Awal*(Penambahan Anggota Patroli Tim Baru 2024*(STEP(1, 2024)-STEP(1, 2025))+Penambahan Anggota Patroli Tim Baru 2025*(STEP(1, 2025)-STEP(1, 2026)))` | People/Year | – |

## K3. Patroli didanai, kebutuhan, intensitas, kesenjangan

**Status:** SETUJU  
**Pengaruh S1/S2:** S1: patroli didanai kas hanya bila ada kas non-karbon; S2: tambahan dari kas karbon  
**Circular dependency:** Tidak  
**Risiko double counting:** Dicegah: kebutuhan patroli dikurangi HOK reguler dan historis; kesenjangan tidak lagi dikurangi Realisasi Pembiayaan Awal (dua kali)  
**Uji:** U3, U7 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Hari Patroli Didanai Kas LPHD` | `— (variabel baru)` | `(Pendanaan Awal untuk Patroli+Realisasi Belanja Perlindungan)/Biaya per Hari Patroli` | HOK/Year | – |
| `Hari Patroli Didanai` | `(Pendanaan Awal untuk Patroli+Realisasi Belanja Perlindungan)/Biaya per Hari Patroli +Hari Patroli Pembiayaan Awal` | `Hari Patroli Pembiayaan Awal+Hari Patroli Didanai Kas LPHD` | HOK/Year | – |
| `Hari Patroli Didanai Kas Non Karbon` | `— (variabel baru)` | `Hari Patroli Didanai Kas LPHD*(1-Porsi Kas Karbon dalam Saldo)` | HOK/Year | Pendekatan proporsional (B) |
| `Hari Patroli Tambahan Dibutuhkan` | `Switch PS*MAX(0, MIN(Hari Patroli Target, Kapasitas Hari Patroli Anggota)-Hari Patroli Swadaya )` | `Switch PS*MAX(0, MIN(Hari Patroli Target, Kapasitas Hari Patroli Anggota)-HOK Patroli Reguler PS-Hari Patroli Pembiayaan Awal)` | HOK/Year | – |
| `Indeks Intensitas Perlindungan` | `IF THEN ELSE(Kebutuhan Hari Patroli>0, MIN(1, (Hari Patroli Swadaya+Hari Patroli Didanai )/Kebutuhan Hari Patroli), 1)` | `IF THEN ELSE(Kebutuhan Hari Patroli>0, MIN(1, (HOK Patroli Reguler PS+Hari Patroli Didanai)/Kebutuhan Hari Patroli), 1)` | Dmnl | – |
| `Indeks Intensitas Perlindungan Tanpa Karbon` | `IF THEN ELSE(Kebutuhan Hari Patroli>0, MIN(1, Hari Patroli Swadaya/Kebutuhan Hari Patroli ), 1)` | `IF THEN ELSE(Kebutuhan Hari Patroli>0, MIN(1, (HOK Patroli Reguler PS+Hari Patroli Pembiayaan Awal+Hari Patroli Didanai Kas Non Karbon)/Kebutuhan Hari Patroli), 1)` | Dmnl | – |
| `Kesenjangan Pembiayaan Minimum` | `MAX(0, Kebutuhan Dana Minimum-Penggunaan Dana Pengelolaan-Realisasi Pembiayaan Awal)` | `MAX(0, Kebutuhan Dana Minimum-Penggunaan Dana Pengelolaan)` | Rupiah/Year | Hapus -Realisasi Pembiayaan Awal (sudah dikeluarkan dari kebutuhan dalam HOK) |
| `Kesenjangan Pembiayaan Semua Sumber` | `MAX(0, Total Kebutuhan Dana Pengelolaan-Penggunaan Dana Pengelolaan-Realisasi Pembiayaan Awal )` | `MAX(0, Total Kebutuhan Dana Pengelolaan-Penggunaan Dana Pengelolaan)` | Rupiah/Year | – |

## K4. Alokasi belanja LPHD tanpa Switch Karbon

**Status:** SETUJU  
**Pengaruh S1/S2:** Belanja dibatasi saldo; S1 = 0 bila tidak ada kas non-karbon  
**Circular dependency:** Tidak: Dana Desa Tersedia = stok/waktu  
**Risiko double counting:** Tidak ada  
**Uji:** U7, U8 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Alokasi Dana Operasional LPHD` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Operasional LPHD, Kebutuhan Dana Operasional LPHD )` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Operasional LPHD, Kebutuhan Dana Operasional LPHD)` | Rupiah/Year | – |
| `Alokasi Dana Perlindungan` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Perlindungan, Kebutuhan Dana Perlindungan )` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Perlindungan, Kebutuhan Dana Perlindungan)` | Rupiah/Year | – |
| `Alokasi Dana Rehabilitasi` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Rehabilitasi, Kebutuhan Dana Rehabilitasi )` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Rehabilitasi, Kebutuhan Dana Rehabilitasi)` | Rupiah/Year | – |
| `Alokasi Dana Penguatan Kelembagaan` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Penguatan Kelembagaan, Kebutuhan Dana Penguatan Kelembagaan)` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Penguatan Kelembagaan, Kebutuhan Dana Penguatan Kelembagaan)` | Rupiah/Year | – |
| `Alokasi Dana Pengembangan KUPS` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Pengembangan KUPS, Kebutuhan Dana Pengembangan KUPS )` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Pengembangan KUPS, Kebutuhan Dana Pengembangan KUPS)` | Rupiah/Year | – |
| `Alokasi Dana Pengendalian Kebakaran` | `Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Pengendalian Kebakaran , Kebutuhan Dana Pengendalian Kebakaran)` | `MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif Pengendalian Kebakaran, Kebutuhan Dana Pengendalian Kebakaran)` | Rupiah/Year | – |

## K5. Kas masuk LPHD karbon dan non-karbon

**Status:** SETUJU STRUKTUR; NILAI KAS NON-KARBON PERLU DATA  
**Pengaruh S1/S2:** Kas non-karbon sama di S1 dan S2 (default 0)  
**Circular dependency:** Tidak: porsi dihitung dari stok  
**Risiko double counting:** Dicegah: dua aliran terpisah, satu stok saldo + satu stok pelacak  
**Uji:** U7, U8 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch Dana Non Karbon` | `— (variabel baru)` | `0` | Dmnl | Desain; 1 bila ada data |
| `Dana Operasional Non Karbon Tunai` | `— (variabel baru)` | `0` | Rupiah/Year | D, PERLU DATA |
| `Tahun Mulai Dana Non Karbon` | `— (variabel baru)` | `2026` | Year | D |
| `Tahun Akhir Dana Non Karbon` | `— (variabel baru)` | `2087` | Year | D |
| `Kas Masuk LPHD Non Karbon` | `— (variabel baru)` | `Switch PS*Switch Dana Non Karbon*Dana Operasional Non Karbon Tunai*(STEP(1, Tahun Mulai Dana Non Karbon)-STEP(1, Tahun Akhir Dana Non Karbon+1))` | Rupiah/Year | – |
| `Kas Masuk LPHD Karbon` | `— (variabel baru)` | `Dana Program PS dari Karbon` | Rupiah/Year | – |
| `Dana Desa Diterima` | `IF THEN ELSE(Switch Dana Program Eksogen=1, Switch Karbon*Dana Program Eksogen*(STEP (1, Tahun Mulai Dana Eksogen)-STEP(1, Tahun Akhir Dana Eksogen+1)), Dana Program PS dari Karbon )` | `Kas Masuk LPHD Karbon+Kas Masuk LPHD Non Karbon` | Rupiah/Year | – |
| `Saldo Dana LPHD dari Karbon` | `— (variabel baru)` | `INTEG(Kas Masuk LPHD Karbon-Penggunaan Dana Desa*Porsi Kas Karbon dalam Saldo, 0)` | Rupiah | Stok pelacak sumber |
| `Porsi Kas Karbon dalam Saldo` | `— (variabel baru)` | `ZIDZ(Saldo Dana LPHD dari Karbon, Saldo Dana LPHD)` | Dmnl | – |

## K6. Kapasitas LPHD dari semua sumber

**Status:** SETUJU STRUKTUR; NILAI PERLU DATA/SENSITIVITAS  
**Pengaruh S1/S2:** Default (0/0): kapasitas tetap 0,5 di S1; S2 naik bila belanja kelembagaan dari kas karbon  
**Circular dependency:** Tidak: target → stok  
**Risiko double counting:** Belanja dan pendampingan non-tunai dijumlahkan; keduanya harus dari sumber berbeda  
**Uji:** U9 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Nilai Pendampingan Kelembagaan Non Tunai` | `— (variabel baru)` | `0` | Rupiah/Year | D, PERLU DATA |
| `Laju Pembelajaran Kelembagaan` | `— (variabel baru)` | `0` | Dmnl | D; sensitivitas 0-0,2 |
| `Efek Pembelajaran Kelembagaan` | `— (variabel baru)` | `Laju Pembelajaran Kelembagaan*Indeks Intensitas Perlindungan` | Dmnl | – |
| `Faktor Penguatan Kelembagaan dari Karbon` | `IF THEN ELSE(Kebutuhan Dana Penguatan Kelembagaan>0, Realisasi Belanja Penguatan Kelembagaan /Kebutuhan Dana Penguatan Kelembagaan, 0)` | `ZIDZ(Realisasi Belanja Penguatan Kelembagaan+Nilai Pendampingan Kelembagaan Non Tunai, Kebutuhan Dana Penguatan Kelembagaan)` | Dmnl | Nama lama dipertahankan; isi = semua sumber |
| `Target Kapasitas LPHD` | `Indeks Kapasitas LPHD Awal+(1-Indeks Kapasitas LPHD Awal)*Faktor Penguatan Kelembagaan dari Karbon` | `Indeks Kapasitas LPHD Awal+(1-Indeks Kapasitas LPHD Awal)*MIN(1, Faktor Penguatan Kelembagaan dari Karbon+Efek Pembelajaran Kelembagaan)` | Dmnl | – |

## K7. KUPS: modal usaha dari laba ditahan

**Status:** SETUJU STRUKTUR; PARAMETER PERLU SENSITIVITAS  
**Pengaruh S1/S2:** S1: penggantian KUPS dibatasi modal dari laba ditahan; S2: + pembentukan dari kas  
**Circular dependency:** Tidak: modal adalah stok  
**Risiko double counting:** Laba ditahan = surplus − bagian anggota, tidak dihitung dua kali dengan pendapatan anggota  
**Uji:** U10 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Porsi Laba Ditahan untuk Reinvestasi` | `— (variabel baru)` | `0.5` | Dmnl | D; sensitivitas 0-1 |
| `Biaya Reaktivasi KUPS` | `— (variabel baru)` | `Biaya Pembentukan KUPS` | Rupiah/Unit | D; sensitivitas 0,25-1 x pembentukan |
| `Modal Usaha KUPS` | `— (variabel baru)` | `INTEG(Akumulasi Modal KUPS-Penggunaan Modal KUPS, 0)` | Rupiah | – |
| `Akumulasi Modal KUPS` | `— (variabel baru)` | `MAX(0, Laba KUPS Ditahan)*Porsi Laba Ditahan untuk Reinvestasi` | Rupiah/Year | – |
| `Penggantian KUPS Berbasis Modal` | `— (variabel baru)` | `MIN(KUPS Menjadi Tidak Aktif, Modal Usaha KUPS/TIME STEP/Biaya Reaktivasi KUPS)` | Unit/Year | – |
| `Penggunaan Modal KUPS` | `— (variabel baru)` | `Penggantian KUPS Berbasis Modal*Biaya Reaktivasi KUPS` | Rupiah/Year | – |
| `Penambahan KUPS` | `IF THEN ELSE(Time < Tahun Akhir Data KUPS, Switch PS*Penambahan KUPS Historis, Switch PS *MIN(KUPS Menjadi Tidak Aktif*Proporsi Penggantian KUPS Tanpa Dana Karbon+Pembentukan KUPS Dana Non Karbon +Pembentukan KUPS Didanai Karbon, MAX(Target Total KUPS-Jumlah KUPS Aktif,0)/TIME STEP +KUPS Menjadi Tidak Aktif))` | `IF THEN ELSE(Time < Tahun Akhir Data KUPS, Switch PS*Penambahan KUPS Historis, Switch PS*MIN(Penggantian KUPS Berbasis Modal+Pembentukan KUPS Dana Non Karbon+Pembentukan KUPS Didanai Karbon, MAX(Target Total KUPS-Jumlah KUPS Aktif,0)/TIME STEP+KUPS Menjadi Tidak Aktif))` | Unit/Year | – |

## K8. Kegiatan didanai kas LPHD tanpa Switch Karbon

**Status:** SETUJU  
**Pengaruh S1/S2:** Sama dengan K4  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak ada  
**Uji:** U7 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Pembentukan KUPS Didanai Karbon` | `Switch Karbon*MIN(Target Pembentukan KUPS*Pengali Kapasitas Mode Lama, MAX(0, Realisasi Belanja Pengembangan KUPS -Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun)/Biaya Pembentukan KUPS)` | `MIN(Target Pembentukan KUPS*Pengali Kapasitas Mode Lama, MAX(0, Realisasi Belanja Pengembangan KUPS-Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun)/Biaya Pembentukan KUPS)` | Unit/Year | nama dipertahankan; = didanai kas LPHD |
| `Pembentukan KUPS Direncanakan` | `Switch Karbon*MAX(0, Alokasi Dana Pengembangan KUPS-Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun )/Biaya Pembentukan KUPS` | `MAX(0, Alokasi Dana Pengembangan KUPS-Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun)/Biaya Pembentukan KUPS` | Unit/Year | – |
| `Penanaman Didanai Karbon` | `Switch Karbon*MIN(MIN(Dana Penanaman Rehabilitasi/Biaya Penanaman per Ha, Target Penanaman *Pengali Kapasitas Mode Lama), MAX(0, Luas Restorasi Selektif Eligible-Luas Tanam Didanai Karbon )/TIME STEP)` | `MIN(MIN(Dana Penanaman Rehabilitasi/Biaya Penanaman per Ha, Target Penanaman*Pengali Kapasitas Mode Lama), MAX(0, Luas Restorasi Selektif Eligible-Luas Tanam Didanai Karbon)/TIME STEP)` | Ha/Year | – |
| `Luas Penanaman Karbon Direncanakan` | `Switch Karbon*MAX(0, Alokasi Dana Rehabilitasi-Kebutuhan Dana Pemeliharaan Rehabilitasi )/Biaya Penanaman per Ha` | `MAX(0, Alokasi Dana Rehabilitasi-Kebutuhan Dana Pemeliharaan Rehabilitasi)/Biaya Penanaman per Ha` | Ha/Year | – |

## K9. Rehabilitasi: tenaga dan material dipisah

**Status:** SETUJU STRUKTUR; DUKUNGAN MATERIAL NON-KARBON PERLU DATA  
**Pengaruh S1/S2:** S1: penanaman non-karbon ≤ realisasi historis dan ≤ dukungan material; default 0 → penanaman hanya dari kas  
**Circular dependency:** Tidak  
**Risiko double counting:** HOK tanam dipisah: didanai kas vs non-karbon; upah non-karbon hanya bila ada pembayar  
**Uji:** U11 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Biaya Tenaga Penanaman per Ha` | `— (variabel baru)` | `HOK Penanaman per Ha*Upah Penanaman per HOK` | Rupiah/Ha | Turunan (85 x 106.000) |
| `Biaya Bibit dan Material per Ha` | `— (variabel baru)` | `MAX(0, Biaya Penanaman per Ha-Biaya Tenaga Penanaman per Ha)` | Rupiah/Ha | Turunan residual (B) |
| `Dukungan Material Rehabilitasi Non Karbon` | `— (variabel baru)` | `0` | Rupiah/Year | D, PERLU DATA (program pemerintah/mitra) |
| `Penanaman Non Karbon` | `— (variabel baru)` | `Switch Rehabilitasi*(1-Periode Historis)*MIN(Proporsi Realisasi Penanaman BAU*Target Penanaman, ZIDZ(Dukungan Material Rehabilitasi Non Karbon, Biaya Bibit dan Material per Ha))` | Ha/Year | – |
| `Proporsi Realisasi Penanaman` | `MIN(1, Proporsi Realisasi Penanaman BAU+Penanaman Didanai Karbon/Target Penanaman)` | `MIN(1, ZIDZ(Penanaman Non Karbon+Penanaman Didanai Karbon, Target Penanaman))` | Dmnl | – |
| `Penambahan Luas Penanaman` | `Switch Rehabilitasi*(1-Periode Historis)*MIN(Proporsi Realisasi Penanaman*Target Penanaman , MIN(MAX(Target Total Penanaman RKPS -Luas Penanaman Program,0)/TIME STEP, NonHutan *Fraksi Maksimum NonHutan Ditanami per Tahun ))` | `Switch Rehabilitasi*(1-Periode Historis)*MIN(Proporsi Realisasi Penanaman*Target Penanaman, MIN(MAX(Target Total Penanaman RKPS-Luas Penanaman Program,0)/TIME STEP, NonHutan*Fraksi Maksimum NonHutan Ditanami per Tahun))` | Ha/Year | persamaan A1 tetap |
| `Porsi Tenaga Penanaman Non Karbon Dibayar` | `— (variabel baru)` | `0` | Dmnl | D; 0/1 sesuai program |
| `HOK Penanaman Didanai Kas` | `— (variabel baru)` | `Penanaman Didanai Karbon*HOK Penanaman per Ha` | HOK/Year | – |
| `HOK Penanaman Non Karbon` | `— (variabel baru)` | `MAX(0, HOK Penanaman-HOK Penanaman Didanai Kas)` | HOK/Year | – |
| `HOK Penanaman Berupah` | `— (variabel baru)` | `HOK Penanaman Didanai Kas+HOK Penanaman Non Karbon*Porsi Tenaga Penanaman Non Karbon Dibayar` | HOK/Year | – |
| `HOK Penanaman Sukarela` | `— (variabel baru)` | `HOK Penanaman Non Karbon*(1-Porsi Tenaga Penanaman Non Karbon Dibayar)` | HOK/Year | – |
| `Manfaat Ekonomi Penanaman` | `HOK Penanaman*Upah Penanaman per HOK` | `HOK Penanaman Non Karbon*Porsi Tenaga Penanaman Non Karbon Dibayar*Upah Penanaman per HOK` | Rupiah/Year | upah dibayar program non-karbon |

## K10. Biaya kegiatan non-karbon sebagai indikator

**Status:** SETUJU  
**Pengaruh S1/S2:** Pelaporan saja  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak masuk kas atau NPV  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Biaya Pengelolaan PS Non Karbon` | `Switch PS*Anggota Patroli Aktif*Biaya Operasional Patroli Sukarela per Anggota per Tahun+Switch Rehabilitasi *(Proporsi Realisasi Penanaman BAU*Target Penanaman*(1-Periode Historis)*Biaya Penanaman per Ha )+Switch PS*Jumlah KUPS Aktif*Biaya Pendampingan per KUPS per Tahun` | `Anggota Patroli Berpartisipasi Reguler*Biaya Operasional Patroli Sukarela per Anggota per Tahun+Penanaman Non Karbon*Biaya Bibit dan Material per Ha+HOK Penanaman Non Karbon*Porsi Tenaga Penanaman Non Karbon Dibayar*Upah Penanaman per HOK+MAX(0, Jumlah KUPS Aktif-KUPS Didukung Karbon)*Biaya Pendampingan per KUPS per Tahun` | Rupiah/Year | indikator, bukan kas |
| `Dana PS Eksisting` | `Switch PS*Biaya Pengelolaan PS Non Karbon` | `Biaya Pengelolaan PS Non Karbon` | Rupiah/Year | indikator |

## K11. Kontribusi non-tunai

**Status:** SETUJU  
**Pengaruh S1/S2:** Pelaporan; tidak masuk pendapatan RT  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak dijumlahkan dengan upah  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Upah Setara Non Tunai Patroli` | `— (variabel baru)` | `Upah Harian Patroli Berbayar` | Rupiah/HOK | C |
| `Anggota Patroli Berpartisipasi Reguler` | `— (variabel baru)` | `ZIDZ(HOK Patroli Reguler PS, HOK Patroli per Anggota 2025)` | People | – |
| `HOK Sukarela PS` | `— (variabel baru)` | `HOK Patroli Reguler PS+HOK Penanaman Sukarela` | HOK/Year | – |
| `Nilai Kontribusi Tenaga Non Tunai` | `— (variabel baru)` | `HOK Patroli Reguler PS*Upah Setara Non Tunai Patroli+HOK Penanaman Sukarela*Upah Penanaman per HOK` | Rupiah/Year | – |
| `Nilai Logistik Non Tunai Patroli` | `— (variabel baru)` | `Anggota Patroli Berpartisipasi Reguler*Biaya Operasional Patroli Sukarela per Anggota per Tahun` | Rupiah/Year | File A (C) |
| `Nilai Kontribusi Swadaya` | `Hari Patroli Swadaya*Biaya per Hari Patroli` | `Nilai Kontribusi Tenaga Non Tunai+Nilai Logistik Non Tunai Patroli` | Rupiah/Year | nama lama |
| `HOK Patroli` | `Hari Patroli Swadaya` | `0` | HOK/Year | patroli sukarela dipindah ke HOK Sukarela PS |

## K12. Kerja berupah vs sukarela

**Status:** SETUJU  
**Pengaruh S1/S2:** FTE berupah dan sukarela terpisah  
**Circular dependency:** Tidak  
**Risiko double counting:** HOK historis 2024–2025 hanya di Hari Patroli Didanai  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `HOK Berupah PS` | `— (variabel baru)` | `Hari Patroli Didanai+HOK Penanaman Berupah+HOK Pengendalian Kebakaran` | HOK/Year | – |
| `Kesempatan Kerja PS` | `Total HOK PS+HOK Patroli Berbayar+HOK Pengendalian Kebakaran` | `HOK Berupah PS+HOK Sukarela PS` | HOK/Year | – |
| `Kesempatan Kerja Berupah Setara Penuh` | `— (variabel baru)` | `HOK Berupah PS/HOK Tersedia per Anggota Kerja per Tahun` | People | – |
| `Kesempatan Kerja Sukarela Setara Penuh` | `— (variabel baru)` | `HOK Sukarela PS/HOK Tersedia per Anggota Kerja per Tahun` | People | – |
| `Upah Kegiatan PS` | `Upah Patroli Berbayar+Manfaat Ekonomi Penanaman+Manfaat Ekonomi Patroli+Upah Pengendalian Kebakaran` | `Upah Patroli Berbayar+Manfaat Ekonomi Penanaman+Upah Penanaman Didanai Karbon+Upah Pengendalian Kebakaran` | Rupiah/Year | A1 memuat Manfaat Ekonomi Patroli (=0); upah tanam didanai kas ditambahkan |

## K13. Partisipasi aktif

**Status:** SETUJU  
**Pengaruh S1/S2:** Anggota pasif tidak dihitung  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak ada  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Anggota Patroli Berpartisipasi` | `— (variabel baru)` | `MIN(Anggota Patroli Aktif, ZIDZ(HOK Patroli Reguler PS+Hari Patroli Didanai, HOK Patroli per Anggota 2025))` | People | – |
| `Total Partisipasi Kegiatan PS` | `Anggota KUPS Aktif+Anggota Patroli Aktif+Penerima Manfaat Penanaman Aktif` | `Anggota KUPS Aktif+Anggota Patroli Berpartisipasi+Penerima Manfaat Penanaman Aktif` | People | – |

## K14. Inisialisasi efek perlindungan dari 2023

**Status:** SETUJU BERSYARAT (estimasi 2.160 kelas B)  
**Pengaruh S1/S2:** Sama di S1 dan S2; 2024 tidak berubah karena Switch Dampak = 0 pada 2024  
**Circular dependency:** Tidak: argumen awal SMOOTHI dievaluasi pada INITIAL TIME  
**Risiko double counting:** Tidak ada  
**Uji:** U13 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Keikutsertaan Patroli 2023` | `— (variabel baru)` | `2160` | HOK/Year | 392 kegiatan x 5,51 (estimasi peneliti, B) |
| `Indeks Intensitas Patroli 2023` | `— (variabel baru)` | `Keikutsertaan Patroli 2023/INITIAL(Kebutuhan Hari Patroli)` | Dmnl | – |
| `Respons Perlindungan Awal` | `— (variabel baru)` | `MAX(0, MIN(1, Rasio Risiko Penempatan Patroli Swadaya*Indeks Intensitas Patroli 2023)-Indeks Perlindungan Baseline)` | Dmnl | – |
| `Efek Pengelolaan PS Aktif` | `Efek Pengelolaan PS Tanpa Karbon+(Switch PS*Switch Dampak Skenario Lahan*SMOOTHI(Respons Perlindungan , Waktu Penyesuaian Efek Pengelolaan PS, Respons Perlindungan)*Efektivitas Perlindungan Penuh terhadap Deforestasi -Efek Pengelolaan PS Tanpa Karbon)*Faktor Mutu Pelaksanaan` | `Efek Pengelolaan PS Tanpa Karbon+(Switch PS*Switch Dampak Skenario Lahan*SMOOTHI(Respons Perlindungan, Waktu Penyesuaian Efek Pengelolaan PS, Respons Perlindungan Awal)*Efektivitas Perlindungan Penuh terhadap Deforestasi-Efek Pengelolaan PS Tanpa Karbon)*Faktor Mutu Pelaksanaan` | Dmnl | – |
| `Efek Pengelolaan PS Tanpa Karbon` | `Switch PS*Switch Dampak Skenario Lahan*SMOOTHI(Respons Perlindungan Tanpa Karbon, Waktu Penyesuaian Efek Pengelolaan PS , Respons Perlindungan Tanpa Karbon)*Efektivitas Perlindungan Penuh terhadap Deforestasi` | `Switch PS*Switch Dampak Skenario Lahan*SMOOTHI(Respons Perlindungan Tanpa Karbon, Waktu Penyesuaian Efek Pengelolaan PS, Respons Perlindungan Awal)*Efektivitas Perlindungan Penuh terhadap Deforestasi` | Dmnl | – |

## K15. Acuan kondisi awal

**Status:** SETUJU  
**Pengaruh S1/S2:** Tidak berdampak selama sensitivitas tekanan = 0  
**Circular dependency:** Tidak: INITIAL  
**Risiko double counting:** Tidak ada  
**Uji:** U13 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Tingkat Kecukupan Patroli Referensi` | `SAMPLE IF TRUE(Time <= Tahun Mulai Dampak Skenario Lahan, Tingkat Kecukupan Anggota Patroli , Tingkat Kecukupan Anggota Patroli)` | `INITIAL(Tingkat Kecukupan Anggota Patroli)` | Dmnl | – |
| `Total Partisipasi Referensi` | `SAMPLE IF TRUE(Time <= Tahun Mulai Dampak Skenario Lahan, Total Partisipasi Kegiatan PS , Total Partisipasi Kegiatan PS)` | `INITIAL(Total Partisipasi Kegiatan PS)` | People | – |

## K16. Atribusi upah karbon

**Status:** SETUJU  
**Pengaruh S1/S2:** S1: 0; S2: upah dari kas karbon saja  
**Circular dependency:** Tidak  
**Risiko double counting:** Dicegah: upah patroli historis tidak lagi dihitung sebagai upah karbon  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Upah Patroli dari Kas LPHD` | `— (variabel baru)` | `Hari Patroli Didanai Kas LPHD*Upah Harian Patroli Berbayar` | Rupiah/Year | – |
| `Upah Kegiatan Didanai Karbon` | `Upah Patroli Berbayar+Upah Pengendalian Kebakaran+Upah Penanaman Didanai Karbon` | `(Upah Patroli dari Kas LPHD+Upah Pengendalian Kebakaran+Upah Penanaman Didanai Karbon)*Porsi Kas Karbon dalam Saldo` | Rupiah/Year | – |

## K17. Agregat manfaat dan FTE

**Status:** SETUJU  
**Pengaruh S1/S2:** Pelaporan  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak ada  
**Uji:** U12 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Total Manfaat Ekonomi PS` | `Pendapatan KUPS Total+Manfaat Ekonomi Patroli+Manfaat Ekonomi Penanaman` | `Pendapatan KUPS Total+Upah Kegiatan PS` | Rupiah/Year | – |
| `Total HOK PS` | `HOK Patroli+HOK Penanaman` | `Kesempatan Kerja PS` | HOK/Year | alias pelaporan |
| `Kesempatan Kerja Setara Penuh` | `Kesempatan Kerja PS/HOK Tersedia per Anggota Kerja per Tahun` | `Kesempatan Kerja Berupah Setara Penuh+Kesempatan Kerja Sukarela Setara Penuh` | People | – |
| `Porsi Tenaga Kerja Program terhadap Penduduk Bekerja` | `ZIDZ(Kesempatan Kerja Setara Penuh, Penduduk Bekerja Tercatat)` | `ZIDZ(Kesempatan Kerja Berupah Setara Penuh, Penduduk Bekerja Tercatat)` | Dmnl | – |

## C1. Jeda pembayaran dan biaya berbasis kas

**Status:** SETUJU; NILAI JEDA PERLU SENSITIVITAS  
**Pengaruh S1/S2:** S2 saja  
**Circular dependency:** Tidak: DELAY FIXED  
**Risiko double counting:** Biaya transaksi/pajak dihitung saat kas diterima, sekali  
**Uji:** U14 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Delay Pembayaran Penjualan` | `— (variabel baru)` | `0` | Year | D; sensitivitas 0/0,5/1 |
| `Kas Penjualan Kredit` | `— (variabel baru)` | `IF THEN ELSE(Delay Pembayaran Penjualan>0, DELAY FIXED(Pendapatan Kotor Penjualan Kredit, Delay Pembayaran Penjualan, 0), Pendapatan Kotor Penjualan Kredit)` | Rupiah/Year | – |
| `Biaya Transaksi Penjualan` | `Pendapatan Kotor Penjualan Kredit*Proporsi Biaya Transaksi Penjualan` | `Kas Penjualan Kredit*Proporsi Biaya Transaksi Penjualan` | Rupiah/Year | – |
| `Pajak dan Pungutan Karbon` | `Pendapatan Kotor Penjualan Kredit*Proporsi Pajak dan Pungutan Karbon` | `Kas Penjualan Kredit*Proporsi Pajak dan Pungutan Karbon` | Rupiah/Year | – |
| `Surplus Sebelum Pemulihan` | `MAX(0, Pendapatan Kotor Penjualan Kredit-Biaya Transaksi dan MRV)` | `MAX(0, Kas Penjualan Kredit-Biaya Transaksi dan MRV)` | Rupiah/Year | – |
| `Kekurangan Biaya Bersama Ditanggung Mitra` | `MAX(0, Biaya Transaksi dan MRV-Pendapatan Kotor Penjualan Kredit)` | `MAX(0, Biaya Transaksi dan MRV-Kas Penjualan Kredit)` | Rupiah/Year | – |

## C2. Status pembiayaan awal dan pemulihan sebelum bagi hasil

**Status:** SETUJU; STATUS PERLU DATA  
**Pengaruh S1/S2:** S1: tidak ada pemulihan; S2: pulih dari surplus bila talangan  
**Circular dependency:** Tidak  
**Risiko double counting:** Dicegah: pemulihan dari surplus sebelum 60/40, bukan dari bagian mitra sendiri  
**Uji:** U15 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Status Pembiayaan Awal` | `— (variabel baru)` | `0` | Dmnl | D: 0 hibah, 1 talangan |
| `Pendanaan Awal Belum Terpulihkan` | `INTEG(Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal*Porsi Pembiayaan Awal sebagai Talangan +Biaya Modal Pendanaan Awal Rp-Pemulihan Pendanaan Awal, 0)` | `INTEG(Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal*Status Pembiayaan Awal+Biaya Modal Pendanaan Awal Rp-Pemulihan Pendanaan Awal, 0)` | Rupiah | – |
| `Pemulihan Pendanaan Awal` | `MIN(Dana Mitra dari Karbon, Pendanaan Awal Belum Terpulihkan/TIME STEP)` | `MIN(MAX(0, Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama), Pendanaan Awal Belum Terpulihkan/TIME STEP)` | Rupiah/Year | dipulihkan sebelum bagi hasil |
| `Pendapatan Karbon Bersih yang Dapat Didistribusikan` | `Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama` | `Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama-Pemulihan Pendanaan Awal` | Rupiah/Year | – |

## C3. Baseline konservatif REDD dan ARR

**Status:** SETUJU SEBAGAI SENSITIVITAS  
**Pengaruh S1/S2:** S2 saja  
**Circular dependency:** Tidak: memakai status SMOOTHI dan stok  
**Risiko double counting:** Lihat AUDIT_AKUNTANSI_KARBON_NPV.md bagian 2  
**Uji:** U16 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Switch Baseline Kredit Konservatif` | `0` | `0` | Dmnl | 0 = BAU (dasar); 1 = konservatif |
| `Porsi ARR Adisional` | `— (variabel baru)` | `ZIDZ(Penanaman Didanai Karbon*Porsi Kas Karbon dalam Saldo, Penambahan Luas Penanaman)` | Dmnl | pendekatan aliran (B) |
| `Kredit ARR Diajukan` | `Pengurangan Emisi Eligible ARR*Switch Karbon*Switch Periode Kredit` | `Pengurangan Emisi Eligible ARR*Switch Karbon*Switch Periode Kredit*(1-Switch Baseline Kredit Konservatif*(1-Porsi ARR Adisional))` | tCO2e/Year | – |
| `Faktor Rekonsiliasi Reversal Kredit A2` | `1.000000` | `1` | Dmnl | ditetapkan 1 |

## C4. NPV di dalam model

**Status:** SETUJU; DISKONTO DAN BIAYA PENGEMBANGAN PERLU DATA  
**Pengaruh S1/S2:** S1: NPV proyek = −PV pembiayaan awal; NPV inkremental = 0  
**Circular dependency:** Tidak: INTEG  
**Risiko double counting:** Identitas: arus proyek = arus mitra + kas LPHD karbon  
**Uji:** U15 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Tingkat Diskonto` | `— (variabel baru)` | `0.1` | 1/Year | D, tidak bersumber; sensitivitas 0,06-0,14 |
| `Faktor Diskonto` | `— (variabel baru)` | `1/((1+Tingkat Diskonto*Satu Tahun)^((Time-INITIAL TIME)/Satu Tahun))` | Dmnl | – |
| `Biaya Pengembangan Proyek` | `— (variabel baru)` | `0` | Rupiah/Year | D, PERLU DATA |
| `Arus Kas Proyek Karbon` | `— (variabel baru)` | `Kas Penjualan Kredit-Biaya Transaksi dan MRV-Biaya Pengembangan Proyek` | Rupiah/Year | – |
| `Arus Kas Proyek Keseluruhan` | `— (variabel baru)` | `Arus Kas Proyek Karbon-Realisasi Pembiayaan Awal` | Rupiah/Year | – |
| `Arus Kas Mitra` | `— (variabel baru)` | `Dana Mitra dari Karbon+Pemulihan Defisit Biaya Bersama+Pemulihan Pendanaan Awal-Kekurangan Biaya Bersama Ditanggung Mitra-Realisasi Pembiayaan Awal-Biaya Pengembangan Proyek` | Rupiah/Year | – |
| `NPV Proyek Keseluruhan` | `— (variabel baru)` | `INTEG(Arus Kas Proyek Keseluruhan*Faktor Diskonto, 0)` | Rupiah | – |
| `NPV Inkremental Perdagangan Karbon` | `— (variabel baru)` | `INTEG(Arus Kas Proyek Karbon*Faktor Diskonto, 0)` | Rupiah | S1: 0 |
| `NPV Mitra` | `— (variabel baru)` | `INTEG(Arus Kas Mitra*Faktor Diskonto, 0)` | Rupiah | – |
| `PV Kas Masuk LPHD` | `— (variabel baru)` | `INTEG(Dana Desa Diterima*Faktor Diskonto, 0)` | Rupiah | – |
| `PV Kebutuhan Dana Minimum` | `— (variabel baru)` | `INTEG(Kebutuhan Dana Minimum*Faktor Diskonto, 0)` | Rupiah | – |
| `Rasio Cakupan Kebutuhan Minimum` | `— (variabel baru)` | `ZIDZ(Penggunaan Dana Pengelolaan, Kebutuhan Dana Minimum)` | Dmnl | – |

## C5. Indikator karbon terpisah

**Status:** SETUJU  
**Pengaruh S1/S2:** Pelaporan  
**Circular dependency:** Tidak  
**Risiko double counting:** Tidak ada  
**Uji:** U16 (lihat RENCANA_UJI_FASE2.md)

| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |
|---|---|---|---|---|
| `Emisi Deforestasi Dihindari terhadap Baseline` | `— (variabel baru)` | `Emisi Deforestasi Biomassa Baseline-Emisi Deforestasi Biomassa` | tCO2e/Year | selisih S2-S1 dihitung antar-run |
| `Serapan Rehabilitasi` | `— (variabel baru)` | `Komitmen Serapan Rehabilitasi` | tCO2e/Year | – |

## Catatan sintaks Vensim dan PySD

- **`STEP(h, t)`.** Naik pada `Time >= t`. Dengan DT 0,0625 dan tahun bulat, `STEP(1,2026)` aktif tepat pada awal 2026. Fungsi ini sudah dipakai A1 dan hasil 2024–2025 terverifikasi.
- **`INITIAL(x)`.** Dievaluasi sekali pada 2024, dan didukung PySD. Dipakai untuk `INITIAL(Kebutuhan Hari Patroli)` dan acuan K15.
- **`SMOOTHI(input, delay, init)`.** Argumen `init` (`Respons Perlindungan Awal`) hanya bergantung pada konstanta dan `INITIAL`, sehingga aman pada t0.
- **`DELAY FIXED(input, delay, init)`.**
  - Waktu tunda dibaca sekali pada t0. Nilai 0,5, 1, 3, 4, dan 5 tahun adalah kelipatan DT 0,0625.
  - Tunda 0 dibungkus `IF THEN ELSE`, karena DELAY FIXED dengan tunda 0 tidak didefinisikan dengan aman.
  - Di PySD, cabang `IF` yang tidak terpilih tetap membuat objek delay. Ini tidak masalah selama parameternya ≥ 0.
- **`ZIDZ(a, b)`.** Dipakai untuk semua pembagian yang penyebutnya dapat 0 (saldo 0 di S1, penanaman 0, HOK 0).
- **`MIN` dan `MAX`.** Tidak ada `MIN` yang memotong aliran stok sehingga stok negatif:
  - `Penggantian KUPS Berbasis Modal` dibatasi `Modal/TIME STEP`, sehingga modal ≥ 0;
  - `Pemulihan Pendanaan Awal` dibatasi sisa talangan/TIME STEP.
- **`EXP(−laju × Δt)`.** Bila laju = 0, nilainya 1. Laju bersatuan 1/Year dan Δt bersatuan Year, sehingga hasilnya Dmnl.
- **`Faktor Diskonto`.** Ditulis dengan `Satu Tahun` (variabel A1) agar satuannya konsisten di Vensim *Units Check*.
- **Nama variabel.** `Hari Patroli Swadaya`, `HOK Patroli`, `Faktor Penguatan Kelembagaan dari Karbon`, `Pembentukan KUPS Didanai Karbon`, dan `Penanaman Didanai Karbon` **dipertahankan** agar 16 View, sketch, dan register tetap utuh. Arti barunya ditulis di komentar Vensim. Mengganti nama akan memutus panah di diagram Vensim asli.
