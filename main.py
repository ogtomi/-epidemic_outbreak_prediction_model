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

def arrange_data(country_code, word_list):
    pytrends.build_payload(word_list, CAT, TIMEFRAMES[2], country_code, GPROP)
    #plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

    for kw in word_list:
        kw_query = t.new_query(kw)
        df[kw] = kw_query.max_ratio
        ax.plot(kw_query.max_ratio, label=kw)
        ax.legend()

    return df

def request_window(search_arr):
    request_arr = []
    plt.figure()

    for i in range(len(search_arr)):
        request_arr.append(search_arr[i])
        
        if i % 5 == 0:
            arrange_data(country_code, request_arr)
            request_arr = []

def plot_data(data):
    plt.figure()
    df.plot()
    plt.show()

# SEARCH_ARR = [*KEYWORDS, *QUERY_ARR]
# #plot_absolute_comparison(country_code, KEYWORDS)
# # get_absolute_data(country_code)
# request_window(SEARCH_ARR)
# plot_data(df)

google_requests = GoogleRequests(KEYWORDS, CAT, TIMEFRAMES, country_code, GPROP)
# google_requests.interest_over_time()
# google_requests.interest_per_region()
# google_requests.country_trends()
data = google_requests.search_array()
#print(data)
request_window(data)
plot_data(data)
