import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 4
ORDER = 3
AR_ORDER = 4

def arx(y, u, data, word_count, y_index):
    form = []
    # form.append([y])
    for j in range(AR_ORDER):
        form.append([y[y_index - j]])

    for i in range(ORDER * word_count):
        form.append([data[u - i]])
    
    print(form)
    return np.array(form, dtype='float')

def ewls(data, t, word_count, y_data):
    j = 0
    Y = [[]]
    R = 0
    p = 0
    #t = int(len(data) / word_count)
    # 0.425
    exp_lambda = 0.01
    Y_array = []
    Y_array.append(1)

    for i in range(ORDER - 1, t - 1):
        w = pow(exp_lambda, i)
        R += w * arx(y_data, i, data, word_count, j) @ arx(y_data, i, data, word_count, j).T
        p += w * y_data[j] * arx(y_data, i, data, word_count, j)
        print("Y-data in j ", y_data[j])
        print("Y-data in j ", y_data[j-1])
        print("Y-data in j ", y_data[j-2])
        print("Y-data in j ", y_data[j-3])
        if np.linalg.det(R) != 0:
            ewls_estimator = np.linalg.inv(R) @ p
            Y = arx(y_data, i, data, word_count, j).T @ ewls_estimator
            Y_array.append(Y[0][0])
        else:
            Y_array.append(np.mean(Y_array))

        j += 1

    return Y_array

def make_vector(dataframe):
    numpy_array = dataframe.to_numpy()
    vector_data = []

    for i in range(len(dataframe.values)):
        for column in range(len(dataframe.columns)):
            print(numpy_array[i][column])
            vector_data.append(numpy_array[i][column])
    
    return np.array(vector_data, dtype='float')
