from datetime import timedelta
from optparse import Values
from re import I
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from datetime import date, timedelta, datetime

def get_mean_from_csv(PATH_TO_FILE):
    data = pd.read_csv(PATH_TO_FILE)
    data = data.drop(columns=['countyFIPS', 'StateFIPS'])
    average_column = data.mean(axis=0).to_frame()
    average_column = average_column.diff()
    
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

    if y_col in df.columns:
        X = df.drop(y_col, axis=1) # splitting data into X and y
        y = df[y_col]

        return X, y
    
    return df 

# APPEND DATA FROM VALUES INTO DATAFRAME
def predict_dataframe(values, mode, ar_order):
    if mode == 0:
        next_date = date.today() + timedelta(days= 7)
        past_date = next_date - timedelta(days=365)
    
    if mode == 1:
        next_date = datetime.strptime("2022-02-27", "%Y-%m-%d").date()
        past_date = next_date - timedelta(days=365)
    
    if mode == 2:
        past_date = datetime.strptime("2020-01-26", "%Y-%m-%d").date()
        past_date = past_date + timedelta(days=7 * ar_order)

    idx = pd.date_range(past_date, periods=len(values), freq="W")
    datetime_series = pd.Series(range(len(idx)), index=idx)

    df = pd.DataFrame(values)
    df['date'] = datetime_series.index
    
    df.reset_index()
    df.set_index(['date'], inplace=True)

    return df

# GET CERTAIN DATA FROM DATAFRAME
def get_data_for_comparison(df, mode, ar_order):
    if mode == 1:
        next_date = datetime.strptime("2022-02-27", "%Y-%m-%d").date()
        past_date = next_date - timedelta(days=365 + 7 * ar_order)
    
    if mode == 0:
        past_date = datetime.strptime("2020-01-26", "%Y-%m-%d").date()
        next_date = past_date + timedelta(days=365 + 7 * ar_order)

    comparable_df = df.loc[str(past_date):str(next_date)]
    
    return comparable_df

# MAKE VECTOR OUT OF DATAFRAME DATA
def make_vector(dataframe):
    vector_arr = []
    for column in dataframe.columns:
        for i in range(len(dataframe[column].values)):
            vector_arr.append(dataframe[column].values[i])
    
    return vector_arr