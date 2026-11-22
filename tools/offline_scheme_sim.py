"""Independent Python evaluator for the small permitted Scheme subset.
For a secondary logic check only. NOT a substitute for Racket 8.x.
"""
from dataclasses import dataclass
from pathlib import Path
import re
import sys
sys.setrecursionlimit(10000)

@dataclass(frozen=True)
class Sym:
    value: str
    def __str__(self): return self.value

class Env(dict):
    def __init__(self, parent=None, **kwargs):
        super().__init__(kwargs); self.parent=parent
    def getvar(self, key):
        if key in self: return self[key]
        if self.parent is not None: return self.parent.getvar(key)
        raise NameError(f'Unbound variable {key}')

class Closure:
    def __init__(self, params, body, env): self.params=params; self.body=body; self.env=env
    def __call__(self, *args):
        if len(args)!=len(self.params): raise TypeError((self.params,args))
        ctx=Env(self.env)
        ctx.update(zip(self.params,args))
        ret=None
        for f in self.body: ret=evaluate(f,ctx)
        return ret


def tokenize(text):
    lines=[l.split(';',1)[0] for l in text.splitlines() if not l.lstrip().startswith('#lang ')]
    s='\n'.join(lines)
    return re.findall(r"\'|\(|\)|[^\s()']+",s)

def parse_all(src):
    tokens=tokenize(src); cursor=0
    def parse():
        nonlocal cursor
        a=tokens[cursor];cursor+=1
        if a=='(':
            ret=[]
            while tokens[cursor]!=')': ret.append(parse())
            cursor+=1
            return ret
        if a=="'": return [Sym('quote'),parse()]
        if a==')': raise ValueError('extra paren')
        try: return int(a)
        except ValueError: return Sym(a)
    forms=[]
    while cursor<len(tokens): forms.append(parse())
    return forms

def sym(x): return isinstance(x,Sym)
def name(x):
    if not sym(x): raise TypeError(x)
    return x.value

def scheme_repr(v):
    if isinstance(v,list): return '('+' '.join(map(scheme_repr,v))+')'
    if sym(v): return v.value
    if isinstance(v,bool): return '#t' if v else '#f'
    return str(v)

def evaluate(form,ctx):
    if sym(form):return ctx.getvar(form.value)
    if not isinstance(form,list):return form
    if not form:return []
    op=form[0]
    if sym(op):
        symbol=name(op)
        if symbol=='quote':return form[1]
        if symbol=='define':
            if isinstance(form[1],list):
                signature=form[1]
                ctx[name(signature[0])]=Closure([name(x) for x in signature[1:]],form[2:],ctx)
            else:ctx[name(form[1])]=evaluate(form[2],ctx)
            return None
        if symbol=='lambda':return Closure([name(x) for x in form[1]],form[2:],ctx)
        if symbol=='letrec':
            c=Env(ctx)
            for binding in form[1]:c[name(binding[0])]=None
            for binding in form[1]:c[name(binding[0])]=evaluate(binding[1],c)
            ret=None
            for f in form[2:]:ret=evaluate(f,c)
            return ret
        if symbol=='let' or symbol=='let*':
            if sym(form[1]):
                ident=name(form[1]); c=Env(ctx); bindings=form[2]
                args=[evaluate(b[1],ctx) for b in bindings]
                clos=Closure([name(b[0]) for b in bindings],form[3:],c)
                c[ident]=clos
                return clos(*args)
            c=Env(ctx)
            for binding in form[1]:
                c[name(binding[0])]=evaluate(binding[1],c if symbol=='let*' else ctx)
            ret=None
            for f in form[2:]:ret=evaluate(f,c)
            return ret
        if symbol=='if':return evaluate(form[2] if truth(evaluate(form[1],ctx)) else form[3],ctx)
        if symbol=='and':
            res=True
            for f in form[1:]:
                res=evaluate(f,ctx)
                if not truth(res):return res
            return res
        if symbol=='or':
            for f in form[1:]:
                res=evaluate(f,ctx)
                if truth(res):return res
            return False
        if symbol=='begin':
            ret=None
            for f in form[1:]:ret=evaluate(f,ctx)
            return ret
        if symbol=='cond':
            for clause in form[1:]:
                if name(clause[0])=='else' or truth(evaluate(clause[0],ctx)):
                    ret=None
                    for f in clause[1:]:ret=evaluate(f,ctx)
                    return ret
            return False
    fn=evaluate(op,ctx)
    return fn(*(evaluate(arg,ctx) for arg in form[1:]))

