
# Introduction

Why GeoTemporal matters
* https://www.youtube.com/watch?v=_t7jlFbpty4
* https://www.youtube.com/watch?v=HyOLKAKh_e8
* https://docs.mobilitydb.com/MobilityDB/master/
* http://data4urbanmobility.l3s.uni-hannover.de/index.php/en/home-2/
* http://data4urbanmobility.l3s.uni-hannover.de/index.php/en/mission-2/
* http://data4urbanmobility.l3s.uni-hannover.de/index.php/en/results/
* https://www.bmvi.de/SharedDocs/DE/Artikel/DG/mfund-projekte/mobility-data-space.html

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

```sql
CREATE TABLE Cars (
  CarId integer NOT NULL UNIQUE,
  Licence varchar(32),
  Type varchar(32),
  Model varchar(32)
)

Alter table cars ADD UNIQUE(carid);
Alter table cars ALTER COLUMN carid SET NOT NULL;
```

`SELECT cdb_cartodbfytable('rasul','Cars')`

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

ALTER TABLE tripsinput ADD COLUMN carid INTEGER;
ALTER TABLE tripsinput ALTER COLUMN carid TYPE INTEGER
Alter TABLE tripsinput ADD UNIQUE (carid, tripid, t)
Alter TABLE tripsinput ADD CONSTRAINT fkcars FOREIGN KEY (carid) REFERENCES cars (carid)

```

```bash
https://localhost.lan/user/rasul/api/v2/sql?q=CREATE TABLE TripsInput (
  CarId integer REFERENCES Cars,
  TripId integer,
  Lon float,
  Lat float,
  T timestamptz,
  PRIMARY KEY (CarId, TripId, T)
)&api_key=b5ea4fd859ec55a4ff965bb1a2b382487130967c
```

`SELECT cdb_cartodbfytable('rasul','TripsInput')`

`https://localhost.lan/user/rasul/api/v2/sql?q=SELECT+cdb_cartodbfytable('rasul','TripsInput')&api_key=b5ea4fd859ec55a4ff965bb1a2b382487130967c`


```sql
CREATE TABLE Instants (
  InstantId integer PRIMARY KEY,
  Instant timestamptz
);

SELECT cdb_cartodbfytable('rasul','TripsInput')

ALTER TABLE instants ADD COLUMN instantid INTEGER UNIQUE NOT NULL

-- ----------

CREATE TABLE Periods (
  PeriodId integer PRIMARY KEY,
  Tstart TimestampTz,
  Tend TimestampTz,
  Period period
);

SELECT cdb_cartodbfytable('rasul','Periods')
ALTER TABLE periods ADD COLUMN periodid INTEGER UNIQUE NOT NULL

CREATE TABLE Points (
  PointId integer PRIMARY KEY,
  PosX double precision,
  PosY double precision,
  Geom Geometry(Point)
);

ALTER TABLE points ADD COLUMN pointid INTEGER UNIQUE NOT NULL

SELECT cdb_cartodbfytable('rasul','Points')

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

SELECT cdb_cartodbfytable('rasul','RegionsInput')

Alter TABLE regionsinput ADD COLUMN regionid int
Alter TABLE regionsinput ADD UNIQUE (regionid, segno)

CREATE TABLE Regions (
  RegionId integer PRIMARY KEY,
  Geom Geometry(Polygon)
)

Alter TABLE regions ADD COLUMN regionid integer UNIQUE NOT NULL

SELECT cdb_cartodbfytable('rasul','Regions')

```
```sql
CREATE TABLE Trips
(
  CarId integer NOT NULL,
  TripId integer NOT NULL,
  Trip tgeompoint,
  PRIMARY KEY (CarId, TripId),
  FOREIGN KEY (CarId) REFERENCES Cars (CarId)
);

SELECT cdb_cartodbfytable('rasul','Trips')

Alter TABLE trips ADD UNIQUE (carId, tripid)

Alter TABLE trips ADD CONSTRAINT fkcars FOREIGN KEY (carid) REFERENCES cars (carid)

```

We created the table `Trips` in order to assemble all points composing a trip into a single temporal point.

Loading the data is as follows:

```sql
COPY Cars(CarId, Licence, Type, Model) FROM ’/home/mobilitydb/data/datamcar.csv’
  DELIMITER  ’,’ CSV HEADER;
COPY TripsInput(CarId, TripId, Lon, Lat, T) FROM ’/home/mobilitydb/data/trips.csv’
  DELIMITER  ’,’ CSV HEADER;
COPY Instants(InstantId, Instant) FROM ’/home/mobilitydb/data/queryinstants.csv’
  DELIMITER  ’,’ CSV HEADER;
COPY Periods(PeriodId, Tstart, Tend) FROM ’/home/mobilitydb/data/queryperiods.csv’
  DELIMITER  ’,’ CSV HEADER;
UPDATE Periods
SET Period = period(Tstart, Tend);
```

```sql
COPY Points(PointId, PosX, PosY) FROM ’/home/mobilitydb/data/querypoints.csv’
  DELIMITER  ’,’ CSV HEADER;
UPDATE Points
SET Geom = ST_Transform(ST_SetSRID(ST_MakePoint(PosX, PosY), 4326), 5676);
COPY RegionsInput(RegionId, SegNo, XStart, YStart, XEnd, YEnd) FROM
  ’/home/mobilitydb/data/queryregions.csv’ DELIMITER  ’,’ CSV HEADER;
```

```sql
Alter table points add column geom(Geometry)

UPDATE points
SET geom =
ST_Transform(ST_SetSRID(ST_MakePoint(posx, posy), 4326), 5676);


```

The following query is used to load table Regions from the data in table RegionsInput.

```sql
INSERT INTO Regions (RegionId, Geom)
WITH RegionsSegs AS
(
  SELECT RegionId, SegNo,
    ST_Transform(ST_SetSRID(St_MakeLine(ST_MakePoint(XStart, YStart),
    ST_MakePoint(XEnd, YEnd)), 4326), 5676) AS Geom
  FROM RegionsInput
)
SELECT RegionId, ST_Polygon(ST_LineMerge(ST_Union(Geom ORDER BY SegNo)), 5676) AS Geom
FROM RegionsSegs
GROUP BY RegionId;


INSERT INTO regions (regionid, geom, the_geom)

with regionssegs as
(
  select regionid, segno,
    st_transform(st_setsrid(st_makeline(st_makepoint(xstart, ystart),
    st_makepoint(xend, yend)), 4326), 5676) as geom,
    st_setsrid(st_makeline(st_makepoint(xstart, ystart),
    st_makepoint(xend, yend)), 4326) as the_geom
  from regionsinput
)
select regionid,
    st_polygon(st_linemerge(st_union(geom order by segno)), 5676) as geom,
    st_polygon(st_linemerge(st_union(the_geom order by segno)), 4326) as the_geom
from regionssegs
group by regionid
```

The following query is used to load table Trips from the data in table TripsInput.

```sql
INSERT INTO Trips
SELECT CarId, TripId, tgeompointseq(array_agg(tgeompointinst(
  ST_Transform(ST_SetSRID(ST_MakePoint(Lon,Lat), 4326), 5676), T) ORDER BY T))
FROM TripsInput
GROUP BY CarId, TripId;

insert into trips(carid,tripid,trip)
select carid, tripid, tgeompointseq(array_agg(tgeompointinst(
  st_transform(st_setsrid(st_makepoint(lon,lat), 4326), 5676), t) order by t)) trip
from tripsinput
group by carid, tripid

```

There are a lot of nested functions, so reading from the innermost:

* Function `ST_MakePoint` construct a point from the Lon and Lat values.
* Function `ST_SetSRID` sets the SRID of the point to 4326, that is, to the standard WGS 84 GPS coordinates.
* Function `ST_Transform` transforms the spherical GPS coordinates to plannar coordinates fitted for Germany.
* Function `tgeompointinst` gets the point and the time values to create a temporal point of instant duration.
* Function array_agg collects in an array all temporal points of a given car and a given trip (as specified by the GROUP BY clause)andsortthembytime(asspecifiedbytheORDER BYclause)
* Function `tgeompointseq` gets the array of temporal points and construct a temporal point of sequence duration.

Finally, we create indexes on `traditional`, `spatial`, `temporal` or `spatiotemporal` attributes as well as views to select a subset of the rows from the corresponding tables. This can be done as follows.

```sql
CREATE UNIQUE INDEX Cars_CarId_Idx ON Cars USING btree(CarId);
CREATE INDEX Instants_Instant_Idx ON Instants USING btree(Instant);
CREATE INDEX Periods_Period_Idx ON Periods USING gist(Period);
CREATE INDEX Points_Geom_Idx ON Points USING gist(Geom);
CREATE INDEX Regions_Geom_Idx ON Regions USING gist(Geom);
CREATE INDEX Trips_CarId_idx ON Trips USING btree(CarId);
CREATE UNIQUE INDEX Trips_pkey_idx ON Trips USING btree(CarId, TripId);
CREATE INDEX Trips_gist_idx ON Trips USING gist(trip);
CREATE VIEW Instants1 AS SELECT * FROM Instants LIMIT 10;
```


