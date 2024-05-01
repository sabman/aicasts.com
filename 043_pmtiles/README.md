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

pmtiles tile https://build.protomaps.com/20240428.pmtiles 12 2048 2048 > tile.mvt
```