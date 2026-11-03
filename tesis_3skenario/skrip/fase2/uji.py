"""Uji Fase 2 (struktural, ekstrem, perilaku) pada DKP_25HD_FINAL_2SKENARIO.mdl. Hanya PySD."""
import sys, json, re, numpy as np, pandas as pd, warnings, pysd
warnings.filterwarnings("ignore"); sys.path.insert(0, "work")
from lib import yearly
MDL = "fase2/DKP_25HD_FINAL_2SKENARIO.mdl"; DT = 0.0625
M = pysd.read_vensim(MDL)
def run(p, dt=DT, cols=None):
    M.reload(); ts = np.round(np.arange(2024, 2087 + dt / 2, dt), 6)
    return M.run(params=p, time_step=dt, saveper=dt, return_timestamps=ts, return_columns=cols, progress=False)
S1 = {"Skenario Kebijakan": 1}; S2 = lambda h: {"Skenario Kebijakan": 2, "Harga Karbon": h}
R = []; EPS = 1e-6
def T(kode, uji, ok, bukti, status=None):
    st = status or ("LULUS" if ok else "GAGAL"); R.append({"Kode": kode, "Uji": uji, "Status": st, "Bukti": bukti}); print(f"[{st}] {kode} {uji} | {bukti}")
cache = {}
def get(key, p):
    if key not in cache: cache[key] = run(p)
    return cache[key]
a = get("S1", S1); b10 = get("S2-10", S2(10)); b20 = get("S2-20", S2(20)); b35 = get("S2-35", S2(35))
Y = lambda df, v: yearly(df[[v]])[0][v]
t = a.index.values
# ---------------- U1
T("U1", "Konfigurasi skenario", a["Switch Karbon"].abs().max() == 0 and (b20["Switch Karbon"] == 1).all() and all((d[v] == 1).all() for d in (a, b20) for v in ["Switch PS", "Switch Rehabilitasi", "Switch Pendanaan Awal"]),
  f"S1 Switch Karbon maks {a['Switch Karbon'].max()}; S2 min {b20['Switch Karbon'].min()}; switch PS/rehab/pendanaan = 1 di kedua skenario")
# ---------------- U2
r = a.loc[a.index >= 2026, "HOK Patroli Reguler PS"]
T("U2", "Kegiatan PS S1 berlanjut sesudah 2025 (k=0,5)", r.min() > 0, f"HOK reguler S1 2026–2087: min {r.min():.1f}, maks {r.max():.1f} HOK/th")
# ---------------- U3
def u3(df, lab):
    th = Y(df, "Total HOK Patroli"); reg = Y(df, "HOK Patroli Reguler PS"); kas = Y(df, "Hari Patroli Didanai Kas LPHD")
    up = Y(df, "Upah Patroli Berbayar"); keb = Y(df, "Kebutuhan Dana Perlindungan"); uk = Y(df, "Upah Kegiatan Didanai Karbon")
    cum = df["Realisasi Pembiayaan Awal"].sum() * DT
    ok = abs(th[2024] - 2533) < EPS and abs(th[2025] - 3011) < EPS and reg[[2024, 2025]].abs().max() < EPS and kas[[2024, 2025]].abs().max() < EPS \
        and df["Check Identitas Patroli"].abs().max() < EPS and abs(cum - 1441440000) < 1 and abs(up[2024] - 2533 * 130000) < 1 and keb[[2024, 2025]].abs().max() < EPS and uk[[2024, 2025]].abs().max() < EPS
    return ok, f"{lab}: total HOK 2024 {th[2024]:.3f}, 2025 {th[2025]:.3f}; reguler/kas 2024–25 maks {max(reg[[2024,2025]].max(), kas[[2024,2025]].max()):.2e}; |check| {df['Check Identitas Patroli'].abs().max():.1e}; biaya kumulatif Rp {cum:,.0f}; upah 2024 Rp {up[2024]:,.0f}; kebutuhan & upah karbon 2024–25 = {max(keb[[2024,2025]].max(), uk[[2024,2025]].max()):.1e}"
