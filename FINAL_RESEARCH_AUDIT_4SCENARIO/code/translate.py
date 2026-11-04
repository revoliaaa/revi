import pysd,glob,sys,time
for f in sorted(glob.glob('*.mdl')):
    t=time.time()
    try:
        m=pysd.read_vensim(f); print('OK',f,round(time.time()-t,1))
    except Exception as e: print('FAIL',f,repr(e)[:300])
