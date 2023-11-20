import pandas as pd
from pandas import DataFrame
from Bayesian_net.customExceptions import *

class ProbTable():
    
    all_variables: list[str] = None
    given_variables: list[str] = None
    assigned_ev_values: list[str] = None
    table: DataFrame = None
    is_conditional: bool = None
    smoothing_factor: float = None
    is_valid: bool = None

    def is_valid_distribution(self) -> bool:

        tot_pr_col = round(self.table[self.table.keys().to_list()[-1]].sum(), 10)
        if self.is_conditional is False: 
            if tot_pr_col == 1.:
                #print(tot_pr_col, "it's a valid joint/marginal PT")
                self.is_valid = True 
                return True
            else:
                #print(tot_pr_col, "it's NOT a valid joint/marginal PT")
                self.is_valid = False
                return False
        elif self.is_conditional is True:
            if len(self.table.columns) == 2 and tot_pr_col == 1.:
                #print(tot_pr_col, len(self.table.columns), "it's a valid conditional PT")
                self.is_valid = True
                return True
            else:
                #print(tot_pr_col, len(self.table.columns), "it's NOT a valid conditional PT")
                self.is_valid = False
                return False
        else:
            return None
    
