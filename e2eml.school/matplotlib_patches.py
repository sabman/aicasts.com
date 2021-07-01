import matplotlib.patches as patches
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.gca()
path = [
    [.1, .3],
    [.2, .9],
    [.8, .4],
]

ax.add_patch(patches.Polygon(
  path,
  alpha=.7,
  edgecolor="darkblue",
  facecolor="red",
  hatch="+",
  joinstyle="miter",
  linestyle="--",
  linewidth=5,
))


fig.savefig("patch.png")
