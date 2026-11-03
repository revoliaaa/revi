import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase3"); import common
R = json.load(open("fase3b/mek_hasil.json")); RUNS = json.load(open("fase3b/runs.json")); SE = json.load(open("fase3b/setara.json"))
OUT = sys.argv[1]; W = pd.ExcelWriter(OUT, engine="openpyxl")
DT = 0.0625; L = lambda k: pd.read_pickle(f"fase3b/runs/{k.replace('|','_')}.pkl"); F = lambda d, v: float(d[v].iloc[:-1].sum() * DT)
clean = lambda x: 0.0 if isinstance(x, float) and abs(x) < 1e-3 and x == x else x
FE = (1 - .1) * (1 - .12) * 0.682
H = [6, 10, 15, 20, 35]
C1, CP = "J1|d5|h0|m0", "JP|d5|h0|m0"
pd.DataFrame({"Isi": [
 "PERBANDINGAN MEKANISME KREDIT DAN PEMBIAYAAN S2 – Fase 3 (audit additionality), dibuat 2026-11-03",
 "Model: DKP_25HD_FINAL_2SKENARIO_MEKANISME.mdl = DKP_25HD_FINAL_2SKENARIO.mdl (md5 aa1428df…, tidak ditimpa) + 11 variabel pembiayaan jembatan (default nonaktif). Dengan switch nonaktif, varian mereproduksi model 2 skenario persis (selisih 0 pada 77 variabel × 6 run; lembar 7).",
 "Hanya dua skenario kebijakan: S1 (PS dengan pembiayaan terbatas) dan S2 (PS + perdagangan karbon). A/B/C adalah eksperimen akuntansi/pembiayaan pada S2, BUKAN skenario kebijakan baru.",
 "A = kredit terhadap baseline BAU model (Switch Baseline Kredit Konservatif = 0, seperti Tahap 1).",
 "B = kredit konservatif: hanya mitigasi dari patroli tambahan yang didanai kas karbon (Switch Baseline Kredit Konservatif = 1), tanpa talangan baru.",
 "C = B + pembiayaan jembatan eksplisit dari mitra: patroli tambahan di atas patroli reguler S1 mulai 2026, dicatat sebagai talangan, dipulihkan dari surplus kredit SESUDAH pemulihan defisit MRV dan SEBELUM bagi hasil 60/40. J1 = Rp 782.860.000/th (3.011 HOK × Rp 260.000, setara tingkat pembiayaan mitra 2025); JP = kebutuhan tambahan penuh (dibatasi kapasitas anggota; ±Rp 1,69 miliar/th). d = durasi (th); h1 = berhenti saat kas karbon LPHD pertama; m = biaya modal per tahun.",
 "Parameter ekologis terkalibrasi tidak diubah. Asumsi kerja lain sama dengan Tahap 1 (k = 0,5; kas non-karbon 0; hibah untuk pembiayaan historis 2024–2025; diskonto 10 %).",
 "STATUS: hanya PySD 3.14.3; Units Check dan run native Vensim belum dilakukan. NPV berstatus SEMENTARA. Kredit model ≠ kredit terverifikasi/VCU. Kelayakan di sini adalah kelayakan menurut model, bukan uji kelayakan menurut standar karbon mana pun.",
 "Konvensi: kumulatif 2024–2086 (keuangan, kredit) atau 2025–2086 (fisik); rerata tahunan 2030–2055; Rp nominal kecuali NPV; tahun = waktu simulasi pertama (desimal = langkah DT)."]}).to_excel(W, sheet_name="0 README", index=False)
# 1 ringkasan utama
cols = {}
for h in H:
    cols[f"A USD{h}"] = R[f"A|{h}"]; cols[f"B USD{h}"] = R[f"B|{h}"]; cols[f"C-J1 USD{h}"] = R[f"C|{h}|{C1}"]; cols[f"C-JP USD{h}"] = R[f"C|{h}|{CP}"]
df = pd.DataFrame(cols).map(clean); df.insert(0, "S1 (acuan)", pd.Series(R["S1"]).map(clean)); df.index.name = "Indikator"; df.to_excel(W, sheet_name="1 Ringkasan A-B-C")
# 2 kisi C
rows = []
for k, r in R.items():
    if not k.startswith("C|"): continue
    _, h, j, d, s, m = k.split("|")
    rows.append(dict({"Harga (USD)": int(h), "Plafon": {"J1": "J1 Rp 782,86 jt/th", "JP": "JP kebutuhan penuh"}[j], "Durasi (th)": int(d[1:]), "Henti saat kas LPHD pertama": int(s[1:]), "Biaya modal (/th)": float(m[1:])}, **{x: clean(v) for x, v in r.items()}))
