from Bayesian_net.results_scripts.single_carbon_query import powerset, get_connectivity_Hasse_diag, inference_results
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from pandas import DataFrame

#validation_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_validation_dataset.csv') 


# sample 144 in the training dataset: c_true = 256.7
design_vars =   {'No_storeys': '1_to_3',
                 'Found_Type': 'Mass(Pads/Strips)',
                 'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 'GIFA_(m2)': 3387.218,
                 #'Clad_Type': 'Other',
                 'Basement': False,
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
                                Validation_Proj_Ref=144, 
                                True_tot_Carbon=256.7, 
                                update_csv_res=False,
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

plt.plot([0, 1], [155.3, 149.3], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([1, 2], [149.3, 122.3], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([2, 3], [122.3, 81], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([3, 4], [81, 45], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')
plt.plot([4, 5], [45, 14.3], marker = 'o', color="black", linewidth=1.2, ms = marker_size, mfc = mcface, mec = 'black')

plt.ylabel(ylabel=r'$\|c_{mode} - c_{true}\|$'+' '+r'$(kgCO_{2e}/m^2)$', fontsize=9)
plt.xlabel(xlabel='No. of evidence variables', fontsize=9)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.ylim(0, 170)
plt.savefig(fname='Figures/accuracy_journeys.jpeg', dpi=300)

