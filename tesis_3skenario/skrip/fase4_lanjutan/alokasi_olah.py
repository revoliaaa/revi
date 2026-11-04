import sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "fase3"); import common
sys.path.insert(0, "fase5"); from alokasi import ALT, P, VAR
OUTX, OUTG = sys.argv[1], sys.argv[2]
R = pd.read_pickle("fase5/alokasi_runs.pkl"); DT = 0.0625
def met(d, s):
    an, a1 = common.annual(d), common.annual(s); A = lambda an_, v, a=2030, b=2055: float(an_[v].loc[a:b].mean())
    F = lambda x, v: float(x[v].iloc[:-1].sum() * DT); E = lambda x, v: float(x[v].iloc[-1])
    dkehil = F(d, "Kehilangan Pendapatan Agregat") - F(s, "Kehilangan Pendapatan Agregat"); komp = E(d, "Kumulatif Realisasi Kompensasi")
    keb = A(an, "Kebutuhan Dana Minimum")
    return {"Deforestasi dihindari S2−S1 (ha)": F(s, "Deforestasi Total") - F(d, "Deforestasi Total"), "Δ hutan 2087 (ha)": E(d, "Total Hutan") - E(s, "Total Hutan"),
            "HOK berupah PS (2030–2055)": A(an, "HOK Berupah PS"), "Upah kegiatan PS (Rp/th)": A(an, "Upah Kegiatan PS"), "FTE berupah": A(an, "Kesempatan Kerja Berupah Setara Penuh"),
            "KUPS aktif rerata": A(an, "Jumlah KUPS Aktif"), "KUPS aktif 2087": E(d, "Jumlah KUPS Aktif"), "Penerimaan anggota KUPS (Rp/th)": A(an, "Pendapatan KUPS Total"),
            "Pendapatan bersih per RT bergantung (Rp/th)": A(an, "Pendapatan Bersih per RT Bergantung"), "Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)": A(an, "Pendapatan Bersih per RT Terdampak"),
            "Pendapatan bersih per RT tidak terdampak (Rp/th)": A(an, "Pendapatan Bersih per RT Tidak Terdampak"), "Kehilangan per RT terdampak (Rp/th)": A(an, "Kehilangan per RT Terdampak"),
            "Kompensasi per RT terdampak (Rp/th)": A(an, "Kompensasi per RT Terdampak"), "Rasio kompensasi thd kehilangan akses total (%)": 100 * A(an, "Rasio Kompensasi terhadap Kehilangan Akses"),
            "Kompensasi kumulatif (Rp)": komp, "Rasio kompensasi thd TAMBAHAN kehilangan S2−S1 (%)": 100 * komp / dkehil if dkehil > 1 else np.nan,
            "Kas LPHD karbon (Rp)": F(d, "Kas Masuk LPHD Karbon"), "Cakupan kebutuhan minimum pengelolaan 2030–2055 (%)": 100 * A(an, "Penggunaan Dana Pengelolaan") / keb if keb else np.nan,
            "Belanja perlindungan (Rp/th)": A(an, "Realisasi Belanja Perlindungan"), "Belanja KUPS (Rp/th)": A(an, "Realisasi Belanja Pengembangan KUPS"),
            "Kapasitas LPHD 2087": E(d, "Indeks Kapasitas LPHD"), "NPV mitra inkremental [SEMENTARA] (Rp)": E(d, "NPV Mitra") - E(s, "NPV Mitra"),
            "_cek_anggaran_min": float(d["Check Anggaran Alokasi"].min()), "_saldo_min": float(d["Saldo Dana LPHD"].min()), "_neraca_maks": float(d["Check Neraca Dana LPHD"].abs().max()),
            "_penggunaan_lebih": float((d["Penggunaan Dana Desa"] - d["Dana Desa Tersedia"]).max()), "_porsi": float(d["Jumlah Porsi Dana Fleksibel"].iloc[0]),
            "_kompensasi_diterima_selisih": float((d["Kompensasi per RT Terdampak"] * d["RT Terdampak Akses"] - d["Realisasi Kompensasi RT Terdampak"]).abs().max()),
            "_ref": float((d["Total Hutan Referensi S1"] - s["Total Hutan"]).abs().max())}
rows = []
for (var, h), r in R.items():
    for alt in ALT: rows.append(dict({"Variasi": var, "Harga": h, "Alternatif": alt}, **met(r[alt], r["S1"])))
