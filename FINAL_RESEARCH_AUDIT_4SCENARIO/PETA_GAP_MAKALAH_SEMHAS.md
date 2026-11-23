# Peta Gap Makalah Seminar Hasil (versi bertanda tangan, 6 November 2026)

**Berkas yang diperiksa:** `MAKALAH_SEMHAS_REVOLIA_AZ-ZAHRA-signed.pdf` (12 halaman, md5 58127e59…).

**Kesamaan dengan versi yang sudah diaudit:**
- Teks hasil `pdftotext` identik baris per baris dengan versi yang sudah diaudit (md5 e74fdbdb…).
- Perbedaannya hanya tanda tangan (AcroForm).
- Seluruh temuan angka di `MANUSCRIPT_CORRECTION_TABLE.md` (kode A1–F6) dan `CRITICAL_FINDINGS_FINAL.md` tetap berlaku untuk versi ini.

**Cakupan dokumen ini:**
- Dokumen ini **tidak mengulang** koreksi angka dan label; bagian itu cukup dirujuk dengan kodenya.
- Yang dipetakan di sini adalah gap **argumen, metode, pembahasan, pustaka, dan struktur**, yaitu hal yang biasanya ditanyakan penguji dan perlu ditutup saat revisi menuju tesis atau artikel.

**Acuan:**
- Checklist skill seminar hasil PWD (contoh makalah Tika).
- PPKI IPB edisi 4.
- Hasil audit model S1–S4 di folder ini.
- Tidak ada model atau hasil S1–S4 yang diubah.

**Status yang dipakai:**
- **REVISI**: perlu diubah.
- **TAMBAH**: bagian belum ada.
- **BELUM DIVERIFIKASI**: bukti tidak tersedia di paket.
- **PASS**: sudah memadai.

---

## Ringkasan prioritas

| Prioritas | Gap | Bagian | Status |
|---|---|---|---|
| 1 | Basis kredit (baseline = S1, A1) tidak dijelaskan di Metode dan tidak dibahas. Padahal 68 % kredit A1 berasal dari efek PS yang sudah berjalan sejak 2017 | Metode, Hasil 2, Simpulan | TAMBAH |
| 2 | Makna "USD 28,04 / cakupan kebutuhan minimum" keliru tafsir | Abstrak, Hasil 2, Simpulan | REVISI (D1–D4) |
| 3 | Tidak ada subbagian keterbatasan penelitian | Sebelum Simpulan | TAMBAH |
| 4 | Bukti validasi (MAPE, Monte Carlo, PRCC, 413.000 nilai) tidak terlampir, tetapi dipakai sebagai dasar klaim "konsisten" | Metode, Hasil, Simpulan | BELUM DIVERIFIKASI (F1–F4) |
| 5 | *Research gap* dan kebaruan tidak dinyatakan eksplisit | Pendahuluan | TAMBAH |
| 6 | Dimensi "pembangunan perdesaan" (judul, prodi PWD) belum dioperasionalkan | Pendahuluan, Pembahasan, Saran | REVISI |
| 7 | Tabel parameter kunci dan definisi skenario belum lengkap (S1, kalibrasi BAU, harga konstan, NPV parsial) | Metode | TAMBAH |
| 8 | Label sosial-ekonomi (5.328, FTE "orang", upah) | Metode, Tabel 4, Hasil 3 | REVISI (A1, B1, B3) |
| 9 | Sumber primer tidak masuk Daftar Pustaka; literatur karbon dan regulasi Indonesia belum ada | Daftar Pustaka | TAMBAH |
| 10 | Klaim RQ4 (R1 dominan) di Abstrak dan Simpulan tidak dapat diperiksa audit 4 skenario | Abstrak, Hasil 4, Simpulan | BELUM DIVERIFIKASI |

---

## 1. Judul, abstrak, dan identitas

