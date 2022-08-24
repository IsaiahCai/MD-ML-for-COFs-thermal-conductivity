from sklearn.ensemble import RandomForestRegressor
from catboost import Pool, CatBoostRegressor
from sklearn import tree 
from sklearn.svm import SVR
import lightgbm as lgb
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

def mode_selection(mode):
    if mode == 'lgb':
        regr = lgb.LGBMRegressor()
        param_grid = {'boosting_type': ['gbdt','dart'],
                         'learning_rate': [0.1,0.001,0.0001,0.00001]}
        
    if mode == 'rf':
        regr =  RandomForestRegressor()
        param_grid = {'bootstrap': [True, False],
                         'max_features': ['auto','log2','sqrt'],
                         'min_samples_split': [2,3,4,5,6,7,8,9]}
    
    if mode == 'catboost':
        regr =  CatBoostRegressor()
        param_grid = {'iterations': [10,50,100],
                        'learning_rate': [0.1,0.001,0.0001,0.00001],
                        'depth' : [2,4,6,8],
                        'silent':[True],
                    }

    if mode == 'svr':
        regr =  SVR()
        param_grid = {'kernel': ['rbf', 'linear', 'poly', 'sigmoid'],
                      'gamma': ['scale', 'auto'],
                      'C': [0.001, 0.1, 1, 10, 50, 100]}        


    if mode == 'dt':
        regr =  tree.DecisionTreeRegressor()
        param_grid = {'criterion': ['mse', 'friedman_mse'],
                      'min_samples_split': [2,3,4,5,6,7,8,9]}
    
    if mode == 'xgb':
        regr = xgb.XGBRegressor()
        param_grid = {'n_estimators': [10,50,100,200],
                        'learning_rate': [0.1,0.001,0.0001,0.00001],
                    }

    regr_grid = GridSearchCV(regr, param_grid, scoring=None)

    return regr_grid

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
df = pd.read_excel(path)
# Generate a numpy array of the features for training
X =  df.iloc[:, 1:-1].values
# Generate a numpy array of values from the last column, which is target feature
Y = df.iloc[:, -1].values

# Obtain the train and test sets. The ratio of train/test set is 0.2
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

mode_list = ['lgb','rf','catboost','svr','dt','xgb']
for mode in mode_list:
    start = time.time()
    model = mode_selection(mode).fit(X_train, Y_train)
    # Use the API from sklearn. Record the best estimators
    best_estimator = model.best_estimator_
    print(mode, 'Best estimator: ', best_estimator)
    print('Time for optimization: %f seconds' %(time.time()-start), flush=True)
    print('---------------------------------')
