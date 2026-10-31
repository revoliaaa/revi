"""Spatial constraint on the Vensim parameter
`Proporsi Kredit REDD dalam Project Area` (current value 0.8535, a bounding
assumption).

The derivation of 0.8535 is not documented in the material available to this
workflow, so this script does NOT claim to recompute it. Instead it produces a
family of spatially explicit candidate ratios, each with its own meaning, so the
researcher can select the one that matches the model equation:

  R0  Project Area / HCV study area (tabular, geometry-free)       = area share
  R1  TC2000(>t) in Project Area / TC2000(>t) in HD-SK domain      = forest share   [needs SK geometry]
  R2  Gross loss 2001-2024 in PA / gross loss in HD-SK domain      = activity share [needs SK geometry]
  R3  Gross loss 2001-2024 in PA / gross loss in ADMIN-DESA domain = landscape context ratio
  R4  TC2000(>t) in PA / TC2000(>t) in ADMIN-DESA domain           = landscape context ratio
  NOTE: with the real Project Area geometry (v. 21-05-2026) 6.0 % (6,709 ha) of the PA lies OUTSIDE the
  25 matched desa, so R3/R4 are NOT strict bounds on R1/R2; they describe how much of the
  landscape's tree cover / loss falls inside the PA.
  R5  Gross loss 2001-2024 in PA / TC2000(>t) in PA               = cumulative PA loss fraction

Usage:
  python s07_project_area_constraint.py <pa_zonal.csv> <desa_zonal.csv> [sk_zonal.csv]
"""
import sys

import pandas as pd

from common import CANOPY_THRESHOLDS, HCV_AREA_HA, MODEL_YEARS, PDD_PROJECT_AREA_HA, ROOT, VENSIM_PROP_KREDIT_REDD


def agg(df):
    g = df.groupby("LANDSCAPE").sum(numeric_only=True)
    g.loc["ALL_25"] = g.sum()
    return g


def loss(g, t, years=MODEL_YEARS):
    return g[[f"LOSS_{y}_GT{t}" for y in years]].sum(axis=1)


def main(pa_csv, desa_csv, sk_csv=None):
    pa, de = agg(pd.read_csv(pa_csv)), agg(pd.read_csv(desa_csv))
    sk = agg(pd.read_csv(sk_csv)) if sk_csv else None
    rows = []
    for L in pa.index:
        hcv = HCV_AREA_HA["TOTAL" if L == "ALL_25" else L]
        rows.append({"GROUP": L, "RATIO": "R0 PA area / HCV area (tabular)", "THRESHOLD_PCT": None,
                     "VALUE": pa.loc[L, "POLY_GEODESIC_HA"] / hcv, "EVIDENCE": "Geometry (PA) / table (HCV)",
                     "STATUS": "COMPUTED"})
        for t in CANOPY_THRESHOLDS:
            rows.append({"GROUP": L, "RATIO": "R3 loss PA / loss desa context (context ratio, not a bound)", "THRESHOLD_PCT": t,
                         "VALUE": loss(pa, t)[L] / loss(de, t)[L], "EVIDENCE": "Hansen v1.13 overlay", "STATUS": "COMPUTED"})
            rows.append({"GROUP": L, "RATIO": "R4 TC2000 PA / TC2000 desa context (context ratio, not a bound)", "THRESHOLD_PCT": t,
                         "VALUE": pa.loc[L, f"TC2000_GT{t}_HA"] / de.loc[L, f"TC2000_GT{t}_HA"],
                         "EVIDENCE": "Hansen v1.13 overlay", "STATUS": "COMPUTED"})
            rows.append({"GROUP": L, "RATIO": "R5 cumulative gross loss 2001-2024 / TC2000 in PA", "THRESHOLD_PCT": t,
                         "VALUE": loss(pa, t)[L] / pa.loc[L, f"TC2000_GT{t}_HA"], "EVIDENCE": "Hansen v1.13 overlay",
                         "STATUS": "COMPUTED"})
            for name, num, den in [("R1 TC2000 PA / TC2000 SK", f"TC2000_GT{t}_HA", None),
                                   ("R2 loss PA / loss SK", None, None)]:
                if sk is None:
                    rows.append({"GROUP": L, "RATIO": name, "THRESHOLD_PCT": t, "VALUE": None,
                                 "EVIDENCE": "Requires HD SK boundary geometry", "STATUS": "NOT AVAILABLE"})
                else:
                    v = (pa.loc[L, num] / sk.loc[L, num]) if num else (loss(pa, t)[L] / loss(sk, t)[L])
                    rows.append({"GROUP": L, "RATIO": name, "THRESHOLD_PCT": t, "VALUE": v,
                                 "EVIDENCE": "Hansen v1.13 overlay", "STATUS": "COMPUTED"})
    out = pd.DataFrame(rows)
    out["VENSIM_CURRENT"] = VENSIM_PROP_KREDIT_REDD
    out["PDD_PROJECT_AREA_HA"] = PDD_PROJECT_AREA_HA
    out.to_excel(ROOT / "05_SYSTEM_DYNAMICS_INPUT" / "PROJECT_AREA_CREDIT_SPATIAL_CONSTRAINT_COMPUTED.xlsx", index=False)
    print(out.round(4).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:4])
