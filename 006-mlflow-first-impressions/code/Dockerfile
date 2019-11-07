FROM python:3.6
LABEL maintainer="shoaib <saburq@gmail.com>"

ENV MLFLOW_VERSION 1.4.0
ARG BACKEND_URI=db_type://<user_name>:<password>@<host>:<port>/<database_name>
ENV BACKEND_URI ${BACKEND_URI}

ENV TERM linux
ARG BUCKET=s3://bucket-for-mlflow
ENV BUCKET ${BUCKET}

RUN pip install mlflow==$MLFLOW_VERSION

RUN mkdir -p /mlflow/

ADD extra-requirements.txt /mlflow/

WORKDIR /mlflow/

RUN pip install -r extra-requirements.txt

EXPOSE 5000

ARG MLFLOW_TRACKING_USERNAME=mlflow
ENV MLFLOW_TRACKING_USERNAME ${MLFLOW_TRACKING_USERNAME}

ARG MLFLOW_TRACKING_TOKEN=506bc28114ceb5fb943f0cad6e4f4de0
ENV MLFLOW_TRACKING_TOKEN ${MLFLOW_TRACKING_TOKEN}

ARG MLFLOW_TRACKING_INSECURE_TLS="true"
ENV MLFLOW_TRACKING_INSECURE_TLS ${MLFLOW_TRACKING_INSECURE_TLS}

CMD mlflow server \
  --backend-store-uri ${BACKEND_URI} \
  --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
  --host 0.0.0.0

# # If access logs needed:
# CMD mlflow server \
#     --file-store /mlflow \
#     --default-artifact-root s3://${BUCKET}/mlflow-artifacts \
#     --host 0.0.0.0 --gunicorn-opts "--access-logfile -"
