"""Pemuat data makalah Seminar Hasil final (dua skenario).

Semua angka makalah dibaca dari workbook hasil yang sudah direkonsiliasi.
Tidak ada simulasi baru yang dijalankan di sini.
"""
import os
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
W = {
    "sim": "fase4/HASIL_SIMULASI_FINAL_PWD.xlsx",
    "mc": "fase4_lanjutan/HASIL_MONTE_CARLO_PRCC_PWD.xlsx",
    "bs": "fase4_lanjutan/HASIL_BENEFIT_SHARING_PWD.xlsx",
    "d03": "fase5_validitas_empiris/HASIL_EKSPERIMEN_D0_D3.xlsx",
    "rek": "audit_akademik/TABEL_REKONSILIASI_AUDIT_AKADEMIK_PWD.xlsx",
    "reg": "fase5_validitas_empiris/REGISTER_PARAMETER_DAN_BUKTI_EMPIRIS.xlsx",
}


def p(key):
    return os.path.join(ROOT, W[key])


def sheet(key, name, **kw):
    return pd.read_excel(p(key), sheet_name=name, **kw)


RUN = sheet("sim", "1 Ringkasan per run", index_col=0)
SEL = sheet("sim", "2 Selisih S2−S1", index_col=0)
LIN = sheet("sim", "3 Lintasan tahunan")
D03 = sheet("d03", "3 Atribusi perlindungan")
MCQ = sheet("mc", "4 Ringkasan median P5-P95")
MCP = sheet("mc", "5 Proporsi ensembel")
PRCC = sheet("mc", "6 PRCC")
PRCC["Harga"] = PRCC["Harga"].ffill()
BS = sheet("bs", "2 Hasil dasar")
BSDEF = sheet("bs", "1 Definisi alternatif")
KAS20 = sheet("rek", "1 Arus kas C-J1 USD20", index_col=0)
KAS35 = sheet("rek", "2 Arus kas C-J1 USD35", index_col=0)
AKSES = sheet("rek", "5 Sensitivitas akses")
KUPS = sheet("rek", "7 Trade-off KUPS")
POP = sheet("rek", "4 Populasi RT", index_col=0)
REG = sheet("reg", "1 Register")

HARGA = [10, 20, 35]


def run(col, row):
    return float(RUN.loc[row, col])


def sel(col, row):
    return float(SEL.loc[row, col])


def lin(run_name, var):
    r = LIN[(LIN.Run == run_name) & (LIN.Variabel == var)].iloc[0]
    yrs = [c for c in LIN.columns if c not in ("Run", "Variabel")]
    return [int(y) for y in yrs], [float(r[y]) for y in yrs]


def d03(variasi, harga, col):
    r = D03[(D03.Variasi == variasi) & (D03.Harga == harga)].iloc[0]
    return float(r[col])


def mcq(harga, ind, stat):
    r = MCQ[(MCQ.Harga == harga) & (MCQ.Indikator == ind)].iloc[0]
    return float(r[stat])


def mcp(harga, prefix):
    r = MCP[(MCP.Harga == harga) & (MCP.Kriteria.str.startswith(prefix))].iloc[0]
    return float(r["Proporsi ensembel (%)"])


def bs(harga, alt, col):
    r = BS[(BS.Harga == harga) & (BS.Alternatif == alt)].iloc[0]
    return float(r[col])


def kups(harga, alt, col):
    r = KUPS[(KUPS.Harga == harga) & (KUPS.Alt == alt)].iloc[0]
    return float(r[col])


def akses(harga, m, col):
    r = AKSES[(AKSES.Harga == harga) & (abs(AKSES["Pengali akses"] - m) < 1e-9)].iloc[0]
    return float(r[col])


def kas(harga, row, col="Total 2024–2086"):
    t = KAS20 if harga == 20 else KAS35
    return float(t.loc[row, col])


def fmt(v, d=0):
    """Format Indonesia: titik ribuan, koma desimal, tanda minus tipografis."""
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 and round(abs(v), d) != 0 else "") + s
