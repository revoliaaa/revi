# Review Perhitungan Karbon Gambut — Hutan Desa, KHG Sungai Mempawah

File yang diperiksa: `Export_Output_Gambut_MEMPAWAH_1_asli.xlsx`, berisi 7 sheet: Detail1, Tuplah, Tuplah (2), 2021, Export_Output, Tutupan lahan, Gambut.
Model koreksi: `Model_Koreksi_Karbon_Gambut_Mempawah.xlsx`. Semua rumus di model ini aktif dan parameternya bisa diubah.

## Kesimpulan

**Data spasial di file ini valid. Perhitungan emisi dan kreditnya belum valid.**

- **Luas sudah konsisten.** Hasil overlay tutupan PL2022 × kedalaman gambut sama dengan sheet Gambut (453,93 / 1.586 / 428,57 ha; total 2.468,5 ha). Total tutupan 2016, 2021, dan 2026 masing-masing 2.468,5 ha. Kehilangan hutan bruto 82,87 ha dikurangi penambahan 41,94 ha sama dengan penurunan hutan neto 40,91 ha.
- **Rumus kerapatan C gambut sudah benar** (tebal × 10.000 × BD × C). Stok gambut berdasarkan kedalaman ≈ **1,36 juta tC (4,99 juta tCO2e)**.
- **Angka kredit belum valid.** Ada empat blok perhitungan kredit, dan hasilnya sangat berbeda: 6 tCO2e/thn, 9.807 tCO2e/thn, 13.745 tCO2e/thn, dan 15.642 tCO2e/thn. Tidak satu pun bisa dipertahankan di depan VVB. Ada empat kesalahan utama:
  1. **Emisi deforestasi dihitung dengan cara yang salah.** Rumusnya: stok karbon *seluruh kolom gambut di seluruh area* × 1,16%. Rumus ini menganggap seluruh gambut, termasuk di lahan non-hutan, langsung terlepas. Biomassa pohon justru tidak dihitung sama sekali.
  2. **Laju 1,16%/thn tidak punya sumber.** Data proyek sendiri menunjukkan laju bruto **0,57%/thn** (2016–2026) atau neto **1,78%/thn** (2021–2026).
  3. **"Additional 43%" dipakai sebagai faktor pengali.** Additionality adalah uji lulus/gagal, bukan pengali emisi.
  4. **Ada kesalahan input dan rujukan sel.** AGB diketik 22291 (seharusnya 222,91). Fraksi C diketik 45 (seharusnya 0,45). Ada rumus yang merujuk kolom emisi padahal seharusnya kolom luas. Q31 merujuk nilai per hektare, bukan total.
- **Hasil model koreksi (indikatif, rerata 10 tahun):**

| Skenario | Laju deforestasi | Stok C hutan | Kredit bersih (tCO2e/thn) |
|---|---|---|---|
| Konservatif (default) | 8,29 ha/thn (bruto 2016–2026) | 135,1 tC/ha | **≈ 1.240** |
| Laju terkini | 27,6 ha/thn (neto 2021–2026) | 135,1 tC/ha | ≈ 4.130 |
| Stok rendah | 8,29 ha/thn | 79,7 tC/ha | ≈ 745 |

Faktor pengurang yang dipakai: efektivitas 43% × (1 − leakage 15%) × (1 − buffer 20%). Dengan dasar ini, kredit di file asal (13.700–15.600 tCO2e/thn) **3,8 sampai 12,6 kali lebih tinggi** dari hasil model koreksi.

Nilai porsi LPHD dalam skenario konservatif (60%, kurs Rp 16.000): sekitar Rp 59 juta/thn pada USD 5, Rp 119 juta/thn pada USD 10, dan Rp 178 juta/thn pada USD 15. Angka di file asal miliaran rupiah per tahun.

## 1. Temuan pemeriksaan

Daftar lengkap ada di sheet `Daftar_Temuan` (22 temuan). Yang paling berpengaruh:

