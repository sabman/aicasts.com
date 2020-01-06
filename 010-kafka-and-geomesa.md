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

WPS plugin

```
wget https://netix.dl.sourceforge.net/project/geoserver/GeoServer/2.14.4/geoserver-2.14.4-bin.zip
```

```
cp ~/tmp/geoserver-2.14.4-wps-plugin/* ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
```



Kafka 
```
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka-clients-2.3.1.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka_2.12-2.3.1.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zkclient-0.11.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zookeeper-3.4.14.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/metrics-core-2.2.0.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/jopt-simple-5.0.4.jar ~/code/geoserver-2.14.4/webapps/geoserver/WEB-INF/lib
```


https://gis.stackexchange.com/questions/210316/access-control-allow-origin-openlayers-wfs

```
vim webapps/geoserver/WEB-INF/web.xml
```

Should have the following:

```xml
  <!-- Uncomment following filter to enable CORS -->
  <filter>
    <filter-name>cross-origin</filter-name>
    <filter-class>org.eclipse.jetty.servlets.CrossOriginFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>cross-origin</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
```


```
❯ curl http://0.0.0.0:8080/geoserver/cite/wfs\?service\=WFS\&version\=1.1.0\&request\=GetFeature\&typeName\=cite:tdrive-quickstart\&outputFormat\=application/json | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   385    0   385    0     0    116      0 --:--:--  0:00:03 --:--:--   116
```

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "1277",
      "geometry": {
        "type": "Point",
        "coordinates": [
          116.31777,
          39.89572
        ]
      },
      "geometry_name": "geom",
      "properties": {
        "taxiId": "1277",
        "dtg": "2008-02-08T17:36:39Z"
      }
    }
  ],
  "totalFeatures": 0,
  "numberMatched": 0,
  "numberReturned": 1,
  "timeStamp": "2019-11-12T16:46:01.630Z",
  "crs": {
    "type": "name",
    "properties": {
      "name": "urn:ogc:def:crs:EPSG::4326"
    }
  }
}
```

# Client

https://github.com/perliedman/leaflet-realtime

```

```