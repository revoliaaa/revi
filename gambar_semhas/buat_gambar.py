import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter,MultipleLocator
from scipy.signal import savgol_filter
R=json.load(open('digitized.json'))
CM=1/2.54
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman','Liberation Serif'],'font.size':8,
 'axes.linewidth':0.6,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':8.5,'axes.titleweight':'normal',
 'axes.titlelocation':'left','axes.labelsize':8,'xtick.direction':'out','ytick.direction':'out','xtick.major.width':0.6,
 'ytick.major.width':0.6,'xtick.major.size':3,'ytick.major.size':3,'xtick.labelsize':7.5,'ytick.labelsize':7.5,
 'legend.fontsize':7,'legend.frameon':False,'lines.solid_capstyle':'butt','mathtext.fontset':'stix','savefig.dpi':600,'hatch.linewidth':0.5})
def idn(dec=0):
    def f(v,_=None):
        s=f'{abs(v):,.{dec}f}'.replace(',','X').replace('.',',').replace('X','.')
        return ('−' if v<0 and round(abs(v),dec)!=0 else '')+s
    return FuncFormatter(f)
fmt=lambda v,d=0: idn(d)(v)
CO2='tCO$_2$e'
def clean(pts,grid,win=9,thr=None,lo=None,hi=None,smooth=7):
    p=np.array(sorted(pts)); x,y=p[:,0],p[:,1]
    if lo is not None: m=(y>=lo(x))&(y<=hi(x)); x,y=x[m],y[m]
    # rolling median outlier removal
    med=np.array([np.median(y[max(0,i-win):i+win+1]) for i in range(len(y))])
    if thr: m=np.abs(y-med)<thr; x,y=x[m],y[m]
    g=np.interp(grid,x,y)
    if smooth and len(g)>smooth: g=savgol_filter(g,smooth,2)
    return g
def clean_fill(pts,grid,ref,**kw):
    p=np.array(sorted(pts)); lo_=kw.pop('lo',None); hi_=kw.pop('hi',None)
    if lo_ is not None:
        m=(p[:,1]>=lo_(p[:,0]))&(p[:,1]<=hi_(p[:,0])); p=p[m]
    med=np.array([np.median(p[max(0,i-9):i+10,1]) for i in range(len(p))]); p=p[np.abs(p[:,1]-med)<0.4]
    x0=p[0,0]; g=np.interp(grid,p[:,0],p[:,1])
    early=grid<x0; off=np.interp(x0,grid,ref)-p[0,1]
    # blend from ref to trace in early region
    w=np.clip((grid-grid[0])/max(x0-grid[0],1e-6),0,1)
    g[early]=ref[early]-off*w[early]
    return savgol_filter(g,7,2)
def anchor(g,grid,start,end):
    w=(grid-grid[0])/(grid[-1]-grid[0]); return g+(start-g[0])*(1-w)+(end-g[-1])*w
def save(fig,name):
    fig.savefig(f'fig/{name}.png',dpi=600,bbox_inches='tight',pad_inches=0.03,facecolor='white'); plt.close(fig)

# ================= Gambar 4
t=np.arange(2024,2087.01,0.25)
f=R['f4a']
s2=anchor(clean(f['S2'],t,thr=0.4),t,94.308,83.615)
s2f=lambda x:np.interp(x,t,s2)
s1=anchor(clean_fill(f['S1'],t,s2,lo=lambda x:np.maximum(81.7,s2f(x)-3),hi=lambda x:s2f(x)-0.02),t,94.308,81.890)
s1=np.minimum(s1,s2)
s4={k:anchor(clean_fill(f[k],t,s2),t,94.308,e) for k,e in (('S4_10',84.233),('S4_20',87.113),('S4_35',90.698))}
s4['S4_10']=np.maximum(s4['S4_10'],s2)
for k in s4: s4[k]=np.minimum(s4[k],94.308)
s3p=np.array(sorted(f['S3'])); d=s3p[:,1]-s2f(s3p[:,0])
z=np.polyfit(s3p[:,0]-2024,d,2); dd=np.clip(np.polyval(z,t-2024),0,None)
dd=dd*np.clip((t-2024)/3,0,1); dd+= (0.164-dd[-1])*np.clip((t-2060)/27,0,1)
s3=s2+dd
fig,(ax,bx)=plt.subplots(1,2,figsize=(13*CM,5.15*CM),gridspec_kw={'width_ratios':[1.15,1],'wspace':0.38})
st=[('S1 tanpa PS aktif',s1,dict(color='black',ls=(0,(5,2)),lw=0.9)),
    ('S2 PS reguler',s2,dict(color='black',lw=0.9)),
    ('S3 S2 + pembiayaan awal',s3,dict(color='black',ls=(0,(1,1.2)),lw=1.1)),
    ('S4 USD10',s4['S4_10'],dict(color='#9a9a9a',lw=1.3)),
    ('S4 USD20',s4['S4_20'],dict(color='#5e5e5e',lw=1.3,ls=(0,(6,1.5,1.5,1.5)))),
    ('S4 USD35',s4['S4_35'],dict(color='#2b2b2b',lw=1.6))]
