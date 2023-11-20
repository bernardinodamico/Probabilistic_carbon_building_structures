import pandas as pd 
pd.set_option('display.max_rows', None)
import itertools
import numpy as np
from pandas import DataFrame 
from Bayesian_net.Utilities import discretizer
from Bayesian_net.customExceptions import *
from Bayesian_net.prob_table import ProbTable
import copy

class Build_ProbTables():

    dataset: DataFrame = None
    
    def load_dataset(self, path: str) -> None:
        self.dataset = pd.read_csv(filepath_or_buffer=path)  
        
        return

    def discretize_cont_vars(self, cont_vars: list[dict], mid_vals: bool = False) -> DataFrame:
        vars_list = []
        bins_list = []
        for v in cont_vars:
            vars_list.append(v['name'])
            bins_list.append(v['bins'])
        
        self.dataset = discretizer(dataset=self.dataset,
                                   vars=vars_list,
                                   bin_counts=bins_list,
                                   mid_vals=mid_vals)
        
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

    def bld_pr_table(self, vars: list[str]) -> ProbTable:
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
    
        j_prob_table = ProbTable()
        j_prob_table.all_variables = vars
        j_prob_table.given_variables = None
        j_prob_table.assigned_ev_values = None
        j_prob_table.table = df_3.rename(columns={df_3.columns[-1]: 'Pr('+st+')'})
        j_prob_table.is_conditional = False
        j_prob_table.smoothing_factor = None
        j_prob_table.is_valid = j_prob_table.is_valid_distribution()

        return j_prob_table


    def bld_cond_pr_table(self, var: str, given_vars: list[str], replace_undef: bool = False) -> ProbTable:
        '''
        Returns the conditional probability table of one single variable "var" given a list of evidence variables.
        When a combination of values for the given variables does not exist in the dataset: the cond. pr. is "undefined".
        If the parameter "replace_undef" is set to True (default=False): undefinded probabilities are set to zero.
        '''
        joint_prob_table = ProbTable()
        margin_prob_table = ProbTable()

        joint_prob_table.table = self.bld_pr_table(vars=[var] + given_vars).table 
        margin_prob_table.table = self.bld_pr_table(vars=given_vars).table # containing the normalisation constant "Z"
        merged = joint_prob_table.table.merge(margin_prob_table.table, how='left', on=given_vars)

        key_joint_pr_col: str = joint_prob_table.table.keys()[-1]
        key_prior_pr_col: str = margin_prob_table.table.keys()[-1]

        st_ev = var+" | "
        for name in given_vars:
            st_ev = st_ev+str(name)+", "
        st_ev = st_ev[:-2]

        merged['Pr('+st_ev+')'] = merged[key_joint_pr_col] / merged[key_prior_pr_col]
        cond_prob_table = merged.drop(columns=[key_joint_pr_col, key_prior_pr_col])

        #----------------------------------------------------------------------------
        if replace_undef == False:
            cond_prob_table['Pr('+st_ev+')'] = cond_prob_table['Pr('+st_ev+')'].fillna('undefined')
        else:
            cond_prob_table['Pr('+st_ev+')'] = cond_prob_table['Pr('+st_ev+')'].fillna(0.)

        prob_table = ProbTable()
        prob_table.all_variables = [var] + given_vars
        prob_table.given_variables = given_vars
        prob_table.assigned_ev_values = None
        prob_table.table = cond_prob_table
        prob_table.is_conditional = True
        prob_table.smoothing_factor = None
        prob_table.is_valid = prob_table.is_valid_distribution()

        return prob_table
    
    def assign_evidence(self, prT: ProbTable, assignment_vals: list[dict])-> ProbTable:
        '''
        Inputs:
        - prob_table: a FULL conditional probability table (i.e. with all possible instantiation value combinations)
        - assignment_vals: a list of dictionaries with 'vr_name' and 'val' as keys. 'vr_name' is the variable to which
        a value 'val' is to be assigned. 
        
        Output:
        - A subset of the input conditional probability table, containing only the instantions matching the assigned values.
        
        Note: if values are assigned to all evidence variables in 'prT': the resulting CPT output will contain only two
        columns, i.e. the query variable and its probability distribution.
        '''
        if prT.is_conditional is True:
            for variable in assignment_vals:
                if variable['vr_name'] not in prT.table.keys().to_list():
                    raise Variable_assignmentError(variable=variable['vr_name'])
                if variable['val'] not in prT.table.values:
                    raise Value_assignmentError(variable=variable['vr_name'], value=variable['val'])

            #--------------------------------------------------------------------
            prT = copy.copy(prT)
            for i in range(len(assignment_vals)):
                vr_name = assignment_vals[i]['vr_name']
                val = assignment_vals[i]['val']
                prT.table = prT.table.loc[(prT.table[vr_name] == val)]
            
            for i in range(len(assignment_vals)):
                vr_name = assignment_vals[i]['vr_name']
                prT.table = prT.table.drop(labels=vr_name, axis='columns')

            #------- rename Pr column-------------------------------------------
            Pr_heading: str = prT.table.keys().to_list()[-1]
            for i in range(len(assignment_vals)):
                vr_name = assignment_vals[i]['vr_name']
                val = str(assignment_vals[i]['val'])
                Pr_heading = Pr_heading.replace(vr_name, vr_name+'='+val)
            
            prT.assigned_ev_values = assignment_vals
            prT.table = prT.table.rename(columns={prT.table.keys().to_list()[-1]: Pr_heading})
            prT.is_valid = prT.is_valid_distribution()

            return prT
        else:
            raise NonConditionalProbTableError(variable=prT)

    def add_lapl_smooth(self, prT: ProbTable, K: float) -> ProbTable:
        '''
        Inputs:
        - prob_table: a two-column Dataframe (either a MPT or a CPT with all evidence variables istantiated)
        - K: smoothing parameter (>0)
        '''
        if len(prT.table.columns) != 2:
            raise ProbTableError(table=prT.table)
        if K <= 0.:
            raise NonPositiveValueError()
        
        var_range: int = prT.table.shape[0]
        
        prT = copy.copy(prT)
        prT.table.iloc[:,-1:] = (prT.table.iloc[:,-1:] * 100. + K) / (100. + var_range * K)
        prT.smoothing_factor = K

        return prT
