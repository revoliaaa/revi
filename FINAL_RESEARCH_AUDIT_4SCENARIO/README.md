# Audit Ilmiah Hasil 4 Skenario (S1–S4): 25 Hutan Desa di Kalimantan Barat

**Tanggal audit:** 4 November 2026
**Cakupan:** model system dynamics basis kredit A1, skenario S1–S4 (harga USD 3/6/10/15/20/35). Eksperimen alokasi manfaat, pemetaan spasial, dan klasterisasi berada di luar cakupan.
**Sifat dokumen:** audit kebijakan berbasis simulasi. Ini bukan evaluasi dampak kausal empiris.

## Konvensi

- Dokumen Markdown memakai koma desimal dan titik ribuan.
- Berkas CSV memakai titik desimal dengan presisi penuh agar dapat dibaca mesin.
- Pembulatan hanya dilakukan untuk penyajian.
- **Fisik** dihitung kumulatif 2025–2086 sebagai integral aliran Euler (DT 0,0625) pada [2025, 2087).
- **Keuangan** dihitung kumulatif 2024–2086 dengan cara yang sama.
- **Indikator tahunan** adalah rerata integral 2030–2055, kecuali jumlah KUPS (lihat 05).
- Semua angka di folder ini berasal dari run ulang PySD 3.14.3 atas salinan berkas `.mdl` di ZIP. Berkas asli tidak diubah.
- Run PySD dicocokkan dengan ekspor `.txt` Vensim untuk tujuh run A1. Variabel kunci berbeda paling besar 7×10⁻⁶ (relatif).

| Folder | Isi |
|---|---|
| `00_SOURCE_INVENTORY` | Inventaris berkas, md5, diff persamaan antar-skenario, matriks keterlacakan |
| `01_ECOLOGICAL_RESULTS` | Hutan, deforestasi, regenerasi, rehabilitasi, emisi, neraca stok-aliran (tahunan dan kumulatif) |
| `02_SCENARIO_COMPARISON` | Dekomposisi S2−S1, S3−S2, S4−S3 (Output 3) |
| `03_CARBON_ACCOUNTING` | Rantai kredit, adisionalitas, diagnostik A2 |
| `04_FINANCIAL_RESULTS` | Arus kas tahunan, NPV proyek dan mitra, cakupan LPHD |
| `05_SOCIOECONOMIC_RESULTS` | HOK/FTE, KUPS, pendapatan RT, uji pengali akses |
| `06_VALIDATION` | Register validasi (Output 4), uji DT, Vensim–PySD, putus loop |
| `07_UNCERTAINTY` | Robustness satu-per-satu (Output 6) |
| `08_MANUSCRIPT_RECONCILIATION` | Rekonsiliasi 35 butir naskah (Output 5) |
| `09_SEMINAR_FINDINGS` | Rumusan temuan siap seminar (Output 7) |
| `code` | Seluruh skrip audit (dapat dijalankan ulang) |
| `FINAL_RESULTS_MATRIX.csv` | Output 2: matriks hasil lengkap dengan klasifikasi bukti |


## Lanjutan audit (4 November 2026)

| Berkas | Isi |
|---|---|
| `CRITICAL_FINDINGS_FINAL.md` | Temuan kritis final: A1/A2, kebutuhan minimum LPHD, label, bukti validasi |
| `A1_A2_BASELINE_RECONCILIATION.csv` | A1, A2 register (direproduksi), dan A2 faktor 1 (diagnostik) per harga |
| `LPHD_FINANCIAL_COVERAGE.csv` | Belanja total vs komponen minimum, kesenjangan, dan cakupan per harga (USD 3–100) |
| `MANUSCRIPT_CORRECTION_TABLE.md` | Kalimat pengganti siap pakai |
| `VALIDATION_EVIDENCE_GAPS.md` | Bukti yang diperlukan untuk MAPE, MC, PRCC, dan Vensim–PySD |

---

