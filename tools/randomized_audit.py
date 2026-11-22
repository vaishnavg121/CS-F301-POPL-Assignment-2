"""Independent property audit of actual Racket source with local restricted evaluator.
Not an execution under Racket itself.
"""
import random
from pathlib import Path
from offline_scheme_sim import Sym, load, evaluate
rnd=random.Random(20261122)
root=Path(__file__).resolve().parents[1] / 'code'
s1,out1=load(root/'id_q3.rkt')

def reference_tree(t):
    if not t:return [],[],[],0,0
    v,l,r=t
    il,pl,ql,hl,ll=reference_tree(l)
    ir,pr,qr,hr,lr=reference_tree(r)
    return il+[v]+ir,[v]+pl+pr,ql+qr+[v],1+max(hl,hr),1 if not l and not r else ll+lr

def make_tree(depth):
    if depth==0 or rnd.randrange(5)==0:return []
    return [rnd.choice([0,1,2,3,Sym('a'),Sym('b')]),make_tree(depth-1),make_tree(depth-1)]

def scheme_str(x):
    if isinstance(x,list):return '('+' '.join(scheme_str(y) for y in x)+')'
    return str(x)

for i in range(100):
    t=make_tree(5)
    expected=reference_tree(t)
    out1.clear()
    evaluate([Sym('print-all-traversals'),[Sym('quote'),t]],s1)
    evaluate([Sym('print-height-and-leaves'),[Sym('quote'),t]],s1)
    want=''.join(scheme_str(v)+'\n' for v in [expected[0],expected[1],expected[2],list(expected[3:])])
    actual=''.join(out1)
    assert actual==want,(i,actual,want)
print('S1: 100 reproducible randomized trees matched independent reference traversal and height/leaves logic')

s2,out2=load(root/'id_q4.rkt')

def make_nested(depth):
    if depth<=0:return []
    return [make_nested(depth-1) if rnd.random() < 0.38 else rnd.choice([0,1,2,Sym('a'),Sym('b')]) for _ in range(rnd.randrange(5))]

def expected_insert(x,lst,n):
    mapped=[expected_insert(x,e,n) if isinstance(e,list) else e for e in lst]
    return ([x]+mapped) if len(lst)<n else mapped

for i in range(150):
    x=rnd.choice([0,7,Sym('z')])
    nested=make_nested(5)
    n=rnd.randrange(7)
    got=s2.getvar('insert-if-short')(x,nested,n)
    want=expected_insert(x,nested,n)
    assert got==want,(i,nested,n,got,want)
print('S2: 150 randomized nested-list cases matched an independent reference transformer')

# Deep nesting, but without requiring runtime-specific tail-call behavior.
level=[]
for i in range(100):level=[level]
out=s2.getvar('insert-if-short')(42,level,2)
assert out==expected_insert(42,level,2)
print('S2: 100-level nested-list case matched the reference transformer')