pd.DataFrame(rows).sort_values(["Harga (USD)", "Plafon", "Durasi (th)", "Henti saat kas LPHD pertama", "Biaya modal (/th)"]).to_excel(W, sheet_name="2 Kisi mekanisme C", index=False)
# 3 diagnostik B
dg = [("B USD20 (dasar)", "B|20", "Kredit konservatif = 0 sepanjang horizon"), ("B tanpa biaya MRV", "Dg-B-tanpaMRV|20", "Biaya MRV bukan penyebab: kredit tetap 0"),
      ("B + kas non-karbon Rp 3 M/th", "Dg-B20-kasNonKarbon", "Patroli dari kas non-karbon bukan mitigasi proyek: kredit tetap 0 (deforestasi turun sama dengan S1+kas non-karbon)"),
      ("B + 'Pendanaan Awal untuk Patroli' Rp 1 M/th, talangan", "Dg-B20-PendanaanAwalPatroli", "Variabel lama TIDAK terhubung ke patroli: tidak ada patroli, kredit 0, tetapi pokok talangan tercatat Rp 64,4 M (inkonsistensi laten)"),
      ("B + 'Besaran Pendanaan Awal Proyek Karbon' Rp 1 M/th", "Dg-B20-PendanaanAwalProyek", "Variabel lama tidak dipakai persamaan mana pun: tidak berpengaruh"),
      ("C jembatan 1 th (2026), kebutuhan penuh", "Dg-C-1th|20", "Pemicu singkat: siklus berjalan lemah, defisit MRV tidak pulih"),
      ("C jembatan 1 th, tanpa biaya MRV", "Dg-C-1th-tanpaMRV|20", "Tanpa beban MRV, pemicu 1 th cukup untuk siklus mandiri yang kecil"),
      ("C jembatan penuh 2026–2087", "Dg-C-penuh-sampai2087|20", "Batas atas: kebutuhan tambahan dibiayai terus-menerus")]
rows = []
for nm, k, cat in dg:
    r = R[k]; rows.append({"Run": nm, "Kunci": k, "Kredit REDD diajukan (tCO2e)": clean(r["Kredit REDD diajukan (tCO2e)"]), "Deforestasi dihindari S2−S1 (ha)": clean(r["Deforestasi dihindari S2−S1 (ha)"]),
        "Kas LPHD karbon (Rp)": clean(r["Kas masuk LPHD karbon (Rp)"]), "Defisit MRV 2087 (Rp)": clean(r["Defisit biaya bersama 2087 (Rp)"]), "Pokok talangan (Rp)": clean(r["Pokok talangan kumulatif (Rp)"]),
        "Sisa talangan 2087 (Rp)": clean(r["Sisa talangan 2087 (Rp)"]), "NPV mitra inkremental [SEMENTARA] (Rp)": clean(r["NPV mitra inkremental thd S1 (Rp) [SEMENTARA]"]), "Catatan": cat})
pd.DataFrame(rows).to_excel(W, sheet_name="3 Diagnostik B", index=False)
# 4 dekomposisi baseline BAU (emisi deforestasi biomassa dihindari terhadap BAU, kumulatif 2024–2086)
s1 = L("S1"); base = F(s1, "Emisi Deforestasi Biomassa Baseline"); e = lambda k: base - F(L(k), "Emisi Deforestasi Biomassa")
v = {k: e(k) for k in ["Dg-S1-tanpa-PS", "Dg-S1-k0-tanpa-mitra", "Dg-S1-k0", "Dg-S1-tanpa-patroli-mitra-2024-25", "S1", "A_20"]}
rows = [{"Komponen": "BAU model = S1 dengan Switch PS = 0 (identik dengan rantai Baseline)", "Urutan 1 (tCO2e)": v["Dg-S1-tanpa-PS"], "Urutan 2 (tCO2e)": v["Dg-S1-tanpa-PS"]},
        {"Komponen": "Sisa respons perlindungan 2023 (kondisi awal SMOOTHI)", "Urutan 1 (tCO2e)": v["Dg-S1-k0-tanpa-mitra"], "Urutan 2 (tCO2e)": v["Dg-S1-k0-tanpa-mitra"]},
        {"Komponen": "Patroli dibiayai mitra 2024–2025 (termasuk warisan rekrutmen 183→254 anggota)", "Urutan 1 (tCO2e)": v["Dg-S1-k0"] - v["Dg-S1-k0-tanpa-mitra"], "Urutan 2 (tCO2e)": v["S1"] - v["Dg-S1-tanpa-patroli-mitra-2024-25"]},
        {"Komponen": "Patroli reguler S1 pasca-2025 (k = 0,5)", "Urutan 1 (tCO2e)": v["S1"] - v["Dg-S1-k0"], "Urutan 2 (tCO2e)": v["Dg-S1-tanpa-patroli-mitra-2024-25"] - v["Dg-S1-k0-tanpa-mitra"]},
        {"Komponen": "= Total S1 terhadap BAU", "Urutan 1 (tCO2e)": v["S1"], "Urutan 2 (tCO2e)": v["S1"]},
        {"Komponen": "Tambahan S2 (A, USD 20) terhadap S1", "Urutan 1 (tCO2e)": v["A_20"] - v["S1"], "Urutan 2 (tCO2e)": v["A_20"] - v["S1"]},
        {"Komponen": "= Total S2 USD 20 terhadap BAU", "Urutan 1 (tCO2e)": v["A_20"], "Urutan 2 (tCO2e)": v["A_20"]}]