## OUTPUT 1 — Tinjauan Ilmiah Eksekutif

### Kredibilitas keseluruhan

**Komputasi: kuat.** Semua angka utama Tabel 4, abstrak, dan teks hasil dapat direproduksi dari berkas model di ZIP, sampai satuan terkecil yang dilaporkan. Ini mencakup NPV, harga impas USD 6,83 dan 7,40, serta ambang USD 28,04, walaupun rumus ketiganya tidak tertulis di naskah. Neraca stok hutan tertutup dengan residu 0 ha. Uji DT lolos. Replikasi Vensim–PySD konsisten.

**Empiris: terbatas.** Validasi historis (MAPE), Monte Carlo, dan PRCC **tidak dapat diverifikasi** dari berkas yang diserahkan. Beberapa besaran kunci, terutama efek karbon, sangat bergantung pada asumsi kelas C/D dan pada definisi baseline kredit.

### Temuan terkuat (robust terhadap uji yang dijalankan)

1. **Arah efek PS (S2 < S1 dalam deforestasi) tidak berubah pada semua uji.** Termasuk efektivitas 0,075, batas bawah dokumentasi. Besarnya berkisar 299–2.799 ha untuk rentang efektivitas 0,075–0,59 (nilai dasar 1.720 ha).
2. **Biaya MRV, verifikasi, dan registri bersifat tetap.** Karena itu kelayakan finansial sangat peka terhadap harga. Pada USD 6, biaya menyerap 80 % penerimaan kotor.
3. **Dana karbon tiba terlambat.** Belanja LPHD baru positif pada 2028,6–2029,9, bergantung harga. Pembiayaan awal S3 menutup sebagian jeda ini, dan efeknya meluruh sampai awal 2030-an.
4. **Perubahan pendapatan rata-rata RT kecil (< 0,5 %) dan tandanya ditentukan asumsi kehilangan akses.** Titik nol pengali akses adalah 0,47 (USD 10) dan 0,40 (USD 20).

### Keterbatasan utama

- **Basis kredit A1 = S1.** Deret "Baseline" internal identik dengan run S1. Kredit model karena itu mencakup efek PS dan pembiayaan awal (68 % + 11 % pada USD 10). Ini menghidupkan loop dana→patroli lebih kuat daripada kredit yang benar-benar aditional.
  - Pada A2 resmi register (paket CLOSURE; switch = 1 dan faktor penutup reversal 0,72–0,76), S4−S3 turun dari 535 ke 31 ha (USD 10) dan dari 3.588 ke 192 ha (USD 20). NPV USD 10 menjadi −2,23 miliar.
  - Pada varian diagnostik audit tanpa faktor penutup (faktor = 1), nilainya 67 ha dan 422 ha, dengan NPV USD 10 −1,35 miliar.
  - **Ralat:** versi awal audit menyebut varian faktor = 1 sebagai "A2". Rinciannya ada di `A1_A2_BASELINE_RECONCILIATION.csv` dan `CRITICAL_FINDINGS_FINAL.md`.
- **Efektivitas perlindungan 0,37 berasal dari studi Nepal (kelas C).** Dokumentasi model sendiri mencatat tidak ada studi yang menghubungkan intensitas patroli komunitas dengan laju kehilangan hutan.
- **S1 bukan "tanpa PS sejak awal".** S1 berarti PS berhenti pada 2024 (Switch S1 = 0; Efek Izin PS = 0). Efek PS seluruhnya mengalir lewat patroli.
- **Mekanisme yang tidak aktif.** Efek penghidupan dan efek pengendalian kebakaran terhadap deforestasi bernilai 0 di semua run, sehingga View Fire Management tidak memengaruhi deforestasi.

### Inkonsistensi kritis