for lab,y,kw in st: ax.plot(t,y,label=lab,**kw)
ax.set_xlim(2024,2087); ax.set_ylim(76,95)
ax.set_xticks([2030,2040,2050,2060,2070,2080])
ax.yaxis.set_major_locator(MultipleLocator(2)); ax.yaxis.set_major_formatter(idn())
ax.set_xlabel('Tahun'); ax.set_ylabel('Luas hutan (ribu ha)')
ax.set_title('(a)')
ax.plot([2086.3,2086.3],[81.89,83.615],color='black',lw=0.6,clip_on=False)
for yy_ in (81.89,83.615): ax.plot([2085.6,2087.0],[yy_,yy_],color='black',lw=0.6,clip_on=False)
ax.text(2086.3,78.9,'S2 − S1 (2087): +1.725 ha',ha='right',va='center',fontsize=6.3,style='italic')
ax.legend(loc='lower left',handlelength=2.4,borderaxespad=0.2,labelspacing=0.15,fontsize=6.6)
# (b)
prices=[6,10,15,20,35]; tot=np.array([2117,2532,3490,5585,8789]); ps=np.full(5,1720.); pa=np.full(5,277.); kb=tot-ps-pa
xpos=np.arange(5); w=0.58
bx.bar(xpos,ps,w,color='#4d4d4d',edgecolor='black',lw=0.5,label='PS (S2−S1)')
bx.bar(xpos,pa,w,bottom=ps,color='#b3b3b3',edgecolor='black',lw=0.5,label='Pembiayaan awal (S3−S2)')
bx.bar(xpos,kb,w,bottom=ps+pa,color='white',edgecolor='black',lw=0.5,hatch='////',label='Perdagangan karbon (S4−S3)')
for i,v in enumerate(tot): bx.text(i,v+150,fmt(v),ha='center',va='bottom',fontsize=7)
for i in range(5):
    bx.text(i,ps[i]/2,f'{round(100*ps[i]/tot[i])}%',ha='center',va='center',fontsize=6.3,color='white')
    if kb[i]>1000:
        bx.text(i,ps[i]+pa[i]+kb[i]/2,f'{round(100*kb[i]/tot[i])}%',ha='center',va='center',fontsize=6.3,
                bbox=dict(boxstyle='square,pad=0.12',fc='white',ec='none'))
bx.set_xticks(xpos,[str(p) for p in prices]); bx.set_xlabel(f'Harga karbon (USD/{CO2})')
bx.set_ylabel('Deforestasi dihindari terhadap S1 (ha)'); bx.set_ylim(0,14000)
bx.yaxis.set_major_locator(MultipleLocator(2000)); bx.yaxis.set_major_formatter(idn()); bx.set_xlim(-0.6,4.6)
bx.legend(loc='upper left',handlelength=1.6,handleheight=1.0,borderaxespad=0.2,labelspacing=0.2,fontsize=6.6)
bx.set_title('(b)')
save(fig,'gambar4')

# ================= Gambar 5
fig=plt.figure(figsize=(13*CM,6.70*CM))
gs=fig.add_gridspec(2,2,width_ratios=[1,1.1],wspace=0.42,hspace=0.12)
a1=fig.add_subplot(gs[0,0]); a2=fig.add_subplot(gs[1,0],sharex=a1); b=fig.add_subplot(gs[:,1])
pr=np.arange(1,40.01,0.25)
npv=clean(R['npv'],pr,thr=1.5,smooth=9); cov=clean(R['cov'],pr,thr=4,smooth=9)
# align to reported points
def fitpts(g,pts):
    xs=np.array([p for p,_ in pts]); err=np.array([v-np.interp(p,pr,g) for p,v in pts])
    return g+np.interp(pr,xs,err)
