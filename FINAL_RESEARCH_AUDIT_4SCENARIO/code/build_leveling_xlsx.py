"""Membangun ANALISIS_KETIDAKPASTIAN_DATA.xlsx dari DATA_UNCERTAINTY_LEVELING.csv, robustness_oat.csv, A1_A2_BASELINE_RECONCILIATION.csv."""
import csv, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule, ColorScaleRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.comments import Comment

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(B, 'ANALISIS_KETIDAKPASTIAN_DATA.xlsx')
rows = list(csv.DictReader(open(os.path.join(B, 'DATA_UNCERTAINTY_LEVELING.csv'), encoding='utf-8')))
rows.sort(key=lambda r: r['id'])
oat = list(csv.DictReader(open(os.path.join(B, '07_UNCERTAINTY', 'robustness_oat.csv'), encoding='utf-8')))
a2 = {r['harga_USD']: r for r in csv.DictReader(open(os.path.join(B, 'A1_A2_BASELINE_RECONCILIATION.csv'), encoding='utf-8')) if r['basis'] == 'A2_register'}

F = 'Arial'
fnt = Font(name=F, size=10); bold = Font(name=F, size=10, bold=True); hfont = Font(name=F, size=10, bold=True, color='FFFFFF')
blue = Font(name=F, size=10, color='0000FF'); green = Font(name=F, size=10, color='008000')
title = Font(name=F, size=14, bold=True)
hfill = PatternFill('solid', fgColor='1F4E78'); yfill = PatternFill('solid', fgColor='FFFF00')
thin = Side(style='thin', color='BFBFBF'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical='top'); center = Alignment(horizontal='center', vertical='center', wrap_text=True)
LVL_FILL = {'1 KRITIS': 'F8CBAD', '2 TINGGI': 'FFE699', '3 SEDANG': 'DDEBF7', '4 RENDAH': 'E2EFDA'}

def header(ws, r, labels, widths=None):
    for i, h in enumerate(labels, 1):
        c = ws.cell(r, i, h); c.font = hfont; c.fill = hfill; c.alignment = center; c.border = box
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = w

