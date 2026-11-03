"""Bangun DKP_25HD_FINAL_2SKENARIO.mdl dari sumber model 3 skenario (rekaman register + REV-3S) ditambah rancangan final (fase1b/usulan.py, G menimpa K/C)."""
import json, sys, re
sys.path.insert(0, "work"); sys.path.insert(0, "fase1b")
from build_mdl import build
import revisi_3s as R3
from usulan import P
OUT = sys.argv[1]
V = json.load(open("vars.json")); RR = [list(r) for r in V[1:] if r[0] not in R3.REMOVE]
# ---- sumber = model 3 skenario persis (register + REV-3S)
src = {}
for r in RR:
    r = (r + [None] * 23)[:23]
    if r[0] in R3.OVERRIDES: r[4], r[22] = R3.OVERRIDES[r[0]][0], R3.OVERRIDES[r[0]][1]
    src[r[0]] = r
for n, v, k, eq, u, c in R3.NEW:
    rr = [None] * 23; rr[0], rr[1], rr[3], rr[4], rr[6], rr[22] = n, v, k, eq, u, c; src[n] = rr
VIEW = {"S-": "16 Scenario Controls", "K1": "04 Forest Patrol Protection", "K2": "04 Forest Patrol Protection", "K3": "04 Forest Patrol Protection",
        "G1": "04 Forest Patrol Protection", "G7": "04 Forest Patrol Protection", "K13": "04 Forest Patrol Protection", "K14": "04 Forest Patrol Protection",
        "K15": "04 Forest Patrol Protection", "K4": "14 LPHD Finance Allocation", "K5": "14 LPHD Finance Allocation", "G3": "14 LPHD Finance Allocation",
        "K10": "14 LPHD Finance Allocation", "K6": "11 LPHD Institutions", "K7": "09 KUPS Economy Membership", "K8": "09 KUPS Economy Membership",
        "G4": "09 KUPS Economy Membership", "K9": "06 Forest Rehabilitation", "G5": "06 Forest Rehabilitation", "K11": "07 Demography and Employment",
        "K12": "07 Demography and Employment", "K16": "07 Demography and Employment", "K17": "07 Demography and Employment",
        "C1": "13 Carbon Finance Revenues", "C2": "13 Carbon Finance Revenues", "C4": "13 Carbon Finance Revenues", "G6": "13 Carbon Finance Revenues",
        "C3": "15 Carbon Emission Accounting", "C5": "15 Carbon Emission Accounting", "D2": "13 Carbon Finance Revenues", "F3": "15 Carbon Emission Accounting"}