| # | Lokasi | Masalah | Dampak |
|---|---|---|---|
| 1 | Tuplah!P53, Tuplah (2)!Q41 | Emisi = stok CO2e gambut seluruh area × 1,16% | Biomassa tidak masuk. Gambut di bawah semak, kebun, dan lahan terbuka ikut dihitung sebagai "hutan" yang terdeforestasi. Seluruh kolom 1,5 m dianggap teroksidasi. |
| 2 | Tuplah (2)!Q31 | `=P37*Q30`, padahal P37 = tCO2e **per ha** | Hasil 22,7 tCO2e/thn, sehingga nilai kredit hanya Rp 0,9 juta |
| 3 | Tuplah (2)!B57, B59, C60 | 22291 / 66876 / 196568, seharusnya 222,91 / 668,73 / 1.965,68 | Nilai membengkak 100×. Baris BGB memakai 64,64 (benar), jadi antarbaris tidak konsisten. |
| 4 | Tuplah (2)!C61–D64 | Biomassa per-ha dijumlah dengan stok gambut total (tC), lalu ×50% dan ×35 | Menjumlahkan dua satuan yang berbeda |
| 5 | Tuplah!D55, D63; Tuplah (2)!D33, D43 | Rumus memakai kolom C (emisi), seharusnya B (luas) | Stok perkebunan 14,8–23,4 juta tC (mustahil) |
| 6 | Tuplah (2)!D34 | Fraksi C diketik `45` | Stok ×100 |
| 7 | Antarblok | Tebal 0,25 / 1 / 1,5 m; BD 0,06–0,13; fraksi C 0,2 / 0,45 / 0,51 / 0,53 / 0,55 | Stok gambut berkisar 0,8–34,5 juta tC tergantung blok. Fraksi C 0,2 tidak realistis untuk gambut. |
| 8 | Tuplah!R52 vs Tuplah (2)!S30 | "Net VCU" = ×0,35 di satu blok, ×(1−0,35) di blok lain | Hasil berbeda hampir 2× |
| 9 | Tuplah!C61:C64 | Kolom "Emisi" berisi 98,84 / 2,5 / 63 / 30 | Ini stok biomassa (tC/ha), bukan FE (tCO2e/ha/thn) |
| 10 | Stok C hutan | 79,67 vs 98,84 vs 135,2 tC/ha | Tiga nilai berbeda untuk satu kelas yang sama |
| 11 | Gambut!F6:H7 | Kerapatan dijumlah antarkelas, stok dibagi 3 | Bukan rerata. Rerata tertimbang luas = 551,8 tC/ha. |
| 12 | Tuplah vs Tuplah (2) | Satu bagian memakai PL2022 1:250.000 (kebun 10 ha), bagian lain memakai interpretasi 2026 (kebun 359 ha) | Ada dua data aktivitas berbeda dalam satu perhitungan |
| 13 | Tuplah (2)!C67:C68 | Luas REDD memasukkan sungai 31,92 ha. Luas ARR memasukkan 82,87 ha yang baru terdeforestasi dan 359 ha kebun aktif. | Masalah kelayakan dan leakage (lihat bagian 2 dan 3) |
| 14 | K53, L53, M41 | `"40.91"` dan `"1.411.16"` tersimpan sebagai teks | Tidak bisa dipakai dalam rumus |
| 15 | Kurs | Rp 18.000 di satu blok, Rp 16.000 di blok lain | Proyeksi pendapatan tidak konsisten |

**Faktor emisi gambut sudah sesuai** dengan IPCC 2013 Wetlands Supplement Tabel 2.1 untuk tropis: sawit 11 tC = 40 tCO2; grassland 9,6 tC ≈ 35 tCO2; hutan atau semak terdrainase 5,3 tC ≈ 19 tCO2. Namun ada tiga catatan:
- Nilai 19 untuk hutan rawa sekunder hanya berlaku jika hutan itu sudah terdrainase. Ini perlu dibuktikan dengan peta kanal dan data muka air tanah.
- CH4, N2O, DOC, dan kebakaran belum dihitung.
- Di file asal, FE dikalikan ke *seluruh luas tutupan* ("Emisi" 48.593 tCO2e/thn). Itu emisi lanskap saat ini, bukan selisih baseline − proyek.

### Cara hitung yang benar (sudah diterapkan di model koreksi)

```
Emisi baseline (thn t) = A_t × (C_hutan − C_pasca) × 44/12          ← biomassa, saat deforestasi
                       + ΣA_1..t × (FE_pasca − FE_hutan)              ← oksidasi gambut, kumulatif per tahun
Kredit bersih          = Emisi baseline × efektivitas × (1 − leakage) × (1 − buffer) × (1 − ketidakpastian)
```

Penjelasan simbol:
- **A_t:** luas deforestasi per tahun.
- **C_hutan:** stok C hutan = (222,91 + 64,64) × 0,47 = 135,1 tC/ha.
- **C_pasca:** stok C setelah deforestasi, tertimbang menurut matriks perubahan 2016–2026 = 14,8 tC/ha.
- **FE_pasca:** FE gambut setelah deforestasi, tertimbang = 31,6 tCO2/ha/thn. Dikurangi FE hutan terdrainase 19, tambahannya +12,6.

