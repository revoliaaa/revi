# Revisi Model SD Tesis: 3 Skenario (25 Hutan Desa, Kalimantan Barat)

Revisi model System Dynamics FINAL A1 (4 skenario) menjadi 3 skenario, memakai data patroli final peneliti: **2.533 HOK (2024, 20 HD)** dan **3.011 HOK (2025, 25 HD)**.

## Isi

| Folder | Berkas | Isi |
|---|---|---|
| `model/` | `DKP_25HD_FINAL_3SKENARIO.mdl` | Model Vensim FINAL 3 skenario: 723 variabel, 39 stok, 16 View. `Skenario Kebijakan` 1 = S1, 2 = S2, 3 = S3 |
| `model/` | `DKP_25HD_FINAL_3SKENARIO_ALOKASI.mdl` | Model eksperimen alokasi B0–B4, R1–R2 berbasis S3 |
| `hasil/` | `REGISTER_HASIL_SIMULASI_3SKENARIO.xlsx` | Register hasil, 23 lembar: indikator, selisih, seri tahunan, semua variabel, grid harga, alokasi, Monte Carlo, PRCC, verifikasi, lama vs baru |
| `laporan/` | `LAPORAN_PERUBAHAN_PERSAMAAN_MODEL_3S.md` | Perubahan persamaan dan penempatan patroli pembiayaan awal |
| `laporan/` | `LAPORAN_VERIFIKASI_VENSIM_PYSD_SENSITIVITAS_3S.md` | Verifikasi komputasi, validasi perilaku, Monte Carlo/PRCC, sensitivitas |
| `laporan/` | `RINGKASAN_PERUBAHAN_HASIL_4S_KE_3S.md` | Perbandingan hasil model lama dan baru |
| `makalah/` | `Makalah_Seminar_Hasil_Kalimantan_Barat_FINAL_REVISI_3SKENARIO.docx/.pdf` | Makalah Seminar Hasil, 10 halaman |
| `gambar/` | `gambar2–7.png` | Gambar 2–7 makalah, dibuat dari hasil model revisi |
| `skrip/` | `*.py` | Skrip rekonstruksi, simulasi, verifikasi, MC, gambar, register, dan makalah |

## Yang masih perlu dilakukan peneliti

1. **Jalankan model revisi di Vensim native**, lalu bandingkan dengan PySD memakai `skrip/bandingkan_vensim_pysd.py`. Langkahnya ada di laporan verifikasi bagian A1. Kalimat `[PERLU DIISI ...]` di subbab Validasi makalah diisi setelah langkah ini.
2. **Diagram View** pada `.mdl` dibuat otomatis, karena `.mdl` asli tidak ada di paket. Bila tata letak asli ingin dipertahankan, terapkan perubahan di laporan perubahan persamaan bagian 3 ke `.mdl` asli.
3. Isi nama mahasiswa di makalah.

## Menjalankan ulang

```bash
python3 -m venv venv && . venv/bin/activate && pip install pysd==3.14.3 openpyxl matplotlib python-docx scipy
```

Skrip mengharapkan struktur kerja `work/` (skrip dan JSON), `paket/` (berkas serah-terima), `fig/`, dan `out/`. Lihat bagian atas masing-masing skrip.
