"""Matriks data per variabel: setiap input .mdl (konstanta, nilai awal stok, deret historis) dipetakan ke kelompok data dan level."""
import json, csv, os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
inp = json.load(open(os.path.join(B, 'code', 'model_inputs.json'), encoding='utf-8'))
lev = {r['id']: r for r in csv.DictReader(open(os.path.join(B, 'DATA_UNCERTAINTY_LEVELING.csv'), encoding='utf-8'))}

# ---- kelompok: kode -> (nama, itu data apa, sumber, level awal, status)
def L(i): return (lev[i]['level'], 'TERUJI' if lev[i]['skor_pengaruh_P_teruji'] not in ('–', '') else 'PENILAIAN')
G = {
 'D01': ('Patroli swadaya pra-proyek dan basis kredit', 'Catatan patroli swadaya sebelum proyek; menentukan basis kredit A1/A2', 'LPHD'),
 'D02': ('Kehilangan akses dan pendapatan dari hutan', 'Pendapatan RT dari kawasan dan berapa yang hilang bila perlindungan diperketat', 'Survei RT (melalui LPHD)'),
 'D03': ('Efektivitas patroli', 'Seberapa besar patroli menekan laju deforestasi', 'LPHD (log patroli) + literatur'),
 'D04': ('Biaya MRV', 'Biaya pemantauan karbon per hektare', 'Dokumen proyek'),
 'D05': ('Laju deforestasi BAU (hutan → nonhutan/perkebunan)', 'Laju perubahan hutan menjadi nonhutan atau perkebunan tanpa intervensi', 'Sekunder publik (HCV, Hansen)'),
 'D06': ('Areal proyek karbon', 'Luas dan porsi pengurangan emisi di dalam areal proyek', 'Dokumen proyek (PDD)'),
 'D07': ('Harga karbon dan nilai tukar', 'Harga kredit REDD/ARR dan kurs', 'Sekunder publik / pasar'),
 'D08': ('Kebakaran (luas, hotspot, emisi)', 'Luas terbakar, hotspot, faktor emisi kebakaran', 'Sekunder publik + LPHD'),
 'D09': ('Biaya operasional dan kelembagaan LPHD', 'Biaya menjalankan dan menguatkan lembaga LPHD', 'LPHD'),
 'D10': ('Biaya patroli', 'Biaya per hari patroli dan biaya patroli sukarela', 'LPHD'),
 'D11': ('Efek izin PS', 'Pengaruh status izin HD terhadap deforestasi', 'Literatur + analisis Hansen'),
 'D12': ('Rumah tangga bergantung hutan', 'Jumlah RT yang bergantung pada hutan dan perubahannya', 'LPHD/desa'),
 'D13': ('Kebocoran', 'Deforestasi/aktivitas yang berpindah ke luar areal', 'Dokumen proyek (PDD)'),
 'D14': ('Bagi hasil', 'Pembagian dana karbon LPHD/mitra dan pemulihan biaya bersama', 'Dokumen proyek / LPHD'),
 'D15': ('Buffer non-permanen', 'Cadangan kredit untuk risiko pembalikan', 'Dokumen proyek (PDD)'),
 'D16': ('Biaya verifikasi, registri, transaksi, pajak', 'Biaya verifikasi per kejadian, penerbitan, transaksi, pajak karbon', 'Dokumen proyek / regulasi'),
 'D17': ('Tingkat diskonto', 'Angka untuk menghitung NPV (di luar model)', 'Literatur'),
 'D18': ('Jadwal kredit', 'Jeda penerbitan, awal dan durasi periode kredit', 'Dokumen proyek'),
 'D19': ('Pembiayaan awal', 'Nilai, periode, dan atribusi pembiayaan awal 2024–2025', 'Dokumen proyek + LPHD'),
 'D20': ('Pendapatan dasar RT', 'Pendapatan RT per tahun sebagai acuan', 'Survei RT / literatur'),
 'D21': ('Data awal dan historis KUPS', 'Jumlah KUPS dan anggota 2023–2025', 'Sekunder publik + LPHD'),
 'D22': ('Densitas karbon', 'Karbon biomassa dan kayu mati per hektare per kelas', 'Dokumen proyek (PDD)'),
 'D23': ('Pemegang garapan', 'Jumlah pemegang garapan di dalam HD', 'LPHD'),
 'D24': ('Penduduk dan demografi', 'Jumlah dan pertumbuhan penduduk, ukuran RT, pengangguran', 'BPS'),
 'D25': ('Bukti validasi', 'Berkas MAPE, Monte Carlo, PRCC (bukan variabel model)', 'Berkas peneliti'),
 'N01': ('Alokasi dana LPHD', 'Porsi dana LPHD ke operasional, patroli, rehabilitasi, kelembagaan, KUPS', 'LPHD'),
 'N02': ('Kapasitas patroli', 'Hari patroli per anggota, anggota per regu, cakupan regu, perekrutan', 'LPHD'),
 'N03': ('Kebutuhan regu pengendalian kebakaran', 'Cakupan, anggota, HOK siaga, upah, sarana regu kebakaran', 'LPHD + standar MPA'),
 'N04': ('Penjualan kredit', 'Laju penjualan dan kedaluwarsa kredit', 'Dokumen proyek / pasar'),
 'N05': ('Mekanisme yang dinonaktifkan (nilai 0)', 'Hubungan yang ada di model tetapi dimatikan; hasil berlaku dengan anggapan hubungan ini tidak ada', 'Literatur / data lapangan'),
 'N06': ('Kapasitas LPHD', 'Kemampuan LPHD merealisasikan anggaran', 'LPHD'),
 'N07': ('Gambut', 'Luas gambut, gangguan, dan faktor emisi gambut', 'Dokumen proyek / literatur'),
 'N08': ('Regenerasi (nonhutan → hutan)', 'Laju pemulihan alami nonhutan menjadi hutan', 'Sekunder publik'),
 'N09': ('Tutupan lahan awal 2024', 'Luas tiap kelas tutupan saat simulasi dimulai', 'Sekunder publik (HCV 2024)'),
 'N10': ('Transisi nonhutan ↔ perkebunan', 'Konversi nonhutan ke perkebunan dan sebaliknya', 'Sekunder (matriks transisi GEE)'),
 'N11': ('Rehabilitasi', 'Biaya, target, keberhasilan, dan waktu penanaman', 'LPHD (RKPS) + proyek'),
 'N12': ('Upah dan kerja', 'Upah harian, HOK per pekerja, porsi upah sebagai tambahan bersih', 'LPHD'),
 'N13': ('Ekonomi KUPS', 'Penjualan, surplus, produktivitas, pendampingan KUPS', 'LPHD / KUPS'),
 'N14': ('Uji akurasi peta tutupan lahan', 'Akurasi klasifikasi peta (bukan variabel model; mendasari D05, N08, N09, N10)', 'Sampel referensi (citra resolusi tinggi / lapangan)'),
 'T': ('Teknis / switch skenario', 'Pengaturan simulasi, switch skenario, konstanta konversi', '–'),
}
NEWLEV = {'N01': '2 TINGGI', 'N02': '2 TINGGI', 'N03': '2 TINGGI', 'N04': '2 TINGGI', 'N05': '2 TINGGI', 'N06': '3 SEDANG', 'N07': '3 SEDANG', 'N08': '3 SEDANG',
          'N09': '2 TINGGI', 'N10': '3 SEDANG', 'N11': '3 SEDANG', 'N12': '3 SEDANG', 'N13': '3 SEDANG', 'N14': '2 TINGGI', 'T': '– TEKNIS'}
