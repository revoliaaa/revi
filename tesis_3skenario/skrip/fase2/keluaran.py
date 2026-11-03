import json, pandas as pd, numpy as np, sys
sys.path.insert(0, "work"); from lib import yearly
R = json.load(open("fase2/hasil_uji_struktural.json")); log = json.load(open("fase2/DKP_25HD_FINAL_2SKENARIO.mdl.log.json"))
teks = json.load(open("fase2/u0b_teks.json")); u4 = json.load(open("fase2/u4.json")); npv = pd.read_json("fase2/npv_sementara.json")
cache = pd.read_pickle("fase2/cache_runs.pkl")
OUT = sys.argv[1]
W = pd.ExcelWriter(OUT, engine="openpyxl")
st = pd.DataFrame(R["struktural"]); pe = pd.DataFrame(R["perilaku"])
allt = pd.concat([st.assign(Kelompok=np.where(st.Kode.str.startswith("E"), "Kondisi ekstrem", "Struktural")), pe.assign(Kelompok="Perilaku kausal")])
summ = allt.groupby(["Kelompok", "Status"]).size().unstack(fill_value=0)
readme = pd.DataFrame({"Isi": [
 "HASIL UJI STRUKTURAL FASE 2 – DKP_25HD_FINAL_2SKENARIO.mdl (md5 aa1428dffdc27541d531926b9806c50e)",
 "Semua uji dijalankan dengan PySD 3.14.3, Euler, DT 0,0625 (U6: juga 0,03125). Vensim native TIDAK digunakan (U0c BELUM DAPAT DIUJI).",
 "Parameter dasar: S1 = Skenario Kebijakan 1; S2 = 2; k = 0,5 (asumsi kerja); kas non-karbon 0; dukungan material 0; hibah; pemulihan talangan sebelum bagi hasil; baseline kredit BAU.",
 "Uji ini memeriksa konsistensi struktur, neraca, dan arah perilaku. Uji ini BUKAN validasi empiris dan BUKAN hasil penelitian.",
 "NPV pada lembar 'NPV sementara' belum memuat biaya pengembangan proyek dan biaya material non-karbon; jangan dipakai sebagai hasil tesis atau dasar harga impas."]})
readme.to_excel(W, sheet_name="0 README", index=False)
summ.to_excel(W, sheet_name="1 Ringkasan")
st[~st.Kode.str.startswith("E")].to_excel(W, sheet_name="2 Uji struktural", index=False)
st[st.Kode.str.startswith("E")].to_excel(W, sheet_name="3 Kondisi ekstrem", index=False)
pe.to_excel(W, sheet_name="4 Perilaku kausal", index=False)
pd.DataFrame([{"Ukuran": k, "Nilai": (", ".join(v) if isinstance(v, list) else v)} for k, v in teks.items()]).to_excel(W, sheet_name="5 U0b teks", index=False)
pd.DataFrame({"Variabel berbeda S1 vs S2 sebelum kas karbon pertama (semua keuangan/kredit)": u4["beda"]}).to_excel(W, sheet_name="6 U4 variabel", index=False)
npv.to_excel(W, sheet_name="7 NPV sementara", index=False)
keys = ["Total Hutan", "Deforestasi Total", "Total HOK Patroli", "HOK Patroli Reguler PS", "Hari Patroli Didanai", "Indeks Intensitas Perlindungan", "Efek Pengelolaan PS Aktif",
        "Kas Penjualan Kredit", "Dana Desa Diterima", "Penggunaan Dana Pengelolaan", "Saldo Dana LPHD", "Kebutuhan Dana Minimum", "Kesenjangan Pembiayaan Minimum",
        "Jumlah KUPS Aktif", "Modal Usaha KUPS", "Kesempatan Kerja Berupah Setara Penuh", "Kesempatan Kerja Sukarela Setara Penuh", "Pendapatan Bersih per RT Bergantung",
        "Nilai Kontribusi Swadaya", "Kredit REDD Diajukan", "Potensi Kredit REDD Konservatif"]
ser = {}
for lab, df in cache.items():
    av, fi = yearly(df[[k for k in keys if k in df.columns]])
    for k in keys:
        if k in df.columns: ser[(lab, k)] = (fi[k] if k in ("Total Hutan", "Saldo Dana LPHD", "Modal Usaha KUPS") else av[k])
s = pd.DataFrame(ser); s.columns = [f"{a} | {b}" for a, b in s.columns]; s.index.name = "Tahun"
s.to_excel(W, sheet_name="8 Seri uji (bukan hasil)")
pd.DataFrame(log, columns=["Kode", "Variabel", "Jenis", "Lama", "Baru", "Satuan", "Alasan"]).to_excel(W, sheet_name="9 Log perubahan", index=False)
W.close()
# log markdown
L = ["# Log Implementasi Fase 2: DKP_25HD_FINAL_2SKENARIO.mdl", "",
 "**Sumber:** `DKP_25HD_FINAL_3SKENARIO.mdl` (md5 `5af5a34e…`, tidak ditimpa). **Hasil:** `DKP_25HD_FINAL_2SKENARIO.mdl` (md5 `aa1428df…`), 817 variabel, 16 View.",
 "",
 "**Cara membangun:** `skrip/fase2/build_2s.py` menyusun ulang model 3 skenario dari register dan REV-3S, lalu menerapkan `skrip/fase1b/usulan.py`. Persamaan G menimpa K/C. Tambahan Fase 2 (D2, F1, F3) ditulis di `build_2s.py`.",
 "",
 f"**Verifikasi teks (U0b):** {teks['identik']}/{teks['rancangan']} persamaan di berkas `.mdl` identik dengan rancangan; {teks['tak_diubah_identik']} persamaan yang tidak diubah identik dengan model 3 skenario.",
 "",
 "Setiap persamaan baru atau diubah memuat tag `REV-2S 2026-11-03 [kode]` dan persamaan lamanya di komentar Vensim.", "",
 "| No | Kode | Variabel | Jenis | Persamaan lama | Persamaan baru | Satuan | Alasan |", "|---|---|---|---|---|---|---|---|"]
for i, (k, n, j, o, nw, u, why) in enumerate(log, 1):
    esc = lambda x: str(x).replace("|", "/").replace("\n", " ")
    L.append(f"| {i} | {k} | `{n}` | {j} | `{esc(o) if o else '—'}` | `{esc(nw) if nw else '—'}` | {u} | {esc(why) or '–'} |")
open(sys.argv[2], "w").write("\n".join(L) + "\n")
print(summ)
