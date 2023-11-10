import pandas as pd 
from pandas import DataFrame 


class Build_ProbTables():

    dataset: DataFrame = None
    
    def load_dataset(self, path: str) -> None:
        self.dataset = pd.read_csv(path)  
        
        return
    
    def pr_table(self, vars_name: list[str]) -> DataFrame:
        '''
        Returns the probability table of a list of variables.
        If 'vars_name' contains only one variable -> the marginal probability table of that variable is returned, 
        Else, the joint probability table of those variables is returned insted.
        '''
        s = self.dataset.value_counts(vars_name, normalize=True)
        df = s.to_frame()
        
        st = ''
        for name in vars_name:
            st = st+str(name)+","
        st = st[:-1]
        
        j_prob_table =  df.rename(columns={'proportion': 'Pr('+st+')'})
        
        return j_prob_table


    def cond_pr_table(self, var: str, evidence_vars: list[str]) -> DataFrame:
        '''
        Returns the conditional probability table of one single variable "var" given a list of evidence variables.
        '''
        s = self.dataset.value_counts([var] + evidence_vars, normalize=True) / self.dataset.value_counts(evidence_vars, normalize=True)
        df = s.to_frame()
        
        st_ev = var+" | "
        for name in evidence_vars:
            st_ev = st_ev+str(name)+","
        st_ev = st_ev[:-1]
        
        c_prob_table =  df.rename(columns={'proportion': 'Pr('+st_ev+')'})
        
        return c_prob_table

#### Add a method to check if there are UNDEFINED probabilities in the full joint so that a warning or error is triggered 
#### test these methods properly!!!

probTables = Build_ProbTables()
probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")

mpt = probTables.pr_table(vars_name=['Temp'])
print(mpt)
mpt2 = probTables.pr_table(vars_name=['Weather'])
print(mpt2)
jpt = probTables.pr_table(vars_name=['Temp', 'Weather'])
print(jpt)


xxx = probTables.cond_pr_table(var='Weather', evidence_vars=['Temp'])
print(xxx)