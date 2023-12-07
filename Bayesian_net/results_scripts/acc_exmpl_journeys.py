from Bayesian_net.results_scripts.single_carbon_query import single_carbon_query_call, get_mode
import pandas as pd


validation_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_validation_dataset.csv') 


# need a method that generates a list of different query calls for each validation datapoint.
# there are 5 vars in each datapoint. 


def powerset(s: set) -> list[set]:
    '''
    given a set "s" of items returns a list containing all subsets of "s", including "s" itself 
    '''
    x = len(list(s))
    list_subsets = []
    for i in range(1 << x):
        subset = set([list(s)[j] for j in range(x) if (i & (1 << j))])
        list_subsets.append(subset)
        #print(subset)
    
    return list_subsets


full_vars_set = set(['n', 'f', 's*', 'g', 'b'])
l_sets = powerset(s=full_vars_set)
l_sets = sorted(l_sets, key=len)


for ss in l_sets:
    print(ss)





















design_vars =   {'No_storeys': '1_to_3',
                 'Found_Type': 'Mass(Pads/Strips)',
                 'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 'GIFA_(m2)': 3387.218,
                 #'Clad_Type': 'Other',
                 'Basement': False,
                 }



#heading for the output dataframe:

'''
Validation_Proj_Ref, True_tot_Carbon, Mode_tot_Carbon, Num_evidence_vars, ID_design_journey
'''