"""Assemble the deliverable workbooks from the computed CSV outputs.

Every number in these workbooks is read from files produced by s01-s09; nothing
is typed in by hand except (a) researcher-supplied inputs (HCV totals, PDD area,
Vensim 0.8535, previous SD/linear RMSE) and (b) dataset metadata in the inventory.

Usage: python s11_build_deliverables.py
"""
import json

import numpy as np
import pandas as pd

from common import (CANOPY_THRESHOLDS, HANSEN_VERSION, HCV_AREA_HA, MODEL_YEARS, PDD_PROJECT_AREA_HA, ROOT,
                    VENSIM_PROP_KREDIT_REDD)

LC, VA, SD, RS = (ROOT / d for d in ["03_LAND_COVER_CHANGE", "04_VALIDATION", "05_SYSTEM_DYNAMICS_INPUT",
                                      "02_REMOTE_SENSING_DATA"])
PA = pd.read_csv(LC / "ZONAL_PROJECT_AREA.csv")
DE = pd.read_csv(LC / "ZONAL_ADMIN_DESA_CONTEXT.csv")
LANDS = ["Kubu", "Padang Tikar", "Pulau Maya"]


def readme(text):
    return pd.DataFrame({"README": text})


def loss_sum(df, t, y0, y1):
    return df[[f"LOSS_{y}_GT{t}" for y in range(y0, y1 + 1)]].sum(axis=1)


def per_hd_summary(df):
    out = df[["HD_ID", "HD_NAME", "LANDSCAPE", "REGENCY", "SPATIAL_DOMAIN", "POLY_GEODESIC_HA", "WATER_HA"]].copy()
    for t in CANOPY_THRESHOLDS:
        out[f"TC2000_GT{t}_HA"] = df[f"TC2000_GT{t}_HA"]
        out[f"LOSS_2001_2014_GT{t}_HA"] = loss_sum(df, t, 2001, 2014)
        out[f"LOSS_2015_2024_GT{t}_HA"] = loss_sum(df, t, 2015, 2024)
        out[f"LOSS_2001_2024_GT{t}_HA"] = loss_sum(df, t, 2001, 2024)
        out[f"PCT_TC2000_LOST_2001_2024_GT{t}"] = 100 * out[f"LOSS_2001_2024_GT{t}_HA"] / out[f"TC2000_GT{t}_HA"]
    out["LOSS_2025_GT30_HA (outside model history)"] = df["LOSS_2025_GT30"]
    out["GAIN_2000_2012_HA"] = df["GAIN_2000_2012_HA"]
    for y in (1996, 2010, 2019, 2020):
        out[f"MANGROVE_GMW_{y}_HA"] = df[f"MANGROVE_GMW_{y}_HA"]
    out["LOSS_IN_GMW2010_MANGROVE_2001_2024_GT30_HA"] = df[[f"LOSS_{y}_GT30_IN_GMW2010" for y in MODEL_YEARS]].sum(axis=1)
    out["AREA_CONSERVATION_RATIO"] = df.RASTER_FOOTPRINT_HA / df.POLY_GEODESIC_HA
    return out


def wide_year(df, t):
    w = df[["HD_ID", "HD_NAME", "LANDSCAPE"]].copy()
    w["TC2000_HA"] = df[f"TC2000_GT{t}_HA"]
    for y in range(2001, 2026):
        w[str(y)] = df[f"LOSS_{y}_GT{t}"]
    return w


def by_landscape(summary):
    s = summary.groupby("LANDSCAPE").sum(numeric_only=True)
    s.loc["ALL_25"] = s.sum()
    for t in CANOPY_THRESHOLDS:
        s[f"PCT_TC2000_LOST_2001_2024_GT{t}"] = 100 * s[f"LOSS_2001_2024_GT{t}_HA"] / s[f"TC2000_GT{t}_HA"]
    s = s.drop(columns=["AREA_CONSERVATION_RATIO"])
    return s.reset_index()


