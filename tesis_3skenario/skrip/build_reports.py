import json, sys
sys.path.insert(0, "work"); import naskah as N
f, R, D, E = N.f, N.R, N.D, N.E
V = json.load(open("work/verifikasi_3s.json")); MC = N.MC; MA = N.MA; OAT = N.OAT; DK = json.load(open("work/dekomposisi.json"))
OLDMC = json.load(open("work/mc_old_test_sum.json"))
pct = N.pct
L = ["# Laporan Verifikasi Vensim–PySD dan Sensitivitas: Model FINAL 3 SKENARIO", "",
 "Laporan ini memisahkan **verifikasi komputasi**, yaitu apakah model dihitung dengan benar sesuai persamaannya, dari **validasi perilaku**, yaitu apakah perilaku model cukup mewakili sistem nyata.", "",
 "## A. Verifikasi komputasi", "",
 "### A1. Vensim native vs PySD (model revisi)", "",
 "**Status: BELUM DILAKUKAN.** Perangkat Vensim tidak tersedia di lingkungan komputasi ini, sehingga perbandingan untuk model revisi belum ada.",
 "Hasil lama (99,87–100 % identik) berlaku untuk model empat skenario dan **tidak** dianggap sebagai verifikasi model revisi.", "",
 "Langkah yang perlu dijalankan peneliti:",
 "1. Buka `DKP_25HD_FINAL_3SKENARIO.mdl` di Vensim, lalu jalankan *Units Check* dan *Check Model*.",
 "2. Jalankan 7 run: `S1`, `S2`, `S3_USD6`, `S3_USD10`, `S3_USD15`, `S3_USD20`, `S3_USD35`. Ubah `Skenario Kebijakan` (1/2/3) dan `Harga Karbon`.",
 "3. Ekspor setiap run ke `.tab`. Jangan membukanya lewat Excel berlocale Indonesia.",
 "4. Jalankan `python bandingkan_vensim_pysd.py DKP_25HD_FINAL_3SKENARIO.mdl S1.tab S2.tab S3_USD10.tab ...`. Kriteria cocok: selisih relatif ≤ 10⁻⁵ atau absolut ≤ 10⁻⁶.", "",
 "### A2. Rekonstruksi model terhadap hasil resmi FINAL A1", "",
 "Berkas `.mdl` asli tidak ada di paket, jadi model direkonstruksi dari register variabel. Hasilnya diuji terhadap register data resmi:", "",
 "| Uji | Nilai dibandingkan | Berbeda > 0,01 % |", "|---|---|---|",
 "| A1 S1–S4 USD6–35 (8 skenario) | 17.472 | 0 |", "| Eksperimen alokasi (7 run B0–R2) | 15.596 | 0 |",
 "| NPV, harga impas (6,83 / 7,40), cakupan 100 % (USD 28,04), S2−S1 (1.720 ha), S4−S3 (535 / 3.588 ha) | – | 0 |", "",
 "Model revisi juga dibaca PySD dengan opsi pemisahan View; ke-16 View terbaca dan hasilnya identik dengan versi tanpa pemisahan.", "",
 "### A3. Uji struktur, penempatan patroli, kondisi ekstrem, dan langkah waktu", "", "| Uji | Status | Rincian |", "|---|---|---|"]
for t in V: L.append(f"| {t['uji']} | {t['status']} | {t['rincian']} |")
L += ["", "Catatan uji ekstrem: tanpa patroli, deforestasi kumulatif S2 sedikit **lebih besar** daripada S1 (+58 ha). Selisih ini bukan galat. Rehabilitasi pada S2 menambah stok hutan, dan deforestasi dihitung proporsional terhadap stok, sehingga hutan yang lebih luas menghasilkan deforestasi absolut yang sedikit lebih besar. Hutan 2087 pada S2 tetap lebih luas daripada S1.", "",
 "### A4. Uji putus loop (dana karbon → patroli)", "", "| Harga | S3−S2 utuh (ha) | S3−S2 tanpa dana ke patroli (ha) | Kredit utuh (tCO₂e) | Kredit putus (tCO₂e) |", "|---|---|---|---|---|"]
