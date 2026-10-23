# Deck: Interpretasi review perhitungan karbon gambut — Hutan Desa, KHG Sungai Mempawah

Mengikuti skill `antislop-decks` dan pola build `build/build_deck.js`.

## Dials
DENSITY: 4 | MOTION: 1 | VARIANCE: 6 — dipresentasikan sekaligus dikirim sebagai pre-read; detail angka di speaker notes.

## Narrative arc (titles-only test)
1. Datanya valid, angka kreditnya belum
2. Data spasial bisa dipakai; metode emisi harus diganti sebelum angka kredit dibawa ke pembeli
3. Hampir seluruh areal bergambut, dan 2.015 ha di antaranya berstatus fungsi lindung
4. Dalam lima tahun terakhir hutan hilang 138 ha dan perkebunan melonjak dari 26 ha menjadi 359 ha
5. File menghitung emisi dari stok seluruh kolom gambut; yang hilang saat deforestasi adalah biomassa dan oksidasi bertahap
6. Empat blok di file memberi empat angka kredit berbeda — semuanya jauh dari hasil model koreksi
7. Salah ketik dan salah rujukan sel melipatgandakan angka hingga 100 kali
8. Dengan data proyek sendiri, baseline ±4.230 tCO₂e/thn menghasilkan ±1.240 tCO₂e kredit bersih per tahun
9. Pilihan laju deforestasi mengubah kredit 3,3 kali; nilai bagi LPHD jutaan, bukan miliaran rupiah per tahun
10. Titik terlemah additionality adalah hukum: gambut lindung memang sudah dilarang dibuka
11. Dari 1.025 ha yang dihitung sebagai ARR, hanya ±591 ha kandidat kuat
12. Leakage di gambut punya empat jalur; yang terbesar adalah 359 ha kebun yang bisa berpindah
13. Perbaiki data aktivitas dulu; harga dan pembeli menyusul (close + satu aksi)
14. Lampiran: parameter model koreksi

## Signature element
**Batang tutupan lahan 2026 (2.468,5 ha)** — hutan sekunder 1.411 · semak 609 · kebun 359 · lahan terbuka 57,6 · sungai 31,9,
proporsional. Besar di cover; mini *locator* di kiri bawah setiap slide yang menyorot kelas tutupan yang sedang dibahas.

## Palette & typography
Gambut gelap `#2B241E` (cover/close/panel) · hutan `#2F5D46` (koreksi/benar) · semak `#8C9A5B` · kebun `#C08A3E` ·
satu aksen bahaya `#B23A2E` hanya untuk kesalahan/angka file. Cambria (display) + Calibri (body).
Angka chart memakai format `[>=1000]0"."000;0` agar ribuan selalu bertitik di Office berbahasa apa pun.

## Build
```bash
npm install pptxgenjs   # lalu set NODE_PATH ke node_modules-nya
node build/build_deck_mempawah.js analisis-gambut-mempawah/Interpretasi_Karbon_Gambut_Mempawah.pptx <pptx-skill>/scripts/apply_theme.js
```
Semua angka berasal dari `Model_Koreksi_Karbon_Gambut_Mempawah.xlsx`.
