"""FINAL handoff: complete metadata for every master attribute and every Vensim parameter row,
enforce completeness, and write the version-freeze manifest. No new analysis.

Decision vocabulary for REV3 (KEPUTUSAN_REV3):
  SIAP_DIGUNAKAN      can be used in REV3 as is (still with stated uncertainty)
  HANYA_SENSITIVITAS  use only in sensitivity runs (includes items that become 'ready' once a stated
                      condition - conversion, validation, definition check - is met; see SYARAT_NAIK_STATUS)
  BELUM_LAYAK         not fit for use in REV3
Usage: python s22_finalize_freeze.py
"""
import hashlib
import json

import pandas as pd

from common import MASTER_VERSION, ROOT

P = ROOT / "08_FINAL_FOR_VENSIM"
M = P / "01_MASTER_SPATIAL"
V = P / "03_VENSIM_INPUT"
DEC = {"LANGSUNG": "SIAP_DIGUNAKAN", "SENSITIVITAS_SAJA": "HANYA_SENSITIVITAS",
       "PERLU_KONVERSI_ATAU_KALIBRASI": "HANYA_SENSITIVITAS", "TIDAK_DAPAT_DIGUNAKAN": "BELUM_LAYAK"}

PA, SK = "PROJECT_AREA (25 poligon, 111.123,16 ha UTM / 111.134,95 ha geodesik)", "SK HD (geometri 125.456 ha UTM; tabel 124.941 ha)"
# field -> (DOMAIN, TAHUN_PERIODE, STATUS_VALIDASI, KEPUTUSAN_REV3, SYARAT_NAIK_STATUS)
F = {
    "HD_ID": ("-", "-", "KUNCI", "SIAP_DIGUNAKAN", ""), "HD_NAME": ("-", "-", "KUNCI (alias terdokumentasi)", "SIAP_DIGUNAKAN", ""),
    "LANDSCAPE": ("-", "-", "KUNCI", "SIAP_DIGUNAKAN", ""), "REGENCY": ("-", "-", "KUNCI", "SIAP_DIGUNAKAN", ""),
    "SK_NUMBER": ("SK (tabel)", "2017-2024", "TRANSKRIPSI Tabel 1 HCV; cocok dengan .dbf SK", "SIAP_DIGUNAKAN", ""),
    "SK_DATE": ("SK (tabel)", "2017-2024", "TRANSKRIPSI Tabel 1 HCV", "SIAP_DIGUNAKAN", ""),
    "SK_AREA_HA": ("SK (tabel)", "statis", "TRANSKRIPSI Tabel 1 HCV (jumlah 124.941 ha)", "SIAP_DIGUNAKAN", ""),
    "AREA_HA": (PA, "2026", "TERVERIFIKASI QA geometri (Gate 1)", "SIAP_DIGUNAKAN", ""),
    "AREA_UTM49S_HA": (PA, "2026", "TERVERIFIKASI; selisih PDD -0,04 ha", "SIAP_DIGUNAKAN", ""),
    "PA_TO_SK_RATIO": ("PA/SK", "statis", "TURUNAN terukur (pangsa luas)", "HANYA_SENSITIVITAS", "Konfirmasi definisi 'Proporsi Kredit REDD' di .mdl"),
    "TREE_2000_HA": (PA, "2000", "PRODUK GLOBAL (Hansen v1.13); belum divalidasi lokal", "HANYA_SENSITIVITAS", "Konversi tutupan pohon->hutan (faktor 0,835) disetujui peneliti"),
    "TREE_2024_HA": (PA, "2024", "TURUNAN (tanpa regrowth); bukan peta hutan", "HANYA_SENSITIVITAS", "-"),
    "LOSS_2001_2024_HA": (PA, "2001-2024", "PRODUK GLOBAL; patahan metode 2011", "HANYA_SENSITIVITAS", "Sampel akurasi (Olofsson 2014)"),
    "LOSS_2001_2014_HA": (PA, "2001-2014", "PRODUK GLOBAL; 2001-2010 belum diproses ulang", "HANYA_SENSITIVITAS", "Sampel akurasi"),
    "LOSS_2015_2016_HA": (PA, "2015-2016", "PRODUK GLOBAL; pulsa kebakaran", "HANYA_SENSITIVITAS", "Sampel akurasi"),
    "LOSS_2017_2024_HA": (PA, "2017-2024", "PRODUK GLOBAL; pasca-SK", "HANYA_SENSITIVITAS", "Sampel akurasi"),
    "LOSS_RATE_HA_YEAR": (PA, "2001-2024", "TURUNAN; non-stasioner", "HANYA_SENSITIVITAS", "Sampel akurasi + pemetaan ke variabel laju .mdl"),
    "LOSS_RATE_PCT_YEAR": (PA, "2001-2024", "TURUNAN; non-stasioner", "HANYA_SENSITIVITAS", "Sampel akurasi + pemetaan ke variabel laju .mdl"),
    "LOSS_2001_2024_T10_HA": (PA, "2001-2024", "SENSITIVITAS ambang 10 %", "HANYA_SENSITIVITAS", "-"),
    "LOSS_2001_2024_T50_HA": (PA, "2001-2024", "SENSITIVITAS ambang 50 %", "HANYA_SENSITIVITAS", "-"),
    "LOSS_IN_MANGROVE_2001_2024_HA": (PA, "2001-2024", "OVERLAY produk global", "HANYA_SENSITIVITAS", "-"),
    "FOREST_2024_HA": (PA, "2024", "TIDAK TERSEDIA (tidak ada klasifikasi hutan 2024 tervalidasi)", "BELUM_LAYAK", "Klasifikasi hutan 2024 + sampel referensi"),
    "FOREST_2024_FLAG": ("-", "-", "META", "SIAP_DIGUNAKAN", ""),
    "PEAT_HA": (PA, "survei 2024 / peta 2025", "PIHAK KETIGA; konsisten Tabel 14 (+/-0,01 ha); belum divalidasi independen", "HANYA_SENSITIVITAS", "Validasi silang kriging + masker mangrove konsisten (G9)"),
    "PEAT_FLAG": ("-", "-", "META", "SIAP_DIGUNAKAN", ""),
    "PEAT_GE300_HA": (PA, "survei 2024 / peta 2025", "PIHAK KETIGA; belum divalidasi independen", "HANYA_SENSITIVITAS", "Validasi kedalaman"),
    "PEAT_MEAN_DEPTH_M": (PA, "survei 2024 / peta 2025", "TURUNAN titik-tengah kelas", "HANYA_SENSITIVITAS", "Validasi kedalaman"),
    "MANGROVE_SED_HA": (PA, "survei 2024 / peta 2025", "PIHAK KETIGA; 44 % selisih vs GMW = patch masker >1 km (QA3)", "HANYA_SENSITIVITAS", "Masker mangrove direkonsiliasi (bukan dikoreksi otomatis dengan GMW)"),
    "MANGROVE_SED_GE50_HA": (PA, "survei 2024 / peta 2025", "PIHAK KETIGA", "HANYA_SENSITIVITAS", "idem"),
    "MINERAL_OR_PEAT_LT50_HA": (PA, "survei 2024 / peta 2025", "PIHAK KETIGA", "HANYA_SENSITIVITAS", "idem"),
    "PEAT_SK_HA": (SK, "survei 2024 / peta 2025", "PIHAK KETIGA", "HANYA_SENSITIVITAS", "Validasi kedalaman"),
    "PEAT_SOIL_C_STOCK_TC": (PA, "survei 2024 / peta 2025", "KONTEKS STOK (bukan emisi/kredit)", "BELUM_LAYAK", "Tidak untuk kredit; emisi WRC butuh model drainase/subsidensi (di luar cakupan)"),
    "MANGROVE_SED_C_STOCK_TC": (PA, "survei 2024 / peta 2025", "KONTEKS STOK (bukan emisi/kredit)", "BELUM_LAYAK", "idem"),
    "MANGROVE_HA": (PA, "2020", "PRODUK GLOBAL (GMW v3.0)", "HANYA_SENSITIVITAS", "Konversi definisi GMW -> stratum mangrove model"),
    "MANGROVE_1996_HA": (PA, "1996", "PRODUK GLOBAL (GMW v3.0)", "HANYA_SENSITIVITAS", "-"),
    "PEAT_DEPTH_SURVEY_M": ("titik survei per desa", "2024", "OBSERVASI TITIK (bukan rata-rata spasial HD)", "HANYA_SENSITIVITAS", "-"),
    "MANGROVE_SED_DEPTH_SURVEY_M": ("titik survei per desa", "2024", "OBSERVASI TITIK", "HANYA_SENSITIVITAS", "-"),
    "SK_GEOM_HA": (SK, "kompilasi 2025", "KOMPILASI OPERASIONAL (bukan salinan legal tersertifikasi); cocok nomor SK 37/37", "SIAP_DIGUNAKAN", "Verifikasi terhadap peta lampiran SK untuk penggunaan legal"),
    "PA_INSIDE_SK_PCT": ("PA/SK", "statis", "TERUKUR (99,94 %)", "SIAP_DIGUNAKAN", ""),
    "TREE_2000_SK_HA": (SK, "2000", "PRODUK GLOBAL", "HANYA_SENSITIVITAS", "idem TREE_2000_HA"),
    "LOSS_2001_2024_SK_HA": (SK, "2001-2024", "PRODUK GLOBAL", "HANYA_SENSITIVITAS", "Sampel akurasi"),
    "MANGROVE_SK_HA": (SK, "2020", "PRODUK GLOBAL", "HANYA_SENSITIVITAS", "-"),
    "R1_TREECOVER_SHARE": ("PA/SK", "2000", "TURUNAN terukur", "HANYA_SENSITIVITAS", "Konfirmasi definisi 'Proporsi Kredit REDD' di .mdl"),
    "R2_ACTIVITY_SHARE": ("PA/SK", "2001-2024", "TURUNAN terukur; bergantung periode", "HANYA_SENSITIVITAS", "Konfirmasi bahwa parameter .mdl = pangsa aktivitas deforestasi"),
    "BPS_NAME_LOCATION_FLAG": ("-", "2020", "META", "SIAP_DIGUNAKAN", ""),
    "SOURCE": ("-", "-", "META", "SIAP_DIGUNAKAN", ""), "QA_STATUS": ("-", "-", "META", "SIAP_DIGUNAKAN", ""),
    "QA_NOTE": ("-", "-", "META", "SIAP_DIGUNAKAN", ""), "MASTER_VERSION": ("-", "-", "META", "SIAP_DIGUNAKAN", ""),
}


