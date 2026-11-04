import pysd,pandas as pd,numpy as np,warnings,json;warnings.filterwarnings('ignore')
res={}
for f,k in [('DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi','S1'),('DKP_25HD_A1_S2_PS_REGULER_rapi','S2'),('DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi','S3'),('DKP_25HD_A1_S4_USD10_rapi','S4USD10'),('DKP_25HD_A1_S4_USD20_rapi','S4USD20'),('DKP_25HD_A1_S4_USD35_rapi','S4USD35')]:
    m=pysd.load(f+'.py')
    for dt in [0.125,0.0625,0.03125]:
        df=m.run(time_step=dt,saveper=dt,return_columns=['Total Hutan','Deforestasi Total','Pendapatan Kotor Penjualan Kredit','Kredit REDD Diajukan','Dana Desa Diterima'],progress=False,reload=True)
        def I(c,a,b): s=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9),c]; return float(s.sum()*dt)
        r=dict(n=len(df),hutan2087=float(df['Total Hutan'].iloc[-1]),defor=I('Deforestasi Total',2025,2087),gross=I('Pendapatan Kotor Penjualan Kredit',2024,2087),kredit=I('Kredit REDD Diajukan',2024,2087),lphd=I('Dana Desa Diterima',2024,2087))
        res[f'{k}|{dt}']=r; print(k,dt,r,flush=True)
json.dump(res,open('dt.json','w'),indent=1)
