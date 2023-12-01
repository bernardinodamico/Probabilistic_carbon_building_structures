from Bayesian_net.query import QueryMaterials, QueryCarbon
from matplotlib import pyplot as plt



#evidence_vals = {} 

evidence_vals = {#'No_storeys': '1_to_3',
                 #'Found_Type': 'Reinforced(Pads/Strips/Raft)',
                 #'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 #'Basement': True,
                 #'Clad_Type': 'Other',
                 #'GIFA_(m2)': 693.11
                 }

qmats = QueryMaterials(update_training_ds=True)
#Run 'run_mats_queries()' only if needing the method's output. It's already called internally when istantiating QueryCarbon()
#res = qmats.run_mats_queries(evidence_vals=evidence_vals) 
queryCarb = QueryCarbon(query_mats=qmats)
carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)
queryCarb.run_tot_carbon(sample_size=20000, carbon_m=carbon_mats, bin_sampling='bin_width', bin_counts=40)

#print(queryCarb.tot_carbon_datapoints)
print('mode=',queryCarb.tot_carbon_mode)
print('mean=',queryCarb.tot_carbon_mean)
print('median=',queryCarb.tot_carbon_median)

#try  project 59 to show progression (and save mats distrib as well)


plt.hist(x=queryCarb.tot_carbon_datapoints, bins=queryCarb.tot_carb_bin_counts, density=True)
plt.show() 