GLEV = {}
for k in G:
    if k in lev: GLEV[k] = L(k)
    else: GLEV[k] = (NEWLEV[k], 'TEKNIS' if k == 'T' else 'PERKIRAAN')

M = {}
def put(code, names):
    for n in names: M[n] = code
put('D01', ['Kegiatan Patroli Swadaya Tahunan 2023', 'Indeks Intensitas Swadaya 2023', 'Hari Patroli Swadaya per Anggota', 'Tahun Patroli Efektif 2023 2024', 'Switch Baseline Kredit Konservatif', 'Faktor Rekonsiliasi Reversal Kredit A2'])
put('D02', ['Pengali Kehilangan Akses', 'Proporsi Pendapatan dari Hutan', 'Elastisitas Pendapatan Hutan terhadap Luas Hutan', 'Proporsi Pendapatan Hutan dari Aktivitas Pemicu Deforestasi'])
put('D03', ['Efektivitas Perlindungan Penuh terhadap Deforestasi', 'Waktu Penyesuaian Efek Pengelolaan PS', 'Rasio Risiko Penempatan Patroli Swadaya', 'Kelengkungan Respons Perlindungan', 'Indeks Perlindungan Baseline'])
put('D04', ['Biaya Monitoring per Ha per Tahun'])
put('D05', ['Laju HMS menjadi NonHutan BAU', 'Laju HRS menjadi NonHutan BAU', 'Laju HLKS menjadi NonHutan BAU', 'Laju HRS menjadi Pr BAU', 'Laju HLKS menjadi Pr BAU', 'Deforestasi Historis Tahunan Referensi', 'Faktor Tekanan Deforestasi Baseline', 'Proporsi Deforestasi Dipengaruhi Tekanan Masyarakat'])
put('D06', ['Proporsi Kredit REDD dalam Project Area', 'Luas Area Proyek Karbon'])
put('D07', ['Harga Karbon', 'Harga Karbon Removal', 'Nilai Tukar USD ke Rupiah'])
put('D08', ['Luas Historis Karhutla', 'Proporsi Alokasi Pengendalian Kebakaran', 'Rasio Luas Terbakar Tahun Kering', 'Interval Tahun Kering', 'Luas Kebakaran per Hotspot Acuan', 'Hotspot Berisiko Acuan', 'Proporsi Karhutla di Lahan Gambut', 'Faktor Emisi Kebakaran Gambut', 'Efektivitas Maksimum Pengendalian Kebakaran', 'Waktu Respons Pengendalian Kebakaran'])
put('D09', ['Biaya Operasional per LPHD per Tahun', 'Jumlah LPHD', 'Biaya Penguatan Kelembagaan per LPHD per Tahun'])
put('D10', ['Biaya per Hari Patroli', 'Biaya Operasional Patroli Sukarela per Anggota per Tahun'])
put('D11', ['Efek Izin PS terhadap Deforestasi', 'Bobot Izin dalam Periode Kalibrasi', 'Tahun Izin Efektif 2017 2024'])
put('D12', ['Masyarakat Bergantung pada Hutan Awal', 'Rumah Tangga per Pekerja Bergantung', 'Laju Pengurangan Ketergantungan Dasar', 'Laju Ketergantungan Masyarakat Pada Hutan'])
put('D13', ['Proporsi Leakage Karbon', 'Proporsi Leakage ARR'])
put('D14', ['Proporsi Manfaat Masyarakat', 'Switch Pemulihan Defisit Biaya Bersama'])
put('D15', ['Proporsi Buffer Risiko Karbon'])
put('D16', ['Biaya Verifikasi per Kejadian', 'Periode Verifikasi', 'Biaya Penerbitan per Kredit', 'Proporsi Biaya Transaksi Penjualan', 'Proporsi Pajak dan Pungutan Karbon'])
put('D18', ['Delay Verifikasi dan Penerbitan Kredit', 'Durasi Periode Kredit', 'Tahun Mulai Karbon'])
put('D19', ['Porsi Kenaikan Patroli 2024 dari Pembiayaan Awal', 'Porsi Pembiayaan Awal sebagai Talangan', 'Tahun Awal Pembiayaan Awal', 'Tahun Akhir Pembiayaan Awal', 'Kegiatan Patroli Tercatat 2024', 'Orang Hari per Kegiatan Patroli', 'Besaran Pendanaan Awal Proyek Karbon', 'Durasi Pendanaan Awal', 'Biaya Modal Pendanaan Awal'])
put('D20', ['Pendapatan Dasar RT Bergantung', 'Pendapatan Dasar Masyarakat'])
put('D21', ['Jumlah KUPS Awal', 'Anggota KUPS Awal', 'Penambahan KUPS Tahun 2024', 'Penambahan KUPS Tahun 2025', 'Penambahan Anggota KUPS Tahun 2024', 'Penambahan Anggota KUPS Tahun 2025', 'Tahun Akhir Data KUPS', 'Penambahan Anggota KUPS Historis', 'Penambahan KUPS Historis'])
put('D22', ['Densitas Biomassa HMS', 'Densitas Biomassa HRS', 'Densitas Biomassa HLKS', 'Densitas Biomassa NonHutan', 'Densitas Biomassa Pr', 'Densitas Kayu Mati dan Serasah HMS', 'Densitas Kayu Mati dan Serasah HRS',
            'Densitas Kayu Mati dan Serasah HLKS', 'Densitas Kayu Mati dan Serasah NonHutan', 'Densitas Kayu Mati dan Serasah Pr', 'Waktu Akumulasi Karbon Hutan Sekunder'])
