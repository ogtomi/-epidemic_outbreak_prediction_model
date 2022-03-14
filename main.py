import pycountry
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

from api_request import GoogleRequests
from filter_data import correlation_filter
from models import gradient_descent, predict
from process_data import convert_to_weekly, get_mean_from_csv, plot_result, preprocess_data

plt.style.use('ggplot')

def get_anchortime(model):
    #"2021-01-01 2022-01-01"
    today_date = date.today()
    past_date = today_date - timedelta(days=365)
    anchor_time = str(past_date) + " " + str(today_date)

    if model == True:
        return "2020-01-20 2022-02-28"
    return anchor_time

COUNTRY = "united states"
KEYWORDS = ['stomach pain']
CAT = '0'
TIMEFRAMES = ['today 12-m', 'today 3-m', 'today 1-m']
GPROP = ''
ANCHOR_TIME_MODEL = get_anchortime(1)
ANCHOR_TIME_PREDICT = get_anchortime(0)
PATH_TO_CSV = 'covid_confirmed_usafacts.csv'
VALUE = 'covid_mean'

google_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME_MODEL)
predict_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME_PREDICT)


# GETTING DATA FROM GOOGLE API AND PROCESSING IT
model_data = google_requests.request_window()
model_data = correlation_filter(model_data, KEYWORDS)

covid_data = get_mean_from_csv(PATH_TO_CSV)
weekly_covid_data = convert_to_weekly(covid_data)

frames = [model_data, weekly_covid_data]
result_array = pd.concat(frames, axis=1)
result_array = correlation_filter(result_array, [VALUE])


# FINAL WORD BANK
word_bank = result_array.drop(VALUE, axis=1)
word_bank = word_bank.columns.values.tolist()


# BUILDING THE MODEL 
X_model, y_model = preprocess_data(result_array, VALUE)
w, b, cost_list, epoch_list = gradient_descent(x=X_model, y=y_model, w=np.zeros(X_model.shape[1]), b=0, learning_rate=0.001, epochs=10000)
y_model_prediction = predict(X_model, w, b)

plot_result(X_model, y_model, X_model, y_model_prediction)

# DISEASE PREDICTION
X_predict = predict_requests.arrange_data(word_bank)
X_predict = preprocess_data(X_predict, VALUE)

y_predict = predict(X_predict, w, b)

plt.figure()
plt.scatter(x=list(range(len(X_model))), y=y_model_prediction, color="blue")
plt.show()

print(result_array)
print(w)
print(b)