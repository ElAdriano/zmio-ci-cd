network_configuration_3x3 = {
    'hidden_layer_sizes': (150000,),
    'activation': 'relu',
    'solver': 'adam',
    'alpha': 0.0001,
    'batch_size': 32,
    'learning_rate': 'adaptive',
    'learning_rate_init': 0.001,
    'shuffle': True,
    'momentum': 0.001,
    'verbose': True,
    'max_iter': 250,
}

network_configuration_4x4 = {
    'hidden_layer_sizes': (400, 250,),
    'activation': 'relu',
    'solver': 'adam',
    'alpha': 0.005,
    'batch_size': 32,
    'learning_rate': 'adaptive',
    'learning_rate_init': 0.01,
    'shuffle': True,
    'momentum': 0.001,
    'verbose': True,
    'max_iter': 50,
    'n_iter_no_change': 50
}

network_configuration_5x5 = {
    'hidden_layer_sizes': (700, 500,),
    'activation': 'relu',
    'solver': 'adam',
    'alpha': 0.0001,
    'batch_size': 32,
    'learning_rate': 'adaptive',
    'learning_rate_init': 0.007,
    'shuffle': True,
    'momentum': 0.001,
    'verbose': True,
    'max_iter': 50,
    'n_iter_no_change': 50
}
