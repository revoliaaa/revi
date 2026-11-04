# Tabel Koreksi Label dan Kalimat Makalah: Model 4 Skenario (S1–S4)

**Ruang lingkup:** koreksi label, satuan, dan definisi. **Angka hasil makalah tidak diubah.** Semua angka di kolom "sesudah" telah direproduksi dari `.mdl` di ZIP ([REPRODUKSI]), kecuali yang diberi label [DIAGNOSTIK BARU].

**Konvensi periode:**
- Fisik: 2025–2086.
- Keuangan: 2024–2086.
- Rerata tahunan: 2030–2055.

**Berkas model:** `DKP_25HD_A1_*_rapi.mdl` (ZIP `MODEL_VENSIM.zip`).

## A. Populasi, pekerja, dan rumah tangga

| # | Lokasi makalah | Teks sekarang | Variabel / persamaan sumber | Periode | Nilai | Kalimat pengganti (siap pakai) | Status |
|---|---|---|---|---|---|---|---|
| A1 | Metode hlm. 2 | "5.328 pekerja berbasis sumber daya alam digunakan sebagai proksi 5.328 rumah tangga bergantung hutan" | `Masyarakat Bergantung pada Hutan Awal = 5328` (People). Dokumentasi: proksi dari 2.144 pemegang garapan + 25,9 % sisa pekerja SDA, diskalakan 20→25 HD; kelas bukti D; rentang uji 2.144–19.038 | 2024 | 5.328 | "Jumlah orang bergantung hutan pada 2024 diestimasi 5.328 orang (estimasi peneliti dari 2.144 pemegang garapan dan sebagian pekerja sektor sumber daya alam; kelas bukti D). Dalam model, setiap orang bergantung hutan diperlakukan sebagai satu rumah tangga (`Rumah Tangga per Pekerja Bergantung = 1`)." | INCONSISTENT (label) → dikoreksi |
| A2 | Metode hlm. 2 (tambahan) | tidak disebut | `Pekerja Berbasis SDA = Pekerja Pertanian + Perkebunan + Perikanan + Peternakan` (rasio profesi × `Populasi`) | 2024 | 24.694 (data SAMPAN 24.099 orang pada 2022–2024 disesuaikan ke populasi 2024) | "Pekerja sektor sumber daya alam (pertanian, perkebunan, perikanan, peternakan) berjumlah sekitar 24.694 orang pada 2024. Sebagian dari mereka, diestimasi 5.328 orang, bergantung pada kawasan Hutan Desa." | [REPRODUKSI] |
| A3 | Metode hlm. 2 | "2.144 pemegang garapan" | `RT Pemegang Garapan dalam HD = 2144` (Household; dokumentasi: individu pemegang SHM/SKT/turun-temurun, diperlakukan setara RT; kelas B) | 2024 | 2.144 | "Sebanyak 2.144 individu pemegang hak garapan (SHM, SKT, atau turun-temurun) di dalam kawasan diperlakukan setara rumah tangga yang berpotensi terdampak pembatasan akses." | perlu klarifikasi |
| A4 | Tabel 4; hlm. 8 | "Pendapatan rata-rata RT" | `Pendapatan Bersih per RT Bergantung`; dasar `Pendapatan Dasar RT Bergantung = 4,176e7` (Setiawan et al. 2021; per responden anggota LPHD; harga 2021) | rerata 2030–2055 | 41,25 / 41,20 / 41,22 / 41,18 / 41,05 / 40,93 juta | "Pendapatan bersih rata-rata rumah tangga bergantung hutan (harga 2021, tidak disesuaikan inflasi; dasar per responden anggota LPHD) …" | CONDITIONAL |
| A5 | Tabel 4; hlm. 8 | "Rumah tangga" (tanpa jumlah) | `Rumah Tangga Bergantung Hutan`; `RT Terdampak Akses` | rerata 2030–2055 | 7.462 RT bergantung; 3.003 RT terdampak (tumbuh 1,66 %/th dari 5.328 dan 2.144) | "Rerata 2030–2055 mencakup sekitar 7.462 rumah tangga bergantung hutan, termasuk sekitar 3.003 rumah tangga pemegang garapan (keduanya tumbuh mengikuti asumsi 1,66 %/th)." | [REPRODUKSI] |