npv=fitpts(npv,[(1,npv[0]),(6.83,0),(10,2.07),(20,11.50),(35,30.79),(40,npv[-1])])
cov=fitpts(cov,[(1,max(cov[0],0)),(10,11.8),(20,49.7),(28.04,100),(40,cov[-1])]); cov=np.clip(cov,0,None)
for axx in (a1,a2): axx.axvspan(6.83,28.04,color='#ececec',lw=0,zorder=0)
a1.plot(pr,npv,color='black',lw=1.2); a1.axhline(0,color='black',lw=0.5)
a1.plot([6.83],[0],'o',ms=3.5,mfc='black',mec='black'); a1.annotate('titik impas USD6,83',(6.83,0),xytext=(12.5,-9),fontsize=7,arrowprops=dict(arrowstyle='-',lw=0.5))
a1.set_ylabel('NPV proyek\n(Rp miliar)'); a1.set_ylim(-12,42); a1.yaxis.set_major_locator(MultipleLocator(20)); a1.yaxis.set_major_formatter(idn())
plt.setp(a1.get_xticklabels(),visible=False)
a1.text(17.4,33,'layak bagi proyek;\nkebutuhan LPHD belum tercukupi',ha='center',va='center',fontsize=6.8,style='italic')
a1.set_title('(a)')
a2.plot(pr,cov,color='black',lw=1.2); a2.axhline(100,color='black',lw=0.5,ls=(0,(3,2)))
a2.plot([28.04],[100],'o',ms=3.5,mfc='black',mec='black'); a2.annotate('tercukupi USD28,04',(28.04,100),xytext=(24.5,30),fontsize=7,ha='left',arrowprops=dict(arrowstyle='-',lw=0.5))
a2.set_ylabel('Cakupan kebutuhan\nminimum LPHD (%)'); a2.set_ylim(0,165); a2.yaxis.set_major_locator(MultipleLocator(50))
a2.set_xlim(1,40); a2.set_xlabel(f'Harga karbon (USD/{CO2})'); a2.xaxis.set_major_locator(MultipleLocator(10))
for axx in (a1,a2): axx.yaxis.set_label_coords(-0.17,0.5)
yr=np.arange(2024,2060.01,0.25)
for k,lab,kw,dy in (('b10','USD10',dict(color='#9a9a9a',lw=1.3),0),('b20','USD20',dict(color='#5e5e5e',lw=1.3,ls=(0,(6,1.5,1.5,1.5))),0),('b35','USD35',dict(color='#2b2b2b',lw=1.6),0)):
    g=clean(R[k],yr,thr=0.4,smooth=5); g[yr<=2027.9]=0; g=np.clip(g,0,None)
    b.plot(yr,g,**kw); b.text(2060.6,g[-1]+dy,lab,va='center',fontsize=7)
b.axhline(5.42,color='black',lw=0.8,ls=(0,(4,2))); b.text(2060.6,5.42,'kebutuhan\nminimum',va='center',fontsize=7)
b.axvspan(2024,2028,color='#ececec',lw=0,zorder=0); b.text(2026,10.8,'jeda kredit\n(belanja = 0)',rotation=90,ha='center',va='top',fontsize=6.3,style='italic',linespacing=1.1)
b.set_xlim(2024,2060); b.set_ylim(0,11); b.set_xticks([2024,2030,2040,2050,2060]); b.yaxis.set_major_locator(MultipleLocator(2))
b.set_ylabel('Belanja LPHD (Rp miliar/tahun)'); b.set_xlabel('Tahun'); b.set_title('(b)')
save(fig,'gambar5')

# ================= Gambar 6
fig,(ax,bx)=plt.subplots(1,2,figsize=(13*CM,5.39*CM),gridspec_kw={'width_ratios':[0.75,1.25],'wspace':0.62})
lab=['S1','S2','S3','S4\n10','S4\n20','S4\n35']; val=[0,13.6,13.6,17.3,32.8,64.5]
ax.bar(range(6),val,0.6,color='#7f7f7f',edgecolor='black',lw=0.5)
for i,v in enumerate(val): ax.text(i,v+1.2,fmt(v,1),ha='center',va='bottom',fontsize=7)
ax.set_xticks(range(6),lab); ax.set_ylabel('Pekerja setara penuh (orang)'); ax.set_ylim(0,72); ax.yaxis.set_major_locator(MultipleLocator(20))
ax.set_xlim(-0.6,5.6); ax.set_title('(a)'); ax.set_xlabel(f'Skenario (S4: harga USD/{CO2})')
cats=['Pendapatan program\nper RT','Perubahan bersih\npendapatan RT (S4−S3)','Kehilangan akses per\nRT (rata-rata)','Kehilangan akses per\nRT pemegang garapan']
v10=[6.3,-40,-227,-564]; v20=[16.3,-93,-448,-1113]
yy=np.arange(4)[::-1]; h=0.36
bx.barh(yy+h/2,v10,h,color='#d0d0d0',edgecolor='black',lw=0.5,label='USD10')
bx.barh(yy-h/2,v20,h,color='#404040',edgecolor='black',lw=0.5,label='USD20')
for y0,v in list(zip(yy+h/2,v10))+list(zip(yy-h/2,v20)):
    s=('+' if v>0 else '')+fmt(v,1 if abs(v)<20 else 0)
    bx.text(v+(18 if v>0 else -18),y0,s,va='center',ha='left' if v>0 else 'right',fontsize=6.8)
