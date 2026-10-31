"""Peat / mangrove-sediment depth classes per HD (PA and SK) from the report's own vector layers.

Input (supplied 31-10-2026, 'Data Kedalaman Gambut_Mangrove_Mineral'):
  Soil_Depth_rev120425.shp  22 class polygons (Peat 50-1400 cm in 14 classes, Mangrove sediment 0-600 cm
                            in 7 classes, 'Mineral' = mineral soil + peat < 50 cm), EPSG:32749
  Gambut_Data_WAS.shp / Mangrove_Data_WAS.shp  subsets used only for consistency checks.
These are vectorised classes of the report's ordinary-kriging raster (10 m). They are used AS DELIVERED:
no re-interpolation, no polygons drawn from survey points. Invalid geometries are repaired with make_valid
(logged). Accuracy caveats of the source (report QA G3-G5) still apply.

Outputs: 03_LAND_COVER_CHANGE/SOIL_DEPTH_BY_HD_LONG.csv, SOIL_DEPTH_BY_HD_WIDE.csv
         04_VALIDATION/SOIL_DEPTH_LAYER_QA.csv
         08_FINAL_FOR_VENSIM/02_THEMATIC_LAYERS/DKP_SOIL_DEPTH_CLASS_PA.gpkg/.shp and _SK.gpkg
Usage: python s20_peat_overlay.py <dir with Soil_Depth_rev120425.shp>
"""
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.validation import make_valid

from common import ROOT, _GEOD

warnings.simplefilter("ignore")
TH = ROOT / "08_FINAL_FOR_VENSIM" / "02_THEMATIC_LAYERS"
# Laporan Gambut & Mangrove 2025, Tabel 14 (area, ha) and Tabel 15 (mean stock, tC/ha) by class
T14 = {("Mangrove", "0-50"): 41696.741, ("Mangrove", "50-100"): 6080.896, ("Mangrove", "100-200"): 3799.048,
       ("Mangrove", "200-300"): 799.776, ("Mangrove", "300-400"): 275.247, ("Mangrove", "400-500"): 51.431,
       ("Mangrove", "500-600"): 0.003, ("Peat", "50-100"): 6191.779, ("Peat", "100-200"): 7894.630,
       ("Peat", "200-300"): 3724.607, ("Peat", "300-400"): 4461.665, ("Peat", "400-500"): 4461.746,
       ("Peat", "500-600"): 3574.672, ("Peat", "600-700"): 3340.525, ("Peat", "700-800"): 3639.126,
       ("Peat", "800-900"): 3855.582, ("Peat", "900-1000"): 3478.437, ("Peat", "1000-1100"): 1320.885,
       ("Peat", "1100-1200"): 819.011, ("Peat", "1200-1300"): 340.980, ("Peat", "1300-1400"): 77.130}
T15 = {("Mangrove", "0-50"): 69.31, ("Mangrove", "50-100"): 466.08, ("Mangrove", "100-200"): 816.43,
       ("Mangrove", "200-300"): 1388.91, ("Mangrove", "300-400"): 1851.47, ("Mangrove", "400-500"): 2234.74,
       ("Mangrove", "500-600"): 2148.29, ("Peat", "50-100"): 366.54, ("Peat", "100-200"): 787.16,
       ("Peat", "200-300"): 1293.53, ("Peat", "300-400"): 1995.61, ("Peat", "400-500"): 2743.88,
       ("Peat", "500-600"): 3513.94, ("Peat", "600-700"): 4254.12, ("Peat", "700-800"): 5029.13,
       ("Peat", "800-900"): 5769.51, ("Peat", "900-1000"): 6465.39, ("Peat", "1000-1100"): 7267.90,
       ("Peat", "1100-1200"): 8012.05, ("Peat", "1200-1300"): 8739.61, ("Peat", "1300-1400"): 9292.57}


