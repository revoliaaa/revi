import pysd,pandas as pd,numpy as np,warnings,pickle;warnings.filterwarnings('ignore')
DT=0.0625; ts=list(np.arange(2024,2087+1e-9,DT))
files={6:'DKP_25HD_A1_S4_USD6_rapi',10:'DKP_25HD_A1_S4_USD10_rapi',15:'DKP_25HD_A1_S4_USD15_rapi',20:'DKP_25HD_A1_S4_USD20_rapi',35:'DKP_25HD_A1_S4_USD35_rapi'}
fac={6:0.718917,10:0.727781,15:0.740124,20:0.762355,35:1.0}
out={}
for p,f in files.items():
    m=pysd.load(f+'.py')
    for lab,par in [('A1',{}),('A2_register',{'Switch Baseline Kredit Konservatif':1,'Faktor Rekonsiliasi Reversal Kredit A2':fac[p]}),('A2_faktor1',{'Switch Baseline Kredit Konservatif':1,'Faktor Rekonsiliasi Reversal Kredit A2':1})]:
        df=m.run(params=par,return_timestamps=ts,progress=False,reload=True)
        out[(lab,p)]=df; print(lab,p,flush=True)
pickle.dump(out,open('a1a2.pkl','wb'))
