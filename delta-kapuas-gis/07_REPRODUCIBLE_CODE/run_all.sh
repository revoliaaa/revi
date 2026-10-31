#!/usr/bin/env bash
# Full pipeline. Prerequisites: pip install -r requirements.txt; ./download_public_data.sh;
# the Project Area shapefile at $DK_PA_SHP (not redistributed here).
set -euo pipefail
cd "$(dirname "$0")/src"
D="${DK_DATA_DIR:-$(cd .. && cd .. && pwd)/_data_cache}"
PA_SHP="${DK_PA_SHP:?set DK_PA_SHP to Delta_Kapuas_Project_Boundary_(Update).shp}"
R=../..
python s01_build_context_domain.py "$D/hdx/idn_admin_boundaries.gdb"
python s02_hansen_clip.py "$D/hansen"
python s06_project_area_qa.py "$PA_SHP" NAMA_DESA
python s03_zonal_stats.py $R/01_BOUNDARY_QA/CONTEXT_DOMAIN_25DESA_BPS2020.gpkg ADMIN_DESA_CONTEXT_BPS2020 "$D/gmw" $R/03_LAND_COVER_CHANGE/ZONAL_ADMIN_DESA_CONTEXT.csv
python s03_zonal_stats.py $R/01_BOUNDARY_QA/PROJECT_AREA_25HD_CLEAN.gpkg PROJECT_AREA "$D/gmw" $R/03_LAND_COVER_CHANGE/ZONAL_PROJECT_AREA.csv
python s03b_gmw_coastal_buffer.py $R/01_BOUNDARY_QA/CONTEXT_DOMAIN_25DESA_BPS2020.gpkg "$D/gmw" $R/04_VALIDATION/GMW_OUTSIDE_DESA_BUFFER.json
python s05_trends_benchmarks.py $R/03_LAND_COVER_CHANGE/ZONAL_ADMIN_DESA_CONTEXT.csv $R/03_LAND_COVER_CHANGE/TRENDS_ADMIN_DESA_CONTEXT
python s05_trends_benchmarks.py $R/03_LAND_COVER_CHANGE/ZONAL_PROJECT_AREA.csv $R/03_LAND_COVER_CHANGE/TRENDS_PROJECT_AREA
python s07_project_area_constraint.py $R/03_LAND_COVER_CHANGE/ZONAL_PROJECT_AREA.csv $R/03_LAND_COVER_CHANGE/ZONAL_ADMIN_DESA_CONTEXT.csv
python s04_landsat_epoch_composites.py $R/02_REMOTE_SENSING_DATA/landsat_pulau_maya      # ~15 min, network
python s09_pulau_maya_anomaly.py $R/02_REMOTE_SENSING_DATA/landsat_pulau_maya $R/01_BOUNDARY_QA/CONTEXT_DOMAIN_25DESA_BPS2020.gpkg "$D/gmw" $R/01_BOUNDARY_QA/PROJECT_AREA_25HD_CLEAN.gpkg
python s12_pulau_maya_terrain.py $R/01_BOUNDARY_QA/PROJECT_AREA_25HD_CLEAN.gpkg
python s13_hcv_tables.py
python s08_hcv_comparison.py ../inputs/HCV_LANDCOVER_TABLES_FROM_REPORTS.csv $R/03_LAND_COVER_CHANGE/ZONAL_ADMIN_DESA_CONTEXT.csv $R/04_VALIDATION/GMW_OUTSIDE_DESA_BUFFER.json $R/03_LAND_COVER_CHANGE/ZONAL_PROJECT_AREA.csv
python s14_hcv_vs_satellite.py
python s11_build_deliverables.py
python s10_figures.py "$D/gmw" $R/02_REMOTE_SENSING_DATA/landsat_pulau_maya
# Final package for Vensim REV3 integration
python s15_master_spatial.py "$D/gmw"
python s16_vensim_input.py
python s17_package.py
