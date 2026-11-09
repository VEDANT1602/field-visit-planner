import copy
import itertools
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core import solve,greedy,verify,validate
from generate import generate
from support import verify_manifest

class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.case={'days':1,'horizon':100,'daily_budget':3,'travel':[[0,5,5,5],[5,0,5,5],[5,5,0,5],[5,5,5,0]],
          'visits':[{'id':str(i),'duration':20,'cost':c,'utility':u,'windows':{'0':[0,100]}} for i,c,u in [(0,3,9),(1,1,6),(2,1,6)]]}
    def test_exact_known_better_subset(self):
        self.assertEqual(12,verify(self.case,solve(self.case))['utility']);self.assertEqual(9,verify(self.case,greedy(self.case))['utility'])
    def test_small_case_matches_exhaustive_route_oracle(self):
        best=0;ids=[v['id'] for v in self.case['visits']]
        for size in range(4):
            for route in itertools.permutations(ids,size):
                try:best=max(best,verify(self.case,[{'day':0,'route':list(route)}])['utility'])
                except ValueError:pass
        self.assertEqual(best,verify(self.case,solve(self.case))['utility'])
    def test_no_calendar_window_means_no_visit(self):
        for v in self.case['visits']:v['windows']={}
        self.assertEqual(0,verify(self.case,solve(self.case))['visits'])
    def test_duplicate_visit_across_days_refused(self):
        self.case['days']=2;self.case['visits'][0]['windows']['1']=[0,100]
        with self.assertRaises(ValueError):verify(self.case,[{'day':0,'route':['0']},{'day':1,'route':['0']}])
    def test_return_to_depot_is_hard_constraint(self):
        self.case['travel'][1][0]=100
        with self.assertRaises(ValueError):verify(self.case,[{'day':0,'route':['0']}])
    def test_noninteger_or_bool_budget_rejected(self):
        for x in [True,float('nan'),float('inf'),3.0,-1]:
            c=copy.deepcopy(self.case);c['daily_budget']=x
            with self.assertRaises(ValueError):validate(c)
    def test_request_size_bound(self):
        self.case['days']=4
        with self.assertRaises(ValueError):solve(self.case)
    def test_noncanonical_day_keys_rejected_before_planning(self):
        for key in [0,'01','00']:
            c=copy.deepcopy(self.case);c['days']=2;c['visits'][0]['windows']={key:[0,100]}
            with self.subTest(key=key),self.assertRaises(ValueError):validate(c)
    def test_exact_never_loses_greedy_in_seeded_scenarios(self):
        for c in generate()[:5]:self.assertGreaterEqual(verify(c,solve(c))['utility'],verify(c,greedy(c))['utility'])
    def test_committed_manifest(self):verify_manifest()
