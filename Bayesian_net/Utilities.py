import pandas as pd 
from pandas import DataFrame
from matplotlib import pyplot as plt

class ProbTableError(Exception):
    '''
    Exception raised for errors in the Plotting method.
    '''
    def __init__(self, table):
        self.table = table

        self.message = "the probability_table must have exactly two columns"
        super().__init__(self.message)


class Plotter():

    _aspect: float = 4.3
    _bottom: float = 0.45

    def plot_pr_table(self, prob_table: DataFrame, savefig_loc_folder: str, size_inches: int = 6, dpi: int = 300, color: str = 'dodgerblue') -> None:
        '''
        Plots a hystogram showing the probability distibution (marginal or conditional) of a variable
        Inputs: 
        - prob_table: a two-column Dataframe
        - savefig_loc_folder: the path of the folder where to safe the figure (the figure filename is not needed)
        - size_inches (optional, default = 6): the Figure width and depth
        - dpi (optional, default = 300)
        - color (optional, default = 'dodgerblue')
        '''
        x_labels = []
        for val in prob_table[list(prob_table.columns)[0]].tolist():
            x_labels.append(str(val))

        if len(prob_table.columns) != 2:
            raise ProbTableError(table=prob_table)
        fig, ax = plt.subplots()
        fig.set_size_inches(size_inches, size_inches)
        fig.set_dpi(dpi)
        ax.set(ylim=[0, 1.], aspect=self._aspect)
        plt.subplots_adjust(bottom=self._bottom)

        plt.bar(x=x_labels, 
                height=prob_table[list(prob_table.columns)[1]],
                width=0.96,
                color=color,
                )
        plt.xticks(rotation=90)
        plt.xlabel(list(prob_table.columns)[0], fontweight='bold')
        plt.ylabel(list(prob_table.columns)[1], fontweight='bold')
        #plt.show()

        fn: str = list(prob_table.columns)[1]
        fn = fn.replace('/', '@')
        filename = fn.replace('|', 'given')
        plt.savefig(savefig_loc_folder+f'/{filename}.png')

        return

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
        
