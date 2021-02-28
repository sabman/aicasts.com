# Mastering Numpy

This is an example of a sine curve created using `numpy` and `matplotlib`.


```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi)
plt.plot(x, np.sin(x))
```

```
[<matplotlib.lines.Line2D at 0x117747438>]
```

![](figures/visual-intro_figure1_1.png)\


## Visual Guide to Numpy




This [article](https://jalammar.github.io/visual-numpy/) about numpy is an excellent resource but build an intuition for numpy arrays if you are a visual thinker.

### Creating Arrays


```python
a = np.array([1,2,3])
print(a)
```

```
[1 2 3]
```



Initialize a certain number of elements in our array using initialization methods:


```python
# ones
print(np.ones(3))
# zeros
print(np.zeros(3))
# random
print(np.random.random(3))
```

```
[1. 1. 1.]
[0. 0. 0.]
[0.92184369 0.19547181 0.78667072]
```



### Array Arithmetic


```python
data = np.array([1,2])
ones = np.ones(2)

# lets add them
# Look ma no loops!
_sum = data + ones
print(_sum)

print(data*ones)
print(data/ones)
```

```
[2. 3.]
[1. 2.]
[1. 2.]
```



### Scalar-Vector operations
operation between an array and a single number (we can also call this an operation between a vector and a scalar)


```python
_ = data * 1.6
print(_)
```

```
[1.6 3.2]
```



### Aggregation


```python
_ = data.max()
print(_)

_ = data.min()
print(_)

_ = data.sum()
print(_)
```

```
2
1
3
```



## More Dimensions

### Creating Matrices



```python
_ = np.array([[1,2],[3,4]])
print(_)

_ = np.ones((3,2))
print("ones: \n", _)

_ = np.zeros((3,2))
print("zeros: \n", _)

_ = np.random.random((3,2))
print("random: \n", _)
```

```
[[1 2]
 [3 4]]
ones:
 [[1. 1.]
 [1. 1.]
 [1. 1.]]
zeros:
 [[0. 0.]
 [0. 0.]
 [0. 0.]]
random:
 [[0.15795171 0.78401414]
 [0.10104205 0.62924756]
 [0.89586602 0.03121201]]
```



### Matrix Arithmetic

Requirement: Matrices must be the same size


```python
data = np.array([[1,2],[3,4]])
ones = np.ones((2,2))
_ = data + ones
print(_)
```

```
[[2. 3.]
 [4. 5.]]
```



Broadcast rules in `numpy` allow perfroming arithmetic on matrices of different sizes.


```python
ones_row = np.ones((1,2))
print(ones_row)
print(data)
_ = data + ones_row
print(_)
```

```
[[1. 1.]]
[[1 2]
 [3 4]]
[[2. 3.]
 [4. 5.]]
```