dfd = pd.DataFrame(rows); dfd["Porsi urutan 1 (%)"] = 100 * dfd["Urutan 1 (tCO2e)"] / v["A_20"]; dfd["Porsi urutan 2 (%)"] = 100 * dfd["Urutan 2 (tCO2e)"] / v["A_20"]
dfd.map(clean).to_excel(W, sheet_name="4 Dekomposisi BAU", index=False)
pd.DataFrame({"Catatan": ["Urutan 1: warisan pembiayaan mitra dihitung lebih dulu (k = 0); urutan 2: patroli reguler dihitung lebih dulu. Selisih antar-urutan muncul karena patroli reguler S1 memakai roster 254 anggota yang terbentuk selama pembiayaan mitra 2024–2025 (tanpa pembiayaan itu anggota tetap 183 dan HOK reguler 1.084,7 bukan 1.505,5).",
    "Emisi = emisi deforestasi biomassa (bruto, sebelum faktor eligible). Dekomposisi ini adalah atribusi model, bukan uji additionality standar."]}).to_excel(W, sheet_name="4 Dekomposisi BAU", startrow=len(dfd) + 3, index=False)
# 5 integritas kredit: kredit vs mitigasi tambahan terhadap tiga acuan (ex post, tanpa umpan balik)
ref2 = F(L("Dg-S1-tanpa-patroli-mitra-2024-25"), "Emisi Deforestasi Biomassa"); es1 = F(s1, "Emisi Deforestasi Biomassa")
rows = []
for h in H:
    for mk, k in [("A", f"A|{h}"), ("B", f"B|{h}"), ("C-J1", f"C|{h}|{C1}"), ("C-JP", f"C|{h}|{CP}")]:
        d = L(k); em = F(d, "Emisi Deforestasi Biomassa"); kr = R[k]["Kredit REDD diajukan (tCO2e)"]
        add_s1 = (es1 - em) * FE; add_r2 = (ref2 - em) * FE; add_bau = (base - em) * FE
        rows.append({"Harga (USD)": h, "Mekanisme": mk, "Kredit REDD diajukan model (tCO2e)": kr, "Mitigasi eligible thd BAU (tCO2e)": add_bau,
                     "Mitigasi eligible thd S1 (tCO2e)": add_s1, "Mitigasi eligible thd S1 tanpa pembiayaan mitra 2024–2025 (tCO2e)": add_r2,
                     "Rasio kredit / mitigasi thd S1": kr / add_s1 if add_s1 > 1 else (np.inf if kr > 1 else np.nan),
                     "Kredit melebihi mitigasi thd S1 (tCO2e)": max(0.0, kr - max(add_s1, 0)), "Kredit ex post konservatif = min(kredit, mitigasi thd S1) (tCO2e)": min(kr, max(add_s1, 0))})
pd.DataFrame(rows).map(clean).to_excel(W, sheet_name="5 Integritas kredit", index=False)
pd.DataFrame({"Catatan": [f"Faktor eligible REDD = (1 − leakage 0,10) × (1 − buffer 0,12) × porsi Project Area 0,682 = {FE:.4f}. Mitigasi dihitung dari emisi deforestasi biomassa; perbandingan ini ex post (tidak mengubah penerimaan dalam run).",
    "Rasio > 1 berarti kredit model melebihi mitigasi tambahan terhadap S1. Pada C, rasio 0,96–1,26 berasal dari pendekatan porsi (Porsi Mitigasi Adisional terhadap S2) yang memakai lintasan S2 sendiri; maka kredit C belum sepenuhnya konservatif dan perlu dipotong ex post (kolom terakhir)."]}).to_excel(W, sheet_name="5 Integritas kredit", startrow=len(rows) + 3, index=False)