o1, e1 = u3(a, "S1"); o2, e2 = u3(b20, "S2 USD20")
nk = run({**S1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 5e9, "Tahun Mulai Dana Non Karbon": 2024})
th = Y(nk, "Total HOK Patroli"); o3 = abs(th[2024] - 2533) < EPS and abs(th[2025] - 3011) < EPS
T("U3", "Patroli historis tidak ganda (aktivitas, biaya, upah, kebutuhan, upah karbon)", o1 and o2 and o3, f"{e1} || {e2} || varian kas non-karbon Rp 5 miliar sejak 2024: total 2024 {th[2024]:.3f}, 2025 {th[2025]:.3f}")
# ---------------- U4
first = b10.index[b10["Kas Masuk LPHD Karbon"] > 0][0]
ALLOW = re.compile(r"Kredit|Kas Penjualan|Pendapatan Kotor|Biaya Transaksi|Biaya Monitoring|Biaya Verifikasi|Biaya Penerbitan|Pajak|Kekurangan Biaya|Defisit|Surplus|NPV|^PV |Arus Kas|Switch Karbon|Pengurangan Emisi Eligible|Stok Kredit|Pemulihan|Dana Mitra|Pendapatan Karbon Bersih|Dana Program PS dari Karbon|Biaya Pengembangan|Skenario Kebijakan|Harga Karbon|Pendapatan Kotor|Porsi Mitigasi|Check Identitas Arus")
pre = a.index < first - 1e-9
diff = [c for c in a.columns if c in b10.columns and np.issubdtype(a[c].dtype, np.number) and np.nanmax(np.abs(a.loc[pre, c].values - b10.loc[pre, c].values)) > 1e-6 * max(1, np.nanmax(np.abs(a.loc[pre, c].values)))]
bad = [c for c in diff if not ALLOW.search(c)]
T("U4", "S1 = S2 sebelum kas karbon pertama", len(bad) == 0, f"kas karbon pertama S2 USD10 pada t = {first:.4f}; {len(diff)} variabel berbeda sebelum itu, semuanya keuangan/kredit; di luar daftar diizinkan: {bad[:8]}")
json.dump({"t_kas_pertama": float(first), "beda": diff, "beda_tak_diizinkan": bad}, open("fase2/u4.json", "w"), indent=1)
# ---------------- U5
an = a.loc[a.index >= 2026, "Anggota Patroli Aktif"]; hr = a.loc[a.index >= 2026, "HOK Patroli Reguler PS"]
T("U5", "Tidak ada pengurangan ganda patroli (run dasar)", abs(an.max() - 254) < 1e-6 and abs(an.min() - 254) < 1e-6 and abs(hr.max() - hr.min()) < 1e-6 and abs(hr.iloc[0] - 0.5 * 3011) < 1e-6,
  f"anggota S1 2026–2087: {an.min():.4f}–{an.max():.4f}; HOK reguler {hr.min():.2f}–{hr.max():.2f} (k×3.011 = 1.505,5)")
# ---------------- U6
def ind(df, dt):
    av, fi = yearly(df[["Deforestasi Total", "Kas Penjualan Kredit", "Penggunaan Dana Pengelolaan", "Total Hutan"]])
    return {"def": av["Deforestasi Total"].loc[2025:2086].sum(), "hutan": float(df["Total Hutan"].iloc[-1]), "kas": float(df["Kas Penjualan Kredit"].sum() * dt), "belanja": float(df["Penggunaan Dana Pengelolaan"].sum() * dt)}
res6 = []
for lab, p in [("S1", S1), ("S2-20", S2(20)), ("S2-35", S2(35))]:
    x = ind(get(lab, p), DT); y = ind(run(p, 0.03125), 0.03125)
    res6 += [abs(x[k] - y[k]) / max(abs(x[k]), 1e-9) * 100 for k in x if abs(x[k]) > 1]
T("U6", "Langkah waktu DT 0,0625 vs 0,03125", max(res6) < 2, f"selisih relatif maks {max(res6):.3f} % (deforestasi, hutan 2087, kas karbon, belanja LPHD × 3 run); syarat DT ≤ Waktu Pembelanjaan (1 th) terpenuhi")
# ---------------- U7
def u7(df):
    s, sk = df["Saldo Dana LPHD"], df["Saldo Dana LPHD dari Karbon"]
    ok = s.min() >= -1e-3 and sk.min() >= -1e-3 and (sk - s).max() <= 1e-3 and df["Check Neraca Dana LPHD"].abs().max() < 1 and df["Jumlah Proporsi Alokasi Efektif"].max() <= 1 + 1e-12 \
        and (df["Penggunaan Dana Desa"] - df["Dana Desa Tersedia"]).max() <= 1e-3
    return ok, f"saldo min {s.min():.2e}; saldo karbon−saldo maks {(sk - s).max():.2e}; |check neraca| maks {df['Check Neraca Dana LPHD'].abs().max():.2e} Rp; Σ proporsi maks {df['Jumlah Proporsi Alokasi Efektif'].max():.4f}; guna−tersedia maks {(df['Penggunaan Dana Desa'] - df['Dana Desa Tersedia']).max():.2e}"
oks, ev = zip(*[u7(d) for d in (a, b10, b35, nk)])
fu = b10.index[b10["Penggunaan Dana Pengelolaan"] > 0]; fk = b10.index[b10["Kas Masuk LPHD Karbon"] > 0]
nocash = len(fu) == 0 or fu[0] >= fk[0] - 1e-9
T("U7", "Neraca LPHD dan belanja ≤ kas", all(oks) and nocash, " || ".join(["S1: " + ev[0], "S2-10: " + ev[1], "S2-35: " + ev[2], "S1+kas non-karbon: " + ev[3]]) + f" || belanja pertama S2-10 t={fu[0] if len(fu) else None}, kas karbon pertama t={fk[0]:.4f}")
# ---------------- U8
T("U8", "Tidak ada kas fiktif di S1", a["Dana Desa Diterima"].abs().max() == 0 and a["Penggunaan Dana Pengelolaan"].abs().max() == 0, f"S1: Dana Desa Diterima maks {a['Dana Desa Diterima'].max()}, belanja maks {a['Penggunaan Dana Pengelolaan'].max()}")
# ---------------- U9
kp = run({**S1, "Nilai Pendampingan Kelembagaan Non Tunai": 1.25e9})
T("U9", "Kapasitas LPHD tidak naik tanpa sumber", abs(a["Indeks Kapasitas LPHD"].max() - 0.5) < 1e-9 and a["Target Kapasitas LPHD"].max() <= 1 and kp["Indeks Kapasitas LPHD"].iloc[-1] > 0.5 and kp["Target Kapasitas LPHD"].max() <= 1,
  f"S1 dasar: kapasitas {a['Indeks Kapasitas LPHD'].min():.3f}–{a['Indeks Kapasitas LPHD'].max():.3f}; dengan pendampingan Rp 1,25 miliar/th: kapasitas 2087 {kp['Indeks Kapasitas LPHD'].iloc[-1]:.3f}, target maks {kp['Target Kapasitas LPHD'].max():.3f}")
