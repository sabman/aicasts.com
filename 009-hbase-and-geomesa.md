install http://www.apache.org/dyn/closer.cgi/hbase/

```sh
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

❯ java -cp geomesa-tutorials-hbase/geomesa-tutorials-hbase-quickstart/target/geomesa-tutorials-hbase-quickstart-2.4.0-SNAPSHOT.jar \
    org.geomesa.example.hbase.HBaseQuickStart \
    --hbase.zookeepers localhost           \
    --hbase.catalog globalevents
```

TODO: Also can be tried with storage S3

- [ ] https://www.geomesa.org/documentation/tutorials/geomesa-hbase-s3-on-aws.html

References

- [ ] https://hbase.apache.org/book.html

## Setting an EMR cluster

```
ssh hadoop@ec2-13-210-102-204.ap-southeast-2.compute.amazonaws.com -v -i ~/code/external-devops.pem
VERSION=2.3.2
JARS=file:///opt/geomesa/dist/spark/geomesa-hbase-spark-runtime_2.11-${VERSION}.jar,file:///usr/lib/hbase/conf/hbase-site.xml
spark-shell --jars $JARS --conf spark.executor.memory=2g
```

## Loading data HBase

```
bucket_name=geomesa-storage
aws s3 mb s3://$bucket_name
aws s3 mb s3://$bucket_name
```
