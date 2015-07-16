'''aspect related functions'''
from location import *
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def aspected(x):
    if x[0] * x[1] < 0 and abs(x[0] - x[1]) < 90:
        return True
    else:
        return False


def _sign(x):
    if x >= 0:
        return 1
    else:
        return -1


def aspect_list(planet1, planet2, start, end, aspect, freq='3H', scale=1):
    """ return a list of aspect made by 2 planets in given time span and aspect
        I only need the exact day so the calculation can be simplified

        modify freq to get different accurance
    """

    # we don't normalize the distance when calculating 0/180 degree.
    if aspect in [0, 180]:
        diffs = location_diff(planet1, planet2, start, end, freq,
                              scale=scale, fit180=False)
        # only search 180 degree aspect when distance bigger than 90 degree.
        if aspect == 180:
            diffs_new = diffs[abs(diffs) > 90].apply(
                lambda x: x - _sign(x) * 180)
        else:
            diffs_new = diffs
    # for other aspects
    else:
        diffs = location_diff(planet1, planet2, start, end, freq, scale=scale)
        # now we can treat all aspect like conjection
        diffs_new = diffs - aspect
    aspectlist = pd.rolling_apply(diffs_new, 2, aspected)
    tindex = aspectlist[aspectlist==True].index
    res = pd.Series([aspect] * len(tindex), tindex)

    return res


def aspect_list2(planet1, planet2, start, end, aspl, freq='3H', scale=1):
    """ Just another version of aspect_list but accept a list of aspects. """

    res = []
    for asp in aspl:
        t = aspect_list(planet1, planet2, start, end, asp, freq, scale=scale)
        res.append(t)
    n = pd.concat(res)
    return n.sort_index()


def next_aspect(planet1, planet2, asps=None,
                start=None, num=1, freq='3H', scale=1):
    """get next n aspects"""

    if not start:
        start = datetime.today()
    elif type(start) is str:
        start = pd.to_datetime(start)

    if not asps:
        asps = [0, 60, 90, 120, 180]
    step = timedelta(days=30)
    res  = pd.Series([])

    while len(res) < num:
        ne  = start + step
        asp = aspect_list2(planet1, planet2, start, ne, asps, freq, scale)
        if len(asp) >= 1:
            res = pd.concat([res, asp])
        start = ne

    return res.sort_index().head(num)

def previous_aspect(planet1, planet2, asps=None,
                start=None, num=1, freq='3H', scale=1):
    """get previous n aspects"""

    if not start:
        start = datetime.today()
    elif type(start) is str:
        start = pd.to_datetime(start)

    if not asps:
        asps = [0, 60, 90, 120, 180]
    step = timedelta(days=30)
    res  = pd.Series([])

    while len(res) < num:
        pr  = start - step
        asp = aspect_list2(planet1, planet2, pr, start, asps, freq, scale)
        if len(asp) >= 1:
            res = pd.concat([res, asp])
        start = pr

    return res.sort_index().head(num)

def revert(n):
    """return the remainder of the given aspect in the 360 cycle.
       e.g. revert(30) == 330
    """
    if n > 0 and n < 360:
        return 360 - n
    else :
        raise ValueError

def next_aspect_states(planet1, planet2, start=None,
                        num=1, asps=None, freq='3H', scale=1):
    """return aspect state changes(station/direction) of given planets
       within given time span.
    """
    if not start:
        start = datetime.today()
    elif type(start) is str:
        start = pd.to_datetime(start)
    if not asps:
        asps = [0, 60, 90, 120, 180]

    res = dict()
    # get last asp
    pre_asp = previous_aspect(planet1, planet2, start=start, asps=asps, freq=freq,
                                    scale=scale, num=1)

    while len(res) < num:
        next_asps = next_aspect(planet1, planet2, start=start, asps=asps,
                                num=10, freq=freq, scale=scale)

        asps_list = pd.concat([pre_asp, next_asps])
        stay_list = pd.rolling_apply(asps_list, 2, lambda xs: True if xs[0] == xs[1] else np.nan)
        stay_list = stay_list.dropna()
        for i in range(len(stay_list)):
            i0 = asps_list.index.get_loc(stay_list.index[i]) - 1
            i1 = i0 + 1
            res[asps_list.index[i0]] = -1
            res[asps_list.index[i1]] = 1

        pre_asp = asps_list[-1:]
        start = asps_list.index[-1]

    return pd.Series(res)
