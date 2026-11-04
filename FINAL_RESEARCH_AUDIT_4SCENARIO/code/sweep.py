import pysd,pandas as pd,numpy as np,warnings,sys;warnings.filterwarnings('ignore')
DT=0.0625
m=pysd.load('DKP_25HD_A1_S4_USD10_rapi.py')
ts=list(np.arange(2024,2087+1e-9,DT))
cols=['Pendapatan Kotor Penjualan Kredit','Biaya Transaksi dan MRV','Realisasi Pembiayaan Awal','Penggunaan Dana Pengelolaan','Dana Mitra dari Karbon','Kekurangan Biaya Bersama Ditanggung Mitra','Pemulihan Defisit Biaya Bersama','Pemulihan Pendanaan Awal','Kebutuhan Dana Minimum','Kesenjangan Pembiayaan Minimum','Dana Desa Diterima','Pendanaan Awal Belum Terpulihkan','Defisit Biaya Bersama Belum Dipulihkan']
rows=[]
prices=[float(x) for x in sys.argv[1:]]
for p in prices:
    m.reload() if hasattr(m,'reload') else None
    df=m.run(params={'Harga Karbon':p},return_timestamps=ts,return_columns=cols,progress=False)
    s=df.loc[df.index<2087-1e-9]; d=1.1**(-(s.index.values-2024))
    pv=lambda c:(s[c].values*d).sum()*DT
    npv=pv('Pendapatan Kotor Penjualan Kredit')-pv('Biaya Transaksi dan MRV')-pv('Realisasi Pembiayaan Awal')-pv('Penggunaan Dana Pengelolaan')
    w=df.loc[(df.index>=2030)&(df.index<2056)]
    cov=w['Penggunaan Dana Pengelolaan'].mean()/w['Kebutuhan Dana Minimum'].mean()
    cov2=1-w['Kesenjangan Pembiayaan Minimum'].mean()/w['Kebutuhan Dana Minimum'].mean()
    p1=pv('Dana Mitra dari Karbon')-pv('Kekurangan Biaya Bersama Ditanggung Mitra')-pv('Realisasi Pembiayaan Awal')
    p2=p1+pv('Pemulihan Defisit Biaya Bersama')
    p3=pv('Dana Mitra dari Karbon')+pv('Pemulihan Defisit Biaya Bersama')-pv('Kekurangan Biaya Bersama Ditanggung Mitra')-pv('Realisasi Pembiayaan Awal')-0
    rows.append(dict(price=p,npv=npv/1e9,cov_use=cov*100,cov_gap=cov2*100,partner1=p1/1e9,partner2=p2/1e9))
print(pd.DataFrame(rows).to_string())
