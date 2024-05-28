```
brew install pmtiles
```

## Usage

```bash
pmtiles --help
Usage: pmtiles <command>

Flags:
  -h, --help    Show context-sensitive help.

Commands:
  convert <input> <output>
    Convert an MBTiles or older spec version to PMTiles.

  show <path>
    Inspect a local or remote archive.

  tile <path> <z> <x> <y>
    Fetch one tile from a local or remote archive and output on stdout.

  extract <input> <output>
    Create an archive from a larger archive for a subset of zoom levels or geographic region.

  verify <input>
    Verify the correctness of an archive structure, without verifying individual tile contents.

  serve <path>
    Run an HTTP proxy server for Z/X/Y tiles.

  download --bucket=STRING <new-file>
    Upload a local archive to remote storage.

  upload --bucket=STRING <input> <key>
    Upload a local archive to remote storage.

  version
    Show the program version.

Run "pmtiles <command> --help" for more information on a command.

pmtiles show https://build.protomaps.com/20240428.pmtiles

pmtiles extract https://build.protomaps.com/20240501.pmtiles my_area.pmtiles --bbox=4.742883,51.830755,5.552837,52.256198
```

https://docs.protomaps.com/pmtiles/

PMTiles is a single-file archive format for pyramids of tiled data. A PMTiles archive can be hosted on a storage platform like S3, and enables low-cost, zero-maintenance map applications.

- PMTiles is a general format for tiled data addressed by Z/X/Y coordinates. This can be cartographic basemap vector tiles, remote sensing observations, JPEG images, or more.

- PMTiles readers use HTTP Range Requests to fetch only the relevant tile or metadata inside a PMTiles archive on-demand.

- The arrangement of tiles and directories is designed to minimize the amount of overhead requests when panning and zooming.

The current specification version of PMTiles is version 3, which you can read on GitHub.

```sh
# PostgreSQL/PostGIS => GeoJSON => PMtiles
source .env

ogr2ogr -progress -f "GeoJSON" doha_buildings.geojson PG:"user=supabase_admin password=$DBPASS host=$DBHOST port=6443 dbname=postgres" doha_buildings

tippecanoe --minimum-zoom=6 --maximum-zoom=21 --projection=EPSG:4326 -o doha_buildings.pmtiles -l doha_buildings doha_buildings.geojson --force
```