for p, v in OAT["putus_loop"].items(): L.append(f"| USD {p} | {f(v['S3-S2 utuh'])} | {f(v['S3-S2 tanpa dana ke patroli'])} | {f(v['kredit utuh'])} | {f(v['kredit putus'])} |")
L += ["", "Seluruh tambahan perlindungan dari karbon bekerja melalui belanja patroli. Kredit yang tersisa saat loop diputus (±45.900 tCO₂e) berasal dari efek patroli pembiayaan awal 2024–2025 terhadap baseline S1.", "",
 "## B. Validasi perilaku", "",
 "- **Stok hutan 2019/2024:** MAPE 3,92 %; pembanding linear 8,88 % dan laju konstan 8,43 %. **Aliran kehilangan Hansen 2017–2024:** MAPE 73,3 %.",
 "- Kedua uji itu berasal dari model lama. **Tetap berlaku** untuk model revisi, karena laju BAU, kondisi awal, dan skenario S1 tidak berubah: hasil S1 identik, yaitu hutan 2087 81.890 ha dan deforestasi 29.812 ha.",
 "- Uji perilaku itu tidak dijalankan ulang di sesi ini. Skrip hindcast-nya tidak ada di paket.",
 "- Belum ada data deforestasi pasca-2025 untuk menguji perilaku S2. Penurunan deforestasi 2025 (520 → 458 ha) masih perlu dibandingkan dengan data Hansen 2025 per HD bila tersedia.", "",
 "## C. Ketidakpastian: Monte Carlo dan PRCC", "",
 f"Desain: hiperkubus Latin, seed 20261101, 13 parameter, n = {f(MC['USD10']['n'])} (USD 10) dan {f(MC['USD20']['n'])} (USD 20). Spesifikasi sebaran ada di register hasil, lembar 18.",
 "Skrip dan berkas Monte Carlo lama tidak ada di paket, jadi spesifikasi disusun ulang dari rentang ketidakpastian di register variabel.",
 "Sebagai uji kewajaran, spesifikasi ini dijalankan pada model lama (n = 200). Hasilnya mendekati angka MC lama:", "",
 "| Ukuran (model lama) | MC lama | Spesifikasi baru pada model lama (n = 200) |", "|---|---|---|",
 f"| Median S2−S1 (ha) | 1.561 | {f(OLDMC['S2-S1']['median'])} |", f"| S4>S3 pada USD 10 | 92,6 % | {pct(OLDMC['USD10']['freq_karbon_tambah_perlindungan'])} % |",
 f"| Median S4−S3 USD 10 (ha) | 265 | {f(OLDMC['USD10']['median_tambahan_ha'])} |", f"| NPV>0 pada USD 10 | 60,9 % | {pct(OLDMC['USD10']['freq_NPV_pos'])} % |", f"| Kebutuhan LPHD tertutup USD 10 | 0 % | {pct(OLDMC['USD10']['freq_kebutuhan_tertutup'])} % |", "",
 "### Hasil model revisi", "", "| Ukuran | USD 10 | USD 20 |", "|---|---|---|"]
m10, m20 = MC["USD10"], MC["USD20"]
for lab, k, fn in [("Frekuensi karbon menambah perlindungan (S3<S2)", "freq_karbon_tambah_perlindungan", lambda x: pct(x) + " %"), ("Median S3−S2 (ha)", "median_tambahan_ha", lambda x: f(x)),
                   ("P5–P95 S3−S2 (ha)", None, None), ("NPV>0", "freq_NPV_pos", lambda x: pct(x) + " %"), ("Median NPV (Rp miliar)", "median_NPV", lambda x: f(x / 1e9, 2)),
                   ("Kebutuhan minimum LPHD tertutup", "freq_kebutuhan_tertutup", lambda x: pct(x) + " %"), ("Median cakupan kebutuhan (%)", "median_cakupan", lambda x: f(x, 1)),
                   ("Pendapatan RT naik (S3>S2)", "freq_pendapatan_naik", lambda x: pct(x) + " %")]:
    if k is None: L.append(f"| {lab} | {f(m10['p5'])}–{f(m10['p95'])} | {f(m20['p5'])}–{f(m20['p95'])} |")
    else: L.append(f"| {lab} | {fn(m10[k])} | {fn(m20[k])} |")
