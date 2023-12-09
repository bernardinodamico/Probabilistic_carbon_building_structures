from Bayesian_net.results_scripts.single_carbon_query import powerset, get_connectivity_Hasse_diag, inference_results_mupti_p
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from Bayesian_net.settings import BNSettings
from Bayesian_net.query import QueryMaterials



update_csv_results=True
test_sample_IDs = BNSettings.test_samples_IDs
QueryMaterials(update_datasets=True) # to update the training and validation datasets before running the queries
validation_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_validation_dataset.csv')

if update_csv_results is True:
    all_results = []
    for i in range(0, len(test_sample_IDs)):
        proj_ref = test_sample_IDs[i]

        n_storeys = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'No_storeys']
        found_type = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'Found_Type']
        ss_type = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'Supstr_Type']
        gifa = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'GIFA_(m2)']
        clad_type = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'Clad_Type']
        basement = validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'Basement']

        design_vars =   {'No_storeys': n_storeys.values[0],
                        'Found_Type': found_type.values[0],
                        'Supstr_Type': ss_type.values[0],
                        'GIFA_(m2)': gifa.values[0],
                        'Clad_Type': clad_type.values[0],
                        'Basement': basement.values[0],
                        }
        
        vars_names = []
        for var in design_vars.keys():
            vars_names.append(var)
            
        full_vars_set = set(vars_names)
        list_sets = powerset(s=full_vars_set)
        list_sets = sorted(list_sets, key=len)

        hasse_conn = get_connectivity_Hasse_diag(list_sets=list_sets)
        print(f'====== Project datapoint {i} out of {len(test_sample_IDs)}===========')
        inf_results = inference_results_mupti_p(list_sets=list_sets, 
                                                design_vars=design_vars, 
                                                Validation_Proj_Ref=proj_ref, 
                                                True_tot_Carbon=validation_dataset.loc[validation_dataset['Proj_Ref'] == proj_ref, 'Total_Carbon_(A1-A5)_(kgCO2e/m2)'].iloc[0], 
                                                ) 
        for r in inf_results:
            all_results.append(r)
    inference_res = pd.DataFrame(all_results)
    inference_res.to_csv(path_or_buf='Bayesian_net/results_scripts/Data_res/accuracy_test.csv') #where the save (or read from) the csv results

#-----Plottting prediction error--------------------------------------

df = pd.read_csv(filepath_or_buffer='Bayesian_net/results_scripts/Data_res/accuracy_test.csv')

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


plt.ylabel(ylabel=r'$\|c_{mode} - c_{true}\|$'+' '+r'$(kgCO_{2e}/m^2)$', fontsize=9)
plt.xlabel(xlabel='No. of evidence variables', fontsize=9)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
#plt.ylim(0, 170)
plt.savefig(fname='Figures/accuracy_test.jpeg', dpi=300)

