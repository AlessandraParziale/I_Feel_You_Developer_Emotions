import re,os,sys,json,collections,javalang
D4J=sys.argv[1] if len(sys.argv)>1 else 'bench/d4j'
GS=re.compile(r'^(get|is|has)[A-Z0-9_]'); SS=re.compile(r'^set[A-Z0-9_]')
def changed_lines(patch):
    out=[]; b=None
    for l in open(patch,errors='ignore'):
        m=re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@',l)
        if m: b=int(m.group(1)); continue
        if b is None or l.startswith(('diff','---','+++','index','\\')): continue
        t=l[1:].strip()
        trivial= t=='' or t in ('{','}','};') or re.match(r'^(import|package)\b',t) or t.startswith(('//','/*','*','*/'))
        if l.startswith('+'):
            if not trivial: out.append(b)
            b+=1
        elif l.startswith('-'):
            if not trivial: out.append(b)
        else: b+=1
    return out
def spans_of(code):
    lines=code.split('\n')
    def end_of(start):
        depth=0; seen=False
        for i in range(start-1,len(lines)):
            s=re.sub(r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|//.*','',lines[i])
            for ch in s:
                if ch=='{': depth+=1; seen=True
                elif ch=='}':
                    depth-=1
                    if seen and depth==0: return i+1
        return len(lines)
    tree=javalang.parse.parse(code); sp=[]
    for _,n in tree.filter(javalang.tree.MethodDeclaration):
        if n.position and n.body is not None:
            st=n.position.line; sp.append(dict(name=n.name,start=st,end=end_of(st),ctor=False,node=n))
    for _,n in tree.filter(javalang.tree.ConstructorDeclaration):
        if n.position: st=n.position.line; sp.append(dict(name=n.name,start=st,end=end_of(st),ctor=True,node=n))
    return sp,len(lines)
def is_accessor(s):
    n=s['node']; body=n.body or []; np=len(n.parameters)
    if GS.match(s['name']) and np==0 and len(body)==1 and isinstance(body[0],javalang.tree.ReturnStatement): return True
    if SS.match(s['name']) and np==1 and len(body)==1 and isinstance(body[0],javalang.tree.StatementExpression): return True
    return False
def calls(node):
    return {(m.member,len(m.arguments or [])) for _,m in node.filter(javalang.tree.MethodInvocation) if m.qualifier in (None,'','this')}
res={}
for l in open('jobs.tsv'):
    p,b,repo,c,path=l.rstrip('\n').split('\t')
    r=dict(project=p,bug=b)
    code=open(f'buggy/{p}_{b}.java',errors='ignore').read()
    try: sp,nl=spans_of(code)
    except Exception as ex: r['status']='parse_error'; res[f'{p}_{b}']=r; continue
    r['lines']=nl
    ch=changed_lines(f'{D4J}/framework/projects/{p}/patches/{b}.src.patch')
    owners=set(); outside=False
    for x in ch:
        inn=[s for s in sp if s['start']<=x<=s['end']]
        if not inn: outside=True; continue
        s=min(inn,key=lambda s:s['end']-s['start']); owners.add((s['name'],s['start']))
    r['single_method']= (not outside) and len(owners)==1 and len(ch)>0
    if r['single_method']:
        fname,fstart=next(iter(owners)); f=[s for s in sp if s['start']==fstart][0]
        r['faulty']=fname; r['faulty_ctor']=f['ctor']
        tt=open(f'{D4J}/framework/projects/{p}/trigger_tests/{b}',errors='ignore').read()
        base=os.path.basename(path)
        frames=[(m.group(1),int(m.group(2))) for m in re.finditer(r'\.([\w$<>]+)\('+re.escape(base)+r':(\d+)\)',tt)]
        fcalls=calls(f['node'])
        cands=[]
        for s in sp:
            if s['ctor'] or s['name']==fname or is_accessor(s): continue
            why=[]
            if any(n==s['name'] and s['start']<=ln<=s['end'] for n,ln in frames): why.append('stack')
            if (s['name'],len(s['node'].parameters)) in fcalls: why.append('callee')
            if (fname,len(f['node'].parameters)) in calls(s['node']): why.append('caller')
            if why: cands.append((s['name'],why))
        names={}
        for n,w in cands: names.setdefault(n,set()).update(w)
        r['candidates']={k:sorted(v) for k,v in names.items()}
    res[f'{p}_{b}']=r
json.dump(res,open('selection.json','w'),indent=1,default=str)

v=list(res.values())
s1=[x for x in v if x.get('single_method')]
s2=[x for x in s1 if x.get('candidates')]
s3=[x for x in s2 if x['lines']<=3000]
print('Single-file bugs:', len(v))
print('(i)   fix modifies a single method:', len(s1))
print('(ii)  at least one candidate incorrect cause:', len(s2))
print('(iii) file of at most 3,000 lines:', len(s3))
print('B =', len(s3), ' P =', len({x['project'] for x in s3}))
print(dict(collections.Counter(x['project'] for x in s3)))
with open('selected_bugs.csv','w') as f:
    f.write('project,bug_id,faulty_method,file_lines,candidates\n')
    for x in sorted(s3,key=lambda x:(x['project'],int(x['bug']))):
        f.write(f"{x['project']},{x['bug']},{x['faulty']},{x['lines']},\"{'; '.join(sorted(x['candidates']))}\"\n")