wb = Workbook()
# ---------------- README ----------------
ws = wb.active; ws.title = 'README'
ws.column_dimensions['A'].width = 26; ws.column_dimensions['B'].width = 110
lines = [
 ('Analisis Ketidakpastian Data — Model S1–S4, 25 Hutan Desa di Kalimantan Barat', None),
 ('', None),
 ('Tujuan', 'Memberi level pada setiap data/parameter menurut pengaruhnya terhadap kesimpulan makalah dan kelemahan buktinya, lalu menyusun prioritas pengumpulan data.'),
 ('Sumber', 'Nilai dasar, sumber, dan kelas bukti dikutip dari catatan persamaan DKP_25HD_A1_*_rapi.mdl. Besaran dampak dari uji audit (07_UNCERTAINTY/robustness_oat.csv; A1_A2_BASELINE_RECONCILIATION.csv; 05_SOCIOECONOMIC_RESULTS). Tidak ada model atau hasil S1–S4 yang diubah.'),
 ('Lembar', 'Matriks (25 butir) · Uji_Sensitivitas (hasil OAT audit + uji P otomatis) · Grid (P × W) · Ringkasan (per level, status, kategori + grafik) · Prioritas (urutan pengumpulan data).'),
 ('', None),
 ('CARA PAKAI', None),
 ('Sel yang boleh diubah', 'Sel berhuruf BIRU berlatar KUNING: skor P dan W di lembar Matriks, dan skor Kemudahan di lembar Prioritas. Semua sel hitam berisi formula dan akan dihitung ulang otomatis.'),
 ('Contoh', 'Bila log patroli 2017–2023 ditemukan dan menunjukkan patroli swadaya sudah rutin, ubah W pada D01 dari 3 menjadi 1; level D01 otomatis turun dari 1 KRITIS ke 2 TINGGI.'),
 ('Warna huruf', 'Biru = input/data tetap (hasil reproduksi audit atau penilaian) · Hitam = formula · Hijau = tautan ke lembar lain.'),
 ('', None),
 ('ATURAN SKOR', None),
 ('P (pengaruh)', '3 = dapat membalik arah/kesimpulan naskah (tanda, kelayakan, ada/tidaknya efek); 2 = menggeser besaran ≥ 15 % tanpa membalik; 1 = hanya indikator tertentu.'),
 ('W (kelemahan bukti)', '3 = asumsi eksploratif, kelas D, data ≤ 2 tahun, atau berkas tidak ada; 2 = proksi eksternal, kelas C, atau provisional; 1 = kelas B data lokal; 0 = kelas A observasi.'),
 ('P teruji', 'Dihitung otomatis di lembar Uji_Sensitivitas untuk butir yang sudah diuji: 3 bila tanda NPV USD 10 atau ΔRT berbalik, atau efek PS (S2−S1), pembiayaan awal (S3−S2), atau karbon (S4−S3 USD 10) berbalik tanda/turun di bawah 10 % nilai dasar; 2 bila perubahan terbesar ≥ 15 %; selain itu 1. Bila ada, P teruji menggantikan P penilaian (kolom P final).'),
 ('Level', '1 KRITIS: P final = 3 dan W ≥ 2 · 2 TINGGI: P final = 3 dan W ≤ 1, atau P final = 2 dan W ≥ 2 · 3 SEDANG: P final = 2 dan W ≤ 1, atau P final = 1 dan W ≥ 2 · 4 RENDAH: lainnya.'),
 ('Prioritas', 'Skor prioritas = P final × W × Kemudahan (1 = data tidak ada/harus survei baru; 2 = kemungkinan ada di arsip; 3 = ada di dokumen yang sudah dimiliki). Kemudahan adalah penilaian awal audit dari kolom ketersediaan data; silakan sesuaikan.'),
 ('', None),
 ('CATATAN INTEGRITAS', None),
 ('Status bukti', 'REPRODUKSI AUDIT = diuji ulang audit · NASKAH (BELUM DIVERIFIKASI) = angka naskah yang belum dapat dihitung ulang · BELUM DIUJI = P adalah penilaian dari struktur model, bukan hasil uji.'),
 ('Batasan', 'Skor adalah penilaian terstruktur, bukan hasil statistik. Kredit model ≠ kredit terverifikasi. Hasil sensitivitas adalah frekuensi/besaran pada asumsi yang diuji, bukan peluang kejadian lapangan.'),
]
for i, (a, b) in enumerate(lines, 1):
    ca = ws.cell(i, 1, a); ca.font = title if i == 1 else bold; ca.alignment = wrap
    if b is not None:
        cb = ws.cell(i, 2, b); cb.font = fnt; cb.alignment = wrap
ws['B8'].fill = yfill

# ---------------- Matriks ----------------
m = wb.create_sheet('Matriks')
H = ['ID', 'Kategori', 'Data', 'Variabel model (.mdl)', 'Nilai dasar', 'Sumber dan kelas bukti (.mdl)', 'Periode data', 'Hasil terdampak', 'Besaran dampak', 'Status bukti dampak',
     'P penilaian (1–3)', 'W kelemahan bukti (0–3)', 'P teruji (otomatis)', 'P final', 'Skor P×W', 'Level', 'Ketersediaan data', 'Cara menutup']
