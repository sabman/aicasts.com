FROM jupyter/scipy-notebook:aarch64-python-3.10.6

# Install dependencies for geopandas
USER root
RUN apt update && apt install -y libgeos-dev libgdal-dev libproj-dev && apt clean

RUN mamba install --quiet --yes \
  'geopandas' \
  'python-dotenv' \
  && \
  mamba clean --all -f -y

RUN pip install --no-cache-dir \
  'geopandas' \
  'pyproj' \
  'cartoframes' \
  'cartopy' \
  'descartes' \
  'markupsafe==2.0.1'