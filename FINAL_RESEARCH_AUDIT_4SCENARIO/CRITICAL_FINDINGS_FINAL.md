# Temuan Kritis Final: Model 4 Skenario (S1–S4), 25 Hutan Desa di Kalimantan Barat

**Tanggal:** 4 November 2026 (lanjutan audit)

**Prinsip audit:**
- Model utama S1–S4 tidak diubah.
- Hasil makalah yang sudah direproduksi dipertahankan.
- Setiap angka baru diberi label:
  - **[REPRODUKSI]**: angka makalah atau register yang dihitung ulang dan cocok.
  - **[DIAGNOSTIK BARU]**: eksperimen audit dengan parameter yang sudah ada di model, ditimpa saat run. Persamaan tidak diubah. Bukan hasil utama.

**Berkas pendukung:**
- `A1_A2_BASELINE_RECONCILIATION.csv`: 15 baris (A1, A2 register, dan A2 faktor 1, masing-masing pada USD 6/10/15/20/35).
- `LPHD_FINANCIAL_COVERAGE.csv`: 14 harga × 2 periode.
- `MANUSCRIPT_CORRECTION_TABLE.md` dan `VALIDATION_EVIDENCE_GAPS.md`.
- Skrip: `code/a1a2.py`, `code/a1a2_table.py`, `code/lphd.py`.

**Konvensi periode:**
- Fisik: integral aliran [2025, 2087).
- Keuangan dan kredit: [2024, 2087).
- Rerata tahunan: integral [2030, 2056)/26.
- DT 0,0625.

**Model:** `DKP_25HD_A1_S4_USD{6,10,15,20,35}_rapi.mdl` dan berkas S1/S2/S3 dari `MODEL_VENSIM.zip`.

---

## Ralat atas audit sebelumnya

Laporan audit pertama menyebut "A2" untuk rerun dengan `Switch Baseline Kredit Konservatif = 1` dan `Faktor Rekonsiliasi Reversal Kredit A2 = 1`.

Register menunjukkan bahwa **A2 resmi (paket CLOSURE)** juga memakai faktor penutup: 0,718917 (USD 6), 0,727781 (USD 10), 0,740124 (USD 15), 0,762355 (USD 20), dan 1 (USD 35). Sumber: `REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx`, lembar `1 Daftar skenario` dan `3 Input per skenario`.

Audit ini **mereproduksi A2 register persis**. Selisih terhadap lembar `8 Kumulatif 2025-2086` < 10⁻⁴ untuk USD 6–20. Pada USD 35 selisihnya 0,02 ha akibat pembulatan konstanta berkas.

Varian faktor = 1 kini diberi label "A2 faktor 1 [DIAGNOSTIK BARU]". Semua laporan folder sudah diperbarui, dan berkasnya diganti nama menjadi `03_CARBON_ACCOUNTING/diagnostic_A2_faktor1_AUDIT_rerun.csv`.

---

## TEMUAN 1 — Baseline kredit A1 dan A2: persamaan, definisi, dan dampak

### 1.1 Persamaan sumber (identik di semua berkas S4)

