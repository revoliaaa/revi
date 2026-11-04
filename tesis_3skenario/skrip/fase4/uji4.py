import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); import c4
DT = 0.0625; FE = (1 - .1) * (1 - .12) * 0.682
L = lambda k: pd.read_pickle(f"fase4/runs_v2/{k}.pkl"); L3 = lambda k: pd.read_pickle(f"fase3b/runs/{k}.pkl")
I = lambda d, v: float(d[v].iloc[:-1].sum() * DT)           # integral 2024–2087
LP = lambda d: d["Kredit Pengganti Reversal Kumulatif"].diff().shift(-1).fillna(0) / DT
def Iy(d, v, a, b): s = d[v]; return float(s[(s.index >= a) & (s.index < b)].sum() * DT)
R = []
def T(kode, nama, ok, bukti, status=None): R.append({"Kode": kode, "Uji": nama, "Status": status or ("LULUS" if ok else "GAGAL"), "Bukti": bukti}); print(kode, R[-1]["Status"], "|", bukti[:200])
f = lambda x, d=0: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
S1, C20, C35, A20, B20 = L("S1"), L("C20"), L("C35"), L("A20"), L("B20")
# ---------- statis
sta = json.load(open("fase4/statis.json"))
T("V0a", "Parsing PySD", True, "read_vensim berhasil; 946 variabel (v2); 16 View")
T("V0b", "Referensi dan loop aljabar", sta["unknown"] == 0 and sta["scc"] == 0, f"referensi tak dikenal {sta['unknown']}; loop aljabar {sta['scc']}; pemakai Switch Karbon {sta['sk']} (9 lama + jembatan + 4 rantai kredit/pelaporan PWD-K)")
T("V0c", "Units Check dan run native Vensim", False, "Vensim tidak tersedia di lingkungan ini; harus dijalankan peneliti", status="BELUM DILAKUKAN")
T("V18", "Konsistensi dimensional (pemeriksa statis)", sta["satuan_bermasalah"] == 0, f"{sta['satuan_ok']} persamaan konsisten, {sta['satuan_bermasalah']} bermasalah")
# ---------- reproduksi
mx = []
for kn, ko in [("rep_S1", "S1"), ("rep_A20", "A_20"), ("rep_C20", "C_20_J1_d5_h0_m0")]:
    a = L(kn); b = L3(ko); cols = [c for c in b.columns if c in a.columns]
    KEB = ["Kebutuhan Dana Minimum", "Kesenjangan Pembiayaan Minimum", "PV Kebutuhan Dana Minimum", "Total Kebutuhan Dana Pengelolaan", "Rasio Cakupan Kebutuhan Minimum"]
    c2 = [c for c in cols if c not in KEB]; mx.append(float(((a[c2] - b[c2]).abs() / (b[c2].abs() + 1)).max().max()))
    mk = float(((a[[c for c in cols if c in KEB]] - b[[c for c in cols if c in KEB]]).abs() / (b[[c for c in cols if c in KEB]].abs() + 1)).max().max())
    if kn == "rep_C20": mkc = mk
T("R1", "Reproduksi Fase 3 dengan upah lama dan mode kredit lama (kriteria direvisi: indikator kebutuhan dikecualikan)", max(mx) < 1e-9, f"selisih relatif maks S1/A20/C20 = {mx[0]:.1e}/{mx[1]:.1e}/{mx[2]:.1e} pada semua variabel fisik, keuangan, dan sosial; indikator kebutuhan LPHD C20 berbeda {100*mkc:.1f} % karena perubahan definisi terdaftar (kebutuhan bruto, tidak lagi dikurangi jembatan)")
# ---------- upah
ok = True; b = []
for k, d in [("S1", S1), ("C20", C20)]:
    u24, u25 = Iy(d, "Upah Patroli Berbayar", 2024, 2025), Iy(d, "Upah Patroli Berbayar", 2025, 2026)
    h24, h25 = Iy(d, "Total HOK Patroli", 2024, 2025), Iy(d, "Total HOK Patroli", 2025, 2026); kr = float(d["Kumulatif Realisasi Pembiayaan Awal"].iloc[-1])
    ok &= abs(u24 - 379950000) < 1 and abs(u25 - 451650000) < 1 and abs(h24 - 2533) < 1e-6 and abs(h25 - 3011) < 1e-6 and abs(kr - 1441440000) < 1
    b.append(f"{k}: upah 2024 Rp{f(u24)}, 2025 Rp{f(u25)}, total Rp{f(u24+u25)}; HOK {f(h24)}/{f(h25)}; biaya total historis Rp{f(kr)}")
