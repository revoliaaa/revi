import sys, json, pickle; sys.path.insert(0, "fase3"); from common import *
runs = pickle.load(open("fase3/det_runs.pkl", "rb")); S = json.load(open("fase3/det_summary.json")); K = pd.read_json("fase3/kronologi.json")
OUT = sys.argv[1]; W = pd.ExcelWriter(OUT, engine="openpyxl")
clean = lambda x: 0.0 if isinstance(x, float) and abs(x) < 1e-6 else x
pd.DataFrame({"Isi": [
 "HASIL SIMULASI FINAL DUA SKENARIO – DKP_25HD_FINAL_2SKENARIO.mdl (md5 aa1428dffdc27541d531926b9806c50e)",
 "S1 = PS dengan pembiayaan terbatas; S2 = PS dengan perdagangan karbon (USD 6/10/15/20/35). Horizon 2024–2087, Euler, DT 0,0625.",
 "STATUS VERIFIKASI: hanya PySD 3.14.3. Units Check dan run native Vensim BELUM dilakukan (verifikasi tertunda).",
 "ASUMSI KERJA (bukan data): k = 0,5; kas non-karbon 0; dukungan material rehabilitasi 0; hibah; pemulihan talangan sebelum bagi hasil; biaya pengembangan 0; diskonto 10 %; biaya reaktivasi KUPS Rp 50 juta; reinvestasi 0,5. Lihat lembar '8 Register asumsi'.",
 "NPV dan turunannya berstatus SEMENTARA (tanpa biaya pengembangan dan biaya material aktual). Harga impas tidak dihitung.",
 "Selisih S2−S1 (lembar 3) adalah dampak perdagangan karbon menurut model. Selisih terhadap baseline referensi karbon (lembar 4) adalah dasar potensi kredit. Keduanya tidak boleh disamakan.",
 "Konvensi: stok = nilai awal tahun; aliran = rerata dalam tahun; fisik kumulatif 2025–2086; keuangan kumulatif 2024–2086; tahunan rerata 2030–2055. Nilai |x| < 10⁻⁶ ditulis 0 (derau numerik).",
 "Kredit model ≠ kredit terverifikasi/VCU. Hasil bersyarat asumsi; bukan prakiraan."]}).to_excel(W, sheet_name="0 README", index=False)
K.to_excel(W, sheet_name="1 Prasyarat kronologi", index=False)
pd.DataFrame([{"Prasyarat": "Kronologi kredit–kas–patroli", "Status": "LULUS", "Catatan": "Patroli tambahan pertama 2029 berasal dari USD20/35; kas LPHD pertama 2031,875 dari USD10. Rantai konsisten di semua harga"},
              {"Prasyarat": "Konsistensi indikator sosial-ekologis dengan pembiayaan", "Status": "LULUS (Fase 2)", "Catatan": "U3, U4, U7, U10–U12, P1–P7 lulus pada berkas yang sama"},
              {"Prasyarat": "Units Check Vensim", "Status": "TERTUNDA", "Catatan": "Vensim tidak tersedia; pemeriksaan satuan statis 813/813 konsisten"},
              {"Prasyarat": "Pembandingan native Vensim–PySD", "Status": "TERTUNDA", "Catatan": "Skrip bandingkan_vensim_pysd.py tersedia; harus dijalankan peneliti"},
              {"Prasyarat": "Penandaan asumsi", "Status": "LULUS", "Catatan": "Lembar 8; komentar PERINGATAN D1/D3 di .mdl"}]).to_excel(W, sheet_name="1 Prasyarat kronologi", startrow=len(K) + 3, index=False)
