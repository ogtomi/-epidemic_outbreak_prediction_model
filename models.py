from math import nan
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 4
ORDER = 3
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
        p += w * y_data[j] * arx(y_data, i, data, word_count, j)

        if np.linalg.det(R) != 0:
            ewls_estimator = np.linalg.inv(R) @ p
            Y = arx(y_data, i, data, word_count, j).T @ ewls_estimator
            Y_array.append(Y[0][0])
        else:
            Y_array.append(np.mean(Y_array))
        
        if j < len(y_data) - 1:
            j += 1

    Y_array = np.nan_to_num(Y_array, nan=0.0)
    return Y_array

def stationary_ls(data, t, word_count, y_data):
    j = 0
    Y = [[]]
    R = 0
    p = 0
    Y_array = []

    for i in range(ORDER - 1, t):
        R += arx(y_data, i, data, word_count, j) @ arx(y_data, i , data, word_count, j).T
        p += y_data[j] * arx(y_data, i, data, word_count, j)

        if np.linalg.det(R) != 0:
            ls_estimator = np.linalg.inv(R) @ p
            Y = arx(y_data, i, data, word_count, j).T @ ls_estimator
            Y_array.append(Y[0][0])
        else:
            Y_array.append(np.mean(Y_array))
        
        j += 1
    
    Y_array = np.nan_to_num(Y_array, nan=0.0)
    return Y_array

def progressive_arx(u, data, order):
    form = []
    for i in range(order):
        form.append([data[u - i]])
    
    print("NEW FORM")
    print(form)
    return np.array(form, dtype='float')

def stationary_ls1(data, t, word_count, y_data):
    j = 0
    i_time = ORDER - 1
    prog_order = 1
    Y = [[]]
    prog_arx = []
    Y_array = []
    
    for regressor in arx(y_data, i_time, data, word_count, j):
        epsilon = 0
        R = 0
        p = 0
        for i in range(ORDER - 1, t):
            R += progressive_arx(i, data, prog_order) @ progressive_arx(i, data, prog_order).T
            p += y_data[j - 1] * progressive_arx(i, data, prog_order)

            if np.linalg.det(R) != 0:
                ls_estimator = np.linalg.inv(R) @ p
                Y = progressive_arx(i, data, prog_order).T * ls_estimator
                Y_array.append(Y[0][0])
            else:
                Y_array.append(np.mean(Y_array))

            epsilon += (y_data[j - 1] - Y_array[j - 1]) ** 2

        prog_order += 1
        j += 1
        i_time += 1
    
    Y_array = np.nan_to_num(Y_array, nan=0.0)
    return Y_array

def akaike_fpe():
    pass
