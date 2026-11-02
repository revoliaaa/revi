# Catatan visualisasi poster A0

Makalah: *Perhutanan Sosial dan Perdagangan Karbon sebagai Strategi Pembangunan Perdesaan di Kalimantan Barat* (seminar hasil, 6 November 2026).

Semua grafik digambar pada ukuran cetak akhir untuk satu kolom poster A0 landscape (lebar sekitar 36 cm). Ukuran huruf yang tercetak: judul 26 pt, label sumbu 21 pt, label nilai 19–23 pt, catatan kaki 14,5 pt. Berkas SVG menyimpan teks sebagai teks, sehingga tetap dapat disunting di Illustrator atau Inkscape.

## 1. Audit data (sebelum menggambar)

| Butir | Status |
|---|---|
| Angka Tabel 1 (25 HD; 32.468 + 76.370 + 16.103 = 124.941 ha) | Cocok; dicek ulang di skrip |
| Waterfall (1.720 / 276 / 3.588 / 5.585 ha) | Cocok dengan lembar 2; nilai presisi dipakai |
| Ambang USD6,83 dan USD28,04; cakupan 11,8% dan 49,7% | Cocok dengan lembar 3–4 |
| Kurva cakupan menurut harga | **Tersedia**: 40 simulasi deterministik USD1–40 (lembar 4). Kurva digambar dari data asli, tidak dibuat-buat |
| Manfaat program (+6.315; +16.331) dan kehilangan akses (−227.077; −448.032) | Cocok dengan lembar 1A |
| Shapefile batas HD, batas administrasi, inset | **DATA TIDAK TERSEDIA** |
| Koordinat B2, B3, B4 (USD10), sumbu Y untuk B3 (USD20) dan R2 | **DATA TIDAK TERSEDIA** dalam angka (hanya titik di Gambar 7) |
| `HASIL_SIMULASI_VENSIM.xlsx` | Tidak dipakai: angka rusak saat ekspor karena pengaturan locale (desimal terbaca sebagai pemisah ribuan, sebagian sel menjadi tanggal/jam). Perlu diekspor ulang dari Vensim dengan titik desimal |

### Temuan yang perlu dicek di makalah

**Gambar 6b, baris "Perubahan bersih pendapatan RT (S4−S3)", USD20 tertulis −93 ribu.** Dari lembar 1A, nilainya 41.047.390 − 41.223.679 = **−176.289** Rp/RT/tahun; lembar 2 juga mencatat −176.289. Teks hlm. 9 sejalan dengan −176.289: jika kehilangan akses ditiadakan, hasilnya −176.289 + (448.032 − 153.114) = **+118.629**, sama dengan angka yang tertulis di teks. Nilai USD10 (−40 ribu ≈ −39.561) sudah benar. Kemungkinan label −93 berasal dari versi model sebelumnya. Grafik 05 tidak memakai baris ini.

## 2. Catatan per grafik

### 01 — Lokasi penelitian (`01_peta_lokasi`)
- **Pesan:** penelitian mencakup 25 HD pada tiga lanskap; Padang Tikar menguasai 61% luas areal, dan Batu Ampar sendiri mencakup 33.140 ha.
- **Status:** peta belum dapat dibuat karena shapefile tidak disertakan. Yang dihasilkan adalah pengganti non-spasial (luas per HD menurut Tabel 1), dengan tanda "PETA: DATA TIDAK TERSEDIA" di dalam gambar. Tidak ada koordinat atau poligon yang dikarang.
- **Untuk membuat peta:** kirim shapefile batas 25 HD (dengan kolom nama lanskap), lalu jalankan
  `python scripts/make_figures.py --only 1 --hd-shapefile HD.shp --landscape-col LANSKAP --admin-shapefile kecamatan.shp --kalbar-shapefile kalbar.shp --indonesia-shapefile indonesia.shp`.
  Fungsi ini memproyeksikan peta ke UTM 49S dan menambahkan skala, panah utara, legenda, serta inset. Jalur kodenya sudah diuji dengan poligon uji.
- **Keterbatasan:** luas yang ditampilkan adalah luas SK (124.941 ha), bukan luas proyek karbon (111.123,17 ha).

### 02 — Mekanisme sistem (`02_mekanisme_sistem`)
- **Pesan:** pembiayaan karbon memengaruhi hasil ekologis dan sosial melalui patroli dan intensitas perlindungan.
- 10 elemen. Loop penguat R: penerimaan karbon → dana LPHD → patroli → intensitas → (−) deforestasi → (−) emisi dihindari & kredit → penerimaan. Dua tanda negatif menjadikan loop ini penguat.
- Garis padat = struktur model (parameter dari kalibrasi atau literatur); garis putus oranye = asumsi model yang diuji sensitivitasnya (kehilangan akses); garis titik abu-abu = hanya ada pada eksperimen alokasi (kompensasi R1).
- **Keterbatasan:** ini penyederhanaan; model lengkap memuat 724 variabel. Kapasitas realisasi belanja LPHD hanya disebut di catatan kaki.

