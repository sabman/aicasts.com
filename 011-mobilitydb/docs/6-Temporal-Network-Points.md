# Chapter 6. Temporal Network Points

The temporal points that we have considered so far represent the movement of objects that can move freely on space since it is assumed that they can change their position from one location to the next one without any motion restriction. This is the case for animals and for flying objects such as planes or drones. However, in many cases, objects do not move freely in space but rather within spatially embedded networks such as routes or railways. In this case, it is necessary to take the embedded networks into account while describing the movements of these moving objects. Temporal network points account for these requirements.

Compared with the free-space temporal points, network-based points have the following advantages:

- Network points provide road constraints that reflect the real movements of moving objects.

- The geometric information is not stored with the moving point, but once and for all in the fixed networks. In this way, the location representations and interpolations are more precise.

- Network points are more efficient in terms of data storage, location update, formulation of query, as well as indexing. These are discussed later in this document.

Temporal network points are based on `pgRouting`, a PostgreSQL extension for developing network routing applications and doing graph analysis. Therefore, temporal network points assume that the underlying network is defined in a table named ways, which has at least three columns: gid containing the unique route identifier, length containing the route length, and `the_geom` containing the route geometry.

There are two static network types, `npoint` (short for network point) and `nsegment` (short for network segment), which represent, respectively, a point and a segment of a route. An `npoint` value is composed of a route identifier and a float number in the range [0,1] determining a relative position of the route, where 0 corresponds to the beginning of the route and 1 to the end of the route. An `nsegment` value is composed of a route identifier and two float numbers in the range [0,1] determining the start and end relative positions. A `nsegment` value whose start and end positions are equal corresponds to an `npoint` value.

The `npoint` type serves as base type for defining the temporal network point type `tnpoint`. The tnpoint type has similar functionality as the temporal point type `tgeompoint` with the exception that it only considers two dimensions. Thus, all functions and operators described before for the `tgeompoint` type are also applicable for the `tnpoint` type. In addition, there are specific functions defined for the `tnpoint` type.

## 6.1. Static Network Types

An `npoint` value is a couple of the form `(rid,position)` where `rid` is a `bigint` value representing a route identifier and `position` is a `float` value in the range `[0,1]` indicating its relative position. The values 0 and 1 of position denote, respectively, the starting and the ending position of the route. The road distance between an `npoint` value and the starting position of route with identifier `rid` is computed by multiplying position by length, where length is the route length. Examples of input of network point values are as follows:

```sql
SELECT npoint 'Npoint(76, 0.3)';
SELECT npoint 'Npoint(64, 1.0)';
```

The constructor function for network points has one argument for the route identifier and one argument for the relative position. An example of a network point value defined with the constructor function is as follows:

```sql
SELECT npoint(76, 0.3);
```

An `nsegment` value is a triple of the form `(rid,startPosition,endPosition)` where rid is a bigint value representing a route identifier and `startPosition` and `endPosition` are float values in the range `[0,1]` such that `startPosition ≤ endPosition`. Semantically, a network segment represents a set of network points `(rid,position)` with `startPosition ≤ position ≤ endPosition`. If `startPosition=0` and `endPosition=1`, the network segment is equivalent to the entire route. If `startPosition=endPosition`, the network segment represents into a single network point. Examples of input of network point values are as follows:

```sql
SELECT nsegment 'Nsegment(76, 0.3, 0.5)';
SELECT nsegment 'Nsegment(64, 0.5, 0.5)';
SELECT nsegment 'Nsegment(64, 0.0, 1.0)';
SELECT nsegment 'Nsegment(64, 1.0, 0.0)';
-- converted to nsegment 'Nsegment(64, 0.0, 1.0)';
```

As can be seen in the last example, the `startPosition` and `endPosition` values will be inverted to ensure that the condition `startPosition ≤ endPosition` is always satisfied. The constructor function for network segments has one argument for the route identifier and two optional arguments for the start and end positions. Examples of network segment values defined with the constructor function are as follows:

