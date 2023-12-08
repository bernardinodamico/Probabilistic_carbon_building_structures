from Bayesian_net.results_scripts.single_carbon_query import powerset, get_connectivity_Hasse_diag, inference_results


#validation_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_validation_dataset.csv') 





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
                                update_csv_res=True,
                                path='Bayesian_net/results_scripts/Data_res/acc_exmpl_journeys.csv') #where the csv results are saved or read





















#heading for the output dataframe:

'''
Validation_Proj_Ref, True_tot_Carbon, Mode_tot_Carbon, Evidence_vars
'''