## B. Kerja, upah, dan kerja swadaya

| # | Lokasi | Teks sekarang | Variabel / persamaan | Periode | Nilai | Kalimat pengganti | Status |
|---|---|---|---|---|---|---|---|
| B1 | Tabel 4; sumbu Gambar 6a | "Pekerja setara penuh (orang)" | `Kesempatan Kerja Setara Penuh = Kesempatan Kerja PS / HOK Tersedia per Anggota Kerja per Tahun (300)` | rerata 2030–2055 | 0 / 13,6 / 13,6 / 17,3 / 32,8 / 64,5 | Label baris: "Setara pekerja penuh (FTE = HOK/300; bukan jumlah orang)". Teks: "Kegiatan PS setara 13,6 pekerja penuh (FTE) pada S2. Angka ini mengukur volume kerja, bukan jumlah orang yang bekerja." | dikoreksi |
| B2 | hlm. 8 | "kegiatan PS menyerap sekitar 4.066 hari orang kerja (HOK) per tahun" | `Kesempatan Kerja PS = Total HOK PS + HOK Patroli Berbayar + HOK Pengendalian Kebakaran`; `HOK Patroli = Hari Patroli Swadaya` | rerata 2030–2055 | S2: 4.066 HOK = 2.355 patroli swadaya + 1.711 penanaman | "Pada S2, kegiatan PS menyerap ±4.066 HOK/th, terdiri atas 2.355 HOK patroli swadaya (tidak dibayar) dan 1.711 HOK penanaman. Tidak ada HOK yang dibayar dari dana karbon pada S1–S3." | [REPRODUKSI]; perlu klarifikasi |
| B3 | hlm. 8 | "upah kegiatan masing-masing Rp 327 juta dan Rp 905 juta" | `Upah Kegiatan PS = Upah Patroli Berbayar + Manfaat Ekonomi Penanaman + Manfaat Ekonomi Patroli + Upah Pengendalian Kebakaran` (memuat **nilai ekonomi kerja swadaya**); `Upah Kegiatan Didanai Karbon = Upah Patroli Berbayar + Upah Pengendalian Kebakaran + Upah Penanaman Didanai Karbon` | rerata 2030–2055 | Upah Kegiatan PS: S2 181,4; USD10 326,9; USD20 905,2 juta. Didanai karbon: USD10 145,5; USD20 723,8 juta | "Upah yang dibayar dari dana karbon rata-rata Rp 146 juta/th (USD 10) dan Rp 724 juta/th (USD 20). Bila nilai ekonomi kerja swadaya ikut dihitung, nilai kegiatan PS menjadi Rp 327 juta dan Rp 905 juta/th (S2 tanpa karbon: Rp 181 juta/th)." | dikoreksi |
| B4 | hlm. 7 | "3.107 HOK patroli tambahan per tahun" | `Hari Patroli Didanai = (Pendanaan Awal untuk Patroli + Realisasi Belanja Perlindungan)/Biaya per Hari Patroli + Hari Patroli Pembiayaan Awal` | rerata 2030–2055 | 740 / 3.107 / 5.407 HOK/th (USD 10/20/35) | "… membiayai rata-rata 3.107 HOK patroli berbayar per tahun pada 2030–2055 (USD 20), di atas 2.355 HOK patroli swadaya." | [REPRODUKSI] |

## C. Kredit karbon