```sql
SELECT nsegment(76, 0.3, 0.3);
SELECT nsegment(76); -- start and end position assumed to be 0 and 1 respectively
SELECT nsegment(76, 0.5); -- end position assumed to be 1
```

Values of the `npoint` type can be converted to the `nsegment` type using an explicit CAST or using the `::` notation as shown next.

```sql
SELECT npoint(76, 0.33)::nsegment;
```

Values of static network types must satisfy several constraints so that they are well defined. These constraints are given next.

- The route identifier `rid` must be found in column `gid` of table ways.

- The `position, startPosition`, and `endPosition` values must be in the range [0,1]. An error is raised whenever one of these constraints are not satisfied.

Examples of incorrect static network type values are as follows.

```sql
-- incorrect rid value
SELECT npoint 'Npoint(87.5, 1.0)';
-- incorrect position value
SELECT npoint 'Npoint(87, 2.0)';
-- rid value not found in the ways table
SELECT npoint 'Npoint(99999999, 1.0)';
```

We give next the functions and operators for the static network types.

### 6.1.1. Constructor Functions

Constructor for network points

```sql
npoint(bigint,double precision): npoint

SELECT npoint(76, 0.3);
```

Constructor for network segments

```sql
nsegment(bigint,double precision,double precision): nsegment

SELECT nsegment(76, 0.3, 0.5);
```

### 6.1.2. Modification Functions

Set the precision of the position(s) of the network point or the network segment to the number of decimal places

`setPrecision({npoint,nsegment},integer): {npoint,nsegment}`

```sql
SELECT setPrecision(npoint(76, 0.33333), 2);
```

### 6.1.3. Accessor Functions

- Get the route identifier

`route({npoint,nsegment}): bigint`

```sql
SELECT route(npoint 'Npoint(63, 0.3)');
-- 63
SELECT route(nsegment 'Nsegment(76, 0.3, 0.3)');
-- 76
```

### 6.1.4. Spatial Functions

```
srid({npoint,nsegment}): int
```

```sql
SELECT SRID(nspoint 'Npoint(76, 0.3)');
-- 5676
SELECT SRID(nsegment 'Nsegment(76, 0.3, 0.5)');
-- 5676
```

Values of the `npoint` and `nsegment` types can be converted to the `geometry` type using an explicit `CAST` or using the `::` notation as shown next.

- Cast a network point to a geometry

`{npoint,nsegment}::geometry`

```sql
SELECT ST_AsText(npoint(76, 0.33)::geometry);
-- POINT(21.6338731332283 50.0545869554067)
SELECT ST_AsText(nsegment(76, 0.33, 0.66)::geometry);
-- LINESTRING(21.6338731332283 50.0545869554067,30.7475989651999 53.9185062927473)
SELECT ST_AsText(nsegment(76, 0.33, 0.33)::geometry);
-- POINT(21.6338731332283 50.0545869554067)
```

Similarly, geometry values of subtype `point` or `linestring` (restricted to two points) can be converted, respectively, to `npoint` and `nsegment` values using an explicit `CAST` or using the `::` notation. For this, the route that intersects the given points must be found, where a tolerance of 0.00001 units (depending on the coordinate system) is assumed so a point and a route that are close are considered to intersect. If no such route is found, a null value is returned.

Values of the npoint and nsegment types can be converted to the geometry type using an explicit CAST or using the :: notation as shown next.

Cast a network point to a geometry

`{npoint,nsegment}::geometry`

### 6.1.5. Comparison Operators

The comparison operators (=, <, and so on) for static network types require that the left and right arguments be of the same type. Excepted the equality and inequality, the other comparison operators are not useful in the real world but allow B-tree indexes to be constructed on static network types.

- Are the values equal?
  `{npoint,nsegment} = {npoint,nsegment}`

```sql
SELECT npoint 'Npoint(3, 0.5)' = npoint 'Npoint(3, 0.5)';
-- true
SELECT nsegment 'Nsegment(3, 0.5, 0.5)' = nsegment 'Nsegment(3, 0.5, 0.6)';
-- false
```

- Are the values different?

`{npoint,nsegment} <> {npoint,nsegment}`

