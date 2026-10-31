"""Landsat Collection 2 Level-2 (OLI/OLI-2) epoch composites for a test window,
used to examine the Pulau Maya HCV 2019->2024 anomaly with an independent,
sensor-consistent observation (Landsat 8 for 2014/2019; Landsat 8+9 for 2024).

Data access: Microsoft Planetary Computer STAC (collection `landsat-c2-l2`),
anonymous SAS token. Landsat 7 is deliberately excluded (SLC-off stripes,
orbital drift) so that all three epochs come from the same OLI sensor family.

Processing per scene:
  * surface reflectance = DN * 0.0000275 - 0.2 (USGS C2 L2 scale/offset)
  * QA_PIXEL mask: drop fill(b0), dilated cloud(b1), cirrus(b2), cloud(b3),
    cloud shadow(b4); keep clear land and water
  * reflectance outside [0, 1] discarded
  * NDVI = (NIR-R)/(NIR+R); NDMI = (NIR-SWIR1)/(NIR+SWIR1); MNDWI = (G-SWIR1)/(G+SWIR1)
Composite: per-pixel median of valid observations within the calendar window;
pixel valid-observation count is written alongside. The grid is the native
Hansen 0.00025-deg grid (nearest-neighbour warp), so composites overlay Hansen
and GMW-derived masks without further resampling.

Usage: python -I s04_landsat_epoch_composites.py <out_dir> [minx miny maxx maxy]
"""
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import rasterio
from pystac_client import Client
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.vrt import WarpedVRT

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
TOKEN_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token/landsateuwest/landsat-c2"
EPOCHS = {  # calendar windows; +/- months added only if needed is NOT done automatically
    2014: ("2014-01-01", "2014-12-31", ["landsat-8"]),
    2019: ("2019-01-01", "2019-12-31", ["landsat-8"]),
    2024: ("2024-01-01", "2024-12-31", ["landsat-8", "landsat-9"]),
}
DEFAULT_BBOX = (109.20, -1.35, 109.82, -0.92)   # Pulau Maya window (5 desa + margin)
RES = 0.00025
BANDS = ["green", "red", "nir08", "swir16", "qa_pixel"]
MASK_BITS = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)
MAX_SCENE_CLOUD = 80


def token():
    with urllib.request.urlopen(TOKEN_URL, timeout=60) as r:
        return json.load(r)["token"]


def grid(bbox):
    x0 = np.floor(bbox[0] / RES) * RES
    y1 = np.ceil(bbox[3] / RES) * RES
    w = int(round((bbox[2] - x0) / RES))
    h = int(round((y1 - bbox[1]) / RES))
    return from_origin(x0, y1, RES, RES), h, w


def read_band(href, tr, h, w, resampling):
    with rasterio.open(href) as src, WarpedVRT(src, crs="EPSG:4326", transform=tr, height=h, width=w,
                                               resampling=resampling, nodata=0) as v:
        return v.read(1)


def composite(year, bbox, tok, out_dir):
    start, end, platforms = EPOCHS[year]
    tr, h, w = grid(bbox)
    cat = Client.open(STAC)
    items = list(cat.search(collections=["landsat-c2-l2"], bbox=bbox, datetime=f"{start}/{end}",
                            query={"platform": {"in": platforms}, "eo:cloud_cover": {"lt": MAX_SCENE_CLOUD}}).items())
    items.sort(key=lambda i: i.datetime)
    stacks = {k: [] for k in ["NDVI", "NDMI", "MNDWI"]}
    log = []
    for it in items:
        try:
            b = {k: read_band(it.assets[k].href + "?" + tok, tr, h, w, Resampling.nearest) for k in BANDS}
        except Exception as e:  # network/asset error: record, skip
            log.append({"id": it.id, "status": f"read_error: {e}"})
            continue
        qa = b["qa_pixel"]
        sr = {k: b[k].astype("float32") * 0.0000275 - 0.2 for k in ["green", "red", "nir08", "swir16"]}
        ok = (qa != 0) & ((qa & MASK_BITS) == 0)
        for v in sr.values():
            ok &= (v >= 0) & (v <= 1)
        nvalid = int(ok.sum())
        log.append({"id": it.id, "date": it.datetime.date().isoformat(), "platform": it.properties["platform"],
                    "wrs": f'{it.properties.get("landsat:wrs_path")}/{it.properties.get("landsat:wrs_row")}',
                    "scene_cloud_cover": it.properties.get("eo:cloud_cover"), "valid_px_in_window": nvalid})
        if nvalid == 0:
            continue
        with np.errstate(divide="ignore", invalid="ignore"):
            idx = {"NDVI": (sr["nir08"] - sr["red"]) / (sr["nir08"] + sr["red"]),
                   "NDMI": (sr["nir08"] - sr["swir16"]) / (sr["nir08"] + sr["swir16"]),
                   "MNDWI": (sr["green"] - sr["swir16"]) / (sr["green"] + sr["swir16"])}
        for k, a in idx.items():
            a = np.where(ok, np.clip(a, -1, 1), np.nan)
            stacks[k].append((a * 10000).astype("float32"))
        print(year, it.id, nvalid)
    prof = dict(driver="GTiff", height=h, width=w, count=4, dtype="int16", crs="EPSG:4326", transform=tr,
                nodata=-32768, compress="deflate", tiled=True, blockxsize=512, blockysize=512)
    out = Path(out_dir) / f"LANDSAT_OLI_MEDIAN_{year}_NDVI_NDMI_MNDWI_NOBS.tif"
    with rasterio.open(out, "w", **prof) as dst:
        nobs = None
        for bi, k in enumerate(["NDVI", "NDMI", "MNDWI"], start=1):
            st = np.stack(stacks[k])
            med = np.nanmedian(st, axis=0)
            nobs = np.isfinite(st).sum(axis=0)
            dst.write(np.where(np.isfinite(med), med, -32768).astype("int16"), bi)
            dst.set_band_description(bi, f"{k} x10000 (median)")
            del st
        dst.write(nobs.astype("int16"), 4)
        dst.set_band_description(4, "valid observation count")
        dst.update_tags(SOURCE="Planetary Computer landsat-c2-l2", WINDOW=f"{start}/{end}", PLATFORMS=",".join(platforms),
                        MASK="QA_PIXEL bits 0-4 removed", SCALE="SR=DN*0.0000275-0.2")
    return log


def main(out_dir, bbox=DEFAULT_BBOX):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    tok = token()
    logs = {}
    for y in EPOCHS:
        logs[y] = composite(y, bbox, tok, out_dir)
    (Path(out_dir) / "LANDSAT_SCENE_LOG.json").write_text(json.dumps({"bbox": bbox, "scenes": logs}, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], tuple(map(float, a[1:5])) if len(a) >= 5 else DEFAULT_BBOX)