# Real World Application

- emergency incident management
- traffic management
- logitics optimisation
- security and servalence
- forensic and legal usecases
- contextual advertising https://www.adonmo.com/


# Installation

```sh
docker pull codewit/mobilitydb
docker volume create mobilitydb_data
docker run --name "mobilitydb" -d -p 25432:5432 -v mobilitydb_data:/var/lib/postgresql codewit/mobilitydb
```

```sh
docker exec -t -i mobilitydb psql -h localhost -p 5432 -d mobilitydb -U docker

# on macs
docker exec -t -i mobilitydb psql -h `docker-machine ip` -p 25432 -d mobilitydb -U docker
```

The first command is to download the latest most up-to-date image of MobilityDB. The second command creates a volume container on the host, that we will use to persist the PostgreSQL database files outside of the MobilityDB container. The third command executes this binary image of PostgreSQL, PostGIS, and MobilityDB with the TCP port 5432 in the container mapped to port 25432 on the Docker host (user = pw = docker, db = mobilitydb). This image is based on this docker container, please refer to it for more information.

# Loading the Data in Partitioned Tables

PostgreSQL provides partitioning mechanisms so that large tables can be split in smaller physical tables. This may result in increased performance when querying and manipulating large tables. We will split the Trips table given in the previous section using **list partitioning**, where each partitition will contain all the **trips that start at a particular date**. For doing this, we use the procedure given next for automatically creating the partitions according to a date range.

```sql
CREATE OR REPLACE FUNCTION create_partitions_by_date(TableName TEXT, StartDate DATE,
  EndDate DATE)
RETURNS void AS $$
DECLARE
  d DATE;
  PartitionName TEXT;
BEGIN
  IF NOT EXISTS
    (SELECT 1
     FROM information_schema.tables
     WHERE table_name = lower(TableName))
  THEN
    RAISE EXCEPTION 'Table % does not exist', TableName;
  END IF;
  IF StartDate >= EndDate THEN
    RAISE EXCEPTION 'The start date % must be before the end date %', StartDate, EndDate;
  END IF;
  d = StartDate;
  WHILE d <= EndDate
  LOOP
    PartitionName = TableName || '_' || to_char(d, 'YYYY_MM_DD');
    IF NOT EXISTS
      (SELECT 1
       FROM information_schema.tables
       WHERE  table_name = lower(PartitionName))
    THEN
      EXECUTE format('CREATE TABLE %s PARTITION OF %s FOR VALUES IN (''%s'');',
        PartitionName, TableName, to_char(d, 'YYYY-MM-DD'));
      RAISE NOTICE 'Partition % has been created', PartitionName;
    END IF;
    d = d + '1 day'::interval;
  END LOOP;
  RETURN;
END
$$ LANGUAGE plpgsql;

```


In order to partition table `Trips` by date we need to add an addition column `TripDate` to table TripsInput.

```sql
ALTER TABLE TripsInput ADD COLUMN TripDate DATE;
UPDATE TripsInput T1
SET TripDate = T2.TripDate
FROM (SELECT DISTINCT TripId, date_trunc('day', MIN(T) OVER (PARTITION BY TripId))
  AS TripDate FROM TripsInput) T2
WHERE T1.TripId = T2.TripId;
```

The following statements create table `Trips` partitioned by date and the associated partitions.

```sql
CREATE TABLE Trips
(
  CarId integer NOT NULL,
  TripId integer NOT NULL,
  TripDate date,
  Trip tgeompoint,
  Traj geometry,
  PRIMARY KEY (CarId, TripId, TripDate),
  FOREIGN KEY (CarId) REFERENCES Cars (CarId)
) PARTITION BY LIST(TripDate);

SELECT create_partitions_by_date('Trips', (SELECT MIN(TripDate) FROM TripsInput),
  (SELECT MAX(TripDate) FROM TripsInput));
```
To see the partitions that have been created automatically we can use the following statement.

```sql
SELECT I.inhrelid::regclass AS child
FROM   pg_inherits I
WHERE  i.inhparent = 'trips'::regclass;
```

We modify the query that loads table Trips from the data in table TripsInput as follows.

```sql
INSERT INTO Trips
SELECT CarId, TripId, TripDate, tgeompointseq(array_agg(tgeompointinst(
  ST_Transform(ST_SetSRID(ST_MakePoint(Lon,Lat), 4326), 5676), T) ORDER BY T))
FROM TripsInput
GROUP BY CarId, TripId, TripDate;
```

Then, we can define the indexes and the views on the table Trips as shown in the previous section.

An important advantage of the partitioning mechanism in PostgreSQL is that the constraints and the indexes defined on the Trips table are propagated to the partitions as shown next.

```sql
INSERT INTO Trips VALUES (1, 10, '2007-05-30', NULL);

ERROR:  duplicate key value violates unique constraint "trips_2007_05_30_pkey"
DETAIL:  Key (carid, TripId, tripdate)=(1, 10, 2007-05-30) already exists.

EXPLAIN SELECT COUNT(*) from Trips where Trip && period '[2007-05-28, 2007-05-29]';

"Aggregate  (cost=59.95..59.96 rows=1 width=8)"
"  ->  Append  (cost=0.14..59.93 rows=8 width=0)"
"        ->  Index Scan using trips_2007_05_27_trip_idx on trips_2007_05_27  (cost=0.14..8.16 rows=1 width=0)"
"              Index Cond: (trip && 'STBOX T((,,2007-05-28 00:00:00+00),(,,2007-05-29 00:00:00+00))'::stbox)"
"        ->  Index Scan using trips_2007_05_28_trip_idx on trips_2007_05_28  (cost=0.27..8.29 rows=1 width=0)"
"              Index Cond: (trip && 'STBOX T((,,2007-05-28 00:00:00+00),(,,2007-05-29 00:00:00+00))'::stbox)"
"        ->  Index Scan using trips_2007_05_29_trip_idx on trips_2007_05_29  (cost=0.27..8.29 rows=1 width=0)"
"              Index Cond: (trip && 'STBOX T((,,2007-05-28 00:00:00+00),(,,2007-05-29 00:00:00+00))'::stbox)"
[...]
```

# Exploring the Data

In order to visualize the data with traditional tools such as QGIS we add to table Trip a column Traj of type geometry containing the trajectory of the trips.

```sql
ALTER TABLE Trips ADD COLUMN traj geometry;
UPDATE Trips
SET Traj = trajectory(Trip);

-- for cartodb
update trips set the_geom = st_transform(traj, 4326)
```

The visualization of the trajectories in QGIS is given in Figure 8.2, “Visualization of the trajectories of the trips in QGIS.”. In the figure red lines correspond to the trajectories of moving cars, while yellow points correspond to the position of stationary cars. In order to know the total number of trips as well as the number of moving and stationary trips we can issue the following queries.

```sql
SELECT count(*) FROM Trips;
-- 1797
SELECT count(*) FROM Trips WHERE GeometryType(Traj) = 'POINT';
-- 969
SELECT count(*) FROM Trips WHERE GeometryType(Traj) = 'LINESTRING';
-- 828
```

We can also determine the spatiotemporal extent of the data using the following query.

```sql
SELECT extent(Trip) from Trips
-- "STBOX T((2983189.5, 5831006.5,2007-05-27 00:00:00+02),
  (3021179.8, 5860883,2007-05-31 00:00:00+02))"
```

## Figure 8.2. Visualization of the trajectories of the trips in QGIS.

We continue investigating the data set by computing the maximum number of concurrent trips over the whole period

```sql
SELECT maxValue(tcount(Trip)) FROM Trips;
```

the average sampling rate

```sql
SELECT AVG(timespan(Trip)/numInstants(Trip)) FROM Trips;
-- "03:43:01.695539"
```

and the total travelled distance in kilometers of all trips:

```sql
SELECT SUM(length(Trip)) / 1e3 as TotalLengthKm FROM Trips;
-- 10074.8123345527
```

Now we want to know the average duration of a trip.

```sql
SELECT AVG(timespan(Trip)) FROM Trips;
--"07:31:57.195325"
```

This average duration is too long. To investigate more we use the following query

```sql
SELECT length(Trip) / 1e3, timespan(Trip) FROM Trips ORDER BY duration;
```

The query shows very many trips with zero length and a duration of more than one day. That would imply that there are stationary trips, representing parking overnight and even over the weekend. The previous query can hence be refined as follows:

```sql
SELECT AVG(timespan(Trip)/numInstants(Trip)) FROM Trips WHERE length(Trip) > 0;
-- "00:00:01.861784"
```

The following query produces a histogram of trip length.

```sql
WITH buckets (bucketNo, bucketRange) AS (
  SELECT 1, floatrange '[0, 0]' UNION
  SELECT 2, floatrange '(0, 100)' UNION
  SELECT 3, floatrange '[100, 1000)' UNION
  SELECT 4, floatrange '[1000, 5000)' UNION
  SELECT 5, floatrange '[5000, 10000)' UNION
  SELECT 6, floatrange '[10000, 50000)' UNION
  SELECT 7, floatrange '[50000, 100000)' ),
histogram AS (
  SELECT bucketNo, bucketRange, count(TripId) as freq
  FROM buckets left outer join trips on length(trip) <@ bucketRange
  GROUP BY bucketNo, bucketRange
  ORDER BY bucketNo, bucketRange
)
SELECT bucketNo, bucketRange, freq,
  repeat('■', ( freq::float / max(freq) OVER () * 30 )::int ) AS bar
FROM histogram;

```