summ = pd.DataFrame(S).map(clean); summ.index.name = "Indikator"; summ.to_excel(W, sheet_name="2 Ringkasan skenario")
s1 = S["S1"]; rows = []
for k in [c for c in S if c != "S1"]:
    s2 = S[k]; d = lambda key, sign=1: clean(sign * (s2[key] - s1[key]))
    rows.append({"Harga": k, "Δ hutan 2087 (ha)": d("Hutan 2087 (ha)"), "Deforestasi dihindari S2−S1 (ha)": d("Deforestasi kumulatif 2025–2086 (ha)", -1),
                 "Emisi deforestasi dihindari S2−S1 (tCO2e)": d("Emisi deforestasi biomassa kumulatif (tCO2e)", -1), "Tambahan serapan rehabilitasi (tCO2e)": d("Serapan rehabilitasi kumulatif (tCO2e)"),
                 "Penurunan emisi bersih S2−S1 (tCO2e)": d("Emisi bersih kumulatif (tCO2e)", -1), "Δ intensitas perlindungan": d("Intensitas perlindungan rerata 2030–2055"),
                 "Patroli tambahan rerata (HOK/th)": d("Patroli tambahan kas rerata 2030–2055 (HOK/th)"), "Δ HOK berupah": d("HOK berupah rerata 2030–2055"), "Δ FTE berupah": d("FTE berupah rerata 2030–2055"),
                 "Δ upah kegiatan PS (Rp/th)": d("Upah kegiatan PS rerata (Rp/th)"), "Δ KUPS aktif rerata": d("KUPS aktif rerata 2030–2055"), "Δ KUPS 2087": d("KUPS aktif 2087"),
                 "Δ penerimaan anggota KUPS (Rp/th)": d("Penerimaan anggota KUPS rerata (Rp/th)"), "Δ pendapatan bersih per RT (Rp/RT/th)": d("Pendapatan bersih per RT bergantung rerata (Rp/RT/th)"),
                 "Δ pendapatan program per RT": d("Pendapatan program per RT rerata (Rp/RT/th)"), "Δ kehilangan akses per RT": d("Kehilangan akses per RT rerata (Rp/RT/th)"),
                 "Δ kehilangan akses per RT terdampak": d("Kehilangan akses per RT terdampak rerata (Rp/RT/th)"), "Kas LPHD karbon (Rp)": d("Kas masuk LPHD karbon (Rp)"),
                 "Δ cakupan kebutuhan minimum (poin %)": d("Cakupan kebutuhan minimum rerata 2030–2055 (%)"), "NPV inkremental [SEMENTARA] (Rp)": d("NPV inkremental karbon (Rp) [SEMENTARA]")})
pd.DataFrame(rows).to_excel(W, sheet_name="3 Selisih S2−S1", index=False)
rows = []
for k, s in S.items():
    bau = s["Potensi kredit REDD vs baseline BAU (tCO2e)"]; kon = s["Potensi kredit REDD konservatif (pelaporan, tCO2e)"]
    rows.append({"Skenario": k, "Deforestasi dihindari vs baseline (ha)": clean(s["Deforestasi baseline kumulatif (ha)"] - s["Deforestasi kumulatif 2025–2086 (ha)"]),
                 "Emisi deforestasi dihindari vs baseline (tCO2e)": clean(s["Emisi deforestasi baseline kumulatif (tCO2e)"] - s["Emisi deforestasi biomassa kumulatif (tCO2e)"]),
                 "Potensi kredit REDD vs BAU (tCO2e)": clean(bau), "Potensi kredit REDD konservatif (tCO2e)": clean(kon), "Potensi kredit ARR (tCO2e)": clean(s["Potensi kredit ARR vs baseline (tCO2e)"]),
                 "Porsi kredit BAU yang berasal dari perlindungan tingkat S1 (%)": clean(100 * (bau - kon) / bau) if bau > 1 else np.nan,
                 "Kredit REDD terbit (tCO2e)": clean(s["Kredit REDD terbit (tCO2e)"]), "Kredit REDD terjual (tCO2e)": clean(s["Kredit REDD terjual (tCO2e)"]), "Kas penjualan (Rp)": clean(s["Kas penjualan kredit 2024–2086 (Rp)"])})
