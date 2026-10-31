# Data provenance

All inputs are listed with source, version, access date (2026-10-31) and SHA-256. Raw downloads are **not** committed (size/licence); `download_public_data.sh` retrieves them.

## Public datasets

| Dataset | Version / ID | Files | Licence |
|---|---|---|---|
| Hansen/UMD Global Forest Change | GFC-2025-v1.13 (GEE `UMD/hansen/global_forest_change_2025_v1_13`) | treecover2000, lossyear, gain, datamask × tiles 00N_100E, 10N_100E | CC BY 4.0 |
| Global Mangrove Watch | v3.0, Zenodo record 6894273 | `gmw_v3_{1996,2007,2010,2015,2016,2019,2020}_gtiff.zip` (tiles N00E109, N01E109, S01E108, S01E109 used) | CC BY 4.0 |
| Landsat Collection 2 Level-2 | Planetary Computer `landsat-c2-l2`, WRS-2 121/061; scene IDs in `02_REMOTE_SENSING_DATA/landsat_pulau_maya/LANDSAT_SCENE_LOG.json` | streamed (not stored) | USGS public domain |
| Copernicus DEM GLO-30 | Planetary Computer `cop-dem-glo-30`; items `Copernicus_DSM_COG_10_S01_00_E109_00_DEM`, `..._S02_00_E109_00_DEM` | streamed | Copernicus DEM licence |
| Indonesia admin boundaries (BPS/OCHA) | HDX `cod-ab-idn`, `idn_admin_boundaries.gdb.zip`, v01, valid 2020-04-01 | layer `idn_admin4` | CC BY-IGO |

### SHA-256
```
  cd1d1cf909233d4cad81a4736b21e5f6a2b74e10d0433eef2ab402ec5f8dff68  Hansen_GFC-2025-v1.13_datamask_00N_100E.tif
  fefd0cdfa029f1612536b6e2246185c73d832259488980e5fa5357ace994d4f6  Hansen_GFC-2025-v1.13_datamask_10N_100E.tif
  b175c18bde06aacaf61175c92bf72c6e102f6aa6c464e9264b9d431c6d877e06  Hansen_GFC-2025-v1.13_gain_00N_100E.tif
  42285c5afd3295202a8007efd5ef0bea8e2853194e0bd6c93a5562bd3b301715  Hansen_GFC-2025-v1.13_gain_10N_100E.tif
  4a676e1df62215ee7ec22f68d7ff610eac1ffcacbe091dcb398c49748759ca9c  Hansen_GFC-2025-v1.13_lossyear_00N_100E.tif
  cf448cb724c852c9e16542858d1fa52736612cd104b0060e1cd2724e9d23d420  Hansen_GFC-2025-v1.13_lossyear_10N_100E.tif
  513e7116a37ae3f8b51b11839625b17519730a8dd7b6df9347f4305cb5821d69  Hansen_GFC-2025-v1.13_treecover2000_00N_100E.tif
  48646e738bb4e20bc05a8acb46e2f97b1d372866ea765c94d4bc5e4a49eb733c  Hansen_GFC-2025-v1.13_treecover2000_10N_100E.tif
  00923d94d3861bb847faf0a91311d39d49242e824f63672e4dbec514df9e46c9  gmw_v3_1996_gtiff.zip
  f150c316f682de58cb58e7d32834472d889a0ff709b66a5b9a82b9bea8a05d9b  gmw_v3_2007_gtiff.zip
  5da7f9d1bfd28aa2002db36153ef7407abb4926fb96474eb3647b4df070f1e15  gmw_v3_2010_gtiff.zip
  7c8945377261c5ef37fd5a3e3a791d4c48ad0b10c7e81feabc605b569ae08166  gmw_v3_2015_gtiff.zip
  c02e04a88cbf83bc74ee7e99e42c7902b27183505d525d93c5170d2049ae5a7f  gmw_v3_2016_gtiff.zip
  5a6e31dcd808e5efd19eb85cbc97275b70a5861847d28cdc076030aae33df102  gmw_v3_2019_gtiff.zip
  97d783a0904fc97738d50bcb3b0a3e2ec0bfc87a2d5d09e349d59a330619f66b  gmw_v3_2020_gtiff.zip
  640c62398b19de310be321b83ccdd56c710cf796247028f453e172ff33a4e308  idn_admin_boundaries.gdb.zip
```

## Researcher-supplied inputs (not redistributed)

