import pysd,pandas as pd,numpy as np,warnings,json;warnings.filterwarnings('ignore')
def integ(df,col,a,b,dt):
    s=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9),col]; return float(s.sum()*dt)
out={}
# 1. DT test
for f,k in [('DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi','S1'),('DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi','S3'),('DKP_25HD_A1_S4_USD10_rapi','S4USD10'),('DKP_25HD_A1_S4_USD20_rapi','S4USD20')]:
    m=pysd.load(f+'.py')
    for dt in [0.125,0.0625,0.03125]:
        ts=list(np.arange(2024,2087+1e-9,dt))
        df=m.run(params={'TIME STEP':dt,'SAVEPER':dt},return_timestamps=ts,return_columns=['Total Hutan','Deforestasi Total','Pendapatan Kotor Penjualan Kredit','Kredit REDD Diajukan'],progress=False)
        out[f'DT|{k}|{dt}']=dict(hutan2087=float(df['Total Hutan'].iloc[-1]),defor=integ(df,'Deforestasi Total',2025,2087,dt),gross=integ(df,'Pendapatan Kotor Penjualan Kredit',2024,2087,dt),kredit=integ(df,'Kredit REDD Diajukan',2024,2087,dt))
        print('DT',k,dt,out[f'DT|{k}|{dt}'],flush=True)
dt=0.0625; ts=list(np.arange(2024,2087+1e-9,dt))
# 2. loop-break: carbon funds cannot buy patrol (override Realisasi Belanja Perlindungan = 0)
for f,k in [('DKP_25HD_A1_S4_USD10_rapi','S4USD10'),('DKP_25HD_A1_S4_USD20_rapi','S4USD20'),('DKP_25HD_A1_S4_USD35_rapi','S4USD35')]:
    m=pysd.load(f+'.py')
    for lab,params in [('Realisasi Belanja Perlindungan=0',{'Realisasi Belanja Perlindungan':0}),('Hari Patroli Didanai=0',{'Hari Patroli Didanai':0})]:
        df=m.run(params=params,return_timestamps=ts,return_columns=['Deforestasi Total','Total Hutan','Pendapatan Kotor Penjualan Kredit'],progress=False)
        out[f'LOOP|{k}|{lab}']=dict(defor=integ(df,'Deforestasi Total',2025,2087,dt),gross=integ(df,'Pendapatan Kotor Penjualan Kredit',2024,2087,dt))
        print('LOOP',k,lab,out[f'LOOP|{k}|{lab}'],flush=True)
# 3. A2 diagnostic: Switch Baseline Kredit Konservatif=1
for f,k in [('DKP_25HD_A1_S4_USD6_rapi','S4USD6'),('DKP_25HD_A1_S4_USD10_rapi','S4USD10'),('DKP_25HD_A1_S4_USD15_rapi','S4USD15'),('DKP_25HD_A1_S4_USD20_rapi','S4USD20'),('DKP_25HD_A1_S4_USD35_rapi','S4USD35')]:
    m=pysd.load(f+'.py')
    cols=['Deforestasi Total','Total Hutan','Kredit REDD Diajukan','Pendapatan Kotor Penjualan Kredit','Biaya Transaksi dan MRV','Dana Desa Diterima','Realisasi Pembiayaan Awal','Penggunaan Dana Pengelolaan','Kebutuhan Dana Minimum','Total Emisi Bersih']
    df=m.run(params={'Switch Baseline Kredit Konservatif':1},return_timestamps=ts,return_columns=cols,progress=False)
    s=df.loc[df.index<2087-1e-9]; d=1.1**(-(s.index.values-2024)); pv=lambda c:float((s[c].values*d).sum()*dt)
    w=df.loc[(df.index>=2030)&(df.index<2056)]
    out[f'A2|{k}']=dict(defor=integ(df,'Deforestasi Total',2025,2087,dt),hutan2087=float(df['Total Hutan'].iloc[-1]),kredit=integ(df,'Kredit REDD Diajukan',2024,2087,dt),gross=integ(df,'Pendapatan Kotor Penjualan Kredit',2024,2087,dt),biaya=integ(df,'Biaya Transaksi dan MRV',2024,2087,dt),danaLPHD=integ(df,'Dana Desa Diterima',2024,2087,dt),
        npv=pv('Pendapatan Kotor Penjualan Kredit')-pv('Biaya Transaksi dan MRV')-pv('Realisasi Pembiayaan Awal')-pv('Penggunaan Dana Pengelolaan'),cov=float(w['Penggunaan Dana Pengelolaan'].mean()/w['Kebutuhan Dana Minimum'].mean()),emis=integ(df,'Total Emisi Bersih',2025,2087,dt))
    print('A2',k,out[f'A2|{k}'],flush=True)
# 4. access multiplier sweep (S3 and S4)
for f,k in [('DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi','S3'),('DKP_25HD_A1_S4_USD10_rapi','S4USD10'),('DKP_25HD_A1_S4_USD20_rapi','S4USD20'),('DKP_25HD_A1_S2_PS_REGULER_rapi','S2')]:
    m=pysd.load(f+'.py')
    for mult in [0,0.25,0.5,0.75,1,2,3.24]:
        df=m.run(params={'Pengali Kehilangan Akses':mult},return_timestamps=ts,return_columns=['Pendapatan Bersih per RT Bergantung','Deforestasi Total'],progress=False)
        out[f'ACC|{k}|{mult}']=dict(rt=integ(df,'Pendapatan Bersih per RT Bergantung',2030,2056,dt)/26,defor=integ(df,'Deforestasi Total',2025,2087,dt))
        print('ACC',k,mult,out[f'ACC|{k}|{mult}'],flush=True)
json.dump(out,open('diag.json','w'),indent=1)
