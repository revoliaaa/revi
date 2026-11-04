import json
T = json.load(open("fase6/tabel_rekon.json"))
doc = f"""# Audit Akademik Final: Hasil Tesis PWD Dua Skenario

**Tanggal:** 4 November 2026

**Model:** tidak diubah.
- `MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl` (md5 `639083f9…`)
- `MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl`

**Data lampiran:** `TABEL_REKONSILIASI_AUDIT_AKADEMIK_PWD.xlsx` (lembar 1–7).

**Status yang tetap berlaku:**
- PySD 3.14.3; Vensim native BELUM DIVERIFIKASI.
- NPV SEMENTARA.
- K7 endogen GAGAL (tidak dipakai).
- Referensi S1 berpasangan lulus pengujian yang telah dilakukan.
- Kewajiban reversal = aturan model.

## Kesimpulan audit

1. **Tidak ditemukan kesalahan material pada model.**
   - Arus kas C-J1 USD 20 dan USD 35 tersambung penuh dari penjualan kredit sampai bagian LPHD dan mitra (cek A–G = 0).
   - Setiap komponen pendapatan dan biaya cocok dengan hitung ulang independen dari penggerak primernya.
   - Model tidak perlu diubah.
2. **Ditemukan satu kesalahan penyajian material di dokumen analisis.**
   - `ANALISIS_SOSIAL_EKONOMI_PWD.md` §1 menjumlahkan biaya bruto (termasuk biaya yang ditalangi mitra) dengan bagian LPHD dan mitra, sehingga totalnya melebihi kas penjualan.
   - Kalimat itu sudah dikoreksi (§1.3). Ringkasan final juga ditambah informasi arus kas mitra nominal.
3. **Dua asumsi populasi dan pendapatan sangat menentukan kesimpulan kesejahteraan dan harus ditulis eksplisit di makalah.**
   - Jumlah RT terdampak tumbuh mengikuti penduduk (2.144 pada 2024 → rerata 3.003 pada 2030–2055 → 6.244 pada 2087).
   - Pengali kehilangan akses (kelas D). Arah dampak terhadap pendapatan rumah tangga berbalik bila pengali di bawah 0,75 (RT bergantung, USD 20) atau 0,30 (RT terdampak, USD 20).
4. **Kesamaan deforestasi R1 dan B0 adalah konsekuensi konstruksi alokasi**, bukan temuan perilaku. R1 tidak optimal secara umum.

---

## 1. Rekonsiliasi keuangan proyek

### 1.1 C-J1 USD 20 (lembar 1)

{T['20']}

### 1.2 C-J1 USD 35 (lembar 2)

{T['35']}

**Definisi cek** (dihitung dari komponen aliran, bukan dari variabel `Check` model):

| Cek | Rumus |
|---|---|
| A | kas − total biaya = surplus − kekurangan |
| B | surplus = pemulihan defisit + pemulihan talangan + bagian LPHD + bagian mitra |
| C | bagian LPHD ÷ (LPHD + mitra) = 0,6 |
| D | defisit awal + kekurangan − pemulihan = defisit akhir |
| E | talangan awal + jembatan + biaya modal − pemulihan − penghapusan = talangan akhir |
| F | saldo LPHD awal + kas masuk − belanja = saldo akhir |
| G | arus kas mitra (S2 − S1) = bagian 40 % + pemulihan defisit + pemulihan talangan − kekurangan − jembatan |

**Hitung ulang independen (lembar 3)**

{T['ind20']}

{T['ind35']}

Cek identitas dan hitung ulang ini membuktikan **konsistensi akuntansi internal dan kesesuaian dengan parameter**. Keduanya tidak membuktikan bahwa angka biaya itu benar secara empiris, karena tarif MRV, pajak 5 %, kurs Rp16.500, dan biaya Rp260.000/HOK masih asumsi.

### 1.3 Rekonsiliasi dengan laporan sosial-ekonomi

Semua angka dihitung pada basis yang sama: kumulatif nominal 2024–2086, mekanisme C-J1, pengali akses 1, B0.

| Angka di `ANALISIS_SOSIAL_EKONOMI_PWD.md` (USD 20) | Nilai | Rekonsiliasi |
|---|---|---|
| Kas penjualan | 29,07 | = baris 1a |
| "Biaya MRV, transaksi, pajak, pengganti" | 27,55 | = baris 8, **biaya bruto**. Rp16,85 M dibayar mitra (baris 10); hanya Rp10,69 M dibayar dari kas penjualan |
| Dana mitra 40 % | 5,12 | = baris 15. Mitra juga menerima pemulihan Rp1,65 M (defisit) + Rp3,91 M (talangan) |
| Kas LPHD | 7,69 | = baris 14 |
| Upah tunai PS S2 − S1 | 4,65 | = upah dari kas LPHD 2,40 (baris 22a) + upah jembatan dibayar mitra 2,26 (baris 23) |
| Defisit MRV yang tetap ditanggung mitra | 15,20 | = baris 19 akhir |
| **Penggunaan kas penjualan Rp29,07 M** | | **= 10,69 (biaya) + 1,65 (pemulihan defisit) + 3,91 (pemulihan talangan) + 7,69 (LPHD) + 5,12 (mitra)** |

**Koreksi yang diterapkan.** Kalimat lama "dari Rp29,1 miliar kas penjualan, Rp27,6 miliar habis untuk MRV …; LPHD menerima Rp7,7 miliar; mitra memperoleh Rp5,1 miliar ditambah pemulihan talangan" menjumlahkan biaya bruto (termasuk yang ditalangi mitra) dengan bagian LPHD dan mitra, sehingga totalnya > kas. Kalimat itu diganti dengan rincian di atas, plus fakta berikut:

**Arus kas mitra (S2 − S1, nominal):**

| Harga | Arus kas mitra nominal | NPV mitra inkremental [SEMENTARA] |
|---|---|---|
| USD 20 | **−Rp10,08 M** | −Rp0,27 M |
| USD 35 | +Rp142,9 M | – |

Pada USD 20, selisih antara arus kas nominal dan NPV terjadi karena hampir seluruh kekurangan (Rp15,2 M) jatuh pada 2051–2086, ketika MRV terus berjalan tanpa kredit, dan nilainya terdiskonto berat. Dengan aturan henti MRV (uji M2), defisit 2087 turun menjadi Rp0,27 M.

---

## 2. Audit populasi dan pendapatan rumah tangga

### 2.1 2.144 pemegang garapan vs ±3.000 RT terdampak (lembar 4)

| Besaran | 2024 | 2030 | 2042 | 2055 | 2087 | Rerata 2030–2055 |
|---|---|---|---|---|---|---|
| Populasi (73.083 → tumbuh 1,66 %/th) | 73.083 | 80.733 | 98.518 | 122.233 | 206.245 | – |
| RT bergantung hutan | 5.373 | 5.970 | 7.342 | 9.154 | 15.516 | 7.462 |
| RT terdampak (pemegang garapan) | 2.162 | 2.402 | 2.955 | 3.684 | 6.244 | 3.003 |

Nilai 2024 adalah rerata tahun; pada t = 2024,0 nilainya tepat 5.328 dan 2.144.

**Penjelasan:**
- **Tidak ada perubahan definisi.** RT terdampak = RT bergantung × (2.144 ÷ 5.328 = 0,402).
- RT bergantung diproksi dari 5.328 pekerja berbasis SDA (1 RT per pekerja) dan tumbuh mengikuti penduduk. Nilai S1 dan S2 identik.
- Seluruh perbedaan 2.144 → ±3.000 berasal dari **pertumbuhan proyeksi** (faktor ±1,40 pada rerata 2030–2055).

**Asumsi yang harus ditulis eksplisit:**
1. Pemegang garapan (individu SHM/SKT/turun-temurun) diperlakukan setara RT. `Faktor Keunikan Catatan Garapan` = 1 adalah batas atas (kelas D).
2. Jumlah pemegang garapan diasumsikan tumbuh 1,66 %/th seperti penduduk. Ini dapat dipersoalkan, karena luas garapan di dalam HD terbatas.
   - Kehilangan agregat tidak bergantung pada asumsi ini.
   - Kehilangan **per RT terdampak** bergantung padanya: bila jumlah pemegang garapan tetap 2.144, kehilangan per RT terdampak rerata 2030–2055 menjadi ±1,40 kali.
   - Bila faktor keunikan 0,5, kehilangan per RT terdampak menjadi 2 kali.

### 2.2 Audit perhitungan

| Unsur | Persamaan model | Hitung ulang (S2 C-J1 USD 20, 2040) |
|---|---|---|
| Kehilangan akses per RT bergantung | pendapatan hutan per RT × 0,25 × pengurangan relatif deforestasi (= efek PS aktif, terhadap BAU tanpa PS) × pengali akses | 8.035.408 × 0,25 × 0,0858 × 1 = 172.446 (model 172.448) |
| Kehilangan per RT terdampak | kehilangan agregat ÷ RT terdampak = per RT × 2,485 | 428.546 (sama) |
| Upah tunai patroli | HOK berbayar × Rp150.000; komponen dari Rp260.000/HOK | rasio upah/biaya = 150/260 tepat (uji W2) |
| Upah di pendapatan RT | upah kegiatan × **0,5** (`Porsi Upah sebagai Tambahan Bersih`) × **0,255** (`Porsi Manfaat Program untuk RT Bergantung` = pangsa RT bergantung) ÷ RT bergantung | identitas lulus (selisih 0) |
| Penerimaan KUPS di pendapatan RT | **perubahan** penerimaan anggota terhadap tingkat 2024 (`Switch Pendapatan KUPS Inkremental` = 1); bisa negatif (S1 2087: −Rp6,7 juta) | identitas lulus |
| Kompensasi | hanya di model alokasi; dibayar dari saldo LPHD; per RT terdampak = realisasi ÷ RT terdampak | dibayar = diterima (selisih ≤ 2·10⁻⁷ Rp) |

**Catatan konseptual:**
- Kehilangan akses diukur terhadap BAU tanpa PS, sehingga S1 pun memiliki kehilangan (Rp228 ribu/RT terdampak/th). Selisih S2 − S1 tetap konsisten.
- Pendapatan hutan juga naik dengan tutupan hutan (indeks ketersediaan sumber daya). Manfaat ini dibagi rata ke semua RT bergantung, sedangkan kehilangan dipusatkan pada RT terdampak.
- Dua porsi (0,5 dan 0,255) membuat sebagian besar upah tunai **tidak** tercermin di pendapatan bersih RT bergantung. Keduanya asumsi kelas D dan harus dinyatakan.

### 2.3 Sensitivitas pengali kehilangan akses terhadap kesimpulan kesejahteraan (lembar 5)

Δ S2 − S1, rerata 2030–2055, Rp/RT/th, C-J1:

| Pengali akses | USD 20: RT bergantung | USD 20: RT terdampak | USD 35: RT bergantung | USD 35: RT terdampak |
|---|---|---|---|---|
| 0 | +54.352 | +54.352 | +112.117 | +112.117 |
| 0,5 | +18.221 | −35.435 | −10.414 | −192.381 |
| 0,75 | +156 | −80.328 | −71.679 | −344.629 |
| 1 (dasar) | −17.909 | −125.222 | −132.944 | −496.878 |
| 1,5 | −54.040 | −215.009 | −255.475 | −801.376 |
| **Pengali impas** | **0,75** | **0,30** | **0,46** | **0,18** |

Pada USD 10, pengali impasnya 0,99 untuk RT bergantung dan 0,40 untuk RT terdampak.

**Monte Carlo** (proporsi ensembel dengan Δ pendapatan RT terdampak > 0, menurut kelas pengali):

| Kelas pengali akses | USD 10 | USD 20 | USD 35 |
|---|---|---|---|
| 0–0,25 | 98,5 % | 95,5 % | 83,6 % |
| 0,25–0,5 | 50,0 % | 18,2 % | 3,0 % |
| 0,5–0,75 | 3,0 % | 0 % | 0 % |
| > 0,75 | 0 % | 0 % | 0 % |

**Kesimpulan kesejahteraan yang dapat dipertanggungjawabkan:**
- "Pendapatan RT terdampak turun" hanya berlaku bila kehilangan akses nyata ≥ ±30 % dari asumsi dasar (USD 20).
- "Pendapatan RT bergantung turun" hanya berlaku bila ≥ ±75 %.

Karena pengali ini belum memiliki data, kesimpulan tentang **arah** dampak kesejahteraan belum dapat diklaim final. Yang dapat diklaim: arah dampak sangat peka terhadap besarnya kehilangan akses, dan rumah tangga terdampak menanggung beban yang jauh lebih besar daripada rata-rata RT bergantung.

---

## 3. Audit eksperimen benefit sharing

### 3.1 Porsi efektif (lembar 6; rerata tahun dengan dana tersedia > 0)

| Alternatif | Patroli | Rehabilitasi | Kebakaran | KUPS | Operasional + kelembagaan | Kompensasi |
|---|---|---|---|---|---|---|
| B0 | 30,0 % | 15,0 % | 10,0 % | 20,0 % | 25,0 % | 0 % |
| B1 | 30,0 % | 15,0 % | 7,5 % | 15,0 % | 25,0 % | 7,5 % |
| B2 | 22,5 % | 11,2 % | 7,5 % | 18,7 % | 25,0 % | 15,0 % |
| B3 | 15,0 % | 7,5 % | 7,5 % | 33,8 % | 25,0 % | 11,2 % |
| B4 | 15,0 % | 7,5 % | 7,5 % | 18,7 % | 25,0 % | 26,2 % |
| R1 | **30,0 %** | **15,0 %** | **10,0 %** | **5,0 %** | 25,0 % | **15,0 %** |
| R2 | 37,5 % | 11,2 % | 7,5 % | 3,8 % | 25,0 % | 15,0 % |

Angka adalah porsi belanja pada USD 20. Dana fleksibel = 75 % dana tersedia, karena operasional dan kelembagaan mengambil 25 % lebih dulu.

**Pernyataan eksplisit:**
- **Kesamaan deforestasi R1 dan B0 adalah konsekuensi konstruksi alokasi.** Porsi fleksibel R1 untuk patroli, rehabilitasi, dan kebakaran (0,4; 0,2; 2/15), dikalikan 0,75, sama tepat dengan porsi B0 (0,30; 0,15; 0,10). Kompensasi R1 (15 %) diambil seluruhnya dari porsi KUPS (20 % → 5 %).
- **B1 juga identik dengan B0 untuk patroli dan rehabilitasi.** Kompensasinya diambil dari kebakaran dan KUPS.
- Uji R1 "tidak memperburuk perlindungan" lulus karena konstruksi itu, bukan karena mekanisme perilaku.

### 3.2 Trade-off R1 terhadap KUPS (lembar 7)

| Indikator | USD 20: B0 | USD 20: R1 | USD 35: B0 | USD 35: R1 |
|---|---|---|---|---|
| KUPS aktif rerata 2030–2055 | 22,3 | 22,1 | 24,8 | 23,3 |
| KUPS aktif 2060 | 13,4 | 13,1 | 28,5 | 16,8 |
| KUPS aktif 2087 | 6,1 | 5,9 | 50,4 | **13,6** (−73 %) |
| Proporsi KUPS produktif | 0,44 | 0,43 | 0,58 | 0,46 |
| Omzet KUPS (Rp juta/th) | 94,3 | 89,3 | 135,9 | 101,4 |
| Penerimaan anggota (Rp juta/th) | 17,1 | 16,2 | 24,7 | 18,4 (−25 %) |
| Penerimaan anggota kumulatif (Rp M) | 0,81 | 0,78 | 2,28 | 1,06 |
| Modal usaha KUPS 2087 (Rp juta) | 0,39 | 0,38 | 141,3 | **1,2** |
| Kompensasi kumulatif ke RT terdampak (Rp M) | 0 | 1,15 | 0 | 31,36 |

**Bacaan:**
- **Pada USD 20,** trade-off kecil karena dana LPHD kecil.
- **Pada USD 35,** R1 memindahkan Rp31,4 M ke RT terdampak dan mengurangi penerimaan anggota KUPS hanya Rp1,2 M kumulatif. Secara tunai, rumah tangga sebagai kelompok memperoleh lebih banyak dengan R1.
- **Namun keberlanjutan usaha melemah tajam:** KUPS aktif 2087 turun 73 %, dan modal usaha hampir habis (Rp141 juta → Rp1,2 juta). R1 menukar basis usaha jangka panjang dengan transfer tunai.
- Penerima kompensasi (±3.000 RT terdampak) dan anggota KUPS (±330–380 orang) tidak sama, sehingga R1 juga mengubah **siapa** yang menerima manfaat.

### 3.3 Kesimpulan alokasi

- **R1 tidak optimal secara umum.** R1 memenuhi uji yang ditetapkan (pendapatan RT terdampak naik tanpa memperburuk perlindungan dibanding B0) pada USD 20–35, karena konstruksi porsinya, dan dengan biaya pada keberlanjutan KUPS.
- Tidak ada alternatif yang dominan:
  - R2 memperkuat perlindungan, tetapi memperbesar kehilangan akses;
  - B4 memperbesar kompensasi, tetapi melemahkan perlindungan dan siklus pembiayaan;
  - B3 memperbesar porsi KUPS, tetapi tidak memperbaiki KUPS jangka panjang karena total kas mengecil.

---

## 4. Tabel hasil akademik final

**Kode status:**

| Kode | Arti |
|---|---|
| **V** | Terverifikasi secara numerik melalui PySD |
| **P** | Bergantung pada parameter asumsi |
| **E** | Membutuhkan validasi empiris |
| **N** | Membutuhkan verifikasi Vensim native |
| **F** | Belum dapat diklaim sebagai hasil final |

### RQ1: Perlindungan hutan dan emisi

| No | Temuan | Angka kunci | Status |
|---|---|---|---|
| 1.1 | S2-C menambah perlindungan di atas S1 pada semua harga dan semua sampel | Deforestasi dihindari > 0 pada 100 % ensembel (USD 10/20/35) | V, P (jembatan, efektivitas), N |
| 1.2 | Besaran tambahan perlindungan | C-J1: 287 / 287 / 338 / 454 / 4.954 ha (USD 6–35); C-JP: 620–7.487 ha; MC USD 20 median 682 ha [P5 137; P95 9.233] | V, P, E, N, F (besaran) |
| 1.3 | Tambahan perlindungan tidak permanen pada USD ≤ 20 | Manfaat bersih turun > 10 % dari puncak pada 99,5 / 76,2 / 21,8 % ensembel (USD 10/20/35) | V, P (laju per ha hutan yang diselamatkan), E, N |
| 1.4 | Emisi dihindari dan kredit model | C-J1 USD 20: 155 ribu tCO₂e emisi deforestasi dihindari; 101 ribu tCO₂e kredit REDD diajukan | V, P, N; kredit: F (≠ kredit terverifikasi) |
| 1.5 | Penentu utama | Efektivitas perlindungan, besaran/durasi jembatan, biaya per HOK, laju deforestasi BAU (\|PRCC\| 0,7–0,8) | V, P |

### RQ2: Pembiayaan dan keberlanjutan LPHD

| No | Temuan | Angka kunci | Status |
|---|---|---|---|
| 2.1 | Arus kas tersambung penuh (penjualan → biaya → pemulihan → bagi hasil → saldo) | Cek A–G = 0; hitung ulang independen cocok | V (konsistensi internal); P (tarif dan kurs) |
| 2.2 | Kas LPHD tertunda karena pemulihan defisit MRV dan talangan lebih dulu | Kas LPHD pertama 2032–2036; tidak ada pada C-J1 USD 6–10 | V, P (urutan pemulihan), E (kontrak), N |
| 2.3 | Pembiayaan LPHD jangka panjang hanya pada harga tinggi | Kas LPHD 2075–2086 > 0 pada 0,5 / 22,2 / 74,0 % ensembel | V, P, N |
| 2.4 | Posisi mitra | USD 20: arus kas nominal −Rp10,08 M; NPV −Rp0,27 M [SEMENTARA]; defisit MRV Rp15,2 M (MRV berjalan tanpa kredit). USD 35: +Rp142,9 M | V, P (aturan MRV), E (kontrak), F (NPV) |
| 2.5 | NPV proyek/mitra positif | Proyek 13,0 / 65,8 / 95,8 %; mitra 4,2 / 46,8 / 88,8 % ensembel | F (biaya pengembangan dan material = 0) |
| 2.6 | Kapasitas LPHD naik hanya bila kas berkelanjutan | 0,50 → 0,87 (USD 35); tetap 0,50 (USD ≤ 20) | V, P, E |

### RQ3: Pekerjaan, KUPS, dan pendapatan rumah tangga

| No | Temuan | Angka kunci | Status |
|---|---|---|---|
| 3.1 | Tambahan kerja seluruhnya berupah; tidak bertahan sesudah 2060 pada USD ≤ 20 | +2,7 FTE (C-J1 USD 20) s.d. +41,7 FTE (C-JP USD 35); bertahan 2060–2086 pada 1,2 / 31,8 / 82,5 % ensembel | V, P, N; FTE ≠ orang |
| 3.2 | Upah patroli Rp150.000/HOK sebagai komponen biaya Rp260.000 | 2024–2025: Rp831,6 juta | V; upah: data terkonfirmasi; biaya total: P, E |
| 3.3 | KUPS S1 menurun; S2 hanya mengubahnya bila kas besar | S1 33,4 → 5,7 (2087); S2 USD 35: 50,4 | V, P (reaktivasi, reinvestasi), E (data KUPS 2024–2025) |
| 3.4 | Arah pendapatan RT bergantung | −17.909 Rp/RT/th (USD 20, pengali 1); impas pada pengali 0,75 | V, P, E, **F** |
| 3.5 | Arah pendapatan RT terdampak | −125.222 Rp/RT/th (USD 20); impas pada pengali 0,30 | V, P, E, **F** |
| 3.6 | Jumlah RT terdampak | 2.144 (2024) → 3.003 (rerata 2030–2055), karena pertumbuhan proyeksi | V (aritmetika); P, E (pertumbuhan pemegang garapan, faktor keunikan) |
| 3.7 | Upah tunai hanya sebagian tercermin di pendapatan bersih RT | Porsi tambahan bersih 0,5 × porsi RT bergantung 0,255 | P, E |

### RQ4: Distribusi manfaat, kompensasi, dan trade-off

| No | Temuan | Angka kunci | Status |
|---|---|---|---|
| 4.1 | Penggunaan kas penjualan (USD 20) | Rp29,07 M = 10,69 biaya + 1,65 pemulihan defisit + 3,91 pemulihan talangan + 7,69 LPHD + 5,12 mitra; mitra menalangi Rp16,85 M biaya | V, P |
| 4.2 | Tambahan uang tunai RT < tambahan kehilangan akses (pengali 1) | USD 20: upah 4,65 + KUPS 0,05 vs kehilangan 16,32 Rp M | V, P, E, F (arah bergantung pengali) |
| 4.3 | Tanpa kompensasi (B0), beban terkonsentrasi pada RT terdampak | Kehilangan per RT terdampak 2,49 × rata-rata RT bergantung | V, P, E |
| 4.4 | R1 = B0 dalam perlindungan karena konstruksi; kompensasi dari porsi KUPS | USD 35: kompensasi Rp31,4 M; KUPS 2087 −73 %; modal KUPS Rp141 → 1,2 juta | V, P; R1 optimal: **F** |
| 4.5 | Kompensasi dari dana LPHD menutup sebagian kecil kehilangan | Maks. 18,9 % kehilangan total (B4, USD 35) | V, P |
| 4.6 | Tidak ada alternatif alokasi yang dominan | R2: perlindungan ↑, kehilangan akses ↑; B4: kompensasi ↑, perlindungan ↓ | V, P, F (alokasi per desa) |

---

## 5. Daftar perubahan yang perlu diterapkan pada makalah

Diterapkan **sesudah** audit ini diterima. Angka makalah empat skenario tidak dipakai.

1. **Judul dan tujuan:** dipertahankan.
2. **Metode, definisi skenario:** empat skenario → dua skenario kebijakan (S1, S2). Mekanisme C sebagai konfigurasi S2; A dan B hanya sebagai eksperimen pembanding dan diagnostik.
3. **Metode, kredit:** kredit konservatif endogen terhadap Referensi S1 berpasangan; buffer, debit, dan penyelesaian *reversal* sebagai aturan model; kredit model ≠ kredit terverifikasi.
4. **Metode, pembiayaan jembatan:** J1 Rp782,86 juta/th 2026–2030 sebagai eksperimen, bukan komitmen mitra; JP sebagai sensitivitas. Urutan pemulihan: defisit MRV → talangan → bagi hasil 60/40.
5. **Metode, upah dan biaya:** upah patroli Rp150.000/HOK (data); biaya total Rp260.000/HOK (asumsi kerja; rentang MC Rp150.000–300.000); nilai tenaga sukarela non-tunai dipisahkan.
6. **Metode, populasi:** nyatakan bahwa 5.328 pekerja SDA dan 2.144 pemegang garapan adalah nilai 2024 yang diproyeksikan tumbuh 1,66 %/th (rerata 2030–2055: 7.462 dan 3.003). Nyatakan juga faktor keunikan 1 (batas atas) dan individu = RT.
7. **Metode, pendapatan RT:** jelaskan porsi upah 0,5, porsi manfaat RT bergantung 0,255, penerimaan KUPS inkremental terhadap 2024, kehilangan akses terhadap BAU, dan kompensasi hanya pada eksperimen alokasi.
8. **Metode, ketidakpastian:** MC LHS berpasangan N = 400 (seed 20261104), 20 parameter. "Proporsi ensembel" menggantikan "peluang"; tidak boleh disebut probabilitas empiris.
9. **Metode, verifikasi:** PySD; Vensim native belum; K7 endogen gagal sehingga dipakai protokol berpasangan; NPV SEMENTARA.
10. **Hasil RQ1:** ganti dengan tabel §4 RQ1. Tambahkan paragraf non-permanensi pada USD ≤ 20.
11. **Hasil RQ2:** gunakan tabel arus kas §1 (versi ringkas). Sajikan arus kas mitra nominal di samping NPV, serta keterlambatan kas LPHD.
12. **Hasil RQ3:** sajikan pemisahan upah tunai, kontribusi sukarela, dan biaya total. Sajikan dekomposisi pendapatan RT dan **tabel sensitivitas pengali akses dengan pengali impas**. Arah dampak pendapatan ditulis sebagai bersyarat.
13. **Hasil RQ4:** sajikan tabel porsi efektif dan pernyataan bahwa kesamaan R1 = B0 adalah konstruksi. Kuantifikasi trade-off KUPS. **Hapus klaim lama bahwa R1 adalah alokasi terbaik.**
14. **Abstrak, simpulan, saran:** tulis ulang berdasarkan `RINGKASAN_HASIL_FINAL_TESIS_PWD.md` (sesudah koreksi) dan tabel §4, dengan status V/P/E/N/F.
15. **Gambar:** ganti dengan F1–F5 (Tahap 3), M1–M3 (MC), dan A1 (alokasi). Diagram model ditambah rantai Referensi S1 dan struktur jembatan, kredit, serta *reversal*.
16. **Hapus dari makalah:**
    - angka empat skenario;
    - klaim kredit terhadap baseline BAU sebagai hasil utama;
    - klaim kesejahteraan tanpa syarat;
    - klaim kemiskinan atau ketimpangan;
    - kata "peluang" untuk frekuensi ensembel.

## 6. Koreksi pada dokumen analisis yang sudah ada

| Dokumen | Koreksi |
|---|---|
| `ANALISIS_SOSIAL_EKONOMI_PWD.md` §1 | Kalimat penggunaan kas USD 20/35 diganti dengan rincian yang terekonsiliasi (§1.3) |
| `RINGKASAN_HASIL_FINAL_TESIS_PWD.md` §2 dan §4 | Ditambah arus kas mitra nominal (USD 20: −Rp10,08 M) dan catatan bahwa kesamaan R1 = B0 adalah konstruksi alokasi; ditambah pengali impas kesejahteraan |

Model tidak diubah.
"""
open("fase6/AUDIT_AKADEMIK_FINAL_PWD.md", "w").write(doc); print("ok")
