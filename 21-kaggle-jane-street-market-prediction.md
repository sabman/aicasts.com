# Challenge

URL https://www.kaggle.com/c/jane-street-market-prediction


This competition is evaluated on a utility score. Each row in the test set represents a trading opportunity for which you will be predicting an action value, 1 to make the trade and 0 to pass on it. Each trade `j` has an associated `weight` and `resp`, which represents a return.

For each date i, we define:

$$
p_i = \sum_j(weight_{ij} * resp_{ij} * action_{ij}),
$$

$$
t = \frac{\sum p_i }{\sqrt{\sum p_i^2}} * \sqrt{\frac{250}{|i|}},
$$

```py
import janestreet
env = janestreet.make_env() # initialize the environment
iter_test = env.iter_test() # an iterator which loops over the test set

for (test_df, sample_prediction_df) in iter_test:
    sample_prediction_df.action = 0 #make your 0/1 prediction here
    env.predict(sample_prediction_df)
```
