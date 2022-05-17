import numpy as np

ORDER = 1
AR_ORDER = 10

# STATIONARY BASIC MODEL
def arx(y, u, u_df, y_index):
    form = []
    # GET DATA FROM REAL CASES
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])   # y - j - 1 results in t - 1 probe

    # GET DATA FROM DATAFRAME
    for column in u_df.columns:
        for i in range(ORDER):                              # ORDER represents the amount of time probes
            form.append([u_df[column].values[u - i - 1]])   # appending ORDER time probes from each column in df
                                                            # u - i - 1 results in t - 1 probe
    return np.array(form, dtype='float')

# STATIONARY LS ESTIMATOR FUNCTION
def ls_est(u_df, t, y_data):
    j = AR_ORDER # AR_ORDER so that there are enough probes to satisfy initial conditions
    i = ORDER
    R = 0
    p = 0

    for _ in range(t - 1):
        R += arx(y_data, i, u_df, j) @ arx(y_data, i, u_df, j).T # regression matrix j
        p += y_data[j] * arx(y_data, i, u_df, j)                 # predicted value is in t + 1
        j += 1                                                   # so y_data in t is needed
        i += 1
    if np.linalg.det(R) != 0:
        ls_estimator = np.linalg.inv(R) @ p

    return ls_estimator

# FUNCTION COUNTING VALUES FROM STATIONARY LS_ESTIMATOR
def ls(u_df, t, y_data, ls_estimator):
    j = AR_ORDER
    i = ORDER
    Y_array = []
    y_index = 0
    err = 0

    for _ in range(t):
        Y = arx(y_data, i, u_df, j).T @ ls_estimator    # multiply regressors @ estimated in ls_est values
        Y_array.append(Y[0][0])
    
        i += 1

        if j < len(y_data):
            # PREDICTION ERROR IS COUNTED IN EACH STEP
            err += pow((y_data[j] - Y_array[y_index]), 2)

        j += 1
        y_index += 1

    print("ERR: ",  err)
    aic = AIC(t - 1, len(ls_estimator), err)
    print("AIC: ", aic)
    
    return Y_array

# FUNCTION COUNTING VALUES FROM DIFF LS_ESTIMATOR
def ls_diff(u_df, t, y_data, ls_estimator, y_real_cases):
    j = AR_ORDER
    i = ORDER
    Y_array = []
    y_index = 0
    err = 0

    for _ in range(t):
        Y = arx(y_data, i, u_df, j).T @ ls_estimator    # multiply regressors @ estimated in ls_est values
        Y_array.append(Y[0][0] + y_real_cases[j - 1])
        i += 1

        if j < len(y_data):
            # PREDICTION ERROR IS COUNTED IN EACH STEP
            err += pow((y_real_cases[j] - Y_array[y_index]), 2)

        j += 1
        y_index += 1

    print("ERR DIFF: ",  err)
    aic = AIC(t - 1, len(ls_estimator), err)
    print("AIC DIFF: ", aic)
    
    return Y_array

# ADAPTIVE MODEL FORM
def arx_ad(y, u, u_df, y_index, i_reg_array):
    form = []
    prog_form = []
    # THE SAME FORM AS IN ARX
    for j in range(AR_ORDER):
        form.append([y[y_index - j - 1]])

    for column in u_df.columns:
        for i in range(ORDER):
            form.append([u_df[column].values[u - i - 1]])
    
    # ADAPTIVE FORM IS BASED ON I_REG_ARRAY VALUE FROM LS_AD
    for i_reg in i_reg_array:
        prog_form.append(form[i_reg])
    
    return np.array(prog_form, dtype='float')

# ADAPTIVE PARAMETER ESTIMATION
# takes i_reg_array as argument --> estimation of parameters takes place every time new reggressor appears
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

def ls_ad(u_df, t, y_data, diff_bool, y_real_cases):
    j = AR_ORDER
    i = ORDER
    y_index = 0
    max_order = AR_ORDER + len(u_df.columns) * ORDER
    indices_arr = list(range(max_order)) # start with array representing regressors position
    Y_array = []
    i_reg_array = []
    err_arr = []
    err = 0
    temp_aic = 1000

    # limits max order
    for k in range(max_order):
        # limits possible indices
        for i_reg in indices_arr:                                                   # 1. take one regressor
            i_reg_array.append(i_reg)
            ls_estimator_ad = ls_est_ad(u_df, t, y_data, i_reg_array)               # 2. estimate parameters

            # estimation of values
            for _ in range(t):                                                      # 3. Predict signal
                Y = arx_ad(y_data, i, u_df, j, i_reg_array).T @ ls_estimator_ad
                
                if diff_bool == False:
                    Y_array.append(Y[0])
                else:
                    Y_array.append(Y[0] + y_real_cases[j - 1])

                i += 1

                if j < len(y_data):
                    err += pow((y_real_cases[j] - Y_array[y_index]), 2)                   # 4. Count estimation error
                
                j += 1
                y_index += 1

            err_arr.append(err)                                                     # 5. For all cases in specific order append the sum of errors to array
            i_reg_array.pop(-1) # pop last element so that loop iterates over 
            j = AR_ORDER        # every possible case
            i = ORDER
            y_index = 0
            err = 0
            Y_array.clear()     # clear signal array so that they don't overlap

        min_val_index = err_arr.index(min(err_arr))                                 # 6. Choose the best regressor (for specific order) based on min. sum of err value
        aic = AIC(t - 1, len(ls_estimator_ad), err_arr[min_val_index])              # 7. Count AIC for the best option

        if aic > temp_aic:                                                          # 8. Check when AIC reaches minimum
            print("FINAL REG ARRAY", i_reg_array)
            print("ORDER OF MODEL", len(i_reg_array))
            print("FINAL EST ARR", ls_estimator_prev)
            print("AIC", aic)
            return i_reg_array, ls_estimator_prev                                   # 9. If it is reached return parameters and regressors' indices

        ls_estimator_prev = ls_estimator_ad
        i_reg_array.append(indices_arr[min_val_index])                              # 10. Append best regressor's index to indices array
        temp_aic = aic                                                              # 11. Save last AIC value to temp so it can be compared in the next step
        err_arr.clear() 

        if indices_arr[min_val_index] in indices_arr:                               # 12. Remove best index from indices so it does not repeat in further steps
            indices_arr.remove(indices_arr[min_val_index])

    print("REG INDEX", i_reg_array)
    return i_reg_array, ls_estimator_ad

# ADAPTIVE MODEL
def ls_val(u_df, t, y_data, ls_estimator_ad, reg_array, diff_bool, y_real_cases):
    j = AR_ORDER
    i = ORDER
    Y_array = []
    y_index = 0
    err = 0

    for _ in range(t):
        Y = arx_ad(y_data, i, u_df, j, reg_array).T @ ls_estimator_ad # take values from time probes defined in reg_array
        if diff_bool == False:
            Y_array.append(Y[0])
        else:
            Y_array.append(Y[0] + y_real_cases[j - 1])                                     # obtained in ls_ad
        
        i += 1

        if j < len(y_data):
            err += pow((y_real_cases[j] - Y_array[y_index]), 2)  # prediction error
        
        j += 1
        y_index += 1

    print("AD ERR", err)
    return Y_array

def AIC(N, K, err):
    # N = number of observations
    # K = number of parameters
    # err = sum of square errors
    return N * np.log(err / N) + 2 * (K + 1)