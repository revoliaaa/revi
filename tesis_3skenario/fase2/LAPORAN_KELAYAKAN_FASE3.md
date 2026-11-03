# Laporan Kelayakan Masuk Fase 3

**Model:** `DKP_25HD_FINAL_2SKENARIO.mdl` (md5 `aa1428dffdc27541d531926b9806c50e`), 817 variabel, 16 View.

**Sumber:** `DKP_25HD_FINAL_3SKENARIO.mdl` (tidak ditimpa).

**Perangkat uji:** PySD 3.14.3. **Vensim native belum digunakan.**

## 1. Rekapitulasi uji

| Kelompok | LULUS | GAGAL | BELUM DAPAT DIUJI |
|---|---|---|---|
| Struktural (U0a–U18) | 21 | 0 | 1 (U0c Units Check Vensim) |
| Kondisi ekstrem (E1–E7) | 7 | 0 | 0 |
| Perilaku kausal (P1–P7) | 8 | 0 | 0 |

Selama pengujian ditemukan 6 kegagalan (F1–F6). Hanya **F1** yang kesalahan model, dan sudah diperbaiki. F3 adalah keterbatasan desain, diatasi dengan variabel pelaporan. F2, F4, F5, dan F6 adalah kesalahan kriteria atau parameter uji. Semua uji yang terdampak diulang, dan baterai lengkap dijalankan ulang pada berkas final. Rincian ada di `AUDIT_KEGAGALAN_DAN_PERBAIKAN.md`, dan bukti numerik per uji di `HASIL_UJI_STRUKTURAL_FASE2.xlsx`.

## 2. Bukti pokok untuk sepuluh perhatian khusus

1. **Rekonsiliasi patroli historis dan biaya (U3, U17).**
   - Total patroli 2024 = 2.533,000 dan 2025 = 3.011,000 HOK di S1 dan S2.
   - Biaya kumulatif tepat Rp 1.441.440.000; upah 2024 tepat Rp 329.290.000.
   - Kebutuhan dan upah karbon 2024–2025 = 0.
   - Tetap benar ketika kas non-karbon Rp 5 miliar/th disuntikkan sejak 2024.
   - Anggota awal 2026 = 254 = 183 + 61 + 10.
2. **Kesamaan historis S1 = S2 (U4, U13).** Identik sampai kas karbon pertama (USD 10: t = 2031,875). Ke-32 variabel yang berbeda sebelum itu seluruhnya keuangan/kredit. Nilai 2024 identik dengan model 3 skenario.
3. **Konservasi luas dan karbon (U16).** \|Check Total Kawasan\| dan \|Check Konservasi Karbon\| ≤ 6,1·10⁻⁸.
4. **Saldo LPHD (U7, U8, E4).**
   - Saldo ≥ 0; 0 ≤ saldo karbon ≤ saldo; neraca kumulatif ≤ 3·10⁻⁴ Rp.
   - Belanja ≤ dana tersedia; Σ proporsi = 1.
   - Tanpa kas non-karbon, S1 tidak membelanjakan apa pun.
   - Dengan Rp 1 triliun/th, kas menumpuk dan tidak dibelanjakan di atas kebutuhan.
5. **Identitas dan modal KUPS (U10).** Stok modal akhir = Σ aliran (Rp 369.467 di S1; Rp 1,50 miliar di S2-35). Modal tidak terpakai sebelum 2026, dan identitas surplus serta penjualan ≤ 6·10⁻⁸.
6. **Rehabilitasi (U11, P7).**
   - Luas tanam ≤ batas; stok luas tanam karbon = Σ luas aktual.
   - Belanja efektif ≤ realisasi.
   - Tanpa dukungan material, penanaman S1 = 0. Dengan Rp 100,5 juta, 20,13 ha/th.
   - Upah hanya muncul bila ada pembayar.
7. **Hibah (U15).** Pokok = 0 dan pemulihan = 0. Talangan: pemulihan = pokok (+ biaya modal), dan identitas arus kas ≤ 2,4·10⁻⁷ Rp/th untuk keempat kombinasi.
8. **Tidak ada belanja karbon sebelum kas (U7, U14).** Belanja pertama S2-10 pada t = 2031,9375, sesudah kas karbon pertama (2031,875). Kredit pertama diajukan 2025, terbit 2025 + jeda, dan kas mengikuti.
9. **Langkah waktu dan kondisi ekstrem (U6, E1–E7).** Selisih DT 0,0625 vs 0,03125 ≤ 0,087 %. Harga 0 → S2 = S1. k = 0, k = 1, kas besar, USD 500, dan efektivitas 0 semua berperilaku sesuai.
10. **Satuan (U18).** 813/813 persamaan konsisten. Uji negatif pemeriksa 4/4 tertangkap. *Units Check* Vensim belum dijalankan (U0c).

## 3. Uji perilaku kausal (D4)

Angka di bawah adalah **keluaran uji**, bukan hasil penelitian. Semua berlaku pada asumsi kerja k = 0,5, hibah, kas non-karbon 0, dan biaya pengembangan 0.

