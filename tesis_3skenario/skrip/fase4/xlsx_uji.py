import json, pandas as pd, sys
R = json.load(open("fase4/uji4_hasil.json")); B = pd.read_json("fase4/banding_kredit.json"); RUNS = json.load(open("fase4/runs4.json"))
W = pd.ExcelWriter(sys.argv[1], engine="openpyxl")
pd.DataFrame({"Isi": ["HASIL UJI MODEL FINAL – MODEL_FINAL_DUA_SKENARIO_PWD.mdl (937 variabel, 16 View), Fase 4 Tahap 2, 2026-11-03",
 "Perangkat: PySD 3.14.3, Euler, DT 0,0625. Units Check dan run native Vensim BELUM DILAKUKAN (V0c).",
 "Konfigurasi dasar: S1 dan S2-C (kredit mode 2 Referensi S1; jembatan J1 Rp782,86 jt/th 2026–2030; biaya modal 0; pemulihan sebelum bagi hasil; aturan henti MRV nonaktif; penggantian reversal aktif); k = 0,5; kas non-karbon 0; upah patroli Rp150.000/HOK; biaya total Rp260.000/HOK (asumsi kerja).",
 "Kriteria uji ditetapkan sebelum melihat hasil. Tiga kriteria direvisi sesudah diagnosis (R1, K3, K7); alasannya dicatat di LAPORAN_VERIFIKASI_MODEL_FINAL.md, lembar 3.",
 "Angka di lembar 2 adalah keluaran uji, bukan hasil penelitian final. NPV SEMENTARA. Kredit model ≠ kredit terverifikasi."]}).to_excel(W, sheet_name="0 README", index=False)
pd.DataFrame(R).to_excel(W, sheet_name="1 Hasil uji", index=False)
B.index.name = "Run"; B.to_excel(W, sheet_name="2 Banding kredit Fase3-4")
pd.DataFrame([{"Kode": "F4-1", "Uji": "K3", "Gejala": "Kredit C > mitigasi berpasangan (1,30× pada USD 6)", "Penyebab": "Reversal: hutan yang diselamatkan jembatan kembali terdeforestasi sesudah ±2052; MAX(0,·) per tahun mengabaikannya", "Kelas": "Kesalahan model (akuntansi kredit)", "Perbaikan": "Saldo mitigasi bertanda + debit dibawa + buffer + pembelian kredit pengganti (arus kas nyata)", "Status": "LULUS"},
 {"Kode": "F4-2", "Uji": "K7", "Gejala": "Galat acuan 2.600 tCO2e/th dengan kas non-karbon", "Penyebab": "Jembatan mengurangi kebutuhan LPHD sehingga dana non-karbon tidak terbelanjakan di S2 (dana dapat dipertukarkan)", "Kelas": "Kesalahan model (atribusi)", "Perbaikan": "Kebutuhan bruto; jembatan mengisi sisa; atribusi non-karbon lebih dulu", "Status": "GAGAL minor: galat kumulatif +163 tCO2e (0,05 %); hanya bila kas non-karbon > 0"},
 {"Kode": "F4-3", "Uji": "T1", "Gejala": "Biaya modal melampaui batas 1,1 %", "Penyebab": "Pembatas memakai stok awal langkah", "Kelas": "Kesalahan model (numerik)", "Perbaikan": "Pembatas eksak MIN(bunga, sisa batas/DT)", "Status": "LULUS"},
 {"Kode": "F4-4", "Uji": "E1b", "Gejala": "Kas penjualan 3·10⁻⁶ Rp pada harga 0", "Penyebab": "Derau numerik; toleransi 10⁻⁶ terlalu ketat", "Kelas": "Kesalahan kriteria", "Perbaikan": "Toleransi 1 Rp", "Status": "LULUS"},
 {"Kode": "F4-5", "Uji": "R1", "Gejala": "Indikator kebutuhan LPHD C20 berbeda 16 %", "Penyebab": "Perubahan definisi terdaftar F4-2 (kebutuhan bruto)", "Kelas": "Kriteria basi", "Perbaikan": "Indikator kebutuhan dikecualikan dan selisihnya dilaporkan; semua variabel lain identik", "Status": "LULUS"},
 {"Kode": "F4-6", "Uji": "K3/K7", "Gejala": "Sisa reversal 30 tCO2e; galat positif sesudah 2046", "Penyebab": "Jeda satu DT pembelian pengganti di akhir horizon; atribusi dana", "Kelas": "Kriteria (toleransi) direvisi", "Perbaikan": "Toleransi 0,5 % reversal; K7 memakai galat kumulatif dan kredit bersih", "Status": "K3 LULUS, K7 GAGAL minor"}]).to_excel(W, sheet_name="3 Kegagalan dan perbaikan", index=False)
pd.DataFrame([{"Run": k, "Parameter": json.dumps(v, ensure_ascii=False)} for k, v in RUNS.items()]).to_excel(W, sheet_name="4 Daftar run", index=False)
W.close(); print("ok")