s21 = MC["S2-S1"]
L += ["", f"S2−S1: positif pada {pct(s21['freq_S2_lt_S1'])} % tarikan; median {f(s21['median'])} ha (P5–P95 {f(s21['p5'])}–{f(s21['p95'])} ha).", "", "**PRCC (empat parameter terkuat):**", ""]
def tp(pr, n=4): return "; ".join(f"{a} {b:+.2f}".replace(".", ",") for a, b in sorted(pr.items(), key=lambda t: -abs(t[1]))[:n])
L += [f"- S2−S1: {tp(s21['prcc'])}", f"- S3−S2 USD 20: {tp(m20['prcc_tambahan'])}", f"- NPV USD 20: {tp(m20['prcc_NPV'])}", f"- Δ pendapatan RT USD 20: {tp(m20['prcc_dpendapatan'])}", "",
 "Frekuensi Monte Carlo adalah proporsi ensembel, bukan peluang kejadian.", "", "## D. Sensitivitas satu-per-satu", "",
 "| Parameter (rendah / tinggi) | S2−S1 (ha) | S3−S2 USD 20 (ha) | S3−S2 USD 35 (ha) | NPV USD 20 (Rp miliar) |", "|---|---|---|---|---|"]
for n, v in OAT["oat"].items():
    lo, hi = v["rendah"], v["tinggi"]
    if "S2-S1 (ha)" not in lo: L.append(f"| {n} | – | – | – | {f(lo['NPV USD20']/1e9,2)} / {f(hi['NPV USD20']/1e9,2)} |"); continue
    L.append(f"| {n} | {f(lo['S2-S1 (ha)'])} / {f(hi['S2-S1 (ha)'])} | {f(lo['S3-S2 USD20 (ha)'])} / {f(hi['S3-S2 USD20 (ha)'])} | {f(lo['S3-S2 USD35 (ha)'])} / {f(hi['S3-S2 USD35 (ha)'])} | {f(lo['NPV USD20']/1e9,2)} / {f(hi['NPV USD20']/1e9,2)} |")
L += ["", "## E. Eksperimen alokasi: kekokohan", "",
 "- **22 kombinasi sensitivitas** (11 varian × USD 10/20): B1 dan R1 tidak pernah lebih buruk daripada B0 (22/22). R2 menambah hutan pada 18/22 kombinasi, tetapi lebih buruk bagi RT terdampak pada sebagian besar kombinasi. B2–B4 lebih buruk bagi hutan pada 18–20/22.",
 f"- **Monte Carlo berpasangan** (n = {f(MA['R1-10']['n'])}):"]
