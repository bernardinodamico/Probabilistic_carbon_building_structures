import pandas as pd 
import itertools
import numpy as np
from pandas import DataFrame 
from Bayesian_net.Utilities import discretizer

class Build_ProbTables():

    dataset: DataFrame = None
    
    def load_dataset(self, path: str) -> None:
        self.dataset = pd.read_csv(filepath_or_buffer=path)  
        
        return
    
    def discretize_cont_vars(self, cont_vars: list[dict]) -> DataFrame:
        vars_list = []
        bins_list = []
        for v in cont_vars:
            vars_list.append(v['name'])
            bins_list.append(v['bins'])
        
        self.dataset = discretizer(dataset=self.dataset,
                                   vars=vars_list,
                                   bin_counts=bins_list,
                                   mid_vals=False)
        
        return self.dataset
    
    def _init_pr_table(self, vars: list[str]) -> DataFrame:
        '''
        Initialises a probability table by entering all potential outcomes, i.e. all possible combinations of values from all variable in the "vars" list.
        A default zero value is assigned to the probability of each outcome.
        '''
        vals_list = []
        for var_name in vars:
            vals_list.append(list(dict.fromkeys(self.dataset[var_name].to_list())))

        outcomes = []
        for outcome in itertools.product(*vals_list):
            outcomes.append(outcome)

        data = np.array([0.] * len(outcomes))
        indexes = pd.MultiIndex.from_tuples(outcomes, names=vars)
        _ini_series = pd.Series(data, index=indexes)

        return _ini_series

    def pr_table(self, vars: list[str]) -> DataFrame:
        '''
        Returns the probability table of a list of variables.
        If 'vars' contains only one variable -> the marginal probability table of that variable is returned, 
        Else, the joint probability table of those variables is returned insted.
        '''
        ini_series = self._init_pr_table(vars=vars)
        series = self.dataset.value_counts(vars, normalize=True)
        series = ini_series.combine(other=series, func=max)
        
        if len(vars) > 1:
            series = series.unstack(fill_value=0).stack()
        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        df_3 = df_1.join(other=df_2)
        
        st = ''
        for name in vars:
            st = st+str(name)+", "
        st = st[:-2]
        
        j_prob_table =  df_3.rename(columns={df_3.columns[-1]: 'Pr('+st+')'})
        
        return j_prob_table


    def cond_pr_table(self, var: str, given_vars: list[str]) -> DataFrame:
        '''
        Returns the conditional probability table of one single variable "var" given a list of evidence variables.
        When a combination of values for the given variables does not exist in the dataset: the cond. pr. is undefined. 
        '''
        joint_prob_table = self.pr_table(vars=[var] + given_vars) 
        margin_prob_table = self.pr_table(vars=given_vars) # containing the normalisation factors "Z"
        merged = joint_prob_table.merge(margin_prob_table, how='left', on=given_vars)

        key_joint_pr_col: str = joint_prob_table.keys()[-1]
        key_prior_pr_col: str = margin_prob_table.keys()[-1]

        st_ev = var+" | "
        for name in given_vars:
            st_ev = st_ev+str(name)+", "
        st_ev = st_ev[:-2]

        merged['Pr('+st_ev+')'] = merged[key_joint_pr_col] / merged[key_prior_pr_col]
        cond_prob_table = merged.drop(columns=[key_joint_pr_col, key_prior_pr_col])

        #----------------------------------------------------------------------------
        cond_prob_table['Pr('+st_ev+')'] = cond_prob_table['Pr('+st_ev+')'].fillna('undefined')

        return cond_prob_table

'''
probTables = Build_ProbTables()
probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")

var = 'Temp'
given_vars = ['Weather', 'Wildfire']

jpt = probTables.cond_pr_table(var=var, given_vars=given_vars)
print(jpt)

probTables = Build_ProbTables()
probTables.load_dataset(path="Data/training_dataset.csv")

var = 'Basement'
given_vars = ['Superstructure_Type', 'Foundation_Type']

jpt = probTables.cond_pr_table(var=var, given_vars=given_vars)
print(jpt)
'''