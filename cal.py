#!/usr/bin/env python

import astoolbox
import swisseph as swe
from datetime import datetime, timedelta
import icalendar as ic


def get_next(num=10, p1=swe.URANUS, p2=swe.SATURN, scale=24):
    '''return next aspects between 2 points'''
    asps1 = [0, 45, 90, 135, 180]
    # asps2 = [0, 30, 45, 60, 90, 135, 150, 120, 180]

    start = datetime.today() - timedelta(20)

    nx = astoolbox.aspect.next_aspect(p1, p2, asps=asps1, num=num,
                                      scale=scale, start=start, freq='6H')

    return nx


def make_cal(target, num=20):
    '''make a ical file
    :parameters:
    target: the target ical file to write
    num: total numbers of aspects.
    '''
    nx = get_next(num)
    cal = ic.Calendar()
    for k, v in nx.iteritems():
        dt = k.to_datetime()
        summary = "{}: URANvsSATU@24".format(v)

        ev = ic.Event()
        ev.add('dtstart', dt.date())
        ev.add('summary', summary)

        # alarm = ic.Alarm()
        # alarm.add('trigger', timedelta(hours=-12))
        # alarm.add('action', 'DISPLAY')
        # alarm.add('description', summary)

        # ev.add_component(alarm)
        cal.add_component(ev)

    with open(target, 'w') as f:
        f.write(cal.to_ical())
        f.close()
