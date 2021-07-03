import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

# Create the curve data.
x = np.linspace(1, 13, 500)
y = 1 + np.sinc(x - 7)
fig = plt.figure()
ax = fig.gca()
ax.plot(x, y)

ax.tick_params(axis="x", labelsize=18, labelrotation=-60, labelcolor="turquoise")
ax.tick_params(axis="y", labelsize=12, labelrotation=20, labelcolor="orange")

