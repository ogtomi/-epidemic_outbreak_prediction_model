from math import nan
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ORDER = 1
AR_ORDER = 5

def make_vector(dataframe):
    numpy_array = dataframe.to_numpy()
    vector_data = []

    for i in range(len(dataframe.values)):
        for column in range(len(dataframe.columns)):
            vector_data.append(numpy_array[i][column])
    
    return np.array(vector_data, dtype='float')

def arx(y, u, data, word_count, y_index):
    form = []
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for i in range(ORDER * word_count):
        form.append([data[u - i - word_count]])
    
    return np.array(form, dtype='float')

def ls_est(data, t, word_count, y_data):
    j = 0
    R = 0
    p = 0

    for i in range(ORDER - 1, t):
        R += arx(y_data, i, data, word_count, j) @ arx(y_data, i, data, word_count, j).T
        p += y_data[j] * arx(y_data, i, data, word_count, j)
        j += 1
    if np.linalg.det(R) != 0:
        ls_estimator = np.linalg.inv(R) @ p

    return ls_estimator

def ls(data, t, word_count, y_data, ls_estimator):
    j = 0
    Y_array = []

    for i in range(ORDER - 1, t):
        Y = arx(y_data, i, data, word_count, j).T @ ls_estimator
        Y_array.append(Y[0][0])
        j += 1
    
    return Y_array
        