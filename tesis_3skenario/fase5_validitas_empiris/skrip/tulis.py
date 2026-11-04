import json
T = json.load(open("fase7/tabel_md.json"))
ST = """**Status:**
- Model `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` dibekukan (md5 `639083f9…`; tidak ada persamaan atau variabel baru).
- PySD 3.14.3; **Vensim native: BELUM DIVERIFIKASI NATIVE**.
- NPV SEMENTARA. K7 endogen GAGAL (tidak dipakai). Referensi S1 berpasangan dipakai di semua konfigurasi S2.
- D0–D3 adalah konfigurasi eksperimen internal, bukan skenario kebijakan. Selisihnya adalah dekomposisi menurut asumsi model, **bukan identifikasi kausal empiris**."""
D = {}
D["LAPORAN_DEKOMPOSISI_PEMBIAYAAN_KARBON.md"] = f"""# Laporan Dekomposisi Pembiayaan Karbon (D0–D3)

**Tanggal:** 4 November 2026

**Data:** `HASIL_EKSPERIMEN_D0_D3.xlsx`. **Grafik:** `GRAFIK_ATRIBUSI_PEMBIAYAAN/G1–G7`.

{ST}

## 1. Konfigurasi

Semua konfigurasi dibentuk hanya dengan menimpa parameter atau variabel yang sudah ada.

| Kode | Jembatan 2026–2030 | Penjualan kredit | Implementasi |
|---|---|---|---|
| D0 | Tidak | Tidak | S1 |
| D1 | Ya (J1, Rp0,78 M/th), **hibah** | Tidak | S2; `Status Proyek Karbon Aktif` := 0, sehingga tanpa kredit, MRV, maupun penerimaan; talangan dihapus 2031 dan diakui sebagai kerugian/hibah mitra |
| D2 | Ya (J1), talangan dipulihkan dari surplus | Ya | S2-C-J1 Fase 4 |
| D3 | Tidak | Hanya bila layak secara endogen | S2; `Switch Pembiayaan Jembatan Karbon` = 0; aturan MRV sama dengan D2. D3h: + aturan henti MRV prospektif |

**Pemeriksaan sebelum interpretasi:**
- D0 = S1 Fase 4 dan D2 = S2-C-J1 Fase 4 (USD 10/20/35): selisih **0** pada 190 variabel.
- D1 tidak mengandung kredit, biaya MRV, kas penjualan, maupun utang tanpa sumber.
- D3 tidak memaksa kredit terbit.

## 2. Hasil dasar

### 2.1 USD 10

{T['d10']}

### 2.2 USD 20

{T['d20']}

### 2.3 USD 35

{T['d35']}

Identitas aritmetis D2 − D0 = (D1 − D0) + (D2 − D1) berlaku untuk semua indikator dan variasi (selisih maks 6·10⁻⁵).

## 3. Atribusi tambahan perlindungan (semua variasi)

{T['atr']}

## 4. Jawaban pertanyaan analitis

1. **Apakah tambahan perlindungan pada USD 10–20 sebagian besar disebabkan talangan awal?**
   - **Ya, menurut model.** Pada konfigurasi dasar, pembiayaan awal menyumbang **100 %** (USD 10) dan **63 %** (USD 20) deforestasi dihindari.
   - Pada USD 10, penjualan karbon tidak menambah perlindungan sama sekali, karena kas karbon tidak pernah sampai ke LPHD.
   - Porsi jembatan naik bila efektivitas rendah (0,2: ±100 % pada USD 10–20) atau biaya per HOK tinggi (Rp300.000: 75–100 %).
   - Porsi jembatan turun bila efektivitas tinggi (0,6: 10 % pada USD 20) atau biaya per HOK rendah (Rp150.000: 8 % pada USD 20).
2. **Apakah penerimaan karbon sesudah jembatan benar-benar mempertahankan tambahan patroli?**
   - **USD 20:** hanya sementara. Patroli dari kas LPHD 2031–2086 hanya 8,9 ribu HOK dan habis sebelum ±2055. Tambahan kerja berupah 2060–2086 = 0.
   - **USD 35:** ya, 236,7 ribu HOK, dan FTE berupah 2060–2086 +39,5.
3. **Apakah pada USD 35 pendapatan karbon menghasilkan penguatan yang bertahan sesudah jembatan?**
   - **Ya:** 94 % deforestasi dihindari berasal dari mekanisme penjualan, dan 98 % dari deforestasi dihindari pasca-2030.
   - LPHD menerima Rp214 M; cakupan kebutuhan 2060–2086 sebesar 90 %; KUPS 2087 +44,7.
   - **Syarat:** pembiayaan awal tetap diperlukan untuk memulai siklus (lihat butir 4).
4. **Apakah tanpa jembatan muncul *bootstrap problem*?**
   - **Ya, secara struktural.** D3 tidak menghasilkan kredit sama sekali pada **semua** harga dan variasi, termasuk efektivitas 0,6 dan biaya Rp150.000/HOK. Kredit konservatif hanya mengakui mitigasi di atas S1, dan tanpa dana tambahan tidak ada kegiatan di atas S1.
   - Bila MRV tetap dijalankan, mitra menanggung Rp22,8 M tanpa penerimaan. Dengan aturan henti MRV (D3h), kerugian itu Rp2,9 M.
5. **Apakah kesimpulan keuangan dan kesejahteraan berubah bila efek talangan dipisahkan?**
   - **Keuangan.** Pada USD 10, mekanisme penjualan memperburuk posisi mitra dibanding hibah murni: arus kas nominal −Rp15,8 M (MRV tanpa penerimaan cukup). Dampak fisiknya nol.
   - Pada USD 20, NPV mitra naik +Rp2,3 M [SEMENTARA] karena penerimaan datang lebih awal, tetapi arus kas nominal turun −Rp6,2 M karena defisit MRV sesudah 2051.
   - Pada USD 35, posisi mitra naik +Rp146,8 M nominal.
   - **Kesejahteraan.** Penurunan pendapatan RT terdampak terbagi ke dua sumber:
     - pembiayaan awal: −57.610 Rp/th;
     - penjualan: −67.612 Rp/th pada USD 20 dan −439.269 pada USD 35.

     Keduanya berasal dari tambahan perlindungan yang sama-sama memperbesar kehilangan akses. Bila pengali akses 0, keduanya positif (tabel di bawah).

{T['akses']}

## 5. Keterbatasan khusus

- D1 memperlakukan jembatan sebagai hibah. Pemulihan tidak mungkin tanpa penerimaan, sehingga talangan dicatat sebagai kerugian mitra. Ini pilihan akuntansi diagnostik, bukan klaim tentang kontrak.
- D1 dibentuk dengan menimpa variabel status proyek, bukan dengan switch baru, agar model tetap dibekukan. Di Vensim native, setara dengan menjadikan variabel itu konstanta 0 pada salinan run; **belum diverifikasi native**.
- D3 memakai aturan MRV yang sama dengan D2 (MRV sejak 2024). Varian D3h menunjukkan sensitivitasnya terhadap aturan henti.
"""
D["LAPORAN_VERIFIKASI_FASE5.md"] = f"""# Laporan Verifikasi Fase 5

**Tanggal:** 4 November 2026

{ST}

## 1. Hasil verifikasi

Lembar 5 `HASIL_EKSPERIMEN_D0_D3.xlsx`.

{T['ver']}

## 2. Pemeriksaan per permintaan

| No | Pemeriksaan | Hasil |
|---|---|---|
| 1 | Kesetaraan D0 dengan S1 | Selisih 0 pada 190 variabel |
| 2 | Kesetaraan D2 dengan S2-C-J1 | Selisih 0 (USD 10/20/35) |
| 3 | Satuan dan referensi persamaan | Model tidak diubah. Hasil Fase 4 tetap berlaku: 0 referensi tak dikenal, 0 loop aljabar, satuan 933/933 konsisten (model utama) dan 960/960 (model alokasi). Penimpaan D1 dan D3 hanya mengganti nilai konstanta/variabel berdimensi sama (Dmnl, Year) |
| 4 | Neraca biaya dan pendapatan | Identitas arus kas ≤ 10⁻⁶ Rp; neraca LPHD ≤ 4·10⁻⁴ Rp; D1: jembatan = kerugian mitra diakui (selisih 0), sisa talangan 0; rekonsiliasi lengkap arus kas D2 di `AUDIT_AKADEMIK_FINAL_PWD.md` |
| 5 | Stok dan aliran ekologis | \\|Check Total Kawasan\\| ≤ 2·10⁻¹⁰ ha; \\|Check Konservasi Karbon\\| ≤ 7·10⁻⁸ |
| 6 | Timestep (argumen `time_step` PySD) | DT 0,0625 vs 0,03125: selisih hutan 2087 ≤ 0,003 %; NPV mitra ≤ 0,37 % |
| 7 | Konfigurasi Referensi S1 | Hutan Referensi S1 = D0 di semua run (selisih 0) |
| 8 | Keberlanjutan pembiayaan sesudah 2030 | Dilaporkan (indikator E10, F10, S3) |
| 9 | Kondisi ekstrem | Tanpa harga (Fase 4 E1/E1b); tanpa kredit (D1); tanpa jembatan (D3): semua berperilaku sesuai definisi |
| 10 | Rekonsiliasi dengan Fase 4 | D0 dan D2 identik dengan Fase 4. Kontras D2 − D0 sama dengan hasil S2 − S1 Fase 4 (deforestasi dihindari 287 / 454 / 4.954 ha) |

**Vensim native:** tidak tersedia di lingkungan ini. Status: **BELUM DIVERIFIKASI NATIVE** (Units Check dan pembandingan lintasan).

## 3. Temuan dokumentasi (bukan kesalahan persamaan)

Komentar parameter `Biaya per Hari Patroli` di berkas model masih menulis "Upah Rp130.000/orang-hari + logistik Rp130.000". Persamaan model sudah benar: upah Rp150.000 di variabel `Upah Harian Patroli Berbayar`, dan komponen non-upah diturunkan sebagai Rp110.000.

Model dibekukan sehingga komentar tidak diubah. Koreksi dicatat di register parameter dan harus diterapkan pada versi model berikutnya (bila ada).

## 4. Kesimpulan

Konfigurasi D0–D3 lulus semua pemeriksaan yang dapat dijalankan di PySD. Monte Carlo baru tidak diperlukan, karena dekomposisi deterministik dan sensitivitas terarah (10 variasi × 3 harga) sudah menjawab pertanyaan atribusi, dan hasilnya konsisten di semua variasi.
"""
D["LAPORAN_VALIDITAS_EMPIRIS_DUA_SKENARIO.md"] = f"""# Laporan Validitas Empiris Dua Skenario

**Tanggal:** 4 November 2026

**Data:** `REGISTER_PARAMETER_DAN_BUKTI_EMPIRIS.xlsx`.

{ST}

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

{T['reg']}

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
"""
D["TEMUAN_FINAL_DAN_KETERBATASAN_PWD.md"] = f"""# Temuan Final dan Keterbatasan (PWD)

**Tanggal:** 4 November 2026

{ST}

## Keputusan akademik

**1. Apakah dua skenario lebih dapat dipertanggungjawabkan daripada empat skenario lama?**

Ya. Patroli 2023–2025 dibiayai mitra proyek karbon, sehingga skenario "PS swadaya" tidak berdasar data, dan "tanpa PS" bukan alternatif kebijakan yang tersedia. Dua skenario memperlakukan sejarah pembiayaan sebagai fakta bersama. Asumsi yang tersisa (jembatan masa depan) kini terukur lewat D1 − D0.

**2. Seberapa besar tambahan perlindungan S2 disebabkan pembiayaan awal dibanding penjualan karbon?**

Menurut model, deforestasi dihindari pada konfigurasi dasar:

| Harga | Dari pembiayaan awal | Dari penjualan karbon |
|---|---|---|
| USD 10 | 287 ha (100 %) | 0 |
| USD 20 | 287 ha (63 %) | 167 ha (37 %) |
| USD 35 | 287 ha (6 %) | 4.667 ha (94 %) |

Pada USD 20, porsi pembiayaan awal berkisar 8–100 % antarvariasi, sangat bergantung pada efektivitas perlindungan dan biaya per HOK.

**3. Kapan pendapatan penjualan karbon mempertahankan kegiatan sesudah dana awal berakhir?**

Hanya pada harga tinggi (USD 35 pada konfigurasi dasar), atau pada USD 20 bila efektivitas tinggi (0,6) atau biaya per HOK rendah (Rp150.000):
- FTE berupah 2060–2086 +16,7 (efektivitas 0,6) dan +30,3 (Rp150.000), sedangkan konfigurasi dasar = 0;
- kas LPHD bertahan.

Pada USD 10 tidak pernah, dan pada USD 20 dasar hanya sampai ±2055. Tanpa pembiayaan awal (D3) siklus tidak pernah dimulai pada kondisi mana pun yang diuji (*bootstrap problem*).

**4. Apakah tambahan kas karbon cukup untuk memperkuat LPHD dan KUPS?**

- **USD 20:** tidak. Dana LPHD Rp7,7 M (cakupan kebutuhan 5,2 % pada 2030–2055 dan 0 % sesudah 2060); KUPS +0,3 pada 2087; kapasitas LPHD tetap 0,50.
- **USD 35:** ya menurut model. Dana LPHD Rp214 M, cakupan 90 % pada 2060–2086, KUPS 2087 +44,7.
- Pembiayaan awal sendiri (D1) tidak menambah dana LPHD maupun KUPS.

**5. Konsekuensi terhadap rumah tangga terdampak?**

Pada pengali kehilangan akses 1, setiap tambahan perlindungan, baik dari jembatan maupun penjualan, memperbesar kehilangan akses:

| Harga | Δ pendapatan RT terdampak (Rp/th) |
|---|---|
| USD 20 | −125.222 |
| USD 35 | −496.878 |

Kompensasi tidak ada pada B0. Arah dampak berbalik bila pengali < 0,30 (USD 20). Karena pengali adalah asumsi D, **arah dampak belum dapat diklaim final**. Yang dapat diklaim: beban terkonsentrasi pada ±2.144 (2024) hingga ±3.000 (rerata 2030–2055) pemegang garapan, dan manfaat tunai kegiatan (upah) mengalir ke kelompok yang tidak selalu sama.

**6. Bagian temuan yang didukung data vs proyeksi bersyarat**

| Status | Temuan |
|---|---|
| Didukung data/terverifikasi | Fakta pembiayaan historis 2023–2025 dan HOK; upah patroli; konsistensi internal model (identitas, rekonsiliasi kas, kesetaraan referensi, DT) |
| Proyeksi bersyarat (bergantung C/D) | Semua besaran S2 − S1 dan D1 − D0 / D2 − D1; ambang harga keberlanjutan; arah dampak pendapatan RT; manfaat KUPS; NPV |
| Belum dapat diklaim | Kausalitas empiris; kredit terverifikasi; NPV final; arah kesejahteraan; alokasi optimal per desa; kesetaraan Vensim native |

---

## Temuan per tujuan penelitian

### RQ1: Ekologi

- Paket S2 menambah perlindungan di atas S1: 287 / 454 / 4.954 ha (USD 10 / 20 / 35).
- Pembiayaan awal saja (D1) menghasilkan 287 ha, sebagian besar pada 2025–2030 (196 ha).
- Manfaat karbon bersih D1 turun dari puncak 127 ribu menjadi 82 ribu tCO₂e pada 2087 (non-permanensi).
- Penjualan karbon menambah manfaat yang bertahan hanya bila siklus pembiayaannya mandiri.

### RQ2: Pembiayaan

| Konfigurasi | Hasil |
|---|---|
| D1 (hibah jembatan) | Biaya mitra Rp3,91 M; tanpa beban MRV |
| D2 USD 10 | MRV dan transaksi Rp25,7 M; penerimaan Rp9,9 M; defisit Rp19,0 M ditanggung mitra |
| D2 USD 20 | Mitra nominal −Rp10,1 M (NPV −Rp0,27 M [SEMENTARA]) |
| D2 USD 35 | Mitra +Rp141,4 M; LPHD Rp214 M |
| D3 (tanpa jembatan) | Kerugian MRV Rp22,8 M (Rp2,9 M dengan aturan henti) |

Kredit model tidak dihitung sebagai pendapatan sebelum terjual dan kasnya diterima.

### RQ3: Sosial-ekonomi

- Upah tunai tambahan USD 20: Rp4,65 M, dari jembatan (dibayar mitra) Rp2,26 M dan dari kas LPHD Rp2,40 M. Kontribusi sukarela tidak dihitung sebagai tunai.
- Kerja berupah sesudah 2060 hanya pada USD 35.
- KUPS hanya menguat pada USD 35.
- Pendapatan RT bersyarat pada pengali akses.

### RQ4: Distribusi

- Penjualan sesudah jembatan menambah dana LPHD hanya bila harga ≥ ±USD 15–20. Dana itu memperkuat KUPS dan mempertahankan perlindungan hanya pada USD 35.
- Kompensasi hanya mungkin bila ada dana LPHD (lihat eksperimen alokasi Fase 4).
- Ketergantungan pada mitra tetap tinggi pada USD ≤ 20: mitra membiayai jembatan dan menalangi defisit MRV. Pada USD 35 ketergantungan berkurang, karena LPHD membiayai patroli sendiri sejak 2032.

## Keterbatasan

1. Vensim native belum diverifikasi.
2. Parameter kelas D menentukan besaran dan arah sebagian temuan (lihat register).
3. Jembatan adalah asumsi eksperimen. Komitmen dan kontrak mitra tidak tersedia.
4. Aturan MRV dan *reversal* adalah aturan model.
5. NPV belum memuat biaya pengembangan dan material.
6. Satuan populasi: pekerja SDA = RT (proksi); pemegang garapan = RT; keduanya tumbuh mengikuti penduduk.
7. Hasil berlaku untuk agregat 25 HD, bukan per desa.
8. Tidak ada indikator kemiskinan atau ketimpangan.

## Saran pengumpulan data (prioritas untuk validasi)

1. Realisasi biaya patroli per komponen 2024–2025.
2. Komitmen pembiayaan mitra pasca-2025 dan ketentuan bagi hasil/talangan.
3. Anggaran MRV dan biaya pengembangan proyek.
4. Survei kehilangan pendapatan pemegang garapan.
5. Daftar RT bergantung hutan dan RT unik pemegang garapan.
6. Data keuangan KUPS 2024–2025.
7. Units Check dan run Vensim native.
"""
for n, t in D.items(): open(f"fase7/out/{n}", "w").write(t)
print("ok")
