pfaedle is a tool for converting locations from GTFS routes to match the road network.

```
mkdir -p osm gtfs
wget https://download.geofabrik.de/europe/germany/baden-wuerttemberg/freiburg-regbez-latest.osm.bz2 -O osm/freiburg-regbez-latest.osm.bz2
wget https://fritz.freiburg.de/csv_Downloads/VAGFR.zip -O gtfs/VAGFR.zip
pfaedle  -x osm/freiburg-regbez-latest.osm.bz2 gtfs/VAGFR.zip
```
