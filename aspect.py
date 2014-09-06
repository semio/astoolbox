from location import *
import pandas as pd

def aspect_list(planet1, planet2, start, end, aspect, scale=1):
    """ return a list of aspect made by 2 planets in given time span and aspect
        I only need the exact day so the calculation can be simplified
    """

    #TODO: rewrite this because the lambda seems too long..
    if aspect in [0, 180]: 
        diffs = location_diff(planet1, planet2, start, end, freq='3H', scale=scale)
    else:
        diffs = location_diff(planet1, planet2, start, end, freq='3H', scale=scale, fit180=True)

    aspected = lambda x: True if (x[0]-aspect) * (x[1]-aspect) < 0 and x[1] > aspect - 10 and x[1] < aspect + 10 else False

    aspectlist = pd.rolling_apply(diffs, 2, aspected)

    tindex = aspectlist[aspectlist==True].index

    res = pd.Series([aspect] * len(tindex), tindex)

    return res
