"""MASTER SPATIAL DATABASE 25 HD + thematic layers for Vensim REV3 integration.

Builds, from results already computed by s03/s06/s14 (no re-analysis):
  08_FINAL_FOR_VENSIM/01_MASTER_SPATIAL/DKP_25HD_MASTER_SPATIAL.gpkg   (primary; full field names)
  08_FINAL_FOR_VENSIM/01_MASTER_SPATIAL/DKP_25HD_MASTER_SPATIAL.shp    (<=10-char field names)
  08_FINAL_FOR_VENSIM/01_MASTER_SPATIAL/DKP_25HD_DATA_DICTIONARY.csv
  08_FINAL_FOR_VENSIM/02_THEMATIC_LAYERS/*.tif, mangrove polygons (gpkg+shp)

Rules: the 25 original Project Area polygons are kept unchanged (only reprojection-free copy);
attributes that cannot be estimated validly are left NULL and carry a *_FLG explanation.

Usage: python s15_master_spatial.py <gmw_dir>
"""
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize, shapes
from rasterio.windows import from_bounds
from shapely.geometry import shape

from common import ROOT, _GEOD, row_pixel_area_ha
from s03_zonal_stats import gmw_mosaic

OUT = ROOT / "08_FINAL_FOR_VENSIM"
M, T = OUT / "01_MASTER_SPATIAL", OUT / "02_THEMATIC_LAYERS"
RS = ROOT / "02_REMOTE_SENSING_DATA"

# Survey means per desa label, Laporan Gambut & Mangrove 2025, Tabel 11 (PDF p.57-58).
PEAT_DEPTH_M = {"Medan Mas": 11.0, "Betuah": 10.3, "Batu Ampar": 9.6, "Tasik Malaya": 9.2, "Tanjung Harapan": 7.6,
                "Nipah Panjang": 7.0, "Sungai Besar": 6.9, "Teluk Bakung": 6.4, "Teluk Nibung": 5.5,
                "Kampung Baru": 4.9, "Ambawang": 4.4, "Sungai Jawi": 3.5, "Satai Lestari": 3.2, "Ambarawa": 2.0,
                "Tanjung Beringin": 1.2}
MANG_DEPTH_M = {"Tanjung Harapan": 2.0, "Batu Ampar": 1.7, "Mengkalang": 1.1, "Tanjung Beringin": 0.6,
                "Nipah Panjang": 0.6, "Tanjung Satai": 0.2, "Ambarawa": 0.2}

