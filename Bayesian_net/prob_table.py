import pandas as pd
from pandas import DataFrame
from Bayesian_net.customExceptions import *

class ProbDistrib():
    
    all_variables: list[str] = None
    given_variables: list[str] = None
    assigned_ev_values: list[str] = None
    table: DataFrame = None
    is_conditional: bool = None
    is_proper: bool = None

    def is_proper_distribution(self) -> bool:
        '''
        Checks whether it's a 'proper' prob table distribution i.e. essentially any ProbDistrib that is not also a 'factor' table.
        Examples of proper ProbTable(s):
        - P(A); P(A, B); P(A, B,...,Z)
        - P(A | B=b); P(A | B=b, C=c); P(A | B=b, C=c,...,Z=z)
        ...

        Examples of improper ProbTable(s):
        - P(A, B=b); P(A, B,...Z=z)
        - P(A | B); P(A | B, C); P(A | B, C,...,Z); P(A | B=b, C,...,Z)

        A proper joint/marginal prob table must have the Pr column summing up to 1.
        
        An proper cond. prob table must have the Pr column summing up to 1 AND have exactly two columns (a Pr column and a query variable column).
        '''
        tot_pr_col = round(self.table[self.table.keys().to_list()[-1]].sum(), 7)
        if self.is_conditional is False: 
            if tot_pr_col == 1.:
                self.is_proper = True 
                return True
            else:
                self.is_proper = False
                return False
        elif self.is_conditional is True:
            if len(self.table.columns) == 2 and tot_pr_col == 1.:
                self.is_proper = True
                return True
            else:
                self.is_proper = False
                return False
        else:
            return None
    
