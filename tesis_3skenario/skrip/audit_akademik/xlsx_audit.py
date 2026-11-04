import pandas as pd, sys
H = pd.read_pickle("fase6/rekon_hasil.pkl"); A = pd.read_pickle("fase6/akses.pkl"); E = pd.read_pickle("fase6/porsi_efektif.pkl"); K = pd.read_pickle("fase6/kups_tradeoff.pkl")
W = pd.ExcelWriter(sys.argv[1], engine="openpyxl")
pd.DataFrame({"Isi": ["TABEL REKONSILIASI AUDIT AKADEMIK FINAL – model v2 dan v2_ALOKASI (tidak diubah), 2026-11-04. PySD; Vensim native BELUM DIVERIFIKASI; NPV SEMENTARA.",
 "Lembar 1–2: arus kas C-J1 USD 20 dan USD 35 per periode (Rp miliar nominal). Cek A–G dihitung dari komponen aliran, bukan dari variabel Check model.",
 "Lembar 3: hitung ulang independen komponen pendapatan dan biaya dari penggerak primer (kredit × harga × kurs, luas × tarif, persentase × kas, HOK × biaya).",
 "Lembar 4: populasi RT; lembar 5: sensitivitas pengali kehilangan akses (deterministik); lembar 6: porsi alokasi efektif; lembar 7: trade-off KUPS antaralternatif."]}).to_excel(W, sheet_name="0 README", index=False)
H["rek"][20].to_excel(W, sheet_name="1 Arus kas C-J1 USD20"); H["rek"][35].to_excel(W, sheet_name="2 Arus kas C-J1 USD35")
rows = [{"Harga": h, "Komponen": k, "Hitung ulang (Rp M)": a, "Keluaran model (Rp M)": b} for h in [20, 35] for k, (a, b) in H["ind"][h].items()]
pd.DataFrame(rows).to_excel(W, sheet_name="3 Hitung ulang independen", index=False)
pd.DataFrame([{"Besaran": "Populasi", "2024 (rerata th)": 73083, "2030": 80733, "2042": 98518, "2055": 122233, "2087": 206245, "Rerata 2030–2055": None},
              {"Besaran": "RT bergantung hutan (5.328 pekerja SDA × 1 RT/pekerja, tumbuh 1,66 %/th)", "2024 (rerata th)": 5373, "2030": 5970, "2042": 7342, "2055": 9154, "2087": 15516, "Rerata 2030–2055": 7462},
              {"Besaran": "RT terdampak = RT bergantung × 2.144/5.328 (pemegang garapan; faktor keunikan 1)", "2024 (rerata th)": 2162, "2030": 2402, "2042": 2955, "2055": 3684, "2087": 6244, "Rerata 2030–2055": 3003}]).to_excel(W, sheet_name="4 Populasi RT", index=False)
A.to_excel(W, sheet_name="5 Sensitivitas akses", index=False); E.to_excel(W, sheet_name="6 Porsi alokasi efektif", index=False); K.to_excel(W, sheet_name="7 Trade-off KUPS", index=False)
W.close(); print("ok")
