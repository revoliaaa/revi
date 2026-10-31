"""Shared constants and helpers for the Delta Kapuas 25-HD GIS workflow.

All area calculations use geodesic (WGS84 ellipsoid) pixel areas so that
results do not depend on a projected CRS. Nothing in this module fabricates
data: the HD list is the study design supplied by the researcher, and the
admin-desa match is a *name* match to a public BPS layer, not a boundary of the
Hutan Desa (HD) themselves.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from pyproj import Geod

ROOT = Path(__file__).resolve().parents[2]          # delta-kapuas-gis/
CODE = ROOT / "07_REPRODUCIBLE_CODE"
DATA_DIR = Path(os.environ.get("DK_DATA_DIR", ROOT / "_data_cache"))  # raw downloads (not in git)

HANSEN_VERSION = "GFC-2025-v1.13"
HANSEN_TILES = ["00N_100E", "10N_100E"]  # AOI straddles the equator
HANSEN_BASE = f"https://storage.googleapis.com/earthenginepartners-hansen/{HANSEN_VERSION}"
HANSEN_LAYERS = ["treecover2000", "lossyear", "gain", "datamask"]
CANOPY_THRESHOLDS = [10, 30, 50]          # sensitivity definitions, not interchangeable standards
LOSS_YEARS = list(range(2001, 2026))      # v1.13 lossyear 1..25 -> 2001..2025
MODEL_YEARS = list(range(2001, 2025))     # 2001-2024 used for comparison with the Vensim history
EPOCHS = [2000, 2003, 2009, 2014, 2019, 2024]
REPROCESSING_BREAK_YEAR = 2011            # UMD: loss 2011+ reprocessed, 2001-2010 not

GMW_VERSION = "GMW v3.0 (Zenodo 10.5281/zenodo.6894273)"
GMW_YEARS = [1996, 2007, 2010, 2015, 2016, 2019, 2020]

# Analysis window (deg) covering all 25 matched desa (bounds 109.169-109.973E, 1.310S-0.092N) plus margin.
AOI_BBOX = (109.10, -1.35, 110.00, 0.12)   # (minx, miny, maxx, maxy); spans Hansen tiles 00N_100E and 10N_100E

# ---------------------------------------------------------------------------
# Study design: 25 HD, landscape and regency as stated by the researcher.
# ADMIN_DESA = name of the matching BPS desa polygon (HDX COD-AB IDN v01, 2020-04-01).
# MATCH = EXACT | SPELLING_VARIANT. Kecamatan from the BPS layer.
# ---------------------------------------------------------------------------
HD_TABLE = [
    # HD_ID, HD_NAME, LANDSCAPE, REGENCY, ADMIN_DESA, ADMIN_PCODE, KECAMATAN, MATCH
    ("HD01", "Kubu", "Kubu", "Kubu Raya", "Kubu", "ID6112030002", "Kubu", "EXACT"),
    ("HD02", "Dabong", "Kubu", "Kubu Raya", "Dabung", None, "Kubu", "SPELLING_VARIANT"),
    ("HD03", "Sungai Bemban", "Kubu", "Kubu Raya", "Sei Bemban", None, "Kubu", "SPELLING_VARIANT"),
    ("HD04", "Ambawang", "Kubu", "Kubu Raya", "Ambawang", "ID6112030014", "Kubu", "EXACT"),
    ("HD05", "Kampung Baru", "Kubu", "Kubu Raya", "Kampung Baru", "ID6112030008", "Kubu", "EXACT"),
    ("HD06", "Mengkalang", "Kubu", "Kubu Raya", "Mengkalang", "ID6112030019", "Kubu", "EXACT"),
    ("HD07", "Seruat Dua", "Kubu", "Kubu Raya", "Seruat II", None, "Kubu", "SPELLING_VARIANT"),
    ("HD08", "Betuah", "Kubu", "Kubu Raya", "Betuah", "ID6112020009", "Terentang", "EXACT"),
    ("HD09", "Tanjung Beringin", "Kubu", "Kubu Raya", "Tanjung Beringin", "ID6112010014", "Batu Ampar", "EXACT"),
    ("HD10", "Teluk Bakung", "Kubu", "Kubu Raya", "Teluk Bakung", "ID6112080013", "Sungai Ambawang", "EXACT"),
    ("HD11", "Medan Mas", "Padang Tikar", "Kubu Raya", "Medan Mas", "ID6112010015", "Batu Ampar", "EXACT"),
    ("HD12", "Padang Tikar 1", "Padang Tikar", "Kubu Raya", "Padang Tikar I", "ID6112010006", "Batu Ampar", "SPELLING_VARIANT"),
    ("HD13", "Tasik Malaya", "Padang Tikar", "Kubu Raya", "Tasik Malaya", "ID6112010005", "Batu Ampar", "EXACT"),
    ("HD14", "Sungai Besar", "Padang Tikar", "Kubu Raya", "Sungai Besar", "ID6112010004", "Batu Ampar", "EXACT"),
    ("HD15", "Sungai Jawi", "Padang Tikar", "Kubu Raya", "Sungai Jawi", "ID6112010003", "Batu Ampar", "EXACT"),
    ("HD16", "Ambarawa", "Padang Tikar", "Kubu Raya", "Ambarawa", "ID6112010002", "Batu Ampar", "EXACT"),
    ("HD17", "Tanjung Harapan", "Padang Tikar", "Kubu Raya", "Tanjung Harapan", "ID6112010001", "Batu Ampar", "EXACT"),
    ("HD18", "Nipah Panjang", "Padang Tikar", "Kubu Raya", "Nipah Panjang", "ID6112010008", "Batu Ampar", "EXACT"),
    ("HD19", "Teluk Nibung", "Padang Tikar", "Kubu Raya", "Teluk Nibung", "ID6112010009", "Batu Ampar", "EXACT"),
    ("HD20", "Batu Ampar", "Padang Tikar", "Kubu Raya", "Batu Ampar", "ID6112010010", "Batu Ampar", "EXACT"),
    ("HD21", "Dusun Besar", "Pulau Maya", "Kayong Utara", "Dusun Besar", "ID6111010002", "Pulau Maya", "EXACT"),
    ("HD22", "Dusun Kecil", "Pulau Maya", "Kayong Utara", "Dusun Kecil", "ID6111010004", "Pulau Maya", "EXACT"),
    ("HD23", "Kemboja", "Pulau Maya", "Kayong Utara", "Kemboja", "ID6111010005", "Pulau Maya", "EXACT"),
    ("HD24", "Tanjung Satai", "Pulau Maya", "Kayong Utara", "Tanjung Satai", "ID6111010003", "Pulau Maya", "EXACT"),
    ("HD25", "Satai Lestari", "Pulau Maya", "Kayong Utara", "Satai Lestari", "ID6111010006", "Pulau Maya", "EXACT"),
]
HD_COLS = ["HD_ID", "HD_NAME", "LANDSCAPE", "REGENCY", "ADMIN_DESA", "ADMIN_PCODE", "KECAMATAN", "MATCH"]

# Areas stated by the researcher / PDD (tabular; NOT geometry).
HCV_AREA_HA = {"Kubu": 32468, "Padang Tikar": 76370, "Pulau Maya": 16103, "TOTAL": 124941}
PDD_PROJECT_AREA_HA = 111123.20
PRIOR_SHP_PROJECT_AREA_HA = 111123.17
VENSIM_PROP_KREDIT_REDD = 0.8535

_GEOD = Geod(ellps="WGS84")


def row_pixel_area_ha(transform, height: int) -> np.ndarray:
    """Geodesic area (ha) of one pixel for each row of a north-up EPSG:4326 grid.

    Cells are treated as lat/lon quadrilaterals on the WGS84 ellipsoid; for
    0.00025 deg cells the difference between geodesic and rhumb edges is
    negligible (<1e-9 relative).
    """
    dx = transform.a
    dy = -transform.e
    x0 = transform.c
    y_top = transform.f - np.arange(height) * dy
    out = np.empty(height, dtype="float64")
    for i, yt in enumerate(y_top):
        yb = yt - dy
        area, _ = _GEOD.polygon_area_perimeter([x0, x0 + dx, x0 + dx, x0], [yb, yb, yt, yt])
        out[i] = abs(area) / 1e4
    return out


def ensure_dirs():
    for d in ["01_BOUNDARY_QA", "02_REMOTE_SENSING_DATA", "03_LAND_COVER_CHANGE", "04_VALIDATION",
              "05_SYSTEM_DYNAMICS_INPUT", "06_PUBLICATION/figures"]:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
