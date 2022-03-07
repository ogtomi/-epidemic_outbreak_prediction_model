from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_mean_from_csv(PATH_TO_FILE):
    data = pd.read_csv(PATH_TO_FILE)
    data = data.drop(columns=['countyFIPS', 'StateFIPS'])
    average_column = data.mean(axis=0).to_frame()
    #plt.figure()
    #average_column.plot()
    #plt.show()

    return average_column

def convert_to_weekly(data):
    # data.set_axis(['covid_mean'], axis='columns', inplace=True)
    # data.index.name = 'Date'
    # data.reset_index(inplace=True)
    
    # data.set_index('Date', inplace=True)
    
    # data_resampled = data.resample('W', label='left')
    data_modified = data.reset_index()
    data_modified = data_modified.assign(Weeks = data_modified['index'].drop(columns = 'index'))

    data_modified['Weeks'] = data_modified['Weeks'].astype('datetime64[ns]')

    data_weekly = data_modified.resample('W-mon', label='left', closed='left', on='Weeks').mean()

    return data_weekly
