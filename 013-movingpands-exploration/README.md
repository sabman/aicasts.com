This docker image contains the full movingpandas and jupyter notebook environment. The image was adapted from https://github.com/aarande/docker-pyart

```sh
docker run --rm -it -p 8888:8888 --name movingpadas \
 -v `pwd`/notebooks:/opt/notebooks \
 -v `pwd`/data:/opt/data movingpandas \
 /bin/bash -c "/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser"
```

```sh
open http://`docker-machine ip`:8888/?token=7ed010e454728cef8025790862f85e928a76940d591dc9d9
```

```sh
cd notebooks
wget https://raw.githubusercontent.com/anitagraser/movingpandas/master/tutorials/3_horse_collar.ipynb

mkdir data

cd data
wget -O demodata_horse_collar.gpkg https://github.com/anitagraser/movingpandas/blob/master/tutorials/data/demodata_horse_collar.gpkg?raw=true

```


```
$ docker build . -t test
$ docker volume create somedir
$ docker run -v somedir:/some_dir alpine chown -R 1001:1001 /some_dir
```