from Bayesian_net.prob_table import ProbDistrib
from Bayesian_net.customExceptions import *
import copy
from pandas import DataFrame


class VariableElimination():
    
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
                if variable['vr_name'] not in prT.all_variables:
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
            
            prT.all_variables 
            prT.assigned_evid_values = assignment_vals
            prT.table = prT.table.rename(columns={prT.table.keys().to_list()[-1]: Pr_heading})
            prT.is_proper = prT.is_proper_distribution()

            return prT
        else:
            raise NonConditionalProbTableError(variable=prT)
    
    def sum_out_var(self, prT: ProbDistrib, sum_out_var: str) -> ProbDistrib:
        '''
        Collapses together rows in the prob table which have same instantiation values (except for the 
        "sum_out_var" i.e. the variable to be eliminate). All prob values of collapsed rows are summed up into
        a signle prob value.  

        Inputs: 
        - a prob. table
        - a variable in the table

        Output:
        a prob. tables with a smaller number of rows and one column less (the eliminated variable) that in the input table.
        '''
        assigned_vars = []
        if prT.assigned_evid_values is not None:
            for d in prT.assigned_evid_values:
                assigned_vars.append(d['vr_name'])
            unassigned_vars = list(set(prT.all_variables) - set(assigned_vars))
        else:
            unassigned_vars = prT.all_variables
        
        if sum_out_var not in unassigned_vars:
            raise Variable_Error(variable=sum_out_var)

        prT = copy.copy(prT)
        
        Pr_heading: str = prT.table.keys().to_list()[-1]

        sub_set = list(set(unassigned_vars) - set([sum_out_var])) 
        series = prT.table.groupby(sub_set)[Pr_heading].sum()
        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        prT.table = df_1.join(other=df_2)
        
        #------- rename Pr column------
        #if series.shape[0] != prT.table.shape[0]:
        Pr_heading = Pr_heading.replace(f'{sum_out_var}, ', '')
        Pr_heading = Pr_heading.replace(f', {sum_out_var}', '')
        prT.table = prT.table.rename(columns={prT.table.keys().to_list()[-1]: Pr_heading})


        prT.all_variables.remove(sum_out_var)
        prT.is_proper = prT.is_proper_distribution()

        return prT
    