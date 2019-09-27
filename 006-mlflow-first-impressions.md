- [MLflow first impressions](#mlflow-first-impressions)
  - [Installation](#installation)
  - [TK: Running in production](#tk-running-in-production)
    - [Dependencies](#dependencies)
  - [Production setup](#production-setup)
    - [Docker container for MLflow](#docker-container-for-mlflow)
- [Source the .env with BACKEND_URI, BUCKET, DOCKER_USER, DOCKER_REPO_NAME](#source-the-env-with-backenduri-bucket-dockeruser-dockerreponame)
- [fails with no db schema](#fails-with-no-db-schema)
- [fails with](#fails-with)
- [sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedObject) constraint "lifecycle_stage" of relation "experiments" does not exist](#sqlalchemyexcprogrammingerror-psycopg2errorsundefinedobject-constraint-%22lifecyclestage%22-of-relation-%22experiments%22-does-not-exist)
- [[SQL: ALTER TABLE experiments DROP CONSTRAINT lifecycle_stage]](#sql-alter-table-experiments-drop-constraint-lifecyclestage)
    - [Docker container for NGINX](#docker-container-for-nginx)
    - [Stiching it together with Docker Compose](#stiching-it-together-with-docker-compose)
  - [Using it for work](#using-it-for-work)
  - [Criticism](#criticism)
  - [TK: Integrations](#tk-integrations)

# MLflow first impressions

Overall goal:

1. train model
2. package model
3. deploy model

## Installation

Installation is pretty simple. Extras installs `scikit-learn` as well

```
pip install mlflow[extras] # install scikit-learn too

git clone https://github.com/mlflow/mlflow

cd mlflow/examples

python sklearn_elasticnet_wine/train.py

mlflow ui

open http://127.0.0.1:5000
```

![](https://www.evernote.com/l/Ah6gYD4HHfBMh5ZDwazSpy5IRjlDImjzY3UB/image.png)

Now the MLFlow UI is tracking data about our Machine Learning experiments, this is great. Before MLFlow a data scientest has to come up with some internal convention for keeping track of their experiments. In a typical Machine Learning workflow.

I can now try running with some other hyperparameters.

```
❯ python sklearn_elasticnet_wine/train.py 0.2 0.4
Elasticnet model (alpha=0.200000, l1_ratio=0.400000):
  RMSE: 0.7900051428308212
  MAE: 0.6176810535103499
  R2: 0.19391709805063506

❯ python sklearn_elasticnet_wine/train.py 0.5 0.4
Elasticnet model (alpha=0.500000, l1_ratio=0.400000):
  RMSE: 0.8134651568415164
  MAE: 0.6249674191990106
  R2: 0.1453313314484228

❯ python sklearn_elasticnet_wine/train.py 0.4 0.5
Elasticnet model (alpha=0.400000, l1_ratio=0.500000):
  RMSE: 0.8110372935550909
  MAE: 0.6242320018195591
  R2: 0.15042539631592833
```

> This example uses the familiar pandas, numpy, and sklearn APIs to create a simple machine learning model. The MLflow tracking APIs log information about each training run, like the hyperparameters alpha and l1_ratio, used to train the model and metrics, like the root mean square error, used to evaluate the model. The example also serializes the model in a format that MLflow knows how to deploy.

My dashboard now looks like the following:

![](https://www.evernote.com/l/Ah4jvauaDn1KG5ymXgFJqziFbJWuahZEUC0B/image.png)

TK: MLFlow diagram https://drive.google.com/file/d/1eA33IE-XGAiLe8F2cvBbNCFa8CLvQMqs/view?usp=sharing

## TK: Running in production

https://github.com/mlflow/mlflow/issues/40
Running the Tracking Server and UI in production means having

### Dependencies

Python 3
pip3
boto3
nginx
nginx htpasswd module
aws s3 bucket and credentials
mlflow

After provisioning a server login in and ensure the dependencies are installed

```
sudo yum update

sudo yum install nginx
# on aws this is: sudo amazon-linux-extras install nginx1.12
sudo service nginx start

sudo vim /etc/nginx/nginx.conf
```

in location add:

```
        location / {
	        proxy_pass http://localhost:5000/;
                auth_basic "Restricted Content";
                auth_basic_user_file /etc/nginx/.htpasswd;
        }
```

```
sudo service nginx reload

sudo yum install httpd-tools
sudo htpasswd -c /etc/nginx/.htpasswd mlflowuser
nohup mlflow server --default-artifact-root s3://bucket-for-mlflow/ --host 0.0.0.0 &

```

Here's a Dockerfile with the above configuration.

```Dockerfile
...
```

## Production setup

```
[nginx reverse proxy] <--> [ Docker [flask app] <--> Backedup Volume]
```

### Docker container for MLflow

- configure S3 location
- configure database connection

Here is a good example of a Dockerise MLFlow
https://github.com/launchpadrecruits/dockerfiles/tree/master/mlflow


Example docker file

```dockerfile
FROM python:3.6
LABEL maintainer="shoaib <saburq@gmail.com>"

ENV MLFLOW_VERSION 1.2.0
ARG BACKEND_URI=db_type://<user_name>:<password>@<host>:<port>/<database_name>
ENV BACKEND_URI ${BACKEND_URI}

ENV TERM linux

ARG BUCKET=s3://bucket-for-mlflow
ENV BUCKET ${BUCKET}

RUN pip install mlflow==${MLFLOW_VERSION}

RUN mkdir -p /mlflow/

ADD extra-requirements.txt /mlflow/

WORKDIR /mlflow/

RUN pip install -r extra-requirements.txt

EXPOSE 5000

CMD mlflow server \
  --backend-store-uri ${BACKEND_URI} \
  --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
  --host 0.0.0.0

# # If access logs needed:
# CMD mlflow server \
#     --file-store /mlflow \
#     --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
#     --host 0.0.0.0 --gunicorn-opts "--access-logfile -"
```


If we look at the database it will look something like the following:


```
❯ psql -U mlflow -h xxx.rds.amazonaws.com mlflow -W
Password:

mlflow=> \dt
           List of relations
 Schema |    Name     | Type  | Owner
--------+-------------+-------+--------
 public | experiments | table | mlflow
 public | metrics     | table | mlflow
 public | params      | table | mlflow
 public | runs        | table | mlflow
 public | tags        | table | mlflow
 ```


### Docker container for Database

```sh
create database mlflow;
create user mlflow with encrypted password 'supersecretpassword';
grant all privileges on database mlflow to mlflow;
```


### Building the image

```sh
# Source the .env with BACKEND_URI, BUCKET, DOCKER_USER, DOCKER_REPO_NAME
source <(grep -v '^#' .env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')

docker build \
  --build-arg BACKEND_URI=${BACKEND_URI} \
  --build-arg BUCKET=${BUCKET} \
  -t="$(DOCKER_USER)/$(DOCKER_REPO_NAME)" .
```

TODO: 
- [ ] setup the mlflow database schema
- [ ] run the container

```sh
docker run -d --name="lon-dev-mlflow"
    -e BACKEND_URI=${BACKEND_URI} \
    -v `pwd`/logs/lon-dev-mlflow/log:/var/log \
    -v /Users/shoaib/code/mlflow/docker/dockerfiles/mlflow/mlruns:/mlflow \
    -p 5000:5000 sabman/mlflow
# fails with no db schema

docker run -d --name="lon-dev-mlflow" \
    -e BACKEND_URI=${BACKEND_URI} \
    -v `pwd`/logs/lon-dev-mlflow/log:/var/log \
    -v /Users/shoaib/code/mlflow/docker/dockerfiles/mlflow/mlruns:/mlflow \
    -p 5000:5000 sabman/mlflow mlflow db upgrade ${BACKEND_URI}
# fails with 
# sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedObject) constraint "lifecycle_stage" of relation "experiments" does not exist
# [SQL: ALTER TABLE experiments DROP CONSTRAINT lifecycle_stage]
```

https://thegurus.tech/posts/2019/06/mlflow-production-setup/



### Docker container for NGINX

### Stiching it together with Docker Compose

## Using it for work

![](https://res.cloudinary.com/practicaldev/image/fetch/s--dc_gXynR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://ishankhare.com/media/images/nginx-reverse-proxy.png)

ref: https://dev.to/ishankhare07/nginx-as-reverse-proxy-for-a-flask-app-using-docker-3ajg

https://stackoverflow.com/questions/57078147/how-should-i-mount-docker-volumes-in-mlflow-project
https://medium.com/ixorthink/our-machine-learning-workflow-dvc-mlflow-and-training-in-docker-containers-5b9c80cdf804
https://towardsdatascience.com/containerize-your-whole-data-science-environment-or-anything-you-want-with-docker-compose-e962b8ce8ce5

Using MLFlow for feature extraction:
https://towardsdatascience.com/feature-factories-pt-2-an-introduction-to-mlflow-873be3c66b66

## Criticism

https://news.ycombinator.com/item?id=18507006

## TK: Integrations

Seldon:

- https://www.seldon.io/open-source/
- https://github.com/SeldonIO/seldon-core/blob/9052cf10d97574babc1459b63917a6b13ec3b7b1/examples/models/mlflow_model/mlflow.ipynb

Neptune.ml:

- https://towardsdatascience.com/collaborate-on-mlflow-experiments-in-neptune-fb4f8f84a995
