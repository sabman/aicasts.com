Make your work grounded in reality. Use real data. To go extra deep try to stay one step ahead.
Imagine you live in Berlin but you wanna get up as late as possible, so you can sleep as much as is possible.

Question: What time should I leave home for work?

- you know the time it takes to get from home -> station and station -> office by foot.
- When do trains arrive at departure station?
- How long do they take to get to destination station?

However departure and transit time has variation. We can rephrase our question to deal with probabilities instead of certainties.

We can set a goal like what time do I need to leave the house to get to office on time 9 times out of 10


## Data

The data that might solve this problem is historic records of train trips. 

i.e what time the trains leave destination station and what time they arrive at departure station.

Berlin data
https://daten.berlin.de/datensaetze/vbb-fahrplandaten-gtfs

```
# https://daten.berlin.de/datensaetze/vbb-fahrplandaten-gtfs
npm install -g print-gtfs-rt-cli
curl 'https://v0.berlin-gtfs-rt.transport.rest/feed' -s | print-gtfs-rt --json | head -n 1 | jq
```

```python

```
