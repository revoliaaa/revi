import pysd,pandas as pd,numpy as np,warnings;warnings.filterwarnings('ignore')
DT=0.0625; ts=list(np.arange(2024,2087+1e-9,DT))
m=pysd.load('DKP_25HD_A1_S4_USD10_rapi.py')
cols=['Kebutuhan Dana Minimum','Kebutuhan Dana Operasional LPHD','Kebutuhan Dana Perlindungan','Kebutuhan Dana Pengendalian Kebakaran','Total Kebutuhan Dana Pengelolaan',
'Penggunaan Dana Pengelolaan','Realisasi Belanja Operasional LPHD','Realisasi Belanja Perlindungan','Realisasi Belanja Pengendalian Kebakaran','Realisasi Belanja Rehabilitasi','Realisasi Belanja Penguatan Kelembagaan','Realisasi Belanja Pengembangan KUPS','Realisasi Pembiayaan Awal',
'Kesenjangan Pembiayaan Minimum','Kesenjangan Pembiayaan Pengelolaan','Dana Desa Diterima','Saldo Dana LPHD','Rasio Realisasi Belanja','Alokasi Tidak Terealisasi']
def run(p):
    df=m.run(params={'Harga Karbon':p},return_timestamps=ts,return_columns=cols,progress=False,reload=True)
    return df
def summarize(p,df,a,b,lab):
    w=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9)]
    need=w['Kebutuhan Dana Minimum'].mean()
    minspend=(w['Realisasi Belanja Operasional LPHD']+w['Realisasi Belanja Perlindungan']+w['Realisasi Belanja Pengendalian Kebakaran']+w['Realisasi Pembiayaan Awal'])
    trueGap=(w['Kebutuhan Dana Minimum']-(w['Realisasi Belanja Operasional LPHD']+w['Realisasi Belanja Perlindungan']+w['Realisasi Belanja Pengendalian Kebakaran']+w['Realisasi Pembiayaan Awal'])).clip(lower=0)
    yrs=[y for y in range(int(a),int(b))]
    def ann(series): return np.array([series.loc[(series.index>=y-1e-9)&(series.index<y+1-1e-9)].mean() for y in yrs])
    yr_need=ann(w['Kebutuhan Dana Minimum']); yr_min=ann(minspend); yr_tot=ann(w['Penggunaan Dana Pengelolaan']); yr_gap=ann(w['Kesenjangan Pembiayaan Minimum'])
    return dict(harga_USD=p,periode=lab,
      kebutuhan_minimum_Rp_th=need,
      kebutuhan_operasional=w['Kebutuhan Dana Operasional LPHD'].mean(),kebutuhan_patroli_tambahan=w['Kebutuhan Dana Perlindungan'].mean(),kebutuhan_kebakaran=w['Kebutuhan Dana Pengendalian Kebakaran'].mean(),
      kebutuhan_pengelolaan_total_6_pos=w['Total Kebutuhan Dana Pengelolaan'].mean(),
      dana_LPHD_diterima_Rp_th=w['Dana Desa Diterima'].mean(),
      belanja_total_Rp_th=w['Penggunaan Dana Pengelolaan'].mean(),
      belanja_operasional=w['Realisasi Belanja Operasional LPHD'].mean(),belanja_patroli=w['Realisasi Belanja Perlindungan'].mean(),belanja_kebakaran=w['Realisasi Belanja Pengendalian Kebakaran'].mean(),pembiayaan_awal=w['Realisasi Pembiayaan Awal'].mean(),
      belanja_rehabilitasi=w['Realisasi Belanja Rehabilitasi'].mean(),belanja_kelembagaan=w['Realisasi Belanja Penguatan Kelembagaan'].mean(),belanja_KUPS=w['Realisasi Belanja Pengembangan KUPS'].mean(),
      belanja_komponen_minimum_Rp_th=minspend.mean(),
      rasio_A_belanja_total_per_kebutuhan_minimum=w['Penggunaan Dana Pengelolaan'].mean()/need,
      rasio_B_1_minus_kesenjangan_model_per_kebutuhan=1-w['Kesenjangan Pembiayaan Minimum'].mean()/need,
      rasio_C_belanja_komponen_minimum_per_kebutuhan=minspend.mean()/need,
      cakupan_operasional=w['Realisasi Belanja Operasional LPHD'].mean()/w['Kebutuhan Dana Operasional LPHD'].mean(),
      cakupan_patroli=w['Realisasi Belanja Perlindungan'].mean()/max(w['Kebutuhan Dana Perlindungan'].mean(),1),
      cakupan_kebakaran=w['Realisasi Belanja Pengendalian Kebakaran'].mean()/w['Kebutuhan Dana Pengendalian Kebakaran'].mean(),
      kesenjangan_versi_model_Rp_th=w['Kesenjangan Pembiayaan Minimum'].mean(),
      kesenjangan_komponen_minimum_Rp_th=trueGap.mean(),
      kesenjangan_pengelolaan_6_pos_Rp_th=w['Kesenjangan Pembiayaan Pengelolaan'].mean(),
      tahun_belanja_total_ge_kebutuhan=int((yr_tot>=yr_need).sum()),tahun_kesenjangan_model_nol=int((yr_gap<1).sum()),tahun_komponen_minimum_ge_kebutuhan=int((yr_min>=yr_need*(1-1e-9)).sum()),jumlah_tahun=len(yrs),
      saldo_LPHD_akhir_periode=float(df.loc[df.index<=b,'Saldo Dana LPHD'].iloc[-1]),
      rasio_realisasi_belanja_rerata=w['Rasio Realisasi Belanja'].mean())
rows=[]
cache={}
for p in [3,6,10,15,20,25,28,28.04,30,35,40,50,75,100]:
    df=run(p); cache[p]=df
    rows.append(summarize(p,df,2030,2056,'rerata 2030–2055'))
    rows.append(summarize(p,df,2024,2087,'rerata 2024–2086'))
    print(p,flush=True)
D=pd.DataFrame(rows); D.to_csv('lphd_sweep.csv',index=False)
# threshold search for rasio C=1 and B=1 (2030-2055)
def f(p,key): return summarize(p,run(p),2030,2056,'x')[key]
for key in ['rasio_B_1_minus_kesenjangan_model_per_kebutuhan','rasio_C_belanja_komponen_minimum_per_kebutuhan']:
    lo,hi=20.0,300.0
    if f(hi,key)<1: print(key,'never reaches 1 up to',hi, f(hi,key)); continue
    for _ in range(14):
        mid=(lo+hi)/2
        if f(mid,key)<1: lo=mid
        else: hi=mid
    print(key,'threshold ~',round(hi,2))
