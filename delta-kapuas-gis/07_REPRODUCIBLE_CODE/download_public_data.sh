#!/usr/bin/env bash
# Download the public inputs into $DK_DATA_DIR (default: ../_data_cache). ~1.3 GB.
# Landsat and Copernicus DEM are streamed from Microsoft Planetary Computer by s04/s12 (no download).
set -euo pipefail
D="${DK_DATA_DIR:-$(cd "$(dirname "$0")/.." && pwd)/_data_cache}"
mkdir -p "$D/hansen" "$D/gmw" "$D/hdx"
H=https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13
for t in 00N_100E 10N_100E; do for l in treecover2000 lossyear gain datamask; do
  curl -fsSL -o "$D/hansen/Hansen_GFC-2025-v1.13_${l}_${t}.tif" "$H/Hansen_GFC-2025-v1.13_${l}_${t}.tif"; done; done
for y in 1996 2007 2010 2015 2016 2019 2020; do
  curl -fsSL -o "$D/gmw/gmw_v3_${y}_gtiff.zip" "https://zenodo.org/records/6894273/files/gmw_v3_${y}_gtiff.zip?download=1"
  (cd "$D/gmw" && unzip -o -q "gmw_v3_${y}_gtiff.zip" "*GMW_N00E109_*" "*GMW_N01E109_*" "*GMW_S01E109_*" "*GMW_S01E108_*" || true)
done
curl -fsSL -o "$D/hdx/idn_admin_boundaries.gdb.zip" \
  "https://data.humdata.org/dataset/84a1d98a-790b-4d66-9d14-bbfa48500802/resource/c740a308-0a63-46d6-ab15-b041e62eff58/download/idn_admin_boundaries.gdb.zip"
(cd "$D/hdx" && unzip -o -q idn_admin_boundaries.gdb.zip)
# Optional (needs a free GFW API key in $GFW_API_KEY): peatland extent tile on the Hansen grid
if [ -n "${GFW_API_KEY:-}" ]; then
  curl -fsSL -H "x-api-key: $GFW_API_KEY" -o "$D/gfw_peatlands_00N_100E.tif" \
    "https://data-api.globalforestwatch.org/dataset/gfw_peatlands/v20230315/download/geotiff?grid=10/40000&tile_id=00N_100E&pixel_meaning=is"
fi
echo "Data in $D. Compare checksums with PROVENANCE.md."
