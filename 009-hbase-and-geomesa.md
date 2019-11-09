install http://www.apache.org/dyn/closer.cgi/hbase/

```
brew install hbase

brew info hbase

hbase: stable 1.3.5 (bottled)
Hadoop database: a distributed, scalable, big data store
https://hbase.apache.org
Not installed
From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/hbase.rb
==> Dependencies
Build: ant ✘
Required: lzo ✔
==> Requirements
Required: x86_64 architecture ✔, java = 1.8 ✔
==> Caveats
To have launchd start hbase now and restart at login:
  brew services start hbase
Or, if you don't want/need a background service you can just run:
  /usr/local/opt/hbase/bin/start-hbase.sh
==> Analytics
install: 542 (30 days), 1,768 (90 days), 7,664 (365 days)
install_on_request: 450 (30 days), 1,424 (90 days), 6,144 (365 days)
build_error: 0 (30 days)

brew services start hbase

```

TODO: Also can be tried with stroage S3
https://www.geomesa.org/documentation/tutorials/geomesa-hbase-s3-on-aws.html
