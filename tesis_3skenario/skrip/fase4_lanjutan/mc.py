"""Monte Carlo LHS berpasangan S1–S2 (mekanisme C, Referensi S1 berpasangan), model v2."""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, "fase4"); sys.path.insert(0, "fase4g"); sys.path.insert(0, "fase3"); import c4, common
from gate import OVR
from multiprocessing import Pool
from scipy.stats import qmc
SEED, N, H = 20261104, 400, [10, 20, 35]
BAU = {"Laju HLKS menjadi NonHutan BAU": 0.00492777, "Laju HMS menjadi NonHutan BAU": 0.00261092, "Laju HRS menjadi NonHutan BAU": 0.00955847, "Laju HRS menjadi Pr BAU": 0.000233486, "Laju HLKS menjadi Pr BAU": 9.43217e-06}
REG = {"Laju NonHutan menjadi HLKS": 1.41648e-05, "Laju NonHutan menjadi HMS": 0.000763614, "Laju NonHutan menjadi HRS": 0.00739492}
# (nama, distribusi, a, b, c, nilai dasar, sumber/kelas)
PAR = [("k (Tingkat Keberlanjutan Patroli Reguler)", "U", 0, 1, None, 0.5, "D: tanpa data pasca-2025"),
       ("Efektivitas Perlindungan Penuh terhadap Deforestasi", "T", 0.2, 0.6, 0.37, 0.37, "C: kalibrasi; rentang literatur"),
       ("Pengali laju deforestasi BAU", "U", 0.7, 1.3, None, 1, "B/C: GIS 2001–2024, rentang periode"),
       ("Pengali laju regenerasi", "U", 0.5, 1.5, None, 1, "C"),
       ("Biaya per Hari Patroli (Rp/HOK)", "U", 150000, 300000, None, 260000, "D: upah 150.000 terkonfirmasi; total belum"),
       ("Pengali biaya MRV", "U", 0.5, 1.5, None, 1, "D"),
       ("Besaran Pembiayaan Jembatan per Tahun (Rp)", "U", 3.9143e8, 1.6876e9, None, 7.8286e8, "Eksperimen: 0,5×J1 s.d. JP"),
       ("Durasi Pembiayaan Jembatan (th)", "U", 3, 8, None, 5, "Eksperimen"),
       ("Delay Verifikasi dan Penerbitan Kredit (th)", "U", 2, 5, None, 3, "D"),
       ("Delay Pembayaran Penjualan (th)", "U", 0, 1, None, 0, "D"),
       ("Laju Penjualan Kredit (/th)", "U", 0.4, 1.0, None, 0.7, "D"),
       ("Pengali Kehilangan Akses", "U", 0, 1.5, None, 1, "D"),
       ("Pengali surplus KUPS", "U", 0.7, 1.3, None, 1, "B/C"),
       ("Porsi Laba Ditahan untuk Reinvestasi", "U", 0.25, 0.75, None, 0.5, "D"),
       ("Biaya Reaktivasi KUPS (Rp)", "U", 1.25e7, 7.5e7, None, 5e7, "D"),
       ("Indeks Kapasitas LPHD Awal", "U", 0.3, 0.7, None, 0.5, "D"),
       ("Pengaruh Kapasitas terhadap Mutu Kegiatan", "U", 0, 0.5, None, 0, "D"),
       ("Proporsi Leakage Karbon", "U", 0.05, 0.2, None, 0.1, "D"),
       ("Proporsi Buffer Risiko Karbon", "U", 0.1, 0.2, None, 0.12, "D"),
       ("Proporsi Kredit REDD dalam Project Area", "U", 0.541, 0.903, None, 0.682, "B: rentang GIS")]
def sample():
    u = qmc.LatinHypercube(d=len(PAR), seed=SEED).random(N); X = np.zeros_like(u)
    for j, (n, dist, a, b, c, _, _) in enumerate(PAR):
        if dist == "U": X[:, j] = a + u[:, j] * (b - a)
        else:
            fc = (c - a) / (b - a); x = u[:, j]
            X[:, j] = np.where(x < fc, a + np.sqrt(x * (b - a) * (c - a)), b - np.sqrt((1 - x) * (b - a) * (b - c)))
    return pd.DataFrame(X, columns=[p[0] for p in PAR])
