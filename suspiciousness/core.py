from suspiciousness.utils import stats
from scipy.stats import chi2


@stats
def logR(a, b, ab, print=False):
    logR = ab.logZ - a.logZ - b.logZ
    if print:
        print(f"logR = {logR.mean()} ± {logR.std()}")
    return logR


@stats
def logS(a, b, ab, print=False):
    logS = ab.logL_P - a.logL_P - b.logL_P
    if print:
        print(f"logS = {logS.mean()} ± {logS.std()}")
    return logS


@stats
def logI(a, b, ab, print=False):
    logI = a.D_KL + b.D_KL - ab.D_KL
    if print:
        print(f"logI = {logI.mean()} ± {logI.std()}")
    return logI


@stats
def bayesian_d(a, b, ab):
    return a.d_G + b.d_G - ab.d_G


@stats
def logp(a, b, ab, print=False):
    d = bayesian_d(a, b, ab)
    logp = chi2.logsf(d-2*logS(a, b, ab), d)
    if print:
        print(f"logp = {logp.mean()} ± {logp.std()}")
    return logp
