This docker image contains the full movingpandas and jupyter notebook environment. The image was adapted from https://github.com/aarande/docker-pyart

```sh
docker run --rm -it -p 8888:8888 --name movingpadas \
 --user "$(id -u):$(id -g)" \
 -v `pwd`/notebooks:/opt/notebooks:rw \
 -v `pwd`/data:/opt/data movingpandas \
 /bin/bash -c "/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser"
```

```sh
open http://`docker-machine ip`:8888/?token=c23b78abd62d53872efda9046f4c09d53b172115ac2f6ecc
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
$ docker run -v somedir:/some_dir:rw alpine chown -R 1001:1001 /some_dir
```

TODO: fix https://vsupalov.com/docker-shared-permissions/
