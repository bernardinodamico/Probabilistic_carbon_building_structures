import pandas as pd 
from pandas import DataFrame
from Bayesian_net.Build_ProbTables import Build_ProbTables
from Utilities import Plotter

pt = Build_ProbTables()
pt.load_dataset(path='Data/training_dataset.csv')

continuous_vars = [
    {'name': 'Concr(kg/m2)', 
     'bins': 18
     },
    {'name': 'Masnry&Blwk(m2/m2)',
     'bins': 5
     },
    {'name': 'Reinf(kg/m2)',
     'bins': 7
     },
    {'name': 'Steel_Sec(kg/m2)', 
     'bins': 12
     },
    {'name': 'Timber_Prod(kg/m2)', 
     'bins': 4
     },
]

dd = pt.discretize_cont_vars(cont_vars=continuous_vars, mid_vals=True)
dd.to_csv(path_or_buf='Data/discrete_training_dataset.csv', index=False) 

mpt_superstr_type = pt.pr_table(vars=['Supstr_Type'])
mpt_cladding_type = pt.pr_table(vars=['Clad_Type'])
mpt_No_storeys = pt.pr_table(vars=['No_storeys'])
mpt_basement = pt.pr_table(vars=['Basement'])

cpt_masonry_BW = pt.cond_pr_table(var='Masnry&Blwk(m2/m2)', given_vars=['Clad_Type', 'Supstr_Type'], replace_undef=True)
cpt_superstr_UW = pt.cond_pr_table(var='Supstr_uw', given_vars=['Supstr_Type'])
cpt_timber_prods = pt.cond_pr_table(var='Timber_Prod(kg/m2)', given_vars=['Supstr_Type'])
cpt_concrete_elems = pt.cond_pr_table(var='Supstr_Cr_elems', given_vars=['Supstr_Type'])
cpt_steel_secs = pt.cond_pr_table(var='Steel_Sec(kg/m2)', given_vars=['Supstr_Type'])
cpt_found_type = pt.cond_pr_table(var='Found_Type', given_vars=['No_storeys', 'Supstr_uw'])
cpt_reinforcement = pt.cond_pr_table(var='Reinf(kg/m2)', given_vars=['Supstr_Cr_elems', 'Found_Type'])
cpt_concrete_qty = pt.cond_pr_table(var='Concr(kg/m2)', given_vars=['Supstr_Cr_elems', 'Found_Type', 'Basement'])


#print(cpt_concrete_qty)


ass_vars_vals: dict = [
    {'vr_name': 'Supstr_Cr_elems', 
     'val': 'Frame&Floors'},
    {'vr_name': 'Found_Type', 
     'val': 'Piled(Ground-beams/Caps)'},
     {'vr_name': 'Basement', 
     'val': True}
    ]

x = pt.assign_evidence(prob_table=cpt_concrete_qty, assignment_vals=ass_vars_vals)

print(x)

figure = Plotter()
figure.plot_pr_table(prob_table=x, savefig_loc_folder='Figures', size_inches=9, break_text_label=True, y_axis='dynamic')

figure.plot_pr_table(prob_table=pt.pr_table(vars=['Concr(kg/m2)']), savefig_loc_folder='Figures', size_inches=9, break_text_label=False, y_axis='dynamic')

#create functions for the lagrange smoothing in the Utilities.py and

# Then work out the equation for the belief prop (Variable Elimin algo) and write them down 
#in the manuscript appendix, based on independencies via d-separation etc. (see notes.txt) for the specific "example" of showing the figures in mind for the
#paper.