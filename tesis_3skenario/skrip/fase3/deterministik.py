import sys, json, pickle; sys.path.insert(0, "fase3"); from common import *
SC = {"S1": {"Skenario Kebijakan": 1}}
for h in [6, 10, 15, 20, 35]: SC[f"S2 USD{h}"] = {"Skenario Kebijakan": 2, "Harga Karbon": h}
runs = {k: run(p) for k, p in SC.items()}
res = {k: summary(d) for k, d in runs.items()}
pickle.dump(runs, open("fase3/det_runs.pkl", "wb")); json.dump(res, open("fase3/det_summary.json", "w"), indent=1)
df = pd.DataFrame(res); pd.set_option("display.width", 250)
print(df.map(lambda x: f"{x:,.4g}" if isinstance(x, float) else x).to_string())
