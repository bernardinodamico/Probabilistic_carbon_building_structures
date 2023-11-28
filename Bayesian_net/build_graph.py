from pgmpy.estimators import PC
import pandas as pd
from Bayesian_net.utilities import Plotter
from pandas import DataFrame



class BuildGraph():


    #dataset = pd.read_csv(filepath_or_buffer='Data/discrete_training_dataset_2.csv')
    #dataset.head()

    dataset: DataFrame = None
    nodes: list[str] = None
    edges: list[tuple[str]] = None

    def load_dataset(self, path: str) -> None:
            self.dataset = pd.read_csv(filepath_or_buffer=path)  
            
            return

    def learn_G_from_data(self) -> list[str] | list[tuple[str]]:

        est = PC(data=self.dataset)

        estimated_model = est.estimate(variant="stable", max_cond_vars=5, ci_test="chi_square", 
                                       significance_level=0.02,
                                       return_type="dag"
                                    )

        self.nodes = estimated_model.nodes
        self.edges = estimated_model.edges

        #print("nodes=", nodes)
        #print("edges=", edges)

        pl = Plotter()
        pl.plot_graph(nodes=self.nodes, edges=self.edges, g_type ="dag", savefig_loc_folder='Figures')

        return self.nodes, self.edges
    
    def set_G_manually(self, nodes: list[str], edges: list[tuple[str]]) -> list[str] | list[tuple[str]]:
        self.nodes = nodes
        self.edges = edges

        return self.nodes, self.edges

    def plot_DAG(self, savefig_loc_folder: str) -> None:
        pl = Plotter()
        pl.plot_graph(nodes=self.nodes, edges=self.edges, g_type ="dag", savefig_loc_folder=savefig_loc_folder)

        return
    
G = BuildGraph()
G.load_dataset(path='Data/discrete_training_dataset.csv')
u_nodes = [
    'No_storeys',
    'Basement',
    'Found_Type',
    'Supstr_Type',
    'Supstr_Cr_elems',
    'Supstr_uw',
    'Clad_Type',
    'Concr(kg/m2)',
    'Masnry&Blwk(m2/m2)',
    'Reinf(kg/m2)',
    'Steel_Sec(kg/m2)',
    'Timber_Prod(kg/m2)'
]
u_edges = [
        ('Supstr_Type', 'Timber_Prod(kg/m2)'),
        ('Supstr_Type', 'Steel_Sec(kg/m2)'),
        ('Supstr_Type', 'Supstr_Cr_elems'),
        ('Supstr_Type', 'Supstr_uw'),
        ('Supstr_Type', 'Masnry&Blwk(m2/m2)'),
        ('Clad_Type', 'Masnry&Blwk(m2/m2)'),
        ('Supstr_uw', 'Found_Type'),
        ('No_storeys', 'Found_Type'),
        ('Found_Type', 'Reinf(kg/m2)'),
        ('Found_Type', 'Concr(kg/m2)'),
        ('Supstr_Cr_elems', 'Reinf(kg/m2)'),
        ('Supstr_Cr_elems', 'Concr(kg/m2)'),
        ('Basement', 'Concr(kg/m2)')
]

nodes, edges = G.set_G_manually(nodes=u_nodes, edges=u_edges)
print(nodes, edges)
G.plot_DAG(savefig_loc_folder='Figures')