put('D23', ['RT Pemegang Garapan dalam HD', 'Faktor Keunikan Catatan Garapan'])
put('D24', ['Laju Pertumbuhan Penduduk', 'Laju Pengurangan Penduduk', 'Populasi', 'Ukuran Rumah Tangga', 'Tingkat Pengangguran Terbuka'])
put('N01', ['Proporsi Alokasi Operasional LPHD', 'Proporsi Alokasi Perlindungan', 'Proporsi Alokasi Rehabilitasi', 'Proporsi Alokasi Penguatan Kelembagaan', 'Proporsi Alokasi Pengembangan KUPS', 'Waktu Pembelanjaan Dana Desa'])
put('N02', ['Frekuensi Patroli Ideal per Anggota', 'Maksimum Hari Patroli per Anggota', 'Proporsi Penggantian Anggota Patroli Swadaya', 'HOK Patroli Berbayar per Anggota', 'Cakupan Kawasan per Regu', 'Jumlah Anggota per Regu',
            'Laju Ketidakaktifan Anggota Patroli Dasar', 'Kapasitas Penambahan Anggota Patroli BAU', 'Anggota Patroli Awal', 'Penambahan Anggota Patroli Tim Baru 2024', 'Penambahan Anggota Patroli Tim Baru 2025', 'Target Pemenuhan Kebutuhan Patroli'])
