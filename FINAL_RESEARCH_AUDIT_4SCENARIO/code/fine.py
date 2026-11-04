import pysd,pandas as pd,numpy as np,warnings;warnings.filterwarnings('ignore')
runs={'S1':'DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi','S2':'DKP_25HD_A1_S2_PS_REGULER_rapi','S3':'DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi','S4USD10':'DKP_25HD_A1_S4_USD10_rapi','S4USD20':'DKP_25HD_A1_S4_USD20_rapi'}
for k,f in runs.items():
    m=pysd.load(f+'.py')
    ts=list(np.arange(2024,2087+1e-9,0.0625))
    df=m.run(return_timestamps=ts,progress=False,return_columns=['Total Hutan','Deforestasi Total','HLKS menjadi NonHutan','HLKS menjadi Pr','HMS menjadi NonHutan','HRS menjadi NonHutan','HRS menjadi Pr','NonHutan menjadi HMS','NonHutan menjadi HRS','NonHutan menjadi HLKS','Rehabilitasi ke HMS','Rehabilitasi ke HRS','Rehabilitasi ke HLKS','Total Hutan Baseline','Deforestasi Total Baseline','Emisi Deforestasi Biomassa','Emisi Deforestasi Biomassa Baseline','Kredit REDD Diajukan','Pengurangan Emisi REDD Bruto','Total Emisi Bersih'])
    df.to_pickle(f'{k}_fine.pkl')
    dt=0.0625
    # Euler: stock(t+dt)=stock(t)+dt*flow(t); integral 2024->2087 = sum flow at t in [2024,2087)
    f2=df.loc[df.index<2087-1e-9]
    inflow=f2[['NonHutan menjadi HMS','NonHutan menjadi HRS','NonHutan menjadi HLKS','Rehabilitasi ke HMS','Rehabilitasi ke HRS','Rehabilitasi ke HLKS']].sum(axis=1).sum()*dt
    out=f2['Deforestasi Total'].sum()*dt
    TH0,TH1=df['Total Hutan'].iloc[0],df['Total Hutan'].iloc[-1]
    ann=df.loc[[float(y) for y in range(2025,2087)],'Deforestasi Total'].sum()
    regen=f2[['NonHutan menjadi HMS','NonHutan menjadi HRS','NonHutan menjadi HLKS']].sum(axis=1).sum()*dt
    rehab=f2[['Rehabilitasi ke HMS','Rehabilitasi ke HRS','Rehabilitasi ke HLKS']].sum(axis=1).sum()*dt
    print(k,'H2024=%.3f H2087=%.3f  int_defor=%.3f int_regen=%.3f int_rehab=%.3f  residual=%.6f  annual_sum_2025_2086=%.3f  diff=%.3f'%(TH0,TH1,out,regen,rehab,TH1-TH0-(inflow-out),ann,out-ann))
