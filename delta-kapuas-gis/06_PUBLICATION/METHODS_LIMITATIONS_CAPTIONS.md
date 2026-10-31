# Publication text: geospatial methods, limitations, figure captions

*Draft for the thesis and the journal manuscript. Numbers are taken from the workbooks in folders 01–05. Re-check them after any re-run.*

## 2.x Geospatial data and methods

**Spatial domains.** Three domains were distinguished and never interchanged.

1. *Carbon Project Area (PA).* The 25-polygon project boundary (one polygon per Hutan Desa; WGS84) was audited for CRS, validity, duplicates, overlaps and name correspondence. Its area is 111,123.16 ha in WGS84/UTM 49S, which agrees with the PDD value of 111,123.20 ha, and 111,134.95 ha on the WGS84 ellipsoid. Geodesic areas were used throughout.
2. *HCV/SK study area.* The 124,941 ha covered by the 25 Hutan Desa decrees (SK), known only from the SK tables of the HCV reports.
3. *Administrative context domain.* The BPS village polygons (OCHA/HDX COD-AB, 2020) bearing the same names. This was used only for landscape context, because nine PA polygons do not fall mainly within the same-named village.

**Tree-cover loss.** Annual gross tree-cover loss for 2001–2024 was derived from the Global Forest Change dataset v1.13 (Hansen et al., 2013; tiles 00N_100E and 10N_100E, native 0.00025° grid). Forest in 2000 was defined as canopy closure of vegetation taller than 5 m exceeding 10, 30 or 50 %. These were treated as sensitivity definitions, with 30 % reported in the text. Loss was attributed to a year where `lossyear` = year − 2000 within the year-2000 tree-cover mask. Each polygon was rasterised separately using the pixel-centre rule. Areas are sums of geodesic pixel areas computed per row on the WGS84 ellipsoid. Rasterised footprints reproduced polygon areas to within 0.27 %. Because the producers reprocessed loss detection from 2011 onward but not 2001–2010, every annual value carries a method-period flag, and trend tests were repeated on 2011–2014 only. Hansen loss is interpreted as gross, stand-replacing tree-cover loss. It is not deforestation as defined by Indonesian regulation or by the carbon methodology, and was not converted to emissions or credits.

**Mangrove extent.** Global Mangrove Watch v3.0 (Bunting et al., 2022) was summarised for 1996, 2007, 2010, 2015, 2016, 2019 and 2020 on its native 0.8″ grid. Loss within mangrove was computed by overlaying the GMW-2010 extent, resampled by nearest neighbour to the Hansen grid.

**Landsat consistency test.** For Pulau Maya, annual median composites were built for 2014, 2019 (Landsat 8 OLI) and 2024 (Landsat 8 OLI and Landsat 9 OLI-2). The source was Collection 2 Level-2 surface reflectance (WRS-2 path/row 121/061; scenes with < 80 % cloud cover; 18, 16 and 31 usable scenes). The QA_PIXEL fill, dilated-cloud, cirrus, cloud and cloud-shadow flags were masked, and reflectance was scaled as SR = DN·2.75×10⁻⁵ − 0.2. NDVI, NDMI and MNDWI were computed per scene and composited by the per-pixel median; the valid-observation count was retained. Landsat 7 was excluded to keep a single sensor family. Transitions from non-vegetated (NDVI < 0.4 or MNDWI > 0) to vegetated (NDVI ≥ 0.5/0.6/0.7) were tabulated for 2014→2019 and 2019→2024.

**HCV comparison.** The six-epoch land-cover tables of the three HCV reports were transcribed. Two transcription repairs were needed. Empty cells lost during PDF text extraction were reconstructed so that each column matched the reported total (Pulau Maya). One class row absent from the summary table was recovered from the per-HD table (Padang Tikar 2024 settlements, 173.5 ha). After repair, every column closed to within 0.02 ha. Natural forest was defined as the dryland, mangrove and swamp forest classes (primary and secondary).

Three tests were applied:
- (i) HCV mangrove area must not exceed GMW mangrove in the PA plus the HCV area outside the PA (assumption A1: PA ⊂ HCV area). An assumption-free variant used the administrative domain plus a 1 km coastal buffer.
- (ii) A net increase in HCV natural forest between epochs requires regrowth or reclassification; Hansen gain (2000–2012) and the Landsat test bound regrowth.
- (iii) HCV totals were compared with a satellite-harmonised, monotone reference S(t) = F_HCV(2000) − k·L_PA(t). Here L_PA is cumulative Hansen gross loss in the PA and k = A_HCV/A_PA. The RMSE of the departure F_HCV(t) − S(t) indicates between-epoch classification inconsistency.

**Benchmarks.** Following the System Dynamics calibration protocol (fit 2001–2014, hold out 2015–2024), four benchmarks were fitted to annual gross loss: constant mean, linear trend, constant proportional rate of remaining tree cover, and constant mean over 2011–2014. Each was evaluated by RMSE, MAE, bias and cumulative relative error.

**Reproducibility.** All processing was scripted in Python (GeoPandas 1.2, Rasterio 1.5/GDAL 3.12, pyproj 3.8). Public inputs are identified by version and SHA-256 checksum. An Earth Engine script reproduces the Hansen, GMW and Landsat steps for independent replication; it was not executed in this study.

