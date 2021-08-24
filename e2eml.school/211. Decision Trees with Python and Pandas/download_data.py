import datetime
import requests

def download_data(verbose=True):
    harvard_stop_id = '70086'
    jfk_stop_id = '70086'
    
    start_time = datetime.time(7, 0)
    end_time = datetime.time(10, 0)
    start_date = datetime.date(2015, 5, 1)
    end_date = datetime.date(2018, 5, 1)

    TTravelURL = "http://realtime.mbta.com/developer/api/v2.1/traveltimes"
    TKey = "?api_key=wX9NwuHnZU2ToO7GmGR9uw"
    TFormat = "&format=json"
    from_stop = "&from_stop="+str(jfk_stop_id) 
    to_stop = "&to_stop="+str(harvard_stop_id)

    # cycle through all the days
    i_day = 0
    trips = []
    while True:
        check_date = start_date + datetime.timedelta(days=i_day)
        if check_date > end_date:
            break

        from_time = datetime.datetime.combine(check_date, start_time)
        to_time = datetime.datetime.combine(check_date, end_time)
        TFrom_time = "&from_datetime="+str(int(from_time.timestamp()))
        TTo_time = "&to_datetime="+str(int(to_time.timestamp()))

        SRequest = "".join([
            TTravelURL,
            TKey,
            TFormat,
            from_stop, to_stop,
            TFrom_time, TTo_time
        ])
        s = requests.get(SRequest)
        s_json = s.json()
        for trip in s_json['travel_times']:
            trips.append({
                dep: datetime.datetime.fromtimestamp(float(trip['dep_dt'])),
                arr: datetime.datetime.fromtimestamp(float(trip['arr_dt']))
            })
        if verbose:
            print(check_date, ':', len(s_json['travel_times']))

        i_day += 1

    return trips

trips = download_data(verbose=True)
