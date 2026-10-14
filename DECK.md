# Deck: Multiusaha Kehutanan Karbon — PT Mayawana Persada — laporan keputusan (decision deck)

Dibuat mengikuti skill `antislop-decks` (jhuse25/anti-slop-kit, MIT) yang terpasang di `.claude/skills/`.

## 0. Dials
DENSITY: 4 | MOTION: 1 | VARIANCE: 6
(Deck dipresentasikan ke manajemen tetapi juga dikirim sebagai pre-read: densitas sedikit di atas baseline,
detail dipindah ke speaker notes. Tanpa animasi/transisi.)

## 1. Format and engine
Aspect: 16:9 (13,33" × 7,5") | Engine: pptx dari nol (pptxgenjs, layout + theme terstruktur)
Brand: tidak ada DESIGN.md klien → identitas minimal dideklarasikan di bawah.

## 2. Narrative arc (titles-only test)
1. Satu izin, dua portofolio: kayu dan karbon di PBPH ±138.258 ha
2. Peluang kuat, tetapi nilainya baru nyata setelah lolos tiga gate
3. Siklus HTI akasia saat ini menciptakan empat sumber emisi yang wajib dipetakan
4. PBPH tidak dilepas: portofolionya dibagi menjadi 66.908 ha kayu dan 71.350 ha karbon
5. — Gate 1 · Legal: Apakah BAU legal dan areal benar-benar eligible?
6. Payung hukumnya sudah tersedia — perubahan masuk lewat RKUPH, bukan izin baru
7. Lima uji legal baseline: jawaban awal positif, tetapi harus dibuktikan dengan dokumen
8. Screening memisahkan areal yang bisa dikreditkan dari areal yang memang wajib dilindungi
9. — Gate 2 · Karbon: Apakah additionality dan metodologi dapat dipertahankan?
10. Unit karbon hanyalah selisih terverifikasi antara skenario baseline dan skenario proyek
11. Kawasan lindung menyimpan 70,3 juta tCO₂e — 4,8 kali stok kawasan budidaya
12. Pembukaan 46.648 ha sejak 2021 melepas ±12,2 juta tCO₂ — hampir separuhnya dari kohort 2023
13. Jika konsesi bergambut, ada lima sumber mitigasi — dan satu larangan: double counting
14. — Gate 3 · Bisnis: Apakah risk-adjusted NPV karbon mengalahkan alternatif HTI?
15. Bandingkan NPV, bukan harga karbon per hektar
16. Empat variabel menentukan apakah 71.350 ha benar-benar bankable
17. Pada skenario konservatif, pendapatan karbon hanya ±US$6,5 juta di atas opportunity cost
18. Risiko terbesar adalah integritas baseline, bukan teknis MRV
19. Tujuh tahap, satu gate: RKUPH baru diubah setelah tahap 03
20. Sepuluh dokumen yang sudah dimiliki perusahaan menjadi bukti baseline
21. Lanjutkan ke feasibility study — bukan langsung ke pengembangan proyek (close + aksi)
22–23. Lampiran: skema kerja sama; data stok & emisi

## 3. Signature element (mandatory, exactly one)
**Batang rasio konsesi 48 : 52** — satu batang horizontal yang membagi PBPH 138.258 ha secara
proporsional menjadi 66.908 ha budidaya (HTI) dan 71.350 ha lindung (kandidat karbon).
Lapisan: data + visual system. Berasal dari angka nyata perusahaan, tidak bisa disalin ke deck lain.
Sustained in: cover (besar), slide model transformasi (penuh, berisi angka), dan sebagai *locator* mini
di kiri bawah setiap slide konten yang menyorot zona mana yang sedang dibahas; kembali penuh di slide penutup.

## 4. Palette and typography
- Dominan: hutan gelap `#163A2E` (cover, divider, penutup) + putih untuk konten
- Data: lindung `#1F5A45`, budidaya/akasia `#9C967F`; satu aksen tembaga `#B5551F` hanya untuk risiko/gate
- Teks off-black `#1B2420` (bukan #000), muted `#5F6B65`, hairline `#D5DBD6`, tint panel `#EEF2EE`
- Display: Cambria (judul, angka besar, divider) | Body: Calibri
  (dipilih karena terpasang di semua Office & ter-render akurat; karakter datang dari pasangan serif–sans + hierarki ukuran, bukan dari default template)

## 5. Archetype system
Cover · Section divider (per gate, angka gate raksasa) · Assertion-evidence (diagram/chart) ·
Big number + chart · Comparison dua zona · Diagram alur buatan sendiri (tanpa SmartArt) · Tabel data-ink ·
Close dengan satu aksi. Tidak ada dua slide berurutan dengan arketipe yang sama.

## 6. Charts
Native PowerPoint chart; bar horizontal untuk stok, kolom untuk emisi per kohort (kohort 2023 disorot tembaga),
clustered bar pendapatan vs opportunity cost. Direct labels, tanpa gridline, tanpa 3D, palet deck.

## 7. Anti-patterns (BANNED)
Judul-label (“Risk Register”) → diganti kalimat asersi · bullet soup · slide “Terima kasih/Pertanyaan?” ·
garis aksen di bawah judul · strip warna di tepi kartu · tiga kartu identik · emoji · SmartArt ·
paragraf di slide (pindah ke notes) · angka bulat palsu · kata klise AI.

## 8. Build
```bash
npm install pptxgenjs            # di folder mana pun, lalu set NODE_PATH ke node_modules-nya
node build/build_deck.js out.pptx <path>/pptx/scripts/apply_theme.js
```
Output: `FINAL_Analisis_Multiusaha_Kehutanan_PT_Mayawana_Persada.pptx` (+ PDF pratinjau).
Original disimpan di `assets/original_Analisis_Multi_Usaha_Kehutanan.pptx`.
Catatan chart: nilai di data chart disimpan ×10 dan diberi format `0\,0` agar label selalu tampil dengan koma desimal (70,3) di Office berbahasa apa pun.
