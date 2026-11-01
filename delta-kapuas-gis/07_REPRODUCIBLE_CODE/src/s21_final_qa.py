"""FINAL QA (handoff) - measurements for checks 1, 3 and 4. No new thematic analysis.

  Q1  Soil-class total vs Project Area: reconcile on ONE area basis (UTM 49S planar = PDD convention),
      decompose the residual (PA outside SK, gaps of the soil layer inside SK, overlay residue), and
      show the unit-mixing component (geodesic vs planar).
  Q3  Mangrove sediment (report) vs GMW 2020 mangrove: pixel-level agreement on the native GMW grid,
      distance of disagreeing pixels to the other layer (registration vs fringe vs separate patches),
      soil class under GMW-only pixels, tree cover under sediment-only pixels, and comparison with the
      HCV 2024 mangrove total. Nothing is corrected.
  Q4  Effect of make_valid on every input layer: per-feature area before/after (and buffer(0) as an
      alternative repair), feature counts, overlaps and gaps.
Usage: python s21_final_qa.py <soil_dir> <sk_shp> <gmw_dir>
"""
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import Resampling, reproject
from scipy.ndimage import distance_transform_edt
from shapely.validation import explain_validity, make_valid

from common import CODE, ROOT, row_pixel_area_ha
from s03_zonal_stats import gmw_mosaic

warnings.simplefilter("ignore")
OUT = ROOT / "08_FINAL_FOR_VENSIM" / "04_QA_DOCS" / "FINAL_QA"


