import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 4
ORDER = 5

def arx(u, data, word_count):
    form = []
    for i in range(ORDER * word_count):
        form.append([data[u-i]])
    return np.array(form, dtype='float')

def ewls(data, t, word_count, y_data):
    Y = [[]]
    R = 0
    p = 0
    #t = int(len(data) / word_count)
    # 0.425
    exp_lambda = 0.425
    Y_array = []

    for i in range(t):
        w = pow(exp_lambda, i)
        R += w * arx(t - i - 1, data, word_count) @ arx(t - i - 1, data, word_count).T
        p += w * y_data[t - i] * arx(t - i - 1, data, word_count)

        if np.linalg.det(R) != 0:
            ewls_estimator = np.linalg.inv(R) @ p
            Y = arx(i, data, word_count).T @ ewls_estimator
            Y_array.append(Y[0][0])

    return Y_array

def make_vector(dataframe):
    numpy_array = dataframe.to_numpy()
    vector_data = []

    for i in range(len(dataframe.values)):
        for column in range(len(dataframe.columns)):
            # print(numpy_array[i][column])
            vector_data.append(numpy_array[i][column])
    
    return np.array(vector_data, dtype='float')