# 6 kelayakan
rows = []
for h in H:
    for mk, k in [("A", f"A|{h}"), ("B", f"B|{h}"), ("C-J1", f"C|{h}|{C1}"), ("C-J1 m10%", f"C|{h}|J1|d5|h0|m0.1"), ("C-JP", f"C|{h}|{CP}"), ("C-JP d8", f"C|{h}|JP|d8|h0|m0")]:
        r = R[k]; d = L(k); em = F(d, "Emisi Deforestasi Biomassa"); add_s1 = (es1 - em) * FE; kr = r["Kredit REDD diajukan (tCO2e)"]
        integ = "tidak ada kredit" if kr < 1 else ("LULUS" if kr <= add_s1 * 1.0 + 1 else ("MENDEKATI (≤ 1,3×)" if kr <= 1.3 * add_s1 else "GAGAL"))
        an = common.annual(d); bertahan = an["Hari Patroli Didanai Kas LPHD"].loc[2060:2080].mean()
        rows.append({"Harga (USD)": h, "Mekanisme": mk, "Integritas kredit (kredit ≤ mitigasi thd S1)": integ,
                     "Mitra: NPV inkremental ≥ 0": "YA" if r["NPV mitra inkremental thd S1 (Rp) [SEMENTARA]"] >= 0 else "TIDAK",
                     "Talangan pulih penuh s.d. 2087": "–" if r["Pokok talangan kumulatif (Rp)"] < 1 else ("YA" if r["Sisa talangan 2087 (Rp)"] < 1e3 else "TIDAK"),
                     "Siklus bertahan (defisit MRV 2087 = 0)": "YA" if r["Defisit biaya bersama 2087 (Rp)"] < 1e3 else "TIDAK",
                     "Patroli didanai kas LPHD rerata 2060–2080 (HOK/th)": clean(float(bertahan)),
                     "NPV mitra inkremental [SEMENTARA] (Rp)": clean(r["NPV mitra inkremental thd S1 (Rp) [SEMENTARA]"]), "Sisa talangan 2087 (Rp)": clean(r["Sisa talangan 2087 (Rp)"]),
                     "Defisit MRV 2087 (Rp)": clean(r["Defisit biaya bersama 2087 (Rp)"]), "Kebutuhan pembiayaan awal/talangan (Rp)": clean(r["Pokok talangan kumulatif (Rp)"]),
                     "Eksposur kas mitra maks. (Rp)": clean(r["Eksposur kas mitra maks. di luar pembiayaan historis (Rp)"]),
                     "LPHD menerima kas karbon": "YA" if r["Kas masuk LPHD karbon (Rp)"] > 1 else "TIDAK", "Tahun kas LPHD pertama": r["Tahun kas LPHD karbon pertama"],
                     "Cakupan kebutuhan minimum 2030–2055 (%)": clean(r["Cakupan kebutuhan minimum LPHD 2030–2055 (%)"]), "Deforestasi dihindari S2−S1 (ha)": clean(r["Deforestasi dihindari S2−S1 (ha)"]),
                     "Δ FTE berupah": clean(r["Δ FTE berupah 2030–2055"]), "Δ pendapatan bersih per RT (Rp/th)": clean(r["Δ pendapatan bersih per RT 2030–2055 (Rp)"])})
pd.DataFrame(rows).to_excel(W, sheet_name="6 Kelayakan", index=False)
rows = []
for j, nm in [("J1", "C-J1"), ("JP", "C-JP")]:
    for h in [20, 22.5, 25, 27.5, 30, 32.5, 35]:
        k = f"C|{h}|{j}|d5|h0|m0" if h in (20, 35) else f"Th-C-{j}-d5|{h}"; a = common.annual(L(k)); r = R[k]
        rows.append({"Mekanisme": nm, "Harga (USD)": h, "Patroli kas LPHD 2045 (HOK/th)": float(a["Hari Patroli Didanai Kas LPHD"][2045]), "Patroli kas LPHD 2060": float(a["Hari Patroli Didanai Kas LPHD"][2060]),
                     "Patroli kas LPHD 2080": float(a["Hari Patroli Didanai Kas LPHD"][2080]), "Kebutuhan tambahan (HOK/th)": float(a["Hari Patroli Tambahan Dibutuhkan"][2060]),
                     "Deforestasi dihindari S2−S1 (ha)": r["Deforestasi dihindari S2−S1 (ha)"], "NPV mitra inkremental [SEMENTARA] (Rp)": r["NPV mitra inkremental thd S1 (Rp) [SEMENTARA]"],
                     "Defisit MRV 2087 (Rp)": r["Defisit biaya bersama 2087 (Rp)"]})
pd.DataFrame(rows).map(clean).to_excel(W, sheet_name="6b Ambang siklus mandiri", index=False)
pd.DataFrame([{"Run": k, **v} for k, v in SE.items()]).to_excel(W, sheet_name="7 Uji reproduksi varian", index=False)
pd.DataFrame([{"Kunci run": k, "Parameter": json.dumps(p, ensure_ascii=False)} for k, p in RUNS.items()]).to_excel(W, sheet_name="8 Daftar run", index=False)
W.close(); print("ok")
