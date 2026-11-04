# Persetujuan Final Model dan Hasil Fase 5

**Tanggal:** 4 November 2026

**Lingkup:** pemeriksaan penutup Fase 5 sebelum revisi makalah.

**Perangkat:** PySD 3.14.3. **Vensim native: BELUM DIVERIFIKASI NATIVE.** NPV: **SEMENTARA**.

---

## Keputusan

1. **Tidak ditemukan kesalahan material pada persamaan model.** Persamaan tidak diubah.
2. **Model dibekukan untuk penulisan makalah** sebagai `MODEL_FINAL_DUA_SKENARIO_PWD_v2_1.mdl` (md5 `66a7fad8decfedad00a72564d9311be4`) dan `MODEL_FINAL_DUA_SKENARIO_PWD_v2_1_ALOKASI.mdl` (md5 `cd99d60fd4b6f8a821cefdcafaa67b22`).
   - v2.1 = v2 dengan **satu koreksi komentar** (biaya patroli, §5).
   - 946/946 dan 964/964 persamaan serta satuan identik; sketsa 16 View identik.
   - Simulasi S1 dan S2-C-J1 USD 20 identik dengan v2 (selisih 0 pada 193 variabel).
   - Semua hasil Fase 4, Fase 4 lanjutan, Audit Akademik, dan Fase 5 tetap berlaku untuk v2.1.
3. **Kesiapan revisi makalah: SIAP**, dengan syarat penulisan di bagian akhir dokumen ini.

---

## 1. Audit konsekuensi `Status Proyek Karbon Aktif = 0` pada D1

**Jalur struktural.** Variabel ini dipakai langsung oleh tujuh persamaan:
- `Kredit REDD Diajukan`, `Kredit ARR Diajukan`, `Kredit Gambut Diajukan`;
- `Biaya Monitoring MRV`, `Biaya Verifikasi Tahunan`;
- `Mitigasi REDD Eligible Bersih Proyek`, `Kontribusi Buffer REDD`.

Secara transitif, 538 variabel berada di hilirnya. Variabel itu **tidak** dipakai oleh `Hari Patroli Didanai Jembatan`, sehingga jembatan identik di D1 dan D2 (15,06 ribu HOK; Rp3,91 M).

**Urutan waktu:**

| | USD 20 | USD 35 |
|---|---|---|
| Kas penjualan pertama di D2 | 2029.12 | 2029.12 |
| Kas LPHD pertama di D2 | 2034.06 | 2032.75 |

- **Sebelum kas LPHD pertama,** D1 dan D2 hanya berbeda pada 34 variabel kredit, MRV, kas, buffer, kewajiban, dan NPV.
- **Semua variabel fisik dan sosial identik** sampai kas LPHD pertama: tutupan, deforestasi, emisi, patroli, HOK berupah, KUPS, pendapatan RT, saldo LPHD, dan penanaman. Variabel fisik pertama yang berbeda adalah total HOK patroli dan saldo LPHD (USD 20: 2034,13; USD 35: 2032,81).

**Uraian D1 → D2** (kumulatif 2024–2086, nominal; ekologis 2025/2031–2086):

