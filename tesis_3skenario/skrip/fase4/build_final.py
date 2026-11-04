"""MODEL_FINAL_DUA_SKENARIO_PWD.mdl = model 2 skenario + mekanisme jembatan (Fase 3) + koreksi final Fase 4:
 PWD-U  upah patroli Rp150.000/HOK; komponen non-upah diturunkan dari biaya total (asumsi kerja)
 PWD-K  kredit konservatif endogen terhadap rantai Referensi S1 (mode 2)
 PWD-M  aturan prospektif penghentian/penundaan MRV
 PWD-T  batas biaya modal, tenor, dan penghapusan talangan dengan pencatatan kerugian mitra"""
import sys, re
sys.path.insert(0, "."); from fase4_parse import parse
src_code = open("fase2/build_2s.py", encoding="utf-8").read()
mek_code = open("fase3b/build_mek.py", encoding="utf-8").read()
MEK = mek_code[mek_code.index("MEK = r'''") + 10: mek_code.index("'''\nsrc = src.replace")]
BASE = parse("fase3b/DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl")
EXCL = {"Indeks Perlindungan Baseline", "Luas Karhutla Baseline", "Emisi Deforestasi Dihindari terhadap Baseline"}
BL = sorted([k for k in BASE if k.endswith(" Baseline") and k not in EXCL], key=len, reverse=True)
FINAL = r'''
TAG3 = "REV-PWD 2026-11-03"
U = lambda n: src[n][6]
FIN = {
 # ---------- PWD-U upah dan biaya patroli
 "Upah Harian Patroli Berbayar": ("150000", "Rupiah/HOK", "PWD-U", "Upah patroli aktual Rp150.000 per orang per hari (1 HOK), dikonfirmasi peneliti 2026-11-03. Menggantikan Rp130.000. Kualitas A (konfirmasi pelaksana). Merupakan KOMPONEN dari Biaya per Hari Patroli, bukan tambahan biaya"),
 "Komponen Non Upah Biaya Patroli": ("MAX(0, Biaya per Hari Patroli-Upah Harian Patroli Berbayar)", "Rupiah/HOK", "PWD-U", "Turunan asumsi: biaya total kerja Rp260.000/HOK dikurangi upah. Rp110.000/HOK BUKAN biaya logistik aktual terverifikasi"),
 "Hari Logistik Swadaya per Anggota": ("9.17", "HOK/(People*Year)", "PWD-U", "Log 2023: 9,17 hari-orang/anggota/tahun (sebelumnya tertanam dalam Biaya Operasional Patroli Sukarela). Kualitas C"),
 "Biaya Operasional Patroli Sukarela per Anggota per Tahun": ("Hari Logistik Swadaya per Anggota*Komponen Non Upah Biaya Patroli", "Rupiah/(People*Year)", "PWD-U", "Nilai NON-TUNAI logistik patroli reguler, kini konsisten dengan dekomposisi biaya Rp260.000 = upah + non-upah (sebelumnya 9,17 x Rp130.000 = 1.192.050). Tidak masuk kas, NPV, atau pendapatan RT (D1)"),
 # ---------- PWD-K kredit konservatif endogen
 "Switch Baseline Kredit Konservatif": ("2", "Dmnl", "PWD-K", "0 = terhadap baseline BAU model (mekanisme A); 1 = pendekatan porsi lama (hanya untuk reproduksi Fase 3, TIDAK dipakai); 2 = terhadap rantai Referensi S1 endogen (mekanisme B/C, default)"),
 "Faktor Tekanan Deforestasi Referensi S1": ("Pengali Izin PS*(1-Efek Pengelolaan PS Tanpa Karbon)*(1-Efek Penghidupan terhadap Deforestasi )*(1-Efek Pengendalian Kebakaran terhadap Deforestasi)*Indeks Harga Komoditas^Elastisitas Deforestasi terhadap Harga Komoditas", "Dmnl", "PWD-K", "Seperti Faktor Tekanan Deforestasi, tetapi efek PS hanya dari kegiatan yang juga ada di S1 (patroli reguler, pembiayaan historis 2024-2025, kas non-karbon). Kanal penghidupan dan kebakaran memakai nilai aktual (tidak dikreditkan); pada parameter dasar keduanya 0"),
 "Aliran Penanaman ke Rehabilitasi Referensi S1": ("Penambahan Luas Penanaman*(1-Porsi ARR Adisional)", "Ha/Year", "PWD-K", "Penanaman yang tidak dibiayai kas karbon (terjadi juga di S1)"),
 "Faktor Ekspansi Kebun Referensi S1": ("Faktor Ekspansi Kebun", "Dmnl", "PWD-K", "Sama dengan aktual (tidak dikreditkan)"),
 "Faktor Gangguan Gambut Tersisa Referensi S1": ("Faktor Gangguan Gambut Tersisa", "Dmnl", "PWD-K", "Sama dengan aktual; gambut tidak dikreditkan"),
 "Emisi Kebakaran Gambut Referensi S1": ("Switch Emisi Kebakaran Gambut*Luas Karhutla Tahunan*Proporsi Karhutla di Lahan Gambut *Faktor Emisi Kebakaran Gambut", "tCO2e/Year", "PWD-K", "Sama dengan aktual"),
 "Rehabilitasi Menjadi Hutan Referensi S1": ("Areal Rehabilitasi Belum Berhutan Referensi S1*Tingkat Keberhasilan Rehabilitasi/Waktu Pembentukan Tutupan Hutan", "Ha/Year", "PWD-K", ""),
 "Kegagalan Rehabilitasi Referensi S1": ("Areal Rehabilitasi Belum Berhutan Referensi S1*(1-Tingkat Keberhasilan Rehabilitasi)/Waktu Pembentukan Tutupan Hutan", "Ha/Year", "PWD-K", ""),
 "Pengurangan Emisi Biomassa Referensi S1": ("Emisi Bersih Biomassa Referensi S1-Emisi Bersih Biomassa", "tCO2e/Year", "PWD-K", "Mitigasi biomassa bersih tambahan terhadap Referensi S1 (tahun berjalan)"),
 "Pengurangan Emisi REDD Bruto Referensi S1": ("MIN(Emisi Deforestasi Biomassa Referensi S1-Emisi Deforestasi Biomassa, Pengurangan Emisi Biomassa Referensi S1 )", "tCO2e/Year", "PWD-K", "BERTANDA: deforestasi dihindari terhadap S1 (negatif = reversal, yaitu S2 mendeforestasi lebih banyak daripada S1); tidak melebihi pengurangan bersih"),
 "Pengurangan Emisi ARR Bruto Referensi S1": ("Pengurangan Emisi Biomassa Referensi S1-Pengurangan Emisi REDD Bruto Referensi S1", "tCO2e/Year", "PWD-K", "Sisa pengurangan bersih (>= 0 menurut konstruksi); REDD + ARR = pengurangan bersih (tanpa hitung ganda)"),
 "Pengurangan Emisi Eligible REDD Referensi S1": ("Pengurangan Emisi REDD Bruto Referensi S1*(1-Proporsi Leakage Karbon)*(1-Proporsi Buffer Risiko Karbon )*Proporsi Kredit REDD dalam Project Area", "tCO2e/Year", "PWD-K", "Leakage, buffer, Project Area sama dengan aturan REDD"),
 "Pengurangan Emisi Eligible ARR Referensi S1": ("Pengurangan Emisi ARR Bruto Referensi S1*(1-Proporsi Leakage ARR)*(1-Proporsi Buffer Risiko Karbon )", "tCO2e/Year", "PWD-K", "ARR tidak dibatasi Project Area (penanaman di dalam PA)"),
 "Mitigasi REDD Eligible Bersih Proyek": ("Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif*Pengurangan Emisi Eligible REDD Referensi S1", "tCO2e/Year", "PWD-K", "Bertanda; reversal masuk sebagai negatif"),
 "Saldo Mitigasi REDD Belum Dikreditkan": ("INTEG(Mitigasi REDD Eligible Bersih Proyek-Kredit REDD Referensi S1 Bersih, 0)", "tCO2e", "PWD-K", "Negatif = debit reversal yang harus ditutup mitigasi berikutnya sebelum kredit baru diajukan"),
 "Kredit REDD Referensi S1 Bersih": ("MAX(0, Saldo Mitigasi REDD Belum Dikreditkan/TIME STEP+Mitigasi REDD Eligible Bersih Proyek)", "tCO2e/Year", "PWD-K", "Kredit hanya bila mitigasi bersih kumulatif positif; hanya informasi tahun berjalan dan lampau"),
 "Reversal Belum Terkompensasi": ("MAX(0, -Saldo Mitigasi REDD Belum Dikreditkan)", "tCO2e", "PWD-K", "Bandingkan dengan Kumulatif Buffer REDD"),
 "Kredit REDD Diajukan": ("Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif*Faktor Rekonsiliasi Reversal Kredit A2*IF THEN ELSE(Switch Baseline Kredit Konservatif=2, Kredit REDD Referensi S1 Bersih, Pengurangan Emisi Eligible REDD*(1-Switch Baseline Kredit Konservatif*(1-Porsi Mitigasi Adisional terhadap S2)))", "tCO2e/Year", "PWD-K", "Kredit endogen: membatasi penerbitan, penjualan, kas"),
 "Kredit ARR Diajukan": ("Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif*IF THEN ELSE(Switch Baseline Kredit Konservatif=2, Pengurangan Emisi Eligible ARR Referensi S1, Pengurangan Emisi Eligible ARR*(1-Switch Baseline Kredit Konservatif*(1-Porsi ARR Adisional)))", "tCO2e/Year", "PWD-K", ""),
 "Kredit Gambut Diajukan": ("Pengurangan Emisi Eligible Gambut*Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif", "tCO2e/Year", "PWD-K", "Switch Klaim Kredit Gambut = 0"),
 "Potensi Kredit REDD terhadap BAU": ("Pengurangan Emisi Eligible REDD*Switch Karbon*Switch Periode Kredit*Faktor Rekonsiliasi Reversal Kredit A2", "tCO2e/Year", "PWD-K", "PELAPORAN batas atas (mekanisme A) pada run mana pun; tidak memengaruhi kas"),
 "Potensi Kredit REDD Referensi S1": ("MAX(0, Pengurangan Emisi Eligible REDD Referensi S1)*Switch Karbon*Switch Periode Kredit*Faktor Rekonsiliasi Reversal Kredit A2", "tCO2e/Year", "PWD-K", "PELAPORAN pada run mana pun (termasuk A)"),
 "Check Referensi S1 Hutan": ("Total Hutan Referensi S1-Total Hutan", "Ha", "PWD-K", "Uji: = 0 pada S1 di semua t"),
 "Kebutuhan Dana Perlindungan": ("Hari Patroli Tambahan Dibutuhkan*Biaya per Hari Patroli", "Rupiah/Year", "PWD-C", "Dikembalikan ke kebutuhan bruto: LPHD tetap menargetkan kebutuhan penuh; jembatan hanya mengisi sisa (perbaikan K7, mencegah jembatan menggeser belanja non-karbon)"),
 "Hari Patroli Didanai Jembatan": ("Switch Karbon*Switch Pembiayaan Jembatan Karbon*Periode Pembiayaan Jembatan*MIN(Besaran Pembiayaan Jembatan per Tahun/Biaya per Hari Patroli, MAX(0, Hari Patroli Tambahan Dibutuhkan-Hari Patroli Didanai Kas LPHD))", "HOK/Year", "PWD-C", "Jembatan mengisi kekurangan sesudah patroli yang dibiayai kas LPHD (non-karbon maupun karbon); tidak ada pembiayaan ganda"),
 "Hari Patroli Dapat Didanai Kas Non Karbon": ("MIN(Hari Patroli Didanai Kas LPHD, MAX(0, Saldo Dana LPHD-Saldo Dana LPHD dari Karbon)/Waktu Pembelanjaan Dana Desa*Proporsi Alokasi Efektif Perlindungan*Rasio Realisasi Belanja/Biaya per Hari Patroli)", "HOK/Year", "PWD-K", "Patroli yang dapat dibiayai saldo non-karbon sendiri (atribusi non-karbon lebih dulu)"),
 "Hari Patroli Didanai Kas Non Karbon": ("MAX(Hari Patroli Didanai Kas LPHD*(1-Porsi Kas Karbon dalam Saldo), Hari Patroli Dapat Didanai Kas Non Karbon)", "HOK/Year", "PWD-K", "Konservatif terhadap dana yang dapat dipertukarkan: patroli LPHD dianggap non-karbon sejauh dapat dibiayai dana non-karbon (perbaikan K7)"),
 # ---------- PWD-K reversal
 "Aturan Penyelesaian Reversal": ("2", "Dmnl", "PWD-K", "ASUMSI MODEL (tidak berdasar kontrak). Debit reversal dibawa ke depan dan dapat dilunasi mitigasi berikutnya; pada setiap peristiwa verifikasi (5 th) debit yang tersisa diselesaikan: 0 = tidak diselesaikan (hanya dilaporkan sebagai kewajiban); 1 = buffer lalu pembatalan stok kredit sendiri yang belum terjual; 2 = 1 + pembelian kredit pengganti untuk sisanya"),
 "Pulsa Verifikasi Reversal": ("PULSE TRAIN(Tahun Mulai Karbon+Delay Verifikasi dan Penerbitan Kredit+Periode Verifikasi, TIME STEP, Periode Verifikasi, FINAL TIME)", "Dmnl", "PWD-K", "Peristiwa verifikasi 2032, 2037, ..., 2082"),
 "Mode Kredit Referensi S1 Aktif": ("IF THEN ELSE(Switch Baseline Kredit Konservatif=2, 1, 0)", "Dmnl", "PWD-K", ""),
 "Kontribusi Buffer REDD": ("Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif*MAX(0, Pengurangan Emisi REDD Bruto Referensi S1)*(1-Proporsi Leakage Karbon)*Proporsi Kredit REDD dalam Project Area*Proporsi Buffer Risiko Karbon", "tCO2e/Year", "PWD-K", "Kredit yang ditahan sebagai buffer risiko"),
 "Kumulatif Buffer REDD": ("INTEG(Kontribusi Buffer REDD, 0)", "tCO2e", "PWD-K", "Kontribusi kumulatif (pelaporan)"),
 "Buffer REDD Tersedia": ("INTEG(Kontribusi Buffer REDD-Penggunaan Buffer Reversal, 0)", "tCO2e", "PWD-K", "Buffer berkurang bila dipakai menutup reversal"),
 "Penggunaan Buffer Reversal": ("Mode Kredit Referensi S1 Aktif*IF THEN ELSE(Aturan Penyelesaian Reversal>=1, 1, 0)*Pulsa Verifikasi Reversal*MIN(Reversal Belum Terkompensasi, Buffer REDD Tersedia)/TIME STEP", "tCO2e/Year", "PWD-K", "Pembatalan kredit buffer pada peristiwa verifikasi"),
 "Stok Kredit REDD Dapat Dibatalkan": ("MAX(0, Stok Kredit REDD Belum Terjual-(Kredit REDD Terjual+Kredit REDD Kedaluwarsa)*TIME STEP)", "tCO2e", "PWD-K", ""),
 "Pembatalan Stok Kredit Reversal": ("Mode Kredit Referensi S1 Aktif*IF THEN ELSE(Aturan Penyelesaian Reversal>=1, 1, 0)*Pulsa Verifikasi Reversal*MIN(MAX(0, Reversal Belum Terkompensasi-Buffer REDD Tersedia), Stok Kredit REDD Dapat Dibatalkan)/TIME STEP", "tCO2e/Year", "PWD-K", "Kredit sendiri yang belum terjual dibatalkan (tanpa arus kas, mengurangi penerimaan masa depan)"),
 "Laju Penggantian Reversal": ("Mode Kredit Referensi S1 Aktif*IF THEN ELSE(Aturan Penyelesaian Reversal>=2, 1, 0)*Pulsa Verifikasi Reversal*MAX(0, Reversal Belum Terkompensasi-Buffer REDD Tersedia-Stok Kredit REDD Dapat Dibatalkan)/TIME STEP", "tCO2e/Year", "PWD-K", "Pembelian kredit pengganti untuk sisa debit sesudah buffer dan stok sendiri"),
 "Kredit Pengganti Reversal Kumulatif": ("INTEG(Laju Penggantian Reversal, 0)", "tCO2e", "PWD-K", ""),
 "Kumulatif Penggunaan Buffer Reversal": ("INTEG(Penggunaan Buffer Reversal, 0)", "tCO2e", "PWD-K", ""),
 "Kumulatif Pembatalan Stok Kredit Reversal": ("INTEG(Pembatalan Stok Kredit Reversal, 0)", "tCO2e", "PWD-K", ""),
 "Saldo Mitigasi REDD Belum Dikreditkan": ("INTEG(Mitigasi REDD Eligible Bersih Proyek-Kredit REDD Referensi S1 Bersih+Penggunaan Buffer Reversal+Pembatalan Stok Kredit Reversal+Laju Penggantian Reversal, 0)", "tCO2e", "PWD-K", "Negatif = debit reversal. Penyelesaian (buffer, pembatalan stok, pengganti) memulihkan saldo sehingga tidak ada penalti ganda"),
 "Stok Kredit REDD Belum Terjual": ("INTEG(Kredit REDD Terbit-Kredit REDD Terjual-Kredit REDD Kedaluwarsa-Pembatalan Stok Kredit Reversal, 0)", "tCO2e", "PWD-K", ""),
 "Kewajiban Reversal Belum Diselesaikan": ("Reversal Belum Terkompensasi*Harga Karbon*Nilai Tukar USD ke Rupiah", "Rupiah", "PWD-K", "Nilai debit yang belum diselesaikan pada harga berjalan (pelaporan, bukan arus kas)"),
 "Biaya Penggantian Reversal": ("Laju Penggantian Reversal*Harga Karbon*Nilai Tukar USD ke Rupiah", "Rupiah/Year", "PWD-K", "Kewajiban non-permanen; ditanggung proyek sebelum bagi hasil, atau ditalangi mitra bila kas tidak cukup"),
 "Biaya Transaksi dan MRV": ("Biaya Penerbitan dan Registri+Biaya Verifikasi Tahunan+Biaya Monitoring MRV+Biaya Transaksi Penjualan +Pajak dan Pungutan Karbon+Biaya Penggantian Reversal", "Rupiah/Year", "PWD-K", "Ditambah biaya penggantian reversal"),
 # ---------- PWD-M MRV
 "Switch Aturan Penghentian MRV": ("0", "Dmnl", "PWD-M", "1 = proyek (pengajuan kredit dan MRV) dihentikan permanen bila rerata kas penjualan < rasio ambang x rerata biaya MRV tetap sesudah tahun evaluasi. Aturan prospektif (hanya data lampau)"),
 "Tahun Mulai Evaluasi MRV": ("2033", "Year", "PWD-M", "Sesudah jembatan 2026-2030 dan jeda penerbitan 3 th. Asumsi"),
 "Waktu Rerata Evaluasi MRV": ("3", "Year", "PWD-M", ""),
 "Rasio Ambang Kas terhadap Biaya MRV": ("1", "Dmnl", "PWD-M", ""),
 "Biaya MRV Tetap": ("Biaya Monitoring MRV+Biaya Verifikasi Tahunan", "Rupiah/Year", "PWD-M", ""),
 "Rerata Kas Penjualan Evaluasi": ("SMOOTH(Kas Penjualan Kredit, Waktu Rerata Evaluasi MRV)", "Rupiah/Year", "PWD-M", ""),
 "Rerata Biaya MRV Evaluasi": ("SMOOTH(Biaya MRV Tetap, Waktu Rerata Evaluasi MRV)", "Rupiah/Year", "PWD-M", ""),
 "Laju Penghentian Proyek Karbon": ("Switch Aturan Penghentian MRV*IF THEN ELSE(Time>=Tahun Mulai Evaluasi MRV :AND: Rerata Kas Penjualan Evaluasi<Rasio Ambang Kas terhadap Biaya MRV*Rerata Biaya MRV Evaluasi, (1-Indikator Proyek Karbon Dihentikan)/TIME STEP, 0)", "1/Year", "PWD-M", ""),
 "Indikator Proyek Karbon Dihentikan": ("INTEG(Laju Penghentian Proyek Karbon, 0)", "Dmnl", "PWD-M", "Kunci permanen 0->1"),
 "Status Proyek Karbon Aktif": ("1-Indikator Proyek Karbon Dihentikan", "Dmnl", "PWD-M", ""),
 "Tahun Mulai Monitoring MRV": ("2024", "Year", "PWD-M", "Penundaan monitoring (uji: 2026)"),
 "Biaya Monitoring MRV": ("Switch Karbon*Switch Periode Kredit*Status Proyek Karbon Aktif*STEP(1, Tahun Mulai Monitoring MRV)*Luas Area Proyek Karbon*Biaya Monitoring per Ha per Tahun", "Rupiah/Year", "PWD-M", ""),
 "Biaya Verifikasi Tahunan": ("Switch Karbon*Status Proyek Karbon Aktif*(STEP(1, Tahun Mulai Karbon+Delay Verifikasi dan Penerbitan Kredit)-STEP (1, Tahun Mulai Karbon+Durasi Periode Kredit+Delay Verifikasi dan Penerbitan Kredit ))*Biaya Verifikasi per Kejadian/Periode Verifikasi", "Rupiah/Year", "PWD-M", ""),
 # ---------- PWD-T talangan
 "Tahun Akhir Tenor Talangan": ("2045", "Year", "PWD-T", "Asumsi uji: 15 th sesudah jembatan berakhir. Biaya modal berhenti dan (bila switch) sisa dihapus pada tahun ini"),
 "Batas Rasio Biaya Modal terhadap Pokok": ("1", "Dmnl", "PWD-T", "Akumulasi biaya modal maks. = 100 % pokok"),
 "Biaya Modal Kumulatif": ("INTEG(Biaya Modal Pendanaan Awal Rp, 0)", "Rupiah", "PWD-T", ""),
 "Biaya Modal Pendanaan Awal Rp": ("IF THEN ELSE(Time<Tahun Akhir Tenor Talangan, MIN(Pendanaan Awal Belum Terpulihkan*Biaya Modal Pendanaan Awal, MAX(0, Batas Rasio Biaya Modal terhadap Pokok*Pokok Talangan Kumulatif-Biaya Modal Kumulatif)/TIME STEP), 0)", "Rupiah/Year", "PWD-T", "Memperbaiki T-a: tidak tumbuh tanpa batas"),
 "Switch Penghapusan Talangan": ("0", "Dmnl", "PWD-T", "1 = sisa talangan dihapus pada akhir tenor dan dicatat sebagai kerugian mitra (bukan arus kas)"),
 "Penghapusan Talangan": ("Switch Penghapusan Talangan*IF THEN ELSE(Time>=Tahun Akhir Tenor Talangan, MAX(0, Pendanaan Awal Belum Terpulihkan/TIME STEP-Pemulihan Pendanaan Awal), 0)", "Rupiah/Year", "PWD-T", ""),
 "Kerugian Mitra dari Penghapusan Talangan": ("INTEG(Penghapusan Talangan, 0)", "Rupiah", "PWD-T", "Kerugian diakui; arus kas mitra tidak berubah karena pokok sudah tercatat sebagai arus keluar"),
 "Pendanaan Awal Belum Terpulihkan": ("INTEG((Pendanaan Awal untuk Patroli+Realisasi Pembiayaan Awal)*Status Pembiayaan Awal+Realisasi Pembiayaan Jembatan+Biaya Modal Pendanaan Awal Rp-Pemulihan Pendanaan Awal-Penghapusan Talangan, 0)", "Rupiah", "PWD-T", ""),
 # ---------- default mekanisme C (J1, 5 th)
 "Switch Pembiayaan Jembatan Karbon": ("1", "Dmnl", "PWD-C", "Default mekanisme C. Hanya aktif pada S2 (dikalikan Switch Karbon). BUKAN komitmen aktual mitra"),
 "Besaran Pembiayaan Jembatan per Tahun": ("7.8286e+08", "Rupiah/Year", "PWD-C", "J1 = 3.011 HOK x Rp260.000 (tingkat pembiayaan mitra 2025). Asumsi eksperimen"),
}
VIEW.update({"PWD-U": "04 Forest Patrol Protection", "PWD-K": "15 Carbon Emission Accounting", "PWD-M": "13 Carbon Finance Revenues", "PWD-T": "13 Carbon Finance Revenues", "PWD-C": "13 Carbon Finance Revenues"})
# ---------- rantai Referensi S1 (salinan rantai Baseline)
BL = __BL__
RN = {b: b[:-9] + " Referensi S1" for b in BL}
RX = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(b) for b in BL) + r")(?![A-Za-z0-9_])")
for b in BL:
    n = RN[b]
    if n in FIN: continue
    eq = RX.sub(lambda m: RN[m.group(1)], re.sub(r"\s+", " ", str(src[b][4])))
    if b == "Faktor Tekanan Deforestasi Baseline": continue
    FIN[n] = (eq, src[b][6], "PWD-K", "Rantai Referensi S1: salinan rantai Baseline dengan tekanan deforestasi S1")
for k, v in FIN.items(): EXTRA[k] = v
'''.replace('__BL__', repr(BL))
src_code = src_code.replace("merged = dict(P)", MEK + "\n" + FINAL + "\nmerged = dict(P)")
src_code = src_code.replace('src[n][22] = f"{TAG} [{code}]', 'src[n][22] = f"{TAG3 if code.startswith(\'PWD\') else (TAG2 if code==\'M1\' else TAG)} [{code}]').replace('rr[22] = n, view, "Auxiliary (dihitung)", eq, u, f"{TAG} [{code}]', 'rr[22] = n, view, "Auxiliary (dihitung)", eq, u, f"{TAG3 if code.startswith(\'PWD\') else (TAG2 if code==\'M1\' else TAG)} [{code}]')
exec(compile(src_code, "build_final", "exec"))
