


class BNSettings():

    smoothCPT: bool = True #whether to smooth the cond prob tables of the bayes net.
    eq_sample_size: int = 10 # parameter for smoothing. The higher the value to more the smoothing.

    # Variables in the dataset to use for building the BN
    graph_nodes = [
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
    # Directed edges between variables. Not needed if the graph structure is learned form data.
    graph_edges = [
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

    # Variables in the dataset to be discretized
    continuous_vars = [
        {'name': 'Concr(kg/m2)', 
        'bins': 18
        },
        {'name': 'Masnry&Blwk(m2/m2)',
        'bins': 5
        },
        {'name': 'Reinf(kg/m2)',
        'bins': 7
        },
        {'name': 'Steel_Sec(kg/m2)', 
        'bins': 12
        },
        {'name': 'Timber_Prod(kg/m2)', 
        'bins': 4
        },
    ]

    material_vars = [
        'Concr(kg/m2)',
        'Masnry&Blwk(m2/m2)',
        'Reinf(kg/m2)',
        'Steel_Sec(kg/m2)',
        'Timber_Prod(kg/m2)'
    ]