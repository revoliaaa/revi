F = "Switch Alokasi Dana Fleksibel"
def flex(cat, porsi, keb):
    return (f"IF THEN ELSE({F}=1, Switch Karbon*MIN(Dana Fleksibel LPHD*{porsi}, {keb}), "
            f"Switch Karbon*MIN(Dana Desa Tersedia*Proporsi Alokasi Efektif {cat}, {keb}))")
OV = {
 "Alokasi Dana Perlindungan": (flex("Perlindungan","Porsi Dana Fleksibel Patroli","Kebutuhan Dana Perlindungan"), "EKSPERIMEN ALOKASI: dana fleksibel bila switch=1"),
 "Alokasi Dana Rehabilitasi": (flex("Rehabilitasi","Porsi Dana Fleksibel Rehabilitasi","Kebutuhan Dana Rehabilitasi"), "EKSPERIMEN ALOKASI"),
 "Alokasi Dana Pengendalian Kebakaran": (flex("Pengendalian Kebakaran","Porsi Dana Fleksibel Pengendalian Kebakaran","Kebutuhan Dana Pengendalian Kebakaran"), "EKSPERIMEN ALOKASI"),
 "Alokasi Dana Pengembangan KUPS": (flex("Pengembangan KUPS","Porsi Dana Fleksibel Pengembangan KUPS","Kebutuhan Dana Pengembangan KUPS"), "EKSPERIMEN ALOKASI"),
 "Total Alokasi Dana Program": ("Alokasi Dana Operasional LPHD+Alokasi Dana Perlindungan+Alokasi Dana Pengendalian Kebakaran +Alokasi Dana Rehabilitasi+Alokasi Dana Penguatan Kelembagaan+Alokasi Dana Pengembangan KUPS+Alokasi Dana Kompensasi RT Terdampak", "EKSPERIMEN ALOKASI: termasuk kompensasi"),
 "Alokasi Tidak Terealisasi": ("Total Alokasi Dana Program-Penggunaan Dana Pengelolaan-Realisasi Kompensasi RT Terdampak", "EKSPERIMEN ALOKASI"),
 "Pendapatan Bersih per RT Bergantung": ("Pendapatan Hutan per RT Bergantung+Pendapatan Non Hutan per RT Bergantung+Pendapatan Program per RT Bergantung -Kehilangan Pendapatan Pembatasan Akses per RT+Kompensasi Rata rata per RT Bergantung", "EKSPERIMEN ALOKASI: + kompensasi rata-rata"),
 "Penggunaan Dana Desa": ("Penggunaan Dana Pengelolaan+Realisasi Kompensasi RT Terdampak", "EKSPERIMEN ALOKASI: kompensasi RT terdampak mengurangi saldo dana LPHD"),
}
