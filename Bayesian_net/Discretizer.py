import pandas as pd 
from pandas import DataFrame


def discretizer(dataset: DataFrame, vars: list[str], bin_counts: list[int], mid_vals: bool = False) -> DataFrame:
    
    for i in range(0, len(vars)):
        col = dataset[vars[i]]
        new_col = pd.cut(x=col, bins=bin_counts[i])
        if mid_vals == True:
            bin_vals = []
            for cat in new_col.items():
                bin_vals.append(round(cat[1].mid, 3))
            dataset[vars[i]] = bin_vals
            dataset = dataset.rename(columns={vars[i]: vars[i]+f'[+/-{round(cat[1].mid - cat[1].left, 3)}]'})
        else:
            dataset[vars[i]] = new_col

    return dataset
        


dataset = pd.read_csv(filepath_or_buffer="Bayesian_net/tests/dummy_dataset_2.csv")
print(dataset)

cont_vars = ['Degrees', 'Wind_speed']
bin_counts = [2, 10]

discrete_dataset = discretizer(dataset=dataset, vars=cont_vars, bin_counts=bin_counts, mid_vals=True)
discrete_dataset.to_csv(path_or_buf="Bayesian_net/tests/dummy_dataset_3.csv")
print(discrete_dataset)