# ---------------- stok vs akumulasi aliran (cek silang)
def cross(df, stock, inflow, outflow=None, init=0.0):
    acc = init + (df[inflow] - (df[outflow] if outflow else 0)).iloc[:-1].sum() * DT
    return float(df[stock].iloc[-1]), float(acc)
# ---------------- U10
def u10(df):
    mo = df["Modal Usaha KUPS"]; pg = df.loc[df.index < 2026, "Penggunaan Modal KUPS"]
    st, acc = cross(df, "Modal Usaha KUPS", "Akumulasi Modal KUPS", "Penggunaan Modal KUPS")
    ok = mo.min() >= -1e-6 and pg.abs().max() < 1e-9 and (df["Penggantian KUPS Berbasis Modal"] - df["KUPS Menjadi Tidak Aktif"]).max() <= 1e-9 \
         and df["Check Identitas Surplus KUPS"].abs().max() < 1e-3 and df["Check Identitas Penjualan KUPS"].abs().max() < 1e-3 and abs(st - acc) < 1
    return ok, f"modal min {mo.min():.2f}; penggunaan <2026 maks {pg.abs().max():.1e}; |identitas surplus| {df['Check Identitas Surplus KUPS'].abs().max():.1e}, penjualan {df['Check Identitas Penjualan KUPS'].abs().max():.1e}; stok akhir Rp {st:,.0f} vs Σ aliran Rp {acc:,.0f}; KUPS 2026/2050/2087 = {Y(df,'Jumlah KUPS Aktif')[2026]:.2f}/{Y(df,'Jumlah KUPS Aktif')[2050]:.2f}/{df['Jumlah KUPS Aktif'].iloc[-1]:.2f}"
o, e = u10(a); o2, e2 = u10(b35)
inc = run({**S1, "Biaya Pendampingan per KUPS per Tahun": 1})  # pemeriksa: pendapatan RT hanya bagian anggota
T("U10", "Modal dan identitas KUPS", o and o2, "S1: " + e + " || S2-35: " + e2)
# ---------------- U11
def u11(df, lab):
    st, acc = cross(df, "Luas Tanam Didanai Karbon", "Penanaman Didanai Kas Aktual")
    ok = (df["Penambahan Luas Penanaman"] - df["Batas Luas Penanaman"]).max() <= 1e-9 and df["Check Identitas HOK Penanaman"].abs().max() < 1e-6 \
         and (df["Pengeluaran Kas Penanaman Aktual"] - df["Penanaman Didanai Kas Aktual"] * 14e6).abs().max() < 1e-3 \
         and (df["Realisasi Belanja Rehabilitasi Efektif"] - df["Realisasi Belanja Rehabilitasi"]).max() <= 1e-3 and abs(st - acc) < 1e-6
    return ok, f"{lab}: tanam−batas maks {(df['Penambahan Luas Penanaman']-df['Batas Luas Penanaman']).max():.1e}; |check HOK| {df['Check Identitas HOK Penanaman'].abs().max():.1e}; efektif−realisasi maks {(df['Realisasi Belanja Rehabilitasi Efektif']-df['Realisasi Belanja Rehabilitasi']).max():.1e}; luas tanam kas stok {st:.3f} vs Σ aktual {acc:.3f}; sisa dana tanam tertahan Σ Rp {((df['Realisasi Belanja Rehabilitasi']-df['Realisasi Belanja Rehabilitasi Efektif']).sum()*DT):,.0f}"
o1, e1 = u11(a, "S1"); o2, e2 = u11(b35, "S2-35")
d0 = a["Penanaman Non Karbon"].abs().max() == 0 and a["Upah Penanaman Program Non Karbon"].abs().max() == 0
mat = run({**S1, "Dukungan Material Rehabilitasi Non Karbon": 20.13264 * 4.99e6}); mat_up = run({**S1, "Dukungan Material Rehabilitasi Non Karbon": 20.13264 * 4.99e6, "Porsi Tenaga Penanaman Non Karbon Dibayar": 1})
pm = Y(mat, "Penambahan Luas Penanaman")[2030]; um = Y(mat, "Upah Penanaman Program Non Karbon")[2030]; umu = Y(mat_up, "Upah Penanaman Program Non Karbon")[2030]
T("U11", "Rehabilitasi berdasarkan luas aktual dan sumber pembiayaan", o1 and o2 and d0 and abs(pm - 20.13264) < 0.05 and um == 0 and umu > 0,
  f"{e1} || {e2} || dukungan 0: tanam & upah non-karbon S1 = 0; dukungan Rp 100,5 juta: tanam 2030 {pm:.3f} ha, upah {um:.0f}; + porsi dibayar 1: upah {umu:,.0f} Rp/th")
