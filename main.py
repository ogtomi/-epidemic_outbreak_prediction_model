from re import search
from urllib import request
from django.http import QueryDict
import pycountry
from pytrends.request import TrendReq
import gtab
import matplotlib.pyplot as plt
import pandas as pd

from api_request import GoogleRequests

plt.style.use('ggplot')
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)

def country_to_code(country):
    return pycountry.countries.get(name=str(country)).alpha_2

country = "united states"
country_code = country_to_code(country)

t = gtab.GTAB()
df = pd.DataFrame()
t.set_options(pytrends_config={"geo": country_code, "timeframe": "2021-01-01 2022-01-01"})
#t.create_anchorbank(verbose=True)

KEYWORDS = ['stomach']
QUERY_ARR = []
SCALING_KW_LIST = ["chicago", "poland", "warsaw", "gdansk"]
CAT = '0'
TIMEFRAMES = ['today 12-m', 'today 3-m', 'today 1-m']
GPROP = ''
KW = []

def plot_data(data):
    plt.figure()
    df.plot()
    print("shit should be plotted")
    plt.show()

google_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, country_code, GPROP)
# google_requests.interest_over_time()
# google_requests.interest_per_region()
# google_requests.country_trends()
data = google_requests.request_window()
print(data)
