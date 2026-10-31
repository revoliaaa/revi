"""HCV vs satellite on the SAME domain (SK geometry): no assumption A1, no area scaling.

  A  Mangrove: HCV mangrove classes vs GMW v3 mangrove inside the SK polygons (nearest GMW year).
  B  Harmonised series on SK: S_SK(t) = F_HCV(2000) - cumulative Hansen gross loss inside SK (k = 1).
     D(t) = F_HCV(t) - S_SK(t); RMSE over 2003-2024 and hold-out 2019/2024; epoch reliability.
  C  Definition conversion at the anchor epoch 2000: HCV natural forest 2000 / Hansen tree cover 2000 (SK).
  D  Activity and tree-cover shares PA/SK by period, landscape and HD.
Usage: python s19_sk_domain_tests.py
"""
import numpy as np
import pandas as pd

from common import CODE, ROOT

EP = [2000, 2003, 2009, 2014, 2019, 2024]
GMW_NEAR = {2000: 1996, 2003: 2007, 2009: 2010, 2014: 2015, 2019: 2019, 2024: 2020}
LANDS = ["Kubu", "Padang Tikar", "Pulau Maya"]
VA = ROOT / "04_VALIDATION"


def main():
    sk = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "ZONAL_SK_HD.csv")
    pa = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "ZONAL_PROJECT_AREA.csv")
    hcv = pd.read_csv(CODE / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv")
    S = sk.groupby("LANDSCAPE").sum(numeric_only=True); S.loc["ALL_25"] = S.sum()
    P = pa.groupby("LANDSCAPE").sum(numeric_only=True); P.loc["ALL_25"] = P.sum()
    F = hcv[hcv.IS_FOREST == 1].pivot_table(index="LANDSCAPE", columns="YEAR", values="AREA_HA", aggfunc="sum")
    F.loc["ALL_25"] = F.sum()
    Mh = hcv[hcv.FOREST_TYPE == "MANGROVE"].pivot_table(index="LANDSCAPE", columns="YEAR", values="AREA_HA", aggfunc="sum")
    Mh.loc["ALL_25"] = Mh.sum()
    cum = lambda D, g, y: sum(D.loc[g, f"LOSS_{yy}_GT30"] for yy in range(2001, y + 1))

    A, B, C, V = [], [], [], []
    for g in LANDS + ["ALL_25"]:
        for y in EP:
            gm = S.loc[g, f"MANGROVE_GMW_{GMW_NEAR[y]}_HA"]
            A.append({"GROUP": g, "HCV_YEAR": y, "HCV_MANGROVE_HA": Mh.loc[g, y], "GMW_YEAR": GMW_NEAR[y],
                      "GMW_MANGROVE_IN_SK_HA": gm, "HCV_MINUS_GMW_HA": Mh.loc[g, y] - gm,
                      "HCV_OVER_GMW": Mh.loc[g, y] / gm if gm else np.nan})
            s = F.loc[g, 2000] - cum(S, g, y)
            B.append({"GROUP": g, "YEAR": y, "HCV_NATURAL_FOREST_HA": F.loc[g, y],
                      "CUM_GROSS_LOSS_SK_HA": cum(S, g, y), "S_SK_HARMONISED_HA": s, "D_HA": F.loc[g, y] - s,
                      "D_PCT_OF_HCV": 100 * (F.loc[g, y] - s) / F.loc[g, y], "ROLE": "CALIBRATION" if y <= 2014 else "HELD_OUT"})
        C.append({"GROUP": g, "HCV_NATURAL_FOREST_2000_HA": F.loc[g, 2000], "HANSEN_TC2000_GT30_SK_HA": S.loc[g, "TC2000_GT30_HA"],
                  "HANSEN_TC2000_GT10_SK_HA": S.loc[g, "TC2000_GT10_HA"], "HANSEN_TC2000_GT50_SK_HA": S.loc[g, "TC2000_GT50_HA"],
                  "FOREST_TO_TREECOVER_RATIO_2000_GT30": F.loc[g, 2000] / S.loc[g, "TC2000_GT30_HA"],
                  "SK_GEOM_HA": S.loc[g, "POLY_GEODESIC_HA"],
                  "NOTE": "Konversi definisi tutupan pohon (Hansen) -> hutan alam (HCV) pada epoch jangkar 2000"})
    A, B, C = pd.DataFrame(A), pd.DataFrame(B), pd.DataFrame(C)
    rm = B[B.YEAR > 2000].groupby("GROUP").apply(lambda d: pd.Series({
        "RMSE_2003_2024_HA": np.sqrt((d.D_HA ** 2).mean()),
        "RMSE_CAL_2003_2014_HA": np.sqrt((d[d.YEAR <= 2014].D_HA ** 2).mean()),
        "RMSE_HOLDOUT_2019_2024_HA": np.sqrt((d[d.YEAR >= 2019].D_HA ** 2).mean())}), include_groups=False).reset_index()
    for g in LANDS:
        for y in EP[1:]:
            b = B[(B.GROUP == g) & (B.YEAR == y)].iloc[0]
            a = A[(A.GROUP == g) & (A.HCV_YEAR == y)].iloc[0]
            mflag = a.HCV_OVER_GMW > 1.15 or a.HCV_OVER_GMW < 0.85
            pct = abs(b.D_PCT_OF_HCV)
            V.append({"LANDSCAPE": g, "EPOCH": y, "ABS_D_PCT": pct, "HCV_OVER_GMW_MANGROVE": a.HCV_OVER_GMW,
                      "MANGROVE_OUTSIDE_15PCT": mflag,
                      "USE_CLASS": "TIDAK_DAPAT_DIGUNAKAN" if pct > 10 else ("SENSITIVITAS_SAJA" if (pct > 5 or mflag) else "LANGSUNG")})
    V = pd.DataFrame(V)
    rank = {"LANGSUNG": 0, "SENSITIVITAS_SAJA": 1, "TIDAK_DAPAT_DIGUNAKAN": 2}
    for y in EP[1:]:
        w = V[V.EPOCH == y].USE_CLASS.map(rank).max()
        V.loc[len(V)] = {"LANDSCAPE": "ALL_25", "EPOCH": y, "USE_CLASS": {v: k for k, v in rank.items()}[w],
                         "ABS_D_PCT": abs(B[(B.GROUP == "ALL_25") & (B.YEAR == y)].D_PCT_OF_HCV.iloc[0])}
    # D: shares
    D = []
    periods = {"2001-2014": (2001, 2014), "2015-2024": (2015, 2024), "2017-2024": (2017, 2024), "2001-2024": (2001, 2024)}
    for g in LANDS + ["ALL_25"]:
        for p, (a, b) in periods.items():
            lp = sum(P.loc[g, f"LOSS_{y}_GT30"] for y in range(a, b + 1))
            ls = sum(S.loc[g, f"LOSS_{y}_GT30"] for y in range(a, b + 1))
            D.append({"GROUP": g, "PERIOD": p, "LOSS_PA_HA": lp, "LOSS_SK_HA": ls, "R2_ACTIVITY_SHARE": lp / ls,
                      "R1_TREECOVER_SHARE": P.loc[g, "TC2000_GT30_HA"] / S.loc[g, "TC2000_GT30_HA"],
                      "R0_AREA_SHARE_GEOM": P.loc[g, "POLY_GEODESIC_HA"] / S.loc[g, "POLY_GEODESIC_HA"]})
    D = pd.DataFrame(D)
    ph = pa.set_index("HD_ID"); sh = sk.set_index("HD_ID")
    L = lambda d: d[[f"LOSS_{y}_GT30" for y in range(2001, 2025)]].sum(axis=1)
    hd = pd.DataFrame({"HD_NAME": ph.HD_NAME, "LANDSCAPE": ph.LANDSCAPE,
                       "SK_GEOM_HA": sh.POLY_GEODESIC_HA, "PA_HA": ph.POLY_GEODESIC_HA,
                       "TC2000_SK_HA": sh.TC2000_GT30_HA, "TC2000_PA_HA": ph.TC2000_GT30_HA,
                       "LOSS0124_SK_HA": L(sh), "LOSS0124_PA_HA": L(ph),
                       "MANGROVE2020_SK_HA": sh.MANGROVE_GMW_2020_HA})
    hd["R1_TREECOVER_SHARE"] = hd.TC2000_PA_HA / hd.TC2000_SK_HA
    hd["R2_ACTIVITY_SHARE"] = np.where(hd.LOSS0124_SK_HA > 1, hd.LOSS0124_PA_HA / hd.LOSS0124_SK_HA, np.nan)
    hd["LOSS_OUTSIDE_PA_HA"] = hd.LOSS0124_SK_HA - hd.LOSS0124_PA_HA
    for nm, df in [("SK_MANGROVE_HCV_VS_GMW", A), ("SK_HARMONISED_SERIES", B), ("SK_HARMONISED_RMSE", rm),
                   ("SK_DEFINITION_CONVERSION_2000", C), ("SK_EPOCH_RELIABILITY", V), ("SK_SHARES_BY_PERIOD", D)]:
        df.to_csv(VA / f"{nm}.csv", index=False)
    hd.reset_index().to_csv(VA / "SK_PER_HD_SHARES.csv", index=False)
    pd.set_option("display.width", 250)
    for df in (A[A.GROUP != "ALL_25"], B, rm, C, V, D):
        print(df.round(3).to_string(), "\n")
    print(hd.round(3).to_string())


if __name__ == "__main__":
    main()
