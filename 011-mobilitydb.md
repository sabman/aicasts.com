
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

> The query performs a bounding box comparison with the && operator using the spatio-temporal index on the Trips table. It then projects the trip to the period, computes the length of the projected trip, and sum the lengths of all the trips of the same car during the period.


9. List the minimum distance ever between each car and each point from Points.

```sql
SELECT T.CarId, P.PointId, MIN(trajectory(T.Trip) <-> P.Geom) AS MinDistance
FROM Trips T, Points P
GROUP BY T.CarId, P.PointId
ORDER BY T.CarId, P.PointId;
```

> The query projects the trip to the spatial dimension with the trajectory function and computes the traditional distance between the trajectory of the trip and the point. The traditional minimum function is then applied for computing the minimum distance between all trips of the car and the point.

 
 10. List the minimum temporal distance between each pair of cars.
 
```sql
SELECT 
  T1.CarId AS Car1Id, 
  T2.CarId AS Car2Id, 
  MIN(T1.Trip <-> T2.Trip) AS MinDistance
FROM Trips T1, Trips T
WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
GROUP BY T1.CarId, T2.CarId
ORDER BY T1.CarId, T2.CarId;
```

The query selects two trips T1 and T2 from distinct cars that were both traveling during a common period of time, computes the temporal distance between the trips, and then computes the temporal minimum distance between all trips of the two cars. The query uses the spatio-temporal index to filter the pairs of trips that were both traveling during a common period of time.

 11. List the nearest approach time, distance, and shortest line between each pair of trips.
 
 ```sql
 SELECT T1.CarId AS Car1Id, T1.TripId AS Trip1Id, T2.CarId AS Car2Id,
  T2.TripId AS Trip2Id, period(NearestApproachInstant(T1.Trip, T2.Trip)) AS Time,
  NearestApproachDistance(T1.Trip, T2.Trip) AS Distance,
  ShortestLine(T1.Trip, T2.Trip) AS Line
FROM Trips1 T1, Trips1 T
WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
ORDER BY T1.CarId, T1.TripId, T2.CarId, T2.TripId;
 ```
 
This query shows similar functionality as that provided by the PostGIS functions `ST_ClosestPointOfApproach` and `ST_DistanceCPA`. The query selects two trips T1 and T2 from distinct cars that were both traveling during a common period of time and computes the required results.

12. List the nearest approach time, distance, and shortest line between each pair of trips.

```sql
SELECT T1.CarId AS CarId1, T2.CarId AS CarId2, atPeriodSet(T1.Trip,
  period(atValue(tdwithin(T1.Trip, T2.Trip, 10.0), TRUE))) AS Position
FROM Trips T1, Trips T
WHERE T1.CarId < T2.CarId AND T1.Trip && expandSpatial(T2.Trip, 10) AND
  atPeriodSet(T1.Trip, period(atValue(tdwithin(T1.Trip, T2.Trip, 10.0), TRUE)))
  IS NOT NULL
ORDER BY T1.CarId, T2.CarId, Position;
```

The query performs for each pair of trips T1 and T2 of distinct cars a bounding box comparison with the && operator using the spatio-temporal index on the Trips table, where the bounding box of T2 is expanded by 10 m. Then, the period expression computes the periods during which the cars were within 10 m. from each other and the atPeriodSet function projects the trips to those periods. Notice that the expression `tdwithin(T1.Trip, T2.Trip, 10.0)` is conceptually equivalent to `dwithin(T1.Trip, T2.Trip) #<= 10.0`. However, in this case the spatio-temporal index cannot be used for filtering values.


**Nearest-Neighbor Queries**

13. For each trip from Trips, list the three points from Points that have been closest to that car.


```sql
WITH TripsTraj AS (
  SELECT *, trajectory(Trip) AS Trajectory FROM Trips )
SELECT T.CarId, P1.PointId, P1.Distance
FROM TripsTraj T CROSS JOIN LATERAL (
  SELECT P.PointId, T.Trajectory <-> P.Geom AS Distance
  FROM Points P
  ORDER BY Distance LIMIT 3 
) AS P1
ORDER BY T.TripId, T.CarId, P1.Distance;
```

This is a nearest-neighbor query where both the reference and the candidate objects are moving. Therefore, it is not possible to proceed as in the previous query to first project the moving points to the spatial dimension and then compute the traditional distance. Given a trip T1 in the outer query, the subquery computes the temporal distance between T1 and a trip T2 of another car distinct from the car from T1 and then computes the minimum value in the temporal distance. Finally,the ORDER BY and LIMIT clauses in the inner query select the three closest cars.


14. For each trip from Trips, list the three cars that are closest to that car

```sql
SELECT T1.CarId AS CarId1, C2.CarId AS CarId2, C2.Distance
FROM Trips T1 CROSS JOIN LATERAL (
SELECT T2.CarId, minValue(T1.Trip <-> T2.Trip) AS Distance
FROM Trips T2
WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
ORDER BY Distance LIMIT 3 ) AS C2
ORDER BY T1.CarId, C2.CarId;
```

