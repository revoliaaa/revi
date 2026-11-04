"""Workbook pendukung makalah final: tabel hasil, cek angka teks, dan matriks keterlacakan.

Setiap angka di makalah dibaca ulang dari workbook sumber, diformat gaya Indonesia,
lalu dicari di naskah Markdown (cek ada/tidak).
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(__file__))
import data as D

OUTD = os.path.join(D.ROOT, "makalah_semhas_final_2skenario")
MD = open(os.path.join(OUTD, "MAKALAH_SEMINAR_HASIL_FINAL_2SKENARIO.md"), encoding="utf-8").read()
SIM = "HASIL_SIMULASI_FINAL_PWD.xlsx"
D03 = "HASIL_EKSPERIMEN_D0_D3.xlsx"
MCW = "HASIL_MONTE_CARLO_PRCC_PWD.xlsx"
BSW = "HASIL_BENEFIT_SHARING_PWD.xlsx"
REK = "TABEL_REKONSILIASI_AUDIT_AKADEMIK_PWD.xlsx"
H = Font(bold=True)
FILL = PatternFill("solid", fgColor="E8EEF4")


def hdr(ws, cols, widths=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = H; c.fill = FILL; c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths or [], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def r1(v):  # pembulatan setengah ke atas
    return float(f"{v + 1e-9:.1f}")


# ------------------------------------------------------------------ cek angka
CEK = []


def cek(label, val, dec, src, tujuan, note="", scale=1.0, sign=False):
    v = val / scale
    s = D.fmt(v, dec)
    if sign and v > 0:
        s = "+" + s
    alt = [s]
    if s[:1] in "+−":
        alt.append(s[0] + "Rp" + s[1:])
    found = next((x for x in alt if x in MD), None)
    CEK.append((tujuan, label, round(v, 6), found or s, src, "YA" if found else "TIDAK", note))


run, sel = D.run, D.sel
for h in D.HARGA:
    c = f"C-J1|{h}"
    cek(f"Deforestasi dihindari C-J1 USD{h} (ha)", -sel(c, "E Deforestasi kumulatif 2025–2086 (ha)"), 0, f"{SIM} lembar 2", "T1")
    cek(f"Δ hutan 2087 USD{h} (ha)", sel(c, "E Hutan 2087 (ha)"), 0, f"{SIM} lembar 2", "T1")
    cek(f"Emisi dihindari USD{h} (ribu tCO2e)", -sel(c, "E Emisi deforestasi biomassa kumulatif (tCO2e)"), 1, f"{SIM} lembar 2", "T1", scale=1e3)
    cek(f"Kredit REDD diajukan USD{h} (ribu tCO2e)", run(c, "F Kredit REDD diajukan (tCO2e)"), 1, f"{SIM} lembar 1", "T1", scale=1e3)
    cek(f"Kas penjualan USD{h} (Rp M)", run(c, "F Kas penjualan (Rp)"), 2, f"{SIM} lembar 1", "T2", scale=1e9)
    cek(f"Cakupan 2030–2055 USD{h} (%)", run(c, "L Cakupan kebutuhan minimum LPHD rerata 2030–2055 (%)"), 1, f"{SIM} lembar 1", "T2")
    cek(f"FTE berupah USD{h}", run(c, "S FTE berupah"), 1, f"{SIM} lembar 1", "T3")
    cek(f"Δ pendapatan RT bergantung USD{h} (Rp)", sel(c, "S Pendapatan bersih per RT bergantung (Rp/th)"), 0, f"{SIM} lembar 2", "T3")
    cek(f"Kontribusi pembiayaan awal D1−D0 USD{h} (ha)", D.d03("dasar", h, "…dari jembatan D1−D0 (ha)"), 0, f"{D03} lembar 3", "T1")
    cek(f"Aktivasi mekanisme karbon D2−D1 USD{h} (ha)", D.d03("dasar", h, "…dari penjualan D2−D1 (ha)"), 0, f"{D03} lembar 3", "T1")
    cek(f"Porsi pembiayaan awal USD{h} (%)", D.d03("dasar", h, "Porsi jembatan (%)"), 0, f"{D03} lembar 3", "T1")
    ind = "Deforestasi dihindari S2−S1 (ha)"
    for st in ("Median", "P5", "P95"):
        cek(f"MC {st} deforestasi dihindari USD{h}", D.mcq(h, ind, st), 0, f"{MCW} lembar 4", "T1")
    for pre, lab, t in (("2b", "Manfaat bersih tidak turun >10 %", "T1"), ("3a", "Kas LPHD 2075–2086 > 0", "T2"),
                        ("4b", "NPV mitra > 0", "T2")):
        cek(f"MC proporsi {lab} USD{h} (%)", r1(D.mcp(h, pre)), 1, f"{MCW} lembar 5", t, "pembulatan setengah ke atas")
    cek(f"RT terdampak Δ USD{h} (Rp)", D.akses(h, 1.0, "Δ pendapatan RT terdampak"), 0, f"{REK} lembar 5", "T3")
    g0 = D.akses(h, 0.0, "Δ pendapatan bersih/RT bergantung"); g1 = D.akses(h, 1.0, "Δ pendapatan bersih/RT bergantung")
    t0 = D.akses(h, 0.0, "Δ pendapatan RT terdampak"); t1 = D.akses(h, 1.0, "Δ pendapatan RT terdampak")
    cek(f"Pengali impas RT bergantung USD{h}", g0 / (g0 - g1), 2, f"{REK} lembar 5 (dihitung, linear)", "T3")
    cek(f"Pengali impas RT terdampak USD{h}", t0 / (t0 - t1), 2, f"{REK} lembar 5 (dihitung, linear)", "T3")
for h in (20, 35):
    c = f"C-J1|{h}"
    cek(f"Kas LPHD USD{h} (Rp M)", run(c, "F Kas LPHD karbon (Rp)"), 2, f"{SIM} lembar 1", "T2", scale=1e9)
    cek(f"Arus kas mitra S2−S1 USD{h} (Rp M)", D.kas(h, "24 Arus kas mitra S2 − S1"), 2, f"{REK} lembar {1 if h == 20 else 2}", "T2", sign=True)
    cek(f"NPV mitra inkremental USD{h} (Rp M) [SEMENTARA]", sel(c, "F NPV mitra (Rp) [SEMENTARA]"), 2, f"{SIM} lembar 2", "T2", scale=1e9, sign=True)
    cek(f"Biaya bersama total USD{h} (Rp M)", D.kas(h, "8 Total biaya bersama periode berjalan"), 2, f"{REK}", "T2")
cek("Biaya dibayar dari kas USD20 (Rp M)", D.kas(20, "1a Kas penjualan diterima") - D.kas(20, "9 Surplus sebelum pemulihan"), 2, REK, "T2")
cek("Pemulihan defisit MRV USD20 (Rp M)", D.kas(20, "11 Pemulihan defisit MRV historis"), 2, REK, "T2")
cek("Talangan jembatan (Rp M)", D.kas(20, "12 Pemulihan talangan jembatan"), 2, REK, "T2")
cek("Bagian mitra USD20 (Rp M)", D.kas(20, "15 Bagian mitra 40 %"), 2, REK, "T2")
cek("Biaya ditalangi mitra USD20 (Rp M)", D.kas(20, "10 Kekurangan biaya ditalangi mitra"), 2, REK, "T2")
cek("NPV inkremental proyek USD20 (Rp M) [SEMENTARA]", sel("C-J1|20", "F NPV inkremental karbon (Rp) [SEMENTARA]"), 2, f"{SIM} lembar 2", "T2", scale=1e9, sign=True)
cek("Biaya kredit pengganti USD20 (Rp M)", run("C-J1|20", "F Biaya kredit pengganti reversal (Rp)"), 2, f"{SIM} lembar 1", "T1", scale=1e9)
cek("Defisit MRV 2087 USD10 (Rp M)", run("C-J1|10", "F Defisit MRV ditalangi mitra 2087 (Rp)"), 2, f"{SIM} lembar 1", "T2", scale=1e9)
cek("Defisit MRV 2087 USD20 (Rp M)", run("C-J1|20", "F Defisit MRV ditalangi mitra 2087 (Rp)"), 2, f"{SIM} lembar 1", "T2", scale=1e9)
cek("Deforestasi S1 2025–2086 (ha)", run("S1", "E Deforestasi kumulatif 2025–2086 (ha)"), 0, f"{SIM} lembar 1", "T1")
cek("Hutan S1 2087 (ha)", run("S1", "E Hutan 2087 (ha)"), 0, f"{SIM} lembar 1", "T1")
cek("Laju deforestasi S1 2030–2055 (ha/th)", run("S1", "E Laju deforestasi rerata 2030–2055 (ha/th)"), 0, f"{SIM} lembar 1", "T1")
cek("FTE 2060–2086 USD35", run("C-J1|35", "S FTE berupah rerata 2060–2086"), 1, f"{SIM} lembar 1", "T3")
cek("KUPS aktif 2087 S1", run("S1", "S KUPS aktif 2087"), 1, f"{SIM} lembar 1", "T3")
cek("Δ KUPS aktif 2087 USD35", sel("C-J1|35", "S KUPS aktif 2087"), 1, f"{SIM} lembar 2", "T3")
cek("Δ penerimaan anggota KUPS USD35 (Rp juta)", sel("C-J1|35", "S Penerimaan anggota KUPS (Rp/th)"), 1, f"{SIM} lembar 2", "T3", scale=1e6)
cek("Δ pendapatan hutan per RT USD20 (Rp)", D.akses(20, 1.0, "Δ pendapatan hutan/RT"), 0, f"{REK} lembar 5", "T3")
cek("Δ kehilangan akses per RT USD20 (Rp)", D.akses(20, 1.0, "Δ kehilangan/RT bergantung"), 0, f"{REK} lembar 5", "T3")
cek("Δ bersih pengali 0 USD20 (Rp)", D.akses(20, 0.0, "Δ pendapatan bersih/RT bergantung"), 0, f"{REK} lembar 5", "T3", sign=True)
cek("PRCC efektivitas USD20 (deforestasi)", float(D.PRCC[(D.PRCC.Harga == 20) & (D.PRCC.Parameter == "Efektivitas Perlindungan Penuh terhadap Deforestasi")]["Deforestasi dihindari S2−S1 (ha)"].iloc[0]), 2, f"{MCW} lembar 6", "T1", sign=True)
cek("PRCC pengali akses USD20 (Δ pendapatan RT bergantung)", float(D.PRCC[(D.PRCC.Harga == 20) & (D.PRCC.Parameter == "Pengali Kehilangan Akses")]["Δ pendapatan bersih per RT bergantung (Rp/th)"].iloc[0]), 2, f"{MCW} lembar 6", "T3")
for al in ("B0", "R1", "R2", "B4"):
    cek(f"KUPS aktif 2087 {al} USD35", D.kups(35, al, "KUPS aktif 2087"), 1, f"{REK} lembar 7", "T4")
    cek(f"Deforestasi dihindari {al} USD35 (ha)", D.bs(35, al, "Deforestasi dihindari S2−S1 (ha)"), 0, f"{BSW} lembar 2", "T4")
    cek(f"Rasio kompensasi {al} USD35 (%)", D.bs(35, al, "Rasio kompensasi thd kehilangan akses total (%)"), 1, f"{BSW} lembar 2", "T4")
cek("Kompensasi kumulatif R1 USD35 (Rp M)", D.bs(35, "R1", "Kompensasi kumulatif (Rp)"), 1, f"{BSW} lembar 2", "T4", scale=1e9)
cek("Kompensasi per RT terdampak R1 USD35 (Rp)", D.bs(35, "R1", "Kompensasi per RT terdampak (Rp/th)"), 0, f"{BSW} lembar 2", "T4")
cek("Penerimaan anggota R1 USD35 (Rp juta)", D.kups(35, "R1", "Penerimaan anggota (Rp juta/th)"), 1, f"{REK} lembar 7", "T4")
cek("Modal KUPS 2087 R1 USD35 (Rp juta)", D.kups(35, "R1", "Modal usaha KUPS 2087 (Rp juta)"), 1, f"{REK} lembar 7", "T4")
cek("Kompensasi kumulatif tertinggi USD20 (Rp M)", max(D.bs(20, a, "Kompensasi kumulatif (Rp)") for a in ("B1", "B2", "B3", "B4", "R1", "R2")), 2, f"{BSW} lembar 2", "T4", scale=1e9)

# ------------------------------------------------------------------ workbook tabel
wb = Workbook()
ws = wb.active; ws.title = "README"
for line in [
    "TABEL HASIL FINAL MAKALAH SEMINAR HASIL (dua skenario, C-J1)",
    "Semua nilai dibaca dari workbook final; tidak ada simulasi baru. Skrip: skrip/makalah_final/xlsx_makalah.py",
    "Status: terverifikasi PySD; Vensim native BELUM DIVERIFIKASI; NPV SEMENTARA.",
    "Kredit model bukan kredit terverifikasi; FTE bukan jumlah orang; kas LPHD bukan pendapatan RT;",
    "proporsi ensembel bukan probabilitas empiris; S2 − S1 = proyeksi model, bukan estimasi kausal.",
]:
    ws.append([line])
ws.column_dimensions["A"].width = 110

ws = wb.create_sheet("Tabel 2 Hasil utama")
hdr(ws, ["Indikator", "S1", "S2 USD 10", "S2 USD 20", "S2 USD 35", "Sumber (baris)"], [52, 14, 14, 14, 14, 60])
cols = ["S1", "C-J1|10", "C-J1|20", "C-J1|35"]
spec = [
    ("Deforestasi dihindari thd S1 (ha)", lambda c: -sel(c, "E Deforestasi kumulatif 2025–2086 (ha)"), "E Deforestasi kumulatif (lembar 2, tanda dibalik)"),
    ("Δ luas hutan 2087 thd S1 (ha)", lambda c: sel(c, "E Hutan 2087 (ha)"), "E Hutan 2087 (ha) (lembar 2)"),
    ("Emisi dihindari (ribu tCO2e)", lambda c: -sel(c, "E Emisi deforestasi biomassa kumulatif (tCO2e)") / 1e3, "E Emisi deforestasi biomassa kumulatif (lembar 2)"),
    ("Kredit model REDD diajukan (ribu tCO2e)", lambda c: run(c, "F Kredit REDD diajukan (tCO2e)") / 1e3, "F Kredit REDD diajukan"),
    ("Kas penjualan (Rp miliar)", lambda c: run(c, "F Kas penjualan (Rp)") / 1e9, "F Kas penjualan (Rp)"),
    ("Kas LPHD karbon (Rp miliar)", lambda c: run(c, "F Kas LPHD karbon (Rp)") / 1e9, "F Kas LPHD karbon (Rp)"),
    ("Tahun dengan kas LPHD > 0 (dari 62)", lambda c: run(c, "L Tahun dengan kas LPHD > 0 (2025–2086)"), "L Tahun dengan kas LPHD > 0"),
    ("Cakupan kebutuhan minimum 2030–2055 (%)", lambda c: run(c, "L Cakupan kebutuhan minimum LPHD rerata 2030–2055 (%)"), "L Cakupan … 2030–2055"),
    ("Cakupan kebutuhan minimum 2060–2086 (%)", lambda c: run(c, "L Cakupan kebutuhan minimum LPHD rerata 2060–2086 (%)"), "L Cakupan … 2060–2086"),
    ("Defisit MRV ditalangi mitra 2087 (Rp miliar)", lambda c: run(c, "F Defisit MRV ditalangi mitra 2087 (Rp)") / 1e9, "F Defisit MRV ditalangi mitra 2087"),
    ("NPV mitra inkremental [SEMENTARA] (Rp miliar)", lambda c: sel(c, "F NPV mitra (Rp) [SEMENTARA]") / 1e9 if c != "S1" else None, "F NPV mitra (lembar 2)"),
    ("Kapasitas LPHD 2087", lambda c: run(c, "L Kapasitas LPHD 2087"), "L Kapasitas LPHD 2087"),
    ("Kerja berupah 2030–2055 (FTE)", lambda c: run(c, "S FTE berupah"), "S FTE berupah"),
    ("Kerja berupah 2060–2086 (FTE)", lambda c: run(c, "S FTE berupah rerata 2060–2086"), "S FTE berupah rerata 2060–2086"),
    ("KUPS aktif 2087", lambda c: run(c, "S KUPS aktif 2087"), "S KUPS aktif 2087"),
    ("Penerimaan anggota KUPS (Rp juta/th)", lambda c: run(c, "S Penerimaan anggota KUPS (Rp/th)") / 1e6, "S Penerimaan anggota KUPS"),
    ("Δ pendapatan bersih RT bergantung (ribu Rp/RT/th)", lambda c: sel(c, "S Pendapatan bersih per RT bergantung (Rp/th)") / 1e3 if c != "S1" else None, "S Pendapatan bersih per RT bergantung (lembar 2)"),
]
for lab, f, src in spec:
    vals = []
    for c in cols:
        try:
            v = f(c)
        except KeyError:
            v = None
        vals.append(None if v is None or (c == "S1" and "thd S1" in lab) else v)
    ws.append([lab] + vals + [f"{SIM}: {src}"])

ws = wb.create_sheet("Gambar 3b D0-D3")
hdr(ws, ["Harga (USD)", "Pembiayaan awal D1−D0 (ha)", "Aktivasi mekanisme karbon D2−D1 (ha)", "Paket lengkap D2−D0 (ha)", "Porsi pembiayaan awal (%)", "D3 kredit (tCO2e)"], [12, 24, 30, 22, 22, 18])
for h in D.HARGA:
    ws.append([h, D.d03("dasar", h, "…dari jembatan D1−D0 (ha)"), D.d03("dasar", h, "…dari penjualan D2−D1 (ha)"),
               D.d03("dasar", h, "Deforestasi dihindari D2−D0 (ha)"), D.d03("dasar", h, "Porsi jembatan (%)"),
               D.d03("dasar", h, "D3 kredit (tCO2e)")])

ws = wb.create_sheet("Gambar 3a dan 4b lintasan")
hdr(ws, ["Run", "Variabel"] + [str(y) for y in D.lin("S1", "Total Hutan")[0]], [16, 36] + [11] * 13)
for rn in ["S1", "C-J1 USD10", "C-J1 USD20", "C-J1 USD35"]:
    for var in ["Total Hutan", "Rasio Cakupan Kebutuhan Minimum", "Kas Masuk LPHD Karbon"]:
        ws.append([rn, var] + D.lin(rn, var)[1])

ws = wb.create_sheet("Gambar 4a arus kas")
hdr(ws, ["Komponen (Rp miliar, 2024–2086)", "USD 20", "USD 35"], [48, 14, 14])
for lab, f in [("Kas penjualan", lambda h: D.kas(h, "1a Kas penjualan diterima")),
               ("Biaya dibayar dari kas", lambda h: D.kas(h, "1a Kas penjualan diterima") - D.kas(h, "9 Surplus sebelum pemulihan")),
               ("Pemulihan defisit MRV", lambda h: D.kas(h, "11 Pemulihan defisit MRV historis")),
               ("Pemulihan talangan jembatan", lambda h: D.kas(h, "12 Pemulihan talangan jembatan")),
               ("Kas LPHD (60 %)", lambda h: D.kas(h, "14 Bagian LPHD 60 %")),
               ("Bagian mitra (40 %)", lambda h: D.kas(h, "15 Bagian mitra 40 %")),
               ("Total biaya bersama", lambda h: D.kas(h, "8 Total biaya bersama periode berjalan")),
               ("Biaya ditalangi mitra (di luar kas)", lambda h: D.kas(h, "10 Kekurangan biaya ditalangi mitra")),
               ("Arus kas mitra nominal S2 − S1", lambda h: D.kas(h, "24 Arus kas mitra S2 − S1"))]:
    ws.append([lab, f(20), f(35)])

ws = wb.create_sheet("Gambar 5 akses")
hdr(ws, list(D.AKSES.columns) + ["Pengali impas RT bergantung", "Pengali impas RT terdampak"], [10, 12, 18, 14, 22, 26, 24, 22, 22])
for h in D.HARGA:
    g0 = D.akses(h, 0.0, "Δ pendapatan bersih/RT bergantung"); g1 = D.akses(h, 1.0, "Δ pendapatan bersih/RT bergantung")
    t0 = D.akses(h, 0.0, "Δ pendapatan RT terdampak"); t1 = D.akses(h, 1.0, "Δ pendapatan RT terdampak")
    for _, r in D.AKSES[D.AKSES.Harga == h].iterrows():
        ws.append(list(r.values) + [g0 / (g0 - g1), t0 / (t0 - t1)])

ws = wb.create_sheet("Tabel 3 alokasi USD35")
hdr(ws, ["Indikator", "B0", "R1", "R2", "B4", "Sumber"], [46, 14, 14, 14, 14, 50])
alts = ["B0", "R1", "R2", "B4"]
for lab, f, src in [
    ("Deforestasi dihindari thd S1 (ha)", lambda a: D.bs(35, a, "Deforestasi dihindari S2−S1 (ha)"), BSW),
    ("Kas LPHD karbon (Rp miliar)", lambda a: D.bs(35, a, "Kas LPHD karbon (Rp)") / 1e9, BSW),
    ("Kapasitas LPHD 2087", lambda a: D.bs(35, a, "Kapasitas LPHD 2087"), BSW),
    ("KUPS aktif 2087", lambda a: D.kups(35, a, "KUPS aktif 2087"), REK),
    ("Penerimaan anggota KUPS (Rp juta/th)", lambda a: D.kups(35, a, "Penerimaan anggota (Rp juta/th)"), REK),
    ("Modal usaha KUPS 2087 (Rp juta)", lambda a: D.kups(35, a, "Modal usaha KUPS 2087 (Rp juta)"), REK),
    ("Kompensasi kumulatif (Rp miliar)", lambda a: D.bs(35, a, "Kompensasi kumulatif (Rp)") / 1e9, BSW),
    ("Kompensasi thd kehilangan akses total (%)", lambda a: D.bs(35, a, "Rasio kompensasi thd kehilangan akses total (%)"), BSW),
    ("Kehilangan akses per RT terdampak (ribu Rp/th)", lambda a: D.bs(35, a, "Kehilangan per RT terdampak (Rp/th)") / 1e3, BSW),
    ("Pendapatan bersih RT terdampak (Rp juta/th)", lambda a: D.bs(35, a, "Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)") / 1e6, BSW),
]:
    ws.append([lab] + [f(a) for a in alts] + [src])

ws = wb.create_sheet("Gambar 7 MC")
hdr(ws, ["Harga", "Indikator", "P5", "P25", "Median", "P75", "P95"], [8, 40, 12, 12, 12, 12, 12])
for h in D.HARGA:
    ind = "Deforestasi dihindari S2−S1 (ha)"
    ws.append([h, ind] + [D.mcq(h, ind, s) for s in ("P5", "P25", "Median", "P75", "P95")])
ws.append([])
ws.append(["Proporsi ensembel (%)", "Kriteria", "USD 10", "USD 20", "USD 35"])
for k in sorted(D.MCP.Kriteria.unique(), key=lambda x: (len(x.split()[0]), x)):
    ws.append(["", k] + [float(D.MCP[(D.MCP.Harga == h) & (D.MCP.Kriteria == k)]["Proporsi ensembel (%)"].iloc[0]) for h in D.HARGA])

ws = wb.create_sheet("Cek angka teks")
hdr(ws, ["Tujuan", "Angka", "Nilai sumber", "Format di naskah", "Sumber", "Ditemukan di naskah", "Catatan"], [7, 56, 16, 14, 46, 12, 30])
for row in CEK:
    ws.append(list(row))
for wsx in wb.worksheets[1:]:
    for row in wsx.iter_rows(min_row=2):
        for c in row:
            if isinstance(c.value, float):
                c.number_format = "#,##0.00"
wb.save(os.path.join(OUTD, "TABEL_HASIL_FINAL_MAKALAH.xlsx"))
miss = [r for r in CEK if r[5] == "TIDAK"]
print("cek", len(CEK), "tidak ditemukan", len(miss))
for r in miss:
    print("  ", r[1], r[3])

# ------------------------------------------------------------------ matriks keterlacakan
wb = Workbook(); ws = wb.active; ws.title = "Matriks"
hdr(ws, ["Tujuan", "Indikator", "Tabel/Gambar", "Sumber data", "Temuan utama (naskah)", "Kesimpulan terkait", "Status bukti"],
    [26, 40, 18, 44, 70, 50, 28])
M = [
    ("T1 Ekologi", "Deforestasi dihindari S2−S1; Δ hutan 2087; emisi dihindari", "Tabel 2; Gambar 3a", f"{SIM} lembar 1–3",
     "287 / 454 / 4.954 ha (USD 10/20/35); Δ hutan 2087 176 / 313 / 4.842 ha; non-permanensi pada USD ≤ 20", "Simpulan 1", "Proyeksi model (PySD); kelas D: efektivitas, jembatan"),
    ("T1 Ekologi", "Dekomposisi D1−D0 dan D2−D1; D3", "Gambar 3b", f"{D03} lembar 3",
     "Pembiayaan awal 287 ha; aktivasi mekanisme karbon 0 / 167 / 4.667 ha; porsi pembiayaan awal 100 / 63 / 6 %; D3 tanpa kredit", "Simpulan 1; Saran (1)", "Identitas aritmetis model, bukan identifikasi kausal"),
    ("T1 Ekologi", "Sebaran MC dan PRCC", "Gambar 7", f"{MCW} lembar 4–6",
     "Deforestasi dihindari > 0 pada 100 % sampel; median 403 / 682 / 4.710 ha; PRCC efektivitas +0,83", "Simpulan 1", "Proporsi ensembel, bukan probabilitas"),
    ("T2 Pembiayaan", "Penggunaan kas penjualan; arus kas mitra S2−S1; NPV", "Gambar 4a; Tabel 2", f"{REK} lembar 1–2; {SIM}",
     "USD 20: kas 29,07 → LPHD 7,69, mitra −10,08 nominal (NPV −0,27); USD 35: LPHD 214,33, mitra +142,89 (NPV +6,66)", "Simpulan 2; Saran (1)–(2)", "NPV SEMENTARA; tarif MRV dan kurs asumsi"),
    ("T2 Pembiayaan", "Cakupan kebutuhan minimum; tahun kas LPHD > 0; kapasitas", "Gambar 4b; Tabel 2", f"{SIM} lembar 1, 3",
     "Cakupan 2030–2055: 0 / 5,2 / 38,1 %; kas LPHD 0 / 17 / 55 dari 62 tahun; kapasitas 0,50 → 0,87 hanya pada USD 35", "Simpulan 2; Saran pemerintah", "Definisi kebutuhan minimum = asumsi peneliti (kelas D)"),
    ("T3 Sosial-ekonomi", "FTE berupah; KUPS aktif; penerimaan anggota", "Tabel 2", f"{SIM} lembar 1–2",
     "FTE +0,4 / 2,7 / 17,4; KUPS 2087 S1 5,7, +44,7 pada USD 35", "Simpulan 3", "FTE ≠ orang; parameter KUPS kelas D"),
    ("T3 Sosial-ekonomi", "Dekomposisi pendapatan RT; sensitivitas pengali akses; titik impas", "Gambar 5", f"{REK} lembar 5; {MCW} lembar 6",
     "Δ bersih −270 / −17.909 / −132.944 Rp; titik impas 0,99 / 0,75 / 0,46 (RT bergantung); PRCC pengali akses −0,89", "Simpulan 3; Saran data", "Bersyarat; kehilangan akses = asumsi kelas D belum tervalidasi"),
    ("T4 Distribusi", "Perlindungan, KUPS, kompensasi, pendapatan RT terdampak, kapasitas per alternatif", "Tabel 3; Gambar 6", f"{BSW} lembar 2; {REK} lembar 6–7",
     "R1 = B0 dalam perlindungan (konstruksi); KUPS 50,4 → 13,6; kompensasi Rp31,4 M (12,4 %); R2 hutan tertinggi, RT terdampak terendah; B4 rasio kompensasi 18,9 %", "Simpulan 4; Saran (3)", "Eksperimen alokasi, bukan kesepakatan aktual; R1 tidak optimal"),
]
for r in M:
    ws.append(list(r))
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
ws2 = wb.create_sheet("Cek angka per tujuan")
hdr(ws2, ["Tujuan", "Jumlah angka diperiksa", "Ditemukan di naskah", "Tidak ditemukan (dilaporkan)"], [10, 22, 22, 26])
for t in ("T1", "T2", "T3", "T4"):
    rows = [r for r in CEK if r[0] == t]
    ws2.append([t, len(rows), sum(r[5] == "YA" for r in rows), sum(r[5] == "TIDAK" for r in rows)])
wb.save(os.path.join(OUTD, "MATRIKS_KETERLACAKAN_TUJUAN_HASIL.xlsx"))
print("OK")
