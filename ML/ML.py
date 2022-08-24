from sklearn.ensemble import RandomForestRegressor
from catboost import Pool, CatBoostRegressor
from sklearn import tree 
from sklearn.svm import SVR
import lightgbm as lgb
import xgboost as xgb
from sklearn.linear_model import Lasso
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def mode_selection(mode):

    if mode == 'lgb':
        regr = make_pipeline(StandardScaler(),lgb.LGBMRegressor())
        
    if mode == 'rf':
        regr =  make_pipeline(StandardScaler(),RandomForestRegressor(n_estimators = 100, random_state=0))
    
    if mode == 'catboost':
        regr =  make_pipeline(StandardScaler(),CatBoostRegressor(iterations=100, 
                              depth=8, 
                              learning_rate=0.1, 
                              loss_function='RMSE',
                              silent=True))
    
    if mode == 'dt':
        regr =  make_pipeline(StandardScaler(),tree.DecisionTreeRegressor(random_state=42, splitter='best',max_depth=4, min_samples_leaf=2))
    
    if mode == 'xgb':
        regr = make_pipeline(StandardScaler(),xgb.XGBRegressor(base_score=0.5, booster='gbtree', callbacks=None,colsample_bylevel=1, colsample_bynode=1, colsample_bytree=1,
                early_stopping_rounds=None, enable_categorical=False,
                eval_metric=None, gamma=0, gpu_id=-1, grow_policy='depthwise',importance_type=None, 
                interaction_constraints='',learning_rate=0.1, max_bin=256, max_cat_to_onehot=4,
                max_delta_step=0, max_depth=6, max_leaves=0, min_child_weight=1,monotone_constraints='()', 
                n_estimators=200, n_jobs=0,num_parallel_tree=1, predictor='auto', random_state=0, reg_alpha=0,reg_lambda=1))
    
    return regr

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
df = pd.read_excel(path)
# Generate a numpy array of the features for training
X =  df.iloc[:, 0:-1].values
# Generate a numpy array of values from the last column, which is target feature
Y = df.iloc[:, -1].values

# Obtain the train and test sets. The ratio of train/test set is 0.2
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Training ML models on the train set and examining (R2, MAE) on the test set
mode_list = ['lgb','rf','catboost','svr','dt','xgb']
for mode in mode_list:
    model = mode_selection(mode).fit(X_train, Y_train)

    # Examine how models fit the training data
    train_score = mode_selection(mode).fit(X_train, Y_train).score(X_train,Y_train)
    Y_Pred = model.predict(X_test)
    print(mode, 'train error', train_score)

    # Examine how models fit the test data
    print(mode,' MAE: ', mean_absolute_error(Y_test, Y_Pred))
    print(mode,' R2: ', r2_score(Y_test, Y_Pred))
    print('---------------------------------')
