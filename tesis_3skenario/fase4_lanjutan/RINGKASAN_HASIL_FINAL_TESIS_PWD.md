# Ringkasan Hasil Final Tesis

**Judul:** Perhutanan Sosial dan Perdagangan Karbon sebagai Strategi Pembangunan Perdesaan di Kalimantan Barat

**Tanggal:** 4 November 2026

**Cakupan:** 25 Hutan Desa Delta Kapuas; 124.941 ha SK; areal proyek karbon 111.123 ha; horizon 2024–2087.

**Status verifikasi:**

| Unsur | Status |
|---|---|
| Model | `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (946 variabel); eksperimen alokasi pada `…_v2_ALOKASI.mdl` (964 variabel; satuan 960/960 konsisten; B0 identik dengan v2) |
| Protokol | Referensi S1 berpasangan: lulus pengujian yang telah dilakukan (15/15 konfigurasi gerbang + 1.200/1.200 pasangan MC + 91/91 run alokasi tanpa ketidaksesuaian). Tidak menjamin kesetaraan untuk kombinasi yang belum diuji |
| K7 mode endogen | **GAGAL**; tidak dipakai |
| Vensim native | **BELUM DIVERIFIKASI** |
| NPV | **SEMENTARA** (tanpa biaya pengembangan dan material aktual) |
| Kewajiban *reversal* | Aturan akuntansi model; belum diverifikasi terhadap standar atau kontrak |
| Kredit model | ≠ kredit terverifikasi |

Proporsi ensembel ≠ probabilitas empiris.

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
1. harga di bawah ±USD 30 (ambang siklus mandiri dari analisis Fase 3; pada v2 terkonfirmasi bahwa USD 20 tidak mandiri dan USD 35 mandiri);
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