put('N03', ['Luas Cakupan per Regu Pengendalian Kebakaran', 'Anggota per Regu Pengendalian Kebakaran', 'HOK Siaga per Anggota Pengendalian Kebakaran', 'Upah Harian Pengendalian Kebakaran', 'Biaya Sarana dan Sekat Kanal per Regu'])
put('N04', ['Laju Penjualan Kredit', 'Laju Kedaluwarsa Kredit', 'Proporsi Kredit Karbon Terjual'])
put('N05', ['Sensitivitas Konversi terhadap Kehilangan Penghidupan', 'Waktu Respons Penghidupan', 'Sensitivitas Rebound Pendapatan terhadap Konversi', 'Proporsi Deforestasi Terkait Kebakaran', 'Pengaruh Pengendalian Kebakaran terhadap Keberhasilan Rehabilitasi',
            'Pengaruh Kapasitas terhadap Mutu Kegiatan', 'Pengaruh Kelembagaan terhadap Retensi Anggota Patroli', 'Sensitivitas Konversi terhadap Substitusi Pendapatan', 'Indeks Harga Komoditas', 'Elastisitas Deforestasi terhadap Harga Komoditas',
            'Efektivitas Patroli terhadap Kebakaran', 'Sensitivitas Tekanan Hutan terhadap Pengurangan Ketergantungan', 'Sensitivitas Tekanan Hutan terhadap Kecukupan Patroli', 'Sensitivitas Gangguan Gambut terhadap Pengurangan Tekanan Hutan',
            'Sensitivitas Gangguan Gambut terhadap Pemulihan', 'Sensitivitas Ekspansi Lahan terhadap Pendapatan PS', 'Proporsi Peserta Program dari Kelompok Bergantung', 'Proporsi Usaha KUPS Berbasis Hutan', 'Prioritas Penerima Kegiatan dari RT Terdampak',
            'Sensitivitas Pengurangan Ketergantungan terhadap Manfaat PS', 'Waktu Penyesuaian Persepsi Manfaat', 'Waktu Transisi Mata Pencaharian'])
