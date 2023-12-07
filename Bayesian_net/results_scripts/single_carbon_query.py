from Bayesian_net.query import QueryMaterials, QueryCarbon
from scipy import stats
import numpy as np


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
    print(mode)

    return mode, lnspc, pdf_gamma