import re,sys
def parse(path):
    t=open(path,encoding='latin-1').read().replace('\r','')
    t=t.split('\\\\\\---///')[0]
    if t.startswith('{UTF-8}'): t=t[7:]
    out={}
    for blk in t.split('|'):
        parts=blk.split('~')
        if len(parts)<2: continue
        eq=parts[0]
        eq=re.sub(r'\\\n','',eq)
        eq=re.sub(r'\s+',' ',eq).strip()
        if not eq: continue
        m=re.match(r'^(.+?)\s*(=|:=|\(|:)',eq)
        name=eq.split('=')[0].strip() if '=' in eq else eq.split('(')[0].strip()
        name=re.sub(r'\s+',' ',name).lower()
        if name.startswith('*'): continue
        out[name]=(eq,re.sub(r'\s+',' ',parts[1]).strip())
    return out
if __name__=='__main__':
    a=parse(sys.argv[1]); b=parse(sys.argv[2])
    for k in sorted(set(a)|set(b)):
        if k not in a: print('ONLY B:',b[k][0][:300]); continue
        if k not in b: print('ONLY A:',a[k][0][:300]); continue
        if a[k][0].replace(' ','')!=b[k][0].replace(' ',''):
            print('DIFF',k); print('  A:',a[k][0][:400]); print('  B:',b[k][0][:400])
    print('nA',len(a),'nB',len(b))