def poly(g):
    g = make_valid(g) if not g.is_valid else g
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    parts = [p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")]
    return gpd.GeoSeries(parts).union_all() if parts else None


def gha(g):
    return abs(_GEOD.geometry_area_perimeter(g)[0]) / 1e4 if g is not None and not g.is_empty else 0.0


def mid_cm(d):
    if not isinstance(d, str):
        return 0.0
    a, b = d.split("-")
    return (float(a) + float(b)) / 2


def overlay(soil, zones, label):
    rows = []
    for z in zones.itertuples():
        hit = soil.iloc[soil.sindex.query(z.geometry, predicate="intersects")]
        for s in hit.itertuples():
            inter = s.geometry.intersection(z.geometry)
            if inter.is_empty:
                continue
            inter = poly(inter)
            if inter is None:
                continue
            rows.append({"DOMAIN": label, "HD_ID": z.HD_ID, "HD_NAME": z.HD_NAME, "LANDSCAPE": z.LANDSCAPE,
                         "SOIL": s.Soil_rev, "DEPTH_CLASS_CM": s.Depth if isinstance(s.Depth, str) else "-",
                         "AREA_UTM_HA": inter.area / 1e4, "geometry": inter})
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=32749)


def main(src):
    src = Path(src)
    soil = gpd.read_file(src / "Soil_Depth_rev120425.shp")
    assert soil.crs.to_epsg() == 32749
    n_bad = int((~soil.geometry.is_valid).sum())
    soil["geometry"] = soil.geometry.apply(poly)
    soil["AREA_UTM_HA"] = soil.area / 1e4
    qa = []
    for r in soil.itertuples():
        key = (r.Soil_rev, r.Depth if isinstance(r.Depth, str) else None)
        rep = T14.get(key, np.nan)
        qa.append({"CHECK": "class area vs Tabel 14", "SOIL": r.Soil_rev, "DEPTH": r.Depth, "LAYER_UTM_HA": r.AREA_UTM_HA,
                   "REPORT_TABEL14_HA": rep, "DIFF_HA": r.AREA_UTM_HA - rep if pd.notna(rep) else np.nan})
    tot = soil.AREA_UTM_HA.sum()
    union = soil.geometry.union_all().area / 1e4
    sep = {n: gpd.read_file(src / f"{n}.shp").to_crs(32749) for n in ["Gambut_Data_WAS", "Mangrove_Data_WAS"]}
    sk = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "SK_25HD_BOUNDARY.gpkg").to_crs(32749)
    pa = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg").to_crs(32749)
    sku = sk.union_all()
    su = soil.geometry.union_all()
    qa += [
        {"CHECK": "invalid geometries repaired (make_valid)", "LAYER_UTM_HA": n_bad},
        {"CHECK": "sum of class areas (ha)", "LAYER_UTM_HA": tot},
        {"CHECK": "union area (ha); sum-union = overlap", "LAYER_UTM_HA": union, "DIFF_HA": tot - union},
        {"CHECK": "Gambut_Data_WAS total vs Peat classes", "LAYER_UTM_HA": sep["Gambut_Data_WAS"].geometry.apply(poly).area.sum() / 1e4,
         "REPORT_TABEL14_HA": soil[soil.Soil_rev == "Peat"].AREA_UTM_HA.sum()},
        {"CHECK": "Mangrove_Data_WAS total vs Mangrove classes", "LAYER_UTM_HA": sep["Mangrove_Data_WAS"].geometry.apply(poly).area.sum() / 1e4,
         "REPORT_TABEL14_HA": soil[soil.Soil_rev == "Mangrove"].AREA_UTM_HA.sum()},
        {"CHECK": "SK geometry area (ha)", "LAYER_UTM_HA": sku.area / 1e4},
        {"CHECK": "soil layer outside SK (ha)", "LAYER_UTM_HA": su.difference(sku).area / 1e4},
        {"CHECK": "SK not covered by soil layer (ha)", "LAYER_UTM_HA": sku.difference(su).area / 1e4},
        {"CHECK": "stock check: sum(area x Tabel15 mean) peat (tC)",
         "LAYER_UTM_HA": sum(r.AREA_UTM_HA * T15.get((r.Soil_rev, r.Depth), 0) for r in soil.itertuples() if r.Soil_rev == "Peat"),
         "REPORT_TABEL14_HA": 144114915.20},
        {"CHECK": "stock check: sum(area x Tabel15 mean) mangrove sediment (tC)",
         "LAYER_UTM_HA": sum(r.AREA_UTM_HA * T15.get((r.Soil_rev, r.Depth), 0) for r in soil.itertuples() if r.Soil_rev == "Mangrove"),
         "REPORT_TABEL14_HA": 10561043.94},
    ]
    qa = pd.DataFrame(qa)
    qa.to_csv(ROOT / "04_VALIDATION" / "SOIL_DEPTH_LAYER_QA.csv", index=False)
    print(qa.round(2).to_string())

    out = []
    for lab, zones in (("PROJECT_AREA", pa), ("SK_HD", sk)):
        o = overlay(soil, zones, lab)
        o["AREA_HA"] = o.to_crs(4326).geometry.apply(gha)
        o["MID_CM"] = o.DEPTH_CLASS_CM.apply(lambda d: mid_cm(d) if d != "-" else 0.0)
        o["SOIL_C_TC_CONTEXT"] = [a * T15.get((s, d), 0.0) for a, s, d in zip(o.AREA_UTM_HA, o.SOIL, o.DEPTH_CLASS_CM)]
        out.append(o)
        o.to_crs(4326).to_file(TH / f"DKP_SOIL_DEPTH_CLASS_{'PA' if lab == 'PROJECT_AREA' else 'SK'}.gpkg",
                               layer="soil_depth_class", driver="GPKG")
        if lab == "PROJECT_AREA":
            o.to_crs(4326).rename(columns={"DEPTH_CLASS_CM": "DEPTH_CM", "AREA_UTM_HA": "AREA_UTM", "SOIL_C_TC_CONTEXT": "SOILC_TC"}
                                  ).to_file(TH / "DKP_SOIL_DEPTH_CLASS_PA.shp", driver="ESRI Shapefile", encoding="UTF-8")
    long = pd.concat(out).drop(columns="geometry")
    long.to_csv(ROOT / "03_LAND_COVER_CHANGE" / "SOIL_DEPTH_BY_HD_LONG.csv", index=False)

    def agg(g):
        pe, mg = g[g.SOIL == "Peat"], g[g.SOIL == "Mangrove"]
        deep = pe.loc[np.array([d != "-" and float(d.split("-")[0]) >= 300 for d in pe.DEPTH_CLASS_CM], dtype=bool)]
        return pd.Series({
            "PEAT_GE50_HA": pe.AREA_HA.sum(), "PEAT_GE300_HA": deep.AREA_HA.sum(),
            "MANGROVE_SED_HA": mg.AREA_HA.sum(),
            "MANGROVE_SED_GE50_HA": mg[mg.DEPTH_CLASS_CM != "0-50"].AREA_HA.sum(),
            "MINERAL_OR_PEAT_LT50_HA": g[g.SOIL == "Mineral"].AREA_HA.sum(),
            "PEAT_MEAN_DEPTH_M": (pe.AREA_HA * pe.MID_CM).sum() / pe.AREA_HA.sum() / 100 if len(pe) else np.nan,
            "PEAT_C_TC_CONTEXT": pe.SOIL_C_TC_CONTEXT.sum(), "MANGROVE_SED_C_TC_CONTEXT": mg.SOIL_C_TC_CONTEXT.sum(),
            "CLASSIFIED_HA": g.AREA_HA.sum()})
    wide = long.groupby(["DOMAIN", "HD_ID", "HD_NAME", "LANDSCAPE"]).apply(agg, include_groups=False).reset_index()
    wide.to_csv(ROOT / "03_LAND_COVER_CHANGE" / "SOIL_DEPTH_BY_HD_WIDE.csv", index=False)
    pd.set_option("display.width", 250)
    print(wide.round(1).to_string())
    print(wide.groupby(["DOMAIN", "LANDSCAPE"])[["PEAT_GE50_HA", "PEAT_GE300_HA", "MANGROVE_SED_HA", "MANGROVE_SED_GE50_HA",
                                                  "MINERAL_OR_PEAT_LT50_HA", "CLASSIFIED_HA", "PEAT_C_TC_CONTEXT"]].sum().round(0))


if __name__ == "__main__":
    main(sys.argv[1])
