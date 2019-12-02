
# Introduction

Why GeoTemporal matters
* https://www.youtube.com/watch?v=_t7jlFbpty4

# Concepts

## Time and Range Data Types
- `timestamptz` (native to postgresql)
- `timestampset`
- `period`
- `periodset`

## Temporal Types

tboolinst, tboolseq, tbooli, and tbools
- `tintinst`, `tintseq`, `tinti`, and `tints`
- `tfloatinst`, `tfloatseq`, `tfloati`, and `tfloats`
- `ttextinst`, `ttextseq`, `ttexti`, and `ttexts`
- `tgeompointinst`, `tgeompointseq`, `tgeompointi`, and `tgeompoints`
- `tgeogpointinst`, `tgeogpointseq`, `tgeogpointi`, and `tgeogpoints`

where the suffixes "inst", "seq", "i", and "s" correspond, respectively, to the durations instant, sequence,
instant set, and sequence set.


## Interesting Operators

```sql
-- Do the operands ever intersect?
SELECT tintersects(tgeompointseq '[Point(0 1),@2001-01-01, Point(3 1)@2001-01-04)', 
  geometry 'Polygon((1 0,1 2,2 2,2 0,1 0))')) &= true;
  
-- Does the operands always intersect?
SELECT tintersects(tgeompointseq '[Point(0 1)@2001-01-01, Point(3 1)@2001-01-04)',
  geometry 'Polygon((0 0,0 2,4 2,4 0,0 0))') @= true;
-- true
```

## Interesting Spatial Functions

`speed`: Speed of the temporal point in units per second
Signature: `speed({tpointseq, tpoints}): tfloats`

```sql
SELECT speed(tgeompoints(ARRAY[tgeompointseq
'[Point(0 0)@2000-01-01, Point(1 1)@2000-01-02, Point(1 0)@2000-01-03]',
'[Point(1 0)@2000-01-04, Point(0 0)@2000-01-05]']))
* 3600 * 24;
-- "{[1.4142135623731@2000-01-01, 1.4142135623731@2000-01-02),
[1@2000-01-02, 1@2000-01-03], [1@2000-01-04, 1@2000-01-05]}"
```

`nearestApproachDistance`: Smallest distance ever between the two arguments
Signature: `nearestApproachDistance({geometry, tgeompointmult}, {geometry, tgeompointmult}): float`

```sql
SELECT nearestApproachDistance(
tgeompointseq '[Point(0 0)@2012-01-02, Point(1 1)@2012-01-04, Point(0 0)@2012-01-06)',
geometry 'Linestring(2 2,2 1,3 1)');
-- "1"
SELECT nearestApproachDistance(
tgeompointseq '[Point(0 0)@2012-01-01, Point(1 1)@2012-01-03, Point(0 0)@2012-01-05)',
tgeompointseq '[Point(2 0)@2012-01-02, Point(1 1)@2012-01-04, Point(2 2)@2012-01-06)');
-- "0.5"
```

```sql
SELECT DISTINCT R.RegionId, T.CarId
FROM Trips T, Regions R
WHERE ST_Intersects(trajectory(T.Trip), R.Geom)
ORDER BY R.RegionId, T.CarId;
```

## Spatial Relationships for Temporal Points

```sql
SELECT intersects(geometry 'Polygon((0 0,0 1,1 1,1 0,0 0))',
  tgeompoint '[Point(0 1)@2012-01-01, Point(1 1)@2012-01-03)');
```

```
SELECT ST_Intersects(geometry 'Polygon((0 0,0 1,1 1,1 0,0 0))',
  geometry 'Linestring(0 1,1 1)');
```

## Range Queries

The queries in this category restrict Trips with respect to a spatial, temporal, or spatio-temporal point or range. In the examples, the spatial points and ranges are given, respectively, in tables Points and Regions, while temporal points and ranges are given, respectively, in tables Instants and Periods.


1. List the cars that have passed at a region from Regions.

```sql 
SELECT DISTINCT R.RegionId, T.CarId
FROM Trips T, Regions R
WHERE ST_Intersects(trajectory(T.Trip), R.Geom)
ORDER BY R.RegionId, T.CarId;
```

