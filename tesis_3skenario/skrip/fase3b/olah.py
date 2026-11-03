import sys, json, pickle, numpy as np, pandas as pd
sys.path.insert(0, "fase3"); import common
DT = common.DT; RUNS = json.load(open("fase3b/runs.json"))
L = lambda k: pd.read_pickle(f"fase3b/runs/{k.replace('|','_')}.pkl")
S1 = L("S1")
def first_t(s, thr=1e-6):
    i = np.where(s.values > thr)[0]; return float(s.index[i[0]]) if len(i) else None
def met(d, ref=S1):
    F = lambda v: float(d[v].iloc[:-1].sum() * DT); E = lambda v: float(d[v].iloc[-1])
    Fr = lambda v: float(ref[v].iloc[:-1].sum() * DT)
    an = common.annual(d); anr = common.annual(ref); A = lambda a, v: float(a[v].loc[2030:2055].mean())
    cm = (d["Arus Kas Mitra"].iloc[:-1] * DT).cumsum()
    cm_inc = ((d["Arus Kas Mitra"] - ref["Arus Kas Mitra"]).iloc[:-1] * DT).cumsum()   # di luar pembiayaan historis yang sama di S1
    tmin = cm_inc.idxmin(); after = cm_inc.loc[tmin:]; pb = after[after >= 0]
    keb = A(an, "Kebutuhan Dana Minimum")
    r = {
     "Kredit REDD diajukan (tCO2e)": F("Kredit REDD Diajukan"), "Kredit ARR diajukan (tCO2e)": F("Kredit ARR Diajukan"),
     "Kredit terbit (tCO2e)": F("Kredit Karbon Terbit"), "Kredit terjual (tCO2e)": F("Kredit REDD Terjual") + F("Kredit ARR Terjual"),
     "Kas penjualan diterima (Rp)": F("Kas Penjualan Kredit"), "Biaya MRV, transaksi, pajak (Rp)": F("Biaya Transaksi dan MRV"),
     "Kas masuk LPHD karbon (Rp)": F("Kas Masuk LPHD Karbon"), "Dana mitra 40 % (Rp)": F("Dana Mitra dari Karbon"),
     "Deforestasi dihindari S2−S1 (ha)": Fr("Deforestasi Total") - F("Deforestasi Total"),
     "Emisi deforestasi dihindari S2−S1 (tCO2e)": Fr("Emisi Deforestasi Biomassa") - F("Emisi Deforestasi Biomassa"),
     "Emisi deforestasi dihindari thd BAU (tCO2e)": F("Emisi Deforestasi Biomassa Baseline") - F("Emisi Deforestasi Biomassa"),
     "Δ hutan 2087 S2−S1 (ha)": E("Total Hutan") - float(ref["Total Hutan"].iloc[-1]),
     "Pembiayaan jembatan kumulatif (Rp)": E("Kumulatif Pembiayaan Jembatan"), "HOK jembatan kumulatif": F("Hari Patroli Didanai Jembatan"),
     "Defisit biaya bersama maks. (Rp)": float(d["Defisit Biaya Bersama Belum Dipulihkan"].max()),
     "Defisit biaya bersama 2087 (Rp)": E("Defisit Biaya Bersama Belum Dipulihkan"),
     "Pokok talangan kumulatif (Rp)": E("Pokok Talangan Kumulatif"), "Biaya modal kumulatif (Rp)": F("Biaya Modal Pendanaan Awal Rp"),
     "Pemulihan talangan kumulatif (Rp)": F("Pemulihan Pendanaan Awal"), "Sisa talangan 2087 (Rp)": E("Pendanaan Awal Belum Terpulihkan"),
     "Eksposur kas mitra maks. di luar pembiayaan historis (Rp)": -float(cm_inc.min()),
     "Tahun eksposur mitra maks.": float(tmin), "Tahun impas kas mitra (tak terdiskonto)": float(pb.index[0]) if len(pb) and cm_inc.min() < -1 else None,
     "NPV proyek keseluruhan (Rp) [SEMENTARA]": E("NPV Proyek Keseluruhan"), "NPV inkremental karbon (Rp) [SEMENTARA]": E("NPV Inkremental Perdagangan Karbon"),
     "NPV mitra (Rp) [SEMENTARA]": E("NPV Mitra"), "NPV mitra inkremental thd S1 (Rp) [SEMENTARA]": E("NPV Mitra") - float(ref["NPV Mitra"].iloc[-1]),
     "Tahun kredit pertama diajukan": first_t(d["Kredit Karbon Diajukan"]), "Tahun kredit pertama terbit": first_t(d["Kredit Karbon Terbit"]),
     "Tahun kas penjualan pertama": first_t(d["Kas Penjualan Kredit"]), "Tahun kas LPHD karbon pertama": first_t(d["Kas Masuk LPHD Karbon"]),
     "Tahun arus kas mitra positif pertama": first_t(d["Arus Kas Mitra"], 1),
     "Cakupan kebutuhan minimum LPHD 2030–2055 (%)": 100 * A(an, "Penggunaan Dana Pengelolaan") / keb if keb else np.nan,
     "Δ FTE berupah 2030–2055": A(an, "Kesempatan Kerja Berupah Setara Penuh") - A(anr, "Kesempatan Kerja Berupah Setara Penuh"),
     "Δ pendapatan bersih per RT 2030–2055 (Rp)": A(an, "Pendapatan Bersih per RT Bergantung") - A(anr, "Pendapatan Bersih per RT Bergantung"),
     "Porsi mitigasi adisional rerata 2030–2055": A(an, "Porsi Mitigasi Adisional terhadap S2"),
     "Patroli tambahan (kas LPHD + jembatan) rerata 2030–2055 (HOK)": A(an, "Hari Patroli Didanai Kas LPHD") + A(an, "Hari Patroli Didanai Jembatan"),
     "maks |Check Identitas Arus Kas|": float(d["Check Identitas Arus Kas"].abs().max()), "maks |Check Identitas Patroli|": float(d["Check Identitas Patroli"].abs().max()),
    }
    # kredit (diajukan) per tCO2e emisi dihindari S2−S1 x faktor eligible
    return r
if __name__ == "__main__":
    R = {k: met(L(k)) for k in RUNS if k != "S1"}
    R["S1"] = met(S1)
    json.dump(R, open("fase3b/mek_hasil.json", "w"), indent=1, ensure_ascii=False, default=float)
    print("ok", len(R))
