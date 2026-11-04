import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "fase3"); import common
R = pd.read_pickle("fase4g/sosek_runs.pkl"); DT = 0.0625
def mx(x): return float(np.nanmax(np.abs(x.values)))
out = {"identitas": [], "upah": [], "banding": None}
s1 = R["S1"]
for k in ["S1", "C20", "C35", "C20_JP"]:
    d = R[k]; rt = d["Rumah Tangga Bergantung Hutan"]
    prog = (d["Pendapatan KUPS untuk Pendapatan RT"] + d["Upah Kegiatan PS"] * 0.5) * d["Porsi Manfaat Program untuk RT Bergantung"] / rt
    net = d["Pendapatan Hutan per RT Bergantung"] + d["Pendapatan Non Hutan per RT Bergantung"] + d["Pendapatan Program per RT Bergantung"] - d["Kehilangan Pendapatan Pembatasan Akses per RT"]
    agg = d["Kehilangan Pendapatan Pembatasan Akses per RT"] * rt
    terd = (d["Kehilangan Pendapatan Agregat"] / d["RT Terdampak Akses"])
    upk = d["Upah Patroli Berbayar"] + d["Upah Penanaman Program Non Karbon"] + d["Upah Penanaman Didanai Karbon"] + d["Upah Pengendalian Kebakaran"]
    out["identitas"].append({"run": k,
        "Upah patroli = HOK berbayar × 150.000": mx(d["Upah Patroli Berbayar"] - d["HOK Patroli Berbayar"] * 150000),
        "Upah patroli kas LPHD = HOK kas LPHD × 150.000": mx(d["Upah Patroli dari Kas LPHD"] - d["Hari Patroli Didanai Kas LPHD"] * 150000),
        "Upah setara non-tunai = 150.000": mx(d["Upah Setara Non Tunai Patroli"] - 150000),
        "Nilai tenaga non-tunai = HOK reguler × 150.000 + HOK tanam sukarela × 106.000": mx(d["Nilai Kontribusi Tenaga Non Tunai"] - (d["HOK Patroli Reguler PS"] * 150000 + d["HOK Penanaman Sukarela"] * 106000)),
        "Upah kegiatan PS = Σ komponen": mx(d["Upah Kegiatan PS"] - upk),
        "Pendapatan program per RT": mx(d["Pendapatan Program per RT Bergantung"] - prog),
        "Pendapatan bersih per RT": mx(d["Pendapatan Bersih per RT Bergantung"] - net),
        "Kehilangan agregat = per RT × RT bergantung": mx(d["Kehilangan Pendapatan Agregat"] - agg),
        "Kehilangan per RT terdampak": mx(d["Kehilangan per RT Terdampak"] - terd),
        "Identitas surplus KUPS": mx(d["Check Identitas Surplus KUPS"]), "Identitas penjualan KUPS": mx(d["Check Identitas Penjualan KUPS"]),
        "Penerimaan anggota ≤ surplus ≤ omzet (pelanggaran maks)": max(mx((d["Pendapatan KUPS Total"] - d["Manfaat Ekonomi KUPS"]).clip(lower=0)), mx((d["Manfaat Ekonomi KUPS"] - d["Penjualan KUPS"]).clip(lower=0))),
        "Manfaat Ekonomi Patroli (variabel lama) = 0": mx(d["Manfaat Ekonomi Patroli"])})
d0, d1 = R["S1"], R["S1_nontunaix10"]
out["nontunai_invarian"] = mx(d1["Pendapatan Bersih per RT Bergantung"] - d0["Pendapatan Bersih per RT Bergantung"])
for k in ["S1", "C20", "C20_JP", "C35"]:
    d = R[k]; Y = lambda v, a=2026, b=2087: float(d[v][(d.index >= a) & (d.index < b)].sum() * DT)
    out["upah"].append({"run": k, "Upah patroli tunai 2026–2086 (Rp)": Y("Upah Patroli Berbayar"), "Biaya patroli total (asumsi Rp260.000/HOK) 2026–2086 (Rp)": Y("Penggunaan Dana Perlindungan Total"),
        "Komponen non-upah implisit (Rp)": Y("Penggunaan Dana Perlindungan Total") - Y("Upah Patroli Berbayar"), "Nilai tenaga sukarela non-tunai (Rp)": Y("Nilai Kontribusi Tenaga Non Tunai"),
        "Nilai logistik sukarela non-tunai (Rp)": Y("Nilai Logistik Non Tunai Patroli"), "Upah pengendalian kebakaran (Rp130.000, belum dikonfirmasi)": Y("Upah Pengendalian Kebakaran"),
        "Upah penanaman (Rp)": Y("Upah Penanaman Program Non Karbon") + Y("Upah Penanaman Didanai Karbon")})
