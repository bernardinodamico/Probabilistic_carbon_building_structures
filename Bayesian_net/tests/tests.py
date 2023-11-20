import unittest
from Bayesian_net.Build_ProbTables import Build_ProbTables

class TestBuild_ProbTables(unittest.TestCase):

    probTables = Build_ProbTables()
    probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")
    
    def test_marginal_probs(self):
        
        mpt = self.probTables.bld_pr_table(vars=['Temp'])
        mpt = mpt.table.to_dict()
        bench = {'Temp': {0: 3.5, 1: 10.2, 2: 26.8}, 'Pr(Temp)': {0: 0.5, 1: 0.2857142857142857, 2: 0.21428571428571427}}

        self.assertEqual(mpt, bench, 'marginal prob table error')

        mpt2 = self.probTables.bld_pr_table(vars=['Weather'])
        mpt2 = mpt2.table.to_dict()
        bench2 = {'Weather': {0: 'cloudy', 1: 'rain', 2: 'sunny'}, 'Pr(Weather)': {0: 0.35714285714285715, 1: 0.35714285714285715, 2: 0.2857142857142857}}

        self.assertEqual(mpt2, bench2, 'marginal prob table error')

        mpt3 = self.probTables.bld_pr_table(vars=['Wildfire'])
        mpt3 = mpt3.table.to_dict()
        bench3 = {'Wildfire': {0: False, 1: True}, 'Pr(Wildfire)': {0: 0.6428571428571429, 1: 0.35714285714285715}}

        self.assertEqual(mpt3, bench3, 'marginal prob table error')

    def test_joint_probs(self):
        jpt = self.probTables.bld_pr_table(vars=['Temp', 'Weather', 'Wildfire'])
        jpt = jpt.table.to_dict()

        bench = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 3.5, 4: 3.5, 5: 3.5, 6: 10.2, 7: 10.2, 8: 10.2, 9: 10.2, 10: 10.2, 11: 10.2, 12: 26.8, 13: 26.8, 14: 26.8, 15: 26.8, 16: 26.8, 17: 26.8}, 
                 'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny', 6: 'cloudy', 7: 'cloudy', 8: 'rain', 9: 'rain', 10: 'sunny', 11: 'sunny', 12: 'cloudy', 13: 'cloudy', 14: 'rain', 15: 'rain', 16: 'sunny', 17: 'sunny'}, 
                 'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True, 8: False, 9: True, 10: False, 11: True, 12: False, 13: True, 14: False, 15: True, 16: False, 17: True}, 
                 'Pr(Temp, Weather, Wildfire)': {0: 0.14285714285714285, 1: 0.0, 2: 0.21428571428571427, 3: 0.07142857142857142, 4: 0.0, 5: 0.07142857142857142, 6: 0.07142857142857142, 7: 0.07142857142857142, 8: 0.07142857142857142, 9: 0.0, 10: 0.07142857142857142, 11: 0.0, 12: 0.07142857142857142, 13: 0.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.14285714285714285}
                 }
        
        self.assertEqual(jpt, bench, 'joint prob table error')

        jpt2 = self.probTables.bld_pr_table(vars=['Temp', 'Weather'])
        jpt2 = jpt2.table.to_dict()

        bench2 = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 10.2, 4: 10.2, 5: 10.2, 6: 26.8, 7: 26.8, 8: 26.8}, 
                  'Weather': {0: 'cloudy', 1: 'rain', 2: 'sunny', 3: 'cloudy', 4: 'rain', 5: 'sunny', 6: 'cloudy', 7: 'rain', 8: 'sunny'}, 
                  'Pr(Temp, Weather)': {0: 0.14285714285714285, 1: 0.2857142857142857, 2: 0.07142857142857142, 3: 0.14285714285714285, 4: 0.07142857142857142, 5: 0.07142857142857142, 6: 0.07142857142857142, 7: 0.0, 8: 0.14285714285714285}
                  }
        
        self.assertEqual(jpt2, bench2, 'joint prob table error')

        jpt3 = self.probTables.bld_pr_table(vars=['Temp', 'Wildfire'])
        jpt3 = jpt3.table.to_dict()

        bench3 = {'Temp': {0: 3.5, 1: 3.5, 2: 10.2, 3: 10.2, 4: 26.8, 5: 26.8}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 
                  'Pr(Temp, Wildfire)': {0: 0.35714285714285715, 1: 0.14285714285714285, 2: 0.21428571428571427, 3: 0.07142857142857142, 4: 0.07142857142857142, 5: 0.14285714285714285}
                  }
        
        self.assertEqual(jpt3, bench3, 'joint prob table error')

        jpt4 = self.probTables.bld_pr_table(vars=['Weather', 'Wildfire'])
        jpt4 = jpt4.table.to_dict()

        bench4 = {'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny'}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 'Pr(Weather, Wildfire)': {0: 0.2857142857142857, 1: 0.07142857142857142, 2: 0.2857142857142857, 3: 0.07142857142857142, 4: 0.07142857142857142, 5: 0.21428571428571427}
                  }
        
        self.assertEqual(jpt4, bench4, 'joint prob table error')

    def test_conditional_probs(self):
        cpt = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Weather', 'Wildfire'])
        cpt = cpt.table.to_dict()

        bench = {'Temp': {0: 3.5, 1: 3.5, 2: 3.5, 3: 3.5, 4: 3.5, 5: 3.5, 6: 10.2, 7: 10.2, 8: 10.2, 9: 10.2, 10: 10.2, 11: 10.2, 12: 26.8, 13: 26.8, 14: 26.8, 15: 26.8, 16: 26.8, 17: 26.8}, 
                 'Weather': {0: 'cloudy', 1: 'cloudy', 2: 'rain', 3: 'rain', 4: 'sunny', 5: 'sunny', 6: 'cloudy', 7: 'cloudy', 8: 'rain', 9: 'rain', 10: 'sunny', 11: 'sunny', 12: 'cloudy', 13: 'cloudy', 14: 'rain', 15: 'rain', 16: 'sunny', 17: 'sunny'}, 
                 'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True, 8: False, 9: True, 10: False, 11: True, 12: False, 13: True, 14: False, 15: True, 16: False, 17: True}, 
                 'Pr(Temp | Weather, Wildfire)': {0: 0.5, 1: 0.0, 2: 0.75, 3: 1.0, 4: 0.0, 5: 0.3333333333333333, 6: 0.25, 7: 1.0, 8: 0.25, 9: 0.0, 10: 1.0, 11: 0.0, 12: 0.25, 13: 0.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.6666666666666666}
                 }
        
        self.assertEqual(cpt, bench, 'cond. prob table error')

        cpt2 = self.probTables.bld_cond_pr_table(var='Temp', given_vars=['Wildfire'])
        cpt2 = cpt2.table.to_dict()
        
        bench2 = {'Temp': {0: 3.5, 1: 3.5, 2: 10.2, 3: 10.2, 4: 26.8, 5: 26.8}, 
                  'Wildfire': {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}, 
                  'Pr(Temp | Wildfire)': {0: 0.5555555555555556, 1: 0.39999999999999997, 2: 0.3333333333333333, 3: 0.19999999999999998, 4: 0.11111111111111109, 5: 0.39999999999999997}}

        self.assertEqual(cpt2, bench2, 'cond. prob table error')

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()