**Stok gambut adalah cadangan, bukan emisi.** Gambut tidak lepas sekaligus saat hutan ditebang. Stok ini hanya relevan untuk kebakaran (kedalaman bakar) dan untuk menunjukkan nilai konservasi.

## 2. Rekomendasi additionality

Area ini adalah **Hutan Desa di Fungsi Lindung Ekosistem Gambut**: 2.015 ha berstatus lindung dan 454 ha budidaya (lihat FEG_KGHLTR di sheet Export_Output). Status ini membuat **uji regulatory surplus menjadi titik paling rawan.** Menurut PP 71/2014 jo. PP 57/2016, pembukaan dan drainase di fungsi lindung sudah dilarang. Akibatnya, "mencegah deforestasi" bisa dinilai sebagai hal yang memang sudah diwajibkan hukum.

Langkah yang direkomendasikan:

1. **Hapus faktor "Additional 43%" dari rumus.** Jika maksudnya asumsi seberapa besar proyek menekan deforestasi, beri nama "efektivitas proyek" dan dukung dengan rencana kegiatan dan anggaran. Additionality diuji terpisah, misalnya dengan alat VCS VT0008, dalam tiga langkah:
   - **Regulatory surplus:** tunjukkan bahwa larangan *tidak ditegakkan secara sistematis*. Bukti dari data sendiri cukup kuat:
     - hutan turun 138 ha (2021–2026);
     - perkebunan naik dari 6 menjadi 359 ha di gambut lindung;
     - muncul 57,6 ha lahan terbuka baru.

     Tambahkan data hotspot/area terbakar (FIRMS/SiPongi), catatan penegakan hukum, dan laju deforestasi di KHG yang sama di luar proyek.
   - **Hambatan investasi:** tunjukkan bahwa LPHD tidak punya pendanaan untuk patroli, sekat kanal, MPA/regu damkar, dan rehabilitasi tanpa pendapatan karbon. Susun arus kas proyek dengan dan tanpa karbon. Daftarkan juga semua dana publik yang sudah masuk (BRGM, dana desa, KLHK/PS). Kegiatan yang sudah didanai pemerintah tidak boleh diklaim ulang.
   - **Praktik umum:** bandingkan dengan Hutan Desa lain di KHG Mempawah–Duri/Peniti yang tidak punya proyek karbon. Jika mereka juga tidak melakukan perlindungan aktif, argumen proyek menguat.
2. **Baseline harus konservatif dan mengikuti metodologi.**
   - Untuk REDD+ Verra, gunakan **VM0048**. Data aktivitas dan peta risiko deforestasi disediakan Verra di tingkat yurisdiksi. Laju 1,16% atau laju proyek sendiri tidak bisa dipakai langsung.
   - Untuk skema domestik (SRN-PPI / SPE-GRK), ikuti Permen LHK 21/2022 dan 7/2023 serta pedoman penghitungan KLHK.
3. **Jelaskan kenaikan hutan +97 ha pada 2016→2021.** Tanpa penjelasan, VVB akan menilai ada ketidakkonsistenan interpretasi atau ancaman yang lemah. Lakukan uji akurasi (≥ 85–90%) untuk setiap peta tahun, termasuk ground check.
4. **Uji kelayakan ARR di setiap poligon, bukan di total luas.**
   - Lahan yang masih hutan dalam 10 tahun sebelum proyek dimulai tidak eligible untuk ARR di VCS. Termasuk di sini 55,22 ha hutan → lahan terbuka dan 7,85 ha hutan → kebun. Lahan ini masuk ke akuntansi REDD+, bukan ARR.
   - Perkebunan aktif 359 ha sebaiknya **tidak** dijadikan ARR (lihat leakage). Kandidat ARR yang kuat adalah semak belukar stabil (±591 ha) dan lahan terbuka lama.
   - Di gambut terdrainase, ARR tanpa pembasahan tetap menghasilkan emisi gambut di skenario proyek. Pertimbangkan **pembasahan ulang (WRC/rewetting)**. Penurunan FE dari ~19 ke mendekati 0 tCO2/ha/thn bisa memberi pengurangan lebih besar daripada serapan pohon, tetapi butuh desain hidrologi di tingkat KHG.
5. **Cegah klaim ganda.**
   - Daftarkan di SRN-PPI.
   - Pastikan area tidak tumpang tindih dengan program yurisdiksi atau proyek lain.
   - Untuk penjualan internasional, siapkan otorisasi dan corresponding adjustment sesuai regulasi NEK yang berlaku. Pastikan regulasi NEK terbaru dan aturan pelaksananya.