| No | Gap | Bukti di naskah | Usulan | Status |
|---|---|---|---|---|
| 1.1 | Judul menjanjikan "strategi pembangunan perdesaan", tetapi isi mengukur perlindungan hutan, kelayakan proyek, HOK, KUPS, dan pendapatan RT agregat. Tidak ada keterkaitan dengan perencanaan desa/daerah selain di Saran | hlm. 1; Saran | Lihat 2.3. Alternatif: pertahankan judul tetapi tambahkan satu paragraf pembahasan "implikasi bagi perencanaan pembangunan desa" yang mengaitkan kebutuhan LPHD Rp 5,42 miliar/th dengan sumber pendanaan desa. Jangan menambah analisis baru | REVISI |
| 1.2 | Abstrak menulis "*average minimum management funding was covered only at about USD 28*" | Abstrak | Ganti sesuai D1: *"total LPHD spending matched the modelled minimum requirement only at about USD 28, while spending on the minimum components themselves reached 25 % of the requirement at USD 20"* | REVISI |
| 1.3 | Abstrak menulis "*Employment increased*" tanpa satuan | Abstrak | *"Paid and voluntary workload increased (13.6 → 32.8 full-time equivalents at USD 20; not a headcount)"* | REVISI |
| 1.4 | Abstrak menyatakan efek karbon 535 / 3.588 ha tanpa syarat basis kredit | Abstrak | Tambah *"under a crediting baseline equal to the no-active-PS scenario"*; lihat C5 | REVISI |
| 1.5 | Kalimat R1 di abstrak adalah klaim RQ4 yang buktinya (1.000 pengulangan berpasangan) tidak ada di paket | Abstrak | Pertahankan hanya bila berkas eksperimen alokasi dilampirkan; lihat 6.1 | BELUM DIVERIFIKASI |
| 1.6 | Baris penulis tanpa koma; superskrip ² rusak | hlm. 1 | F6 | REVISI |
| 1.7 | Struktur heading (Pendahuluan–Daftar Pustaka), ABSTRACT bahasa Inggris, dan Keywords | – | Sesuai contoh PWD | PASS |

## 2. Pendahuluan

| No | Gap | Bukti | Usulan | Status |
|---|---|---|---|---|
| 2.1 | **Research gap tidak dinyatakan.** Paragraf 3 hanya menyatakan hasil literatur beragam (Santika 2017 vs Kraus 2021), lalu langsung ke metode | hlm. 1–2 | Tambah 2–3 kalimat yang menyatakan apa yang belum diketahui. Contoh rumusan yang konsisten dengan desain model (bukan klaim bahwa belum ada studi sama sekali; itu perlu ditelusuri): "Kajian terdahulu umumnya menilai PS atau imbal jasa karbon secara terpisah dan pada satu titik waktu; hubungan berulang antara penerimaan karbon, belanja lembaga pengelola, dan kegiatan perlindungan belum banyak dikaji secara dinamis pada tingkat gabungan Hutan Desa [PERLU DIISI: 2–3 rujukan yang mendukung]" | TAMBAH |
| 2.2 | **Kebaruan atau kontribusi tidak disebut.** Kontribusi riil yang didukung hasil: (a) pemisahan bertahap efek PS, pembiayaan awal, dan karbon (S1→S4); (b) pemisahan kelayakan proyek dari kecukupan dana lembaga | hlm. 2 | Satu kalimat kontribusi setelah tujuan | TAMBAH |
| 2.3 | Kerangka pembangunan perdesaan (PWD) tipis. Ostrom (2009) dan Sterman (2000) dipakai untuk SD, tetapi tidak ada konsep pembangunan perdesaan atau penghidupan yang menjadi lensa indikator RQ3 | hlm. 2 | Tambah satu paragraf yang mengaitkan indikator (kerja, usaha KUPS, pendapatan RT, dana kelembagaan) dengan kerangka penghidupan atau pembangunan perdesaan yang dipakai dalam tesis [PERLU DIISI: rujukan yang benar-benar dipakai di proposal/tesis] | TAMBAH |
| 2.4 | Angka konteks Hansen 17.183 ha (2001–2024) setara ±716 ha/th kehilangan tutupan pohon bruto. Laju deforestasi BAU model 494 ha/th (rerata 2030–2055) dan 522 ha pada 2024. Selisih ini tidak dijelaskan dan akan ditanyakan | hlm. 1 vs hlm. 6 | Jelaskan di Metode: definisi hutan model vs tutupan pohon, pengaruh kebakaran 2015–2016, dan periode kalibrasi (F5). Ini permintaan penjelasan, **bukan** temuan kesalahan | REVISI |
| 2.5 | "Menopang penghidupan 72.516 penduduk", tetapi model memakai 5.328 RT bergantung. Hubungan kedua angka tidak dijelaskan | hlm. 1, 2 | Sebut sumber 72.516 dan bahwa 5.328 adalah estimasi kelas D (A1) | REVISI |

