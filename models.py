import numpy as np
from regex import P

ORDER = 1
AR_ORDER = 1

def arx(y, u, data, word_count, y_index):
    form = []
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])
        print("DATA", y_index - j - 1)
        print(([y[y_index - j - 1]]))

    # for num in range(word_count * ORDER):
    #     for i in range(ORDER):
    #         form.append([data[u - i + num * int(len(data) / word_count)]])

    print("FORM", np.array(form, dtype='float'))
    return np.array(form, dtype='float')

def ls_est(u_df, t, word_count, y_data):
    j = AR_ORDER
    i = (ORDER * word_count) - word_count
    R = 0
    p = 0

    for _ in range(t - 1):
        print("j", j)
        #print("i", i + 2)
        print("Y_data", y_data[j])
        R += arx(y_data, i, u_df, word_count, j) @ arx(y_data, i, u_df, word_count, j).T
        p += y_data[j] * arx(y_data, i, u_df, word_count, j)
        j += 1
        i += 1
    if np.linalg.det(R) != 0:
        print("R", R)
        print("p", p)
        ls_estimator = np.linalg.inv(R) @ p
    print(ls_estimator)

    return ls_estimator

def ls(u_df, t, word_count, y_data, ls_estimator):
    j = AR_ORDER
    i = (ORDER * word_count) - word_count
    Y_array = []

    for _ in range(t):
        print("TIME", j)
        Y = arx(y_data, i, u_df, word_count, j).T @ ls_estimator
        Y_array.append(Y[0][0])
        j += 1
        i += 1
    
    return Y_array

def arx_ad(y, u, u_df, word_count, y_index, index):
    form = []

    if index < AR_ORDER:
        form.append([y[y_index - index]])
    
    if index >= AR_ORDER:
        form.append([u_df[u - index + AR_ORDER]])
    
    #print("FORM", form)
    return np.array(form, dtype='float')

def ls_ad(data, t, word_count, y_data, ls_estimator):
    j = AR_ORDER - 1
    i = (ORDER * word_count) - word_count
    Y_array = []
    coeff_array = np.array([])
    arx_reg = arx(y_data, i, data, word_count, j)
    regressors_array = np.array([])
    err = 0
    temp_err = 1000

    for index, coeff in enumerate(ls_estimator):
        coeff_array = np.append(coeff_array, coeff)
        for _ in range(t):
            Y = arx_ad(y_data, i, data, word_count, j, index).T @ coeff_array
            #print("Regressors array", regressors_array)
            Y_array.append(Y)
            j += 1
            i += 1
            err += (y_data[j - 1] - Y) ** 2
        
        coeff_array = np.delete(coeff_array, -1)
        j = AR_ORDER - 1
        i = (ORDER * word_count) - word_count
        err = 0
        #Y_array.clear()

    return Y_array
        