| # | Butir | Akibat |
|---|---|---|
| K1 | "Cakupan kebutuhan minimum LPHD" (3,6–133,5 %) dan "tertutup pada USD 28,04" memakai belanja **total** (termasuk rehabilitasi, KUPS, kelembagaan) sebagai pembilang. | Pada USD 28,04 kesenjangan rerata masih Rp 0,62 miliar/th. Cakupan komponen minimum saja: 24,8 % (USD 20) dan 57,8 % (USD 35). **Klaim abstrak "covered at about USD 28" tidak tepat.** |
| K2 | Besaran efek karbon (535 / 3.588 ha) disajikan tanpa syarat basis A1. | Besaran efek karbon bergantung pada pengkreditan efek PS. |
| K3 | "5.328 pekerja berbasis SDA". | Di model, 5.328 adalah *estimasi orang bergantung hutan* (kelas D). Pekerja SDA berjumlah 24.099–24.694 orang. |
| K4 | MAPE, Monte Carlo, PRCC, dan "413.000 nilai, 99,87–100 %". | Tidak dapat diverifikasi dari berkas yang diserahkan. Register README bahkan menulis "Vensim native belum dijalankan". |
| K5 | `HASIL SIMULASI VENSIM.xlsx` rusak (pemisah desimal hilang: 20,1326 → 201326). | Tidak boleh dipakai sebagai sumber. Run USD 20 tidak punya ekspor Vensim yang terbaca. |

### Kesiapan seminar dan sisa validasi

Koreksi K1–K3 hanya menyangkut penulisan dan label, bukan model, sehingga dapat diselesaikan sebelum Jumat, 6 November. Setelah itu, butir yang masih harus dilengkapi:

- data dan skrip MAPE;
- konfigurasi dan keluaran Monte Carlo/PRCC;
- ekspor `.txt` Vensim untuk USD 20;
- sumber data KUPS 2023;
- berkas induk `DELTA_KAPUAS_25HD_SD_FINAL_A1.mdl` (md5 f1bfaa88…), yang **tidak ada di ZIP**.

---

## OUTPUT 2 — Matriks Hasil Final (ringkas; lengkap di `FINAL_RESULTS_MATRIX.csv`)

