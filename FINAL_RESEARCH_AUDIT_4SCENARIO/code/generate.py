import sys,os,json,hashlib,datetime
sys.path.insert(0,os.path.dirname(__file__))
from calc import *
import pandas as pd,numpy as np
O='/home/user/revi/FINAL_RESEARCH_AUDIT_4SCENARIO/'
SRC='/tmp/claude-0/-home-user-revi/2fafe0e9-8133-579b-9506-9462c793243c/scratchpad/src/MODEL VENSIM/'
P=['S4USD3','S4USD6','S4USD10','S4USD15','S4USD20','S4USD35']
ALL=['S1','S2','S3']+P
def pv(k,col,rate=0.10,a=2024,b=2087):
    df=F(k); s=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9),col]
    return float((s.values*(1+rate)**(-(s.index.values-2024))).sum()*DT)
# ---------- 00 inventory
rows=[]
meta={'DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi.mdl':('S1','Skenario Kebijakan=1; konstanta dibulatkan 6 angka penting'),
'DKP_25HD_A1_S2_PS_REGULER_rapi.mdl':('S2','Skenario Kebijakan=2; konstanta dibulatkan'),
'DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi.mdl':('S3','Skenario Kebijakan=3; konstanta dibulatkan'),
'DKP_25HD_A1_S4_USD3_rapi.mdl':('S4 USD3 (arsip)','Harga Karbon=3; konstanta tidak dibulatkan'),
'DKP_25HD_A1_S4_USD6_rapi.mdl':('S4 USD6','Harga Karbon=6; konstanta tidak dibulatkan'),
'DKP_25HD_A1_S4_USD10_rapi.mdl':('S4 USD10','Harga Karbon=10; konstanta tidak dibulatkan (acuan diff)'),
'DKP_25HD_A1_S4_USD15_rapi.mdl':('S4 USD15','Harga Karbon=15; konstanta tidak dibulatkan'),
'DKP_25HD_A1_S4_USD20_rapi.mdl':('S4 USD20','Harga Karbon=20; konstanta tidak dibulatkan'),
'DKP_25HD_A1_S4_USD35_rapi.mdl':('S4 USD35','Harga Karbon=35; konstanta dibulatkan'),
'DKP_25HD_A1_S4_USD35_rapi.2mdl':('S4 USD35 (duplikat)','md5 identik dengan ..._USD35_rapi.mdl'),
'DKP 25HD_A1_BENEFIT_ALLOCATION_EXPERIMENT_rapi.mdl':('Eksperimen alokasi (di luar cakupan)','740 variabel; Switch Alokasi Dana Fleksibel=0'),
'Ext Data/Skenario1.txt':('S1','Ekspor Vensim, run SKENARIO1, 686 variabel'),
'Ext Data/Skenario2.txt':('S2','Ekspor Vensim, run Run/Skenario2'),
'Ext Data/Skenario3.txt':('S3','Ekspor Vensim, label run "Run/Untitled" (bukan "Skenario3")'),
'Ext Data/Skenario4USD6.txt':('S4 USD6','Ekspor Vensim'),
'Ext Data/Skenario4USD10.txt':('S4 USD10','Ekspor Vensim'),
'Ext Data/Skenario4USD15.txt':('S4 USD15','Ekspor Vensim'),
'Ext Data/Untitled.txt':('S4 USD35','Nama berkas "Untitled" tetapi label run "Run/Skenario4USD35"'),
'Ext Data/benefit allocation.txt':('Eksperimen alokasi','di luar cakupan'),
'Run/SKENARIO1.vdfx':('S1','biner Vensim; tidak dapat dibaca tanpa Vensim'),
'Run/Skenario2.vdfx':('S2','biner'),'Run/Untitled.vdfx':('S3 (diduga)','biner; label run S3 di ekspor'),
'Run/Skenario4USD6.vdfx':('S4 USD6','biner'),'Run/Skenario4USD10.vdfx':('S4 USD10','biner'),'Run/Skenario4USD15.vdfx':('S4 USD15','biner'),
'Run/Skenario4USD20.vdfx':('S4 USD20','biner; SATU-SATUNYA keluaran Vensim USD20 dan tidak ada ekspor .txt'),
'Run/Skenario4USD35.vdfx':('S4 USD35','biner'),'Run/Benefit alloc.vdfx':('Eksperimen alokasi','biner'),
'HASIL SIMULASI VENSIM.xlsx':('S1–S4 + alokasi','RUSAK: pemisah desimal hilang saat impor (mis. 20.1326 -> 201326); 20–35 % nilai tidak cocok dengan .txt'),
'REGISTER_DATA_SEMUA_SKENARIO_A1.xlsx':('Semua','Register PySD; README: "Vensim native belum dijalankan"; sumber hasil resmi a1/out/FINAL_THESIS_RESULTS.xlsx TIDAK disertakan'),
'.DS_Store':('-','metadata macOS')}
for rel,(sc,note) in meta.items():
    p=SRC+rel; b=open(p,'rb').read()
    rows.append(dict(berkas=rel,jenis=os.path.splitext(rel)[1] or '-',skenario=sc,md5=hashlib.md5(b).hexdigest(),ukuran_byte=len(b),mtime_zip=datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M'),catatan=note))
rows.append(dict(berkas='MAKALAH_SEMHAS_REVOLIA_AZ-ZAHRA.pdf',jenis='.pdf',skenario='Naskah',md5='e74fdbdba6b1726a97dec0a7ffe000ed',ukuran_byte='',mtime_zip='',catatan='12 halaman; dua unggahan identik'))
rows.append(dict(berkas='DELTA_KAPUAS_25HD_SD_FINAL_A1.mdl (md5 f1bfaa88d84d61d6d9f990cda990253a)',jenis='.mdl',skenario='(disebut pengguna)',md5='TIDAK ADA DI ZIP',ukuran_byte='',mtime_zip='',catatan='Berkas induk yang disebut tidak tersedia; keterlacakan ke berkas ini BELUM TERVERIFIKASI'))
pd.DataFrame(rows).to_csv(O+'00_SOURCE_INVENTORY/source_inventory.csv',index=False)
# ---------- 01 ecological
eco=[];ann=[]
reg=['NonHutan menjadi HMS','NonHutan menjadi HRS','NonHutan menjadi HLKS'];reh=['Rehabilitasi ke HMS','Rehabilitasi ke HRS','Rehabilitasi ke HLKS']
for k in ALL:
    df=F(k)
    for c in ['__reg','__reh']: pass
    df['__reg']=df[reg].sum(axis=1); df['__reh']=df[reh].sum(axis=1)
    H24=V(k,'Total Hutan',2024);H25=V(k,'Total Hutan',2025);H87=V(k,'Total Hutan',2087)
    d=I(k,'Deforestasi Total',2025,2087); g=I(k,'__reg',2025,2087); r=I(k,'__reh',2025,2087)
    eco.append(dict(skenario=k,hutan_2024_ha=H24,hutan_2025_ha=H25,perubahan_bersih_2024_ha=H25-H24,deforestasi_2024_ha=I(k,'Deforestasi Total',2024,2025),regenerasi_2024_ha=I(k,'__reg',2024,2025),
        deforestasi_kum_2025_2086_ha=d,regenerasi_alami_kum_2025_2086_ha=g,rehabilitasi_menjadi_hutan_kum_2025_2086_ha=r,hutan_2087_ha=H87,residu_neraca_ha=H87-(H25-d+g+r),
        deforestasi_rerata_2030_2055_ha_th=Mint(k,'Deforestasi Total'),intensitas_perlindungan_rerata_2030_2055=Mint(k,'Indeks Intensitas Perlindungan'),
        emisi_bersih_kum_2025_2086_tCO2e=I(k,'Total Emisi Bersih',2025,2087),emisi_deforestasi_biomassa_kum_tCO2e=I(k,'Emisi Deforestasi Biomassa',2025,2087),
        emisi_dihindari_vs_S1_tCO2e=I('S1','Total Emisi Bersih',2025,2087)-I(k,'Total Emisi Bersih',2025,2087),deforestasi_dihindari_vs_S1_ha=I('S1','Deforestasi Total',2025,2087)-d,selisih_hutan_2087_vs_S1_ha=H87-V('S1','Total Hutan',2087)))
    for y in range(2024,2087):
        ann.append(dict(skenario=k,tahun=y,hutan_awal_tahun_ha=V(k,'Total Hutan',y),deforestasi_ha=I(k,'Deforestasi Total',y,y+1),regenerasi_ha=I(k,'__reg',y,y+1),rehabilitasi_ha=I(k,'__reh',y,y+1),intensitas_perlindungan=Mint(k,'Indeks Intensitas Perlindungan',y,y),emisi_bersih_tCO2e=I(k,'Total Emisi Bersih',y,y+1)))
E=pd.DataFrame(eco); E.to_csv(O+'01_ECOLOGICAL_RESULTS/ecological_summary.csv',index=False)
pd.DataFrame(ann).to_csv(O+'01_ECOLOGICAL_RESULTS/ecological_annual.csv',index=False)
# ---------- 02 decomposition
e=E.set_index('skenario'); dec=[]
for k in P:
    tot=e.loc['S1','deforestasi_kum_2025_2086_ha']-e.loc[k,'deforestasi_kum_2025_2086_ha']
    a=e.loc['S1','deforestasi_kum_2025_2086_ha']-e.loc['S2','deforestasi_kum_2025_2086_ha']; b=e.loc['S2','deforestasi_kum_2025_2086_ha']-e.loc['S3','deforestasi_kum_2025_2086_ha']; c=e.loc['S3','deforestasi_kum_2025_2086_ha']-e.loc[k,'deforestasi_kum_2025_2086_ha']
    em=lambda x,y:e.loc[x,'emisi_bersih_kum_2025_2086_tCO2e']-e.loc[y,'emisi_bersih_kum_2025_2086_tCO2e']
    dec.append(dict(harga=k,S2_S1_ha=a,S3_S2_ha=b,S4_S3_ha=c,total_vs_S1_ha=tot,porsi_PS=a/tot,porsi_pembiayaan_awal=b/tot,porsi_karbon=c/tot,S2_S1_tCO2e=em('S1','S2'),S3_S2_tCO2e=em('S2','S3'),S4_S3_tCO2e=em('S3',k),total_vs_S1_tCO2e=em('S1',k),
        selisih_hutan2087_S4_S3_ha=e.loc[k,'hutan_2087_ha']-e.loc['S3','hutan_2087_ha']))
pd.DataFrame(dec).to_csv(O+'02_SCENARIO_COMPARISON/decomposition_by_price.csv',index=False)
tl=[dict(tahun=y,S2_S1=I('S1','Deforestasi Total',y,y+1)-I('S2','Deforestasi Total',y,y+1),S3_S2=I('S2','Deforestasi Total',y,y+1)-I('S3','Deforestasi Total',y,y+1),**{f'{k}_S3':I('S3','Deforestasi Total',y,y+1)-I(k,'Deforestasi Total',y,y+1) for k in P}) for y in range(2024,2087)]
pd.DataFrame(tl).to_csv(O+'02_SCENARIO_COMPARISON/annual_avoided_deforestation.csv',index=False)
# ---------- 03 carbon
car=[]
for k in P:
    eb=lambda x:I(x,'Emisi Deforestasi Biomassa',2025,2087)
    tot=eb('S1')-eb(k); ps=eb('S1')-eb('S2'); fin=eb('S2')-eb('S3'); cb=eb('S3')-eb(k)
    f=0.9*0.88*0.682
    car.append(dict(harga=k,PE_REDD_bruto_vs_baseline_internal_tCO2e=I(k,'Pengurangan Emisi REDD Bruto',2024,2087),PE_eligible_REDD_tCO2e=I(k,'Pengurangan Emisi Eligible REDD',2024,2087),
        kredit_REDD_diajukan_tCO2e=I(k,'Kredit REDD Diajukan',2024,2087),kredit_REDD_terbit_tCO2e=I(k,'Kredit REDD Terbit',2024,2087),kredit_REDD_terjual_tCO2e=I(k,'Kredit REDD Terjual',2024,2087),kredit_REDD_kedaluwarsa_tCO2e=I(k,'Kredit REDD Kedaluwarsa',2024,2087),
        stok_REDD_belum_terjual_2087=V(k,'Stok Kredit REDD Belum Terjual',2087),kredit_ARR_diajukan_tCO2e=I(k,'Kredit ARR Diajukan',2024,2087),kredit_ARR_terjual_tCO2e=I(k,'Kredit ARR Terjual',2024,2087),kredit_karbon_terjual_total_tCO2e=I(k,'Kredit Karbon Terjual',2024,2087),
        emisi_def_biomassa_dihindari_vs_S1=tot,porsi_atribusi_PS=ps/tot,porsi_atribusi_pembiayaan_awal=fin/tot,porsi_atribusi_karbon=cb/tot,
        diag_kredit_hanya_efek_karbon_statis_tCO2e=cb*f,diag_rasio_terhadap_kredit_A1=cb*f/I(k,'Kredit REDD Diajukan',2024,2087)))
C=pd.DataFrame(car); C.to_csv(O+'03_CARBON_ACCOUNTING/carbon_accounting_A1.csv',index=False)
diag=json.load(open(W+'diag.json'))
a2=[]
for k in ['S4USD6','S4USD10','S4USD15','S4USD20','S4USD35']:
    d=diag[f'A2|{k}']
    a2.append(dict(harga=k,A2_deforestasi_kum_ha=d['defor'],A2_S4_S3_ha=I('S3','Deforestasi Total',2025,2087)-d['defor'],A1_S4_S3_ha=I('S3','Deforestasi Total',2025,2087)-I(k,'Deforestasi Total',2025,2087),
        A2_kredit_tCO2e=d['kredit'],A1_kredit_tCO2e=I(k,'Kredit REDD Diajukan',2024,2087),A2_penerimaan_kotor_Rp=d['gross'],A2_biaya_MRV_trans_pajak_Rp=d['biaya'],A2_dana_LPHD_Rp=d['danaLPHD'],A2_NPV_proyek_Rp=d['npv'],A2_cakupan_belanja_per_kebutuhan=d['cov']))
pd.DataFrame(a2).to_csv(O+'03_CARBON_ACCOUNTING/diagnostic_A2_additional_to_S2_rerun.csv',index=False)
# ---------- 04 financial
fin=[]
for k in ['S3']+P:
    g=I(k,'Pendapatan Kotor Penjualan Kredit',2024,2087)
    row=dict(skenario=k,penerimaan_kotor=g,biaya_monitoring_MRV=I(k,'Biaya Monitoring MRV',2024,2087),biaya_verifikasi=I(k,'Biaya Verifikasi Tahunan',2024,2087),biaya_penerbitan_registri=I(k,'Biaya Penerbitan dan Registri',2024,2087),
        biaya_transaksi_penjualan=I(k,'Biaya Transaksi Penjualan',2024,2087),pajak_pungutan=I(k,'Pajak dan Pungutan Karbon',2024,2087),biaya_MRV_trans_pajak_total=I(k,'Biaya Transaksi dan MRV',2024,2087),
        kekurangan_biaya_ditanggung_mitra=I(k,'Kekurangan Biaya Bersama Ditanggung Mitra',2024,2087),pemulihan_defisit_biaya_bersama=I(k,'Pemulihan Defisit Biaya Bersama',2024,2087),defisit_belum_pulih_2087=V(k,'Defisit Biaya Bersama Belum Dipulihkan',2087),
        pendapatan_bersih_distribusi=I(k,'Pendapatan Karbon Bersih yang Dapat Didistribusikan',2024,2087),dana_LPHD_diterima=I(k,'Dana Desa Diterima',2024,2087),dana_mitra=I(k,'Dana Mitra dari Karbon',2024,2087),
        pemulihan_pembiayaan_awal=I(k,'Pemulihan Pendanaan Awal',2024,2087),pembiayaan_awal_belum_pulih_2087=V(k,'Pendanaan Awal Belum Terpulihkan',2087),pembiayaan_awal_S3=I(k,'Realisasi Pembiayaan Awal',2024,2087),
        belanja_LPHD_total=I(k,'Penggunaan Dana Pengelolaan',2024,2087),saldo_LPHD_2087=V(k,'Saldo Dana LPHD',2087),
        NPV_proyek_10=pv(k,'Pendapatan Kotor Penjualan Kredit')-pv(k,'Biaya Transaksi dan MRV')-pv(k,'Realisasi Pembiayaan Awal')-pv(k,'Penggunaan Dana Pengelolaan'),
        NPV_mitra_10=pv(k,'Dana Mitra dari Karbon')+pv(k,'Pemulihan Defisit Biaya Bersama')-pv(k,'Kekurangan Biaya Bersama Ditanggung Mitra')-pv(k,'Realisasi Pembiayaan Awal'))
    w=F(k); w=w.loc[(w.index>=2030)&(w.index<2056)]
    need=w['Kebutuhan Dana Minimum'].mean()
    row.update(kebutuhan_minimum_rerata_2030_2055=need,belanja_total_rerata=w['Penggunaan Dana Pengelolaan'].mean(),cakupan_versi_makalah=w['Penggunaan Dana Pengelolaan'].mean()/need,
        kesenjangan_minimum_rerata=w['Kesenjangan Pembiayaan Minimum'].mean(),cakupan_berbasis_kesenjangan=1-w['Kesenjangan Pembiayaan Minimum'].mean()/need,
        cakupan_komponen_minimum_saja=(w['Realisasi Belanja Operasional LPHD']+w['Realisasi Belanja Perlindungan']+w['Realisasi Belanja Pengendalian Kebakaran']+w['Realisasi Pembiayaan Awal']).mean()/need,
        hari_patroli_didanai_rerata=w['Hari Patroli Didanai'].mean())
    yrs=F(k); first=yrs.index[(yrs['Penggunaan Dana Pengelolaan']>0)]; row['belanja_LPHD_pertama_kali_positif_t']=float(first[0]) if len(first) else None
    ex=yrs.index[(yrs['Penggunaan Dana Pengelolaan']>=yrs['Kebutuhan Dana Minimum'])&(yrs.index>2025)]; row['belanja_total_melampaui_kebutuhan_pertama_t']=float(ex[0]) if len(ex) else None
    fin.append(row)
FN=pd.DataFrame(fin); FN.to_csv(O+'04_FINANCIAL_RESULTS/financial_summary.csv',index=False)
cf=[]
for k in ['S3']+P:
    for y in range(2024,2087):
        cf.append(dict(skenario=k,tahun=y,**{c:I(k,c,y,y+1) for c in ['Pendapatan Kotor Penjualan Kredit','Biaya Transaksi dan MRV','Kekurangan Biaya Bersama Ditanggung Mitra','Pemulihan Defisit Biaya Bersama','Pendapatan Karbon Bersih yang Dapat Didistribusikan','Dana Desa Diterima','Dana Mitra dari Karbon','Pemulihan Pendanaan Awal','Realisasi Pembiayaan Awal','Penggunaan Dana Pengelolaan','Kebutuhan Dana Minimum','Kesenjangan Pembiayaan Minimum']},saldo_LPHD_awal_tahun=V(k,'Saldo Dana LPHD',y)))
pd.DataFrame(cf).to_csv(O+'04_FINANCIAL_RESULTS/annual_cashflow.csv',index=False)
# ---------- 05 socio
so=[]
for k in ALL:
    so.append(dict(skenario=k,HOK_rerata=Mint(k,'Kesempatan Kerja PS'),HOK_patroli_swadaya=Mint(k,'Hari Patroli Swadaya'),HOK_patroli_berbayar=Mint(k,'HOK Patroli Berbayar'),HOK_penanaman=Mint(k,'HOK Penanaman'),HOK_pengendalian_kebakaran=Mint(k,'HOK Pengendalian Kebakaran'),
        FTE_HOK_per_300=Mint(k,'Kesempatan Kerja PS')/300,upah_didanai_karbon_Rp_th=Mint(k,'Upah Kegiatan Didanai Karbon'),
        KUPS_aktif_rerata_sampel_tahunan=Mann(k,'Jumlah KUPS Aktif'),KUPS_aktif_rerata_integral=Mint(k,'Jumlah KUPS Aktif'),anggota_KUPS=Mint(k,'Anggota KUPS Aktif'),KUPS_2087=V(k,'Jumlah KUPS Aktif',2087),
        penerimaan_anggota_KUPS_total_Rp_th=Mint(k,'Pendapatan KUPS Total'),pendapatan_bersih_RT_Rp_th=Mint(k,'Pendapatan Bersih per RT Bergantung'),pendapatan_program_per_RT=Mint(k,'Pendapatan Program per RT Bergantung'),
        kehilangan_akses_per_RT_rata=Mint(k,'Kehilangan Pendapatan Pembatasan Akses per RT'),kehilangan_per_RT_terdampak=Mint(k,'Kehilangan per RT Terdampak'),RT_bergantung=Mint(k,'Rumah Tangga Bergantung Hutan'),RT_terdampak=Mint(k,'RT Terdampak Akses')))
pd.DataFrame(so).to_csv(O+'05_SOCIOECONOMIC_RESULTS/socioeconomic_2030_2055.csv',index=False)
acc=[]
for k in ['S2','S3','S4USD10','S4USD20']:
    for m in [0,0.25,0.5,0.75,1,2,3.24]: acc.append(dict(skenario=k,pengali=m,pendapatan_RT_rerata=diag[f'ACC|{k}|{m}']['rt']))
A=pd.DataFrame(acc); A.to_csv(O+'05_SOCIOECONOMIC_RESULTS/access_multiplier_sweep.csv',index=False)
s1rt=Mint('S1','Pendapatan Bersih per RT Bergantung'); zc=[]
def get(k,m): return float(A[(A.skenario==k)&(A.pengali==m)].pendapatan_RT_rerata.iloc[0])
for lab,a,b in [('S2-S1','S2',None),('S3-S2','S3','S2'),('S4USD10-S3','S4USD10','S3'),('S4USD20-S3','S4USD20','S3')]:
    d0=get(a,0)-(s1rt if b is None else get(b,0)); d1=get(a,1)-(s1rt if b is None else get(b,1))
    zc.append(dict(perbandingan=lab,selisih_pada_pengali0=d0,selisih_pada_pengali1=d1,pengali_titik_nol=d0/(d0-d1) if d0!=d1 else None))
pd.DataFrame(zc).to_csv(O+'05_SOCIOECONOMIC_RESULTS/access_multiplier_zero_crossing.csv',index=False)
# ---------- 06/07 misc
dtj=json.load(open(W+'dt.json')); dtr=[]
for key,v in dtj.items():
    k,dt=key.split('|'); dtr.append(dict(skenario=k,DT=float(dt),**v))
DTR=pd.DataFrame(dtr); base=DTR[DTR.DT==0.0625].set_index('skenario')
for c in ['hutan2087','defor','gross','kredit','lphd']:
    DTR[c+'_rel_vs_0.0625_%']=DTR.apply(lambda r:100*(r[c]-base.loc[r.skenario,c])/base.loc[r.skenario,c] if base.loc[r.skenario,c] else 0,axis=1)
DTR.to_csv(O+'06_VALIDATION/dt_sensitivity.csv',index=False)
lp=[]
for k in ['S4USD10','S4USD20','S4USD35']:
    for lab in ['Realisasi Belanja Perlindungan=0','Hari Patroli Didanai=0']:
        d=diag[f'LOOP|{k}|{lab}']; lp.append(dict(skenario=k,intervensi=lab,deforestasi_kum=d['defor'],S4_S3_ha=I('S3','Deforestasi Total',2025,2087)-d['defor'],S4_S3_ha_basis=I('S3','Deforestasi Total',2025,2087)-I(k,'Deforestasi Total',2025,2087),penerimaan_kotor=d['gross']))
pd.DataFrame(lp).to_csv(O+'06_VALIDATION/loop_break_test.csv',index=False)
import shutil
for f in ['pysd_vs_vensim.csv','key_vensim_pysd.csv','robustness_oat.csv']:
    shutil.copy(W+f,O+('06_VALIDATION/' if 'vensim' in f else '07_UNCERTAINTY/')+f)
print('done')
