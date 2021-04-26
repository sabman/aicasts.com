# Anatomy of an array


```python
Z = np.ones(4*1000000, np.float32)
# Z[...] = 0
Z.vew(np.int8)[...] = 0
```

```
---------------------------------------------------------------------------NameError
Traceback (most recent call last)<ipython-input-1-5bbe55bff0e2> in
<module>
----> 1 Z = np.ones(4*1000000, np.float32)
      2 # Z[...] = 0
      3 Z.vew(np.int8)[...] = 0
NameError: name 'np' is not defined
```



