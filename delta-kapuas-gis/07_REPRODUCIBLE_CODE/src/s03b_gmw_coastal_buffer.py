"""GMW mangrove lying OUTSIDE all 25 desa polygons but within 1/2/5 km of a
landscape's desa (captures intertidal mangrove clipped by admin coastlines).

Usage: python s03b_gmw_coastal_buffer.py <desa_context.gpkg> <gmw_dir> <out.json>
"""
import json
import sys

import geopandas as gpd
import numpy as np
from rasterio.features import rasterize

from common import GMW_YEARS, row_pixel_area_ha
from s03_zonal_stats import gmw_mosaic


def main(gpkg, gmw_dir, out_json):
    d = gpd.read_file(gpkg)
    allx = d.union_all()
    res, table = {}, []
    for y in GMW_YEARS:
        m, tr = gmw_mosaic(gmw_dir, y)
        pa = row_pixel_area_ha(tr, m.shape[0])[:, None]
        inall = rasterize([(allx, 1)], out_shape=m.shape, transform=tr, dtype="uint8") == 1
        for L, g in d.groupby("LANDSCAPE"):
            for km in (1, 2, 5):
                buf = gpd.GeoSeries([g.union_all()], crs=d.crs).to_crs(32749).buffer(km * 1000).to_crs(4326).iloc[0]
                inb = rasterize([(buf, 1)], out_shape=m.shape, transform=tr, dtype="uint8") == 1
                v = float((pa * (m & inb & ~inall)).sum())
                table.append({"LANDSCAPE": L, "GMW_YEAR": y, "BUFFER_KM": km, "GMW_OUTSIDE_DESA_HA": v})
                if km == 1:
                    res.setdefault(L, {})[str(y)] = v
    json.dump(res, open(out_json, "w"), indent=1)
    import pandas as pd
    t = pd.DataFrame(table)
    t.to_csv(out_json.replace(".json", ".csv"), index=False)
    print(t.pivot_table(index=["LANDSCAPE", "BUFFER_KM"], columns="GMW_YEAR", values="GMW_OUTSIDE_DESA_HA").round(0))


if __name__ == "__main__":
    main(*sys.argv[1:4])