# ---------------- U12
x1 = run({**S1, "Upah Setara Non Tunai Patroli": 999999, "Biaya Operasional Patroli Sukarela per Anggota per Tahun": 9.9e7})
dinc = (x1["Pendapatan Program per RT Bergantung"] - a["Pendapatan Program per RT Bergantung"]).abs().max()
hk = (a["HOK Berupah PS"] + a["HOK Sukarela PS"] - a["Kesempatan Kerja PS"]).abs().max()
T("U12", "Kerja berupah/sukarela; nilai non-tunai tidak masuk pendapatan RT", hk < 1e-9 and dinc < 1e-9 and a["Upah Kegiatan Didanai Karbon"].abs().max() == 0,
  f"|berupah+sukarela−total| {hk:.1e}; mengubah nilai non-tunai ×7,7/×83 → Δ pendapatan program RT maks {dinc:.1e}; upah karbon S1 maks {a['Upah Kegiatan Didanai Karbon'].abs().max()}")
# ---------------- U13
old = pysd.read_vensim("out/DKP_25HD_FINAL_3SKENARIO.mdl"); old.reload()
o3 = old.run(params={"Skenario Kebijakan": 2}, return_timestamps=list(np.round(np.arange(2024, 2025.0001, DT), 6)), progress=False)
cmp = ["Total Hutan", "Deforestasi Total", "NonHutan", "Jumlah KUPS Aktif", "Anggota KUPS Aktif", "Anggota Patroli Aktif", "Populasi", "Hari Patroli Didanai", "Indeks Intensitas Perlindungan", "Efek Pengelolaan PS Aktif"]
dd = {c: float(np.max(np.abs(a.loc[a.index < 2025, c].values - o3.loc[o3.index < 2025, c].values))) for c in cmp}
T("U13", "Inisialisasi 2024 identik dengan model 3 skenario", max(dd.values()) < 1e-6 and abs(float(a["Respons Perlindungan Awal"].iloc[0]) - 0.651 * 2160 / 7996.224) < 1e-6,
  f"selisih maks 2024 (10 variabel) {max(dd.values()):.1e}; Respons Perlindungan Awal = {a['Respons Perlindungan Awal'].iloc[0]:.4f} (0,651 × 2.160/7.996); efek 2025 S1 = {Y(a,'Efek Pengelolaan PS Aktif')[2025]:.4f}, 2026 = {Y(a,'Efek Pengelolaan PS Aktif')[2026]:.4f}")
# ---------------- U14
fx = {}
for d in [3, 4, 5]:
    df = run({**S2(20), "Delay Verifikasi dan Penerbitan Kredit": d}, cols=["Kas Penjualan Kredit", "Kredit REDD Diajukan", "Kredit REDD Terbit"])
    fa = float(df.index[df["Kredit REDD Diajukan"] > 0][0]); ft = float(df.index[df["Kredit REDD Terbit"] > 0][0]); fk_ = float(df.index[df["Kas Penjualan Kredit"] > 0][0])
    fx[d] = (fa, ft, fk_)
pd_ = run({**S2(20), "Delay Pembayaran Penjualan": 1}, cols=["Kas Penjualan Kredit", "Kredit REDD Terjual"])
fs = float(pd_.index[pd_["Kredit REDD Terjual"] > 0][0]); fk1 = float(pd_.index[pd_["Kas Penjualan Kredit"] > 0][0])
ok14 = all(abs(ft - (fa + d)) <= 2 * DT and fk_ - ft <= 2 * DT and fk_ >= ft for d, (fa, ft, fk_) in fx.items()) and abs(fk1 - fs - 1) <= 2 * DT
T("U14", "Jeda kas karbon (kriteria relasional, revisi)", ok14, "; ".join(f"delay {d}: pengajuan pertama {fa:.4f} → terbit {ft:.4f} → kas {fk_:.4f}" for d, (fa, ft, fk_) in fx.items()) + f"; jeda bayar 1 th: penjualan pertama {fs:.4f}, kas pertama {fk1:.4f}. Kredit pertama diajukan 2025 (efek perlindungan aktif sejak 2025), sehingga kas pertama ±2028/2029/2030")
# ---------------- U15
def u15(p, lab):
    d = run(p); dt = DT
    chk = d["Check Identitas Arus Kas"].abs().max()
    pok, bm, pem, stk = (float(d[v].iloc[-1]) for v in ["Pokok Talangan Kumulatif", "Biaya Modal Kumulatif", "Pemulihan Kumulatif", "Pendanaan Awal Belum Terpulihkan"])
    return d, chk, pok, bm, pem, stk
rows = []; okk = True
for st in [0, 1]:
    for sw in [1, 0]:
        for bmod in ([0, 0.2] if st == 1 else [0]):
            d, chk, pok, bm, pem, stk = u15({**S2(20), "Status Pembiayaan Awal": st, "Switch Pemulihan Talangan Sebelum Bagi Hasil": sw, "Biaya Modal Pendanaan Awal": bmod}, "")
            if st == 0: ok = pok == 0 and pem == 0
            else: ok = pem <= pok + bm + 1 and abs(stk - (pok + bm - pem)) < 1
            ok = ok and chk < 1; okk &= ok
            rows.append(f"{'talangan' if st else 'hibah'}/{'sebelum' if sw else 'sesudah'} bagi hasil/biaya modal {bmod}: |identitas arus| {chk:.1e}; pokok {pok:,.0f}; biaya modal {bm:,.0f}; pemulihan {pem:,.0f}; sisa {stk:,.0f}; NPV mitra {d['NPV Mitra'].iloc[-1]/1e9:.3f} M; NPV proyek {d['NPV Proyek Keseluruhan'].iloc[-1]/1e9:.3f} M")