put('N06', ['Indeks Kapasitas LPHD Awal', 'Waktu Pembangunan Kapasitas LPHD', 'Indeks Kapasitas untuk Realisasi Penuh'])
put('N07', ['Luas Total Gambut Lindung', 'Luas Total Gambut Budidaya', 'Luas Gambut Lindung Terganggu Awal', 'Luas Gambut Budidaya Terganggu Awal', 'Faktor Emisi Gambut Budidaya', 'Faktor Emisi Gambut Lindung',
            'Tingkat Gangguan Gambut Budidaya BAU', 'Tingkat Gangguan Gambut Lindung BAU', 'Faktor Gangguan Gambut Tersisa Baseline'])
put('N08', ['Laju NonHutan menjadi HLKS', 'Laju NonHutan menjadi HMS', 'Laju NonHutan menjadi HRS'])
put('N09', ['Hutan Mangrove Sekunder', 'Hutan Rawa Sekunder', 'Hutan Lahan Kering Sekunder', 'NonHutan', 'Perkebunan', 'Porsi Koreksi HMS', 'Porsi Koreksi HRS', 'Porsi Koreksi HLKS'])
put('N10', ['Laju NonHutan menjadi Pr', 'Laju Perkebunan menjadi NonHutan', 'Faktor Ekspansi Kebun Baseline'])
put('N11', ['Biaya Penanaman per Ha', 'Biaya Pemeliharaan Tanaman per Ha per Tahun', 'Luas Restorasi Selektif Eligible', 'Tingkat Keberhasilan Rehabilitasi dengan Pemeliharaan Penuh', 'Durasi Pemeliharaan Tanaman', 'Target Total Penanaman RKPS',
            'Target Penanaman', 'Fraksi Maksimum NonHutan Ditanami per Tahun', 'Waktu Pembentukan Tutupan Hutan', 'Tingkat Keberhasilan Rehabilitasi Dasar', 'Proporsi Rehabilitasi ke HLKS', 'Proporsi Rehabilitasi ke HMS', 'Proporsi Rehabilitasi ke HRS',
            'HOK Penanaman per Pekerja per Tahun', 'Proporsi Realisasi Penanaman BAU', 'Luas Penanaman Awal', 'HOK Penanaman per Ha'])
put('N12', ['Upah Harian Patroli Berbayar', 'Upah Penanaman per HOK', 'Upah Patroli per HOK', 'Porsi Upah sebagai Tambahan Bersih', 'HOK Tersedia per Anggota Kerja per Tahun', 'Faktor Penargetan Manfaat ke RT Bergantung', 'Faktor Tumpang Tindih Penerima'])
put('N13', ['Surplus Operasional per KUPS Produktif', 'Porsi Surplus KUPS Dibagikan ke Anggota', 'Penjualan per KUPS Produktif', 'Proporsi KUPS Produktif Bersurplus', 'Proporsi KUPS Produktif Tanpa Dukungan', 'Proporsi KUPS Produktif Maksimum',
            'Waktu Respons Produktivitas KUPS', 'Biaya Pendampingan per KUPS per Tahun', 'Proporsi Penggantian KUPS Tanpa Dana Karbon', 'Pembentukan KUPS Dana Non Karbon', 'Biaya Pembentukan KUPS', 'Jumlah Minimum Anggota per KUPS',
            'Target Pembentukan KUPS', 'Laju Ketidakaktifan KUPS Dasar', 'Laju Ketidakaktifan Anggota KUPS Dasar', 'Pengurangan Maksimum Ketidakaktifan dari Kelembagaan', 'Manfaat Ekonomi KUPS BAU per Anggota', 'Target Total KUPS'])

KEEP_DERET = {'Luas Historis Karhutla', 'Penambahan Anggota KUPS Historis', 'Penambahan KUPS Historis'}
rows = []
seen = set()
for o in inp:
    n = o['nama']
    if o['jenis'] == 'deret_waktu' and n not in KEEP_DERET: continue
    if n.endswith(' Baseline') and o['jenis'] == 'stok_awal': continue
    if n in seen: continue
    seen.add(n)
    code = M.get(n, 'T')
    val = o['nilai']
    if o['jenis'] == 'stok_awal': val = re.split(r'-Switch', val.replace(' ', ''))[0]
    doc = re.sub(r'^(?:[A-Z0-9][\w.\- ]*20\d\d-\d\d-\d\d[^:]*:\s*)', '', o['doc']).strip()
    kls = re.findall(r'(?:Kualitas|Kelas bukti)\s*:?\s*([A-D](?:/[A-D])?|-)', o['doc'])
    rows.append([n, val, o['satuan'], {'konstanta': 'Konstanta', 'stok_awal': 'Nilai awal stok', 'deret_waktu': 'Deret historis'}[o['jenis']], kls[0] if kls else '', o['tag'], code, doc[:220]])
