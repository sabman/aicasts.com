
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

# Gets the day of the week for a given date.
# Monday is 0, Sunday is 6
weekday_number = start_datetime.date().weekday()


# Pass a date string and a code for interpreting it.
new_datetime = datetime.datetime.strptime(
    '2018-06-21', '%Y-%m-%d')
# Turn a datetime into a date string.
datestr = new_datetime.strftime('%Y-%m-%d')
print(datestr)