# perbandingan S1–S2
def ind(d):
    an = common.annual(d); A = lambda v: float(an[v].loc[2030:2055].mean())
    return {"HOK patroli reguler": A("HOK Patroli Reguler PS"), "HOK patroli berbayar (jembatan + kas LPHD)": A("HOK Patroli Berbayar"), "HOK berupah PS": A("HOK Berupah PS"), "HOK sukarela PS": A("HOK Sukarela PS"),
            "HOK penanaman berupah": A("HOK Penanaman Berupah"), "HOK penanaman sukarela": A("HOK Penanaman Sukarela"), "HOK pengendalian kebakaran": A("HOK Pengendalian Kebakaran"),
            "FTE berupah": A("Kesempatan Kerja Berupah Setara Penuh"), "FTE sukarela": A("Kesempatan Kerja Sukarela Setara Penuh"),
            "Upah kegiatan PS (Rp/th)": A("Upah Kegiatan PS"), "Upah patroli (Rp/th)": A("Upah Patroli Berbayar"),
            "KUPS aktif": A("Jumlah KUPS Aktif"), "KUPS aktif 2087": float(d["Jumlah KUPS Aktif"].iloc[-1]), "Anggota KUPS": A("Anggota KUPS Aktif"), "Proporsi KUPS produktif": A("Proporsi KUPS Produktif"),
            "Omzet KUPS (Rp/th)": A("Penjualan KUPS"), "Surplus KUPS (Rp/th)": A("Manfaat Ekonomi KUPS"), "Penerimaan anggota KUPS (Rp/th)": A("Pendapatan KUPS Total"), "Modal usaha KUPS 2087 (Rp)": float(d["Modal Usaha KUPS"].iloc[-1]),
            "Pendapatan program per RT (Rp/th)": A("Pendapatan Program per RT Bergantung"), "Kehilangan akses per RT (Rp/th)": A("Kehilangan Pendapatan Pembatasan Akses per RT"),
            "Kehilangan per RT terdampak (Rp/th)": A("Kehilangan per RT Terdampak"), "Pendapatan bersih per RT bergantung (Rp/th)": A("Pendapatan Bersih per RT Bergantung"),
            "Kompensasi (Rp/th)": 0.0, "Kapasitas LPHD 2087": float(d["Indeks Kapasitas LPHD"].iloc[-1]), "Dana LPHD diterima (Rp/th)": A("Dana Desa Diterima"), "Belanja LPHD (Rp/th)": A("Penggunaan Dana Pengelolaan"),
            "Cakupan kebutuhan minimum (%)": 100 * A("Penggunaan Dana Pengelolaan") / A("Kebutuhan Dana Minimum") if A("Kebutuhan Dana Minimum") else np.nan,
            "Kesenjangan minimum (Rp/th)": A("Kesenjangan Pembiayaan Minimum")}
I = {k: ind(R[k]) for k in ["S1", "C10", "C20", "C35", "C10_JP", "C20_JP", "C35_JP", "S1_akses0", "C20_akses0"]}
df = pd.DataFrame(I)
for k in ["C10", "C20", "C35", "C10_JP", "C20_JP", "C35_JP"]: df[f"Δ {k}−S1"] = df[k] - df["S1"]
df["Δ C20−S1 (akses 0)"] = df["C20_akses0"] - df["S1_akses0"]
out["banding"] = df
pd.to_pickle(out, "fase4g/sosek_hasil.pkl")
pd.set_option("display.width", 250)
print(pd.DataFrame(out["identitas"]).set_index("run").T.to_string(float_format=lambda x: f"{x:.2e}"))
print("non-tunai ×10 → Δ pendapatan RT", out["nontunai_invarian"])
print(pd.DataFrame(out["upah"]).set_index("run").T.map(lambda x: f"{x/1e9:,.2f} M").to_string())
print(df[[c for c in df.columns if c.startswith("Δ")] + ["S1"]].to_string(float_format=lambda x: f"{x:,.1f}"))
