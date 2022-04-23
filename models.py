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

def arx_ad(y, u, u_df, y_index, i_reg):
    form = []
    prog_form = []

    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for column in u_df.columns:
        for i in range(ORDER):
            form.append([u_df[column].values[u - i - 1]])
    
    prog_form.append(form[i_reg])
    print("Index", i_reg)
    print("FORM", form)
    print("PROG FORM", prog_form)
    
    return np.array(prog_form, dtype='float')

def ls_ad(u_df, t, y_data, ls_estimator):
    j = AR_ORDER
    i = ORDER
    max_order = AR_ORDER + len(u_df.columns) * ORDER
    Y_array = []

    for i_reg in range(max_order):
        for _ in range(t):
            Y = arx_ad(y_data, i, u_df, j, i_reg).T @ ls_estimator[i_reg]
            Y_array.append(Y[0][0])
            j += 1
            i += 1
        
        j = AR_ORDER
        i = ORDER
    
    return Y_array
    # coeff_array = np.array([])

    # for index, coeff in enumerate(ls_estimator):
    #     coeff_array = np.append(coeff_array, coeff)
    #     for _ in range(t):
    #         Y = arx_ad(y_data, i, data, word_count, j, index).T @ coeff_array
    #         #print("Regressors array", regressors_array)
    #         Y_array.append(Y)
    #         j += 1
    #         i += 1
    #         err += (y_data[j - 1] - Y) ** 2
        
    #     coeff_array = np.delete(coeff_array, -1)
    #     j = AR_ORDER - 1
    #     i = (ORDER * word_count) - word_count
    #     err = 0
    #     #Y_array.clear()

    return Y_array
        