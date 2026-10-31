# Recommended updates to Vensim V5.4.2R (25 HD)

**The model was not modified.** The `.mdl` file was not available in this session, so CURRENT values of rate parameters show as "NOT SUPPLIED" in `VENSIM_SPATIAL_PARAMETER_CANDIDATES.xlsx`. Map each candidate to its model variable before use. All previous results (SD RMSE ≈ 5,445 ha; linear benchmark ≈ 4,991 ha) are retained as benchmarks.

## Answers to the research questions

**1. Which historical HCV observations are reliable enough for calibration?**
- Padang Tikar: all six epochs are consistent with satellite-observed gross loss (departure ≤ 3.5 %).
- Kubu: 2000, 2003, 2019 and 2024 are usable.
- Pulau Maya: 2000–2009 natural-forest totals are usable.

**2. Which years contain classification problems?**
- **Kubu 2009** (natural forest −5,091 ha, then +5,851 ha by 2014, with only 283 ha and 391 ha of Hansen gross loss in the PA over those two intervals).
- **Kubu 2014** (mangrove 12,771 ha vs GMW ≈ 9,096 ha in the PA).
- **Pulau Maya 2014, 2019, 2024** (2024: mangrove +3,773 ha and dryland forest +581 ha with no spectral change).
- Every landscape shows a net natural-forest **gain** in 2019→2024 (+7,273 ha in total). The satellite evidence offers no corresponding regrowth signal.

**3. How much spatially observed forest loss occurred within the Project Area?**
**11,724 ha gross tree-cover loss in 2001–2024** (canopy >30 %; 11,695–11,730 ha across thresholds), i.e. 10.6 % of the 110,809 ha tree-covered in 2000. Of this:
- 3,852 ha in 2001–2014.
- 7,872 ha in 2015–2024, of which 5,952 ha fell in 2015–2016.

By landscape: Padang Tikar 7,786 ha, Pulau Maya 2,258 ha, Kubu 1,679 ha. Loss inside GMW-2010 mangrove: 915 ha. These are map-based estimates without sample-based accuracy, and gross tree-cover loss is not "deforestation" in the regulatory or VM-methodology sense.

**4. Can the spatial eligibility approximation (0.8535) be improved?**
Partly.
- The **area** share is now measured: 0.8895, or per landscape 0.909 / 0.868 / 0.950, with per-HD values from 0.26 to 1.00.
- The **activity** share, which is what crediting needs, still requires SK geometry.
- Desa-context evidence shows loss is concentrated outside the PA, so the activity share could be much lower than the area share.

→ Keep 0.8535; run 0.8895 and the per-landscape values as sensitivity cases.

**5. Which deforestation parameters can be supported by independent geospatial evidence?**
Only as **sensitivity / benchmark** values (fraction of 2000 tree cover per year, PA, canopy >30 %):

| Period | Rate |
|---|---|
| 2001–2014 (calibration window) | 0.248 %/yr |
| 2015–2024 (held-out) | 0.710 %/yr (fire-dominated) |
| 2017–2024 (post-2016 background) | 0.217 %/yr |
| 2001–2024 | 0.441 %/yr |
| Landscapes (2001–2024) | Kubu 0.237, Padang Tikar 0.491, Pulau Maya 0.618 %/yr |

None qualifies for **REPLACE**, because each measures gross tree-cover loss in the PA rather than the model's forest-conversion rate in the 124,941 ha domain.

**6. Which uncertainties must remain explicit?** See `04_VALIDATION/SPATIAL_ACCURACY_AND_UNCERTAINTY.md`. The four that matter most:
- (i) HCV inter-epoch classification inconsistency, RMSE ≈ 3,600–4,200 ha.
- (ii) The Hansen 2011 method break.
- (iii) Episodic fire-year loss (2015).
- (iv) The unknown PA/SK activity share.

## Concrete actions (ordered)

1. **Re-state the validation result.** HCV-based hold-out errors below about 4,200 ha are not resolvable. The previous finding that "SD did not beat linear" is a *data-limited* result, not evidence against the model structure.
2. **Re-calibrate as a sensitivity run** with either (a) the flagged epochs excluded, or (b) the satellite-harmonised series `S2(t)` as target (`04_VALIDATION/HCV_HARMONISED_SERIES.csv`). Report both alongside the original calibration.
3. **Represent episodic disturbance** (fire years such as 2015) explicitly, e.g. a pulse or stochastic disturbance term. Calibrating a constant rate on 2001–2014 under-predicts PA loss in 2015–2024 by 9–66 % (benchmarks B1–B3). The same benchmarks *over*-predict loss by up to 300 % in the wider desa landscape.
4. **Do not use HCV class *gains*** (Pulau Maya mangrove 2024, Kubu mangrove 2014/2024, dryland forest 2024) as regeneration or ARR evidence.
5. **For the post-2017 period, treat the low background rate (0.217 %/yr) with care.** It overlaps the period after HD designation (SK 2017–2020) and could partly reflect an intervention effect. Using it as a without-project baseline would understate the counterfactual.
6. **Obtain the SK polygons** and run `s07_project_area_constraint.py` with an SK zonal file to compute R1/R2. That is the only way to replace 0.8535 with a measured activity share.
7. **Add a probability-sample accuracy assessment** inside the PA (Olofsson et al. 2014) before any rate is used in a journal-grade calibration.

## Relevance to carbon activities

| Activity | What the GIS outputs support | What they do **not** support |
|---|---|---|
| REDD (AUD) | PA-specific gross loss history, threshold sensitivity, episodic structure, PA/SK area shares | Verified activity data, baseline deforestation rates, credit volumes |
| ARR | Only very small historical non-tree areas exist in the PA (TC2000 > 30 % covers 99.7 %); Hansen gain 2000–2012 = 332 ha | Natural spectral recovery is not eligible ARR; no planting evidence was assessed |
| WRC peatland | Nothing quantitative. Peat map not acquired; forest loss ≠ peat oxidation emissions. | Any peat emission estimate |
| WRC mangrove | GMW mangrove in the PA: 45,050 ha (2020), stable since 1996 (45,151 ha); loss in mangrove 915 ha | Full wetland carbon accounting; soil carbon |
