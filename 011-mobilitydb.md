
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