## 3. Metode penelitian

| No | Gap | Bukti | Usulan | Status |
|---|---|---|---|---|
| 3.1 | **Basis kredit tidak dijelaskan.** Kredit dihitung terhadap baseline internal yang identik dengan S1, tanpa uji adisionalitas terhadap PS reguler (`Switch Baseline Kredit Konservatif = 0`). Ini penentu terbesar hasil RQ2: A1 535 ha vs A2 register 31 ha pada USD 10 | Tidak ada di Metode | Tambah 2–3 kalimat definisi basis kredit, rantai kebocoran 10 %, buffer 12 %, porsi areal 0,682, jeda 3 tahun, penjualan 70 %/th, dan kedaluwarsa 10 %/th. Lihat C1–C6 dan `A1_A2_BASELINE_RECONCILIATION.csv` | TAMBAH |
| 3.2 | Definisi S1 ambigu. "Tanpa PS aktif" sebenarnya berarti kegiatan PS berhenti mulai 2024, bukan kondisi tanpa PS sejak 2017 | Tabel 3 | Ubah kolom intervensi S1 | REVISI |
| 3.3 | Kalibrasi laju BAU tidak dijelaskan (data, periode, metode). Gambar 2 menyebut kalibrasi 2001–2014 | hlm. 4; Gambar 2 | Satu paragraf kalibrasi; seragamkan periode (F5) | TAMBAH |
| 3.4 | Tidak ada tabel parameter kunci (nilai, satuan, sumber, kelas bukti). Minimal untuk: efektivitas 0,37; biaya patroli/hari; biaya MRV tetap; porsi 60/40; porsi alokasi LPHD; pengali akses; pendapatan dasar RT; diskonto 10 % | – | Tabel 3 baru atau lampiran; nilai diambil dari `.mdl` (`00_SOURCE_INVENTORY/traceability_matrix.csv`) | TAMBAH |
| 3.5 | Harga karbon dianggap konstan selama 2024–2086 dan tidak disebut sebagai asumsi | Tabel 3 | Sebut eksplisit sebagai asumsi dan keterbatasan | REVISI |
| 3.6 | NPV proyek bersifat parsial: tanpa biaya pengembangan proyek, diskonto 10 %, PV kontinu. Komponen NPV tidak dijelaskan dan dihitung di luar model | Tabel 4 | D5 | REVISI |
| 3.7 | Horizon 2087 tidak dijustifikasi (periode kredit proyek? umur model?) | hlm. 4 | [PERLU DIISI: dasar horizon, mis. periode proyek di PDD] | TAMBAH |
| 3.8 | 25 HD dengan SK 2017–2024 diagregasi menjadi satu unit. Kemboja baru ber-SK pada 2024 tetapi diperlakukan sama dalam agregat (perlakuan per HD tidak dapat diperiksa dari model agregat). Heterogenitas antardesa tidak dimodelkan | Tabel 1 | Nyatakan sebagai keterbatasan. Klasterisasi desa di luar cakupan dan tidak perlu ditambahkan | REVISI |
| 3.9 | Validasi perilaku hanya MAPE stok pada 2 titik (2019, 2024). MAPE aliran Hansen (73,3 %; lebih buruk dari pembanding 60,4 %) tidak dilaporkan. Hasil uji kondisi ekstrem tidak dilaporkan, padahal disebut dilakukan | hlm. 5–6 | Laporkan apa adanya sebagai keterbatasan; F3; `VALIDATION_EVIDENCE_GAPS.md` §1–2 | REVISI |
| 3.10 | 13 parameter Monte Carlo dan sebarannya tidak disebut | hlm. 5 | Daftar parameter dan sebaran (dari skrip asli) [PERLU DIISI] | BELUM DIVERIFIKASI |
| 3.11 | Uji putus loop (dana→patroli) adalah uji struktur yang kuat tetapi hanya muncul sebagai angka di Hasil, dan variabel yang diputus tidak disebut (naskah −9 ha; audit −13 ha) | hlm. 7 | Pindahkan ke Validasi; sebut variabelnya (T31) | REVISI |
| 3.12 | "Verifikasi Vensim–PySD" dilaporkan; pemisahan verifikasi numerik dan validasi perilaku sudah benar | hlm. 5 | Ganti angka 413.000 dengan F2 bila berkasnya tidak ada | PASS dengan REVISI angka |

