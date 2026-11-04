import json
T = json.load(open("fase5/tabel_md.json"))
STATUS = """**Status verifikasi:**

| Unsur | Status |
|---|---|
| Model | `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (946 variabel); eksperimen alokasi pada `…_v2_ALOKASI.mdl` (964 variabel; satuan 960/960 konsisten; B0 identik dengan v2) |
| Protokol | Referensi S1 berpasangan: lulus pengujian yang telah dilakukan (15/15 konfigurasi gerbang + 1.200/1.200 pasangan MC + 91/91 run alokasi tanpa ketidaksesuaian). Tidak menjamin kesetaraan untuk kombinasi yang belum diuji |
| K7 mode endogen | **GAGAL**; tidak dipakai |
| Vensim native | **BELUM DIVERIFIKASI** |
| NPV | **SEMENTARA** (tanpa biaya pengembangan dan material aktual) |
| Kewajiban *reversal* | Aturan akuntansi model; belum diverifikasi terhadap standar atau kontrak |
| Kredit model | ≠ kredit terverifikasi |

Proporsi ensembel ≠ probabilitas empiris."""
docs = {}
docs["ANALISIS_KETIDAKPASTIAN_PWD.md"] = f"""# Analisis Ketidakpastian: Monte Carlo Berpasangan dan PRCC

**Tanggal:** 4 November 2026

**Data:** `HASIL_MONTE_CARLO_PRCC_PWD.xlsx`. **Grafik:** `GRAFIK_MONTE_CARLO_DAN_BENEFIT_SHARING/M1–M3`.

{STATUS}

## 1. Rancangan

| Unsur | Isi |
|---|---|
| Sampel | Latin Hypercube Sampling, N = 400, seed 20261104 |
| Parameter | 20 parameter; distribusi di lembar 1 |
| Protokol per sampel | Satu run S1 mandiri, lalu S2 mekanisme C pada USD 10, 20, dan 35 dengan tujuh masukan Referensi S1 diambil dari run S1 itu |
| Total | 1.600 run, 1.200 pasangan |

**Parameter yang disampel:**
- keberlanjutan patroli reguler k (0–1);
- efektivitas perlindungan (segitiga 0,2–0,37–0,6);
- laju deforestasi BAU (×0,7–1,3) dan regenerasi (×0,5–1,5);
- biaya patroli total Rp150.000–300.000/HOK (upah Rp150.000 tetap) dan biaya MRV (×0,5–1,5);
- besaran jembatan Rp0,39–1,69 miliar/th (0,5×J1 s.d. JP) dan durasinya (3–8 th);
- jeda penerbitan (2–5 th), jeda pembayaran (0–1 th), dan laju penjualan (0,4–1,0/th);
- pengali kehilangan akses (0–1,5);
- surplus KUPS (×0,7–1,3), porsi reinvestasi (0,25–0,75), dan biaya reaktivasi (Rp12,5–75 juta);
- kapasitas awal LPHD (0,3–0,7) dan pengaruh kapasitas terhadap mutu (0–0,5);
- leakage (0,05–0,2), buffer (0,1–0,2), dan porsi Project Area (0,541–0,903).

Semua rentang adalah asumsi yang dinyatakan (kelas B–D). Proporsi ensembel bergantung pada rentang itu.

**Pemeriksaan pasangan** (lembar 3): 1.200/1.200 pasangan setara.
- Selisih hutan dan emisi Referensi S1 terhadap S1 mandiri = 0.
- Identitas arus kas ≤ 4·10⁻⁶ Rp.
- 0 run gagal.

## 2. Proporsi ensembel

Kriteria ditetapkan sebelum hasil dilihat.

{T['mc_prop']}

## 3. Sebaran hasil

{T['mc_kuantil']}

## 4. PRCC (USD 20; lembar 6 untuk USD 10 dan 35)

{T['mc_prcc']}

**Peran k** (keberlanjutan patroli reguler S1) kecil hingga sedang. Ini karena k menaikkan perlindungan di S1 dan S2 sekaligus, sehingga pengaruhnya pada selisih berpasangan teredam. Pada Fase 3 (kredit terhadap BAU), k adalah penentu utama; dalam mekanisme C tidak lagi.

{T['mc_k']}

## 5. Bacaan

1. **Tambahan perlindungan selalu positif** (100 % ensembel pada semua harga), karena jembatan membiayai patroli tambahan. Besarnya sangat lebar:
   - USD 20: median 682 ha [P5 137; P95 9.233];
   - ditentukan oleh efektivitas perlindungan, besaran dan durasi jembatan, serta biaya per HOK.
2. **Manfaat karbon bersih kumulatif 2087 selalu positif**, tetapi pada USD ≤ 20 umumnya turun lebih dari 10 % dari puncaknya (*reversal*). Bagian ensembel yang tidak turun: 0,5 % (USD 10), 23,8 % (USD 20), 78,2 % (USD 35).
3. **Pembiayaan LPHD jangka panjang** hanya berlanjut pada sebagian kecil ensembel USD 20: kas LPHD masih mengalir 2075–2086 pada 22,2 % ensembel, dan cakupan kebutuhan ≥ 50 % pada 10,8 %. Pada USD 35 angkanya 74,0 % dan 57,2 %. Pada USD 10 praktis tidak pernah.
4. **NPV [SEMENTARA].**
   - NPV inkremental proyek positif pada 13,0 / 65,8 / 95,8 % ensembel (USD 10 / 20 / 35).
   - NPV mitra positif pada 4,2 / 46,8 / 88,8 %.
   - Status biaya: biaya pengembangan proyek = 0 dan biaya material = 0, sehingga NPV ini batas atas.
5. **Pendapatan bersih rumah tangga.**
   - RT bergantung hutan: naik pada 60,0 / 47,5 / 33,8 % ensembel dan turun pada sisanya.
   - RT terdampak: naik hanya pada 25,2 / 19,0 / 14,5 %.
   - Pengali kehilangan akses mendominasi (PRCC −0,89).
6. **KUPS 2087 ≥ 90 % tingkat 2026** pada 15,0 / 24,8 / 62,5 % ensembel S2, dibanding 14,5 % pada S1. Penentunya biaya reaktivasi dan porsi reinvestasi, kecuali pada USD 35 ketika kas karbon cukup besar.

## 6. Keterbatasan

- Distribusi parameter bersifat asumsi.
- Harga diperlakukan sebagai skenario (tiga level), bukan disampel.
- Struktur model tetap; ketidakpastian struktural (bentuk respons patroli, mekanisme kehilangan akses) tidak tercakup.
- Aturan *reversal* dan urutan pemulihan dana mitra tidak divariasikan.
"""
docs["ANALISIS_SOSIAL_EKONOMI_PWD.md"] = f"""# Analisis Sosial-Ekonomi PWD: Pekerjaan, KUPS, dan Ekonomi Rumah Tangga

**Tanggal:** 4 November 2026

**Sumber:**
- deterministik: `HASIL_SIMULASI_FINAL_PWD.xlsx` (Fase 4 Tahap 3);
- Monte Carlo: `HASIL_MONTE_CARLO_PRCC_PWD.xlsx`;
- alokasi: `HASIL_BENEFIT_SHARING_PWD.xlsx`.

{STATUS}

## 1. Manfaat kolektif LPHD ≠ pendapatan tunai rumah tangga

Kas karbon yang masuk ke LPHD adalah **dana kolektif desa**. Dana ini membiayai patroli, rehabilitasi, pengendalian kebakaran, KUPS, operasional, dan penguatan kelembagaan. Hanya sebagian yang menjadi uang tunai rumah tangga, yaitu:
- upah kegiatan berupah (patroli, tanam, kebakaran);
- bagian surplus KUPS yang dibagikan kepada anggota (26,3 %);
- kompensasi, bila dialokasikan.

Kontribusi tenaga sukarela (Rp150.000/HOK) dan logistik bukan pendapatan.

**Aliran kumulatif** (deterministik, B0, tanpa kompensasi):

{T['aliran']}

**Bacaan:**
- Pada C-J1 USD 20, dari Rp29,1 miliar kas penjualan:
  - Rp27,6 miliar habis untuk MRV, transaksi, pajak, dan kredit pengganti;
  - LPHD menerima Rp7,7 miliar;
  - mitra memperoleh Rp5,1 miliar ditambah pemulihan talangan, tetapi tetap menanggung defisit MRV Rp15,2 miliar.
- Tambahan uang tunai bagi rumah tangga Rp4,7 miliar upah dan Rp0,05 miliar penerimaan KUPS. Nilai ini **lebih kecil** daripada tambahan kehilangan pendapatan akibat pembatasan akses (Rp16,3 miliar).
- Pada USD 35 polanya sama dalam skala lebih besar: upah Rp67,0 miliar dan KUPS Rp1,5 miliar, berbanding kehilangan akses Rp254,0 miliar.

## 2. Kesempatan kerja

- **Patroli reguler (sukarela)** 1.506 HOK/th (5,0 FTE) sama di S1 dan S2. Seluruh tambahan kerja S2 adalah kerja **berupah**: patroli (Rp150.000/HOK), penanaman, dan pengendalian kebakaran (Rp130.000/HOK, belum dikonfirmasi).
- **Deterministik C-J1:** +0,4 / +2,7 / +17,4 FTE berupah 2030–2055 (USD 10 / 20 / 35). Sesudah 2060 tambahan itu hanya bertahan pada USD 35.
- **Monte Carlo:** Δ FTE 2030–2055 median 1,2 / 5,0 / 21,2. Kerja tambahan masih ada 2060–2086 hanya pada 1,2 / 31,8 / 82,5 % ensembel.
- FTE adalah setara kerja penuh, **bukan** jumlah orang yang memperoleh pekerjaan.

## 3. KUPS

- **Di S1**, KUPS aktif turun dari 33,4 (2026) menjadi 5,7 pada 2087 (deterministik). Ini akibat biaya reaktivasi Rp50 juta dan porsi reinvestasi 0,5 (kelas D).
- **Pada USD ≤ 20**, S2 hampir tidak mengubah lintasan itu: +0,3 KUPS pada 2087 di C-J1 USD 20, dengan penerimaan anggota +Rp1,4 juta/th.
- **Pada USD 35**, KUPS 2087 naik ke 50,4 dan penerimaan anggota +Rp9,0 juta/th.
- **Monte Carlo:** biaya reaktivasi (PRCC −0,82) dan porsi reinvestasi (+0,69) lebih menentukan daripada harga karbon pada USD ≤ 20.
- Omzet bukan penerimaan anggota: yang dibagikan hanya 26,3 % surplus.
- **Sesudah kas karbon menurun** (USD ≤ 20, sesudah ±2050), KUPS mengikuti lintasan S1, karena tidak ada sumber modal pengganti.

## 4. Pendapatan rumah tangga

| Komponen Δ S2 − S1 (C-J1 USD 20, Rp/RT/th) | Nilai |
|---|---|
| Pendapatan hutan (ketersediaan sumber daya membaik) | +52.266 |
| Pendapatan program (upah × 0,5 + penerimaan KUPS) | +2.086 |
| Kehilangan akses | −72.261 |
| **Pendapatan bersih RT bergantung** | **−17.909** (pada pengali akses 0: +54.352) |
| Kompensasi (B0) | 0 |

- **RT terdampak** (±3.000 RT pemegang garapan) menanggung kehilangan Rp408 ribu/RT/th pada C-J1 USD 20, dibanding Rp228 ribu di S1.
- **Monte Carlo:** pendapatan RT terdampak naik hanya pada 25,2 / 19,0 / 14,5 % ensembel. Penentunya pengali kehilangan akses (PRCC −0,89).
- Pengali kehilangan akses adalah asumsi kelas D. Data garapan, nilai hasil hutan yang hilang, dan kepatuhan belum tersedia.
- Model tidak memiliki indikator kemiskinan atau ketimpangan, sehingga **tidak ada klaim** tentang keduanya.

## 5. Kelembagaan LPHD

- **Kapasitas LPHD** tetap 0,50 pada USD ≤ 20 (deterministik) dan naik ke 0,86–0,87 pada USD 35. Monte Carlo: median 0,52 (USD 20) dan 0,80 (USD 35).
- **Ketergantungan:** tanpa kas non-karbon, 100 % dana LPHD berasal dari karbon.
- **Penundaan manfaat:**
  - kas LPHD pertama datang 3–7 tahun sesudah kas penjualan pertama, karena defisit MRV dan talangan mitra dipulihkan lebih dulu;
  - pada USD ≤ 20, kas itu berhenti sebelum ±2050–2060.

  Bagi desa, artinya pengelolaan yang dibangun dengan dana karbon kehilangan pembiayaan ketika kapasitasnya belum terbentuk.
"""
docs["ANALISIS_ALOKASI_MANFAAT_PWD.md"] = f"""# Analisis Alokasi Manfaat dan Kompensasi

**Tanggal:** 4 November 2026

**Data:** `HASIL_BENEFIT_SHARING_PWD.xlsx`. **Grafik:** `GRAFIK_MONTE_CARLO_DAN_BENEFIT_SHARING/A1`.

{STATUS}

## 1. Rancangan

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl` = v2 ditambah dana fleksibel dan kompensasi. Mekanisme C, J1, Referensi S1 berpasangan.

**Alternatif:**

| Alternatif | Patroli | Rehabilitasi | Kebakaran | KUPS | Kompensasi |
|---|---|---|---|---|---|
| B0 | 0,30 | 0,15 | 0,10 | 0,20 | 0 |
| B1 | 0,40 | 0,20 | 0,10 | 0,20 | 0,10 |
| B2 | 0,30 | 0,15 | 0,10 | 0,25 | 0,20 |
| B3 | 0,20 | 0,10 | 0,10 | 0,45 | 0,15 |
| B4 | 0,20 | 0,10 | 0,10 | 0,25 | 0,35 |
| R1 | 0,40 | 0,20 | 2/15 | 1/15 | 0,20 |
| R2 | 0,50 | 0,15 | 0,10 | 0,05 | 0,20 |

- **B0** = alokasi proporsional dasar: porsi di atas adalah porsi dari seluruh dana tersedia, ditambah operasional 0,10 dan kelembagaan 0,15.
- **B1–B4, R1, R2:** operasional dan kelembagaan tetap proporsional. Sisanya menjadi dana fleksibel yang dibagi dengan porsi di atas, masing-masing dibatasi kebutuhan pos.
- **Kompensasi** dibayar dari saldo LPHD (tercatat di `Penggunaan Dana Desa`) dan diterima RT pemegang garapan yang terdampak.

**Konfigurasi run:**
- USD 10, 20, 35;
- sensitivitas pada USD 20: k 0/1, efektivitas 0,2/0,6, akses 0/1,5, biaya patroli Rp150.000/300.000, JP, MRV ×1,5.

**Identitas anggaran** (lembar 6), seluruhnya terpenuhi di 91 run:
- Σ alokasi ≤ dana tersedia (selisih minimum −2·10⁻⁶ Rp);
- penggunaan ≤ dana tersedia;
- saldo ≥ 0;
- neraca saldo seimbang (selisih ≤ 4·10⁻⁴ Rp);
- kompensasi dibayar = diterima RT terdampak.

Kompensasi tidak memakai dana yang sudah dibelanjakan untuk kegiatan lain.

## 2. Hasil

**USD 10:** semua alternatif identik, karena kas karbon tidak pernah sampai ke LPHD (defisit MRV dan talangan menyerap seluruh surplus). Kompensasi = 0. **Alokasi tidak berarti tanpa kas.**

**USD 20 (deterministik)**

{T['alok_20']}

**USD 35 (deterministik)**

{T['alok_35']}

## 3. Uji R1

**Kriteria** (ditetapkan sebelum hasil): R1 lulus bila pendapatan bersih RT terdampak R1 > B0 **dan** deforestasi dihindari R1 tidak lebih buruk dari B0 (toleransi 1 ha). Hasil R1 model empat skenario lama tidak dipakai.

{T['r1']}

**Bacaan:**
- R1 lulus pada 12 dari 13 konfigurasi. Satu-satunya yang tidak lulus adalah USD 10, karena di sana tidak ada kas untuk dialokasikan.
- **Penyebab protektifnya:** dengan dana fleksibel = 75 % dana tersedia, porsi R1 untuk patroli, rehabilitasi, dan kebakaran sama dengan B0 (0,30 / 0,15 / 0,10 dari dana tersedia). Kompensasi R1 diambil seluruhnya dari porsi KUPS (0,20 → 0,05 dari dana tersedia). Jadi perlindungan R1 = B0 menurut konstruksi.
- **Biaya R1 ditanggung KUPS:** penerimaan anggota KUPS turun Rp0,9 juta/th (USD 20) dan Rp6,3 juta/th (USD 35). KUPS aktif 2087 pada USD 35 turun dari 50,4 menjadi 13,6.
- **Besaran kompensasi R1** hanya 3,8 % (USD 20) dan 12,4 % (USD 35) dari kehilangan akses total, atau 7,1 % dan 12,3 % dari tambahan kehilangan S2 − S1.

## 4. Trade-off antaralternatif

| Alternatif | Dampak |
|---|---|
| **R2** (patroli 0,5) | Perlindungan tertinggi (+101 ha USD 20; +1.490 ha USD 35 dibanding B0) dan NPV mitra tertinggi. Tetapi kehilangan akses per RT terdampak juga tertinggi, sehingga pendapatan RT terdampak lebih rendah daripada B0 walau ada kompensasi |
| **B4** (kompensasi 0,35) | Pendapatan RT terdampak tertinggi (+64 ribu USD 20; +420 ribu USD 35 dibanding B0). Tetapi perlindungan turun tajam (USD 35: 553 vs 4.954 ha), siklus pembiayaan mandiri USD 35 terputus, dan kapasitas LPHD tetap 0,50 |
| **B2, B3** | Melemahkan perlindungan pada USD 35 (1.114 dan 553 ha). Tambahan KUPS kecil |
| **B1** | Hampir sama dengan B0 dengan kompensasi kecil (1,9–6,2 % kehilangan) |

## 5. Kesimpulan alokasi

1. **Tidak ada alternatif yang memaksimalkan semua tujuan.** Perlindungan hutan, penerimaan KUPS, dan kompensasi bersaing pada dana LPHD yang sama.
2. **R1 memenuhi syarat uji** (pendapatan RT terdampak naik tanpa memperburuk perlindungan) pada USD 20–35, **dengan biaya pada KUPS**. Klaim lama bahwa R1 unggul tanpa trade-off tidak berlaku.
3. **Kompensasi maksimum** yang diuji hanya menutup 18,9 % kehilangan total (B4, USD 35). Kompensasi dari dana LPHD tidak cukup untuk menetralkan kehilangan akses menurut asumsi model.
4. Hasil berlaku untuk tujuh alternatif ini dan agregat 25 HD. **Bukan** alokasi optimal untuk setiap desa.
"""
docs["RINGKASAN_HASIL_FINAL_TESIS_PWD.md"] = f"""# Ringkasan Hasil Final Tesis

**Judul:** Perhutanan Sosial dan Perdagangan Karbon sebagai Strategi Pembangunan Perdesaan di Kalimantan Barat

**Tanggal:** 4 November 2026

**Cakupan:** 25 Hutan Desa Delta Kapuas; 124.941 ha SK; areal proyek karbon 111.123 ha; horizon 2024–2087.

{STATUS}

**Skenario:**

| Skenario | Isi |
|---|---|
| S1 | PS dengan pembiayaan terbatas |
| S2 | PS dengan perdagangan karbon, mekanisme C: kredit konservatif endogen terhadap Referensi S1 berpasangan + pembiayaan jembatan mitra 2026–2030 |

Hasil S2 − S1 adalah selisih menurut asumsi model, **bukan estimasi kausal empiris**.

Makalah empat skenario **belum direvisi**. Angkanya tidak dipakai sebagai hasil baru.

---

## Pertanyaan pokok

> Dalam kondisi apa perdagangan karbon mampu menambah perlindungan hutan, membiayai pengelolaan LPHD secara berkelanjutan, meningkatkan kesempatan kerja dan ekonomi lokal, serta memberi manfaat yang adil bagi masyarakat desa?

**Jawaban menurut model:**
- Perdagangan karbon dengan kredit konservatif **menambah perlindungan hutan** pada semua kondisi yang diuji, karena pembiayaan jembatan membiayai patroli tambahan.
- Perdagangan karbon **membiayai pengelolaan LPHD secara berkelanjutan hanya pada harga tinggi** (±USD 35) dengan biaya per HOK rendah dan efektivitas perlindungan tinggi.
- **Tidak meningkatkan pendapatan bersih rumah tangga terdampak** pada sebagian besar kondisi, karena manfaat tunai rumah tangga lebih kecil daripada kehilangan akses.
- **Tidak adil** dalam distribusinya tanpa kompensasi, dan kompensasi dari dana LPHD hanya menutup sebagian kecil kehilangan.

## 1. Keberlanjutan perlindungan hutan (RQ1)

- **Deterministik C-J1:** deforestasi dihindari S2 − S1 287 / 287 / 338 / 454 / 4.954 ha (USD 6 / 10 / 15 / 20 / 35). C-JP: 620–7.487 ha.
- **Monte Carlo:** 100 % ensembel menunjukkan tambahan perlindungan; median USD 20 = 682 ha [P5 137; P95 9.233].
- **Tidak berkelanjutan pada USD ≤ 20:** patroli tambahan hilang sebelum 2060, dan sebagian mitigasi kembali hilang (*reversal*). Manfaat karbon bersih yang tidak turun > 10 % dari puncaknya: 0,5 / 23,8 / 78,2 % ensembel (USD 10 / 20 / 35).
- **Penentu** (PRCC): efektivitas perlindungan, besaran dan durasi jembatan, biaya patroli per HOK, laju deforestasi BAU.

## 2. Keberlanjutan pembiayaan dan kelembagaan LPHD (RQ2)

- **Kas LPHD pertama** datang 2032–2036, sesudah defisit MRV dan talangan mitra dipulihkan. Kas karbon tidak sampai ke LPHD pada C-J1 USD 6–10.
- **Kas LPHD 2075–2086** masih mengalir pada 0,5 / 22,2 / 74,0 % ensembel. Cakupan kebutuhan minimum ≥ 50 % pada 0,2 / 10,8 / 57,2 %.
- **NPV [SEMENTARA]** positif: proyek 13,0 / 65,8 / 95,8 %; mitra 4,2 / 46,8 / 88,8 % ensembel. Pada USD ≤ 20 mitra menanggung defisit MRV Rp11–19 miliar.
- **Kapasitas LPHD** naik hanya bila kas berkelanjutan (USD 35: 0,50 → 0,87). LPHD sepenuhnya bergantung pada kas karbon.

## 3. Kesempatan kerja, KUPS, dan ekonomi rumah tangga (RQ3)

- **Kerja berupah:** +2,7 FTE (C-J1 USD 20) s.d. +41,7 FTE (C-JP USD 35) pada 2030–2055. Sesudah 2060 hanya bertahan pada harga tinggi (82,5 % ensembel USD 35; 31,8 % USD 20).
- **KUPS:** tanpa kas yang cukup, KUPS mengikuti penurunan S1 (33,4 → 5,7 pada 2087). Penentunya biaya reaktivasi dan porsi reinvestasi.
- **Pendapatan rumah tangga:** tambahan upah tunai dan penerimaan KUPS lebih kecil daripada tambahan kehilangan akses.
  - Contoh C-J1 USD 20: Rp4,7 miliar + Rp0,05 miliar vs Rp16,3 miliar.
  - Pendapatan RT terdampak naik hanya pada 25,2 / 19,0 / 14,5 % ensembel.
  - Penentu utamanya pengali kehilangan akses (asumsi kelas D).

## 4. Keadilan distribusi manfaat dan kompensasi (RQ4)

| Pihak | Peran dalam model |
|---|---|
| **Penerima manfaat** | Mitra (40 % surplus, pemulihan talangan dan biaya MRV lebih dulu); LPHD sebagai pengelola dana kolektif (60 %); pekerja berupah; anggota KUPS (porsi surplus kecil) |
| **Penanggung biaya** | RT pemegang garapan yang terdampak pembatasan akses (±3.000 RT): kehilangan +Rp96 ribu hingga +Rp1,37 juta/RT/th di atas S1, tanpa kompensasi pada B0. Mitra juga menanggung risiko defisit MRV dan talangan pada harga rendah. Tenaga sukarela patroli (Rp225,8 juta/th setara non-tunai) sama di S1 dan S2 |
| **Alokasi** | R1 meningkatkan pendapatan RT terdampak tanpa memperburuk perlindungan dibanding B0 (lulus 12/13 konfigurasi; tidak berlaku pada USD 10 karena tidak ada kas), tetapi mengurangi dana KUPS. R2 memperkuat perlindungan tetapi memperbesar kehilangan akses. B4 memperbesar kompensasi tetapi melemahkan perlindungan. Kompensasi tertinggi menutup ≤ 18,9 % kehilangan total |

## 5. Kapan manfaat perdagangan karbon tidak berkelanjutan

Menurut model, manfaat tidak berkelanjutan bila salah satu kondisi berikut berlaku:
1. harga di bawah ±USD 30;
2. biaya patroli per HOK tinggi;
3. efektivitas perlindungan rendah;
4. biaya MRV tinggi relatif terhadap kredit konservatif;
5. pembiayaan awal kecil atau singkat;
6. biaya reaktivasi KUPS tinggi dan reinvestasi rendah;
7. kehilangan akses besar tanpa kompensasi.

## 6. Hal yang belum dapat diklaim

- Kredit model sebagai kredit terverifikasi.
- Probabilitas empiris.
- Dampak terhadap kemiskinan atau ketimpangan.
- Alokasi optimal per desa.
- Kesetaraan Vensim native.
- NPV final.
- Kewajiban *reversal* menurut kontrak.

## 7. Data dan keputusan yang masih diperlukan

- Biaya total patroli per HOK dan upah tim kebakaran.
- Komitmen dan kontrak pembiayaan mitra (jembatan, prioritas pemulihan, ketentuan *reversal*).
- Biaya MRV dan biaya pengembangan proyek aktual.
- Data garapan dan nilai kehilangan akses.
- Data KUPS 2024–2025.
- Status pembiayaan mitra 2023–2025 sebagai aktivitas proyek.
- Units Check dan run Vensim native.
"""
for n, t in docs.items(): open(f"fase5/{n}", "w").write(t)
print("ok")
