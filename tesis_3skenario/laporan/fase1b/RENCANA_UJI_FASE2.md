# Rencana Uji Fase 2 dan 3 (revisi final gate)

Uji dijalankan **setelah** persamaan disetujui dan diterapkan pada salinan model baru. Model sebelumnya tidak ditimpa. Kriteria lulus/gagal ditetapkan sebelum melihat hasil.

Toleransi numerik: ε_Rp = 1 Rp/th atau 10⁻⁹ relatif; ε_fisik = 10⁻⁶ (ha, HOK, orang).

Satu kegagalan pada uji struktural (U0–U4, U7, U10, U11, U15–U18) **menghentikan Fase 3**.

## A. Sebelum simulasi (Fase 2)

| Kode | Uji | Prosedur | LULUS bila | GAGAL bila |
|---|---|---|---|---|
| U0a | Parsing | PySD `read_vensim` (+ `split_views=True`) | tanpa galat; 16 View terbaca | ada galat atau View hilang |
| **U0b** | Analisis statis (revisi) | `cek_statis.py` pada **model hasil implementasi**, bukan rancangan; bandingkan setiap persamaan dengan `usulan.py` | 0 referensi tak dikenal; 0 loop aljabar; pemakai `Switch Karbon` = tepat 7 variabel (daftar di final gate); **163/163 persamaan identik teks dengan rancangan** | ada selisih teks, loop, atau pemakai `Switch Karbon` lain |
| U0c | Units Check Vensim | peneliti | tanpa peringatan pada variabel baru/diubah | ada peringatan yang tidak dijelaskan |
| U0d | Reproduksi struktur lama | parameter peniru model lama | selisih terhadap model 3 skenario dapat diatribusikan ke perubahan definisi yang terdaftar | ada selisih tanpa penjelasan |

## B. Verifikasi struktural (Fase 2–3)

