import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

THRESHOLD = 0.4

def correlation_filter(data, keywords):
    corr = data.corr()
    
    plt.figure(figsize=(15,10))
    sns.heatmap(corr, annot=False)
    plt.show()

    for column in corr[keywords]:
        column_series = corr[column]
        for name, row_value in column_series.iteritems():
            if row_value < THRESHOLD:
                data.drop(name, axis='columns', inplace=True)
    
    corr = data.corr()
    
    plt.figure(figsize=(15,10))
    sns.heatmap(corr, annot=True)
    plt.show()

    return data
    
