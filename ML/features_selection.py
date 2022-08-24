import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
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
        
    return regr

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
df = pd.read_excel(path)
feature_df = df.iloc[:, 1:-1]

for i in range(200):
    # Generate a dataframe with randomly selected features 
    sampled_df = feature_df.sample(23,random_state=i,axis=1)
    X =  sampled_df.values
    Y = df.iloc[:, -1].values
    # Obtain the train and test sets. The ratio of train/test set is 0.2
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    mode_list = ['lgb']
    for mode in mode_list:
        model = mode_selection(mode).fit(X_train, Y_train)
        Y_Pred = model.predict(X_test)
        # Examine how models fit the test data
        print(mode,', MAE: ', mean_absolute_error(Y_test, Y_Pred))
        print(mode, ', R2: ', r2_score(Y_test, Y_Pred))
        print('---------------------------------')