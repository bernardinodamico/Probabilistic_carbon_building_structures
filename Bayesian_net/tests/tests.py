import unittest
from Bayesian_net.Build_ProbTables import Build_ProbTables
from Bayesian_net.variable_elimination import VariableElimination
from random import randint

class TestBuild_ProbTables(unittest.TestCase):
    maxDiff = None
    probTables = Build_ProbTables()
    varElim = VariableElimination()
    probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")
    
    def get_probs_as_list(self, d1: dict, d2: dict = None, precision: int = 3) -> list | list:
        l1 = []
        l2 = []
        pr_key = list(d1)[-1]
        for k in d1[pr_key]:
            l1.append(round(d1[pr_key][k], precision))
            if d2 is not None: 
                l2.append(round(d2[pr_key][k], precision)) 
        return l1, l2

    def test_marginal_probs(self):
        
        mpt = self.probTables.bld_pr_table(vars=['Temp'])
        mpt = mpt.table.to_dict()
        bench = {'Temp': {0: 3.5, 1: 10.2, 2: 26.8}, 'Pr(Temp)': {0: 0.5, 1: 0.2857142857142857, 2: 0.21428571428571427}}

        mpt, bench = self.get_probs_as_list(d1=mpt, d2=bench)
        self.assertEqual(mpt, bench, 'marginal prob table error')
 
        mpt2 = self.probTables.bld_pr_table(vars=['Weather'])
        mpt2 = mpt2.table.to_dict()
        bench2 = {'Weather': {0: 'cloudy', 1: 'rain', 2: 'sunny'}, 'Pr(Weather)': {0: 0.35714285714285715, 1: 0.35714285714285715, 2: 0.2857142857142857}}

        mpt2, bench2 = self.get_probs_as_list(d1=mpt2, d2=bench2)
        self.assertEqual(mpt2, bench2, 'marginal prob table error')

        mpt3 = self.probTables.bld_pr_table(vars=['Wildfire'])
        mpt3 = mpt3.table.to_dict()
        bench3 = {'Wildfire': {0: False, 1: True}, 'Pr(Wildfire)': {0: 0.6428571428571429, 1: 0.35714285714285715}}

        mpt3, bench3 = self.get_probs_as_list(d1=mpt3, d2=bench3)
        self.assertEqual(mpt3, bench3, 'marginal prob table error')

        #test Laplace smoothing---------------------------------------------
        param = randint(0, 8)
        smoothed_mpt = self.probTables.bld_pr_table(vars=['Temp'], K=param)
        smoothed_mpt, _ = self.get_probs_as_list(smoothed_mpt.table.to_dict())
        self.assertAlmostEqual(round(sum(smoothed_mpt), 7), 1., f'Laplace smoothing error: marginal probs do not sum up to 1. with K={param}')

        param = randint(0, 8)
        smoothed_mpt = self.probTables.bld_pr_table(vars=['Weather'], K=param)
        smoothed_mpt, _ = self.get_probs_as_list(smoothed_mpt.table.to_dict())
        self.assertAlmostEqual(round(sum(smoothed_mpt), 7), 1., f'Laplace smoothing error: marginal probs do not sum up to 1. with K={param}')

        param = randint(0, 8)
        smoothed_mpt = self.probTables.bld_pr_table(vars=['Wildfire'], K=param)
        smoothed_mpt, _ = self.get_probs_as_list(smoothed_mpt.table.to_dict())
        self.assertAlmostEqual(round(sum(smoothed_mpt), 7), 1., f'Laplace smoothing error: marginal probs do not sum up to 1. with K={param}')

    def test_joint_probs(self):
        jpt = self.probTables.bld_pr_table(vars=['Temp', 'Weather', 'Wildfire'])
        jpt = jpt.table.to_dict()

        bench = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 3.5, 4: 3.5, 5: 3.5, 6: 10.2, 7: 10.2, 8: 10.2, 9: 10.2, 10: 10.2, 11: 10.2, 12: 26.8, 13: 26.8, 14: 26.8, 15: 26.8, 16: 26.8, 17: 26.8}, 
                 'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny', 6: 'cloudy', 7: 'cloudy', 8: 'rain', 9: 'rain', 10: 'sunny', 11: 'sunny', 12: 'cloudy', 13: 'cloudy', 14: 'rain', 15: 'rain', 16: 'sunny', 17: 'sunny'}, 
                 'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True, 8: False, 9: True, 10: False, 11: True, 12: False, 13: True, 14: False, 15: True, 16: False, 17: True}, 
                 'Pr(Temp, Weather, Wildfire)': {0: 0.14285714285714285, 1: 0.0, 2: 0.21428571428571427, 3: 0.07142857142857142, 4: 0.0, 5: 0.07142857142857142, 6: 0.07142857142857142, 7: 0.07142857142857142, 8: 0.07142857142857142, 9: 0.0, 10: 0.07142857142857142, 11: 0.0, 12: 0.07142857142857142, 13: 0.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.14285714285714285}
                 }
        
        jpt, bench = self.get_probs_as_list(d1=jpt, d2=bench)
        self.assertEqual(jpt, bench, 'joint prob table error')



        jpt2 = self.probTables.bld_pr_table(vars=['Temp', 'Weather'])
        jpt2 = jpt2.table.to_dict()

        bench2 = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 10.2, 4: 10.2, 5: 10.2, 6: 26.8, 7: 26.8, 8: 26.8}, 
                  'Weather': {0: 'cloudy', 1: 'rain', 2: 'sunny', 3: 'cloudy', 4: 'rain', 5: 'sunny', 6: 'cloudy', 7: 'rain', 8: 'sunny'}, 
                  'Pr(Temp, Weather)': {0: 0.14285714285714285, 1: 0.2857142857142857, 2: 0.07142857142857142, 3: 0.14285714285714285, 4: 0.07142857142857142, 5: 0.07142857142857142, 6: 0.07142857142857142, 7: 0.0, 8: 0.14285714285714285}
                  }
        
        jpt2, bench2 = self.get_probs_as_list(d1=jpt2, d2=bench2)
        self.assertEqual(jpt2, bench2, 'joint prob table error')



        jpt3 = self.probTables.bld_pr_table(vars=['Temp', 'Wildfire'])
        jpt3 = jpt3.table.to_dict()

        bench3 = {'Temp': {0: 3.5, 1: 3.5, 2: 10.2, 3: 10.2, 4: 26.8, 5: 26.8}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 
                  'Pr(Temp, Wildfire)': {0: 0.35714285714285715, 1: 0.14285714285714285, 2: 0.21428571428571427, 3: 0.07142857142857142, 4: 0.07142857142857142, 5: 0.14285714285714285}
                  }
        
        jpt3, bench3 = self.get_probs_as_list(d1=jpt3, d2=bench3)
        self.assertEqual(jpt3, bench3, 'joint prob table error')



        jpt4 = self.probTables.bld_pr_table(vars=['Weather', 'Wildfire'])
        jpt4 = jpt4.table.to_dict()

        bench4 = {'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny'}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 'Pr(Weather, Wildfire)': {0: 0.2857142857142857, 1: 0.07142857142857142, 2: 0.2857142857142857, 3: 0.07142857142857142, 4: 0.07142857142857142, 5: 0.21428571428571427}
                  }
        
        jpt4, bench4 = self.get_probs_as_list(d1=jpt4, d2=bench4)
        self.assertEqual(jpt4, bench4, 'joint prob table error')

    def test_conditional_probs(self):
        
        cpt = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather', 'Wildfire'])
        cpt = cpt.table.to_dict()

        bench = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 3.5, 4: 3.5, 5: 3.5, 6: 10.2, 7: 10.2, 8: 10.2, 9: 10.2, 10: 10.2, 11: 10.2, 12: 26.8, 13: 26.8, 14: 26.8, 15: 26.8, 16: 26.8, 17: 26.8}, 
                 'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny', 6: 'cloudy', 7: 'cloudy', 8: 'rain', 9: 'rain', 10: 'sunny', 11: 'sunny', 12: 'cloudy', 13: 'cloudy', 14: 'rain', 15: 'rain', 16: 'sunny', 17: 'sunny'}, 
                 'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True, 8: False, 9: True, 10: False, 11: True, 12: False, 13: True, 14: False, 15: True, 16: False, 17: True}, 
                 'Pr(Temp | Weather, Wildfire)': {0: 0.5, 1: 0.0, 2: 0.75, 3: 1.0, 4: 0.0, 5: 0.3333333333333333, 6: 0.25, 7: 1.0, 8: 0.25, 9: 0.0, 10: 1.0, 11: 0.0, 12: 0.25, 13: 0.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.6666666666666666}
                 }

        cpt, bench = self.get_probs_as_list(d1=cpt, d2=bench)
        self.assertEqual(cpt, bench, 'cond. prob. table error')


        cpt2 = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Wildfire'])
        cpt2 = cpt2.table.to_dict()
        
        bench2 = {'Temp': {0: 3.5, 1: 3.5, 2: 10.2, 3: 10.2, 4: 26.8, 5: 26.8}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 
                  'Pr(Temp | Wildfire)': {0: 0.5555555555555555, 1: 0.4, 2: 0.3333333333333333, 3: 0.2, 4: 0.11111111111111111, 5: 0.4}}

        cpt2, bench2 = self.get_probs_as_list(d1=cpt2, d2=bench2)
        self.assertEqual(cpt2, bench2, 'cond. prob. table error')

        #test Laplace smoothing---------------------------------------------
        param = randint(0, 8)
        smoothed_cpt = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather', 'Wildfire'], K=param)
        smoothed_cpt, _ = self.get_probs_as_list(smoothed_cpt.table.to_dict())
        self.assertAlmostEqual(round(sum(smoothed_cpt)/6., 3), 1., f'Laplace smoothing error: cond. probs do not sum up to 1. with K={param}')
        
        param = randint(0, 8)
        smoothed_cpt2 = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather'], K=param)
        smoothed_cpt2, _ = self.get_probs_as_list(smoothed_cpt2.table.to_dict())
        self.assertAlmostEqual(round(sum(smoothed_cpt2)/3., 3), 1., f'Laplace smoothing error: cond. probs do not sum up to 1. with K={param}')


    def test_assign_evidence(self):
        ass_vars_vals = [
            {'vr_name': 'Weather', 'val': 'rain'},
            {'vr_name': 'Wildfire', 'val': False}
            ]
        
        cpt = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather', 'Wildfire'])
        ass_cpt = self.varElim.assign_evidence(prT=cpt, assignment_vals=ass_vars_vals)
        out = ass_cpt.table.to_dict()
        bench = {'Temp': {2: 3.5, 8: 10.2, 14: 26.8}, 'Pr(Temp | Weather=rain, Wildfire=False)': {2: 0.75, 8: 0.25, 14: 0.0}}
        
        self.assertEqual(out, bench, f'assign_evidence() method error.\n Expected table = {bench}\n Obtained table = {out}')

        ass_vars_vals2 = [
            {'vr_name': 'Temp', 'val': 3.5},
            ]
        
        cpt2 = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather', 'Wildfire'])
        ass_cpt2 = self.varElim.assign_evidence(prT=cpt2, assignment_vals=ass_vars_vals2)
        out2 = ass_cpt2.table.to_dict()
        bench2 = {'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny'}, 'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 'Pr(Temp=3.5 | Weather, Wildfire)': {0: 0.5, 1: 0.0, 2: 0.75, 3: 1.0, 4: 0.0, 5: 0.3333333333333333}}
        
        self.assertEqual(out2, bench2, f'assign_evidence() method error.\n Expected table = {bench2}\n Obtained table = {out2}')

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()