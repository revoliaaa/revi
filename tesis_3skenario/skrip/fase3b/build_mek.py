"""Varian mekanisme pembiayaan: DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl.
Sama persis dengan model 2 skenario + struktur pembiayaan jembatan (mekanisme C) yang default-nya NONAKTIF.
Dengan Switch Pembiayaan Jembatan Karbon = 0 model harus mereproduksi model 2 skenario persis."""
import sys
src = open("fase2/build_2s.py", encoding="utf-8").read()
MEK = r'''
TAG2 = "REV-2S-MEK 2026-11-03"
MEK = {
 "Switch Pembiayaan Jembatan Karbon": ("0", "Dmnl", "M1", "Mekanisme C: 1 = mitra menyalurkan pembiayaan jembatan (talangan eksplisit) untuk patroli TAMBAHAN di atas patroli reguler S1 sebelum penerimaan kredit pertama. Eksperimen akuntansi/pembiayaan, BUKAN aturan kontraktual yang disetujui"),
 "Besaran Pembiayaan Jembatan per Tahun": ("0", "Rupiah/Year", "M1", "Plafon tahunan pembiayaan jembatan. Nilai uji: Rp 782.860.000 (= 3.011 HOK x Rp 260.000, setara tingkat pembiayaan mitra 2025) dan plafon kebutuhan penuh. [PERLU DIISI] komitmen nyata mitra. Kelas D"),
 "Tahun Awal Pembiayaan Jembatan": ("2026", "Year", "M1", "Sesudah pembiayaan awal historis 2024-2025 berakhir"),
 "Durasi Pembiayaan Jembatan": ("5", "Year", "M1", "Durasi maksimum. Kelas D (uji 3/5/8)"),
 "Switch Henti Jembatan saat Kas Karbon Pertama": ("0", "Dmnl", "M1", "1 = jembatan berhenti ketika LPHD pertama kali menerima kas karbon (berbasis stok, tanpa loop aljabar)"),
 "Kumulatif Kas Masuk LPHD Karbon": ("INTEG(Kas Masuk LPHD Karbon, 0)", "Rupiah", "M1", "Stok penanda kas karbon pertama"),
 "Periode Pembiayaan Jembatan": ("(STEP(1, Tahun Awal Pembiayaan Jembatan)-STEP(1, Tahun Awal Pembiayaan Jembatan+Durasi Pembiayaan Jembatan))*IF THEN ELSE(Switch Henti Jembatan saat Kas Karbon Pertama=1 :AND: Kumulatif Kas Masuk LPHD Karbon>0, 0, 1)", "Dmnl", "M1", ""),
 "Hari Patroli Didanai Jembatan": ("Switch Karbon*Switch Pembiayaan Jembatan Karbon*Periode Pembiayaan Jembatan*MIN(Besaran Pembiayaan Jembatan per Tahun/Biaya per Hari Patroli, Hari Patroli Tambahan Dibutuhkan)", "HOK/Year", "M1", "Patroli tambahan (di atas reguler S1) yang dibiayai jembatan; dibatasi kebutuhan tambahan dan kapasitas anggota. Tidak masuk Indeks Intensitas Perlindungan Tanpa Karbon, sehingga dihitung sebagai mitigasi proyek pada kredit konservatif"),
 "Realisasi Pembiayaan Jembatan": ("Hari Patroli Didanai Jembatan*Biaya per Hari Patroli", "Rupiah/Year", "M1", "Arus keluar mitra; dicatat sebagai pokok talangan"),
 "Kumulatif Pembiayaan Jembatan": ("INTEG(Realisasi Pembiayaan Jembatan, 0)", "Rupiah", "M1", ""),
 "PV Pembiayaan Jembatan": ("INTEG(Realisasi Pembiayaan Jembatan*Faktor Diskonto, 0)", "Rupiah", "M1", "SEMENTARA (D3)"),
 "Hari Patroli Didanai": ("Hari Patroli Pembiayaan Awal+Hari Patroli Didanai Kas LPHD+Hari Patroli Didanai Jembatan", "HOK/Year", "M1", ""),
 "Total HOK Patroli": ("Hari Patroli Pembiayaan Awal+HOK Patroli Reguler PS+Hari Patroli Didanai Kas LPHD+Hari Patroli Didanai Jembatan", "HOK/Year", "M1", ""),
 "Kebutuhan Dana Perlindungan": ("MAX(0, Hari Patroli Tambahan Dibutuhkan-Hari Patroli Didanai Jembatan)*Biaya per Hari Patroli", "Rupiah/Year", "M1", "Kebutuhan yang sudah dibiayai jembatan tidak dibebankan ke LPHD"),
 "Pendanaan Awal Belum Terpulihkan": ("INTEG((Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal)*Status Pembiayaan Awal+Realisasi Pembiayaan Jembatan+Biaya Modal Pendanaan Awal Rp-Pemulihan Pendanaan Awal, 0)", "Rupiah", "M1", "Jembatan selalu talangan (dipulihkan); pembiayaan historis mengikuti Status Pembiayaan Awal"),
 "Pokok Talangan Kumulatif": ("INTEG((Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal)*Status Pembiayaan Awal+Realisasi Pembiayaan Jembatan, 0)", "Rupiah", "M1", ""),
 "Arus Kas Proyek Karbon": ("Kas Penjualan Kredit-Biaya Transaksi dan MRV-Biaya Pengembangan Proyek Efektif-Realisasi Pembiayaan Jembatan", "Rupiah/Year", "M1", "Jembatan adalah biaya proyek karbon (hanya S2)"),
 "Arus Kas Mitra": ("Dana Mitra dari Karbon+Pemulihan Defisit Biaya Bersama+Pemulihan Talangan Sebelum Bagi Hasil-Kekurangan Biaya Bersama Ditanggung Mitra-Realisasi Pembiayaan Awal-Biaya Pengembangan Proyek Efektif-Realisasi Pembiayaan Jembatan", "Rupiah/Year", "M1", ""),
 "Penggunaan Dana Perlindungan Total": ("Realisasi Belanja Perlindungan+Realisasi Pembiayaan Awal+Realisasi Pembiayaan Jembatan", "Rupiah/Year", "M1", ""),
}
VIEW["M1"] = "13 Carbon Finance Revenues"
for k, (eq, u, code, s) in MEK.items(): EXTRA[k] = (eq, u, code, s)
'''
src = src.replace("merged = dict(P)", MEK + "\nmerged = dict(P)")
src = src.replace('src[n][22] = f"{TAG} [{code}]', 'src[n][22] = f"{TAG2 if code==\'M1\' else TAG} [{code}]').replace('rr[22] = n, view, "Auxiliary (dihitung)", eq, u, f"{TAG} [{code}]', 'rr[22] = n, view, "Auxiliary (dihitung)", eq, u, f"{TAG2 if code==\'M1\' else TAG} [{code}]')
exec(compile(src, "build_2s+mek", "exec"))