| Komponen | D1 USD 20 | D2 USD 20 | D2−D1 USD 20 | D1 USD 35 | D2 USD 35 | D2−D1 USD 35 |
|---|---|---|---|---|---|---|
| **A. Kredit** | | | | | | |
| Kredit diajukan (ribu tCO₂e) | 0,00 | 100,67 | 100,67 | 0,00 | 908,85 | 908,85 |
| Kredit terbit (ribu tCO₂e) | 0,00 | 100,67 | 100,67 | 0,00 | 841,35 | 841,35 |
| Kredit terjual (ribu tCO₂e) | 0,00 | 88,08 | 88,08 | 0,00 | 711,33 | 711,33 |
| **B. Biaya MRV dan transaksi (Rp M)** | | | | | | |
| Monitoring MRV | 0,00 | 13,86 | 13,86 | 0,00 | 13,86 | 13,86 |
| Verifikasi | 0,00 | 8,91 | 8,91 | 0,00 | 8,91 | 8,91 |
| Penerbitan dan registri | 0,00 | 0,42 | 0,42 | 0,00 | 3,47 | 3,47 |
| Transaksi penjualan | 0,00 | 0,06 | 0,06 | 0,00 | 0,90 | 0,90 |
| Pajak dan pungutan | 0,00 | 1,45 | 1,45 | 0,00 | 20,44 | 20,44 |
| Pembelian kredit pengganti | 0,00 | 2,84 | 2,84 | 0,00 | 0,00 | 0,00 |
| Total biaya bersama periode berjalan | 0,00 | 27,55 | 27,55 | 0,00 | 47,58 | 47,58 |
| **C. Penjualan dan bagi hasil (Rp M)** | | | | | | |
| Kas penjualan diterima | 0,00 | 29,07 | 29,07 | 0,00 | 408,71 | 408,71 |
| Bagian LPHD 60 % | 0,00 | 7,69 | 7,69 | 0,00 | 214,33 | 214,33 |
| Bagian mitra 40 % | 0,00 | 5,12 | 5,12 | 0,00 | 142,89 | 142,89 |
| **D. Kewajiban dan pemulihan (Rp M)** | | | | | | |
| Pembiayaan jembatan | 3,91 | 3,91 | 0,00 | 3,91 | 3,91 | 0,00 |
| Kerugian/hibah jembatan diakui mitra | 3,91 | 0,00 | -3,91 | 3,91 | 0,00 | -3,91 |
| Pemulihan talangan jembatan | 0,00 | 3,91 | 3,91 | 0,00 | 3,91 | 3,91 |
| Kekurangan biaya ditalangi mitra | 0,00 | 16,85 | 16,85 | 0,00 | 1,59 | 1,59 |
| Pemulihan defisit MRV historis | 0,00 | 1,65 | 1,65 | 0,00 | 1,59 | 1,59 |
| Defisit MRV belum dipulihkan, akhir periode | 0,00 | 15,20 | 15,20 | 0,00 | 0,00 | 0,00 |
| **E. Kegiatan LPHD yang dibiayai kas karbon** | | | | | | |
| Belanja LPHD perlindungan | 0,00 | 2,31 | 2,31 | 0,00 | 61,55 | 61,55 |
| Belanja LPHD rehabilitasi | 0,00 | 1,15 | 1,15 | 0,00 | 31,36 | 31,36 |
| Belanja LPHD pengendalian kebakaran | 0,00 | 0,77 | 0,77 | 0,00 | 20,91 | 20,91 |
| Belanja LPHD KUPS | 0,00 | 1,54 | 1,54 | 0,00 | 41,82 | 41,82 |
| Belanja LPHD operasional | 0,00 | 0,77 | 0,77 | 0,00 | 20,91 | 20,91 |
| Belanja LPHD kelembagaan | 0,00 | 1,15 | 1,15 | 0,00 | 31,36 | 31,36 |
| Patroli dari kas LPHD (ribu HOK) | 0,00 | 8,87 | 8,87 | 0,00 | 236,73 | 236,73 |
| HOK pengendalian kebakaran (ribu) | 0,00 | 4,27 | 4,27 | 0,00 | 116,16 | 116,16 |
| Rehabilitasi ditanam (ha) | 0 | 57 | 57 | 0 | 1.567 | 1.567 |
| **F. Dampak ekologis** | | | | | | |
| Deforestasi 2031–2086 (ha) | 25.640 | 25.473 | -167 | 25.640 | 20.973 | -4.667 |
| Serapan rehabilitasi (ribu tCO₂e) | 0,00 | 12,44 | 12,44 | 0,00 | 303,42 | 303,42 |
| Emisi bersih biomassa (ribu tCO₂e) | 7.431,78 | 7.375,61 | -56,17 | 7.431,78 | 5.837,61 | -1.594,16 |

**Bacaan:**
- **USD 20.** Aktivasi mekanisme menghasilkan Rp29,07 M kas penjualan dengan biaya MRV dan transaksi Rp27,55 M.
  - Rp16,85 M dari biaya itu ditalangi mitra, dan hanya Rp1,65 M yang pulih.
  - Jembatan berubah status dari hibah (D1: kerugian Rp3,91 M) menjadi talangan yang pulih penuh.
  - LPHD menerima Rp7,69 M dan membelanjakannya untuk patroli (8,87 ribu HOK), rehabilitasi (57 ha), kebakaran, KUPS, operasional, dan kelembagaan.
  - Hasil ekologis bersihnya: 167 ha deforestasi dihindari dan 56,2 ribu tCO₂e emisi bersih.
