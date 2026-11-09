import math
import random
from support import ROOT,dump

def generate():
    rng=random.Random(1602);cases=[]
    for k in range(30):
        n=7;days=2;coords=[(0,0)]+[(rng.randint(0,45),rng.randint(0,45)) for _ in range(n)]
        travel=[[0 if i==j else math.ceil(math.dist(a,b)) for j,b in enumerate(coords)] for i,a in enumerate(coords)]
        visits=[]
        for i in range(n):
            windows={}
            for d in range(days):
                if rng.random()<0.8:
                    opening=rng.randrange(0,120,15);windows[str(d)]=[opening,min(240,opening+rng.choice([60,90,120]))]
            visits.append({'id':f'site-{i}','duration':rng.choice([20,30,45]),'cost':rng.randint(1,4),'utility':rng.randint(2,12),'windows':windows})
        cases.append({'id':f'fixture-{k:02d}','days':days,'horizon':240,'daily_budget':8,'visits':visits,'travel':travel})
    dump(ROOT/'data/scenarios.json',cases);return cases
