# Skrip audit

Lingkungan: Python 3.13, PySD 3.14.3 (virtualenv), pandas, openpyxl.

## Urutan run

Model `.mdl` disalin ke folder kerja terlebih dahulu. Berkas asli tidak diubah.

1. `translate.py`: menerjemahkan semua `.mdl` ke `.py` (PySD).
2. `runall.py`: menjalankan run tahunan untuk perbandingan dengan ekspor Vensim.
3. `compare.py`: membandingkan hasil dengan ekspor Vensim (`vload.py` membaca `.txt` Vensim).
4. `runfine_all.py`: menjalankan run resolusi DT (0,0625) untuk semua skenario A1. Ini dasar semua angka.
5. `fine.py`: uji neraca stok-aliran.
6. `sweep.py <harga…>`: sapuan harga (ambang NPV dan cakupan).
7. `diag.py`: uji putus loop, rerun A2 (`Switch Baseline Kredit Konservatif` = 1), dan sapuan pengali akses.
8. `dt.py`: uji sensitivitas DT.
9. `robust.py`, `robust2.py`: robustness OAT.
10. `generate.py`, `tables.py`, `matrix.py`: menulis semua CSV di folder audit.

## Catatan

- `calc.py` berisi fungsi integral (Σ nilai × DT pada [a, b)), rerata integral, dan rerata sampel tahunan.
- Path di skrip menunjuk ke folder kerja sesi audit (scratchpad). Sesuaikan variabel `W`, `O`, `SRC` bila dijalankan ulang di tempat lain.
- `mdlparse.py` adalah parser sederhana untuk diff semantik persamaan `.mdl`.