```sql
SELECT npoint 'Npoint(3, 0.5)' <> npoint 'Npoint(3, 0.6);
-- true
SELECT nsegment 'Nsegment(3, 0.5, 0.5)' <> nsegment 'Nsegment(3, 0.5, 0.5)';
-- false
```

- Is the left value less than the right value?

`{npoint,nsegment} < {npoint,nsegment}`

```sql
SELECT npoint 'Npoint(3, 0.5)' < npoint 'Npoint(3, 0.6)';
-- true
SELECT nsegment 'Nsegment(3, 0.5, 0.5)' < nsegment 'Nsegment(3, 0.5, 0.6)';
-- true
```

- Is the left value less than or equal to the right value?

`{npoint,nsegment} <= {npoint,nsegment}`

```sql
SELECT npoint 'Npoint(3, 0.5)' <= npoint 'Npoint(3, 0.6)';
-- true
SELECT nsegment 'Nsegment(3, 0.5, 0.5)' <= nsegment 'Nsegment(3, 0.5, 0.6)';
```

- Is the left value greater than the right value?

`{npoint,nsegment} > {npoint,nsegment}`

```sql
SELECT npoint 'Npoint(3, 0.5)' > npoint 'Npoint(3, 0.6)';
-- false
SELECT nsegment 'Nsegment(3, 0.5, 0.5)' > nsegment 'Nsegment(3, 0.5, 0.6)';
-- false
```

## 6.2. Temporal Network Points

The temporal network point type `tnpoint` allows to represent the movement of objects over a network. It corresponds to the temporal point type `tgeompoint` restricted to two-dimensional coordinates. As all the other temporal types it comes in four subtypes, namely, instant, instant set, sequence, and sequence set. Examples of tnpoint values in these subtypes are given next.

```sql
SELECT tnpoint 'Npoint(1, 0.5)@2000-01-01';
SELECT tnpoint '{Npoint(1, 0.3)@2000-01-01, Npoint(1, 0.5)@2000-01-02,
  Npoint(1, 0.5)@2000-01-03}';
SELECT tnpoint '[Npoint(1, 0.2)@2000-01-01, Npoint(1, 0.4)@2000-01-02,
  Npoint(1, 0.5)@2000-01-03]';
SELECT tnpoint '{[Npoint(1, 0.2)@2000-01-01, Npoint(1, 0.4)@2000-01-02,
  Npoint(1, 0.5)@2000-01-03], [Npoint(2, 0.6)@2000-01-04, Npoint(2, 0.6)@2000-01-05]}';
```
The temporal network point type accepts type modifiers (or typmod in PostgreSQL terminology). The possible values for the type modifier are Instant, InstantSet, Sequence, and SequenceSet. If no type modifier is specified for a column, values of any subtype are allowed.

```sql
SELECT tnpoint(Sequence) '[Npoint(1, 0.2)@2000-01-01, Npoint(1, 0.4)@2000-01-02,
  Npoint(1, 0.5)@2000-01-03]';
SELECT tnpoint(Sequence) 'Npoint(1, 0.2)@2000-01-01';
-- ERROR: Temporal type (Instant) does not match column type (Sequence)
```

the network point changes its route at 2001-01-03.

Temporal network point values of sequence or sequence set subtype are converted into a normal form so that equivalent values have identical representations. For this, consecutive instant values are merged when possible. Three consecutive instant values can be merged into two if the linear functions defining the evolution of values are the same. Examples of transformation into a normal form are as follows.

```sql
SELECT tnpoint '[NPoint(1, 0.2)@2001-01-01, NPoint(1, 0.4)@2001-01-02,
  NPoint(1, 0.6)@2001-01-03)';
-- [NPoint(1,0.2)@2001-01-01, NPoint(1,0.6)@2001-01-03)
SELECT tnpoint '{[NPoint(1, 0.2)@2001-01-01, NPoint(1, 0.3)@2001-01-02,
  NPoint(1, 0.5)@2001-01-03), [NPoint(1, 0.5)@2001-01-03, NPoint(1, 0.7)@2001-01-04)}';
-- {[NPoint(1,0.2)@2001-01-01, NPoint(1,0.3)@2001-01-02, NPoint(1,0.7)@2001-01-04)}
```

