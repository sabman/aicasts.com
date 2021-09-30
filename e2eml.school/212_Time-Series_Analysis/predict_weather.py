weather_filename = "fort-lauderdale-beach-weather.csv"
weather_file = open(weather_filename)
weather_data = weather_file.read()
# print(len(weather_data))
# print(weather_data[:200])
lines = weather_data.split("\n")
print(lines[:5])
labels = lines[0]
values = lines[1:]
print(labels)
for i in range(10):
    print(values[i])