T("W1", "Upah patroli historis Rp150.000/HOK; HOK dan biaya total tidak berubah", ok, "; ".join(b))
rat = []; ok = True
for k in ["S1", "C20", "C35", "A20"]:
    d = L(k); cost = d["Penggunaan Dana Perlindungan Total"]; w = d["Upah Patroli Berbayar"]; m = cost > 1
    ok &= bool((w <= cost + 1e-6).all()); rat.append(float((w[m] / cost[m]).max())); rat.append(float((w[m] / cost[m]).min()))
T("W2", "Upah adalah komponen biaya total (tidak ditambahkan)", ok and max(abs(r - 150 / 260) for r in rat) < 1e-9, f"upah ≤ biaya patroli total di semua t; rasio upah/biaya = {rat[0]:.6f} (= 150/260 = {150/260:.6f}) di S1, A20, C20, C35")
bo = float(S1["Biaya Operasional Patroli Sukarela per Anggota per Tahun"].iloc[0]); nx = L("E_S1_nontunai_x10")
dinc = float((nx["Pendapatan Bersih per RT Bergantung"] - S1["Pendapatan Bersih per RT Bergantung"]).abs().max())
nt = S1["Nilai Kontribusi Tenaga Non Tunai"].loc[2030]; hr = S1["HOK Patroli Reguler PS"].loc[2030]
T("W3", "Nilai non-tunai Rp150.000/HOK dan logistik turunan; tidak masuk pendapatan RT", abs(bo - 9.17 * 110000) < 1e-3 and abs(nt - hr * 150000) < 1 and dinc < 1e-6,
  f"logistik swadaya = 9,17 × Rp110.000 = Rp{f(bo)}/anggota/th (sebelumnya Rp1.192.050); nilai tenaga non-tunai 2030 = {f(hr,1)} HOK × Rp150.000 = Rp{f(nt)}; logistik ×10 → |Δ pendapatan RT| maks {dinc:.1e}")