| # | Lokasi | Teks sekarang | Variabel | Periode | Nilai (ribu tCO₂e) | Kalimat pengganti | Status |
|---|---|---|---|---|---|---|---|
| C1 | Tabel 4 | "Kredit model (ribu tCO₂e)" 460 / 1.017 / 1.615 | `Kredit REDD Diajukan` | 2024–2086 | 460,3 / 1.017,2 / 1.614,8 | Label baris: "Kredit REDD diajukan, model basis A1 (ribu tCO₂e; bukan VCU)" | dikoreksi |
| C2 | Tabel 4 (baris baru) | – | `Kredit REDD Terbit` (jeda 3 th) | 2024–2086 | 452,6 / 995,4 / 1.548,9 | "Kredit REDD terbit (model)" | [REPRODUKSI] |
| C3 | Tabel 4 (baris baru) | – | `Kredit Karbon Terjual` (REDD + ARR; penjualan 70 %/th, kedaluwarsa 10 %/th) | 2024–2086 | 394,6 / 870,2 / 1.396,2 | "Kredit terjual (REDD+ARR; dasar penerimaan)" | [REPRODUKSI] |
| C4 | hlm. 7 | "Kredit model … lebih kecil daripada emisi yang dihindari terhadap S1 karena kebocoran, buffer, dan pembatasan areal proyek" | `Pengurangan Emisi Eligible REDD`; `Total Emisi Bersih` | 2025–2086 | – | "Kredit REDD diajukan (460 ribu tCO₂e pada USD 10) lebih kecil daripada emisi bersih yang dihindari (862 ribu tCO₂e) karena tiga hal: (i) kredit hanya menghitung emisi deforestasi biomassa, tidak termasuk gambut dan kebakaran; (ii) dikurangi kebocoran 10 % dan buffer 12 %; (iii) dibatasi porsi areal proyek 0,682 (provisional). Dari kredit diajukan, 453 ribu terbit dalam periode simulasi dan 393 ribu kredit REDD terjual." | dikoreksi |
| C5 | Abstrak; Hasil; Simpulan | Efek karbon 535 / 3.588 ha tanpa syarat | `Switch Baseline Kredit Konservatif = 0`; deret Baseline = S1 | 2025–2086 | A1: 535 / 3.588 ha. A2 register: 31 / 192 ha | "Tambahan perlindungan dari perdagangan karbon (535 ha pada USD 10; 3.588 ha pada USD 20) dihitung pada basis kredit A1, yaitu terhadap baseline tanpa PS aktif. Dengan basis ini, kredit model mencakup efek patroli swadaya (68 %) dan pembiayaan awal (11 %) pada USD 10. Pada basis pembanding yang hanya mengkreditkan pengurangan di atas PS reguler (A2), tambahan perlindungan menjadi 31 ha dan 192 ha. Kepatuhan kedua basis terhadap metodologi standar karbon belum diuji." | CONDITIONAL |
| C6 | Seluruh naskah | "kredit karbon" | – | – | – | Gunakan konsisten "kredit model" atau "kredit REDD diajukan/terbit/terjual (model)". Jangan gunakan "VCU" atau "kredit terverifikasi". | dikoreksi |

## D. Keuangan dan LPHD