- **USD 35.** Kas penjualan Rp408,71 M, biaya Rp47,58 M, LPHD Rp214,33 M, dan 4.667 ha deforestasi dihindari.

## 2. Label kontras

| Kontras | Label yang dipakai mulai dokumen ini dan di makalah | Isi |
|---|---|---|
| D1 − D0 | **Efek pembiayaan awal (jembatan) tanpa mekanisme karbon** | Patroli tambahan 2026–2030 yang dibiayai mitra sebagai hibah |
| D2 − D1 | **Kontribusi bersih aktivasi mekanisme perdagangan karbon setelah pembiayaan awal** | Gabungan: biaya MRV dan transaksi; kredit dan penjualan; perubahan status jembatan (hibah → talangan dipulihkan); prioritas pemulihan defisit dan talangan; bagi hasil 60/40; kegiatan LPHD yang dibiayai kas karbon; penyelesaian *reversal* |
| D2 − D0 | **Efek paket lengkap S2** | = S2 − S1 |
| D3 − D0 | **Mekanisme karbon tanpa pembiayaan awal** | Lihat §4 |

**D2 − D1 bukan pengaruh murni penjualan kredit.** Label "penjualan karbon sesudah jembatan" di `HASIL_EKSPERIMEN_D0_D3.xlsx`, `LAPORAN_DEKOMPOSISI_PEMBIAYAAN_KARBON.md`, `TEMUAN_FINAL_DAN_KETERBATASAN_PWD.md`, dan grafik G1–G6 **digantikan** oleh label di atas. Angkanya tidak berubah.

## 3. Status D0–D3

D0–D3 adalah **eksperimen diagnostik internal** untuk memisahkan pengaruh pembiayaan awal dari mekanisme perdagangan karbon.
- D0–D3 **bukan** empat skenario kebijakan dan tidak menggantikan desain dua skenario (S1, S2).
- Dekomposisi D2 − D0 = (D1 − D0) + (D2 − D1) adalah identitas aritmetis menurut asumsi model, **bukan identifikasi kausal empiris**.

## 4. Tafsir D3 (tanpa kredit)

D3 tidak menghasilkan kredit pada semua harga dan variasi yang diuji. Ini **hasil struktur model dan aturan additionality internal**, bukan hukum umum perdagangan karbon.

**Penyebabnya:**
1. Kredit mekanisme C hanya mengakui mitigasi **di atas Referensi S1**, yang sudah memuat semua kegiatan tanpa dana karbon.
2. Tanpa dana di luar penjualan kredit, tidak ada kegiatan di atas S1.
3. Tanpa kegiatan itu tidak ada kredit, dan tanpa kredit tidak ada kas.

**Kondisi yang dapat mengubah hasil itu tidak dimodelkan pada D3:**
- pembiayaan pra-penjualan (investor, pembelian di muka/ERPA);
- baseline kredit lain, misalnya baseline BAU (mekanisme A Fase 3 menghasilkan kredit tanpa jembatan, tetapi tidak lolos uji additionality model);
- pendanaan non-karbon untuk kegiatan tambahan;
- aturan crediting standar tertentu.

Pernyataan yang sah: *dalam kerangka kredit konservatif penelitian ini, mekanisme karbon memerlukan pembiayaan awal untuk dapat berjalan.*

## 5. Audit metadata biaya patroli

| Lokasi | Sebelum | Sesudah (v2.1) |
|---|---|---|
| Komentar `Biaya per Hari Patroli` (baris 1715) | "Upah Rp130.000/orang-hari + logistik Rp130.000 …" (REV-V4) | Biaya **total** Rp260.000/HOK = **asumsi kerja kelas D, belum terverifikasi**. Terdiri atas upah Rp150.000/HOK (data dikonfirmasi peneliti, kelas A) + komponen non-upah implisit Rp110.000/HOK (turunan asumsi, bukan logistik terverifikasi). Upah adalah komponen, bukan tambahan. Asal nilai dan rentang uji dicantumkan |
| `Upah Harian Patroli Berbayar` (persamaan 150.000; komentar PWD-U) | sudah benar | tidak berubah |
| `Komponen Non Upah Biaya Patroli`, `Biaya Operasional Patroli Sukarela…` | sudah benar (komentar menyebut 130.000 hanya sebagai nilai sebelumnya) | tidak berubah |
| `Upah Harian Pengendalian Kebakaran` = 130.000 | aktivitas lain; belum dikonfirmasi | tidak berubah; tetap ditandai [PERLU KONFIRMASI] |

