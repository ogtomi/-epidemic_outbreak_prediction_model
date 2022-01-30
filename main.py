import pycountry
from pytrends.request import TrendReq
import gtab
import matplotlib.pyplot as plt

plt.style.use('ggplot')
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)

def country_to_code(country):
    return pycountry.countries.get(name=str(country)).alpha_2

country = "poland"
country_code = country_to_code(country)

t = gtab.GTAB()
t.set_options(pytrends_config={"geo": country_code, "timeframe": "2021-01-01 2022-01-01"})
#t.create_anchorbank(verbose=True)

KEYWORDS = ["covid", 'pizza', 'porno']
SCALING_KW_LIST = ["chicago", "poland", "warsaw", "gdansk"]
CAT = '0'
TIMEFRAMES = ['today 12-m', 'today 3-m', 'today 1-m']
GPROP = ''
KW = []

def interest_over_time(country_code):
    pytrends.build_payload(KW, CAT, TIMEFRAMES[2], country_code, GPROP)
    data = pytrends.interest_over_time()
    return data

def plot_absolute_comparison(country_code):
    pytrends.build_payload(KEYWORDS, CAT, TIMEFRAMES[2], country_code, GPROP)
    plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

    for kw in KEYWORDS:
        kw_query = t.new_query(kw)
        ax.plot(kw_query.max_ratio, label=kw)
        ax.legend()

    plt.show()

def get_absolute_data(country_code):
    pytrends.build_payload(KEYWORDS, CAT, TIMEFRAMES[2], country_code, GPROP)
    
    for kw in KEYWORDS:
        kw_query = t.new_query(kw)
        print(kw_query['max_ratio'][0])
        print(kw_query['max_ratio'][1])
        print(kw_query['max_ratio'][0] + kw_query['max_ratio'][1])

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

        print(kw + ' rising queries: ')
        if data[kw]['rising'] is None:
            print('There is not enough data')
        else:
            print(data[kw]['rising'].head(9))
        print('___________')

def country_trends(country_code):
    data = pytrends.trending_searches(country_code)
    print(data)

# for kw in KEYWORDS:
#     KW.append(kw)
#     over_time_interest = interest_over_time(country_code)
#     per_region_interest = interest_per_region(country_code)
#     print(over_time_interest)
#     print(per_region_interest)
#     KW.pop()

# related_queries(country_code)
# country_trends(country)
# plot_absolute_comparison(country_code)
get_absolute_data(country_code)
