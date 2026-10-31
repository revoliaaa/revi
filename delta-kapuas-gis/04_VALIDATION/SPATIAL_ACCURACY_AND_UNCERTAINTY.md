# Spatial accuracy and uncertainty

## What was *not* done, and why

- **No confusion matrix, overall/user's/producer's accuracy, or area-adjusted estimate is reported.** No independent reference sample (field plots or a probability sample of interpreted high-resolution imagery) was available. Reporting accuracies without one would be fabrication. All areas are **map-based pixel counts**, and UMD explicitly cautions against definitive area estimation from GFC pixel counts.
- **No supervised land-cover classification and no transition matrix** were produced. The six HCV epochs cannot serve as training data: this study shows they are internally inconsistent. Landsat spectra alone cannot separate mangrove, peat-swamp forest and swamp shrub without reference data (Stage 3 feasibility = **not feasible with current references**).
- **Peat stratum not analysed:** the GFW peatland raster requires an API key (HTTP 403). Forest loss does not quantify peat emissions in any case.

To move from map-based to design-based estimates, follow Olofsson et al. (2014). Draw a stratified random sample (strata: stable tree cover, loss 2001–2010, loss 2011–2024, non-tree), with about 50–100 points per stratum inside the PA. Interpret it against the Landsat archive and VHR imagery, then compute area-adjusted loss with 95 % CIs. `07_REPRODUCIBLE_CODE` contains the strata rasters needed (Hansen layers on the native grid).

## Uncertainty sources and their treatment

| Source | Magnitude / evidence in this study | Treatment |
|---|---|---|
| **Forest definition (canopy threshold)** | PA gross loss 2001–2024: 11,730 / 11,724 / 11,695 ha at >10/30/50 %, a range of 0.3 %. TC2000: 110,899 / 110,809 / 110,616 ha. | Reported for all three thresholds; >30 % used in text. Threshold is **not** a dominant uncertainty here, because the PA was almost fully closed-canopy in 2000. |
| **Tree cover ≠ forest; loss ≠ deforestation** | Hansen counts any >5 m vegetation, including swamp shrub regrowth and tree crops. HCV classes 74–76 % of the HCV area as natural forest in 2024, whereas Hansen implies about 89 % tree cover remaining in the PA. | Hansen is used as *gross loss activity*, never as forest area or as deforestation under Indonesian regulation. |
| **Hansen method break (2011)** | UMD reprocessed loss from 2011 onward, not 2001–2010. PA mean 2001–2010 = 170 ha/yr vs 2011–2014 = 537 ha/yr. Part of this jump may be an artefact. | Flag on every annual record; benchmark B4 uses only 2011–2014. |
| **Episodic disturbance** | 2015–2016 = 5,952 ha (51 % of all PA loss 2001–2024); Padang Tikar 2015 = 2,423 ha, 2016 = 2,334 ha | Rates are reported by interval; constant-rate assumptions are flagged. |
| **Spatial resolution / mixed pixels** | 0.00025° (≈ 27.8 m) Hansen; 0.000222° GMW; small HD (Padang Tikar 1, 48.75 ha ≈ 630 Hansen pixels of ≈ 0.077 ha) | Per-HD values for HD12 are flagged as low-precision by size. |
| **Rasterisation / boundary** | Raster footprint / geodesic polygon area = 0.9973–1.0013 | Negligible. |
| **Cross-product misregistration** | GMW resampled (nearest) to the Hansen grid for loss-in-mangrove; not quantified | Loss-in-mangrove marked `CROSS_PRODUCT_OVERLAY`. |
| **Cloud / cloud shadow** | Landsat PM window: median 7–12 clear observations per pixel; < 0.5 % of PA pixels with < 3 observations (2019 worst) | QA_PIXEL bits 0–4 masked; observation-count band written to every composite. |
| **Tides** | Wet surface (MNDWI > 0) in PM PA: 14–27 ha per epoch | Median compositing; tides cannot explain thousand-ha class changes. |
| **Acquisition dates / season** | Calendar-year composites, all months represented; single WRS-2 path/row 121/061 | Same sensor family (OLI/OLI-2) for 2014/2019/2024; Landsat 7 excluded. |
| **Boundary uncertainty (HCV/SK)** | SK geometry unavailable; PA ⊂ HCV assumed (A1) in T1b and in area-scaling | Every A1-dependent result is labelled; T1 (desa + 1 km) gives an assumption-free bound. |
| **HCV transcription** | Columns close to ±0.02 ha after two documented repairs: Pulau Maya empty cells reconstructed from totals; Padang Tikar 2024 *Pemukiman* row (173.5 ha) missing from Tabel 15, recovered from Tabel 16 | Quality flag per cell; `VERIFIED = NO` until checked against the PDFs. |
| **Admin context domain** | BPS desa clip intertidal mangrove (Kubu ≈ 1,250 ha, Padang Tikar ≈ 3,060 ha GMW within 1 km outside desa); 9 PA polygons mismatched by name | Desa domain used only for landscape context. |

## HCV epoch reliability (from `HCV_EPOCH_RELIABILITY.csv`)

The rule flags an epoch if the HCV natural-forest total departs by more than 10 % from a monotone, satellite-harmonised trajectory, or if the HCV mangrove area exceeds the GMW-based bound.

| Landscape | 2003 | 2009 | 2014 | 2019 | 2024 |
|---|---|---|---|---|---|
| Kubu | usable | **problematic** (−23 %) | **problematic** (mangrove +3,675 ha over GMW) | usable (−4 %) | usable (+1 %) |
| Padang Tikar | usable | usable | usable | usable | usable (+3.5 %) |
| Pulau Maya | problematic\* | problematic\* | **problematic** (−14 %) | **problematic** (−13 %) | **problematic** (+23 %; mangrove +4,295 ha over GMW) |

\* Flagged only by the mangrove bound (HCV 7,941 ha vs GMW-PA bound 7,104–7,109 ha). This holds under assumption A1 and if GMW is not missing back-mangrove. Treat as "caution" rather than "problematic".

The HCV departure from the harmonised series has RMSE 3,644 ha over 2003–2024 for all 25 HD, and **4,200 ha in the 2019/2024 hold-out years**. That is comparable to the previous SD (5,445 ha) and linear (4,991 ha) hold-out RMSEs. Consequence: the HCV hold-out cannot discriminate between those models.
