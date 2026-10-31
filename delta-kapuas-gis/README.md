# Delta Kapuas 25-HD: geospatial reconstruction and validation for the System Dynamics model

**Bottom line.**
- Independent satellite data (Hansen GFC v1.13, GMW v3.0 and Landsat 8/9) give a consistent, Project-Area-specific record of gross tree-cover loss for 2001–2024.
- They show that the HCV land-cover series contains epoch-to-epoch classification artefacts, notably Kubu 2009/2014 and Pulau Maya 2014–2024, that are as large as the model errors being compared.
- They strengthen the *uncertainty assessment* and the *spatial consistency* of the model.
- They do **not** yet supply a replacement for any Vensim parameter. Every candidate is "sensitivity only" until the SK geometry and a probability-sample accuracy assessment are available.

## Key results

| Question | Answer (evidence) |
|---|---|
| Project Area forest loss 2001–2024 | **11,724 ha** gross tree-cover loss = 10.6 % of the 110,809 ha tree cover of 2000 (canopy > 30 %; 11,695–11,730 ha across 10/30/50 %). Padang Tikar 7,786; Pulau Maya 2,258; Kubu 1,679 ha. 51 % occurred in 2015–2016. Map-based; not deforestation sensu regulation. |
| PA vs surrounding landscape | The PA holds 26 % of the 2000 tree cover but only 10.4 % of the 2001–2024 loss in the 25 villages. Loss is concentrated outside the PA. |
| Reliable HCV epochs | Padang Tikar all epochs; Kubu 2000/2003/2019/2024; Pulau Maya 2000–2009 |
| Problematic HCV epochs | Kubu 2009, Kubu 2014, Pulau Maya 2014/2019/2024 (`04_VALIDATION/HCV_EPOCH_RELIABILITY.csv`) |
| Pulau Maya 2019→2024 (+3,773 ha mangrove, +581 ha dryland forest) | Not ecological change. Only 3–11 ha became newly vegetated in the PA. GMW mangrove has been stable at 6,309–6,335 ha since 1996. Forested hills existed throughout. Most consistent with re-classification (H2 + H4). |
| HCV noise vs model error | HCV departs from a monotone satellite-harmonised series by RMSE 4,200 ha in 2019/2024, about the size of the SD (5,445) and linear (4,991) hold-out RMSEs. The hold-out cannot discriminate the models. |
| 0.8535 parameter | With SK geometry: area share 0.8895, tree-cover share R1 = **0.903**, gross-loss activity share R2 = **0.682** (0.54–0.78 by period). Keep 0.8535 as baseline; run R2/R1 as S4 sensitivity. |

## Gate report

| Gate | Status | Evidence / limitation |
|---|---|---|
| 1 Input audit & boundary | **PASS** (PA and SK) | PA: 25 valid, non-overlapping polygons; UTM sum within 0.04 ha of PDD. SK: 38 pieces → 25 HD, assignment verified by SK number 37/37, 99.94 % of PA inside SK; SK geometry +0.41 % vs SK table (Ambawang +10.6 %). |
| 2 Public data acquisition | **PASS** | Hansen v1.13 (both tiles), GMW v3 (7 years), Landsat C2 L2 (68 scenes), Copernicus DEM, BPS boundaries. Not obtained: GFW peat (API key), KLHK land cover (unreachable), Dynamic World (no GEE credentials). |
| 3 Historical forest change | **PASS** (gross loss) / CONDITIONAL (forest-type maps) | Annual 2001–2025 loss per HD × 3 thresholds; six epochs. No multi-class maps: no reference data. |
| 4 Harmonisation & anomaly | **PASS** | HCV tables transcribed (columns close ±0.02 ha); T1/T1b/T2/T3 tests; Pulau Maya H1–H4 evaluated |
| 5 Project Area analysis | **PASS** | `03_LAND_COVER_CHANGE/FOREST_CHANGE_PROJECT_AREA.xlsx` |
| 6 Accuracy & uncertainty | **CONDITIONAL** | Sensitivity, break and episodic analyses done. **No accuracy assessment**: no probability reference sample exists, and none was invented. |
| 7 SD parameter recommendations | **CONDITIONAL** | Candidates and decisions in `05_SYSTEM_DYNAMICS_INPUT/`. `.mdl` not supplied, so current rate values are unknown. Model not modified. |
| 8 Publication package | **CONDITIONAL** | 7 figures, methods, limitations, captions. Needs the accuracy assessment and PDF verification of flagged HCV cells before submission. |

## Final deliverable for System Dynamics integration

**`DELTA_KAPUAS_25HD_GIS_FINAL_FOR_VENSIM.zip`** (also unpacked in `08_FINAL_FOR_VENSIM/`) contains:
- **Master spatial database:** `DKP_25HD_MASTER_SPATIAL` (GPKG primary + SHP) with the 25 original Project Area polygons and 33 attributes.
- Thematic layers: tree-cover status, loss year, GMW mangrove. Peat is **not** mapped; the reason is documented.
- **Vensim input table:** `DKP_VENSIM_SPATIAL_INPUT.csv/.xlsx`, 121 rows classified as observation / estimate / candidate / assumption and as direct / conversion / sensitivity / unusable.
- QA report and the REV3 integration README (Indonesian).

## Folder map

- `01_BOUNDARY_QA/`: PA audit, clean PA GeoPackage, desa context domain, `SPATIAL_DOMAIN_RECONCILIATION.md`
- `02_REMOTE_SENSING_DATA/`: Hansen AOI rasters (native grid), Landsat composites (Pulau Maya), metadata, `SATELLITE_DATASET_INVENTORY.xlsx`
- `03_LAND_COVER_CHANGE/`: per-HD and per-year loss (long format per the required schema), epochs, PA summaries
- `04_VALIDATION/`: HCV vs satellite tests, Pulau Maya investigation, uncertainty report
- `05_SYSTEM_DYNAMICS_INPUT/`: parameter candidates, calibration benchmarks, PA crediting constraint, recommendations
- `06_PUBLICATION/`: figures, methods / limitations / captions
- `08_FINAL_FOR_VENSIM/`: final master database, thematic layers, Vensim input, QA, REV3 README
- `07_REPRODUCIBLE_CODE/`: scripts, GEE replica (not executed), inputs, provenance, run instructions

Not produced, deliberately: `LAND_COVER_TRANSITION_MATRIX.xlsx` and any confusion matrix. Neither is supportable without reference data (see `04_VALIDATION/SPATIAL_ACCURACY_AND_UNCERTAINTY.md`).