Laporan lama yang memuat Rp130.000 sebagai upah patroli (Fase 1B dan audit 3 skenario) adalah arsip. Daftarnya ada di `fase4/LAPORAN_KOREKSI_UPAH_DAN_BIAYA_PATROLI.md` §6; seluruh hasil Fase 4 dan sesudahnya memakai Rp150.000.

## 6. Rekonsiliasi hasil USD 20 dan USD 35

| Harga | Indikator | Fase 4 Tahap 3 | Audit Akademik | Fase 5 (D2 − D0) | Status | Keterangan |
|---|---|---|---|---|---|---|
| USD 20 | Deforestasi dihindari 2025–2086 (ha) | 454 | – | 454 | KONSISTEN |  |
| USD 20 | Arus kas mitra nominal S2−S1 (Rp M) | – | -10,08 | -10,08 | KONSISTEN | Nilai absolut D2 di tabel Fase 5 (−11,52 / +141,45) memuat pembiayaan historis Rp1,44 M yang sama di S1 |
| USD 20 | NPV mitra inkremental (Rp M) [SEMENTARA] | -0,27 | – | -0,27 | KONSISTEN | Nilai absolut D2 (−1,58 / +5,35) memuat −1,31 historis |
| USD 20 | NPV inkremental karbon/proyek (Rp M) [SEMENTARA] | 1,75 | – | 1,75 | KONSISTEN |  |
| USD 20 | Dana kolektif LPHD dari karbon (Rp M) | 7,69 | 7,69 | 7,69 | KONSISTEN |  |
| USD 20 | Δ FTE berupah 2030–2055 | 2,69 | – | 2,69 | KONSISTEN |  |
| USD 20 | Δ FTE berupah 2060–2086 | 0,00 | – | 0,00 | KONSISTEN |  |
| USD 20 | KUPS aktif 2087 (S2) | 6,06 | – | 6,06 | KONSISTEN |  |
| USD 20 | Δ pendapatan bersih per RT bergantung (Rp/th) | -17.909 | -17.909 | -17.909 | KONSISTEN |  |
| USD 20 | Δ pendapatan per RT terdampak (Rp/th) | – | -125.222 | -125.222 | KONSISTEN | Fase 4 Tahap 3 melaporkan Δ kehilangan per RT terdampak (+179.574 / +608.995), bukan pendapatan |
| USD 20 | Upah tunai PS S2−S1 (Rp M) | – | 4,65 | 4,65 | KONSISTEN |  |
| USD 35 | Deforestasi dihindari 2025–2086 (ha) | 4.954 | – | 4.954 | KONSISTEN |  |
| USD 35 | Arus kas mitra nominal S2−S1 (Rp M) | – | 142,89 | 142,89 | KONSISTEN | Nilai absolut D2 di tabel Fase 5 (−11,52 / +141,45) memuat pembiayaan historis Rp1,44 M yang sama di S1 |
| USD 35 | NPV mitra inkremental (Rp M) [SEMENTARA] | 6,66 | – | 6,66 | KONSISTEN | Nilai absolut D2 (−1,58 / +5,35) memuat −1,31 historis |
| USD 35 | NPV inkremental karbon/proyek (Rp M) [SEMENTARA] | 18,36 | – | 18,36 | KONSISTEN |  |
| USD 35 | Dana kolektif LPHD dari karbon (Rp M) | 214,33 | 214,33 | 214,33 | KONSISTEN |  |
| USD 35 | Δ FTE berupah 2030–2055 | 17,36 | – | 17,36 | KONSISTEN |  |
| USD 35 | Δ FTE berupah 2060–2086 | 39,50 | – | 39,50 | KONSISTEN |  |
| USD 35 | KUPS aktif 2087 (S2) | 50,44 | – | 50,44 | KONSISTEN |  |
| USD 35 | Δ pendapatan bersih per RT bergantung (Rp/th) | -132.944 | -132.944 | -132.944 | KONSISTEN |  |
| USD 35 | Δ pendapatan per RT terdampak (Rp/th) | – | -496.878 | -496.878 | KONSISTEN | Fase 4 Tahap 3 melaporkan Δ kehilangan per RT terdampak (+179.574 / +608.995), bukan pendapatan |
| USD 35 | Upah tunai PS S2−S1 (Rp M) | – | 66,99 | 66,99 | KONSISTEN |  |