def val_status(r):
    s = f"{r.SUMBER} {r.STATUS_DATA}"
    if pd.isna(r.NILAI):
        return "TIDAK TERSEDIA"
    if "Shapefile Delta_Kapuas" in s or "TERVERIFIKASI" in s:
        return "TERVERIFIKASI (QA geometri)"
    if "ASUMSI" in r.STATUS_DATA:
        return "ASUMSI PENELITI (tidak terdokumentasi)"
    if "Laporan Gambut" in s:
        return "PIHAK KETIGA; konsisten Tabel 14/15; belum divalidasi independen"
    if r.STATUS_DATA.startswith("HCV"):
        return "DIUJI KONSISTENSI vs satelit (domain SK)"
    if "TRANSKRIPSI" in r.STATUS_DATA or "Laporan HCV" in r.SUMBER and "SK" in r.KONSEP_TARGET:
        return "TRANSKRIPSI tabel HCV"
    if "KANDIDAT" in r.STATUS_DATA or "ESTIMASI" in r.STATUS_DATA:
        return "TURUNAN TERUKUR; belum divalidasi lokal"
    if "OBSERVASI PETA" in r.STATUS_DATA:
        return "PRODUK GLOBAL TERDOKUMENTASI; belum divalidasi lokal"
    return "LIHAT KETIDAKPASTIAN"


