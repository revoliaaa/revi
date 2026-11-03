# Laporan Kredit Konservatif Endogen dan Additionality

**Model:** `MODEL_FINAL_DUA_SKENARIO_PWD.mdl` (937 variabel, 16 View).
- Sumber: `DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl`, tidak ditimpa.
- Perangkat: PySD 3.14.3. *Units Check* Vensim native belum dilakukan.
- Status: verifikasi Tahap 2 (lihat `LAPORAN_VERIFIKASI_MODEL_FINAL.md`).
- Kredit model ≠ kredit terverifikasi dan bukan klaim memenuhi persyaratan Verra atau standar lain.

## 1. Masalah yang diperbaiki

Pada Fase 3, kredit mekanisme C dihitung dengan **pendekatan porsi**: (efek PS aktif − efek PS tanpa karbon) ÷ efek PS aktif, dikalikan pengurangan emisi terhadap baseline BAU.
- Pendekatan itu memakai stok hutan S2 sendiri.
- Hasilnya 0,96–1,34 kali mitigasi tambahan berpasangan terhadap S1.
- Koreksi ex post tidak diizinkan, karena kredit berlebih ikut mengalirkan kas fiktif ke LPHD dan mitra.

Tahap 1 Fase 4 menemukan dua masalah tambahan:
1. ***Reversal*.** Sesudah jembatan berakhir, hutan yang diselamatkan S2 kembali terdeforestasi dengan laju per ha yang sama seperti S1. Mulai ±2052, deforestasi S2 melebihi S1 (C20: −34,5 ribu tCO₂e pada tahun-tahun negatif). Rumus `MAX(0, …)` per tahun mengabaikan kehilangan ini.
2. **Dana yang dapat dipertukarkan.** Di Fase 3, jembatan mengurangi kebutuhan dana LPHD. Bila ada kas non-karbon, dana itu tidak terbelanjakan di S2 padahal di S1 dipakai untuk patroli. Kredit lalu menghitung patroli yang di S1 tetap terjadi.

## 2. Rancangan endogen

### 2.1 Rantai Referensi S1 di dalam setiap run

Rantai baru berisi **78 variabel `… Referensi S1`**, salinan rantai Baseline: tutupan lahan, rehabilitasi, regenerasi karbon, gambut, dan emisi. Perbedaannya hanya pada empat penggerak:

| Penggerak | Baseline BAU | Referensi S1 |
|---|---|---|
| Tekanan deforestasi | 1 (tanpa PS) | `Pengali Izin PS × (1 − Efek Pengelolaan PS Tanpa Karbon) × (1 − efek penghidupan) × (1 − efek kebakaran) × indeks harga` |
| Penanaman | 0 | `Penambahan Luas Penanaman × (1 − Porsi ARR Adisional)` (penanaman yang tidak dibiayai kas karbon) |
| Keberhasilan rehabilitasi, ekspansi kebun, gangguan gambut, luas karhutla | parameter dasar | sama dengan aktual |
| Kondisi awal | sama dengan aktual | sama dengan aktual |

`Efek Pengelolaan PS Tanpa Karbon` hanya memuat:
- patroli reguler S1;
- patroli dari pembiayaan historis 2024–2025;
- patroli yang dibiayai kas non-karbon.

Patroli dari kas karbon LPHD dan dari jembatan tidak termasuk. Rantai ini hanya memakai nilai tahun berjalan dan stok, **tanpa informasi masa depan**, dan **tanpa loop aljabar** (uji V0b).

Pada parameter dasar, kanal penghidupan dan kebakaran bernilai 0, sehingga patroli adalah satu-satunya kanal tekanan deforestasi. Bila kanal itu diaktifkan dalam sensitivitas, perubahannya tidak dikreditkan karena memakai nilai aktual S2.

### 2.2 Atribusi dana yang dapat dipertukarkan (perbaikan K7)

- `Kebutuhan Dana Perlindungan` dikembalikan ke kebutuhan bruto. LPHD tetap menargetkan kebutuhan penuh dengan dana yang ada.
- `Hari Patroli Didanai Jembatan` = MIN(plafon ÷ biaya, kebutuhan tambahan − patroli dari kas LPHD). Jembatan hanya mengisi kekurangan, sehingga tidak ada pembiayaan ganda.
- `Hari Patroli Didanai Kas Non Karbon` = MAX(porsi saldo non-karbon × patroli LPHD, patroli yang dapat dibiayai saldo non-karbon sendiri). Dana non-karbon dianggap dibelanjakan lebih dulu (konservatif).

### 2.3 Kredit dengan saldo mitigasi bertanda dan penyelesaian *reversal*

