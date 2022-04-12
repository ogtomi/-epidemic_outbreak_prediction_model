from math import nan
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 4
ORDER = 4
AR_ORDER = 2

def make_vector(dataframe):
    numpy_array = dataframe.to_numpy()
    vector_data = []

    for i in range(len(dataframe.values)):
        for column in range(len(dataframe.columns)):
            print(numpy_array[i][column])
            vector_data.append(numpy_array[i][column])
    
    return np.array(vector_data, dtype='float')

def arx(y, u, data, word_count, y_index):
    form = []
    # form.append([y])
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for i in range(ORDER * word_count):
        form.append([data[u - i - word_count]])
    
    return np.array(form, dtype='float')

def ewls(data, t, word_count, y_data):
    j = 0
    Y = [[]]
    R = 0
    p = 0
    exp_lambda = 0.9
    Y_array = []

    for i in range(ORDER - 1, t):
        w = pow(exp_lambda, i)
        R += w * arx(y_data, i, data, word_count, j) @ arx(y_data, i, data, word_count, j).T
        p += w * y_data[j - 1] * arx(y_data, i, data, word_count, j)

        if np.linalg.det(R) != 0:
            ewls_estimator = np.linalg.inv(R) @ p
            Y = arx(y_data, i, data, word_count, j).T @ ewls_estimator
            Y_array.append(Y[0][0])
        else:
            Y_array.append(np.mean(Y_array))
        
        j += 1

    Y_array = np.nan_to_num(Y_array, nan=0.0)
    return Y_array

def stationary_wls(data, t, word_count, y_data):
    j = 0 
    Y = [[]]
    R = 0
    p = 0
    Y_array = []

    for i in range(ORDER - 1, t):
        R += arx(y_data, i , data, word_count, j) @ arx(y_data, i, data, word_count, j).T
        p += y_data[j - 1] * arx(y_data, i, data, word_count, j)

        if np.linalg.det(R) != 0:
            wls_estimator = np.linalg.inv(R) @ p
            Y = arx(y_data, i, data, word_count, j).T @ wls_estimator
            Y_array.append(Y[0][0])
        else:
            Y_array.append(np.mean(Y_array))
        
        j += 1
    
    Y_array = np.nan_to_num(Y_array, nan=0.0)
    return Y_array

def akaike_fpe():
    pass
