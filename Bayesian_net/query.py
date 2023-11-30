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
import matplotlib.pyplot as plt
from numpy import ndarray
from utilities import discretizer, Plotter

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
    evidence_vals: dict = None
    tot_carbon_mean: float = None
    tot_carbon_median: float = None
    tot_carbon_mode: float = None #the value that shows up most often
    prob_distrib_Totcarbon: DataFrame = None
    tot_carbon_datapoints: DataFrame = None
    tot_carb_bin_counts: int = None

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
            self.evidence_vals = evidence_vals
            L[mat] = carbon_mat_prb_dist

        return L
    
    def fetch_heading_compl(self) -> str:
        if self.evidence_vals is None:
            return ")"
        else:
            s = " | "
            for var_namekey in self.evidence_vals.keys():
                s = s + f"{var_namekey}={self.evidence_vals[var_namekey]}, " 
            s = s + ")"
            string = s.replace(", )", "")
            return string


    def run_tot_carbon(self, sample_size: int, carbon_m: dict[str: DataFrame], bin_sampling: str = 'mid_val', bin_counts: int = 40) -> DataFrame:
        '''
        Montecarlo sampling to get the sample carbon pop of all carbon material distributions combined

        If  bin_sampling = mid_val -> the carbon material sampling only draws values among the discrete range of bins' mid values.

        If bin_sampling = bin_width -> the carbon material sampling draws values across the continuous range (with probability of the bin where the value falls).
        '''
        
        tot_carbon_datapoints = np.zeros(sample_size)
        
        for mat_name in carbon_m.keys():
            carbon_mat = carbon_m[mat_name]
            bin_width = carbon_mat.iloc[-1, 0] - carbon_mat.iloc[-2, 0] 
            weighted_draw = np.random.choice(a=carbon_mat.iloc[:, 0], size=sample_size, p=carbon_mat.iloc[:, -1])
            
            if bin_sampling == 'bin_width':
                # to pick uniformly within the bin(s) instead of picking the mid-value(s) all the time
                noise = (np.random.rand(sample_size) * bin_width) - (bin_width / 2.)
                weighted_draw = np.add(weighted_draw, noise)
            else:
                pass
            tot_carbon_datapoints = np.add(tot_carbon_datapoints, weighted_draw)
        
        tot_carbon_datapoints = pd.DataFrame(tot_carbon_datapoints, columns=['tot_carbon'])

        self.tot_carbon_mean = list(tot_carbon_datapoints.mean())[0]
        self.tot_carbon_median = list(tot_carbon_datapoints.median())[0]

        tot_carb_disc = discretizer(dataset=tot_carbon_datapoints, vars=['tot_carbon'], bin_counts=[bin_counts], mid_vals = True) 
        self.tot_carbon_mode = tot_carb_disc.mode()

        series = tot_carb_disc.value_counts(subset='tot_carbon', normalize=True)
        df_1 = series.index.to_frame().reset_index(drop=True)
        df_2 = series.to_frame().reset_index(drop=True)
        prT = df_1.join(other=df_2)

        prT = prT.rename({'proportion': 'Pr(tot_carbon'+f'{self.fetch_heading_compl()})'}, axis='columns')
        
        self.prob_distrib_Totcarbon = prT
        self.tot_carbon_datapoints = tot_carbon_datapoints
        self.tot_carb_bin_counts = bin_counts

        return 
    
        


#evidence_vals = {} 

evidence_vals = {#'No_storeys': '1_to_3',
                 #'Found_Type': 'Reinforced(Pads/Strips/Raft)',
                 #'Supstr_Type': 'Timber_Frame(Glulam&CLT)',
                 #'Basement': True,
                 #'Clad_Type': 'Other',
                 #'GIFA_(m2)': 693.11
                 }

qmats = QueryMaterials(update_training_ds=True)
#Run 'run_mats_queries()' only if needing the method's output. It's already called internally when istantiating QueryCarbon()
#res = qmats.run_mats_queries(evidence_vals=evidence_vals) 
queryCarb = QueryCarbon(query_mats=qmats)
carbon_mats = queryCarb.run_carbon_mats_queries(evidence_vals=evidence_vals)
queryCarb.run_tot_carbon(sample_size=20000, carbon_m=carbon_mats, bin_sampling='bin_width', bin_counts=40)

#print(queryCarb.tot_carbon_datapoints)
print(queryCarb.tot_carbon_mode)


#try  project 59 to show progression (and save mats distrib as well)


plt.hist(x=queryCarb.tot_carbon_datapoints, bins=queryCarb.tot_carb_bin_counts, density=True)
plt.show() 

