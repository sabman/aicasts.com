import datetime
import requests
import os
import pandas as pd
import time
import tools
os.environ['TZ'] = "US/Eastern"
time.tzset()


def download_data(verbose=True):
    harvard_stop_id = '70068'
    jfk_stop_id = '70086'

    start_time = datetime.time(7, 0)
    end_time = datetime.time(10, 0)
    start_date = datetime.date(2021, 5, 1)
    end_date = datetime.date(2021, 8, 1)

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
        print(SRequest)
        s = requests.get(SRequest)
        s_json = s.json()
        for trip in s_json['travel_times']:
            trips.append({
                "dep": datetime.datetime.fromtimestamp(float(trip['dep_dt'])),
                "arr": datetime.datetime.fromtimestamp(float(trip['arr_dt']))
            })
        if verbose:
            print(check_date, ':', len(s_json['travel_times']))

        i_day += 1

    return trips


def calculate_arrival_times(
    trips,
    harvard_walk=4,
    jfk_walk=6,
    target_hour=9,
    target_minute=0,
    train_dep_min=-60,
    train_dep_max=0,
    debug=False,
):
    """
    Based on the downloaded trips data, calculate the departure times that each
    possible departure time would result in.

    The kwargs above default to our specific use case (work starts at 9:00, it
    take 6 minutes to walk to JFK, and it take 4 minutes to walk from Harvard
    square to work)

    Parameters
    ----------
    harvard_walk, jfk_walk: int
        the time in min to take these walks
    trips: Dataframe
    target_hour, target_minute: int
        The time work starts is target_hour:target_minute
    train_dep_min, train_dep_max: int
        The time relative to the target, in minutes when the train departs from
        JFK. Negative number means minutes *before* the target. Min max define
        the time window under consideration.
    debug: boolean
    """
    minuites_per_hour = 60
    date_format = "%Y-%m-%d"
    trips_expanded = []
    for raw_trip in trips:
        rel_dep = (
            minuites_per_hour * (raw_trip['dep'].hour - target_hour) +
            (raw_trip['dep'].minute - target_minute))
        rel_arr = (
            minuites_per_hour * (raw_trip['arr'].hour - target_hour) +
            (raw_trip['arr'].minute - target_minute))

        if rel_dep > train_dep_min and rel_dep <= train_dep_max:
            new_trip = {
                'departure': rel_dep,
                'arrival': rel_arr,
                'date': raw_trip['dep'].date()
            }
            trips_expanded.append(new_trip)

    trips_df = pd.DataFrame(trips_expanded)

    if debug:
        print(trips_df)
        tools.custom_scatter(trips_df['departure'], trips_df['arrival'])
    door_arrivals = {}



def get_trips():
    """
    Attempt to restore a saved copy.
    If unsuccessful, download a new one.

    Returns
    -------

    trips: list of dicts
    """

    trips_filename = "trips.pickle"
    try:
        trips = tools.restore(trips_filename)
    except Exception:
        trips = download_data()
        tools.store(trips, trips_filename, True)
    return trips


if __name__ == "__main__":
    trips = get_trips()
    # make arrival time a function of departure time for everyday
    # date, dep time (decision), rel arr time (relative to when we wanna get to work)
    # decision: when do we leave home
    # outcome: when do we get to work
    # check every min of leaving house what time we'll get to work
    # relative arr time
    arrival_times = calculate_arrival_times(trips, debug=False)