for k, v in MA.items(): L.append(f"  - {k}: tidak lebih buruk {pct(v['tidak_lebih_buruk'])} %; dominan lemah {pct(v['dominan_lemah'])} %; hutan naik {pct(v['hutan_naik'])} %; median Δ pendapatan RT terdampak Rp {f(v['median_dpend'])}")
open("out/LAPORAN_VERIFIKASI_VENSIM_PYSD_SENSITIVITAS_3S.md", "w").write("\n".join(L) + "\n")
# ---------------- ringkasan perubahan
o = {"S2-S1": 1720, "S3-S1old": 1997}
rows = [("Patroli 2024 (HOK)", "S3: 5.757 (2.355 swadaya + 3.402 pembiayaan awal)", "2.533 (S2, S3)"),
 ("Patroli 2025 (HOK)", "S3: 5.757 (2025 = 2024)", "3.011 (S2, S3)"),
 ("Patroli setelah 2025 tanpa dana karbon", "2.355 HOK/th swadaya (S2–S4)", "0"),
 ("Pembiayaan awal (Rp miliar)", "1,77 (estimasi)", f(R['S2']['Pembiayaan awal 2024-2025 (Rp)']/1e9, 2)),
 ("Deforestasi dihindari oleh PS ± pembiayaan awal vs S1 (ha)", "S2 1.720; S3 1.997", f"S2 {f(N.av('S2'))}"),
 ("Emisi dihindari vs S1 (tCO₂e)", "S2 597.963; S3 675.168", f"S2 {f(N.em('S2'))}"),
 ("Hutan 2087 (ha)", "S2 83.615; S3 83.779; S4 USD10 84.233; USD20 87.113; USD35 90.698", f"S2 {f(R['S2']['Hutan 2087 (ha)'])}; S3 USD10 {f(R['S3 USD10']['Hutan 2087 (ha)'])}; USD20 {f(R['S3 USD20']['Hutan 2087 (ha)'])}; USD35 {f(R['S3 USD35']['Hutan 2087 (ha)'])}"),
 ("Tambahan dari karbon (ha)", "S4−S3: USD6 120; USD10 535; USD15 1.494; USD20 3.588; USD35 6.792", "S3−S2: " + "; ".join(f"USD{p} {f(N.add(f'S3 USD{p}'))}" for p in [6, 10, 15, 20, 35])),
 ("Kredit model (ribu tCO₂e)", "USD10 460; USD20 1.017; USD35 1.615", "; ".join(f"USD{p} {f(R[f'S3 USD{p}']['Kredit REDD model diajukan (tCO2e)']/1000, 1)}" for p in [6, 10, 20, 35])),
 ("Dana LPHD (Rp miliar)", "USD10 22,4; USD20 147,1; USD35 431,6", "; ".join(f"USD{p} {f(R[f'S3 USD{p}']['Dana LPHD diterima 2024-2086 (Rp)']/1e9, 1)}" for p in [10, 20, 35])),
 ("NPV proyek (Rp miliar)", "S3 −1,62; USD10 2,07; USD20 11,50; USD35 30,79", f"S2 {f(R['S2']['NPV proyek 10% (Rp)']/1e9,2)}; " + "; ".join(f"USD{p} {f(R[f'S3 USD{p}']['NPV proyek 10% (Rp)']/1e9, 2)}" for p in [10, 20, 35])),
 ("Harga impas proyek / mitra (USD/tCO₂e)", "6,83 / 7,40", f"{f(N.BE['npv'],2)} / {f(N.BE['npv_mitra'],2)}"),
 ("Kebutuhan minimum LPHD (Rp miliar/th)", "5,42", "6,03"),
 ("Harga saat kebutuhan minimum tercukupi (USD)", "28,04", f(N.BE['cov'], 2)),
 ("Cakupan kebutuhan USD10 / USD20 / USD35 (%)", "11,8 / 49,7 / 133,5", " / ".join(f(R[f'S3 USD{p}']['Cakupan kebutuhan minimum LPHD (%)'], 1) for p in [10, 20, 35])),
 ("Intensitas perlindungan rerata 2030–2055", "S2 0,29; USD10 0,39; USD20 0,68; USD35 0,97", f"S2 0; USD10 {f(R['S3 USD10']['Intensitas perlindungan rerata 2030-2055'],3)}; USD20 {f(R['S3 USD20']['Intensitas perlindungan rerata 2030-2055'],3)}; USD35 {f(R['S3 USD35']['Intensitas perlindungan rerata 2030-2055'],2)}"),
 ("FTE rerata", "S2 13,6; USD10 17,3; USD20 32,8; USD35 64,5", f"S2 {f(N.fte('S2'),1)}; USD10 {f(N.fte('S3 USD10'),1)}; USD20 {f(N.fte('S3 USD20'),1)}; USD35 {f(N.fte('S3 USD35'),1)}"),
 ("Pendapatan rata-rata RT (Rp juta)", "41,18–41,25 (perubahan < 0,5 %)", f"{f(R['S3 USD35']['Pendapatan bersih per RT bergantung (Rp/RT/th)']/1e6,2)}–{f(R['S2']['Pendapatan bersih per RT bergantung (Rp/RT/th)']/1e6,2)} (perubahan < 0,5 %)"),
 ("R1 vs B0", "tidak lebih buruk 22/22; dominan lemah 100 % / 99,9 % MC", f"tidak lebih buruk 22/22; tidak lebih buruk {pct(MA['R1-10']['tidak_lebih_buruk'])} % / {pct(MA['R1-20']['tidak_lebih_buruk'])} % MC (USD10/20)"),
 ("Monte Carlo: karbon menambah perlindungan USD10 / USD20", "92,6 % / 99,5 %", f"{pct(m10['freq_karbon_tambah_perlindungan'])} % / {pct(m20['freq_karbon_tambah_perlindungan'])} %"),
 ("Monte Carlo: NPV>0 USD10 / USD20", "60,9 % / 94,6 %", f"{pct(m10['freq_NPV_pos'])} % / {pct(m20['freq_NPV_pos'])} %")]
