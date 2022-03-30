import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ORDER = 4

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
    exp_lambda = 0.25
    Y_array = []

    for i in range(ORDER, t + ORDER):
        w = pow(exp_lambda, i)
        R += w * arx(t - i, data, word_count) @ arx(t - i, data, word_count).T
        p += w * y_data[t - i] * arx(t - i, data, word_count)

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

column = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

# column1 = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
# column2 = [[10], [11], [12], [13], [14], [15], [16], [17], [18], [19]]

# np_array = np.array(column)

# df = pd.DataFrame(column1)
# df2 = pd.DataFrame(column2)

# df[1] = df2
# vector = make_vector(df)
# y_predict = ewls(np_array, len(np_array))
# print(y_predict)
# t = len(y_predict)

# plt.figure()
# plt.plot(y_predict)
# plt.plot(np_array)
# plt.show()

# form = []
# for i in range(4):
#     form.append([column[i]])

# print(form)

# form = [[column[-1]], [column[-2]], [column[-3]], [column[-4]]]

# print(form)