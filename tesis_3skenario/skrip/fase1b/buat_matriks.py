import re, sys, json
sys.path.insert(0, "fase1b"); from usulan import P
txt = open("out/DKP_25HD_FINAL_3SKENARIO.mdl", encoding="utf-8").read().split("\\\\\\---///")[0]
base = {}
for blk in txt.split("|\n"):
    m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
    if m: base[m.group(1).strip()] = (re.sub(r"\s+", " ", m.group(3).strip()), m.group(4).strip())
ST = json.load(open("fase1b/cek_statis.json"))
G = {  # kode: (judul, status, pengaruh S1/S2, circular, double counting, uji)
 "S-1": ("Kode skenario", "SETUJU", "Menentukan S1/S2", "Tidak ada", "Tidak ada", "U1"),
 "S-2": ("PS aktif di kedua skenario", "SETUJU", "S1 tidak lagi tanpa PS; semua kegiatan PS aktif", "Tidak ada", "Tidak ada", "U1, U2"),
 "S-3": ("Rehabilitasi aktif di kedua skenario", "SETUJU", "idem", "Tidak ada", "Tidak ada", "U2"),
 "S-4": ("Pembiayaan awal historis di kedua skenario", "SETUJU", "Patroli 2024–2025 = 2.533/3.011 HOK di S1 dan S2", "Tidak ada", "Tidak ada: hanya satu jalur patroli 2024–2025", "U3"),
 "S-5": ("Switch Karbon hanya pada rantai kredit/MRV", "SETUJU", "Satu-satunya pembeda S1–S2", "Tidak ada", "Tidak ada", "U1, U4"),
 "K1": ("Patroli reguler pasca-2025", "SETUJU STRUKTUR; NILAI k PERLU SENSITIVITAS", "S1 dan S2 identik: 254 × 11,85 × k HOK/th mulai 2026", "Tidak: memakai stok Anggota Patroli Aktif", "Dicegah: (1−Periode Pembiayaan Awal) dan STEP 2026; basis anggota dibatasi roster 2025 sehingga anggota rekrutan dana karbon tidak menambah patroli sukarela", "U3, U5, U6"),
 "K2": ("Penggantian dan rekrutmen anggota", "SETUJU", "Penggantian 1 (A1) → anggota S1 tetap 254; rekrutmen tambahan hanya bila ada alokasi kas perlindungan", "Tidak: Alokasi ← Kebutuhan ← HOK reguler ← stok", "Pengurangan ganda dihindari: penurunan partisipasi hanya lewat satu tuas (k dan laju penurunan), bukan juga lewat penyusutan anggota", "U5"),
 "K3": ("Patroli didanai, kebutuhan, intensitas, kesenjangan", "SETUJU", "S1: patroli didanai kas hanya bila ada kas non-karbon; S2: tambahan dari kas karbon", "Tidak", "Dicegah: kebutuhan patroli dikurangi HOK reguler dan historis; kesenjangan tidak lagi dikurangi Realisasi Pembiayaan Awal (dua kali)", "U3, U7"),
 "K4": ("Alokasi belanja LPHD tanpa Switch Karbon", "SETUJU", "Belanja dibatasi saldo; S1 = 0 bila tidak ada kas non-karbon", "Tidak: Dana Desa Tersedia = stok/waktu", "Tidak ada", "U7, U8"),
 "K5": ("Kas masuk LPHD karbon dan non-karbon", "SETUJU STRUKTUR; NILAI KAS NON-KARBON PERLU DATA", "Kas non-karbon sama di S1 dan S2 (default 0)", "Tidak: porsi dihitung dari stok", "Dicegah: dua aliran terpisah, satu stok saldo + satu stok pelacak", "U7, U8"),
 "K6": ("Kapasitas LPHD dari semua sumber", "SETUJU STRUKTUR; NILAI PERLU DATA/SENSITIVITAS", "Default (0/0): kapasitas tetap 0,5 di S1; S2 naik bila belanja kelembagaan dari kas karbon", "Tidak: target → stok", "Belanja dan pendampingan non-tunai dijumlahkan; keduanya harus dari sumber berbeda", "U9"),
 "K7": ("KUPS: modal usaha dari laba ditahan", "SETUJU STRUKTUR; PARAMETER PERLU SENSITIVITAS", "S1: penggantian KUPS dibatasi modal dari laba ditahan; S2: + pembentukan dari kas", "Tidak: modal adalah stok", "Laba ditahan = surplus − bagian anggota, tidak dihitung dua kali dengan pendapatan anggota", "U10"),
 "K8": ("Kegiatan didanai kas LPHD tanpa Switch Karbon", "SETUJU", "Sama dengan K4", "Tidak", "Tidak ada", "U7"),
 "K9": ("Rehabilitasi: tenaga dan material dipisah", "SETUJU STRUKTUR; DUKUNGAN MATERIAL NON-KARBON PERLU DATA", "S1: penanaman non-karbon ≤ realisasi historis dan ≤ dukungan material; default 0 → penanaman hanya dari kas", "Tidak", "HOK tanam dipisah: didanai kas vs non-karbon; upah non-karbon hanya bila ada pembayar", "U11"),
 "K10": ("Biaya kegiatan non-karbon sebagai indikator", "SETUJU", "Pelaporan saja", "Tidak", "Tidak masuk kas atau NPV", "U12"),
 "K11": ("Kontribusi non-tunai", "SETUJU", "Pelaporan; tidak masuk pendapatan RT", "Tidak", "Tidak dijumlahkan dengan upah", "U12"),
 "K12": ("Kerja berupah vs sukarela", "SETUJU", "FTE berupah dan sukarela terpisah", "Tidak", "HOK historis 2024–2025 hanya di Hari Patroli Didanai", "U12"),
 "K13": ("Partisipasi aktif", "SETUJU", "Anggota pasif tidak dihitung", "Tidak", "Tidak ada", "U12"),
 "K14": ("Inisialisasi efek perlindungan dari 2023", "SETUJU BERSYARAT (estimasi 2.160 kelas B)", "Sama di S1 dan S2; 2024 tidak berubah karena Switch Dampak = 0 pada 2024", "Tidak: argumen awal SMOOTHI dievaluasi pada INITIAL TIME", "Tidak ada", "U13"),
 "K15": ("Acuan kondisi awal", "SETUJU", "Tidak berdampak selama sensitivitas tekanan = 0", "Tidak: INITIAL", "Tidak ada", "U13"),
 "K16": ("Atribusi upah karbon", "SETUJU", "S1: 0; S2: upah dari kas karbon saja", "Tidak", "Dicegah: upah patroli historis tidak lagi dihitung sebagai upah karbon", "U12"),
 "K17": ("Agregat manfaat dan FTE", "SETUJU", "Pelaporan", "Tidak", "Tidak ada", "U12"),
 "C1": ("Jeda pembayaran dan biaya berbasis kas", "SETUJU; NILAI JEDA PERLU SENSITIVITAS", "S2 saja", "Tidak: DELAY FIXED", "Biaya transaksi/pajak dihitung saat kas diterima, sekali", "U14"),
 "C2": ("Status pembiayaan awal dan pemulihan sebelum bagi hasil", "SETUJU; STATUS PERLU DATA", "S1: tidak ada pemulihan; S2: pulih dari surplus bila talangan", "Tidak", "Dicegah: pemulihan dari surplus sebelum 60/40, bukan dari bagian mitra sendiri", "U15"),
 "C3": ("Baseline konservatif REDD dan ARR", "SETUJU SEBAGAI SENSITIVITAS", "S2 saja", "Tidak: memakai status SMOOTHI dan stok", "Lihat AUDIT_AKUNTANSI_KARBON_NPV.md bagian 2", "U16"),
 "C4": ("NPV di dalam model", "SETUJU; DISKONTO DAN BIAYA PENGEMBANGAN PERLU DATA", "S1: NPV proyek = −PV pembiayaan awal; NPV inkremental = 0", "Tidak: INTEG", "Identitas: arus proyek = arus mitra + kas LPHD karbon", "U15"),
 "C5": ("Indikator karbon terpisah", "SETUJU", "Pelaporan", "Tidak", "Tidak ada", "U16"),
}
L = ["# Fase 1B: Matriks Persamaan Final (usulan, belum diterapkan)", "",
 "Dihasilkan dari `fase1b/usulan.py`, dan dibandingkan dengan persamaan yang berlaku di `DKP_25HD_FINAL_3SKENARIO.mdl`.",
 "**Belum ada berkas `.mdl` yang diubah dan belum ada simulasi.**", "",
 "**Pemeriksaan statis atas 723 persamaan model + persamaan usulan** (penelusuran teks persamaan, bukan simulasi):", "",
 f"- Referensi ke variabel yang tidak ada: **{'tidak ada' if not ST['unknown'] else ST['unknown']}**.",
 f"- Loop aljabar: **{'tidak ada' if not ST['scc'] else ST['scc']}**. Semua umpan balik melewati stok (INTEG) atau fungsi berstatus (SMOOTHI, DELAY FIXED, INITIAL).",
 f"- Pemakai `Switch Karbon` setelah usulan: {', '.join('`'+x+'`' for x in ST['switch_karbon'])}. `Pendanaan Awal Proyek Karbon` tetap 0 karena besarannya 0.", "",
 "Status per kelompok: **SETUJU** = konsisten secara struktur dan dapat disetujui; **PERLU DATA** = struktur siap, nilai menunggu data; **SENSITIVITAS** = hanya dapat dibenarkan sebagai rentang uji.", ""]