## Querying the Data

We discuss next four categories of queries: range queries, distance queries, temporal aggregate queries, and nearest-neighbor queries[2].

### Range Queries

The queries in this category restrict `Trips` with respect to a spatial, temporal, or spatio-temporal point or range. In the examples, the spatial points and ranges are given, respectively, in tables Points and Regions, while temporal points and ranges are given, respectively, in tables Instants and Periods.

1. List the cars that have passed at a region from Regions.

```sql
SELECT DISTINCT R.RegionId, T.CarId
FROM Trips T, Regions R
WHERE ST_Intersects(trajectory(T.Trip), R.Geom)
ORDER BY R.RegionId, T.CarId;
```

This is a spatial range query. The query verifies that the trajectory of the car intersects the region. PostGIS performs an implicit bounding box comparison `trajectory(T.Trip)` && R.Geom using the spatial index on table Regions when executing the predicate `ST_Intersects`.

2. List the cars that were within a region from `Regions` during a period from Periods.

```sql
SELECT R.RegionId, P.PeriodId, T.CarId
FROM Trips T, Regions R, Periods P
WHERE T.Trip && stbox(R.Geom, P.Period) AND -- bbox
  _intersects(atPeriod(T.Trip, P.Period), R.Geom) -- location and time interesect
ORDER BY R.RegionId, P.PeriodId, T.CarId;
```

This is a spatio-temporal range query. The query performs a bounding box comparison with the `&&` operator using the spatio-temporal index on table Trips. After that, the query verifies that the location of the car during the period intersects the region. Notice that the predicate `_intersects` is used instead of intersects to avoid an implicit index test with the bounding box comparison `atPeriod(Trip, P.Period)` `&&` `R.Geom` is performed using the spatio-temporal index.

3. List the pairs of cars that were both located within a region from `Regions` during a period from `Periods`.

```sql
SELECT DISTINCT T1.CarId AS CarId1, T2.CarId AS CarId2, R.RegionId, P.PeriodId
FROM Trips T1, Trips T2, Regions R, Periods P
WHERE T1.CarId < T2.CarId AND T1.Trip && stbox(R.Geom, P.Period) AND
  T2.Trip && stbox(R.Geom, P.Period) AND
  _intersects(atPeriod(T1.Trip, P.Period), R.Geom) AND
  _intersects(atPeriod(T2.Trip, P.Period), R.Geom)
ORDER BY T1.CarId, T2.CarId, R.RegionId, P.PeriodId;

```

This is a **spatio-temporal range join query**. The query selects two trips of different cars and performs bounding box comparisons of each trip with a region and a period using the spatio-temporal index of the `Trips` table. The query then verifies that both cars were located within the region during the period.


4. List the first time at which a car visited a point in Points.

```sql

SELECT
  T.CarId,
  P.PointId,
  MIN(
    startTimestamp( -- startTimestamp: get the first `timestamp` of the projected trip
      atValue(T.Trip,P.Geom))) AS Instant -- atValue function projects the trip
FROM Trips T, Points P
-- verifies that the car passed by the point
WHERE ST_Contains(trajectory(T.Trip), P.Geom) -- testing that the trajectory contains the point
GROUP BY T.CarId, P.PointId;
```

The query selects a trip and a point and verifies that the car passed by the point by testing that the trajectory of the trip contains the point. Notice that PostGIS will perform the bounding box containment `trajectory(T.Trip) ~ P.Geom` using the spatial index on table Points before executing `ST_Contains`. Then, the query projects the trip to the point with the `atValue` function, get the first `timestamp` of the projected trip with the `startTimestamp` function, and applies the traditional `MIN` aggregate function for all trips of the car and the point.

## Temporal Aggregate Queries
There are three common types of temporal aggregate queries.

* Instant temporal aggregate queries in which, from a conceptual perspective, the traditional aggregate function is applied at each instant.

* Window temporal aggregate queries (also known as cumulative queries), which, given a time interval w, compute the value of the aggregate at a time instant t from the values during the time period [t-w, t].

* Span temporal aggregate queries, which, first, split the time line into predefined intervals independently of the target data, and then, for each of these intervals, aggregate the data that overlap the interval.


5. Compute how many cars were active at each period in Periods.

```sql
SELECT P.PeriodID, COUNT(*), TCOUNT(atPeriod(T.Trip, P.Period))
FROM Trips T, Periods P
WHERE T.Trip && P.Period
GROUP BY P.PeriodID
ORDER BY P.PeriodID;
```

This is an **instant temporal aggregate query**. For each period, the query projects the trips to the given period and applies the temporal count to the projected trips. The condition in the `WHERE` clause is used for filtering the trips with the spatio-temporal index on table `Trips`.

6. For each region in `Regions`, give the window temporal count of trips with a 10-minute interval.

```sql
SELECT R.RegionID, WCOUNT(atGeometry(T.Trip, R.Geom), interval '10 min')
FROM Trips T, Regions R
WHERE T.Trip && R.Geom
GROUP BY R.RegionID
HAVING WCOUNT(atGeometry(T.Trip, R.Geom), interval '10 min') IS NOT NULL
ORDER BY R.RegionID;
```

This is a window temporal aggregate query. Suppose that we are computing pollution levels by region. Since the effect of a car passing at a location lasts some time interval, this is a typical case for window aggregates. For each region, the query computes the spatial projection of the trips to the given region and apply the window temporal count to the projected trips. The condition in the `WHERE` clause is used for filtering the trips with the spatio-temporal index. The condition in the `HAVING` clause is used for removing regions that do not intersect with any trip.

7. Count the number of trips that were active during each hour in May 29, 2007.

```sql
WITH TimeSplit(Period) AS (
  SELECT period(H, H + interval '1 hour')
  FROM generate_series(timestamptz '2007-05-29 00:00:00',
    timestamptz '2007-05-29 23:00:00', interval '1 hour') AS H )
SELECT Period, COUNT(*)
FROM TimeSplit S, Trips T
WHERE S.Period && T.Trip AND atPeriod(Trip, Period) IS NOT NULL
GROUP BY S.Period
ORDER BY S.Period;
```

This is a span temporal aggregate query. The query defines the intervals to consider in the `TimeSplit` temporary table. For each of these intervals, the main query applies the traditional count function for counting the trips that overlap the interval.


### Distance queries

The queries in this category deal with either the distance travelled by a single object or the distance between two objects. The complexity of the latter queries depend, on the one hand, on whether the reference objects are static or moving, and on the other, on whether the operation required is either the minimum distance ever or the temporal distance computed at each instant.

8. List the overall traveled distances of the cars during the periods from `Periods`.

```sql
SELECT T.CarId, P.PeriodId, P.Period,
  SUM(
    length(atPeriod(T.Trip, P.Period)) -- length of projected trip
  ) AS Distance
FROM Trips T, Periods P
WHERE T.Trip && P.Period -- && bounding box commparison uses spatio-temporal index
GROUP BY T.CarId, P.PeriodId, P.Period
ORDER BY T.CarId, P.PeriodId;
```

The query performs a bounding box comparison with the `&&` operator using the spatio-temporal index on the `Trips` table. It then projects the trip to the period, computes the length of the projected trip, and sum the lengths of all the trips of the same car during the period.


9. List the minimum distance ever between each car and each point from Points.


```sql
SELECT T.CarId, P.PointId, MIN(trajectory(T.Trip) <-> P.Geom) AS MinDistance
FROM Trips T, Points P
GROUP BY T.CarId, P.PointId
ORDER BY T.CarId, P.PointId;
```
The query projects the trip to the spatial dimension with the `trajectory` function and computes the traditional distance between the trajectory of the trip and the point. The traditional minimum function is then applied for computing the minimum distance between all trips of the car and the point.


10. List the minimum temporal distance between each pair of cars.

```sql
SELECT T1.CarId AS Car1Id, T2.CarId AS Car2Id, MIN(T1.Trip <-> T2.Trip) AS MinDistance
FROM Trips T1, Trips T
WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
GROUP BY T1.CarId, T2.CarId
ORDER BY T1.CarId, T2.CarId;
```

The query selects two trips `T1` and `T2` from distinct cars that were both traveling during a common period of time, computes the temporal distance between the trips, and then computes the temporal minimum distance between all trips of the two cars. The query uses the spatio-temporal index to filter the pairs of trips that were both traveling during a common period of time.

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

This query shows similar functionality as that provided by the PostGIS functions `ST_ClosestPointOfApproach` and `ST_DistanceCPA`. The query selects two trips `T1` and `T2` from distinct cars that were both traveling during a common period of time and computes the required results.

12. List when and where a pairs of cars have been at 10 m or less from each other.


