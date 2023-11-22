from Bayesian_net.prob_table import ProbDistrib
from pandas import DataFrame


class VariableElimination():

    def sum_out_var(self, prob_table: ProbDistrib) -> ProbDistrib:
        print(prob_table.table)
        return