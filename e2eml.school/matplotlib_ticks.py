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

