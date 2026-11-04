# 00 — Inventaris Sumber dan Provenans Hasil

Berkas pendukung:
- `source_inventory.csv`: md5, ukuran, waktu, dan catatan untuk setiap berkas di ZIP.
- `model_equation_diff.txt`: diff semantik persamaan.
- `traceability_matrix.csv`: keterlacakan dari naskah ke variabel.

## Berkas yang dibuka dan diperiksa

ZIP `MODEL_VENSIM.zip` berisi:
- 10 berkas `.mdl`/`.2mdl`;
- 9 `.vdfx` (biner Vensim; tidak dapat dibaca tanpa Vensim);
- 8 ekspor `.txt`;
- 2 `.xlsx`.

Naskah PDF dua kali diunggah dan identik (md5 `e74fdbdb…`). Semua berkas dibuka. Berkas `.vdfx` hanya dicatat md5-nya.

## Konfigurasi model (semua berkas A1)

| Unsur | Nilai |
|---|---|
| Waktu | 2024–2087 |
| Metode / langkah | Euler, DT 0,0625, SAVEPER 1 |
| Jumlah variabel | 724 (dihitung parser audit; 723 terbaca PySD + `Time`) |
| Switch S1 | 0 |
| Switch Baseline Kredit Konservatif | 0 |
| Faktor Rekonsiliasi Reversal Kredit A2 | 1 |

## Perbedaan antar-berkas skenario (diff semantik terhadap S4 USD10)

- **Tuas yang memang berbeda:** `Skenario Kebijakan` (1/2/3/4) dan `Harga Karbon`. Berkas S1–S3 memuat Harga Karbon = 6, tetapi tidak aktif karena Switch Karbon = 0.
- **Perbedaan yang tidak disengaja:** berkas S1, S2, S3, dan USD35 (disimpan 2 November) membulatkan 9 konstanta ke 6 angka penting. Contohnya:
  - luas PA 111.123 vs 111.123,17;
  - HMS awal 52.398,2 vs 52.398,18;
  - HRS awal 36.931,9 vs 36.931,85.
- **Akibatnya:** hutan awal 94.307,88 ha di berkas yang dibulatkan, dan 94.307,81 ha di berkas USD3/6/10/15/20. Dampaknya terhadap hasil ≤ 0,07 ha. **Tidak material, tetapi melanggar prinsip kondisi awal identik.**
- **Duplikat:** `DKP_25HD_A1_S4_USD35_rapi.2mdl` identik (md5) dengan `.mdl`.

## Provenans keluaran

| Skenario | Ekspor Vensim `.txt` | Label run di ekspor | Catatan |
|---|---|---|---|
| S1 | Skenario1.txt | SKENARIO1 | 686 variabel |
| S2 | Skenario2.txt | Run/Skenario2 | |
| S3 | Skenario3.txt | **Run/Untitled** | nama run tidak deskriptif |
| S4 USD6 / 10 / 15 | Skenario4USD*.txt | sesuai | |
| S4 USD20 | **tidak ada** | – | hanya `.vdfx` dan lembar xlsx yang rusak |
| S4 USD35 | **Untitled.txt** | Run/Skenario4USD35 | nama berkas tidak sesuai isi |

- **`HASIL SIMULASI VENSIM.xlsx` rusak.** Pemisah desimal hilang saat impor, sehingga 20–35 % nilai per lembar tidak cocok dengan `.txt` (contoh 20,1326 → 201326). Lembar S4USD20 berisi 1.530 baris, bukan ±1.053. **Status: INCONSISTENT; tidak dipakai.**
- **`REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx`** adalah hasil PySD dari berkas `.py` beku. README-nya menyatakan "Vensim native belum dijalankan", dan sumber hasil resminya, `a1/out/FINAL_THESIS_RESULTS.xlsx`, tidak disertakan. Nilai register cocok dengan run audit sampai pembulatan konstanta (contoh hutan S1 2087: register 81.889,746; audit 81.889,795).
- **Berkas induk `DELTA_KAPUAS_25HD_SD_FINAL_A1.mdl` (md5 f1bfaa88d84d61d6d9f990cda990253a) tidak ada di ZIP.** Keterlacakan ke berkas induk itu **BELUM TERVERIFIKASI**. Audit ini memakai berkas skenario di ZIP sebagai sumber otoritatif.

## Hierarki sumber yang dipakai

1. Run ulang PySD 3.14.3 atas salinan `.mdl` di ZIP, yang telah dicocokkan dengan ekspor `.txt` Vensim.
2. Persamaan `.mdl`.
3. Register.
4. Naskah.

Untuk USD 20, sumbernya adalah PySD saja. Run ini konsisten dengan register, dan berkasnya hanya berbeda dari USD 10 pada `Harga Karbon`.

## Matriks keterlacakan (ringkas)

Lihat `traceability_matrix.csv` dan `../08_MANUSCRIPT_RECONCILIATION/manuscript_reconciliation.csv`. Konvensi perhitungan yang direkonstruksi:

| Indikator | Variabel / rumus | Periode |
|---|---|---|
| Kumulatif fisik | Σ aliran × DT pada [2025, 2087) | 2025–2086 |
| Kumulatif keuangan | Σ aliran × DT pada [2024, 2087) | 2024–2086 |
| Rerata tahunan | integral [2030, 2056) / 26 | 2030–2055 |
| Jumlah KUPS | rerata nilai stok pada 26 titik tahunan | 2030–2055 (konvensi berbeda) |
| "Kredit model" | `Kredit REDD Diajukan` | 2024–2086 |
| NPV proyek | PV kontinu 10 % dari (kotor − biaya MRV/transaksi/pajak − pembiayaan awal − belanja LPHD) | 2024–2086 |
| NPV mitra | PV (Dana Mitra + Pemulihan Defisit − Kekurangan Biaya Ditanggung Mitra − Pembiayaan Awal) | 2024–2086 |
| "Cakupan kebutuhan minimum" | rerata `Penggunaan Dana Pengelolaan` / rerata `Kebutuhan Dana Minimum` | 2030–2055 |
