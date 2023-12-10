from Bayesian_net.results_scripts.single_carbon_query import powerset, get_connectivity_Hasse_diag, inference_results
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from Bayesian_net.query import QueryMaterials

proj_ref = 153
update_csv_results = False
QueryMaterials(update_datasets=True) # to update the training and validation datasets before running the queries
training_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_training_dataset.csv') 

n_storeys = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'No_storeys']
found_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Found_Type']
ss_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Supstr_Type']
gifa = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'GIFA_(m2)']
#clad_type = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Clad_Type']
basement = training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Basement']

design_vars =   {'No_storeys': n_storeys.values[0],
                 'Found_Type': found_type.values[0],
                 'Supstr_Type': ss_type.values[0],
                 'GIFA_(m2)': gifa.values[0],
                 #'Clad_Type': clad_type.values[0],
                 'Basement': basement.values[0],
                 }


vars_names = []
for var in design_vars.keys():
    vars_names.append(var)
    
full_vars_set = set(vars_names)
list_sets = powerset(s=full_vars_set)
list_sets = sorted(list_sets, key=len)

hasse_conn = get_connectivity_Hasse_diag(list_sets=list_sets)
    
inf_results = inference_results(list_sets=list_sets, 
                                design_vars=design_vars, 
                                Validation_Proj_Ref=proj_ref, 
                                True_tot_Carbon=training_dataset.loc[training_dataset['Proj_Ref'] == proj_ref, 'Total_Carbon_(A1-A5)_(kgCO2e/m2)'].iloc[0], 
                                update_csv_res=update_csv_results,
                                path='Bayesian_net/results_scripts/Data_res/accuracy_journeys.csv') #where the save (or read from) the csv results


#-----Plottting design journeys--------------------------------------

df = pd.read_csv(filepath_or_buffer='Bayesian_net/results_scripts/Data_res/accuracy_journeys.csv')

list_x = []
list_y = []
for link in hasse_conn:
    x_st_node = len(link[0])
    x_end_node = len(link[1])
    list_x.append([x_st_node, x_end_node])
    
    evid_st = str(link[0])
    evid_end = str(link[1])

    y_st_node = abs(df.loc[df['Evidence_vars'] == evid_st, 'Mode_tot_Carbon'] - df.loc[df['Evidence_vars'] == evid_st, 'True_tot_Carbon'])
    y_end_node = abs(df.loc[df['Evidence_vars'] == evid_end, 'Mode_tot_Carbon'] - df.loc[df['Evidence_vars'] == evid_end, 'True_tot_Carbon'])
    #print(y_st_node.values[0], y_end_node.values[0])
    list_y.append([y_st_node, y_end_node])

marker_size = 12
mcface = 'lightgrey'
figure(figsize=(8, 4))
for i in range(0, len(list_x)):
    plt.plot(list_x[i], list_y[i], marker = 'o', color="black", linewidth=0.4, ms = marker_size, mfc = mcface, mec = 'grey')

plt.plot([0, 1], [277., 272.], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([1, 2], [272., 262.], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([2, 3], [262., 250.], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([3, 4], [250., 128.], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([4, 5], [128., 72.], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')

plt.ylabel(ylabel=r'$\|c_{mode} - c_{true}\|$'+' '+r'$(kgCO_{2e}/m^2)$', fontsize=9)
plt.xlabel(xlabel='No. of evidence variables', fontsize=9)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.ylim(0, 350)
plt.savefig(fname='Figures/accuracy_journeys.jpeg', dpi=300)