def syarat(r):
    if r.KELAS_PENGGUNAAN == "PERLU_KONVERSI_ATAU_KALIBRASI":
        if "Proporsi" in r.TARGET_VENSIM_VARIABLE:
            return "Naik ke SIAP jika persamaan .mdl mendefinisikan parameter sebagai pangsa aktivitas deforestasi"
        if "gambut" in r.KONSEP_TARGET.lower():
            return "Naik ke SIAP setelah validasi silang kedalaman dan rekonsiliasi masker mangrove (G9)"
        if "konversi" in r.KONSEP_TARGET.lower():
            return "Naik ke SIAP jika model memakai luas hutan HCV dan peneliti menyetujui faktor konversi"
        return "Naik ke SIAP setelah konversi definisi ke variabel model"
    if r.KELAS_PENGGUNAAN == "TIDAK_DAPAT_DIGUNAKAN":
        return "Tidak untuk REV3 pada versi ini"
    if r.KELAS_PENGGUNAAN == "SENSITIVITAS_SAJA":
        return "Sensitivitas; naik status hanya dengan sampel akurasi/validasi independen"
    return ""


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    # --- master data dictionary ---
    dd = pd.read_csv(M / "DKP_25HD_DATA_DICTIONARY.csv")
    missing = sorted(set(dd.FIELD_GPKG) - set(F))
    assert not missing, f"metadata missing for {missing}"
    meta = pd.DataFrame([(k, *v) for k, v in F.items()],
                        columns=["FIELD_GPKG", "DOMAIN", "TAHUN_PERIODE", "STATUS_VALIDASI", "KEPUTUSAN_REV3", "SYARAT_NAIK_STATUS"])
    dd = dd.drop(columns=[c for c in meta.columns if c != "FIELD_GPKG" and c in dd.columns]).merge(meta, on="FIELD_GPKG", how="left")
    for c in ["UNIT", "DOMAIN", "TAHUN_PERIODE", "SOURCE", "STATUS_VALIDASI", "KEPUTUSAN_REV3"]:
        assert dd[c].notna().all() and (dd[c].astype(str).str.len() > 0).all(), c
    dd["MASTER_VERSION"] = MASTER_VERSION
    dd.to_csv(M / "DKP_25HD_DATA_DICTIONARY.csv", index=False)

    # --- Vensim parameter table ---
    v = pd.read_csv(V / "DKP_VENSIM_SPATIAL_INPUT.csv")
    v["STATUS_VALIDASI"] = [val_status(r) for r in v.itertuples()]
    v["KEPUTUSAN_REV3"] = v.KELAS_PENGGUNAAN.map(DEC)
    v.loc[v.NILAI.isna(), "KEPUTUSAN_REV3"] = "BELUM_LAYAK"
    v["SYARAT_NAIK_STATUS"] = [syarat(r) for r in v.itertuples()]
    v["MASTER_VERSION"] = MASTER_VERSION
    req = ["UNIT", "DOMAIN_SPASIAL", "TAHUN_PERIODE", "SUMBER", "STATUS_VALIDASI", "KEPUTUSAN_REV3"]
    for c in req:
        bad = v[c].isna() | (v[c].astype(str).str.strip().isin(["", "-"]) & (c != "UNIT"))
        assert not bad.any(), (c, v.loc[bad, ["VAR_ID", "KONSEP_TARGET"]])
    assert v.VAR_ID.is_unique
    v.to_csv(V / "DKP_VENSIM_SPATIAL_INPUT.csv", index=False, encoding="utf-8-sig")
    xl = pd.read_excel(V / "DKP_VENSIM_SPATIAL_PARAMETERS.xlsx", sheet_name=None)
    with pd.ExcelWriter(V / "DKP_VENSIM_SPATIAL_PARAMETERS.xlsx") as xw:
        pd.DataFrame({"README": [
            f"{MASTER_VERSION} - versi BEKU untuk integrasi Vensim REV3. Model .mdl tidak diubah.",
            "KEPUTUSAN_REV3: SIAP_DIGUNAKAN / HANYA_SENSITIVITAS / BELUM_LAYAK. SYARAT_NAIK_STATUS menyebut syarat agar status naik.",
            "Gross tree-cover loss != net forest loss != deforestasi regulasi. Stok karbon tanah != emisi yang dapat dikreditkan; tidak ada kredit dihitung dari stok.",
            "Nama variabel Vensim: hanya 'Proporsi Kredit REDD dalam Project Area' (diberikan peneliti); lainnya 'BELUM DIPETAKAN'.",
        ]}).to_excel(xw, sheet_name="README", index=False)
        v.to_excel(xw, sheet_name="SEMUA_PARAMETER", index=False)
        for k, sh in [("SIAP_DIGUNAKAN", "A_SIAP_REV3"), ("HANYA_SENSITIVITAS", "B_SENSITIVITAS"), ("BELUM_LAYAK", "C_BELUM_LAYAK")]:
            v[v.KEPUTUSAN_REV3 == k].to_excel(xw, sheet_name=sh, index=False)
        for k in ["CROSSWALK_GIS_VENSIM", "PER_HD"]:
            xl[k].to_excel(xw, sheet_name=k, index=False)
        dd.to_excel(xw, sheet_name="KAMUS_ATRIBUT_MASTER", index=False)
        v.groupby(["KEPUTUSAN_REV3", "KATEGORI"]).size().unstack(fill_value=0).to_excel(xw, sheet_name="RINGKASAN")
    print(v.groupby(["KEPUTUSAN_REV3", "KATEGORI"]).size().unstack(fill_value=0))
    print(dd.KEPUTUSAN_REV3.value_counts())

    # --- freeze manifest ---
    files = sorted(list(M.glob("*")) + list(V.glob("*")))
    man = {"MASTER_VERSION": MASTER_VERSION, "FROZEN_ON": "2026-11-01",
           "POLICY": "Master dibekukan. Tidak ada perluasan analisis GIS; perubahan hanya lewat versi baru (v1.1+) dengan changelog.",
           "FILES": {f.name: sha(f) for f in files if f.is_file()}}
    (P / "VERSION_FREEZE.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(len(man["FILES"]), "files frozen")


if __name__ == "__main__":
    main()
