import datetime

def download_data(verbose=True):
    harvard_stop_id = '70086'
    jfk_stop_id = '70086'
    
    start_time = datetime.time(7, 0)
    end_time = datetime.time(10, 0)
    start_date = datetime.date(2015, 5, 1)
    end_date = datetime.date(2018, 5, 1)

    TTravelURL = "http://realtime.mbta.com/developer/api/v2.1/traveltimes"
    TKey = "?api_key=wX9NwuHnZU2To07GmGR"
    TFormat = "json"
