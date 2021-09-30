
weather_filename = "fort-lauderdale-beach-weather.csv"
weather_file = open(weather_filename)
weather_data = weather_file.read()
# print(len(weather_data))
# print(weather_data[:200])
lines = weather_data.split("\n")
print(lines[:5])
labels = lines[0]
values = lines[1:]
n_values = len(values)
print(labels)
for i in range(10):
    print(values[i])

year = []
month = []
day = []
max_temp = []
j_year = 1
j_month = 2
j_day = 3
j_max_temp = 5

for i_row in range(n_values):
    split_values = values[i_row].split(",")
    print(split_values)
    year.append(int(split_values[j_year]))
    month.append(int(split_values[j_month]))
    day.append(int(split_values[j_day]))
    max_temp.append(float(split_values[j_max_temp]))
