import pysd, numpy as np, pandas as pd, openpyxl, json, warnings
warnings.filterwarnings("ignore")
DT = 0.0625
def load(mdl):
    return pysd.read_vensim(mdl)
def run(model, params, vars_=None):
    model.reload()
    ts = np.round(np.arange(2024, 2087 + DT/2, DT), 6)
    df = model.run(params=params, return_timestamps=ts, return_columns=vars_, progress=False)
    return df
def yearly(df):
    """stok = nilai awal tahun; aliran/aux = rerata langkah DT dalam [t,t+1)"""
    yr = np.floor(df.index.values + 1e-9).astype(int)
    avg = df.groupby(yr).mean()
    first = df.groupby(yr).first()
    return avg, first
def summaries(df, kinds):
    avg, first = yearly(df)
    out = {}
    for v in df.columns:
        k = kinds.get(v, "")
        s = first[v] if k == "Stok" else avg[v]
        out[v] = {"2030": s.get(2030), "2050": s.get(2050),
                  "2087": df[v].iloc[-1] if k != "Stok" else df[v].iloc[-1],
                  "avg": s.loc[2030:2055].mean(), "cum": avg[v].loc[2025:2086].sum()}
    return out