def truth(a):return a is not False

def primitives(ctx, output):
    def operate(op):
        return lambda a,*args: ({'+':lambda:sum((a,*args)),
                                 '-':lambda:a-sum(args) if args else -a,
                                 '*':lambda:prod((a,*args)),
                                 '<':lambda:compare((a,*args),lambda x,y:x<y),
                                 '>':lambda:compare((a,*args),lambda x,y:x>y),
                                 '<=':lambda:compare((a,*args),lambda x,y:x<=y),
                                 '>=':lambda:compare((a,*args),lambda x,y:x>=y),
                                 '=':lambda:compare((a,*args),lambda x,y:x==y)}[op])()
    def prod(xs):
        n=1
        for x in xs:n*=x
        return n
    def compare(vals,fn):return all(fn(x,y) for x,y in zip(vals,vals[1:]))
    def car(v):return v[0]
    def cdr(v):return v[1:]
    def cons(a,b):return [a]+b
    def emit(v):output.append(scheme_repr(v))
    builtin={'null?':lambda x:x==[], 'pair?':lambda x:isinstance(x,list) and bool(x),
             'not':lambda x:not truth(x), 'eq?':lambda x,y:x==y,
             'car':car,'cdr':cdr,'cons':cons,'list':lambda *x:list(x),
             'max':max,'display':emit,'newline':lambda:output.append('\n')}
    for op in ['+','-','*','<','>','<=','>=','=']:builtin[op]=operate(op)
    for chars in ['cadr','caddr','cdddr','cadddr','cddddr','cddr','cdar','caar','cadar']:
        def make(chars):
            def get(v):
                for a in chars[-2:0:-1]:v=car(v) if a=='a' else cdr(v)
                return v
            return get
        builtin[chars]=make(chars)
    ctx.update(builtin)

def load(file):
    out=[]; env=Env();primitives(env,out)
    for form in parse_all(Path(file).read_text()):evaluate(form,env)
    return env,out

def check():
    root=Path(__file__).resolve().parents[1] / 'code'
    s1,o1=load(root/'id_q3.rkt')
    assert not o1
    tree=[4,[2,[1,[],[]],[3,[],[]]],[6,[5,[],[]],[7,[],[]]]]
    evaluate([Sym('print-inorder'),[Sym('quote'),tree]],s1)
    evaluate([Sym('print-all-traversals'),[Sym('quote'),tree]],s1)
    evaluate([Sym('print-height-and-leaves'),[Sym('quote'),tree]],s1)
    got=''.join(o1)
    expect='(1 2 3 4 5 6 7)\n'*2+'(4 2 1 3 6 5 7)\n(1 3 2 5 7 6 4)\n(3 4)\n'
    assert got==expect,(got,expect)
    print('S1 sample checked against actual Racket source forms using Python subset evaluator')
    s2,o2=load(root/'id_q4.rkt')
    assert not o2
    cases=[(42,[[1,2],[3,4,5],[6],[]],3,[[42,1,2],[3,4,5],[42,6],[42]]),
           (0,[[[1],2],[3],[[4,5,6],[]]],3,[[0,[0,1],2],[0,3],[0,[4,5,6],[0]]]),
           (7,[],3,[7]),(7,[],0,[]),
           (Sym('z'),[[Sym('a')],[]],2,[[Sym('z'),Sym('a')],[Sym('z')]])]
    for x,lst,n,expected in cases:
        got=s2.getvar('insert-if-short')(x,lst,n)
        assert got==expected,(x,lst,n,got,expected)
    for n in [0,1,2,3,10]:
        def reference(x,lst):
            nested=[reference(x,e) if isinstance(e,list) else e for e in lst]
            return ([x]+nested) if len(lst)<n else nested
        examples=[[],[1,2,3],[[],[1],[]],[[1],[2,3],[[4],[]]]]
        for lst in examples:
            got=s2.getvar('insert-if-short')(99,lst,n)
            assert got==reference(99,lst),(n,lst,got)
    print('S2 documented examples and additional nested/threshold cases passed Python subset evaluator')

if __name__=='__main__':check()
