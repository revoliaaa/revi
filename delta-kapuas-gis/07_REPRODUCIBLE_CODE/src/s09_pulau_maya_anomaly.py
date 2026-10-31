"""Pulau Maya HCV 2019->2024 anomaly: independent Landsat/GMW/Hansen evidence.

Domains:
  PROJECT_AREA_PM  the 5 Pulau Maya Project Area polygons (15,308 ha geodesic; ~95 % of
                   the 16,103 ha HCV study area, whose geometry is not available)
  DESA_PLUS_1KM    the 5 Pulau Maya BPS desa polygons + 1 km (a superset; every quantity
                   there is an UPPER BOUND for the HCV/HD area)

Tests
  A  Newly vegetated area 2019->2024: pixels non-/sparsely vegetated in the 2019
     median composite (NDVI < 0.4, or MNDWI > 0) that are densely vegetated in
     2024 (NDVI >= 0.6). Real mangrove expansion of +3,773 ha (HCV) would have to
     appear here (mangrove colonisation of mudflat/water or regrowth of cleared land).
  B  Same test for 2014->2019 (reference period with no reported anomaly).
  C  Stability of the GMW-2020 mangrove stratum: NDVI/NDMI distributions by epoch.
  D  Observation-count adequacy (pixels with < 3 valid observations flagged).
Thresholds are sensitivity choices (0.5/0.6/0.7 tested), not calibrated class rules.

Usage: python -I s09_pulau_maya_anomaly.py <landsat_dir> <desa_context.gpkg> <gmw_dir> <project_area_clean.gpkg>
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import Resampling, reproject

from common import ROOT, row_pixel_area_ha
from s03_zonal_stats import gmw_mosaic


def load(ldir, y):
    with rasterio.open(Path(ldir) / f"LANDSAT_OLI_MEDIAN_{y}_NDVI_NDMI_MNDWI_NOBS.tif") as r:
        a = r.read().astype("float32")
        tr, shape = r.transform, (r.height, r.width)
    nd = a[0] == -32768
    ndvi, ndmi, mndwi = [np.where(nd, np.nan, a[i] / 10000) for i in range(3)]
    return dict(NDVI=ndvi, NDMI=ndmi, MNDWI=mndwi, NOBS=a[3]), tr, shape


def main(ldir, gpkg, gmw_dir, pa_gpkg):
    E = {}
    for y in (2014, 2019, 2024):
        E[y], tr, shape = load(ldir, y)
    pa_px = row_pixel_area_ha(tr, shape[0])[:, None] * np.ones((1, shape[1]))
    d = gpd.read_file(gpkg)
    pm = d[d.LANDSCAPE == "Pulau Maya"]
    buf = gpd.GeoSeries([pm.union_all()], crs=d.crs).to_crs(32749).buffer(1000).to_crs(4326).iloc[0]
    desa_dom = rasterize([(buf, 1)], out_shape=shape, transform=tr, dtype="uint8") == 1
    pa = gpd.read_file(pa_gpkg).query("LANDSCAPE == 'Pulau Maya'")
    pa_dom = rasterize([(pa.union_all(), 1)], out_shape=shape, transform=tr, dtype="uint8") == 1
    g20, gtr = gmw_mosaic(gmw_dir, 2020)
    gm_all = np.zeros(shape, "uint8")
    reproject(g20.astype("uint8"), gm_all, src_transform=gtr, src_crs="EPSG:4326", dst_transform=tr,
              dst_crs="EPSG:4326", resampling=Resampling.nearest)
    rows = []
    for dname, dom in (("PROJECT_AREA_PM", pa_dom), ("DESA_PLUS_1KM", desa_dom)):
        gm = (gm_all == 1) & dom
        rows += tests(E, pa_px, dom, gm, dname)
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "04_VALIDATION" / "PULAU_MAYA_LANDSAT_TESTS.csv", index=False)
    pd.set_option("display.width", 250)
    print(out.round(2).to_string())
    np.savez_compressed(Path(ldir) / "_pm_masks.npz", dom=desa_dom, pa=pa_dom, gm=(gm_all == 1) & desa_dom)


def tests(E, pa, dom, gm, dname):
    rows = []
    for y, e in E.items():
        valid = dom & np.isfinite(e["NDVI"])
        rows.append({"TEST": "D obs adequacy", "EPOCH": y, "DOMAIN_HA": pa[dom].sum(),
                     "VALID_COMPOSITE_HA": pa[valid].sum(),
                     "PCT_DOMAIN_WITH_LT3_OBS": 100 * pa[dom & (e["NOBS"] < 3)].sum() / pa[dom].sum(),
                     "MEDIAN_NOBS": float(np.median(e["NOBS"][dom]))})
        for t in (0.5, 0.6, 0.7):
            rows.append({"TEST": "Vegetated area", "EPOCH": y, "NDVI_THRESHOLD": t,
                         "AREA_HA": pa[valid & (e["NDVI"] >= t)].sum()})
        rows.append({"TEST": "Water/wet surface (MNDWI>0)", "EPOCH": y, "AREA_HA": pa[valid & (e["MNDWI"] > 0)].sum()})
        rows.append({"TEST": "C GMW-2020 stratum", "EPOCH": y,
                     "GMW2020_HA_IN_DOMAIN": pa[gm].sum(),
                     "NDVI_MEDIAN": float(np.nanmedian(e["NDVI"][gm])),
                     "NDMI_MEDIAN": float(np.nanmedian(e["NDMI"][gm])),
                     "PCT_GMW_PX_NDVI_LT_0.5": 100 * pa[gm & (e["NDVI"] < 0.5)].sum() / pa[gm & np.isfinite(e["NDVI"])].sum()})
    for a, b in ((2014, 2019), (2019, 2024)):
        A, B = E[a], E[b]
        both = dom & np.isfinite(A["NDVI"]) & np.isfinite(B["NDVI"])
        for t in (0.5, 0.6, 0.7):
            new_veg = both & ((A["NDVI"] < 0.4) | (A["MNDWI"] > 0)) & (B["NDVI"] >= t)
            lost_veg = both & (A["NDVI"] >= t) & ((B["NDVI"] < 0.4) | (B["MNDWI"] > 0))
            from_water = both & (A["MNDWI"] > 0) & (B["NDVI"] >= t)
            rows.append({"TEST": f"{'A' if a == 2019 else 'B'} transition {a}->{b}", "NDVI_THRESHOLD": t,
                         "NEWLY_VEGETATED_HA": pa[new_veg].sum(),
                         "of_which_FROM_WATER_OR_MUDFLAT_HA": pa[from_water].sum(),
                         "of_which_OUTSIDE_GMW2020_HA": pa[new_veg & ~gm].sum(),
                         "DEVEGETATED_HA": pa[lost_veg].sum(),
                         "COMPARED_HA": pa[both].sum(),
                         "HCV_REPORTED_MANGROVE_GAIN_HA": 3773 if a == 2019 else None})
    for r in rows:
        r["DOMAIN"] = dname
    return rows


if __name__ == "__main__":
    main(*sys.argv[1:5])
