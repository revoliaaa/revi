# Rencana Uji Fase 2 dan 3

Uji dijalankan **setelah** persamaan Fase 1B disetujui dan diterapkan pada salinan model baru. Model sebelumnya tidak ditimpa. Kriteria lulus ditetapkan sebelum melihat hasil.

## A. Sebelum simulasi (Fase 2)

| Kode | Uji | Prosedur | Kriteria lulus |
|---|---|---|---|
| U0a | Parsing sintaks | PySD `read_vensim` pada model baru, termasuk `split_views=True` | Tanpa galat; 16 View terbaca |
| U0b | Analisis statis | `cek_statis.py` pada model hasil implementasi | 0 referensi tak dikenal; 0 loop aljabar; `Switch Karbon` hanya pada 6 variabel rantai karbon |
| U0c | Satuan | Pemeriksaan manual semua persamaan baru (tabel satuan di matriks) + *Units Check* Vensim oleh peneliti | Tidak ada ketidakcocokan; Vensim: PERLU DIJALANKAN PENELITI |
| U0d | Reproduksi struktur lama | Pada model baru, setel parameter peniru model lama (k dan basis menghasilkan 2.355 HOK, kas non-karbon 0, dukungan material = biaya historis, upah non-karbon dibayar, init SMOOTHI dari 2024, Status talangan, NPV lama) | Mendekati hasil 3 skenario/A1 sejauh strukturnya setara. Selisih dijelaskan per perubahan definisi |

## B. Verifikasi struktural (Fase 2–3)

| Kode | Uji | Kriteria lulus |
|---|---|---|
| U1 | Konfigurasi skenario | S1: `Switch Karbon` = 0 sepanjang waktu; S2: 1 sejak 2024; switch PS/rehabilitasi/pendanaan awal = 1 di keduanya |
| U2 | Kegiatan PS S1 setelah 2025 | Pada k > 0: `HOK Patroli Reguler PS` > 0 untuk 2026–2087; LPHD, KUPS, dan rehabilitasi mengikuti sumber daya (tidak 0 karena switch) |
| U3 | Patroli historis tidak ganda | 2024 = 2.533, 2025 = 3.011 di S1 dan S2; `HOK Patroli Reguler PS` = 0 pada 2024–2025; `Realisasi Pembiayaan Awal` kumulatif = Rp 1.441.440.000 |
| U4 | Kesamaan S1 = S2 sebelum kas karbon | Semua variabel non-keuangan identik (selisih < 10⁻⁹) sampai tahun pertama `Penggunaan Dana Pengelolaan` S2 dari kas karbon > 0 |
| U5 | Pengurangan ganda patroli | Pada parameter dasar, `Anggota Patroli Aktif` S1 konstan 254 dan HOK reguler konstan 1.506. Penurunan hanya terjadi pada run sensitivitas yang menyalakan satu tuas saja |
| U6 | Langkah waktu | DT 0,0625 vs 0,03125: selisih indikator utama < 2 % |
| U7 | Kas dan belanja | `Saldo Dana LPHD` ≥ 0; `Saldo … dari Karbon` dalam [0, saldo]; belanja ≤ `Dana Desa Tersedia`; tidak ada belanja kas karbon sebelum kas pertama |
| U8 | Kas fiktif | S1 dengan kas non-karbon 0: `Dana Desa Diterima` = 0 dan semua belanja = 0 |
| U9 | Kapasitas LPHD | Default: kapasitas S1 tetap 0,5; naik bila pendampingan > 0 atau pembelajaran > 0; target ≤ 1 |
| U10 | KUPS | `Modal Usaha KUPS` ≥ 0; penggantian ≤ keluar; arah perubahan sesuai tabel analitis di audit konsistensi (bagian 4) |
| U11 | Rehabilitasi | Default dukungan 0: penanaman non-karbon S1 = 0, tanpa upah. Dukungan Rp 100 juta: ≈ 20,13 ha/th. Upah hanya bila porsi dibayar > 0. Cek dana penanaman vs luas terpotong batas lahan |
| U12 | Kerja dan pendapatan | HOK berupah + sukarela = total; FTE terpisah; nilai sukarela tidak masuk `Pendapatan Program per RT Bergantung`; upah karbon S1 = 0 |
| U13 | Inisialisasi | 2024 identik dengan model 3 skenario pada semua stok dan deforestasi; status SMOOTHI awal = 0,176 |
| U14 | Jeda kas | Kas pertama pada ±2027 / 2028 / 2029 untuk delay 3 / 4 / 5; jeda bayar menggeser kas, bukan penjualan |
| U15 | Neraca keuangan | Identitas `arus proyek = arus mitra + kas karbon LPHD` dengan selisih < 1 Rp/th, untuk status hibah dan talangan; NPV inkremental S1 = 0; NPV proyek S1 = −PV pembiayaan awal |
| U16 | Akuntansi karbon | Konservasi luas dan karbon (`Check …` ≈ 0); kredit konservatif ≤ kredit BAU; kredit konservatif vs (S1−S2 emisi dihindari × faktor eligible): selisih dilaporkan; harga 0 → S2 = S1 secara fisik |

