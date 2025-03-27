from scipy.stats import randint, uniform


light_params = {
    'n_estimators': randint(50,500),
    'max_depth': randint(2,50),
    'learning_rate': uniform(0.01,0.2),
    'num_leaves': randint(2,100),
    'boosting_type': ['gbdt','dart','goss']
}


random_search_params = {
    'n_iter' : 20,
    'cv' : 5,
    'verbose': 2,
    'scoring': 'f1',
    'n_jobs': -1,
    'random_state': 42
}