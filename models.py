import numpy as np

ORDER = 1
AR_ORDER = 5

def arx(y, u, data, word_count, y_index):
    form = []
    for j in range(AR_ORDER):
        form.append([y[y_index - j]])

    for i in range(ORDER * word_count):
        form.append([data[u - i]])
    
    return np.array(form, dtype='float')

def ls_est(data, t, word_count, y_data):
    j = AR_ORDER - 1
    i = (ORDER * word_count) - word_count
    R = 0
    p = 0

    for _ in range(t):
        R += arx(y_data, i, data, word_count, j) @ arx(y_data, i, data, word_count, j).T
        p += y_data[j] * arx(y_data, i, data, word_count, j)
        j += 1
        i += 1
    if np.linalg.det(R) != 0:
        ls_estimator = np.linalg.inv(R) @ p

    return ls_estimator

def ls(data, t, word_count, y_data, ls_estimator):
    j = AR_ORDER - 1
    i = (ORDER * word_count) - word_count
    Y_array = []

    for _ in range(t + 1):
        Y = arx(y_data, i, data, word_count, j).T @ ls_estimator
        Y_array.append(Y[0][0])
        j += 1
        i += 1
    
    return Y_array
        