| Indikator | S1 | S2 | S3 | S4 USD10 | S4 USD20 | S4 USD35 | Bukti |
|---|---|---|---|---|---|---|---|
| Hutan 2087 (ha) | 81.890 | 83.615 | 83.779 | 84.233 | 87.113 | 90.698 | VERIFIED |
| Deforestasi 2025–2086 (ha) | 29.812 | 28.092 | 27.816 | 27.281 | 24.227 | 21.023 | VERIFIED |
| Regenerasi alami 2025–2086 (ha) | 17.678 | 17.166 | 17.054 | 16.891 | 16.206 | 15.333 | VERIFIED |
| Rehabilitasi → hutan 2025–2086 (ha) | 0 | 516 | 516 | 599 | 1.110 | 2.365 | VERIFIED |
| Deforestasi dihindari vs S1 (ha) | – | 1.720 | 1.997 | 2.532 | 5.585 | 8.789 | VERIFIED / CONDITIONAL |
| Emisi bersih dihindari vs S1 (ribu tCO₂e) | – | 598 | 675 | 862 | 1.941 | 3.245 | VERIFIED / CONDITIONAL |
| Intensitas perlindungan (0–1) | 0 | 0,29 | 0,29 | 0,39 | 0,68 | 0,97 | VERIFIED |
| Kredit REDD **diajukan**, basis A1 (ribu tCO₂e) | – | – | – | 460 | 1.017 | 1.615 | bukan VCU; CONDITIONAL |
| Kredit karbon **terjual** (ribu tCO₂e) | – | – | – | 395 | 870 | 1.396 | bukan VCU |
| Penerimaan kotor (Rp miliar) | – | – | 0 | 65,4 | 287,2 | 790,1 | VERIFIED |
| MRV + transaksi + pajak (Rp miliar) | – | – | 0 | 28,1 | 41,9 | 70,7 | VERIFIED |
| Dana kolektif LPHD (Rp miliar) | – | – | 0 | 22,4 | 147,1 | 431,6 | VERIFIED |
| NPV proyek 10 %, parsial (Rp miliar) | – | – | −1,62 | 2,07 | 11,50 | 30,79 | VERIFIED (rekonstruksi) / CONDITIONAL |
| NPV mitra 10 %, parsial (Rp miliar) | – | – | −1,62 | 1,46 | 9,61 | 26,33 | VERIFIED (rekonstruksi) / CONDITIONAL |
| Belanja total / kebutuhan minimum | – | 0 % | 0 % | 11,8 % | 49,7 % | 133,5 % | INCONSISTENT sebagai "cakupan" |
| Cakupan berbasis kesenjangan | – | 0 % | 0 % | 11,8 % | 49,7 % | 95,7 % | VERIFIED |
| Belanja komponen minimum / kebutuhan | – | 0 % | 0 % | 5,9 % | 24,8 % | 57,8 % | VERIFIED (diagnostik) |
| HOK/th | 0 | 4.066 | 4.066 | 5.191 | 9.852 | 19.343 | VERIFIED |
| FTE (HOK/300; **bukan orang**) | 0 | 13,6 | 13,6 | 17,3 | 32,8 | 64,5 | VERIFIED |
| KUPS aktif (unit) | 6,7 | 33,4 | 33,4 | 33,4 | 33,4 | 64,2 | CONDITIONAL |
| Penerimaan anggota KUPS total (Rp juta/th) | 4,8 | 24,5 | 24,5 | 27,0 | 34,6 | 89,9 | CONDITIONAL |
| Pendapatan rata-rata RT (Rp juta/th, harga 2021) | 41,25 | 41,20 | 41,22 | 41,18 | 41,05 | 40,93 | CONDITIONAL |
| Kehilangan akses rata-rata (Rp/RT/th) | 0 | 141.352 | 153.114 | 227.077 | 448.032 | 682.096 | CONDITIONAL (asumsi D) |

---

## OUTPUT 8 — Putusan Ilmiah Final

**Klasifikasi: MEMERLUKAN KOREKSI KRITIS (koreksi penulisan, bukan model). Setelah koreksi: SIAP SEMINAR DENGAN KETERBATASAN METODOLOGIS EKSPLISIT.**

### Alasan

1. **Tidak ada kesalahan komputasi atau akuntansi stok-aliran.** Semua angka utama tereproduksi dari model yang diserahkan, sehingga koreksi tidak mengubah tabel inti.
2. **Satu klaim utama di abstrak dan simpulan tidak didukung definisinya** ("kebutuhan minimum tertutup pada USD 28", K1). Ini harus dikoreksi sebelum disajikan.
3. **Klaim efek karbon harus diberi syarat basis kredit A1** (K2). Tanpa itu, penguji REDD+ akan mempertanyakan over-crediting, dan pada A2 besarannya turun 88–95 % pada USD 10–20 (A2 register 94–95 %; varian diagnostik tanpa faktor penutup 88 %).
4. **Validasi historis dan Monte Carlo** belum dapat diperiksa. Cantumkan sebagai "dilaporkan oleh peneliti; berkas pendukung [PERLU DIISI]", bukan sebagai temuan yang sudah tervalidasi.
5. **Desain S1–S4 tetap sah sebagai eksperimen kebijakan** dan tidak perlu diganti.

### Rerun yang disarankan (opsional; tidak mengubah model)

| Rerun | Tujuan |
|---|---|
| Ekspor `.txt` Vensim untuk S4 USD 20 | Melengkapi replikasi Vensim |
| Ekspor ulang tabel dari `.vdfx` dengan *locale* titik desimal | Mengganti xlsx yang rusak |
| Simpan ulang S1, S2, S3, USD35 dari berkas induk tanpa pembulatan konstanta | Selisih saat ini ≤ 0,07 ha, tidak material |