header(m, 1, H, [6, 16, 34, 30, 20, 40, 16, 30, 44, 18, 11, 11, 11, 9, 9, 12, 26, 36])
keys = ['id', 'kategori', 'data', 'variabel_model', 'nilai_dasar', 'sumber_dan_kelas_bukti_mdl', 'periode_data', 'hasil_terdampak', 'besaran_dampak', 'status_bukti_dampak']
N = len(rows); last = N + 1
for i, r in enumerate(rows, 2):
    for j, k in enumerate(keys, 1):
        c = m.cell(i, j, r[k]); c.font = fnt; c.alignment = wrap; c.border = box
    for col, k in ((11, 'skor_pengaruh_P_penilaian'), (12, 'skor_kelemahan_bukti_W')):
        c = m.cell(i, col, int(r[k])); c.font = blue; c.fill = yfill; c.alignment = center; c.border = box
    m.cell(i, 13, f'=IF(COUNTIF(Uji_Sensitivitas!$A:$A,A{i})=0,"–",_xlfn.MAXIFS(Uji_Sensitivitas!$Y:$Y,Uji_Sensitivitas!$A:$A,A{i}))')
    m.cell(i, 14, f'=IF(M{i}="–",K{i},M{i})')
    m.cell(i, 15, f'=N{i}*L{i}')
    m.cell(i, 16, f'=IF(AND(N{i}=3,L{i}>=2),"1 KRITIS",IF(OR(N{i}=3,AND(N{i}=2,L{i}>=2)),"2 TINGGI",IF(OR(N{i}=2,AND(N{i}=1,L{i}>=2)),"3 SEDANG","4 RENDAH")))')
    for col in (13, 14, 15, 16):
        c = m.cell(i, col); c.font = green if col == 13 else fnt; c.alignment = center; c.border = box
    for col, k in ((17, 'ketersediaan_data'), (18, 'cara_menutup')):
        c = m.cell(i, col, r[k]); c.font = fnt; c.alignment = wrap; c.border = box
m.freeze_panes = 'D2'; m.auto_filter.ref = f'A1:R{last}'
dvP = DataValidation(type='whole', operator='between', formula1='1', formula2='3', showErrorMessage=True, error='P harus 1–3')
dvW = DataValidation(type='whole', operator='between', formula1='0', formula2='3', showErrorMessage=True, error='W harus 0–3')
m.add_data_validation(dvP); m.add_data_validation(dvW); dvP.add(f'K2:K{last}'); dvW.add(f'L2:L{last}')
for lv, col in LVL_FILL.items():
    m.conditional_formatting.add(f'A2:R{last}', FormulaRule(formula=[f'$P2="{lv}"'], fill=PatternFill('solid', fgColor=col)))
m['K1'].comment = Comment('Input: penilaian audit. Ubah sesuai bukti baru.', 'audit')
m['M1'].comment = Comment('Dari lembar Uji_Sensitivitas (maksimum skor varian dengan ID yang sama). "–" = belum diuji.', 'audit')

# ---------------- Uji_Sensitivitas ----------------
u = wb.create_sheet('Uji_Sensitivitas')
UH = ['ID data', 'Varian uji', 'Sumber/rentang', 'S2−S1 (ha)', 'S3−S2 (ha)', 'S4−S3 USD 10 (ha)', 'S4−S3 USD 20 (ha)', 'NPV USD 10 (Rp M)', 'NPV USD 20 (Rp M)',
      'Belanja/kebutuhan LPHD USD 20', 'ΔRT S4−S3 USD 10 (Rp/RT/th)', 'Emisi dihindari S4 USD 10 vs S1 (ribu tCO₂e) [info]',
      'Δ% S2−S1', 'Δ% S3−S2', 'Δ% S4−S3 USD 10', 'Δ% S4−S3 USD 20', 'Δ% NPV USD 10', 'Δ% NPV USD 20', 'Δ% belanja/kebutuhan', 'Δ% ΔRT',
      'Tanda NPV USD 10 berbalik?', 'Tanda ΔRT berbalik?', 'Efek PS/pembiayaan awal/karbon hilang atau berbalik?', 'Perubahan terbesar |Δ%|', 'P teruji', 'Catatan']
