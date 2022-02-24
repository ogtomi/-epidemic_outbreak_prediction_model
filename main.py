from re import search
from urllib import request
from django.http import QueryDict
import pycountry
from pytrends.request import TrendReq
import gtab
import matplotlib.pyplot as plt
import pandas as pd

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

def interest_over_time(country_code):
    pytrends.build_payload(KW, CAT, TIMEFRAMES[2], country_code, GPROP)
    data = pytrends.interest_over_time()
    return data

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

def interest_per_region(country_code):
    pytrends.build_payload(KW, CAT, TIMEFRAMES[2], country_code, GPROP)
    data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
    data = data.sort_values(by=KW, ascending=False)
    return data

def related_queries(country_code):
    pytrends.build_payload(KEYWORDS, CAT, TIMEFRAMES[2], country_code, GPROP)
    data = pytrends.related_queries()

    for kw in KEYWORDS:
        print(kw + ' top queries: ')
        if data[kw]['top'] is None:
            print('There is not enough data')
        else:
            print(data[kw]['top'].head(9))
            for index, row in data[kw]['top'].iterrows():
                QUERY_ARR.append(row['query'])

        print(kw + ' rising queries: ')
        if data[kw]['rising'] is None:
            print('There is not enough data')
        else:
            print(data[kw]['rising'].head(9))
        print('___________')

def country_trends(country_code):
    data = pytrends.trending_searches(country_code)
    print(data)

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
    print("shit should be plotted")
    plt.show()

# for kw in KEYWORDS:
#     KW.append(kw)
#     over_time_interest = interest_over_time(country_code)
#     per_region_interest = interest_per_region(country_code)
#     print(over_time_interest)
#     print(per_region_interest)
#     KW.pop()

related_queries(country_code)
# country_trends(country)
# print(QUERY_ARR)
SEARCH_ARR = [*KEYWORDS, *QUERY_ARR]
#plot_absolute_comparison(country_code, KEYWORDS)
# get_absolute_data(country_code)
request_window(SEARCH_ARR)
plot_data(df)