# NonHutan (nilai awal tidak terbaca otomatis karena ada switch dalam INTEG)
rows.append(['NonHutan', '29087.1', 'Ha', 'Nilai awal stok', 'A', '', 'N09', 'Nilai awal = observasi tutupan lahan 2024 (HCV); + koreksi kontrafaktual S1 bila Switch S1 = 1'])
for code, name in (('D17', 'Tingkat diskonto (dihitung di luar model)'), ('D25', 'Berkas validasi MAPE/Monte Carlo/PRCC (bukan variabel)'), ('N14', 'Uji akurasi peta tutupan lahan (bukan variabel)')):
    rows.append([name, '–', '–', 'Bukan variabel model', '', '', code, G[code][1]])
order = {k: i for i, k in enumerate(G)}
rows.sort(key=lambda r: (order[r[6]], r[0]))
missing = [n for n in M if n not in seen and n != 'NonHutan']
print('tidak ditemukan di model:', missing)

# ---- workbook
F = 'Arial'; fnt = Font(name=F, size=10); bold = Font(name=F, size=10, bold=True); hf = Font(name=F, size=10, bold=True, color='FFFFFF')
blue = Font(name=F, size=10, color='0000FF'); title = Font(name=F, size=14, bold=True)
hfill = PatternFill('solid', fgColor='1F4E78'); yfill = PatternFill('solid', fgColor='FFFF00')
thin = Side(style='thin', color='BFBFBF'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical='top'); center = Alignment(horizontal='center', vertical='top', wrap_text=True)
LF = {'1 KRITIS': 'F8CBAD', '2 TINGGI': 'FFE699', '3 SEDANG': 'DDEBF7', '4 RENDAH': 'E2EFDA', '– TEKNIS': 'EDEDED'}
def hdr(ws, r, labels, widths):
    for i, (h, w) in enumerate(zip(labels, widths), 1):
        c = ws.cell(r, i, h); c.font = hf; c.fill = hfill; c.alignment = center; c.border = box
        ws.column_dimensions[c.column_letter].width = w
wb = Workbook()
k = wb.active; k.title = 'Per_Kelompok'
k['A1'] = 'Matriks data per kelompok'; k['A1'].font = title
k['A2'] = 'Ubah Level (kolom D, biru-kuning) bila ada bukti baru; lembar Per_Variabel mengikuti otomatis. Status: TERUJI = dari uji sensitivitas audit; PENILAIAN = skor audit tanpa uji; PERKIRAAN = kelompok baru, belum diuji.'; k['A2'].font = fnt
hdr(k, 4, ['Kode', 'Kelompok data', 'Itu data apa', 'Level', 'Status level', 'Sumber data', 'Jumlah variabel', 'Di antaranya kelas D / asumsi / placeholder'], [7, 34, 52, 12, 12, 30, 11, 16])
kl = 4 + len(G); vl = 1 + len(rows)
for i, (code, (nm, apa, src)) in enumerate(G.items(), 5):
    lv, st = GLEV[code]
    vals = [code, nm, apa, lv, st, src]
    for j, v in enumerate(vals, 1):
        c = k.cell(i, j, v); c.font = blue if j == 4 else fnt; c.border = box; c.alignment = wrap if j in (2, 3, 6) else center
    k.cell(i, 4).fill = yfill
    k.cell(i, 7, f'=COUNTIF(Per_Variabel!$H$2:$H${vl},A{i})').font = fnt
    k.cell(i, 8, f'=COUNTIFS(Per_Variabel!$H$2:$H${vl},A{i},Per_Variabel!$E$2:$E${vl},"D")+COUNTIFS(Per_Variabel!$H$2:$H${vl},A{i},Per_Variabel!$E$2:$E${vl},"<>D",Per_Variabel!$F$2:$F${vl},"?*")').font = fnt
    for j in (7, 8): k.cell(i, j).border = box; k.cell(i, j).alignment = center
