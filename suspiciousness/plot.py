import matplotlib.pyplot as plt
import smplotlib
from suspiciousness.core import samples


@samples
def sigma8plot(a, b, ab, labels=("a", "b", "ab"), ax=None, x="omegam", y="sigma8"):
    if ax is None:
        _, ax = plt.subplots()

    for ns, label, alpha in zip((a, b, ab), labels, (0.5, 0.5, 0.9)):
        ns.plot.kde_2d(x, y, ax=ax, label=label, alpha=alpha)

    ax.set(xlabel=a.get_label(x), ylabel=a.get_label(y),
           xlim=(0.18, 0.50), ylim=(0.70, 1.00))
    ax.legend()
    return ax


@samples
def cornerplot(a, b, ab, axes, labels=("a", "b", "ab")):
    for ns, label, alpha in zip((a, b, ab), labels, (0.5, 0.5, 0.9)):
        ns.plot_2d(axes, label=label, alpha=alpha)
    axes.iloc[1, 0].legend(loc=(3, 0.5))

    return axes