pd.DataFrame(rows).to_excel(W, sheet_name="4 Terhadap baseline karbon", index=False)
for k, d in runs.items():
    an = annual(d).map(clean) if hasattr(annual(d), "map") else annual(d); an.index.name = "Tahun"
    an.to_excel(W, sheet_name=f"5 Tahunan {k}"[:31])
cum = {}
for k, d in runs.items():
    an = annual(d); cum[k] = {v: clean(float(an[v].loc[2025:2086].sum())) for v in V if v not in STOCK}
c = pd.DataFrame(cum); c.index.name = "Variabel aliran (Σ rerata tahunan 2025–2086)"; c.to_excel(W, sheet_name="6 Kumulatif")
pd.DataFrame([
 ("Tingkat Keberlanjutan Patroli Reguler (k)", 0.5, "D", "Tidak ada data patroli pasca-2025; sensitivitas 0–1"),
 ("Laju Penurunan Partisipasi Sukarela", 0, "D", "Sensitivitas"), ("Proporsi Penggantian Anggota Patroli", 1, "D", "A1"),
 ("Dana Operasional Non Karbon Tunai", 0, "D – PERLU DATA", "Dana desa/APBD/program belum tercatat"), ("Dukungan Material Rehabilitasi Non Karbon", 0, "D – PERLU DATA", "Sumber realisasi historis 0,0123 belum diketahui"),
 ("Porsi Tenaga Penanaman Non Karbon Dibayar", 0, "D – PERLU DATA", ""), ("Nilai Pendampingan Kelembagaan Non Tunai", 0, "D – PERLU DATA", ""), ("Laju Pembelajaran Kelembagaan", 0, "D", ""),
 ("Biaya Reaktivasi KUPS (Rp)", 5e7, "D", "= biaya pembentukan"), ("Porsi Laba Ditahan untuk Reinvestasi", 0.5, "D", ""), ("Status Pembiayaan Awal", "hibah (0)", "D – PERLU DATA", ""),
 ("Switch Pemulihan Talangan Sebelum Bagi Hasil", 1, "Desain", "bukan aturan kontraktual"), ("Biaya Pengembangan Proyek (Rp/th)", 0, "D – PERLU DATA", "parameter berupa aliran tahunan konstan; perlu jadwal"),
 ("Tingkat Diskonto", 0.10, "D", "tidak bersumber"), ("Delay Pembayaran Penjualan (th)", 0, "D", ""), ("Delay Verifikasi dan Penerbitan Kredit (th)", 3, "A (register A1)", ""),
 ("Efektivitas Perlindungan Penuh", 0.37, "D (register FINAL)", "literatur luar lokasi"), ("Waktu Penyesuaian Efek Pengelolaan PS (th)", 3, "D", ""),
 ("Norma kebutuhan patroli (4 orang/regu; 750 ha/regu; 12 HOK/orang)", "7.996 HOK/th", "D / tanpa sumber", ""), ("Rasio Risiko Penempatan Patroli", 0.651, "C", "log 2023"),
 ("Keikutsertaan Patroli 2023", 2160, "B", "392 × 5,51"), ("Biaya per Hari Patroli (Rp/HOK)", 260000, "C – PERLU KONFIRMASI SATUAN", "per orang-hari vs per regu-hari"),
 ("Upah Harian Patroli Berbayar (Rp/HOK)", 130000, "C", ""), ("Harga Karbon Removal / ARR (USD)", 20, "keputusan peneliti", "tetap, tidak ikut variasi harga REDD"),
 ("Pengali Kehilangan Akses", 1, "D", "0–3,24"), ("Biaya Operasional Patroli Sukarela per Anggota (Rp/th)", 1192050, "C", "nilai logistik non-tunai; ketersediaan tidak terbukti (D1)")],
 columns=["Parameter", "Nilai dasar", "Kelas / status", "Catatan"]).to_excel(W, sheet_name="8 Register asumsi", index=False)
W.close(); print("ok")
