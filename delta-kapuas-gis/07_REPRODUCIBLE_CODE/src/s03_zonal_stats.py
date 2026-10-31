"""Per-polygon zonal statistics: Hansen GFC v1.13 + Global Mangrove Watch v3.

Works on ANY polygon layer that carries HD_ID, HD_NAME, LANDSCAPE, REGENCY
(e.g. the BPS desa context domain now, the carbon Project Area once supplied).
Each polygon is rasterised separately (pixel-centre rule) so overlapping
polygons are handled correctly; per-HD observations are kept before any
aggregation.

Indicators (all geodesic-area weighted, ha):
  * POLY_GEODESIC_HA, RASTER_FOOTPRINT_HA (area-conservation check)
  * LAND_HA / WATER_HA  (Hansen datamask 1 / 2)
  * TC2000_GT{t}_HA     tree cover in 2000 with canopy > t %  (t = 10, 30, 50)
  * LOSS_{yyyy}_GT{t}   gross tree-cover loss detected in yyyy inside TC2000>t
  * GAIN_2000_2012_HA   Hansen gain (no year; 2000-2012 only)
  * MANGROVE_GMW_{yyyy} GMW v3 extent on its native 0.8" grid
  * LOSS_{yyyy}_GT{t}_IN_GMW2010  loss inside GMW 2010 mangrove extent

Usage:
  python -I s03_zonal_stats.py <polygons.gpkg> <DOMAIN_LABEL> <gmw_dir> <out_csv>
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window, from_bounds
from rasterio.merge import merge
from rasterio.warp import Resampling, reproject

from common import (AOI_BBOX, CANOPY_THRESHOLDS, GMW_VERSION, GMW_YEARS, HANSEN_VERSION, LOSS_YEARS, ROOT,
                    _GEOD, row_pixel_area_ha)

RS = ROOT / "02_REMOTE_SENSING_DATA"


def load(name):
    with rasterio.open(RS / name) as r:
        return r.read(1), r.transform, r.crs


def gmw_mosaic(gmw_dir, year):
    files = sorted(Path(gmw_dir).glob(f"gmw_v3_{year}/GMW_*_{year}_v3.tif"))
    srcs = [rasterio.open(f) for f in files]
    # keep tiles that intersect the AOI
    srcs = [s for s in srcs if not (s.bounds.right <= AOI_BBOX[0] or s.bounds.left >= AOI_BBOX[2]
                                    or s.bounds.top <= AOI_BBOX[1] or s.bounds.bottom >= AOI_BBOX[3])]
    arr, tr = merge(srcs, bounds=AOI_BBOX, nodata=0)
    for s in srcs:
        s.close()
    return (arr[0] == 1), tr


def zonal(polys, gmw_dir):
    tc, tr, crs = load("FOREST_COVER_BASELINE_2000_canopy_pct.tif")
    ly, _, _ = load("ANNUAL_TREE_COVER_LOSS_2001_2025_lossyear.tif")
    gain, _, _ = load("HANSEN_GAIN_2000_2012.tif")
    dm, _, _ = load("HANSEN_DATAMASK.tif")
    pa = row_pixel_area_ha(tr, tc.shape[0])[:, None] * np.ones((1, tc.shape[1]))

    gmw = {y: gmw_mosaic(gmw_dir, y) for y in GMW_YEARS}
    gtr = gmw[2010][1]
    gpa = row_pixel_area_ha(gtr, gmw[2010][0].shape[0])[:, None] * np.ones((1, gmw[2010][0].shape[1]))
    # GMW 2010 resampled (nearest) to the Hansen grid for loss-in-mangrove
    g10h = np.zeros(tc.shape, dtype="uint8")
    reproject(gmw[2010][0].astype("uint8"), g10h, src_transform=gtr, src_crs="EPSG:4326",
              dst_transform=tr, dst_crs="EPSG:4326", resampling=Resampling.nearest)

    recs = []
    polys = polys.to_crs("EPSG:4326")
    for p in polys.itertuples():
        geom = p.geometry
        rec = {"HD_ID": p.HD_ID, "HD_NAME": p.HD_NAME, "LANDSCAPE": p.LANDSCAPE, "REGENCY": p.REGENCY,
               "POLY_GEODESIC_HA": abs(_GEOD.geometry_area_perimeter(geom)[0]) / 1e4}
        # --- Hansen grid ---
        win = bbox_window(geom, tr, tc.shape)
        r0, c0 = win.row_off, win.col_off
        h, w = win.height, win.width
        wtr = rasterio.windows.transform(win, tr)
        m = rasterize([(geom, 1)], out_shape=(h, w), transform=wtr, fill=0, all_touched=False, dtype="uint8") == 1
        sl = (slice(r0, r0 + h), slice(c0, c0 + w))
        A, TC, LY, G, DM, M10 = pa[sl], tc[sl], ly[sl], gain[sl], dm[sl], g10h[sl] == 1
        rec["RASTER_FOOTPRINT_HA"] = A[m].sum()
        rec["LAND_HA"] = A[m & (DM == 1)].sum()
        rec["WATER_HA"] = A[m & (DM == 2)].sum()
        rec["GAIN_2000_2012_HA"] = A[m & (G == 1)].sum()
        rec["LOSS_ANY_CANOPY_2001_2025_HA"] = A[m & (LY > 0)].sum()
        for t in CANOPY_THRESHOLDS:
            f = m & (TC > t)
            rec[f"TC2000_GT{t}_HA"] = A[f].sum()
            rec[f"GAIN_2000_2012_IN_NONTC{t}_HA"] = A[m & (TC <= t) & (G == 1)].sum()
            fl = LY[f]
            fa = A[f]
            fm = M10[f]
            sums = np.bincount(fl, weights=fa, minlength=26)
            sums_m = np.bincount(fl[fm], weights=fa[fm], minlength=26)
            for k, y in enumerate(LOSS_YEARS, start=1):
                rec[f"LOSS_{y}_GT{t}"] = sums[k]
                rec[f"LOSS_{y}_GT{t}_IN_GMW2010"] = sums_m[k]
        # --- GMW native grid ---
        gwin = bbox_window(geom, gtr, gmw[2010][0].shape)
        gsl = (slice(gwin.row_off, gwin.row_off + gwin.height), slice(gwin.col_off, gwin.col_off + gwin.width))
        gm = rasterize([(geom, 1)], out_shape=(gwin.height, gwin.width),
                       transform=rasterio.windows.transform(gwin, gtr), fill=0, dtype="uint8") == 1
        for y in GMW_YEARS:
            rec[f"MANGROVE_GMW_{y}_HA"] = gpa[gsl][gm & gmw[y][0][gsl]].sum()
        recs.append(rec)
        print(p.HD_ID, p.HD_NAME, round(rec["POLY_GEODESIC_HA"]), round(rec["TC2000_GT30_HA"]),
              round(sum(rec[f'LOSS_{y}_GT30'] for y in LOSS_YEARS)), round(rec["MANGROVE_GMW_2020_HA"]))
    return pd.DataFrame(recs)


def bbox_window(geom, transform, shape):
    """Integer pixel window covering the geometry bounds (+1 px pad), clipped to the grid."""
    w = from_bounds(*geom.bounds, transform=transform)
    r0 = max(int(np.floor(w.row_off)) - 1, 0)
    c0 = max(int(np.floor(w.col_off)) - 1, 0)
    r1 = min(int(np.ceil(w.row_off + w.height)) + 1, shape[0])
    c1 = min(int(np.ceil(w.col_off + w.width)) + 1, shape[1])
    return Window(c0, r0, c1 - c0, r1 - r0)


def to_long(wide, domain):
    """Reshape to the required analysis data structure (one row per HD x year x variable)."""
    base = dict(SPATIAL_DOMAIN=domain, CRS="EPSG:4326 (geodesic WGS84 pixel areas)",
                VALIDATION_STATUS="NOT INDEPENDENTLY VALIDATED IN THIS STUDY")
    rows = []
    for r in wide.itertuples():
        ids = dict(HD_ID=r.HD_ID, HD_NAME=r.HD_NAME, LANDSCAPE=r.LANDSCAPE, REGENCY=r.REGENCY)
        H = dict(DATASET="Hansen GFC", DATASET_VERSION=HANSEN_VERSION, SPATIAL_RESOLUTION="0.00025 deg (~27.8 m)",
                 SOURCE_ID="UMD/hansen/global_forest_change_2025_v1_13")
        for t in CANOPY_THRESHOLDS:
            fd = f"Tree canopy cover 2000 > {t}% (vegetation > 5 m)"
            rows.append({**ids, **base, **H, "YEAR": 2000, "FOREST_DEFINITION": fd,
                         "LAND_COVER_CLASS": "TREE_COVER_2000", "AREA_HA": getattr(r, f"TC2000_GT{t}_HA"),
                         "LOSS_HA": None, "ESTIMATION_METHOD": "Pixel-area sum (pixel-centre rasterisation)",
                         "QUALITY_FLAG": "OBSERVED_MAP_PRODUCT", "UNCERTAINTY": "Map-based; no sample-based area adjustment",
                         "NOTES": "Tree cover, not a forest land-use class; includes tree crops/plantations if >5 m."})
            cum = 0.0
            for y in LOSS_YEARS:
                v = getattr(r, f"LOSS_{y}_GT{t}")
                cum += v
                flag = "OBSERVED_MAP_PRODUCT_PRE2011_NOT_REPROCESSED" if y < 2011 else "OBSERVED_MAP_PRODUCT_REPROCESSED_2011PLUS"
                if y == 2025:
                    flag += ";OUTSIDE_MODEL_HISTORY"
                rows.append({**ids, **base, **H, "YEAR": y, "FOREST_DEFINITION": fd,
                             "LAND_COVER_CLASS": "GROSS_TREE_COVER_LOSS", "AREA_HA": None, "LOSS_HA": v,
                             "ESTIMATION_METHOD": "Pixel-area sum of lossyear==year within TC2000>t",
                             "QUALITY_FLAG": flag,
                             "UNCERTAINTY": "Map-based; omission/commission not quantified locally",
                             "NOTES": f"Gross stand-replacing loss; not deforestation per Indonesian regulation. Cumulative 2001-{y}: {cum:.1f} ha"})
                rows.append({**ids, **base, **H, "YEAR": y, "FOREST_DEFINITION": fd,
                             "LAND_COVER_CLASS": "GROSS_TREE_COVER_LOSS_IN_GMW2010_MANGROVE",
                             "AREA_HA": None, "LOSS_HA": getattr(r, f"LOSS_{y}_GT{t}_IN_GMW2010"),
                             "ESTIMATION_METHOD": "As above, restricted to GMW v3 2010 extent (nearest-resampled to Hansen grid)",
                             "QUALITY_FLAG": flag + ";CROSS_PRODUCT_OVERLAY",
                             "UNCERTAINTY": "Map-based; misregistration between products not quantified",
                             "NOTES": "Mangrove stratum defined by GMW, not by HCV classes."})
        rows.append({**ids, **base, **H, "YEAR": "2000-2012", "FOREST_DEFINITION": "Hansen gain definition",
                     "LAND_COVER_CLASS": "TREE_COVER_GAIN_2000_2012", "AREA_HA": r.GAIN_2000_2012_HA, "LOSS_HA": None,
                     "ESTIMATION_METHOD": "Pixel-area sum of gain==1", "QUALITY_FLAG": "OBSERVED_MAP_PRODUCT;NO_YEAR_OF_GAIN",
                     "UNCERTAINTY": "Gain known to have low accuracy; not used for net change",
                     "NOTES": "Cannot be combined with 2013-2025 loss to estimate net change."})
        G = dict(DATASET="Global Mangrove Watch", DATASET_VERSION=GMW_VERSION, SPATIAL_RESOLUTION="0.0002222 deg (~25 m)",
                 SOURCE_ID="doi:10.5281/zenodo.6894273")
        for y in GMW_YEARS:
            rows.append({**ids, **base, **G, "YEAR": y, "FOREST_DEFINITION": "GMW mangrove extent",
                         "LAND_COVER_CLASS": "MANGROVE", "AREA_HA": getattr(r, f"MANGROVE_GMW_{y}_HA"), "LOSS_HA": None,
                         "ESTIMATION_METHOD": "Pixel-area sum (native GMW grid)", "QUALITY_FLAG": "OBSERVED_MAP_PRODUCT",
                         "UNCERTAINTY": "GMW v3 global accuracy reported by producers; no local validation here",
                         "NOTES": "ALOS PALSAR + Landsat based; tidal/seaward-edge uncertainty."})
    return pd.DataFrame(rows)


def main(poly_path, domain, gmw_dir, out_csv):
    polys = gpd.read_file(poly_path)
    wide = zonal(polys, gmw_dir)
    wide.insert(4, "SPATIAL_DOMAIN", domain)
    out_csv = Path(out_csv)
    wide.to_csv(out_csv, index=False)
    to_long(wide, domain).to_csv(out_csv.with_name(out_csv.stem + "_LONG.csv"), index=False)
    print("area conservation (raster footprint / geodesic polygon):",
          (wide.RASTER_FOOTPRINT_HA / wide.POLY_GEODESIC_HA).describe().round(4).to_dict())


if __name__ == "__main__":
    main(*sys.argv[1:5])