## 3. Rekomendasi leakage

Pemicu utama di area ini (data 2016–2026) adalah **ekspansi perkebunan** (+353 ha), **pembukaan lahan** (+57,6 ha), dan **kebakaran gambut**. Ada empat jenis leakage yang perlu dikelola.

1. **Activity-shifting leakage (pemindahan kegiatan pemicu deforestasi):**
   - **Jangan mengusir kebun yang ada.** Tetapkan 359 ha perkebunan sebagai zona paludikultur atau agroforestri: jelutung rawa, sagu, kopi liberika, dan tanaman lain yang toleran muka air tinggi. Jangan mengubahnya menjadi ARR murni. Ini menekan pemindahan kegiatan sampai mendekati nol.
   - Petakan pelaku pembukaan lahan (warga desa, pendatang, perusahaan) dan siapkan alternatif mata pencaharian. Tingkatkan produktivitas lahan budidaya yang sudah ada **di luar kubah gambut** (zona budidaya 454 ha < 50 cm) agar kebutuhan lahan baru turun.
   - Tetapkan **sabuk leakage** di sekitar proyek dalam KHG yang sama, dan pantau deforestasinya dengan citra yang sama dan pada periode yang sama. Hitung potongan leakage dengan modul metodologi terpilih. Selama belum ada data, model memakai 15%.
2. **Market leakage:** relevan jika proyek mengurangi produksi komoditas (misalnya sawit dari 359 ha). Dengan opsi paludikultur di atas, produksi tidak hilang dan market leakage bisa diabaikan secara terdokumentasi.
3. **Leakage hidrologis (khas gambut).** Kanal di luar batas proyek bisa terus mengeringkan gambut di dalam proyek, dan sebaliknya.
   - Tarik batas proyek mengikuti satuan hidrologis (sub-KHG), atau tambahkan zona penyangga.
   - Inventarisasi seluruh kanal yang terhubung.
   - Bangun sekat kanal bersama BRGM, desa, dan pemegang konsesi di sekitarnya.
   - Pantau muka air tanah (TMAT) di dalam dan di luar batas. Target TMAT ≤ 0,4 m sesuai PP 57/2016.
4. **Kebakaran (risiko reversal, bukan leakage).**
   - Masukkan ke penilaian risiko non-permanen. Untuk gambut, buffer kemungkinan di atas 20%.
   - Bentuk dan danai MPA/regu damkar.
   - Siapkan sumur bor dan sekat kanal, serta sistem peringatan dini berbasis hotspot.

## 4. Langkah perbaikan berikutnya (prioritas)

1. Pakai **satu** data tutupan lahan resolusi tinggi (bukan PL2022 1:250.000) untuk 2016, 2021, dan 2026, lengkap dengan uji akurasi dan matriks perubahan bruto **per periode**, termasuk 2021–2026.
2. Tetapkan **satu** tabel parameter gambut per kelas kedalaman (BD, %C) dari sampel lab, dan **satu** stok biomassa hutan dari plot (SNI 7724:2019, CI 90%).
3. Pilih jalur pasar dan metodologi: Verra VM0048 + WRC, atau skema domestik SPE-GRK. Lalu ganti laju dan faktor indikatif di model dengan nilai sesuai metodologi tersebut.
4. Susun analisis additionality (bagian 2) dan rencana pengelolaan leakage (bagian 3) sebagai bab PDD.
5. Hitung buffer dengan VCS AFOLU Non-Permanence Risk Tool. Seragamkan kurs dan gunakan harga pasar terkini untuk proyeksi.

## Isi model koreksi

| Sheet | Isi |
|---|---|
| Parameter | Semua input (biru) dan asumsi kunci (kuning) beserta sumbernya. Laju deforestasi bisa dipilih: 1 = bruto 2016–2026, 2 = neto 2021–2026. |
| Data_Aktivitas | Tutupan 2016/2021/2026, matriks kehilangan hutan, pengecekan neraca luas, laju deforestasi |
| Stok_Gambut | Stok C gambut per kedalaman dengan rerata tertimbang luas |
| Baseline_REDD | Emisi baseline (biomassa + gambut kumulatif) dan kredit bersih per tahun; porsi LPHD dan nilainya (Rp) pada 3 harga; pembanding dengan angka file asal |
| Sensitivitas | Kredit bersih menurut laju deforestasi × stok biomassa |
| Daftar_Temuan | 22 temuan lengkap dengan lokasi sel dan perbaikannya |
