import matplotlib.pyplot as plt
import smplotlib
from suspiciousness.utils import samples


@samples
def sigma8plot(*nestedsamples, ax=None, x="omegam", y="sigma8",
               plot_kwargs, **kwargs):
    """
    Create kde from *nestedsamples[x], *nestedsamples[y].

    *nestedsamples: anesthetic.NestedSamples

    ax: axis to plot on.

    x, y: str. axes to plot.

    plot_kwargs: dict. plot_args[nestedsamples.label]
                 are the kwargs for that plot.

    **kwargs: kwargs to pass to every plot.
    """
    if ax is None:
        _, ax = plt.subplots()

    for ns in nestedsamples:
        ns_kwargs = plot_kwargs.get(ns.label, {})
        if 'label' not in ns_kwargs:
            ns_kwargs['label'] = ns.label
        ns.plot.kde_2d(x, y, ax=ax, **ns_kwargs, **kwargs)

    ax.set(xlabel=nestedsamples[0].get_label(x),
           ylabel=nestedsamples[0].get_label(y),
           xlim=(0.18, 0.50), ylim=(0.70, 1.00))
    ax.legend()
    return ax


@samples
def cornerplot(axes, *nestedsamples, prior=False, plot_kwargs, **kwargs):
    """
    Create corner plot from *nestedsamples.

    axes: Pandas array of axes (output of anesthetic.make_2d_axes)

    *nestedsamples: anesthetic.NestedSamples

    prior: bool. Use nestedsamples[0].set_beta(0) to show the prior too.

    plot_kwargs: dict. plot_args[nestedsamples.label]
                 are the kwargs for that plot.

    **kwargs: kwargs to pass to every plot.
    """
    if prior:
        nestedsamples[0].set_beta(0).plot_2d(axes, alpha=0.25,
                                             color="blue", label="prior")

    for ns in nestedsamples:
        if 'tau' in ns:
            # required due to Cobaya update
            ns.set_label('tau', r'$\tau$')
        ns_kwargs = plot_kwargs.get(ns.label, {})
        ns.plot_2d(axes, **ns_kwargs, **kwargs)
    axes.iloc[1, 0].legend(loc=(3, 0.5))

    return axes