header(u, 1, UH, [8, 34, 30, 10, 10, 11, 11, 11, 11, 12, 13, 13, 9, 9, 9, 9, 9, 9, 10, 9, 11, 11, 14, 11, 8, 46])
MAP = {'Efektivitas': 'D03', 'MRV': 'D04', 'Verifikasi': 'D16', 'Delay': 'D18', 'Proporsi PA': 'D06', 'Buffer': 'D15', 'Leakage': 'D13', 'Diskonto': 'D17', 'Kapasitas': 'LAIN'}
NOTE = {'Tahun kering ekstrem aktif': 'Emisi bersih kumulatif S4 USD 10 naik 79,9 → 159,4 juta tCO₂e, tetapi deforestasi, kredit, NPV, dan kebutuhan dana tidak berubah: kebakaran tidak terhubung ke stok hutan dan kebutuhan dana (temuan struktural).',
        'Efek izin PS −0,15': 'Arah kontribusi PS berbalik (S2−S1 negatif): izin menaikkan kehilangan hutan lebih besar daripada efek patroli.',
        'Atribusi patroli 2024 ke pembiayaan awal = 0': 'Efek pembiayaan awal (S3−S2) hilang seluruhnya: bergantung penuh pada asumsi atribusi.',
        'RT bergantung 2.144': 'Indikator per RT tidak bergantung jumlah RT; total agregat tidak diuji.',
        'RT bergantung 19.038': 'Indikator per RT tidak bergantung jumlah RT; total agregat tidak diuji.',
        'Harga turun 40 % dalam 10 th lalu tetap': 'NPV USD 10 menjadi negatif.'}
data = []
fl = lambda r, k: float(r[k]) if r.get(k) not in (None, '') else None
for r in oat:
    vid = 'DASAR' if r['variant'] == 'BASE' else next(v for k, v in MAP.items() if r['variant'].startswith(k))
    data.append([vid, r['variant'], 'OAT audit (robustness_oat.csv)', fl(r, 'S2-S1 ha'), fl(r, 'S3-S2 ha'), fl(r, 'S4-S3 USD10 ha'), fl(r, 'S4-S3 USD20 ha'),
                 fl(r, 'NPV USD10 (Rp M)'), fl(r, 'NPV USD20 (Rp M)'), fl(r, 'Cakupan USD20 (%)') / 100, fl(r, 'dRT S4-S3 USD10 (Rp)'), None, ''])
base = data[0]
data.append(['D01', 'Basis kredit A2 register (CLOSURE)', 'A1_A2_BASELINE_RECONCILIATION.csv', base[3], base[4], float(a2['10']['S4_S3_ha']), float(a2['20']['S4_S3_ha']),
             float(a2['10']['NPV_proyek_10_Rp']) / 1e9, float(a2['20']['NPV_proyek_10_Rp']) / 1e9, None, None, None, 'Pembanding resmi register, direproduksi audit.'])
for pg, v in (('0', 34403), ('3,24', -205238)):
    data.append(['D02', f'Pengali kehilangan akses = {pg}', '05_SOCIOECONOMIC_RESULTS (rerata 2030–2055)', None, None, None, None, None, None, None, v, None, ''])
oat3 = list(csv.DictReader(open(os.path.join(B, '07_UNCERTAINTY', 'robustness_oat3.csv'), encoding='utf-8')))
for r in oat3:
    if r['id'] == 'DASAR': continue
    data.append([r['id'], r['variant'], r['sumber_rentang'] + ' (robustness_oat3.csv)', fl(r, 'S2-S1 ha'), fl(r, 'S3-S2 ha'), fl(r, 'S4-S3 USD10 ha'), fl(r, 'S4-S3 USD20 ha'),
                 fl(r, 'NPV USD10 (Rp M)'), fl(r, 'NPV USD20 (Rp M)'), fl(r, 'Cakupan USD20 (%)') / 100, fl(r, 'dRT S4-S3 USD10 (Rp)'),
                 fl(r, 'Emisi dihindari S4 USD10 vs S1 (ribu tCO2e)'), NOTE.get(r['variant'], '')])