# (gpkg full name, shp name, unit, definition, source, status)
DICT = [
    ("HD_ID", "HD_ID", "-", "Kode HD (HD01-HD25) sesuai desain studi", "Studi", "KEY"),
    ("HD_NAME", "HD_NAME", "-", "Nama Hutan Desa / LPHD", "Shapefile PA (NAMA_DESA) + alias terdokumentasi", "KEY"),
    ("LANDSCAPE", "LANDSCAPE", "-", "Lanskap: Kubu / Padang Tikar / Pulau Maya", "Desain studi", "KEY"),
    ("REGENCY", "REGENCY", "-", "Kabupaten", "Desain studi", "KEY"),
    ("SK_NUMBER", "SK_NO", "-", "Nomor SK penetapan HD", "Laporan HCV Tabel 1", "TABULAR"),
    ("SK_DATE", "SK_DATE", "date", "Tanggal SK penetapan HD", "Laporan HCV Tabel 1", "TABULAR"),
    ("SK_AREA_HA", "SK_HA", "ha", "Luas SK (tabel, bukan geometri)", "Laporan HCV Tabel 1", "TABULAR"),
    ("AREA_HA", "AREA_HA", "ha", "Luas poligon Project Area, geodesik elipsoid WGS84 (dipakai semua statistik zonal)", "Shapefile PA 21-05-2026", "OBSERVASI_GEOMETRI"),
    ("AREA_UTM49S_HA", "AREA_UTM", "ha", "Luas planar WGS84/UTM 49S (konvensi PDD; total 111.123,16 ha)", "Shapefile PA", "OBSERVASI_GEOMETRI"),
    ("PA_TO_SK_RATIO", "PA_SK", "fraksi", "AREA_UTM49S_HA / SK_AREA_HA (pangsa luas, BUKAN pangsa kredit)", "Turunan", "ESTIMASI_SPASIAL"),
    ("TREE_2000_HA", "TREE00_HA", "ha", "Tutupan pohon 2000: kanopi >30 % vegetasi >5 m (Hansen). BUKAN hutan legal", "Hansen GFC v1.13", "OBSERVASI_EMPIRIS"),
    ("TREE_2024_HA", "TREE24_HA", "ha", "Tutupan pohon 2000 (>30 %) TANPA loss terdeteksi 2001-2024 = tutupan pohon persisten. Batas bawah tutupan pohon 2024 (regrowth tidak dihitung)", "Hansen GFC v1.13", "ESTIMASI_SPASIAL"),
    ("LOSS_2001_2024_HA", "LOSS0124", "ha", "Gross tree-cover loss 2001-2024 di dalam TREE_2000 (bukan net forest loss, bukan deforestasi regulasi)", "Hansen GFC v1.13", "OBSERVASI_EMPIRIS"),
    ("LOSS_2001_2014_HA", "LOSS0114", "ha", "Gross loss 2001-2014 (jendela kalibrasi; 2001-2010 belum diproses ulang UMD)", "Hansen GFC v1.13", "OBSERVASI_EMPIRIS"),
    ("LOSS_2015_2016_HA", "LOSS1516", "ha", "Gross loss 2015-2016 (tahun El Nino/kebakaran)", "Hansen GFC v1.13", "OBSERVASI_EMPIRIS"),
    ("LOSS_2017_2024_HA", "LOSS1724", "ha", "Gross loss 2017-2024 (setelah mayoritas SK HD)", "Hansen GFC v1.13", "OBSERVASI_EMPIRIS"),
    ("LOSS_RATE_HA_YEAR", "LOSS_RATE", "ha/tahun", "Rata-rata gross loss 2001-2024 (24 tahun)", "Turunan Hansen", "ESTIMASI_SPASIAL"),
    ("LOSS_RATE_PCT_YEAR", "LOSS_PCT", "%/tahun", "LOSS_RATE_HA_YEAR / TREE_2000_HA x 100", "Turunan Hansen", "ESTIMASI_SPASIAL"),
    ("LOSS_2001_2024_T10_HA", "LOSS_T10", "ha", "Sensitivitas: gross loss dengan definisi kanopi >10 %", "Hansen GFC v1.13", "SENSITIVITAS"),
    ("LOSS_2001_2024_T50_HA", "LOSS_T50", "ha", "Sensitivitas: gross loss dengan definisi kanopi >50 %", "Hansen GFC v1.13", "SENSITIVITAS"),
    ("LOSS_IN_MANGROVE_2001_2024_HA", "LOSS_MG", "ha", "Gross loss (kanopi >30 %) di dalam ekstensi GMW 2010", "Hansen x GMW v3", "ESTIMASI_SPASIAL"),
    ("FOREST_2024_HA", "FOREST24", "ha", "Luas HUTAN 2024 menurut definisi kelas hutan tervalidasi", "-", "NOT_AVAILABLE"),
    ("FOREST_2024_FLAG", "FOR24_FLG", "-", "Alasan FOREST_2024_HA kosong", "-", "FLAG"),
    ("PEAT_HA", "PEAT_HA", "ha", "Luas gambut berdasarkan geometri", "-", "NOT_AVAILABLE"),
    ("PEAT_FLAG", "PEAT_FLG", "-", "Alasan PEAT_HA kosong", "-", "FLAG"),
    ("MANGROVE_HA", "MANGR_HA", "ha", "Ekstensi mangrove GMW v3.0 tahun 2020 (definisi GMW; BUKAN kelas mangrove HCV)", "GMW v3.0", "OBSERVASI_EMPIRIS"),
    ("MANGROVE_1996_HA", "MANGR96", "ha", "Ekstensi mangrove GMW v3.0 tahun 1996 (stabilitas)", "GMW v3.0", "OBSERVASI_EMPIRIS"),
    ("PEAT_DEPTH_SURVEY_M", "PT_DEPTH", "m", "Rata-rata kedalaman gambut plot survei per label desa (Laporan Gambut 2025, Tabel 11). Rata-rata TITIK, bukan rata-rata spasial HD", "Laporan Gambut & Mangrove 2025", "OBSERVASI_TITIK"),
    ("MANGROVE_SED_DEPTH_SURVEY_M", "MG_DEPTH", "m", "Rata-rata kedalaman sedimen mangrove plot survei per label desa (Tabel 11)", "Laporan Gambut & Mangrove 2025", "OBSERVASI_TITIK"),
    ("BPS_NAME_LOCATION_FLAG", "LOC_FLAG", "-", "Poligon PA tidak terutama berada di desa BPS bernama sama (informasi; tidak memengaruhi atribut PA)", "Overlay BPS 2020", "FLAG"),
    ("SOURCE", "SOURCE", "-", "Ringkasan sumber data atribut", "-", "META"),
    ("QA_STATUS", "QA_STATUS", "-", "PASS / PASS_WITH_NOTES", "QA s06/s15", "META"),
    ("QA_NOTE", "QA_NOTE", "-", "Catatan QA per HD", "QA s06/s15", "META"),
]


