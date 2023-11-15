import pandas as pd 
from pandas import DataFrame
from Bayesian_net.Build_ProbTables import Build_ProbTables


pt = Build_ProbTables()
pt.load_dataset(path='Data/training_dataset.csv')

continuous_vars = [
    {'name': 'Concrete_Mass_(kg/m2)', 
     'bins': 18
     },
    {'name': 'Masonry_&_Blockwork_Area_(m2/m2)',
     'bins': 5
     },
    {'name': 'Reinforcement_Mass_(kg/m2)',
     'bins': 7
     },
    {'name': 'Steel_(Sections)_Mass_(kg/m2)', 
     'bins': 12
     },
    {'name': 'Timber_(Products)_Mass_(kg/m2)', 
     'bins': 4
     },
]

dd = pt.discretize_cont_vars(cont_vars=continuous_vars)
#dd.to_csv(path_or_buf='Data/discrete_training_dataset.csv', index=False)

mpt_superstr_type = pt.pr_table(vars=['Superstructure_Type'])
mpt_cladding_type = pt.pr_table(vars=['Cladding_Type'])
mpt_No_storeys = pt.pr_table(vars=['No_storeys'])
mpt_basement = pt.pr_table(vars=['Basement'])

cpt_masonry_BW = pt.cond_pr_table(var='Masonry_&_Blockwork_Area_(m2/m2)', given_vars=['Cladding_Type', 'Superstructure_Type'], replace_undef=True)
cpt_superstr_UW = pt.cond_pr_table(var='Superstructure_unit_weight', given_vars=['Superstructure_Type'])
cpt_timber_prods = pt.cond_pr_table(var='Timber_(Products)_Mass_(kg/m2)', given_vars=['Superstructure_Type'])
cpt_concrete_elems = pt.cond_pr_table(var='Superstructure_Concrete_elements', given_vars=['Superstructure_Type'])
cpt_steel_secs = pt.cond_pr_table(var='Steel_(Sections)_Mass_(kg/m2)', given_vars=['Superstructure_Type'])
cpt_found_type = pt.cond_pr_table(var='Foundation_Type', given_vars=['No_storeys', 'Superstructure_unit_weight'])
cpt_reinforcement = pt.cond_pr_table(var='Reinforcement_Mass_(kg/m2)', given_vars=['Superstructure_Concrete_elements', 'Foundation_Type'])
cpt_concrete_qty = pt.cond_pr_table(var='Concrete_Mass_(kg/m2)', given_vars=['Superstructure_Concrete_elements', 'Foundation_Type', 'Basement'])


