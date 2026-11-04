# Final Gate Fase 4: Model PWD Dua Skenario

**Tanggal:** 4 November 2026

**Model yang diperiksa:**
- `MODEL_FINAL_DUA_SKENARIO_PWD.mdl` (v1; 937 variabel; md5 `1cffa4b7…`). Tidak ditimpa.
- `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (v2; 946 variabel; 16 View; md5 `639083f9ca53da5601610211a1ccddfc`). Hanya akuntansi *reversal* yang diperbaiki; struktur ekologis dan dua skenario tidak berubah.

**Status:**
- Perangkat: PySD 3.14.3. **Vensim native BELUM DIVERIFIKASI.**
- **NPV berstatus SEMENTARA.**
- Kredit model ≠ kredit terverifikasi.

**Lampiran data:** `HASIL_UJI_FINAL_GATE_FASE4_PWD.xlsx` (lembar 1–10).

---

## Keputusan

### SIAP BERSYARAT untuk simulasi deterministik final (Tahap 3)

**Masalah struktural material yang ditemukan dan diselesaikan:**
1. **K7.** Kesalahan **atribusi** dana non-karbon yang dapat dipertukarkan. Diselesaikan dengan **protokol Referensi S1 berpasangan**, yang terbukti setara persis dengan S1 mandiri pada 15 dari 15 konfigurasi uji.
2. **Akuntansi reversal v1** memiliki tiga cacat:
   - saldo tidak dipulihkan sesudah penyelesaian, sehingga ada risiko penalti ganda;
   - buffer tidak pernah berkurang;
   - stok kredit sendiri tidak dibatalkan lebih dulu.

   Ketiganya diperbaiki di v2 dan diuji ulang (RV1–RV4 LULUS).
3. **Metode uji U6 (langkah waktu) v1 tidak sah.** Diulang dengan metode yang benar dan LULUS.

**Syarat yang tetap berlaku:**
1. Semua run S2 final memakai **mode Referensi S1 berpasangan**: tujuh masukan rantai referensi diambil dari run S1 mandiri dengan parameter identik. Mode endogen hanya sah bila tidak ada kas non-karbon atau dukungan material rehabilitasi.
2. Uji K7 dalam mode endogen **tetap tercatat GAGAL**. Kegagalan itu tidak dihapus.
3. Units Check dan run native Vensim belum dilakukan (V0c).
4. NPV SEMENTARA.
5. Aturan penyelesaian *reversal* adalah asumsi model tanpa dasar kontraktual (bagian 2).

Monte Carlo, PRCC, eksperimen benefit sharing, dan revisi makalah **belum dijalankan**.

---

## 1. Diagnosis dan penyelesaian K7

**Kondisi uji:** S2-C USD 20 dengan kas non-karbon Rp3 miliar/th; pembanding S1 mandiri dengan kas yang sama.

### 1.1 Konvergensi langkah waktu (lembar 3)

DT dimasukkan lewat argumen `time_step` PySD.

| DT | Galat emisi deforestasi Ref S1 − S1, kumulatif | Galat tahunan maks / min |
|---|---|---|
| 0,125 | +164,4 tCO₂e | +93,3 / −337,7 |
| 0,0625 | +163,0 | +92,9 / −327,1 |
| 0,03125 | +162,2 | +92,7 / −322,0 |
| 0,015625 | +161,8 | +92,6 / −319,6 |

Galat **konvergen ke ±161 tCO₂e, bukan ke 0**. Jadi galat ini **bukan perbedaan integrasi numerik**.

### 1.2 Rekonsiliasi tahunan per saluran (lembar 4)

Masukan rantai Referensi S1 diganti, bertahap, dengan deret dari run S1 mandiri pada waktu yang sama:

| Langkah | Galat kumulatif |
|---|---|
| Endogen | 163,0 tCO₂e |
| + faktor tekanan deforestasi dari S1 mandiri | 99,3 tCO₂e (saluran patroli ≈ 64) |
| + aliran penanaman dari S1 mandiri | **0,0** (saluran penanaman ≈ 99) |

### 1.3 Klasifikasi

| Kemungkinan sumber | Temuan |
|---|---|
| **Kesalahan atribusi** | **YA, sumber tunggal.** Di S2, dana karbon dan non-karbon bercampur di saldo LPHD. Patroli dan penanaman yang di S1 dibiayai dana non-karbon, di S2 sebagian dibiayai dana karbon, sehingga dana non-karbon tertahan atau dipakai untuk pos lain. Atribusi "porsi saldo" dan "non-karbon lebih dulu" di dalam satu run tidak dapat merekonstruksi pola belanja S1 tanpa mereplikasi seluruh subsistem keuangan, KUPS, dan rehabilitasi S1 |
| Kesalahan pembukuan temporal | Tidak. Rantai referensi memakai nilai tahun berjalan; galat hilang tepat bila masukan diambil dari S1 pada waktu yang sama |
| Perbedaan integrasi numerik | Tidak (1.1) |
| Kesalahan persamaan lain | Tidak ditemukan. Dengan masukan berpasangan, ke-78 variabel rantai sama persis dengan S1 |

### 1.4 Penyelesaian: Referensi S1 berpasangan

- **Tujuh masukan** rantai Referensi S1 ditimpa dengan deret run S1 mandiri yang memakai parameter identik:
  - `Faktor Tekanan Deforestasi Referensi S1` ← `Faktor Tekanan Deforestasi`;
  - `Aliran Penanaman ke Rehabilitasi Referensi S1` ← `Penambahan Luas Penanaman`;
  - `Rehabilitasi Menjadi Hutan Referensi S1` dan `Kegagalan Rehabilitasi Referensi S1`;
  - `Faktor Ekspansi Kebun Referensi S1`, `Faktor Gangguan Gambut Tersisa Referensi S1`, `Emisi Kebakaran Gambut Referensi S1`.
- **Sifat:** prospektif (nilai S1 pada t yang sama, tanpa informasi masa depan), tanpa loop aljabar, dan kredit tetap endogen terhadap kas, bagi hasil, dan patroli.
- **Biaya komputasi:** run S1 tetap diperlukan sebagai pasangan pada setiap konfigurasi, termasuk Monte Carlo berpasangan.
- **Implementasi:** di PySD, deret S1 dimasukkan sebagai `params` (pandas Series). Di Vensim, setara dengan menjadikan ketujuh variabel itu variabel data dari run S1; ini **belum diuji di Vensim native**.
- **Alternatif yang ditolak:**
  - Menyalin seluruh subsistem keuangan, KUPS, dan rehabilitasi S1 ke dalam S2 sama dengan membangun model kedua; bertentangan dengan instruksi.
  - Memperbesar toleransi tidak menyelesaikan masalah.

**Hasil:** uji K7b LULUS 15/15 konfigurasi (galat ≤ 10⁻⁹). K7 dalam mode endogen tetap tercatat **GAGAL**.

---

## 2. Audit reversal dan kewajiban penggantian

### 2.1 Lima besaran yang dipisahkan

Lembar 6; aturan 2 = default v2.

| Besaran | USD 6 | USD 15 | USD 20 | USD 35 |
|---|---|---|---|---|
| (1) Tahun pertama deforestasi S2 > S1 | 2040,8 | 2046,2 | 2052,8 | tidak terjadi |
| (1) Deforestasi tambahan S2 pada tahun-tahun itu | 68,6 ha (31,0 ribu tCO₂e bruto) | 69,6 ha | 77,7 ha (34,5 ribu tCO₂e) | 0 |
| (2) Puncak manfaat bersih eligible kumulatif | 68,8 ribu tCO₂e (2039,8) | 78,0 ribu (2045,1) | 100,7 ribu (2051,7) | 897,3 ribu (2087) |
| (2) Manfaat bersih eligible 2087 | 44,1 ribu | 53,3 ribu | 74,4 ribu | 897,3 ribu |
| Kredit REDD diajukan | 68,8 ribu | 78,0 ribu | 100,7 ribu | 897,3 ribu |
| (3) Pembatalan stok kredit sendiri | ≈ 0 (stok sudah terjual) | ≈ 0 | ≈ 0 | 0 |
| (3) Debit belum diselesaikan 2087 (sesudah verifikasi terakhir 2082) | 2,5 ribu tCO₂e (Rp0,25 M) | 2,9 ribu (Rp0,72 M) | 3,9 ribu (Rp1,28 M) | 0 |
| (4) Kontribusi buffer / dipakai | 9,4 / 9,4 ribu | 10,6 / 10,6 ribu | 13,7 / 13,7 ribu | 122,4 / 0 ribu |
| (5) Kredit pengganti dibeli | 12,9 ribu (pertama 2062,1) | 11,1 ribu (2067,1) | 8,6 ribu (2072,1) | 0 |
| (5) Biaya kas pengganti | Rp1,27 M | Rp2,75 M | Rp2,84 M | 0 |
| NPV mitra inkremental [SEMENTARA] | −Rp4,16 M | −Rp1,54 M | −Rp0,27 M | +Rp6,66 M |

**Bacaan:**
- **Deforestasi S2 > S1 pada satu tahun tidak langsung menjadi kewajiban.** Pada USD 20, tahun negatif pertama 2052,8, tetapi pembelian pertama baru 2072,1.
- **Jalurnya bertahap:**
  1. kehilangan tahunan mengurangi saldo mitigasi;
  2. saldo negatif menghentikan pengajuan kredit baru dan dapat dilunasi mitigasi berikutnya;
  3. pada setiap verifikasi (lima tahunan), debit tersisa ditutup buffer;
  4. lalu dengan pembatalan stok kredit sendiri;
  5. baru sisanya dengan pembelian.
- **Penyebab reversal di model:** hutan yang diselamatkan jembatan 2026–2030 menghadapi laju deforestasi per ha yang sama dengan S1 setelah pembiayaan berhenti. Pada USD 35 siklus pembiayaan mandiri, sehingga reversal tidak terjadi.

### 2.2 Perbandingan aturan penyelesaian (USD 20)

| Aturan | Debit 2087 | Biaya pengganti | NPV mitra inkremental | Defisit MRV 2087 |
|---|---|---|---|---|
| 0: tidak diselesaikan, hanya dilaporkan | 26,2 ribu tCO₂e (Rp8,65 M pada harga berjalan) | 0 | −Rp0,25 M | Rp12,4 M |
| 1: buffer + pembatalan stok | 12,5 ribu tCO₂e | 0 | −Rp0,25 M | Rp12,4 M |
| **2: + pembelian pengganti (default)** | 3,9 ribu tCO₂e | Rp2,84 M | −Rp0,27 M | Rp15,2 M |

NPV mitra hampir sama karena pembelian terjadi sesudah 2072 (terdiskonto) dan ditanggung lewat defisit biaya bersama. Kewajiban nominalnya tetap besar dan harus dilaporkan terpisah.

### 2.3 Dasar aturan akuntansi

| Unsur aturan | Status |
|---|---|
| Penghentian penerbitan sampai defisit tertutup (debit dibawa ke depan) | Asumsi model. Sejalan dengan prinsip umum mekanisme non-permanen standar sukarela: tidak ada penerbitan baru selama manfaat bersih kumulatif di bawah yang sudah diterbitkan. Teks standar yang berlaku **BELUM DIVERIFIKASI** |
| Pembatalan kredit buffer untuk menutup reversal | Asumsi model. Sejalan dengan prinsip umum *buffer pool* AFOLU; aturan rinci (pool proyek vs pool bersama, besaran berbasis penilaian risiko) **BELUM DIVERIFIKASI**. Porsi buffer 12 % adalah parameter model |
| Penyelesaian pada peristiwa verifikasi lima tahunan | Asumsi model, mengikuti `Periode Verifikasi` = 5 th |
| Pembatalan stok kredit sendiri sebelum membeli | Asumsi model |
| Pembelian kredit pengganti pada harga berjalan | **Asumsi model tanpa dasar kontraktual.** Mirip ketentuan reversal disengaja di sebagian program kepatuhan dan klausul ERPA, tetapi kontrak proyek DKP tidak tersedia: **[PERLU DIISI]** |
| Reversal diukur terhadap Referensi S1 | Konsekuensi pilihan konservatif penelitian. Standar mengukur terhadap baseline yang ditetapkan, bukan terhadap skenario kebijakan model. Terhadap baseline BAU model, S2 tidak pernah mengalami reversal |

---

## 3. Uji kesetaraan Referensi S1

**Toleransi ditetapkan sebelum melihat hasil** (`toleransi.json`):

| Mode | Kriteria "setara" |
|---|---|
| Endogen | selisih hutan maks ≤ 1 ha **dan** \|galat emisi deforestasi kumulatif\| ≤ 0,1 % dari sinyal mitigasi S1−S2 |
| Berpasangan | selisih relatif ≤ 10⁻⁹ pada semua besaran |

Besaran yang dibandingkan pada semua t:
- stok hutan;
- laju deforestasi;
- stok karbon biomassa (dihitung dari stok lahan × densitas − defisit regenerasi);
- emisi deforestasi tahunan;
- emisi bersih biomassa tahunan;
- emisi kumulatif.

Konfigurasi memakai USD 20 kecuali disebut.

| Konfigurasi | Endogen: Δhutan maks (ha) | Endogen: galat emisi kumulatif (tCO₂e; % sinyal) | Endogen | Berpasangan |
|---|---|---|---|---|
| Dasar (k 0,5; kas non-karbon 0) | 0 | ≈ 0 | SETARA | SETARA |
| k = 0 | 0 | 0 | SETARA | SETARA |
| k = 1 | 0 | ≈ 0 | SETARA | SETARA |
| Efektivitas 0,2 | 0 | ≈ 0 | SETARA | SETARA |
| Efektivitas 0,6 | 1,5·10⁻¹¹ | ≈ 0 | SETARA | SETARA |
| Keberhasilan rehabilitasi dasar 0,5 | 0 | ≈ 0 | SETARA | SETARA |
| DT 0,03125 | 0 | ≈ 0 | SETARA | SETARA |
| Kas non-karbon Rp3 M | 10,0 | +163 (0,03 %) | SELISIH MATERIAL | SETARA |
| Kas non-karbon + k = 0 | 6,4 | +49 (0,02 %) | SELISIH MATERIAL | SETARA |
| Kas non-karbon + k = 1 | 105 | −32.300 (2,4 %) | SELISIH MATERIAL | SETARA |
| Kas non-karbon, USD 10 | 1,2 | +4 (0,002 %) | SELISIH MATERIAL | SETARA |
| Kas non-karbon, USD 35 | 242 | −103.000 (5,8 %) | SELISIH MATERIAL | SETARA |
| Kas non-karbon, DT 0,03125 | 10,0 | +162 | SELISIH MATERIAL | SETARA |
| Dukungan material rehabilitasi Rp100 juta/th | 22,9 | +743 (0,48 %) | SELISIH MATERIAL | SETARA |
| Dukungan material + kas non-karbon | 29,4 | +699 (0,12 %) | SELISIH MATERIAL | SETARA |

**Penjelasan selisih material:** semua selisih mode endogen hanya muncul bila ada sumber daya non-karbon yang dapat dipertukarkan dengan dana karbon (kas non-karbon atau dukungan material rehabilitasi).
- Galat positif (kredit berlebih) hingga 743 tCO₂e.
- Galat negatif (kredit kurang, konservatif) hingga 103.000 tCO₂e pada USD 35.
- Tanpa sumber daya itu, mode endogen setara persis, termasuk pada k = 0 dan k = 1, variasi efektivitas, variasi rehabilitasi, dan DT halus.
- Mode berpasangan setara persis di semua 15 konfigurasi.

---

## 4. Konsistensi indikator sosial-ekonomi

### 4.1 Upah Rp150.000/HOK di semua variabel upah patroli (lembar 7)

| Identitas (semua t; S1, C20, C35, C20-JP) | Selisih maks |
|---|---|
| `Upah Patroli Berbayar` = HOK berbayar × 150.000 | 0 |
| `Upah Patroli dari Kas LPHD` = HOK kas LPHD × 150.000 | 0 |
| `Upah Setara Non Tunai Patroli` = 150.000 | 0 |
| Nilai tenaga non-tunai = HOK reguler × 150.000 + HOK tanam sukarela × 106.000 | 0 |
| `Upah Kegiatan PS` = patroli + tanam + kebakaran | 0 |
| `Manfaat Ekonomi Patroli` (variabel lama) | 0 |

Nilai 130.000 yang tersisa di model hanya `Upah Harian Pengendalian Kebakaran`. Itu aktivitas lain dan **[PERLU KONFIRMASI]**.

### 4.2 Pemisahan upah tunai, kontribusi sukarela, dan biaya total (lembar 8; kumulatif 2026–2086, nominal)

| Komponen | S1 | S2 C-J1 USD 20 | S2 C-JP USD 20 | S2 C-J1 USD 35 |
|---|---|---|---|---|
| Upah patroli tunai (Rp150.000/HOK) | 0 | Rp3,59 M | Rp10,48 M | Rp37,77 M |
| Biaya patroli total (asumsi Rp260.000/HOK) | 0 | Rp6,22 M | Rp18,16 M | Rp65,46 M |
| Komponen non-upah implisit (asumsi, belum terverifikasi) | 0 | Rp2,63 M | Rp7,68 M | Rp27,70 M |
| Nilai tenaga sukarela (non-tunai, tidak masuk pendapatan) | Rp13,78 M | Rp13,78 M | Rp13,78 M | Rp13,78 M |
| Nilai logistik sukarela (non-tunai) | Rp7,81 M | Rp7,81 M | Rp7,81 M | Rp7,81 M |
| Upah pengendalian kebakaran (Rp130.000, belum dikonfirmasi) | 0 | Rp0,56 M | Rp2,34 M | Rp15,10 M |

### 4.3 Identitas pendapatan

Semua identitas di bawah memiliki selisih maks 0 kecuali disebut:
- pendapatan program per RT = (penerimaan KUPS untuk RT + upah PS × 0,5) × porsi manfaat ÷ RT bergantung;
- pendapatan bersih per RT = pendapatan hutan + non-hutan + program − kehilangan akses;
- kehilangan agregat = per RT × RT bergantung;
- kehilangan per RT terdampak = agregat ÷ RT terdampak;
- identitas surplus KUPS (selisih ≤ 3·10⁻⁸) dan identitas penjualan KUPS;
- penerimaan anggota ≤ surplus ≤ omzet (tanpa pelanggaran);
- nilai non-tunai tidak masuk pendapatan: logistik ×10 → Δ pendapatan RT = 0.

**Kompensasi:** model utama tidak memiliki variabel kompensasi; nilainya 0 di S1 dan S2. Kompensasi hanya ada di eksperimen alokasi (B0–B4, R1–R2) yang belum dijalankan.

### 4.4 S1–S2 sosial-ekonomi

Lembar 9. Rerata 2030–2055; mekanisme C, Referensi S1 endogen (setara persis karena kas non-karbon 0).

| Indikator | S1 | Δ C-J1 USD 10 | Δ C-J1 USD 20 | Δ C-J1 USD 35 | Δ C-JP USD 20 | Δ C-JP USD 35 |
|---|---|---|---|---|---|---|
| HOK patroli reguler (sukarela) | 1.505,5 | 0 | 0 | 0 | 0 | 0 |
| HOK berupah PS | 0 | +116 | +806 | +5.209 | +3.039 | +12.517 |
| FTE berupah | 0 | +0,4 | +2,7 | +17,4 | +10,1 | +41,7 |
| Upah kegiatan PS (Rp/th) | 0 | +17,4 juta | +109,5 juta | +694,9 juta | +409,5 juta | +1.648 juta |
| KUPS aktif (rerata / 2087) | 21,8 / 5,7 | +0 / +0 | +0,6 / +0,3 | +3,0 / +44,7 | +2,0 / +1,5 | +24,2 / +60,1 |
| Penerimaan anggota KUPS (Rp/th) | 15,8 juta | 0 | +1,4 juta | +9,0 juta | +5,4 juta | +43,2 juta |
| Pendapatan program per RT (Rp/th) | 179 | +368 | +2.086 | +11.847 | +7.502 | +28.979 |
| Kehilangan akses per RT bergantung (Rp/th) | 91.803 | +38.611 | +72.261 | +245.061 | +213.282 | +552.157 |
| Kehilangan per RT terdampak (Rp/th) | 228.136 | +95.952 | +179.574 | +608.995 | +530.023 | +1.372.152 |
| Pendapatan bersih per RT bergantung (Rp/th) | 41,2 juta | −270 | −17.909 | −132.944 | −74.116 | −290.079 |
| Kompensasi | 0 | 0 | 0 | 0 | 0 | 0 |
| Cakupan kebutuhan minimum LPHD (%) | 0 | 0 | 5,2 | 38,1 | 21,1 | 95,2 |

**Dekomposisi Δ pendapatan bersih per RT** (lembar 10), contoh USD 20 C-J1:

| Komponen | Δ (Rp/RT/th) |
|---|---|
| Pendapatan hutan (ketersediaan sumber daya naik) | +52.266 |
| Pendapatan program | +2.086 |
| Kehilangan akses | −72.261 |
| **Bersih** | **−17.909** |

Bila pengali kehilangan akses = 0, Δ bersih = **+54.352**. Arah dampak terhadap pendapatan rumah tangga ditentukan oleh asumsi kehilangan akses (kelas D), bukan oleh penerimaan karbon. Belum ada kompensasi di model utama.

---

## 5. Rekonsiliasi status uji

### 5.1 Baterai v1 (37 uji; dilaporkan 2026-11-03)

| Status | Jumlah | Kode |
|---|---|---|
| LULUS | 34 | termasuk U6, yang **ternyata tidak sah** (DT tidak berubah); status v1 U6 dikoreksi menjadi TIDAK SAH |
| GAGAL | 1 | K7 |
| BELUM DILAKUKAN | 1 | V0c (Units Check dan run native Vensim) |
| DILAPORKAN | 1 | W5 (dampak koreksi upah; uji tanpa kriteria lulus) |

### 5.2 Baterai v2 (42 uji; run baru dari model v2)

| Status | Jumlah | Kode |
|---|---|---|
| **LULUS** | **39** | – |
| **GAGAL** | **1** | K7 (mode endogen) |
| **BELUM DILAKUKAN** | **1** | V0c |
| **DILAPORKAN** | **1** | W5 |

Tambahan v2 dibanding v1: RV1, RV2, RV3, RV4, dan K7b.

### 5.3 Riwayat kriteria (lembar 2)

| Kode | Kriteria awal | Kriteria direvisi sesudah hasil | Alasan | Uji ulang independen? |
|---|---|---|---|---|
| R1 | Semua kolom selisih < 10⁻⁹ | Lima indikator kebutuhan LPHD dikecualikan dan selisihnya dilaporkan | Perubahan definisi terdaftar (kebutuhan bruto) | Tidak: penguji sama; v2 memakai run baru |
| K3 | Σ kredit ≤ mitigasi berpasangan | v1: identitas saldo, lalu toleransi 0,5 % (**pelonggaran**). v2: identitas lengkap + mitigasi ≤ berpasangan + kredit bersih − debit ≤ berpasangan | Struktur akuntansi berubah; pelonggaran v1 **dicabut** di v2 | Tidak (penguji sama); run baru |
| K7 | Galat ≤ 10⁻⁶ dan kredit ≤ berpasangan | v1: arah galat, lalu galat kumulatif ≤ 0 | Upaya membedakan arah galat; **tetap GAGAL**, tidak dipakai untuk meloloskan | Diganti K7b (kriteria 10⁻⁹ ditetapkan sebelum hasil) |
| E1b | Kas < 10⁻⁶ Rp | < 1 Rp | Derau numerik 3·10⁻⁶ Rp | Tidak |
| T1 | Biaya modal ≤ pokok | Tidak direvisi; model diperbaiki | Kesalahan numerik model | Run baru |
| U6 | Selisih DT < 2 % | Kriteria tetap; **metode** diperbaiki | v1 tidak mengubah DT | Run baru |
| K7b, RV1–RV4, toleransi A3 | Ditetapkan sebelum run v2 | – | – | – |

Tidak ada uji yang dinyatakan lulus hanya karena toleransinya diperbesar. Satu-satunya pelonggaran (K3 v1) sudah dicabut.

### 5.4 Status per uji (baterai v2)

| Kode | Uji | Status | Bukti ringkas |
|---|---|---|---|
| V0a | Parsing PySD | **LULUS** | read_vensim berhasil; 946 variabel (v2); 16 View |
| V0b | Referensi dan loop aljabar | **LULUS** | referensi tak dikenal 0; loop aljabar 0; pemakai Switch Karbon 14 (9 lama + jembatan + 4 rantai kredit/pelaporan PWD-K) |
| V0c | Units Check dan run native Vensim | **BELUM DILAKUKAN** | Vensim tidak tersedia di lingkungan ini; harus dijalankan peneliti |
| V18 | Konsistensi dimensional (pemeriksa statis) | **LULUS** | 933 persamaan konsisten, 0 bermasalah |
| R1 | Reproduksi Fase 3 dengan upah lama dan mode kredit lama (kriteria direvisi: indikator kebutuhan dikecualikan) | **LULUS** | selisih relatif maks S1/A20/C20 = 0.0e+00/0.0e+00/0.0e+00 pada semua variabel fisik, keuangan, dan sosial; indikator kebutuhan LPHD C20 berbeda 16.1 % karena perubahan definisi terdaftar (kebutuhan bruto, tidak lagi dikurangi jemb… |
| W1 | Upah patroli historis Rp150.000/HOK; HOK dan biaya total tidak berubah | **LULUS** | S1: upah 2024 Rp379.950.000, 2025 Rp451.650.000, total Rp831.600.000; HOK 2.533/3.011; biaya total historis Rp1.441.440.000; C20: upah 2024 Rp379.950.000, 2025 Rp451.650.000, total Rp831.600.000; HOK 2.533/3.011; biaya total histo… |
| W2 | Upah adalah komponen biaya total (tidak ditambahkan) | **LULUS** | upah ≤ biaya patroli total di semua t; rasio upah/biaya = 0.576923 (= 150/260 = 0.576923) di S1, A20, C20, C35 |
| W3 | Nilai non-tunai Rp150.000/HOK dan logistik turunan; tidak masuk pendapatan RT | **LULUS** | logistik swadaya = 9,17 × Rp110.000 = Rp1.008.700/anggota/th (sebelumnya Rp1.192.050); nilai tenaga non-tunai 2030 = 1.505,5 HOK × Rp150.000 = Rp225.825.000; logistik ×10 → /Δ pendapatan RT/ maks 0.0e+00 |
| W4 | Identitas HOK berupah + sukarela = total; identitas patroli | **LULUS** | Kesempatan Kerja PS = HOK berupah + sukarela; Check Identitas Patroli = 0 (S1, A20, C20, C35) |
| W5 | Dampak koreksi upah (S1, terhadap upah lama) | **DILAPORKAN** | pendapatan program per RT 2024: Rp7.765 → Rp8.960; upah kegiatan PS 2025: Rp391.430.000 → Rp451.650.000; hutan 2087 tidak berubah (0,000000 ha) |
| K1 | Rantai Referensi S1 = S1 aktual pada run S1 | **LULUS** | /hutan ref − aktual/ maks 0.0e+00 ha; /emisi bersih biomassa ref − aktual/ maks 0.0e+00 tCO2e/th |
| K2 | B (tanpa jembatan): Referensi S1 = aktual, kredit 0 | **LULUS** | kredit maks B20 0.0e+00, B35 0.0e+00 tCO2e/th: tanpa modal awal tambahan siklus tidak dimulai (diagnostik dipertahankan) |
| K3 | Kredit C endogen (v2): Σ kredit = Σ mitigasi + Σ penyelesaian − saldo; mitigasi ≤ berpasangan; kredit bersih − debit belum diselesaikan ≤ mitigasi berpasangan | **LULUS** | USD6: kredit diajukan 68.835; dibatalkan dari stok sendiri 0; pengganti dibeli 12.862; buffer dipakai 9.387; kredit bersih 46.586; debit belum diselesaikan 2087 2.475; mitigasi eligible (Ref S1) 44.111; mitigasi deforestasi berpas… |
| K4 | Tanpa hitung ganda REDD dan ARR | **LULUS** | REDD (bertanda) + ARR (≥ 0) = pengurangan biomassa bersih terhadap Referensi S1 di semua t (C6, C10, C20, C35) |
| K5 | Konservasi kredit (diajukan → terbit → terjual/stok/kedaluwarsa) | **LULUS** | stok akhir = Σ terbit − Σ terjual − Σ kedaluwarsa (REDD, ARR); C20: diajukan − terbit = 0 (antrean 3 th terakhir); C35: diajukan − terbit = 67.500 (antrean 3 th terakhir); A20: diajukan − terbit = 8.813 (antrean 3 th terakhir) |
| K6 | Kredit konservatif ≤ potensi terhadap BAU | **LULUS** | C20: Σ kredit REDD 100.666 ≤ potensi BAU 271.969 tCO2e |
| K7 | Kas non-karbon tidak dikreditkan (kriteria direvisi: galat acuan kumulatif konservatif dan kredit bersih) | **GAGAL** | kas non-karbon Rp3 M/th: galat emisi Referensi S1 − S1 berpasangan per tahun ∈ [-327; 93] tCO2e/th, kumulatif 163 tCO2e (negatif = acuan lebih protektif = konservatif); penyimpangan positif sesudah 2046 berjumlah 2,046 tCO2e (atri… |
| J1 | Pembiayaan jembatan sesuai kegiatan aktual | **LULUS** | HOK jembatan ≤ kebutuhan tambahan; total patroli ≤ kapasitas; Rp = HOK × 260.000; hanya 2026–2030; S1 = 0; C20: Σ jembatan Rp3.914.300.000, HOK 15.055; C6: Σ jembatan Rp3.914.300.000, HOK 15.055; C35: Σ jembatan Rp3.914.300.000, H… |
| N1 | Neraca kas LPHD dan mitra | **LULUS** | /Check Identitas Arus Kas/ maks 9.5e-07 Rp/th di 11 run; saldo ≥ 0; saldo karbon ≤ saldo |
| N2 | Konsistensi NPV | **LULUS** | NPV inkremental S1 = 0.0e+00; /NPV(C20) − NPV(S1) − NPV inkremental(C20)/ = 9.54e-07 Rp; NPV keseluruhan S1 = −PV pembiayaan historis = Rp-1.310.893.298 |
| N3 | S1 = S2 (fisik dan sosial) sebelum kegiatan proyek pertama (2026) | **LULUS** | selisih maks 2024–2025 pada 7 variabel = 0.0e+00 |
| M1 | Penghentian MRV prospektif (B20) | **LULUS** | proyek dihentikan t = 2033.0625; biaya MRV sesudahnya 0; biaya MRV ditanggung mitra Rp2.894.247.632 (vs Rp22.771.504.226 tanpa aturan) |
| M2 | Penghentian MRV pada C20 hanya sesudah penerimaan < biaya | **LULUS** | t henti = 2054.1875; NPV mitra Rp-1.354.264.687 (tanpa aturan Rp-1.578.730.679); defisit MRV 2087 Rp269.543.019 (tanpa aturan Rp15.203.196.868) |
| M3 | Penundaan monitoring MRV | **LULUS** | biaya monitoring 2024–2025 = 0 bila ditunda ke 2026; Σ MRV Rp27.101.664.952 vs Rp27.545.525.942 |
| T1 | Biaya modal dibatasi (perbaikan T-a) | **LULUS** | T_C6_bm10: pokok Rp3.914.300.000, biaya modal Rp3.914.300.000, sisa 2087 Rp7.828.600.000; T_C10_sesudah_bm10: pokok Rp3.914.300.000, biaya modal Rp3.914.300.000, sisa 2087 Rp6.523.222.874 (Fase 3: sisa C6 bm10 = Rp1.344 M) |
| T2 | Penghapusan talangan dengan pengakuan kerugian | **LULUS** | sisa sesudah 2045 = 0.0e+00; kerugian mitra diakui Rp7.828.600.000; identitas pokok + biaya modal − pemulihan − penghapusan − sisa = 5.7e-06 Rp; NPV mitra sama dengan tanpa penghapusan (-5.471.722.186 vs -5.471.722.186) |
| RV1 | Penyelesaian reversal hanya pada peristiwa verifikasi, tidak pada setiap tahun S2 > S1 | **LULUS** | C6: deforestasi S2>S1 pertama 2040.75; debit pertama 2039.875; pembelian pertama 2062.0; penyelesaian hanya pada pulsa verifikasi; C15: deforestasi S2>S1 pertama 2046.1875; debit pertama 2045.25; pembelian pertama 2067.0; penyeles… |
| RV2 | Tanpa penalti ganda: saldo dipulihkan sesudah penyelesaian (aturan 2) | **LULUS** | C6: 11 pulsa verifikasi; C15: 11 pulsa verifikasi; C20: 11 pulsa verifikasi; sesudah setiap penyelesaian saldo kembali ke ≥ −(mitigasi negatif satu DT) |
| RV3 | Konservasi buffer dan stok kredit sesudah pembatalan | **LULUS** | buffer tersedia = kontribusi − pemakaian; buffer dan stok ≥ 0 (C6, C20, aturan 1) |
| RV4 | Aturan 0/1/2 berperilaku sesuai definisi | **LULUS** | debit 2087: aturan 0 26.216, aturan 1 12.489, aturan 2 3.878 tCO2e; biaya pengganti aturan 2 Rp2.841.464.079; NPV mitra aturan 0/1/2 = -1.563.007.354/-1.563.007.355/-1.578.730.679 |
| K7b | Referensi S1 berpasangan = S1 mandiri pada semua konfigurasi gerbang (termasuk kas non-karbon) | **LULUS** | 15/15 konfigurasi setara (galat relatif ≤ 1e-9) |
| E1 | Harga 0 tanpa jembatan → S2 = S1 | **LULUS** | selisih maks 0.0e+00 |
| E1b | Harga 0 dengan jembatan: kas penjualan 0, mitra menanggung jembatan + MRV | **LULUS** | Δ hutan 2087 = 175,7 ha (efek jembatan saja); NPV mitra Rp-7.485.931.308 |
| E2 | k = 0: patroli reguler S1 = 0 sesudah 2025 | **LULUS** | kredit C20 (k = 0) = 84.466 tCO2e |
| E3 | k = 1: patroli reguler = 3.011 ≤ kapasitas | **LULUS** | HOK reguler 2030 = 3.011,0 |
| E4 | Kas non-karbon sangat besar | **LULUS** | belanja ≤ kebutuhan; intensitas maks 1.000; saldo 2087 Rp60.366.283.690.665 |
| E5 | Harga USD 500 | **LULUS** | stok ≥ 0; intensitas maks 1.000; hutan 2087 89.944 ha |
| E6 | Efektivitas 0: patroli tidak mengubah deforestasi; kredit REDD 0 | **LULUS** | Δ deforestasi 0.0e+00 ha; kredit REDD 0.0e+00 |
| U6 | Langkah waktu 0,0625 vs 0,03125 (v2: DT lewat argumen time_step; v1 tidak sah) | **LULUS** | S1 Total Hutan 0.002 %; S1 NPV Mitra 0.149 %; S1 Kredit Karbon Diajukan 0.000 %; S1 Deforestasi Total 0.002 %; C20 Total Hutan 0.001 %; C20 NPV Mitra 0.369 %; C20 Kredit Karbon Diajukan 0.080 %; C20 Deforestasi Total 0.001 % |
| P1 | Urutan kausal jembatan → patroli → deforestasi → kredit → kas → patroli LPHD (C20) | **LULUS** | patroli jembatan 2026.0; deforestasi C20 < S1 2026.0625; kredit diajukan 2026.0625; kredit terbit 2029.0625; kas penjualan 2029.125; kas LPHD karbon 2034.0625; patroli kas LPHD 2034.125 |
| P2 | Putus loop dana LPHD → patroli (C35) | **LULUS** | Δ hutan 2087: 4.842 ha → 220 ha (sisa = efek jembatan + rehabilitasi) |
| P3 | Harga naik → hutan 2087 tidak turun (C) | **LULUS** | 82.975 / 82.975 / 83.016 / 83.112 / 87.641 ha (USD 6–35) |

---

## 6. Langkah sesudah gerbang

Semua masalah struktural material sudah diselesaikan dengan syarat di bagian Keputusan. Karena itu dilanjutkan ke **Tahap 3: simulasi deterministik**, dengan konfigurasi:
- S1 dan S2 mekanisme C;
- jembatan J1 dan JP;
- harga USD 6, 10, 15, 20, dan 35;
- protokol Referensi S1 berpasangan;
- model v2.

Hasilnya ada di `LAPORAN_SIMULASI_DETERMINISTIK_FASE4.md` dan `HASIL_SIMULASI_FINAL_PWD.xlsx`.

**Berkas skrip:** `skrip/fase4_gate/`
- `k7.py`, `k7dt.py`: diagnosis K7;
- `gate.py`, `gate_olah.py`: uji kesetaraan Referensi S1;
- `sosek.py`, `sosek_olah.py`: audit sosial-ekonomi;
- `xlsx_gate.py`;
- `skrip/fase4/runs4.py` dan `uji4.py`: baterai v2.