order = ["S-1","S-2","S-3","S-4","S-5","K1","K2","K3","K4","K5","K6","K7","K8","K9","K10","K11","K12","K13","K14","K15","K16","K17","C1","C2","C3","C4","C5"]
for k in order:
    t, st, eff, cyc, dbl, uji = G[k]
    L += [f"## {k}. {t}", "", f"**Status:** {st}  ", f"**Pengaruh S1/S2:** {eff}  ", f"**Circular dependency:** {cyc}  ", f"**Risiko double counting:** {dbl}  ", f"**Uji:** {uji} (lihat RENCANA_UJI_FASE2.md)", "",
          "| Variabel | Persamaan lama | Persamaan usulan final | Satuan | Sumber / kelas |", "|---|---|---|---|---|"]
    for n, (eq, u, kk, s) in P.items():
        if kk != k: continue
        old = base.get(n, ("— (variabel baru)", ""))[0]
        L.append(f"| `{n}` | `{old}` | `{eq}` | {u} | {s or '–'} |".replace("\n", " "))
    L.append("")
L += ["## Catatan sintaks Vensim dan PySD", "",
 "- **`STEP(h, t)`.** Naik pada `Time >= t`. Dengan DT 0,0625 dan tahun bulat, `STEP(1,2026)` aktif tepat pada awal 2026. Fungsi ini sudah dipakai A1 dan hasil 2024–2025 terverifikasi.",
 "- **`INITIAL(x)`.** Dievaluasi sekali pada 2024, dan didukung PySD. Dipakai untuk `INITIAL(Kebutuhan Hari Patroli)` dan acuan K15.",
 "- **`SMOOTHI(input, delay, init)`.** Argumen `init` (`Respons Perlindungan Awal`) hanya bergantung pada konstanta dan `INITIAL`, sehingga aman pada t0.",
 "- **`DELAY FIXED(input, delay, init)`.**",
 "  - Waktu tunda dibaca sekali pada t0. Nilai 0,5, 1, 3, 4, dan 5 tahun adalah kelipatan DT 0,0625.",
 "  - Tunda 0 dibungkus `IF THEN ELSE`, karena DELAY FIXED dengan tunda 0 tidak didefinisikan dengan aman.",
 "  - Di PySD, cabang `IF` yang tidak terpilih tetap membuat objek delay. Ini tidak masalah selama parameternya ≥ 0.",
 "- **`ZIDZ(a, b)`.** Dipakai untuk semua pembagian yang penyebutnya dapat 0 (saldo 0 di S1, penanaman 0, HOK 0).",
 "- **`MIN` dan `MAX`.** Tidak ada `MIN` yang memotong aliran stok sehingga stok negatif:",
 "  - `Penggantian KUPS Berbasis Modal` dibatasi `Modal/TIME STEP`, sehingga modal ≥ 0;",
 "  - `Pemulihan Pendanaan Awal` dibatasi sisa talangan/TIME STEP.",
 "- **`EXP(−laju × Δt)`.** Bila laju = 0, nilainya 1. Laju bersatuan 1/Year dan Δt bersatuan Year, sehingga hasilnya Dmnl.",
 "- **`Faktor Diskonto`.** Ditulis dengan `Satu Tahun` (variabel A1) agar satuannya konsisten di Vensim *Units Check*.",
 "- **Nama variabel.** `Hari Patroli Swadaya`, `HOK Patroli`, `Faktor Penguatan Kelembagaan dari Karbon`, `Pembentukan KUPS Didanai Karbon`, dan `Penanaman Didanai Karbon` **dipertahankan** agar 16 View, sketch, dan register tetap utuh. Arti barunya ditulis di komentar Vensim. Mengganti nama akan memutus panah di diagram Vensim asli.", ""]
open("/home/user/revi/tesis_3skenario/laporan/fase1b/FASE1B_MATRIKS_PERSAMAAN_FINAL.md", "w").write("\n".join(L))
print(len(P), "persamaan usulan")