## 6.3. Validity of Temporal Network Points
Temporal network point values must satisfy the constraints specified in Section 3.2 so that they are well defined. An error is raised whenever one of these constraints are not satisfied. Examples of incorrect values are as follows.

```
-- null values are not allowed
SELECT tnpoint 'NULL@2001-01-01 08:05:00';
SELECT tnpoint 'Point(0 0)@NULL';
-- base type is not a network point
SELECT tnpoint 'Point(0 0)@2001-01-01 08:05:00';
-- multiple routes in a sequence
SELECT tnpoint '[Npoint(1, 0.2)@2001-01-01 09:00:00, Npoint(2, 0.2)@2001-01-01 09:05:00)';
```

## 6.4. Constructors for Temporal Network Points

- Constructor for temporal network points of instant subtype

`tnpoint_inst(val npoint,t timestamptz):tnpoint_inst`

```sql
SELECT tnpoint_inst('Npoint(1, 0.5)', '2000-01-01');
-- NPoint(1,0.5)@2000-01-01
```

- Constructors for temporal network points of instant set subtype

`tnpoint_instset(tnpoint[]):tnpoint_instset`

`tnpoint_instset(npoint,timestampset):tnpoint_instset`

```sql
SELECT tnpoint_instset(ARRAY[tnpoint 'Npoint(1, 0.3)@2000-01-01',
  'Npoint(1, 0.5)@2000-01-02', 'Npoint(1, 0.5)@2000-01-03']);
-- {NPoint(1,0.3)@2000-01-01, NPoint(1,0.5)@2000-01-02, NPoint(1,0.5)@2000-01-03}
SELECT tnpoint_instset('Npoint(1, 0.3)', '{2000-01-01, 2000-01-03, 2000-01-05}');
-- {NPoint(1,0.3)@2000-01-01, NPoint(1,0.3)@2000-01-03, NPoint(1,0.3)@2000-01-05}
```

- Constructor for temporal network points of sequence subtype

```c
tnpoint_seq(
  tnpoint[],
  lower_inc boolean=true,
  upper_inc boolean=true, 
  linear boolean=true
):tnpoint_seq

tnpoint_seq(
  npoint,
  period,
  linear boolean=true
):tnpoint_seq
```

```sql
SELECT tnpoint_seq(ARRAY[tnpoint 'Npoint(1, 0.2)@2000-01-01', 'Npoint(1, 0.4)@2000-01-02',
  'Npoint(1, 0.5)@2000-01-03']);
-- [NPoint(1,0.2)@2000-01-01, NPoint(1,0.4)@2000-01-02, NPoint(1,0.5)@2000-01-03]
SELECT tnpoint_seq(npoint 'Npoint(1, 0.2)', '[2000-01-01, 2000-01-03]', false);
-- Interp=Stepwise;[NPoint(1,0.2)@2000-01-01, NPoint(1,0.2)@2000-01-03]
```

- Constructor for temporal network points of sequence set subtype

```c
tnpoint_seqset(tnpoint[]):tnpoint_seqset

tnpoint_seqset(npoint,periodset,boolean=true):tnpoint_seqset
```

```sql
SELECT tnpoint_seqset(ARRAY[tnpoint '[Npoint(1, 0.2)@2000-01-01, Npoint(1, 0.4)@2000-01-02,
  Npoint(1, 0.5)@2000-01-03]', '[Npoint(2, 0.6)@2000-01-04, Npoint(2, 0.6)@2000-01-05]']);
-- {[NPoint(1,0.2)@2000-01-01, NPoint(1,0.4)@2000-01-02, NPoint(1,0.5)@2000-01-03],
  [NPoint(2,0.6)@2000-01-04, NPoint(2,0.6)@2000-01-05]}
```

## 6.5. Casting for Temporal Network Points

