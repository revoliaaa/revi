# Pulau Maya HCV land-cover anomaly, 2019 → 2024

## The anomaly (HCV Pulau Maya, Tabel 15, PDF p. 52; study area 16,103 ha)

| Class | 2000 | 2003 | 2009 | 2014 | 2019 | 2024 |
|---|---|---|---|---|---|---|
| Hutan Mangrove Sekunder | 7,941.11 | 7,941.11 | 7,941.11 | 6,978.25 | **6,843.77** | **10,617.08** |
| Hutan Rawa Sekunder | 3,621.93 | 3,517.76 | 3,338.68 | 2,052.21 | 1,410.76 | 742.31 |
| Hutan Lahan Kering Sekunder | 0 | 0 | 0 | 0 | **0** | **580.63**\* |
| Semak Belukar Rawa | 3,422.48 | 3,526.65 | 3,705.72 | 5,718.34 | 6,714.59 | 3,531.19 |

\* The PDF text extraction lost the empty cells for this row. Its year was reconstructed from the column totals (16,103.00 ha every year; reconstruction unique to ±0.01 ha). Verify against the PDF.

The reported change is +3,773 ha mangrove in five years (+11 % per year) and +581 ha of dryland forest appearing from zero. The HCV report text describes Pulau Maya land cover as "stable" (p. 51).

## Independent evidence

| # | Evidence | Domain | Result |
|---|---|---|---|
| E1 | GMW v3 mangrove extent, 1996–2020 | Pulau Maya PA (15,308 ha) | 6,309–6,335 ha in all seven years (range 26 ha). No expansion trend. |
| E2 | Bound test T1b (assumption A1: PA ⊂ HCV area) | PA + the 795 ha of HCV area outside the PA | HCV 2019 = 6,844 ≤ bound 7,130: **consistent**. HCV 2024 = 10,617 > bound 7,117: **exceeds by 3,500 ha**. |
| E3 | Same bound without A1: GMW in the 5 desa + 1 km | 116,302 ha superset | GMW 2020 = 9,728 ha. HCV 2024 still exceeds even this superset by 889 ha. |
| E4 | Landsat 8/9 OLI median composites (Collection 2 L2, WRS-2 121/061; 18, 16 and 31 usable scenes in 2014, 2019 and 2024; median 7–12 clear observations per pixel) | PA | Densely vegetated (NDVI ≥ 0.6) area: 15,218 ha (2014), 15,255 ha (2019), 15,278 ha (2024), i.e. ≈ 100 % of the PA in every epoch. **Newly vegetated 2019→2024: 3–11 ha** (NDVI threshold 0.7–0.5). Water/mudflat (MNDWI > 0): 14–27 ha. |
| E5 | Same test | Desa + 1 km superset | Newly vegetated 2019→2024: 60–189 ha, of which 38–144 ha came from water or mudflat |
| E6 | Spectral stability of the GMW-2020 mangrove stratum | PA | Median NDVI 0.84 / 0.85 / 0.87; median NDMI 0.58 / 0.57 / 0.59 (2014 / 2019 / 2024) |
| E7 | Hansen gross loss in the PM PA, 2020–2024 | PA | 97 ha in 2020–2024. There is no disturbance that would explain a large class swap via clearing and regrowth. |
| E8 | Copernicus GLO-30 DSM + Hansen (`PULAU_MAYA_TERRAIN_CHECK.csv`) | PA | 347 ha has DSM ≥ 50 m (maximum 211 m), i.e. hills. Tree-covered in 2000: 346.6 ha (>30 % canopy). Gross loss 2001–2024: 15.8 ha (0.3 ha since 2020). |

## Evaluation of hypotheses

| Hypothesis | Assessment | Basis |
|---|---|---|
| **H1** Real ecological change (mangrove expansion, dryland forest recovery) | **Contradicted** for the reported magnitude | E4/E5: no land became vegetated at anything near 3,773 ha; the PA was already ≈ 100 % densely vegetated in 2019. E1: GMW shows no expansion trend to 2020. E8: the elevated terrain was continuously tree-covered, so dryland forest was not "new" in 2024. Natural mangrove colonisation of +3,773 ha requires new intertidal substrate, but only 14–27 ha of water/mudflat exists in the PA. |
| **H2** Different classification methods between epochs | **Supported** (most likely, jointly with H4) | The change is a relabelling of already-vegetated pixels: mangrove +3,773 ha coincides with *hutan rawa sekunder* −668 ha and *semak belukar rawa* −3,183 ha. Similar oscillations occur in Kubu (mangrove 9,137 → 12,771 → 7,122 → 10,317 ha in 2009–2024), where GMW is stable (range 75 ha). This points to a method artefact affecting the series generally, not a local event. |
| **H3** Image timing, tides, season | **Insufficient** to explain the magnitude | Tides can shift the seaward mangrove edge by tens to hundreds of ha, not thousands. In Landsat, wet-surface area in the PA is under 30 ha in every epoch. |
| **H4** Inconsistent definitions or mapping of forest classes | **Supported** | GMW's mangrove definition is stable through time. The HCV 2024 mangrove class is about 4,300 ha larger than GMW mangrove inside the PA. It probably includes back-mangrove, nipah or transitional swamp vegetation that the 2019 map assigned to *rawa* or *semak belukar rawa*. The *hutan lahan kering* class appears only in 2024, although E8 shows forested hills throughout. |

**Conclusion.** The independent observations show that the 2019→2024 HCV changes in Pulau Maya are **not ecological change**. Spectrally, the area did not change. The changes are most consistent with **class re-definition or re-mapping (H2 + H4)**.

The data cannot establish *which* HCV epoch is "right":
- Under GMW's definition, HCV 2019 (6,844 ha) is consistent and HCV 2024 is not.
- Under a broader mangrove definition, the reverse could hold.

What the data do establish is that the 2019 and 2024 HCV class areas **are not comparable** and must not be used as a change signal.

## Limits of this investigation

- NDVI/NDMI cannot separate mangrove from peat-swamp or shrub vegetation. The Landsat test detects changes in *vegetated vs non-vegetated* state, not changes between forest types. A relabelling between vegetated classes is therefore invisible to it, which is exactly why it rules out H1 but cannot adjudicate class definitions.
- GMW ends in 2020, and no independent mangrove map for 2024 was used. Sentinel-2 or a GMW v4 update would strengthen the 2024 side.
- The HCV area geometry is unavailable. E2 relies on assumption A1 (PA ⊂ HCV area); E3 avoids that assumption.
- No field reference data. No accuracy can be stated for any class.

## Consequence for the Vensim model

Do not use Pulau Maya 2019→2024 class changes (or Kubu 2009/2014 mangrove values) as observed regeneration or as validation targets. Either exclude the flagged epochs (`HCV_EPOCH_RELIABILITY.csv`) or use the satellite-harmonised series (`HCV_HARMONISED_SERIES.csv`) as a sensitivity target.
