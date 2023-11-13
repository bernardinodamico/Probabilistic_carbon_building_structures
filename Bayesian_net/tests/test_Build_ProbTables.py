from Bayesian_net.Build_ProbTables import *

probTables = Build_ProbTables()
probTables.load_dataset(path="Bayesian_net/tests/dummy_dataset.csv")

mpt = probTables.pr_table(vars=['Temp'])
print(mpt)
#mpt2 = probTables.pr_table(vars=['Weather'])
#print(mpt2)
#jpt = probTables.pr_table(vars=['Temp', 'Weather'])
#print(jpt)

#cpt = probTables.cond_pr_table(var='Weather', given_vars=['Temp'])

#print(cpt)