| Kode | Uji | LULUS bila | GAGAL bila |
|---|---|---|---|
| U1 | Konfigurasi | S1: `Switch Karbon` = 0 di semua t; S2: = 1 sejak 2024; switch PS/rehabilitasi/pendanaan awal = 1 di keduanya | selain itu |
| U2 | Kegiatan PS S1 pasca-2025 | k > 0: `HOK Patroli Reguler PS` > 0 untuk semua t ≥ 2026 | patroli S1 = 0 pada k > 0 |
| **U3** | Patroli historis tidak ganda (revisi) | S1 dan S2: `Total HOK Patroli` = 2.533 (2024) dan 3.011 (2025) ± ε; `HOK Patroli Reguler PS` = 0 dan `Hari Patroli Didanai Kas LPHD` = 0 pada 2024–2025; `Check Identitas Patroli` = 0 di semua t; `Realisasi Pembiayaan Awal` kumulatif = Rp 1.441.440.000 ± ε; `Upah Patroli Berbayar` 2024 = 2.533 × 130.000; tidak ada komponen 2024–2025 di `Kebutuhan Dana Perlindungan`, `Kesenjangan`, atau `Upah Kegiatan Didanai Karbon`; **juga diuji dengan kas non-karbon > 0 mulai 2024**: total patroli 2024–2025 tetap = data | ada satu pelanggaran |
| **U4** | S1 = S2 sebelum kas karbon (revisi) | Semua variabel **fisik dan sosial** (tutupan, deforestasi, HOK, KUPS, anggota, pendapatan RT, saldo LPHD, belanja) identik ± ε sampai `Kas Masuk LPHD Karbon` S2 > 0 pertama kali. Yang boleh berbeda sebelum itu **hanya**: variabel kredit, `Biaya Transaksi dan MRV`, `Kekurangan Biaya Bersama Ditanggung Mitra`, `Defisit Biaya Bersama Belum Dipulihkan`, dan NPV | ada variabel lain yang berbeda |
| U5 | Pengurangan ganda patroli | Dasar: anggota S1 konstan 254; HOK reguler konstan (k × 3.011). Run sensitivitas menyalakan satu tuas saja | anggota menyusut pada run dasar |
| U6 | Langkah waktu | DT 0,0625 vs 0,03125: indikator utama berbeda < 2 %. Syarat DT ≤ `Waktu Pembelanjaan Dana Desa` dicek | > 2 % atau syarat dilanggar |
| **U7** | Neraca LPHD (revisi) | `Saldo Dana LPHD` ≥ 0; 0 ≤ `Saldo … dari Karbon` ≤ `Saldo`; `Check Neraca Dana LPHD` = 0 ± ε; `Jumlah Proporsi Alokasi Efektif` ≤ 1; Σ alokasi ≤ `Dana Desa Tersedia`; `Penggunaan Dana Desa` ≤ `Dana Desa Tersedia`; tidak ada belanja kas karbon sebelum kas pertama; model alokasi: Σ porsi fleksibel = 1 dan kompensasi termasuk penggunaan | ada satu pelanggaran |
| U8 | Kas fiktif | S1, kas non-karbon 0: `Dana Desa Diterima` = 0 dan semua belanja = 0 | ada belanja > 0 |
| U9 | Kapasitas LPHD | Default: kapasitas S1 = 0,5 konstan; target ≤ 1 | kapasitas naik tanpa sumber |
| **U10** | KUPS (revisi) | `Modal Usaha KUPS` ≥ 0; `Penggunaan Modal KUPS` = 0 untuk t < 2026; penggantian ≤ keluar; `Check Identitas Surplus KUPS` = 0 dan `Check Identitas Penjualan KUPS` = 0 ± ε; Σ akumulasi − Σ penggunaan = modal akhir; hanya `Pendapatan KUPS Total` (bagian anggota) yang masuk pendapatan RT | ada satu pelanggaran |
| **U11** | Rehabilitasi (revisi) | `Penambahan Luas Penanaman` ≤ `Batas Luas Penanaman`; `Check Identitas HOK Penanaman` = 0; `Pengeluaran Kas Penanaman Aktual` = luas kas aktual × Rp 14 juta; `Realisasi Belanja Rehabilitasi Efektif` ≤ `Realisasi Belanja Rehabilitasi` (selisih tetap di saldo); `Luas Tanam Didanai Karbon` = Σ luas kas **aktual**; dukungan 0: penanaman non-karbon = 0 dan upah non-karbon = 0; dukungan Rp 100 juta: ≈ 20,13 ha/th; upah non-karbon hanya bila porsi dibayar > 0 | ada satu pelanggaran |
| U12 | Kerja dan pendapatan | HOK berupah + sukarela = total; FTE terpisah; nilai sukarela, logistik, dan dukungan material tidak masuk `Pendapatan Program per RT Bergantung`; upah karbon S1 = 0 | ada nilai non-tunai di pendapatan RT |
| U13 | Inisialisasi | Semua stok dan deforestasi 2024 identik dengan model 3 skenario; status SMOOTHI awal = 0,176 | nilai 2024 berubah |
| U14 | Jeda kas | Kas pertama ±2027 / 2028 / 2029 untuk delay 3 / 4 / 5; jeda bayar menggeser kas, bukan penjualan | kas sebelum kredit terbit |
| **U15** | Keuangan dan NPV (revisi) | `Check Identitas Arus Kas` = 0 ± ε di semua t, untuk hibah dan talangan; NPV(S2) − NPV(S1) = NPV inkremental ± ε; NPV inkremental S1 = 0; NPV keseluruhan S1 = −`PV Pembiayaan Awal`; **hibah:** `Pokok Talangan Kumulatif` = 0 dan `Pemulihan Kumulatif` = 0; **talangan:** `Pemulihan Kumulatif` ≤ `Pokok Talangan Kumulatif` + `Biaya Modal Kumulatif`, stok talangan = pokok + biaya modal − pemulihan ± ε; biaya sebelum kas pertama tercatat di `Kekurangan Biaya Bersama Ditanggung Mitra`; LPHD tidak menanggung biaya karbon | ada satu pelanggaran |
| **U16** | Akuntansi karbon (revisi) | `Check Total Kawasan` dan `Check Konservasi Karbon` ≈ 0; kredit konservatif ≤ kredit BAU (REDD dan ARR); kredit konservatif dibandingkan dengan (emisi dihindari S2−S1 × faktor eligible) dan selisihnya dilaporkan; indikator 1–5 dilaporkan terpisah dan tidak dijumlahkan; harga 0 → S2 = S1 fisik; **kredit ARR konservatif hanya dari luas kas karbon aktual** | kredit konservatif > BAU, atau indikator dijumlahkan |
| **U17** | Konsistensi data historis 2023–2025 dengan kondisi awal 2024 (baru) | (a) `Anggota Patroli Aktif`: 183 (awal 2024) + 61 (2024) + 10 (2025) = 254 pada awal 2026 dengan penggantian penuh = `Anggota Patroli Roster 2025`; (b) HOK per anggota 2024 (2.533 ÷ rerata anggota 2024) dan 2025 (3.011 ÷ rerata anggota 2025) dilaporkan dan dibandingkan dengan 11,85; (c) `Keikutsertaan Patroli 2023` = 2.160 ≈ 392 × 5,51 (±1 %) dan hanya dipakai di `Respons Perlindungan Awal`; (d) tidak ada arus kas 2023 di model; (e) `Tahun Awal/Akhir Pembiayaan Awal` = 2024/2025; (f) indeks intensitas 2023 (0,270) dan 2024 (0,317) dilaporkan berdampingan dengan `Indeks Intensitas Swadaya 2023` (0,2251, tidak aktif) dan selisih basisnya dijelaskan | (a) atau (c)–(e) gagal |
| **U18** | Konsistensi dimensional (baru) | `cek_satuan.py semua` pada model hasil implementasi: semua persamaan konsisten untuk dimensi stok (X), aliran (X/Year), HOK, People, Ha, Rupiah, dan Rupiah/Year; uji negatif pemeriksa (4 kasus) tertangkap semua; ditambah U0c Vensim | ada persamaan tidak konsisten atau uji negatif lolos |