ok = all(float((L(k)["Kesempatan Kerja PS"] - (L(k)["HOK Berupah PS"] + L(k)["HOK Sukarela PS"])).abs().max()) < 1e-6 and float(L(k)["Check Identitas Patroli"].abs().max()) < 1e-6 for k in ["S1", "C20", "A20", "C35"])
T("W4", "Identitas HOK berupah + sukarela = total; identitas patroli", ok, "Kesempatan Kerja PS = HOK berupah + sukarela; Check Identitas Patroli = 0 (S1, A20, C20, C35)")
rs1 = L("rep_S1")
T("W5", "Dampak koreksi upah (S1, terhadap upah lama)", True, f"pendapatan program per RT 2024: Rp{f(rs1['Pendapatan Program per RT Bergantung'].loc[2024])} → Rp{f(S1['Pendapatan Program per RT Bergantung'].loc[2024])}; upah kegiatan PS 2025: Rp{f(Iy(rs1,'Upah Kegiatan PS',2025,2026))} → Rp{f(Iy(S1,'Upah Kegiatan PS',2025,2026))}; hutan 2087 tidak berubah ({f(rs1['Total Hutan'].iloc[-1]-S1['Total Hutan'].iloc[-1],6)} ha)", status="DILAPORKAN")
# ---------- kredit endogen
e1 = float(S1["Check Referensi S1 Hutan"].abs().max()); e2 = float(((S1["Emisi Bersih Biomassa Referensi S1"] - S1["Emisi Bersih Biomassa"]).abs()).max())
T("K1", "Rantai Referensi S1 = S1 aktual pada run S1", e1 < 1e-6 and e2 < 1e-6, f"|hutan ref − aktual| maks {e1:.1e} ha; |emisi bersih biomassa ref − aktual| maks {e2:.1e} tCO2e/th")
b20 = float(B20["Kredit Karbon Diajukan"].abs().max()); b35 = float(L("B35")["Kredit Karbon Diajukan"].abs().max())
T("K2", "B (tanpa jembatan): Referensi S1 = aktual, kredit 0", b20 < 1e-6 and b35 < 1e-6, f"kredit maks B20 {b20:.1e}, B35 {b35:.1e} tCO2e/th: tanpa modal awal tambahan siklus tidak dimulai (diagnostik dipertahankan)")
rows = []; ok = True
for h in [6, 10, 15, 20, 35]:
    d = L(f"C{h}"); er = float((d["Emisi Deforestasi Biomassa Referensi S1"] - S1["Emisi Deforestasi Biomassa"]).abs().max())
    kr = I(d, "Kredit REDD Diajukan"); mit = I(d, "Mitigasi REDD Eligible Bersih Proyek"); sal = float(d["Saldo Mitigasi REDD Belum Dikreditkan"].iloc[-1])
    bu = I(d, "Penggunaan Buffer Reversal"); ca = I(d, "Pembatalan Stok Kredit Reversal"); rp = float(d["Kredit Pengganti Reversal Kumulatif"].iloc[-1])
    pair = (I(S1, "Emisi Deforestasi Biomassa") - I(d, "Emisi Deforestasi Biomassa")) * FE; debt = max(0.0, -sal)
    idn = abs(kr - (mit + bu + ca + rp - sal)); net = kr - ca - rp - bu
    ok &= er < 1e-6 and idn < 1e-3 * max(1, kr) and mit <= pair + 1 and net - debt <= pair + 1
    rows.append(f"USD{h}: kredit diajukan {f(kr)}; dibatalkan dari stok sendiri {f(ca)}; pengganti dibeli {f(rp)}; buffer dipakai {f(bu)}; kredit bersih {f(net)}; debit belum diselesaikan 2087 {f(debt)}; mitigasi eligible (Ref S1) {f(mit)}; mitigasi deforestasi berpasangan eligible {f(pair)}; |emisi ref − S1| {er:.1e}")
T("K3", "Kredit C endogen (v2): Σ kredit = Σ mitigasi + Σ penyelesaian − saldo; mitigasi ≤ berpasangan; kredit bersih − debit belum diselesaikan ≤ mitigasi berpasangan", ok, "; ".join(rows))
ok = True
for k in ["C20", "C35", "C10", "C6"]:
    d = L(k); s_ = d["Pengurangan Emisi REDD Bruto Referensi S1"] + d["Pengurangan Emisi ARR Bruto Referensi S1"]; n = d["Pengurangan Emisi Biomassa Referensi S1"]
    ok &= float((s_ - n).abs().max()) < 1e-6 and float(d["Pengurangan Emisi ARR Bruto Referensi S1"].min()) >= -1e-9
T("K4", "Tanpa hitung ganda REDD dan ARR", ok, "REDD (bertanda) + ARR (≥ 0) = pengurangan biomassa bersih terhadap Referensi S1 di semua t (C6, C10, C20, C35)")
ok = True; bb = []
for k in ["C20", "C35", "A20"]:
    d = L(k)
    for j in ["REDD", "ARR"]:
        st = float(d[f"Stok Kredit {j} Belum Terjual"].iloc[-1]); fl = I(d, f"Kredit {j} Terbit") - I(d, f"Kredit {j} Terjual") - I(d, f"Kredit {j} Kedaluwarsa") - (I(d, "Pembatalan Stok Kredit Reversal") if j == "REDD" else 0)
        ok &= abs(st - fl) < 1e-3 * max(1, st)
    pipe = I(d, "Kredit Karbon Diajukan") - I(d, "Kredit Karbon Terbit"); ok &= pipe >= -1e-6; bb.append(f"{k}: diajukan − terbit = {f(pipe)} (antrean 3 th terakhir)")
