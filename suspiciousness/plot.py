import matplotlib.pyplot as plt
import smplotlib
from suspiciousness.core import samples


@samples
def plot(a, b, ab, labels=("a", "b", "ab"), ax=None, x="omegam", y="sigma8"):
    if ax is None:
        _, ax = plt.subplots()

    for ns, label in zip((a, b, ab), labels):
        ns.plot.kde_2d(x, y, ax=ax, label=label, alpha=0.5)

    ax.set(xlabel=a.get_label(x), ylabel=a.get_label(y),
           xlim=(0.18, 0.50), ylim=(0.70, 1.00))
    ax.legend()
    return ax