## C. Kondisi ekstrem

| Kode | Kondisi | LULUS bila |
|---|---|---|
| E1 | Harga karbon 0 | S2 = S1 pada semua variabel fisik dan sosial |
| E2 | k = 0 | Patroli S1 = 0 setelah 2025; selisih terhadap model 3 skenario S2 lama dijelaskan per perubahan |
| E3 | k = 1 | HOK reguler = 3.011 ≤ kapasitas |
| E4 | Kas non-karbon sangat besar | belanja ≤ kebutuhan; patroli ≤ kapasitas; intensitas ≤ 1; saldo menumpuk, tidak dibelanjakan fiktif |
| E5 | Harga USD 500 | stok ≥ 0; intensitas ≤ 1; tanam ≤ batas luas |
| E6 | Efektivitas 0 | patroli tidak mengubah deforestasi |
| E7 | Talangan + biaya modal 20 %/th | pemulihan ≤ pokok + biaya modal; NPV proyek keseluruhan tidak berubah |

## D. Simulasi dan sensitivitas (Fase 3)

1. **Deterministik.** S1 dan S2 × USD 6/10/15/20/35.
2. **Keberlanjutan PS.** k = 0 / 0,25 / 0,5 / 0,75 / 1 (S1 dan S2), ditambah satu run per tuas (laju penurunan 0,01/0,03; penggantian 0,625), tidak digabung.
3. **Waktu dan harga.** Delay 3/4/5 × jeda bayar 0/0,5/1 × harga 10 dan 20.
4. **Sumber daya non-karbon.** Dukungan material 0 / Rp 100 juta; upah tanam 0/1; pendampingan 0/data; pembelajaran 0/0,1/0,2; kas non-karbon 0/data.
5. **Keuangan.** Hibah/talangan; diskonto 6/10/14 %; biaya pengembangan 0/data; harga ARR tetap/ikut REDD.
6. **Baseline.** BAU vs konservatif.
7. **Monte Carlo dan PRCC.** Hiperkubus Latin, seed tetap, distribusi dinyatakan. Frekuensi dilaporkan sebagai proporsi ensembel.
8. **Eksperimen alokasi** B0–B4, R1–R2 pada S2.
9. **Verifikasi Vensim–PySD.** Dijalankan peneliti; tidak diklaim.
10. **Dekomposisi perubahan terhadap model sebelumnya.** Pisahkan perubahan karena (a) definisi skenario, (b) koreksi persamaan, dan (c) parameter baru.