A temporal network point value can be converted to and from a temporal geometry point. This can be done using an explicit `CAST` or using the `::` notation. A null value is returned if any of the composing geometry point values cannot be converted into a npoint value.

- Cast a temporal network point to a temporal geometry point

`tnpoint::tgeompoint`

```sql
SELECT astext((tnpoint '[NPoint(1, 0.2)@2001-01-01,
  NPoint(1, 0.3)@2001-01-02)')::tgeompoint);
-- [POINT(23.057077727326 28.7666335767956)@2001-01-01,
  POINT(48.7117553116406 20.9256801894708)@2001-01-02)
```

- Cast a temporal geometry point to a temporal network point


`tgeompoint::tnpoint`
  
```sql
SELECT tgeompoint '[POINT(23.057077727326 28.7666335767956)@2001-01-01,
  POINT(48.7117553116406 20.9256801894708)@2001-01-02)'::tnpoint
-- [NPoint(1,0.2)@2001-01-01, NPoint(1,0.3)@2001-01-02)
SELECT tgeompoint '[POINT(23.057077727326 28.7666335767956)@2001-01-01,
  POINT(48.7117553116406 20.9)@2001-01-02)'::tnpoint
-- NULL
```

We give next the functions and operators for network point types.

## 6.6. Functions and Operators for Temporal Network Points
All functions for temporal types described in Chapter 5 can be applied for temporal network point types. Therefore, in the signatures of the functions, the notation `base` also represents an npoint and the notations `ttype`, `tpoint`, and `tgeompoint` also represent a `tnpoint`. Furthermore, the functions that have an argument of type `geometry` accept in addition an argument of type `npoint`. To avoid redundancy, we only present next some examples of these functions and operators for temporal network points.

Transform a temporal network point to another subtype

`tnpoint_inst(tnpoint): tnpoint_inst`

`tnpoint_instset(tnpoint): tnpoint_instset`

`tnpoint_seq(tnpoint): tnpoint_seq`

`tnpoint_seqset(tnpoint): tnpoint_seqset`

```sql
SELECT tnpoint_seqset(tnpoint 'NPoint(1, 0.5)@2001-01-01');
-- {[NPoint(1,0.5)@2001-01-01]}
```

- Set the precision of the fraction of the temporal network point to the number of decimal places

`setPrecision(tnpoint,integer): tnpoint`

```sql
SELECT setPrecision(tnpoint '{[NPoint(1, 0.123456789)@2012-01-01, NPoint(1, 0.5)@2012-01-02)}', 6);
-- {[NPoint(1,0.123457)@2012-01-01 00:00:00+01, NPoint(1,0.5)@2012-01-02 00:00:00+01)}
```

- Get the values

`getValues(tnpoint): npoint[]`
  
  ```sql
SELECT getValues(tnpoint '{[NPoint(1, 0.3)@2012-01-01, NPoint(1, 0.5)@2012-01-02)}');
-- {"NPoint(1,0.3)","NPoint(1,0.5)"}
SELECT getValues(tnpoint '{[NPoint(1, 0.3)@2012-01-01, NPoint(1, 0.3)@2012-01-02)}');
-- {"NPoint(1,0.3)"}
```

- Get the value at a timestamp

`valueAtTimestamp(tnpoint,timestamptz): npoint`

```sql
SELECT valueAtTimestamp(tnpoint '[NPoint(1, 0.3)@2012-01-01, NPoint(1, 0.5)@2012-01-03)',
  '2012-01-02');
-- NPoint(1,0.4)
```


- Get the length traversed by the temporal network point

`length(tnpoint): float``

```sql
SELECT length(tnpoint '[NPoint(1, 0.3)@2000-01-01, NPoint(1, 0.5)@2000-01-02]');
-- 54.3757408468784
```

- Get the cumulative length traversed by the temporal network point

`length(tnpoint): float`

```sql
SELECT length(tnpoint '[NPoint(1, 0.3)@2000-01-01, NPoint(1, 0.5)@2000-01-02]');
-- 54.3757408468784
```


- Get the speed of the temporal network point in units per second

`speed({tnpoint_seq, tpoint_seqset}): tfloat_seqset`

```sql
SELECT speed(tnpoint '[NPoint(1, 0.1)@2000-01-01, NPoint(1, 0.4)@2000-01-02,
  NPoint(1, 0.6)@2000-01-03]') * 3600 * 24;
