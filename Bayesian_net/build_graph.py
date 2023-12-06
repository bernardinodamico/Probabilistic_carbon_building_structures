from pgmpy.estimators import PC
import pandas as pd
from Bayesian_net.utilities import Plotter
from pandas import DataFrame
from Bayesian_net.utilities import discretizer
from copy import deepcopy

class BuildGraph():

    continuous_full_dataset: DataFrame = None
    discrete_full_dataset: DataFrame = None
    tr_dataset: DataFrame = None
    vald_dataset: DataFrame = None
    nodes: list[str] = None
    edges: list[tuple[str]] = None

    def load_dataset(self, path: str) -> None:
            self.continuous_full_dataset = pd.read_csv(filepath_or_buffer=path)  
            
            return
    
    def discretize_cont_vars(self, cont_vars: list[dict], mid_vals: bool = False) -> DataFrame:
        vars_list = []
        bins_list = []
        for v in cont_vars:
            vars_list.append(v['name'])
            bins_list.append(v['bins'])
        
        self.discrete_full_dataset = discretizer(dataset=self.continuous_full_dataset,
                                      vars=vars_list,
                                      bin_counts=bins_list,
                                      mid_vals=mid_vals)
        
        return self.discrete_full_dataset

    def extract_vald_dataset(self, ID_projs: list[int])-> None:
        '''
        ID_projs = a list containing Project refs in the "full_dataset.csv" to be used for the validation dataset
        '''
        self.vald_dataset = deepcopy(self.discrete_full_dataset)
        self.tr_dataset = deepcopy(self.discrete_full_dataset)

        indexRows = self.discrete_full_dataset[self.discrete_full_dataset['Proj_Ref'].isin(ID_projs)].index
        self.tr_dataset = self.tr_dataset.drop(indexRows)

        indexRows = self.discrete_full_dataset[~self.discrete_full_dataset['Proj_Ref'].isin(ID_projs)].index
        self.vald_dataset = self.vald_dataset.drop(indexRows)

        return


    def learn_G_from_data(self, signif_lev: float, nodes: list[str]) -> list[str] | list[tuple[str]]:


        ds = pd.DataFrame()
        for var in nodes:
            if var in self.tr_dataset.columns:
                ds[var] = self.tr_dataset[var]

        est = PC(data=ds)

        estimated_model = est.estimate(variant="stable", max_cond_vars=5, ci_test="chi_square", 
                                       significance_level=signif_lev,
                                       return_type="dag"
                                    )

        self.nodes = estimated_model.nodes
        self.edges = estimated_model.edges
        self.tr_dataset = ds

        #print("nodes=", nodes)
        #print("edges=", edges)

        return self.nodes, self.edges
    
    def set_G_manually(self, nodes: list[str], edges: list[tuple[str]]) -> list[str] | list[tuple[str]]:
        ds = pd.DataFrame()
        for var in nodes:
            if var in self.tr_dataset.columns:
                ds[var] = self.tr_dataset[var]
        
        self.nodes = nodes
        self.edges = edges
        self.tr_dataset = ds

        return self.nodes, self.edges

    def plot_DAG(self, savefig_loc_folder: str) -> None:
        pl = Plotter()
        pl.plot_graph(nodes=self.nodes, edges=self.edges, g_type ="dag", savefig_loc_folder=savefig_loc_folder)

        return
    

