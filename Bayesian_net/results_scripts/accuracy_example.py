from matplotlib import pyplot as plt
from Bayesian_net.results_scripts.single_carbon_query import get_mode, single_carbon_query_call
from Bayesian_net.settings import BNSettings
import pandas as pd
from Bayesian_net.query import QueryMaterials

ylabels = [r'$P(Q)$', r'$P(Q | n)$', r'$P(Q | n,f)$', r'$P(Q | n,f,s^*)$', r'$P(Q | n,f,s^*,g)$', r'$P(Q | n,f,s^*,g,b)$']

proj_ref = 153
QueryMaterials(update_datasets=True) # to update the training and validation datasets before running the queries
training_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_training_dataset.csv') 

n_storeys = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'No_storeys']
found_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Found_Type']
ss_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Supstr_Type']
gifa = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'GIFA_(m2)']
#clad_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Clad_Type']
basement = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Basement']
c_true = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Total_Carbon_(A1-A5)_(kgCO2e/m2)'].iloc[0]

design_vars =   {'No_storeys': n_storeys.values[0],
                 'Found_Type': found_type.values[0],
                 'Supstr_Type': ss_type.values[0],
                 'GIFA_(m2)': gifa.values[0],
                 #'Clad_Type': clad_type[0],
                 'Basement': basement.values[0],
                 }

evidence_vals = {}

list_queries = []
out_query = single_carbon_query_call(evidence_vals={})
list_queries.append(out_query)

for var in design_vars.keys():
    evidence_vals[var] = design_vars[var]
    out_query = single_carbon_query_call(evidence_vals=evidence_vals)
    list_queries.append(out_query)

#---Plotting material distributions----------
vline= [[0.81, 0.81, 0.81, 0.81, 0.81, 0.81],
        [-0.49, -0.49, -0.49, -0.49, -0.49, -0.49],
        [0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01],
        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2]]


fig, axs = plt.subplots(nrows=6, ncols=5, gridspec_kw={'width_ratios': [16./41., 4./41., 7./41., 10./41., 4./41]})

fig.set_size_inches(12.5, 12.5)
plt.subplots_adjust(wspace=0.15, hspace=0.05)

titles = [484.15, 0.001, 16.01, 5.94, 120.9]
mat_labels = ['Concrete', 'Masonry&Blockw.\n', 'Reinf.\n', 'Steel(sections)\n', 'Timber(products)\n']

for j in range(0, 6):
    for i in range(0, 5):
        mat_name = BNSettings._material_vars[i]
        Pr_conc = list_queries[j]['mats_qtys'][mat_name]

        x_labels = []
        for val in Pr_conc[list(Pr_conc.columns)[0]].tolist():
            if mat_labels[i] == 'Masonry&Blockw.\n': x_labels.append(str(round(val,2)))
            else: x_labels.append(str(int(val)))
        axs[j, i].bar(x=x_labels, 
                height=Pr_conc[list(Pr_conc.columns)[1]],
                width=1.,
                color='steelblue',
                edgecolor='black', 
                linewidth=0.3
                )
        axs[j, i].axvline(x=vline[i][j], color = 'black', linewidth=1.2, alpha=1., linestyle='dashed', label=r'$q_{true}$')

        axs[j, i].set_ylabel(ylabels[j], fontsize=12)
        if mat_labels[i] == 'Masonry&Blockw.\n': axs[j, i].set_xlabel(mat_labels[i]+r' $(m^2/m^2)$', fontsize=12)
        else: axs[j, i].set_xlabel(mat_labels[i]+r' $(kg/m^2)$', fontsize=12)
        axs[j, i].set_xticks(ticks=x_labels, labels=x_labels, rotation=90)

        axs[j, i].tick_params('x', labelleft=False)
        if j == 0 and i == 0: axs[j, i].set_title(r'$q_{true}= $'+str(titles[i]), fontsize=12)
        elif j == 0: axs[j, i].set_title(str(titles[i]), fontsize=12)

for ax in axs.flat:
    ax.label_outer()
    ax.set_facecolor('whitesmoke')

plt.savefig(fname='Figures/accuracy_example_mats.jpeg', dpi=300)


#---Plotting Tot carbon-----------------------
alphas = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
ylabels = [r'$P(C_T)$', r'$P(C_T | n)$', r'$P(C_T | n,f)$', r'$P(C_T | n,f,s^*)$', r'$P(C_T | n,f,s^*,g)$', r'$P(C_T | n,f,s^*,g,b)$']
titles = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
fig, axs = plt.subplots(2, 3)
fig.set_size_inches(12.5, 8)
plt.subplots_adjust(wspace=0.2, hspace=0.32)
k = 0
for j in range(0, 2):
    for i in range(0, 3):
        
        axs[j, i].hist(x=list_queries[k]['tot_carbon_datapoints'], 
                    bins=list_queries[k]['bins'], 
                    density=True, 
                    alpha=0.7, 
                    label=r'$CI_{95\%}=$'+str(int(list_queries[k]['CI_95'][0][0])),
                    color='moccasin',
                    edgecolor='black', 
                    linewidth=0.3)
        mode, lnspc, pdf_gamma = get_mode(ser=list_queries[k]['tot_carbon_datapoints'])

        axs[j, i].plot(lnspc, pdf_gamma, label=None, color = 'black', linewidth=0.6)
        axs[j, i].axvline(x=mode, color = 'red', linewidth=1.5, alpha=1., label=r'$c_{mode}$')
        axs[j, i].axvline(x=c_true, color = 'black', linewidth=1.2, alpha=1., linestyle='dashed', label=r'$c_{true}$')
        deviation = r'$\|c_{mode} - c_{true}\|=$'+str(int(mode - c_true))
        axs[j, i].legend(loc='upper right', title=deviation)
        axs[j,i].set_xlabel(r'$C_T$'+' '+ r'$(kgCO_{2e}/m^2)$')
        axs[j, i].set_title(titles[k])
        axs[j, i].set_xlim(left=0., right=1200.)
        axs[j, i].set_ylim(top=0.0065)
        axs[j, i].set_ylabel(ylabels[k])
        axs[j, i].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        k = k + 1



    
plt.savefig(fname='Figures/accuracy_example.jpeg', dpi=300)