### 03 — Waterfall (`03_waterfall_deforestasi`)
- **Pesan:** pada USD20, perdagangan karbon menambah 3.588 ha di atas PS reguler (1.720 ha) dan pembiayaan awal (276 ha); porsinya 64% dari total.
- **Pembulatan:** nilai presisi 1.720,4 + 276,3 + 3.588,2 = 5.584,9 ha. Jumlah label yang sudah dibulatkan adalah 5.584, sedangkan total yang dilaporkan 5.585. Selisih 1 ha ini dijelaskan di catatan kaki; angka sumber tidak diubah.
- **Keterbatasan:** hasil simulasi deterministik, bukan dampak kausal terukur. Monte Carlo menunjukkan arah yang konsisten tetapi besaran yang bervariasi (S2−S1 median 1.561 ha; P5–P95 671–2.740 ha). Kontribusi karbon bergantung pada harga: hanya 535 ha pada USD10.

### 04 — Ambang harga (`04_threshold_pembiayaan`)
- **Pesan:** proyek layak secara finansial mulai USD6,83, tetapi kebutuhan minimum LPHD baru tertutup rata-rata pada USD28,04. Rentang di antaranya (diarsir) adalah zona "proyek layak, LPHD belum cukup".
- Kurva berasal dari 40 run deterministik pada harga bulat; garis hanya menghubungkan titik secara visual. Kedua ambang berasal dari lembar 3.
- **Keterbatasan:** cakupan adalah rerata 2030–2055, bukan jaminan untuk setiap tahun (pada 2024–2027 belum ada belanja dari kredit). Kebutuhan ideal tidak pernah tertutup hingga USD40. Di Monte Carlo, NPV positif pada USD10 hanya muncul pada 60,9% pengulangan.

### 05 — Diverging bar (`05_diverging_pendapatan`)
- **Pesan:** dalam asumsi model, kehilangan akses per RT sekitar 36× (USD10) dan 27× (USD20) lebih besar daripada manfaat program per RT.
- Sumbu simetris (±560 ribu) dengan titik nol di tengah, agar ketimpangan besaran terlihat jujur.
- **Keterbatasan:** kedua batang adalah komponen pada skenario S4, bukan perubahan total pendapatan terhadap baseline (Rp41,25 juta/RT/tahun). Kehilangan akses merupakan asumsi (kelas D), sangat sensitif (PRCC −0,79), dan diuji pada pengali 0–3,24. Tanpa kehilangan akses, selisih S4−S3 justru positif.

### 06 — Quadrant scatter (`06_quadrant_alokasi`)
- **Pesan:** desain alokasi menghasilkan trade-off. Mengurangi porsi patroli (B4) menaikkan pendapatan RT terdampak tetapi mengurangi deforestasi yang dihindari sebanyak 2.801 ha; R1 menaikkan pendapatan tanpa mengurangi perlindungan.
- **Hanya titik bernilai numerik yang digambar.** B0 (0,0); B1 dan R1 pada X = 0; B4 USD20 (−2.801 ha; +Rp572.157). B3 USD20 ditampilkan sebagai rentang (X sama, 0 < Y ≤ B4). R2 ditampilkan sebagai panah ke bawah pada X = +237 dan +2.475 ha karena besaran Y tidak dilaporkan.
- Nilai Rp572.157 disebut dalam teks sebagai nilai tertinggi B3–B4 ("hingga"); nilai ini dikaitkan ke B4 sesuai Gambar 7. B1 berasal dari kotak Gambar 7 (dibulatkan ke Rp100).
- **Data yang dibutuhkan untuk melengkapi grafik:** tabel keluaran eksperimen alokasi (ΔX dan ΔY terhadap B0 untuk B1–B4, R1, R2 pada USD10 dan USD20). Setelah tersedia, isi kolom kosong di `data/alokasi_manfaat_makalah.csv` lalu jalankan ulang skrip.
- **Keterbatasan:** hanya tujuh alternatif yang diuji; R1 bukan solusi optimal untuk semua desa, dan kompensasinya hanya menutup sekitar 6–12% kehilangan akses yang diasumsikan.

## 3. Pemeriksaan kualitas

1. Angka cocok dengan makalah: `make_figures.py` menghentikan proses (`assert`) jika nilai yang dibulatkan berbeda dari makalah.
2. Satuan dan periode tercantum di setiap sumbu atau subjudul, serta di catatan kaki.
3. Keterbacaan: ukuran huruf minimum 14,5 pt pada ukuran cetak.
4. Tumpang tindih label sudah diperiksa secara visual pada PNG 300 dpi.
5. Warna tetap sama artinya di semua grafik (lihat kamus `C` di `scripts/make_figures.py`). Pada cetak abu-abu, kategori tetap terbaca karena setiap batang dan titik diberi label langsung.
6. Tanpa efek 3D, bayangan, gradien, atau ikon dekoratif.

## 4. Susunan poster yang disarankan (belum dibuat)
Sesuai permintaan, poster penuh baru dibuat setelah keenam visual diperiksa. Usulan susunan: tiga kolom, dengan kolom tengah sedikit lebih lebar (kira-kira 36 / 42 / 36 cm):
- **kiri:** 01, masalah dan tujuan, 02, metode/skenario/validasi;
- **tengah:** 03, 04, masing-masing dengan interpretasi;
- **kanan:** 05, 06, kontribusi, simpulan dan implikasi kebijakan.
