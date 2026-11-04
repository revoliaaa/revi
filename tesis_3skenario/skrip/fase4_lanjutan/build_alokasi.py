"""MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl = v2 + struktur eksperimen alokasi (dana fleksibel dan kompensasi RT terdampak).
Dengan Switch Alokasi Dana Fleksibel = 0 model harus identik dengan v2."""
src = open("fase4/build_final.py", encoding="utf-8").read()
F = "Switch Alokasi Dana Fleksibel"
def flex(cat, porsi, keb):
    return f"IF THEN ELSE({F}=1, MIN(Dana Fleksibel LPHD*{porsi}, {keb}), MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif {cat}, {keb}))"
AL = {
 F: ("0", "Dmnl", "PWD-A", "1 = eksperimen alokasi dana fleksibel (B1–B4, R1, R2); 0 = alokasi proporsional dasar (B0). Hanya mengubah pembagian kas LPHD yang tersedia"),
 "Porsi Dana Fleksibel Patroli": ("0.4", "Dmnl", "PWD-A", ""), "Porsi Dana Fleksibel Rehabilitasi": ("0.2", "Dmnl", "PWD-A", ""),
 "Porsi Dana Fleksibel Pengendalian Kebakaran": ("0.1", "Dmnl", "PWD-A", ""), "Porsi Dana Fleksibel Pengembangan KUPS": ("0.2", "Dmnl", "PWD-A", ""),
 "Porsi Dana Fleksibel Kompensasi RT Terdampak": ("0.1", "Dmnl", "PWD-A", ""),
 "Jumlah Porsi Dana Fleksibel": ("Porsi Dana Fleksibel Patroli+Porsi Dana Fleksibel Rehabilitasi+Porsi Dana Fleksibel Pengendalian Kebakaran+Porsi Dana Fleksibel Pengembangan KUPS+Porsi Dana Fleksibel Kompensasi RT Terdampak", "Dmnl", "PWD-A", "Harus = 1"),
 "Dana Fleksibel LPHD": ("MAX(0, Dana Desa Tersedia-Alokasi Dana Operasional LPHD-Alokasi Dana Penguatan Kelembagaan)", "Rupiah/Year", "PWD-A", "Sisa dana tersedia sesudah operasional dan kelembagaan"),
 "Kebutuhan Dana Kompensasi": ("Kehilangan Pendapatan Agregat", "Rupiah/Year", "PWD-A", "Kehilangan pendapatan akibat pembatasan akses (total, bukan hanya tambahan S2)"),
 "Alokasi Dana Kompensasi RT Terdampak": (f"{F}*MIN(Dana Fleksibel LPHD*Porsi Dana Fleksibel Kompensasi RT Terdampak, Kebutuhan Dana Kompensasi)", "Rupiah/Year", "PWD-A", "Dibiayai dari saldo LPHD (dana karbon dan non-karbon)"),
 "Realisasi Kompensasi RT Terdampak": ("Alokasi Dana Kompensasi RT Terdampak*Rasio Realisasi Belanja", "Rupiah/Year", "PWD-A", "Mengurangi saldo LPHD melalui Penggunaan Dana Desa"),
 "Kumulatif Realisasi Kompensasi": ("INTEG(Realisasi Kompensasi RT Terdampak, 0)", "Rupiah", "PWD-A", ""),
 "Kompensasi per RT Terdampak": ("IF THEN ELSE(RT Terdampak Akses>0, Realisasi Kompensasi RT Terdampak/RT Terdampak Akses, 0)", "Rupiah/(Household*Year)", "PWD-A", "Diterima RT pemegang garapan yang terdampak pembatasan akses"),
 "Kompensasi Rata rata per RT Bergantung": ("IF THEN ELSE(Rumah Tangga Bergantung Hutan>0, Realisasi Kompensasi RT Terdampak/Rumah Tangga Bergantung Hutan, 0)", "Rupiah/(Household*Year)", "PWD-A", ""),
 "Rasio Kompensasi terhadap Kehilangan Akses": ("IF THEN ELSE(Kebutuhan Dana Kompensasi>0, Realisasi Kompensasi RT Terdampak/Kebutuhan Dana Kompensasi, 0)", "Dmnl", "PWD-A", ""),
 "Pendapatan Bersih per RT Terdampak": ("Pendapatan Hutan per RT Bergantung+Pendapatan Non Hutan per RT Bergantung+Pendapatan Program per RT Bergantung-Kehilangan per RT Terdampak+Kompensasi per RT Terdampak", "Rupiah/(Household*Year)", "PWD-A", "RT pemegang garapan dalam HD"),
 "Pendapatan Bersih per RT Tidak Terdampak": ("Pendapatan Hutan per RT Bergantung+Pendapatan Non Hutan per RT Bergantung+Pendapatan Program per RT Bergantung", "Rupiah/(Household*Year)", "PWD-A", ""),
 "Alokasi Dana Perlindungan": (flex("Perlindungan", "Porsi Dana Fleksibel Patroli", "Kebutuhan Dana Perlindungan"), "Rupiah/Year", "PWD-A", ""),
 "Alokasi Dana Rehabilitasi": (flex("Rehabilitasi", "Porsi Dana Fleksibel Rehabilitasi", "Kebutuhan Dana Rehabilitasi"), "Rupiah/Year", "PWD-A", ""),
 "Alokasi Dana Pengendalian Kebakaran": (flex("Pengendalian Kebakaran", "Porsi Dana Fleksibel Pengendalian Kebakaran", "Kebutuhan Dana Pengendalian Kebakaran"), "Rupiah/Year", "PWD-A", ""),
 "Alokasi Dana Pengembangan KUPS": (flex("Pengembangan KUPS", "Porsi Dana Fleksibel Pengembangan KUPS", "Kebutuhan Dana Pengembangan KUPS"), "Rupiah/Year", "PWD-A", ""),
 "Total Alokasi Dana Program": ("Alokasi Dana Operasional LPHD+Alokasi Dana Perlindungan+Alokasi Dana Pengendalian Kebakaran +Alokasi Dana Rehabilitasi+Alokasi Dana Penguatan Kelembagaan+Alokasi Dana Pengembangan KUPS+Alokasi Dana Kompensasi RT Terdampak", "Rupiah/Year", "PWD-A", "Termasuk kompensasi"),
 "Alokasi Tidak Terealisasi": ("Total Alokasi Dana Program-Penggunaan Dana Pengelolaan-Realisasi Kompensasi RT Terdampak", "Rupiah/Year", "PWD-A", ""),
 "Penggunaan Dana Desa": ("Penggunaan Dana Pengelolaan+Realisasi Kompensasi RT Terdampak", "Rupiah/Year", "PWD-A", "Kompensasi mengurangi saldo LPHD"),
 "Pendapatan Bersih per RT Bergantung": ("Pendapatan Hutan per RT Bergantung+Pendapatan Non Hutan per RT Bergantung+Pendapatan Program per RT Bergantung -Kehilangan Pendapatan Pembatasan Akses per RT+Kompensasi Rata rata per RT Bergantung", "Rupiah/(Household*Year)", "PWD-A", "+ kompensasi rata-rata"),
 "Check Anggaran Alokasi": ("Dana Desa Tersedia-Total Alokasi Dana Program", "Rupiah/Year", "PWD-A", "Uji: >= 0 (alokasi tidak melebihi dana tersedia)"),
}
inj = "AL = " + repr(AL) + "\nFIN.update(AL)\nVIEW['PWD-A'] = '14 LPHD Finance Allocation'\n"
src = src.replace("for k, v in FIN.items(): EXTRA[k] = v", inj + "for k, v in FIN.items(): EXTRA[k] = v")
assert "FIN.update(AL)" in src
exec(compile(src, "build_alokasi", "exec"))
