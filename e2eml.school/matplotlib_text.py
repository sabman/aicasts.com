import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

# Create the curve data.
x = np.linspace(-6, 6, 500)
y = np.sinc(x)
fig = plt.figure()
ax = fig.gca()
ax.plot(x, y)