**Catatan basis:**
- **Arus kas mitra dan NPV mitra** harus dilaporkan sebagai **kontras (S2 − S1 = D2 − D0)**. Nilai absolut D2 memuat pembiayaan historis 2024–2025 (−Rp1,44 M nominal; −Rp1,31 M PV) yang sama di S1.
- **Erratum:** di `TEMUAN_FINAL_DAN_KETERBATASAN_PWD.md`, baris USD 35 semula memakai nilai absolut (+Rp141,4 M) sedangkan baris USD 20 memakai kontras. Sudah dikoreksi menjadi +Rp142,9 M (D2 − D0).
- **NPV inkremental karbon** (+1,75 / +18,36 M) berbeda dari NPV mitra inkremental (−0,27 / +6,66 M). Keduanya SEMENTARA.
- **"Pendapatan RT terdampak"** = pendapatan hutan + non-hutan + program − kehilangan per RT terdampak (rerata 2030–2055). Fase 4 Tahap 3 hanya melaporkan komponen kehilangan.
- **FTE berupah 2060–2086 pada USD 20** = 0,0001, dibaca 0.

## 7. Keterbatasan yang tetap berlaku

1. Vensim native belum diverifikasi (Units Check dan pembandingan lintasan).
2. K7 mode endogen GAGAL; semua hasil S2 memakai Referensi S1 berpasangan.
3. NPV SEMENTARA: biaya pengembangan dan material = 0; diskonto 10 % tidak bersumber.
4. Parameter kelas D menentukan besaran dan sebagian arah hasil:
   - biaya total Rp260.000/HOK;
   - jembatan J1/JP;
   - pengali kehilangan akses (arah pendapatan RT);
   - RT bergantung 5.328 (proksi);
   - parameter KUPS;
   - k; porsi upah bersih.
5. Aturan MRV, penyelesaian *reversal*, dan prioritas pemulihan adalah aturan model tanpa dasar kontraktual.
6. D1 dibentuk dengan menimpa variabel status (bukan switch eksplisit). Ekuivalensinya di Vensim native belum diuji.
7. Hasil berlaku untuk agregat 25 HD. Tidak ada klaim kemiskinan, ketimpangan, atau kausalitas empiris.

## 8. Syarat penulisan makalah

1. **Model:** pakai v2.1 dan nyatakan statusnya (PySD; Vensim native belum; NPV SEMENTARA).
2. **Desain:** dua skenario kebijakan (S1, S2-C). D0–D3 disajikan sebagai eksperimen diagnostik dengan label §2.
3. **Atribusi:** sebutkan bahwa pada USD ≤ 20 sebagian besar tambahan perlindungan berasal dari pembiayaan awal (100 % / 63 %, rentang 8–100 % antarvariasi). Sebutkan juga bahwa mekanisme karbon tidak berjalan tanpa pembiayaan awal dalam kerangka kredit konservatif (§4).
4. **Keuangan:** laporkan kontras S2 − S1 (nominal dan NPV), dengan rekonsiliasi Audit Akademik §1.
5. **Pendapatan RT:** sajikan sebagai bersyarat pada pengali kehilangan akses, dengan pengali impas.
6. **Alokasi:** kesamaan R1 = B0 adalah konstruksi; R1 tidak optimal secara umum.
7. **Larangan:**
   - angka empat skenario;
   - kata "peluang" untuk frekuensi ensembel;
   - kredit model sebagai kredit terverifikasi;
   - NPV sebagai hasil final.
8. **Daftar perubahan makalah:** `AUDIT_AKADEMIK_FINAL_PWD.md` §5, ditambah butir 2–3 di atas.
