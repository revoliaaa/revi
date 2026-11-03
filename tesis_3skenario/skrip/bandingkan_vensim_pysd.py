"""
Bandingkan ekspor Vensim native (.tab atau .csv, titik desimal) dengan PySD untuk model FINAL 3 SKENARIO.

Cara pakai:
  1. Di Vensim: buka DKP_25HD_FINAL_3SKENARIO.mdl, jalankan run dengan nama S1, S2, S3_USD6, S3_USD10, S3_USD15, S3_USD20, S3_USD35
     (ubah 'Skenario Kebijakan' = 1/2/3 dan 'Harga Karbon').
  2. Model > Export Dataset (atau Tools > Export) setiap run ke .tab (pemisah TAB, waktu sebagai kolom), SAVEPER = 1.
     Jangan buka/simpan ulang lewat Excel berlocale Indonesia.
  3. python bandingkan_vensim_pysd.py DKP_25HD_FINAL_3SKENARIO.mdl S1.tab S2.tab S3_USD10.tab ...
     Nama berkas menentukan skenario: S1, S2, S3_USD<harga>.
Kriteria cocok: selisih relatif <= 1e-5 ATAU selisih absolut <= 1e-6 (presisi ekspor Vensim 6 angka penting).
"""
import sys, re, numpy as np, pandas as pd, pysd
mdl, files = sys.argv[1], sys.argv[2:]
model = pysd.read_vensim(mdl)
rows = []
for f in files:
    tag = re.sub(r"\.(tab|csv|txt)$", "", f.split("/")[-1], flags=re.I)
    if tag.upper() == "S1": p = {"Skenario Kebijakan": 1}
    elif tag.upper() == "S2": p = {"Skenario Kebijakan": 2}
    else: p = {"Skenario Kebijakan": 3, "Harga Karbon": float(re.search(r"(\d+(\.\d+)?)$", tag).group(1))}
    sep = "\t" if f.lower().endswith((".tab", ".txt")) else ","
    v = pd.read_csv(f, sep=sep, index_col=0)
    v.index = v.index.astype(str).str.strip().str.strip('"')
    v.columns = [float(str(c).strip()) for c in v.columns]
    v = v.apply(pd.to_numeric, errors="coerce")
    model.reload()
    py = model.run(params=p, return_timestamps=list(v.columns), progress=False)
    for name in v.index:
        if name not in py.columns: continue
        a = v.loc[name].values.astype(float); b = py[name].reindex(v.columns).values.astype(float)
        ok = (np.abs(a - b) <= np.maximum(1e-5 * np.abs(b), 1e-6)) | (np.isnan(a) & np.isnan(b))
        rows.append({"skenario": tag, "variabel": name, "sel": len(a), "cocok": int(ok.sum()), "selisih_rel_maks": float(np.nanmax(np.abs(a - b) / np.maximum(np.abs(b), 1e-12)))})
r = pd.DataFrame(rows)
s = r.groupby("skenario")[["sel", "cocok"]].sum(); s["% cocok"] = 100 * s["cocok"] / s["sel"]
print(s.to_string()); out = "HASIL_BANDING_VENSIM_PYSD_3S.xlsx"
with pd.ExcelWriter(out) as w: s.to_excel(w, sheet_name="Ringkasan"); r.sort_values("selisih_rel_maks", ascending=False).to_excel(w, sheet_name="Per variabel", index=False)
print("disimpan:", out)
