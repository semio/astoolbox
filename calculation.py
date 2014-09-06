import pandas as pd
import swisseph as swe
import pytz
import numpy as np
import math


def _fit360(n):
    while n >= 360:
        n = n - 360

    return n
#

def loc_of_planet(planet, start, end, freq='1D', scale=1, fit360=False):
    """Calculate the locations of planet within a time span.

        parameters:

        planet: the planet variable in swisseph
        start, end: the time span
        freq: the calculation freq
        scale: mulitply the planet location 

        return a pandas Series with planet location

    """
    
    results = []
    drange = pd.date_range(start, end, freq=freq, tz='utc')
    
    for date in drange:
        year   = date.year
        month  = date.month
        day    = date.day
        hour   = date.hour
        minute = date.minute
        second = date.second
        
        jd = swe.utc_to_jd(year, month, day, hour, minute, second, 1)
        ut = jd[1]
        
        loc = swe.calc_ut(ut, planet)
        
        results.append(loc[0]*scale)
        
    res = pd.Series(results, drange, name=swe.get_planet_name(planet))
    
    if scale > 1 and fit360:
        return res.apply(_fit360)

    return res
#

def lon_to_text(lon):
    """return the text represetation of the location"""
    
    signs = ['Ari', 'Tau', 'Gem', 'Can',
             'Leo', 'Vir', 'Lib', 'Sco',
             'Sag', 'Cap', 'Aqu', 'Pis'
            ]

    unifiedLon = _fit360(lon)

    signum    = int(unifiedLon // 30)
    deg_float = unifiedLon % 30
    
    minutef, deg = math.modf(deg_float)
    
    minute = round(minutef * 60)
    
    string = str(int(deg)) + signs[signum] + str(int(minute))
    
    return string

#

def _fit180(n):
    if abs(n) >= 180:
        return 360 - abs(n)
    else: 
        return abs(n)

def location_diff(planet1, planet2, start, end, freq="1D", scale=1, fit180=False):
    """Calculate the difference of location between 2 planets in given time span"""

    loc_planet1 = loc_of_planet(planet1, start, end, freq, scale, fit360=True)
    loc_planet2 = loc_of_planet(planet2, start, end, freq, scale, fit360=True)

    #name1 = swe.get_planet_name(planet1)
    #name2 = swe.get_planet_name(planet2)

    diff = loc_planet1 - loc_planet2

    if fit180:
        return diff.apply(_fit180)

    return diff

#
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



