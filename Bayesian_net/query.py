from Bayesian_net.settings import BNSettings
from Bayesian_net.build_graph import BuildGraph
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pandas import DataFrame
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination
import pandas as pd
from copy import deepcopy
import numpy as np
from numpy import ndarray
from utilities import Plotter

class QueryMaterials():
    
    model: BayesianNetwork = None
    dataset: DataFrame = None
    CPDs: list[TabularCPD] = None

    def __init__(self, update_training_ds: bool = True) -> None:
        self._init_BN_model(update_training_ds=update_training_ds)
        self._buildCPTs()

        return
    
    def _init_BN_model(self, update_training_ds: bool) -> None:
        g_nodes = BNSettings.graph_nodes
        g_edges = BNSettings.graph_edges
        continuous_vars = BNSettings.continuous_vars

        G = BuildGraph()
        if update_training_ds is True:
            G.load_dataset(path='Data/training_dataset.csv')
            G.discretize_cont_vars(cont_vars=continuous_vars, mid_vals=True)
            G.dataset.to_csv(path_or_buf='Data/discrete_training_dataset.csv', index=False)
        else:
            G.load_dataset(path='Data/discrete_training_dataset.csv')
        
        nodes, edges = G.set_G_manually(nodes=g_nodes, edges=g_edges)
        #nodes, edges = G.learn_G_from_data(signif_lev=0.01, nodes=g_nodes)

        model = BayesianNetwork(ebunch=edges)

        self.model = model
        self.dataset = G.dataset

        return
    
    def _buildCPTs(self) -> None:
        if BNSettings.smoothCPT is True:
            self.model.fit(data=self.dataset,
                estimator=BayesianEstimator,  
                prior_type="BDeu",
                equivalent_sample_size=BNSettings.eq_sample_size #the higher the value the more the smoothing
                )
        else:
            self.model.fit(data=self.dataset, estimator=None)

        self.CPDs = self.model.get_cpds()

        return self.CPDs

    def run_inference(self, query_var: str, evidence_vals: dict) -> DataFrame:
        '''
        each dict-key in 'evidence_vals' is a BN variable name whereas the dict-value is the value name assigned
        to that variable, e.g.: {'Supstr_Type': 'Timber_Frame(Glulam&CLT)', 'Basement': False, etc.}
        '''
        inference = VariableElimination(self.model)
        phi_query = inference.query(variables=[query_var], evidence=evidence_vals, elimination_order='MinFill',joint=True, show_progress=False)

        #-------for printing------------- 
        key_st =''
        for k in evidence_vals.keys():
            key_st = key_st+k+'='+f'{evidence_vals[k]}, '
        pr_head  = f'Pr({query_var} | {key_st})'
        pr_head = pr_head.replace(', )', ')')
        query_dic = {**phi_query.state_names, **{pr_head: list(phi_query.values)}}

        #----------return CPD of queried material
        query_cpd = pd.DataFrame(query_dic)
        #print(query_cpd)
        #plot = Plotter()
        #plot.plot_pr_distrib(prT=query_cpd, savefig_loc_folder='Figures', break_text_label=True)

        return query_cpd
    
    def run_mats_queries(self, evidence_vals: dict) -> dict[str: DataFrame]:
        '''
        returns a dictionary with dict-keys = material variable names and dict-values = the corresponding prob distribution
        '''
        L = {}
        for mat in BNSettings._material_vars:
            query_cpd = self.run_inference(query_var=mat, evidence_vals=evidence_vals)
            L[mat] = query_cpd

        return L