| Uji | Hubungan yang diuji | Bukti |
|---|---|---|
| P1 | Kas karbon → patroli → intensitas → deforestasi → hutan dan kerja | Patroli tambahan pertama 2029 dan deforestasi S2 < S1 pertama juga 2029 (urutan benar). Δ hutan 2087: USD 20 +1.018 ha, USD 35 +6.268 ha. Δ FTE berupah 2030–2055: +6,8 dan +27,6 |
| P2 | Putus loop dana → patroli (USD 35) | Δ hutan turun dari 6.268 menjadi 167 ha (sisa dari rehabilitasi kas karbon) |
| P3 | k naik → deforestasi S1 turun (monoton) | 29.702 / 29.173 / 28.640 / 28.102 / 27.561 ha untuk k = 0 … 1 |
| P4 | Kas non-karbon S1 → patroli, KUPS, kapasitas, hutan | Rp 3 miliar/th: 3.500 HOK didanai (2030), Δ hutan +2.472 ha, KUPS 2087 23,6 (vs 5,7), kapasitas 0,68 |
| P5 | Biaya reaktivasi KUPS → kelangsungan KUPS → penerimaan anggota | Rp 12,5 juta: KUPS bertahan 33,4; penerimaan anggota 2050 Rp 24,5 juta (vs 12,3) |
| P6 | Harga naik → hutan 2087 tidak turun | 82.799 / 82.866 / 83.181 / 83.818 / 89.067 ha (USD 6–35) |
| P7 | Dukungan material → tanam → hutan dan serapan | Δ hutan +335 ha; serapan 2050 3.273 tCO₂e/th |

## 4. Keputusan

### **SIAP BERSYARAT untuk Fase 3**

**Alasan:**
- Implementasi identik dengan rancangan (168/168 persamaan).
- Tidak ada loop aljabar maupun ketidakkonsistenan satuan.
- Semua uji struktural, ekstrem, dan perilaku yang dapat dijalankan dengan PySD lulus.
- Struktur baru mereproduksi model lama dengan persis bila diberi parameter setara.
- Hubungan kausal pembiayaan → aktivitas → tutupan hutan → manfaat ekonomi bekerja dengan arah dan urutan yang benar.

**Syarat (harus dipenuhi atau dinyatakan sebelum hasil Fase 3 ditafsirkan):**
1. **U0c:** peneliti menjalankan *Units Check* dan run native Vensim (S1, S2 × 5 harga), lalu membandingkannya dengan PySD memakai `bandingkan_vensim_pysd.py`. Sampai itu dilakukan, hasil hanya dapat disebut "terverifikasi PySD".
2. **Parameter tanpa data dijalankan sebagai rentang**, bukan nilai tunggal:
   - k (0–1);
   - biaya reaktivasi dan porsi reinvestasi KUPS;
   - kas non-karbon;
   - dukungan material rehabilitasi;
   - status hibah/talangan dan mekanisme pemulihan sebelum/sesudah bagi hasil;
   - biaya pengembangan proyek; diskonto;
   - norma kebutuhan patroli.
3. **Varian switch konservatif tidak dipakai.** Kredit konservatif dilaporkan dari variabel pelaporan F3.
4. **Kombinasi talangan sesudah bagi hasil dengan biaya modal > 0 tidak dipakai** sebelum ada batas penghapusan (T-a).
5. **NPV dan harga impas tetap berstatus SEMENTARA** sampai biaya pengembangan proyek dan biaya material tersedia.
6. **Keputusan harga ARR** (tetap USD 20 atau mengikuti REDD).
7. **Konfirmasi data:** satuan Rp 260.000 (orang-hari atau regu-hari), upah patroli 2024–2025, roster 254, dan data KUPS 2024–2025.

## 5. Uji yang gagal atau belum dapat diuji, dan dampaknya terhadap validitas

| Uji | Status | Dampak |
|---|---|---|
| U0c Units Check / run native Vensim | BELUM DAPAT DIUJI | Konsistensi satuan sudah diperiksa secara statis (813/813), tetapi tidak menggantikan Vensim. Kesetaraan numerik Vensim–PySD untuk model ini belum terbukti. Pada model lama kesetaraannya 99,87–100 %, tetapi itu tidak otomatis berlaku untuk model baru |
| Validasi perilaku empiris pasca-2025 | tidak dalam lingkup (data tidak ada) | Patroli reguler, KUPS, dan rehabilitasi S1 bergantung pada asumsi kelas D. **Perbedaan S2−S1 adalah konsekuensi asumsi model, bukan dampak kausal empiris** |
| Tidak ada uji yang GAGAL pada berkas final | – | Kegagalan F1–F6 selama proses sudah diperbaiki atau dikoreksi kriterianya |

**Batasan yang tetap berlaku pada Fase 3:** Monte Carlo, PRCC, eksperimen benefit sharing lengkap, dan revisi makalah belum dijalankan. Semuanya menunggu persetujuan atas laporan ini.
