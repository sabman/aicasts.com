# Kepler + Carto + Jupyter

- https://github.com/CartoDB/kepler.gl/blob/master/docs/keplergl-jupyter/README.md
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
apt update && apt install -y python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv expect
# expect command is used for setting password https://likegeeks.com/expect-command/

su - sammy
mkdir environments
cd environments
python3.6 -m venv my_env
source my_env/bin/activate

# https://www.digitalocean.com/community/tutorials/how-to-install-run-connect-to-jupyter-notebook-on-remote-server
python3 -m pip install jupyter

# (my_env) sammy@665b78d8f1be:~/environments$ which jupyter
# /home/sammy/environments/my_env/bin/jupyter


jupyter notebook --generate-config
# /home/sammy/.jupyter/jupyter_notebook_config.py
# jupyter notebook password
(my_env) sammy@665b78d8f1be:~$ JUPYTER_HASHED_PW=`python3 -c "from notebook.auth import passwd; print(passwd('your_password'))"`
(my_env) sammy@665b78d8f1be:~$ echo $JUPYTER_HASHED_PW
sha1:cfa3f5498c81:9a74501e8126bae20c9938b0e0a1bcca80d9e990

# replace
#c.NotebookApp.base_url = '/'
# with
# c.NotebookApp.base_url = '/jupyter'

sed -i.back -e "s/#c.NotebookApp.base_url = '\/'/c.NotebookApp.base_url = '\/jupyter'/" /home/sammy/.jupyter/jupyter_notebook_config.py

sed -i.bak -e "s/#c.NotebookApp.allow_remote_access = False/c.NotebookApp.allow_remote_access = True/" /home/sammy/.jupyter/jupyter_notebook_config.py

sed -i.bak -e "s/#c.NotebookApp.quit_button = True/c.NotebookApp.quit_button = False/" /home/sammy/.jupyter/jupyter_notebook_config.py

```

supervisor

```
[program:jupyter]
user=sammy
environment=HOME=/home/sammy
directory=/home/sammy/environments
priority=500
command=/bin/bash -c 'source /home/sammy/environments/my_env/bin/activate && jupyter-notebook --notebook-dir=/home/sammy/environments --no-browser --ip=127.0.0.1'

```

```bash
supervisorctl -c /opt/supervisord.conf update jupyter
# jupyter: added process group
```