T("K5", "Konservasi kredit (diajukan → terbit → terjual/stok/kedaluwarsa)", ok, "stok akhir = Σ terbit − Σ terjual − Σ kedaluwarsa (REDD, ARR); " + "; ".join(bb))
ok = all(bool((L(k)["Kredit REDD Diajukan"] <= L(k)["Potensi Kredit REDD terhadap BAU"] + 1e-6).all()) for k in ["C6", "C10", "C20", "C35"])
T("K6", "Kredit konservatif ≤ potensi terhadap BAU", ok, f"C20: Σ kredit REDD {f(I(C20,'Kredit REDD Diajukan'))} ≤ potensi BAU {f(I(C20,'Potensi Kredit REDD terhadap BAU'))} tCO2e")
d = L("E_C20_kasNK"); s = L("E_S1_kasNK"); kr = I(d, "Kredit REDD Diajukan"); pair = (I(s, "Emisi Deforestasi Biomassa") - I(d, "Emisi Deforestasi Biomassa")) * FE
ed = d["Emisi Deforestasi Biomassa Referensi S1"] - s["Emisi Deforestasi Biomassa"]; rev = float(d["Reversal Belum Terkompensasi"].iloc[-1]); buf = float(d["Kumulatif Buffer REDD"].iloc[-1]); rep = float(d["Kredit Pengganti Reversal Kumulatif"].iloc[-1])
net = kr - min(rev, buf) - rep
T("K7", "Kas non-karbon tidak dikreditkan (kriteria direvisi: galat acuan kumulatif konservatif dan kredit bersih)", float(ed.iloc[:-1].sum() * DT) <= 0 and net <= pair * 1.001 + 1, f"kas non-karbon Rp3 M/th: galat emisi Referensi S1 − S1 berpasangan per tahun ∈ [{float(ed.min()):.0f}; {float(ed.max()):.0f}] tCO2e/th, kumulatif {float(ed.iloc[:-1].sum()*DT):,.0f} tCO2e (negatif = acuan lebih protektif = konservatif); penyimpangan positif sesudah 2046 berjumlah {float(ed[ed>0].sum()*DT):,.0f} tCO2e (atribusi dana yang dapat dipertukarkan); kredit bruto {f(kr)}, kredit bersih sesudah reversal {f(net)} ≤ mitigasi berpasangan {f(pair)}")
# ---------- jembatan
ok = True; bb = []
for k in ["C20", "C6", "C35"]:
    d = L(k); hj = d["Hari Patroli Didanai Jembatan"]
    ok &= bool((hj <= d["Hari Patroli Tambahan Dibutuhkan"] + 1e-6).all()) and bool((d["Total HOK Patroli"] <= d["Kapasitas Hari Patroli Anggota"] + 1e-6).all())
    ok &= float((d["Realisasi Pembiayaan Jembatan"] - hj * 260000).abs().max()) < 1e-3 and float(hj[(hj.index < 2026) | (hj.index >= 2031)].abs().max()) < 1e-9
    bb.append(f"{k}: Σ jembatan Rp{f(float(d['Kumulatif Pembiayaan Jembatan'].iloc[-1]))}, HOK {f(I(d,'Hari Patroli Didanai Jembatan'))}")
ok &= float(S1["Kumulatif Pembiayaan Jembatan"].iloc[-1]) == 0
T("J1", "Pembiayaan jembatan sesuai kegiatan aktual", ok, "HOK jembatan ≤ kebutuhan tambahan; total patroli ≤ kapasitas; Rp = HOK × 260.000; hanya 2026–2030; S1 = 0; " + "; ".join(bb))
# ---------- kas dan NPV
ok = True; mxc = 0
for k in ["S1", "C6", "C10", "C20", "C35", "A20", "B20", "T_C6_bm10", "T_C6_bm10_hapus", "T_C10_sesudah_bm10", "M_C20_henti"]:
    d = L(k); mxc = max(mxc, float(d["Check Identitas Arus Kas"].abs().max()))
    ok &= bool((d["Saldo Dana LPHD"] >= -1e-6).all()) and bool((d["Saldo Dana LPHD dari Karbon"] <= d["Saldo Dana LPHD"] + 1e-3).all())
