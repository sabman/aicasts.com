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

## Running in production