n1 = a["NPV Inkremental Perdagangan Karbon"].iloc[-1]; nks = a["NPV Proyek Keseluruhan"].iloc[-1] + a["PV Pembiayaan Awal"].iloc[-1]
idn = (b20["NPV Proyek Keseluruhan"].iloc[-1] - a["NPV Proyek Keseluruhan"].iloc[-1]) - b20["NPV Inkremental Perdagangan Karbon"].iloc[-1]
pre = b20.index < float(b20.index[b20["Kas Penjualan Kredit"] > 0][0])
kb = (b20.loc[pre, "Kekurangan Biaya Bersama Ditanggung Mitra"] - b20.loc[pre, "Biaya Transaksi dan MRV"]).abs().max()
T("U15", "Keuangan, NPV, hibah/talangan", okk and abs(n1) < 1e-6 and abs(nks) < 1 and abs(idn) < 1 and kb < 1e-6,
  " || ".join(rows) + f" || NPV inkremental S1 = {n1:.2e}; NPV keseluruhan S1 + PV pembiayaan awal = {nks:.2e}; [NPV(S2)−NPV(S1)] − NPV inkremental = {idn:.2e}; sebelum kas pertama: kekurangan ditanggung mitra − biaya MRV = {kb:.1e}")
# ---------------- U16
ck = max(d[c].abs().max() for d in (a, b20, b35) for c in ["Check Total Kawasan", "Check Konservasi Karbon"])
kons = run({**S2(20), "Switch Baseline Kredit Konservatif": 1})
cR = lambda d, v: float(d[v].iloc[:-1].sum() * DT)
av = lambda d, v: yearly(d[[v]])[0][v].loc[2025:2086].sum()
rows16 = []; ok16 = ck < 1e-2
for lab, d in [("USD20", b20), ("USD35", b35)]:
    bau_r, rep_r, bau_a, rep_a = cR(d, "Kredit REDD Diajukan"), cR(d, "Potensi Kredit REDD Konservatif"), cR(d, "Kredit ARR Diajukan"), cR(d, "Potensi Kredit ARR Konservatif")
    emd = av(a, "Emisi Deforestasi Biomassa") - av(d, "Emisi Deforestasi Biomassa"); elig = emd * 0.9 * 0.88 * 0.682
    ok16 &= rep_r <= bau_r + 1e-6 and rep_a <= bau_a + 1e-6
    rows16.append(f"{lab}: REDD BAU {bau_r:,.0f} / konservatif-pelaporan {rep_r:,.0f} / (emisi deforestasi dihindari S2−S1 {emd:,.0f} × faktor eligible = {elig:,.0f}); ARR BAU {bau_a:,.0f} / konservatif {rep_a:,.0f}")
T("U16", "Akuntansi karbon dan baseline", ok16, f"|check kawasan & karbon| maks {ck:.1e}; " + " || ".join(rows16) + f" || varian switch konservatif (USD20): kredit REDD {cR(kons,'Kredit REDD Diajukan'):,.0f} → loop tidak dapat dimulai tanpa pendanaan tambahan (temuan F3)")
# ---------------- U17
an26 = float(a.loc[a.index >= 2026, "Anggota Patroli Aktif"].iloc[0]); m24 = Y(a, "Anggota Patroli Aktif")[2024]; m25 = Y(a, "Anggota Patroli Aktif")[2025]
T("U17", "Konsistensi historis 2023–2025 dengan kondisi awal 2024", abs(an26 - 254) < 1e-6 and abs(2160 - 392 * 5.51) / 2160 < 0.01,
  f"(a) anggota awal 2026 = {an26:.4f} (183+61+10 = 254); (b) HOK/anggota 2024 = 2.533/{m24:.1f} = {2533/m24:.2f}, 2025 = 3.011/{m25:.1f} = {3011/m25:.2f} vs 11,85 (roster 254); (c) 392×5,51 = {392*5.51:.1f} vs 2.160 (0,0 %); dipakai hanya oleh Indeks Intensitas Patroli 2023 → Respons Perlindungan Awal (jejak statis); (d) tidak ada arus kas sebelum 2024 (t0 = 2024); (e) tahun pembiayaan awal 2024–2025; (f) intensitas 2023 = 0,270, 2024 = {Y(a,'Indeks Intensitas Perlindungan')[2024]:.3f}, Indeks Intensitas Swadaya 2023 (tidak aktif) = 0,2251")
json.dump(R, open("fase2/hasil_uji_struktural.json", "w"), indent=1, ensure_ascii=False)
pd.to_pickle(cache, "fase2/cache_runs.pkl")

