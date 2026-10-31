"""Mosaic + clip Hansen GFC v1.13 layers to the Delta Kapuas AOI (native grid, no resampling).

Inputs: the 8 GeoTIFFs for tiles 00N_100E and 10N_100E (download with
`download_public_data.sh`). Output: compressed GeoTIFFs in 02_REMOTE_SENSING_DATA
on the native 0.00025-deg Hansen grid, plus a metadata JSON.

Usage: python s02_hansen_clip.py <hansen_dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.merge import merge

from common import AOI_BBOX, HANSEN_BASE, HANSEN_TILES, HANSEN_VERSION, ROOT

OUT_NAMES = {
    "treecover2000": "FOREST_COVER_BASELINE_2000_canopy_pct.tif",
    "lossyear": "ANNUAL_TREE_COVER_LOSS_2001_2025_lossyear.tif",
    "gain": "HANSEN_GAIN_2000_2012.tif",
    "datamask": "HANSEN_DATAMASK.tif",
}


def main(hdir):
    hdir = Path(hdir)
    out = ROOT / "02_REMOTE_SENSING_DATA"
    meta = {"dataset": "Hansen/UMD/Google/USGS/NASA Global Forest Change", "version": HANSEN_VERSION,
            "tiles": HANSEN_TILES, "aoi_bbox_minx_miny_maxx_maxy": AOI_BBOX, "crs": "EPSG:4326",
            "resolution_deg": 0.00025, "license": "CC BY 4.0", "layers": {}}
    for layer, name in OUT_NAMES.items():
        srcs = [rasterio.open(hdir / f"Hansen_{HANSEN_VERSION}_{layer}_{t}.tif") for t in HANSEN_TILES]
        arr, tr = merge(srcs, bounds=AOI_BBOX, nodata=None)
        prof = srcs[0].profile
        prof.update(height=arr.shape[1], width=arr.shape[2], transform=tr, compress="deflate", predictor=2,
                    tiled=True, blockxsize=512, blockysize=512, nodata=None)
        with rasterio.open(out / name, "w", **prof) as dst:
            dst.write(arr)
            dst.update_tags(SOURCE=f"{HANSEN_BASE}/Hansen_{HANSEN_VERSION}_{layer}_<tile>.tif",
                            VERSION=HANSEN_VERSION, LICENSE="CC BY 4.0",
                            CITATION="Hansen et al. 2013, Science 342:850-853")
        vals, cnt = np.unique(arr, return_counts=True)
        meta["layers"][layer] = {"file": name, "shape": list(arr.shape[1:]), "transform": list(tr)[:6],
                                 "min": int(vals.min()), "max": int(vals.max()),
                                 "n_unique": int(len(vals))}
        print(layer, arr.shape, vals.min(), vals.max(), tr)
        for s in srcs:
            s.close()
    meta["notes"] = [
        "lossyear: 0 = no loss; k = stand-replacing loss detected in year 2000+k (k=1..25 -> 2001..2025).",
        "gain: 1 = gain detected during 2000-2012 only (no year of gain).",
        "datamask: 0 no data, 1 mapped land, 2 persistent water (2000-2012).",
        "UMD: loss from 2011 onward reprocessed with updated method; 2001-2010 not reprocessed -> possible structural break at 2011.",
        "UMD: definitive area estimation should not be made from pixel counts of loss layers.",
        "treecover2000 = canopy closure (%) of vegetation >5 m tall in 2000; forest threshold applied downstream (10/30/50%).",
    ]
    (out / "HANSEN_GFC_v1.13_AOI_metadata.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
