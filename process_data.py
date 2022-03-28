from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def get_mean_from_csv(PATH_TO_FILE):
    data = pd.read_csv(PATH_TO_FILE)
    data = data.drop(columns=['countyFIPS', 'StateFIPS'])
    average_column = data.mean(axis=0).to_frame()
    average_column = average_column.diff()

    # plt.figure()
    # average_column.plot()
    # plt.show()
    return average_column

def convert_to_weekly(data):
    offset = pd.offsets.DateOffset(-1)

    data.set_axis(['covid_mean'], axis='columns', inplace=True)
    data_modified = data.reset_index()
    data_modified = data_modified.assign(date = data_modified['index'].drop(columns = 'index'))

    data_modified['date'] = data_modified['date'].astype('datetime64[ns]')

    data_weekly = data_modified.resample('W-mon', label='left', closed='left', on='date', loffset=offset).mean()
    data_weekly.drop(index=('2020-01-19'), inplace=True)

    return data_weekly

def preprocess_data(df, y_col):
    df = df.fillna(df.mean()) # fill na / nan values with mean value

    sc = StandardScaler()

    if y_col in df.columns:
        X = df.drop(y_col, axis=1) # splitting data into X and y
        X = sc.fit_transform(X) # scaling by removing the mean and dividing by standard deviation so that there's no feature bias
        y = df[y_col]

        return X, y
    
    return sc.fit_transform(df)

    #X = shuffle(X)

def plot_result(X, y, X_test, y_pred):
    plt.figure()
    plt.scatter(x=list(range(len(X))), y=y, color="blue")
    plt.scatter(x=list(range(len(X_test))), y=y_pred, color="red")
    plt.show()

get_mean_from_csv('covid_confirmed_usafacts.csv')