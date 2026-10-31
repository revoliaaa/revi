"""HCV historical land-cover series vs independent satellite evidence (Objective 3, 5).

Inputs: HCV_LANDCOVER_TABLES_FROM_REPORTS.csv (s13), ZONAL_PROJECT_AREA.csv (s03),
        HCV_SK_AREAS.csv (Tabel 1 of each report).

Analyses
  A  Per-HD Project Area / SK area (spatial constraint for the crediting share).
  B  Interval test T3: HCV net natural-forest change vs Hansen gross loss in the PA.
     A monotone gross-loss process cannot produce net forest INCREASES unless regrowth
     occurs; independent regrowth evidence is small (Hansen gain 2000-2012; Landsat test).
  C  Satellite-harmonised reference series, anchored to the HCV 2000 forest total:
        S_k(t) = F_HCV(2000) - k * cumulative gross loss in PA (2001..t)
     k = 1 (PA loss only; lower bound on loss in the larger HCV area)
     k = A_HCV / A_PA (area-scaled; assumes excluded area loses at the PA rate)
     D(t) = F_HCV(t) - S_k(t) measures the HCV departure from a definitionally
     consistent, monotone loss trajectory. RMSE(D) over 2003-2024 quantifies
     between-epoch classification inconsistency ("noise floor" for calibration).
  D  Mangrove: HCV mangrove classes vs GMW v3 in the PA, all landscapes.
Assumption A1 (stated, unverified): the PA lies inside the HCV study area.

Usage: python -I s14_hcv_vs_satellite.py
"""
import numpy as np
import pandas as pd

from common import CODE, HCV_AREA_HA, ROOT

EP = [2000, 2003, 2009, 2014, 2019, 2024]
GMW_NEAR = {2000: 1996, 2003: 2007, 2009: 2010, 2014: 2015, 2019: 2019, 2024: 2020}
LANDS = ["Kubu", "Padang Tikar", "Pulau Maya"]
VA, LC, SD = ROOT / "04_VALIDATION", ROOT / "03_LAND_COVER_CHANGE", ROOT / "05_SYSTEM_DYNAMICS_INPUT"


