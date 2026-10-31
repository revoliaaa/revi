"""Historical tree-cover-loss trends, epoch summaries and calibration/hold-out
benchmarks from a zonal-statistics table produced by s03.

Design (mirrors the Vensim calibration protocol):
  calibration years : loss 2001-2014  (epochs 2000-2003-2009-2014)
  held-out years    : loss 2015-2024  (epochs 2014-2019-2024)
Benchmarks fitted on the calibration years only:
  B1 constant mean annual loss (ha/yr)
  B2 linear trend in annual loss (OLS, floored at 0)
  B3 constant proportional rate of remaining tree cover
     (loss_y = k * R_{y-1}, R = TC2000 - cumulative gross loss; no regrowth)
  B4 = B1 fitted on 2011-2014 only (reprocessed Hansen years; tests the 2011 break)
Metrics on held-out years: RMSE, MAE, bias of annual loss, and error in the
'remaining tree cover' indicator at 2019 and 2024.

R_t is a DERIVED INDICATOR (2000 tree cover net of gross loss, regrowth ignored).
It is NOT a forest-area map and must not be presented as forest area.

Usage: python -I s05_trends_benchmarks.py <zonal_wide.csv> <out_prefix>
"""
import sys

import numpy as np
import pandas as pd

from common import CANOPY_THRESHOLDS, EPOCHS, MODEL_YEARS

CAL = list(range(2001, 2015))
HOLD = list(range(2015, 2025))


def series(df, t):
    cols = [f"LOSS_{y}_GT{t}" for y in MODEL_YEARS]
    s = df[cols].sum()
    s.index = MODEL_YEARS
    return s, df[f"TC2000_GT{t}_HA"].sum()


def remaining(tc0, loss):
    return tc0 - loss.cumsum()


def bench(loss, tc0):
    cal = loss.loc[CAL]
    out = {}
    out["B1_CONST_MEAN_2001_2014"] = pd.Series(cal.mean(), index=HOLD)
    b, a = np.polyfit(CAL, cal.values, 1)
    out["B2_LINEAR_TREND_2001_2014"] = pd.Series(np.maximum(a + b * np.array(HOLD), 0), index=HOLD)
    R = remaining(tc0, loss)
    Rprev = R.shift(1).fillna(tc0)
    k = (cal / Rprev.loc[CAL]).mean()
    # forecast recursively from the 2014 stock (no peeking at held-out losses)
    r, pred = R.loc[2014], []
    for _ in HOLD:
        l = k * r
        pred.append(l)
        r -= l
    out["B3_CONST_PROPORTIONAL_2001_2014"] = pd.Series(pred, index=HOLD)
    out["B4_CONST_MEAN_2011_2014_REPROCESSED"] = pd.Series(loss.loc[2011:2014].mean(), index=HOLD)
    params = {"B1_mean_ha_yr": cal.mean(), "B2_intercept": a, "B2_slope_ha_yr2": b, "B3_k_per_yr": k,
              "B4_mean_ha_yr": loss.loc[2011:2014].mean()}
    return out, params


def metrics(obs, pred, tc0, loss):
    e = pred - obs
    R_obs = remaining(tc0, loss)
    R_pred = R_obs.loc[2014] - pred.cumsum()
    return {"RMSE_annual_ha": float(np.sqrt((e ** 2).mean())), "MAE_annual_ha": float(e.abs().mean()),
            "BIAS_annual_ha": float(e.mean()),
            "PRED_CUM_LOSS_2015_2024_ha": float(pred.sum()), "OBS_CUM_LOSS_2015_2024_ha": float(obs.sum()),
            "REL_DIFF_CUM_pct": float(100 * (pred.sum() - obs.sum()) / obs.sum()),
            "R2019_ERR_ha": float(R_pred.loc[2019] - R_obs.loc[2019]),
            "R2024_ERR_ha": float(R_pred.loc[2024] - R_obs.loc[2024])}


def main(csv, prefix):
    w = pd.read_csv(csv)
    domain = w.SPATIAL_DOMAIN.iloc[0]
    groups = {lv: g for lv, g in w.groupby("LANDSCAPE")}
    groups["ALL_25"] = w
    annual, epochs, bm, pars = [], [], [], []
    for gname, g in groups.items():
        for t in CANOPY_THRESHOLDS:
            loss, tc0 = series(g, t)
            R = remaining(tc0, loss)
            for y in MODEL_YEARS:
                annual.append({"SPATIAL_DOMAIN": domain, "GROUP": gname, "THRESHOLD_PCT": t, "YEAR": y,
                               "TC2000_HA": tc0, "GROSS_LOSS_HA": loss[y],
                               "LOSS_PCT_OF_TC2000": 100 * loss[y] / tc0,
                               "LOSS_PCT_OF_REMAINING_PREV": 100 * loss[y] / (R.get(y - 1, tc0)),
                               "TC2000_NET_OF_GROSS_LOSS_HA (derived, not forest area)": R[y],
                               "HANSEN_METHOD_PERIOD": "2001-2010 original" if y < 2011 else "2011+ reprocessed"})
            for a, b in zip(EPOCHS[:-1], EPOCHS[1:]):
                l = loss.loc[a + 1:b].sum()
                epochs.append({"SPATIAL_DOMAIN": domain, "GROUP": gname, "THRESHOLD_PCT": t,
                               "INTERVAL": f"{a}-{b}", "YEARS": b - a, "GROSS_LOSS_HA": l,
                               "MEAN_ANNUAL_LOSS_HA_YR": l / (b - a),
                               "MEAN_ANNUAL_PCT_OF_TC2000": 100 * l / (b - a) / tc0,
                               "TC_NET_OF_LOSS_AT_END_HA (derived)": R[b] if b in R.index else np.nan,
                               "ROLE": "CALIBRATION" if b <= 2014 else "HELD_OUT",
                               "STRADDLES_2011_BREAK": a < 2011 <= b})
            preds, p = bench(loss, tc0)
            pars.append({"SPATIAL_DOMAIN": domain, "GROUP": gname, "THRESHOLD_PCT": t, "TC2000_HA": tc0, **p,
                         "MEAN_2001_2010_ha_yr": loss.loc[2001:2010].mean(),
                         "MEAN_2011_2014_ha_yr": loss.loc[2011:2014].mean(),
                         "MEAN_2015_2019_ha_yr": loss.loc[2015:2019].mean(),
                         "MEAN_2017_2024_ha_yr": loss.loc[2017:2024].mean(),
                         "MEAN_2020_2024_ha_yr": loss.loc[2020:2024].mean()})
            for name, pr in preds.items():
                bm.append({"SPATIAL_DOMAIN": domain, "GROUP": gname, "THRESHOLD_PCT": t, "BENCHMARK": name,
                           **metrics(loss.loc[HOLD], pr, tc0, loss)})
    pd.DataFrame(annual).to_csv(prefix + "_ANNUAL.csv", index=False)
    pd.DataFrame(epochs).to_csv(prefix + "_EPOCHS.csv", index=False)
    pd.DataFrame(bm).to_csv(prefix + "_BENCHMARKS.csv", index=False)
    pd.DataFrame(pars).to_csv(prefix + "_PARAMS.csv", index=False)
    print(pd.DataFrame(bm).query("THRESHOLD_PCT==30").round(0).to_string())
    print(pd.DataFrame(pars).query("THRESHOLD_PCT==30").round(4).T.to_string())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
