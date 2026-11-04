import json, pandas as pd, sys
PR = pd.read_pickle("fase5/mc_prcc.pkl"); P20 = PR[PR["Harga"] == 20].pivot_table(index="Parameter", columns="Indikator", values="PRCC")
SRC = json.load(open("fase7/param_sumber.json"))
def prcc(name):
    if name not in P20.index: return "tidak disampel MC"
    r = P20.loc[name]; f = lambda x: f"{x:+.2f}".replace(".", ",")
    return f"PRCC USD20: deforestasi dihindari {f(r['Deforestasi dihindari S2−S1 (ha)'])}; NPV mitra {f(r['NPV mitra inkremental [SEMENTARA] (Rp)'])}; Δ pendapatan RT terdampak {f(r['Δ pendapatan per RT terdampak (Rp/th)'])}"
K = "k (Tingkat Keberlanjutan Patroli Reguler)"
R = [
 # prioritas 1–10
 (1, "Upah Harian Patroli Berbayar", "150.000", "Rp/HOK", "2024–2025", "Konfirmasi peneliti 2026-11-03 (pelaksana)", "Observasi/konfirmasi langsung; 1 HOK = 1 orang × 1 hari", "A", "Tidak memengaruhi kas/NPV (komponen biaya total); memengaruhi upah tunai dan pendapatan program", "Bukti pembayaran 2024–2025 (daftar hadir/kuitansi) untuk menegaskan seluruh 5.544 HOK dibayar tunai"),
 (2, "Biaya per Hari Patroli", "260.000", "Rp/HOK", "2020 (nominal sumber)", "Cuplikan Perbup Kotawaringin Barat 29/2020 (bukan Kubu Raya); pembanding rencana anggaran WAS Rp966,84 juta/th (File 4)", "Upah + logistik; dengan upah 150.000 komponen non-upah implisit 110.000. Komentar model masih menyebut upah 130.000 (inkonsistensi dokumentasi, persamaan benar)", "D", prcc("Biaya per Hari Patroli (Rp/HOK)") + "; D0–D3: porsi jembatan USD20 8 % (150.000) vs 75 % (300.000)", "Realisasi biaya patroli mitra 2024–2025 per komponen (BBM, konsumsi, alat, transport)"),
 (3, "HOK Patroli Pembiayaan Awal Aktual 2024 / 2025", "2.533 / 3.011", "HOK/th", "2024 / 2025", "Rekap final patroli peneliti (20 HD / 25 HD)", "Jumlah keikutsertaan anggota; 1 keikutsertaan = 1 HOK", "A", "Menentukan kondisi awal, roster 254, dan J1", "–"),
 (3, "Keikutsertaan Patroli 2023", "2.160", "HOK/th", "2023", "392 kegiatan × 5,51 orang/kegiatan (MR1 2024)", "Diturunkan: jumlah kegiatan × rerata peserta; hanya kondisi awal respons", "B", "Kecil (kondisi awal SMOOTHI)", "Daftar peserta 2023"),
 (4, "Realisasi pembiayaan mitra 2024–2025 (Status Pembiayaan Awal = 0, hibah)", "Rp1.441.440.000 (= 5.544 × 260.000)", "Rp", "2024–2025", "HOK = A; biaya per HOK = D; status hibah = D", "Diturunkan HOK × biaya per HOK", "B (HOK) / D (Rp, status)", "Sama di S1 dan S2; tidak memengaruhi S2 − S1", "Bukti pengeluaran mitra 2023–2025; status hibah/talangan; apakah bagian proyek karbon (prior consideration)"),
 (5, "Besaran Pembiayaan Jembatan per Tahun / Durasi", "782.860.000 / 5", "Rp/th / th", "2026–2030 (proyeksi)", "Eksperimen: J1 = 3.011 HOK × 260.000 (meniru tingkat 2025)", "Asumsi eksperimen, bukan komitmen", "D", prcc("Besaran Pembiayaan Jembatan per Tahun (Rp)") + "; D1−D0 = 287 ha (J1), 620 ha (JP)", "Komitmen/kontrak mitra (besaran, durasi, status hibah/talangan, prioritas pemulihan)"),
 (6, "Biaya Monitoring per Ha per Tahun", "1.980", "Rp/(ha·th)", "c. 2010 (USD 0,12/ha)", "Rendon Thompson dkk. 2013 (Peru)", "Literatur dikonversi kurs", "C", prcc("Pengali biaya MRV"), "Anggaran MRV proyek Delta Kapuas (PDD/kontrak VVB)"),
 (6, "Biaya Verifikasi per Kejadian", "742.500.000", "Rp/kejadian", "2019–2026", "WCS/Landscapes and Livelihoods 2024; Beers dkk. 2019; Verra Fee Schedule v1.2", "USD 45.000 × 16.500", "C", "bersama biaya monitoring (pengali MRV)", "Penawaran VVB aktual"),
 (6, "Biaya Penerbitan per Kredit", "0,25", "USD/tCO2e", "2026", "Verra Program Fee Schedule v1.2", "Dokumen resmi", "C (dokumen resmi standar)", "kecil", "–"),
 (6, "Proporsi Pajak dan Pungutan Karbon", "0,05", "–", "2024–2026", "PP 36/2024; Permenhut 6/2026 Ps. 46", "Dokumen resmi", "C (dokumen resmi)", "sedang (5 % kas)", "Perlakuan PPN unit karbon"),
 (6, "Biaya Pengembangan Proyek", "0", "Rp/th", "–", "Tidak ada data", "Default 0", "D", "NPV SEMENTARA (batas atas)", "Biaya pengembangan PDD, validasi, registrasi aktual"),
 (7, "Masyarakat Bergantung pada Hutan Awal", "5.328", "orang (= RT)", "2024", "PROKSI: 4.104 (20 HD, File A) × pekerja SDA 25 HD/20 HD (24.099/18.563)", "Diturunkan dengan penskalaan; 1 pekerja SDA = 1 RT", "D (komentar model: kelas bukti D)", "Menentukan kehilangan agregat dan RT bergantung; tidak disampel MC", "Sensus/daftar RT bergantung hutan per HD"),
 (8, "RT Pemegang Garapan dalam HD", "2.144", "RT (individu)", "2024", "File A sheet Ang Kerja (Andil Garapan): pemegang SHM/SKT/turun-temurun di 15 desa, 4.322 ha", "Observasi catatan; individu diperlakukan setara RT", "A (catatan) / D (individu = RT)", "Kehilangan per RT terdampak berbanding terbalik", "Verifikasi RT unik per catatan"),
 (8, "Faktor Keunikan Catatan Garapan", "1", "–", "–", "Tidak tersedia", "Batas atas", "D", "×2 kehilangan per RT terdampak bila 0,5", "Pencocokan nama/NIK pemegang garapan"),
 (8, "Laju Pertumbuhan Penduduk (diterapkan juga ke RT terdampak)", "0,0166", "/th", "–", "File A sheet All/Vensim_Clean", "Laju bersih", "B (laju penduduk) / D (penerapan ke pemegang garapan)", "RT terdampak 2.144 → 3.003 (rerata 2030–2055)", "Apakah jumlah pemegang garapan tumbuh"),
 (9, "Pengali Kehilangan Akses", "1", "–", "–", "Angelsen dkk. 2014 (rentang PEN, C); porsi pemicu = asumsi D", "Skala relatif V5.2", "D", prcc("Pengali Kehilangan Akses") + "; impas USD20: RT bergantung 0,75, RT terdampak 0,30", "Survei kehilangan pendapatan akibat pembatasan akses (pemegang garapan)"),
 (9, "Proporsi Pendapatan Hutan dari Aktivitas Pemicu Deforestasi", "0,25", "–", "–", "Asumsi peneliti", "–", "D", "Setara pengali akses", "Idem"),
 (9, "Proporsi Pendapatan dari Hutan", "0,201", "–", "–", "Angelsen dkk. 2014 (PEN Asia; rentang 5,5–32,6 %)", "Literatur", "C", "Menentukan pendapatan hutan dan kehilangan", "Data pendapatan lokal"),
 (9, "Pendapatan Dasar RT Bergantung", "41.760.000", "Rp/RT/th", "c. 2021", "Setiawan dkk. 2021, Tabel 4 (70 responden anggota LPHD)", "Rerata TR − TC per responden", "C", "Skala pendapatan", "Survei terbaru 25 HD"),
 (10, "Biaya Reaktivasi KUPS (= Biaya Pembentukan KUPS)", "50.000.000", "Rp/unit", "–", "Asumsi: 2 × biaya pendampingan tahunan", "–", "D", prcc("Biaya Reaktivasi KUPS (Rp)") + "; PRCC KUPS 2087 −0,82", "Biaya nyata pembentukan/reaktivasi KUPS"),
 (10, "Porsi Laba Ditahan untuk Reinvestasi", "0,5", "–", "–", "Asumsi", "–", "D", prcc("Porsi Laba Ditahan untuk Reinvestasi") + "; PRCC KUPS 2087 +0,69", "Data keuangan KUPS 2024–2025"),
 (10, "Surplus Operasional per KUPS Produktif", "6.647.300", "Rp/unit/th", "Okt 2026 (disetahunkan)", "Lembar Status KUPS 25 Desa Minggu IV Okt 2026 (33 unit; 14 menjual)", "Median penjualan − OPEX tercatat; tanpa penyusutan; OPEX in-kind tidak tercatat (cenderung terlalu tinggi)", "B", prcc("Pengali surplus KUPS"), "Pencatatan OPEX in-kind"),
 (10, "Porsi Surplus KUPS Dibagikan ke Anggota", "0,263", "–", "2026", "Audit 3 unit bagi hasil", "Diturunkan; bersifat kotor", "B", "Penerimaan anggota", "Data bagi hasil semua unit"),
 # parameter lain yang menentukan hasil
 (None, "Tingkat Keberlanjutan Patroli Reguler (k)", "0,5", "–", "pasca-2025", "Nilai tengah eksploratif", "–", "D", prcc(K), "Data patroli pasca-2025 tanpa pembiayaan"),
 (None, "Efektivitas Perlindungan Penuh terhadap Deforestasi", "0,37", "–", "–", "Literatur pengelolaan hutan komunitas (Nepal); dosis-respons linear = asumsi struktural", "Literatur + asumsi struktural", "C / D (bentuk)", prcc("Efektivitas Perlindungan Penuh terhadap Deforestasi") + "; porsi jembatan USD20 100 % (0,2) vs 10 % (0,6)", "Bukti lokal hubungan intensitas patroli–deforestasi"),
 (None, "Laju deforestasi BAU (mis. Laju HRS menjadi NonHutan BAU)", "0,00956 (HRS)", "/th", "2001–2024", "Kalibrasi HCV + Hansen GFC; validasi tertahan 2017–2024 rasio 0,98", "Kalibrasi dari data", "B", prcc("Pengali laju deforestasi BAU"), "–"),
 (None, "Proporsi Kredit REDD dalam Project Area", "0,682", "–", "2001–2024", "Pangsa loss bruto Hansen di Project Area (DKP-GIS-MASTER v1.0)", "Proksi GIS provisional", "B (provisional)", prcc("Proporsi Kredit REDD dalam Project Area"), "Ketentuan metodologi/PDD"),
 (None, "Proporsi Buffer Risiko Karbon", "0,12", "–", "PDD", "PDD Delta Kapuas hal. 331 (NPR 12 %)", "Ex-ante, belum divalidasi Verra", "B", prcc("Proporsi Buffer Risiko Karbon"), "Validasi Verra"),
 (None, "Proporsi Leakage Karbon", "0,10", "–", "–", "Filewod & McCarney 2023; Haya dkk. 2023 (median VM0007 ±11 %)", "Literatur", "C", prcc("Proporsi Leakage Karbon"), "Nilai PDD"),
 (None, "Harga Karbon", "6 (dasar), uji 10/20/35", "USD/tCO2e", "2024", "Ecosystem Marketplace 2025 (rerata REDD+ 2024: 6,03)", "Literatur; level uji adalah skenario", "C", "Penentu kelayakan siklus", "Harga kontrak/ERPA"),
 (None, "Nilai Tukar USD ke Rupiah", "16.500", "Rp/USD", "2024–2025", "Bank Indonesia SEKI Tabel V.40", "Data resmi", "A", "Linear terhadap kas", "–"),
 (None, "Delay Verifikasi dan Penerbitan Kredit", "3", "th", "–", "Liu & Gurrola-Perez 2025 (rerata 2,76 th)", "Literatur", "C", prcc("Delay Verifikasi dan Penerbitan Kredit (th)"), "Jadwal verifikasi proyek"),
 (None, "Proporsi Manfaat Masyarakat (60/40)", "0,6", "–", "–", "Instruksi peneliti", "Ketentuan desain", "D (belum terverifikasi kontrak)", "Pembagian LPHD/mitra", "Perjanjian bagi hasil"),
 (None, "Porsi Upah sebagai Tambahan Bersih", "0,5", "–", "–", "Asumsi", "Biaya peluang tenaga kerja", "D", "Pendapatan program RT", "Data alokasi waktu kerja"),
 (None, "Upah Harian Pengendalian Kebakaran", "130.000", "Rp/HOK", "2020", "Cuplikan Perbup Kobar 29/2020", "–", "D (belum dikonfirmasi untuk lokasi)", "Upah kegiatan kebakaran", "Konfirmasi upah MPA lokal"),
 (None, "Tingkat Diskonto", "0,10", "/th", "–", "Tidak bersumber", "–", "D", "NPV SEMENTARA", "Pilihan diskonto beralasan"),
 (None, "Anggota Patroli Roster 2025", "254", "orang", "2025", "MR1 roster 2025", "Data", "A/B", "Kapasitas patroli", "–"),
 (None, "Indeks Kapasitas LPHD Awal", "0,5", "–", "–", "Asumsi peneliti", "–", "D", prcc("Indeks Kapasitas LPHD Awal"), "Penilaian kapasitas LPHD"),
 (None, "Hari Logistik Swadaya per Anggota", "9,17", "HOK/orang/th", "2023", "Log 2023", "Diturunkan", "C (komentar model)", "Hanya nilai non-tunai", "–"),
]
cols = ["Prioritas", "Nama variabel Vensim", "Nilai dasar", "Satuan", "Tahun referensi", "Sumber", "Metode", "Kelas data (A/B/C/D)", "Sensitivitas hasil", "Kebutuhan verifikasi"]
df = pd.DataFrame(R, columns=cols)
df["Komentar sumber di model (kutipan)"] = [next((v[:400] for k, v in SRC.items() if k in r[1]), "") for r in R]
W = pd.ExcelWriter(sys.argv[1], engine="openpyxl")
pd.DataFrame({"Isi": ["REGISTER PARAMETER DAN BUKTI EMPIRIS – Fase 5, 2026-11-04. Model dibekukan: MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl.",
 "Kelas: A = data empiris langsung (dokumen/observasi lapangan); B = diturunkan dari data empiris dengan rumus/asumsi yang dinyatakan; C = literatur atau dokumen resmi; D = asumsi eksploratif.",
 "Sumber diambil dari komentar parameter di berkas model dan dari konfirmasi peneliti yang tercatat; tidak ada sumber baru yang ditambahkan. Bila komentar model menyebut kelas berbeda, keduanya ditulis.",
 "Sensitivitas: PRCC Monte Carlo berpasangan USD 20 (N = 400) bila parameter disampel; selain itu hasil uji terarah Fase 4/Fase 5.",
 "Catatan: komentar parameter 'Biaya per Hari Patroli' di model masih menyebut upah Rp130.000; persamaan model memakai Rp150.000 di variabel upah. Inkonsistensi dokumentasi, bukan persamaan; model tidak diubah (dibekukan)."]}).to_excel(W, sheet_name="0 README", index=False)
df.to_excel(W, sheet_name="1 Register", index=False)
cnt = df["Kelas data (A/B/C/D)"].str[0].value_counts().rename_axis("Kelas utama").reset_index(name="Jumlah parameter"); cnt.to_excel(W, sheet_name="2 Ringkasan kelas", index=False)
W.close(); df.to_pickle("fase7/register.pkl"); print(cnt.to_string())