TAG = "REV-2S 2026-11-03"
# ---- tambahan Fase 2 (pengendalian D2: talangan sebelum/sesudah bagi hasil)
EXTRA = {
 "Switch Pemulihan Talangan Sebelum Bagi Hasil": ("1", "Dmnl", "D2", "Desain: 1 = pemulihan talangan dari surplus sebelum 60/40; 0 = dari bagian 40 % mitra (mekanisme A1). BUKAN aturan kontraktual yang disetujui"),
 "Pemulihan Talangan Sebelum Bagi Hasil": ("Switch Pemulihan Talangan Sebelum Bagi Hasil*MIN(MAX(0, Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama), Pendanaan Awal Belum Terpulihkan/TIME STEP)", "Rupiah/Year", "D2", "dari surplus sebelum 60/40"),
 "Pemulihan Talangan Sesudah Bagi Hasil": ("(1-Switch Pemulihan Talangan Sebelum Bagi Hasil)*MIN(Dana Mitra dari Karbon, Pendanaan Awal Belum Terpulihkan/TIME STEP)", "Rupiah/Year", "D2", "dari bagian 40 % mitra (A1)"),
 "Pemulihan Pendanaan Awal": ("Pemulihan Talangan Sebelum Bagi Hasil+Pemulihan Talangan Sesudah Bagi Hasil", "Rupiah/Year", "D2", "perbaikan F1: dipecah agar tidak ada loop aljabar"),
 "Pendapatan Karbon Bersih yang Dapat Didistribusikan": ("Surplus Sebelum Pemulihan-Pemulihan Defisit Biaya Bersama-Pemulihan Talangan Sebelum Bagi Hasil", "Rupiah/Year", "D2", ""),
 "Potensi Kredit REDD Konservatif": ("Pengurangan Emisi Eligible REDD*Switch Karbon*Switch Periode Kredit*Porsi Mitigasi Adisional terhadap S2*Faktor Rekonsiliasi Reversal Kredit A2", "tCO2e/Year", "F3", "PELAPORAN: kredit REDD di atas perlindungan tingkat S1, dihitung dalam run BAU tanpa memengaruhi penerimaan (perbaikan F3: varian switch konservatif tidak dapat memulai loop)"),
 "Potensi Kredit ARR Konservatif": ("Pengurangan Emisi Eligible ARR*Switch Karbon*Switch Periode Kredit*Porsi ARR Adisional", "tCO2e/Year", "F3", "PELAPORAN"),
 "Arus Kas Mitra": ("Dana Mitra dari Karbon+Pemulihan Defisit Biaya Bersama+Pemulihan Talangan Sebelum Bagi Hasil-Kekurangan Biaya Bersama Ditanggung Mitra-Realisasi Pembiayaan Awal-Biaya Pengembangan Proyek Efektif", "Rupiah/Year", "D2", "varian sesudah bagi hasil: pemulihan dari bagian mitra sendiri bukan arus masuk tambahan"),
}
merged = dict(P)
for k, (eq, u, code, s) in EXTRA.items(): merged[k] = (eq, u, code, s)
log = []
for n, (eq, u, code, s) in merged.items():
    view = VIEW.get(code, VIEW.get(code[:2], "16 Scenario Controls"))
    if n in src:
        old = src[n][4]; src[n][4] = eq; src[n][6] = u
        src[n][22] = f"{TAG} [{code}]: {s} || Sebelumnya: {old}"; log.append((code, n, "diubah", old, eq, u, s))
    else:
        rr = [None] * 23; rr[0], rr[1], rr[3], rr[4], rr[6], rr[22] = n, view, "Auxiliary (dihitung)", eq, u, f"{TAG} [{code}]: {s}"
        if eq.startswith("INTEG("): rr[3] = "Stok"
        elif re.fullmatch(r"[\d.]+", eq): rr[3] = "Konstanta"
        src[n] = rr; log.append((code, n, "baru", "", eq, u, s))
# ---- hapus variabel yang tidak dipakai lagi dan sudah digantikan rancangan
SUPERSEDED = {"Switch Patroli Swadaya Reguler": "K1 menggantikan gerbang REV-3S", "Proporsi Penggantian Anggota Patroli Swadaya": "diganti Proporsi Penggantian Anggota Patroli (K2)",
              "Proporsi Penggantian KUPS Tanpa Dana Karbon": "diganti mekanisme modal (K7)", "Dana Program Eksogen": "diganti Dana Operasional Non Karbon Tunai (K5)",
              "Switch Dana Program Eksogen": "diganti Switch Dana Non Karbon (K5)", "Tahun Mulai Dana Eksogen": "diganti (K5)", "Tahun Akhir Dana Eksogen": "diganti (K5)",
              "Porsi Pembiayaan Awal sebagai Talangan": "diganti Status Pembiayaan Awal (C2)", "Hari Patroli Swadaya per Anggota": "angka 2.355 HOK tidak dipakai (K1)"}
names = sorted(src, key=len, reverse=True)
BIG = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(x) for x in names) + r")(?![A-Za-z0-9_])")
used = set()
for k, r in src.items():
    for m in BIG.findall(" " + re.sub(r"\s+", " ", str(r[4])) + " "):
        if m != k: used.add(m)
for n, why in SUPERSEDED.items():
    if n in src and n not in used: log.append(("hapus", n, "dihapus", src[n][4], "", src[n][6], why)); del src[n]
    elif n in src: print("PERINGATAN: masih dipakai, tidak dihapus:", n)
recs = list(src.values())
build(recs, OUT)
json.dump(log, open(OUT + ".log.json", "w"), indent=1, default=str)
print("variabel:", len(recs), "| perubahan:", len(log))