| Variabel | Persamaan | Satuan |
|---|---|---|
| `Faktor Tekanan Deforestasi Baseline` | `= 1` | Dmnl |
| `Laju HMS/HRS/HLKS menjadi NonHutan Baseline` | `= Laju … BAU × Faktor Tekanan Deforestasi Baseline` | 1/Year |
| `Emisi Deforestasi Biomassa Baseline` | `= Emisi HLKS Baseline + Emisi HMS Menjadi Non Hutan Baseline + Emisi HRS Baseline − Koreksi Emisi Hutan Regenerasi Baseline` | tCO₂e/Year |
| `Pengurangan Emisi REDD Bruto` | `= MAX(0, MIN(Emisi Def. Biomassa Baseline − Emisi Def. Biomassa, Pengurangan Emisi Biomassa))` | tCO₂e/Year |
| `Pengurangan Emisi Eligible REDD` | `= Bruto × (1 − 0,10) × (1 − 0,12) × 0,682` | tCO₂e/Year |
| `Porsi Mitigasi Adisional terhadap S2` | `= IF Efek Pengelolaan PS Aktif > 0 THEN MAX(0, Efek Aktif − Efek Tanpa Karbon)/Efek Aktif ELSE 1` | Dmnl |
| `Efek Pengelolaan PS Tanpa Karbon` | `= Switch PS × Switch Dampak Skenario Lahan × SMOOTHI(Respons Perlindungan Tanpa Karbon, 3 th) × 0,37` (respons dari **patroli swadaya saja**) | Dmnl |
| `Kredit REDD Diajukan` | `= Eligible × Switch Karbon × Switch Periode Kredit × (1 − SwitchKonservatif × (1 − Porsi Mitigasi Adisional thd S2)) × Faktor Rekonsiliasi Reversal Kredit A2` | tCO₂e/Year |
| `Kredit REDD Terbit` | `= DELAY FIXED(Kredit REDD Diajukan, 3 th, 0)` | tCO₂e/Year |
| `Kredit REDD Terjual` | `= Switch Inventori (=1) × Stok Belum Terjual × MIN(1, 0,7 × DT)/DT` | tCO₂e/Year |
| `Kredit REDD Kedaluwarsa` | `= MIN(Stok × 0,1, …)` | tCO₂e/Year |
| `Pendapatan Kotor REDD` | `= Kredit REDD Terjual × Harga Karbon × 16.500` | Rp/Year |

### 1.2 Basis referensi dan definisi "tambahan mitigasi"

| Unsur | A1 (hasil utama) | A2 register (pembanding CLOSURE) |
|---|---|---|
| Switch / faktor | `Switch Baseline Kredit Konservatif = 0`; faktor = 1 | `= 1`; faktor 0,72–0,76 (USD 6–20), 1 (USD 35) |
| Referensi emisi | Kembaran "Baseline" internal = run S1. **[REPRODUKSI]** Deret `Deforestasi Total Baseline` S4 = `Deforestasi Total` S1 dengan selisih 0 pada berkas berpembulatan sama. | Referensi yang sama (S1), lalu dikalikan porsi mitigasi adisional dan faktor penutup |
| Tambahan mitigasi yang dikreditkan | Seluruh pengurangan terhadap S1: efek PS swadaya + pembiayaan awal + karbon | Bagian efek pengelolaan di atas efek patroli swadaya. **Efek pembiayaan awal ikut dihitung aditional**, karena `Efek Tanpa Karbon` hanya memuat swadaya. |
| Plafon tersirat | Dokumentasi: kredit kumulatif ≤ (emisi def. biomassa S1 − S4) × 0,9 × 0,88 × 0,682 (`solve_a1.py`) | Kredit kumulatif = (emisi def. biomassa S2 − S4) × 0,9 × 0,88 × 0,682 (`solve_closure.py`) |
| Konsistensi terhadap definisinya sendiri | **CONSISTENT.** Kredit = 99,0–99,97 % plafon S1 di semua harga. | **CONSISTENT setelah faktor penutup.** Kredit = plafon S2 untuk USD 6–20 (USD 10: 57.019 vs 57.008). Pada USD 35 faktor = 1 dan kredit = 97,2 % plafon S2. |
| Faktor = 1 (tanpa penutup) | – | **INCONSISTENT terhadap definisi A2 sendiri.** Kredit melebihi plafon S2 sebesar 38 / 36 / 32 / 24 % (USD 6 / 10 / 15 / 20); USD 10: 86.632 vs 63.723 |

Sumber persamaan: semua `.mdl` S4 di ZIP. Sumber definisi plafon: dokumentasi variabel `Faktor Rekonsiliasi Reversal Kredit A2`. Skrip `solve_a1.py` dan `solve_closure.py` **tidak disertakan**, sehingga prosedur iterasinya UNVERIFIED, walaupun nilai faktornya tereproduksi.

### 1.3 Diajukan, terbit, dan terjual (ribu tCO₂e, 2024–2086)