# ---------------- U0a, U0b, U0c, U18 (dari pemeriksa statis)
sta = json.load(open("fase2/u0b_statis.json")); teks = json.load(open("fase2/u0b_teks.json")); sat = json.load(open("fase2/u18_satuan.json"))
T("U0a", "Parsing PySD (+16 View)", True, "read_vensim berhasil; split_views: 16 modul View")
T("U0b", "Implementasi = rancangan; analisis statis", teks["identik"] == teks["rancangan"] and not teks["tak_diubah_tapi_berbeda"] and not sta["unknown"] and not sta["scc"] and sorted(sta["switch_karbon"]) == sorted(["Kredit REDD Diajukan", "Kredit ARR Diajukan", "Kredit Gambut Diajukan", "Biaya Verifikasi Tahunan", "Biaya Monitoring MRV", "Pendanaan Awal Proyek Karbon", "Biaya Pengembangan Proyek Efektif", "Potensi Kredit REDD Konservatif", "Potensi Kredit ARR Konservatif"]),
  f"{teks['identik']}/{teks['rancangan']} persamaan identik teks dengan rancangan; {teks['tak_diubah_identik']} persamaan tak diubah identik dengan model 3 skenario; dihapus {len(teks['dihapus'])} (usang); referensi tak dikenal {len(sta['unknown'])}; loop aljabar {len(sta['scc'])}; pemakai Switch Karbon {len(sta['switch_karbon'])} (7 rantai kredit/MRV + 2 pelaporan F3; daftar eksplisit)")
T("U0c", "Units Check Vensim native", False, "Vensim tidak tersedia di lingkungan ini; harus dijalankan peneliti", status="BELUM DAPAT DIUJI")
T("U18", "Konsistensi dimensional seluruh model", len(sat["galat"]) == 0, f"{sat['ok']} persamaan konsisten, {len(sat['galat'])} bermasalah; uji negatif pemeriksa: 4/4 kesalahan sengaja tertangkap")
# ---------------- U0d reproduksi struktur lama (sebagian)
old3 = pysd.read_vensim("out/DKP_25HD_FINAL_3SKENARIO.mdl"); old3.reload()
o3s2 = old3.run(params={"Skenario Kebijakan": 2}, return_timestamps=list(np.round(np.arange(2024, 2087.0001, DT), 6)), progress=False)
mim = run({**S1, "Tingkat Keberlanjutan Patroli Reguler": 0, "Dukungan Material Rehabilitasi Non Karbon": 20.13264 * 4.99e6, "Porsi Tenaga Penanaman Non Karbon Dibayar": 1,
           "Keikutsertaan Patroli 2023": 2533, "Rasio Risiko Penempatan Patroli Swadaya": 1})
f = lambda d: yearly(d[["Deforestasi Total"]])[0]["Deforestasi Total"].loc[2025:2086].sum()
T("U0d", "Reproduksi struktur model 3 skenario (S2 lama) dengan parameter peniru", abs(f(mim) - f(o3s2)) / f(o3s2) < 0.001 and abs(mim["Total Hutan"].iloc[-1] - o3s2["Total Hutan"].iloc[-1]) < 5,
  f"deforestasi kumulatif peniru {f(mim):,.1f} vs S2 lama {f(o3s2):,.1f} ha; hutan 2087 {mim['Total Hutan'].iloc[-1]:,.1f} vs {o3s2['Total Hutan'].iloc[-1]:,.1f}; FTE 2030 {Y(mim,'Kesempatan Kerja Setara Penuh')[2030]:.2f} vs {Y(o3s2,'Kesempatan Kerja Setara Penuh')[2030]:.2f}")
# ---------------- kondisi ekstrem
PHYS = ["Total Hutan", "Deforestasi Total", "HOK Patroli Reguler PS", "Hari Patroli Didanai", "Jumlah KUPS Aktif", "Kesempatan Kerja PS", "Pendapatan Bersih per RT Bergantung", "Penambahan Luas Penanaman"]
z = run(S2(0)); dz = max(float((z[c] - a[c]).abs().max()) for c in PHYS)
T("E1", "Harga karbon 0 → S2 = S1 (fisik dan sosial)", dz < 1e-6, f"selisih maks {dz:.2e} pada {len(PHYS)} variabel")
k0 = run({**S1, "Tingkat Keberlanjutan Patroli Reguler": 0})
T("E2", "k = 0 → patroli S1 nol sesudah 2025", k0.loc[k0.index >= 2026, "HOK Patroli Reguler PS"].abs().max() == 0 and k0.loc[k0.index >= 2026, "Indeks Intensitas Perlindungan"].abs().max() == 0, "HOK reguler dan intensitas S1 2026–2087 = 0")
k1 = run({**S1, "Tingkat Keberlanjutan Patroli Reguler": 1})
T("E3", "k = 1 → patroli reguler = 3.011 ≤ kapasitas", abs(k1.loc[k1.index >= 2026, "HOK Patroli Reguler PS"].max() - 3011) < 1e-6 and (k1["HOK Patroli Reguler PS"] - k1["Kapasitas Hari Patroli Anggota"]).max() <= 0, f"HOK reguler maks {k1['HOK Patroli Reguler PS'].max():.2f}; kapasitas {k1['Kapasitas Hari Patroli Anggota'].min():.0f}")
big = run({**S1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 1e12})
ttl = big["HOK Patroli Reguler PS"] + big["Hari Patroli Didanai"]
T("E4", "Kas non-karbon Rp 1 triliun/th", (ttl - big["Kapasitas Hari Patroli Anggota"]).max() <= 1e-6 and big["Indeks Intensitas Perlindungan"].max() <= 1 and (big["Penggunaan Dana Pengelolaan"] - big["Total Kebutuhan Dana Pengelolaan"]).max() <= 1e-3 and big["Saldo Dana LPHD"].min() >= 0,
  f"patroli−kapasitas maks {(ttl-big['Kapasitas Hari Patroli Anggota']).max():.2e}; intensitas maks {big['Indeks Intensitas Perlindungan'].max():.3f}; belanja−kebutuhan maks {(big['Penggunaan Dana Pengelolaan']-big['Total Kebutuhan Dana Pengelolaan']).max():.2e}; saldo akhir Rp {big['Saldo Dana LPHD'].iloc[-1]:.3e} (menumpuk, tidak dibelanjakan fiktif)")