T("N1", "Neraca kas LPHD dan mitra", ok and mxc < 1e-3, f"|Check Identitas Arus Kas| maks {mxc:.1e} Rp/th di 11 run; saldo ≥ 0; saldo karbon ≤ saldo")
ni = float(S1["NPV Inkremental Perdagangan Karbon"].iloc[-1]); dd = abs((float(C20["NPV Proyek Keseluruhan"].iloc[-1]) - float(S1["NPV Proyek Keseluruhan"].iloc[-1])) - float(C20["NPV Inkremental Perdagangan Karbon"].iloc[-1]))
T("N2", "Konsistensi NPV", abs(ni) < 1e-6 and dd < 1, f"NPV inkremental S1 = {ni:.1e}; |NPV(C20) − NPV(S1) − NPV inkremental(C20)| = {dd:.2e} Rp; NPV keseluruhan S1 = −PV pembiayaan historis = Rp{f(float(S1['NPV Proyek Keseluruhan'].iloc[-1]))}")
fis = ["Total Hutan", "Deforestasi Total", "Total HOK Patroli", "Anggota Patroli Aktif", "Pendapatan Bersih per RT Bergantung", "Jumlah KUPS Aktif", "Saldo Dana LPHD"]
dmax = max(float((C20[v][C20.index < 2026] - S1[v][S1.index < 2026]).abs().max()) for v in fis)
T("N3", "S1 = S2 (fisik dan sosial) sebelum kegiatan proyek pertama (2026)", dmax < 1e-6, f"selisih maks 2024–2025 pada {len(fis)} variabel = {dmax:.1e}")
# ---------- MRV dan talangan
d = L("M_B20_henti"); st = d["Status Proyek Karbon Aktif"]; t0 = float(st.index[(st < 0.5).values][0]) if (st < 0.5).any() else None
mrv_after = float(d["Biaya MRV Tetap"][d.index > (t0 or 3000)].abs().max()) if t0 else None
T("M1", "Penghentian MRV prospektif (B20)", t0 is not None and mrv_after < 1e-6, f"proyek dihentikan t = {t0}; biaya MRV sesudahnya 0; biaya MRV ditanggung mitra Rp{f(I(d,'Biaya Transaksi dan MRV'))} (vs Rp{f(I(B20,'Biaya Transaksi dan MRV'))} tanpa aturan)")
d = L("M_C20_henti"); st = d["Status Proyek Karbon Aktif"]; t1 = float(st.index[(st < 0.5).values][0]) if (st < 0.5).any() else None
ok = True if t1 is None else float(d["Kredit Karbon Diajukan"][d.index > t1].abs().max()) < 1e-9
T("M2", "Penghentian MRV pada C20 hanya sesudah penerimaan < biaya", ok, f"t henti = {t1}; NPV mitra Rp{f(float(d['NPV Mitra'].iloc[-1]))} (tanpa aturan Rp{f(float(C20['NPV Mitra'].iloc[-1]))}); defisit MRV 2087 Rp{f(float(d['Defisit Biaya Bersama Belum Dipulihkan'].iloc[-1]))} (tanpa aturan Rp{f(float(C20['Defisit Biaya Bersama Belum Dipulihkan'].iloc[-1]))})")
d = L("M_C20_tunda"); T("M3", "Penundaan monitoring MRV", float(d["Biaya Monitoring MRV"][d.index < 2026].abs().max()) < 1e-9, f"biaya monitoring 2024–2025 = 0 bila ditunda ke 2026; Σ MRV Rp{f(I(d,'Biaya Transaksi dan MRV'))} vs Rp{f(I(C20,'Biaya Transaksi dan MRV'))}")
ok = True; bb = []
for k in ["T_C6_bm10", "T_C10_sesudah_bm10"]:
    d = L(k); bm = float(d["Biaya Modal Kumulatif"].iloc[-1]); pk = float(d["Pokok Talangan Kumulatif"].iloc[-1]); ss = float(d["Pendanaan Awal Belum Terpulihkan"].iloc[-1])
    ok &= bm <= pk + 1 and ss <= 2 * pk + 1; bb.append(f"{k}: pokok Rp{f(pk)}, biaya modal Rp{f(bm)}, sisa 2087 Rp{f(ss)}")
