from Bayesian_net.query import QueryMaterials, QueryCarbon
from matplotlib import pyplot as plt

def single_carbon_query_call(evidence_vals: dict) -> dict:

    qmats = QueryMaterials(update_training_ds=True)
    #Run 'run_mats_queries()' only if needing the method's output. It's already called internally when istantiating QueryCarbon()
    #res = qmats.run_mats_queries(evidence_vals=evidence_vals) 
    queryCarb = QueryCarbon(query_mats=qmats)
    carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)
    queryCarb.run_tot_carbon(sample_size=50000, carbon_m=carbon_mats, bin_sampling='bin_width', bin_counts=40)

    #print('mode=',queryCarb.tot_carbon_mode)
    print('mean=',queryCarb.tot_carbon_mean)
    #print('median=',queryCarb.tot_carbon_median)

    return {
        'evidence_vals': evidence_vals,
        'tot_carbon_datapoints': queryCarb.tot_carbon_datapoints,
        'mean': queryCarb.tot_carbon_mean,
        'bins': queryCarb.tot_carb_bin_counts,
        'CI_95': queryCarb.confidence_interval
            }

#----------------------------------------------------------------------------------------------------------------------

# sample 144 in the training dataset: true c = 256.7
design_vars =   {'No_storeys': '1_to_3',
                 'Found_Type': 'Mass(Pads/Strips)',
                 'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 'GIFA_(m2)': 3387.218,
                 #'Clad_Type': 'Other',
                 'Basement': False,
                 }

evidence_vals = {}

list_queries = []
out_query = single_carbon_query_call(evidence_vals={})
list_queries.append(out_query)

for var in design_vars.keys():
    evidence_vals[var] = design_vars[var]
    out_query = single_carbon_query_call(evidence_vals=evidence_vals)
    list_queries.append(out_query)

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
                    alpha=alphas[k], 
                    label=r'$CI_{95\%}=$'+str(round(list_queries[k]['CI_95'][0][0], 1)),
                    color='blue',
                    edgecolor='black', 
                    linewidth=0.4)
        axs[j, i].axvline(x=list_queries[k]['mean'], color = 'red', linewidth=1.2, alpha=1., label=r'$c_{mean}$')
        axs[j, i].axvline(x=256.7, color = 'black', linewidth=1.2, alpha=1., linestyle='dashed', label=r'$c_{true}$')
        deviation = r'$\|c_{mean} - c_{true}\|=$'+str(round(list_queries[k]['mean'] - 256.7, 1))
        axs[j, i].legend(loc='upper right', title=deviation)
        axs[j,i].set_xlabel(r'$C_T$'+' '+ r'$(kgCO_{2e}/m^2)$')
        axs[j, i].set_title(titles[k])
        axs[j, i].set_xlim(left=0., right=1200.)
        axs[j, i].set_ylim(top=0.0065)
        axs[j, i].set_ylabel(ylabels[k])
        axs[j, i].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        k = k + 1



#for ax in axs.flat:
    #ax.label_outer()
    

plt.savefig(fname='Figures/accuracy_example.jpeg', dpi=300)