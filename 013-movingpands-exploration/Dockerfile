# adapted from https://github.com/aarande/docker-pyart/blob/master/Dockerfile-py3
FROM continuumio/miniconda3
MAINTAINER Shoaib Burq

ARG MOVINGPANDAS_VERSION=0.1.dev3

RUN groupadd -r devuser && useradd --no-log-init -ms /bin/bash -r -g devuser devuser
RUN apt-get update && apt-get install -y gcc git && apt-get clean
RUN conda config --append channels conda-forge &&\
    conda install --yes numpy scipy xarray jupyter matplotlib pyproj basemap nose pillow owslib pyepsg cartopy hvplot geoviews 
RUN pip install git+https://github.com/anitagraser/movingpandas.git && pip install nexradaws && conda clean --all

EXPOSE 8888
RUN mkdir /opt/notebooks /opt/data /opt/source && chown devuser:devuser /opt/notebooks && chown devuser:devuser /opt/data && chown devuser:devuser /opt/source
VOLUME /opt/notebooks /opt/data /opt/source
USER devuser
WORKDIR /opt/source
CMD ["python"]
