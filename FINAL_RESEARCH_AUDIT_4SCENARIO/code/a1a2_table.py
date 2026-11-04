import pandas as pd,numpy as np,pickle,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-revi/2fafe0e9-8133-579b-9506-9462c793243c/scratchpad/tools')
from calc import F as FF
DT=0.0625
out=pickle.load(open('a1a2.pkl','rb'))
S1=FF('S1');S2=FF('S2');S3=FF('S3')
def I(df,c,a,b): s=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9),c]; return float(s.sum()*DT)
def pv(df,c): s=df.loc[df.index<2087-1e-9,c]; return float((s.values*1.1**(-(s.index.values-2024))).sum()*DT)
def M(df,c): return I(df,c,2030,2056)/26
reg={  # register sheet 8 (kumulatif 2025-2086) A2 values
 6:dict(defor=27815.59673646777,kredit=51257.31026989602,terbit=51257.31023421408,terjual=44850.14641830757,gross=4625112314.251542,lphd=0),
 10:dict(defor=27784.78419008119,kredit=57019.11008209837,terbit=57019.10996344657,terjual=49891.72109615117,gross=8388460598.338614,lphd=1341912016.381529),
 15:dict(defor=27727.69522267739,kredit=67642.81015967781,terbit=67642.8097336446,terjual=59187.45807893283,gross=14795085723.3668,lphd=3821346077.184621),
 20:dict(defor=27623.90914885431,kredit=86990.1158832075,terbit=86990.11262284881,terjual=76116.34518574261,gross=25360753120.50592,lphd=8295644964.795124),
 35:dict(defor=21639.50958741254,kredit=1144609.874509366,terbit=1089846.584059146,terjual=933210.2153942254,gross=547306414930.7465,lphd=294808632313.1376)}
rows=[]
eS1=I(S1,'Emisi Deforestasi Biomassa',2025,2087); eS2=I(S2,'Emisi Deforestasi Biomassa',2025,2087)
cap=0.9*0.88*0.682
for (lab,p),df in out.items():
    d=I(df,'Deforestasi Total',2025,2087); e4=I(df,'Emisi Deforestasi Biomassa',2025,2087)
    r=dict(basis=lab,harga_USD=p,
      status={'A1':'HASIL UTAMA (direproduksi; = naskah)','A2_register':'PEMBANDING RESMI REGISTER (CLOSURE; direproduksi audit)','A2_faktor1':'DIAGNOSTIK BARU AUDIT (A2 tanpa faktor penutup reversal)'}[lab],
      Switch_Baseline_Kredit_Konservatif=0 if lab=='A1' else 1,
      Faktor_Rekonsiliasi_Reversal=float(df['Faktor Rekonsiliasi Reversal Kredit A2'].iloc[0]),
      porsi_mitigasi_adisional_thd_S2_rerata_2030_2055=M(df,'Porsi Mitigasi Adisional terhadap S2'),
      deforestasi_kum_2025_2086_ha=d, S4_S3_ha=I(S3,'Deforestasi Total',2025,2087)-d, S4_S1_ha=I(S1,'Deforestasi Total',2025,2087)-d,
      hutan_2087_ha=float(df['Total Hutan'].iloc[-1]),
      emisi_def_biomassa_dihindari_vs_S1_tCO2e=eS1-e4, emisi_def_biomassa_dihindari_vs_S2_tCO2e=eS2-e4,
      plafon_eligible_vs_S1_tCO2e=(eS1-e4)*cap, plafon_eligible_vs_S2_tCO2e=(eS2-e4)*cap,
      PE_REDD_bruto_tCO2e=I(df,'Pengurangan Emisi REDD Bruto',2024,2087), PE_eligible_REDD_tCO2e=I(df,'Pengurangan Emisi Eligible REDD',2024,2087),
      kredit_REDD_diajukan=I(df,'Kredit REDD Diajukan',2024,2087), kredit_REDD_terbit=I(df,'Kredit REDD Terbit',2024,2087), kredit_REDD_terjual=I(df,'Kredit REDD Terjual',2024,2087),
      kredit_REDD_kedaluwarsa=I(df,'Kredit REDD Kedaluwarsa',2024,2087), kredit_ARR_diajukan=I(df,'Kredit ARR Diajukan',2024,2087), kredit_karbon_terjual_total=I(df,'Kredit Karbon Terjual',2024,2087),
      penerimaan_kotor_Rp=I(df,'Pendapatan Kotor Penjualan Kredit',2024,2087), biaya_MRV_trans_pajak_Rp=I(df,'Biaya Transaksi dan MRV',2024,2087),
      dana_LPHD_Rp=I(df,'Dana Desa Diterima',2024,2087), belanja_LPHD_Rp=I(df,'Penggunaan Dana Pengelolaan',2024,2087),
      defisit_biaya_belum_pulih_2087_Rp=float(df['Defisit Biaya Bersama Belum Dipulihkan'].iloc[-1]), pembiayaan_awal_belum_pulih_2087_Rp=float(df['Pendanaan Awal Belum Terpulihkan'].iloc[-1]),
      NPV_proyek_10_Rp=pv(df,'Pendapatan Kotor Penjualan Kredit')-pv(df,'Biaya Transaksi dan MRV')-pv(df,'Realisasi Pembiayaan Awal')-pv(df,'Penggunaan Dana Pengelolaan'),
      NPV_mitra_10_Rp=pv(df,'Dana Mitra dari Karbon')+pv(df,'Pemulihan Defisit Biaya Bersama')-pv(df,'Kekurangan Biaya Bersama Ditanggung Mitra')-pv(df,'Realisasi Pembiayaan Awal'),
      intensitas_rerata=M(df,'Indeks Intensitas Perlindungan'), hari_patroli_didanai_rerata=M(df,'Hari Patroli Didanai'))
    if lab=='A2_register':
        R=reg[p]
        r['cek_register_defor_selisih']=I(df,'Deforestasi Total',2025,2087)-R['defor']
        r['cek_register_kredit_2025_2086_selisih']=I(df,'Kredit REDD Diajukan',2025,2087)-R['kredit']
        r['cek_register_terjual_selisih']=I(df,'Kredit REDD Terjual',2025,2087)-R['terjual']
        r['cek_register_kotor_selisih']=I(df,'Pendapatan Kotor Penjualan Kredit',2025,2087)-R['gross']
        r['cek_register_lphd_selisih']=I(df,'Dana Desa Diterima',2025,2087)-R['lphd']
    rows.append(r)
D=pd.DataFrame(rows).sort_values(['harga_USD','basis'])
D.to_csv('/home/user/revi/FINAL_RESEARCH_AUDIT_4SCENARIO/A1_A2_BASELINE_RECONCILIATION.csv',index=False)
pd.set_option('display.width',250)
print(D.set_index(['basis','harga_USD']).T.to_string())
