from Bayesian_net.query import QueryMaterials, QueryCarbon
from matplotlib import pyplot as plt
import pandas as pd
from pandas import DataFrame


def single_carbon_query_call(evidence_vals: dict) -> dict:

    qmats = QueryMaterials(update_training_ds=True)
    #Run 'run_mats_queries()' only if needing the method's output. It's already called internally when istantiating QueryCarbon()
    #res = qmats.run_mats_queries(evidence_vals=evidence_vals) 
    queryCarb = QueryCarbon(query_mats=qmats)
    carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)
    queryCarb.run_tot_carbon(sample_size=40000, carbon_m=carbon_mats, bin_sampling='bin_width', bin_counts=60)

    #print('mode=',queryCarb.tot_carbon_mode)
    print('mean=',queryCarb.tot_carbon_mean)
    #print('median=',queryCarb.tot_carbon_median)

    return {
        'evidence_vals': evidence_vals,
        'tot_carbon_datapoints': queryCarb.tot_carbon_datapoints,
        'mean': queryCarb.tot_carbon_mean,
        'bins': queryCarb.tot_carb_bin_counts
            }

#----------------------------------------------------------------------------------------------------------------------

# sample 144 in the training dataset: true c = 256.7
design_vars =   {'No_storeys': '1_to_3',
                 'Found_Type': 'Mass(Pads/Strips)',
                 'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 'GIFA_(m2)': 3387.218,
                 'Clad_Type': 'Other',
                 'Basement': False,
                 }

evidence_vals = {}

single_carbon_query_call(evidence_vals=evidence_vals)

colors = ['deeppink', 'purple', 'blueviolet', 'dodgerblue', 'lime', 'orange', 'red']
list_queries = []
for var in design_vars.keys():
    evidence_vals[var] = design_vars[var]
    out_query = single_carbon_query_call(evidence_vals=evidence_vals)
    list_queries.append(out_query)
    print(out_query['evidence_vals'])


i = 0
for query_res in list_queries:

    plt.hist(x=query_res['tot_carbon_datapoints'], 
             bins=query_res['bins'], 
             density=True, 
             alpha=0.7, 
             label="aspe",
             color = colors[i],
             edgecolor='black', 
             linewidth=0.75)
    plt.axvline(x=query_res['mean'],
                color = colors[i],
                linewidth=1.5,
                alpha=1.)
    i = i+1

plt.axvline(x=256.7, color='black', linewidth=1.5, alpha=1.) 
plt.legend(loc='upper right')
plt.show()