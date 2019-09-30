- [MLflow first impressions](#mlflow-first-impressions)
	- [Installation](#installation)
	- [TK: Running in production](#tk-running-in-production)
		- [Dependencies](#dependencies)
	- [Production setup](#production-setup)
		- [Docker container for MLflow](#docker-container-for-mlflow)
			- [using sqlite database](#using-sqlite-database)
		- [Docker container for Database](#docker-container-for-database)
		- [Building the image](#building-the-image)
		- [TK: Adding Authentication](#tk-adding-authentication)
		- [Docker container for NGINX](#docker-container-for-nginx)
		- [Stitching it together with Docker Compose](#stitching-it-together-with-docker-compose)
	- [Using it for work](#using-it-for-work)
	- [Criticism](#criticism)
	- [TK: Integrations](#tk-integrations)

# MLflow first impressions

Overall goal:

1. train model
2. package model
3. deploy model
4. production use case

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

ARG MLFLOW_TRACKING_USERNAME mlflow
ENV MLFLOW_TRACKING_USERNAME=${MLFLOW_TRACKING_USERNAME}

ARG MLFLOW_TRACKING_TOKEN 506bc28114ceb5fb943f0cad6e4f4de0
ENV MLFLOW_TRACKING_TOKEN=${MLFLOW_TRACKING_TOKEN}

ARG ENV MLFLOW_TRACKING_INSECURE_TLS "true"
ENV MLFLOW_TRACKING_INSECURE_TLS=${MLFLOW_TRACKING_INSECURE_TLS}

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

#### using sqlite database

```
sqlite3 mlflow.db "create table aTable(field1 int); drop table aTable;"

mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
  --host 0.0.0.0
```

If we look at the database it will look something like the following:

![](006-mlflow-first-impressions/mlflow.png)

```
sqlite> .databases
main: /mlflow/mlflow.db
sqlite> .schema
```

```sql
CREATE TABLE experiments (
	experiment_id INTEGER NOT NULL,
	name VARCHAR(256) NOT NULL,
	artifact_location VARCHAR(256),
	lifecycle_stage VARCHAR(32),
	CONSTRAINT experiment_pk PRIMARY KEY (experiment_id),
	CONSTRAINT experiments_lifecycle_stage CHECK (lifecycle_stage IN ('active', 'deleted')),
	UNIQUE (name)
);
CREATE TABLE runs (
	run_uuid VARCHAR(32) NOT NULL,
	name VARCHAR(250),
	source_type VARCHAR(20),
	source_name VARCHAR(500),
	entry_point_name VARCHAR(50),
	user_id VARCHAR(256),
	status VARCHAR(20),
	start_time BIGINT,
	end_time BIGINT,
	source_version VARCHAR(50),
	lifecycle_stage VARCHAR(20),
	artifact_uri VARCHAR(200),
	experiment_id INTEGER,
	CONSTRAINT run_pk PRIMARY KEY (run_uuid),
	CONSTRAINT source_type CHECK (source_type IN ('NOTEBOOK', 'JOB', 'LOCAL', 'UNKNOWN', 'PROJECT')),
	CONSTRAINT status CHECK (status IN ('SCHEDULED', 'FAILED', 'FINISHED', 'RUNNING')),
	CONSTRAINT runs_lifecycle_stage CHECK (lifecycle_stage IN ('active', 'deleted')),
	FOREIGN KEY(experiment_id) REFERENCES experiments (experiment_id)
);
CREATE TABLE params (
	"key" VARCHAR(250) NOT NULL,
	value VARCHAR(250) NOT NULL,
	run_uuid VARCHAR(32) NOT NULL,
	CONSTRAINT param_pk PRIMARY KEY ("key", run_uuid),
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
);
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE IF NOT EXISTS "metrics" (
	"key" VARCHAR(250) NOT NULL,
	value FLOAT NOT NULL,
	timestamp BIGINT NOT NULL,
	run_uuid VARCHAR(32) NOT NULL,
	step BIGINT DEFAULT '0' NOT NULL,
	is_nan BOOLEAN DEFAULT '0' NOT NULL,
	CONSTRAINT metric_pk PRIMARY KEY ("key", timestamp, step, run_uuid, value, is_nan),
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
);
CREATE TABLE experiment_tags (
	"key" VARCHAR(250) NOT NULL,
	value VARCHAR(5000),
	experiment_id INTEGER NOT NULL,
	CONSTRAINT experiment_tag_pk PRIMARY KEY ("key", experiment_id),
	FOREIGN KEY(experiment_id) REFERENCES experiments (experiment_id)
);
CREATE TABLE IF NOT EXISTS "tags" (
	"key" VARCHAR(250) NOT NULL,
	value VARCHAR(5000),
	run_uuid VARCHAR(32) NOT NULL,
	CONSTRAINT tag_pk PRIMARY KEY ("key", run_uuid),
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
);
```

```sh
root@c67be17b3e16:/mlflow# mlflow server \
  --backend-store-uri ${BACKEND_URI} \
  --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
  --host 0.0.0.0

2019/09/27 22:49:02 INFO mlflow.store.sqlalchemy_store: Creating initial MLflow database tables...
2019/09/27 22:49:10 INFO mlflow.store.db.utils: Updating database tables at postgresql://mlflow:xxxx@xxxx.rds.amazonaws.com:5432/mlflow
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 451aebb31d03, add metric step
INFO  [alembic.runtime.migration] Running upgrade 451aebb31d03 -> 90e64c465722, migrate user column to tags
INFO  [alembic.runtime.migration] Running upgrade 90e64c465722 -> 181f10493468, allow nulls for metric values
INFO  [alembic.runtime.migration] Running upgrade 181f10493468 -> df50e92ffc5e, Add Experiment Tags Table
INFO  [alembic.runtime.migration] Running upgrade df50e92ffc5e -> 7ac759974ad8, Update run tags with larger limit
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
[2019-09-27 22:49:29 +0000] [332] [INFO] Starting gunicorn 19.9.0
[2019-09-27 22:49:29 +0000] [332] [INFO] Listening at: http://0.0.0.0:5000 (332)
[2019-09-27 22:49:29 +0000] [332] [INFO] Using worker: sync
[2019-09-27 22:49:29 +0000] [335] [INFO] Booting worker with pid: 335
[2019-09-27 22:49:29 +0000] [336] [INFO] Booting worker with pid: 336
[2019-09-27 22:49:29 +0000] [337] [INFO] Booting worker with pid: 337
[2019-09-27 22:49:29 +0000] [338] [INFO] Booting worker with pid: 338
```

```
❯ psql -U mlflow -h xxx.rds.amazonaws.com mlflow -W
Password:

mlflow=> \dt
             List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+--------
 public | alembic_version | table | mlflow
 public | experiment_tags | table | mlflow
 public | experiments     | table | mlflow
 public | metrics         | table | mlflow
 public | params          | table | mlflow
 public | runs            | table | mlflow
 public | tags            | table | mlflow
(7 rows)
```

### Docker container for Database

```sh
create database mlflow;
create user mlflow with encrypted password 'supersecretpassword';
grant all privileges on database mlflow to mlflow;
```

### Building the image

Source the .env with BACKEND_URI, BUCKET, DOCKER_USER, DOCKER_REPO_NAME

```sh
source <(grep -v '^#' .env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')

docker build \
  --build-arg BACKEND_URI=${BACKEND_URI} \
  --build-arg BUCKET=${BUCKET} \
  -t="$(DOCKER_USER)/$(DOCKER_REPO_NAME)" .
```

```sh
docker run -d --name="lon-dev-mlflow"
    -e BACKEND_URI=${BACKEND_URI} \
    -v `pwd`/logs/lon-dev-mlflow/log:/var/log \
    -v /Users/shoaib/code/mlflow/docker/dockerfiles/mlflow/mlruns:/mlflow \
    -p 5000:5000 sabman/mlflow
```

> "fails with no db schema"

```sh
docker run -d --name="lon-dev-mlflow" \
    -e BACKEND_URI=${BACKEND_URI} \
    -v `pwd`/logs/lon-dev-mlflow/log:/var/log \
    -v /Users/shoaib/code/mlflow/docker/dockerfiles/mlflow/mlruns:/mlflow \
    -p 5000:5000 sabman/mlflow mlflow db upgrade ${BACKEND_URI}
```

output:

```

fails with
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedObject) constraint "lifecycle_stage" of relation "experiments" does not exist

[SQL: ALTER TABLE experiments DROP CONSTRAINT lifecycle_stage]

```

### TK: Adding Authentication

TK: Add the following to the Dockerfile

<!-- TODO: Add the following ARGS to Dockerfile -->

- MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD - username and password to use with HTTP Basic authentication. To use Basic authentication, you must set both environment variables .
- MLFLOW_TRACKING_TOKEN - token to use with HTTP Bearer authentication. Basic authentication takes precedence if set.
- MLFLOW_TRACKING_INSECURE_TLS - if set to the literal true, MLflow does not verify the TLS connection, meaning it does not validate certificates or hostnames for https:// tracking URIs. This flag is not recommended for production environments.

https://www.mlflow.org/docs/latest/tracking.html#tracking-auth

https://thegurus.tech/posts/2019/06/mlflow-production-setup/

### Docker container for NGINX

### Stitching it together with Docker Compose

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
