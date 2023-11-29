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
from utilities import Plotter

class QueryMaterials():
    
    model: BayesianNetwork = None
    dataset: DataFrame = None
    CPDs: list[TabularCPD] = None

    def __init__(self) -> None:
        self._init_BN_model()
        self._buildCPTs()

        return
    
    def _init_BN_model(self) -> None:
        g_nodes = BNSettings.graph_nodes
        g_edges = BNSettings.graph_edges
        continuous_vars = BNSettings.continuous_vars

        G = BuildGraph()
        G.load_dataset(path='Data/training_dataset.csv')
        G.discretize_cont_vars(cont_vars=continuous_vars, mid_vals=True)

        nodes, edges = G.set_G_manually(nodes=g_nodes, edges=g_edges)
        #nodes, edges = G.learn_G_from_data(signif_lev=0.01, nodes=g_nodes)

        G.dataset.to_csv(path_or_buf='Data/discrete_training_dataset.csv', index=False)

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

    def __init__(self) -> None:
        self.qm = QueryMaterials()
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
    


#evidence_vals = {'Supstr_Type': 'Timber_Frame(Glulam&CLT)', 'Basement': False } 

#qmats = QueryMaterials()
#res = qmats.run_mats_queries(evidence_vals=evidence_vals)
#print(res['Concr(kg/m2)'])

#queryCarb = QueryCarbon()
#res = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)

#print(res['Concr(kg/m2)'])

sample_size: int = 10
data_a = [[7.5, 0.7], [12.5, 0.3]] 
data_b = [[5., 0.4], [11., 0.6]]
carbon_mat_a = pd.DataFrame(data_a, columns=['carbon_mat_a', 'Pr(a)']) 
carbon_mat_b = pd.DataFrame(data_b, columns=['carbon_mat_b', 'Pr(b)']) 


bin_width_a = carbon_mat_a.iloc[-1, 0] - carbon_mat_a.iloc[-2, 0]    
bin_width_b = carbon_mat_b.iloc[-1, 0] - carbon_mat_b.iloc[-2, 0]
noise_a = (np.random.rand(sample_size) * bin_width_a) - (bin_width_a / 2.)
noise_b = (np.random.rand(sample_size) * bin_width_b) - (bin_width_b / 2.)
print(carbon_mat_a)
#print(carbon_mat_b)


weighted_draw_a = np.random.choice(a=carbon_mat_a.iloc[:, 0], size=sample_size, p=carbon_mat_a.iloc[:, -1])
print(weighted_draw_a)
weighted_draw_b = np.random.choice(a=carbon_mat_b.iloc[:, 0], size=sample_size, p=carbon_mat_b.iloc[:, -1])
#print(weighted_draw_b)


weighted_draw_a = np.add(weighted_draw_a, noise_a)
print(weighted_draw_a)

tot_carb_sample = np.add(weighted_draw_a, weighted_draw_b)
#print(tot_carb_sample)