class QueryCarbon():
    qm: QueryMaterials = None

    def __init__(self, query_mats: QueryMaterials) -> None:
        self.qm = query_mats
        return

    def run_carbon_mats_queries(self, evidence_vals: dict) -> dict[str: DataFrame]:
        '''
        Each dict-key in 'evidence_vals' is a BN variable name whereas the dict-value is the value name assigned
        to that variable, e.g.: {'Supstr_Type': 'Timber_Frame(Glulam&CLT)', 'Basement': False, etc.}

        Returns a dictionary with dict-keys = material variable names and dict-values = the corresponding carbon prob distribution
        '''
        
        pr_distrib_all_mats = self.qm.run_mats_queries(evidence_vals=evidence_vals)

        L = {}
        for mat in pr_distrib_all_mats.keys():

            mat_prb_dist: DataFrame = pr_distrib_all_mats[mat]

            carbon_mat_prb_dist = deepcopy(mat_prb_dist)
            carbon_mat_prb_dist[mat] = carbon_mat_prb_dist[mat] * BNSettings.carbon_coefficients[mat]

            #-----rename Pr column----
            pr_name_old: str = carbon_mat_prb_dist.keys().to_list()[-1]
            pr_name: str = pr_name_old.replace(mat, 'Carbon_'+mat)
            carbon_mat_prb_dist = carbon_mat_prb_dist.rename(columns={mat: 'Carbon_'+mat, pr_name_old: pr_name})

            #print(carbon_mat_prb_dist)
            L[mat] = carbon_mat_prb_dist

        return L
    


    def run_tot_carbon(self, sample_size: int, carbon_m: dict[str: DataFrame], bin_sampling: str = 'mid_val') -> DataFrame:
        '''
        Montecarlo sampling to get the sample carbon pop of two carbon material populations combined

        If  bin_sampling = mid_val -> the carbon material sampling only draws values among the discrete range of bins' mid values.

        If bin_sampling = bin_width -> the carbon material sampling draws values across the continuous range (with probability of the bin where the value falls).
        '''

        carbon_mat_a = carbon_m['Concr(kg/m2)']
        carbon_mat_b = carbon_m['Masnry&Blwk(m2/m2)']
        carbon_mat_c = carbon_m['Reinf(kg/m2)']
        carbon_mat_d = carbon_m['Steel_Sec(kg/m2)']
        carbon_mat_e = carbon_m['Timber_Prod(kg/m2)']
        
        bin_width_a = carbon_mat_a.iloc[-1, 0] - carbon_mat_a.iloc[-2, 0]    
        bin_width_b = carbon_mat_b.iloc[-1, 0] - carbon_mat_b.iloc[-2, 0]
        bin_width_c = carbon_mat_c.iloc[-1, 0] - carbon_mat_c.iloc[-2, 0]    
        bin_width_d = carbon_mat_d.iloc[-1, 0] - carbon_mat_d.iloc[-2, 0]
        bin_width_e = carbon_mat_e.iloc[-1, 0] - carbon_mat_e.iloc[-2, 0]    


        
        weighted_draw_a = np.random.choice(a=carbon_mat_a.iloc[:, 0], size=sample_size, p=carbon_mat_a.iloc[:, -1]) 
        weighted_draw_b = np.random.choice(a=carbon_mat_b.iloc[:, 0], size=sample_size, p=carbon_mat_b.iloc[:, -1])
        weighted_draw_c = np.random.choice(a=carbon_mat_c.iloc[:, 0], size=sample_size, p=carbon_mat_c.iloc[:, -1]) 
        weighted_draw_d = np.random.choice(a=carbon_mat_d.iloc[:, 0], size=sample_size, p=carbon_mat_d.iloc[:, -1])
        weighted_draw_e = np.random.choice(a=carbon_mat_e.iloc[:, 0], size=sample_size, p=carbon_mat_e.iloc[:, -1]) 
        print(weighted_draw_a)
        print(weighted_draw_b)

        
        if bin_sampling == 'bin_width':
            # to pick uniformly within the bin(s) instead of picking the mid-value(s) all the time
            noise_a = (np.random.rand(sample_size) * bin_width_a) - (bin_width_a / 2.)
            noise_b = (np.random.rand(sample_size) * bin_width_b) - (bin_width_b / 2.)
            noise_c = (np.random.rand(sample_size) * bin_width_c) - (bin_width_c / 2.)
            noise_d = (np.random.rand(sample_size) * bin_width_d) - (bin_width_d / 2.)
            noise_e = (np.random.rand(sample_size) * bin_width_e) - (bin_width_e / 2.)
            weighted_draw_a = np.add(weighted_draw_a, noise_a)
            weighted_draw_b = np.add(weighted_draw_b, noise_b)
            weighted_draw_c = np.add(weighted_draw_c, noise_c)
            weighted_draw_d = np.add(weighted_draw_d, noise_d)
            weighted_draw_e = np.add(weighted_draw_e, noise_e)
        elif bin_sampling == 'mid_val':
            pass 

        tot_carbon = np.add(weighted_draw_a, weighted_draw_b)
        tot_carbon = np.add(tot_carbon, weighted_draw_c)
        tot_carbon = np.add(tot_carbon, weighted_draw_d)
        tot_carbon = np.add(tot_carbon, weighted_draw_e)

        return tot_carbon
        


#evidence_vals = {'Supstr_Type': 'Timber_Frame(Glulam&CLT)', 'Basement': False } 

qmats = QueryMaterials(update_training_ds=True)
#res = qmats.run_mats_queries(evidence_vals=evidence_vals)
#print(res['Concr(kg/m2)'])

queryCarb = QueryCarbon(query_mats=qmats)
#carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)

#print(res['Concr(kg/m2)'])


data_a = [[7.5, 0.7], [12.5, 0.3]] 
data_b = [[5., 0.4], [11., 0.6]]
carb_mat_a = pd.DataFrame(data_a, columns=['carbon_mat_a', 'Pr(a)']) 
carb_mat_b = pd.DataFrame(data_b, columns=['carbon_mat_b', 'Pr(b)']) 
carb_mat_c = pd.DataFrame(data_a, columns=['carbon_mat_c', 'Pr(c)']) 
carb_mat_d = pd.DataFrame(data_b, columns=['carbon_mat_d', 'Pr(d)'])
carb_mat_e = pd.DataFrame(data_a, columns=['carbon_mat_e', 'Pr(e)']) 

carbon_mats = {
    'Concr(kg/m2)': carb_mat_a,
    'Masnry&Blwk(m2/m2)': carb_mat_b,
    'Reinf(kg/m2)': carb_mat_c,
    'Steel_Sec(kg/m2)': carb_mat_d,
    'Timber_Prod(kg/m2)': carb_mat_e
}

tot_carbon = queryCarb.run_tot_carbon(sample_size=10, carbon_m=carbon_mats, bin_sampling='mid_val')

print(tot_carbon)