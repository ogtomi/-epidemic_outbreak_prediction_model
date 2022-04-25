import numpy as np

ORDER = 1
AR_ORDER = 3

def arx(y, u, u_df, y_index):
    form = []
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for column in u_df.columns:
        for i in range(ORDER):
            form.append([u_df[column].values[u - i - 1]])

    return np.array(form, dtype='float')

def ls_est(u_df, t, y_data):
    j = AR_ORDER
    i = ORDER
    R = 0
    p = 0

    for _ in range(t - 1):
        R += arx(y_data, i, u_df, j) @ arx(y_data, i, u_df, j).T
        p += y_data[j] * arx(y_data, i, u_df, j)
        j += 1
        i += 1
    if np.linalg.det(R) != 0:
        ls_estimator = np.linalg.inv(R) @ p

    return ls_estimator

def ls(u_df, t, y_data, ls_estimator):
    j = AR_ORDER
    i = ORDER
    Y_array = []

    for _ in range(t):
        Y = arx(y_data, i, u_df, j).T @ ls_estimator
        Y_array.append(Y[0][0])
        j += 1
        i += 1
    
    return Y_array

def arx_ad(y, u, u_df, y_index, i_reg_array):
    form = []
    prog_form = []

    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for column in u_df.columns:
        for i in range(ORDER):
            form.append([u_df[column].values[u - i - 1]])
    
    for i_reg in i_reg_array:
        prog_form.append(form[i_reg])
    
    return np.array(prog_form, dtype='float')

def ls_est_ad(u_df, t, y_data, i_reg_array):
    j = AR_ORDER
    i = ORDER
    R = 0
    p = 0

    for _ in range(t - 1):
        R += arx_ad(y_data, i, u_df, j, i_reg_array) @ arx_ad(y_data, i, u_df, j, i_reg_array).T
        p += y_data[j] * arx_ad(y_data, i, u_df, j, i_reg_array)
        j += 1
        i += 1
    if np.linalg.det(R) != 0:
        ls_estimator = np.linalg.inv(R) @ p

    return ls_estimator

def ls_ad(u_df, t, y_data):
    j = AR_ORDER
    i = ORDER
    y_index = 0
    max_order = AR_ORDER + len(u_df.columns) * ORDER
    indices_arr = list(range(max_order))
    Y_array = []
    i_reg_array = []
    final_reg_array = []
    err_arr = []
    err = 0
    temp_aic = 1000

    for k in range(max_order):
        for i_reg in indices_arr:
            i_reg_array.append(i_reg)
            ls_estimator_ad = ls_est_ad(u_df, t, y_data, i_reg_array)
            print("AD ESTIMATOR", ls_estimator_ad)
            print("FORM", arx(y_data, i, u_df, j))
            print("PROG FORM", arx_ad(y_data, i, u_df, j, i_reg_array))
            for _ in range(t):
                Y = arx_ad(y_data, i, u_df, j, i_reg_array).T @ ls_estimator_ad
                Y_array.append(Y[0])
                
                if j < len(y_data):
                    err += pow((y_data[j] - Y_array[y_index]), 2) 
                j += 1
                i += 1
                y_index += 1
            # zmienić dane na te do uczenia
            err_arr.append(err)
            i_reg_array.pop(-1)
            j = AR_ORDER
            i = ORDER
            y_index = 0
            err = 0
            Y_array.clear()

        min_val_index = err_arr.index(min(err_arr))
        i_reg_array.append(indices_arr[min_val_index])
        aic = AIC(t, len(ls_estimator_ad), err_arr[min_val_index])
        if aic > temp_aic:
            print("FINAL REG ARRAY", i_reg_array)
            print("FINAL EST ARR", ls_estimator_ad)
            return i_reg_array, ls_estimator_ad
        temp_aic = aic
        err_arr.clear()
        if indices_arr[min_val_index] in indices_arr:
            indices_arr.remove(indices_arr[min_val_index])

    return i_reg_array, ls_estimator_ad

def AIC(N, K, err):
    return N * np.log(err / N) + 2 * (K + 1)
    # N = number of observations
    # K = number of parameters
    # err = sum of square errors