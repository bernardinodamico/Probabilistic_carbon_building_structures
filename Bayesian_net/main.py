import pandas as pd 
from pandas import DataFrame
from Bayesian_net.Build_ProbTables import Build_ProbTables

from matplotlib import pyplot as plt

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


print(mpt_superstr_type)

# def plot_pr_table()
fig, ax = plt.subplots()
fig.set_size_inches(6,6)
fig.set_dpi(300)
_aspect = 4.3 # this parm must have assigned the same val for all plots (it can be an internal property of the Plotter() class)
_bottom = 0.45 # this parm must have assigned the same val for all plots 
ax.set(ylim=[0, 1.], aspect=_aspect)
plt.subplots_adjust(bottom=_bottom)

ax.set_ylim([0, 1])
plt.bar(x=mpt_superstr_type['Superstructure_Type'].tolist(), 
        height=mpt_superstr_type['Pr(Superstructure_Type)'],
        width=0.96,
        color='dodgerblue',
        )
plt.xticks(rotation=90)
plt.xlabel('Superstructure_Type', fontweight='bold')
plt.ylabel('Pr(Superstructure_Type)', fontweight='bold')
#plt.show()
plt.savefig('Figures/fig_name2.png')

#create functions for the lagrange smoothing in the Utilities.py and
#apply it to the above cpts and mpts here, as well as a general method to plot distributions.

# Then work out the equation for the belief prop (Variable Elimin algo) and write them down 
#in the manuscript appendix, based on independencies via d-separation etc. (see notes.txt) for the specific "example" of showing the figures in mind for the
#paper.