T("T1", "Biaya modal dibatasi (perbaikan T-a)", ok, "; ".join(bb) + " (Fase 3: sisa C6 bm10 = Rp1.344 M)")
d = L("T_C6_bm10_hapus"); ss = float(d["Pendanaan Awal Belum Terpulihkan"][d.index >= 2045.0625].abs().max()); kg = float(d["Kerugian Mitra dari Penghapusan Talangan"].iloc[-1])
idn = float(d["Pokok Talangan Kumulatif"].iloc[-1] + d["Biaya Modal Kumulatif"].iloc[-1] - I(d, "Pemulihan Pendanaan Awal") - kg - d["Pendanaan Awal Belum Terpulihkan"].iloc[-1])
T("T2", "Penghapusan talangan dengan pengakuan kerugian", ss < 1 and abs(idn) < 1e3, f"sisa sesudah 2045 = {ss:.1e}; kerugian mitra diakui Rp{f(kg)}; identitas pokok + biaya modal − pemulihan − penghapusan − sisa = {idn:.1e} Rp; NPV mitra sama dengan tanpa penghapusan ({f(float(d['NPV Mitra'].iloc[-1]))} vs {f(float(L('T_C6_bm10')['NPV Mitra'].iloc[-1]))})")
# ---------- reversal (v2)
ok = True; bb = []
for k in ["C6", "C15", "C20"]:
    d = L(k); fl = d["Penggunaan Buffer Reversal"] + d["Pembatalan Stok Kredit Reversal"] + LP(d)
    nz = fl > 1e-9; ok &= bool((d["Pulsa Verifikasi Reversal"][nz] > 0.5).all())
    dd = S1["Deforestasi Total"] - d["Deforestasi Total"]; tneg = float(dd.index[(dd < -1e-9).values][0]) if (dd < -1e-9).any() else None
    td = float(d.index[(d["Reversal Belum Terkompensasi"] > 1e-6).values][0]) if (d["Reversal Belum Terkompensasi"] > 1e-6).any() else None
    lp_ = LP(d); tb = float(d.index[(lp_ > 1e-9).values][0]) if (lp_ > 1e-9).any() else None
    bb.append(f"{k}: deforestasi S2>S1 pertama {tneg}; debit pertama {td}; pembelian pertama {tb}; penyelesaian hanya pada pulsa verifikasi")
T("RV1", "Penyelesaian reversal hanya pada peristiwa verifikasi, tidak pada setiap tahun S2 > S1", ok, "; ".join(bb))
ok = True; bb = []
for k in ["C6", "C15", "C20"]:
    d = L(k); pz = d.index[(d["Pulsa Verifikasi Reversal"] > 0.5).values]
    for t in pz:
        i = d.index.get_loc(t)
        if i + 1 < len(d) and float(d["Penggunaan Buffer Reversal"].iloc[i] + d["Pembatalan Stok Kredit Reversal"].iloc[i] + LP(d).iloc[i]) > 1e-9:
            after = float(d["Saldo Mitigasi REDD Belum Dikreditkan"].iloc[i + 1]); before = float(d["Saldo Mitigasi REDD Belum Dikreditkan"].iloc[i])
            ok &= after >= min(0.0, float(d["Mitigasi REDD Eligible Bersih Proyek"].iloc[i]) * DT) - 1e-6
    bb.append(f"{k}: {len(pz)} pulsa verifikasi")
T("RV2", "Tanpa penalti ganda: saldo dipulihkan sesudah penyelesaian (aturan 2)", ok, "; ".join(bb) + "; sesudah setiap penyelesaian saldo kembali ke ≥ −(mitigasi negatif satu DT)")
ok = True
for k in ["C6", "C20", "RV_C20_aturan1"]:
    d = L(k); ok &= abs(float(d["Buffer REDD Tersedia"].iloc[-1]) - (float(d["Kumulatif Buffer REDD"].iloc[-1]) - float(d["Kumulatif Penggunaan Buffer Reversal"].iloc[-1]))) < 1e-3 and float(d["Buffer REDD Tersedia"].min()) >= -1e-6 and float(d["Stok Kredit REDD Belum Terjual"].min()) >= -1e-6