| # | Lokasi | Teks sekarang | Variabel | Periode | Nilai | Kalimat pengganti | Status |
|---|---|---|---|---|---|---|---|
| D1 | Abstrak | "average minimum management funding was covered only at about USD 28" | `Penggunaan Dana Pengelolaan` / `Kebutuhan Dana Minimum` | rerata 2030–2055 | 100,0 % pada USD 28,04; komponen minimum 46,1 % [DIAGNOSTIK BARU] | "Total LPHD spending matched the modelled minimum management requirement only at about USD 28/tCO₂e. Even then, spending on the minimum components (operations, patrol, fire control) covered about 46 % of that requirement." | INCONSISTENT → dikoreksi |
| D2 | Tabel 4 (baris baru), hlm. 7, Gambar 5 | "Cakupan kebutuhan minimum 3,6 / 11,8 / 26,8 / 49,7 / 133,5 %" | rasio di atas; `Realisasi Belanja Operasional LPHD + Perlindungan + Pengendalian Kebakaran` | rerata 2030–2055 | Rasio belanja total: 3,6 / 11,8 / 26,8 / 49,7 / 133,5 %. Komponen minimum: 1,8 / 5,9 / 13,4 / 24,8 / 57,8 % | Label: "Belanja LPHD total terhadap kebutuhan minimum (%)" dan baris baru "Belanja komponen minimum terhadap kebutuhan minimum (%)". Teks: "Pada USD 10 dan USD 20, belanja LPHD total setara 11,8 % dan 49,7 % kebutuhan minimum, sedangkan belanja untuk komponen minimum itu sendiri baru 5,9 % dan 24,8 %." | dikoreksi |
| D3 | Tabel 4 | "Kesenjangan kebutuhan minimum LPHD (Rp miliar/th)" 5,42 / 4,78 / 2,73 / 0,23 | `Kesenjangan Pembiayaan Minimum = MAX(0, Kebutuhan Minimum − Penggunaan Dana Pengelolaan − Realisasi Pembiayaan Awal)` | rerata 2030–2055 | Versi model: 5,42 / 4,78 / 2,73 / 0,23. Komponen minimum: 5,42 / 5,10 / 4,07 / 2,29 [DIAGNOSTIK BARU] | Catatan tabel: "Kesenjangan dihitung setelah dikurangi seluruh belanja LPHD, termasuk pos non-minimum. Kesenjangan untuk komponen minimum saja adalah 5,10 / 4,07 / 2,29 miliar/th (USD 10/20/35)." | CONDITIONAL |
| D4 | hlm. 7 | "Cakupan rata-rata 100 % baru tercapai sekitar USD 28,04" | idem | rerata 2030–2055 | – | "Belanja LPHD total baru menyamai kebutuhan minimum model pada sekitar USD 28. Pada harga tersebut, kesenjangan rata-rata masih Rp 0,62 miliar/th dan belanja komponen minimum baru 46 % kebutuhan. Dalam simulasi hingga USD 300, belanja komponen minimum tidak mencapai 100 % karena alokasi pengendalian kebakaran tetap 10 %." | dikoreksi |
| D5 | Tabel 4; hlm. 7 | "NPV proyek 10 %" | dihitung di luar model: PV kontinu [penerimaan kotor − biaya MRV/transaksi/pajak − pembiayaan awal − belanja LPHD] | 2024–2086 | −1,62 / −0,50 / 2,07 / 6,09 / 11,50 / 30,79 | "NPV proyek parsial (diskonto 10 %, tanpa biaya pengembangan proyek; penerimaan kredit dikurangi biaya MRV, transaksi, pajak, pembiayaan awal, dan belanja LPHD)." | CONDITIONAL |
| D6 | Tabel 4 | "Dana kolektif LPHD" | `Dana Desa Diterima` (60 % pendapatan bersih terdistribusi) | 2024–2086 | 5,2 / 22,4 / 62,0 / 147,1 / 431,6 miliar | Tambahkan catatan: "Dana kolektif lembaga; bukan pendapatan rumah tangga." | [REPRODUKSI] |
| D7 | Tabel 4; hlm. 8 | "Penerimaan anggota KUPS" dan "omzet" | `Pendapatan KUPS Total` (surplus dibagikan); `Penjualan KUPS` (omzet) | rerata 2030–2055 | Penerimaan 4,8 / 24,5 / 27,0 / 34,6 / 89,9 juta; omzet 135,0 (S2) – 190,2 (USD 20) juta | "Omzet KUPS (Rp 135–190 juta/th) berbeda dari penerimaan anggota (Rp 24,5–34,6 juta/th untuk seluruh anggota)." | [REPRODUKSI] |

## E. Ekologi dan emisi

