# Laporan Audit Akademik Makalah Seminar Hasil (Final, Dua Skenario)

**Tanggal:** 4 November 2026

**Naskah:** `MAKALAH_SEMINAR_HASIL_FINAL_2SKENARIO.md` / `.docx`, dengan render periksa `.pdf`.

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD_v2_1.mdl` (md5 `66a7fad8…`) dan `…_v2_1_ALOKASI.mdl` (md5 `cd99d60f…`).
- Keduanya tidak diubah; md5 diperiksa ulang sesudah penulisan.
- Tidak ada simulasi baru yang dijalankan.

**Status hasil:**
- Terverifikasi PySD.
- **Vensim native BELUM DIVERIFIKASI.**
- **NPV SEMENTARA.**

## 1. Keputusan

**SIAP DITELAAH PEMBIMBING, dengan empat butir yang harus dilengkapi peneliti (bagian 6).**

| Aspek | Hasil |
|---|---|
| Panjang | 10 halaman A4 pada render LibreOffice; Word dapat berbeda ± beberapa baris |
| Tujuan | Keempat tujuan dijawab |
| Angka | 106 angka naskah dibaca ulang dari workbook dan semuanya ditemukan dengan format yang sama |
| Sitasi | 15 sitasi = 15 entri daftar pustaka |
| Larangan istilah | Tidak ada pelanggaran |

## 2. Inventarisasi sumber (Tahap 1)

| Sumber yang diminta | Status | Tindakan |
|---|---|---|
| `MAKALAH SEMHAS_REVOLIA AZ-ZAHRA(2).pdf` | **Tidak ditemukan** di repositori maupun di ruang kerja (pencarian nama di seluruh sistem berkas) | Dipakai makalah asli terdekat yang tersedia, yaitu `Makalah_Seminar_Hasil_Kalimantan_Barat_REVISI3.docx/.pdf` (versi empat skenario, 10 halaman) |
| Model v2.1 dan v2.1 ALOKASI | Ada; dibekukan | Hanya dibaca |
| 11 laporan final (Fase 4, Fase 4 lanjutan, Audit Akademik, Fase 5) | Ada | Dipakai sebagai acuan keputusan dan rekonsiliasi |
| 6 workbook primer | Ada | Dibaca langsung lewat `skrip/makalah_final/data.py` |
| Pedoman format | Contoh Tika (aset skill) dan PPKI IPB | Format mengikuti makalah asli (REVISI3); lihat bagian 5 |

**Bagian makalah asli yang dipertahankan:**
- identitas penulis/pembimbing beserta catatan kaki afiliasi;
- ABSTRACT bahasa Inggris dan *Keywords*;
- sistematika PENDAHULUAN – METODE PENELITIAN – HASIL DAN PEMBAHASAN – Keterbatasan – SIMPULAN DAN SARAN – DAFTAR PUSTAKA;
- gaya sitasi pengarang–tahun;
- fakta wilayah (luas SK, lanskap, tutupan 2024, penduduk, kehilangan tutupan 2001–2024);
- peta lokasi;
- referensi yang masih relevan.

**Bagian yang diperbarui:**
- desain skenario (empat → dua skenario + diagnostik D0–D3);
- mekanisme kredit;
- validasi;
- seluruh hasil, simpulan, dan saran;
- diagram model;
- semua tabel dan Gambar 2–7.

**Bagian yang dihapus:**
- angka empat skenario;
- klaim patroli swadaya 2024 dan 2.355 HOK;
- klaim R1 sebagai alokasi terbaik;
- ambang USD 6,83 dan USD 28;
- referensi Lewis (1982), Sze et al. (2022), dan Setiawan et al. (2021) yang tidak lagi disitasi.

## 3. Audit kontrol kualitas (bagian K instruksi)

| No | Butir | Status | Bukti |
|---|---|---|---|
| 1 | Seluruh tujuan terjawab | PASS | Empat subbab hasil dan empat paragraf simpulan, masing-masing satu tujuan; matriks keterlacakan |
| 2 | Definisi S1–S2 konsisten | PASS | Metode "Formulasi Skenario", Tabel 1, dan Tabel 2 memakai definisi yang sama; historis 2023–2025 sama |
| 3 | D0–D3 tidak disebut skenario utama | PASS | Dinyatakan eksplisit "bukan sebagai empat skenario kebijakan baru"; label D1−D0 / D2−D1 sesuai instruksi C |
| 4 | Tidak ada angka empat skenario lama | PASS | Pencarian "2.355", "6,83", "535 ha", "3.588", "1.720": tidak ada |
| 5 | Angka cocok dengan workbook terbaru | PASS | `TABEL_HASIL_FINAL_MAKALAH.xlsx` lembar "Cek angka teks": 106/106 ditemukan |
| 6 | Satuan dan periode konsisten | PASS | Rerata 2030–2055 dan kumulatif 2025–2086 / 2024–2086 dinyatakan pada tabel dan teks |
| 7 | Arus kas mitra sebagai S2 − S1 | PASS | −Rp10,08 miliar (USD 20) dan +Rp142,89 miliar (USD 35) ditulis "arus kas mitra nominal S2 − S1", berdampingan dengan NPV |
| 8 | NPV berlabel sementara | PASS | Label [SEMENTARA] di teks dan Tabel 2; alasannya di Metode |
| 9 | Kredit model ≠ kredit terverifikasi | PASS | Metode, catatan Tabel 2 |
| 10 | Monte Carlo ≠ probabilitas empiris | PASS | "proporsi ensembel"; kata "peluang" tidak dipakai untuk frekuensi ensembel |
| 11 | Asumsi kehilangan akses eksplisit | PASS | Subbab 3.3: "mekanisme asumsi kelas D yang belum divalidasi", titik impas, Gambar 5b |
| 12 | Kas LPHD ≠ pendapatan RT | PASS | Paragraf akhir subbab 3.2 (kas bruto, kas bersih, kas LPHD, uang RT) dan catatan Tabel 2 |
| 13 | R1 tidak disebut optimal | PASS | "R1 bukan alokasi optimal"; kesamaan dengan B0 disebut sebagai konstruksi |
| 14 | Status Vensim native | PASS | Metode "Validasi dan Pengujian" dan Keterbatasan |
| 15 | Sitasi = daftar pustaka | PASS | 15 sitasi, 15 entri; tidak ada sitasi tanpa entri atau entri tanpa sitasi |
| 16 | Tidak ada klaim empiris yang hanya didukung persamaan model | PASS | Mekanisme ditulis "dalam model"/"menurut asumsi"; S2 − S1 disebut proyeksi; pendapatan RT bersyarat |

**Pemeriksaan tambahan:**
- **Frasa terbatas** ("Hasil ini menunjukkan", "Dengan demikian", "Hal ini sejalan dengan", dan lain-lain): 0 kemunculan.
- **Kemiskinan/ketimpangan:** hanya disebut dalam keterbatasan, yaitu bahwa keduanya tidak diukur.
- **Harga USD 35:** dinyatakan bukan patokan harga, baik di Hasil maupun di Saran.
- **Patroli 2023–2025:** dinyatakan dibiayai mitra.

## 4. Rekonsiliasi angka

Semua angka mengikuti keputusan audit terbaru:
- `AUDIT_AKADEMIK_FINAL_PWD.md` §1–§5;
- `TEMUAN_FINAL_DAN_KETERBATASAN_PWD.md` (erratum: arus kas mitra USD 35 = +Rp142,89 miliar sebagai kontras S2 − S1, bukan +141,4 absolut);
- `PERSETUJUAN_FINAL_MODEL_DAN_HASIL_FASE5.md` §6.

| Butir | Keputusan |
|---|---|
| NPV mitra | Dipakai NPV mitra **inkremental** (S2 − S1): −2,82 / −0,27 / +6,66 miliar. NPV mitra absolut S2 (−4,13 / −1,58 / +5,35) tidak dipakai, agar konsisten dengan arus kas S2 − S1 |
| Proporsi ensembel | Dibulatkan satu desimal setengah ke atas dari nilai workbook. Contoh: 22,25 → 22,3; 4,25 → 4,3; 78,25 → 78,3. Ringkasan lama yang menulis 22,2 / 4,2 / 78,2 berbeda hanya karena aturan pembulatan |
| Pengali impas | Dihitung linear dari lembar 5 tabel rekonsiliasi (Δ pada pengali 0 dan 1). Titik audit 0,5; 0,75; dan 1,5 terletak tepat pada garis (diplot di Gambar 5b) |
| Lintasan Gambar 3a/4b | Tahun terpilih dari `HASIL_SIMULASI_FINAL_PWD.xlsx` lembar 3 (13 titik). Puncak 331 ha (2040, USD 10) dan 494 ha (2050, USD 20) adalah nilai pada titik itu, bukan maksimum tahunan eksak |
| Kas penjualan pertama | Ditulis 2029 (2029,12). Kas LPHD pertama: 2034 (2034,06) dan 2032 (2032,75) |
| Angka di luar workbook | Diambil dari laporan yang sudah direkonsiliasi: D3 MRV Rp22,8 miliar dan rentang porsi 8–100 % (Fase 5); upah tunai Rp4,65 miliar dan kehilangan Rp16,32 miliar (Audit Akademik §2); 39/1/1/1 uji, 933/933 satuan, DT ≤ 0,37 %, 15/15, 1.200/1.200, dan 91/91 (Final Gate, Fase 4 lanjutan, Fase 5); rasio validasi 0,98 (Register) |

## 5. Audit format (checklist skill IPB PWD)

| Butir | Status | Keterangan |
|---|---|---|
| Masalah, kesenjangan, tujuan, kontribusi | PASS | Pendahuluan enam langkah argumen, diakhiri tujuan dan kontribusi |
| Data dapat ditelusuri | PASS | Matriks keterlacakan; sumber pada setiap tabel dan gambar |
| Metode dan validasi sesuai bukti | PASS | Termasuk K7 GAGAL dan Vensim BELUM |
| Halaman identitas Seminar Sekolah Pascasarjana | **BELUM DIVERIFIKASI** | Makalah asli (REVISI3) tidak memuat halaman identitas berlogo, sehingga format asli diikuti. Bila panitia mewajibkan halaman identitas seperti contoh Tika, halaman itu perlu ditambahkan dengan jadwal, tempat, dan moderator |
| A4, satu kolom, margin 3 cm | PASS | Diwarisi dari DOCX asli; diperiksa pada render |
| Judul Indonesia/Inggris, penulis, afiliasi | **REVISI** | Nama mahasiswa masih `[NAMA MAHASISWA]` (tidak ada di sumber; tidak dikarang). Judul memakai judul penelitian pada instruksi A. Judul artikel REVISI3 lebih panjang ("… RENDAH KARBON: PENDEKATAN *SYSTEM DYNAMICS* PADA 25 HUTAN DESA …"); pilih salah satu bersama pembimbing |
| ABSTRACT Inggris + Keywords | PASS | 228 kata. Abstrak Indonesia tidak ditambahkan karena makalah asli hanya memakai ABSTRACT |
| Struktur bagian | PASS | Subjudul hasil sesuai empat tujuan |
| Tabel/gambar bernomor dan dirujuk | PASS | Tabel 1–3 dan Gambar 1–7 dirujuk di teks; judul tabel di atas, judul gambar di bawah; header Tabel 2 diulang bila terpotong halaman |
| Ejaan, angka, satuan (PPKI) | PASS | Koma desimal, titik ribuan, tanda minus tipografis, spasi sebelum % |
| Tidak menerapkan aturan AGB | PASS | Satu kolom, Times New Roman, satu abstrak |
| Tidak ada sisa isi/identitas Tika | PASS | Tata letak berasal dari makalah peneliti sendiri |
| Penomoran subbab "2.1, 3.1" | Catatan | Instruksi E/F memakai nomor, tetapi makalah asli dan contoh Tika tidak bernomor. Format asli dipertahankan; urutan dan isi mengikuti 2.1–2.7 dan 3.1–3.4 |

## 6. Hal yang harus dilengkapi peneliti

1. **Nama penulis.** Isi `[NAMA MAHASISWA]` (dan NIM bila diminta panitia). Unggah `MAKALAH SEMHAS_REVOLIA AZ-ZAHRA(2).pdf` bila identitas atau sistematikanya berbeda dari REVISI3.
2. **Halaman identitas seminar.** Tambahkan bila diwajibkan: jadwal, ruang, moderator.
3. **Literatur tambahan (instruksi H).** Topik additionality proyek karbon, pembiayaan konservasi pra-penjualan, *benefit sharing*, dan KUPS/penghidupan belum didukung rujukan baru. Rujukan tidak ditambahkan karena sumbernya tidak dapat diakses dan diverifikasi di sesi ini. Klaim terkait ditulis sebagai hasil model, bukan sebagai temuan literatur. Disarankan menambah 3–5 artikel primer yang sudah dibaca peneliti.
4. **Render Word.** Periksa ulang di Microsoft Word bahwa naskah tetap ≤ 10 halaman. Render LibreOffice menghasilkan tepat 10 halaman, dan pustaka berakhir di halaman 10.

## 7. Keterbatasan audit

- Gaya penulisan belum dikalibrasi terhadap teks asli peneliti; profil gaya di paket tidak menemukan contoh karya peneliti.
- Peta (Gambar 1) dipakai ulang dari makalah REVISI3. Data spasial mentah tidak tersedia di repositori, sehingga batas wilayah tidak dibuat ulang.
- Pemeriksaan angka mencocokkan string angka berformat di naskah. Pencocokan ini membuktikan angka sumber muncul di naskah, tetapi konteks kalimatnya diperiksa manual pada butir yang dipakai sebagai temuan utama.

## 8. Berkas keluaran

| Berkas | Isi |
|---|---|
| `MAKALAH_SEMINAR_HASIL_FINAL_2SKENARIO.md` | Naskah sumber |
| `MAKALAH_SEMINAR_HASIL_FINAL_2SKENARIO.docx` | Word dapat disunting, tata letak makalah asli |
| `MAKALAH_SEMINAR_HASIL_FINAL_2SKENARIO.pdf` | Render periksa (LibreOffice) |
| `TABEL_HASIL_FINAL_MAKALAH.xlsx` | Data Tabel 2–3, data setiap gambar, cek 106 angka |
| `GRAFIK_MAKALAH/` | Gambar 1–7 (PNG 300 dpi) |
| `MATRIKS_KETERLACAKAN_TUJUAN_HASIL.xlsx` | Tujuan → indikator → tabel/gambar → sumber → temuan → kesimpulan → status bukti |
| `../skrip/makalah_final/` | `data.py`, `grafik.py`, `build_docx.py`, `xlsx_makalah.py` (reproduksi penuh) |