| Harga | Basis | Diajukan | Terbit | Terjual REDD | Terjual REDD+ARR | Status |
|---|---|---|---|---|---|---|
| USD 6 | A1 | 385,5 | 376,7 | 326,3 | 327,1 | [REPRODUKSI] |
| | A2 register | 51,3 | 51,3 | 44,9 | 45,4 | [REPRODUKSI register] |
| | A2 faktor 1 | 74,8 | 74,8 | 65,4 | 65,9 | [DIAGNOSTIK BARU] |
| USD 10 | A1 | 460,3 | 452,6 | 392,9 | 394,6 | [REPRODUKSI] |
| | A2 register | 57,0 | 57,0 | 49,9 | 50,4 | [REPRODUKSI register] |
| | A2 faktor 1 | 86,6 | 86,6 | 75,8 | 76,2 | [DIAGNOSTIK BARU] |
| USD 15 | A1 | 634,5 | 625,6 | 543,5 | 547,6 | [REPRODUKSI] |
| | A2 register | 67,6 | 67,6 | 59,2 | 59,6 | [REPRODUKSI register] |
| USD 20 | A1 | 1.017,2 | 995,4 | 861,3 | 870,2 | [REPRODUKSI] |
| | A2 register | 87,0 | 87,0 | 76,1 | 76,9 | [REPRODUKSI register] |
| | A2 faktor 1 | 160,7 | 160,7 | 140,7 | 142,2 | [DIAGNOSTIK BARU] |
| USD 35 | A1 | 1.614,8 | 1.548,9 | 1.330,8 | 1.396,2 | [REPRODUKSI] |
| | A2 register = A2 faktor 1 | 1.144,6 | 1.089,8 | 933,2 | 958,6 | [REPRODUKSI register] |

- **Terbit < diajukan** karena jeda 3 tahun memindahkan kredit 2084–2086 ke luar horizon.
- **Terjual < terbit** karena 70 %/th dari stok terjual dan 10 %/th kedaluwarsa (USD 10 A1: 56,1 ribu kedaluwarsa).
- **Penerimaan dihitung dari kredit terjual**, bukan diajukan.
- **"Kredit model" di Tabel 4 makalah = Diajukan (A1).**

### 1.4 Dampak terhadap hasil ekologis dan finansial

| Harga | Indikator | A1 [REPRODUKSI; makalah] | A2 register [REPRODUKSI register] | A2 faktor 1 [DIAGNOSTIK BARU] |
|---|---|---|---|---|
| USD 6 | S4−S3 deforestasi dihindari (ha) | 120 | 0 | 15 |
| | NPV proyek 10 % (Rp miliar) | −0,50 | −3,19 | −2,67 |
| | Defisit biaya belum pulih 2087 (Rp miliar) | 2,07 | 18,60 | 17,89 |
| USD 10 | S4−S3 (ha) | 535 | 31 | 67 |
| | Hutan 2087 (ha) | 84.233 | 83.802 | 83.829 |
| | Penerimaan kotor / biaya MRV+transaksi+pajak (Rp miliar) | 65,39 / 28,06 | 8,39 / 23,45 | 12,65 / 23,79 |
| | Dana LPHD (Rp miliar) | 22,40 | 1,34 | 2,91 |
| | NPV proyek / mitra (Rp miliar) | 2,07 / 1,46 | −2,23 / −2,31 | −1,35 / −1,53 |
| | Pembiayaan awal belum pulih 2087 (Rp miliar) | 0 | 0,87 | 0 |
| | Intensitas perlindungan | 0,387 | 0,302 | 0,310 |
| USD 15 | S4−S3 (ha) | 1.494 | 88 | 181 |
| | NPV proyek (Rp miliar) | 6,09 | −0,94 | 0,50 |
| USD 20 | S4−S3 (ha) | 3.588 | 192 | 422 |
| | Hutan 2087 (ha) | 87.113 | 83.925 | 84.112 |
| | Penerimaan kotor / biaya (Rp miliar) | 287,16 / 41,91 | 25,36 / 24,46 | 46,94 / 25,89 |
| | Dana LPHD (Rp miliar) | 147,15 | 8,30 | 18,08 |
| | NPV proyek / mitra (Rp miliar) | 11,50 / 9,61 | 0,63 / 0,20 | 2,79 / 2,05 |
| | Defisit biaya belum pulih 2087 (Rp miliar) | 0 | 12,92 | 9,09 |
| USD 35 | S4−S3 (ha) | 6.792 | 6.176 | 6.176 |
| | NPV proyek (Rp miliar) | 30,79 | 16,26 | 16,26 |

