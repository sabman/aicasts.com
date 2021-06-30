import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1)
y = x + np.random.normal(size=x.size)

fig = plt.figure()
ax = fig.gca()