df = pd.DataFrame(rows)
IND = [c for c in df.columns if c not in ("Variasi", "Harga", "Alternatif") and not c.startswith("_")]
b0 = df[df["Alternatif"] == "B0"].set_index(["Variasi", "Harga"])
dB = df.copy()
for c in IND: dB[c] = df.apply(lambda r: r[c] - b0.loc[(r["Variasi"], r["Harga"]), c], axis=1)
# uji R1 (kriteria ditetapkan sebelum hasil): pendapatan RT terdampak R1 > B0 dan deforestasi R1 ≤ B0 + 1 ha
r1 = dB[dB["Alternatif"] == "R1"][["Variasi", "Harga", "Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)", "Deforestasi dihindari S2−S1 (ha)", "Pendapatan bersih per RT bergantung (Rp/th)", "Penerimaan anggota KUPS (Rp/th)"]].copy()
r1["R1 lulus"] = (r1["Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)"] > 0) & (r1["Deforestasi dihindari S2−S1 (ha)"] >= -1)
cekA = df[["Variasi", "Harga", "Alternatif"] + [c for c in df.columns if c.startswith("_")]]
okA = bool((cekA["_cek_anggaran_min"] >= -1).all() and (cekA["_saldo_min"] >= -1e-3).all() and (cekA["_neraca_maks"] < 1).all() and (cekA["_penggunaan_lebih"] <= 1).all() and (cekA["_kompensasi_diterima_selisih"] < 1).all() and (cekA["_ref"] < 1e-6).all())
W = pd.ExcelWriter(OUTX, engine="openpyxl")
pd.DataFrame({"Isi": ["EKSPERIMEN BENEFIT SHARING – MODEL_FINAL_DUA_SKENARIO_PWD_v2_ALOKASI.mdl (v2 + struktur dana fleksibel dan kompensasi); S2 mekanisme C (J1) dengan Referensi S1 berpasangan; USD 10, 20, 35; sensitivitas pada USD 20.",
 "B0 = alokasi proporsional dasar (operasional 0,10; perlindungan 0,30; rehabilitasi 0,15; kelembagaan 0,15; KUPS 0,20; kebakaran 0,10), tanpa kompensasi. B0 identik dengan model v2 (selisih 0).",
 "B1–B4, R1, R2: operasional dan kelembagaan tetap proporsional; sisa = dana fleksibel dibagi porsi (patroli, rehabilitasi, kebakaran, KUPS, kompensasi) dan dibatasi kebutuhan tiap pos. Kompensasi dibayar dari saldo LPHD (mengurangi Penggunaan Dana Desa) dan diterima RT pemegang garapan terdampak.",
 "Identitas anggaran diuji: Σ alokasi ≤ dana tersedia; penggunaan ≤ dana tersedia; saldo ≥ 0; neraca saldo; kompensasi yang dibayar = kompensasi yang diterima RT terdampak. Hasil: " + ("SEMUA TERPENUHI" if okA else "ADA PELANGGARAN (lihat lembar 6)"),
 "Uji R1 (kriteria sebelum hasil): R1 lulus bila pendapatan bersih RT terdampak > B0 DAN deforestasi dihindari tidak lebih buruk dari B0 (toleransi 1 ha). Hasil R1 model empat skenario lama TIDAK dipakai.",
 "STATUS: PySD; Vensim native BELUM DIVERIFIKASI; NPV SEMENTARA; kompensasi menutup kehilangan TOTAL (S2), rasio terhadap tambahan kehilangan S2−S1 dilaporkan terpisah. Bukan rekomendasi alokasi optimal untuk semua desa."]}).to_excel(W, sheet_name="0 README", index=False)
pd.DataFrame([{"Alternatif": a, **({"Patroli": None} if v is None else dict(zip(["Patroli", "Rehabilitasi", "Kebakaran", "KUPS", "Kompensasi"], v)))} for a, v in ALT.items()]).to_excel(W, sheet_name="1 Definisi alternatif", index=False)
df[df["Variasi"] == "dasar"][["Harga", "Alternatif"] + IND].to_excel(W, sheet_name="2 Hasil dasar", index=False)
dB[dB["Variasi"] == "dasar"][["Harga", "Alternatif"] + IND].to_excel(W, sheet_name="3 Selisih thd B0", index=False)
r1.to_excel(W, sheet_name="4 Uji R1", index=False)
df[df["Variasi"] != "dasar"][["Variasi", "Harga", "Alternatif"] + IND].to_excel(W, sheet_name="5 Sensitivitas USD20", index=False)
cekA.to_excel(W, sheet_name="6 Cek anggaran", index=False)
W.close(); df.to_pickle("fase5/alok_df.pkl"); dB.to_pickle("fase5/alok_dB.pkl"); r1.to_pickle("fase5/alok_r1.pkl")
# grafik
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e4e4", "axes.axisbelow": True})
def fmt(x, d=0): s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
FM = matplotlib.ticker.FuncFormatter(lambda v, p: fmt(v, 0 if abs(v) >= 10 or v == 0 else 1))
NOTE = "Benefit sharing pada S2 mekanisme C (J1), Referensi S1 berpasangan. PySD; Vensim native belum. Bukan rekomendasi alokasi optimal untuk semua desa."
alts = [a for a in ALT if a != "B0"]; x = np.arange(len(alts)); w = 0.27
fig, axs = plt.subplots(1, 3, figsize=(17, 5.4))
for ax, (c, sc, t) in zip(axs, [("Deforestasi dihindari S2−S1 (ha)", 1, "Δ deforestasi dihindari thd B0 (ha)"), ("Pendapatan bersih per RT terdampak/pemegang garapan (Rp/th)", 1e3, "Δ pendapatan RT terdampak thd B0 (Rp ribu/th)"), ("Penerimaan anggota KUPS (Rp/th)", 1e6, "Δ penerimaan anggota KUPS thd B0 (Rp juta/th)")]):
    for i, (h, col) in enumerate([(10, "#b9e3cf"), (20, "#1aa874"), (35, "#0b4a33")]):
        sub = dB[(dB["Variasi"] == "dasar") & (dB["Harga"] == h)].set_index("Alternatif")
        ax.bar(x + (i - 1) * w, [sub.loc[a, c] / sc for a in alts], w, color=col, label=f"USD {h}")
    ax.axhline(0, color="#999", lw=1); ax.set_xticks(x, alts); ax.set_title(t, fontsize=12); ax.yaxis.set_major_formatter(FM)
axs[0].legend(frameon=False); fig.text(0.01, 0.005, NOTE, fontsize=9, color="#666"); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{OUTG}/A1_alokasi_vs_B0.png", dpi=200); plt.close(fig)
print("anggaran:", okA); print(cekA.describe().loc[["min", "max"]].to_string())
print(df[df["Variasi"] == "dasar"].set_index(["Harga", "Alternatif"])[IND].round(1).to_string())
print(r1.to_string())
