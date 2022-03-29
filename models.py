import numpy as np
import pandas as pd

def arx(U, data):
    form = [[data[U-1]], [data[U-2]], [data[U-3]], [data[U-4]]]
    return np.array(form, dtype='float')

def ewls(data):
    Y = 0
    R = 0
    p = 0
    exp_lambda = 0.25
    t = len(data)

    for i in range(4, t):
        w = pow(exp_lambda, i)

        R += w * arx(t - i, data) @ arx(t - i, data).T
        p += w * data[t - i] * arx(t - i, data)

        if np.linalg.det(R) != 0:
            ewls_estimator = np.linalg.inv(R) @ p
            Y = arx(i, data).T @ ewls_estimator
            #Y_array.append(Y)
            print(Y)
        else:
            print("R!=0")  

def make_vector(dataframe):
    numpy_array = dataframe.to_numpy()
    vector_data = []

    for i in range(len(dataframe.values)):
        for column in range(len(dataframe.columns)):
            print(numpy_array[i][column])
            vector_data.append(numpy_array[i][column])
    
    return np.array(vector_data, dtype='float')

column = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

column1 = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
column2 = [[10], [11], [12], [13], [14], [15], [16], [17], [18], [19]]

np_array = np.array(column)
df = pd.DataFrame(column1)
df2 = pd.DataFrame(column2)

df[1] = df2
make_vector(df)
# ewls(np_array)