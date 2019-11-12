# Introduction


# Geomesa

```
git clone https://github.com/geomesa/geomesa-tutorials.git
gco geomesa-tutorials-2.3.1
mvn clean install -pl geomesa-tutorials-kafka/geomesa-tutorials-kafka-quickstart -am


```

# Kafka

```
brew install kafka
brew services start kafka
brew install zookeeper
brew services start zookeeper
```

# GeoServer


```
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka-clients-2.3.1.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka_2.12-2.3.1.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zkclient-0.11.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zookeeper-3.4.14.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/metrics-core-2.2.0.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/jopt-simple-5.0.4.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
```


# Client

```

```