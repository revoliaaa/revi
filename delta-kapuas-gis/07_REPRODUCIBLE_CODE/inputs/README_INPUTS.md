# Inputs

| File / input | Status | Used by |
|---|---|---|
| `HCV_LANDCOVER_TABLES_FROM_REPORTS.csv` | Transcribed from HCV Kubu Tabel 14, Padang Tikar Tabel 15 (+16), Pulau Maya Tabel 15. Per-cell `QUALITY` flag; `VERIFIED = NO` until checked against the PDFs. | s08, s11, s14 |
| `HCV_SK_AREAS.csv` | SK number, date and area of all 25 HD (Tabel 1 of each report; sum 124,941 ha) | s14 |
| Project Area shapefile `Delta_Kapuas_Project_Boundary_(Update)` | Supplied by the researcher (not redistributed); cleaned copy in `01_BOUNDARY_QA/` | s06 → s03 |
| `BOUNDARY_AND_PULAU_MAYA_VERIFICATION.xlsx` | **Not present** in this session; the audit was redone from the shapefile | – |
| HD SK boundary geometry | **Not supplied** (needed for R1/R2 activity shares) | s07 (optional 3rd argument) |
| Vensim V5.4.2R `.mdl` | **Not supplied**; parameter mapping left to the researcher | – |

Cells flagged `RECONSTRUCTED_BY_COLUMN_TOTAL` (Pulau Maya: dryland forest, settlements, plantations, dryland agriculture, mixed dryland agriculture, swamp, rice field) and `ADDED_FROM_TABEL16...` (Padang Tikar 2024 settlements) are reconstructions. Verify them against the PDF tables before publication.
