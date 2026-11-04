import sys, json, numpy as np, pandas as pd
DT = 0.0625; FE = (1-.1)*(1-.12)*.682
L = lambda k: pd.read_pickle(f"fase4/runs_v2/{k}.pkl"); I = lambda d, v: float(d[v].iloc[:-1].sum() * DT); E = lambda d, v: float(d[v].iloc[-1])
S1 = L("S1"); rows = []
for k, lab in [("C6", "USD6 aturan 2"), ("C10", "USD10 aturan 2"), ("C15", "USD15 aturan 2"), ("C20", "USD20 aturan 2"), ("RV_C20_aturan1", "USD20 aturan 1"), ("RV_C20_aturan0", "USD20 aturan 0"), ("C35", "USD35 aturan 2")]:
    d = L(k); dd = S1["Deforestasi Total"] - d["Deforestasi Total"]; neg = dd[dd < -1e-9]
    cm = (d["Mitigasi REDD Eligible Bersih Proyek"] * DT).cumsum(); lp = d["Kredit Pengganti Reversal Kumulatif"]
    ed = (S1["Emisi Deforestasi Biomassa"] - d["Emisi Deforestasi Biomassa"]); edn = ed[ed < -1e-9]
    rows.append({"Run": lab, "(1) Tahun pertama deforestasi S2 > S1": float(neg.index[0]) if len(neg) else None, "(1) Deforestasi tambahan S2 pada tahun-tahun itu (ha)": float(-neg.sum() * DT),
        "(1) Emisi tambahan S2 pada tahun-tahun itu (tCO2e bruto)": float(-edn.sum() * DT),
        "(2) Puncak manfaat bersih eligible kumulatif (tCO2e)": float(cm.max()), "(2) Tahun puncak": float(cm.idxmax()), "(2) Manfaat bersih eligible 2087 (tCO2e)": float(cm.iloc[-2]),
        "(2) Penurunan dari puncak (tCO2e)": float(cm.max() - cm.iloc[-2]),
        "Kredit REDD diajukan (tCO2e)": I(d, "Kredit REDD Diajukan"),
        "(3) Pembatalan stok kredit sendiri (tCO2e)": E(d, "Kumulatif Pembatalan Stok Kredit Reversal"), "(3) Debit belum diselesaikan 2087 (tCO2e)": E(d, "Reversal Belum Terkompensasi"),
        "(3) Nilai debit belum diselesaikan 2087 (Rp, pelaporan)": E(d, "Kewajiban Reversal Belum Diselesaikan"),
        "(4) Kontribusi buffer (tCO2e)": E(d, "Kumulatif Buffer REDD"), "(4) Buffer dipakai (tCO2e)": E(d, "Kumulatif Penggunaan Buffer Reversal"), "(4) Buffer tersisa (tCO2e)": E(d, "Buffer REDD Tersedia"),
        "(5) Kredit pengganti dibeli (tCO2e)": float(lp.iloc[-1]), "(5) Tahun pembelian pertama": float(lp.index[(lp > 1e-6).values][0]) if (lp > 1e-6).any() else None,
        "(5) Biaya kas pengganti (Rp)": I(d, "Biaya Penggantian Reversal"), "NPV mitra inkremental [SEMENTARA] (Rp)": E(d, "NPV Mitra") - E(S1, "NPV Mitra"),
        "Kas LPHD karbon (Rp)": I(d, "Kas Masuk LPHD Karbon"), "Defisit MRV 2087 (Rp)": E(d, "Defisit Biaya Bersama Belum Dipulihkan")})
RV = pd.DataFrame(rows); RV.to_pickle("fase4g/reversal_audit.pkl")
if len(sys.argv) > 1:
    W = pd.ExcelWriter(sys.argv[1], engine="openpyxl")
    pd.DataFrame({"Isi": ["HASIL UJI FINAL GATE FASE 4 – MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl (946 variabel, 16 View), 2026-11-04",
      "PySD 3.14.3; Euler; DT 0,0625 kecuali disebut. Units Check dan run native Vensim BELUM DILAKUKAN. NPV SEMENTARA. Kredit model ≠ kredit terverifikasi.",
      "Model v1 (937 variabel) tidak ditimpa; v2 memperbaiki akuntansi reversal. Protokol referensi berpasangan ditetapkan untuk simulasi final.",
      "Lembar: 1 status uji v2; 2 riwayat kriteria; 3 K7 konvergensi DT; 4 K7 dekomposisi; 5 kesetaraan Referensi S1; 6 audit reversal; 7 identitas sosial-ekonomi; 8 upah vs biaya; 9 S1–S2 sosial-ekonomi; 10 dekomposisi pendapatan RT"]}).to_excel(W, sheet_name="0 README", index=False)
    pd.DataFrame(json.load(open("fase4/uji4_hasil_v2.json"))).to_excel(W, sheet_name="1 Status uji v2", index=False)
    pd.read_json("fase4g/riwayat_kriteria.json").to_excel(W, sheet_name="2 Riwayat kriteria", index=False)
    pd.read_json("fase4g/k7_dt.json").to_excel(W, sheet_name="3 K7 konvergensi DT", index=False)
    pd.read_json("fase4g/k7_dekomposisi.json").to_excel(W, sheet_name="4 K7 dekomposisi", index=False)
    pd.read_pickle("fase4g/gate_tabel.pkl").to_excel(W, sheet_name="5 Kesetaraan Referensi S1", index=False)
    RV.to_excel(W, sheet_name="6 Audit reversal", index=False)
    so = pd.read_pickle("fase4g/sosek_hasil.pkl")
    pd.DataFrame(so["identitas"]).to_excel(W, sheet_name="7 Identitas sosek", index=False)
    pd.DataFrame(so["upah"]).to_excel(W, sheet_name="8 Upah vs biaya", index=False)
    so["banding"].to_excel(W, sheet_name="9 S1-S2 sosek")
    pd.read_pickle("fase4g/sosek_dekomposisi.pkl").to_excel(W, sheet_name="10 Dekomposisi pendapatan RT")
    W.close()
pd.set_option("display.width", 300); print(RV.T.to_string())