def params(row):
    p = {"Tingkat Keberlanjutan Patroli Reguler": row.iloc[0], "Efektivitas Perlindungan Penuh terhadap Deforestasi": row.iloc[1],
         "Biaya per Hari Patroli": row.iloc[4], "Biaya Monitoring per Ha per Tahun": 1980 * row.iloc[5], "Biaya Verifikasi per Kejadian": 7.425e8 * row.iloc[5],
         "Besaran Pembiayaan Jembatan per Tahun": row.iloc[6], "Durasi Pembiayaan Jembatan": row.iloc[7], "Delay Verifikasi dan Penerbitan Kredit": row.iloc[8],
         "Delay Pembayaran Penjualan": row.iloc[9], "Laju Penjualan Kredit": row.iloc[10], "Pengali Kehilangan Akses": row.iloc[11], "Surplus Operasional per KUPS Produktif": 6.6473e6 * row.iloc[12],
         "Porsi Laba Ditahan untuk Reinvestasi": row.iloc[13], "Biaya Reaktivasi KUPS": row.iloc[14], "Indeks Kapasitas LPHD Awal": row.iloc[15], "Pengaruh Kapasitas terhadap Mutu Kegiatan": row.iloc[16],
         "Proporsi Leakage Karbon": row.iloc[17], "Proporsi Buffer Risiko Karbon": row.iloc[18], "Proporsi Kredit REDD dalam Project Area": row.iloc[19]}
    p.update({k: v * row.iloc[2] for k, v in BAU.items()}); p.update({k: v * row.iloc[3] for k, v in REG.items()})
    return p
COLS = list(dict.fromkeys(["Total Hutan", "Deforestasi Total", "Emisi Bersih Biomassa", "Emisi Deforestasi Biomassa", "Total Hutan Referensi S1", "Emisi Deforestasi Biomassa Referensi S1",
        "Kredit REDD Diajukan", "Kredit ARR Diajukan", "Reversal Belum Terkompensasi", "Kredit Pengganti Reversal Kumulatif", "Kas Penjualan Kredit", "Kas Masuk LPHD Karbon", "Dana Desa Diterima",
        "Penggunaan Dana Pengelolaan", "Kebutuhan Dana Minimum", "Realisasi Belanja Operasional LPHD", "NPV Inkremental Perdagangan Karbon", "NPV Mitra", "NPV Proyek Keseluruhan", "Pendapatan Bersih per RT Bergantung",
        "Pendapatan Hutan per RT Bergantung", "Pendapatan Program per RT Bergantung", "Kehilangan Pendapatan Pembatasan Akses per RT", "Kehilangan per RT Terdampak", "Jumlah KUPS Aktif", "Pendapatan KUPS Total",
        "Kesempatan Kerja Berupah Setara Penuh", "Upah Kegiatan PS", "Indeks Kapasitas LPHD", "Defisit Biaya Bersama Belum Dipulihkan", "Pendanaan Awal Belum Terpulihkan", "Check Identitas Arus Kas"] + list(OVR) + list(OVR.values())))
