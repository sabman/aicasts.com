# Introduction

https://www.geomesa.org/documentation/tutorials/geomesa-quickstart-kafka.html

# Geomesa

Installing Geomesa:

```sh
# download the tutorials
git clone https://github.com/geomesa/geomesa-tutorials.git
git checkout geomesa-tutorials-2.3.1
mvn clean install -pl geomesa-tutorials-kafka/geomesa-tutorials-kafka-quickstart -am
java -cp geomesa-tutorials-kafka/geomesa-tutorials-kafka-quickstart/target/geomesa-tutorials-kafka-quickstart-2.3.1.jar \
    org.geomesa.example.kafka.KafkaListener \
    --kafka.brokers localhost:9092 \
    --kafka.zookeepers localhost:2181
```

# Kafka and Zookeeper

```sh
brew install kafka
brew services start kafka
brew install zookeeper
brew services start zookeeper
# brew services restart zookeeper
# brew services restart kafka
```

# GeoServer

## WPS plugin

Download WPS plugin:

```sh
GEOSERVER_VERSION=2.14.4
wget https://netix.dl.sourceforge.net/project/geoserver/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-bin.zip

```

Install WPS plugin in Geoserver:

```sh
wget https://iweb.dl.sourceforge.net/project/geoserver/GeoServer/${GEOSERVER_VERSION}/extensions/geoserver-${GEOSERVER_VERSION}-wps-plugin.zip

cp ~/tmp/geoserver-${GEOSERVER_VERSION}-wps-plugin/* ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib

geoserver /usr/local/Cellar/geoserver/2.15.2/libexec/webapps/geoserver/data
```


Kafka:

```sh
wget https://repo1.maven.org/maven2/org/locationtech/geomesa/geomesa-kafka-gs-plugin_2.11/2.3.2/geomesa-kafka-gs-plugin_2.11-2.3.2-install.tar.gz
```

```sh
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka-clients-2.3.1.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/kafka_2.12-2.3.1.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zkclient-0.11.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/zookeeper-3.4.14.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/metrics-core-2.2.0.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
cp /usr/local/Cellar/kafka/2.3.1/libexec/libs/jopt-simple-5.0.4.jar ~/code/geoserver-${GEOSERVER_VERSION}/webapps/geoserver/WEB-INF/lib
```


https://gis.stackexchange.com/questions/210316/access-control-allow-origin-openlayers-wfs

```sh
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


```sh
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

```sh
...
```

Taxi Data: https://publish.illinois.edu/dbwork/open-data/

The logic is contained in the generic `org.geomesa.example.quickstart.GeoMesaQuickStart`

Some relevant methods are:

* `createDataStore` get a `datastore` instance from the input configuration
* `createSchema` create the schema in the datastore, as a pre-requisite to writing data
* `writeFeatures` overridden in the `KafkaQuickStart` to simultaneously write and read features from Kafka
`queryFeatures` not used in this tutorial
* `cleanup` delete the sample data and dispose of the `datastore` instance


```sh
cd leaflet-realtime

```

### Register the GeoMesa Store with GeoServer

Log into GeoServer using your user and password credentials. Click “Stores” and “Add new Store”. Select the Kafka (GeoMesa) vector data source, and fill in the required parameters.

Basic store info:

workspace this is dependent upon your GeoServer installation
data source name pick a sensible name, such as geomesa_quick_start
description this is strictly decorative; GeoMesa quick start
Connection parameters:

these are the same parameter values that you supplied on the command line when you ran the tutorial; they describe how to connect to the Kafka instance where your data reside
Click “Save”, and GeoServer will search Zookeeper for any GeoMesa-managed feature types.

#### Publish the Layer

If you have already run the command to start the tutorial, then GeoServer should recognize the tdrive-quickstart feature type, and should present that as a layer that can be published. Click on the “Publish” link. If not, then run the tutorial as described above in Running the Tutorial. When the tutorial pauses, go to “Layers” and “Add new Layer”. Select the GeoMesa Kafka store you just created, and then click “publish” on the tdrive-quickstart layer.

You will be taken to the Edit Layer screen. You will need to enter values for the data bounding boxes. For this demo, use the values MinX: 116.22366, MinY: 39.72925, MaxX: 116.58804, MaxY: 40.09298.

Click on the “Save” button when you are done.

