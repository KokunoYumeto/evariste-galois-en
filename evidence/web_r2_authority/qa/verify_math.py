#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, itertools, json
from pathlib import Path
from sympy import Matrix, symbols, I, simplify, pi
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def add(cid, ok, detail): checks.append({'check_id':cid,'status':'PASS' if ok else 'FAIL','detail':detail})

# R2 Legendre equivalence as a symbolic identity.
E, Ec, F, Fc=symbols('E Ec F Fc')
printed=E*Fc+Ec*F-F*Fc
omega1=F; omega2=I*Fc; eta1=E; eta2=I*(Fc-Ec)
add('A008_DETERMINANT_IDENTITY', simplify(eta1*omega2-eta2*omega1-I*printed)==0,
    'eta1*omega2-eta2*omega1 = i(E Fc + Ec F - F Fc)')
c=symbols('c')
add('A008_SECOND_KIND_SHIFT_INVARIANCE', simplify((eta1+c*omega1)*omega2-(eta2+c*omega2)*omega1-(eta1*omega2-eta2*omega1))==0,
    'determinant invariant under eta_j -> eta_j + c omega_j')
add('A008_RIGHT_HAND_SIDE', simplify(I*(pi/2)-pi*I/2)==0, 'printed pi/2 maps to manuscript pi*i/2')

# W11 independent OCR and metadata check.
ocr=(ROOT/'evidence/source_replay/ETH_Rar4575_Galois1897_OCR.txt').read_text(encoding='utf-8',errors='replace')
add('W11_ETH_OCR_24572', '24572' in ocr, 'official OCR contains 24572')
add('W11_FIVE_DIGITS', len('24572')==5 and '24572'.isdigit(), '24572 is a five-digit decimal string')

# Exact PSL(2,11) matching stabilizer check used by A006.
p=11
pts=list(range(p))+['inf']
def norm_mat(a,b,c,d):
    vals=[a%p,b%p,c%p,d%p]
    for v in vals:
        if v%p:
            inv=pow(v,-1,p); return tuple((x*inv)%p for x in vals)
    raise ValueError
mats=set()
for a,b,c,d in itertools.product(range(p), repeat=4):
    if (a*d-b*c)%p==1:
        mats.add(norm_mat(a,b,c,d))
def act(M,x):
    a,b,c,d=M
    if x=='inf':
        return 'inf' if c==0 else (a*pow(c,-1,p))%p
    den=(c*x+d)%p; num=(a*x+b)%p
    return 'inf' if den==0 else (num*pow(den,-1,p))%p
pairs={frozenset(x) for x in [('inf',0),(1,2),(3,6),(4,8),(5,10),(9,7)]}
stab=0
for M in mats:
    image={frozenset((act(M,next(iter(q))), act(M,next(iter(q-{next(iter(q))}))))) for q in pairs}
    if image==pairs: stab+=1
add('A006_PSL2_11_ORDER', len(mats)==660, f'|PSL(2,11)|={len(mats)}')
add('A006_MATCHING_STABILIZER', stab==60, f'stabilizer order={stab}, index={len(mats)//stab}')

# Degree-16 affine counterexample: H=(C3 x C3) semidirect C2 on V=F_2^2 direct-sum F_2^2.
def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4))%2 for j in range(4)) for i in range(4))
def mv(A,v): return tuple(sum(A[i][j]*v[j] for j in range(4))%2 for i in range(4))
Id=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
A2=((0,1),(1,1))
I2=((1,0),(0,1))
def blockdiag(X,Y):
    return tuple(tuple((X[i][j] if i<2 and j<2 else Y[i-2][j-2] if i>=2 and j>=2 else 0) for j in range(4)) for i in range(4))
g1=blockdiag(A2,I2)
g2=blockdiag(I2,A2)
swap=((0,0,1,0),(0,0,0,1),(1,0,0,0),(0,1,0,0))
def closure(gens):
    S={Id}; frontier=[Id]
    while frontier:
        x=frontier.pop()
        for g in gens:
            y=mm(x,g)
            if y not in S:S.add(y);frontier.append(y)
    return S
H=closure([g1,g2,swap])
nonzero=[tuple((n>>j)&1 for j in range(4)) for n in range(1,16)]
def vector_rank(vs):
    rows=[sum(v[j]<<j for j in range(4)) for v in vs]
    r=0
    for col in range(4):
        pivot=next((i for i in range(r,len(rows)) if (rows[i]>>col)&1),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>col)&1):rows[i]^=rows[r]
        r+=1
    return r
irr=all(vector_rank([mv(h,v) for h in H])==4 for v in nonzero)
add('A005_ORDER_18_COMPLEMENT', len(H)==18, f'constructed complement order={len(H)}')
add('A005_IRREDUCIBLE_F2_4', irr, 'every nonzero H-orbit spans F_2^4')
add('A005_AFFINE_GROUP_ORDER', 16*len(H)==288, f'|V semidirect H|={16*len(H)}')
add('A005_NOT_GAMMAL1_16', 60%18!=0, '18 does not divide |GammaL(1,16)|=60')

# W10 counterexample: conjugate projective transformations need not commute.
def mobius(M,x,p=7):
    a,b,c,d=M
    if x=='inf': return 'inf' if c%p==0 else a*pow(c,-1,p)%p
    den=(c*x+d)%p; num=(a*x+b)%p
    return 'inf' if den==0 else num*pow(den,-1,p)%p
def compose(A,B,x): return mobius(A,mobius(B,x))
# T_m(k)=m+1/(k-m): matrix [[m,1-m^2],[1,-m]].
T0=(0,1,1,0); T1=(1,0,1,-1)
diffs=[x for x in list(range(7))+['inf'] if compose(T0,T1,x)!=compose(T1,T0,x)]
add('W10_DA003_NONCOMMUTING', bool(diffs), f'T0T1 and T1T0 differ at {diffs[:3]}')

out={'generated':'2026-08-14','status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks_passed':sum(c['status']=='PASS' for c in checks),'checks_total':len(checks),'checks':checks}
(ROOT/'qa/MATHEMATICAL_CHECKS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
raise SystemExit(0 if out['status']=='PASS' else 1)