```sql
SELECT T1.CarId AS CarId1, T2.CarId AS CarId2, atPeriodSet(T1.Trip,
  period(atValue(tdwithin(T1.Trip, T2.Trip, 10.0), TRUE))) AS Position
FROM Trips T1, Trips T
WHERE T1.CarId < T2.CarId AND T1.Trip && expandSpatial(T2.Trip, 10) AND
  atPeriodSet(T1.Trip, period(atValue(tdwithin(T1.Trip, T2.Trip, 10.0), TRUE)))
  IS NOT NULL
ORDER BY T1.CarId, T2.CarId, Position;
```

The query performs for each pair of trips `T1` and `T2` of distinct cars a bounding box comparison with the `&&` operator using the spatio-temporal index on the `Trips` table, where the bounding box of `T2` is expanded by 10 m. Then, the `period` expression computes the periods during which the cars were within 10 m. from each other and the `atPeriodSet` function projects the trips to those periods. Notice that the expression `tdwithin(T1.Trip, T2.Trip, 10.0)` is conceptually equivalent to `dwithin(T1.Trip, T2.Trip) #<= 10.0`. However, in this case the spatio-temporal index cannot be used for filtering values.


## Nearest-Neighbor Queries

There are three common types of nearest-neighbor queries in spatial databases.

- k-nearest-neighbor (kNN) queries find the k nearest points to a given point.
- Reverse k-nearest-neighbor (RkNN) queries find the points that have a given point among their k nearest-neighbors.
- Given two sets of points P and Q, aggregate nearest-neighbor (ANN) queries find the points from P that have minimum aggregated distance to all points from Q.

The above types of queries are generalized to temporal points. However, the complexity of these queries depend on whether the reference object and the candidate objects are static or moving. In the examples that follow we only consider the nontemporal version of the nearest-neighbor queries, that is, the one in which the calculation is performed on the projection of temporal points on the spatial dimension. The temporal version of the nearest-neighbor queries remains to be done.


13. For each trip from `Trips`, list the three points from `Points` that have been closest to that car.

```sql
WITH TripsTraj AS (
  SELECT *, trajectory(Trip) AS Trajectory FROM Trips )
SELECT T.CarId, P1.PointId, P1.Distance
FROM TripsTraj T CROSS JOIN LATERAL (
SELECT P.PointId, T.Trajectory <-> P.Geom AS Distance
FROM Points P
ORDER BY Distance LIMIT 3 ) AS P1
ORDER BY T.TripId, T.CarId, P1.Distance;
```

This is a nearest-neighbor query with moving reference objects and static candidate objects. The query above uses PostgreSQL's lateral join, which intuitively iterates over each row in a result set and evaluates a subquery using that row as a parameter. The query starts by computing the trajectory of the trips in the temporary table `TripsTraj`. Then, given a trip `T` in the outer query, the subquery computes the traditional distance between the trajectory of `T` and each point `P`. The ORDER BY and LIMIT clauses in the inner query select the three closest points. PostGIS will use the spatial index on the `Points` table for selecting the three closest points.

14. For each trip from `Trips`, list the three cars that are closest to that car

```sql
SELECT T1.CarId AS CarId1, C2.CarId AS CarId2, C2.Distance
FROM Trips T1 CROSS JOIN LATERAL (
SELECT T2.CarId, minValue(T1.Trip <-> T2.Trip) AS Distance
FROM Trips T2
WHERE T1.CarId < T2.CarId AND period(T1.Trip) && period(T2.Trip)
ORDER BY Distance LIMIT 3 ) AS C2
ORDER BY T1.CarId, C2.CarId;
```


TThis is a nearest-neighbor query where both the reference and the candidate objects are moving. Therefore, it is not possible to proceed as in the previous query to first project the moving points to the spatial dimension and then compute the traditional distance. Given a trip T1 in the outer query, the subquery computes the temporal distance between T1 and a trip T2 of another car distinct from the car from T1 and then computes the minimum value in the temporal distance. Finally, the ORDER BY and LIMIT clauses in the inner query select the three closest cars.


15. For each trip from `Trips`, list the points from `Points` that have that car among their three nearest neighbors.


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

This is a reverse nearest-neighbor query with moving reference objects and static candidate objects. The query starts by computing the corresponding nearest-neighbor query in the temporary table `PointTrips` as it is done in Query 13. Then, in the main query it verifies for each trip `T` and point `P` that both belong to the `PointTrips` table.


16. For each trip from `Trips`, list the cars having the car of the trip among the three nearest neighbors.

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

This is a reverse nearest-neighbor query where both the reference and the candidate objects are moving. The query starts by computing the corresponding nearest-neighbor query in the temporary table `TripDistances` as it is done in Query 14. Then, in the main query it verifies for each pair of trips `T1` and `T2` that both belong to the `TripDistances` table.


17. For each group of ten disjoint cars, list the point(s) from `Points`, having the minimum aggregated distance from the given group of ten cars during the given period.

```sql
WITH Groups AS (
  SELECT ((ROW_NUMBER() OVER (ORDER BY C.CarId))-1)/10 + 1 AS GroupId, C.CarId
  FROM Cars C ),
SumDistances AS (
  SELECT G.GroupId, P.PointId,
    SUM(ST_Distance(trajectory(T.Trip), P.Geom)) AS SumDist
  FROM Groups G, Points P, Trips T
  WHERE T.CarId = G.CarId
  GROUP BY G.GroupId, P.PointId )
SELECT S1.GroupId, S1.PointId, S1.SumDist
FROM SumDistances S
WHERE S1.SumDist <= ALL (
  SELECT SumDist
  FROM SumDistances S
  WHERE S1.GroupId = S2.GroupId )
  ORDER BY S1.GroupId, S1.PointId;
```

This is an aggregate nearest-neighbor query. The temporary table `Groups` splits the cars in groups where the `GroupId` column takes the values from 1 to total number of groups. The temporary table `SumDistances` computes for each group G and point P the sum of the distances between a trip of a car in the group and the point. The main query then selects for each group in table `SumDistances` the points(s) that have the minimum aggregated distance.


# BerlinMOD/R Queries

1. What are the models of the vehicles with licence plate numbers from Licences?

```sql
SELECT DISTINCT L.Licence, C.Model AS Model
FROM Cars C, Licences L
WHERE C.Licence = L.Licence;
```

2. How many vehicles exist that are passenger cars?

```sql
SELECT COUNT (Licence)
FROM Cars C
WHERE Type = 'passenger';
```

----

# Summary


Time types Period, PeriodSet, and TimestampSet which, in addition of the the TimestampTz type provided by PostgreSQL, are used to represent time spans.
Temporal types tbool, tint, tfloat, and ttext which are based on the bool, int, float, and text types provided by PostgreSQL and are used to represent basic types that evolve on time.
Spatio-temporal types tgeompoint and tgeogpoint which are based on the geometry and geography types provided by PostGIS (restricted to 2D or 3D points) and are used to represent points that evolve on time. Range types intrange and floatrange which are used to represent ranges of int and float values.


-----

## Loading mobility data via SQL API

1. Create table https://carto.com/developers/sql-api/guides/creating-tables/

2. https://carto.com/developers/sql-api/guides/copy-queries/


```sql
TABLE Bus ( LineNo integer, TripNo integer, Trip tgeompoint(Sequence, Point, 3812) );
TABLE POI ( POINo integer, Name text, Geo GEOMETRY(3812) );
```

List the bus lines that traverse Place Louise

```sql
SELECT TripNo
FROM Bus B, (SELECT P.Geo FROM POI P WHERE P.Name = ‘Place Louise' LIMIT 1) T
WHERE intersects(B.Trip, T.Geo)
```

The intersects function is index supported, i.e., it is defined as follows

```sql
'SELECT $1 OPERATOR(@extschema@.&&) $2 AND @extschema@._intersects($1,$2)'
```

The && operator performs a bounding box overlaps index filtering

# Chapter 1. Managing Ship Trajectories (AIS)

AIS stands for Automatic Identification System. It is the location tracking system for sea vessels. This module illustrates how to load big AIS data sets into MobilityDB, and do basic exploration.

The idea of this module is inspired from the tutorial of MovingPandas on ship data analysis by Anita Graser.

**This Module Covers**

- Loading large trajectory datasets into MobilityDB
- Create proper indexes to speed up trajectory construction
- Select trajectories by a spatial window
- Join trajectories tables by proximity
- Select certain parts inside individual trajectories
- Manage the temporal speed and azimuth features of ships

## Data

The Danish Maritime Authority publishes about 3 TB of AIS routes here, in CSV format. The columns in the CSV are listed in Table 1.1, “AIS columns”

Table 1.1. AIS columns

