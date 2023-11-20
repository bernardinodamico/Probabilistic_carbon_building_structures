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

    def __init__(self) -> None:
        super().__init__()
        return
