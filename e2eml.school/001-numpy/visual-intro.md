# Mastering Numpy

This is an example of a sine curve created using `numpy` and `matplotlib`.


```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi)
plt.plot(x, np.sin(x))
```

```
[<matplotlib.lines.Line2D at 0x120cc7518>]
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
[0.23984192 0.70604736 0.6491148 ]
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
 [[0.21901291 0.41987117]
 [0.56806437 0.62961135]
 [0.52870911 0.38462356]]
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



### Dot Product

NumPy gives every matrix a `dot()` method we can use to carry-out dot product operations with other matrices:


```python

data = np.array([1,2,3])
powers_of_ten = np.array([[1,10],[100,1000], [10000, 100000]])

_ = data.dot(powers_of_ten)
print(_)
```

```
[ 30201 302010]
```






```python
import seaborn as sns
sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")
ax = sns.stripplot(x=tips["total_bill"])
```

![](figures/visual-intro_figure11_1.png)\

### Matrix Indexing


```python
data = np.array([[1,2],[3,4],[5,6]])
print(data.max())
print(data.min())
print(data.sum())
```

```
6
1
21
```



### Aggregation acrosss rows or columns

Not only can we aggregate all the values in a matrix, but we can also aggregate across the rows or columns by using the `axis` parameter:


```python
data = np.array([[1,2],[3,4],[5,6]])
print(data.max(axis=0))
print(data.max(axis=1))
```

```
[5 6]
[2 4 6]
```




### Transposing and Reshaping



```python
print("Data:")
print(data)

print("Transpose:")
print(data.T)
```

```
Data:
[[1 2]
 [3 4]
 [5 6]]
Transpose:
[[1 3 5]
 [2 4 6]]
```



### Reshaping


```python
print(data)
_ = data.reshape(2,3)
print(_)
_ = data.reshape(3,2)
print(_)
```

```
[[1 2]
 [3 4]
 [5 6]]
[[1 2 3]
 [4 5 6]]
[[1 2]
 [3 4]
 [5 6]]
```



### Adding ndimensions


```python
_ = np.array([
    [[1,2],[3,4]],
    [[5,6],[7,8]]
])
print(_)

_ = np.ones((4,3,2)) # 4 x 3 x 2 matrix
print(_)

_ = np.zeros((4,3,2)) # 4 x 3 x 2 matrix
print(_)

_ = np.random.random((4,3,2)) # 4 x 3 x 2 matrix
print(_)
```

```
[[[1 2]
  [3 4]]

 [[5 6]
  [7 8]]]
[[[1. 1.]
  [1. 1.]
  [1. 1.]]

 [[1. 1.]
  [1. 1.]
  [1. 1.]]

 [[1. 1.]
  [1. 1.]
  [1. 1.]]

 [[1. 1.]
  [1. 1.]
  [1. 1.]]]
[[[0. 0.]
  [0. 0.]
  [0. 0.]]

 [[0. 0.]
  [0. 0.]
  [0. 0.]]

 [[0. 0.]
  [0. 0.]
  [0. 0.]]

 [[0. 0.]
  [0. 0.]
  [0. 0.]]]
[[[0.42644035 0.45161003]
  [0.41108986 0.15633924]
  [0.35845932 0.42255224]]

 [[0.98574712 0.39417963]
  [0.00862692 0.96417456]
  [0.36743981 0.5300963 ]]

 [[0.74022469 0.35144511]
  [0.93843963 0.21871381]
  [0.92081369 0.86264438]]

 [[0.25035937 0.19749698]
  [0.75246796 0.97502874]
  [0.2681811  0.49977709]]]
```



## Practical Usage

### key use 

Mathematical formulas that work on matrices and vectors.

For example: Mean Square Error 


```python
n = 3
predictions = np.ones(n)
labels = np.array([1,2,3])
error = (1/n * np.sum(np.square(predictions - labels))
print(error)
```

```
  File "<ipython-input-1-2bcf442807ad>", line 5
    print(error)
        ^
SyntaxError: invalid syntax
```