| Input | SHA-256 | Notes |
|---|---|---|
| `Delta_Kapuas_Project_Boundary_Update.rar` (shapefile `Delta_Kapuas_Project_Boundary_(Update)`, 25 features, metadata processing date 21-05-2026 / 23-09-2026) | `b825d0c926b4367b82e512f59d986254855c79e0ebae9bcdadcc92ff54de8768` | Cleaned copy: `01_BOUNDARY_QA/PROJECT_AREA_25HD_CLEAN.gpkg` |
| `HCV_Kubu.md` (text of `HCV Kubu Lanskap.pdf`) | `900ab41ded9c560065707cb64aa5599f93c14ccdcfb27dbc38b8c622711b5567` | Tabel 1, 14 |
| `HCV_Padang_Tikar.md` (text of `HCV Padang Tikar Lanskap.pdf`) | `1e622f584b670939809e18d292622656997e63361a20d4e03d2a379d4bd9e7a9` | Tabel 1, 15, 16 |
| `HCV_Pulau_Maya.md` (text of `FINAL_HCV Report_Pulau Maya_24022025.docx.pdf`) | `f89bb729496377c09d429ead5265bf013c65ebe769a9b30728bfd9174b819308` | Tabel 1, 15 |

Values transcribed from these reports live in `inputs/HCV_LANDCOVER_TABLES_FROM_REPORTS.csv` and `inputs/HCV_SK_AREAS.csv`, with page references and per-cell quality flags.

## Not obtained

- `BOUNDARY_AND_PULAU_MAYA_VERIFICATION.xlsx`: not present in the session; the boundary audit was redone from the shapefile.
- HD SK boundary geometry, Vensim `.mdl`, PDD: not supplied.
- GFW peatland extent: HTTP 403 without API key. KLHK land cover: geoportal unreachable. Dynamic World: no Earth Engine credentials.

## SK boundary input (supplied 31-10-2026)

```
841211ec8fd66d6c2ee37c212d3bce377d23e7bda1fdd4e1bac2ce93a601f34c  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.dbf
af362dfc5d1b69c1caff40c742195e0bfefdf3530bd3c7696552d9a5758a91dd  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.prj
2950f900d3d6f60a03023fdbe92f9585129c8a0fca162bb6f58d82a9d698765f  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.sbn
459dbbc60f513ec250ba9440cf315ac5d8820a1f25c0520a2596265f3722a34b  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.sbx
88090f0f3cc0c12c478affaebb72c734cbfd80c4ce4ad41b794a09fc2df120c8  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.shp
1433d777881413b22626352c9b3b115b775f4a5506d81eb61d94f8a420ae6b13  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.shp.xml
97d391479867f7aef2c341eee4c39a6b23b41c47c6565cb39a19c394a747d32a  SHP_Gabungan_Hutan_Desa_Delta_Kapuas.shx
b2475c8ff3e90fb27d9eae5f6ecc3479c802818299c2f49fc6a78a85e2cb5231  Laporan_Gambut_dan_Mangrove_Delta_Kapuas.md
```

## Peat / mangrove depth-class input (supplied 31-10-2026)

```
530a92e168d928745f22f0c510c55d492b8efe60c18e42690d87bef10f56353c  Gambut_Data_WAS.shp
975f52b0d151c79436a32f493f7c1ddb82d13e1be19a32baea7b4f244eae552f  Mangrove_Data_WAS.shp
65e889083e70110234233cc0f87c42a395929944ad032109f258e06c85b6766f  Soil_Depth_rev120425.shp
3745a85d9cba1fd8b231c45b2011b2bd9e0f596a981ccc475837cc66c3bcf80a  Gambut_Data_WAS.dbf
4e6eee24d355a58479c5691c46db470b17928da989574ac880cb02f65d932014  Mangrove_Data_WAS.dbf
de7848e2bde5962ed24d17b3969a573eaa8ec9a52463b2c61d5eedb0a82f7daf  Soil_Depth_rev120425.dbf
af362dfc5d1b69c1caff40c742195e0bfefdf3530bd3c7696552d9a5758a91dd  Gambut_Data_WAS.prj
af362dfc5d1b69c1caff40c742195e0bfefdf3530bd3c7696552d9a5758a91dd  Mangrove_Data_WAS.prj
af362dfc5d1b69c1caff40c742195e0bfefdf3530bd3c7696552d9a5758a91dd  Soil_Depth_rev120425.prj
7ca10031aea0acf35ec6de6372b3eafc3a4aa2e71d9408c3e0b78e18f869758d  Data_Kedalaman_Gambut_Mangrove_Mineral-20261031T164441Z-1-001.zip
```
