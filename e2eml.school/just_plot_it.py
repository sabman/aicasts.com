import numpy as np
import matplotlib.pyplot as plt

x_curve = np.linespace(-2 * np.pi, 2 * np.pi, 500)
y_curve = np.sinc(x_curve)
plt.figure()
plt.plot(x_curve, y_curve)
plt.savefig("images/line_plot.png")
plt.show()