```
REDD bertanda        = MIN(Emisi Deforestasi Ref S1 − Emisi Deforestasi, Pengurangan Biomassa Bersih Ref S1)
ARR                  = Pengurangan Biomassa Bersih Ref S1 − REDD bertanda           (≥ 0; REDD + ARR = bersih)
Mitigasi eligible    = REDD bertanda × (1 − leakage 0,10) × (1 − buffer 0,12) × Project Area 0,682
Saldo mitigasi       = INTEG(Mitigasi eligible − Kredit REDD, 0)                    (negatif = debit reversal)
Kredit REDD diajukan = MAX(0, Saldo/DT + Mitigasi eligible)                          (mode 2)
Reversal > buffer    = MAX(0, −Saldo − Kumulatif buffer)
Kredit pengganti     = dibeli pada harga berjalan × kurs → Biaya Transaksi dan MRV (sebelum bagi hasil)
```

**Sifat rancangan:**
- Kredit hanya diajukan bila mitigasi bersih kumulatif terhadap S1 positif.
- Kehilangan sesudah kredit terbit pertama-tama mengurangi kredit berikutnya, lalu ditutup buffer, lalu dengan membeli kredit pengganti. Pembelian itu adalah **arus kas nyata** yang mengurangi surplus atau ditalangi mitra.
- Penerbitan, penjualan, kas, bagi hasil, dan belanja LPHD semuanya memakai kredit endogen ini.
- Deforestasi dihindari, emisi dihindari, serapan ARR, dan kredit model dilaporkan sebagai variabel terpisah.
- Kredit gambut tetap 0 (`Switch Klaim Kredit Gambut` = 0).

**Mode kredit** (`Switch Baseline Kredit Konservatif`):

| Mode | Isi | Dipakai sebagai |
|---|---|---|
| 0 | Terhadap baseline BAU | Mekanisme A, pembanding eksploratif |
| 1 | Pendekatan porsi Fase 3 | Hanya untuk uji reproduksi |
| **2** | **Terhadap Referensi S1, endogen** | **Default; mekanisme B dan C** |

Variabel pelaporan `Potensi Kredit REDD terhadap BAU` dan `Potensi Kredit REDD Referensi S1` tersedia di setiap run.

## 3. Bukti uji (ringkas)

Rincian ada di `LAPORAN_VERIFIKASI_MODEL_FINAL.md`.

| Uji | Hasil |
|---|---|
| K1: Referensi S1 = S1 aktual pada run S1 | Selisih 0 (hutan dan emisi, semua t) |
| K2: B tanpa jembatan | Kredit 0 di USD 20 dan 35. Tanpa modal awal tambahan siklus tidak dimulai (diagnostik dipertahankan) |
| K3: identitas dan batas kredit | Σ kredit = Σ mitigasi bersih − saldo akhir. Emisi Referensi S1 dalam run C = emisi run S1 terpisah (selisih ≤ 6·10⁻¹¹). Sesudah penyelesaian *reversal*, kredit bersih ≤ mitigasi bersih (sisa ≤ 0,1 % karena jeda satu DT di akhir horizon) |
| K4: tanpa hitung ganda | REDD + ARR = pengurangan biomassa bersih di semua t |
| K5: konservasi kredit | Stok akhir = Σ terbit − Σ terjual − Σ kedaluwarsa |
| K6: konservatif ≤ BAU | Lulus di semua harga |
| K7: kas non-karbon Rp 3 M/th | **GAGAL minor.** Galat acuan kumulatif +163 tCO₂e (0,05 % kredit); kredit bersih 300.059 ≤ mitigasi berpasangan 314.668 tCO₂e. Tidak memengaruhi konfigurasi dasar (kas non-karbon 0) |

## 4. Dampak terhadap hasil (deterministik, k = 0,5; jembatan J1 2026–2030, biaya modal 0; pembanding C Fase 3 dan A)

Satuan: ribu tCO₂e untuk kredit dan mitigasi; Rp miliar untuk kas dan NPV (nominal, kecuali NPV). NPV berstatus SEMENTARA. Mitigasi eligible S2−S1 = emisi deforestasi dihindari berpasangan × 0,5401.

