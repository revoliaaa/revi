import re,sys
t=open(sys.argv[1],encoding='utf-8').read().split('\\\\\\---///')[0]
blocks=t.split('|')
for b in blocks:
    b=b.strip().replace('{UTF-8}','').strip()
    if not b: continue
    head=b.split('~')[0]
    m=re.match(r'([^=(]+?)\s*(=|\()',head)
    if not m: continue
    name=m.group(1).strip().replace('\\\n','').replace('\n',' ')
    name=re.sub(r'\s+',' ',name)
    if name in sys.argv[2:] or any(a.startswith('~') and re.search(a[1:],name) for a in sys.argv[2:]):
        print('##',re.sub(r'\s+',' ',head.replace('\\\n',' ')).strip()[:900]); 
