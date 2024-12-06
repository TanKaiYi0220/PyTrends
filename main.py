import time
import pandas as pd
import json

import pytrends
from pytrends.request import TrendReq

def googletrends_queries(keywords, geo, loops=3, wait=10, csv='trends.csv', timeframe="all"):
    # Perform searches
    print('Number of queries to do: ', len(keywords) * len(geo))

    # Prepare containers
    trends = dict.fromkeys(geo)
    errors_list = []
    cnt = 1

    # Start loops
    for g in geo:
        trends[g] = {}
        for k in keywords:
            try:
                time.sleep(wait)
                pytrends.build_payload([k], timeframe=timeframe, geo=g, gprop='')
                
                req = json.dumps(pytrends.interest_over_time_widget["request"])
                
                trends[g][k] = pytrends.interest_over_time()[k]
                #print(cnt, 'Success: ', g, k)

            except Exception as e:
                print(cnt, ') Error: ', g, ' & ', k)
                print(e)
                errors_list.append([g,k])
            cnt+=1

    ### Redo searches with errors
    if len(errors_list) > 0:
        print('\nStart errors:')

        for t in range(1,loops+1):

            if len(errors_list) > 0:
                print('Loop ', t, ': ', len(errors_list), 'errors')

                for i in errors_list:
                    g = i[0]  # 1st element geo
                    k = i[1]  # 2nd element keyword
                    try:
                        time.sleep(wait)
                        pytrends.build_payload([k], timeframe='all', 
                                               geo=g, gprop='')
                        trends[g][k] = pytrends.interest_over_time()[k]
                        errors_list.remove([g,k])  # remove from list of errors
                        #print('Success: ', g, k)
                    except:
                        #print('*** Error: ', g, ' & ', k)
                        pass
    print('\nDone -', len(errors_list), 'errors left')
    
    ### Save dataframe
    dict_of_trends = {g: pd.DataFrame(k) for g,k in trends.items()}
    data_df = pd.concat(dict_of_trends, axis=1)
    data_df.to_csv(csv,index=False)
    
    return data_df

if __name__ == "__main__":
    # tz: -480=UTC+8
    # retries=3 is the best (https://github.com/GeneralMills/pytrends/issues/561)
    pytrends = TrendReq(hl='en-US', tz=-480, retries=3)

    # keywords
    keywords = ['apple', 'facebook']
    keywords.sort() # Sort the list

    # locations
    geo = ['US', 'AU']
    geo.sort()

    # date frames
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    date_frame = start_date + " " + end_date if start_date != "" and end_date != "" else "all"
    
    # Perform searches
    wait = 6 # in seconds

    # Prepare containers
    trends = dict.fromkeys(geo)
    errors_list = []
    cnt = 1

    data_df = googletrends_queries(keywords=keywords, geo=geo, loops=2, timeframe=date_frame)
    print(data_df)