import os
import pandas as pd
from dython.nominal import associations
from dython.nominal import identify_nominal_columns

df= pd.read_csv(str(os.getcwd())+"/Data/training_dataset.csv")


df.drop(columns=['Project Ref',
                 'Calculation Design Stage',
                 'GIFA (m2)',
                 'Concrete Carbon (A1-A5) (kgCO2e/m2)',
                 'Masonry & Blockwork Carbon (A1-A5) (kgCO2e/m2)',
                 'Reinforcement  Carbon (A1-A5) (kgCO2e/m2)',
                 'Steel (Sections) Carbon (A1-A5) (kgCO2e/m2)',
                 'Timber (Products) Carbon (A1-A5) (kg/m2)',
                 'Total Carbon (A1-A5) (kgCO2e/m2)'
                 ],
        inplace=True)

#categorical_features = identify_nominal_columns(df)
'''
Documentation for associations method: http://shakedzy.xyz/dython/modules/nominal/#associations

'''
complete_correlation = associations(dataset=df, 
                                    filename=str(os.getcwd())+"/Correlation_Script/CorrelationMatrix.png", 
                                    figsize=(15,15),
                                    num_num_assoc='pearson', #continuous-continuous 
                                    nom_num_assoc='correlation_ratio', #categorical-continuous 
                                    nom_nom_assoc='cramer', #categorical-categorical
                                    cramers_v_bias_correction=True #Bergsma and Wicher, Journal of the Korean Statistical Society 42 (2013): 323-328.
                                    )


