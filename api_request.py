import pycountry
from pytrends.request import TrendReq
import gtab
import matplotlib.pyplot as plt
import pandas as pd

class GoogleRequests:
    def __init__(self, keywords_arr, cat, timeframes, country, gprop, anchor_time):
        self.keywords_arr = keywords_arr
        self.cat = cat
        self.timeframes = timeframes
        self.country = country
        self.gprop = gprop
        self.anchor_time = anchor_time
        self.querry_arr = []
        self.trends_arr = []
        self.country_code = self.country_to_code(self.country)
        self.underscored_countryname = country.replace(" ", "_")

        self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        self.t = gtab.GTAB()
        self.t.set_options(pytrends_config={"geo": self.country_code, "timeframe": self.anchor_time})
        #self.t.create_anchorbank(verbose=True)
        self.df = pd.DataFrame()

    def country_to_code(self, country):
        return pycountry.countries.get(name=str(country)).alpha_2
    
    def interest_over_time(self, word_list):
        self.pytrends.build_payload(word_list, self.cat, self.timeframes[0], self.country_code, self.gprop)
        data = self.pytrends.interest_over_time()
        print(data)
        return data

    def interest_per_region(self, word_list):
        self.pytrends.build_payload(word_list, self.cat, self.timeframes[0], self.country_code, self.gprop)
        data = self.pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
        #data = data.sort_values(by=self.keywords_arr, ascending=False)
        print(data)
        return data
    
    def related_queries(self):
        self.pytrends.build_payload(self.keywords_arr, self.cat, self.timeframes[0], self.country_code, self.gprop)
        data = self.pytrends.related_queries()

        for kw in self.keywords_arr:
            print(kw + ' top queries: ')
            if data[kw]['top'] is None:
                print('There is not enough data')
            else:
                print(data[kw]['top'].head(9))
                for index, row in data[kw]['top'].iterrows():
                    self.querry_arr.append(row['query'])

            print(kw + ' rising queries: ')
            if data[kw]['rising'] is None:
                print('There is not enough data')
            else:
                print(data[kw]['rising'].head(9))
                for index, row in data[kw]['rising'].iterrows():
                    self.querry_arr.append(row['query'])
            #print('___________')
    
    def country_trends(self):
        data = self.pytrends.trending_searches(self.underscored_countryname)
        for index, row in data.iterrows():
            self.trends_arr.append(row.values[0])
    
    def search_array(self):
        self.related_queries()
        self.country_trends()
        return [*self.keywords_arr, *self.querry_arr, *self.trends_arr]
    
    def arrange_data(self, word_list):
        ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

        for kw in word_list:
            kw_query = self.t.new_query(kw)
            self.df[kw] = kw_query.max_ratio
            ax.plot(kw_query.max_ratio, label=kw)
            ax.legend()
    
    def request_window(self):
        request_arr = []
        search_arr = self.search_array()
        #plt.figure()

        for i in range(len(search_arr)):
            request_arr.append(search_arr[i])
            
            if i % 5 == 0:
                self.arrange_data(request_arr)
                #self.interest_over_time(request_arr)
                #self.interest_per_region(request_arr)
                request_arr = []
        
        return self.df