```
Timestamp  Timestamp from the AIS base station, format: 31/12/2015 23:59:59
Type of mobile  Describes what type of target this message is received from (class A AIS Vessel, Class B AIS vessel, etc)
MMSI  MMSI number of vessel
Latitude  Latitude of message report (e.g. 57,8794)
Longitude  Longitude of message report (e.g. 17,9125)
Navigational status  Navigational status from AIS message if available, e.g.: 'Engaged in fishing', 'Under way using engine', mv.
ROT  Rot of turn from AIS message if available
SOG  Speed over ground from AIS message if available
COG  Course over ground from AIS message if available
Heading  Heading from AIS message if available
IMO  IMO number of the vessel
Callsign  Callsign of the vessel
Name  Name of the vessel
Ship type  Describes the AIS ship type of this vessel
Cargo type  Type of cargo from the AIS message
Width  Width of the vessel
Length  Lenght of the vessel
Type of position fixing device  Type of positional fixing device from the AIS message
Draught  Draugth field from AIS message
Destination  Destination from AIS message
ETA  Estimated Time of Arrival, if available
Data source type  Data source type, e.g. AIS
Size A  Length from GPS to the bow
Size B  Length from GPS to the stern
Size C  Length from GPS to starboard side
Size D  Length from GPS to port side
```
This module uses the data of one day April 1st 2018. The CSV file size is 1.9 GB, and it contains about 10 M rows.

**Tools used**

- MobilityDB, on top of PostgreSQL and PostGIS. Here I use the MobilityDB docker image.
- QGIS

## Preparing the Database

```sql
CREATE TABLE AISInput(
  T  timestamp,
  TypeOfMobile varchar(50),
  MMSI integer,
  Latitude float,
  Longitude float,
  navigationalStatus varchar(50),
  ROT float,
  SOG float,
  COG float,
  Heading integer,
  IMO varchar(50),
  Callsign varchar(50),
  Name varchar(100),
  ShipType varchar(50),
  CargoType varchar(100),
  Width float,
  Length float,
  TypeOfPositionFixingDevice varchar(50),
  Draught float,
  Destination varchar(50),
  ETA varchar(50),
  DataSourceType varchar(50),
  SizeA float,
  SizeB float,
  SizeC float,
  SizeD float,
  Geom geometry(Point, 4326)
);
```

## Loading the Data

For importing CSV data into a PostgreSQL database one can use the COPY command as follows:

```sql
COPY AISInput(T, TypeOfMobile, MMSI, Latitude, Longitude, NavigationalStatus,
  ROT, SOG, COG, Heading, IMO, CallSign, Name, ShipType, CargoType, Width, Length,
  TypeOfPositionFixingDevice, Draught, Destination, ETA, DataSourceType,
  SizeA, SizeB, SizeC, SizeD)
FROM '/home/mobilitydb/DanishAIS/aisdk_20180401.csv' DELIMITER  ',' CSV HEADER;
```

This import took about 3 minutes on my machine, which is an average laptop. The CSV file has 10,619,212 rows, all of which were correctly imported. For bigger datasets, one could alternative could use the program pgloader.

We clean up some of the fields in the table and create spatial points with the following command.

```sql
UPDATE AISInput SET
  NavigationalStatus = CASE NavigationalStatus WHEN 'Unknown value' THEN NULL END,
  IMO = CASE IMO WHEN 'Unknown' THEN NULL END,
  ShipType = CASE ShipType WHEN 'Undefined' THEN NULL END,
  TypeOfPositionFixingDevice = CASE TypeOfPositionFixingDevice
    WHEN 'Undefined' THEN NULL END,
  Geom = ST_SetSRID( ST_MakePoint( Longitude, Latitude ), 4326);
```

This took about 5 minutes on my machine. Let's visualize the spatial points on QGIS.

Clearly, there are noise points that are far away from Denmark or even outside earth. This module will not discuss a thorough data cleaning. However, we do some basic cleaning in order to be able to construct trajectories:

Filter out points that are outside the window defined by bounds point(-16.1,40.18) and point(32.88, 84.17). This window is obtained from the specifications of the projection in https://epsg.io/25832.

Filter out the rows that have the same identifier (MMSI, T)

```sql
CREATE TABLE AISInputFiltered AS
  SELECT DISTINCT ON(MMSI,T) *
  FROM AISInput
  WHERE Longitude BETWEEN -16.1 and 32.88 AND Latitude BETWEEN 40.18 AND 84.17;
-- Query returned successfully: 10357703 rows affected, 01:14 minutes execution time.
SELECT COUNT(*) FROM AISInputFiltered;
--10357703
```

### Constructing Trajectories

Now we are ready to construct ship trajectories out of their individual observations:

```sql
CREATE TABLE Ships(MMSI, Trip, SOG, COG) AS
  SELECT MMSI,
    tgeompointseq(array_agg(tgeompointinst( ST_Transform(Geom, 25832), T) ORDER BY T)),
    tfloatseq(array_agg(tfloatinst(SOG, T) ORDER BY T) FILTER (WHERE SOG IS NOT NULL)),
    tfloatseq(array_agg(tfloatinst(COG, T) ORDER BY T) FILTER (WHERE COG IS NOT NULL))
  FROM AISInputFiltered
  GROUP BY MMSI;
-- Query returned successfully: 2995 rows affected, 01:16 minutes execution time.
```

This query constructs, per ship, its spatiotemporal trajectory Trip, and two temporal attributes `SOG` and `COG`. `Trip` is a `temporal geometry point`, and both `SOG` and `COG` are `temporal floats`. MobilityDB builds on the coordinate transformation feature of PostGIS. Here the `SRID 25832` (European Terrestrial Reference System 1989) is used, because it i`s the one advised by Danish Maritime Authority in the download page of this dataset. Now, let's visualize the constructed trajectories in QGIS.


```sql
ALTER TABLE Ships ADD COLUMN Traj geometry;
UPDATE Ships SET Traj= trajectory(Trip);
-- Query returned successfully: 2995 rows affected, 3.8 secs execution time.
```

### Basic Data Exploration

The total distance traveled by all ships:

```sql
SELECT SUM( length( Trip ) ) FROM Ships;
--500433519.121321
```

This query uses the length function to compute per trip the sailing distance in meters. We then aggregate over all trips and calculate the sum. Let's have a more detailed look, and generate a histogram of trip lengths:

```sql
WITH buckets (bucketNo, RangeKM) AS (
  SELECT 1, floatrange '[0, 0]' UNION
  SELECT 2, floatrange '(0, 50)' UNION
  SELECT 3, floatrange '[50, 100)' UNION
  SELECT 4, floatrange '[100, 200)' UNION
  SELECT 5, floatrange '[200, 500)' UNION
  SELECT 6, floatrange '[500, 1500)' UNION
  SELECT 7, floatrange '[1500, 10000)' ),
histogram AS (
  SELECT bucketNo, RangeKM, count(MMSI) as freq
  FROM buckets left outer join Ships on (length(Trip)/1000) <@ RangeKM
  GROUP BY bucketNo, RangeKM
  ORDER BY bucketNo, RangeKM
)
SELECT bucketNo, RangeKM, freq,
  repeat('▪', ( freq::float / max(freq) OVER () * 30 )::int ) AS bar
FROM histogram;
--Total query runtime: 5.6 secs

bucketNo,   bucketRange,        freq     bar
1;          "[0,0]";            303;       ▪▪▪▪▪
2;          "(0,50)";           1693;      ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪
3;          "[50,100)";         267;       ▪▪▪▪▪
4;          "[100,200)";        276;       ▪▪▪▪▪
5;          "[200,500)";        361;       ▪▪▪▪▪▪
6;          "[500,1500)";       86;        ▪▪
7;          "[1500,10000)";     6;
```

Surprisingly there are trips with zero length. These are clearly noise that can be deleted. Also there are very many short trips, that are less than 50 km long. On the other hand, there are few long trips that are more than 1,500 km long. Let's visualize these last two cases in Figure 1.3, “Visualizing trips with abnormal lengths”. They look like noise. Normally one should validate more, but to simplify this module, we consider them as noise, and delete them.

```sql
DELETE FROM Ships
WHERE length(Trip) = 0 OR length(Trip) >= 1500000;
-- Query returned successfully in 7 secs 304 msec.
```

Let's have a look at the speed of the ships. There are two speed values in the data; the speed calculated from the spatiotemporal trajectory speed(Trip), and the SOG attribute. Optimally, the two will be the same. A small variance would still be OK, because of sensor errors. Note that both are temporal floats. In the next query, we compare the averages of the two speed values for every ship:

```sql
SELECT ABS(twavg(SOG) * 1.852 - twavg(speed(Trip))* 3.6 ) SpeedDifference
FROM Ships
ORDER BY SpeedDifference DESC;
--Total query runtime: 8.2 secs
--990 rows retrieved.

SpeedDifference
NULL
NULL
NULL
NULL
NULL
107.861100067879
57.1590253627668
42.4207839833568
39.5819188407125
33.6182789410313
30.9078594633161
26.514042447366
22.1312646226031
20.5389022294181
19.8500569368283
19.4134688682774
18.180139457754
17.4859077178001
17.3155991287105
17.1739822139821
12.9571603234404
12.6195380496344
12.2714437568609
10.9619033557275
10.4164745930929
10.3306155308426
9.46457823214455
...
```

The `twavg` computes a **time-weighted average of a temporal float**. It basically computes the area under the curve, then divides it by the time duration of the temporal float. By doing so, the speed values that remain for longer durations affect the average more than those that remain for shorter durations. Note that SOG is in knot, and Speed(Trip) is in m/s. The query converts both to km/h.

The query shows that 26 out of the 990 ship trajectories in the table have a difference of more than 10 km/h or NULL. These trajectories are shown in Figure 1.5, “Ship trajectories with big difference between speed(Trip) and SOG”. Again they look like noise, so we remove them.

Figure 1.5. Ship trajectories with big difference between speed(Trip) and SOG

![](https://docs.mobilitydb.com/MobilityDB/master/workshop/workshopimages/trajsWrongSpeed.png)

Now we do a similar comparison between the calculated azimuth from the spatiotemporal trajectory, and the attribute COG:

```sql
SELECT ABS(twavg(COG) - twavg(azimuth(Trip)) * 180.0/pi() ) AzimuthDifference
FROM Ships
ORDER BY AzimuthDifference DESC;
--Total query runtime: 4.0 secs
--964 rows retrieved.