## 4. Hasil dan pembahasan

| No | Gap | Bukti | Usulan | Status |
|---|---|---|---|---|
| 4.1 | **Adisionalitas dan risiko kelebihan kredit tidak dibahas.** 24 dari 25 HD ber-SK sebelum proyek; kredit A1 memuat efek PS (68 %) dan pembiayaan awal (11 %) pada USD 10. Penguji bidang karbon hampir pasti menanyakan ini | Hasil 2 | Satu paragraf pembahasan: hasil A1 vs A2 register, syarat validitas masing-masing (apakah patroli swadaya berlanjut tanpa proyek), dan kepatuhan metodologi standar = belum diuji | TAMBAH |
| 4.2 | Permanensi atau pembalikan (*reversal*) dan kebocoran hanya berupa faktor tetap; tidak dibahas | Hasil 2 | Satu kalimat keterbatasan | TAMBAH |
| 4.3 | Kredit diajukan, terbit, dan terjual disamakan | Tabel 4; hlm. 7 | C1–C4 | REVISI |
| 4.4 | Tafsir cakupan LPHD (11,8 %, 49,7 %, 100 % pada USD 28,04) | hlm. 7–8 | D2–D4; `LPHD_FINANCIAL_COVERAGE.csv` | REVISI |
| 4.5 | Efek pembiayaan awal: naskah "tidak berlanjut setelah 2025", padahal efeknya +345 ha (2025–2036) dan −69 ha (2037–2086) | hlm. 7 | E4 | REVISI |
| 4.6 | Pembandingan dengan literatur tipis dan hanya kualitatif. Tidak ada pembanding besaran: biaya per ha dihindari, rasio biaya MRV terhadap penerimaan, efektivitas patroli di Indonesia | Hasil 1–3 | Tambah pembanding yang dapat diverifikasi [PERLU DIISI rujukan]. Jangan menambah angka tanpa sumber | TAMBAH |
| 4.7 | Hasil RQ3 tidak membedakan pemanfaatan hutan legal dan ilegal; "kehilangan akses" bisa berarti hilangnya pendapatan dari aktivitas pemicu deforestasi | hlm. 8–9 | Satu kalimat kualifikasi (sudah ada di `09_SEMINAR_FINDINGS` §5) | TAMBAH |
| 4.8 | Pendapatan dasar RT Rp 41,25 juta berasal dari satu studi di lanskap Padang Tikar (Setiawan et al. 2021) tetapi dipakai untuk 25 HD | hlm. 8 | Sebut sebagai keterbatasan | REVISI |
| 4.9 | Label FTE, upah, dan 5.328 | hlm. 8, Tabel 4 | A1, B1–B4 | REVISI |
| 4.10 | Pernyataan bahwa model tidak mengukur kemiskinan atau ketimpangan | hlm. 9 | Sudah tepat | PASS |
| 4.11 | **Tidak ada subbagian keterbatasan.** Contoh makalah PWD mencantumkan keterbatasan sebelum Simpulan | – | Tambah subbagian "Keterbatasan Penelitian" (draf di §8) | TAMBAH |