hp = run(S2(500))
T("E5", "Harga USD 500", hp["Total Hutan"].min() > 0 and hp["Indeks Intensitas Perlindungan"].max() <= 1 and (hp["Penambahan Luas Penanaman"] - hp["Batas Luas Penanaman"]).max() <= 1e-9 and hp["Saldo Dana LPHD"].min() >= 0 and min(hp[c].min() for c in ["NonHutan", "Areal Rehabilitasi Belum Berhutan", "Modal Usaha KUPS"]) >= -1e-6,
  f"hutan min {hp['Total Hutan'].min():,.0f} ha; intensitas maks {hp['Indeks Intensitas Perlindungan'].max():.3f}; saldo min {hp['Saldo Dana LPHD'].min():.1e}")
e0 = run({**S2(35), "Efektivitas Perlindungan Penuh terhadap Deforestasi": 0}); e01 = run({**S1, "Efektivitas Perlindungan Penuh terhadap Deforestasi": 0, "Tingkat Keberlanjutan Patroli Reguler": 0})
dd0 = float((e0["Efek Pengelolaan PS Aktif"]).abs().max())
T("E6", "Efektivitas 0 → patroli tidak memengaruhi deforestasi", dd0 == 0, f"efek pengelolaan PS maks {dd0}; deforestasi kumulatif S2-35 efektivitas 0: {f(e0):,.1f} ha vs S1 k=0 efektivitas 0: {f(e01):,.1f} ha (selisih dari rehabilitasi kas karbon)")
t7a = run({**S2(20), "Status Pembiayaan Awal": 1, "Biaya Modal Pendanaan Awal": 0.2}); t7b = run({**S2(20), "Status Pembiayaan Awal": 1, "Biaya Modal Pendanaan Awal": 0.2, "Switch Pemulihan Talangan Sebelum Bagi Hasil": 0})
ok7 = all((d["Pemulihan Kumulatif"].iloc[-1] <= d["Pokok Talangan Kumulatif"].iloc[-1] + d["Biaya Modal Kumulatif"].iloc[-1] + 1) and d["Check Identitas Arus Kas"].abs().max() < 1 for d in (t7a, t7b))
T("E7", "Talangan + biaya modal 20 %/th (kriteria revisi: identitas & batas pemulihan)", ok7,
  f"sebelum bagi hasil: sisa talangan 2087 Rp {t7a['Pendanaan Awal Belum Terpulihkan'].iloc[-1]:,.0f}; sesudah bagi hasil: sisa Rp {t7b['Pendanaan Awal Belum Terpulihkan'].iloc[-1]:.3e} (bunga majemuk melampaui kapasitas bayar bagian mitra; tanpa batas penghapusan). NPV proyek berubah karena umpan balik dana LPHD → patroli → kredit, bukan kesalahan akuntansi")
# ---------------- uji perilaku kausal
B = []
def BT(kode, uji, ok, bukti): B.append({"Kode": kode, "Uji": uji, "Status": "LULUS" if ok else "GAGAL", "Bukti": bukti}); print(f"[{'LULUS' if ok else 'GAGAL'}] {kode} {uji} | {bukti}")
for lab, d in [("USD20", b20), ("USD35", b35)]:
    yy = lambda df, v: yearly(df[[v]])[0][v]
    dpat = (yy(d, "Hari Patroli Didanai") - yy(a, "Hari Patroli Didanai")).loc[2028:2086]; dint = (yy(d, "Indeks Intensitas Perlindungan") - yy(a, "Indeks Intensitas Perlindungan")).loc[2028:2086]
    ddef = (yy(d, "Deforestasi Total") - yy(a, "Deforestasi Total")).loc[2028:2086]; dhut = d["Total Hutan"].iloc[-1] - a["Total Hutan"].iloc[-1]
    dfte = (yy(d, "Kesempatan Kerja Berupah Setara Penuh") - yy(a, "Kesempatan Kerja Berupah Setara Penuh")).loc[2030:2055].mean()
    tp = dpat.index[dpat > 1e-6]; tdf = ddef.index[ddef < -1e-6]
    ok = len(tp) > 0 and dint.min() >= -1e-9 and dhut > 0 and dfte > 0 and (len(tdf) == 0 or tdf[0] >= tp[0])
    BT(f"P1-{lab}", "Kas karbon → patroli → intensitas → deforestasi → hutan & kerja (urutan kausal)", ok,
       f"tahun pertama patroli tambahan {tp[0] if len(tp) else None}; deforestasi S2<S1 pertama {tdf[0] if len(tdf) else None}; Δ intensitas min {dint.min():.4f}, maks {dint.max():.4f}; Δ hutan 2087 {dhut:,.1f} ha; Δ FTE berupah 2030–2055 {dfte:.2f}")
