import os
import graphviz 

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

u = graphviz.Digraph('G', 
                     engine= 'dot',#'dot', #fdp
                     filename='DAG.gv',
                     graph_attr={'splines': 'false',
                                 'pack': 'true'

                                 }
                     )


#----------------------------------------------------------------------------------------
u.attr('node', fontname='Sans',fontsize='9',shape='box',penwidth='1',fillcolor='azure2', style='filled',rank='sink') 
u.node('Cladding \ntype')
u.node('Superstructure \ntype')
u.node('GIFA')
u.node('No. \nstoreys')
u.node('Basement')
u.node('Foundations \ntype')
u.attr('node', fontname='Sans',fontsize='9',shape='oval',penwidth='1',fillcolor='azure2', style='filled',rank='sink') 
u.node('Timber \n(products) qty.')
u.node('Steel \n(sections) qty.')
u.node('Masonry & \nblockworks qty.') 
u.node('Reinforcement \nqty.')
u.node('Concrete \nqty.')
u.attr('node', fontname='Sans',fontsize='9',shape='octagon',penwidth='1',fillcolor='azure2', style='filled',rank='sink')
u.node('Concrete \nelements')
u.node('Superstructure \nunit-weight')

u.attr('edge',arrowsize='0.7',arrowhead='normal',color="gray30",penwidth='1.2',)
u.edge('Foundations \ntype', 'Reinforcement \nqty.')
u.edge('GIFA', 'Timber \n(products) qty.')
u.edge('GIFA', 'Steel \n(sections) qty.')
u.edge('GIFA', 'Masonry & \nblockworks qty.')
u.edge('GIFA', 'Reinforcement \nqty.')
u.edge('GIFA', 'Concrete \nqty.')

u.edge('Superstructure \ntype', 'Timber \n(products) qty.')
u.edge('Superstructure \ntype', 'Steel \n(sections) qty.')
u.edge('Superstructure \ntype', 'Superstructure \nunit-weight')
u.edge('Superstructure \nunit-weight', 'Foundations \ntype')
u.edge('Concrete \nelements', 'Reinforcement \nqty.')
u.edge('Cladding \ntype', 'Masonry & \nblockworks qty.')
u.edge('No. \nstoreys', 'Foundations \ntype')
u.edge('Foundations \ntype', 'Concrete \nqty.')
u.edge('Basement', 'Concrete \nqty.')
u.edge('Concrete \nelements', 'Concrete \nqty.')
u.edge('Superstructure \ntype', 'Masonry & \nblockworks qty.')
u.edge('Superstructure \ntype', 'Concrete \nelements')




#------------------------------

c = u.unflatten(stagger=3) 
c.render(directory=str(os.getcwd())+"/DAG_Script").replace('\\', '/')
