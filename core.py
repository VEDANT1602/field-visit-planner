"""Exact subset/time-window planning for a deliberately bounded local problem."""

def integer(value,label,minimum=0):
    if isinstance(value,bool) or not isinstance(value,int) or value<minimum:raise ValueError(label+' must be integer >= '+str(minimum))
    return value

def validate(case):
    visits=case['visits'];days=integer(case['days'],'days',1)
    if days>3 or len(visits)>10:raise ValueError('partition requests above10sites or3days')
    integer(case['horizon'],'horizon',1);integer(case['daily_budget'],'daily_budget',1)
    ids=[v['id'] for v in visits]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids))!=len(ids):raise ValueError('unique site ids required')
    for v in visits:
        for key in ['duration','cost','utility']:integer(v[key],key,1)
        if not isinstance(v['windows'],dict):raise ValueError('windows must be object')
        for day,window in v['windows'].items():
            if not isinstance(day,str) or not day.isdigit() or day!=str(int(day)) or not 0<=int(day)<days:
                raise ValueError('day keys must be canonical decimal strings in the declared range')
            if not isinstance(window,list) or len(window)!=2:raise ValueError('window must contain opening and latest finish')
            start,end=window;integer(start,'opening');integer(end,'latest finish')
            if start>end or end>case['horizon']:raise ValueError('invalid time window')
    n=len(visits);matrix=case['travel']
    if len(matrix)!=n+1 or any(len(row)!=n+1 for row in matrix):raise ValueError('travel matrix shape')
    for i,row in enumerate(matrix):
        for j,value in enumerate(row):
            integer(value,'travel')
            if i==j and value!=0:raise ValueError('travel diagonal must be zero')
    return n

def day_routes(case,day):
    n=len(case['visits']);visits=case['visits'];travel=case['travel'];horizon=case['horizon']
    # Earliest finish dominates other paths with the same visited subset and last
    # site: utility/cost depend only on the subset, and later arrivals never help.
    states={(0,0):(0,())};routes={0:(0,())}
    for mask in range(1<<n):
        for last in range(n+1):
            if (mask,last) not in states:continue
            finish,path=states[(mask,last)]
            if finish+travel[last][0]<=horizon:
                candidate=(finish+travel[last][0],path)
                if mask not in routes or candidate<routes[mask]:routes[mask]=candidate
            used=sum(v['cost'] for i,v in enumerate(visits) if mask>>i&1)
            for i,v in enumerate(visits):
                if mask>>i&1 or str(day) not in v['windows'] or used+v['cost']>case['daily_budget']:continue
                opening,latest=v['windows'][str(day)]
                end=max(finish+travel[last][i+1],opening)+v['duration']
                if end>latest or end>horizon:continue
                key=(mask|1<<i,i+1);candidate=(end,path+(i,))
                if key not in states or candidate<states[key]:states[key]=candidate
    return routes

def solve(case):
    n=validate(case);states={0:(0,())}
    for day in range(case['days']):
        routes=day_routes(case,day);new={}
        for used,(time,plan) in states.items():
            for mask,(end,path) in routes.items():
                if used&mask:continue
                key=used|mask;candidate=(time+end,plan+(path,))
                if key not in new or candidate<new[key]:new[key]=candidate
        states=new
    best=max(states,key=lambda m:(sum(v['utility'] for i,v in enumerate(case['visits']) if m>>i&1),m.bit_count(),-states[m][0],-m))
    return [{'day':d,'route':[case['visits'][i]['id'] for i in route]} for d,route in enumerate(states[best][1])]

def greedy(case):
    validate(case);seen=set();plan=[]
    for day in range(case['days']):
        route=[];last=0;finish=0;cost=0
        while True:
            options=[]
            for i,v in enumerate(case['visits']):
                if v['id'] in seen or str(day) not in v['windows'] or cost+v['cost']>case['daily_budget']:continue
                opening,latest=v['windows'][str(day)]
                end=max(finish+case['travel'][last][i+1],opening)+v['duration']
                if end<=latest and end+case['travel'][i+1][0]<=case['horizon']:
                    options.append((-v['utility'],end,v['id'],i))
            if not options:break
            _,finish,vid,i=min(options);v=case['visits'][i];route.append(vid);seen.add(vid);cost+=v['cost'];last=i+1
        plan.append({'day':day,'route':route})
    return plan

def verify(case,plan):
    validate(case);lookup={v['id']:(i+1,v) for i,v in enumerate(case['visits'])};seen=set();days=set();trace=[];utility=0
    for item in plan:
        day=integer(item['day'],'day')
        if day>=case['days'] or day in days:raise ValueError('duplicate or invalid day')
        days.add(day);last=0;finish=0;cost=0
        for vid in item['route']:
            if vid not in lookup or vid in seen:raise ValueError('unknown or repeated site')
            index,v=lookup[vid]
            if str(day) not in v['windows']:raise ValueError('site unavailable on day')
            opening,latest=v['windows'][str(day)];arrival=finish+case['travel'][last][index]
            start=max(arrival,opening);finish=start+v['duration'];cost+=v['cost']
            if finish>latest or cost>case['daily_budget']:raise ValueError('window or budget exceeded')
            trace.append({'day':day,'site':vid,'arrival':arrival,'start':start,'finish':finish,'cost_to_date':cost})
            seen.add(vid);utility+=v['utility'];last=index
        if finish+case['travel'][last][0]>case['horizon']:raise ValueError('depot return exceeds workday')
    return {'utility':utility,'visits':len(seen),'trace':trace}
