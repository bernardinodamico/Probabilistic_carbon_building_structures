import pandas as pd 
from pandas import DataFrame
from matplotlib import pyplot as plt
from Bayesian_net.customExceptions import ProbTableError
import time
from Bayesian_net.prob_table import ProbTable

class Plotter():

    _bottom: float = 0.4
    _left: float = 0.2

    def plot_pr_distrib(self, prT: ProbTable, savefig_loc_folder: str, size_inches: int = 6, dpi: int = 300, color: str = 'dodgerblue', break_text_label: bool = False, y_axis: str = 'dynamic') -> None:
        '''
        Plots a hystogram showing the probability distibution (marginal or conditional) of a variable
        Inputs: 
        - prob_table: a two-column Dataframe
        - savefig_loc_folder: the path of the folder where to safe the figure (the figure filename is not needed)
        - size_inches (optional, default = 6): the Figure width and depth
        - dpi (optional, default = 300)
        - color (optional, default = 'dodgerblue')
        - y_axis (optional, defaul = 'dynamic'): if y_axis='dynamic' the 'y' axis is scaled to the max probability vale in the distribution
        if y_axis='constant' the 'y' axis is scaled to 100% probability value.
        '''
        x_labels = []
        for val in prT.table[list(prT.table.columns)[0]].tolist():
            x_labels.append(str(val))

        if len(prT.table.columns) != 2:
            raise ProbTableError(table=prT.table)
        fig, ax = plt.subplots()
        fig.set_size_inches(size_inches, size_inches)
        fig.set_dpi(dpi)
        if y_axis == 'constant': ax.set(ylim=[0, 1])
        plt.subplots_adjust(bottom=self._bottom, left=self._left)

        plt.bar(x=x_labels, 
                height=prT.table[list(prT.table.columns)[1]],
                width=0.96,
                color=color,
                )
        plt.xticks(rotation=90)
        
        plt.xlabel(list(prT.table.columns)[0], fontweight='bold')
        if break_text_label is True: y_label = break_labels(text=list(prT.table.columns)[1])
        else: y_label = list(prT.table.columns)[1]
        plt.ylabel(y_label, fontweight='bold')
        #plt.show()

        #----Save figure---------------------------------
        fn: str = list(prT.table.columns)[1]
        fn = fn.replace('/', '@')
        filename = fn.replace('|', 'given')
        filename = filename + current_time_millisecond()
        path: str = savefig_loc_folder+f'/{filename}.png'
    
        plt.savefig(path)

        return

def current_time_millisecond():
    return str(round(time.time() * 1000))

def break_labels(text: str)-> str:
    text = text.replace('|', '|\n')
    btext = text.replace(',', ',\n')
    return btext

def discretizer(dataset: DataFrame, vars: list[str], bin_counts: list[int], mid_vals: bool = False) -> DataFrame:
    '''
    A method to discretise values of a continuous variable.
    Inputs:
        - dataset: a panda Dataframe
        - vars: a list of the columns headings to be discretised
        - bin_counts: a list matching "vars". Each integer in the list indicates the number of equally sized bins to divide the variabel domain into.
        - mid_vals (optional, default=False): if True, the bins mid-values are returned. If False, a pandas category dtype is returned containing the min/max value of each bin
    Output: 
        - the dataset with updated columns values
    '''
    for i in range(0, len(vars)):
        col = dataset[vars[i]]
        new_col = pd.cut(x=col, bins=bin_counts[i])
        if mid_vals == True:
            bin_vals = []
            for cat in new_col.items():
                bin_vals.append(round(cat[1].mid, 3))
            dataset[vars[i]] = bin_vals
            #dataset = dataset.rename(columns={vars[i]: vars[i]+f'[+/-{round(cat[1].mid - cat[1].left, 3)}]'})
        else:
            dataset[vars[i]] = new_col

    return dataset
        
