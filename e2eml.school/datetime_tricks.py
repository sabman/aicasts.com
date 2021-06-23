
# https://e2eml.school/datetime_tricks.html
# DateTime Object

import datetime

# (hours, minutes)
start_time = datetime.time(7, 0)
# (year, month, day)
start_date = datetime.date(2015, 5, 1)
# Create a datetime object
start_datetime = datetime.datetime.combine(
    start_date, start_time)


# Number of seconds from 12:00 am, January 1, 1970, UTC
# is a computer-friendly way to handle time.
unix_epoch = timestamp(start_datetime)
start_datetime = fromtimestamp(1457453760)
