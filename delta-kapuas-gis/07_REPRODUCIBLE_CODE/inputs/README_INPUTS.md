# Inputs that must be supplied by the researcher

| File | Status in this session | Used by |
|---|---|---|
| Original 25-polygon Project Area shapefile (.shp/.shx/.dbf/.prj) | **NOT FOUND** in the container, repository (all 15 branches) or upload folders | `s06_project_area_qa.py` → `s03_zonal_stats.py` → `s07_project_area_constraint.py` |
| `BOUNDARY_AND_PULAU_MAYA_VERIFICATION.xlsx` | **NOT FOUND** | reference only (cannot replace geometry) |
| HD SK boundary geometry (25 HD) | not supplied; may not exist | `s07` ratios R1/R2 |
| HCV historical land-cover tables (all classes × 2000/2003/2009/2014/2019/2024 × 3 landscapes) | only the values quoted in the brief are pre-filled in `HCV_HISTORICAL_TABLE_TEMPLATE.csv` (VERIFIED = NO) | `s08_hcv_comparison.py` |
| Vensim model V5.4.2R (.mdl) + calibration series | not supplied | parameter mapping in `05_SYSTEM_DYNAMICS_INPUT` |

Fill the template with one row per landscape × year × HCV class, mark `IS_FOREST` (1/0) and
`FOREST_TYPE` (MANGROVE / PEAT_SWAMP / DRYLAND / OTHER_FOREST / NONFOREST), cite the table/page,
and set `VERIFIED=YES` only after checking against the report.
