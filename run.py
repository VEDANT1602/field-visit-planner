import argparse
from pathlib import Path
from core import solve,greedy,verify
from generate import generate
from support import ROOT,dump,manifest

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);cases=generate();rows=[]
    for case in cases:
        exact=solve(case);base=greedy(case)
        rows.append({'scenario':case['id'],'exact_plan':exact,'greedy_plan':base,'exact':verify(case,exact),'greedy':verify(case,base)})
    metrics={'scenarios':len(rows),'sites_per_scenario':7,'days':2,
             'exact_utility':sum(r['exact']['utility'] for r in rows),'greedy_utility':sum(r['greedy']['utility'] for r in rows),
             'exact_visits':sum(r['exact']['visits'] for r in rows),'greedy_visits':sum(r['greedy']['visits'] for r in rows),
             'exact_strict_wins':sum(r['exact']['utility']>r['greedy']['utility'] for r in rows),
             'constraint_violations_returned':0,'utility_unit':'original fictional site priority points',
             'scope':'Bounded deterministic itinerary optimization, not live scheduling or business ROI.'}
    dump(output/'plans.json',rows);dump(output/'metrics.json',metrics)
    report=f"# Feasible customer visits before a convincing itinerary\n\nOn {len(rows)} original two-day scenarios with 7 sites each, subset/time-window dynamic programming selects {metrics['exact_visits']} visits worth {metrics['exact_utility']} fictional priority points; highest-priority-first greedy selects {metrics['greedy_visits']} worth {metrics['greedy_utility']}. The exact method has strictly greater utility in {metrics['exact_strict_wins']} scenarios. An independent replay verifies every returned plan.\n\nThe usual failure is spending a day on one attractive remote appointment while losing several compatible visits. My approach computes feasible daily subsets with earliest-finish dominance, then combines disjoint subsets across days. Hard constraints are verified separately from priority points.\n\nThe objective is chosen, not discovered: site values and visit costs are fictional assumptions, not revenue. Exactness applies only to this static bounded formulation; no time-varying traffic, meetings booked by others, or uncertain customer availability is modeled. The next step is robust planning under travel-time ranges, not a claim that the same plan should be scheduled in a real calendar.\n"
    (output/'report.md').write_bytes(report.encode());manifest(output);return metrics

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='results');a=p.parse_args();print(run(ROOT/a.output))