NUMF = {4: '#,##0;-#,##0', 5: '#,##0;-#,##0', 6: '#,##0;-#,##0', 7: '#,##0;-#,##0', 8: '#,##0.00;-#,##0.00', 9: '#,##0.00;-#,##0.00', 10: '0.0%', 11: '#,##0;-#,##0', 12: '#,##0.0;-#,##0.0'}
for i, d in enumerate(data, 2):
    for j, v in enumerate(d[:12], 1):
        c = u.cell(i, j, v); c.font = blue if j >= 4 else fnt; c.border = box
        if j in NUMF: c.number_format = NUMF[j]
    for col, L in zip(range(13, 21), 'DEFGHIJK'):
        c = u.cell(i, col, f'=IF(OR({L}{i}="",{L}$2="",{L}$2=0),"",{L}{i}/{L}$2-1)'); c.number_format = '0.0%;-0.0%;0.0%'; c.font = fnt; c.border = box
    u.cell(i, 21, f'=IF(H{i}="","",IF(SIGN(H{i})<>SIGN(H$2),"YA","tidak"))')
    u.cell(i, 22, f'=IF(K{i}="","",IF(SIGN(K{i})<>SIGN(K$2),"YA","tidak"))')
    gone = '+'.join(f'IF({L}{i}="",0,IF(OR(SIGN({L}{i})<>SIGN({L}$2),ABS({L}{i})<0.1*ABS({L}$2)),1,0))' for L in 'DEF')
    u.cell(i, 23, f'=IF(A{i}="DASAR","",IF({gone}>0,"YA","tidak"))')
    u.cell(i, 24, '=MAX(' + ','.join(f'IF({L}{i}="",0,ABS({L}{i}))' for L in ['M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']) + ')'); u.cell(i, 24).number_format = '0.0%'
    u.cell(i, 25, f'=IF(A{i}="DASAR","",IF(OR(U{i}="YA",V{i}="YA",W{i}="YA"),3,IF(X{i}>=0.15,2,1)))')
    for col in range(21, 26):
        c = u.cell(i, col); c.font = fnt; c.alignment = center; c.border = box
    c = u.cell(i, 26, d[12]); c.font = fnt; c.alignment = wrap; c.border = box
ul = len(data) + 1
u.freeze_panes = 'C2'; u.auto_filter.ref = f'A1:Z{ul}'
u.conditional_formatting.add(f'U2:W{ul}', FormulaRule(formula=['U2="YA"'], fill=PatternFill('solid', fgColor='F8CBAD')))
u.conditional_formatting.add(f'Y2:Y{ul}', FormulaRule(formula=['Y2=3'], fill=PatternFill('solid', fgColor='F8CBAD')))
n = ul + 2
for t in ['Catatan:', 'Baris 2 (DASAR) adalah acuan semua Δ%. Kolom D–L berisi hasil run audit (huruf biru, tidak diubah). Semua varian adalah DIAGNOSTIK AUDIT, bukan hasil utama makalah.',
          'Rentang: "Dok. .mdl" = rentang yang tercatat di catatan persamaan; "UJI AUDIT" = rentang dipilih audit karena dokumentasi tidak memberi rentang.',
          'P teruji = 3 bila tanda NPV USD 10 atau ΔRT berbalik, atau S2−S1 / S3−S2 / S4−S3 USD 10 berbalik tanda atau turun di bawah 10 % nilai dasar; 2 bila perubahan terbesar ≥ 15 %; selain itu 1.',
          'NPV = NPV proyek parsial (diskonto 10 % kecuali varian diskonto), dihitung di luar model. Lintasan harga diterapkan pada Harga Karbon (REDD) saja; harga ARR tetap. "LAIN" = varian tanpa butir di Matriks.']:
    u.cell(n, 1, t).font = bold if t == 'Catatan:' else fnt; n += 1

# ---------------- Grid ----------------
g = wb.create_sheet('Grid')
g['A1'] = 'Grid pengaruh (P final) × kelemahan bukti (W): jumlah butir per sel'; g['A1'].font = title
g['A3'] = 'P final \\ W'; g['A3'].font = hfont; g['A3'].fill = hfill; g['A3'].alignment = center
for j, w in enumerate([0, 1, 2, 3], 2):
    c = g.cell(3, j, f'W = {w}'); c.font = hfont; c.fill = hfill; c.alignment = center
for i, p in enumerate([3, 2, 1], 4):
    c = g.cell(i, 1, f'P = {p}'); c.font = hfont; c.fill = hfill; c.alignment = center
    for j, w in enumerate([0, 1, 2, 3], 2):
        c = g.cell(i, j, f'=COUNTIFS(Matriks!$N$2:$N${last},{p},Matriks!$L$2:$L${last},{w})'); c.font = fnt; c.alignment = center; c.border = box
