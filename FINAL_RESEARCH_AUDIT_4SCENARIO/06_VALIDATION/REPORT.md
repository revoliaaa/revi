# 06 — Register Validasi (OUTPUT 4)

Data:
- `validation_register.csv` (lengkap);
- `dt_sensitivity.csv`;
- `pysd_vs_vensim.csv` (semua variabel);
- `key_vensim_pysd.csv` (variabel kunci);
- `loop_break_test.csv`.

| Uji | Tujuan | Metode | Bukti | Hasil | Status | Keterbatasan |
|---|---|---|---|---|---|---|
| Integritas persamaan antar-skenario | Skenario hanya beda pada tuas | diff semantik 724 persamaan | `00/model_equation_diff.txt` | Hanya Skenario Kebijakan dan Harga Karbon; 9 konstanta dibulatkan di S1/S2/S3/USD35 | CONSISTENT | Efek ≤ 0,07 ha |
| Konservasi kawasan | Total kawasan tetap | Check Total Kawasan | PySD | residu ≤ 1×10⁻¹⁰ ha | VERIFIED | – |
| Neraca stok-aliran hutan | Stok = awal + masuk − keluar | integral aliran pada DT | `01/ecological_summary.csv` | residu 0,000 ha (9 skenario) | VERIFIED | Agregat hutan saja |
| Konservasi karbon biomassa | Stok + emisi kumulatif tetap | Check Konservasi Karbon | PySD, Vensim | ≤ 8×10⁻⁸ tCO₂e (PySD); ≤ 0,0008 (Vensim) | VERIFIED | Gambut tidak diuji terpisah |
| Identitas keuangan | 60/40, pemulihan | arus kas tahunan | `04/annual_cashflow.csv` | Dana LPHD = 0,6 × bersih terdistribusi; pembiayaan awal pulih ≥ USD 6 | VERIFIED | Tanpa biaya pengembangan |
| Kondisi ekstrem: harga rendah | Perilaku saat rugi | USD 3 | `04/financial_summary.csv` | Defisit 9,72 miliar tidak pulih; S4−S3 = 1 ha | VERIFIED | – |
| Kondisi ekstrem: efektivitas 0,075 | Patroli hampir tak efektif | rerun | `07/robustness_oat.csv` | S2−S1 = 299 ha; S4−S3 USD 10 = 0 ha | VERIFIED | – |
| Sensitivitas DT | Stabilitas numerik | DT 0,125 / 0,0625 / 0,03125 | `dt_sensitivity.csv` | Pada DT/2: hutan ≤ 0,002 %, deforestasi ≤ 0,01 %, penerimaan ≤ 0,05 % | VERIFIED | – |
| Replikasi Vensim–PySD | Konsistensi komputasi | 7 ekspor `.txt` A1, rtol 5×10⁻⁶ | `pysd_vs_vensim.csv`, `key_vensim_pysd.csv` | 99,05–99,86 % nilai identik 6 angka penting; variabel kunci beda maks 7×10⁻⁶ | VERIFIED (7 dari 8 run) | USD 20 tanpa ekspor; klaim naskah "413.000 nilai, 99,87–100 %" tidak tereproduksi persis |
| Putus loop R | Efek karbon lewat dana→patroli | `Realisasi Belanja Perlindungan` = 0 | `loop_break_test.csv` | S4−S3 USD 10: 535 → −13 ha | CONSISTENT | Naskah −9 ha; prosedur tak terdokumentasi |
| Baseline kredit vs S1 | Definisi baseline | bandingkan deret | `03` | identik | VERIFIED | Lihat isu adisionalitas |
| Validasi historis stok (MAPE 3,92 %) | Kecocokan perilaku | – | tidak disertakan | diklaim | **UNVERIFIED** | Data dan skrip tidak ada; model mulai 2024 |
| Validasi historis aliran (MAPE 73,3 %) | Kecocokan laju | – | tidak disertakan | diklaim; lebih buruk dari pembanding | **UNVERIFIED** | Tidak disebut di naskah |
| Periode kalibrasi | – | – | Gambar 2 vs register | 2001–2014 vs 2000–2014 / 2003–2014 | UNVERIFIED | Tidak seragam |
| Konsistensi satuan | Dimensi | Units Check Vensim | – | – | NOT TESTED | Contoh: FTE bersatuan *People* |
| Monte Carlo | Ketidakpastian | 13 parameter; n = 3.000/1.500; seed 20261101 | tidak disertakan | diklaim | **UNVERIFIED** | Distribusi dan keluaran tidak ada |
| PRCC | Pengaruh parameter | – | tidak disertakan | +0,77; −0,79; +0,95 | **UNVERIFIED** | −0,79 dilabeli berbeda (akses vs biaya MRV) |
| Ekstrem lain (populasi 0, harga sangat tinggi, DT besar) | – | – | – | – | NOT TESTED | – |

## Pembedaan jenis validitas

| Jenis | Status |
|---|---|
| Validitas struktural | Neraca stok, konservasi kawasan/karbon, dan identitas keuangan: **VERIFIED**. Asumsi struktural utama (dosis-respons linear patroli, kehilangan akses) masih kelas C/D. |
| Verifikasi numerik | DT dan replikasi Vensim–PySD: **VERIFIED**. |
| Validitas perilaku historis | **UNVERIFIED** dari berkas yang ada. Validasi aliran yang dilaporkan lemah. |
| Robustness kebijakan | Lihat 07. Arah S2−S1 robust; besaran S4−S3 dan kelayakan USD 10 tidak robust. |

**Kebenaran komputasi tidak membuktikan validitas empiris.**