15. For each trip from Trips, list the points from Points that have that car among their three nearest neighbors.

```sql
WITH TripsTraj AS (
  SELECT *, trajectory(Trip) AS Trajectory FROM Trips ),
PointTrips AS (
  SELECT P.PointId, T2.CarId, T2.TripId, T2.Distance
  FROM Points P CROSS JOIN LATERAL (
  SELECT T1.CarId, T1.TripId, P.Geom <-> T1.Trajectory AS Distance
  FROM TripsTraj T
  ORDER BY Distance LIMIT 3 ) AS T2 )
SELECT T.CarId, T.TripId, P.PointId, PT.Distance
FROM Trips T CROSS JOIN Points P JOIN PointTrips PT
ON T.CarId = PT.CarId AND T.TripId = PT.TripId AND P.PointId = PT.PointId
ORDER BY T.CarId, T.TripId, P.PointId;
 ```
 
This is a reverse nearest-neighbor query with moving reference objects and static candidate objects. The query starts by computing the corresponding nearest-neighbor query in the temporary table PointTrips as it is done in Query 13. Then, in the main query it verifies for each trip T and point P that both belong to the PointTrips table.

16. For each trip from Trips, list the cars having the car of the trip among the three nearest neighbors.

```sql
WITH TripDistances AS (
  SELECT T1.CarId AS CarId1, T1.TripId AS TripId1, T3.CarId AS CarId2,
    T3.TripId AS TripId2, T3.Distance
  FROM Trips T1 CROSS JOIN LATERAL (
  SELECT T2.CarId, T2.TripId, minValue(T1.Trip <-> T2.Trip) AS Distance
  FROM Trips T
  WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
  ORDER BY Distance LIMIT 3 ) AS T3 )
SELECT T1.CarId, T1.TripId, T2.CarId, T2.TripId, TD.Distance
FROM Trips T1 JOIN Trips T2 ON T1.CarId < T2.CarId
  JOIN TripDistances TD ON T1.CarId = TD.CarId1 AND T1.TripId = TD.TripId1 AND
  T2.CarId = TD.CarId2 AND T2.TripId = TD.TripId
ORDER BY T1.CarId, T1.TripId, T2.CarId, T2.TripId;
```
This is a reverse nearest-neighbor query where both the reference and the candidate objects are moving. The query starts by computing the corresponding nearest-neighbor query in the temporary table TripDistances as it is done in Query 14. Then, in the main query it verifies for each pair of trips T1 and T2 that both belong to the TripDistances table.

17. Foreachgroupoftendisjointcars,listthepoint(s)fromPoints,havingtheminimumaggregateddistancefromthegiven group of ten cars during the given period.
 
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

The ZIP file with the data for this tutorial contains a set of CSV files as follows:
* datamcar.csv with fields Moid, Licence, Type, and Model contains the vehiclede scriptions (without position history).
* trips.csv with fields Moid, Tripid, Pos_x, Pos_y, and Instant contains vehicles movements and pauses
* queryinstants.csv with fields Id and Instant contains timestamps used for queries.
* queryperiods.csv with fields Id, Begin, and End contains periods used for the queries.
* querypoints.csv with fields Id, Pos_x, and Pos_y contains points used for queries.
* queryregions.csv with fields Id, SegNo, Xstart, Ystart, Xend, and Yend contains the polygons used for queries.

```
CREATE EXTENSION MobilityDB CASCADE;
```

By using `CASCADE` we load the required "PostGIS" extension prior to loading MobilityDB.

### Schema

**Cars**

```sql
CREATE TABLE Cars (
  CarId integer PRIMARY KEY,
  Licence varchar(32),
  Type varchar(32),
  Model varchar(32)
)
```

**Trips**

```sql
CREATE TABLE TripsInput (
  CarId integer REFERENCES Cars,
  TripId integer,
  Lon float,
  Lat float,
  T timestamptz,
  PRIMARY KEY (CarId, TripId, T)
);  
```

```sql
CREATE TABLE Instants (
  InstantId integer PRIMARY KEY,
  Instant timestamptz
);
CREATE TABLE Periods (
  PeriodId integer PRIMARY KEY,
  Tstart TimestampTz,
  Tend TimestampTz,
  Period period
);
CREATE TABLE Points (
  PointId integer PRIMARY KEY,
  PosX double precision,
  PosY double precision,
  Geom Geometry(Point)
);
CREATE TABLE RegionsInput
(
  RegionId integer,
  SegNo integer,
  XStart double precision,
  YStart double precision,
  XEnd double precision,
  YEnd double precision,
  PRIMARY KEY (RegionId, SegNo)
);
CREATE TABLE Regions (
  RegionId integer PRIMARY KEY,
  Geom Geometry(Polygon)
);
```

# Real World Application

- emergency incident management
- traffic management
- logitics optimisation
- security and servalence
- forensic and legal usecases
