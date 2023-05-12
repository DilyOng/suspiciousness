from functools import wraps
import anesthetic as ac


def samples(func):
    @wraps(func)
    def inner(*args, chains=None, **kwargs):
        if chains is None:
            return func(*args, **kwargs)
        args = tuple(ac.read_chains(f"{chains}/{a}/{a}_polychord_raw/{a}")
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