264.838740787458
220.958372832234
180.867071483688
178.774337481463
154.239639388087
139.633953692907
137.347542674865
128.239459879571
121.107566199195
119.843262642657
116.685117326047
116.010477588934
109.830338231363
106.94301191915
106.890186229337
106.55297972109
103.20192549283
102.585009756697
...

```

Here we see that the COG is not as accurate as the SOG attribute. More than 100 trajectories have an azimuth difference bigger than 45 degrees. Figure 1.6, “Ship trajectories with big difference between `azimuth(Trip)` and COG” visualizes them. Some of them look like noise, but some look fine. For simplicity, we keep them all.

Figure 1.6. Ship trajectories with big difference between azimuth(Trip) and COG

![](https://docs.mobilitydb.com/MobilityDB/master/workshop/workshopimages/trajsWrongAzimuth.png)

### Analyzing the Trajectories

Now we dive into MobilityDB and explore more of its functions. In Figure 1.7, “A sample ship trajectory between Rødby and Puttgarden”, we notice trajectories that keep going between Rødby and Puttgarden. Most probably, these are the ferries between the two ports. The task is simply to spot which Ships do so, and to count how many one way trips they did in this day. This is expressed in the following query:

```sql
CREATE INDEX Ships_Trip_Idx ON Ships USING GiST(Trip);

EXPLAIN
WITH Ports(Rodby, Puttgarden) AS
(
 SELECT ST_MakeEnvelope(651135, 6058230, 651422, 6058548, 25832),
  ST_MakeEnvelope(644339, 6042108, 644896, 6042487, 25832)
)
SELECT S.*, Rodby, Puttgarden
FROM Ports P, Ships S
WHERE intersects(S.Trip, P.Rodby) AND intersects(S.Trip, P.Puttgarden)
--Total query runtime: 462 msec
--4 rows retrieved.
```

Figure 1.7. A sample ship trajectory between Rødby and Puttgarden

![](https://docs.mobilitydb.com/MobilityDB/master/workshop/workshopimages/trajFerry.png)

Figure 1.8. All ferries between Rødby and Puttgarden

![](https://docs.mobilitydb.com/MobilityDB/master/workshop/workshopimages/trajFerries.png)

This query creates two envelope geometries that represent the locations of the two ports, then intersects them with the spatiotemporal trajectories of the ships. The intersects function checks whether a temporal point has ever intersects a geometry. To speed up the query, a spatiotemporal GiST index is first built on the Trip attribute. The query identified four Ships that commuted between the two ports, Figure 1.8, “All ferries between Rødby and Puttgarden”. To count how many one way trips each of them did, we extend the previous query as follows:

```sql
WITH Ports(Rodby, Puttgarden) AS
(
  SELECT ST_MakeEnvelope(651135, 6058230, 651422, 6058548, 25832),
    ST_MakeEnvelope(644339, 6042108, 644896, 6042487, 25832)
)
SELECT MMSI, (numSequences(atGeometry(S.Trip, P.Rodby)) +
  numSequences(atGeometry(S.Trip, P.Puttgarden)))/2.0 AS NumTrips
FROM Ports P, Ships S
WHERE intersects(S.Trip, P.Rodby) AND intersects(S.Trip, P.Puttgarden)
--Total query runtime: 1.1 secs

MMSI NumTrips
219000429;  24.0
211188000;  24.0
211190000;  25.0
219000431;  16.0
```

The function atGeometry restricts the temporal point to the parts where it is inside the given geometry. The result is thus a temporal point that consists of multiple pieces (sequences), with temporal gaps in between. The function numSequences counts the number of these pieces.

With this high number of ferry trips, one wonders whether there are collision risks with ships that traverse this belt (the green trips in Figure 1.7, “A sample ship trajectory between Rødby and Puttgarden”). To check this, we query whether a pair of ship come very close to one another as follows:

```sql
WITH B(Belt) AS
(
  SELECT ST_MakeEnvelope(640730, 6058230, 654100, 6042487, 25832)
), BeltShips AS (
  SELECT MMSI, atGeometry(S.TripETRS, B.Belt) AS TripETRS,
    trajectory(atGeometry(S.TripETRS, B.Belt)) AS Traj
  FROM Ships S, B
  WHERE intersects(S.TripETRS, B.Belt)
)
SELECT S1.MMSI,
       S2.MMSI,
       S1.Traj,
       S2.Traj,
       shortestLine(S1.tripETRS, S2.tripETRS) Approach
FROM BeltShips S1,
     BeltShips S2
WHERE S1.MMSI > S2.MMSI AND
      dwithin(S1.tripETRS, S2.tripETRS, 300)

--Total query runtime: 28.5 secs
--7 rows retrieved.
```

The query first defines the area of interest as an envelope `ST_MakeEnvelope(640730, 6058230, 654100, 6042487, 25832)`, the red dashed line in Figure 1.9, “Ship that come closer than 300 meters to one another”).

It then *restricts/crops the trajectories to only this envelope* using the `atGeometry` function.

```sql
atGeometry(S.TripETRS, B.Belt)
-- where B.Belt is the AoI
```

 The **main query** then *find pairs of different trajectories* that ever came within a distance of `300 meters` `dwithin(S1.tripETRS, S2.tripETRS, 300)` to one another (the `dwithin`).

 For these trajectories, it computes the *spatial line that connects the two instants where the two trajectories were closest to one another* (the `shortestLine` function).

 ```sql
 shortestLine(S1.tripETRS, S2.tripETRS) Approach
 ```

 Figure 1.9, “Ship that come closer than 300 meters to one another” shows the green trajectories that came close to the blue trajectories, and their shortest connecting line in solid red. Most of the approaches occur at the entrance of the Rødby port, which looks normal. But we also see two interesting approaches, that may indicate danger of collision away from the port. They are shown with more zoom in Figure 1.10, “A zoom-in on a dangerous approach” and Figure 1.11, “Another dangerous approach”

Figure 1.9. Ship that come closer than 300 meters to one another

![](https://docs.mobilitydb.com/nightly/workshop/workshopimages/trajApproach.png)
![](https://docs.mobilitydb.com/nightly/workshop/workshopimages/approach1.png)
![](https://docs.mobilitydb.com/nightly/workshop/workshopimages/approach2.png)

# Chapter 2. Managing GTFS Data

The General Transit Feed Specification (GTFS) defines a common format for public transportation schedules and associated geographic information. GTFS-realtime is used to specify real-time transit data. Many transportation agencies around the world publish their data in GTFS and GTFS-realtime format and make them publicly available. A well-known repository containing such data is OpenMobilityData.

In this chapter, we illustrate how to load GTFS data in MobilityDB. For this, we first need to import the GTFS data into `PostgreSQL` and then transform this data so that it can be loaded into MobilityDB. The data used in this tutorial is obtained from [STIB-MIVB](https://www.stib-mivb.be/), the Brussels public transportation company and is available as a [ZIP](https://docs.mobilitydb.com/data/gtfs_data.zips) file. You must be aware that GTFS data is typically of big size. In order to reduce the size of the dataset, this file only contains schedules for one week and five transportation lines, whereas typical GTFS data published by STIB-MIVB contains schedules for one month and 99 transportation lines. In the reduced dataset used in this tutorial the final table containing the GTFS data in MobilityDB format has almost 10,000 trips and its size is 241 MB. Furtheremore, we need several temporary tables to transform GTFS format into MobilityDB and these tables are also big, the largest one has almost 6 million rows and its size is 621 MB.

Several tools can be used to import GTFS data into PostgreSQL. For example, one publicly available in Github can be found [here](https://github.com/fitnr/gtfs-sql-importer). These tools load GTFS data into PostgreSQL tables, allowing one to perform multiple imports of data provided by the same agency covering different time frames, perform various complex tasks including data validation, and take into account variations of the format provided by different agencies, updates of route information among multiple imports, etc. For the purpose of this tutorial we do a simple import and transformation using only SQL. This is enough for loading the data set we are using but a much more robust solution should be used in an operational environment, if only for coping with the considerable size of typical GTFS data, which would require parallelization of this task.


## Loading GTFS Data in PostgreSQL

The [ZIP](https://docs.mobilitydb.com/data/gtfs_data.zip) file with the data for this tutorial contains a set of CSV files (with extension .txt) as follows:

* agency.txt contains the description of the transportation agencies provinding the services (a single one in our case).

* calendar.txt contains service patterns that operate recurrently such as, for example, every weekday.

* calendar_dates.txt define exceptions to the default service patterns defined in calendar.txt. There are two types of exceptions: 1 means that the service has been added for the specified date, and 2 means that the service has been removed for the specified date.

* route_types.txt contains transportation types used on routes, such as bus, metro, tramway, etc.

* routes.txt contains transit routes. A route is a group of trips that are displayed to riders as a single service.

* shapes.txt contains the vehicle travel paths, which are used to generate the corresponding geometry.

* stop_times.txt contains times at which a vehicle arrives at and departs from stops for each trip.

* translations.txt contains the translation of the route information in French and Dutch. This file is not used in this tutorial.

* trips.txt contains trips for each route. A trip is a sequence of two or more stops that occur during a specific time period.

We decompress the file with the data into a directory. This can be done using the command.

`unzip gtfs_data.zip`

We suppose in the following that the directory used is as follows /home/gtfs_tutorial/.

We create the tables to be loaded with the data in the CSV files as follows.

```sql
CREATE TABLE agency (
  agency_id text DEFAULT '',
  agency_name text DEFAULT NULL,
  agency_url text DEFAULT NULL,
  agency_timezone text DEFAULT NULL,
  agency_lang text DEFAULT NULL,
  agency_phone text DEFAULT NULL,
  CONSTRAINT agency_pkey PRIMARY KEY (agency_id)
);

