import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1)
y = x + np.random.normal(size=x.size)

fig = plt.figure()
ax = fig.gca()

# Change the size
ax.scatter(x, y, s=80)

# Make every marker a different size
# The real power of the scatter() function somes out when we want to modify markers individually.

sizes = (np.random.sample(size=x.size) * 10) ** 2
ax.scatter(x, y, s=sizes)

from matplotlib.colors import LinearSegmentedColormap
custom_cmap = LinearSegmentedColormap.from_list("my_cmap", ["red", "black", "white"])
print(custom_cmap)

