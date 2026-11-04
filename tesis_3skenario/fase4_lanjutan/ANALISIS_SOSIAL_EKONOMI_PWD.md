# Analisis Sosial-Ekonomi PWD: Pekerjaan, KUPS, dan Ekonomi Rumah Tangga

**Tanggal:** 4 November 2026

**Sumber:**
- deterministik: `HASIL_SIMULASI_FINAL_PWD.xlsx` (Fase 4 Tahap 3);
- Monte Carlo: `HASIL_MONTE_CARLO_PRCC_PWD.xlsx`;
- alokasi: `HASIL_BENEFIT_SHARING_PWD.xlsx`.

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

## 1. Manfaat kolektif LPHD ≠ pendapatan tunai rumah tangga

Kas karbon yang masuk ke LPHD adalah **dana kolektif desa**. Dana ini membiayai patroli, rehabilitasi, pengendalian kebakaran, KUPS, operasional, dan penguatan kelembagaan. Hanya sebagian yang menjadi uang tunai rumah tangga, yaitu:
- upah kegiatan berupah (patroli, tanam, kebakaran);
- bagian surplus KUPS yang dibagikan kepada anggota (26,3 %);
- kompensasi, bila dialokasikan.

Kontribusi tenaga sukarela (Rp150.000/HOK) dan logistik bukan pendapatan.

**Aliran kumulatif** (deterministik, B0, tanpa kompensasi):

| Aliran kumulatif 2024–2086 (Rp miliar, nominal) | C-J1 USD 20 | C-J1 USD 35 | C-JP USD 20 | C-JP USD 35 |
|---|---|---|---|---|
| Kas penjualan kredit | 29,07 | 408,71 | 81,53 | 655,24 |
| Biaya MRV, transaksi, pajak, pengganti | 27,55 | 47,58 | 30,12 | 62,47 |
| Dana mitra 40 % | 5,12 | 142,89 | 21,61 | 233,73 |
| Pembiayaan jembatan oleh mitra | 3,91 | 3,91 | 8,44 | 8,44 |
| Kas LPHD (dana kolektif) | 7,69 | 214,33 | 32,42 | 350,60 |
| …dibelanjakan LPHD | 7,69 | 207,91 | 32,42 | 344,85 |
| …di antaranya upah tunai dibayar dari kas LPHD | 2,40 | 64,73 | 10,07 | 101,67 |
| Upah tunai PS total S2−S1 (termasuk jembatan) | 4,65 | 66,99 | 14,94 | 106,54 |
| Penerimaan anggota KUPS S2−S1 | 0,05 | 1,53 | 0,20 | 3,53 |
| Tambahan kehilangan akses agregat S2−S1 | 16,32 | 254,00 | 50,69 | 368,44 |
| Kompensasi (B0) | 0,00 | 0,00 | 0,00 | 0,00 |
| Defisit MRV yang tetap ditanggung mitra 2087 | 15,20 | 0,00 | 11,06 | 0,00 |

**Bacaan:**
- Pada C-J1 USD 20, kas penjualan Rp29,07 miliar dipakai untuk:
  - biaya bersama yang dibayar dari penjualan Rp10,69 miliar;
  - pemulihan defisit MRV Rp1,65 miliar;
  - pemulihan talangan jembatan Rp3,91 miliar;
  - bagian LPHD Rp7,69 miliar dan bagian mitra Rp5,12 miliar.

  Biaya bersama bruto Rp27,55 miliar (baris tabel di atas) mencakup Rp16,85 miliar yang ditalangi mitra; hanya Rp1,65 miliar yang dipulihkan, sehingga sisa defisit Rp15,20 miliar. Arus kas mitra nominal S2 − S1 = −Rp10,08 miliar (NPV −Rp0,27 miliar [SEMENTARA], karena defisit jatuh sesudah 2051). Rekonsiliasi lengkap: `AUDIT_AKADEMIK_FINAL_PWD.md` §1.
  - *Koreksi 2026-11-04:* versi sebelumnya menjumlahkan biaya bruto dengan bagian LPHD dan mitra sehingga totalnya melebihi kas penjualan.
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
