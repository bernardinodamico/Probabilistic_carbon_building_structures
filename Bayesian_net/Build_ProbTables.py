import pandas as pd 
pd.set_option('display.max_rows', None)
import itertools
import numpy as np
from pandas import DataFrame 
from Bayesian_net.utilities import discretizer
from Bayesian_net.customExceptions import *
from Bayesian_net.prob_table import ProbDistrib
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

    def bld_pr_table(self, vars: list[str], K: float = 0.) -> ProbDistrib:
        '''
        Returns the probability table of a list of variables 'vars'.
        If 'vars' contains only one variable -> the marginal probability table of that variable is returned, 
        Else, the joint probability table of those variables is returned insted.
        K is the Laplace smoothing parameter (default value = 0.0 i.e. no smoothing is applied).  NOTE: it only applies to
        marginal prob tables i.e with one variable.
        '''
        
        ini_series = self._init_pr_table(vars=vars)
        if len(vars)  == 1:
            series = self.dataset.value_counts(vars, normalize=False)
        else:
            series = self.dataset.value_counts(vars, normalize=True)
        series = ini_series.combine(other=series, func=max)
        
        if len(vars) > 1:
            series = series.unstack(fill_value=0).stack()
        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        df_3 = df_1.join(other=df_2)

        if len(vars)  == 1:
            df_3 = self.smooth_marginal(m_prob_table=df_3, K=K)

        st = ''
        for name in vars:
            st = st+str(name)+", "
        st = st[:-2]
    
        j_prob_table = ProbDistrib()
        j_prob_table.all_variables = vars
        j_prob_table.given_variables = None
        j_prob_table.assigned_ev_values = None
        j_prob_table.table = df_3.rename(columns={df_3.columns[-1]: 'Pr('+st+')'})
        j_prob_table.is_conditional = False
        j_prob_table.is_proper = j_prob_table.is_proper_distribution()

        return j_prob_table


    def bld_cond_pr_table(self, var: str, given_vars: list[str], K: float = 0.0) -> ProbDistrib:
        '''
        Returns the conditional probability table of one single variable "var" given a list of evidence variables.

        Inputs:
        - var: query variable
        - given_vars: evidence variables
        - K: Laplace smoothing parameter (default value = 0.0 i.e. no smoothing is applied).
        '''
        if K < 0.:
            raise NonPositiveValueError()
        
        joint_prob_table = ProbDistrib()
        margin_prob_table = ProbDistrib()

        joint_prob_table.table = self.bld_pr_table(vars=[var] + given_vars, K=0.).table 
        margin_prob_table.table = self.bld_pr_table(vars=given_vars, K=0.).table # containing the normalisation constant "Z"
        merged = joint_prob_table.table.merge(margin_prob_table.table, how='left', on=given_vars)

        key_joint_pr_col: str = joint_prob_table.table.keys()[-1]
        key_prior_pr_col: str = margin_prob_table.table.keys()[-1]

        st_ev = var+" | "
        for name in given_vars:
            st_ev = st_ev+str(name)+", "
        st_ev = st_ev[:-2]

        count_joint = self.dataset.shape[0] * merged[key_joint_pr_col]
        count_prior = self.dataset.shape[0] * merged[key_prior_pr_col]
        var_range = merged[var].nunique()

        merged['Pr('+st_ev+')'] = (count_joint + K) / (count_prior + var_range * K)
        cond_prob_table = merged.drop(columns=[key_joint_pr_col, key_prior_pr_col])
        
        cond_prob_table['Pr('+st_ev+')'] = cond_prob_table['Pr('+st_ev+')'].fillna(0.) #replace NaN values with 0.0
        #----------------------------------------------------------------------------

        prob_table = ProbDistrib()
        prob_table.all_variables = [var] + given_vars
        prob_table.given_variables = given_vars
        prob_table.assigned_ev_values = None
        prob_table.table = cond_prob_table
        prob_table.is_conditional = True
        prob_table.is_proper = prob_table.is_proper_distribution()

        return prob_table
    
    def assign_evidence(self, prT: ProbDistrib, assignment_vals: list[dict])-> ProbDistrib:
        '''
        Inputs:
        - prob_table: a conditional probability table
        - assignment_vals: a list of dictionaries with 'vr_name' and 'val' as keys. 'vr_name' is the variable to which
        a value 'val' is to be assigned. 
        
        Output:
        - A subset of the input conditional probability table, where some/all of the variables have a value assigned.

        If values are assigned to all evidence variables in 'prT': the resulting CPT output will contain only two
        columns, i.e. the query variable and its probability distribution.
        NOTE: value assignments are not limited to evidence variables. The query variable can also be assigned a value. E.g. 
        if all variables in the table are assigned a value, the output is a one-column one-row table. 
        
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
            prT.is_proper = prT.is_proper_distribution()

            return prT
        else:
            raise NonConditionalProbTableError(variable=prT)

    def smooth_marginal(self, m_prob_table: DataFrame, K: float = 0.) -> DataFrame:
        '''
        Inputs:
        - m_prob_table: a marginal probability table (i.e. a two-column Dataframe)
        - K: Laplace smoothing parameter (default value = 0.0 i.e. no smoothing is applied).
        '''
        if len(m_prob_table.columns) != 2:
            raise ProbTableError(table=m_prob_table)
        if K < 0.:
            raise NonPositiveValueError()
        
        var_range: int = m_prob_table.shape[0]
        key_frequency_col: str = m_prob_table.keys()[-1]
 
        m_prob_table[key_frequency_col] = (m_prob_table[key_frequency_col] + K) / (self.dataset.shape[0] + var_range * K)

        return m_prob_table 
