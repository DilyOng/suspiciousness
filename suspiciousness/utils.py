from functools import wraps
import numpy as np
import anesthetic as ac


def read_cobaya_chains(chains, name):
    ns = ac.read_chains(f"{chains}/{name}/{name}_polychord_raw/{name}")
    if 'S8' not in ns and 'sigma8' in ns and 'omegam' in ns:
        ns['S8'] = ns.sigma8 * np.sqrt(ns.omegam / 0.3)
        ns.set_label('S8', '$S_8$')
    return ns


def samples(func):
    @wraps(func)
    def inner(*args, chains=None, **kwargs):
        if chains is None:
            return func(*args, **kwargs)
        args = tuple(read_cobaya_chains(chains, a)
                     if isinstance(a, str) else a for a in args)
        return func(*args, **kwargs)
    return inner


def stats(func):
    @wraps(func)
    @samples
    def inner(*args, nsamples=1000, **kwargs):
        args = tuple(a.stats(nsamples=nsamples)
                     if isinstance(a, ac.NestedSamples) else a for a in args)
        return func(*args, **kwargs)
    return inner