g.conditional_formatting.add('B4:E6', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='max', end_color='F4B183'))
g['A8'] = 'Level menurut sel'; g['A8'].font = bold
for j, w in enumerate([0, 1, 2, 3], 2):
    c = g.cell(9, j, f'W = {w}'); c.font = hfont; c.fill = hfill; c.alignment = center
for i, p in enumerate([3, 2, 1], 10):
    c = g.cell(i, 1, f'P = {p}'); c.font = hfont; c.fill = hfill; c.alignment = center
    for j, w in enumerate([0, 1, 2, 3], 2):
        lv = 1 if (p == 3 and w >= 2) else 2 if (p == 3 or (p == 2 and w >= 2)) else 3 if (p == 2 or (p == 1 and w >= 2)) else 4
        name = {1: '1 KRITIS', 2: '2 TINGGI', 3: '3 SEDANG', 4: '4 RENDAH'}[lv]
        c = g.cell(i, j, name); c.font = fnt; c.alignment = center; c.border = box; c.fill = PatternFill('solid', fgColor=LVL_FILL[name])
g['A14'] = 'Tabel level di atas adalah aturan tetap (dokumentasi); jumlah di grid atas dihitung dari lembar Matriks.'; g['A14'].font = fnt
g.column_dimensions['A'].width = 14
for col in 'BCDE': g.column_dimensions[col].width = 13

# ---------------- Ringkasan ----------------
s = wb.create_sheet('Ringkasan')
s['A1'] = 'Ringkasan leveling'; s['A1'].font = title
header(s, 3, ['Level', 'Jumlah butir', 'Porsi'], None)
for i, lv in enumerate(LVL_FILL, 4):
    s.cell(i, 1, lv).font = fnt; s.cell(i, 1).fill = PatternFill('solid', fgColor=LVL_FILL[lv])
    s.cell(i, 2, f'=COUNTIF(Matriks!$P$2:$P${last},A{i})').font = fnt
    c = s.cell(i, 3, f'=IF(B$8=0,0,B{i}/B$8)'); c.number_format = '0.0%'; c.font = fnt
s['A8'] = 'Total'; s['A8'].font = bold; s['B8'] = '=SUM(B4:B7)'; s['B8'].font = bold
header(s, 10, ['Status bukti dampak', 'Jumlah butir', 'Di antaranya Level 1–2'], None)
for i, st in enumerate(['REPRODUKSI AUDIT', 'NASKAH (BELUM DIVERIFIKASI)', 'BELUM DIUJI'], 11):
    s.cell(i, 1, st).font = fnt
    s.cell(i, 2, f'=COUNTIF(Matriks!$J$2:$J${last},A{i})').font = fnt
    s.cell(i, 3, f'=COUNTIFS(Matriks!$J$2:$J${last},A{i},Matriks!$P$2:$P${last},"1 KRITIS")+COUNTIFS(Matriks!$J$2:$J${last},A{i},Matriks!$P$2:$P${last},"2 TINGGI")').font = fnt
cats = sorted({r['kategori'] for r in rows})
header(s, 16, ['Kategori'] + list(LVL_FILL) + ['Total'], None)
for i, ct in enumerate(cats, 17):
    s.cell(i, 1, ct).font = fnt
    for j, lv in enumerate(LVL_FILL, 2):
        s.cell(i, j, f'=COUNTIFS(Matriks!$B$2:$B${last},$A{i},Matriks!$P$2:$P${last},"{lv}")').font = fnt
    s.cell(i, 6, f'=SUM(B{i}:E{i})').font = bold