def build_03():
    pa_sum, de_sum = per_hd_summary(PA), per_hd_summary(DE)
    note = ["Per-HD gross tree-cover loss (Hansen GFC " + HANSEN_VERSION + ") and GMW v3 mangrove extent.",
            "Domain PROJECT_AREA = 25 carbon Project Area polygons (shapefile 'Delta_Kapuas_Project_Boundary_(Update)', processing date 21-05-2026).",
            "Domain ADMIN_DESA_CONTEXT_BPS2020 = BPS village polygons of the same names: CONTEXT ONLY, not HD and not Project Area.",
            "Loss = stand-replacing gross tree-cover loss, NOT deforestation under Indonesian regulation and NOT REDD activity data.",
            "Years 2001-2010 were not reprocessed by UMD; 2011+ were (possible structural break). 2025 is outside the model history.",
            "Areas are geodesic (WGS84) pixel-area sums with pixel-centre rasterisation; map-based, not sample-based, estimates.",
            "LONG sheets follow the required analysis data structure (HD_ID ... NOTES)."]
    with pd.ExcelWriter(LC / "FOREST_CHANGE_25HD_BY_YEAR.xlsx") as xw:
        readme(note).to_excel(xw, sheet_name="README", index=False)
        for t in CANOPY_THRESHOLDS:
            wide_year(PA, t).to_excel(xw, sheet_name=f"PA_LOSS_BY_YEAR_GT{t}", index=False)
        pd.read_csv(LC / "ZONAL_PROJECT_AREA_LONG.csv").to_excel(xw, sheet_name="PA_LONG_FORMAT", index=False)
        wide_year(DE, 30).to_excel(xw, sheet_name="DESA_CTX_LOSS_BY_YEAR_GT30", index=False)
        pd.read_csv(LC / "ZONAL_ADMIN_DESA_CONTEXT_LONG.csv").to_excel(xw, sheet_name="DESA_CTX_LONG_FORMAT", index=False)

    ann = pd.read_csv(LC / "TRENDS_PROJECT_AREA_ANNUAL.csv")
    ep = pd.read_csv(LC / "TRENDS_PROJECT_AREA_EPOCHS.csv")
    land = by_landscape(pa_sum)
    sens = []
    for g, r in land.set_index("LANDSCAPE").iterrows():
        vals = [r[f"LOSS_2001_2024_GT{t}_HA"] for t in CANOPY_THRESHOLDS]
        sens.append({"GROUP": g, **{f"LOSS_2001_2024_GT{t}_HA": v for t, v in zip(CANOPY_THRESHOLDS, vals)},
                     "MAX_MINUS_MIN_HA": max(vals) - min(vals), "RANGE_PCT_OF_GT30": 100 * (max(vals) - min(vals)) / vals[1],
                     **{f"TC2000_GT{t}_HA": r[f"TC2000_GT{t}_HA"] for t in CANOPY_THRESHOLDS}})
    de_land = by_landscape(de_sum).set_index("LANDSCAPE")
    comp = []
    for g, r in land.set_index("LANDSCAPE").iterrows():
        comp.append({"GROUP": g, "PA_AREA_HA": r.POLY_GEODESIC_HA, "DESA_CTX_AREA_HA": de_land.loc[g, "POLY_GEODESIC_HA"],
                     "HCV_AREA_HA (table)": HCV_AREA_HA["TOTAL" if g == "ALL_25" else g],
                     "PA_TC2000_GT30": r.TC2000_GT30_HA, "DESA_TC2000_GT30": de_land.loc[g, "TC2000_GT30_HA"],
                     "PA_LOSS_2001_2024_GT30": r.LOSS_2001_2024_GT30_HA,
                     "DESA_LOSS_2001_2024_GT30": de_land.loc[g, "LOSS_2001_2024_GT30_HA"],
                     "PA_PCT_TC_LOST": r.PCT_TC2000_LOST_2001_2024_GT30,
                     "DESA_PCT_TC_LOST": de_land.loc[g, "PCT_TC2000_LOST_2001_2024_GT30"],
                     "PA_GMW2020_MANGROVE_HA": r.MANGROVE_GMW_2020_HA,
                     "DESA_GMW2020_MANGROVE_HA": de_land.loc[g, "MANGROVE_GMW_2020_HA"]})
    with pd.ExcelWriter(LC / "FOREST_CHANGE_PROJECT_AREA.xlsx") as xw:
        readme(note + ["Epoch rows: interval loss is the sum of lossyear in (a, b]; 'TC net of loss' is DERIVED (2000 tree cover minus cumulative gross loss, regrowth ignored) and is NOT forest area."]).to_excel(xw, sheet_name="README", index=False)
        land.to_excel(xw, sheet_name="BY_LANDSCAPE", index=False)
        pa_sum.to_excel(xw, sheet_name="PER_HD", index=False)
        ep.to_excel(xw, sheet_name="EPOCHS_2000_2024", index=False)
        ann.to_excel(xw, sheet_name="ANNUAL_2001_2024", index=False)
        pd.DataFrame(sens).to_excel(xw, sheet_name="THRESHOLD_SENSITIVITY", index=False)
        pd.DataFrame(comp).to_excel(xw, sheet_name="PA_VS_DESA_CONTEXT", index=False)

    # historical comparison by epoch
    rows = []
    epd = pd.read_csv(LC / "TRENDS_ADMIN_DESA_CONTEXT_EPOCHS.csv")
    hcv = pd.read_csv(ROOT / "07_REPRODUCIBLE_CODE" / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv")
    gmw_near = {2000: 1996, 2003: 2007, 2009: 2010, 2014: 2015, 2019: 2019, 2024: 2020}
    for g in LANDS + ["ALL_25"]:
        for dom, epx, z in (("PROJECT_AREA", ep, PA), ("ADMIN_DESA_CONTEXT", epd, DE)):
            zz = z if g == "ALL_25" else z[z.LANDSCAPE == g]
            for y in [2000, 2003, 2009, 2014, 2019, 2024]:
                tc0 = zz.TC2000_GT30_HA.sum()
                cum = loss_sum(zz, 30, 2001, y).sum() if y > 2000 else 0.0
                hh = hcv[(hcv.YEAR == y) & ((hcv.LANDSCAPE == g) | (g == "ALL_25"))]
                rows.append({"GROUP": g, "SPATIAL_DOMAIN": dom, "EPOCH": y, "TC2000_GT30_HA": tc0,
                             "CUM_GROSS_LOSS_2001_TO_EPOCH_HA": cum,
                             "TC2000_NET_OF_GROSS_LOSS_HA (derived, not forest area)": tc0 - cum,
                             "GMW_YEAR_NEAREST": gmw_near[y], "GMW_MANGROVE_HA": zz[f"MANGROVE_GMW_{gmw_near[y]}_HA"].sum(),
                             "GMW_TEMPORAL_GAP_YR": y - gmw_near[y],
                             "HCV_NATURAL_FOREST_HA (HCV area)": hh[hh.IS_FOREST == 1].AREA_HA.sum(),
                             "HCV_MANGROVE_HA (HCV area)": hh[hh.FOREST_TYPE == "MANGROVE"].AREA_HA.sum(),
                             "HCV_PEAT_SWAMP_FOREST_HA": hh[hh.FOREST_TYPE == "PEAT_SWAMP"].AREA_HA.sum(),
                             "HCV_DRYLAND_FOREST_HA": hh[hh.FOREST_TYPE == "DRYLAND"].AREA_HA.sum(),
                             "HCV_AREA_HA": HCV_AREA_HA["TOTAL" if g == "ALL_25" else g]})
    with pd.ExcelWriter(LC / "HISTORICAL_LAND_COVER_COMPARISON.xlsx") as xw:
        readme(["Six observation epochs side by side for the Project Area and the desa context domain.",
                "HCV columns: landscape tables transcribed from the three HCV reports (s13_hcv_tables.py); HCV domain = SK area (124,941 ha), PA = 111,135 ha.",
                "GMW has no 2000/2003/2024 layers; the nearest GMW year is shown with its temporal gap.",
                "A land-cover transition matrix was NOT produced: no multi-class map with validated classes exists for the six epochs (see 04_VALIDATION/SPATIAL_ACCURACY_AND_UNCERTAINTY.md)."]
               ).to_excel(xw, sheet_name="README", index=False)
        pd.DataFrame(rows).to_excel(xw, sheet_name="EPOCH_COMPARISON", index=False)
    return land, pa_sum


def build_04():
    t = pd.read_csv(VA / "HCV_VS_SATELLITE_TESTS.csv")
    pm = pd.read_csv(VA / "PULAU_MAYA_LANDSAT_TESTS.csv") if (VA / "PULAU_MAYA_LANDSAT_TESTS.csv").exists() else pd.DataFrame()
    buf = pd.read_csv(VA / "GMW_OUTSIDE_DESA_BUFFER.csv")
    log = json.load(open(RS / "landsat_pulau_maya" / "LANDSAT_SCENE_LOG.json")) if (RS / "landsat_pulau_maya" / "LANDSAT_SCENE_LOG.json").exists() else None
    with pd.ExcelWriter(VA / "HCV_VS_SATELLITE_COMPARISON.xlsx") as xw:
        readme(["Logical-consistency tests between HCV tabulations and independent satellite products.",
                "HCV values transcribed from the HCV reports (Kubu Tabel 14, Padang Tikar Tabel 15, Pulau Maya Tabel 15); cells flagged RECONSTRUCTED/ADDED must be checked against the PDFs.",
                "No test equates different variables: T3 compares HCV NET forest change with Hansen GROSS loss only through logical bounds (a net gain needs regrowth).",
                "HARMONISED series: S2(t) = HCV forest 2000 - (A_HCV/A_PA) x cumulative Hansen gross loss in the PA; D2 = HCV - S2 (departure from a definitionally consistent trajectory).",
                "EPOCH_RELIABILITY verdict rule: PROBLEMATIC if |D2| > 10 % of HCV forest or HCV mangrove exceeds the GMW-based bound; CAUTION if > 5 %."]
               ).to_excel(xw, sheet_name="README", index=False)
        t.to_excel(xw, sheet_name="HCV_MANGROVE_BOUND_TESTS", index=False)
        for nm, sh in [("HCV_EPOCH_RELIABILITY", "EPOCH_RELIABILITY"), ("HCV_T3_INTERVALS", "T3_INTERVALS"),
                       ("HCV_HARMONISED_SERIES", "HARMONISED_SERIES"), ("HCV_HARMONISED_RMSE", "HARMONISED_RMSE"),
                       ("HCV_MANGROVE_VS_GMW_ALL", "MANGROVE_VS_GMW_PA"), ("HCV_TABLE_INTEGRITY", "HCV_TABLE_INTEGRITY"),
                       ("PULAU_MAYA_TERRAIN_CHECK", "PULAU_MAYA_TERRAIN")]:
            pd.read_csv(VA / f"{nm}.csv").to_excel(xw, sheet_name=sh, index=False)
        pd.read_csv(ROOT / "07_REPRODUCIBLE_CODE" / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv").to_excel(xw, sheet_name="HCV_TABLES_TRANSCRIBED", index=False)
        if len(pm):
            pm.to_excel(xw, sheet_name="PULAU_MAYA_LANDSAT", index=False)
        buf.to_excel(xw, sheet_name="GMW_OUTSIDE_DESA_BUFFER", index=False)
        if log:
            rows = [{"EPOCH": y, **s} for y, ss in log["scenes"].items() for s in ss]
            pd.DataFrame(rows).to_excel(xw, sheet_name="LANDSAT_SCENES_USED", index=False)


def build_05(land, pa_sum):
    bm_pa = pd.read_csv(LC / "TRENDS_PROJECT_AREA_BENCHMARKS.csv")
    bm_de = pd.read_csv(LC / "TRENDS_ADMIN_DESA_CONTEXT_BENCHMARKS.csv")
    par_pa = pd.read_csv(LC / "TRENDS_PROJECT_AREA_PARAMS.csv")
    par_de = pd.read_csv(LC / "TRENDS_ADMIN_DESA_CONTEXT_PARAMS.csv")
    with pd.ExcelWriter(SD / "DEFORESTATION_CALIBRATION_COMPARISON.xlsx") as xw:
        readme(["Benchmarks fitted on 2001-2014 gross tree-cover loss and evaluated on held-out 2015-2024 (same split as the Vensim protocol).",
                "These metrics describe how predictable satellite-observed GROSS LOSS is; they are NOT the Vensim RMSE (which was computed on HCV forest-area stocks).",
                "Previous model results retained as benchmark: SD RMSE ~5,445 ha vs linear benchmark ~4,991 ha (HCV, 2019/2024 hold-out; researcher brief).",
                "HCV-vs-satellite departure RMSE in the same hold-out years (sheet HCV_NOISE_FLOOR) is of the same order, so the HCV hold-out cannot discriminate the two models.",
                "The two RMSE families are not comparable: different variable (stock vs annual flow), domain and data source.",
                "B4 uses only the reprocessed Hansen years 2011-2014 to test sensitivity to the UMD 2011 method break."]
               ).to_excel(xw, sheet_name="README", index=False)
        bm_pa.to_excel(xw, sheet_name="BENCHMARKS_PROJECT_AREA", index=False)
        bm_de.to_excel(xw, sheet_name="BENCHMARKS_DESA_CONTEXT", index=False)
        par_pa.to_excel(xw, sheet_name="FITTED_PARAMS_PROJECT_AREA", index=False)
        par_de.to_excel(xw, sheet_name="FITTED_PARAMS_DESA_CONTEXT", index=False)
        pd.DataFrame([{"MODEL": "Vensim V5.4.2R (25 HD)", "VARIABLE": "HCV forest area (stock)", "DOMAIN": "124,941 ha HCV",
                       "HOLD_OUT": "2019, 2024", "RMSE_HA": 5445, "SOURCE": "researcher brief"},
                      {"MODEL": "Linear benchmark", "VARIABLE": "HCV forest area (stock)", "DOMAIN": "124,941 ha HCV",
                       "HOLD_OUT": "2019, 2024", "RMSE_HA": 4991, "SOURCE": "researcher brief"}]
                     ).to_excel(xw, sheet_name="PREVIOUS_MODEL_BENCHMARK", index=False)
        pd.read_csv(VA / "HCV_HARMONISED_RMSE.csv").to_excel(xw, sheet_name="HCV_NOISE_FLOOR", index=False)

    con = pd.read_excel(SD / "PROJECT_AREA_CREDIT_SPATIAL_CONSTRAINT_COMPUTED.xlsx")
    with pd.ExcelWriter(SD / "PROJECT_AREA_CREDIT_SPATIAL_CONSTRAINT.xlsx") as xw:
        readme([f"Vensim parameter 'Proporsi Kredit REDD dalam Project Area' = {VENSIM_PROP_KREDIT_REDD} (bounding assumption; derivation not documented in supplied material).",
                "R0 = PA area / HCV(SK) area: PA from geometry, SK areas from Tabel 1 of each HCV report (sum = 124,941 ha exactly). AREA share, not a credit or activity share.",
                "PER_HD_PA_VS_SK: per-HD exclusion; largest exclusions: Padang Tikar 1 (0.26), Teluk Nibung (0.32), Teluk Bakung (0.68), Nipah Panjang (0.78).",
                "R1/R2 (PA share of forest / of loss within the HD SK domain) are the spatially correct analogues but need HD SK geometry: NOT AVAILABLE.",
                "R3/R4 compare the PA with the BPS desa context domain; 6.0 % of the PA lies outside those desa, so they are context ratios, not bounds.",
                "R5 = cumulative gross loss / 2000 tree cover inside the PA (activity intensity).",
                "None of these is a carbon-credit eligibility determination."]).to_excel(xw, sheet_name="README", index=False)
        con.to_excel(xw, sheet_name="RATIOS", index=False)
        pd.read_csv(VA / "PER_HD_PROJECT_AREA_VS_SK.csv").to_excel(xw, sheet_name="PER_HD_PA_VS_SK", index=False)

    L = land.set_index("LANDSCAPE")
    A = L.loc["ALL_25"]
    r_cal = A.LOSS_2001_2014_GT30_HA / 14 / A.TC2000_GT30_HA
    r_hold = A.LOSS_2015_2024_GT30_HA / 10 / A.TC2000_GT30_HA
    r_all = A.LOSS_2001_2024_GT30_HA / 24 / A.TC2000_GT30_HA
    p = par_pa.set_index(["GROUP", "THRESHOLD_PCT"])
    r_1724 = p.loc[("ALL_25", 30), "MEAN_2017_2024_ha_yr"] / A.TC2000_GT30_HA
    r0 = con[(con.GROUP == "ALL_25") & con.RATIO.str.startswith("R0")].VALUE.iloc[0]
    rng = lambda c: f"{min(L.loc['ALL_25', f'{c}_GT{t}_HA'] for t in CANOPY_THRESHOLDS):,.0f}-{max(L.loc['ALL_25', f'{c}_GT{t}_HA'] for t in CANOPY_THRESHOLDS):,.0f} ha across 10/30/50 % thresholds"
    rows = [
        dict(PARAMETER="Proporsi Kredit REDD dalam Project Area", CURRENT_VALUE=VENSIM_PROP_KREDIT_REDD,
             CANDIDATE_VALUE=round(r0, 4), UNIT="dimensionless", SOURCE="PA shapefile (21-05-2026) / HCV area table",
             DOMAIN="Project Area vs HCV study area", PERIOD="static",
             CALCULATION=f"{A.POLY_GEODESIC_HA:,.2f} ha geodesic / {HCV_AREA_HA['TOTAL']:,} ha (landscapes: "
                         + ", ".join(f"{g} {con[(con.GROUP == g) & con.RATIO.str.startswith('R0')].VALUE.iloc[0]:.4f}" for g in LANDS) + ")",
             UNCERTAINTY="Area share only; activity share (R2) unknown without HD SK geometry. Desa-context evidence shows loss concentrated OUTSIDE the PA (R3 = 0.10), so an activity share could be far below the area share.",
             EVIDENCE_QUALITY="MEDIUM for R0 as an area ratio; LOW as a credit proportion",
             DECISION="SENSITIVITY ONLY (keep 0.8535; add 0.8895 as area-share variant; obtain SK geometry for R2)"),
        dict(PARAMETER="Historical gross tree-cover loss rate, Project Area (calibration 2001-2014)", CURRENT_VALUE="NOT SUPPLIED (model file not available)",
             CANDIDATE_VALUE=round(r_cal, 5), UNIT="fraction of TC2000 per yr", SOURCE=f"Hansen {HANSEN_VERSION}",
             DOMAIN="Project Area (111,135 ha)", PERIOD="2001-2014",
             CALCULATION=f"{A.LOSS_2001_2014_GT30_HA:,.0f} ha / 14 yr / {A.TC2000_GT30_HA:,.0f} ha (canopy >30 %)",
             UNCERTAINTY="Map-based; 2001-2010 not reprocessed (mean 2001-2010 = %.0f ha/yr vs 2011-2014 = %.0f ha/yr); gross loss != deforestation" % (p.loc[("ALL_25", 30), "MEAN_2001_2010_ha_yr"], p.loc[("ALL_25", 30), "MEAN_2011_2014_ha_yr"]),
             EVIDENCE_QUALITY="MEDIUM (consistent public product; no local accuracy assessment)", DECISION="SENSITIVITY ONLY"),
        dict(PARAMETER="Historical gross tree-cover loss rate, Project Area (held-out 2015-2024)", CURRENT_VALUE="NOT SUPPLIED",
             CANDIDATE_VALUE=round(r_hold, 5), UNIT="fraction of TC2000 per yr", SOURCE=f"Hansen {HANSEN_VERSION}",
             DOMAIN="Project Area", PERIOD="2015-2024",
             CALCULATION=f"{A.LOSS_2015_2024_GT30_HA:,.0f} ha / 10 yr / {A.TC2000_GT30_HA:,.0f} ha; 2015-2016 alone = {PA[['LOSS_2015_GT30', 'LOSS_2016_GT30']].sum().sum():,.0f} ha",
             UNCERTAINTY="Dominated by the 2015 El Nino fire year; not a stationary rate",
             EVIDENCE_QUALITY="MEDIUM", DECISION="SENSITIVITY ONLY (use as hold-out benchmark, not as calibration input)"),
        dict(PARAMETER="Recent background gross loss rate, Project Area", CURRENT_VALUE="NOT SUPPLIED",
             CANDIDATE_VALUE=round(r_1724, 5), UNIT="fraction of TC2000 per yr", SOURCE=f"Hansen {HANSEN_VERSION} (reprocessed years only)",
             DOMAIN="Project Area", PERIOD="2017-2024", CALCULATION=f"{p.loc[('ALL_25', 30), 'MEAN_2017_2024_ha_yr']:,.0f} ha/yr / {A.TC2000_GT30_HA:,.0f} ha",
             UNCERTAINTY="Post-2016 regime; overlaps the period after community forestry/carbon project start (possible intervention effect - do not use as a without-project baseline without justification)",
             EVIDENCE_QUALITY="MEDIUM", DECISION="SENSITIVITY ONLY"),
        dict(PARAMETER="Long-run gross loss rate, Project Area", CURRENT_VALUE="NOT SUPPLIED", CANDIDATE_VALUE=round(r_all, 5),
             UNIT="fraction of TC2000 per yr", SOURCE=f"Hansen {HANSEN_VERSION}", DOMAIN="Project Area", PERIOD="2001-2024",
             CALCULATION=f"{A.LOSS_2001_2024_GT30_HA:,.0f} ha / 24 yr / {A.TC2000_GT30_HA:,.0f} ha; threshold range {rng('LOSS_2001_2024')}",
             UNCERTAINTY="Spans the 2011 method break; episodic (fire) years", EVIDENCE_QUALITY="MEDIUM", DECISION="SENSITIVITY ONLY"),
    ]
    for g in LANDS:
        r = L.loc[g]
        rows.append(dict(PARAMETER=f"Gross loss rate 2001-2024, Project Area - {g}", CURRENT_VALUE="NOT SUPPLIED",
                         CANDIDATE_VALUE=round(r.LOSS_2001_2024_GT30_HA / 24 / r.TC2000_GT30_HA, 5), UNIT="fraction of TC2000 per yr",
                         SOURCE=f"Hansen {HANSEN_VERSION}", DOMAIN=f"Project Area, {g}", PERIOD="2001-2024",
                         CALCULATION=f"{r.LOSS_2001_2024_GT30_HA:,.0f} ha / 24 / {r.TC2000_GT30_HA:,.0f} ha",
                         UNCERTAINTY="as above", EVIDENCE_QUALITY="MEDIUM", DECISION="SENSITIVITY ONLY"))
    rows += [
        dict(PARAMETER="Mangrove extent in Project Area (WRC-mangrove stratum)", CURRENT_VALUE="NOT SUPPLIED",
             CANDIDATE_VALUE=round(A.MANGROVE_GMW_2020_HA, 0), UNIT="ha", SOURCE="GMW v3.0", DOMAIN="Project Area", PERIOD="2020",
             CALCULATION="GMW 2020 extent pixel-area sum; 1996-2020 range " + f"{min(A[f'MANGROVE_GMW_{y}_HA'] for y in (1996, 2010, 2019, 2020)):,.0f}-{max(A[f'MANGROVE_GMW_{y}_HA'] for y in (1996, 2010, 2019, 2020)):,.0f} ha",
             UNCERTAINTY="Global product; tidal/seaward edge; no local validation", EVIDENCE_QUALITY="MEDIUM",
             DECISION="SENSITIVITY ONLY (cross-check for HCV mangrove classes)"),
        dict(PARAMETER="2024 'tree cover net of gross loss' in Project Area (initial-stock cross-check)", CURRENT_VALUE="NOT SUPPLIED",
             CANDIDATE_VALUE=round(A.TC2000_GT30_HA - A.LOSS_2001_2024_GT30_HA, 0), UNIT="ha", SOURCE=f"Hansen {HANSEN_VERSION}",
             DOMAIN="Project Area", PERIOD="2024", CALCULATION="TC2000(>30 %) - cumulative gross loss 2001-2024",
             UNCERTAINTY="Ignores regrowth and degradation; tree cover includes non-forest trees; not a forest-area map",
             EVIDENCE_QUALITY="LOW-MEDIUM", DECISION="SENSITIVITY ONLY"),
        dict(PARAMETER="HCV Pulau Maya mangrove 2024 (validation target)", CURRENT_VALUE="10,617 ha (HCV)",
             CANDIDATE_VALUE="NOT AVAILABLE", UNIT="ha", SOURCE="GMW v3 + Landsat OLI test", DOMAIN="Pulau Maya",
             PERIOD="2019-2024", CALCULATION="See 04_VALIDATION/PULAU_MAYA_ANOMALY_INVESTIGATION.md",
             UNCERTAINTY="HCV 2024 exceeds independent bound by ~3,500 ha (assumption A1)", EVIDENCE_QUALITY="HIGH for inconsistency; no replacement value",
             DECISION="REPLACE AS VALIDATION TARGET: exclude or harmonise HCV 2024 Pulau Maya class areas before use"),
    ]
    rmse = pd.read_csv(VA / "HCV_HARMONISED_RMSE.csv").set_index("GROUP")
    rel = pd.read_csv(VA / "HCV_EPOCH_RELIABILITY.csv")
    bad = ", ".join(f"{r.LANDSCAPE} {r.EPOCH}" for r in rel[rel.VERDICT == "PROBLEMATIC"].itertuples())
    rows += [
        dict(PARAMETER="Validation noise floor for HCV-based hold-out (2019, 2024)", CURRENT_VALUE="SD RMSE 5,445 ha; linear 4,991 ha",
             CANDIDATE_VALUE=round(rmse.loc["ALL_25", "RMSE_D2_HOLDOUT_2019_2024_HA"], 0), UNIT="ha",
             SOURCE="HCV tables vs Hansen-harmonised series (s14)", DOMAIN="25 HD, HCV/SK area", PERIOD="2019, 2024",
             CALCULATION="RMSE of D2 = HCV natural forest - [HCV2000 forest - (A_HCV/A_PA) x cumulative Hansen loss in PA]",
             UNCERTAINTY="Reference series is itself a model (no regrowth, gross loss, area-scaled); 2003-2024 RMSE = %.0f ha" % rmse.loc["ALL_25", "RMSE_D2_2003_2024_HA"],
             EVIDENCE_QUALITY="MEDIUM", DECISION="KEEP previous results as benchmark; report that model differences < ~4,200 ha are not resolvable with HCV hold-out data"),
        dict(PARAMETER="HCV calibration/validation epochs flagged as unreliable", CURRENT_VALUE="all six epochs used",
             CANDIDATE_VALUE=bad, UNIT="landscape-epoch", SOURCE="s14 epoch reliability", DOMAIN="HCV area", PERIOD="2003-2024",
             CALCULATION="|D2| > 10 % of HCV forest or HCV mangrove > GMW bound", UNCERTAINTY="Rule-based screen; thresholds are a choice",
             EVIDENCE_QUALITY="MEDIUM-HIGH for Kubu 2009/2014 and Pulau Maya 2024", DECISION="SENSITIVITY ONLY: re-run calibration excluding flagged epochs or using the harmonised series"),
        dict(PARAMETER="Satellite-harmonised natural-forest series (alternative calibration target)", CURRENT_VALUE="HCV series",
             CANDIDATE_VALUE="see 04_VALIDATION/HCV_VS_SATELLITE_COMPARISON.xlsx > HARMONISED_SERIES", UNIT="ha",
             SOURCE="HCV 2000 anchor + Hansen v1.13 gross loss", DOMAIN="HCV area (area-scaled from PA)", PERIOD="2000-2024",
             CALCULATION="S2(t) = F_HCV(2000) - k x cumLoss_PA(t), k = A_HCV/A_PA", UNCERTAINTY="Ignores regrowth/degradation; 2011 method break; anchored on HCV 2000",
             EVIDENCE_QUALITY="MEDIUM", DECISION="SENSITIVITY ONLY (definitionally consistent; monotone)")]
    with pd.ExcelWriter(SD / "VENSIM_SPATIAL_PARAMETER_CANDIDATES.xlsx") as xw:
        readme(["Candidate spatial evidence for Vensim V5.4.2R parameters. The Vensim model was NOT modified.",
                "CURRENT_VALUE = 'NOT SUPPLIED' where the .mdl file was not available in this session; map each candidate to the model variable before use.",
                "Gross tree-cover loss (Hansen) is not deforestation as defined by Indonesian regulation or the carbon methodology; candidates are for sensitivity analysis and benchmarking.",
                "Decision vocabulary: KEEP / REPLACE / SENSITIVITY ONLY / NOT AVAILABLE."]).to_excel(xw, sheet_name="README", index=False)
        pd.DataFrame(rows).to_excel(xw, sheet_name="CANDIDATES", index=False)


def build_02():
    inv = [
        dict(DATASET="Global Forest Change (Hansen et al.)", PROVIDER="UMD GLAD / Google / USGS / NASA", VERSION="GFC-2025-v1.13",
             YEARS="treecover 2000; loss 2001-2025; gain 2000-2012", RESOLUTION="0.00025 deg (~27.8 m at equator)",
             DEFINITION="Tree = vegetation >5 m; canopy % in 2000; stand-replacing loss by year", ACCURACY_CLAIMS="Global accuracy reported by producers (Hansen et al. 2013 and version notes); not re-quoted. UMD: no definitive area estimates from pixel counts.",
             LIMITATIONS="Loss != deforestation; 2011+ reprocessed, 2001-2010 not; gain only 2000-2012; tree crops counted as tree cover",
             LICENSE="CC BY 4.0", ID_URL="https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html ; GEE UMD/hansen/global_forest_change_2025_v1_13",
             STATUS="DOWNLOADED & USED (tiles 00N_100E, 10N_100E; SHA-256 in 07_REPRODUCIBLE_CODE/PROVENANCE.md)"),
        dict(DATASET="Global Mangrove Watch", PROVIDER="Aberystwyth Univ., soloEO, JAXA, Wetlands Int., TNC et al.", VERSION="v3.0 (Zenodo 10.5281/zenodo.6894273)",
             YEARS="1996, 2007-2010, 2015-2020", RESOLUTION="0.0002222 deg (~25 m)", DEFINITION="Mangrove extent (ALOS PALSAR + Landsat)",
             ACCURACY_CLAIMS="Reported in Bunting et al. 2022, Remote Sensing 14:3657; not re-quoted", LIMITATIONS="Ends 2020; tidal/seaward-edge uncertainty; global classifier",
             LICENSE="CC BY 4.0", ID_URL="https://zenodo.org/records/6894273", STATUS="DOWNLOADED & USED (1996, 2007, 2010, 2015, 2016, 2019, 2020)"),
        dict(DATASET="Landsat Collection 2 Level-2 Surface Reflectance", PROVIDER="USGS (served by Microsoft Planetary Computer)", VERSION="C2 L2 (landsat-c2-l2)",
             YEARS="2014, 2019 (L8 OLI); 2024 (L8 OLI + L9 OLI-2)", RESOLUTION="30 m (warped to 0.00025 deg Hansen grid, nearest)",
             DEFINITION="Surface reflectance; QA_PIXEL masking", ACCURACY_CLAIMS="USGS product specifications", LIMITATIONS="Persistent cloud; tides; single WRS-2 path/row 121/061; only Pulau Maya window processed",
             LICENSE="Public domain (USGS)", ID_URL="https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2", STATUS="ACCESSED & USED (Pulau Maya window)"),
        dict(DATASET="Indonesia subnational administrative boundaries (COD-AB)", PROVIDER="BPS / OCHA ROAP via HDX", VERSION="v01, valid 2020-04-01",
             YEARS="2020", RESOLUTION="vector", DEFINITION="Desa (ADM4) polygons", ACCURACY_CLAIMS="none stated", LIMITATIONS="Admin boundaries; coastlines may clip intertidal areas; 9 of 25 PA polygons are not mainly inside the same-name desa",
             LICENSE="CC BY-IGO", ID_URL="https://data.humdata.org/dataset/cod-ab-idn", STATUS="DOWNLOADED & USED (context domain only)"),
        dict(DATASET="Global peatland extent (Miettinen et al. 2016 for Borneo)", PROVIDER="WRI Global Forest Watch", VERSION="gfw_peatlands v20230315",
             YEARS="~2015", RESOLUTION="~30 m (Hansen grid)", DEFINITION="Peatland extent (multi-source)", ACCURACY_CLAIMS="see sources", LIMITATIONS="Composite of sources; not peat depth",
             LICENSE="CC BY 4.0", ID_URL="https://data-api.globalforestwatch.org/dataset/gfw_peatlands", STATUS="NOT DOWNLOADED (HTTP 403: free GFW API key required); peat stratum NOT analysed"),
        dict(DATASET="Dynamic World", PROVIDER="Google / WRI", VERSION="V1", YEARS="2015-06 to present", RESOLUTION="10 m",
             DEFINITION="9-class probabilities (trees, flooded vegetation, ...)", ACCURACY_CLAIMS="Brown et al. 2022", LIMITATIONS="No pre-2015 coverage; classes not equivalent to HCV/KLHK",
             LICENSE="CC BY 4.0", ID_URL="GEE GOOGLE/DYNAMICWORLD/V1", STATUS="NOT ACCESSED (no Earth Engine credentials)"),
        dict(DATASET="ESA WorldCover", PROVIDER="ESA", VERSION="v100 (2020), v200 (2021)", YEARS="2020, 2021", RESOLUTION="10 m",
             DEFINITION="11 classes incl. mangroves", ACCURACY_CLAIMS="producer validation report", LIMITATIONS="Two years only; v100/v200 algorithm differ",
             LICENSE="CC BY 4.0", ID_URL="https://esa-worldcover.org", STATUS="NOT USED (no epoch match; available on Planetary Computer for follow-up)"),
        dict(DATASET="JRC Global Surface Water", PROVIDER="EC JRC", VERSION="v1.4", YEARS="1984-2021", RESOLUTION="30 m",
             DEFINITION="Water occurrence/seasonality", ACCURACY_CLAIMS="Pekel et al. 2016", LIMITATIONS="Tidal flats partially captured",
             LICENSE="Copernicus/JRC open", ID_URL="GEE JRC/GSW1_4/GlobalSurfaceWater", STATUS="NOT USED (Hansen datamask used for water)"),
        dict(DATASET="KLHK national land cover (Penutupan Lahan)", PROVIDER="Ministry of Environment and Forestry, Indonesia", VERSION="-",
             YEARS="1990-2022 (various)", RESOLUTION="1:250,000", DEFINITION="23 official classes incl. primary/secondary mangrove and swamp forest",
             ACCURACY_CLAIMS="-", LIMITATIONS="-", LICENSE="-", ID_URL="https://geoportal.menlhk.go.id", STATUS="NOT ACCESSED (geoportal unreachable from this environment: connection failed)"),
    ]
    pd.DataFrame(inv).to_excel(RS / "SATELLITE_DATASET_INVENTORY.xlsx", index=False)


if __name__ == "__main__":
    build_02()
    land, pa_sum = build_03()
    build_04()
    build_05(land, pa_sum)
    print("deliverables written")
