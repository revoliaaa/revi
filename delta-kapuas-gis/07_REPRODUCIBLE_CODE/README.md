# Reproducible code: Delta Kapuas 25-HD GIS workflow

## Environment

Python 3.13 with the pinned packages in `requirements.txt`. The Rasterio and pyogrio wheels bundle GDAL 3.12, so no system GDAL is needed.

```bash
pip install -r requirements.txt
```

## Run

```bash
./download_public_data.sh                       # ~1.3 GB into ../_data_cache (or $DK_DATA_DIR)
```

```bash
DK_PA_SHP="/path/Delta_Kapuas_Project_Boundary_(Update).shp" ./run_all.sh
```

Landsat (s04) and the Copernicus DEM (s12) are streamed from Microsoft Planetary Computer, which issues anonymous SAS tokens. The full run takes about 20 minutes, 15 of them for s04.

## Scripts (executed in this study unless marked)

| Script | Purpose | Main outputs |
|---|---|---|
| `src/common.py` | HD list, landscape/regency, constants, geodesic pixel area | – |
| `src/s01_build_context_domain.py` | BPS desa polygons matching the 25 HD names (context only) + QA | `01_BOUNDARY_QA/CONTEXT_DOMAIN_25DESA_*` |
| `src/s02_hansen_clip.py` | Mosaic and clip GFC v1.13 to the AOI on the native grid | `02_REMOTE_SENSING_DATA/*.tif` |
| `src/s06_project_area_qa.py` | Project Area audit: CRS, validity, areas, overlaps, names, desa overlay | `PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx`, `PROJECT_AREA_25HD_CLEAN.gpkg` |
| `src/s03_zonal_stats.py` | Per-polygon Hansen (3 thresholds, 2001–2025) and GMW statistics | `03_LAND_COVER_CHANGE/ZONAL_*.csv` |
| `src/s03b_gmw_coastal_buffer.py` | GMW mangrove just seaward of the desa polygons | `04_VALIDATION/GMW_OUTSIDE_DESA_BUFFER.*` |
| `src/s05_trends_benchmarks.py` | Epochs, annual rates, calibration/hold-out benchmarks | `TRENDS_*` |
| `src/s07_project_area_constraint.py` | Candidate ratios for the 0.8535 parameter | `PROJECT_AREA_CREDIT_SPATIAL_CONSTRAINT_COMPUTED.xlsx` |
| `src/s04_landsat_epoch_composites.py` | Landsat 8/9 OLI median NDVI/NDMI/MNDWI composites, 2014/2019/2024 | `landsat_pulau_maya/*.tif` |
| `src/s09_pulau_maya_anomaly.py` | Vegetation-transition and stability tests | `PULAU_MAYA_LANDSAT_TESTS.csv` |
| `src/s12_pulau_maya_terrain.py` | DSM ≥ 50 m terrain vs tree cover/loss | `PULAU_MAYA_TERRAIN_CHECK.csv` |
| `src/s13_hcv_tables.py` | HCV table transcription + column-total integrity check | `inputs/HCV_LANDCOVER_TABLES_FROM_REPORTS.csv` |
| `src/s08_hcv_comparison.py` | Mangrove bound tests T1/T1b/T2 | `HCV_VS_SATELLITE_TESTS.csv` |
| `src/s14_hcv_vs_satellite.py` | T3 interval test, harmonised series, epoch reliability, per-HD PA/SK | `HCV_*.csv`, `PER_HD_PROJECT_AREA_VS_SK.csv` |
| `src/s11_build_deliverables.py` | Assembles all deliverable workbooks from the CSVs | `*.xlsx` in 02–05 |
| `src/s10_figures.py` | Publication figures | `06_PUBLICATION/figures/*.png` |
| `gee/delta_kapuas_hansen_gmw_landsat.js` | **NOT EXECUTED.** Earth Engine replica for independent replication | – |

## Reproduction checklist

- [x] Re-run from a clean state reproduced all 24 output CSVs to numerical identity (2026-10-31, excluding s04, which is deterministic given the same scene list in `LANDSAT_SCENE_LOG.json`).
- [x] Raster/vector area conservation within 0.27 % for all 25 PA polygons.
- [x] HCV transcription: every landscape × epoch column closes to the reported total (±0.02 ha).
- [x] PA total matches the PDD (UTM 49S planar, −0.04 ha).
- [ ] Check flagged HCV cells (`QUALITY != TRANSCRIBED`) against the original PDFs.
- [ ] Run the GEE script and compare per-HD totals (tolerance 0.5 %).
- [ ] Add the SK geometry and re-run `s07` with an SK zonal file.
- [ ] Probability-sample accuracy assessment (Olofsson et al. 2014) before journal submission.