L = ["# Ringkasan Perubahan Hasil: Model 4 Skenario (FINAL A1) → Model 3 Skenario", "",
 "## Perubahan kunci", "",
 f"1. **Struktur skenario.** Skenario lama S1 (tanpa PS), S2 (PS reguler + swadaya 2.355 HOK/th), S3 (+ pembiayaan awal Rp 1,77 miliar), dan S4 (+ karbon) diganti menjadi S1 (tanpa PS aktif), **S2 (PS + pembiayaan awal; patroli aktual 2.533 HOK pada 2024 dan 3.011 HOK pada 2025)**, dan **S3 (S2 + karbon)**.",
 "2. **Patroli setelah 2025.** Patroli swadaya lama tidak dipakai lagi. Tanpa sumber dana, tidak ada patroli setelah 2025, kecuali yang dibiayai penerimaan karbon pada S3.",
 f"3. **Kontribusi S2−S1 turun dari 1.720 ha menjadi {f(N.av('S2'))} ha.** Uji diagnostik memisahkan sumbernya (diagnostik ini bukan skenario penelitian):",
 f"   - Patroli final 2024–2025 ditambah swadaya lama 2.355 HOK/th setelah 2025 memberi {f(DK['Diagnostik: patroli final 2024-25 + swadaya lama 2.355 HOK sesudah 2025'])} ha. Angka ini dekat dengan nilai lama S3 1.997 ha dan S2 1.720 ha.",
 f"   - Setelah swadaya dihapus, nilainya menjadi {f(N.av('S2'))} ha.",
 f"   - Jadi sekitar {f(100*(DK['Diagnostik: patroli final 2024-25 + swadaya lama 2.355 HOK sesudah 2025']-N.av('S2'))/(1997-N.av('S2')),0)} % perubahan berasal dari dihapusnya patroli swadaya berkelanjutan. Penggantian angka patroli 2024–2025 hanya berpengaruh kecil.",
 "4. **Loop karbon melemah pada harga rendah.**",
 "   - Dulu kredit awal berasal dari efek swadaya terhadap baseline S1, sehingga loop dana–patroli langsung berjalan.",
 "   - Kini kredit awal hanya berasal dari efek patroli 2024–2025 yang memudar, sementara biaya MRV tetap.",
 f"   - Akibatnya tambahan karbon pada USD 10 turun dari 535 menjadi {f(N.add('S3 USD10'))} ha, dan pada USD 20 dari 3.588 menjadi {f(N.add('S3 USD20'))} ha. Loop baru berjalan kuat pada USD 35 ({f(N.add('S3 USD35'))} ha).",
 f"5. **Ambang finansial naik.** Harga impas proyek naik dari USD 6,83 menjadi USD {f(N.BE['npv'],2)}. Kebutuhan minimum LPHD naik dari Rp 5,42 menjadi Rp 6,03 miliar/th, dan baru tercukupi pada USD {f(N.BE['cov'],0)} (dulu USD 28).",
 "6. **Kesimpulan alokasi R1 tetap berlaku.** R1 tidak mengurangi hutan dan menaikkan pendapatan RT terdampak. Besarannya jauh lebih kecil pada USD 10–20 karena dana fleksibel kecil.",
 "7. **Kesimpulan yang berubah arah:**",
 "   - Dulu: \"PS menahan sebagian besar kehilangan hutan\" dan \"proyek layak mulai USD 6,83\".",
 "   - Kini: perlindungan hanya bertahan selama patroli didanai, dan kelayakan finansial baru tercapai di atas sekitar USD 18.",
 "   - Rekomendasi bergeser ke **pembiayaan terpadu yang menjembatani jeda** antara akhir pembiayaan awal dan penerimaan karbon pertama.", "",
 "## Tabel perbandingan", "", "| Indikator | Model 4 skenario (lama) | Model 3 skenario (baru) |", "|---|---|---|"]
L += [f"| {a} | {b} | {c} |" for a, b, c in rows]
L += ["", "Angka lama dari `RANGKUMAN_SERAH_TERIMA_CHAT.md` dan `REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx`; angka baru dari `REGISTER_HASIL_SIMULASI_3SKENARIO.xlsx`.",
 "Monte Carlo lama dan baru memakai spesifikasi yang tidak persis sama (lihat laporan verifikasi bagian C)."]
open("out/RINGKASAN_PERUBAHAN_HASIL_4S_KE_3S.md", "w").write("\n".join(L) + "\n")
print("ok")
