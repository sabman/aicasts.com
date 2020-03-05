
# Kepler + Carto + Jupyter

- https://github.com/CartoDB/kepler.gl/blob/master/docs/keplergl-jupyter/user-guide.md
- https://github.com/keplergl/kepler.gl/blob/master/bindings/kepler.gl-jupyter/notebooks/Load%20kepler.gl.ipynb
- https://github.com/keplergl/kepler.gl/blob/master/bindings/kepler.gl-jupyter/notebooks/Geometry%20as%20String.ipynb
- https://github.com/keplergl/kepler.gl/blob/master/bindings/kepler.gl-jupyter/notebooks/GeoJSON.ipynb
- https://carto.com/blog/plotly/

# Cartoframes

- https://carto.com/developers/cartoframes/

# Connect to DBs
- https://towardsdatascience.com/heres-how-to-run-sql-in-jupyter-notebooks-f26eb90f3259


# Install



```bash

# https://www.digitalocean.com/community/tutorials/how-to-install-run-connect-to-jupyter-notebook-on-remote-server

adduser sammy
usermod -aG sudo sammy

# https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-18-04-server
apt update && apt install -y python3-pip
apt install build-essential libssl-dev libffi-dev python3-dev
apt install -y python3-venv
su - sammy
mkdir environments
cd environments
python3.6 -m venv my_env
source my_env/bin/activate

# https://www.digitalocean.com/community/tutorials/how-to-install-run-connect-to-jupyter-notebook-on-remote-server
python3 -m pip install jupyter

```