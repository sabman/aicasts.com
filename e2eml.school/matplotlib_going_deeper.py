import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca()
ax.plot(x, y)

fig.savefig("my_new_plot.png")