dv = DataValidation(type='list', formula1='"1 KRITIS,2 TINGGI,3 SEDANG,4 RENDAH,– TEKNIS"'); k.add_data_validation(dv); dv.add(f'D5:D{kl}')
for lv, col in LF.items():
    k.conditional_formatting.add(f'A5:H{kl}', FormulaRule(formula=[f'$D5="{lv}"'], fill=PatternFill('solid', fgColor=col)))
k.freeze_panes = 'C5'
t = kl + 2
k.cell(t, 1, 'Ringkasan').font = bold
hdr(k, t + 1, ['', 'Level', 'Jumlah kelompok', 'Jumlah variabel'], [7, 34, 52, 12])
for i, lv in enumerate(LF, t + 2):
    k.cell(i, 2, lv).font = fnt; k.cell(i, 2).fill = PatternFill('solid', fgColor=LF[lv])
    k.cell(i, 3, f'=COUNTIF($D$5:$D${kl},B{i})').font = fnt
    k.cell(i, 4, f'=COUNTIF(Per_Variabel!$I$2:$I${vl},B{i})').font = fnt
k.cell(t + 7, 2, 'Total').font = bold
k.cell(t + 7, 3, f'=SUM(C{t+2}:C{t+6})').font = bold; k.cell(t + 7, 4, f'=SUM(D{t+2}:D{t+6})').font = bold
for col in (2, 3, 4): k.column_dimensions[k.cell(1, col).column_letter].width = [7, 34, 52, 12][col - 1]

v = wb.create_sheet('Per_Variabel')
hdr(v, 1, ['Variabel (.mdl)', 'Nilai di model', 'Satuan', 'Jenis', 'Kelas bukti (.mdl)', 'Tanda di catatan', 'Kode kelompok', 'Kode', 'Level', 'Kelompok data', 'Itu data apa (kelompok)', 'Sumber data', 'Keterangan di catatan model'],
    [40, 14, 18, 15, 10, 18, 1, 7, 12, 30, 40, 26, 60])
v.column_dimensions['G'].hidden = True
for i, r in enumerate(rows, 2):
    n, val, sat, jen, kls, tag, code, doc = r
    try:
        fv = float(val); vv = fv
    except ValueError:
        vv = val
    vals = [n, vv, sat, jen, kls, tag, code, code]
    for j, x in enumerate(vals, 1):
        c = v.cell(i, j, x); c.font = blue if j == 2 else fnt; c.border = box; c.alignment = wrap if j in (1, 3, 6) else center
        if j == 2 and isinstance(vv, float): c.number_format = 'General'
    for j, col in ((9, 'D'), (10, 'B'), (11, 'C'), (12, 'F')):
        c = v.cell(i, j, f'=INDEX(Per_Kelompok!${col}$5:${col}${kl},MATCH(H{i},Per_Kelompok!$A$5:$A${kl},0))'); c.font = Font(name=F, size=10, color='008000'); c.border = box; c.alignment = wrap if j != 9 else center
    c = v.cell(i, 13, doc); c.font = fnt; c.border = box; c.alignment = wrap
for lv, col in LF.items():
    v.conditional_formatting.add(f'A2:M{vl}', FormulaRule(formula=[f'$I2="{lv}"'], fill=PatternFill('solid', fgColor=col)))
v.freeze_panes = 'B2'; v.auto_filter.ref = f'A1:M{vl}'
wb.move_sheet('Per_Variabel', offset=-1)
out = os.path.join(B, 'MATRIKS_DATA_PER_VARIABEL.xlsx'); wb.save(out)
with open(os.path.join(B, 'MATRIKS_DATA_PER_VARIABEL.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['variabel', 'nilai', 'satuan', 'jenis', 'kelas_bukti', 'tanda', 'kode', 'level', 'status_level', 'kelompok', 'itu_data_apa', 'sumber', 'keterangan_model'])
    for r in rows:
        c = r[6]; w.writerow(r[:7] + [GLEV[c][0], GLEV[c][1], G[c][0], G[c][1], G[c][2], r[7]])
from collections import Counter
print(len(rows), 'baris;', Counter(GLEV[r[6]][0] for r in rows))