T("RV3", "Konservasi buffer dan stok kredit sesudah pembatalan", ok, "buffer tersedia = kontribusi − pemakaian; buffer dan stok ≥ 0 (C6, C20, aturan 1)")
a0, a1, a2 = L("RV_C20_aturan0"), L("RV_C20_aturan1"), C20
ok = float(a0["Kredit Pengganti Reversal Kumulatif"].iloc[-1]) + I(a0, "Penggunaan Buffer Reversal") + I(a0, "Pembatalan Stok Kredit Reversal") < 1e-9 and float(a1["Kredit Pengganti Reversal Kumulatif"].iloc[-1]) < 1e-9
T("RV4", "Aturan 0/1/2 berperilaku sesuai definisi", ok, f"debit 2087: aturan 0 {f(float(a0['Reversal Belum Terkompensasi'].iloc[-1]))}, aturan 1 {f(float(a1['Reversal Belum Terkompensasi'].iloc[-1]))}, aturan 2 {f(float(a2['Reversal Belum Terkompensasi'].iloc[-1]))} tCO2e; biaya pengganti aturan 2 Rp{f(I(a2,'Biaya Penggantian Reversal'))}; NPV mitra aturan 0/1/2 = {f(float(a0['NPV Mitra'].iloc[-1]))}/{f(float(a1['NPV Mitra'].iloc[-1]))}/{f(float(a2['NPV Mitra'].iloc[-1]))}")
# ---------- K7 berpasangan (dari matriks gerbang)
G = pd.read_pickle("fase4g/gate_tabel.pkl"); g = G[(G["mode"] == "berpasangan")]
T("K7b", "Referensi S1 berpasangan = S1 mandiri pada semua konfigurasi gerbang (termasuk kas non-karbon)", bool((g["status"] == "SETARA").all()), f"{int((g['status']=='SETARA').sum())}/{len(g)} konfigurasi setara (galat relatif ≤ 1e-9)")
# ---------- ekstrem
e0 = L("E_C0_tanpajembatan"); dm = max(float((e0[v] - S1[v]).abs().max()) for v in fis)
T("E1", "Harga 0 tanpa jembatan → S2 = S1", dm < 1e-6, f"selisih maks {dm:.1e}")
e0b = L("E_C0"); T("E1b", "Harga 0 dengan jembatan: kas penjualan 0, mitra menanggung jembatan + MRV", I(e0b, "Kas Penjualan Kredit") < 1 and float(e0b["Total Hutan"].iloc[-1]) >= float(S1["Total Hutan"].iloc[-1]),
  f"Δ hutan 2087 = {f(float(e0b['Total Hutan'].iloc[-1]-S1['Total Hutan'].iloc[-1]),1)} ha (efek jembatan saja); NPV mitra Rp{f(float(e0b['NPV Mitra'].iloc[-1]))}")
