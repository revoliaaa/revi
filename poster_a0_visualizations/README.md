# Visualisasi poster A0

Enam visual untuk poster seminar hasil (A0 landscape). Interpretasi, keterbatasan, dan hasil audit data ada di `visualization_notes.md`; sumber dan definisi tiap indikator ada di `data_sources.csv`.

| Berkas | Isi |
|---|---|
| `01_peta_lokasi.{png,svg,pdf}` | Pengganti non-spasial: luas per HD. **Peta menunggu shapefile.** |
| `02_mekanisme_sistem.*` | Diagram loop umpan balik inti |
| `03_waterfall_deforestasi.*` | S2−S1, S3−S2, S4−S3 (USD20), total |
| `04_threshold_pembiayaan.*` | NPV dan cakupan LPHD menurut harga, USD1–40 |
| `05_diverging_pendapatan.*` | Manfaat program vs kehilangan akses (USD10, USD20) |
| `06_quadrant_alokasi.*` | Alternatif alokasi B0–B4, R1, R2 (hanya titik bernilai numerik) |
| `poster_visual_preview.pdf` | Keenam visual, satu halaman per visual |

## Reproduksi

```bash
pip install matplotlib pandas numpy openpyxl     # + geopandas bila ada shapefile
python scripts/extract_data.py --results FINAL_THESIS_RESULTS.xlsx --out data
python scripts/make_figures.py
```

`data/hutan_desa_tabel1.csv` dan `data/alokasi_manfaat_makalah.csv` diketik dari makalah, dengan rujukan halaman. Berkas lain di `data/` diekstrak dari `FINAL_THESIS_RESULTS.xlsx` dengan presisi penuh. Huruf: Liberation Sans (metrik setara Arial).