## 3.x Results (key numbers)

- **PA tree cover in 2000:** 110,809 ha (99.7 % of the PA; canopy > 30 %).
- **Gross loss 2001–2024:** 11,724 ha (10.6 %).
  - Padang Tikar 7,786 ha; Pulau Maya 2,258 ha; Kubu 1,679 ha.
  - Threshold range 11,695–11,730 ha.
  - 2001–2014: 3,852 ha; 2015–2024: 7,872 ha; 2015–2016 alone: 5,952 ha.
  - Mean 2017–2024: 240 ha/yr.
- **Desa landscape context:** the PA contains 26 % of the year-2000 tree cover but only 10.4 % of the 2001–2024 gross loss (112,443 ha).
- **GMW mangrove in the PA:** 45,151 ha (1996) and 45,050 ha (2020).
- **HCV natural forest** (124,941 ha): 102,530 (2000), 101,577, 95,392, 96,744, 86,997 and 94,270 ha (2024). It includes net gains of +1,352 ha (2009–2014) and +7,273 ha (2019–2024). Departure RMSE from the harmonised reference: 3,644 ha (2003–2024) and 4,200 ha (2019/2024).
- **Pulau Maya:** newly vegetated area 2019→2024 in the PA was 3–11 ha, against a reported mangrove gain of 3,773 ha. GMW mangrove in the PA stayed at 6,309–6,335 ha over 1996–2020.

## Limitations

1. No probability-sample reference data: all areas are map-based, without accuracy or confidence intervals.
2. Hansen tree cover includes non-forest woody vegetation, and gross loss excludes regrowth and degradation. The 2001–2010 and 2011–2024 loss series were produced with different methods.
3. The SK (HD) geometry is unavailable. PA/HCV comparisons rely on area tables and on assumption A1. The crediting-relevant activity share cannot be computed.
4. GMW ends in 2020. No independent 2024 mangrove map was used, and mangrove vs peat-swamp separation was not attempted with Landsat.
5. The peat extent map was not acquired. Nothing here quantifies peat or WRC emissions.
6. HCV tables were transcribed from PDF text extraction. Repaired cells are flagged and must be checked against the original PDFs.
7. Satellite results are not carbon-credit eligibility determinations, and do not replace methodology-based MRV.

## Figure captions

**Figure 1.** Delta Kapuas study landscapes. Coloured polygons are the BPS village (desa) polygons matched by name to the 25 Hutan Desa (context domain; not HD or Project Area boundaries). Dark grey: mangrove extent, GMW v3.0, 2020. Numbers are HD identifiers.

**Figure 2.** Year of gross tree-cover loss 2001–2024 (Hansen GFC v1.13; canopy > 30 % in 2000) with village context polygons. Light grey: year-2000 tree cover without detected loss.

**Figure 3.** Annual gross tree-cover loss by landscape in the village context domain (canopy > 30 %). The shaded area marks the 2001–2014 calibration window; the dashed line marks the producers' 2011 reprocessing break.

**Figure 4.** Benchmarks fitted to 2001–2014 annual gross loss and evaluated on 2015–2024 (all 25 desa, canopy > 30 %). Grey bars: observed loss.

**Figure 5.** Pulau Maya mangrove area reported by the HCV assessment (squares) against GMW v3.0 mangrove extent in the five villages plus a 1 km coastal buffer, a superset of the HCV study area.

**Figure 6.** Pulau Maya Landsat OLI annual median NDVI in 2019 and 2024. Right: pixels inside the Project Area (black outline) that changed from non-vegetated to vegetated (NDVI ≥ 0.6) between 2019 and 2024, totalling 6.7 ha. Grey: GMW 2020 mangrove; thin grey lines: BPS villages.

**Figure 7.** HCV natural-forest totals (solid) against a monotone, satellite-harmonised reference (dashed): the HCV 2000 total minus area-scaled cumulative Hansen gross loss in the Project Area. The shaded area marks the 2019/2024 hold-out epochs.

## Data sources and citations

- Hansen, M.C. et al. (2013). High-resolution global maps of 21st-century forest cover change. *Science* 342, 850–853. Data: GFC-2025-v1.13, CC BY 4.0.
- Bunting, P. et al. (2022). Global Mangrove Extent Change 1996–2020: Global Mangrove Watch Version 3.0. *Remote Sensing* 14, 3657. Data: doi:10.5281/zenodo.6894273, CC BY 4.0.
- U.S. Geological Survey. Landsat Collection 2 Level-2 Science Products, accessed via Microsoft Planetary Computer (`landsat-c2-l2`).
- European Space Agency. Copernicus DEM GLO-30, accessed via Microsoft Planetary Computer (`cop-dem-glo-30`).
- BPS / OCHA ROAP. Indonesia subnational administrative boundaries (COD-AB), HDX, CC BY-IGO.
- Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57 (recommended next step).
- HCV assessment reports for the Kubu, Padang Tikar and Pulau Maya landscapes (Tabel 1, 14–16), as supplied by the researcher.
