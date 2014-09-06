from location import *
import pandas as pd

def aspected(x, asp):
    if asp in [0, 180]:
        if (x[1] - x[0]) * (x[3] - x[2]) < 0 and x[2] > asp - 10 and x[2] < asp + 10 :
            return True
    else:
        if (x[0]-asp) * (x[1]-asp) < 0:
            return True

    return False

def aspect_list(planet1, planet2, start, end, aspect, scale=1):
    """ return a list of aspect made by 2 planets in given time span and aspect
        I only need the exact day so the calculation can be simplified
    """

    diffs = location_diff(planet1, planet2, start, end, freq='3H', scale=scale)

    #TODO: reimplement this because only 2 rows of data is needed to get list in Astrolog 5.4
    if aspect in [0, 180]:
        aspectlist = pd.rolling_apply(diffs, 4, lambda x: aspected(x, aspect))
    else:
        aspectlist = pd.rolling_apply(diffs, 2, lambda x: aspected(x, aspect))

    tindex = aspectlist[aspectlist==True].index

    res = pd.Series([aspect] * len(tindex), tindex)

    return res
