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

mlflow/examples on  master took 3s
❯ python sklearn_elasticnet_wine/train.py 0.5 0.4
Elasticnet model (alpha=0.500000, l1_ratio=0.400000):
  RMSE: 0.8134651568415164
  MAE: 0.6249674191990106
  R2: 0.1453313314484228

mlflow/examples on  master took 3s
❯ python sklearn_elasticnet_wine/train.py 0.4 0.5
Elasticnet model (alpha=0.400000, l1_ratio=0.500000):
  RMSE: 0.8110372935550909
  MAE: 0.6242320018195591
  R2: 0.15042539631592833
```

> This example uses the familiar pandas, numpy, and sklearn APIs to create a simple machine learning model. The MLflow tracking APIs log information about each training run, like the hyperparameters alpha and l1_ratio, used to train the model and metrics, like the root mean square error, used to evaluate the model. The example also serializes the model in a format that MLflow knows how to deploy.

My dashboard now looks like the following: 

![](https://www.evernote.com/l/Ah4jvauaDn1KG5ymXgFJqziFbJWuahZEUC0B/image.png)

## Running in production



