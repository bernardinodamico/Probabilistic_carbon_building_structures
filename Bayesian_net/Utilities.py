import pandas as pd 
from pandas import DataFrame


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
        

'''
dataset = pd.read_csv(filepath_or_buffer="Bayesian_net/tests/dummy_dataset_2.csv")
print(len(dataset.columns))

cont_vars = ['Degrees', 'Wind_speed']
bin_counts = [2, 10]

discrete_dataset = discretizer(dataset=dataset, vars=cont_vars, bin_counts=bin_counts, mid_vals=False)
discrete_dataset.to_csv(path_or_buf="Bayesian_net/tests/dummy_dataset_3.csv", index=False)
print(len(discrete_dataset.columns))
'''