-- Interp=Stepwise;[21.4016800272077@2000-01-01, 14.2677866848051@2000-01-02,
  14.2677866848051@2000-01-03]
```

- Construct the bounding box from a npoint and, optionally, a timestamp or a period

`stbox(npoint): stbox`

`stbox(npoint,{timestamptz,period}): stbox`

```sql
SELECT stbox(npoint 'NPoint(1,0.3)');
-- STBOX((48.711754,20.92568),(48.711758,20.925682))
SELECT stbox(npoint 'NPoint(1,0.3)', timestamptz '2000-01-01');
-- STBOX T((62.786633,80.143555,2000-01-01),(62.786636,80.143562,2000-01-01))
SELECT stbox(npoint 'NPoint(1,0.3)', period '[2000-01-01,2000-01-02]');
-- STBOX T((62.786633,80.143555,2000-01-01),(62.786636,80.143562,2000-01-02))
```

- Get the time-weighted centroid

`twCentroid(tnpoint): geometry(Point)`

```sql
SELECT st_astext(twCentroid(tnpoint '{[NPoint(1, 0.3)@2012-01-01,
  NPoint(1, 0.5)@2012-01-02, NPoint(1, 0.5)@2012-01-03, NPoint(1, 0.7)@2012-01-04)}'));
-- POINT(79.9787466444847 46.2385558051041)
```

- Get the temporal azimuth

`azimuth(tnpoint): tfloat`

```sql
SELECT azimuth(tnpoint '[NPoint(2, 0.3)@2012-01-01, NPoint(2, 0.7)@2012-01-02]');
-- {[0.974681063778863@2012-01-01 00:00:00+01,
  0.974681063778863@2012-01-01 23:54:36.721091+01),
  [3.68970843029227@2012-01-01 23:54:36.721091+01,
  3.68970843029227@2012-01-02 00:00:00+01)}