## 5. Simpulan dan saran

| No | Gap | Usulan | Status |
|---|---|---|---|
| 5.1 | Simpulan 1: "Arah pengurangan ini konsisten dalam uji ketidakpastian" bergantung pada berkas Monte Carlo yang tidak ada | "… arah pengurangan bertahan pada seluruh uji efektivitas perlindungan 0,075–0,59 (rentang 299–2.799 ha) [REPRODUKSI AUDIT]". Kalimat Monte Carlo dipertahankan hanya bila berkasnya dilampirkan | REVISI |
| 5.2 | Simpulan 2: efek karbon tanpa syarat basis kredit; "tercakup secara rata-rata sekitar USD 28" | Tambah syarat A1 dan sebutkan sensitivitas A2 register (31 / 192 ha); ganti tafsir USD 28 sesuai D4 | REVISI |
| 5.3 | Simpulan cenderung mengulang angka, bukan menjawab tujuan secara analitis | Awali tiap paragraf dengan jawaban tujuan (mis. "PS berkontribusi melalui kegiatan patroli, bukan izin semata …"), lalu satu angka pendukung | REVISI |
| 5.4 | Saran tidak memuat arahan penelitian lanjutan, padahal ada beberapa asumsi kunci yang belum diukur | Tambah: (a) pengukuran efektivitas patroli di 25 HD; (b) survei pemanfaatan hutan oleh pemegang garapan; (c) uji kesesuaian basis kredit dengan metodologi standar dan PDD; (d) validasi aliran deforestasi | TAMBAH |
| 5.5 | Saran kebijakan belum merujuk instrumen regulasi karbon atau PS Indonesia | Rujuk regulasi yang benar-benar berlaku (lihat 7.3) | REVISI |

## 6. RQ4: eksperimen alokasi

| No | Gap | Status |
|---|---|---|
| 6.1 | Eksperimen alokasi (B0–B4, R1–R2) berada di luar cakupan audit 4 skenario. Di paket hanya ada 1 ekspor eksperimen alokasi; berkas 1.000 pengulangan berpasangan dan 22 kombinasi sensitivitas tidak ada. Klaim "R1 tidak mengurangi deforestasi dihindari" dan "dominasi lemah 99,9–100 %" **tidak saya nilai salah**, tetapi juga tidak dapat diverifikasi | BELUM DIVERIFIKASI |
| 6.2 | Semua hasil alokasi dihitung pada basis kredit A1. Pada A2 register, dana LPHD jauh lebih kecil (belanja/kebutuhan USD 20: 12,4 % pada varian diagnostik), sehingga besaran kompensasi R1 kemungkinan berubah. Ini **dugaan dari struktur model, belum diuji** | BELUM DIVERIFIKASI |
| 6.3 | Pernyataan "R1 bukan rumusan optimal untuk semua desa" dan "hanya tujuh alternatif diuji" | PASS (bahasa sudah terukur) |

## 7. Daftar pustaka dan sumber

| No | Gap | Usulan | Status |
|---|---|---|---|
| 7.1 | Kecocokan sitasi dan Daftar Pustaka: 18 sitasi pengarang–tahun di teks, semuanya ada di Daftar Pustaka | – | PASS |
| 7.2 | Sumber primer dikutip di Tabel 1, Tabel 2, dan teks tetapi tidak ada di Daftar Pustaka: Dokumen Desain Proyek (PDD), laporan pemantauan MR1, Laporan Kajian Identifikasi NKT tiga lanskap, Laporan Pendampingan SAMPAN Kalimantan, PP 36/2024 | Tambahkan sebagai entri dokumen atau laporan tak terbit sesuai PPKI [PERLU DIISI: penerbit, tahun, judul resmi] | TAMBAH |
| 7.3 | Tidak ada rujukan regulasi nilai ekonomi karbon dan perdagangan karbon sektor kehutanan Indonesia. Calon yang perlu dicek keberlakuan dan nomornya sebelum dipakai: Perpres 98/2021 tentang Nilai Ekonomi Karbon dan peraturan menteri turunannya | Telusuri dan kutip versi berlaku | BELUM DIVERIFIKASI |
| 7.4 | Tidak ada rujukan metodologi standar karbon (VCS dan metodologi REDD yang dipakai PDD; register menyebut VM0048) | Sebut metodologi PDD bila dibahas di 3.1 / 4.1 [PERLU DIISI] | TAMBAH |
| 7.5 | Tidak ada rujukan studi system dynamics untuk REDD+, karbon hutan, atau PS sebagai pembanding metode | 2–3 rujukan [PERLU DIISI] | TAMBAH |
| 7.6 | Sumber biaya MRV dan biaya patroli per hari tidak dikutip | Kutip sumber parameter (3.4) | TAMBAH |

