# MLflow

A Dockerfile that produces a Python 3.6 image with [MLflow](https://www.mlflow.org) installed.

## Build

First, edit the `MLFLOW_VERSION` variable from the `Dockerfile` to the latest.

This example creates the image with the tag `launchpadrecruits/mlflow`, but you can change this to use your own username.


```
$ docker build -t="launchpadrecruits/mlflow" .
```

Alternately, you can run the following if you have *GNU Make* installed.

```
$ make
```

You can also specify a custom Docker username like so:

```
$ make DOCKER_USER=launchpadrecruits
```

This will set the `latest` tag to the docker image. So you need to add `VERSION` to the
`docker tag` command:

```
docker tag launchpadrecruits/mlflow:latest launchpadrecruits/mlflow:VERSION

# Example
docker tag launchpadrecruits/mlflow:latest launchpadrecruits/mlflow:1.2.0
```

## Usage

To run this image

```
docker run -v /tmp/mlruns:/mlflow/ -p 5000:5000 -e mybucket launchpadrecruits/mlflow
```

Or alternatively, using the `Makefile`:

```
# You might want to edit the defaults
make run
```