endc = 16 + len(cats)
s.cell(endc + 2, 1, 'Konsistensi P penilaian vs P teruji').font = bold
s.cell(endc + 3, 1, 'Butir yang sudah diuji').font = fnt
s.cell(endc + 3, 2, f'=COUNTIF(Matriks!$M$2:$M${last},"<>–")').font = fnt
s.cell(endc + 4, 1, 'P penilaian = P teruji').font = fnt
s.cell(endc + 4, 2, f'=SUMPRODUCT((Matriks!$M$2:$M${last}<>"–")*(Matriks!$K$2:$K${last}=Matriks!$N$2:$N${last}))').font = fnt
s.column_dimensions['A'].width = 30
for col in 'BCDEF': s.column_dimensions[col].width = 14
ch = BarChart(); ch.type = 'col'; ch.title = 'Jumlah butir data per level'; ch.y_axis.title = 'Butir'
ch.add_data(Reference(s, min_col=2, min_row=3, max_row=7), titles_from_data=True); ch.set_categories(Reference(s, min_col=1, min_row=4, max_row=7))
ch.roundedCorners = False; ch.legend = None; ch.x_axis.delete = False; ch.y_axis.delete = False
ch.title.overlay = False; ch.y_axis.title.overlay = False; ch.height = 7; ch.width = 13
s.add_chart(ch, 'H3')

# ---------------- Prioritas ----------------
p = wb.create_sheet('Prioritas')
PH = ['ID', 'Data', 'Level', 'P final', 'W', 'Kemudahan (1–3)', 'Skor prioritas', 'Peringkat', 'Ketersediaan data', 'Cara menutup']
header(p, 1, PH, [6, 40, 12, 8, 6, 12, 11, 10, 30, 40])
def ease(t):
    t = t.lower()
    if t.startswith('tidak ada') or 'proyeksi' in t: return 1
    if t.startswith('ada') and 'tidak ada' in t: return 2
    if t.startswith('ada') or t == 'literatur' or t == '–': return 3
    return 2
for i, r in enumerate(rows, 2):
    mi = i  # baris yang sama di Matriks
    p.cell(i, 1, f'=Matriks!A{mi}').font = green
    p.cell(i, 2, f'=Matriks!C{mi}').font = green
    p.cell(i, 3, f'=Matriks!P{mi}').font = green
    p.cell(i, 4, f'=Matriks!N{mi}').font = green
    p.cell(i, 5, f'=Matriks!L{mi}').font = green
    c = p.cell(i, 6, ease(r['ketersediaan_data'])); c.font = blue; c.fill = yfill
    p.cell(i, 7, f'=D{i}*E{i}*F{i}').font = fnt
    p.cell(i, 8, f'=RANK(G{i},$G$2:$G${last},0)+COUNTIF($G$2:G{i},G{i})-1').font = fnt
    p.cell(i, 9, f'=Matriks!Q{mi}').font = green
    p.cell(i, 10, f'=Matriks!R{mi}').font = green
    for col in range(1, 11):
        c = p.cell(i, col); c.border = box; c.alignment = wrap if col in (2, 9, 10) else center
dvE = DataValidation(type='whole', operator='between', formula1='1', formula2='3', showErrorMessage=True, error='Kemudahan 1–3')
p.add_data_validation(dvE); dvE.add(f'F2:F{last}')
p.conditional_formatting.add(f'G2:G{last}', ColorScaleRule(start_type='min', start_color='FFFFFF', end_type='max', end_color='F4B183'))
for lv, col in LVL_FILL.items():
    p.conditional_formatting.add(f'C2:C{last}', FormulaRule(formula=[f'$C2="{lv}"'], fill=PatternFill('solid', fgColor=col)))
p.freeze_panes = 'C2'; p.auto_filter.ref = f'A1:J{last}'
p.cell(last + 2, 1, 'Kemudahan: 1 = data tidak ada / perlu survei baru; 2 = kemungkinan ada di arsip LPHD/proyek; 3 = ada di dokumen yang sudah dimiliki. Nilai awal = penilaian audit dari kolom ketersediaan data.').font = fnt
p.cell(last + 3, 1, 'Skor prioritas tinggi = data berpengaruh besar, buktinya lemah, dan relatif mudah diperoleh. Urutkan kolom Peringkat (filter) untuk daftar kerja.').font = fnt

for sh in wb.worksheets:
    for row in sh.iter_rows():
        for c in row:
            if c.font is None or c.font.name != F:
                c.font = Font(name=F, size=c.font.size or 10, bold=c.font.bold, color=c.font.color)
wb.save(OUT); print(OUT)
