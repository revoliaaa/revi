# 08 — Rekonsiliasi Numerik dengan Naskah (OUTPUT 5)

Tabel lengkap 35 butir ada di `manuscript_reconciliation.csv`. Setiap baris memuat:
1. lokasi;
2. pernyataan naskah;
3. keluaran model pendukung;
4. sifat ketidaksesuaian;
5. signifikansi;
6. koreksi;
7. apakah koreksi mengubah simpulan utama.

## Rekap klasifikasi

| Klasifikasi | Jumlah | Butir |
|---|---|---|
| Benar dan didukung | 12 | T01, T04, T09, T10, T12, T13, T14, T19, T20, T21, T26, T34 |
| Benar tetapi bersyarat | 7 | T02, T05, T08, T15, T16, T24, T25 |
| Benar tetapi perlu klarifikasi | 2 | T07, T31 |
| Perlu klarifikasi | 9 | T03, T06, T11, T18, T22, T23, T28, T32, T35 |
| Tidak konsisten secara numerik/definisi | 2 | **T17** (cakupan LPHD), **T27** (5.328) |
| Tidak didukung bukti yang tersedia | 3 | T29 (MAPE), T30 (Monte Carlo/PRCC), T33 (daftar 13 parameter) |

**Tidak ada angka di Tabel 4 yang salah hitung.** Semua nilai Tabel 4 tereproduksi.

## Butir yang mengubah atau melemahkan simpulan utama

**T17 — "kebutuhan minimum LPHD tertutup pada USD 28,04"**
- **Lokasi:** Abstrak, hlm. 7, Gambar 5a, Simpulan.
- **Masalah:** metrik = belanja total / kebutuhan minimum, padahal belanja total termasuk pos di luar kebutuhan minimum.
- **Koreksi yang disarankan:** "Belanja LPHD total baru setara dengan kebutuhan minimum pada sekitar USD 28. Namun, belanja untuk komponen minimum (operasional, patroli, kebakaran) hanya 25 % dari kebutuhan pada USD 20 dan 58 % pada USD 35."
- Ganti juga baris Tabel 4 dan label Gambar 5.

**T08 / T15 — besaran efek karbon dan kelayakan**
- **Lokasi:** Abstrak, Hasil, Simpulan.
- **Koreksi yang disarankan:** tambahkan, "Besaran ini dihitung pada basis kredit A1, yaitu terhadap baseline tanpa PS, sehingga kredit model turut mencakup efek PS dan pembiayaan awal (68 % dan 11 % pada USD 10). Bila kredit dibatasi pada pengurangan aditional terhadap S2, tambahan perlindungan menjadi 31 ha (USD 10) dan 192 ha (USD 20) pada basis A2 register, dan NPV USD 10 negatif."
- **Catatan:** sensitivitas A2 dihitung pada audit ini; diskusikan dengan pembimbing apakah dimasukkan ke naskah.

**T27 — "5.328 pekerja berbasis sumber daya alam"**
- **Lokasi:** Metode, hlm. 2.
- **Koreksi yang disarankan:** "5.328 orang bergantung hutan (estimasi; 2.144 pemegang garapan ditambah sebagian pekerja SDA) diperlakukan sebagai 5.328 rumah tangga."
- Angkanya tetap, tetapi interpretasinya berubah.

## Butir klarifikasi yang perlu sebelum seminar

| Butir | Teks/label sekarang | Usulan |
|---|---|---|
| T22 | Tabel 4 "Pekerja setara penuh (orang)"; sumbu Gambar 6a "(orang)" | "Setara pekerja penuh (FTE; HOK/300)" |
| T11 | "Kredit model" | "Kredit REDD diajukan (model, basis A1)"; tambah baris kredit terjual 395 / 870 / 1.396 ribu |
| T03 | Neraca dengan angka 284 tanpa nama | 284 = perubahan bersih 2024 (deforestasi 522 − regenerasi 238) |
| T06 | 1.725 ha di Gambar 4a vs 1.720 di teks | Beri label "selisih stok hutan 2087" |
| T07 | "Tidak berlanjut setelah 2025" | "Dana berhenti 2025; efek meluruh sampai pertengahan 2030-an, lalu sebagian terkoreksi" |
| T15 | NPV tanpa definisi | Tulis rumus, batas (tanpa biaya pengembangan; saldo LPHD tak dikurangkan), sebut "NPV parsial" |
| T23 | "Upah kegiatan Rp 327 juta dan Rp 905 juta" | Pisahkan upah didanai karbon (146 / 724 juta) dari nilai kerja swadaya |
| T24 | "Status KUPS 2026" (Gambar 2) vs data 2023 | Seragamkan; sumber data KUPS [PERLU DIISI] |
| T28 | "413.000 nilai, 99,87–100 %" | Ganti dengan hasil uji yang berkasnya tersedia, atau lampirkan berkas uji asli |
| T29, T30, T33 | MAPE, Monte Carlo, PRCC | Tandai sebagai hasil peneliti dengan berkas pendukung [PERLU DIISI]; sebut MAPE aliran 73,3 % sebagai keterbatasan |
| T30 | PRCC −0,79 | Pastikan label: "biaya MRV" (konteks peneliti) atau "asumsi akses" (naskah hlm. 9) |
| T31 | Uji putus loop −9 ha | Dokumentasikan variabel yang diputus (audit: −13 ha) |
| T35 | "Revolia Az-Zahra Akhmad Fauzi¹" | "Revolia Az-Zahra, Akhmad Fauzi¹, Andrea Emma Pravitasari²" |

## Konvensi yang perlu ditulis di Metode

- Kumulatif adalah integral aliran pada langkah DT, bukan penjumlahan ekspor tahunan. Contoh S1: penjumlahan ekspor tahunan 2025–2086 = 29.844 ha, sedangkan integral = 29.812 ha.
- Rerata tahunan 2030–2055 adalah rerata integral.
- Jumlah KUPS memakai rerata sampel tahunan.
