from functools import wraps
import anesthetic as ac


def read_cobaya_chains(chains, name):
    return ac.reach_chains(f"{chains}/{name}/{name}_polychord_raw/{name}")


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
