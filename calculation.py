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
    """Calculate the locations of planet with in a time period.

        parameters:

        planet: the planet variable in swisseph
        start, end: the time span
        freq: the calculation freq
        scale: mulitply the planet location 

        return a pandas dataframe with planet location

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

def lat_to_text(lat):
    """return the text represetation of the location"""
    
    signs = ['Ari', 'Tau', 'Gem', 'Can',
             'Leo', 'Vir', 'Lib', 'Sco',
             'Sag', 'Cap', 'Aqu', 'Pis'
            ]

    unifiedLat = _fit360(lat)

    signum    = int(unifiedLat // 30)
    deg_float = unifiedLat % 30
    
    minutef, deg = math.modf(deg_float)
    
    minute = round(minutef * 60)
    
    string = str(int(deg)) + signs[signum] + str(int(minute))
    
    return string

#
def location_diff(planet1, planet2, start, end, freq="1D", scale=1):
    """Calculate the difference of location between 2 planets in given time span"""

    loc_planet1 = loc_of_planet(planet1, start, end, freq, scale, fit360=True)
    loc_planet2 = loc_of_planet(planet2, start, end, freq, scale, fit360=True)

    #name1 = swe.get_planet_name(planet1)
    #name2 = swe.get_planet_name(planet2)

    diff = abs(loc_planet1 - loc_planet2)

    fit180 = lambda x: 360 - x if x >= 180 else x

    return diff.apply(fit180)




