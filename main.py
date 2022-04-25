import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime

from api_request import GoogleRequests
from filter_data import correlation_filter
from models import ls_ad, ls_est, ls, ls_val
from process_data import convert_to_weekly, get_data_for_comparison, get_mean_from_csv, predict_dataframe, make_vector

plt.style.use('ggplot')

ORDER = 5
AR_ORDER = 3

def get_anchortime(get_time):
    if get_time == 0:
        return "2020-01-19 2022-02-27"

    if get_time == 1:
        last_date = datetime.strptime("2022-02-27" , "%Y-%m-%d").date()
        first_date = last_date - timedelta(days=365 + ORDER * 7)
        return str(first_date) + " " + str(last_date)
    
    if get_time == 2:
        today_date = date.today()
        past_date = today_date - timedelta(days=365)
        anchor_time = str(past_date) + " " + str(today_date)
        return anchor_time
    
    if get_time == 3:
        first_date = datetime.strptime("2020-01-26", "%Y-%m-%d").date()
        last_date = first_date + timedelta(days=365 + ORDER * 7)
        return str(first_date) + " " + str(last_date)

COUNTRY = "united states"
KEYWORDS = ['nausea', 'stomach pain']
CAT = '0'
TIMEFRAMES = ['today 12-m', 'today 3-m', 'today 1-m']
GPROP = ''
ANCHOR_TIME_MODEL = get_anchortime(3) 
ANCHOR_TIME_COMPARISON = get_anchortime(1)
ANCHOR_TIME_PREDICT = get_anchortime(2)
PATH_TO_CSV = 'covid_confirmed_usafacts.csv'
VALUE = 'covid_mean'

model_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME_MODEL)
compare_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME_COMPARISON)
# predict_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME_PREDICT)

# GETTING DATA FROM GOOGLE API AND PROCESSING IT
# model_data = model_requests.request_window()
# model_data = correlation_filter(model_data, KEYWORDS)

covid_data = get_mean_from_csv(PATH_TO_CSV)

weekly_covid_data = convert_to_weekly(covid_data)
weekly_covid_array = weekly_covid_data.to_numpy()

# GET DATA FROM THE FIRST YEAR OF THE PANDEMIC
first_year_weekly_covid_data = get_data_for_comparison(weekly_covid_data, 0, AR_ORDER)
first_year_weekly_covid_data_array = make_vector(first_year_weekly_covid_data)
print("FIRST YEAR WEEKLY COVID DATA ARRAY")
print(first_year_weekly_covid_data_array)

# print("First year covid data array len", len(first_year_weekly_covid_data_array))
# print("FIRST YEAR DATA")
# print(first_year_weekly_covid_data)

# GET DATA FROM THE LAST YEAR OF THE PANDEMIC
last_year_weekly_covid_data = get_data_for_comparison(weekly_covid_data, 1, AR_ORDER)
last_year_weekly_covid_data_array = make_vector(last_year_weekly_covid_data)

# print("LAST YEAR WEEKLY COVID DATA ARRAY")
# print(last_year_weekly_covid_data_array)

# frames = [model_data, weekly_covid_data]
# result_array = pd.concat(frames, axis=1)
# result_array = correlation_filter(result_array, [VALUE])

#FINAL WORD BANK
# word_bank = result_array.drop(VALUE, axis=1)
# word_bank_rows = len(word_bank.index)
# word_bank = word_bank.columns.values.tolist()

# BUILDING THE MODEL 
X_model = model_requests.arrange_data(KEYWORDS)
X_predict = compare_requests.arrange_data(KEYWORDS)

vector_data_compare = make_vector(X_predict)
vector_data_model = make_vector(X_model)
print("X_model")
print(X_model)
print("X_PREDICT")
print(X_predict)
# GET THE ESTIMATED PARAMETERS
ls_estimator = ls_est(X_model, len(first_year_weekly_covid_data_array) - AR_ORDER + 1, first_year_weekly_covid_data_array)

Y_model = ls(X_model, len(first_year_weekly_covid_data_array) - AR_ORDER + 1, first_year_weekly_covid_data_array, ls_estimator)
Y_model_dataframe = predict_dataframe(Y_model, 2, AR_ORDER)
print("_______")
# PREDICTION
Y_predict = ls(X_predict, len(last_year_weekly_covid_data_array) - AR_ORDER + 1, last_year_weekly_covid_data_array, ls_estimator)
Y_predict_dataframe = predict_dataframe(Y_predict, 1, AR_ORDER)
print("_________")

# GET ESTIMATED COEFF & MODEL ORDER
reg_array, ls_estimator_ad = ls_ad(X_model, len(first_year_weekly_covid_data_array) - AR_ORDER + 1, first_year_weekly_covid_data_array)

Y_val_ad = ls_val(X_predict, len(last_year_weekly_covid_data_array) - AR_ORDER + 1, last_year_weekly_covid_data_array, ls_estimator_ad, reg_array)
Y_val_ad_predict_dataframe = predict_dataframe(Y_val_ad, 1, AR_ORDER)

# print("LEN DATA COVID")
# print(len(last_year_weekly_covid_data_array) - AR_ORDER)
# print("LEN PREDICTED DATA")
# print(len(Y_predict))
# print(len(X_predict.index))

plt.figure()
plt.plot(weekly_covid_data, 'r',label="Rzeczywiste zachorowania")
#plt.plot(Y_model_dataframe, label="LS model")
plt.plot(Y_predict_dataframe, 'b',label="Model o pełnym rzędzie")
plt.plot(Y_val_ad_predict_dataframe, 'y',label="Model adaptacyjny")
plt.ylim([-50, 350])
plt.legend()
plt.show()