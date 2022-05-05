---
title: "Geospatial Feature Engineering and Viz"
date: 2022-05-05T22:29:49+02:00
draft: true
---

There is the potential to add a lot of different features based on these dataframes, but my goal was to focus on engineering the following (predominantly geospatial) features for each data point:

1. The name of the nearest city.
2. The distance from the district's coordinates to the nearest city.
3. The population of the nearest city.
4. The nearest 'big city' (a big city is categorized as >500,000 residents in the given year, 1990).
5. The distance to the nearest 'big city'.

Below I walk through the code I used to add these 5 bits of information to each housing district's list of predictors. I then develop some maps/plots to help visualize the new features and see what information was added, and finally I train an xgboost model on the expanded feature set and assess its performance relative to the previous models I had built using the original data only.

Before we start a few limitations to note on the data we are adding - I am not sure if these are comprehensive lists of the cities in California. In fact there is imperfect overlap between the coordinates and population data (so some of the smaller towns are not prefectly represented in the added features), so the data aren't perfect but do a fair job of representing the large/medium cities and towns in California

If there are more good features you can think of engineering I encourage you to give the notebook a fork and try them out!