CREATE TABLE calendar (
  service_id text,
  monday int NOT NULL,
  tuesday int NOT NULL,
  wednesday int NOT NULL,
  thursday int NOT NULL,
  friday int NOT NULL,
  saturday int NOT NULL,
  sunday int NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  CONSTRAINT calendar_pkey PRIMARY KEY (service_id)
);
CREATE INDEX calendar_service_id ON calendar (service_id);

CREATE TABLE exception_types (
  exception_type int PRIMARY KEY,
  description text
);

CREATE TABLE calendar_dates (
  service_id text,
  date date NOT NULL,
  exception_type int REFERENCES exception_types(exception_type)
);
CREATE INDEX calendar_dates_dateidx ON calendar_dates (date);

```


```sql
CREATE TABLE route_types (
  route_type int PRIMARY KEY,
  description text
);

CREATE TABLE routes (
  route_id text,
  route_short_name text DEFAULT '',
  route_long_name text DEFAULT '',
  route_desc text DEFAULT '',
  route_type int REFERENCES route_types(route_type),
  route_url text,
  route_color text,
  route_text_color text,
  CONSTRAINT routes_pkey PRIMARY KEY (route_id)
);
```

```sql
CREATE TABLE shapes (
  shape_id text NOT NULL,
  shape_pt_lat double precision NOT NULL,
  shape_pt_lon double precision NOT NULL,
  shape_pt_sequence int NOT NULL
);
CREATE INDEX shapes_shape_key ON shapes (shape_id);
```

```sql
-- Create a table to store the shape geometries
CREATE TABLE shape_geoms (
  shape_id text NOT NULL,
  shape_geom geometry('LINESTRING', 4326),
  CONSTRAINT shape_geom_pkey PRIMARY KEY (shape_id)
);
CREATE INDEX shape_geoms_key ON shapes (shape_id);
```

```sql
CREATE TABLE location_types (
  location_type int PRIMARY KEY,
  description text
);

CREATE TABLE stops (
  stop_id text,
  stop_code text,
  stop_name text DEFAULT NULL,
  stop_desc text DEFAULT NULL,
  stop_lat double precision,
  stop_lon double precision,
  zone_id text,
  stop_url text,
  location_type integer  REFERENCES location_types(location_type),
  parent_station integer,
  stop_geom geometry('POINT', 4326),
  platform_code text DEFAULT NULL,
  CONSTRAINT stops_pkey PRIMARY KEY (stop_id)
);

CREATE TABLE pickup_dropoff_types (
  type_id int PRIMARY KEY,
  description text
);
```

```sql
CREATE TABLE stop_times (
  trip_id text NOT NULL,
  -- Check that casting to time interval works.
  arrival_time interval CHECK (arrival_time::interval = arrival_time::interval),
  departure_time interval CHECK (departure_time::interval = departure_time::interval),
  stop_id text,
  stop_sequence int NOT NULL,
  pickup_type int REFERENCES pickup_dropoff_types(type_id),
  drop_off_type int REFERENCES pickup_dropoff_types(type_id),
  CONSTRAINT stop_times_pkey PRIMARY KEY (trip_id, stop_sequence)
);
CREATE INDEX stop_times_key ON stop_times (trip_id, stop_id);
CREATE INDEX arr_time_index ON stop_times (arrival_time);
CREATE INDEX dep_time_index ON stop_times (departure_time);
```

```sql
CREATE TABLE trips (
  route_id text NOT NULL,
  service_id text NOT NULL,
  trip_id text NOT NULL,
  trip_headsign text,
  direction_id int,
  block_id text,
  shape_id text,
  CONSTRAINT trips_pkey PRIMARY KEY (trip_id)
);
CREATE INDEX trips_trip_id ON trips (trip_id);
```

```sql
INSERT INTO exception_types (exception_type, description) VALUES
  (1, 'service has been added'),
  (2, 'service has been removed');

INSERT INTO location_types(location_type, description) VALUES
  (0,'stop'),
  (1,'station'),
  (2,'station entrance');

INSERT INTO pickup_dropoff_types (type_id, description) VALUES
  (0,'Regularly Scheduled'),
  (1,'Not available'),
  (2,'Phone arrangement only'),
  (3,'Driver arrangement only');
```

We created one table for each CSV file. In addition, we created a table `shape_geoms` in order to assemble all segments composing a route into a single `geometry` and auxiliary tables `exception_types`, `location_types`, and `pickup_dropoff_types` containing acceptable values for some columns in the CSV files.

We can load the CSV files into the corresponding tables as follows.

```sql
COPY calendar(service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,
	start_date,end_date) FROM '/home/gtfs_tutorial/calendar.txt' DELIMITER ',' CSV HEADER;
COPY calendar_dates(service_id,date,exception_type)
	FROM '/home/gtfs_tutorial/calendar_dates.txt' DELIMITER ',' CSV HEADER;
COPY stop_times(trip_id,arrival_time,departure_time,stop_id,stop_sequence,
	pickup_type,drop_off_type) FROM '/home/gtfs_tutorial/stop_times.txt' DELIMITER ','
	CSV HEADER;
COPY trips(route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id)
	FROM '/home/gtfs_tutorial/trips.txt' DELIMITER ',' CSV HEADER;
COPY agency(agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone)
	FROM '/home/gtfs_tutorial/agency.txt' DELIMITER ',' CSV HEADER;
COPY route_types(route_type,description)
	FROM '/home/gtfs_tutorial/route_types.txt' DELIMITER ',' CSV HEADER;
COPY routes(route_id,route_short_name,route_long_name,route_desc,route_type,route_url,
	route_color,route_text_color) FROM '/home/gtfs_tutorial/routes.txt' DELIMITER ','
	CSV HEADER;
COPY shapes(shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence)
	FROM '/home/gtfs_tutorial/shapes.txt' DELIMITER ',' CSV HEADER;
COPY stops(stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,
	location_type,parent_station) FROM '/home/gtfs_tutorial/stops.txt' DELIMITER ','
	CSV HEADER;
```

Finally, we create the geometries for routes and stops as follows.

```sql
INSERT INTO shape_geoms
SELECT shape_id, ST_MakeLine(array_agg(
	ST_SetSRID(ST_MakePoint(shape_pt_lon, shape_pt_lat),4326) ORDER BY shape_pt_sequence))
FROM shapes
GROUP BY shape_id;

UPDATE stops
SET stop_geom = ST_SetSRID(ST_MakePoint(stop_lon, stop_lat),4326);
```

The visualization of the routes and stops in QGIS is given in Figure 2.1, “Visualization of the routes and stops for the GTFS data from Brussels.”. In the figure, red lines correspond to the trajectories of vehicles, while orange points correspond to the location of stops.

Figure 2.1. Visualization of the routes and stops for the GTFS data from Brussels.

![](https://docs.mobilitydb.com/MobilityDB/master/workshop/workshopimages/stib.png)

#  Transforming GTFS Data for MobilityDB

We start by creating a table that contains couples of `service_id` and `date` defining the dates at which a service is provided.

```sql
DROP TABLE IF EXISTS service_dates;
CREATE TABLE service_dates AS (
	SELECT service_id, date_trunc('day', d)::date AS date
	FROM calendar c, generate_series(start_date, end_date, '1 day'::interval) AS d
	WHERE (
		(monday = 1 AND extract(isodow FROM d) = 1) OR
		(tuesday = 1 AND extract(isodow FROM d) = 2) OR
		(wednesday = 1 AND extract(isodow FROM d) = 3) OR
		(thursday = 1 AND extract(isodow FROM d) = 4) OR
		(friday = 1 AND extract(isodow FROM d) = 5) OR
		(saturday = 1 AND extract(isodow FROM d) = 6) OR
		(sunday = 1 AND extract(isodow FROM d) = 7)
	)
	EXCEPT
	SELECT service_id, date
	FROM calendar_dates WHERE exception_type = 2
	UNION
	SELECT c.service_id, date
	FROM calendar c JOIN calendar_dates d ON c.service_id = d.service_id
	WHERE exception_type = 1 AND start_date <= date AND date <= end_date
);
```

This table transforms the service patterns in the calendar table valid between a `start_date` and an end_date taking into account the week days, and then remove the exceptions of type 2 and add the exceptions of type 1 that are specified in table `calendar_dates`.

We now create a table `trip_stops` that determines the stops for each trip.

```sql
DROP TABLE IF EXISTS trip_stops;
CREATE TABLE trip_stops
(
  trip_id text,
  stop_sequence integer,
  no_stops integer,
  route_id text,
  service_id text,
  shape_id text,
  stop_id text,
  arrival_time interval,
  perc float
);

