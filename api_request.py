from pytrends.request import TrendReq

class GoogleRequests:
    def __init__(self, keywords_arr, cat, timeframes, country_code, gprop):
        self.keywords_arr = keywords_arr
        self.cat = cat
        self.timeframes = timeframes
        self.country_code = country_code
        self.gprop = gprop
        self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        self.querry_arr = []
    
    def interest_over_time(self):
        self.pytrends.build_payload(self.keywords_arr, self.cat, self.timeframes[2], self.country_code, self.gprop)
        data = self.pytrends.interest_over_time()
        print(data)
        return data

    def interest_per_region(self):
        self.pytrends.build_payload(self.keywords_arr, self.cat, self.timeframes[2], self.country_code, self.gprop)
        data = self.pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
        data = data.sort_values(by=self.keywords_arr, ascending=False)
        print(data)
        return data
    
    def related_queries(self):
        self.pytrends.build_payload(self.keywords_arr, self.cat, self.timeframes[2], self.country_code, self.gprop)
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
            print('___________')
    
    def country_trends(self):
        data = self.pytrends.trending_searches(self.country_code)
        print(data)
    
    def search_array(self):
        self.related_queries()
        return [*self.keywords_arr, *self.querry_arr]