## 8. Draf subbagian "Keterbatasan Penelitian" (siap disunting)

> **Keterbatasan Penelitian**
>
> Hasil penelitian ini merupakan simulasi bersyarat asumsi, bukan dampak kausal yang teramati.
>
> Pertama, parameter efektivitas perlindungan 0,37 diambil dari studi di Nepal dan belum diukur di 25 Hutan Desa. Dalam rentang 0,075–0,59, deforestasi yang dihindari oleh PS berkisar 299–2.799 ha.
>
> Kedua, kredit model dihitung terhadap baseline yang identik dengan skenario tanpa PS aktif. Kredit tersebut karena itu turut mencakup efek patroli swadaya dan pembiayaan awal. Bila kredit dibatasi pada pengurangan di atas PS reguler, tambahan perlindungan dari karbon turun dari 535 menjadi 31 ha pada USD 10, dan dari 3.588 menjadi 192 ha pada USD 20. Kesesuaian kedua basis dengan metodologi standar karbon belum diuji. Kredit model bukan kredit terverifikasi.
>
> Ketiga, harga karbon diasumsikan tetap selama 2024–2086, sedangkan kebocoran (10 %) dan buffer (12 %) diperlakukan sebagai faktor tetap; pembalikan tidak dimodelkan.
>
> Keempat, validasi historis terbatas pada stok hutan 2019 dan 2024; aliran kehilangan tutupan pohon tahunan belum direproduksi dengan baik [lengkapi bila berkas MAPE aliran tersedia].
>
> Kelima, 25 Hutan Desa dianalisis secara agregat, sehingga perbedaan antardesa tidak tergambar.
>
> Keenam, jumlah rumah tangga bergantung, pendapatan dasar rumah tangga (satu studi di Padang Tikar), dan kehilangan pendapatan akibat pembatasan akses merupakan estimasi atau asumsi. Model tidak membedakan pemanfaatan hutan legal dan ilegal.

Semua angka dalam draf ini berasal dari reproduksi audit (`01`, `07`, `A1_A2_BASELINE_RECONCILIATION.csv`). Tidak ada angka baru.

## 9. Format (contoh PWD dan PPKI)

| Butir | Status | Catatan |
|---|---|---|
| Halaman identitas seminar, judul Indonesia dan Inggris, catatan afiliasi | PASS | Kecuali baris penulis (F6) |
| Tabel bernomor, judul di atas; gambar bernomor, judul di bawah; semua dirujuk di teks | PASS | Gambar 1–7 dan Tabel 1–4 dirujuk |
| Satuan di Tabel 4: "Pekerja setara penuh (orang)" | REVISI | B1 |
| Desimal koma, ribuan titik | PASS | Pengecualian wajar di ABSTRACT bahasa Inggris |
| Spasi angka–satuan tidak konsisten ("USD10" vs "USD 10"; "Rp1,77" vs "Rp 1,77") | REVISI | Seragamkan sesuai PPKI |
| Tabel 2 berlabel "RQ" | REVISI | Ganti "Tujuan 1–4" agar konsisten dengan Pendahuluan |
| Saran terpisah dari Simpulan | PASS | Contoh PWD tidak memisahkan, tetapi pemisahan tidak dilarang |
| Margin, huruf, dan render DOCX | BELUM DIVERIFIKASI | Hanya PDF yang tersedia |