DT = 0.0625
def metr(s, d):
    F = lambda x, v: float(x[v].iloc[:-1].sum() * DT); E = lambda x, v: float(x[v].iloc[-1])
    ans, and_ = common.annual(s), common.annual(d); A = lambda an, v, a=2030, b=2055: float(an[v].loc[a:b].mean())
    cumnet = ((s["Emisi Bersih Biomassa"] - d["Emisi Bersih Biomassa"]) * DT).cumsum()
    terd = lambda an: A(an, "Pendapatan Hutan per RT Bergantung") + A(an, "Pendapatan Program per RT Bergantung") - A(an, "Kehilangan per RT Terdampak")
    keb = float(and_["Kebutuhan Dana Minimum"].loc[2060:2086].mean())
    return {"Deforestasi dihindari S2−S1 (ha)": F(s, "Deforestasi Total") - F(d, "Deforestasi Total"), "Δ hutan 2087 (ha)": E(d, "Total Hutan") - E(s, "Total Hutan"),
            "Manfaat karbon bersih kumulatif 2087 (tCO2e)": float(cumnet.iloc[-2]), "Puncak manfaat karbon bersih (tCO2e)": float(cumnet.max()),
            "Kredit diajukan (tCO2e)": F(d, "Kredit REDD Diajukan") + F(d, "Kredit ARR Diajukan"), "Debit reversal belum diselesaikan 2087 (tCO2e)": E(d, "Reversal Belum Terkompensasi"),
            "Kredit pengganti dibeli (tCO2e)": E(d, "Kredit Pengganti Reversal Kumulatif"), "Kas LPHD karbon (Rp)": F(d, "Kas Masuk LPHD Karbon"),
            "Kas LPHD rerata 2075–2086 (Rp/th)": float(and_["Dana Desa Diterima"].loc[2075:2086].mean()), "Cakupan kebutuhan minimum 2060–2086 (%)": 100 * float(and_["Penggunaan Dana Pengelolaan"].loc[2060:2086].mean()) / keb if keb > 0 else np.nan,
            "Belanja operasional LPHD rerata 2060–2086 (Rp/th)": float(and_["Realisasi Belanja Operasional LPHD"].loc[2060:2086].mean()),
            "NPV inkremental proyek [SEMENTARA] (Rp)": E(d, "NPV Inkremental Perdagangan Karbon"), "NPV mitra inkremental [SEMENTARA] (Rp)": E(d, "NPV Mitra") - E(s, "NPV Mitra"),
            "Defisit MRV 2087 (Rp)": E(d, "Defisit Biaya Bersama Belum Dipulihkan"), "Sisa talangan 2087 (Rp)": E(d, "Pendanaan Awal Belum Terpulihkan"),
            "Δ pendapatan bersih per RT bergantung (Rp/th)": A(and_, "Pendapatan Bersih per RT Bergantung") - A(ans, "Pendapatan Bersih per RT Bergantung"),
            "Δ pendapatan per RT terdampak (Rp/th)": terd(and_) - terd(ans), "Δ kehilangan per RT terdampak (Rp/th)": A(and_, "Kehilangan per RT Terdampak") - A(ans, "Kehilangan per RT Terdampak"),
            "Δ FTE berupah 2030–2055": A(and_, "Kesempatan Kerja Berupah Setara Penuh") - A(ans, "Kesempatan Kerja Berupah Setara Penuh"),
            "Δ FTE berupah 2060–2086": float(and_["Kesempatan Kerja Berupah Setara Penuh"].loc[2060:2086].mean() - ans["Kesempatan Kerja Berupah Setara Penuh"].loc[2060:2086].mean()),
            "Δ upah kegiatan PS (Rp/th)": A(and_, "Upah Kegiatan PS") - A(ans, "Upah Kegiatan PS"), "KUPS aktif 2087 S2": E(d, "Jumlah KUPS Aktif"), "KUPS aktif 2087 S1": E(s, "Jumlah KUPS Aktif"),
            "KUPS aktif 2026 S2": float(and_["Jumlah KUPS Aktif"].loc[2026]), "Δ penerimaan anggota KUPS (Rp/th)": A(and_, "Pendapatan KUPS Total") - A(ans, "Pendapatan KUPS Total"),
            "Kapasitas LPHD 2087 S2": E(d, "Indeks Kapasitas LPHD"),
            "_cek_hutan_ref": float((d["Total Hutan Referensi S1"] - s["Total Hutan"]).abs().max()), "_cek_emisi_ref": float((d["Emisi Deforestasi Biomassa Referensi S1"] - s["Emisi Deforestasi Biomassa"]).abs().max()),
            "_cek_arus_kas": float(d["Check Identitas Arus Kas"].abs().max())}
def job(i):
    try:
        p = params(X.iloc[i]); m = c4.model(); m.reload()
        s = m.run(params=dict({"Skenario Kebijakan": 1}, **p), return_timestamps=c4.TS, return_columns=COLS, progress=False)
        ov = {k: pd.Series(s[v].values, index=s.index) for k, v in OVR.items()}; out = []
        for h in H:
            m.reload(); d = m.run(params=dict({"Skenario Kebijakan": 2, "Harga Karbon": h}, **p, **ov), return_timestamps=c4.TS, return_columns=COLS, progress=False)
            out.append(dict({"sampel": i, "harga": h, "galat": ""}, **metr(s, d)))
        return out
    except Exception as e:
        return [{"sampel": i, "harga": h, "galat": repr(e)[:300]} for h in H]
X = sample()
if __name__ == "__main__":
    X.to_csv("fase5/mc_sampel.csv", index=False)
    res = []
    with Pool(4) as pool:
        for k, out in enumerate(pool.imap_unordered(job, range(N))):
            res += out
            if k % 20 == 0: print(k, flush=True); pd.DataFrame(res).to_pickle("fase5/mc_hasil.pkl")
    pd.DataFrame(res).to_pickle("fase5/mc_hasil.pkl"); print("selesai", len(res))