| # | Lokasi | Teks sekarang | Variabel | Periode | Nilai | Kalimat pengganti | Status |
|---|---|---|---|---|---|---|---|
| E1 | Gambar 4a | "S2 − S1 pada 2087: +1.725 ha" | `Total Hutan` | 2087 | 1.725,2 ha | "Selisih stok hutan 2087 (S2 − S1): +1.725 ha. Berbeda dari deforestasi dihindari kumulatif 1.720 ha karena regenerasi alami dan rehabilitasi." | dikoreksi |
| E2 | Hasil hlm. 6 | "… regenerasi sekitar 17.678 ha lahan nonhutan" (neraca dengan 284) | `Total Hutan`; aliran | 2024–2087 | 94.308 − 284 − 29.812 + 17.678 = 81.890 | "Luas hutan S1 turun dari 94.308 ha (2024) menjadi 81.890 ha (2087): perubahan bersih 2024 −284 ha (deforestasi 522 ha, regenerasi 238 ha), deforestasi 2025–2086 29.812 ha, dan regenerasi alami 17.678 ha." | dikoreksi |
| E3 | Tabel 4 | "Emisi dihindari vs S1" | `Total Emisi Bersih` (biomassa + gambut + kebakaran − serapan) | 2025–2086 | 598 / 675 / 862 / 1.941 / 3.245 ribu tCO₂e | Catatan tabel: "Emisi bersih seluruh kompartemen; kredit hanya menghitung biomassa REDD." | [REPRODUKSI] |
| E4 | Hasil hlm. 7 | "Pembiayaan awal ini tidak berlanjut setelah 2025" | `Deforestasi Total` S2, S3 | tahunan | +345 ha (2025–2036); −69 ha (2037–2086) | "Pembiayaan awal berhenti pada 2025. Efeknya terhadap deforestasi meluruh hingga pertengahan 2030-an (±345 ha), lalu sebagian terkoreksi karena stok hutan yang lebih besar tetap terpapar laju deforestasi. Hasil netonya 276 ha." | dikoreksi |

## F. Ketidakpastian dan validasi

| # | Lokasi | Teks sekarang | Kalimat pengganti | Status |
|---|---|---|---|---|
| F1 | hlm. 5, 6, 8 | Persentase Monte Carlo (92,6 %, 60,9 %, …) | "… muncul pada 92,6 % pengulangan Monte Carlo, yaitu frekuensi pada sebaran parameter yang diasumsikan, bukan peluang kejadian di lapangan. Berkas konfigurasi dan keluaran Monte Carlo: [PERLU DIISI]." | UNVERIFIED (bukan gagal) |
| F2 | hlm. 5 | "Dari sekitar 413.000 nilai tahunan, 99,87–100 % sesuai" | "Keluaran PySD 3.14.3 dibandingkan dengan ekspor Vensim pada 7 run A1. Variabel indikator utama berbeda paling besar 7×10⁻⁶ (relatif). Uji ±413.000 nilai yang dilaporkan sebelumnya memerlukan berkas pendukung [PERLU DIISI]." | UNVERIFIED (bukan gagal) |
| F3 | hlm. 6 | "MAPE stok hutan 3,92 % …" | "… (berkas data historis dan skrip perhitungan: [PERLU DIISI]). Validasi aliran kehilangan tutupan pohon Hansen menghasilkan MAPE 73,3 %, lebih buruk daripada pembanding sederhana; laju tahunan model belum tervalidasi." | UNVERIFIED (bukan gagal) |
| F4 | hlm. 9 | "(PRCC −0,79)" untuk asumsi akses | Pastikan parameter yang dimaksud. Catatan peneliti mengaitkan −0,79 dengan biaya MRV; naskah mengaitkannya dengan asumsi akses. Tulis nama parameter dan keluaran yang diuji. | UNVERIFIED |
| F5 | Gambar 2 | "status KUPS 2026"; "kalibrasi 2001–2014" | "status KUPS 2023 [sumber: PERLU DIISI]"; periode kalibrasi diseragamkan dengan register (laju terkalibrasi 2000–2014 / 2003–2014) | perlu klarifikasi |
| F6 | Halaman judul | "Revolia Az-Zahra Akhmad Fauzi¹"; "² )" tanpa superskrip | "Revolia Az-Zahra, Akhmad Fauzi¹, Andrea Emma Pravitasari²" | dikoreksi |