def polyonly(g):
    if g is None or g.is_empty:
        return g
    g = make_valid(g) if not g.is_valid else g
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    parts = [p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")]
    return gpd.GeoSeries(parts).union_all() if parts else None


def safe(f):
    try:
        return f()
    except Exception as e:  # GEOS topology errors on invalid input
        return f"NOT COMPUTABLE ({type(e).__name__})"


def q4(layers):
    feat, summ = [], []
    for name, g in layers.items():
        g = g.to_crs(32749)
        before_valid = g.geometry.is_valid
        a_before = g.area / 1e4
        fixed = g.geometry.apply(polyonly)
        buf0 = g.geometry.buffer(0)
        for i in np.where(~before_valid)[0]:
            feat.append({"LAYER": name, "FID": int(i), "REASON": explain_validity(g.geometry.iloc[i]),
                         "AREA_BEFORE_SHOELACE_HA": a_before.iloc[i], "AREA_AFTER_MAKE_VALID_HA": fixed.iloc[i].area / 1e4,
                         "AREA_BUFFER0_HA": buf0.iloc[i].area / 1e4,
                         "DIFF_MAKE_VALID_HA": fixed.iloc[i].area / 1e4 - a_before.iloc[i],
                         "DIFF_MAKE_VALID_VS_BUFFER0_HA": (fixed.iloc[i].area - buf0.iloc[i].area) / 1e4})
        fg = gpd.GeoSeries(fixed, crs=32749)
        degenerate = int((fg.area < 100).sum())   # < 0.01 ha
        sum_after = fg.area.sum() / 1e4
        union_after = fg.union_all().area / 1e4
        union_before = safe(lambda: g.geometry.union_all().area / 1e4)
        summ.append({"LAYER": name, "N_FEATURES_BEFORE": len(g), "N_INVALID_BEFORE": int((~before_valid).sum()),
                     "N_FEATURES_AFTER": int(len(fg) - degenerate), "N_DEGENERATE_DROPPED(<0.01ha)": degenerate,
                     "SUM_AREA_BEFORE_HA": a_before.sum(), "SUM_AREA_AFTER_HA": sum_after,
                     "DIFF_SUM_HA": sum_after - a_before.sum(),
                     "UNION_BEFORE_HA": union_before, "UNION_AFTER_HA": union_after,
                     "OVERLAP_AFTER_HA (sum-union)": sum_after - union_after,
                     "OVERLAP_BEFORE_HA": (a_before.sum() - union_before) if isinstance(union_before, float) else union_before})
    return pd.DataFrame(summ), pd.DataFrame(feat)


def main(soil_dir, sk_shp, gmw_dir):
    OUT.mkdir(parents=True, exist_ok=True)
    soil_dir = Path(soil_dir)
    soil = gpd.read_file(soil_dir / "Soil_Depth_rev120425.shp")
    sk_raw = gpd.read_file(sk_shp)
    pa = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg").to_crs(32749)
    sk = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "SK_25HD_BOUNDARY.gpkg").to_crs(32749)

    # ---------------- Q4 make_valid ----------------
    layers = {"PROJECT_AREA (shp 21-05-2026)": gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg"),
              "SK (SHP Gabungan HD)": sk_raw, "Soil_Depth_rev120425": soil,
              "Gambut_Data_WAS": gpd.read_file(soil_dir / "Gambut_Data_WAS.shp"),
              "Mangrove_Data_WAS": gpd.read_file(soil_dir / "Mangrove_Data_WAS.shp")}
    s4, f4 = q4(layers)
    soil_fix = soil.to_crs(32749).copy()
    soil_fix["geometry"] = soil_fix.geometry.apply(polyonly)
    sku = sk.union_all()
    su = soil_fix.union_all()
    gap_sk = sku.difference(su).area / 1e4
    s4["GAP_SK_NOT_COVERED_BY_SOIL_HA"] = np.where(s4.LAYER == "Soil_Depth_rev120425", gap_sk, np.nan)
    s4.to_csv(OUT / "Q4_MAKE_VALID_SUMMARY.csv", index=False)
    f4.to_csv(OUT / "Q4_MAKE_VALID_PER_FEATURE.csv", index=False)

    # ---------------- Q1 soil total vs PA ----------------
    pau = pa.union_all()
    pa_utm = pa.area.sum() / 1e4
    covered = pau.intersection(su).area / 1e4
    unc = pau.difference(su)
    unc_out_sk = unc.difference(sku).area / 1e4
    unc_in_sk = unc.intersection(sku).area / 1e4
    long = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "SOIL_DEPTH_BY_HD_LONG.csv").query("DOMAIN == 'PROJECT_AREA'")
    soil_utm_sum = long.AREA_UTM_HA.sum()
    soil_geo_sum = long.AREA_HA.sum()
    pa_geo = gpd.read_file(ROOT / "08_FINAL_FOR_VENSIM" / "01_MASTER_SPATIAL" / "DKP_25HD_MASTER_SPATIAL.gpkg",
                           layer="DKP_25HD_MASTER_SPATIAL").AREA_HA.sum()
    q1 = pd.DataFrame([
        ("A  Luas PA, UTM 49S planar (konvensi PDD)", pa_utm),
        ("B  Luas PA, geodesik WGS84 (dipakai statistik zonal)", pa_geo),
        ("C  Jumlah kelas tanah dalam PA, geodesik (angka 111.061)", soil_geo_sum),
        ("D  Jumlah kelas tanah dalam PA, UTM 49S", soil_utm_sum),
        ("E  Selisih yang ditanyakan: A - C (mencampur satuan)", pa_utm - soil_geo_sum),
        ("F  Selisih satuan-sama UTM: A - D", pa_utm - soil_utm_sum),
        ("F1   PA di luar geometri SK (serpihan tepi; layer tanah hanya mencakup SK)", unc_out_sk),
        ("F2   PA di dalam SK tetapi tidak tercakup poligon kelas tanah (gap layer tanah)", unc_in_sk),
        ("F3   Residu overlay (bagian non-poligon yang dibuang, pembulatan) = F - F1 - F2", pa_utm - soil_utm_sum - unc_out_sk - unc_in_sk),
        ("G  Selisih satuan-sama geodesik: B - C", pa_geo - soil_geo_sum),
        ("H  Komponen beda satuan (geodesik - UTM) pada kelas tanah: C - D", soil_geo_sum - soil_utm_sum),
        ("I  Luas PA yang tercakup layer tanah, UTM (cek: = D)", covered),
    ], columns=["ITEM", "HA"])
    q1.to_csv(OUT / "Q1_SOIL_VS_PA_RECONCILIATION.csv", index=False)
    per = []
    for r in pa.itertuples():
        u = r.geometry.difference(su)
        per.append({"HD_ID": r.HD_ID, "HD_NAME": r.HD_NAME, "PA_UTM_HA": r.geometry.area / 1e4,
                    "SOIL_UTM_HA": long[long.HD_ID == r.HD_ID].AREA_UTM_HA.sum(),
                    "UNCOVERED_OUTSIDE_SK_HA": u.difference(sku).area / 1e4, "UNCOVERED_INSIDE_SK_HA": u.intersection(sku).area / 1e4})
    per = pd.DataFrame(per)
    per["RESIDUAL_HA"] = per.PA_UTM_HA - per.SOIL_UTM_HA - per.UNCOVERED_OUTSIDE_SK_HA - per.UNCOVERED_INSIDE_SK_HA
    per.to_csv(OUT / "Q1_PER_HD.csv", index=False)

    # ---------------- Q3 mangrove sediment vs GMW ----------------
    gm, gtr = gmw_mosaic(gmw_dir, 2020)
    shape = gm.shape
    sk4 = sk.to_crs(4326); pa4 = pa.to_crs(4326)
    s4g = soil_fix.to_crs(4326)
    code = {"Mangrove": 1, "Peat": 2, "Mineral": 3}
    soilr = rasterize([(g, code[c]) for g, c in zip(s4g.geometry, s4g.Soil_rev) if g is not None],
                      out_shape=shape, transform=gtr, dtype="uint8")
    skm = rasterize([(sk4.union_all(), 1)], out_shape=shape, transform=gtr, dtype="uint8") == 1
    pam = rasterize([(pa4.union_all(), 1)], out_shape=shape, transform=gtr, dtype="uint8") == 1
    hdr = rasterize([(g, i + 1) for i, g in enumerate(sk4.geometry)], out_shape=shape, transform=gtr, dtype="uint8")
    A = row_pixel_area_ha(gtr, shape[0])[:, None] * np.ones((1, shape[1]))
    sed = soilr == 1
    gmw = gm.astype(bool)
    px = abs(gtr.a) * 111320  # ~ metres per pixel at the equator (approx. for distance bins)
    d_to_gmw = distance_transform_edt(~gmw) * px
    d_to_sed = distance_transform_edt(~sed) * px
    with rasterio.open(ROOT / "02_REMOTE_SENSING_DATA" / "FOREST_COVER_BASELINE_2000_canopy_pct.tif") as r:
        tc = np.zeros(shape, "uint8")
        reproject(r.read(1), tc, src_transform=r.transform, src_crs=r.crs, dst_transform=gtr, dst_crs="EPSG:4326",
                  resampling=Resampling.nearest)
    bins = [(0, 30, "<=30 m (registrasi/resolusi piksel)"), (30, 250, "30-250 m (tepi/peralihan)"),
            (250, 1000, "250-1000 m"), (1000, 1e9, ">1000 m (patch terpisah)")]
    rows = []
    for dom, M in (("SK_HD", skm), ("PROJECT_AREA", pam)):
        so, go, both = M & sed & ~gmw, M & gmw & ~sed, M & sed & gmw
        rows += [{"DOMAIN": dom, "ITEM": "Sedimen mangrove (laporan)", "HA": A[M & sed].sum()},
                 {"DOMAIN": dom, "ITEM": "Mangrove GMW 2020", "HA": A[M & gmw].sum()},
                 {"DOMAIN": dom, "ITEM": "Keduanya (irisan)", "HA": A[both].sum()},
                 {"DOMAIN": dom, "ITEM": "Hanya sedimen (tidak dipetakan GMW)", "HA": A[so].sum()},
                 {"DOMAIN": dom, "ITEM": "Hanya GMW (tidak dipetakan sebagai sedimen)", "HA": A[go].sum()},
                 {"DOMAIN": dom, "ITEM": "Kesesuaian (irisan / gabungan)", "HA": A[both].sum() / A[M & (sed | gmw)].sum()}]
        for lo, hi, lab in bins:
            rows.append({"DOMAIN": dom, "ITEM": f"Hanya sedimen, jarak ke GMW {lab}", "HA": A[so & (d_to_gmw > lo) & (d_to_gmw <= hi)].sum()})
        for lo, hi, lab in bins:
            rows.append({"DOMAIN": dom, "ITEM": f"Hanya GMW, jarak ke sedimen {lab}", "HA": A[go & (d_to_sed > lo) & (d_to_sed <= hi)].sum()})
        for c, k in code.items():
            if c != "Mangrove":
                rows.append({"DOMAIN": dom, "ITEM": f"Hanya GMW, kelas tanah laporan = {c}", "HA": A[go & (soilr == k)].sum()})
        rows.append({"DOMAIN": dom, "ITEM": "Hanya GMW, di luar layer tanah", "HA": A[go & (soilr == 0)].sum()})
        rows.append({"DOMAIN": dom, "ITEM": "Hanya sedimen, tutupan pohon 2000 >30 % (Hansen)", "HA": A[so & (tc > 30)].sum()})
    hcv = pd.read_csv(CODE / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv")
    rows.append({"DOMAIN": "HCV/SK", "ITEM": "Kelas mangrove HCV 2024 (tabel)", "HA": hcv[(hcv.FOREST_TYPE == "MANGROVE") & (hcv.YEAR == 2024)].AREA_HA.sum()})
    rows.append({"DOMAIN": "HCV/SK", "ITEM": "Kelas mangrove HCV 2019 (tabel)", "HA": hcv[(hcv.FOREST_TYPE == "MANGROVE") & (hcv.YEAR == 2019)].AREA_HA.sum()})
    q3 = pd.DataFrame(rows)
    q3.to_csv(OUT / "Q3_MANGROVE_SEDIMENT_VS_GMW.csv", index=False)
    hd = []
    for i, r in enumerate(sk4.itertuples(), start=1):
        m = hdr == i
        so, go = m & sed & ~gmw, m & gmw & ~sed
        hd.append({"HD_ID": r.HD_ID, "HD_NAME": r.HD_NAME, "LANDSCAPE": r.LANDSCAPE, "SED_HA": A[m & sed].sum(),
                   "GMW_HA": A[m & gmw].sum(), "BOTH_HA": A[m & sed & gmw].sum(), "SED_ONLY_HA": A[so].sum(),
                   "GMW_ONLY_HA": A[go].sum(), "SED_ONLY_GT1KM_HA": A[so & (d_to_gmw > 1000)].sum(),
                   "SED_ONLY_LE30M_HA": A[so & (d_to_gmw <= 30)].sum()})
    hd = pd.DataFrame(hd)
    hd["DOMINANT_CAUSE"] = np.select(
        [hd.SED_ONLY_HA + hd.GMW_ONLY_HA < 50,
         hd.SED_ONLY_GT1KM_HA > 0.5 * hd.SED_ONLY_HA,
         hd.SED_ONLY_LE30M_HA > 0.5 * hd.SED_ONLY_HA],
        ["SELARAS (<50 ha selisih)", "PATCH TERPISAH >1 km: masker/klasifikasi", "TEPI <=30 m: registrasi/resolusi"],
        default="TEPI/PERALIHAN 30-1000 m: definisi ekosistem (mangrove belakang, nipah, peralihan rawa)")
    hd.to_csv(OUT / "Q3_PER_HD.csv", index=False)
    pd.set_option("display.width", 250)
    for df in (q1, per.round(2), q3, hd, s4, f4):
        print(df.round(3).to_string(), "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
