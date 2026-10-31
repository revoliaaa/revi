# Spatial domain reconciliation: 25 HD, Delta Kapuas

**Status:** GATE 1 PASS for the Project Area geometry **and** for the SK geometry. The SK file is *SHP Gabungan Hutan Desa Delta Kapuas* (supplied 31-10-2026; see `SK_25HD_BOUNDARY_AUDIT.xlsx`): HD assignment agrees with the SK numbers in the .dbf for 37/37 pieces, and 99.94 % of the PA lies inside the SK.

## 1. Domains used in this study

| Domain | Area (ha) | Source | Geometry | Role |
|---|---|---|---|---|
| **HCV / SK study area** | 124,941 by table (Kubu 32,468; Padang Tikar 76,370; Pulau Maya 16,103); 125,456 UTM / 125,470 geodesic by geometry | Tabel 1 of the HCV reports; geometry from *SHP Gabungan Hutan Desa Delta Kapuas* | **Available** (`SK_25HD_BOUNDARY.gpkg`) | Vensim land-system domain; HCV land-cover tables |
| **Carbon Project Area (PA)** | 111,123.16 (UTM 49S planar) / **111,134.95 (geodesic WGS84)** | `Delta_Kapuas_Project_Boundary_(Update).shp`, processing date 21-05-2026 | Available: 25 polygons, 1 per LPHD | All per-HD satellite statistics |
| **Admin-desa context** | 441,002 (geodesic) | BPS desa polygons (HDX COD-AB IDN v01, 2020-04-01) whose names match the 25 HD | Available | Landscape context only. **Not** HD and **not** PA |

The PA and the HCV area must not be treated as the same domain. The 0.8535 Vensim parameter links the two; see §4.

## 2. Project Area boundary audit (`PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx`)

| Check | Result |
|---|---|
| Features / HD | 25 polygons, exactly one per HD, no HD missing |
| CRS | EPSG:4326 (.prj). The `.shp.xml` history shows two `DefineProjection` steps (UTM 49S, then GCS WGS84). Coordinates were verified to be geographic degrees in the correct location (bounds 109.15–109.87°E, 1.31°S–0.003°N). |
| Validity / empties / duplicates | 0 invalid, 0 empty, 0 duplicate geometries, 0 HD with more than one feature |
| Overlaps | 0 pairwise overlaps > 0.01 ha; union area = sum of areas |
| Area vs PDD | UTM 49S planar sum **111,123.16 ha**; PDD 111,123.20 ha (−0.04 ha); previous check 111,123.17 ha (−0.01 ha). The `Luasan` attribute equals the UTM 49S planar area for every polygon. |
| Geodesic area | **111,134.95 ha**, +11.79 ha versus planar. This is UTM scale distortion: the PA lies about 1.5° west of the 111°E central meridian. All zonal statistics use geodesic pixel areas. |
| Name matching | 24 exact; `Padang Tikar` → HD12 *Padang Tikar 1* by documented alias (only one Padang Tikar HD exists, and the polygon lies 100 % inside BPS desa Padang Tikar I) |
| Raster/vector area conservation | Pixel-centre rasterisation reproduces each polygon's geodesic area to within 0.27 % (ratio 0.9973–1.0013) |

### Per-HD Project Area vs SK area (`04_VALIDATION/PER_HD_PROJECT_AREA_VS_SK.csv`)

PA/SK = 0.889 overall (Kubu 0.909, Padang Tikar 0.868, Pulau Maya 0.950). Most HD keep 0.85–1.00 of their SK area. The large exclusions are:

| HD | SK (ha) | PA (ha, UTM) | PA/SK |
|---|---|---|---|
| HD12 Padang Tikar 1 | 190 | 48.75 | **0.26** |
| HD19 Teluk Nibung | 2,900 | 928.86 | **0.32** |
| HD10 Teluk Bakung | 5,565 | 3,778.64 | 0.68 |
| HD18 Nipah Panjang | 6,940 | 5,438.53 | 0.78 |
| HD16 Ambarawa | 4,775 | 3,936.31 | 0.82 |

HCV Tabel 16 (Padang Tikar) shows 2024 plantation (*perkebunan*) and settlement classes concentrated in Teluk Nibung (806 + 77 ha) and Nipah Panjang (341 + 52 ha). That is *consistent with* the hypothesis that the PA excluded non-forest land. It cannot be confirmed without SK geometry.

**Legal-status note:** the SK for HD23 Kemboja is dated **10-06-2024** (KEPMENLHK 8492/2024), while the other 24 SK date from 2017–2020. The HCV tables still report Kemboja land cover for 2000–2019. That is legitimate for land cover, but matters for any REDD baseline or crediting-period reasoning that depends on management rights.

## 3. Name–location inconsistency between the PA and BPS desa polygons

Nine PA polygons do not lie mainly in the BPS desa of the same name (`NAME_LOCATION_VS_BPS_DESA` sheet). Examples:
- Sungai Besar PA: 75 % in Tasik Malaya desa.
- Sungai Jawi PA: 69 % in Sungai Besar desa.
- Mengkalang PA: 92 % outside all 25 matched desa.
- Seruat Dua PA: 99.9 % outside all 25 matched desa.

Overall, 6,709 ha (6.0 %) of the PA lies outside the 25 desa. Hutan Desa are designated in state forest and need not coincide with administrative villages. **Per-HD comparisons between PA and desa are therefore invalid.** The desa domain is used only at landscape level.

## 4. Why 124,941 ha ≠ 111,123 ha, and what it means for `Proporsi Kredit REDD dalam Project Area = 0.8535`

- The area ratio is now measured from geometry and SK tables: **R0 = 0.8895** (geodesic PA / SK total). It is landscape-specific: 0.909, 0.868 and 0.950.
- 0.8535 is not reproduced by any ratio computed here. Its derivation is not documented in the material supplied.
- The ratio that matters for crediting is the PA's share of *baseline activity* (deforestation) within the HD. That requires the SK geometry, which was not available, so it is **NOT AVAILABLE**.
- Context evidence warns against assuming activity share = area share. In the desa context domain, the PA holds 26 % of the 2000 tree cover but only **10.4 %** of the 2001–2024 gross loss. Loss is concentrated outside the PA.

**Update with SK geometry (s18/s19):**
- R1 (2000 tree-cover share PA/SK) = **0.903**.
- R2 (2001–2024 gross-loss activity share PA/SK) = **0.682**. It is threshold-robust (0.680–0.686) but period-dependent: 0.541 for 2001–2014, 0.782 for 2015–2024 and 0.604 for 2017–2024. By landscape: Kubu 0.543, Padang Tikar 0.673, Pulau Maya 0.893.
- 0.8535 lies between R2 and R1. The areas excluded from the PA hold about 10 % of the SK tree cover but 32 % of its 2001–2024 gross loss.

**Recommendation:** keep 0.8535 as the baseline. Run 0.682 (R2) and 0.903 (R1) as S4 sensitivity cases. Adopt R2 only if the model equation defines the parameter as a share of deforestation activity.