**Pembacaan:**
- Pada USD 6–20, **hampir seluruh efek ekologis S4−S3 dan kelayakan finansial A1 bergantung pada pengkreditan efek PS swadaya.** Pada A1, 68 % kredit USD 10 berasal dari efek PS dan 11 % dari pembiayaan awal.
- Pada A2 register, NPV proyek baru positif di antara USD 15 dan USD 20.
- Pada USD 35, loop dana→patroli cukup kuat sehingga kedua basis memberi efek besar.

### 1.5 Validitas model ≠ kepatuhan metodologi standar karbon

| Pertanyaan | A1 | A2 register | Status |
|---|---|---|---|
| Apakah kredit konsisten dengan definisi yang dinyatakan di model? | Ya (≤ plafon S1) | Ya (= plafon S2, setelah faktor penutup) | VERIFIED |
| Apakah definisi itu valid secara empiris? | Valid **bila** patroli swadaya tidak akan berlanjut tanpa proyek. Dokumentasi `Switch Baseline Kredit Konservatif` menyebut asumsi S2 "belum didukung data lapangan". | Valid **bila** patroli swadaya akan berlanjut tanpa proyek. Asumsi ini juga belum didukung data. | **CONDITIONAL.** Bergantung pada fakta kontrafaktual patroli swadaya yang belum diukur |
| Apakah A2 lebih valid karena lebih konservatif? | – | **Tidak dapat disimpulkan.** Konservatif ≠ benar. A2 juga mengkreditkan efek pembiayaan awal, memakai proksi rasio efek yang dihaluskan (SMOOTHI 3 th), dan faktor penutup skalar yang diselesaikan di luar model. Ketepatan waktu tahunan kreditnya tetap berbasis proksi. | CONDITIONAL |
| Apakah A1 atau A2 patuh pada metodologi standar (mis. VCS/VM0048 yang disebut register; PDD Delta Kapuas)? | Tidak diuji | Tidak diuji | **NOT TESTED.** Dokumen metodologi dan PDD (Appendix 11–12 dicatat "tidak tersedia" di register) tidak ada di paket. Baseline metodologi ditetapkan dengan prosedurnya sendiri, bukan dari simulasi SD. Register mencatat baseline PDD 469.495 tCO₂e/th hanya sebagai pembanding, bukan target kalibrasi. |
| Isu aditionalitas faktual | 24 dari 25 HD ber-SK 2017–2020, sebelum proyek 2024 | sama | Perlu dibahas sebagai keterbatasan |

**Rekomendasi:**
- A1 tetap dipakai sebagai hasil utama sesuai desain.
- Laporkan A2 register sebagai **batas bawah aditionalitas ketat**, bukan sebagai "hasil yang benar".
- Nyatakan bahwa **kredit model ≠ VCU** dan kepatuhan metodologi belum diuji.

---

## TEMUAN 2 — Indikator kebutuhan minimum LPHD

### Persamaan sumber

- `Kebutuhan Dana Minimum = Kebutuhan Dana Operasional LPHD + Kebutuhan Dana Perlindungan + Kebutuhan Dana Pengendalian Kebakaran`. Rerata 2030–2055: 1,250 + 1,467 + 2,702 = 5,418 miliar/th.
- `Penggunaan Dana Pengelolaan` = realisasi belanja **6 pos**: operasional, perlindungan, kebakaran, rehabilitasi, kelembagaan, KUPS.
- Alokasi pos tetap: 10 / 30 / 10 / 15 / 15 / 20 %. Setiap pos dibatasi kebutuhannya dan dikali `Rasio Realisasi Belanja`.
- `Kesenjangan Pembiayaan Minimum = MAX(0, Kebutuhan Dana Minimum − Penggunaan Dana Pengelolaan − Realisasi Pembiayaan Awal)`.

