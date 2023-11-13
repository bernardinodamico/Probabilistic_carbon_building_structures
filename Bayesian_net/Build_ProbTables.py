import pandas as pd 
from pandas import DataFrame 
from tabulate import tabulate


class Build_ProbTables():

    dataset: DataFrame = None
    
    def load_dataset(self, path: str) -> None:
        self.dataset = pd.read_csv(path)  
        
        return
    
    def pr_table(self, vars: list[str]) -> DataFrame:
        '''
        Returns the probability table of a list of variables.
        If 'vars' contains only one variable -> the marginal probability table of that variable is returned, 
        Else, the joint probability table of those variables is returned insted.
        '''
        series = self.dataset.value_counts(vars, normalize=True)
        if len(vars) > 1:
            series = series.unstack(fill_value=0).stack()
        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        df_3 = df_1.join(other=df_2)
        
        st = ''
        for name in vars:
            st = st+str(name)+","
        st = st[:-1]
        
        j_prob_table =  df_3.rename(columns={df_3.columns[-1]: 'Pr('+st+')'})
        
        return j_prob_table


    def cond_pr_table(self, var: str, given_vars: list[str]) -> DataFrame:
        '''
        Returns the conditional probability table of one single variable "var" given a list of evidence variables.
        '''
        series = self.dataset.value_counts([var] + given_vars, normalize=True) / self.dataset.value_counts(given_vars, normalize=True)
        series = series.unstack(fill_value=0).stack()

        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        df_3 = df_1.join(other=df_2)

        st_ev = var+" | "
        for name in given_vars:
            st_ev = st_ev+str(name)+","
        st_ev = st_ev[:-1]
        
        c_prob_table = df_3.rename(columns={df_3.columns[-1]: 'Pr('+st_ev+')'})
        
        return c_prob_table

#### Now istantiations of non-existing outcomes in the dataset are accounted for in the joint and cond. tables
# mening that zero probabilities are entered for these....Add a method to check if there are UNDEFINED probabilities in the CPTs so that a warning or error is triggered 
#### test these methods properly!!!
'''
probTables = Build_ProbTables()
probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")

mpt = probTables.pr_table(vars=['Temp'])
print(mpt)
mpt2 = probTables.pr_table(vars=['Weather'])
print(mpt2)
jpt = probTables.pr_table(vars=['Temp', 'Weather'])
print(jpt)

cpt = probTables.cond_pr_table(var='Weather', given_vars=['Temp'])

print(cpt)
'''