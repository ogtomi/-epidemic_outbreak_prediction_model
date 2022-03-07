import pycountry
import matplotlib.pyplot as plt
from datetime import date, timedelta

from api_request import GoogleRequests
from filter_data import correlation_filter
from process_data import get_mean_from_csv

plt.style.use('ggplot')

def get_anchortime():
    #"2021-01-01 2022-01-01"
    today_date = date.today()
    past_date = today_date - timedelta(days=365)
    anchor_time = str(past_date) + " " + str(today_date)
    return anchor_time

COUNTRY = "united states"
KEYWORDS = ['stomach pain']
CAT = '0'
TIMEFRAMES = ['today 12-m', 'today 3-m', 'today 1-m']
GPROP = ''
ANCHOR_TIME = get_anchortime()
PATH_TO_CSV = 'covid_deaths_usafacts.csv'

google_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, COUNTRY, GPROP, ANCHOR_TIME)

#data = google_requests.request_window()
covid_data = get_mean_from_csv(PATH_TO_CSV)
#print(data)
#data = correlation_filter(data, KEYWORDS)
print(covid_data)