```

Since the underlying geometry associated to a route may have several vertices, the azimuth value may change between instants of the input temporal network point, as shown in the example above.

- Get the instant of the first temporal network point at which the two arguments are at the nearest distance

`nearestApproachInstant({geo,npoint,tpoint},{geo,npoint,tpoint}): tpoint`

```sql
SELECT nearestApproachInstant(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', geometry 'Linestring(50 50,55 55)');
-- NPoint(2,0.349928)@2012-01-01 02:59:44.402905+01
SELECT nearestApproachInstant(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', npoint 'NPoint(1, 0.5)');
-- NPoint(2,0.592181)@2012-01-01 17:31:51.080405+01
```

- Get the smallest distance ever between the two arguments

`nearestApproachDistance({geo,npoint,tpoint},{geo,npoint,tpoint}): float``

```sql
SELECT nearestApproachDistance(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', geometry 'Linestring(50 50,55 55)');
-- 1.41793220500979
SELECT nearestApproachDistance(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', npoint 'NPoint(1, 0.5)');
-- NPoint(2,0.592181)@2012-01-01 17:31:51.080405+01
```

Function `nearestApproachDistance` has an associated operator `|=|` that can be used for doing nearest neightbor searches using a `GiST` index (see Section 5.17. Indexing of Temporal Types).


- Get the line connecting the nearest approach point between the two arguments

`shortestLine({geo,npoint,tpoint},{geo,npoint,tpoint}): geometry`

The function will only return the first line that it finds if there are more than one

```sql
SELECT st_astext(shortestLine(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', geometry 'Linestring(50 50,55 55)'));
-- LINESTRING(50.7960725266492 48.8266286733015,50 50)
SELECT st_astext(shortestLine(tnpoint '[NPoint(2, 0.3)@2012-01-01,
  NPoint(2, 0.7)@2012-01-02]', npoint 'NPoint(1, 0.5)'));
-- LINESTRING(77.0902838115125 66.6659083092593,90.8134936900394 46.4385792121146)
```

Function `shortestLine` can be used to obtain the result provided by the PostGIS function `ST_CPAWithin` when both arguments are trajectories as shown next.

- Restrict to a value

`atValue(tnpoint,base): tnpoint`

```sql
SELECT atValue(tnpoint '[NPoint(2, 0.3)@2012-01-01, NPoint(2, 0.7)@2012-01-03]',
  'NPoint(2, 0.5)');
-- {[NPoint(2,0.5)@2012-01-02]}
```

- Restrict to a geometry

`atGeometry(tnpoint,geometry): tnpoint`

```sql
SELECT atGeometry(tnpoint '[NPoint(2, 0.3)@2012-01-01, NPoint(2, 0.7)@2012-01-03]',
  'Polygon((40 40,40 50,50 50,50 40,40 40))');
```

- Difference with a value

`minusValue(tnpoint,base): tnpoint``

```sql
SELECT minusValue(tnpoint '[NPoint(2, 0.3)@2012-01-01, NPoint(2, 0.7)@2012-01-03]',
  'NPoint(2, 0.5)');
-- {[NPoint(2,0.3)@2012-01-01, NPoint(2,0.5)@2012-01-02),
  (NPoint(2,0.5)@2012-01-02, NPoint(2,0.7)@2012-01-03]}
```

- Difference with a geometry

`minusGeometry(tnpoint,geometry): tnpoint`

```sql
SELECT minusGeometry(tnpoint 
  '[NPoint(2, 0.3)@2012-01-01, NPoint(2, 0.7)@2012-01-03]', 
  'Polygon((40 40,40 50,50 50,50 40,40 40))'
);
-- {(NPoint(2,0.342593)@2012-01-01 05:06:40.364673+01, NPoint(2,0.7)@2012-01-03 00:00:00+01]}
```

- Traditional comparison operators

```
tnpoint = tnpoint: boolean

tnpoint <> tnpoint: boolean

tnpoint < tnpoint: boolean

tnpoint > tnpoint: boolean

tnpoint <= tnpoint: boolean

tnpoint >= tnpoint: boolean
```

```sql
SELECT tnpoint '{[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.3)@2001-01-02),
  [NPoint(1, 0.3)@2001-01-02, NPoint(1, 0.5)@2001-01-03]}' =
  tnpoint '[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.5)@2001-01-03]';
-- true
SELECT tnpoint '{[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.5)@2001-01-03]}' <>
  tnpoint '[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.5)@2001-01-03]';
-- false
SELECT tnpoint '[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.5)@2001-01-03]' <
  tnpoint '[NPoint(1, 0.1)@2001-01-01, NPoint(1, 0.6)@2001-01-03]';
-- true
```

- Temporal comparison operators

```
tnpoint #= tnpoint: tbool
tnpoint #<> tnpoint: tbool
```

```sql
SELECT tnpoint '[NPoint(1, 0.2)@2012-01-01, NPoint(1, 0.4)@2012-01-03)' #=
  npoint 'NPoint(1, 0.3)';
-- {[f@2012-01-01, t@2012-01-02], (f@2012-01-02, f@2012-01-03)}
SELECT tnpoint '[NPoint(1, 0.2)@2012-01-01, NPoint(1, 0.8)@2012-01-03)' #<>
  tnpoint '[NPoint(1, 0.3)@2012-01-01, NPoint(1, 0.7)@2012-01-03)';
-- {[t@2012-01-01, f@2012-01-02], (t@2012-01-02, t@2012-01-03)}
```

- Ever and always equal operators

```
tnpoint ?= tnpoint: boolean

tnpoint &= tnpoint: boolean
```

```sql
SELECT tnpoint '[Npoint(1, 0.2)@2012-01-01, Npoint(1, 0.4)@2012-01-04)' ?= Npoint(1, 0.3);
-- true
SELECT tnpoint '[Npoint(1, 0.2)@2012-01-01, Npoint(1, 0.2)@2012-01-04)' &= Npoint(1, 0.2);
-- true
```
