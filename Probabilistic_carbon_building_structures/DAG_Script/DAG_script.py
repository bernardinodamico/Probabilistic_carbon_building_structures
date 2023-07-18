import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'


u = graphviz.Digraph('G', 
                     engine= 'dot',#'dot', #fdp
                     filename='DAG.gv',
                     graph_attr={'splines': 'true',
                                 'dim':'2',
                                 'K': '100.6',
                                 'sep': '5.2',
                                 }
                     )  


u.attr('edge',
        arrowsize='0.7',
        arrowhead='normal',
        color="gray30",
        penwidth='1.2',
        #weight='0.9'
        )
 
u.attr('node', 
        fontname='Sans',
        fontsize='9',
        shape='oval', #'cicrle'
        penwidth='1.',
        #fillcolor='cornflowerblue', 
        style='filled',
        concentrate='true'
        ) 
#u.node('Evidence')

u.node('No. \nstoreys')#, pos='4.5,0!')
u.node('Cladding \ntype')#, pos='0,0!')
u.node('Superstructure \ntype')#, pos='1.5,0!')
u.node('Superstructure \nunit-weight')#, pos='1.5,0!')
u.node('Concrete \nelements')#, pos='1.5,0!')

u.node('Basement')#, pos='7.5,0!')
u.node('Foundations \ntype')#, pos='7.5,1.25!')

u.attr('node', 
        #fontname='Sans',
        shape='oval',
        penwidth='1',
        #fillcolor='coral', 
        style='filled',
        ) 
#u.node('Query')

u.node('Reinforcement \nqty.')#, pos='5.75,3!')
u.node('Masonry & \nblockworks qty.')#, pos='0.75,-2.5!')
u.node('Concrete \nqty.')#, pos='5.25,2.5!')
u.node('Timber \n(products) qty.')#, pos='2.25,2.5!')
u.node('Steel \n(sections) qty.')#, pos='3.75,2.5!')

u.attr('node', 
        #fontname='Sans',
        shape='oval',
        penwidth='1',
        fillcolor='gray66', 
        style='filled',
        ) 

#u.node('Embodied \n carbon') Superstruct. weight


u.edge('Cladding \ntype', 'Masonry & \nblockworks qty.')


u.edge('No. \nstoreys', 'Foundations \ntype')


u.edge('Foundations \ntype', 'Concrete \nqty.')
u.edge('Foundations \ntype', 'Reinforcement \nqty.')

u.edge('Basement', 'Concrete \nqty.')

u.edge('Superstructure \ntype', 'Masonry & \nblockworks qty.')
u.edge('Superstructure \ntype', 'Concrete \nelements')
u.edge('Concrete \nelements', 'Concrete \nqty.')
u.edge('Superstructure \ntype', 'Timber \n(products) qty.')
u.edge('Superstructure \ntype', 'Steel \n(sections) qty.')
u.edge('Superstructure \ntype', 'Superstructure \nunit-weight')
u.edge('Superstructure \nunit-weight', 'Foundations \ntype')
u.edge('Concrete \nelements', 'Reinforcement \nqty.')

#------------------------------
'''
u.edge('Masonry & \nblockworks', 'Embodied \n carbon')
u.edge('Timber \n(plain)', 'Embodied \n carbon')
u.edge('Steel \n(other)', 'Embodied \n carbon')
u.edge('Reinforcement', 'Embodied \n carbon')
u.edge('Concrete', 'Embodied \n carbon')
u.edge('Timber \n(products)', 'Embodied \n carbon')
u.edge('Steel \n(sections)', 'Embodied \n carbon')
'''

c = u.unflatten(stagger=3) 

c.view()

