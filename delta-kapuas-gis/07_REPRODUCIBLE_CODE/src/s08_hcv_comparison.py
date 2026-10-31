"""Compare HCV historical tabulations with independent satellite products.

Different variables are NEVER compared as if identical. The script reports
logical-consistency tests instead:

  T1 (mangrove bound)  HCV mangrove area in the HCV study area must be <= GMW
       mangrove mapped in the (larger) admin-desa domain + 1 km coastal buffer
       for the nearest GMW year, if both maps describe the same thing.
  T2 (gain plausibility) HCV net forest INCREASE between epochs is flagged when
       independent products show no corresponding expansion (GMW stable) or show
       gross loss in the same interval.
  T3 (direction/timing) Sign and relative timing of HCV net forest decrease vs
       Hansen gross loss per interval (requires the full HCV series).

  T1b (Project Area bound) Under assumption A1 (Project Area is contained in the HCV study
       area of the same landscape; plausible because PA/HCV area = 0.87-0.95 but NOT verified
       without HD SK geometry): HCV mangrove <= GMW mangrove inside the PA + (HCV area - PA area),
       i.e. even if every hectare of HCV area outside the PA were mangrove.

Usage: python -I s08_hcv_comparison.py <hcv_table.csv> <desa_zonal.csv> <gmw_buffer_1km_ha.json> [pa_zonal.csv]
"""
import json
import sys

import pandas as pd

from common import EPOCHS, GMW_YEARS, HCV_AREA_HA, ROOT


def nearest_gmw(y):
    return min(GMW_YEARS, key=lambda g: (abs(g - y), -g))


def main(hcv_csv, desa_csv, buf_json, pa_csv=None):
    hcv = pd.read_csv(hcv_csv)
    z = pd.read_csv(desa_csv).groupby("LANDSCAPE").sum(numeric_only=True)
    buf = json.loads(open(buf_json).read())       # {"Pulau Maya": {"2019": ha_outside_desa_within_1km, ...}}
    rows = []
    hcv = hcv[hcv.YEAR.astype(str) != "ALL"].copy()
    hcv["YEAR"] = hcv.YEAR.astype(int)
    mg = (hcv[hcv.FOREST_TYPE == "MANGROVE"].groupby(["LANDSCAPE", "YEAR"], as_index=False)
          .agg(AREA_HA=("AREA_HA", "sum"), VERIFIED=("VERIFIED", "first")))
    for r in mg.itertuples():
        y = int(r.YEAR)
        gy = nearest_gmw(y)
        gm = z.loc[r.LANDSCAPE, f"MANGROVE_GMW_{gy}_HA"] + buf.get(r.LANDSCAPE, {}).get(str(gy), 0.0)
        rows.append({"TEST": "T1 mangrove upper bound", "LANDSCAPE": r.LANDSCAPE, "HCV_YEAR": y,
                     "HCV_MANGROVE_HA": r.AREA_HA, "GMW_YEAR_USED": gy,
                     "GMW_MANGROVE_DESA_PLUS_1KM_HA": round(gm, 1),
                     "HCV_MINUS_BOUND_HA": round(r.AREA_HA - gm, 1),
                     "RESULT": "CONSISTENT" if r.AREA_HA <= gm else "EXCEEDS_INDEPENDENT_BOUND",
                     "TEMPORAL_GAP_YR": y - gy, "HCV_VERIFIED": r.VERIFIED})
    if pa_csv:
        pz = pd.read_csv(pa_csv).groupby("LANDSCAPE").sum(numeric_only=True)
        for r in mg.itertuples():
            y = int(r.YEAR); gy = nearest_gmw(y)
            hcv_area = float(HCV_AREA_HA[r.LANDSCAPE])
            slack = max(hcv_area - pz.loc[r.LANDSCAPE, "POLY_GEODESIC_HA"], 0.0)
            gm = pz.loc[r.LANDSCAPE, f"MANGROVE_GMW_{gy}_HA"]
            rows.append({"TEST": "T1b mangrove bound via Project Area (assumption A1)", "LANDSCAPE": r.LANDSCAPE,
                         "HCV_YEAR": y, "HCV_MANGROVE_HA": r.AREA_HA, "GMW_YEAR_USED": gy,
                         "GMW_MANGROVE_IN_PA_HA": round(gm, 1), "HCV_AREA_OUTSIDE_PA_HA": round(slack, 1),
                         "BOUND_HA": round(gm + slack, 1), "HCV_MINUS_BOUND_HA": round(r.AREA_HA - gm - slack, 1),
                         "RESULT": "CONSISTENT" if r.AREA_HA <= gm + slack else "EXCEEDS_INDEPENDENT_BOUND",
                         "TEMPORAL_GAP_YR": y - gy, "HCV_VERIFIED": r.VERIFIED})
    # T2 mangrove change between HCV epochs vs GMW change over overlapping years
    for L, g in mg.groupby("LANDSCAPE"):
        g = g.assign(Y=g.YEAR.astype(int)).sort_values("Y")
        for a, b in zip(g.itertuples(), list(g.itertuples())[1:]):
            ga, gb = nearest_gmw(a.Y), nearest_gmw(b.Y)
            gmw_change = z.loc[L, f"MANGROVE_GMW_{gb}_HA"] - z.loc[L, f"MANGROVE_GMW_{ga}_HA"]
            loss_m = sum(z.loc[L, f"LOSS_{y}_GT30_IN_GMW2010"] for y in range(a.Y + 1, b.Y + 1))
            rows.append({"TEST": "T2 mangrove change plausibility", "LANDSCAPE": L, "HCV_YEAR": f"{a.Y}-{b.Y}",
                         "HCV_MANGROVE_CHANGE_HA": b.AREA_HA - a.AREA_HA,
                         "HCV_MANGROVE_CHANGE_PCT_PER_YR": 100 * (b.AREA_HA - a.AREA_HA) / a.AREA_HA / (b.Y - a.Y),
                         "GMW_YEARS_USED": f"{ga}-{gb}", "GMW_CHANGE_DESA_HA": round(gmw_change, 1),
                         "HANSEN_LOSS_IN_GMW2010_GT30_HA": round(loss_m, 1),
                         "RESULT": "HCV GAIN NOT CORROBORATED BY GMW (GMW ends 2020; see Landsat test)"
                         if (b.AREA_HA - a.AREA_HA) > 0 and abs(gmw_change) < 0.05 * abs(b.AREA_HA - a.AREA_HA)
                         else "SEE NOTES", "HCV_VERIFIED": b.VERIFIED})
    # T3 requires full series
    forest = hcv[hcv.IS_FOREST == 1]
    have = forest.groupby("LANDSCAPE").YEAR.nunique()
    for L in ["Kubu", "Padang Tikar", "Pulau Maya"]:
        n = int(have.get(L, 0))
        if n < len(EPOCHS):
            rows.append({"TEST": "T3 HCV forest trend vs Hansen gross loss", "LANDSCAPE": L,
                         "RESULT": f"NOT AVAILABLE - HCV forest series has {n}/{len(EPOCHS)} epochs in the input table"})
        else:
            rows.append({"TEST": "T3 HCV forest trend vs Hansen gross loss", "LANDSCAPE": L,
                         "RESULT": "DONE in s14_hcv_vs_satellite.py -> HCV_T3_INTERVALS.csv / HCV_HARMONISED_SERIES.csv"})
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "04_VALIDATION" / "HCV_VS_SATELLITE_TESTS.csv", index=False)
    print(out.T.to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
