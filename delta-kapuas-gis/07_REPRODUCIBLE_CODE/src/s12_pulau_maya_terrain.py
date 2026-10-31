"""Pulau Maya 'dryland forest 0 ha (<=2019) -> 580.63 ha (2024)' check.

Copernicus GLO-30 is a DSM (includes canopy, ~20-40 m in swamp/mangrove forest),
so only DSM >= 50 m is treated as indicative of elevated mineral terrain (hills).
For that terrain we report Hansen tree cover 2000 and gross loss 2001-2024: if the
hills were tree-covered throughout, a 'dryland forest' class absent in 2019 and
present in 2024 is more consistent with re-classification (H4) than with new forest (H1).

Usage: python -I s12_pulau_maya_terrain.py <project_area_clean.gpkg>
"""
import json
import sys
import urllib.request

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from pystac_client import Client
from rasterio.features import rasterize
from rasterio.vrt import WarpedVRT
from rasterio.windows import from_bounds

from common import ROOT, row_pixel_area_ha


def main(pa_gpkg):
    pa = gpd.read_file(pa_gpkg).query("LANDSCAPE == 'Pulau Maya'")
    with rasterio.open(ROOT / "02_REMOTE_SENSING_DATA" / "FOREST_COVER_BASELINE_2000_canopy_pct.tif") as r:
        win = from_bounds(*pa.total_bounds, transform=r.transform).round_offsets().round_lengths()
        tc = r.read(1, window=win); tr = r.window_transform(win)
    with rasterio.open(ROOT / "02_REMOTE_SENSING_DATA" / "ANNUAL_TREE_COVER_LOSS_2001_2025_lossyear.tif") as r:
        ly = r.read(1, window=win)
    h, w = tc.shape
    items = list(Client.open("https://planetarycomputer.microsoft.com/api/stac/v1").search(
        collections=["cop-dem-glo-30"], bbox=tuple(pa.total_bounds)).items())
    tok = json.load(urllib.request.urlopen("https://planetarycomputer.microsoft.com/api/sas/v1/token/cop-dem-glo-30"))["token"]
    dem = np.full((h, w), np.nan, "float32")
    for it in items:
        with rasterio.open(it.assets["data"].href + "?" + tok) as s, \
                WarpedVRT(s, crs="EPSG:4326", transform=tr, width=w, height=h, nodata=-9999) as v:
            a = v.read(1).astype("float32"); dem = np.where(a > -9999, a, dem)
    m = rasterize([(pa.union_all(), 1)], out_shape=(h, w), transform=tr, dtype="uint8") == 1
    A = row_pixel_area_ha(tr, h)[:, None] * np.ones((1, w))
    rows = []
    for t in (30, 50, 75, 100):
        z = m & (dem >= t)
        rows.append({"DSM_THRESHOLD_M": t, "PA_PM_AREA_HA": A[z].sum(),
                     "TC2000_GT30_HA": A[z & (tc > 30)].sum(),
                     "GROSS_LOSS_2001_2024_IN_TC30_HA": A[z & (tc > 30) & (ly >= 1) & (ly <= 24)].sum(),
                     "GROSS_LOSS_2020_2024_IN_TC30_HA": A[z & (tc > 30) & (ly >= 20) & (ly <= 24)].sum(),
                     "NOTE": "DSM includes canopy; >=50 m indicative of hills"})
    out = pd.DataFrame(rows)
    out["DEM_ITEMS"] = ";".join(i.id for i in items)
    out.to_csv(ROOT / "04_VALIDATION" / "PULAU_MAYA_TERRAIN_CHECK.csv", index=False)
    print(out.round(1).to_string())


if __name__ == "__main__":
    main(sys.argv[1])
