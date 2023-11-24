from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork
import numpy as np
import pandas as pd
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.estimators import BayesianEstimator
from utilities import Plotter


# 1) load dataset
dataset = pd.read_csv(filepath_or_buffer='Bayesian_net/tests/dummy_dataset.csv')
# 2) discretize it

# 3) istantiate BN
graph = [('Temp', 'Wildfire'), ('Weather', 'Wildfire')]
model = BayesianNetwork(ebunch=graph)


# 4) set smoothing to CPTs
smooth = False
ess = 5
if smooth is True:
    model.fit(data=dataset,
            estimator=BayesianEstimator,  
            prior_type="BDeu",
            equivalent_sample_size=ess #the higher the value the more the smoothing
            )
else:
    model.fit(data=dataset,
            estimator=None  
            )

# for printing the CPTs 
cpd: TabularCPD
for cpd in model.get_cpds():
    print(f'CPT of {cpd.variable}:')
    print(cpd, '\n')

# 5) run inference on materials: set query mats var and evidence(s) 
inference = VariableElimination(model)
query_var = 'Wildfire'
evidence_vals = {'Temp': 3.5, 'Weather': 'rain'} 
phi_query = inference.query(variables=[query_var], evidence=evidence_vals, elimination_order='MinFill',joint=True, show_progress=False)

# for printing 
key_st =''
for k in evidence_vals.keys():
    key_st = key_st+k+'='+f'{evidence_vals[k]}, '
pr_head  = f'Pr({query_var} | {key_st})'
pr_head = pr_head.replace(', )', ')')

query_dic = {**phi_query.state_names, **{pr_head: list(phi_query.values)}}

# return query_cpd of each mat
query_cpd = pd.DataFrame(query_dic)

print(query_cpd)

plot = Plotter()
plot.plot_pr_distrib(prT=query_cpd, savefig_loc_folder='Figures')

'''
make a QueryMats class out of this, with properties:
- dataset
- CPTs
- evidence_VarsVals
- mats_distributions

 and following methods:
- load_dataset()
- discretize_cont_vars()
- print_CPTs()
- print_mats_distributions()
- run_inference()

The call is then instantiated into another QueryCarbon class (to get all mats distributions given a variable set of evidences)
that computes carbon distributions. This will have properties:
- carbon_distribution
- confidence-interval
- mean, mode
- carbon coeffs

and methods:
- run_montecarlo_sampling
- get_statistics
- etc

the QueryCarbon class is then istantiated into 'performance_validation' scripts to assess how far
from unseen ground truth datapoint the inference engine does e.g. by measuring the error trend as 
more evidence (design choices) accumulates. 

'''
