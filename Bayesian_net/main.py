from Bayesian_net.Build_ProbTables import Build_ProbTables, Fetch_ProbTables
from Bayesian_net.variable_elimination import VariableElimination
from utilities import Plotter

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

mpt_superstr_type = pt.bld_pr_table(vars=['Supstr_Type'], K=1.)
mpt_cladding_type = pt.bld_pr_table(vars=['Clad_Type'], K=1.)
mpt_No_storeys = pt.bld_pr_table(vars=['No_storeys'], K=1.)
mpt_basement = pt.bld_pr_table(vars=['Basement'], K=1.)

cpt_masonry_BW = pt.bld_cond_pr_table(var='Masnry&Blwk(m2/m2)', given_vars=['Clad_Type', 'Supstr_Type'], K=1.)
cpt_superstr_UW = pt.bld_cond_pr_table(var='Supstr_uw', given_vars=['Supstr_Type'], K=1.)
cpt_timber_prods = pt.bld_cond_pr_table(var='Timber_Prod(kg/m2)', given_vars=['Supstr_Type'], K=1.)
cpt_concrete_elems = pt.bld_cond_pr_table(var='Supstr_Cr_elems', given_vars=['Supstr_Type'], K=1.)
cpt_steel_secs = pt.bld_cond_pr_table(var='Steel_Sec(kg/m2)', given_vars=['Supstr_Type'], K=1.)
cpt_found_type = pt.bld_cond_pr_table(var='Found_Type', given_vars=['No_storeys', 'Supstr_uw'], K=1.)
cpt_reinforcement = pt.bld_cond_pr_table(var='Reinf(kg/m2)', given_vars=['Supstr_Cr_elems', 'Found_Type'], K=1.)
cpt_concrete_qty = pt.bld_cond_pr_table(var='Concr(kg/m2)', given_vars=['Supstr_Cr_elems', 'Found_Type', 'Basement'], K=1.)


#print(cpt_concrete_qty)


ass_vars_vals = [
    {'vr_name': 'Supstr_Cr_elems', 
     'val': 'Frame&Floors'},
    {'vr_name': 'Found_Type', 
     'val': 'Piled(Ground-beams/Caps)'},
     {'vr_name': 'Basement', 
     'val': True}
    ]

figure = Plotter()

ve = VariableElimination()
x = ve.assign_evidence(prT=cpt_concrete_qty, assignment_vals=ass_vars_vals)
#figure.plot_pr_distrib(prT=x, savefig_loc_folder='Figures', size_inches=9, break_text_label=True, y_axis='dynamic')
#print(x.table)
# Then work out the equation for the belief prop (Variable Elimin algo) and write them down 
#in the manuscript appendix, based on independencies via d-separation etc. (see notes.txt) for the specific "example" of showing the figures in mind for the
#paper.


pt = Fetch_ProbTables()
mpt_burgler = pt.fetch_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_Burgler.csv')
mpt_earthqk = pt.fetch_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_Earthqk.csv')
cpt_alarm = pt.fetch_cond_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_Alarm_given_B_E.csv', given_vars=['Burgler', 'Earthqk'])
cpt_J_calls = pt.fetch_cond_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_J_calls_given_Alarm.csv', given_vars=['Alarm'])
cpt_M_calls = pt.fetch_cond_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_M_calls_given_Alarm.csv', given_vars=['Alarm'])

pt_Alarm_Earthqk_given_B = pt.fetch_cond_pr_table(csv_file_loc='Bayesian_net/tests/dummy_PrTables/Pr_Alarm_Earthqk_given_B.csv', given_vars=['Burgler'])
print(pt_Alarm_Earthqk_given_B.table)
ass_vars_vals = [
    {'vr_name': 'Earthqk', 
     'val': 'yes'},
     {'vr_name': 'Burgler', 
     'val': 'yes'}
    ]
x = ve.assign_evidence(prT=pt_Alarm_Earthqk_given_B, assignment_vals=ass_vars_vals)
print(x.table)
y = ve.sum_out_var(prT=x, sum_out_var='Alarm')
print(y.table)
print("ddd")

###Write test for sum_out_var() e.g. check total of I and O table matches or check against P(A | B) in the notes