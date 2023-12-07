from Bayesian_net.results_scripts.single_carbon_query import single_carbon_query_call, get_mode
import pandas as pd


validation_dataset = pd.read_csv(filepath_or_buffer='Data/discrete_validation_dataset.csv') 


# need a method that generates a list of different query calls for each validation datapoint.
# there are 5 vars in each datapoint. 


def powerset(s: list):
    x = len(s)
    for i in range(1 << x):
        print([s[j] for j in range(x) if (i & (1 << j))])


powerset(['n', 'f', 's*', 'g', 'b'])


design_vars =   {'No_storeys': '1_to_3',
                 'Found_Type': 'Mass(Pads/Strips)',
                 'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 'GIFA_(m2)': 3387.218,
                 #'Clad_Type': 'Other',
                 'Basement': False,
                 }



#heading for the output dataframe:

'''
Validation_Proj_Ref, True_tot_Carbon, Mode_tot_Carbon, No_evidence_vars, ID_design_journey
'''