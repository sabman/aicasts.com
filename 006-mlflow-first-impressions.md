# MLflow first impressions

Overall goal:

1. train model
2. package model
3. deploy model

## Installation

Installation is pretty simple. Extras installs `scikit-learn` as well

```shell
pip install mlflow[extras]
git clone https://github.com/mlflow/mlflow
cd mlflow/examples
python sklearn_elasticnet_wine/train.py
mlflow ui
```
