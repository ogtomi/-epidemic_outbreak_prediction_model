import numpy as np

ORDER = 1
AR_ORDER = 2

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
        print("LS EST", ls_estimator)

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
    print("Index", i_reg)
    print("FORM", form)
    print("PROG FORM", prog_form)
    
    return np.array(prog_form, dtype='float')

def ls_ad(u_df, t, y_data, ls_estimator):
    j = AR_ORDER
    i = ORDER
    y_index = 0
    max_order = AR_ORDER + len(u_df.columns) * ORDER
    indices_arr = list(range(max_order))
    Y_array = []
    i_reg_array = []
    ls_estimator_array = np.array([])
    err_arr = []
    err = 0
    Y_all = []

    for k in range(max_order):
        for i_reg in indices_arr:
            print("START INDICES", indices_arr)
            i_reg_array.append(i_reg)
            ls_estimator_array = np.append(ls_estimator_array, ls_estimator[i_reg])
            print("OG ESTIMATOR", ls_estimator)
            print("ESTIMATOR ARRAY", ls_estimator_array)
            for _ in range(t):
                Y = arx_ad(y_data, i, u_df, j, i_reg_array).T @ ls_estimator_array
                Y_array.append(Y[0])
                
                if j < len(y_data):
                    err += pow((y_data[j] - Y_array[y_index]), 2) 
                j += 1
                i += 1
                y_index += 1

            err_arr.append(err)
            i_reg_array.pop(-1)
            ls_estimator_array = np.delete(ls_estimator_array, -1)
            j = AR_ORDER
            i = ORDER
            y_index = 0
            err = 0
            if k != max_order - 1:
                Y_array.clear()

        print("ERR ARR", err_arr)
        min_val_index = err_arr.index(min(err_arr))
        print("MIN VAL INDEX", min_val_index)
        print("MIN INDEX", indices_arr[min_val_index])
        print("ESTIMATOR:", ls_estimator[indices_arr[min_val_index]])
        i_reg_array.append(indices_arr[min_val_index])
        # ls_estimator = np.delete(ls_estimator, min_val_index)
        ls_estimator_array = np.append(ls_estimator_array, ls_estimator[indices_arr[min_val_index]])
        err_arr.clear()
        if indices_arr[min_val_index] in indices_arr:
            indices_arr.remove(indices_arr[min_val_index])
    
    print("OG ESTIMATOR", ls_estimator)
    print("FINAL ESTIMATOR ARR", ls_estimator_array)
    return Y_array

def AIC():
    aic = N * np.ln