bx.axvline(0,color='black',lw=0.6); bx.set_yticks(yy,cats); bx.tick_params(axis='y',length=0)
bx.set_xlim(-1400,150); bx.xaxis.set_major_locator(MultipleLocator(400)); bx.xaxis.set_major_formatter(idn())
bx.set_xlabel('Rp ribu per RT per tahun (rerata 2030–2055)'); bx.spines['left'].set_visible(False)
bx.legend(loc='upper left',handlelength=1.4,borderaxespad=0.2); bx.set_title('(b)')
save(fig,'gambar6')

# ================= Gambar 7
fig,ax=plt.subplots(figsize=(13*CM,6.2*CM))
P={'B1':((0,16.6),(0,66.4)),'B2':((-187,79.1),(-1921,357.7)),'B3':((-330,110.1),(-2801,486.8)),
   'B4':((-331,137.7),(-2801,572.2)),'R1':((0,33.6),(0,134.3)),'R2':((237,-22.4),(2475,-115.8))}
ax.axhline(0,color='black',lw=0.6); ax.axvline(0,color='black',lw=0.6)
for k,(p10,p20) in P.items():
    ax.annotate('',xy=p20,xytext=p10,arrowprops=dict(arrowstyle='-|>',lw=0.6,color='#555555',mutation_scale=7,shrinkA=3.5,shrinkB=3.5))
    ax.plot(*p10,'o',ms=4.5,mfc='white',mec='black',mew=0.8,zorder=3)
    ax.plot(*p20,'o',ms=4.5,mfc='black',mec='black',zorder=3)
ax.plot(0,0,'s',ms=4.5,color='black',zorder=4)
lab={'B0':((0,0),(-70,-28),'right'),'B1':((0,66.4),(70,66),'left'),'R1':((0,134.3),(70,140),'left'),
     'B2':((-1921,357.7),(-1990,372),'right'),'B3':((-2801,486.8),(-2870,487),'right'),'B4':((-2801,572.2),(-2870,572),'right'),'R2':((2475,-115.8),(2560,-116),'left')}
for k,(_,xy,ha) in lab.items(): ax.text(*xy,k,fontsize=7.5,fontweight='bold',ha=ha,va='center')
ax.set_xlim(-3300,3000); ax.set_ylim(-200,650)
ax.xaxis.set_major_locator(MultipleLocator(1000)); ax.xaxis.set_major_formatter(idn()); ax.yaxis.set_major_locator(MultipleLocator(100)); ax.yaxis.set_major_formatter(idn())
ax.set_xlabel('Δ deforestasi dihindari terhadap B0 (ha, 2025–2086)'); ax.set_ylabel('Δ pendapatan RT terdampak\n(Rp ribu/RT/tahun)')
kw=dict(fontsize=6.3,style='italic',color='#333333')
ax.text(-90,630,'Pendapatan naik,\nperlindungan hutan melemah',ha='right',va='top',linespacing=1.15,**kw)
ax.text(90,630,'Pendapatan naik tanpa\nmengurangi perlindungan hutan',ha='left',va='top',linespacing=1.15,**kw)
ax.text(150,-190,'Perlindungan hutan meningkat, pendapatan turun',va='bottom',**kw)
ax.text(2950,330,'Pada sumbu nol (hutan sama dengan B0):\nR1  +33,6 → +134,3\nB1  +16,6 → +66,4\n(USD10 → USD20; Rp ribu/RT/tahun)',ha='right',va='center',fontsize=6.8,linespacing=1.35)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker='o',ls='',mfc='white',mec='black',ms=4.5,label='USD10'),Line2D([],[],marker='o',ls='',color='black',ms=4.5,label='USD20'),Line2D([],[],marker='s',ls='',color='black',ms=4.5,label='B0 (alokasi dasar)')],loc='lower left',borderaxespad=0.3,handletextpad=0.3)
save(fig,'gambar7')
print('ok')
