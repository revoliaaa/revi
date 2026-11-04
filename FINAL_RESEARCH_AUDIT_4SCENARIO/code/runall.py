import pysd,glob,pandas as pd,warnings,sys
warnings.filterwarnings('ignore')
runs={'S1':'DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi','S2':'DKP_25HD_A1_S2_PS_REGULER_rapi','S3':'DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi',
'S4USD3':'DKP_25HD_A1_S4_USD3_rapi','S4USD6':'DKP_25HD_A1_S4_USD6_rapi','S4USD10':'DKP_25HD_A1_S4_USD10_rapi','S4USD15':'DKP_25HD_A1_S4_USD15_rapi',
'S4USD20':'DKP_25HD_A1_S4_USD20_rapi','S4USD35':'DKP_25HD_A1_S4_USD35_rapi','BENEFIT':'BENEFIT_rapi'}
for k,f in runs.items():
    m=pysd.load(f+'.py')
    df=m.run(return_timestamps=list(range(2024,2088)),progress=False)
    df.to_pickle(f'{k}.pkl'); print(k,df.shape,flush=True)