def main():
    hcv = pd.read_csv(CODE / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv")
    sk = pd.read_csv(CODE / "inputs" / "HCV_SK_AREAS.csv")
    pa = pd.read_csv(LC / "ZONAL_PROJECT_AREA.csv")

    # ---- A: per-HD PA / SK
    a = sk.merge(pa[["HD_ID", "HD_NAME", "POLY_GEODESIC_HA", "TC2000_GT30_HA"]], on="HD_NAME", how="left")
    utm = pd.read_excel(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx", sheet_name="PER_POLYGON")[["HD_NAME", "UTM49S_PLANAR_AREA_HA"]]
    a = a.merge(utm, on="HD_NAME", how="left")
    a["PA_OVER_SK_GEODESIC"] = a.POLY_GEODESIC_HA / a.SK_AREA_HA
    a["PA_OVER_SK_UTM49S"] = a.UTM49S_PLANAR_AREA_HA / a.SK_AREA_HA
    a["SK_MINUS_PA_UTM49S_HA"] = a.SK_AREA_HA - a.UTM49S_PLANAR_AREA_HA
    tot = a.groupby("LANDSCAPE")[["SK_AREA_HA", "UTM49S_PLANAR_AREA_HA", "POLY_GEODESIC_HA"]].sum()
    tot.loc["ALL_25"] = tot.sum()
    tot["PA_OVER_SK_UTM49S"] = tot.UTM49S_PLANAR_AREA_HA / tot.SK_AREA_HA
    a.to_csv(VA / "PER_HD_PROJECT_AREA_VS_SK.csv", index=False)
    print(a[["HD_ID", "HD_NAME", "LANDSCAPE", "SK_AREA_HA", "UTM49S_PLANAR_AREA_HA", "PA_OVER_SK_UTM49S", "SK_DATE"]].round(3).to_string())
    print(tot.round(3))

    # ---- natural forest series
    nat = hcv[hcv.IS_FOREST == 1]
    F = nat.pivot_table(index="LANDSCAPE", columns="YEAR", values="AREA_HA", aggfunc="sum")
    F.loc["ALL_25"] = F.sum()
    P = pa.groupby("LANDSCAPE").sum(numeric_only=True)
    P.loc["ALL_25"] = P.sum()
    cum = lambda g, y: sum(P.loc[g, f"LOSS_{yy}_GT30"] for yy in range(2001, y + 1))

    # ---- B: interval test
    rows = []
    for g in LANDS + ["ALL_25"]:
        k = (HCV_AREA_HA["TOTAL" if g == "ALL_25" else g]) / P.loc[g, "POLY_GEODESIC_HA"]
        for a_, b_ in zip(EP[:-1], EP[1:]):
            dF = F.loc[g, b_] - F.loc[g, a_]
            L = cum(g, b_) - cum(g, a_)
            rows.append({"GROUP": g, "INTERVAL": f"{a_}-{b_}", "HCV_NET_FOREST_CHANGE_HA": dF,
                         "HANSEN_GROSS_LOSS_PA_HA": L, "HANSEN_GROSS_LOSS_AREA_SCALED_HA": k * L,
                         "IMPLIED_MIN_REGROWTH_HA (dF + loss_PA)": max(dF + L, 0.0),
                         "HCV_MINUS_SATELLITE_EXPECTED_HA (k=1)": dF + L,
                         "HCV_MINUS_SATELLITE_EXPECTED_HA (area-scaled)": dF + k * L,
                         "DIRECTION_AGREES": (dF <= 0),
                         "FLAG": ("HCV NET GAIN: requires regrowth/reclassification" if dF > 0 else
                                  ("HCV LOSS >> SATELLITE LOSS" if -dF > 3 * k * L + 500 else "CONSISTENT ORDER OF MAGNITUDE"))})
    B = pd.DataFrame(rows)

    # ---- C: harmonised series and HCV departures
    rows = []
    for g in LANDS + ["ALL_25"]:
        k = (HCV_AREA_HA["TOTAL" if g == "ALL_25" else g]) / P.loc[g, "POLY_GEODESIC_HA"]
        for y in EP:
            s1 = F.loc[g, 2000] - cum(g, y)
            s2 = F.loc[g, 2000] - k * cum(g, y)
            rows.append({"GROUP": g, "YEAR": y, "HCV_NATURAL_FOREST_HA": F.loc[g, y],
                         "S1_HCV2000_MINUS_PA_LOSS_HA": s1, "S2_HCV2000_MINUS_AREA_SCALED_LOSS_HA": s2,
                         "D1_HA": F.loc[g, y] - s1, "D2_HA": F.loc[g, y] - s2,
                         "D2_PCT_OF_HCV_FOREST": 100 * (F.loc[g, y] - s2) / F.loc[g, y],
                         "ROLE": "CALIBRATION" if y <= 2014 else "HELD_OUT"})
    C = pd.DataFrame(rows)
    rm = (C[C.YEAR > 2000].groupby("GROUP")
          .apply(lambda d: pd.Series({"RMSE_D1_2003_2024_HA": np.sqrt((d.D1_HA ** 2).mean()),
                                      "RMSE_D2_2003_2024_HA": np.sqrt((d.D2_HA ** 2).mean()),
                                      "RMSE_D2_CAL_2003_2014_HA": np.sqrt((d[d.YEAR <= 2014].D2_HA ** 2).mean()),
                                      "RMSE_D2_HOLDOUT_2019_2024_HA": np.sqrt((d[d.YEAR >= 2019].D2_HA ** 2).mean()),
                                      "MAX_ABS_D2_HA": d.D2_HA.abs().max(),
                                      "YEAR_OF_MAX_ABS_D2": int(d.loc[d.D2_HA.abs().idxmax(), "YEAR"])}),
                 include_groups=False).reset_index())
    rm["PREVIOUS_SD_RMSE_HA"] = np.where(rm.GROUP == "ALL_25", 5445, np.nan)
    rm["PREVIOUS_LINEAR_RMSE_HA"] = np.where(rm.GROUP == "ALL_25", 4991, np.nan)

    # ---- D: mangrove
    M = hcv[hcv.FOREST_TYPE == "MANGROVE"].pivot_table(index="LANDSCAPE", columns="YEAR", values="AREA_HA", aggfunc="sum")
    rows = []
    for g in LANDS:
        slack = max(HCV_AREA_HA[g] - P.loc[g, "POLY_GEODESIC_HA"], 0)
        for y in EP:
            gm = P.loc[g, f"MANGROVE_GMW_{GMW_NEAR[y]}_HA"]
            rows.append({"LANDSCAPE": g, "HCV_YEAR": y, "HCV_MANGROVE_HA": M.loc[g, y], "GMW_YEAR": GMW_NEAR[y],
                         "GMW_MANGROVE_IN_PA_HA": gm, "HCV_AREA_OUTSIDE_PA_HA": slack,
                         "UPPER_BOUND_HA (A1)": gm + slack, "HCV_MINUS_GMW_PA_HA": M.loc[g, y] - gm,
                         "T1b_RESULT": "CONSISTENT" if M.loc[g, y] <= gm + slack else "EXCEEDS_INDEPENDENT_BOUND"})
    D = pd.DataFrame(rows)
    Dsum = D.groupby("LANDSCAPE").agg(HCV_MANGROVE_MIN=("HCV_MANGROVE_HA", "min"), HCV_MANGROVE_MAX=("HCV_MANGROVE_HA", "max"),
                                      GMW_PA_MIN=("GMW_MANGROVE_IN_PA_HA", "min"), GMW_PA_MAX=("GMW_MANGROVE_IN_PA_HA", "max"))
    Dsum["HCV_RANGE_HA"] = Dsum.HCV_MANGROVE_MAX - Dsum.HCV_MANGROVE_MIN
    Dsum["GMW_RANGE_HA"] = Dsum.GMW_PA_MAX - Dsum.GMW_PA_MIN

    # ---- epoch reliability verdict
    ver = []
    for g in LANDS:
        for y in EP[1:]:
            d2 = C[(C.GROUP == g) & (C.YEAR == y)].D2_HA.iloc[0]
            pct = 100 * abs(d2) / F.loc[g, y]
            mg = D[(D.LANDSCAPE == g) & (D.HCV_YEAR == y)].iloc[0]
            mg_flag = mg.T1b_RESULT != "CONSISTENT"
            ver.append({"LANDSCAPE": g, "EPOCH": y, "ABS_D2_HA": abs(d2), "ABS_D2_PCT_OF_HCV_FOREST": pct,
                        "MANGROVE_BOUND_EXCEEDED": mg_flag,
                        "VERDICT": ("PROBLEMATIC" if (pct > 10 or mg_flag) else ("CAUTION" if pct > 5 else "USABLE_WITH_UNCERTAINTY"))})
    V = pd.DataFrame(ver)

    for name, df in [("HCV_T3_INTERVALS", B), ("HCV_HARMONISED_SERIES", C), ("HCV_HARMONISED_RMSE", rm),
                     ("HCV_MANGROVE_VS_GMW_ALL", D), ("HCV_EPOCH_RELIABILITY", V)]:
        df.to_csv(VA / f"{name}.csv", index=False)
    F.to_csv(VA / "HCV_NATURAL_FOREST_SERIES.csv")
    pd.set_option("display.width", 250)
    print(B.round(0).to_string()); print(C.round(0).to_string()); print(rm.round(0).to_string())
    print(D.round(0).to_string()); print(Dsum.round(0)); print(V.round(1).to_string())


if __name__ == "__main__":
    main()
