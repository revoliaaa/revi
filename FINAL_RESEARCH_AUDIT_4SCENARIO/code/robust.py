import pysd,pandas as pd,numpy as np,warnings,json;warnings.filterwarnings('ignore')
DT=0.0625; ts=list(np.arange(2024,2087+1e-9,DT))
files={'S1':'DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi','S2':'DKP_25HD_A1_S2_PS_REGULER_rapi','S3':'DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi','S4USD10':'DKP_25HD_A1_S4_USD10_rapi','S4USD20':'DKP_25HD_A1_S4_USD20_rapi'}
models={k:pysd.load(v+'.py') for k,v in files.items()}
cols=['Deforestasi Total','Pendapatan Kotor Penjualan Kredit','Biaya Transaksi dan MRV','Realisasi Pembiayaan Awal','Penggunaan Dana Pengelolaan','Kebutuhan Dana Minimum','Kesenjangan Pembiayaan Minimum','Kredit REDD Diajukan','Pendapatan Bersih per RT Bergantung']
variants={'BASE':{},
 'Efektivitas=0.20':{'Efektivitas Perlindungan Penuh terhadap Deforestasi':0.20},
 'Efektivitas=0.50':{'Efektivitas Perlindungan Penuh terhadap Deforestasi':0.50},
 'MRV/ha x2 (3960)':{'Biaya Monitoring per Ha per Tahun':3960},
 'Verifikasi x2 (1,485e9)':{'Biaya Verifikasi per Kejadian':1.485e9},
 'Delay penerbitan=5':{'Delay Verifikasi dan Penerbitan Kredit':5},
 'Proporsi PA=0.5':{'Proporsi Kredit REDD dalam Project Area':0.5},
 'Buffer=0.20':{'Proporsi Buffer Risiko Karbon':0.20},
 'Leakage=0.20':{'Proporsi Leakage Karbon':0.20},
 'Diskonto 6%':{},'Diskonto 15%':{},
 'Kapasitas realisasi penuh=1.0':{'Indeks Kapasitas untuk Realisasi Penuh':1.0},
}
res=[]
for vn,par in variants.items():
    r={'variant':vn}; R={}
    for k,m in models.items():
        df=m.run(params=par,return_timestamps=ts,return_columns=cols,progress=False,reload=True)
        s=df.loc[df.index<2087-1e-9]
        rate=0.10 if 'Diskonto' not in vn else (0.06 if '6%' in vn else 0.15)
        d=(1+rate)**(-(s.index.values-2024)); pv=lambda c:float((s[c].values*d).sum()*DT)
        defor=float(df.loc[(df.index>=2025-1e-9)&(df.index<2087-1e-9),'Deforestasi Total'].sum()*DT)
        w=df.loc[(df.index>=2030)&(df.index<2056)]
        R[k]=dict(defor=defor,npv=pv('Pendapatan Kotor Penjualan Kredit')-pv('Biaya Transaksi dan MRV')-pv('Realisasi Pembiayaan Awal')-pv('Penggunaan Dana Pengelolaan'),
                  cov=float(w['Penggunaan Dana Pengelolaan'].mean()/max(w['Kebutuhan Dana Minimum'].mean(),1)),kredit=float(s['Kredit REDD Diajukan'].sum()*DT),rt=float(w['Pendapatan Bersih per RT Bergantung'].mean()))
    r.update({'S2-S1 ha':R['S1']['defor']-R['S2']['defor'],'S3-S2 ha':R['S2']['defor']-R['S3']['defor'],'S4-S3 USD10 ha':R['S3']['defor']-R['S4USD10']['defor'],'S4-S3 USD20 ha':R['S3']['defor']-R['S4USD20']['defor'],
      'NPV USD10 (Rp M)':R['S4USD10']['npv']/1e9,'NPV USD20 (Rp M)':R['S4USD20']['npv']/1e9,'Cakupan USD20 (%)':100*R['S4USD20']['cov'],'Kredit USD10 (ribu)':R['S4USD10']['kredit']/1e3,'dRT S4-S3 USD10 (Rp)':R['S4USD10']['rt']-R['S3']['rt'],'dRT S4-S3 USD20 (Rp)':R['S4USD20']['rt']-R['S3']['rt']})
    res.append(r); print(r,flush=True)
pd.DataFrame(res).to_csv('robustness_oat.csv',index=False)
