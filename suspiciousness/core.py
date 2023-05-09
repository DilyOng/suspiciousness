from functools import wraps
import numpy as np
from scipy.stats import chi2
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


@stats
def logR(a, b, ab):
    logR = ab.logZ - a.logZ - b.logZ
    print(f"logR = {logR.mean()} ± {logR.std()}")
    return logR


@stats
def logS(a, b, ab):
    logS = ab.logL_P - a.logL_P - b.logL_P
    print(f"logS = {logS.mean()} ± {logS.std()}")
    return logS


@stats
def logI(a, b, ab):
    logI = a.D_KL + b.D_KL - ab.D_KL
    print(f"logI = {logI.mean()} ± {logI.std()}")
    return logI


@stats
def bayesian_d(a, b, ab):
    return a.d_G + b.d_G - ab.d_G


@stats
def logp(a, b, ab):
    d = bayesian_d(a, b, ab)
    logp = chi2.logsf(d-2*logS(a, b, ab), d)
    print(f"logp = {logp.mean()} ± {logp.std()}")
    return logp