### Apa yang sebenarnya diukur "USD 28,04"

**[REPRODUKSI]** Pada USD 28,04, rerata 2030–2055 dari `Penggunaan Dana Pengelolaan` / `Kebutuhan Dana Minimum` = 1,000.

Artinya: **belanja LPHD total untuk enam pos sama besar dengan kebutuhan tiga pos minimum.** Angka ini **bukan** titik ketika kebutuhan minimum terpenuhi. Pada harga tersebut:

| Ukuran (rerata 2030–2055, USD 28,04) | Nilai | Label |
|---|---|---|
| Belanja total / kebutuhan minimum (= indikator makalah) | 100,0 % | [REPRODUKSI] |
| 1 − kesenjangan model / kebutuhan | 88,6 % (kesenjangan 0,62 miliar/th) | [REPRODUKSI dari variabel model] |
| Belanja komponen minimum / kebutuhan minimum | **46,1 %** (kesenjangan 2,92 miliar/th) | [DIAGNOSTIK BARU] |
| Per komponen: operasional / patroli / kebakaran | 46,7 % / 90,8 % / 21,6 % | [DIAGNOSTIK BARU] |
| Tahun 2030–2055 dengan belanja total ≥ kebutuhan | 15 dari 26 | [DIAGNOSTIK BARU] |
| Tahun dengan belanja komponen minimum ≥ kebutuhan | 0 dari 26 | [DIAGNOSTIK BARU] |

**Ambang lain [DIAGNOSTIK BARU, sapuan harga pada `DKP_25HD_A1_S4_USD10_rapi.mdl`]:**
- Kesenjangan versi model rerata = 0 tercapai sekitar **USD 72,6**.
- Belanja komponen minimum **tidak mencapai 100 % rerata hingga USD 300** (99,2 %). Penyebabnya:
  - alokasi tetap hanya 10 % untuk kebakaran, padahal kebakaran = 50 % dari kebutuhan minimum;
  - rasio realisasi kapasitas < 1.
- Pada harga tinggi, dana menumpuk sebagai saldo tak terbelanja (USD 75: saldo 2055 = Rp 167 miliar).

Tabel lengkap per harga ada di `LPHD_FINANCIAL_COVERAGE.csv`. Ringkasnya (rerata 2030–2055, Rp miliar/th):

| Harga | Kebutuhan minimum | Dana LPHD diterima | Belanja total | Belanja komponen minimum | Belanja total/kebutuhan **[makalah]** | 1 − kesenjangan model/kebutuhan | Komponen minimum/kebutuhan **[cakupan sebenarnya]** | Kesenjangan model | Kesenjangan komponen minimum |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 5,418 | 0,193 | 0,193 | 0,097 | 3,6 % | 3,6 % | 1,8 % | 5,225 | 5,322 |
| 10 | 5,418 | 0,636 | 0,641 | 0,321 | 11,8 % | 11,8 % | 5,9 % | 4,777 | 5,098 |
| 15 | 5,418 | 1,463 | 1,452 | 0,726 | 26,8 % | 26,8 % | 13,4 % | 3,966 | 4,692 |
| 20 | 5,418 | 2,748 | 2,692 | 1,346 | 49,7 % | 49,7 % | 24,8 % | 2,726 | 4,072 |
| 28,04 | 5,418 | 5,586 | 5,419 | 2,500 | 100,0 % | 88,6 % | 46,1 % | 0,620 | 2,918 |
| 35 | 5,418 | 7,482 | 7,232 | 3,130 | 133,5 % | 95,7 % | 57,8 % | 0,233 | 2,288 |
| 50 | 5,418 | 11,201 | 10,164 | 4,335 | 187,6 % | 99,6 % | 80,0 % | 0,020 | 1,083 |