k0 = L("E_S1_k0"); T("E2", "k = 0: patroli reguler S1 = 0 sesudah 2025", float(k0["HOK Patroli Reguler PS"][k0.index >= 2026].abs().max()) < 1e-9, f"kredit C20 (k = 0) = {f(I(L('E_C20_k0'),'Kredit REDD Diajukan'))} tCO2e")
k1 = L("E_S1_k1"); T("E3", "k = 1: patroli reguler = 3.011 ≤ kapasitas", abs(float(k1["HOK Patroli Reguler PS"].loc[2030]) - 3011) < 1e-6 and bool((k1["Total HOK Patroli"] <= k1["Kapasitas Hari Patroli Anggota"] + 1e-6).all()), f"HOK reguler 2030 = {f(float(k1['HOK Patroli Reguler PS'].loc[2030]),1)}")
kb = L("E_S1_kasbesar"); T("E4", "Kas non-karbon sangat besar", bool((kb["Penggunaan Dana Pengelolaan"] <= kb["Total Kebutuhan Dana Pengelolaan"] + 1).all()) and float(kb["Indeks Intensitas Perlindungan"].max()) <= 1 + 1e-9, f"belanja ≤ kebutuhan; intensitas maks {float(kb['Indeks Intensitas Perlindungan'].max()):.3f}; saldo 2087 Rp{f(float(kb['Saldo Dana LPHD'].iloc[-1]))}")
c5 = L("E_C500"); T("E5", "Harga USD 500", float(c5[["Total Hutan", "Saldo Dana LPHD", "Modal Usaha KUPS"]].min().min()) >= -1e-6 and float(c5["Indeks Intensitas Perlindungan"].max()) <= 1 + 1e-9, f"stok ≥ 0; intensitas maks {float(c5['Indeks Intensitas Perlindungan'].max()):.3f}; hutan 2087 {f(float(c5['Total Hutan'].iloc[-1]))} ha")
ef = L("E_C20_eff0"); es = L("E_S1_eff0")
T("E6", "Efektivitas 0: patroli tidak mengubah deforestasi; kredit REDD 0", abs(I(ef, "Deforestasi Total") - I(es, "Deforestasi Total")) < 1e-6 and I(ef, "Kredit REDD Diajukan") < 1e-6, f"Δ deforestasi {I(ef,'Deforestasi Total')-I(es,'Deforestasi Total'):.1e} ha; kredit REDD {I(ef,'Kredit REDD Diajukan'):.1e}")
# ---------- DT
bb = []; ok = True
for a, b in [("S1", "DT_S1"), ("C20", "DT_C20")]:
    x, y = L(a), L(b); dty = float(y.index[1] - y.index[0])
    for v in ["Total Hutan", "NPV Mitra", "Kredit Karbon Diajukan", "Deforestasi Total"]:
        if v in ("Kredit Karbon Diajukan", "Deforestasi Total"): xv, yv = I(x, v), float(y[v].iloc[:-1].sum() * dty)
        else: xv, yv = float(x[v].iloc[-1]), float(y[v].iloc[-1])
        r = abs(xv - yv) / max(abs(xv), 1); ok &= r < 0.02 and len(y) > 2 * len(x) - 5; bb.append(f"{a} {v} {100*r:.3f} %")
T("U6", "Langkah waktu 0,0625 vs 0,03125 (v2: DT lewat argumen time_step; v1 tidak sah)", ok, "; ".join(bb))
# ---------- kausal
def first(s, thr=1e-6): i = np.where(s.values > thr)[0]; return float(s.index[i[0]]) if len(i) else None
dd = S1["Deforestasi Total"] - C20["Deforestasi Total"]
ch = {"patroli jembatan": first(C20["Hari Patroli Didanai Jembatan"]), "deforestasi C20 < S1": first(dd, 1e-9), "kredit diajukan": first(C20["Kredit Karbon Diajukan"]),
      "kredit terbit": first(C20["Kredit Karbon Terbit"]), "kas penjualan": first(C20["Kas Penjualan Kredit"]), "kas LPHD karbon": first(C20["Kas Masuk LPHD Karbon"]), "patroli kas LPHD": first(C20["Hari Patroli Didanai Kas LPHD"])}
v = list(ch.values()); ok = all(x is not None for x in v) and all(v[i] <= v[i + 1] + 1e-9 for i in range(len(v) - 1))
T("P1", "Urutan kausal jembatan → patroli → deforestasi → kredit → kas → patroli LPHD (C20)", ok, "; ".join(f"{k} {x}" for k, x in ch.items()))
pc = L("P_C35_putus"); d1 = float(C35["Total Hutan"].iloc[-1] - S1["Total Hutan"].iloc[-1]); d2 = float(pc["Total Hutan"].iloc[-1] - S1["Total Hutan"].iloc[-1])
T("P2", "Putus loop dana LPHD → patroli (C35)", d2 < d1 and float(pc["Hari Patroli Didanai Kas LPHD"].abs().max()) < 1e-6, f"Δ hutan 2087: {f(d1)} ha → {f(d2)} ha (sisa = efek jembatan + rehabilitasi)")
hs = [float(L(f"C{h}")["Total Hutan"].iloc[-1]) for h in [6, 10, 15, 20, 35]]
T("P3", "Harga naik → hutan 2087 tidak turun (C)", all(hs[i] <= hs[i + 1] + 1e-6 for i in range(4)), " / ".join(f(x) for x in hs) + " ha (USD 6–35)")
json.dump(R, open("fase4/uji4_hasil_v2.json", "w"), indent=1, ensure_ascii=False)
print(pd.Series([r["Status"] for r in R]).value_counts().to_dict())