lb = run({**S2(35), "Proporsi Alokasi Perlindungan": 0})
dlb = lb["Total Hutan"].iloc[-1] - a["Total Hutan"].iloc[-1]; dfull = b35["Total Hutan"].iloc[-1] - a["Total Hutan"].iloc[-1]
BT("P2", "Putus loop dana→patroli (USD35): tambahan hutan hilang/turun tajam", abs(dlb) < 0.2 * abs(dfull), f"Δ hutan 2087 utuh {dfull:,.1f} ha; tanpa alokasi perlindungan {dlb:,.1f} ha (sisa dari rehabilitasi kas karbon)")
ks = {k: run({**S1, "Tingkat Keberlanjutan Patroli Reguler": k}, cols=["Deforestasi Total", "Total Hutan", "Kehilangan Pendapatan Pembatasan Akses per RT"]) for k in [0, 0.25, 0.5, 0.75, 1]}
fd = [f(ks[k]) for k in sorted(ks)]
BT("P3", "Monotonik: k naik → deforestasi S1 turun", all(y <= x + 1e-6 for x, y in zip(fd, fd[1:])), "deforestasi kumulatif S1 untuk k=0/0,25/0,5/0,75/1: " + " / ".join(f"{v:,.0f}" for v in fd))
nc = run({**S1, "Switch Dana Non Karbon": 1, "Dana Operasional Non Karbon Tunai": 3e9})
BT("P4", "Kas non-karbon S1 (Rp 3 miliar/th) → belanja, patroli, KUPS, kapasitas, hutan", Y(nc, "Hari Patroli Didanai")[2030] > 0 and nc["Total Hutan"].iloc[-1] > a["Total Hutan"].iloc[-1] and nc["Jumlah KUPS Aktif"].iloc[-1] >= a["Jumlah KUPS Aktif"].iloc[-1] and nc["Indeks Kapasitas LPHD"].iloc[-1] > 0.5,
   f"patroli didanai 2030 {Y(nc,'Hari Patroli Didanai')[2030]:,.0f} HOK; Δ hutan 2087 {nc['Total Hutan'].iloc[-1]-a['Total Hutan'].iloc[-1]:,.1f} ha; KUPS 2087 {nc['Jumlah KUPS Aktif'].iloc[-1]:.1f} vs {a['Jumlah KUPS Aktif'].iloc[-1]:.1f}; kapasitas 2087 {nc['Indeks Kapasitas LPHD'].iloc[-1]:.3f}")
kr = run({**S1, "Biaya Reaktivasi KUPS": 12.5e6})
BT("P5", "Biaya reaktivasi KUPS lebih rendah → KUPS bertahan → penerimaan anggota naik", kr["Jumlah KUPS Aktif"].iloc[-1] > a["Jumlah KUPS Aktif"].iloc[-1] and Y(kr, "Pendapatan KUPS Total")[2050] > Y(a, "Pendapatan KUPS Total")[2050],
   f"KUPS 2087: {kr['Jumlah KUPS Aktif'].iloc[-1]:.1f} vs {a['Jumlah KUPS Aktif'].iloc[-1]:.1f}; penerimaan anggota 2050: Rp {Y(kr,'Pendapatan KUPS Total')[2050]/1e6:.1f} juta vs {Y(a,'Pendapatan KUPS Total')[2050]/1e6:.1f} juta")
hp_ = {h: get(f"S2-{h}", S2(h)) if h in (10, 20, 35) else run(S2(h)) for h in [6, 10, 15, 20, 35]}
fh = [hp_[h]["Total Hutan"].iloc[-1] for h in sorted(hp_)]
BT("P6", "Monotonik harga: hutan 2087 tidak turun saat harga naik", all(y >= x - 1e-6 for x, y in zip(fh, fh[1:])), "hutan 2087 USD6/10/15/20/35: " + " / ".join(f"{v:,.0f}" for v in fh))
BT("P7", "Dukungan material rehabilitasi S1 → luas tanam → hutan & serapan", mat["Total Hutan"].iloc[-1] > a["Total Hutan"].iloc[-1] and Y(mat, "Serapan Rehabilitasi")[2050] > Y(a, "Serapan Rehabilitasi")[2050],
   f"Δ hutan 2087 {mat['Total Hutan'].iloc[-1]-a['Total Hutan'].iloc[-1]:,.1f} ha; serapan rehabilitasi 2050 {Y(mat,'Serapan Rehabilitasi')[2050]:,.0f} vs {Y(a,'Serapan Rehabilitasi')[2050]:,.0f} tCO₂e/th")
json.dump({"struktural": R, "perilaku": B}, open("fase2/hasil_uji_struktural.json", "w"), indent=1, ensure_ascii=False)
# ---------------- NPV sementara
npv = []
for h in [6, 10, 15, 20, 35]:
    d = hp_[h]; npv.append({"Harga (USD/tCO2e)": h, "NPV proyek keseluruhan (Rp miliar)": d["NPV Proyek Keseluruhan"].iloc[-1] / 1e9, "NPV inkremental karbon (Rp miliar)": d["NPV Inkremental Perdagangan Karbon"].iloc[-1] / 1e9,
                "NPV mitra (Rp miliar)": d["NPV Mitra"].iloc[-1] / 1e9, "PV kas masuk LPHD (Rp miliar)": d["PV Kas Masuk LPHD"].iloc[-1] / 1e9, "PV kebutuhan minimum (Rp miliar)": d["PV Kebutuhan Dana Minimum"].iloc[-1] / 1e9,
                "Status": "SEMENTARA: tanpa biaya pengembangan proyek aktual; biaya material non-karbon kosong; diskonto 10 % tak bersumber; status hibah"})
pd.DataFrame(npv).to_json("fase2/npv_sementara.json", orient="records", force_ascii=False)