**Status:**
- Indikator makalah: **INCONSISTENT dengan labelnya** ("cakupan kebutuhan minimum").
- Persamaan `Kesenjangan Pembiayaan Minimum`: **INCONSISTENT secara definisi**, karena mengurangkan belanja non-minimum. Ketidaksesuaian ini dapat direproduksi dari persamaan.
- Model **tidak diubah**. Indikator pengganti dihitung di luar model dari variabel `Realisasi Belanja *` yang sudah ada.

---

## TEMUAN 3 — Label variabel

Rincian lengkap dan kalimat pengganti ada di `MANUSCRIPT_CORRECTION_TABLE.md`. Butir kritis:

| Butir | Variabel sumber (`.mdl`) | Sebelum (makalah) | Sesudah | Status |
|---|---|---|---|---|
| 5.328 | `Masyarakat Bergantung pada Hutan Awal = 5328` (People; kelas D; rentang uji 2.144–19.038) | "5.328 pekerja berbasis SDA" | "5.328 orang bergantung hutan (estimasi)" | INCONSISTENT → dikoreksi label |
| 24.694 | `Pekerja Berbasis SDA` = pertanian + perkebunan + perikanan + peternakan; 24.694 pada 2024 (data SAMPAN 24.099 disesuaikan ke populasi 2024) | tidak disebut | "24.694 pekerja sektor SDA (2024)" | [REPRODUKSI] |
| FTE | `Kesempatan Kerja Setara Penuh = Kesempatan Kerja PS / 300` (satuan model: People) | "pekerja setara penuh (orang)" | "setara pekerja penuh (FTE; HOK/300)" | label dikoreksi |
| Upah | `Upah Kegiatan PS = Upah Patroli Berbayar + Manfaat Ekonomi Penanaman + Manfaat Ekonomi Patroli + Upah Pengendalian Kebakaran` | "upah kegiatan Rp 327 juta / Rp 905 juta" | Upah dibayar dari karbon (`Upah Kegiatan Didanai Karbon`) Rp 145,5 / 723,8 juta. Nilai ekonomi kerja swadaya S2 Rp 181,4 juta/th | label dikoreksi |
| Kredit | `Kredit REDD Diajukan` / `Terbit` / `Terjual` | "kredit model" | lihat 1.3 | label dikoreksi |

---

## TEMUAN 4 — Bukti validasi yang belum tersedia

Rinciannya ada di `VALIDATION_EVIDENCE_GAPS.md`.

MAPE, Monte Carlo, PRCC, dan klaim "±413.000 nilai, 99,87–100 %" berstatus **BELUM DAPAT DIVERIFIKASI**. **Ini bukan GAGAL**: log dan berkasnya tidak ada di paket.

Laporan pada branch `claude/new-session-bao4rv` (model 3 skenario) mencatat bahwa skrip dan berkas Monte Carlo model 4 skenario "tidak ada di paket". Berkas pada branch itu memakai versi model lain dan **tidak boleh dipakai** sebagai bukti untuk S1–S4.

---

## Temuan lain yang tetap berlaku (dari audit pertama)

| Butir | Sumber | Periode | Sebelum → sesudah | Status |
|---|---|---|---|---|
| Neraca stok hutan | `Total Hutan`, aliran HLKS/HMS/HRS | 2024–2087 | residu 0,000 ha; "284" = neto 2024 (522,2 − 238,4) | VERIFIED |
| S3−S2 setelah 2025 | `Deforestasi Total` S2, S3 | tahunan | "tidak berlanjut" → +345 ha (2025–2036), −69 ha (2037–2086), neto 276 | VERIFIED; perlu klarifikasi teks |
| `HASIL SIMULASI VENSIM.xlsx` | ekspor Vensim | – | 20–35 % nilai rusak (desimal hilang) | INCONSISTENT; jangan dipakai |
| Ekspor Vensim USD 20 | `Run/Skenario4USD20.vdfx` | – | tidak ada `.txt` | perlu ekspor ulang |
| Konstanta dibulatkan (S1, S2, S3, USD35) | `.mdl` | – | selisih hutan awal 0,07 ha | CONSISTENT; tidak material |

**Tidak ada temuan yang mengharuskan perubahan model atau angka S1–S4.** Semua koreksi adalah label, definisi indikator, dan pengungkapan basis kredit.
