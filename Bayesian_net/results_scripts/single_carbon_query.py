from Bayesian_net.query import QueryMaterials, QueryCarbon
from scipy import stats
import numpy as np
import pandas as pd 
from pandas import DataFrame


def single_carbon_query_call(evidence_vals: dict) -> dict:

    qmats = QueryMaterials(update_training_ds=True)
    #Run 'run_mats_queries()' only if needing the method's output. It's already called internally when istantiating QueryCarbon()
    mats_qtys = qmats.run_mats_queries(evidence_vals=evidence_vals) 
    queryCarb = QueryCarbon(query_mats=qmats)
    carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)
    queryCarb.run_tot_carbon(sample_size=50000, carbon_m=carbon_mats, bin_sampling='bin_width', bin_counts=40)


    return {
        'evidence_vals': evidence_vals,
        'tot_carbon_datapoints': queryCarb.tot_carbon_datapoints,
        'mean': queryCarb.tot_carbon_mean,
        'bins': queryCarb.tot_carb_bin_counts,
        'CI_95': queryCarb.confidence_interval,
        'mats_qtys': mats_qtys
            }

def get_mode(ser)-> float:


    lnspc = np.arange(0,2000) # the range of x 

    ag,bg,cg = stats.gamma.fit(ser)  
    pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  

    mode = lnspc[stats.gamma.pdf(lnspc, ag, bg,cg).argmax()] # find the x value to maximize pdf
    #print(mode)

    return mode, lnspc, pdf_gamma

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



def inference_results(list_sets: list[set], design_vars: dict, Validation_Proj_Ref: int, True_tot_Carbon: float, update_csv_res: bool, path: str) -> DataFrame:

    if update_csv_res is True:
        t = []
        for ss in list_sets:
            #print(ss)
            evidence_vals = {}
            for var in ss:
                evidence_vals[var] = design_vars[var]
            #print(evidence_vals)
            out = single_carbon_query_call(evidence_vals=evidence_vals)

            mode, lnspc, pdf_gamma = get_mode(ser=out['tot_carbon_datapoints'])
            print(f'query {list_sets.index(ss)} out of {len(list_sets)}')
            t.append({'Validation_Proj_Ref': Validation_Proj_Ref, 'True_tot_Carbon': True_tot_Carbon, 'Mode_tot_Carbon': mode, 'Evidence_vars': ss})
        inference_res = pd.DataFrame(t)
        inference_res.to_csv(path_or_buf=path)
    
    else:
        inference_res = pd.read_csv(path_or_buf=path)
    
    return inference_res



def get_connectivity_Hasse_diag(list_sets: list[set]) ->list[list[set]]:
    '''
    given a list of sets returns a list containing a two-item list of start node (set) and end node (set) of the Hasse diagram
    see: https://demonstrations.wolfram.com/HasseDiagramOfPowerSets/
    '''
    connectivity_L = []
    for i in range(0, len(list_sets)):
        st_node = list_sets[i]
        for j in range(0, len(list_sets)):
            if len(list_sets[j]) == len(list_sets[i]) + 1:
                if st_node.issubset(list_sets[j]) is True:
                    end_node = list_sets[j]
                    connectivity_L.append([st_node, end_node])
                    #print([st_node, end_node])
    
    return connectivity_L