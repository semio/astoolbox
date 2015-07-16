#!/usr/bin/env python

# misc functions(data downloader, drawings etc.)

import pandas as pd
import numpy as np

def load_from_xueqiu(stock, start=None, end=None):
    """ load bars data from XueQiu """
    import requests
    from StringIO import StringIO
    link = "http://xueqiu.com/S/%s/historical.csv" % stock

    header = {
        "User-Agent" :
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
    }

    r = requests.get(link, headers=header)

    df = pd.DataFrame.from_csv(StringIO(r.content), index_col=1, parse_dates=True)

    if start:
        if end:
            return df[start:end]
        else:
            return df[start:]
    elif end:
        return df[:end]
    else:
        return df

def candlestick(ax, df, width=0.4, colorup='k', colordown='r',alpha=1.0):
    """ draw candle stick chart on an matplotlib axis """
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from matplotlib.dates import date2num
    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker

    OFFSET = width / 2.0

    low = df.low.values
    high = df.high.values
    op = df.open.values
    co = df.close.values
    t = df.index.to_pydatetime()
    tt = date2num(t)

    lines = []
    rects = []

    for i in range(len(tt)):

        if co[i] >= op[i]:
            color = colorup
            lower = op[i]
            height = co[i] - op[i]
        else:
            color = colordown
            lower = co[i]
            height = op[i] - co[i]

        vline = Line2D(
            xdata=(tt[i], tt[i]),
            ydata=(low[i], high[i]),
            color=color,
            linewidth=0.5,
            #antialiased=True,
        )
        vline.set_alpha(alpha)

        rect = Rectangle(
            xy=(tt[i] - OFFSET, lower),
            width = width,
            height = height,
            facecolor = color,
            edgecolor = color,
        )
        rect.set_alpha(alpha)

        lines.append(vline)
        rects.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    # end of for
    ax.autoscale_view()
    return lines, rects
