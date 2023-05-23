from suspiciousness.utils import stats
from scipy.stats import chi2


@stats
def logR(a, b, ab, show=False):
    logR = ab.logZ - a.logZ - b.logZ
    if show:
        print(f"logR = {logR.mean()} ± {logR.std()}")
    return logR


@stats
def logS(a, b, ab, show=False):
    logS = ab.logL_P - a.logL_P - b.logL_P
    if show:
        print(f"logS = {logS.mean()} ± {logS.std()}")
    return logS


@stats
def logI(a, b, ab, show=False):
    logI = a.D_KL + b.D_KL - ab.D_KL
    if show:
        print(f"logI = {logI.mean()} ± {logI.std()}")
    return logI


@stats
def bayesian_d(a, b, ab):
    return a.d_G + b.d_G - ab.d_G


@stats
def logp(a, b, ab, show=False):
    d = bayesian_d(a, b, ab)
    logp = chi2.logsf(d-2*logS(a, b, ab), d)
    if show:
        print(f"logp = {logp.mean()} ± {logp.std()}")
    return logp


@stats
def p(a, b, ab, show=False):
    d = bayesian_d(a, b, ab)
    p = chi2.sf(d-2*logS(a, b, ab), d)
    if show:
        print(f"p = {p.mean()} ± {p.std()}")
    return p