def build_master():
    pa = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg")
    z = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "ZONAL_PROJECT_AREA.csv")
    sk = pd.read_csv(ROOT / "07_REPRODUCIBLE_CODE" / "inputs" / "HCV_SK_AREAS.csv")
    loc = pd.read_excel(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx", sheet_name="NAME_LOCATION_VS_BPS_DESA")
    L = lambda t, a, b: z[[f"LOSS_{y}_GT{t}" for y in range(a, b + 1)]].sum(axis=1)
    d = pd.DataFrame({"HD_ID": z.HD_ID, "HD_NAME": z.HD_NAME, "LANDSCAPE": z.LANDSCAPE, "REGENCY": z.REGENCY})
    d = d.merge(sk[["HD_NAME", "SK_NUMBER", "SK_DATE", "SK_AREA_HA"]], on="HD_NAME", how="left")
    g = pa[["HD_ID", "GEODESIC_AREA_HA", "UTM49S_PLANAR_AREA_HA", "geometry"]].rename(
        columns={"GEODESIC_AREA_HA": "AREA_HA", "UTM49S_PLANAR_AREA_HA": "AREA_UTM49S_HA"})
    d = g.merge(d, on="HD_ID")
    zz = z.set_index("HD_ID").loc[d.HD_ID]
    d["PA_TO_SK_RATIO"] = d.AREA_UTM49S_HA / d.SK_AREA_HA
    d["TREE_2000_HA"] = zz.TC2000_GT30_HA.values
    d["LOSS_2001_2024_HA"] = L(30, 2001, 2024).loc[zz.index.map(lambda h: z.index[z.HD_ID == h][0])].values
    idx = [z.index[z.HD_ID == h][0] for h in d.HD_ID]
    for k, (a, b) in {"LOSS_2001_2014_HA": (2001, 2014), "LOSS_2015_2016_HA": (2015, 2016),
                      "LOSS_2017_2024_HA": (2017, 2024)}.items():
        d[k] = L(30, a, b).loc[idx].values
    d["TREE_2024_HA"] = d.TREE_2000_HA - d.LOSS_2001_2024_HA
    d["LOSS_RATE_HA_YEAR"] = d.LOSS_2001_2024_HA / 24
    d["LOSS_RATE_PCT_YEAR"] = 100 * d.LOSS_RATE_HA_YEAR / d.TREE_2000_HA
    d["LOSS_2001_2024_T10_HA"] = L(10, 2001, 2024).loc[idx].values
    d["LOSS_2001_2024_T50_HA"] = L(50, 2001, 2024).loc[idx].values
    d["LOSS_IN_MANGROVE_2001_2024_HA"] = z.loc[idx, [f"LOSS_{y}_GT30_IN_GMW2010" for y in range(2001, 2025)]].sum(axis=1).values
    d["FOREST_2024_HA"] = np.nan
    d["FOREST_2024_FLAG"] = "NA: tidak ada klasifikasi hutan 2024 tervalidasi; HCV 2024 inkonsisten antar-epoch (lihat QA). Gunakan TREE_2024_HA sebagai proksi tutupan pohon, bukan hutan."
    d["PEAT_HA"] = np.nan
    d["PEAT_FLAG"] = "NA: raster kedalaman gambut (Laporan 2025) tidak diserahkan; peta GFW butuh API key; poligon tidak dibuat dari titik survei."
    d["MANGROVE_HA"] = zz.MANGROVE_GMW_2020_HA.values
    d["MANGROVE_1996_HA"] = zz.MANGROVE_GMW_1996_HA.values
    d["PEAT_DEPTH_SURVEY_M"] = d.HD_NAME.map(PEAT_DEPTH_M)
    d["MANGROVE_SED_DEPTH_SURVEY_M"] = d.HD_NAME.map(MANG_DEPTH_M)
    lf = loc.set_index("HD_NAME").FLAG
    d["BPS_NAME_LOCATION_FLAG"] = d.HD_NAME.map(lf).fillna("OK")
    d["SOURCE"] = "PA shp 21-05-2026; Hansen GFC-2025-v1.13; GMW v3.0; HCV Tabel 1; Laporan Gambut 2025 Tabel 11"
    notes = []
    for r in d.itertuples():
        n = []
        if r.AREA_HA < 100:
            n.append("poligon kecil (<100 ha): presisi piksel rendah")
        if r.PA_TO_SK_RATIO < 0.75:
            n.append(f"PA hanya {r.PA_TO_SK_RATIO:.2f} dari luas SK")
        if r.HD_NAME == "Kemboja":
            n.append("SK baru 10-06-2024")
        if r.HD_NAME == "Padang Tikar 1":
            n.append("nama di shp 'Padang Tikar' (alias)")
        if pd.isna(r.PEAT_DEPTH_SURVEY_M) and pd.isna(r.MANGROVE_SED_DEPTH_SURVEY_M):
            n.append("tidak ada plot survei gambut/mangrove 2024 berlabel desa ini")
        notes.append("; ".join(n))
    d["QA_NOTE"] = notes
    d["QA_STATUS"] = np.where(d.QA_NOTE == "", "PASS", "PASS_WITH_NOTES")
    order = [c[0] for c in DICT if c[0] in d.columns] + ["geometry"]
    d = gpd.GeoDataFrame(d[order], geometry="geometry", crs=pa.crs).sort_values("HD_ID").reset_index(drop=True)

    # --- QA checks (hard) ---
    assert len(d) == 25 and d.HD_ID.is_unique and d.geometry.is_valid.all()
    assert abs(d.AREA_UTM49S_HA.sum() - 111123.20) < 1.0
    geo = d.geometry.apply(lambda x: abs(_GEOD.geometry_area_perimeter(x)[0]) / 1e4)
    assert np.allclose(geo, d.AREA_HA, atol=0.01)
    assert (d.TREE_2024_HA >= 0).all() and (d.LOSS_2001_2024_HA <= d.TREE_2000_HA).all()
    assert np.allclose(d.LOSS_2001_2014_HA + d.LOSS_2015_2016_HA + d.LOSS_2017_2024_HA, d.LOSS_2001_2024_HA)

    M.mkdir(parents=True, exist_ok=True)
    d.to_file(M / "DKP_25HD_MASTER_SPATIAL.gpkg", layer="DKP_25HD_MASTER_SPATIAL", driver="GPKG")
    ren = {c[0]: c[1] for c in DICT}
    s = d.rename(columns=ren)
    s["SK_DATE"] = s.SK_DATE.astype(str)
    s["QA_NOTE"] = s.QA_NOTE.str.slice(0, 254)
    s["FOR24_FLG"] = s.FOR24_FLG.str.slice(0, 254)
    s["PEAT_FLG"] = s.PEAT_FLG.str.slice(0, 254)
    s.to_file(M / "DKP_25HD_MASTER_SPATIAL.shp", driver="ESRI Shapefile", encoding="UTF-8")
    dd = pd.DataFrame(DICT, columns=["FIELD_GPKG", "FIELD_SHP", "UNIT", "DEFINITION", "SOURCE", "DATA_CLASS"])
    dd["SHP_NAME_LEN_OK"] = dd.FIELD_SHP.str.len() <= 10
    dd.to_csv(M / "DKP_25HD_DATA_DICTIONARY.csv", index=False)
    assert dd.SHP_NAME_LEN_OK.all()
    print(d.drop(columns="geometry").round(2).to_string())
    return d


def clip_to_pa(src_path, pa_union, bounds, nodata, transform_fn=None):
    with rasterio.open(src_path) as r:
        win = from_bounds(*bounds, transform=r.transform).round_offsets().round_lengths()
        a = r.read(1, window=win)
        tr = r.window_transform(win)
        prof = r.profile
    inside = rasterize([(pa_union, 1)], out_shape=a.shape, transform=tr, dtype="uint8") == 1
    return a, inside, tr, prof


def build_layers(gmw_dir, d):
    T.mkdir(parents=True, exist_ok=True)
    U = d.union_all()
    b = d.total_bounds + np.array([-0.002, -0.002, 0.002, 0.002])
    tc, inside, tr, prof = clip_to_pa(RS / "FOREST_COVER_BASELINE_2000_canopy_pct.tif", U, b, 255)
    ly, _, _, _ = clip_to_pa(RS / "ANNUAL_TREE_COVER_LOSS_2001_2025_lossyear.tif", U, b, 255)
    base = dict(driver="GTiff", count=1, dtype="uint16", crs="EPSG:4326", transform=tr, height=tc.shape[0],
                width=tc.shape[1], compress="deflate", tiled=True, blockxsize=256, blockysize=256)
    # 1) Tree cover status (proxy for 'forest cover 2024'; NOT a forest map)
    st = np.full(tc.shape, 0, "uint16")
    t30 = tc > 30
    st[inside & ~t30] = 1
    st[inside & t30 & ((ly == 0) | (ly == 25))] = 2          # persisted to end-2024 (2025 loss excluded from window)
    st[inside & t30 & (ly >= 1) & (ly <= 24)] = 3
    with rasterio.open(T / "DKP_TREECOVER_STATUS_2024_PA.tif", "w", nodata=0, **base) as o:
        o.write(st, 1)
        o.update_tags(CLASSES="0=outside PA; 1=no tree cover >30% in 2000; 2=tree cover 2000 (>30%) with no loss detected 2001-2024 (persistent tree cover, proxy only - NOT forest); 3=tree cover 2000 lost 2001-2024",
                      SOURCE="Hansen GFC-2025-v1.13", GRID="native 0.00025 deg")
    # 2) Loss year 2001-2024 within TC2000>30
    lo = np.where(inside & t30 & (ly >= 1) & (ly <= 24), ly.astype("uint16") + 2000, 0).astype("uint16")
    with rasterio.open(T / "DKP_TREECOVER_LOSS_YEAR_2001_2024_PA.tif", "w", nodata=0, **base) as o:
        o.write(lo, 1)
        o.update_tags(VALUES="year of gross tree-cover loss (2001-2024) within TC2000>30%; 0=no loss/outside PA",
                      SOURCE="Hansen GFC-2025-v1.13")
    A = row_pixel_area_ha(tr, tc.shape[0])[:, None]
    chk = {"STATUS_PERSIST_HA": float((A * (st == 2)).sum()), "STATUS_LOST_HA": float((A * (st == 3)).sum()),
           "LOSSYEAR_HA": float((A * (lo > 0)).sum())}
    # 3) Mangrove GMW 2020: native grid raster + vector (pixel-exact)
    gm, gtr = gmw_mosaic(gmw_dir, 2020)
    with rasterio.MemoryFile() as mf:
        with mf.open(driver="GTiff", count=1, dtype="uint8", crs="EPSG:4326", transform=gtr,
                     height=gm.shape[0], width=gm.shape[1]) as tmp:
            tmp.write(gm.astype("uint8"), 1)
        g, ginside, gtr2, _ = clip_to_pa(mf.name, U, b, 0)
    mg = ((g == 1) & ginside).astype("uint8")
    with rasterio.open(T / "DKP_MANGROVE_GMW2020_PA.tif", "w", driver="GTiff", count=1, dtype="uint8", crs="EPSG:4326",
                       transform=gtr2, height=mg.shape[0], width=mg.shape[1], nodata=0, compress="deflate") as o:
        o.write(mg, 1)
        o.update_tags(VALUES="1=mangrove (GMW v3.0, 2020) inside Project Area", SOURCE="GMW v3.0 doi:10.5281/zenodo.6894273")
    # vectorise ALL GMW pixels in the bbox, then clip exactly to the PA polygons (no pixel-centre pre-mask,
    # which would drop partially covered boundary pixels before the exact intersection)
    gb = (g == 1).astype("uint8")
    polys = [shape(geom) for geom, v in shapes(gb, mask=gb == 1, transform=gtr2) if v == 1]
    mv = gpd.GeoDataFrame(geometry=polys, crs="EPSG:4326")
    mv = gpd.overlay(mv, d[["HD_ID", "HD_NAME", "LANDSCAPE", "geometry"]], how="intersection", keep_geom_type=True)
    mv = mv.dissolve(by=["HD_ID", "HD_NAME", "LANDSCAPE"], as_index=False)
    mv["AREA_HA"] = mv.geometry.apply(lambda x: abs(_GEOD.geometry_area_perimeter(x)[0]) / 1e4)
    mv["SOURCE"] = "GMW v3.0 2020, vectorised native pixels, clipped to PA"
    mv.to_file(T / "DKP_MANGROVE_GMW2020_PA.gpkg", layer="mangrove_gmw2020", driver="GPKG")
    mv.to_file(T / "DKP_MANGROVE_GMW2020_PA.shp", driver="ESRI Shapefile", encoding="UTF-8")
    comp = d[["HD_ID", "MANGROVE_HA"]].merge(mv[["HD_ID", "AREA_HA"]], on="HD_ID", how="left").fillna(0)
    comp["DIFF_HA"] = comp.AREA_HA - comp.MANGROVE_HA
    comp["NOTE"] = "vector = exact clip of pixel polygons; master = pixel-centre rule; differences are boundary pixels"
    chk.update({"MANGROVE_VECTOR_HA": float(mv.AREA_HA.sum()), "MANGROVE_MASTER_HA": float(d.MANGROVE_HA.sum()),
                "MANGROVE_MAX_ABS_DIFF_PER_HD_HA": float(comp.DIFF_HA.abs().max())})
    chk.update({"MASTER_TREE24_HA": float(d.TREE_2024_HA.sum()), "MASTER_LOSS0124_HA": float(d.LOSS_2001_2024_HA.sum())})
    pd.Series(chk).to_csv(T / "LAYER_CONSISTENCY_CHECK.csv", header=["VALUE"])
    comp.to_csv(T / "MANGROVE_VECTOR_VS_MASTER_PER_HD.csv", index=False)
    print(pd.Series(chk).round(2))


if __name__ == "__main__":
    d = build_master()
    build_layers(sys.argv[1], d)
