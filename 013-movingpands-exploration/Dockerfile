FROM continuumio/miniconda3
MAINTAINER Shoaib Burq

RUN groupadd -r devuser && useradd --no-log-init -ms /bin/bash -r -g devuser devuser
RUN apt-get update && apt-get install -y gcc git && apt-get clean
RUN conda config --append channels conda-forge &&\
    conda install --yes numpy scipy xarray jupyter matplotlib pyproj basemap nose pillow owslib pyepsg cartopy \
    movingpandas && pip install nexradaws && conda clean --all

EXPOSE 8888
RUN mkdir /opt/notebooks /opt/data /opt/source && chown devuser:devuser /opt/notebooks && chown devuser:devuser /opt/data && chown devuser:devuser /opt/source
VOLUME /opt/notebooks /opt/data /opt/source
USER devuser
WORKDIR /opt/source
CMD ["python"]