INSERT INTO trip_stops (trip_id, stop_sequence, no_stops, route_id, service_id,
	shape_id, stop_id, arrival_time)
SELECT t.trip_id, stop_sequence, MAX(stop_sequence) OVER (PARTITION BY t.trip_id),
	route_id, service_id, shape_id, stop_id, arrival_time
FROM trips t JOIN stop_times s ON t.trip_id = s.trip_id;

UPDATE trip_stops t
SET perc = CASE
	WHEN stop_sequence =  1 then 0.0
	WHEN stop_sequence =  no_stops then 1.0
	ELSE ST_LineLocatePoint(g.the_geom, s.the_geom)
END
FROM shape_geoms g, stops s
WHERE t.shape_id = g.shape_id AND t.stop_id = s.stop_id;
```

We perform a join between `trips` and `stop_times` and determine the number of stops in a trip. Then, we compute the relative location of a stop within a trip using the function `ST_LineLocatePoint`.

We now create a table `trip_segs` that defines the segments between two consecutive stops of a trip.

```sql
DROP TABLE IF EXISTS trip_segs;
CREATE TABLE trip_segs (
	trip_id text,
	route_id text,
	service_id text,
	stop1_sequence integer,
	stop2_sequence integer,
	no_stops integer,
	shape_id text,
	stop1_arrival_time interval,
	stop2_arrival_time interval,
	perc1 float,
	perc2 float,
	seg_geom geometry,
	seg_length float,
	no_points integer,
	PRIMARY KEY (trip_id, stop1_sequence)
);

INSERT INTO trip_segs (trip_id, route_id, service_id, stop1_sequence, stop2_sequence,
	no_stops, shape_id, stop1_arrival_time, stop2_arrival_time, perc1, perc2)
WITH temp AS (
	SELECT trip_id, route_id, service_id, stop_sequence,
		LEAD(stop_sequence) OVER w AS stop_sequence2,
		MAX(stop_sequence) OVER (PARTITION BY trip_id),
		shape_id, arrival_time, LEAD(arrival_time) OVER w, perc, LEAD(perc) OVER w
	FROM trip_stops WINDOW w AS (PARTITION BY trip_id ORDER BY stop_sequence)
)
SELECT * FROM temp WHERE stop_sequence2 IS NOT null;

UPDATE trip_segs t
SET seg_geom = ST_LineSubstring(g.the_geom, perc1, perc2)
FROM shape_geoms g
WHERE t.shape_id = g.shape_id;

UPDATE trip_segs
SET seg_length = ST_Length(seg_geom), no_points = ST_NumPoints(seg_geom);
```

We use twice the LEAD window function for obtaning the next stop and the next percentage of a given stop and the MAX window function for obtaining the total number of stops in a trip. 

```sql
LEAD(stop_sequence) OVER w AS stop_sequence2,
MAX(stop_sequence) OVER (PARTITION BY trip_id),
```

Then, we generate the `geometry` of the segment betwen two stops using the function `ST_LineSubstring` and compute the length and the number of points in the segment with functions `ST_Length` and `ST_NumPoints`.

The geometry of a segment is a linestring containing multiple points. From the previous table we know at which time the trip arrived at the first point and at the last point of the segment. To determine at which time the trip arrived at the intermediate points of the segments, we create a table trip_points that contains all the points composing the geometry of a segment.


```sql
DROP TABLE IF EXISTS trip_points;
CREATE TABLE trip_points (
	trip_id text,
	route_id text,
	service_id text,
	stop1_sequence integer,
	point_sequence integer,
	point_geom geometry,
	point_arrival_time interval,
	PRIMARY KEY (trip_id, stop1_sequence, point_sequence)
);

INSERT INTO trip_points (trip_id, route_id, service_id, stop1_sequence,
	point_sequence, point_geom, point_arrival_time)
WITH temp1 AS (
	SELECT trip_id, route_id, service_id, stop1_sequence, stop2_sequence,
		no_stops, stop1_arrival_time, stop2_arrival_time, seg_length,
		(dp).path[1] AS point_sequence, no_points, (dp).geom as point_geom
	FROM trip_segs, ST_DumpPoints(seg_geom) AS dp
),
temp2 AS (
	SELECT trip_id, route_id, service_id, stop1_sequence, stop1_arrival_time,
		stop2_arrival_time, seg_length, point_sequence, no_points, point_geom
	FROM temp1
	WHERE point_sequence <> no_points OR stop2_sequence = no_stops
),
temp3 AS (
	SELECT trip_id, route_id, service_id, stop1_sequence, stop1_arrival_time,
		stop2_arrival_time, point_sequence, no_points, point_geom,
		ST_Length(ST_MakeLine(array_agg(point_geom) OVER w)) / seg_length AS perc
	FROM temp2 WINDOW w AS (PARTITION BY trip_id, service_id, stop1_sequence
		ORDER BY point_sequence)
)
SELECT trip_id, route_id, service_id, stop1_sequence, point_sequence, point_geom,
	CASE
	WHEN point_sequence = 1 then stop1_arrival_time
	WHEN point_sequence = no_points then stop2_arrival_time
	ELSE stop1_arrival_time + ((stop2_arrival_time - stop1_arrival_time) * perc)
	END AS point_arrival_time
FROM temp3;
```

In the temporary table `temp1` we use the function `ST_DumpPoints` to obtain the points composing the geometry of a segment. Nevertheless, this table contains *duplicate* points, that is, the last point of a segment is equal to the first point of the next one.

```sql
SELECT trip_id, route_id, service_id, stop1_sequence, stop2_sequence,
		no_stops, stop1_arrival_time, stop2_arrival_time, seg_length,
		(dp).path[1] AS point_sequence, no_points, (dp).geom as point_geom
	FROM trip_segs, ST_DumpPoints(seg_geom) AS dp
```

In the temporary table `temp2` we filter out the last point of a segment unless it is the last segment of the trip. 

```sql
SELECT trip_id, route_id, service_id, stop1_sequence, stop1_arrival_time,
		stop2_arrival_time, seg_length, point_sequence, no_points, point_geom
	FROM temp1
	WHERE point_sequence <> no_points OR stop2_sequence = no_stops
```

In the temporary table `temp3` we compute in the attribute `perc` the relative position of a point within a `trip` segment with window functions.

```sql
SELECT trip_id, route_id, service_id, stop1_sequence, stop1_arrival_time,
		stop2_arrival_time, point_sequence, no_points, point_geom,
		ST_Length(ST_MakeLine(array_agg(point_geom) OVER w)) / seg_length AS perc
	FROM temp2 WINDOW w AS (PARTITION BY trip_id, service_id, stop1_sequence
		ORDER BY point_sequence)
```

For this we use the function `ST_MakeLine` to construct the subsegment from the first point of the segment to the current one, determine the length of the subsegment with function `ST_Length` and divide this length by the overall *segment length*.

`ST_Length(ST_MakeLine(array_agg(point_geom) OVER w)) / seg_length AS perg c`

Finally, in the outer query we use the computed percentage to determine the arrival time to that point.

```sql
SELECT trip_id, route_id, service_id, stop1_sequence, point_sequence, point_geom,
	CASE
	WHEN point_sequence = 1 then stop1_arrival_time
	WHEN point_sequence = no_points then stop2_arrival_time
	ELSE stop1_arrival_time + ((stop2_arrival_time - stop1_arrival_time) * perc)
	END AS point_arrival_time
FROM temp3;
```

Our last temporary table `trips_input` contains the data in the format that can be used for creating the MobilityDB trips.

```sql
DROP TABLE IF EXISTS trips_input;
CREATE TABLE trips_input (
	trip_id text,
	route_id text,
	service_id text,
	date date,
	point_geom geometry,
	t timestamptz
);

INSERT INTO trips_input
SELECT trip_id, route_id, t.service_id, date, point_geom, date + point_arrival_time AS t
FROM trip_points t JOIN
	( SELECT service_id, MIN(date) AS date FROM service_dates GROUP BY service_id) s
	ON t.service_id = s.service_id;
```

In the inner query of the `INSERT` statement, we select the first date of a service in the `service_dates` table and then we join the resulting table with the `trip_points` table to compute the arrival time at each point composing the trips. Notice that we filter the first date of each trip for optimization purposes because in the next step below we use the shift function to compute the trips to all other dates. Alternatively, we could join the two tables but this will be considerably slower for big GTFS files.

