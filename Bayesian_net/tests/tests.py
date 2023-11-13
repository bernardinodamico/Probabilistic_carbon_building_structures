import unittest
from Bayesian_net.Build_ProbTables import Build_ProbTables

class TestBuild_ProbTables(unittest.TestCase):

    probTables = Build_ProbTables()
    probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")
    
    def test_marginal_probs(self):
        
        mpt = self.probTables.pr_table(vars=['Temp'])
        mpt = mpt.to_dict()
        bench = {'Temp': {0: 3.5, 1: 10.2, 2: 26.8}, 'Pr(Temp)': {0: 0.5, 1: 0.2857142857142857, 2: 0.21428571428571427}}

        self.assertEqual(mpt, bench, 'marginal prob table error')

        mpt2 = self.probTables.pr_table(vars=['Weather'])
        mpt2 = mpt2.to_dict()
        bench2 = {'Weather': {0: 'cloudy', 1: 'rain', 2: 'sunny'}, 'Pr(Weather)': {0: 0.35714285714285715, 1: 0.35714285714285715, 2: 0.2857142857142857}}

        self.assertEqual(mpt2, bench2, 'marginal prob table error')

        mpt3 = self.probTables.pr_table(vars=['Wildfire'])
        mpt3 = mpt3.to_dict()
        bench3 = {'Wildfire': {0: False, 1: True}, 'Pr(Wildfire)': {0: 0.6428571428571429, 1: 0.35714285714285715}}

        self.assertEqual(mpt3, bench3, 'marginal prob table error')

    def test_joint_probs(self):
        jpt = self.probTables.pr_table(vars=['Temp', 'Weather', 'Wildfire'])
        #jpt = jpt.to_dict()
        print(jpt)



#--------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()