This is a spatial range query. The query verifies that the trajectory of the car intersects the region. PostGIS performs an implicit bounding box comparison trajectory(T.Trip) && R.Geom using the spatial index on table Regions when executing the predicate ST_Intersects.

2. List the cars that were within a region from Regions during a period from Periods.

```sql
SELECT R.RegionId, P.PeriodId, T.CarId
FROM Trips T, Regions R, Periods P
WHERE T.Trip && stbox(R.Geom, P.Period) AND
  _intersects(atPeriod(T.Trip, P.Period), R.Geom)
ORDER BY R.RegionId, P.PeriodId, T.CarId;
```

This is a spatio-temporal range query. The query performs a bounding box comparison with the && operator using the spatio-temporal index on table Trips. After that, the query verifies that the location of the car during the period intersects the region. Notice that the predicate \_intersects is used instead of intersects to avoid an implicit index test with the bounding box comparison atPeriod(Trip, P.Period) && R.Geom is performed using the spatio-temporal index.

3. List the pairs of cars that were both located within a region from Regions during a period from Periods.

```sql
SELECT DISTINCT T1.CarId AS CarId1, T2.CarId AS CarId2, R.RegionId, P.PeriodId
FROM Trips T1, Trips T2, Regions R, Periods P
WHERE T1.CarId < T2.CarId AND T1.Trip && stbox(R.Geom, P.Period) AND
  T2.Trip && stbox(R.Geom, P.Period) AND
  _intersects(atPeriod(T1.Trip, P.Period), R.Geom) AND
  _intersects(atPeriod(T2.Trip, P.Period), R.Geom)
ORDER BY T1.CarId, T2.CarId, R.RegionId, P.PeriodId;
```

4. List the first time at which a car visited a point in Points.

```sql
SELECT T.CarId, P.PointId, MIN(startTimestamp(atValue(T.Trip,P.Geom))) AS Instant
FROM Trips T, Points P
WHERE ST_Contains(trajectory(T.Trip), P.Geom)
GROUP BY T.CarId, P.PointId;
```

5. Compute how many cars were active at each period in Periods.

```sql
SELECT P.PeriodID, COUNT(*), TCOUNT(atPeriod(T.Trip, P.Period))
FROM Trips T, Periods P
WHERE T.Trip && P.Period
GROUP BY P.PeriodID
ORDER BY P.PeriodID;
```

6. For each region in Regions, give the window temporal count of trips with a 10-minute interval.

```sql
SELECT R.RegionID, WCOUNT(atGeometry(T.Trip, R.Geom), interval '10 min')
FROM Trips T, Regions R
WHERE T.Trip && R.Geom
GROUP BY R.RegionID
HAVING WCOUNT(atGeometry(T.Trip, R.Geom), interval '10 min') IS NOT NULL
ORDER BY R.RegionID;
```

7. Count the number of trips that were active during each hour in May 29, 2007.

```sql
WITH TimeSplit(Period) AS (
  SELECT period(H, H + interval ’1 hour’)
  FROM generate_series(timestamptz ’2007-05-29 00:00:00’,
    timestamptz ’2007-05-29 23:00:00’, interval ’1 hour’) AS H )
SELECT Period, COUNT(*)
FROM TimeSplit S, Trips T
WHERE S.Period && T.Trip AND atPeriod(Trip, Period) IS NOT NULL
GROUP BY S.Period
ORDER BY S.Period;
```

8. List the overall traveled distances of the cars during the periods from Periods.

```sql
SELECT T.CarId, P.PeriodId, P.Period,
  SUM(length(atPeriod(T.Trip, P.Period))) AS Distance
FROM Trips T, Periods P
WHERE T.Trip && P.Period
GROUP BY T.CarId, P.PeriodId, P.Period
ORDER BY T.CarId, P.PeriodId;
```
 
# Installation

```
docker pull codewit/mobilitydb
docker volume create mobilitydb_data
docker run --name "mobilitydb" -d -p 25432:5432 -v mobilitydb_data:/var/lib/postgresql
codewit/mobilitydb
```

```
docker exec -t -i mobilitydb psql -h localhost -p 5432 -d mobilitydb -U docker
```

```
CREATE EXTENSION MobilityDB CASCADE;
```

# Testing

## Loading data

# Real World Application
