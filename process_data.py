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
    offset = pd.offsets.DateOffset(-1)

    data.set_axis(['covid_mean'], axis='columns', inplace=True)
    data_modified = data.reset_index()
    data_modified = data_modified.assign(date = data_modified['index'].drop(columns = 'index'))

    data_modified['date'] = data_modified['date'].astype('datetime64[ns]')

    data_weekly = data_modified.resample('W-mon', label='left', closed='left', on='date', loffset=offset).mean()
    data_weekly.drop(index=('2020-01-19'), inplace=True)

    return data_weekly
