import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import pandas as pd

def mode_selection(mode):

    if mode == 'lgb':
        regr = make_pipeline(StandardScaler(),lgb.LGBMRegressor())
    return regr

# Import your dataset
path= 'The path to your dataset (whose format is excel spreadsheet in this case)'
df = pd.read_excel(path)

for i in range(200):
    X =  df.iloc[:, 1:-1].values
    Y = df.iloc[:, -1].values
    # Randomly split the train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=i)
    mode_list = ['lgb']
    for mode in mode_list:
        model = mode_selection(mode).fit(X_train, Y_train)
        Y_Pred = model.predict(X_test)
        # Examine how models fit the test data
        print(i,mode,', MAE: ', mean_absolute_error(Y_test, Y_Pred))
        print(i,mode, ', R2: ', r2_score(Y_test, Y_Pred))
        print('---------------------------------')