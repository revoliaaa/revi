"""Definisi perubahan persamaan: FINAL A1 (4 skenario) -> FINAL 3 SKENARIO (patroli pembiayaan awal aktual)."""
TAG = "REV-3S 2026-11-03"
OVERRIDES = {
 "Skenario Kebijakan": ("3", f"{TAG}: 1 = S1 tanpa PS aktif; 2 = S2 PS + pembiayaan awal; 3 = S3 PS + pembiayaan awal + perdagangan karbon. Kode 4 tidak dipakai lagi. Desain."),
 "Switch Pendanaan Awal": ("IF THEN ELSE(Skenario Kebijakan>=2, 1, 0)", f"{TAG}: pembiayaan awal kini bagian dari S2 dan S3 (sebelumnya hanya S3/S4: Skenario Kebijakan>=3)."),
 "Switch Karbon": ("IF THEN ELSE(Skenario Kebijakan=3, STEP(1,Tahun Mulai Karbon), 0)", f"{TAG}: perdagangan karbon hanya pada S3 (sebelumnya Skenario Kebijakan=4)."),
 "Hari Patroli Pembiayaan Awal": (
    "Switch Pendanaan Awal*(HOK Patroli Pembiayaan Awal Aktual 2024*(STEP(1, Tahun Awal Pembiayaan Awal)-STEP(1, Tahun Awal Pembiayaan Awal+1))"
    "+HOK Patroli Pembiayaan Awal Aktual 2025*(STEP(1, Tahun Akhir Pembiayaan Awal)-STEP(1, Tahun Akhir Pembiayaan Awal+1)))",
    f"{TAG}: patroli aktual yang didukung pembiayaan awal proyek karbon, langsung dari rekap final peneliti (2024 = 2.533 HOK, 20 HD; 2025 = 3.011 HOK, 25 HD). Satu keikutsertaan anggota = satu HOK. Tidak diekstrapolasi, tidak dibatasi kapasitas, dan tidak berulang setelah 2025. Ini SATU-SATUNYA jalur patroli 2024-2025 sehingga tidak dihitung ganda dengan patroli swadaya."),
 "Hari Patroli Swadaya": (
    "Switch PS*Switch Patroli Swadaya Reguler*(1-Periode Pembiayaan Awal)*MIN(Anggota Patroli Aktif, Anggota Patroli Awal)*Hari Patroli Swadaya per Anggota",
    f"{TAG}: patroli swadaya reguler TIDAK aktif (Switch Patroli Swadaya Reguler = 0). Nilai lama 2.355 HOK/th tidak dipakai. Faktor (1-Periode Pembiayaan Awal) mencegah penghitungan ganda dengan patroli aktual 2024-2025 bila switch kelak diaktifkan dengan data terpisah."),
 "Penggunaan Dana Perlindungan Total": ("Realisasi Belanja Perlindungan+Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal",
    f"{TAG}: menambahkan belanja patroli pembiayaan awal agar total belanja perlindungan lengkap (variabel pelaporan)."),
 "Besaran Pendanaan Awal Proyek Karbon": ("0", f"{TAG}: jalur pendanaan awal generik DINONAKTIFKAN tetap 0. Pembiayaan awal hanya lewat Hari Patroli Pembiayaan Awal agar kegiatan yang sama tidak masuk dua komponen pembiayaan."),
 "Total Pembiayaan Tambahan S3": ("Pendanaan Awal untuk Patroli+Penggunaan Dana Pengelolaan+Realisasi Pembiayaan Awal",
    f"{TAG}: nama variabel dipertahankan; isinya total pembiayaan tambahan (pembiayaan awal + belanja dana LPHD) untuk S2/S3 struktur baru."),
}
NEW = [  # name, view, kind, eq, unit, comment
 ("HOK Patroli Pembiayaan Awal Aktual 2024", "04 Forest Patrol Protection", "Konstanta", "2533", "HOK/Year",
  f"{TAG}: total keikutsertaan anggota patroli 2024 (20 HD) = 2.533; 1 keikutsertaan = 1 HOK. Sumber: rekap final patroli peneliti. Kelas A (data final peneliti)."),
 ("HOK Patroli Pembiayaan Awal Aktual 2025", "04 Forest Patrol Protection", "Konstanta", "3011", "HOK/Year",
  f"{TAG}: total keikutsertaan anggota patroli 2025 (25 HD) = 3.011; 1 keikutsertaan = 1 HOK. Sumber: rekap final patroli peneliti. Kelas A (data final peneliti)."),
 ("Switch Patroli Swadaya Reguler", "16 Scenario Controls", "Switch/kontrol skenario", "0", "Dmnl [0,1]",
  f"{TAG}: 0 = tidak ada patroli swadaya reguler di luar pembiayaan awal (dasar data terpisah belum tersedia). Hanya boleh 1 bila ada data patroli swadaya yang terpisah dari rekap pembiayaan awal. Desain."),
 ("Periode Pembiayaan Awal", "04 Forest Patrol Protection", "Auxiliary (dihitung)",
  "STEP(1, Tahun Awal Pembiayaan Awal)-STEP(1, Tahun Akhir Pembiayaan Awal+1)", "Dmnl",
  f"{TAG}: 1 selama 2024-2025 (periode yang didukung pembiayaan awal), 0 di luar periode itu."),
]
REMOVE = ["Kegiatan Patroli Tercatat 2024", "Kegiatan Patroli Swadaya Tahunan 2023", "Orang Hari per Kegiatan Patroli",
          "Porsi Kenaikan Patroli 2024 dari Pembiayaan Awal", "Hari Patroli Tambahan Tercatat 2024"]