## C. Kondisi ekstrem

| Kode | Kondisi | Kriteria |
|---|---|---|
| E1 | Harga karbon 0 | S2 = S1 pada semua variabel fisik dan sosial |
| E2 | k = 0 | Patroli S1 = 0 setelah 2025. Hasil setara dengan model 3 skenario S2 lama, kecuali perubahan K9, K14, dan seterusnya. Jelaskan |
| E3 | k = 1 | HOK reguler = 3.011 dan ≤ kapasitas |
| E4 | Kas non-karbon sangat besar | Belanja ≤ kebutuhan; patroli ≤ kapasitas; intensitas ≤ 1 |
| E5 | Harga USD 500 | Stok ≥ 0; intensitas ≤ 1; saldo terkendali |
| E6 | Efektivitas 0 | Patroli tidak mengubah deforestasi |

## D. Simulasi dan sensitivitas (Fase 3)

1. **Deterministik.** S1 dan S2 × harga USD 6/10/15/20/35, parameter dasar sama.
2. **Keberlanjutan PS.** k = 0 / 0,25 / 0,5 / 0,75 / 1 untuk S1 dan S2. Ditambah satu run per tuas: laju penurunan 0,01/0,03 dan penggantian 0,625, tidak digabung.
3. **Waktu dan harga.** Delay verifikasi 3/4/5 × jeda bayar 0/0,5/1 × harga 10 dan 20, terhadap NPV, kas LPHD, dan perlindungan.
4. **Sumber daya non-karbon.** Dukungan material 0 / Rp 100 juta; upah tanam 0 / 1; pendampingan 0 / data; pembelajaran 0 / 0,1 / 0,2.
5. **Keuangan.** Hibah vs talangan; diskonto 6/10/14 %; biaya pengembangan 0 / data; harga ARR tetap vs mengikuti REDD.
6. **Baseline kredit.** BAU vs konservatif.
7. **Monte Carlo dan PRCC.**
   - Hiperkubus Latin dengan seed tetap.
   - 13 parameter lama ditambah k, biaya reaktivasi, dan porsi reinvestasi, dengan distribusi dinyatakan di register.
   - Keluaran: S2−S1 deforestasi, emisi, NPV inkremental, kecukupan LPHD, Δ pendapatan RT.
   - Frekuensi ensembel dilaporkan sebagai proporsi, bukan peluang.
8. **Eksperimen alokasi B0–B4, R1–R2 pada S2** (USD 10, 20, 35), 22 kombinasi sensitivitas, dan Monte Carlo berpasangan. Diperiksa apakah kesimpulan R1 tetap berlaku.
9. **Verifikasi Vensim–PySD.** Skrip `bandingkan_vensim_pysd.py` disesuaikan untuk 2 skenario. Pengujian native dijalankan peneliti; tidak akan diklaim sudah dilakukan.
10. **Perbandingan dengan model sebelumnya.** Perubahan dipisahkan menurut sumbernya: (a) definisi skenario, (b) koreksi persamaan K1–K17 dan C1–C5, dan (c) parameter baru. Caranya menerapkan perubahan satu per satu (dekomposisi bertahap).