| Harga | Mekanisme | Kredit REDD diajukan | Mitigasi eligible S2−S1 | *Reversal* (buffer / pengganti) | Biaya pengganti | Deforestasi dihindari S2−S1 (ha) | Kas LPHD | Kas LPHD pertama | NPV mitra inkremental | Defisit MRV 2087 |
|---|---|---|---|---|---|---|---|---|---|---|
| USD 6 | C Fase 4 | 68,8 | 52,9 | 24,7 (9,4 / 15,3) | 1,52 | 287 | 0 | – | −4,17 | 18,9 |
| USD 6 | C Fase 3 | 71,0 | 52,9 | tidak dihitung | – | 287 | 0 | – | −4,13 | 17,2 |
| USD 6 | A | 197,5 | 0 | – | – | 0 | 0 | – | −1,06 | 8,0 |
| USD 10 | C Fase 4 | 68,8 | 52,9 | 24,7 (9,4 / 15,3) | 2,53 | 287 | 0 | – | −2,83 | 19,3 |
| USD 10 | A | 211,9 | 14,4 | – | – | 78 | 3,56 | 2032 | +0,16 | 1,6 |
| USD 15 | C Fase 4 | 78,0 | 62,3 | 24,6 (10,6 / 14,0) | 3,46 | 338 | 2,36 | 2035 | −1,55 | 18,4 |
| USD 15 | A | 274,1 | 75,8 | – | – | 415 | 18,5 | 2030 | +1,44 | 0 |
| USD 20 | C Fase 4 | 100,7 | 83,8 | 26,2 (13,7 / 12,4) | 4,11 | 454 | 7,69 | 2034 | −0,28 | 16,5 |
| USD 20 | C Fase 3 | 104,2 | 83,8 | tidak dihitung | – | 454 | 7,67 | 2034 | −0,23 | 11,4 |
| USD 20 | A | 395,5 | 195,0 | – | – | 1.072 | 48,2 | 2030 | +3,08 | 0 |
| USD 35 | C Fase 4 | 897,3 (+ARR 11,5) | 898,2 | 0 | 0 | 4.954 | 214,3 | 2033 | +6,66 | 0 |
| USD 35 | C Fase 3 | 698,5 | 726,7 | tidak dihitung | – | 4.002 | 167,4 | 2033 | +6,10 | 0 |
| USD 35 | A | 1.310,1 (+ARR 33,3) | 1.100,0 | – | – | 6.045 | 335,7 | 2029 | +12,16 | 0 |

**Bacaan:**
1. **USD ≤ 20.** Kredit C sedikit turun dibanding Fase 3, tetapi *reversal* sekarang menimbulkan **kewajiban nyata**: Rp1,5–4,1 miliar biaya penggantian kredit. Akibatnya defisit MRV yang ditalangi mitra pada 2087 naik menjadi Rp16,5–19,3 miliar.

   Perlindungan yang hanya dibiayai lima tahun tidak permanen. Bila tidak diteruskan, mitigasinya sebagian hilang. Ini konsekuensi langsung dari asumsi laju deforestasi per ha yang sama pada hutan yang diselamatkan.
2. **USD 35.** Kredit C justru naik (698,5 → 897,3 ribu tCO₂e) dan deforestasi dihindari naik (4.002 → 4.954 ha). Ada dua penyebab:
   - pendekatan porsi Fase 3 memberi kredit di bawah mitigasi sebenarnya pada harga tinggi (rasio 0,96);
   - jembatan kini mengisi kekurangan sesudah patroli LPHD, tanpa mengurangi kebutuhan LPHD.

   Pada harga ini siklus mandiri, sehingga *reversal* tidak terjadi.
3. **A tetap tidak lolos uji additionality model.** Pada USD 6, A menerbitkan 197,5 ribu tCO₂e tanpa mitigasi tambahan sama sekali terhadap S1.

## 5. Patroli historis 2023–2025 dan additionality

- Pembiayaan mitra 2023–2025 diakui di **kedua** skenario. Patroli itu masuk efek "tanpa karbon", sehingga **tidak dikreditkan** dalam mode 2.
- Bila peneliti dapat membuktikan pembiayaan itu adalah aktivitas proyek karbon (tanggal mulai, *prior consideration*, kontrak), dampaknya diuji sebagai sensitivitas. Nilai Fase 3: +64,5 ribu tCO₂e eligible terhadap acuan "S1 tanpa pembiayaan mitra 2024–2025".
- Sampai bukti tersedia, status ini [PERLU DIISI], dan baseline BAU internal tidak disamakan dengan baseline resmi standar karbon mana pun.

## 6. Keterbatasan

1. Referensi S1 adalah **kontrafaktual model**, bukan baseline tervalidasi. Kualitasnya bergantung pada asumsi kelas D, terutama k = 0,5 dan efektivitas 0,37.
2. *Reversal* muncul karena hutan yang diselamatkan menghadapi laju per ha yang sama dengan S1. Tidak ada data yang menguji apakah hutan yang sudah dilindungi lebih atau kurang rentan.
3. Kredit pengganti dibeli pada harga berjalan yang sama. Pasar kredit pengganti tidak dimodelkan.
4. Penerbitan kredit masih kontinu (bukan per verifikasi lima tahunan).
5. Atribusi dana yang dapat dipertukarkan masih menyisakan galat kecil bila kas non-karbon > 0 (K7).
6. Kanal penghidupan dan kebakaran tidak dikreditkan. Pada parameter dasar keduanya 0.
