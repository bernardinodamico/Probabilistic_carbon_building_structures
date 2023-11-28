from Bayesian_net.settings import BNSettings
from Bayesian_net.build_graph import BuildGraph
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pandas import DataFrame
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination
import pandas as pd
from utilities import Plotter

class QueryMaterial():
    
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
    
    def run_mats_queries(self, evidence_vals: dict) -> list[DataFrame]:
        L = []
        for mat in BNSettings.material_vars:
            query_cpd = self.run_inference(query_var=mat, evidence_vals=evidence_vals)
            L.append(query_cpd)

        return L


qm = QueryMaterial()

evidence_vals = {'Supstr_Type': 'Timber_Frame(Glulam&CLT)', 'Basement': False } 
query_cpd = qm.run_inference(query_var='Concr(kg/m2)', evidence_vals=evidence_vals)

print(query_cpd)

plot = Plotter()
plot.plot_pr_distrib(prT=query_cpd, savefig_loc_folder='Figures',break_text_label=True)

pr_distrib_all_mats = qm.run_mats_queries(evidence_vals=evidence_vals)